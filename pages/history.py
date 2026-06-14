import streamlit as st

from database.database import delete_chat, list_chats, messages_as_dicts


def _user_id():
    return st.session_state.get("user_email", "default")


def show_history():
    st.markdown(
        '<div class="page-title">Chat History</div>',
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search Chats",
        placeholder="Search previous conversations...",
    )

    chats = list_chats(_user_id(), search.strip())

    if not chats:
        st.info("No saved chats found.")
        return

    for chat in chats:
        title = chat["title"]
        updated_at = chat["updated_at"]
        message_count = chat["message_count"]
        preview = chat["preview"] or "No user messages yet."

        with st.expander(f"{title} - {message_count} messages"):
            st.caption(f"Last updated: {updated_at}")
            st.write(preview)

            for message in messages_as_dicts(chat["id"]):
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            open_col, delete_col = st.columns(2)
            with open_col:
                if st.button("Open in Chat", key=f"open_history_{chat['id']}"):
                    st.session_state.current_chat_id = chat["id"]
                    st.session_state.messages = messages_as_dicts(chat["id"])
                    st.session_state.page = "Chat"
                    st.rerun()

            with delete_col:
                if st.button("Delete", key=f"delete_history_{chat['id']}"):
                    delete_chat(chat["id"])
                    if st.session_state.get("current_chat_id") == chat["id"]:
                        st.session_state.pop("current_chat_id", None)
                        st.session_state.pop("messages", None)
                    st.rerun()
