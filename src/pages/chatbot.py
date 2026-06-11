import os
import time

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

from src.db import save_history

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])

_MODEL = "gemini-1.5-flash"
_AI_AVATAR = "✨"


def show(username: str) -> None:
    st.subheader("Symptom Checker 🩺")
    st.caption(
        "Describe your symptoms and get an AI-powered analysis. "
        "This is not a substitute for professional medical advice."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "gemini_history" not in st.session_state:
        st.session_state.gemini_history = []

    model = genai.GenerativeModel(_MODEL)
    chat = model.start_chat(history=st.session_state.gemini_history)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar")):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe your symptoms…"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = chat.send_message(prompt, stream=True)

        with st.chat_message("ai", avatar=_AI_AVATAR):
            placeholder = st.empty()
            full = ""
            for chunk in response:
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
