import streamlit as st

from src.db import fetch_history


def show(username: str) -> None:
    st.subheader("Health History 📋")
    records = fetch_history(username)

    if not records:
        st.info("No history yet. Use the Symptom Checker to get started.")
        return

    for symptoms, analysis, timestamp in records:
        with st.container(border=True):
            st.write(f"**Symptoms:** {symptoms}")
            st.write(f"**Status:** {analysis}")
            st.caption(f"🕐 {timestamp}")
