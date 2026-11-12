import os
abspath = os.path.abspath('')
import sys
sys.path.append(f'{abspath}/../../fibrilgen_local')

from builder import *

## Load PDB
pymol.cmd.load('AL1_bilayer_em.pdb')

## Create a periodic unit
# INPUT: (peptide length, the number of peptides per sheet, start residue index, end residue index)
unit = create_sheet_unit(12,9,2,11)

## Create a fibril object
fibril = create_fibril(unit)

## Build a rod
fibril.build_a_stacked_rod(10,[[1,1],[1,1],[1,1]],10,1)
print ('This is a stacked rod:')
fibril.get_dimension()
pymol.cmd.save('AL1_stacked_rod.pdb','s_rod')
pymol.cmd.delete('delete *contact*')
pymol.cmd.delete('delete *s_rod*')
pymol.cmd.delete('delete *visBox*')

## List geometrically feasible conformations
lo_init_tilt = [5,10,15,20,25,30]
lo_out_radius,lo_out_rise = [],[]
for init_tilt in lo_init_tilt:
	fibril.build_a_stacked_rod(init_tilt,[[1,1],[1,1],[1,1]],10,1) 
	if fibril.write_output == 1:
		lo_out_radius += [float(fibril.radius)]
		lo_out_rise += [float(4.8*(1-np.sin(fibril.angle_z*np.pi/180)))]
		pymol.cmd.delete('delete *contact*')
		pymol.cmd.delete('delete *s_rod*')
		pymol.cmd.delete('delete *visBox*')
with open('AL1_stacked_rods.txt', 'w') as file:
	x = [(radius,rise) for (radius,rise) in zip(lo_out_radius,lo_out_rise)]
	file.write('Available (radius,rise) pairs:\n')
	file.write(str(x)+'\n')


