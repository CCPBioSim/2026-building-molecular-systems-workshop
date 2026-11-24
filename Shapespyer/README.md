# Shapespyer

Workshop material for the `Shapespyer` package.

## Workshop checklist

### Content
- [V] Python notebook containing training material.
- [V] List of dependencies and accepted version ranges for each.
- [V] Supporting material e.g. images, input files.

## Installing Shapespyer from PyPI.org

python -m pip install "Shapespyer[protein]==0.3.1"

Check `requirements.txt` for the dependencies (which are installed automatically by the above command)

## Project Source

| Category       | Badges |
|----------------|--------|
| **Source Code** | [![Code](https://img.shields.io/badge/gitlab-repo-green%3Flogo%3Dgitlab)](https://gitlab.com/simnavi/shapespyer) |
| **Documentation** | [![Docs]()](https://simnavi.gitlab.io/shapespyer.io/) |
| **PyPI**       | [![PyPI - Version](https://img.shields.io/pypi/v/shapespyer.svg)](https://pypi.org/project/Shapespyer/) [![PyPI - Status](https://img.shields.io/pypi/status/shapespyer.svg)](https://pypi.org/project/shapespyer/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shapespyer.svg)](https://pypi.org/project/shapespyer/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/shapespyer.svg)](https://pypi.org/project/shapespyer/) |

Jupyter notebooks containing hands-on training material for Shapespyer package - a versatile Python toolchain for creating a variety of complex (bio-) molecular structures to seed numerical simulations thereof. - ***For more details see README.md in each tutorial's subfolder***.

## Notebooks

Run them in this order:

1. `AB_GMX_LIPIDS_WORKFLOW/SHAPESPYER_INTRO.ipynb`: a short introduction (~10 mins); **Colab-ready** version: `AB_GMX_LIPIDS_WORKFLOW/_ipynb_colab/SHAPESPYER_INTRO_Colab.ipynb`.
2. `AK_PROJECTS/0?_*.ipynb`: an overview of a GUI backend APIs and User Project structure; run in the order of the numercial index of notebooks (~30 mins); **Colab-ready** version: https://github.com/seventil/shapespyer-workshop/tree/main.
3. `AB_GMX_LIPIDS_WORKFLOW/GMX_LIPID_VESICLE.ipynb`: from SMILES to multicomponent lipid vesicle structure - using Shapespyer CLI with hints for preparing Gromacs simulations (~40 mins); **Colab-ready** version: `AB_GMX_LIPIDS_WORKFLOW/_ipynb_colab/GMX_LIPID_VESICLE_Colab.ipynb`.
4. `VL_NAMD_BILAYERS/Shapespyer_Workshop[_50 min].ipynb`: building planar lipid bilayers with inclusion of proteins and preparation of NAMD simulations (~50 mins); the maim tutorial is already **Colab-ready** (combined version).

Documentation on Zenodo: **DOI:10.5281/zenodo.19074587** (all versions) : https://zenodo.org/records/19074587