import streamlit as st
from chatbot.database import get_all_chats

st.title("🕘 Chat History")

chats = get_all_chats()

if chats:
    for chat in chats:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.caption(f"📅 {chat.get('created_at', 'N/A')[:10]}")
        
        with st.expander(f"💬 Chat #{chats.index(chat) + 1}"):
            st.write("**User:**")
            st.info(chat.get('user_message', 'N/A'))
            
            st.write("**AI Response:**")
            st.success(chat.get('ai_response', 'N/A'))
            
        st.divider()
else:
    st.info("No chat history available yet. Start a conversation in Chat to see history here.")