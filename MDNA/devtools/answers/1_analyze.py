# Answers for 1_analyze.ipynb. `python devtools/make_solutions.py 1_analyze` builds solutions/1_analyze_solutions.ipynb
# from them. See devtools/make_solutions.py for the format.

# %% [markdown] after a6a0fcf7  (Load molecular dynamics data: ### Questions)
# **Answers**
#
# a. `TTGGCCCGCTGGTCGCCGCTATCGACAGGC`, 30 base pairs. `dna.describe()` prints it.
#
# b. 201 frames: see `Trajectory: <mdtraj.Trajectory with 201 frames ...>`, or the second number in `Frames: (30, 201, 4, 3)`.
#
# c. In the notebook, use `view(traj[0])`. In a viewer, load `dna.pdb` and `dna.xtc` and go to the first frame.

# %% after a6a0fcf7  (Load molecular dynamics data: ### Questions)
view(traj[0])

# %% replace 76c82558  (Extracting and Visualizing Rigid Base Parameters: for name in names: )
# a. All parameters in one figure. Each row pairs a base-pair parameter with the step parameter
# that describes the same motion between neighbouring base pairs (shear and shift, ..., opening and twist).
def plot_all_parameters(obj):
    fig = plt.figure(figsize=[12, 13], layout='constrained')
    groups = [('Base-pair parameters', ['shear', 'stretch', 'stagger', 'buckle', 'propeller', 'opening'], 'tab:blue'),
              ('Step parameters', ['shift', 'slide', 'rise', 'tilt', 'roll', 'twist'], 'tab:orange')]
    for column, (title, group, color) in zip(fig.subfigures(1, 2), groups):
        column.suptitle(title)
        axes = column.subplots(len(group), 1, sharex=True)
        for ax, name in zip(axes, group):
            plot_parameters(obj, name, ax=ax, color=color)
            ax.set_title('')
            ax.set_xlabel('')
        axes[-1].set_xlabel('Base pair' if title.startswith('Base') else 'Base pair step')

plot_all_parameters(dna)

# %% [markdown] after 76c82558  (Extracting and Visualizing Rigid Base Parameters: for name in names: )
# **Answers**
#
# a. See the figure above.
#
# b. The translational parameters are distances, in Å: shear, stretch and stagger (base pair) and shift, slide and rise (step). The rotational parameters are angles, in degrees: buckle, propeller and opening (base pair) and tilt, roll and twist (step).
#
# c. A step parameter describes how a base pair sits relative to the previous base pair. The first base pair has no previous base pair, so mdna fills this position with zeros.
#
# d. Two examples, away from the frayed ends of the duplex:
# - Opening: A-T pairs open more than G-C pairs (on average 3.8 vs 2.1 degrees) and fluctuate more (standard deviation 6.9 vs 5.0 degrees). An A-T pair has two hydrogen bonds, a G-C pair three.
# - Roll: pyrimidine-purine steps (CpG, CpA, TpG, TpA) have a larger roll (about +9 degrees) than purine-pyrimidine steps (about -4 degrees). Pyrimidine-purine steps are the most flexible steps in DNA.
#
# The base pairs at both ends fluctuate most of all: the ends of the duplex fray.

# %% replace fb8db742  (RNA: for name in names: )
plot_all_parameters(rna)

# %% [markdown] after fb8db742  (RNA: for name in names: )
# **Answers**
#
# a. `UAUGUACGACUGAAGCGAUU`, 20 base pairs.
#
# b. 201 frames.
#
# c. `view(traj[0])`, or load `rna.pdb` and `rna.xtc` in a viewer.
#
# d. See the figure above.
#
# e. As in DNA, A-U pairs open more than G-C pairs (on average 5.4 vs 2.4 degrees).
#
# f. Double-stranded RNA forms an A-form helix, DNA a B-form helix. Compared to the DNA trajectory (averages over the inner base pairs):
#
# | parameter | DNA | RNA |
# |---|---|---|
# | slide | -0.3 Å | -1.5 Å |
# | roll | 1.9° | 9.0° |
# | twist | 34.2° (10.5 bp per turn) | 30.5° (11.8 bp per turn) |
# | propeller | -10° | -15° |
# | rise | 3.3 Å | 3.3 Å |
#
# The rise per step is about the same. The A-form helix is still shorter per base pair along its axis, because the base pairs are tilted and pushed away from the helix axis. The distributions below show the same differences.
