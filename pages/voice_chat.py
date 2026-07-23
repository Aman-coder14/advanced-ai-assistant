import streamlit as st
import streamlit.components.v1 as components
import json
import traceback

from modules.llm import generate_response
try:
    from modules.voice_service import synthesize_text_to_speech, clean_text_for_speech
except ImportError:
    import re
    from modules.voice_service import synthesize_text_to_speech

    def clean_text_for_speech(text: str) -> str:
        if not text:
            return ""
        cleaned = re.sub(r"```[\s\S]*?```", " Code snippet omitted. ", text)
        cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
        cleaned = re.sub(r"\*+([^\*]+)\*+", r"\1", cleaned)
        cleaned = re.sub(r"_+([^_]+)_+", r"\1", cleaned)
        cleaned = re.sub(r"^#+\s+", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", cleaned)
        cleaned = re.sub(r"https?://\S+", "", cleaned)
        return re.sub(r"\s+", " ", cleaned).strip()
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


def show_voice_chat():
    user_id = _ensure_user()
    _ensure_active_chat(user_id)

    # State initialization
    if "voice_status" not in st.session_state:
        st.session_state.voice_status = "idle"  # idle, listening, processing, speaking
    if "auto_speak" not in st.session_state:
        st.session_state.auto_speak = True
    if "last_spoken_text" not in st.session_state:
        st.session_state.last_spoken_text = ""
    if "voice_input_text" not in st.session_state:
        st.session_state.voice_input_text = ""

    # Header Card
    st.markdown(
        f"""
        <div class="voice-header-card">
            <div>
                <h2 style="margin:0; font-size: 26px; color: white;">🎙️ Voice Chat</h2>
                <div style="font-size: 13px; color: #8B949E; margin-top: 4px;">
                    ChatGPT & Gemini Live Style Continuous Voice Assistant
                </div>
            </div>
            <div>
                <span class="voice-status-pill status-{st.session_state.voice_status}">
                    ● {st.session_state.voice_status.upper()}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1.2, 3.8])

    with left_col:
        _render_voice_sidebar(user_id)

    with right_col:
        _render_voice_chat_window(user_id)


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


def _render_voice_sidebar(user_id: str) -> None:
    st.subheader("Voice Sessions")

    if st.button("➕ New Voice Chat", use_container_width=True, key="new_voice_chat_btn"):
        chat_id = create_new_chat(user_id)
        _set_active_chat(chat_id)
        st.rerun()

    search = st.text_input(
        "Search Sessions",
        placeholder="Search history...",
        key="voice_chat_search",
    )
    _refresh_chat_history(search)

    active_chat = None
    try:
        active_chat = get_chat(st.session_state.active_chat_id)
    except Exception:
        pass

    current_title = active_chat.title if active_chat else "New Voice Chat"

    with st.expander("Manage Session", expanded=False):
        new_title = st.text_input(
            "Session title",
            value=current_title,
            key=f"voice_title_{st.session_state.active_chat_id}",
        )
        rename_col, delete_col = st.columns(2)
        with rename_col:
            if st.button("Rename", use_container_width=True, key="rename_voice_session"):
                try:
                    rename_chat(st.session_state.active_chat_id, new_title)
                except Exception:
                    pass
                _refresh_chat_history(search)
                st.rerun()
        with delete_col:
            if st.button("Delete", use_container_width=True, key="delete_voice_session"):
                try:
                    delete_chat(st.session_state.active_chat_id)
                    next_id = get_latest_or_create_chat(user_id)
                    _set_active_chat(next_id)
                except Exception:
                    pass
                st.rerun()

    st.divider()

    st.subheader("Voice Settings")
    st.checkbox(
        "🔊 Auto-speak AI responses",
        value=st.session_state.auto_speak,
        key="auto_speak_toggle",
    )

    st.divider()

    chat_history = st.session_state.get("chat_history", [])
    if not chat_history:
        st.caption("No past sessions found.")
        return

    for chat in chat_history:
        is_active = chat.id == st.session_state.active_chat_id
        label = f"🎙️ {chat.title}" if not is_active else f"👉 🎙️ {chat.title}"
        if st.button(label, key=f"voice_nav_{chat.id}", use_container_width=True):
            _set_active_chat(chat.id)
            st.rerun()


def _render_voice_chat_window(user_id: str) -> None:
    active_chat = None
    try:
        active_chat = get_chat(st.session_state.active_chat_id)
    except Exception:
        pass

    title = active_chat.title if active_chat else "New Voice Session"
    st.markdown(f"### {title}")

    # Messages Display Container
    messages = st.session_state.get("messages", [])
    chat_container = st.container()
    with chat_container:
        if not messages:
            st.info("👋 Welcome to Voice Chat! Tap the microphone button below or type a message to start.")

        for msg in messages:
            _render_message_bubble(msg["role"], msg["content"])

    st.divider()

    # Voice Input Console with Web Speech API Component
    _render_web_speech_console()


def _render_message_bubble(role: str, content: str) -> None:
    if role == "assistant":
        bg = "#1F2937"
        border = "#374151"
        avatar = "🤖 AI Assistant"
    else:
        bg = "#1E3A8A"
        border = "#2563EB"
        avatar = "🎙️ You"

    st.markdown(
        f"""
        <div style="
            background: {bg};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 14px 18px;
            margin: 10px 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <div style="font-size: 12px; font-weight: 600; color: #9CA3AF; margin-bottom: 6px;">
                {avatar}
            </div>
            <div style="font-size: 15px; color: #F9FAFB; white-space: pre-wrap; line-height: 1.5;">
                {_escape_html(content)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_web_speech_console() -> None:
    # 1. Interactive Form for submitting speech/text prompt
    with st.form(key="voice_chat_form", clear_on_submit=True):
        user_prompt = st.text_input(
            "Speech Transcript / Type Message",
            placeholder="Click the Mic button to speak, or type here...",
            key="voice_input_box",
        )
        col_send, col_stop = st.columns([4, 1])
        with col_send:
            submitted = st.form_submit_button("🚀 Send Message", use_container_width=True)

    # Handle text or speech submission
    if submitted and user_prompt and user_prompt.strip():
        _process_voice_prompt(user_prompt.strip())

    # 2. Web Speech API JavaScript Live Controller Component
    js_component = """
    <div style="text-align: center; padding: 10px; font-family: sans-serif;">
        <button id="micBtn" onclick="toggleMic()" style="
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
            border: none;
            color: white;
            font-size: 32px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
            transition: all 0.3s ease;
        ">🎙️</button>
        <div id="micStatus" style="margin-top: 10px; font-size: 14px; color: #9CA3AF; font-weight: bold;">
            Click Microphone to Speak
        </div>
    </div>

    <script>
    let recognition = null;
    let isListening = false;

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            isListening = true;
            document.getElementById('micBtn').style.transform = 'scale(1.1)';
            document.getElementById('micBtn').style.boxShadow = '0 0 35px rgba(239, 68, 68, 0.8)';
            document.getElementById('micStatus').innerText = '🎙️ Listening... Speak now!';
            document.getElementById('micStatus').style.color = '#EF4444';
        };

        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            // Put transcript into parent Streamlit text input box if found
            const parentInputs = window.parent.document.querySelectorAll('input[type="text"]');
            parentInputs.forEach(input => {
                if (input.placeholder && input.placeholder.includes('Mic')) {
                    input.value = transcript;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            document.getElementById('micStatus').innerText = 'Mic error: ' + event.error;
            stopMic();
        };

        recognition.onend = function() {
            stopMic();
        };
    } else {
        document.getElementById('micStatus').innerText = 'Web Speech API not supported in this browser.';
    }

    function toggleMic() {
        if (!recognition) return;
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }

    function stopMic() {
        isListening = false;
        document.getElementById('micBtn').style.transform = 'scale(1)';
        document.getElementById('micBtn').style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.4)';
        document.getElementById('micStatus').innerText = 'Click Microphone to Speak';
        document.getElementById('micStatus').style.color = '#9CA3AF';
    }
    </script>
    """
    components.html(js_component, height=140)

    # 3. Speech Synthesis Output Controller (if auto-speak enabled)
    messages = st.session_state.get("messages", [])
    if messages and messages[-1]["role"] == "assistant" and st.session_state.auto_speak:
        last_msg = messages[-1]["content"]
        clean_text = clean_text_for_speech(last_msg)
        if clean_text and st.session_state.get("last_spoken_text") != clean_text:
            st.session_state.last_spoken_text = clean_text
            tts_js = f"""
            <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance({json.dumps(clean_text)});
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            }}
            </script>
            """
            components.html(tts_js, height=0)


def _process_voice_prompt(prompt: str) -> None:
    chat_id = st.session_state.active_chat_id
    if not chat_id:
        st.error("Error: Active session missing.")
        return

    st.session_state.voice_status = "processing"

    try:
        # Save User Message to Database
        save_message(chat_id, "user", prompt)

        # Generate Response using existing AI pipeline
        with st.spinner("AI is thinking..."):
            response = generate_response(prompt)

        response = (response or "").strip()
        if not response:
            response = "I received your message, but could not generate a response."

        # Save AI Response to Database
        save_message(chat_id, "assistant", response)

        st.session_state.voice_status = "speaking"

    except Exception as exc:
        st.error(f"Error generating AI response: {exc}")
        st.session_state.voice_status = "idle"

    # Refresh chat state
    try:
        st.session_state.messages = load_chat(chat_id)
    except Exception:
        pass

    _refresh_chat_history()
    st.rerun()


def _escape_html(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
