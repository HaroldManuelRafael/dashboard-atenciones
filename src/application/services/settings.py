"""Persistent, non-secret user settings and environment overrides."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from application.services.data_source import (
    DATA_SOURCE_ENV,
    GOOGLE_SERVICE_ACCOUNT_FILE_ENV,
    GOOGLE_SPREADSHEET_ID_ENV,
    GOOGLE_WORKSHEET_NAME_ENV,
)

SETTINGS_FILE_NAME = "settings.json"
_ALLOWED_SOURCES = {"local", "google_sheets"}
_SETTING_KEYS = {"data_source", "spreadsheet_id", "worksheet_name", "google_service_account_file"}


@dataclass(frozen=True)
class Settings:
    data_source: str = "local"
    spreadsheet_id: str = ""
    worksheet_name: str = ""
    google_service_account_file: str = ""


def settings_path() -> Path:
    """Return the per-user settings path without creating it."""
    if os.environ.get("APPDATA"):
        base = Path(os.environ["APPDATA"])
    elif os.environ.get("XDG_CONFIG_HOME"):
        base = Path(os.environ["XDG_CONFIG_HOME"])
    else:
        base = Path.home() / ".config"
    return base / "DashboardAtenciones" / "config" / SETTINGS_FILE_NAME


def _from_mapping(values: dict[str, object]) -> Settings:
    source = str(values.get("data_source", "local")).strip().casefold()
    if source not in _ALLOWED_SOURCES:
        raise ValueError("data_source debe ser 'local' o 'google_sheets'.")
    return Settings(
        data_source=source,
        spreadsheet_id=str(values.get("spreadsheet_id", "") or "").strip(),
        worksheet_name=str(values.get("worksheet_name", "") or "").strip(),
        google_service_account_file=str(values.get("google_service_account_file", "") or "").strip(),
    )


def load_settings(path: Path | None = None) -> Settings:
    """Load settings, treating a missing file as defaults."""
    target = path or settings_path()
    if not target.exists():
        return Settings()
    try:
        values = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("El archivo settings.json no es válido o no se puede leer.") from error
    if not isinstance(values, dict):
        raise TypeError("El archivo settings.json debe contener un objeto JSON.")
    return _from_mapping(values)


def resolve_settings(path: Path | None = None) -> Settings:
    """Merge environment overrides over persisted settings and defaults."""
    persisted = load_settings(path)
    values = asdict(persisted)
    overrides = {
        "data_source": os.environ.get(DATA_SOURCE_ENV),
        "spreadsheet_id": os.environ.get(GOOGLE_SPREADSHEET_ID_ENV),
        "worksheet_name": os.environ.get(GOOGLE_WORKSHEET_NAME_ENV),
        "google_service_account_file": os.environ.get(GOOGLE_SERVICE_ACCOUNT_FILE_ENV),
    }
    values.update({key: value for key, value in overrides.items() if value is not None})
    return _from_mapping(values)


def validate_settings(settings: Settings, *, require_credentials_file: bool = True) -> None:
    if settings.data_source not in _ALLOWED_SOURCES:
        raise ValueError("La fuente debe ser Excel local o Google Sheets.")
    if settings.data_source == "google_sheets":
        if not settings.spreadsheet_id:
            raise ValueError("Indica el Spreadsheet ID de Google Sheets.")
        if not settings.worksheet_name:
            raise ValueError("Indica el nombre de la hoja de Google Sheets.")
        if not settings.google_service_account_file:
            raise ValueError("Indica la ruta del JSON de la cuenta de servicio.")
        if require_credentials_file and not Path(settings.google_service_account_file).expanduser().is_file():
            raise ValueError("El archivo JSON de credenciales no existe.")


def save_settings(settings: Settings, path: Path | None = None) -> Path:
    """Persist only the supported non-secret settings."""
    validate_settings(settings)
    target = path or settings_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {key: value for key, value in asdict(settings).items() if key in _SETTING_KEYS}
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target
