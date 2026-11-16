"""Show DNA structures and trajectories in 3D inside a notebook, with Mol* (molstar.org).

    from devtools.viewer import view
    view(dna)     # a structure made or loaded with mdna
    view(traj)    # an mdtraj trajectory; with more than one frame it plays as a movie

Mol* is loaded from the internet, so this needs a connection.
"""
import itertools
import string
import tempfile

import numpy as np
import molviewspec as mvs

MOLSTAR_VERSION = '5.13.1'  # a fixed version, so the viewer looks the same throughout the workshop
STRAND_COLORS = ['#e8a33d', '#3d84c6']  # DNA and RNA strands take turns: orange and blue
PROTEIN_COLOR = '#b4bcc8'
CHAIN_IDS = string.ascii_uppercase + string.ascii_lowercase + string.digits


def _file_contents(traj, extension):
    with tempfile.TemporaryDirectory() as folder:
        traj.save(f'{folder}/structure.{extension}')
        with open(f'{folder}/structure.{extension}', 'rb') as file:
            return file.read()


def view(structure, representation='cartoon', max_frames=100, width=900, height=500):
    """Show an mdna structure or an mdtraj trajectory in Mol*.

    DNA and RNA strands are orange and blue, proteins grey; water and ions are left out.
    representation: 'cartoon', 'ball_and_stick', 'spacefill' or 'surface'.
    A trajectory longer than max_frames frames is shown with every n-th frame, to keep the notebook small.
    """
    traj = structure.get_traj() if hasattr(structure, 'get_traj') else structure
    if traj.n_frames > max_frames:
        stride = int(np.ceil(traj.n_frames / max_frames))
        traj = traj[::stride]
        print(f'Showing 1 of every {stride} frames ({traj.n_frames} frames).')

    # Leave out water and ions, and give every chain its own chain id, so that each strand gets its own colour
    chains = [chain for chain in traj.topology.chains
              if not all(residue.is_water or residue.n_atoms == 1 for residue in chain.residues)]
    traj = traj.atom_slice([atom.index for chain in chains for atom in chain.atoms])
    for chain, chain_id in zip(traj.topology.chains, itertools.cycle(CHAIN_IDS)):
        chain.chain_id = chain_id

    builder = mvs.create_builder()
    builder.canvas(background_color='white')
    data = {'structure.pdb': _file_contents(traj[0], 'pdb')}
    if traj.n_frames > 1:
        data['frames.xtc'] = _file_contents(traj, 'xtc')
        builder.download(url='frames.xtc').parse(format='xtc').coordinates(ref='frames')
        model = builder.download(url='structure.pdb').parse(format='pdb').model_structure(coordinates_ref='frames')
    else:
        model = builder.download(url='structure.pdb').parse(format='pdb').model_structure()

    strands = itertools.cycle(STRAND_COLORS)
    for chain in traj.topology.chains:
        color = PROTEIN_COLOR if any(residue.is_protein for residue in chain.residues) else next(strands)
        selection = mvs.ComponentExpression(auth_asym_id=chain.chain_id)
        model.component(selector=selection).representation(type=representation).color(color=color)

    builder.molstar_notebook(data=data, width=width, height=height, molstar_version=MOLSTAR_VERSION)
