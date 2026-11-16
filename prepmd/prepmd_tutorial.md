# preparing protein structures with prepmd

This tutorial will cover:
* Preparing protein structures from the PDB for simulation with prepmd
* Running simple molecular dynamics simulations with prepmd
* Preparing and running simulations with ligands with prepmd
* Integrating EM data to refine a structure with TEMPy-ReFF

The final section is provided as an example of an integrative biology workflow. You are encouraged to do whatever you want with the resulting pdb, or to run prepmd using a structure that you are interested in instead of the provided examples.

## Setup

Before we can start preparing structures, we need to set up a conda environment. If you don't already have conda, you can install it by [following the instructions on conda-forge](https://conda-forge.org/download/). Note that some of the software used in this tutorial is not availabnle on windows, so if you're using windows, you will additionally need to [setup WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

Once conda is installed, use mamba to install the conda dependencies:

```
mamba install -c CCPBioSim -c salilab torchvision prepmd ambertools openmm pandas scipy mrcfile pdbfixer gemmi networkx pymol-open-source
```

Then use pip to install extra dependencies from pypi:
```
python -m pip install voxcov
git clone https://gitlab.com/topf-lab/tempy-reff.git
pip install -e tempy-reff
```

## Preparing a protein structure
We are now ready to start preparing structures. We will use [human presequence protease](https://www.rcsb.org/structure/6XOV) (PDB ID: 6XOV) as our demonstration structure. This structure was derived from Cryogenic Electron Microscopy (cryo-EM) and contains a loop region that was too flexible to show up in the electron density map. The code below will view the structure in pymol.

```
wget https://files.rcsb.org/download/6XOV.pdb
pymol 6XOV.pdb
```

By default, pymol doesn't display long missing loops, but you can force it to display them by running running `set cartoon_gap_cutoff, 50` in the console.

To prepare the system, we run prepmd with two arguments, the PDB ID to be downloaded (6xov) and the output filenane (6xov.pdb). prepmd will automatically work through the following steps:
* Fill missing loops
* Add missing atoms
* Fix non-standard residues
* Resolve steric clashes and minimise structure

By default, prepmd uses PDBFixer to fill loops, but PDBFixer's loop-filling tools are very basic. If you have a valid MODELLER license, you can use MODELLER instead by running this command:

```
add_modeller_license <LICENSE_KEY>
```
Note: if you have a structure file you want to use that's not available on the PDB, you can use the `-s`\ `--structure` argument to supply it. You still need to give it an ID in place of 6XOV - this could be anything, it's just required because some tools need to see a pdb file have a pdb ID.

prepmd has lots of optional features and settings, so if have more specific requirements you might want to consult the [readthedocs page](https://prepmd.readthedocs.io/en/latest/Prep-Structure.html).

prepmd has now written the output molecule to 6xov.pdb. We will eventually view the output file, but for now, we may as well run an MD simulation, because that's what you always do in tutorials like this.

## Run an MD simulation

prepmd has the ability to run molecular dynamics simulations by wrapping OpenMM functions. This can be useful to quickly run MD simulations for validation or as part of some larger automation, but it only supports a limited subset of OpenMM's functionality.

Here are some of the default parameters:
*   Force field: charmm36 (or amber14 if the system contains ligands)
*   Solvent: implicit equivalent to amber's igb=8 (or tip3p if the system contains ligands)
*   Timestep: 0.002 picoseconds (or 0.0002 picoseconds if the system contains ligands)
*   Constrain: Hbonds
*   Non bonded method: CutoffNonPeriodic (or PME if solvent is explicit)

runmd supports a selection of common MD settings, including several force fields,  integrators, solvent models, etc. Fore more information on these settings, [consult the runmd documentation](https://prepmd.readthedocs.io/en/latest/Run-with-runmd.html). The cell below will run a simulation of 50,000 MD steps, which should run fairly quickly, and write a trajectory file in the gromacs compressed trajectory format to traj.xtc.

```
runmd 6xov.pdb -o 6xov_minimised.pdb --traj_out traj.xtc --md_steps 10000
```
We can now view the resulting trajectory in pymol (you should also be able to see that the missing loop has been filled in!):
```
pymol 6xov_minimised.pdb
```
Then, in the pymol console, run:
```
load_traj traj.xtc
```

## Optional: run a ligand simulation
One of most fiddly and difficult and entirely necessary things you can do with a molecular dynamics simulation is to simulate a ligand. prpemd can automatically use rdkit to extract ligands from structure files and fix their geometry. runmd can run simulations containing ligands, and will automatically adjust md parameters and import the force fields provided by OpenFF. The cell below shows a ligand simulation of Alpha-Kinase Domain of Myosin Heavy chain Kinase (3PDT) being prepared and run. The parameter `-hetatms` tells prepmd to fix each small molecule and write it to a separate .sdf file. We're only interested in the ADP molecule, so we add it back to runmd via the `-l` argument.

```
prepmd --hetatms 3PDT 3PDT.pdb
runmd 3PDT.pdb -l ADP.sdf -o 3PDT_minimised.pdb --traj_out ligand_traj.xtc --md_steps 10000
```

## Optional: refine a structure using TEMPy-ReFF
This is getting outside of the scope of the tutorial, but the whole 'make a pdb, run a simulation' thing is sort of old hat, it's what every structure preparation tutorial has you do, and although the tools and structures are much better now, it's been philosophically unchanged for a long time. There are many more interesting things you can do with a prepared .pdb file, and as a somewhat arbitrary example, this tutorial will now show you how to refine the structure you've generated so that it matches an electron density map.

The structure we initially used was derived from an cryo-EM map, but we've now made a load of modifications to it, and it no longer matches the original data. By running TEMPy-ReFF, we can fit our fixed structure back into that original map.

The code below downloads the electron density map EMD-22281 (which corresponds to the PDB ID 6XOV) from the EMDB and runs TEMPy-ReFF.
```
wget https://files.wwpdb.org/pub/emdb/structures/EMD-22281/map/emd_22281.map.gz
python -m tempy_reff.main --model 6xov.pdb --map emd_22281.map.gz --resolution 0.855 --fitting-gmm --platform-cuda --output-dir tempy_out
```
View the outputs:
```
pymol tempy_out/final.pdb
```

To see how the pdb fits into the electron density map, load the isosurface and make it transparent. In the pymol console:
```
set normalize_ccp4_maps, 1
load /home/rob/Downloads/emd_22281.map, emd_22281
isosurface emd_22281_isosurface, emd_22281, 0.0053
set transparency, 0.5, emd_22281_isosurface
```

## End of tutorial!
Congratulations, you've reached the end of the tutorial! Feel free to use the remaining time to try whatever prepmd settings or molecules you like. Or do something else, I can't tell you what to do.
