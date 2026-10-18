"""Read-only Google Sheets data source."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

LOGGER = logging.getLogger(__name__)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Replace these examples with the exact form headers when the production sheet is known.
EXAMPLE_HEADER_MAPPING = {
    "Marca temporal": "fecha_hora",
    "Código del estudiante": "codigo_estudiante",
    "Apellidos y nombres": "nombre_estudiante",
    "Dirección de correo electrónico": "correo",
    "Número de celular": "celular",
    "Campus": "campus",
    "Motivo de consulta": "motivo_consulta",
}


class GoogleSheetsDataSourceError(RuntimeError):
    """Safe, user-facing error raised by the Google Sheets adapter."""


def _worksheet_range(worksheet_name: str) -> str:
    return f"'{worksheet_name.replace(chr(39), chr(39) * 2)}'"


def _map_headers(data: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    return data.rename(columns={**EXAMPLE_HEADER_MAPPING, **mapping})


def load_google_sheet(
    spreadsheet_id: str,
    worksheet_name: str,
    credentials_file: str | Path,
    header_mapping: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Fetch one worksheet using a service account and read-only scope."""
    credentials_path = Path(credentials_file).expanduser()
    if not credentials_path.is_file():
        raise GoogleSheetsDataSourceError("No se encontró el archivo de credenciales configurado.")
    if not spreadsheet_id or not worksheet_name:
        raise GoogleSheetsDataSourceError(
            "Faltan GOOGLE_SPREADSHEET_ID o GOOGLE_WORKSHEET_NAME para Google Sheets."
        )
    try:
        credentials = Credentials.from_service_account_file(str(credentials_path), scopes=SCOPES)
        service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
        response = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=_worksheet_range(worksheet_name))
            .execute()
        )
    except Exception as error:
        LOGGER.exception("Google Sheets read failed for worksheet=%s", worksheet_name)
        raise GoogleSheetsDataSourceError(
            "No se pudo leer Google Sheets. Verifica las credenciales, permisos, "
            "spreadsheet, pestaña y conexión de red."
        ) from error

    values = response.get("values", [])
    if not values:
        raise GoogleSheetsDataSourceError("La hoja de Google Sheets está vacía.")
    headers = values[0]
    rows = [row + [None] * (len(headers) - len(row)) for row in values[1:]]
    data = pd.DataFrame(rows, columns=headers)
    return _map_headers(data, header_mapping or {})
