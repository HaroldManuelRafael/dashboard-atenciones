"""Filtered detail table with only operationally useful columns."""

import pandas as pd
import streamlit as st

DETAIL_COLUMNS = {
    "fecha_hora": "Fecha",
    "codigo_estudiante": "Código de estudiante",
    "nombre_estudiante": "Nombre del estudiante",
    "campus": "Campus",
    "motivo_consulta": "Motivo",
    "area_responsable": "Área responsable",
    "canal_atencion": "Canal",
    "estado": "Estado",
    "resuelto_primer_contacto": "Resuelto al primer contacto",
    "derivado": "Derivado",
}


def render_detail_table(data: pd.DataFrame) -> None:
    st.subheader("Detalle de atenciones")
    if data.empty:
        st.info("No existen registros para los filtros seleccionados.")
        return
    details = data[list(DETAIL_COLUMNS)].rename(columns=DETAIL_COLUMNS).sort_values("Fecha", ascending=False)
    st.dataframe(details, use_container_width=True, hide_index=True)
