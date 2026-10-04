"""Main dashboard page."""

from pathlib import Path

import streamlit as st

from application.services.atenciones import filter_atenciones, load_atenciones
from presentation.components.charts import render_charts
from presentation.components.detail_table import render_detail_table
from presentation.components.filters import render_filters
from presentation.components.kpis import render_kpis

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "sample_atenciones.csv"


@st.cache_data(show_spinner="Cargando atenciones...")
def _load_data():
    return load_atenciones(DATA_PATH)


def render_dashboard() -> None:
    st.title("Dashboard de atenciones")
    try:
        data = _load_data()
    except (OSError, ValueError, UnicodeError) as error:
        st.error(f"No se pudieron cargar las atenciones. Revisa el archivo de datos. ({error})")
        return

    if data.empty:
        st.info("No hay registros válidos en el dataset.")
        return

    start, end, selections, derived = render_filters(data)
    filtered = filter_atenciones(data, start, end, selections, derived)
    render_kpis(filtered)
    render_charts(filtered)
    render_detail_table(filtered)
