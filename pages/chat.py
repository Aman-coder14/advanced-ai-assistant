import streamlit as st
import traceback

from modules.llm import generate_response, get_ai_debug_status
from services.chat_service import (
    clear_chat,
    create_new_chat,
    delete_chat,
    get_chat,
    get_latest_or_create_chat,
    get_or_create_user,
    get_user_chats,
    load_chat,
    rename_chat,
    save_message,
)


def show_chat():
    user_id = _ensure_user()
    _ensure_active_chat(user_id)

    st.markdown(
        '<div class="page-title">AI Chat</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 3.8])

    with left:
        _render_chat_sidebar(user_id)

    with right:
        _render_chat_window(user_id)


def _ensure_user() -> str:
    email = st.session_state.get("user_email", "default")
    user = get_or_create_user(email=email)
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email
    return user.id


def _ensure_active_chat(user_id: str) -> None:
    active_chat_id = st.session_state.get("active_chat_id")
    query_chat_id = st.query_params.get("chat_id")
    if query_chat_id:
        active_chat_id = query_chat_id

    if active_chat_id:
        chat = get_chat(active_chat_id)
        if chat and chat.user_id == user_id:
            _set_active_chat(active_chat_id)
            return

    latest_chat_id = get_latest_or_create_chat(user_id)
    _set_active_chat(latest_chat_id)


def _set_active_chat(chat_id: str) -> None:
    st.session_state.active_chat_id = chat_id
    st.session_state.messages = load_chat(chat_id)
    _refresh_chat_history()
    st.query_params["chat_id"] = chat_id


def _refresh_chat_history(search: str = "") -> None:
    user_id = st.session_state.user_id
    st.session_state.chat_history = get_user_chats(user_id, search)


def _render_chat_sidebar(user_id: str) -> None:
    st.subheader("Chats")

    if st.button("New Chat", use_container_width=True):
        chat_id = create_new_chat(user_id)
        _set_active_chat(chat_id)
        st.rerun()

    search = st.text_input(
        "Search Chats",
        placeholder="Search history...",
        key="chat_search",
    )
    _refresh_chat_history(search)

    active_chat = get_chat(st.session_state.active_chat_id)
    current_title = active_chat.title if active_chat else "New Chat"

    with st.expander("Manage Active Chat", expanded=False):
        new_title = st.text_input(
            "Chat title",
            value=current_title,
            key=f"title_{st.session_state.active_chat_id}",
        )
        rename_col, delete_col = st.columns(2)
        with rename_col:
            if st.button("Rename", use_container_width=True):
                rename_chat(st.session_state.active_chat_id, new_title)
                _refresh_chat_history(search)
                st.rerun()
        with delete_col:
            if st.button("Delete", use_container_width=True):
                _delete_active_chat(user_id)
                st.rerun()

    st.divider()

    if not st.session_state.chat_history:
        st.caption("No chats found.")
        return

    for chat in st.session_state.chat_history:
        is_active = chat.id == st.session_state.active_chat_id
        label = chat.title if not is_active else f"> {chat.title}"
        if st.button(label, key=f"chat_nav_{chat.id}", use_container_width=True):
            _set_active_chat(chat.id)
            st.rerun()
        if chat.preview:
            st.caption(chat.preview[:70])


def _render_chat_window(user_id: str) -> None:
    active_chat = get_chat(st.session_state.active_chat_id)
    title = active_chat.title if active_chat else "New Chat"
    st.subheader(title)

    messages = load_chat(st.session_state.active_chat_id)
    st.session_state.messages = messages
    if not messages:
        st.info("Start this conversation with a message.")

    for message in messages:
        _render_message(message["role"], message["content"])

    prompt = st.chat_input("Type your message...")
    if prompt and prompt.strip():
        _send_message(prompt.strip())
        st.rerun()

    st.divider()
    if st.button("Clear Chat"):
        clear_chat(st.session_state.active_chat_id)
        st.session_state.messages = []
        st.session_state.last_ai_exception = ""
        _refresh_chat_history()
        st.success("Current chat messages cleared.")
        st.rerun()

    _render_debug_panel()


def _send_message(prompt: str) -> None:
    chat_id = st.session_state.active_chat_id
    if not chat_id:
        st.session_state.last_ai_exception = "Missing active_chat_id."
        st.error("AI Error: Missing active chat id.")
        return

    st.session_state.last_ai_exception = ""
    try:
        st.session_state.last_ai_status = "Saving user message"
        save_message(chat_id, "user", prompt)

        context_text = st.session_state.get("uploaded_pdf_text", "")
        composed_prompt = _build_prompt(prompt, context_text)

        st.session_state.last_ai_status = "Calling generate_response"
        print(f"[CHAT] Calling generate_response for chat_id={chat_id}")
        with st.spinner("Thinking..."):
            assistant_response = generate_response(composed_prompt)
        print(f"[CHAT] AI response received for chat_id={chat_id}")

        if context_text:
            assistant_response = (
                f"{assistant_response}\n\n"
                "Answer generated from uploaded PDF"
            )
        assistant_response = (assistant_response or "").strip()
        if not assistant_response:
            assistant_response = (
                "I received your message, but the AI service returned an empty "
                "response. Please try again."
            )

        st.session_state.last_ai_status = "Saving assistant message"
        save_message(chat_id, "assistant", assistant_response)
        st.session_state.last_ai_status = "Assistant message saved"
    except Exception as exc:
        error_trace = traceback.format_exc()
        st.session_state.last_ai_exception = error_trace
        st.session_state.last_ai_status = "Chat send failed"
        assistant_response = (
            "AI Error: I could not generate a response.\n\n"
            f"{exc}"
        )
        st.error(f"AI Error: {exc}")
        st.code(error_trace)
        try:
            save_message(chat_id, "assistant", assistant_response)
        except Exception:
            st.session_state.last_ai_exception += "\n\nFailed to save assistant error:\n"
            st.session_state.last_ai_exception += traceback.format_exc()

    st.session_state.messages = load_chat(chat_id)
    _refresh_chat_history()


def _build_prompt(prompt: str, context_text: str) -> str:
    if not context_text:
        return prompt

    truncated = context_text[:10000]
    return (
        "You are answering based on the uploaded PDF.\n\n"
        f"PDF Content:\n{truncated}\n\n"
        f"Question:\n{prompt}\n\n"
        "Answer only from the PDF content.\n"
        "If the answer is not present, say:\n"
        '"The answer was not found in the uploaded document."'
    )


def _render_message(role: str, content: str) -> None:
    if role == "assistant":
        label = "AI"
        background = "#182033"
        border = "#31568f"
    else:
        label = "You"
        background = "#1b1f2a"
        border = "#30363d"

    st.markdown(
        f"""
        <div style="
            border: 1px solid {border};
            background: {background};
            border-radius: 8px;
            padding: 12px 14px;
            margin: 10px 0;
        ">
            <div style="font-size: 12px; color: #9CA3AF; margin-bottom: 6px;">
                {label}
            </div>
            <div style="white-space: pre-wrap; color: white;">{_escape_html(content)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _escape_html(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _render_debug_panel() -> None:
    status = get_ai_debug_status()
    messages = st.session_state.get("messages", [])
    last_exception = st.session_state.get("last_ai_exception", "")

    with st.expander("Debug Panel", expanded=bool(last_exception)):
        st.write(f"Current chat id: {st.session_state.get('active_chat_id', 'missing')}")
        st.write(f"Number of messages: {len(messages)}")
        st.write(f"Selected provider: {status.get('provider') or 'none'}")
        st.write(f"GROQ_API_KEY detected: {status.get('groq_key')}")
        st.write(f"GEMINI_API_KEY detected: {status.get('gemini_key')}")
        st.write(f"OPENAI_API_KEY detected: {status.get('openai_key')}")
        st.write(f"SERPER_API_KEY detected: {status.get('serper_key')}")
        st.write(f"Last AI status: {st.session_state.get('last_ai_status', 'idle')}")
        if last_exception:
            st.error("Last exception")
            st.code(last_exception)


def _delete_active_chat(user_id: str) -> None:
    delete_chat(st.session_state.active_chat_id)
    next_chat_id = get_latest_or_create_chat(user_id)
    _set_active_chat(next_chat_id)
