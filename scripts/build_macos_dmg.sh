#!/usr/bin/env bash
# Build a signed & notarized DMG for macOS distribution.
# Prerequisites:
#   1. Developer ID Application certificate in Keychain
#   2. Generate an App-Specific Password at appleid.apple.com
#   3. Set APPLE_PASSWORD env var before running:
#        export APPLE_PASSWORD="xxxx-xxxx-xxxx-xxxx"
# Usage: bash scripts/build_macos_dmg.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -z "${APPLE_PASSWORD:-}" ]]; then
  echo "ERROR: APPLE_PASSWORD is not set."
  echo "  Generate an App-Specific Password at appleid.apple.com, then:"
  echo "  export APPLE_PASSWORD=\"xxxx-xxxx-xxxx-xxxx\""
  exit 1
fi

# ---- Step 1: Build Python sidecars ----
echo "==> Building Python sidecars..."
bash scripts/build_python.sh

# ---- Step 2: Set signing / notarization env vars ----
export APPLE_SIGNING_IDENTITY="Developer ID Application: Tomohiro TANIGUCHI (72Y2MB92H5)"
export APPLE_TEAM_ID="72Y2MB92H5"
export APPLE_ID="tomohiron907@gmail.com"
# APPLE_PASSWORD must be set externally (App-Specific Password from appleid.apple.com)

# ---- Step 3: Tauri build (sign → notarize → DMG) ----
echo "==> Running tauri build..."
npm run tauri build -- --target aarch64-apple-darwin

DMG_DIR="src-tauri/target/aarch64-apple-darwin/release/bundle/dmg"
APP_PATH="src-tauri/target/aarch64-apple-darwin/release/bundle/macos/G-coordinator.app"

echo ""
echo "==> Build complete."
echo "    DMG: $DMG_DIR/"
ls -lh "$DMG_DIR/"

# ---- Step 4: Verify signature ----
echo ""
echo "==> Verifying code signature..."
codesign --verify --deep --strict "$APP_PATH" && echo "    Signature OK"

echo ""
echo "==> Checking Gatekeeper acceptance..."
spctl --assess --type execute --verbose "$APP_PATH" && echo "    Gatekeeper: accepted"
