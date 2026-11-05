"""Workarounds for known issues in mdna 0.2.0, used by the workshop notebooks.

Import this module before mdna:

    import devtools.mdna_workarounds
    import mdna

Every patch only applies to mdna 0.2.0, so with a newer mdna this module does nothing.
Once mdna is updated, the import can be removed from the notebooks.
"""
import contextlib
import io
import warnings
from importlib.metadata import version

import mdtraj as md
import numpy as np
from scipy.spatial.transform import Rotation

# mdna warns at import that an optional compiled speed-up (Cython) is missing; the fallback works fine.
warnings.filterwarnings('ignore', message='Cython version of .* not compiled')
# The convergence check of the MC minimization fits a curve, which can overflow or fail to estimate its
# uncertainty; the result of the minimization is not affected.
warnings.filterwarnings('ignore', message='overflow encountered in exp', category=RuntimeWarning, module='mdna')
warnings.filterwarnings('ignore', message='Covariance of the parameters could not be estimated', module='mdna')

import mdna  # noqa: E402

PATCHED_VERSION = '0.2.0'


def _silent(*args, **kwargs):
    pass


def _with_partners(dna, mutations):
    """The mutations plus the matching mutations of their partner bases, as mutate(complementary=True) intends."""
    partner = {}
    for a, b in utils.get_base_pair_dict(dna.traj).items():
        partner[a.index], partner[b.index] = b.index, a.index
    added = {partner[index]: dna.base_pair_map[base] for index, base in mutations.items()}
    return {**added, **mutations}


def _mutate(self, mutations=None, complementary=True, frame=-1, verbose=False):
    # mutate() prints debug output, and leaves the atom numbering of the topology out of sync
    # with the coordinates, so get_frames(), draw() and get_parameters() fail afterwards.
    # With complementary=True it also raises a KeyError for a base on the complementary strand, because it only
    # looks up the partners of the leading strand, so the partner mutations are added here instead.
    if self.traj is None:
        self._frames_to_traj()
    if mutations is not None and complementary:
        mutations, complementary = _with_partners(self, mutations), False
    output = contextlib.nullcontext() if verbose else contextlib.redirect_stdout(io.StringIO())
    with output:
        _original_mutate(self, mutations=mutations, complementary=complementary, frame=frame, verbose=verbose)
    for index, atom in enumerate(self.traj.top.atoms):
        atom.index = index


def _adjust_for_circular(self):
    # Same as mdna 0.2.0, but rounds the number of turns to the nearest whole number instead of
    # always rounding up, which overwound "relaxed" circles by up to one turn (Lk 20 instead of 19 for 200 bp)
    total_twist = np.sum(self.twists)
    needed_twist = np.round(total_twist / 360) * 360
    adjustment = (needed_twist - total_twist) / self.n_bp

    self.twist_angle = self.twist_angle + adjustment
    self.twists += adjustment
    self.accumulated_twists = np.cumsum(self.twists) - self.twist_angle

    print(f"Structure is requested to be circular:\n\tExcess twist per base to make ends meet: {self.twist_angle - (360 / self.bp_per_turn):.2f} degrees\n\tNew twist angle per base pair:", np.round(self.twist_angle, 2), '\n')


def _scale_to_nbp(self):
    # Same as mdna 0.2.0, but scales the control points around their centroid instead of around the origin.
    # Otherwise a design away from the origin moves off its own spline when n_bp does not fit its length.
    target_bp = self.n_bp if self.closed else self.n_bp - 1
    ratio = target_bp * self.frame_spacing / self.arc_length[-1]
    control_points = np.asarray(self.control_points, dtype=float)
    centroid = control_points.mean(axis=0)
    self.update_control_points(centroid + (control_points - centroid) * ratio)

    if self.frames.shape[0] == self.n_bp:
        print(f"\tSpline scaled to match the target number of base pairs: {self.n_bp}\n")
    else:
        print(f"\tError: Spline could not be scaled to match the target number of base pairs: {target_bp}")
        print("\tNew number of base pairs:", self.frames.shape[0])


def _make(*args, **kwargs):
    # A circular structure only closes when the first and last control point are the same
    control_points = kwargs.get('control_points')
    circular = kwargs.get('circular') or kwargs.get('closed')
    if circular and control_points is not None and not np.allclose(control_points[0], control_points[-1]):
        warnings.warn('circular=True, but the first and last control points differ: the DNA will not close. '
                      'Add the first point again at the end.', stacklevel=2)
    return _original_make(*args, **kwargs)


def _is_rna(sequence):
    return 'U' in sequence and 'T' not in sequence


def _load(*args, circular=None, **kwargs):
    # load() ignores its circular argument, and its base_pair_map pairs A with T, also in RNA
    nucleic = _original_load(*args, **kwargs)
    if circular is not None:
        nucleic.circular = circular
    if _is_rna(nucleic.sequence):
        nucleic.base_pair_map = {**nucleic.base_pair_map, 'A': 'U'}
    return nucleic


def _straight_linker(connector, index=0):
    # mdna 0.2.0 wraps the twist difference between the two ends wrongly, so it often picks a whole number of
    # turns regardless of the gap (42 bp between two pieces of one straight DNA, whether they are 2 or 7 nm apart).
    # It also squeezes the linker into the gap, and its spline scaling moves the linker away from the two ends.
    # Here the linker runs straight from one end to the other.
    start, end = connector.start, connector.end
    direction = end[0] - start[0]
    distance = np.linalg.norm(direction)
    direction /= distance

    # Turn both end frames so their helix axis (the last axis) points along the linker, then measure the twist between them
    axes_start = Rotation.align_vectors([direction], [start[3]])[0].apply(start[1:])
    axes_end = Rotation.align_vectors([direction], [end[3]])[0].apply(end[1:])
    twist = np.degrees(np.arctan2(np.cross(axes_start[0], axes_end[0]) @ direction, axes_start[0] @ axes_end[0]))
    step_twist = 360 / 10.5

    if connector.n_bp is None:
        # Smallest number of base pairs that spans the gap and leaves little twist to absorb, as mdna intends
        min_bp = max(1, int(np.round(distance / 0.34)) - 1)
        n_bp = np.arange(min_bp, min_bp + 1000)
        mismatch = np.abs(((n_bp + 1) * step_twist - twist + 180) % 360 - 180)
        options = [n for i, n in enumerate(n_bp[:-1]) if (i == 0 or mismatch[i - 1] > mismatch[i]) and mismatch[i] < mismatch[i + 1]
                   and mismatch[i] / (n + 1) < connector.twist_tolerance]
        connector.n_bp = int(options[index])
        print(f'Optimal number of base pairs: {connector.n_bp}')

    # Spread the twist evenly over the steps, adding whole turns until it is closest to B-DNA
    n_steps = connector.n_bp + 1
    total_twist = twist + 360 * np.round((n_steps * step_twist - twist) / 360)
    linker = []
    for i in range(1, n_steps):
        rotation = Rotation.from_rotvec(np.radians(i * total_twist / n_steps) * direction)
        linker.append(np.vstack([start[0] + i / n_steps * (end[0] - start[0]), rotation.apply(axes_start)]))
    return np.array(linker)


def _connect(self, index=0, control_points=None):
    # Same as mdna 0.2.0, but with a working straight linker. With control points, mdna 0.2.0 also prints an
    # 'Optimal BP' that it does not use: the number of base pairs follows from the length of the curve.
    self.start, self.end = self._get_start_and_end()
    if control_points is None:
        linker = _straight_linker(self, index)
    else:
        linker = nucleic.SplineFrames(control_points=control_points, frame_spacing=0.34, initial_frame=self.start).frames[1:-1]
    frames = np.concatenate([self.frames0, linker, self.frames1])

    fixed_0 = list(range(self.frames0.shape[0] - self.margin))
    fixed_1 = list(range(frames.shape[0] - self.frames1.shape[0] + self.margin, frames.shape[0]))
    self.fixed = fixed_0 + fixed_1

    self.sequence, self.n_bp = nucleic._check_input(sequence=self.sequence, n_bp=len(linker))
    return nucleic.Nucleic(sequence=self.Nucleic0.sequence + self.sequence + self.Nucleic1.sequence, frames=frames)


def _get_linking_number(self, frame=-1):
    # The Gauss integral divides by zero when two pieces of the strands lie exactly in one plane, which can happen
    # in a perfectly symmetric circle such as mdna.make(n_bp=200, circular=True). The linking number does not
    # change when the base pairs move a tiny bit, so then try again with them moved by at most 1e-6 nm.
    try:
        return _original_get_linking_number(self, frame)
    except ZeroDivisionError:
        frames = self.frames
        self.frames = frames.copy()
        self.frames[:, :, 0] += 1e-6 * np.sin(np.arange(frames.shape[0] * 3)).reshape(-1, 1, 3)
        try:
            return _original_get_linking_number(self, frame)
        finally:
            self.frames = frames


def _sequence_to_md(sequence=None, time=10, time_unit='picoseconds', temperature=310, solvated=False, filename='my_dna',
                    save=True, output='GROMACS', shape=None, n_bp=None, circular=False, dLk=None, save_location='./'):
    # Same as mdna 0.2.0, with two fixes. A solvated system sits in a periodic box, so it needs PME instead of
    # CutoffNonPeriodic. And a 2 fs time step needs constraints on the bonds to hydrogen (constraints=app.HBonds).
    try:
        import openmm as mm
        from openmm import app, unit
        from mdtraj.reporters import HDF5Reporter
    except ImportError:
        return _original_sequence_to_md(sequence=sequence, filename=filename, shape=shape, n_bp=n_bp, circular=circular,
                                        dLk=dLk, save_location=save_location)  # prints that OpenMM is missing

    if filename is None:
        filename = sequence
    pdb = nucleic.sequence_to_pdb(sequence=sequence, filename=f'{save_location}{filename}', save=True, output='GROMACS',
                                  shape=shape, n_bp=n_bp, circular=circular, dLk=dLk)
    if time_unit not in ('picoseconds', 'nanoseconds'):
        raise ValueError("time_unit should be 'picoseconds' or 'nanoseconds'")
    simulation_time = time * getattr(unit, time_unit)
    time_step = 2 * unit.femtoseconds
    temperature = temperature * unit.kelvin
    steps = int(simulation_time / time_step)

    print(f'Initialize DNA openMM simulation at {temperature._value} K for', simulation_time, 'time units')
    modeller = app.Modeller(pdb.topology.to_openmm(), pdb.xyz[0])
    forcefield = app.ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
    modeller.addHydrogens(forcefield)
    if solvated:
        print('Solvate DNA with padding of 1.0 nm and 0.1 M KCl')
        modeller.addSolvent(forcefield, padding=1.0 * unit.nanometers, ionicStrength=0.1 * unit.molar, positiveIon='K+')

    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME if solvated else app.CutoffNonPeriodic,
                                     constraints=app.HBonds)
    integrator = mm.LangevinIntegrator(temperature, 1.0 / unit.picoseconds, time_step)
    simulation = app.Simulation(modeller.topology, system, integrator)
    simulation.context.setPositions(modeller.positions)
    simulation.reporters.append(HDF5Reporter(f'{save_location}{filename}.h5', 100))
    simulation.reporters.append(app.StateDataReporter(f'{save_location}/output_{filename}.csv', 100, step=True,
                                                      potentialEnergy=True, temperature=True, speed=True))
    print('Minimize energy')
    simulation.minimizeEnergy()
    print('Run simulation for', steps, 'steps')
    simulation.step(steps)
    simulation.reporters[0].close()
    print('Simulation completed')
    print('Saved trajectory as:', f'{save_location}{filename}.h5')
    return md.load_hdf5(f'{save_location}{filename}.h5')


def _describe(self):
    # describe() calls every structure DNA, also RNA
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        _original_describe(self)
    text = buffer.getvalue()
    if _is_rna(self.sequence):
        text = text.replace('DNA structure', 'RNA structure', 1)
    print(text, end='')


if version('mdna') == PATCHED_VERSION:
    from mdna import nucleic, spline, utils
    from mdna.simulate.Evals.PyLk.pylk import eval_link

    _original_mutate = nucleic.Nucleic.mutate
    _original_make = mdna.make
    _original_load = mdna.load
    _original_describe = nucleic.Nucleic.describe
    _original_get_linking_number = nucleic.Nucleic.get_linking_number
    _original_sequence_to_md = nucleic.sequence_to_md

    nucleic.Nucleic.mutate = _mutate
    nucleic.Nucleic.describe = _describe
    nucleic.Nucleic.get_linking_number = _get_linking_number
    nucleic.Connector.connect = _connect
    spline.Twister.adjust_for_circular = _adjust_for_circular
    spline.SplineFrames._scale_to_nbp = _scale_to_nbp
    mdna.make = _make
    mdna.load = _load
    mdna.sequence_to_md = nucleic.sequence_to_md = _sequence_to_md
    eval_link.print = _silent  # get_linking_number() prints 'using numba' every time
