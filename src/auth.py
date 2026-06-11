import streamlit as st

from src.db import authenticate_user, add_user


def show_login() -> None:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.warning("Please enter your username and password.")
        elif authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password.")


def show_signup() -> None:
    st.title("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up", use_container_width=True):
        if not username or not password:
            st.warning("Please fill out all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif add_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Username already exists. Please choose another.")
