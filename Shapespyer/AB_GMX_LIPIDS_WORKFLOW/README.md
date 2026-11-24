# Shapespyer — Building Molecular Systems Workshop 2026

This folder contains hands-on training material for [Shapespyer](https://gitlab.com/simnavi/shapespyer) - a versatile Python toolchain for creating a variety of complex (bio-) molecular structures to seed numerical simulations thereof.

The tutorials presented at the workshop illustrate the preparation of lipid vesicles and bilayers followed by setting up molecular dynamics (MD) simulations to be carried out with Gromacs or NAMD packages.

## Workshop notebook

The Jupyter notebook **GMX_LIPIDS_WORKFLOW.ipynb** found in this folder contains a full set of instructions for:

1. Generating a template (seeding) 3D structure of a molecule based on its SMILES string(s).

2. Atomatically ordering and renaming atoms in a template structure (.pdb) in accord with the CHARMM36 FF conventions and simultaneously creating a consistently arranged Gromacs-style topology file (.itp) by using DL_FIELD software.

3. Aligning hydrocarbon tails in a lipid molecule by running short MD simulations using Gromacs.

4. Preparing an initial configuration of a multicomponent vesicle, starting with template molecular structures of its constituents, to seed an MD simulation to be run using Gromacs engine.

This is the recommended starting point for workshop participants.

## Running in Google Colab

The Colab-ready notebooks can be run within Google Colab *cloud* environment and *do not require a local Shapespyer installation*.

1. Open the combined notebook in Google Colab from this repository.
2. Run the Environment setup cell first.
3. Follow further instructions as usual.

**NOTE** For each given Shapespyer tutorial presented at the workshop the Colab-ready notebookalls may be located in different folders! 

For the current tutorial **GMX_LIPIDS_WORKFLOW** you will find Colab-ready notebooks in `Shapespyer/AB_GMX_LIPIDS_WORKFLOW/_ipynb_colab/`.

## Installing and running locally

Python 3.11 or later is required.

Create a Python environment:

    python3 -m venv .venv

The above command will set up a new environment in (sub)directory called `.venv` (in the current working directory).

Install Shapespyer with its protein-preparation dependencies:

    python -m pip install "shapespyer[protein]==0.3.1"

Launch Jupyter from the Shapespyer directory:

    jupyter lab

The notebooks use Shapespyer's command-line tools to build molecular systems and prepare Gromacs inputs.


## Dependencies

Shapespyer automatically installs its standard Python dependencies:

- Python >=3.11
- MDTraj >=1.11.1 — trajectory analysis
- NGLView ==4.0 — molecular visualisation
- ipywidgets >=8.1.7 — interactive widgets
- Jupyter >=1.1.1 — notebook execution

See `requirements.txt` for the full list of Shapespyer dependencies.

## Project source and other links

- [Shapespyer source code](https://gitlab.com/simnavi/shapespyer)
- [Shapespyer documentation](https://simnavi.gitlab.io/shapespyer.io/)
- [Shapespyer on PyPI](https://pypi.org/project/shapespyer/)
- **DOI:10.5281/zenodo.19074587 (all versions)** : https://zenodo.org/records/19074587

