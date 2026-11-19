# Local workshop installation

## 1. Download the workshop

Download and extract the [workshop repository](https://github.com/CCPBioSim/2026-building-molecular-systems-workshop), or clone it with Git (via `git clone https://github.com/CCPBioSim/2026-building-molecular-systems-workshop` in the terminal).

On **Windows**, first install [WSL and Ubuntu](https://learn.microsoft.com/windows/wsl/install), then use the Ubuntu terminal. On **macOS**, use Terminal; on **Linux**, use your usual terminal.

## 2. Install and start JupyterLab

```bash
bash install/install_workshop.sh
```

The script installs Miniforge if needed, creates a `workshop` conda environment, installs the dependencies, downloads FibrilGen and starts JupyterLab. It requires an internet connection and can take some time. Open the URL printed in the terminal and select a notebook. If prompted for a kernel, select the workshop Python kernel.

The script does not overwrite an existing workshop environment. To continue an interrupted installation in the existing environment, run:

```bash
bash install/install_workshop.sh --resume
```

This rechecks conda dependencies and repeats the remaining installation steps. On macOS, if a source build reports missing developer tools, run `xcode-select --install` and complete the installation.

## Later sessions

In the workshop folder, activate the environment and start JupyterLab:

```bash
conda activate workshop
jupyter lab
```

If `conda` is not available in a new terminal, initialise your shell using the conda executable printed during installation or see the [Miniforge instructions](https://github.com/conda-forge/miniforge#install), then open a new terminal.

## Notes

- On Apple Silicon, use macOS rather than Docker for native OpenCL. Check it with `python -m openmm.testInstallation`. GPU support depends on the software; CUDA requires an NVIDIA GPU.
- MODELLER requires a separate licence. Without one, prepmd uses PDBFixer.
