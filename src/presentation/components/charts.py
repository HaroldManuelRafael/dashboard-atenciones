"""Plotly charts for filtered atenciones."""

import pandas as pd
import plotly.express as px
import streamlit as st


def _bar(data: pd.DataFrame, column: str, title: str, *, limit: int | None = None) -> None:
    counts = data[column].fillna("Sin dato").value_counts().rename_axis(column).reset_index(name="Atenciones")
    if limit:
        counts = counts.head(limit)
    if counts.empty:
        st.info("No hay datos para mostrar en este gráfico.")
        return
    figure = px.bar(counts, x=column, y="Atenciones", title=title)
    figure.update_layout(xaxis_title=None, yaxis_title="Atenciones")
    st.plotly_chart(figure, use_container_width=True)


def render_charts(data: pd.DataFrame) -> None:
    if data.empty:
        st.info("No existen registros para los filtros seleccionados.")
        return

    daily = data.assign(fecha=data["fecha_hora"].dt.date).groupby("fecha").size().reset_index(name="Atenciones")
    figure = px.line(daily, x="fecha", y="Atenciones", markers=True, title="Atenciones por día")
    figure.update_layout(xaxis_title="Fecha", yaxis_title="Atenciones")
    st.plotly_chart(figure, use_container_width=True)

    left, right = st.columns(2)
    with left:
        _bar(data, "campus", "Atenciones por campus")
        _bar(data, "area_responsable", "Atenciones por área responsable")
        _bar(data, "estado", "Estado de resolución")
    with right:
        _bar(data, "lugar_atencion", "Atenciones por lugar de atención")
        _bar(data, "motivo_consulta", "Top 10 motivos de consulta", limit=10)
