#!/usr/bin/env bash
# Build PyInstaller sidecar binaries for G-coordinator.
# Run from the repository root: bash scripts/build_python.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VENV=".venv-build"
BINARIES_DIR="src-tauri/binaries"
PYTHON_VERSION="3.12"

# ---- Detect target triple ----
OS=$(uname -s)
ARCH=$(uname -m)

case "$OS" in
  Darwin)
    case "$ARCH" in
      arm64)  TRIPLE="aarch64-apple-darwin" ;;
      x86_64) TRIPLE="x86_64-apple-darwin"  ;;
      *) echo "Unsupported macOS arch: $ARCH"; exit 1 ;;
    esac
    ;;
  Linux)
    case "$ARCH" in
      x86_64)  TRIPLE="x86_64-unknown-linux-gnu" ;;
      aarch64) TRIPLE="aarch64-unknown-linux-gnu" ;;
      *) echo "Unsupported Linux arch: $ARCH"; exit 1 ;;
    esac
    ;;
  MINGW*|CYGWIN*|MSYS*)
    TRIPLE="x86_64-pc-windows-msvc"
    ;;
  *)
    echo "Unsupported OS: $OS"; exit 1 ;;
esac

echo "==> Target triple: $TRIPLE"

# ---- Create isolated build venv ----
echo "==> Creating build venv at $VENV"
uv venv "$VENV" --python "$PYTHON_VERSION"

PYTHON="$VENV/bin/python"
if [[ "$OS" == MINGW* || "$OS" == CYGWIN* || "$OS" == MSYS* ]]; then
  PYTHON="$VENV/Scripts/python.exe"
fi

echo "==> Installing dependencies"
uv pip install --python "$PYTHON" \
  "gcoordinator==0.0.23" \
  "pyinstaller>=6.0" \
  "numpy" \
  "contourpy" \
  "msgpack"

# ---- Locate gcoordinator settings data ----
GC_PKG=$("$PYTHON" -c "import gcoordinator, os; print(os.path.dirname(gcoordinator.__file__))")
GC_SETTINGS="$GC_PKG/settings"

# ---- Helper: run PyInstaller ----
build_binary() {
  local script="$1"
  local name="$2"

  echo "==> Building $name from python/$script"

  "$PYTHON" -m PyInstaller \
    --onefile \
    --noconfirm \
    --distpath dist-pyinstaller \
    --workpath build-pyinstaller \
    --name "$name-$TRIPLE" \
    --hidden-import gcoordinator \
    --hidden-import gcoordinator.path_generator \
    --hidden-import gcoordinator.gcode_generator \
    --hidden-import gcoordinator.gui_export \
    --hidden-import gcoordinator.preview \
    --hidden-import gcoordinator.settings \
    --hidden-import numpy \
    --hidden-import numpy.core \
    --hidden-import contourpy \
    --hidden-import msgpack \
    --add-data "$GC_SETTINGS:gcoordinator/settings" \
    "python/$script"
}

# ---- Build both scripts ----
build_binary "runner.py"    "runner"
build_binary "gcode_gen.py" "gcode-gen"

# ---- Copy to src-tauri/binaries/ ----
mkdir -p "$BINARIES_DIR"
cp "dist-pyinstaller/runner-$TRIPLE"    "$BINARIES_DIR/runner-$TRIPLE"
cp "dist-pyinstaller/gcode-gen-$TRIPLE" "$BINARIES_DIR/gcode-gen-$TRIPLE"

# Mark binaries executable (no-op on Windows, required on macOS/Linux)
chmod +x "$BINARIES_DIR/runner-$TRIPLE"
chmod +x "$BINARIES_DIR/gcode-gen-$TRIPLE"

echo ""
echo "==> Done. Binaries written to $BINARIES_DIR/"
ls -lh "$BINARIES_DIR/"
