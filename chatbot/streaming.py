import time
import streamlit as st


def stream_text(text):

    placeholder = st.empty()

    output = ""

    for word in text.split():

        output += word + " "

        placeholder.markdown(output)

        time.sleep(0.05)