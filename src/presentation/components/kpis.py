"""KPI presentation components."""

import pandas as pd
import streamlit as st

from application.services.atenciones import calculate_kpis


def render_kpis(data: pd.DataFrame) -> None:
    metrics = calculate_kpis(data)
    columns = st.columns(6)
    columns[0].metric("Total de atenciones", metrics["total"])
    columns[1].metric("Atenciones de hoy", metrics["today"])
    columns[2].metric("Atenciones de la semana", metrics["week"])
    columns[3].metric("Tasa de resolución", f"{metrics['resolution_rate']:.1f}%")
    columns[4].metric("Resolución al primer contacto", f"{metrics['first_contact_rate']:.1f}%")
    columns[5].metric("Casos derivados", metrics["derived"])
