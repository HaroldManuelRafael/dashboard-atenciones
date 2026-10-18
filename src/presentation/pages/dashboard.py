"""Main dashboard page."""

import os
import zipfile

import streamlit as st

from application.services.atenciones import (
    filter_atenciones,
    load_atenciones,
    normalize_google_sheet,
)
from application.services.data_source import resolve_data_source
from application.services.settings import Settings, resolve_settings, save_settings
from infrastructure.google_sheets.google_sheets_data_source import load_google_sheet
from presentation.components.charts import render_charts
from presentation.components.detail_table import render_detail_table
from presentation.components.filters import render_filters
from presentation.components.kpis import render_kpis


@st.cache_data(show_spinner="Cargando atenciones...")
def _load_data(settings: Settings, data_path=None):
    source = settings.data_source
    if source == "local":
        return load_atenciones(data_path)
    remote = load_google_sheet(
        settings.spreadsheet_id,
        settings.worksheet_name,
        settings.google_service_account_file,
    )
    return normalize_google_sheet(remote)


def _render_settings(settings: Settings) -> Settings:
    with st.sidebar.expander("Configuración de fuente", expanded=False):
        source_label = st.selectbox(
            "Fuente de datos",
            ["Excel local", "Google Sheets"],
            index=0 if settings.data_source == "local" else 1,
        )
        source = "local" if source_label == "Excel local" else "google_sheets"
        spreadsheet_id = st.text_input("Spreadsheet ID", value=settings.spreadsheet_id, disabled=source == "local")
        worksheet_name = st.text_input("Nombre de la hoja", value=settings.worksheet_name, disabled=source == "local")
        credentials_file = st.text_input(
            "Ruta del JSON de cuenta de servicio",
            value=settings.google_service_account_file,
            disabled=source == "local",
        )
        if source == "local":
            st.caption(f"Excel activo: {resolve_data_source()}")
        if st.button("Guardar configuración"):
            candidate = Settings(source, spreadsheet_id.strip(), worksheet_name.strip(), credentials_file.strip())
            try:
                save_settings(candidate)
            except (OSError, ValueError) as error:
                st.error(str(error))
            else:
                st.cache_data.clear()
                st.rerun()
    return settings


def render_dashboard() -> None:
    st.title("Dashboard de atenciones")
    try:
        settings = resolve_settings()
        _render_settings(settings)
        data_path = resolve_data_source() if settings.data_source == "local" else None
        data = _load_data(settings, data_path)
    except (OSError, ValueError, UnicodeError, ImportError, zipfile.BadZipFile, RuntimeError) as error:
        st.error(f"No se pudieron cargar las atenciones. Revisa el archivo de datos. ({error})")
        return

    if settings.data_source == "local":
        st.caption(f"Fuente de datos: Excel local | Ruta: {data_path}")
    else:
        st.caption(f"Fuente de datos: Google Sheets | Hoja: {settings.worksheet_name}")
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
