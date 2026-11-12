import os
abspath = os.path.abspath('')
import sys
sys.path.append(f'{abspath}/../../fibrilgen_local')

from pep2unit import *
from reordering import *

def mol2pdb_convertsion(filename):
	os.system(f'obabel {filename}.mol -O {filename}_temp.pdb')
	pymol.cmd.load(f'{filename}_temp.pdb')
	pymol.cmd.save(f'{filename}.pdb',f'{filename}_temp')
	os.system(f'rm {filename}_temp.pdb')

## Load PDB
pymol.cmd.load('../../data_b_strands/ref/K10.pdb')

## Create a periodic unit
# INPUT: (peptide, start residue index, end residue index, does the start residue locate at the face)
unit = create_pep_unit('K10',2,9,1)

## --- Examples of sheet structures ---
# INPUT: (peptide unit)
sheet = create_sheet(unit)
# INPUT: (peptide alignment aaa/apa/aap/app/paa/ppa/pap/ppp, does two beta-sheet aligned face-to-face, num of units per sheet)
sheet.build_a_plain_sheet('aaa',1,5)
## --- End ---

## Save the structure
pymol.cmd.save('bilayer.pdb','plain_sheet')
ordering_indices('','bilayer.pdb','bilayer_indexed.pdb')

# Import openbabel and optimization library
from optimize import *
# Remove steric clashes
pymol.cmd.create('plain_sheet_em','plain_sheet')
minimize('plain_sheet_em',nsteps0=10)
pymol.cmd.save('bilayer_em.mol','plain_sheet_em')
mol2pdb_convertsion('bilayer_em')
ordering_indices('','bilayer_em.pdb','bilayer_em_indexed.pdb')
reordering_indices('','bilayer_indexed','bilayer_em_indexed','K10_bilayer_em',20,8)
os.system(f'rm bilayer*')
