import gridData
import MDAnalysis as mda
import io

def convert_to_dx(input_mrc, output_dx):
  g = gridData.Grid(input_mrc)
  g.export(output_dx)

def get_pdb_traj(top, traj):
  u = mda.Universe(top, traj)
  atoms_to_view = u.select_atoms("not resname WAT and not resname HOH and not "
    "resname SOD and not resname CLA and not type H")
  pdb_stream = io.StringIO()
  with mda.Writer(pdb_stream, format="PDB", multiframe=True) as W:
    for ts in u.trajectory[::3]:
      W.write(atoms_to_view)
    trajectory_pdb_string = pdb_stream.getvalue()
  pdb_stream.close()
  return trajectory_pdb_string