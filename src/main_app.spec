# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['‘modeling’'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas += [('print_setting.ini', './/print_setting.ini', 'DATA')]
a.datas += [('G-coordinator.gcode', './/G-coordinator.gcode', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='main_app.app',
    icon=None,
    bundle_identifier=None,
)
