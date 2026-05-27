import streamlit as st

from chatbot.voice import listen_voice
from chatbot.voice import speak
from chatbot.llm import get_response

st.title("🎤 Voice Assistant")

if st.button("Start Voice Chat"):

    text = listen_voice()

    st.write("You Said:", text)

    response = get_response(text)

    st.write(response)

    speak(response)