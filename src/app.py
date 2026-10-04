"""Streamlit entry point."""

import streamlit as st

from presentation.pages.dashboard import render_dashboard

st.set_page_config(page_title="Dashboard de atenciones", page_icon="📊", layout="wide")
render_dashboard()
