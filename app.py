import streamlit as st

from src.db import init_db
from src.auth import show_login, show_signup
from src.pages import chatbot, appointment, history

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
        if st.sidebar.button("Logout", use_container_width=True):
            for key in ("logged_in", "username", "messages", "gemini_history"):
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
