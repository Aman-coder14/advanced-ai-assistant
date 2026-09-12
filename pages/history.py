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
        """
        <div class="page-title">🕐 Chat History</div>
        <div class="page-subtitle">Browse and restore your previous conversations.</div>
        """,
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search conversations",
        placeholder="🔍  Search previous conversations...",
    )
    chats = get_user_chats(user.id, search.strip())
    st.session_state.chat_history = chats

    if not chats:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <div class="empty-state-text">No saved chats found. Start a conversation to see it here.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for chat in chats:
        preview = chat.preview or "No messages in this chat."
        msg_badge = f'<span style="background:rgba(99,102,241,0.15);color:#A5B4FC;padding:2px 8px;border-radius:99px;font-size:11px;font-weight:600;">{chat.message_count} msgs</span>'

        with st.expander(f"  {chat.title}"):
            st.markdown(
                f'<p style="font-family:Inter,sans-serif;font-size:12px;color:#64748B;margin-bottom:8px;">🕐 Last updated: {chat.updated_at} &nbsp; {msg_badge}</p>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<p style="font-family:Inter,sans-serif;font-size:13px;color:#94A3B8;margin-bottom:12px;">{preview}</p>',
                unsafe_allow_html=True,
            )

            for message in load_chat(chat.id):
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            open_col, delete_col = st.columns(2)
            with open_col:
                if st.button("Open in Chat", key=f"open_history_{chat.id}", use_container_width=True):
                    st.session_state.active_chat_id = chat.id
                    st.session_state.messages = load_chat(chat.id)
                    st.session_state.page = "Chat"
                    st.query_params["chat_id"] = chat.id
                    st.rerun()

            with delete_col:
                if st.button("🗑 Delete", key=f"delete_history_{chat.id}", use_container_width=True):
                    delete_chat(chat.id)
                    if st.session_state.get("active_chat_id") == chat.id:
                        next_chat_id = get_latest_or_create_chat(user.id)
                        st.session_state.active_chat_id = next_chat_id
                        st.session_state.messages = load_chat(next_chat_id)
                        st.query_params["chat_id"] = next_chat_id
                    st.session_state.chat_history = get_user_chats(user.id)
                    st.rerun()
