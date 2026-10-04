from datetime import date

import pandas as pd
import pytest

from application.services.atenciones import (
    calculate_kpis,
    filter_atenciones,
    load_atenciones,
    normalize_atenciones,
)

SAMPLE_PATH = "data/sample_atenciones.csv"


def test_loads_sample_and_preserves_student_codes_as_text():
    data = load_atenciones(SAMPLE_PATH)

    assert len(data) == 30
    assert data.loc[0, "codigo_estudiante"] == "E0001"
    assert data.loc[0, "campus"] == "Huancayo"


def test_normalization_handles_whitespace_categories_booleans_and_invalid_dates():
    raw = pd.DataFrame(
        {
            "fecha_hora": ["2026-10-03 09:00", "fecha inválida"],
            "codigo_estudiante": [" E0001 ", "E0002"],
            "nombre_estudiante": [" Ana   Torres ", "Luis"],
            "campus": [" HUANCAYO ", "Cusco"],
            "motivo_consulta": [" Consulta ", "Otro"],
            "estado": [" resuelto ", "Pendiente"],
            "derivado": [" Sí ", "no"],
            "resuelto_primer_contacto": ["SI", "NO"],
        }
    )

    result = normalize_atenciones(raw)

    assert len(result) == 1
    assert result.loc[0, "nombre_estudiante"] == "Ana Torres"
    assert result.loc[0, "campus"] == "Huancayo"
    assert result.loc[0, "estado"] == "Resuelto"
    assert result.loc[0, "derivado"]
    assert result.loc[0, "resuelto_primer_contacto"]
    assert pd.isna(result.loc[0, "celular"])


def test_missing_required_columns_raise_a_clear_error():
    with pytest.raises(ValueError, match="Faltan columnas obligatorias"):
        normalize_atenciones(pd.DataFrame({"fecha_hora": []}))


def test_filters_apply_date_categories_and_derived_status():
    data = load_atenciones(SAMPLE_PATH)

    result = filter_atenciones(
        data,
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 3),
        selections={"Campus": ["Cusco"], "Estado": ["Resuelto"]},
        derived="No",
    )

    assert len(result) == 3
    assert result["campus"].eq("Cusco").all()
    assert result["estado"].eq("Resuelto").all()
    assert result["derivado"].eq(False).all()


def test_kpis_use_filtered_denominator_and_monday_week_start():
    data = load_atenciones(SAMPLE_PATH)
    metrics = calculate_kpis(data, today=date(2026, 10, 3))

    assert metrics == {
        "total": 30,
        "today": 5,
        "week": 30,
        "resolution_rate": pytest.approx(19 / 30 * 100),
        "first_contact_rate": pytest.approx(60.0),
        "derived": 11,
    }
    filtered = filter_atenciones(data, selections={"Campus": ["Cusco"]})
    assert calculate_kpis(filtered, today=date(2026, 10, 3))["total"] == 6


def test_empty_kpis_are_zero_and_empty_filters_stay_empty():
    data = load_atenciones(SAMPLE_PATH)
    empty = filter_atenciones(data, selections={"Campus": ["No existe"]})

    assert empty.empty
    assert calculate_kpis(empty, today=date(2026, 10, 3)) == {
        "total": 0,
        "today": 0,
        "week": 0,
        "resolution_rate": 0.0,
        "first_contact_rate": 0.0,
        "derived": 0,
    }
