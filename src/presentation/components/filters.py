"""Streamlit filter controls for the dashboard."""

from datetime import date, datetime, timezone

import pandas as pd
import streamlit as st

from application.services.atenciones import FILTER_COLUMNS


def render_filters(data: pd.DataFrame) -> tuple[date | None, date | None, dict[str, list[str]], str]:
    st.sidebar.header("Filtros")
    today = datetime.now(timezone.utc).date()
    min_date = data["fecha_hora"].min().date() if not data.empty else today
    max_date = data["fecha_hora"].max().date() if not data.empty else today
    date_range = st.sidebar.date_input(
        "Rango de fechas", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    if isinstance(date_range, (tuple, list)):
        start_date = date_range[0] if date_range else None
        end_date = date_range[1] if len(date_range) > 1 else start_date
    else:
        start_date = end_date = date_range

    selections: dict[str, list[str]] = {}
    for label, column in FILTER_COLUMNS.items():
        values = sorted(data[column].dropna().unique().tolist())
        selections[label] = st.sidebar.multiselect(label, values)
    derived = st.sidebar.selectbox("Derivación", ["Todos", "Sí", "No"])
    return start_date, end_date, selections, derived
