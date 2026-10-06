"""Resolve the editable CSV used by the dashboard."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

APP_NAME = "DashboardAtenciones"
DATA_FILE_NAME = "atenciones.csv"
SAMPLE_FILE_NAME = "sample_atenciones.csv"
EXPLICIT_DATA_PATH_ENV = "DASHBOARD_ATENCIONES_DATA_PATH"


def _bundle_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[3]


def _editable_data_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise OSError("No se encontró la variable de entorno APPDATA del usuario.")
    return Path(appdata) / APP_NAME / "data" / DATA_FILE_NAME


def resolve_data_source() -> Path:
    """Return the CSV path, initializing the Windows user copy when packaged."""
    explicit_path = os.environ.get(EXPLICIT_DATA_PATH_ENV)
    if explicit_path and not getattr(sys, "frozen", False):
        return Path(explicit_path).expanduser()
    if not getattr(sys, "frozen", False):
        return _bundle_root() / "data" / SAMPLE_FILE_NAME

    target = _editable_data_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copyfile(_bundle_root() / "data" / SAMPLE_FILE_NAME, target)
    return target
