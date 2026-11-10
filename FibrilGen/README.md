# FibrilGen

`FibrilGen` is a Python library for bottom-up construction of various cross-beta structures using user-initiated parameters. These structures can be built to fit experimental observations (e.g., cryo-EM or ssNMR data) or be fully hypothetical. A FibrilGen/MD workflow can screen geometrically feasible and energetically favourable cross-beta structures.

In this workshop, I will use a Jupyter notebook to demonstrate FibrilGen building cross-beta structures (see the [presentation file](FibrilGen-workshop-material.pdf). You could run [this notebook](demo_Colab.ipynb) in Google Colab and adjust the input variables to see how they change the assembled structures. Note that FibrilGen conducts geometry searches to assemble compact cross-beta structures. Neighbouring peptides are kept within the nonbonding interaction cutoff to allow further energy-based optimisations and hypothesise cross-beta structures.

To store FibrilGen structures locally, you can download the workshop GitHub repository and run the notebooks on your computer.

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

You can run the Jupyter notebooks separately.

| Content | Links | Data |
| --- | --- | --- |
| Build a beta-strand| [build_a_b_strand.ipynb](build_a_b_strand.ipynb) | [data_b_strands](data_b_strands)  |
| Build a bilayer structure| [build_a_bilayer.ipynb](build_a_bilayer.ipynb)  | [data_bilayers](data_bilayers) |
| Build a fibril structure| [build_a_fibril.ipynb](build_a_fibril.ipynb) | [data_fibrils](data_fibrils) |

To leave the fibrilgen workspace, close your terminal by Crtl-C and deactivate the environment.
```bash
conda deactivate fibrilgen
```

To re-enter the fibrilgen workspace, activate your `fibrilgen` environment and initiate `JupyterLab`.
```bash
conda activate fibrilgen
jupyter lab
```

For first-time users, start with [peptide molecules](data_b_strands/ref) and [periodic assembly patterns](data_bilayers/ref) known to form cross-beta structures. You could build cross-beta structures as seen in the TEM and cryo-EM images. You are then invited to change the stacking and the initial twists to see whether there are other geometrically feasible cross-beta assemblies (see examples in [build_fibrils](data_fibrils/ref). Finally, we suggest that you try your own peptide molecule and reference bilayer structure to construct cross-beta fibril structures. 

## Resources
Please explore the websites to learn more about FibrilGen. FibrilGen reference API is available at this [page](https://chaoyuyang0.github.io/fibrilgen-docs/). The latest FibrilGen version, FibrilGen-v1, is available at this [GitHub repository](https://github.com/ChaoYuYang0/FibrilGen-v1).

## Author
Chao-Yu Yang

<!-- | **PyPI** || -->




