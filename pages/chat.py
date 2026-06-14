import streamlit as st

from database.database import (
    add_message,
    create_chat,
    delete_chat,
    get_chat,
    list_chats,
    messages_as_dicts,
    rename_chat,
)
from modules.llm import generate_response


WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Hello Aman, how can I help you today?",
}


def _user_id():
    return st.session_state.get("user_email", "default")


def _new_chat():
    chat_id = create_chat(_user_id())
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = [WELCOME_MESSAGE.copy()]


def _load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    messages = messages_as_dicts(chat_id)
    st.session_state.messages = messages or [WELCOME_MESSAGE.copy()]


def show_chat():
    st.markdown(
        '<div class="page-title">AI Chat</div>',
        unsafe_allow_html=True,
    )

    if "current_chat_id" not in st.session_state:
        chats = list_chats(_user_id())
        if chats:
            _load_chat(chats[0]["id"])
        else:
            _new_chat()

    if "messages" not in st.session_state:
        _load_chat(st.session_state.current_chat_id)

    left, right = st.columns([1, 4])

    with left:
        st.subheader("Chats")

        if st.button("New Chat"):
            _new_chat()
            st.rerun()

        current_chat = get_chat(st.session_state.current_chat_id)
        current_title = current_chat["title"] if current_chat else "New Chat"
        new_title = st.text_input("Chat title", value=current_title)

        if st.button("Rename"):
            rename_chat(st.session_state.current_chat_id, new_title)
            st.rerun()

        if st.button("Delete"):
            delete_chat(st.session_state.current_chat_id)
            st.session_state.pop("messages", None)
            st.session_state.pop("current_chat_id", None)
            st.rerun()

        st.divider()

        for chat in list_chats(_user_id()):
            if st.button(chat["title"], key=f"chat_{chat['id']}"):
                _load_chat(chat["id"])
                st.rerun()

    with right:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Type your message...")

        if prompt:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )
            add_message(st.session_state.current_chat_id, "user", prompt)

            current_chat = get_chat(st.session_state.current_chat_id)
            if current_chat and current_chat["title"] == "New Chat":
                rename_chat(st.session_state.current_chat_id, prompt[:50])

            try:
                context_text = st.session_state.get("uploaded_pdf_text", "")
                if context_text:
                    truncated = context_text[:10000]
                    composed_prompt = (
                        "You are answering based on the uploaded PDF.\n\n"
                        f"PDF Content:\n{truncated}\n\n"
                        f"Question:\n{prompt}\n\n"
                        "Answer only from the PDF content.\n"
                        "If the answer is not present, say:\n"
                        '"The answer was not found in the uploaded document."'
                    )
                else:
                    composed_prompt = prompt

                with st.spinner("Thinking..."):
                    assistant_response = generate_response(composed_prompt)

                if context_text:
                    assistant_response = (
                        f"{assistant_response}\n\n"
                        "Answer generated from uploaded PDF"
                    )
            except Exception as exc:
                assistant_response = (
                    "I'm sorry, I couldn't generate a response right now. "
                    "Please try again in a moment."
                )
                st.error(f"AI service error: {exc}")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_response,
                }
            )
            add_message(
                st.session_state.current_chat_id,
                "assistant",
                assistant_response,
            )

            st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            st.button("Copy Last Response")

        with col2:
            if st.button("Clear Chat"):
                delete_chat(st.session_state.current_chat_id)
                _new_chat()
                st.rerun()
