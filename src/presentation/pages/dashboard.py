"""Main dashboard page."""

import os

import streamlit as st

from application.services.atenciones import filter_atenciones, load_atenciones
from application.services.data_source import resolve_data_source
from presentation.components.charts import render_charts
from presentation.components.detail_table import render_detail_table
from presentation.components.filters import render_filters
from presentation.components.kpis import render_kpis


@st.cache_data(show_spinner="Cargando atenciones...")
def _load_data(data_path):
    return load_atenciones(data_path)


def render_dashboard() -> None:
    st.title("Dashboard de atenciones")
    try:
        data_path = resolve_data_source()
        data = _load_data(data_path)
    except (OSError, ValueError, UnicodeError) as error:
        st.error(f"No se pudieron cargar las atenciones. Revisa el archivo de datos. ({error})")
        return

    st.caption(f"Fuente de datos: {data_path}")
    if data_path.parent.exists() and st.button("Abrir carpeta de datos"):
        if hasattr(os, "startfile"):
            os.startfile(data_path.parent)
        else:
            st.info("La apertura automática de carpetas está disponible en Windows.")

    if data.empty:
        st.info("No hay registros válidos en el dataset.")
        return

    start, end, selections, derived = render_filters(data)
    filtered = filter_atenciones(data, start, end, selections, derived)
    render_kpis(filtered)
    render_charts(filtered)
    render_detail_table(filtered)
