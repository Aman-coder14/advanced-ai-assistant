import streamlit as st
import traceback

from modules.llm import generate_response, get_ai_debug_status
from modules.voice_service import synthesize_text_to_speech, transcribe_audio
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
        """
        <div class="page-title">💬 AI Chat</div>
        <div class="page-subtitle">Ask anything — your AI is ready.</div>
        """,
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
    try:
        st.session_state.messages = load_chat(chat_id)
    except Exception:
        st.session_state.messages = []
    _refresh_chat_history()
    st.query_params["chat_id"] = chat_id


def _refresh_chat_history(search: str = "") -> None:
    user_id = st.session_state.user_id
    try:
        st.session_state.chat_history = get_user_chats(user_id, search)
    except Exception:
        st.session_state.chat_history = []


def _render_chat_sidebar(user_id: str) -> None:
    st.markdown('<div style="font-family:Inter,sans-serif;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#64748B;margin-bottom:10px;">💬 Conversations</div>', unsafe_allow_html=True)

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

    active_chat = None
    try:
        active_chat = get_chat(st.session_state.active_chat_id)
    except Exception:
        pass
        
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
                try:
                    rename_chat(st.session_state.active_chat_id, new_title)
                except Exception:
                    pass
                _refresh_chat_history(search)
                st.rerun()
        with delete_col:
            if st.button("Delete", use_container_width=True):
                _delete_active_chat(user_id)
                st.rerun()

    st.divider()

    chat_history = st.session_state.get("chat_history", [])
    if not chat_history:
        st.caption("No chats found.")
        return

    for chat in chat_history:
        is_active = chat.id == st.session_state.active_chat_id
        label = chat.title if not is_active else f"> {chat.title}"
        if st.button(label, key=f"chat_nav_{chat.id}", use_container_width=True):
            _set_active_chat(chat.id)
            st.rerun()
        if chat.preview:
            st.caption(chat.preview[:70])


def _render_chat_window(user_id: str) -> None:
    active_chat = None
    try:
        active_chat = get_chat(st.session_state.active_chat_id)
    except Exception:
        pass
        
    title = active_chat.title if active_chat else "New Chat"
    st.subheader(title)

    messages = st.session_state.get("messages", [])
    if not messages:
        st.info("Start this conversation with a message.")

    for message in messages:
        _render_message(message["role"], message["content"])

    if "voice_transcript" not in st.session_state:
        st.session_state.voice_transcript = ""
    if "voice_upload_name" not in st.session_state:
        st.session_state.voice_upload_name = ""
    if "last_ai_audio" not in st.session_state:
        st.session_state.last_ai_audio = None

    with st.expander("Voice Chat", expanded=False):
        audio_file = st.file_uploader(
            "Upload voice message",
            type=["wav", "mp3", "m4a", "ogg"],
            key="voice_upload",
        )
        if audio_file:
            if st.session_state.voice_upload_name != audio_file.name:
                st.session_state.voice_upload_name = audio_file.name
                st.session_state.voice_transcript = ""
            if not st.session_state.voice_transcript:
                try:
                    with st.spinner("Transcribing voice..."):
                        st.session_state.voice_transcript = transcribe_audio(audio_file)
                except Exception as exc:
                    st.error(f"Voice transcription failed: {exc}")
                    st.session_state.voice_transcript = ""

        st.text_area(
            "Transcribed text",
            value=st.session_state.voice_transcript,
            height=130,
            key="voice_transcript",
        )

        with st.form(key="voice_text_form", clear_on_submit=True):
            voice_text = st.text_input("Say (type) and press Enter", key="voice_text_input")
            submitted = st.form_submit_button("Send")
            if submitted and voice_text and voice_text.strip():
                st.session_state.voice_prompt = voice_text.strip()

        if st.button("Send transcribed voice", use_container_width=True, key="send_voice"):
            st.session_state.voice_prompt = st.session_state.voice_transcript.strip()

        st.checkbox(
            "Play AI response audio",
            value=st.session_state.get("play_ai_audio", False),
            key="play_ai_audio",
        )

    prompt = None
    typed_prompt = st.chat_input("Type your message...")
    if st.session_state.get("voice_prompt"):
        prompt = st.session_state.voice_prompt
        st.session_state.voice_prompt = ""
    elif typed_prompt and typed_prompt.strip():
        prompt = typed_prompt.strip()

    if prompt:
        chat_id = st.session_state.active_chat_id

        if not chat_id:
            st.session_state.last_ai_exception = "Missing active_chat_id."
            st.error("AI Error: Missing active chat id.")
            return

        st.session_state.last_ai_exception = ""

        # 1. Save User Message to Database
        try:
            st.session_state.last_ai_status = "Before save_message"
            save_message(chat_id, "user", prompt)
            st.session_state.last_ai_status = "After save_message"
        except Exception as e:
            st.error(f"Save error: {e}")

        # 2. Query AI Model Pipeline
        try:
            context_text = st.session_state.get("uploaded_pdf_text", "")
            composed_prompt = _build_prompt(prompt, context_text)

            st.session_state.last_ai_status = "Calling generate_response"
            with st.spinner("Thinking..."):
                assistant_response = generate_response(composed_prompt)

            if context_text:
                assistant_response += "\n\nAnswer generated from uploaded PDF"

            assistant_response = (assistant_response or "").strip()
            if not assistant_response:
                assistant_response = "I received your message, but the AI service returned an empty response."

            # 3. Save Assistant Response to Database
            try:
                st.session_state.last_ai_status = "Saving assistant message"
                save_message(chat_id, "assistant", assistant_response)
                st.session_state.last_ai_status = "Assistant message saved"
            except Exception as e:
                st.warning(f"Assistant save warning: {e}")

            if st.session_state.get("play_ai_audio"):
                try:
                    st.session_state.last_ai_audio = synthesize_text_to_speech(assistant_response)
                except Exception as audio_exc:
                    st.warning(f"Audio response generation failed: {audio_exc}")

        except Exception as exc:
            error_trace = traceback.format_exc()
            st.session_state.last_ai_exception = error_trace
            st.session_state.last_ai_status = "Chat send failed"
            st.error(f"AI Error: {exc}")

        # 4. Sync State and Force Refresh Interface
        try:
            st.session_state.messages = load_chat(chat_id)
        except Exception:
            pass

        _refresh_chat_history()
        st.rerun()

    if st.session_state.last_ai_audio:
        st.audio(st.session_state.last_ai_audio, format="audio/mp3")

    st.divider()
    if st.button("Clear Chat"):
        try:
            clear_chat(st.session_state.active_chat_id)
        except Exception:
            pass
        st.session_state.messages = []
        st.session_state.last_ai_exception = ""
        _refresh_chat_history()
        st.success("Current chat messages cleared.")
        st.rerun()

    _render_debug_panel()


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
        css_class = "chat-msg-ai"
        label = "🤖 &nbsp;AI Assistant"
    else:
        css_class = "chat-msg-user"
        label = "👤 &nbsp;You"

    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="chat-msg-label">{label}</div>
            <div class="chat-msg-content">{_escape_html(content)}</div>
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
    try:
        delete_chat(st.session_state.active_chat_id)
    except Exception:
        pass
    try:
        next_chat_id = get_latest_or_create_chat(user_id)
        _set_active_chat(next_chat_id)
    except Exception:
        pass