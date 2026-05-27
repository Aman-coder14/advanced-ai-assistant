import streamlit as st

from chatbot.database import get_all_chats

st.title("🔍 Search Chats")

query = st.text_input("Search")

chats = get_all_chats()

if query:

    for chat in chats:

        if query.lower() in chat[1].lower():

            st.write(chat[1])
            st.write(chat[2])
            st.divider()