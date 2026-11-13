# MDNA

Workshop material for the `MDNA` package.

## Workshop checklist

### Content
- [x] Python notebook containing training material.
- [ ] List of dependencies and accepted version ranges for each.
- [x] Supporting material e.g. images, input files.

## Project Source

| Category       | Badges |
|----------------|--------|
| **Source Code** | [![Code](https://img.shields.io/badge/github-repo-blue)](https://github.com/Heezch/mdna) |
| **Documentation** | [![Docs]()](https://heezch.github.io/mdna/) |
| **PyPI**       | [![PyPI - Version](https://img.shields.io/pypi/v/mdna.svg)](https://pypi.org/project/mdna/) [![PyPI - Status](https://img.shields.io/pypi/status/mdna.svg)](https://pypi.org/project/mdna/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdna.svg)](https://pypi.org/project/mdna/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/mdna.svg)](https://pypi.org/project/mdna/) |

Jupyter notebooks that teach how to build 3D models of DNA, and how to measure the shape of DNA and RNA, with the [`mdna`](https://pypi.org/project/mdna/) Python package.

## Notebooks

Run them in this order:

1. `0_intro-jupyter.ipynb`: a short Python and Jupyter introduction.
2. `1_analyze.ipynb`: measure the shape of a DNA and an RNA trajectory.
3. `2_build.ipynb`: build DNA structures, from straight helices to knots.
4. `3_bonus.ipynb` (optional, for fast participants): build DNA systems for MD. A nucleosome with linker DNA, connecting DNA pieces and a DNA loop between proteins, chemical modifications, supercoiled minicircles, interlocked DNA rings, and checks before a simulation.

The `solutions/` folder has the same notebooks with the answers filled in.

The notebooks import two helpers from the `devtools/` folder, so keep it next to them: `devtools/mdna_workarounds.py` fixes known issues in mdna 0.2.0 (with a newer mdna it does nothing), and `devtools/viewer.py` shows structures in 3D inside the notebooks (`view(dna)`, with [Mol*](https://molstar.org)). The 3D viewer loads Mol* from the internet, so it needs a connection.

## Install

Pick one option.

### Option A: pixi (recommended)

[pixi](https://pixi.sh) installs everything in one step, including Python.

```
pixi install
pixi run lab
```

`pixi run lab` opens JupyterLab in your browser. Works on macOS (Apple Silicon), Linux and Windows.

### Option B: pip

Use this if you already have Python 3.10 or newer.

```
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

## Data files

The `data/` folder has the files the notebooks read, so keep it next to them: the DNA and RNA trajectories for `1_analyze.ipynb`, and the Protein Data Bank structures 1KX5 and 8SRP for `3_bonus.ipynb`. Both trajectories cover 1 µs in 201 frames, 5 ns apart; `rna.xtc` is every 50th frame of the original 10001-frame simulation output, to keep the download small.

## For organisers

The answers are kept in `devtools/answers/<notebook>.py`, and `devtools/make_solutions.py` fills them into the exercise notebooks to make the notebooks in `solutions/`. So after changing a notebook or an answer, rebuild the solutions instead of editing them by hand:

```
pixi run solutions
```

This runs every solutions notebook, which takes about 10 minutes. `python devtools/make_solutions.py --help` shows how to rebuild one notebook, or skip running it. The format of the answer files is explained at the top of `devtools/make_solutions.py`.

## Troubleshooting

If a notebook says the kernel failed to start, or it points to a folder that no longer exists, you may have an old `python3` kernel registered in Jupyter. Remove the folder named `python3` in your Jupyter kernels folder, then restart JupyterLab and pick the kernel again.

## Source of this material

This folder is a copy of `Heezch/mdna-workshop`, tag `ccpbiosim-2026`, commit `488c1fe`. Changes made here are not copied back to that repo automatically.
