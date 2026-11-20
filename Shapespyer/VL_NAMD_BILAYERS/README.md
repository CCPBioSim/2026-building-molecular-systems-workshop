# Shapespyer — Building Molecular Systems Workshop 2026

Hands-on workshop material for [Shapespyer](https://gitlab.com/simnavi/shapespyer), a Python toolkit for building and preparing complex molecular systems.

The workshop introduces the construction of lipid bilayers, preparation of molecular dynamics simulations with NAMD, and building membrane–protein systems.

## Workshop notebook

The [Shapespyer Workshop](Shapespyer_Workshop.ipynb) notebook contains all three tutorials:

1. Building a POPC bilayer.
2. Preparing and simulating a POPC bilayer with NAMD.
3. Building and preparing a membrane-protein system.

This is the recommended starting point for workshop participants.

## Running in Google Colab

The combined notebook supports Google Colab without requiring a local Shapespyer installation.

1. Open the combined notebook in Google Colab from this repository.
2. Run the environment setup cell first.
3. Follow the exercises in order.

The setup cell installs Shapespyer with its protein-preparation dependencies and downloads the required input structures and reference data.

The notebook currently installs Shapespyer from the `workshop-tutorials` development branch. This will be updated when the workshop changes are merged into the main software repository.

Running NAMD simulations is optional. The workshop includes reference data for trajectory analysis without running a full simulation.


## Running locally

Python 3.11 or later is required.

Create a Python environment and install Shapespyer with its protein-preparation dependencies:

    python -m pip install "shapespyer[protein] @ git+https://gitlab.com/simnavi/shapespyer.git@workshop-tutorials"

Launch Jupyter from the Shapespyer directory:

    jupyter lab

The notebooks use Shapespyer's command-line tools to build molecular systems and prepare NAMD inputs.


## Dependencies

Shapespyer automatically installs its standard Python dependencies:

- Python >=3.11
- MDTraj >=1.11.1 — trajectory analysis
- NGLView ==4.0 — molecular visualisation
- ipywidgets >=8.1.7 — interactive widgets
- Jupyter >=1.1.1 — notebook execution

The optional `shapespyer[protein]` installation also provides:

- PDBFixer — protein structure reconstruction
- OpenMM — molecular structure handling, required by PDBFixer

NAMD is an optional external executable and is not installed automatically.


## Supporting materials

- `inputs/` — starting POPC and bacteriorhodopsin structures.
- `toppar/` — CHARMM parameter files for NAMD preparation.
- `reference/` — precomputed POPC structures and trajectory.
- `outputs/tutorial_03/reference/` — reference data for the membrane–protein tutorial.
- `*_template.conf` — NAMD configuration templates.

Generated simulation files are written to `outputs/` when the notebooks are executed.

## Project source

- [Shapespyer source code](https://gitlab.com/simnavi/shapespyer)
- [Shapespyer documentation](https://simnavi.gitlab.io/shapespyer.io/)
- [Shapespyer on PyPI](https://pypi.org/project/shapespyer/)

