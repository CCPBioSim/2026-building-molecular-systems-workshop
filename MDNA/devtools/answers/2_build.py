# Answers for 2_build.ipynb. `python devtools/make_solutions.py 2_build` builds solutions/2_build_solutions.ipynb
# from them. See devtools/make_solutions.py for the format.

# %% replace 0d6ed5d3  (Linear DNA Structure Generation: # Add length)
# Add length
length = [12, 24, 48]
for l in length:
    dna_l = mdna.make(n_bp=l)
    dna_l.describe()
    dna_l.save_pdb(f'./dna_length_{l}')
    print(f'{l} bp = {l / 10.5:.2f} turns\n')

# %% [markdown] after 0d6ed5d3  (Linear DNA Structure Generation: # Add length)
# B-DNA has 10.5 base pairs per turn. 12 bp is 1.14 turns (1 complete turn), 24 bp is 2.29 turns (2 complete turns) and 48 bp is 4.57 turns (4 complete turns).

# %% replace f519c3d3  (Linear DNA Structure Generation: #mutate the random sequence)
#mutate the random sequence
#get the sequence
dna.describe()

# swap every A for G and every G for A
swap = {'A': 'G', 'G': 'A'}
mutations = {i: swap[b] for i, b in enumerate(dna.sequence) if b in swap}

#perform the mutation
dna.mutate(mutations)

#check
dna.describe()

#visualize / save coordinates
dna.save_pdb('./random_20bp_mutated')

# %% after d51223cd  (Linear DNA Structure Generation: ### Do it yourself!)
# a. the structure with sequence GCGCGCGCGC (also saved as GCGCGCGCGC.pdb)
gcgc = mdna.make(sequence='GCGCGCGCGC')
view(gcgc)

# b. and c. are done in the cells above: describe() prints the random sequence,
# and the structures are saved as random_20bp.pdb and random_20bp_mutated.pdb
view(dna)

# d.
atcg = mdna.make(sequence='ATCGATCGATCGATCGATCG')
view(atcg)
atcg.save_pdb('./ATCGATCGATCGATCGATCG')

# %% [markdown] after 7250e35a  (Closed loops: ### Do it yourself!)
# **Answers**
#
# a. The ideal minicircle is a perfect circle. After minimization it is no longer perfectly round: the MC simulation runs at 300 K, so the circle shows thermal bending.
#
# b. Lk = Tw + Wr. With dLk = 0 almost all of the linking number is twist (Wr close to 0), and the circle stays roughly flat. With dLk = 8 the DNA has 8 extra turns. Right after building, all of these are twist (Lk = Tw = 27, Wr = 0). Overwinding costs elastic energy, so during minimization part of the extra twist turns into writhe: the circle bends out of its plane, which is supercoiling. Lk stays exactly 27, while Wr grows to about 2 and Tw drops by the same amount (the exact numbers vary between runs).
#
# Note: for a closed circle, Lk has to be a whole number. 200 bp at 10.5 bp per turn is 19.05 turns, so mdna adjusts the twist slightly to make exactly 19 turns. That is the "Excess twist per base to make ends meet" in the output of `make()`.

# %% after bc5871ad  (Knotted DNA: ### Do it yourself)
# figure-eight knot
control_points = np.array(parametric_figure_eight(np.linspace(0, 2 * np.pi, 50))).T
figure_eight = mdna.make(control_points=control_points, circular=True)
print(f'Number of base pairs is {figure_eight.n_bp} that fit along the spline.')
view(figure_eight)
figure_eight.save_pdb('./figure_eight_knot')

# cinquefoil knot, the (2, 5) torus knot
control_points = np.array(parametric_another_knot(np.linspace(0, 2 * np.pi, 100))).T
cinquefoil = mdna.make(control_points=control_points, circular=True)
print(f'Number of base pairs is {cinquefoil.n_bp} that fit along the spline.')
view(cinquefoil)
cinquefoil.save_pdb('./cinquefoil_knot')
