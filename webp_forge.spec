# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec – WebP Forge
# Użycie: pyinstaller webp_forge.spec

import os
from pathlib import Path

ROOT = Path(SPECPATH)

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Zasoby aplikacji
        (str(ROOT / "app" / "assets"), "app/assets"),
    ],
    hiddenimports=[
        "PIL",
        "PIL.Image",
        "PIL.WebPImagePlugin",
        "customtkinter",
        "packaging",
        "packaging.version",
        "packaging.specifiers",
        "packaging.requirements",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "numpy", "scipy", "pandas"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="WebPForge",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,   # brak okna konsoli
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ROOT / "app" / "assets" / "icons" / "app.ico"),
)
