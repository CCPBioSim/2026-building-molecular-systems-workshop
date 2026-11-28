# 2026-building-molecular-systems-workshop

Repository containing workshop material for the 2026 Building Molecular Systems Workshop.

The workshop has concluded and this repository is now marked as archived. This means the material in this repository will no longer be updated or changed, but can still be forked or cloned. 


## Running the workshop

There are two options for installing the software dependencies for this workshop. You can either install all dependencies and run jupyterlab locally. Alternatively, you can run via a docker container without having to install dependencies locally.

- [Local installation (conda)](docs/local_installation.md): `bash install/install_workshop.sh`
- [Docker installation](docs/docker_installation.md): `docker pull ghcr.io/ccpbiosim/2026-building-molecular-systems-workshop:latest`

## Repository layout

- `docs/`: installation instructions
- `docker/`: `dockerfile` for the workshop image (build from the repository root)
- `install/`: local install script and the pinned requirements shared with the Docker image
- `prepmd/`, `Shapespyer/`, `FibrilGen/`, `MDNA/`: workshop materials
