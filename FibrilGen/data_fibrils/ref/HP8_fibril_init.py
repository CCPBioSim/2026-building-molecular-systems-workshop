import os
abspath = os.path.abspath('')
import sys
sys.path.append(f'{abspath}/../../fibrilgen_local')

from builder import *

## Load PDB
pymol.cmd.load('HP8_bilayer_em.pdb')

## Create a periodic unit
# INPUT: (peptide length, the number of peptides per sheet, start residue index, end residue index)
unit = create_sheet_unit(10,9,2,9,True)

## Create a fibril object
fibril = create_fibril(unit)
fibril.tilt_s1, fibril.tilt_s2 = 0, 20

## Build a ribbon
fibril.build_a_ribbon(30,60,30,1)
print ('This is a ribbon:')
fibril.get_dimension()
pymol.cmd.save('HP8_ribbon.pdb','a_ribbon')
pymol.cmd.delete('delete *contact*')
pymol.cmd.delete('delete *a_ribbon*')
pymol.cmd.delete('delete *visBox*')

## List geometrically feasible conformations
lo_init_radius = [15,20,25,30,35]
lo_out_radius,lo_out_rise = [],[]
for init_radius in lo_init_radius:
	fibril.build_a_ribbon(30,init_radius,30,1)
	if fibril.write_output == 1:
		lo_out_radius += [fibril.radius]
		lo_out_rise += [float(4.8*(1-np.sin(fibril.angle_z*np.pi/180)))]
		pymol.cmd.delete('delete *contact*')
		pymol.cmd.delete('delete *a_ribbon*')
		pymol.cmd.delete('delete *visBox*')
with open('HP8_ribbons.txt', 'w') as file:
	x = [(radius,rise) for (radius,rise) in zip(lo_out_radius,lo_out_rise)]
	file.write('Available (radius,rise) pairs:\n')
	file.write(str(x)+'\n')

## Build a C4 tube
print ('\nThis is a stacked tube:')
fibril.build_a_stacked_ribbon(20,30,90,4,20,1)
fibril.get_dimension()
pymol.cmd.save('HP8_C4_tube.pdb','s_ribbon')
pymol.cmd.delete('delete *contact*')
pymol.cmd.delete('delete *s_ribbon*')
pymol.cmd.delete('delete *visBox*')

## List geometrically feasible conformations
lo_init_radius = [15,20,25,30,35]
lo_out_radius,lo_out_rise = [],[]
for init_radius in lo_init_radius:
	fibril.build_a_stacked_ribbon(20,init_radius,90,4,20,1)
	if fibril.write_output == 1:
		lo_out_radius += [fibril.radius]
		lo_out_rise += [float(4.8*(1-np.sin(fibril.angle_z*np.pi/180)))]
		pymol.cmd.delete('delete *contact*')
		pymol.cmd.delete('delete *a_ribbon*')
		pymol.cmd.delete('delete *visBox*')
with open('HP8_C4_tubes.txt', 'w') as file:
	x = [(radius,rise) for (radius,rise) in zip(lo_out_radius,lo_out_rise)]
	file.write('Available (radius,rise) pairs:\n')
	file.write(str(x)+'\n')

## Build a C5 tube
print ('\nThis is a stacked tube:')
fibril.build_a_stacked_ribbon(20,30,72,5,20,1)
fibril.get_dimension()
pymol.cmd.save('HP8_C5_tube.pdb','s_ribbon')
pymol.cmd.delete('delete *contact*')
pymol.cmd.delete('delete *s_ribbon*')
pymol.cmd.delete('delete *visBox*')

## List geometrically feasible conformations
lo_init_radius = [15,20,25,30,35]
lo_out_radius,lo_out_rise = [],[]
for init_radius in lo_init_radius:
	fibril.build_a_stacked_ribbon(20,init_radius,72,5,20,1)
	if fibril.write_output == 1:
		lo_out_radius += [fibril.radius]
		lo_out_rise += [float(4.8*(1-np.sin(fibril.angle_z*np.pi/180)))]
		pymol.cmd.delete('delete *contact*')
		pymol.cmd.delete('delete *a_ribbon*')
		pymol.cmd.delete('delete *visBox*')
with open('HP8_C5_tubes.txt', 'w') as file:
	x = [(radius,rise) for (radius,rise) in zip(lo_out_radius,lo_out_rise)]
	file.write('Available (radius,rise) pairs:\n')
	file.write(str(x)+'\n')

