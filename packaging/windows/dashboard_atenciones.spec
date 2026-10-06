# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


SPEC_DIR = Path(SPECPATH).resolve()
PROJECT_ROOT = SPEC_DIR.parent.parent
LAUNCHER_PATH = SPEC_DIR / "launcher.py"
SRC_PATH = PROJECT_ROOT / "src"
SAMPLE_CSV_PATH = PROJECT_ROOT / "data" / "sample_atenciones.csv"

hiddenimports = collect_submodules("streamlit")
datas = [
    (str(SRC_PATH), "src"),
    (str(SAMPLE_CSV_PATH), "data"),
    *collect_data_files("streamlit"),
]

a = Analysis(
    [str(LAUNCHER_PATH)],
    pathex=[str(SRC_PATH)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    name="DashboardAtenciones",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    exclude_binaries=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="DashboardAtenciones",
)
