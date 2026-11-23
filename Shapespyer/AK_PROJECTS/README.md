# Shapespyer: the `shapes.project` workflow

Four notebooks for a one-hour hands-on session with `shapes.project`, the Python API of [Shapespyer](https://gitlab.com/simnavi/shapespyer) that the EasyShapes desktop app uses as its backend. They build components, structures and a sample model, then equilibrate a sample model with GROMACS inside a project.

| Notebook | GROMACS | Time | Content |
|---|---|---|---|
| `01_components.ipynb` | no | 10 min | the library, `.show()`, a component from your own file and from a SMILES string, saving both to the library |
| `02_structures.ipynb` | no | 10 min | ring, rod, bilayer, ball, vesicle and lattice, assembled, exported and viewed |
| `03_sample_model.ipynb` | yes | 10 min | an asymmetric DOPC/POPC vesicle in TIP3 water with NaCl, assembled with `gmx insert-molecules` and `gmx solvate`, then exported |
| `04_equilibration.ipynb` | yes | 15 min | an SDS micelle project with stage 0 (minimisation) and an optional stage 1 (short MD, about 20 min on 2 CPU cores), the trajectory and micelle Rg, saving and loading the project, and the stages exported for VMD |

Each notebook starts with the same overview of the workflow and runs on its own.

## Running locally

Python 3.11 or later is required. Install Shapespyer 0.3.1:

    python -m pip install "shapespyer==0.3.1"

Notebooks 03 and 04 also need GROMACS. On WSL or Linux, install it with `sudo apt install gromacs`. On Windows, run 03 and 04 in WSL, or set `gmx_executable` in `shapespyer.yaml` to a Windows build of GROMACS.

Start Jupyter in this folder and open the notebooks. In VS Code, allow widget scripts from a CDN when it asks (setting `jupyter.widgetScriptSources`), so the molecule views show.

## Where the files go

`shapespyer.yaml` keeps the workshop's files apart from your own Shapespyer data. It sets `app_path: .data`, so the library goes to `.data/LocalAssets/`, the working files to `.data/Temp/`, the projects to `.data/Projects/` and the exports to `.data/work/`. The clean up cell at the end of each notebook deletes the work folder. Git ignores `.data/`.

Keep `shapespyer.yaml` next to the notebooks. The setup cell of each notebook stops with a message if it can't find it.

## Troubleshooting

| Message or symptom | Fix |
|---|---|
| `No shapespyer.yaml in ...; run the notebook in its own folder, next to shapespyer.yaml` | The notebook runs in another folder than its own. In VS Code, check the setting `jupyter.notebookFileRoot`; its default `${fileDirname}` is right. |
| `This notebook needs GROMACS: gmx not found ...` | Install GROMACS (on WSL or Linux: `sudo apt install gromacs`). On Windows, use WSL, or set `gmx_executable`. |
| A molecule view stays empty | In VS Code, allow widget scripts from a CDN (setting `jupyter.widgetScriptSources`), then run the view cell again. If that fails, restart the kernel and run all. |
| `Stage 0 hasn't finished, so stage 1 can't start` | Run stage 0 first. |
| `... was assembled again since stage 0 ran; run from stage 0` | The model changed. Set `first_stage = 0`. |
| `... is in use by this session ... Pass force=True to delete it anyway` | Assets of this session still use the files. Use `force=True`. |
| `Only N of M ... fit into the box` | Too much salt for the box. Lower the concentration. |
| `Layer 1 of ... needs an rmin of at least ...` (or `The inner leaflet of lamella 1 ...`) | A layer's or leaflet's `rmin` must be at least 1.6 times its `dmin`. Raise the `rmin` or lower the `dmin`. |
| `Asset with the name ... could not be downloaded`, with `429 Too Many Requests` in the warning above | GitLab limits downloads of the library files. Wait a minute, then run the cell again. |
| Windows: `FileNotFoundError` for a file in `.data\Temp\...\assembly.tmp\` (the lattice makes the deepest paths) | The path is longer than 260 characters. Move the folder closer to the drive root, or turn on long paths in an admin PowerShell: `New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -Value 1 -PropertyType DWORD -Force` |
