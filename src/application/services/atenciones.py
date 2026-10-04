"""Carga, normalización, filtros y métricas de atenciones."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "fecha_hora",
    "codigo_estudiante",
    "nombre_estudiante",
    "campus",
    "motivo_consulta",
    "estado",
}
OPTIONAL_COLUMNS = {
    "correo",
    "celular",
    "detalle_consulta",
    "area_responsable",
    "canal_atencion",
    "lugar_atencion",
    "resuelto_primer_contacto",
    "derivado",
    "area_derivacion",
    "observacion",
}
TEXT_COLUMNS = (REQUIRED_COLUMNS | OPTIONAL_COLUMNS) - {
    "fecha_hora",
    "resuelto_primer_contacto",
    "derivado",
}
FILTER_COLUMNS = {
    "Campus": "campus",
    "Lugar de atención": "lugar_atencion",
    "Canal de atención": "canal_atencion",
    "Área responsable": "area_responsable",
    "Motivo de consulta": "motivo_consulta",
    "Estado": "estado",
}


def _normalize_text(value: object) -> str | None:
    if pd.isna(value):
        return None
    normalized = " ".join(str(value).split())
    return normalized or None


def _normalize_category(value: object) -> str | None:
    normalized = _normalize_text(value)
    if normalized is None:
        return None
    if normalized.casefold() in {"resuelto", "pendiente", "derivado"}:
        return normalized.capitalize()
    if normalized.isupper():
        return normalized.title()
    return normalized


def _normalize_bool(value: object) -> bool | None:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    normalized = str(value).strip().casefold()
    if normalized in {"si", "sí", "s", "true", "1", "yes"}:
        return True
    if normalized in {"no", "n", "false", "0"}:
        return False
    return None


def normalize_atenciones(data: pd.DataFrame) -> pd.DataFrame:
    """Return a normalized copy conforming to the internal data contract."""
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {', '.join(sorted(missing))}")

    normalized = data.copy()
    for column in OPTIONAL_COLUMNS - set(normalized.columns):
        normalized[column] = None
    normalized["fecha_hora"] = pd.to_datetime(
        normalized["fecha_hora"], errors="coerce", dayfirst=False, format="mixed"
    ).astype("datetime64[ns]")
    for column in TEXT_COLUMNS:
        normalized[column] = normalized[column].map(_normalize_text)
    for column in ("campus", "estado"):
        normalized[column] = normalized[column].map(_normalize_category)
    for column in ("resuelto_primer_contacto", "derivado"):
        normalized[column] = pd.array(
            normalized[column].map(_normalize_bool), dtype="boolean"
        )

    # Filas sin fecha, estudiante o motivo no pueden representar atenciones válidas.
    normalized = normalized.dropna(
        subset=["fecha_hora", "codigo_estudiante", "nombre_estudiante", "campus", "motivo_consulta", "estado"]
    ).reset_index(drop=True)
    return normalized


def load_atenciones(path: str | Path) -> pd.DataFrame:
    """Load the local CSV while preserving identifier columns as text."""
    data = pd.read_csv(path, dtype={"codigo_estudiante": "string", "celular": "string"})
    return normalize_atenciones(data)


def filter_atenciones(
    data: pd.DataFrame,
    start_date: date | None = None,
    end_date: date | None = None,
    selections: dict[str, list[str]] | None = None,
    derived: str = "Todos",
) -> pd.DataFrame:
    """Apply inclusive date and category filters to normalized records."""
    filtered = data
    if start_date:
        filtered = filtered[filtered["fecha_hora"].dt.date >= start_date]
    if end_date:
        filtered = filtered[filtered["fecha_hora"].dt.date <= end_date]
    for label, values in (selections or {}).items():
        column = FILTER_COLUMNS[label]
        if values:
            filtered = filtered[filtered[column].isin(values)]
    if derived == "Sí":
        filtered = filtered[filtered["derivado"].eq(True)]
    elif derived == "No":
        filtered = filtered[filtered["derivado"].eq(False)]
    return filtered.copy()


def calculate_kpis(data: pd.DataFrame, today: date | None = None) -> dict[str, int | float]:
    """Calculate dashboard KPIs; week starts on Monday."""
    reference = today or datetime.now(timezone.utc).date()
    dates = data["fecha_hora"].dt.date
    week_start = reference - timedelta(days=reference.weekday())
    total = len(data)
    resolved = int(data["estado"].eq("Resuelto").sum())
    first_contact = int(data["resuelto_primer_contacto"].eq(True).sum())
    return {
        "total": total,
        "today": int(dates.eq(reference).sum()),
        "week": int((dates >= week_start).mul(dates <= reference).sum()),
        "resolution_rate": resolved / total * 100 if total else 0.0,
        "first_contact_rate": first_contact / total * 100 if total else 0.0,
        "derived": int(data["derivado"].eq(True).sum()),
    }
