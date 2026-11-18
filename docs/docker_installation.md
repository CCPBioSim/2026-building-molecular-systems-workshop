# Running the workshop with Docker

## 1. Install Docker

- **macOS:** Install and start [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/). Choose Apple silicon or Intel to match your Mac.
- **Windows:** Install and start [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Use the WSL 2 backend and Linux containers.
- **Linux:** Install [Docker Desktop](https://docs.docker.com/desktop/setup/install/linux/) or [Docker Engine](https://docs.docker.com/engine/install/) for your distribution, and start it.

Open a terminal (PowerShell on Windows) and check that Docker is running:

```bash
docker version
```

Docker Desktop licensing may depend on your organisation; see the installation page for details.

## 2. Build the workshop image

Download or clone the workshop repository, then open a terminal in its root folder, containing `docker/dockerfile` and `install/requirements.txt`. For example:

```bash
git clone https://github.com/CCPBioSim/2026-building-molecular-systems-workshop.git
cd 2026-building-molecular-systems-workshop
docker build -f docker/dockerfile -t workshop:latest .
```

If you already have the repository, just change into its root folder and run the build command. The first build downloads dependencies and may take some time. The `docker/dockerfile` and workshop materials need to be present in the checkout; the image is not yet provided as a published download.

## 3. Start JupyterLab

Run this once to create and start the workshop container (for NVIDIA GPU access, see below):

```bash
docker run -it --name workshop -p 127.0.0.1:8888:8888 workshop:latest
```

Open the `http://127.0.0.1:8888/lab?token=...` URL printed in the terminal. In JupyterLab, open a notebook and run its cells.

Press `Ctrl+C` in the terminal to stop JupyterLab. To start the same container again later, run:

```bash
docker start -ai workshop
```

Notebook changes and output files saved inside this container persist when it stops, but are **deleted if the container is removed**. Download important files from JupyterLab to keep a separate copy.

## Optional: NVIDIA GPU on Linux or Windows

1. Install a compatible NVIDIA driver. On **Linux**, install and configure the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). On **Windows**, use Docker Desktop with WSL 2 and follow [Docker's GPU setup](https://docs.docker.com/desktop/features/gpu/).
2. Before starting JupyterLab, check whether OpenMM can use CUDA:

   ```bash
   docker run --rm --gpus all workshop:latest python -m openmm.testInstallation
   ```

   Look for a successful CUDA test. The Dockerfile does not explicitly ensure CUDA-enabled OpenMM or PyTorch packages, so GPU access alone may not be sufficient. The notebook must also select a compatible GPU backend.
3. If the test succeeds, create the container with GPU access **instead of** the run command above:

   ```bash
   docker run -it --gpus all --name workshop -p 127.0.0.1:8888:8888 workshop:latest
   ```

   If you already created `workshop` without GPU access, use a different container name, such as `workshop-gpu`, and use that name when restarting it.

On Apple Silicon, this Linux container cannot access the Apple GPU. For native macOS OpenCL, use the [local installation instructions](local_installation.md). AMD and Intel GPUs require different configuration.
