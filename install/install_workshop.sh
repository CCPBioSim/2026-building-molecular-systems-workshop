#!/usr/bin/env bash
set -euo pipefail

# Everything is inside main() so bash parses the whole script before running;
# editing the file during a long install can no longer corrupt execution.
main() {
RESUME=false
if [ "$#" -gt 0 ]; then
    if [ "$#" -eq 1 ] && [ "$1" = "--resume" ]; then
        RESUME=true
    else
        echo "Usage: bash install/install_workshop.sh [--resume]" >&2
        exit 1
    fi
fi

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSHOP_DIR="$(dirname "$INSTALL_DIR")"
SYSTEM="$(uname -s)"
ARCH="$(uname -m)"

case "$SYSTEM:$ARCH" in
    Darwin:arm64|Darwin:x86_64) INSTALLER_SYSTEM="MacOSX" ;;
    Linux:x86_64|Linux:aarch64) INSTALLER_SYSTEM="Linux" ;;
    *)
        echo "Unsupported system: $SYSTEM $ARCH. On Windows, run this script in WSL." >&2
        exit 1
        ;;
esac

if command -v conda >/dev/null 2>&1; then
    CONDA_BASE="$(conda info --base)"
elif [ -x "$HOME/miniforge3/bin/conda" ]; then
    CONDA_BASE="$HOME/miniforge3"
else
    if [ -e "$HOME/miniforge3" ]; then
        echo "$HOME/miniforge3 already exists but does not contain conda; refusing to overwrite it." >&2
        exit 1
    fi
    if ! command -v curl >/dev/null 2>&1; then
        echo "Install curl before running this script." >&2
        exit 1
    fi
    INSTALLER="$(mktemp "${TMPDIR:-/tmp}/miniforge-installer.XXXXXX")"
    trap 'rm -f "$INSTALLER"' EXIT
    echo "Installing Miniforge into $HOME/miniforge3..."
    curl -fsSL "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$INSTALLER_SYSTEM-$ARCH.sh" -o "$INSTALLER"
    bash "$INSTALLER" -b -p "$HOME/miniforge3"
    CONDA_BASE="$HOME/miniforge3"
fi

ENV_DIR="$CONDA_BASE/envs/workshop"
if [ "$RESUME" = true ]; then
    if [ ! -f "$ENV_DIR/conda-meta/history" ]; then
        echo "No conda environment found at $ENV_DIR; cannot resume." >&2
        exit 1
    fi
    echo "Resuming installation in $ENV_DIR."
    CONDA_ACTION=install
else
    if [ -e "$ENV_DIR" ]; then
        echo "Environment already exists at $ENV_DIR; refusing to overwrite it." >&2
        echo "To continue an interrupted workshop installation, rerun with --resume." >&2
        exit 1
    fi
    CONDA_ACTION=create
fi

if [ -x "$CONDA_BASE/bin/mamba" ]; then
    SOLVER="$CONDA_BASE/bin/mamba"
else
    SOLVER="$CONDA_BASE/bin/conda"
fi

# Pinned versions and commits mirror the dockerfile.
TEMPY_REFF_COMMIT=af82854a3785174912da4f1c55ddbcc4d3cc8236
VOXCOV_COMMIT=65d5466de415dbcd60e51523238a8fe5e46a31a5
VOXCOVPY_COMMIT=3f8ef818f0da38ba9466e3a0ec81b8378b8eba7c
FIBRILGEN_COMMIT=1149ee77060343dc717b8d7cc3e9ec205facfd3f

for f in tempyreff_requirements.txt requirements.txt; do
    if [ ! -f "$INSTALL_DIR/$f" ]; then
        echo "Missing $INSTALL_DIR/$f." >&2
        exit 1
    fi
done

# jupyterlab, prepmd, pymol (for fibrilgen) and the first of tempy-reff's deps
"$SOLVER" "$CONDA_ACTION" -y -p "$ENV_DIR" -c CCPBioSim -c salilab -c conda-forge \
    python=3.13 jupyterlab==4.6.6 prepmd==1.0.2 pymol-open-source==3.1.0 \
    git wget conda-forge::xz --file "$INSTALL_DIR/tempyreff_requirements.txt"

# Conda activation hooks may reference unset variables.
set +u
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate "$ENV_DIR"
set -u

BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/workshop-build.XXXXXX")"

echo "Installing tempy-reff..."
git clone https://gitlab.com/topf-lab/tempy-reff.git "$BUILD_DIR/tempy-reff"
git -C "$BUILD_DIR/tempy-reff" checkout "$TEMPY_REFF_COMMIT"
python -m pip install "$BUILD_DIR/tempy-reff"

echo "Building voxcov from source in $BUILD_DIR..."
git clone https://github.com/thomasmulvaney/voxcov.git "$BUILD_DIR/voxcov"
git -C "$BUILD_DIR/voxcov" checkout "$VOXCOV_COMMIT"
git clone https://github.com/thomasmulvaney/voxcov-py.git "$BUILD_DIR/voxcov-py"
git -C "$BUILD_DIR/voxcov-py" checkout "$VOXCOVPY_COMMIT"
(cd "$BUILD_DIR/voxcov-py" && maturin develop --release)

if [ ! -e "$WORKSHOP_DIR/FibrilGen/fibrilgen_local" ]; then
    git clone https://github.com/ChaoYuYang0/FibrilGen-v1.git "$WORKSHOP_DIR/FibrilGen/fibrilgen_local"
    git -C "$WORKSHOP_DIR/FibrilGen/fibrilgen_local" checkout --detach "$FIBRILGEN_COMMIT"
elif [ ! -d "$WORKSHOP_DIR/FibrilGen/fibrilgen_local/.git" ]; then
    echo "FibrilGen/fibrilgen_local exists but is not a Git checkout; inspect it before continuing." >&2
    exit 1
else
    echo "Using existing FibrilGen/fibrilgen_local."
fi

# deps for fibrilgen, shapespyer and mdna
python -m pip install --no-cache-dir -r "$INSTALL_DIR/requirements.txt"

echo "Setup complete. Source build files are in $BUILD_DIR."
echo "For later sessions, initialise your shell if necessary with:"
printf '  "%s/bin/conda" init\n' "$CONDA_BASE"
echo "Then activate $ENV_DIR and run jupyter lab from $WORKSHOP_DIR."
cd "$WORKSHOP_DIR"
jupyter lab
}

main "$@"
exit
