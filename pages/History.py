import streamlit as st

from chatbot.database import get_all_chats

st.title("🕘 Chat History")

chats = get_all_chats()

for chat in chats:

    st.write("User:", chat[1])

    st.write("AI:", chat[2])

    st.divider()