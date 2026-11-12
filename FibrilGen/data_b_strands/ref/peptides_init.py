import os
abspath = os.path.abspath('')
import sys
sys.path.append(f'{abspath}/../../fibrilgen_local/')

from seq2pep import *

## Create a b-strand structure
# Initialize the first example b-strand
get_b_strand('FEFKFEFK')
# Align bulky residues on the cross-section
set_chi_angle(1,'n','ca','cb','cg',-20)
set_chi_angle(3,'n','ca','cb','cg',-20)
set_chi_angle(5,'n','ca','cb','cg',-20)
set_chi_angle(7,'n','ca','cb','cg',-20)
# Save structure
pymol.cmd.save('F8.pdb','pep')

# Initialize the second example b-strand
get_b_strand('KFEFKFEFKK')
# Align bulky residues on the cross-section
set_chi_angle(2,'n','ca','cb','cg',-20)
set_chi_angle(4,'n','ca','cb','cg',-20)
set_chi_angle(6,'n','ca','cb','cg',-20)
set_chi_angle(8,'n','ca','cb','cg',-20)
# Save structure
pymol.cmd.save('K10.pdb','pep')

# Initialize the thrid example b-strand
get_b_strand('IGSNVVTWYQQL')
# Save structure
pymol.cmd.save('AL1.pdb','pep')