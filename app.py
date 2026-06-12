import streamlit as st
from google import genai

from src.auth import show_login, show_signup
from src.db import init_db
from src.pages import appointment, chatbot, history

_SIDEBAR_MD = """
## CareReach 🏥

AI-powered telemedicine for remote consultations.

---
- 🩺 **Symptom Checker** — describe symptoms, get analysis
- 📅 **Book Appointment** — find hospitals near you
- 📋 **Health History** — review past consultations

---
*Not a substitute for professional medical advice.*
"""


def _fetch_models(api_key: str) -> list[str]:
    client = genai.Client(api_key=api_key)
    models = []
    for m in client.models.list():
        name = m.name or ""
        if "gemini" in name.lower():
            models.append(name.removeprefix("models/"))
    return sorted(models)


def _gemini_settings_sidebar() -> None:
    st.sidebar.divider()
    with st.sidebar.expander(
        "⚙️ AI Settings", expanded=not st.session_state.get("gemini_api_key")
    ):
        key_input = st.text_input(
            "Your Gemini API Key",
            type="password",
            placeholder="AIza…",
            help="Free at aistudio.google.com — stays in your browser session only.",
            value=st.session_state.get("gemini_api_key", ""),
        )
        if st.button("Apply", use_container_width=True):
            if not key_input:
                for k in ("gemini_api_key", "gemini_models", "selected_model"):
                    st.session_state.pop(k, None)
                st.rerun()
            else:
                with st.spinner("Fetching available models…"):
                    try:
                        models = _fetch_models(key_input)
                        if not models:
                            st.error("No Gemini models found for this key.")
                        else:
                            st.session_state.gemini_api_key = key_input
                            st.session_state.gemini_models = models
                            if st.session_state.get("selected_model") not in models:
                                st.session_state.selected_model = models[0]
                            st.session_state.pop("messages", None)
                            st.session_state.pop("gemini_history", None)
                            st.rerun()
                    except Exception as exc:
                        st.error(f"Invalid key or API error: {exc}")

        if st.session_state.get("gemini_models"):
            models = st.session_state.gemini_models
            current = st.session_state.get("selected_model", models[0])
            idx = models.index(current) if current in models else 0
            chosen = st.selectbox("Model", models, index=idx)
            if chosen != st.session_state.get("selected_model"):
                st.session_state.selected_model = chosen
                st.session_state.pop("messages", None)
                st.session_state.pop("gemini_history", None)
                st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="CareReach",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_db()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

    st.sidebar.markdown(_SIDEBAR_MD)

    if st.session_state.logged_in:
        st.sidebar.write(f"👤 **{st.session_state.username}**")
        page = st.sidebar.selectbox(
            "Navigate",
            ["Symptom Checker", "Book Appointment", "Health History"],
        )
        _gemini_settings_sidebar()

        if st.sidebar.button("Logout", use_container_width=True):
            for key in (
                "logged_in", "username", "messages", "gemini_history",
                "gemini_api_key", "gemini_models", "selected_model",
            ):
                st.session_state.pop(key, None)
            st.rerun()

        st.title(f"Welcome back, {st.session_state.username}! 👋")

        if page == "Symptom Checker":
            chatbot.show(st.session_state.username)
        elif page == "Book Appointment":
            appointment.show(st.session_state.username)
        elif page == "Health History":
            history.show(st.session_state.username)
    else:
        page = st.sidebar.radio("Account", ["Login", "Sign Up"])
        if page == "Login":
            show_login()
        else:
            show_signup()


if __name__ == "__main__":
    main()
