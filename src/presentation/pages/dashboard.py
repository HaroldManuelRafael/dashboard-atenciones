"""Main dashboard page."""

import os
import zipfile

import streamlit as st

from application.services.atenciones import (
    filter_atenciones,
    load_atenciones,
    normalize_google_sheet,
)
from application.services.data_source import (
    GOOGLE_SERVICE_ACCOUNT_FILE_ENV,
    GOOGLE_SPREADSHEET_ID_ENV,
    GOOGLE_WORKSHEET_NAME_ENV,
    configured_data_source,
    resolve_data_source,
)
from infrastructure.google_sheets.google_sheets_data_source import load_google_sheet
from presentation.components.charts import render_charts
from presentation.components.detail_table import render_detail_table
from presentation.components.filters import render_filters
from presentation.components.kpis import render_kpis


@st.cache_data(show_spinner="Cargando atenciones...")
def _load_data(source, data_path=None):
    if source == "local":
        return load_atenciones(data_path)
    remote = load_google_sheet(
        os.environ.get(GOOGLE_SPREADSHEET_ID_ENV, ""),
        os.environ.get(GOOGLE_WORKSHEET_NAME_ENV, ""),
        os.environ.get(GOOGLE_SERVICE_ACCOUNT_FILE_ENV, ""),
    )
    return normalize_google_sheet(remote)


def render_dashboard() -> None:
    st.title("Dashboard de atenciones")
    try:
        source = configured_data_source()
        data_path = resolve_data_source() if source == "local" else None
        data = _load_data(source, data_path)
    except (OSError, ValueError, UnicodeError, ImportError, zipfile.BadZipFile, RuntimeError) as error:
        st.error(f"No se pudieron cargar las atenciones. Revisa el archivo de datos. ({error})")
        return

    if source == "local":
        st.caption(f"Fuente de datos: Excel local | Ruta: {data_path}")
    else:
        st.caption(f"Fuente de datos: Google Sheets | Hoja: {os.environ.get(GOOGLE_WORKSHEET_NAME_ENV, '')}")
    if data_path and data_path.parent.exists() and st.button("Abrir carpeta de datos"):
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
