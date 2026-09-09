import streamlit as st

from services.chat_service import (
    delete_chat,
    get_latest_or_create_chat,
    get_or_create_user,
    get_user_chats,
    load_chat,
)


def show_history():
    user = get_or_create_user(st.session_state.get("user_email", "default"))
    st.session_state.user_id = user.id

    st.markdown(
        '<div class="page-title">Chat History</div>',
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search Chats",
        placeholder="Search previous conversations...",
    )
    chats = get_user_chats(user.id, search.strip())
    st.session_state.chat_history = chats

    if not chats:
        st.info("No saved chats found.")
        return

    for chat in chats:
        preview = chat.preview or "No messages in this chat."
        with st.expander(f"{chat.title} - {chat.message_count} messages"):
            st.caption(f"Last updated: {chat.updated_at}")
            st.write(preview)

            for message in load_chat(chat.id):
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            open_col, delete_col = st.columns(2)
            with open_col:
                if st.button("Open in Chat", key=f"open_history_{chat.id}"):
                    st.session_state.active_chat_id = chat.id
                    st.session_state.messages = load_chat(chat.id)
                    st.session_state.page = "Chat"
                    st.query_params["chat_id"] = chat.id
                    st.rerun()

            with delete_col:
                if st.button("Delete", key=f"delete_history_{chat.id}"):
                    delete_chat(chat.id)
                    if st.session_state.get("active_chat_id") == chat.id:
                        next_chat_id = get_latest_or_create_chat(user.id)
                        st.session_state.active_chat_id = next_chat_id
                        st.session_state.messages = load_chat(next_chat_id)
                        st.query_params["chat_id"] = next_chat_id
                    st.session_state.chat_history = get_user_chats(user.id)
                    st.rerun()
