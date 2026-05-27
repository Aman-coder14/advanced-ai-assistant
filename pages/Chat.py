import streamlit as st

from chatbot.llm import get_response
from chatbot.database import save_chat
from chatbot.streaming import stream_text

st.title("💬 AI Chat")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask Anything")

if user_input:

    st.chat_message("user").write(user_input)

    response = get_response(user_input)

    st.chat_message("assistant").write(response)

    save_chat(user_input, response)

    st.session_state.history.append((user_input, response))