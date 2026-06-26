@echo off
REM Build Windows installer (NSIS + MSI) without code signing.
REM Run from the repository root on a Windows machine with:
REM   - Node.js, Rust (stable), Visual C++ Build Tools installed
REM   - uv (for Python sidecar build)

echo =^> Building Python sidecars...
bash scripts\build_python.sh
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python sidecar build failed.
    exit /b %ERRORLEVEL%
)

echo =^> Running tauri build...
npm run tauri build

echo.
echo =^> Done. Installer files are in:
echo     src-tauri\target\release\bundle\nsis\
echo     src-tauri\target\release\bundle\msi\
