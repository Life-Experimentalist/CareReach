import time

import streamlit as st
from google import genai

from src.db import save_history

_AI_AVATAR = "✨"


def show(username: str) -> None:
    st.subheader("Symptom Checker 🩺")
    st.caption(
        "Describe your symptoms and get an AI-powered analysis. "
        "This is not a substitute for professional medical advice."
    )

    api_key = st.session_state.get("gemini_api_key")
    model_name = st.session_state.get("selected_model")

    if not api_key or not model_name:
        st.info(
            "Enter your **Gemini API Key** in the ⚙️ AI Settings panel on the left to get started. "
            "Get a free key at [aistudio.google.com](https://aistudio.google.com/)."
        )
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "gemini_history" not in st.session_state:
        st.session_state.gemini_history = []

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model=model_name,
        history=st.session_state.gemini_history,
    )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar")):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe your symptoms…"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("ai", avatar=_AI_AVATAR):
            placeholder = st.empty()
            full = ""
            for chunk in chat.send_message_stream(prompt):
                if chunk.text:
                    for word in chunk.text.split(" "):
                        full += word + " "
                        time.sleep(0.04)
                        placeholder.write(full + "▌")
            placeholder.write(full.strip())

        st.session_state.messages.append(
            {"role": "ai", "content": full.strip(), "avatar": _AI_AVATAR}
        )
        st.session_state.gemini_history = chat.history
        save_history(username, symptoms=prompt, analysis=full)
