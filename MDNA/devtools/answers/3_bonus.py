# Answers for 3_bonus.ipynb. `python devtools/make_solutions.py 3_bonus` builds solutions/3_bonus_solutions.ipynb
# from them. See devtools/make_solutions.py for the format.

# %% replace 8169e134  (1. A nucleosome with linker DNA: # your code here)
# a. period of the roll, from a Fourier transform (leave out the first step, which is always 0)
spectrum = np.abs(np.fft.rfft(roll[1:] - roll[1:].mean()))
frequencies = np.fft.rfftfreq(len(roll) - 1)
print(f'period of the roll: {1 / frequencies[1:][spectrum[1:].argmax()]:.1f} bp')

# %% after 8169e134  (1. A nucleosome with linker DNA: # your code here)
# b.
twist = params[0, 1:, names.index('twist')]
print(f'mean twist {twist.mean():.1f} degrees, {360 / twist.mean():.2f} bp per turn')

# %% after 8169e134  (1. A nucleosome with linker DNA: # your code here)
# c.
nucleosome_A = mdna.load(pdb, chainids=[0, 1])
nucleosome_A.extend(sequence='A'*30, exvol_rad=0)
nucleosome_A.describe()

# %% after 8169e134  (1. A nucleosome with linker DNA: # your code here)
# d. histone atoms within 0.2 nm of the linker DNA (the first and last 30 nucleotides of both strands)
n = nucleosome.n_bp
linker = [a.index for a in complex_traj.top.atoms
          if a.residue.chain.index in (0, 1) and (a.residue.index % n < 30 or a.residue.index % n >= n - 30)]
protein = complex_traj.top.select('protein')
close = md.compute_neighbors(complex_traj, 0.2, np.array(linker), haystack_indices=protein)[0]
print(f'{len(close)} histone atoms within 0.2 nm of the linkers')
print(sorted({f'chain {complex_traj.top.atom(i).residue.chain.index} {complex_traj.top.atom(i).residue}' for i in close}))

# %% after 8169e134  (1. A nucleosome with linker DNA: # your code here)
# e. three starting structures; compare the distance between the two ends of the DNA
for i in range(3):
    replica = mdna.load(pdb, chainids=[0, 1])
    replica.extend(n_bp=30, exvol_rad=0)
    replica.extend(n_bp=30, exvol_rad=0, forward=False)
    replica.get_traj().stack(histones).save_pdb(f'./nucleosome_replica_{i}.pdb')
    ends = replica.get_frames()[[0, -1], -1, 0]
    print(f'replica {i}: the two ends of the DNA are {np.linalg.norm(ends[0] - ends[1]):.1f} nm apart')

# %% [markdown] after 8169e134  (1. A nucleosome with linker DNA: # your code here)
# **Answers**
#
# a. The roll oscillates with a period of about 10.4 bp, one helical turn. Each turn, the major groove faces the histones once (positive roll, the DNA bends towards the major groove) and the minor groove faces the histones once (negative roll). Adding up these small bends wraps the DNA around the histones.
#
# b. The mean twist is about 34.6 degrees, 10.4 bp per turn: slightly more twisted than ideal B-DNA (10.5 bp per turn).
#
# c. See the code above.
#
# d. Yes, a few atoms. In our runs the new linkers ran into the N-terminal tail of histone H3 (chain 6, residues 14 to 33) and sometimes the C-terminal tail of histone H2A (chain 4). The exact contacts vary, because the linkers are minimized with MC. Histone tails are flexible and stick out of the core of the nucleosome. Before MD, you would move the tails or minimize the whole complex carefully, for example with restraints on the DNA.
#
# e. The distance between the two ends of the DNA differs by several nm between the replicas: each linker is a different thermal conformation at 300 K. Starting replicas from different structures makes them more independent than starting them all from the same structure.

# %% replace 7637acfa  (2. Connecting DNA: # your code here)
# a. see the output above

# b.
moved = frames[24:].copy()
moved[:, 0] += [1, 0, 0]
moved_right = mdna.load(frames=moved, sequence=dna.sequence[24:])
joined_moved = mdna.connect(left, moved_right)
linker_shape(joined_moved, left, moved_right)

# %% after 7637acfa  (2. Connecting DNA: # your code here)
# c.
for n_bp in [12, 13, 14, 15, 16, 17]:
    joined_n = mdna.connect(left, moved_right, n_bp=n_bp)
    linker_shape(joined_n, left, moved_right)

# %% [markdown] after 7637acfa  (2. Connecting DNA: # your code here)
# **Answers**
#
# a. 12 bp, exactly the number you cut out. The gap is 13 base-pair steps long, and with 12 new base pairs the twist also matches both ends. The rise and twist of the new DNA are close to B-DNA (3.4 Å and 34.3 degrees), but vary from step to step, because the MC minimization runs at 300 K.
#
# b. 33 bp, although about 15 bp would fit the 5.4 nm gap. `connect()` takes the smallest number of base pairs that spans the gap and whose twist matches both ends within 0.65 degrees per step. You moved the right piece without turning it, so the twist no longer fits 15 bp, and the first number that fits is two helical turns later. The 33 bp are squeezed into the gap: in our runs the rise stayed between 1.7 and 2.8 Å after the minimization, which cannot fix this because both ends are held in place. Not a good model: always check the new DNA, or choose the number of base pairs yourself.
#
# c. Fewer base pairs stretch the new DNA, more squeeze it, and the twist changes with the number. With 12 bp the twist is right (about 34 degrees) but the rise is 4.0 Å; with 15 bp the rise is right (3.4 Å) but the DNA is underwound (about 28 degrees). No number fits both, because the right piece moved without turning. A compromise such as 14 or 15 bp is a reasonable start for MD, which relaxes the rest.

# %% replace a8cb4818  (2. Connecting DNA: # your code here)
# a.
for height in [10, 15, 20]:
    control_points = np.array([start, start + 3 * away, middle + height * away, end + 3 * away, end])
    loop_h = mdna.connect(dna_a, dna_b, control_points=control_points)
    print(f'height {height} nm: {loop_h.n_bp - dna_a.n_bp - dna_b.n_bp} bp in the loop\n')

# %% after a8cb4818  (2. Connecting DNA: # your code here)
# b.
straight = mdna.connect(dna_a, dna_b)
linker_shape(straight, dna_a, dna_b)

# %% after a8cb4818  (2. Connecting DNA: # your code here)
# c.
dna_atoms = np.arange(protein.n_atoms, complex_loop.n_atoms)
protein_atoms = np.arange(protein.n_atoms)
close_protein = md.compute_neighbors(complex_loop, 0.2, dna_atoms, haystack_indices=protein_atoms)[0]
close_dna = md.compute_neighbors(complex_loop, 0.2, protein_atoms, haystack_indices=dna_atoms)[0]
print(f'{len(close_protein)} protein atoms within 0.2 nm of the DNA')
print('nucleotides involved:', sorted({str(complex_loop.top.atom(i).residue) for i in close_dna}))

crystal = md.compute_neighbors(foxp3, 0.2, foxp3.top.select('not protein'), haystack_indices=foxp3.top.select('protein'))[0]
print(f'crystal structure: {len(crystal)} protein atoms within 0.2 nm of the DNA')

# %% [markdown] after a8cb4818  (2. Connecting DNA: # your code here)
# **Answers**
#
# a. With `height = 15` the loop has about 90 bp; in our runs 10 nm gave about 60 bp and 20 nm about 120 bp. With control points, `connect()` takes the number of base pairs from the length of the curve through them. The minimization then spreads any mismatch in twist over the loop.
#
# b. 20 bp. About 15 bp would span the 5.2 nm gap, but their twist does not match both ends; 20 bp is the first number that does. On a straight line they would have a rise of only 2.5 Å, so during the minimization the new DNA stays compressed or bends sideways. With control points you choose the path, the number of base pairs follows from its length, and a loop is long enough to spread any twist mismatch over many base pairs. That is why a loop is the better way to connect these two duplexes.
#
# c. About a dozen protein atoms come within 0.2 nm, and they touch a few nucleotides of the original duplexes, not the new loop. In the crystal structure nothing is that close. mdna rebuilds every nucleotide from ideal templates placed on the base-pair frames, also the nucleotides that were already in the crystal structure, so small overlaps appear where the protein binds. Energy minimization with the force field removes them. Alternatively, keep the crystal coordinates of the bound DNA and use mdna only for the new loop.

# %% replace 4e442984  (3. Modifications your force field may not know: # your code here)
# a.
print(sorted({residue.name for residue in dna.get_traj().top.residues}))

# %% after 4e442984  (3. Modifications your force field may not know: # your code here)
# c.
def c1_distance(obj, bp):
    """Distance (nm) between the C1' atoms of base pair bp."""
    traj = obj.get_traj()
    partner = 2 * obj.n_bp - 1 - bp   # index of the partner nucleotide on the other strand
    a = traj.top.select(f"resid {bp} and name \"C1'\"")[0]
    b = traj.top.select(f"resid {partner} and name \"C1'\"")[0]
    return md.compute_distances(traj, [[a, b]])[0, 0]

print(f"C1'-C1': Watson-Crick {c1_distance(watson_crick, 5):.2f} nm, Hoogsteen {c1_distance(hoogsteen, 5):.2f} nm")

# %% after 4e442984  (3. Modifications your force field may not know: # your code here)
# d.
for sequence in ['GCGAEAGCG', 'GCBSPZGC']:
    obj = mdna.make(sequence=sequence)
    print(sequence, sorted({residue.name for residue in obj.get_traj().top.residues}))

# %% [markdown] after 4e442984  (3. Modifications your force field may not know: # your code here)
# **Answers**
#
# a. `DCM`. Standard nucleic-acid force fields contain parameters for A, C, G and T (and U for RNA) only. Parameters for 5-methylcytosine have been published for the common force fields, but you usually have to add them yourself.
#
# b. Opening changes by 180 degrees, because the base is rotated half a turn and its reference frame rotates with it. Shear and stretch change too (to about 4.8 and -3.4 Å), because the reference point of the flipped base moves. The other parameters stay the same, since only one base moves.
#
# c. mdna only rotates the base: the C1'-C1' distance stays at 1.08 nm in both structures. In a real Hoogsteen pair the backbones come closer. In a simulation setup the structure has to relax into this geometry during minimization and equilibration, possibly with restraints that keep the Hoogsteen hydrogen bonds intact.
#
# d. 2-aminopurine is `DE`. The Hachimoji bases are `DB`, `DS`, `DP` and `DZ`. None of these are in standard force fields.

# %% replace 1165bd6e  (4. Supercoiled minicircles: # your code here)
# a.
for dLk, (lk, wr, tw) in zip(dLk_values, results):
    if dLk != 0:
        print(f'dLk = {dLk:2d}: Wr = {wr:.2f}, so {100 * wr / dLk:.0f}% of dLk went into writhe')

# %% after 1165bd6e  (4. Supercoiled minicircles: # your code here)
# c.
lk0 = 200 / 10.5
print(f'Lk0 = {lk0:.2f}; sigma = -0.06 means dLk = {-0.06 * lk0:.1f}')
print('sigma of the values used here:', np.round(np.array(dLk_values) / lk0, 2))

# %% after 1165bd6e  (4. Supercoiled minicircles: # your code here)
# d. (takes about 2 minutes)
for dLk in [-4, -8]:
    circle = mdna.make(n_bp=200, circular=True, dLk=dLk)
    circle.minimize(equilibrate_writhe=True)
    print(f'dLk = {dLk}: [Lk, Wr, Tw] =', np.round(circle.get_linking_number(), 2))

# %% [markdown] after 1165bd6e  (4. Supercoiled minicircles: # your code here)
# **Answers** (the exact numbers vary between runs)
#
# a. Roughly 20 to 40%, and less for larger dLk; the rest stays as twist. The exact numbers vary between runs, because the minimization runs at 300 K. Writhe grows with dLk, but more slowly than dLk itself.
#
# b. At dLk = 0 the circle stays roughly flat. At dLk = 4 it already bends clearly out of its plane. At larger dLk the DNA winds further around itself, so the writhe keeps growing.
#
# c. Lk0 = 19.05, so σ = -0.06 is dLk ≈ -1.1. The values used here are σ = 0.2 to 0.6, far beyond what cells reach. A 200 bp circle is short and stiff: bending it into a supercoil costs a lot of energy, so it only writhes when it is strongly overwound. Plasmids of thousands of base pairs writhe at much smaller σ.
#
# d. Wr becomes negative, with about the same size as for the same positive dLk (compare with the output of question a; the numbers vary between runs). In this elastic model the response is roughly symmetric. Real DNA responds differently to underwinding than to overwinding: it can open base pairs or form other structures, which an elastic model of rigid base pairs cannot describe.
#
# e. The movie starts from the flat, overwound circle (Wr = 0). Early in the simulation the circle bends out of its plane and the writhe jumps to about 3; after that it only fluctuates. The linking number stays the same in every frame.

# %% replace e04a25cc  (5. Interlocked DNA rings: # your code here)
# a.
points_far = ring(radius, center=[2.5 * radius, 0, 0], plane='xz')
print('a. moved ring:', round(linking_number(points1, points_far), 2))

# b.
print('b. reversed ring:', round(linking_number(points1, points2[::-1]), 2))

# %% after e04a25cc  (5. Interlocked DNA rings: # your code here)
# c.
chain_points = [ring(radius, center=[1.5 * i * radius, 0, 0], plane='xy' if i % 2 == 0 else 'xz') for i in range(5)]
chain_rings = [mdna.make(control_points=points, circular=True) for points in chain_points]

chain_traj = chain_rings[0].get_traj()
for r in chain_rings[1:]:
    chain_traj = chain_traj.stack(r.get_traj())
chain_traj.save_pdb('./ring_chain.pdb')

lk = np.array([[linking_number(p, q) if i != j else 0 for j, q in enumerate(chain_points)] for i, p in enumerate(chain_points)])
print(np.round(lk).astype(int))

# %% [markdown] after e04a25cc  (5. Interlocked DNA rings: # your code here)
# **Answers**
#
# a. 0: the rings are no longer linked.
#
# b. The linking number changes sign, from -1 to +1. The sign depends on the direction of the curves. For DNA, the direction is the 5' to 3' direction of the strands.
#
# c. Each ring is linked to its neighbours (linking number +1 or -1) and not to the other rings (0).
#
# d. By 1. Look at the two rings from one direction and count the points where one ring crosses over the other: the linking number is half the sum of the signs (+1 or -1) of these crossings. Passing one ring through the other turns one crossing into its mirror image, which changes the sum by 2 and the linking number by 1. (Within a single circular DNA, topoisomerase II changes Lk by 2 per step, because it passes a double strand through a double strand.)

# %% replace 81ffd2c5  (6. Before you simulate: # your code here)
# b.
for scaling in [3, 2, 1.5]:
    knot = mdna.make(control_points=np.array(parametric_trefoil(t, scaling=scaling)).T, circular=True)
    print(f'scaling {scaling}: {knot.n_bp} bp, closest approach {closest_approach(knot):.2f} nm')

# %% after 81ffd2c5  (6. Before you simulate: # your code here)
# c.
system_size(mdna.make(n_bp=200))
system_size(mdna.make(n_bp=200, circular=True))

# %% [markdown] after 81ffd2c5  (6. Before you simulate: # your code here)
# **Answers**
#
# a. A circular DNA has no 5' ends: the phosphate of the first nucleotide connects it to the last nucleotide of the strand. Removing it would cut the circle open.
#
# b. At `scaling=2` the closest approach is about 2.4 nm, at `scaling=1.5` about 1.8 nm. Below roughly 1.7 the DNA overlaps itself.
#
# c. The straight 200 bp DNA is 68 nm long, so a cubic box around it is 70 nm wide: about 11 million waters and 35 million atoms. The minicircle fits in a 26 nm box: about 0.6 million waters and 1.7 million atoms, 20 times fewer. For long linear DNA you can use a rectangular box with the DNA along its long axis, or connect the DNA to its own periodic copy through the wall of the box, which models an infinitely long DNA.
