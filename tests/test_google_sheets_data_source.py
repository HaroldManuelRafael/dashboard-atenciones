import pandas as pd
import pytest

from infrastructure.google_sheets.google_sheets_data_source import (
    GoogleSheetsDataSourceError,
    _map_headers,
    _worksheet_range,
)


def test_worksheet_range_quotes_names_with_spaces_and_quotes():
    assert _worksheet_range("Respuestas de formulario 1") == "'Respuestas de formulario 1'"
    assert _worksheet_range("A'B") == "'A''B'"


def test_example_headers_are_mapped_without_affecting_unknown_columns():
    data = pd.DataFrame(columns=["Marca temporal", "Código del estudiante", "Otro"])

    mapped = _map_headers(data, {})

    assert list(mapped.columns) == ["fecha_hora", "codigo_estudiante", "Otro"]


def test_missing_credentials_is_user_facing_error(tmp_path):
    from infrastructure.google_sheets.google_sheets_data_source import load_google_sheet

    with pytest.raises(GoogleSheetsDataSourceError, match="credenciales"):
        load_google_sheet("sheet-id", "Hoja", tmp_path / "missing.json")
