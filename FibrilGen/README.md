# FibrilGen

`FibrilGen` is a Python library for bottom-up construction of various cross-beta structures using user-initiated parameters. These structures can be built to fit experimental observations (e.g., cryo-EM or ssNMR data) or be fully hypothetical. A FibrilGen/MD workflow can screen geometrically feasible and energetically favourable cross-beta structures.

In this workshop, we will use a Jupyter notebook to demonstrate FibrilGen building cross-beta structures (see the [presentation file](FibrilGen-workshop-material.pdf). You could run [this notebook](demo_Colab.ipynb) in Google Colab and adjust the input variables to see how they change the assembled structures. Note that FibrilGen conducts geometry searches to assemble compact cross-beta structures. Neighbouring peptides are kept within the nonbonding interaction cutoff to allow further energy-based optimisations and hypothesise cross-beta structures.

You can also download the workshop materials to your computer and set up a conda environment to generate FibrilGen structures locally.

```bash
# Download the workshop GitHub repository
git clone https://github.com/CCPBioSim/2026-building-molecular-systems-workshop.git
# Navigate to the FibrilGen folder
cd FibrilGen
# Create a conda environment
conda create -n fibrilgen
conda activate fibrilgen
# Download the source code and install the Python packages
python3 setup.py
# Initiate Jupyter Lab
jupyter lab
```

Use JupyterLab to run these Jupyter notebooks.

| Content | Links | Data |
| --- | --- | --- |
| Build a beta-strand| [build_a_b_strand.ipynb](build_a_b_strand.ipynb) | [data_b_strands](data_b_strands)  |
| Build a bilayer structure| [build_a_bilayer.ipynb](build_a_bilayer.ipynb)  | [data_bilayers](data_bilayers) |
| Build a fibril structure| [build_a_fibril.ipynb](build_a_fibril.ipynb) | [data_fibrils](data_fibrils) |

To leave the workspace, close your terminal by pressing Ctrl-C and deactivate the `fibrilgen` environment.

```bash
conda deactivate fibrilgen
```

To re-enter the workspace, activate your `fibrilgen` environment and initiate JupyterLab.
```bash
conda activate fibrilgen
jupyter lab
```

For first-time users, try building example [peptide molecules](data_b_strands/ref), [bilayer structures](data_bilayers/ref), and [fibril structures](data_fibrils/ref). You can find reference codes inside the folders. After that, feel free to use your own peptide molecule and bilayer structure to construct cross-beta fibril structures.

## Resources
Please explore the websites to learn more about FibrilGen. FibrilGen reference API is available at this [page](https://chaoyuyang0.github.io/fibrilgen-docs/). The latest FibrilGen version, FibrilGen-v1, is available at this [GitHub repository](https://github.com/ChaoYuYang0/FibrilGen-v1).

## Author
Chao-Yu Yang

<!-- | **PyPI** || -->




