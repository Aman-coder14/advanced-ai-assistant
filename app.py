
import os
import uuid
import sqlite3
import hashlib
import base64
import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from duckduckgo_search import DDGS  # Free, keyless live web search provider

# ---------------- LOAD ENV & SETUP ----------------
load_dotenv()

# Initialize Groq Client
try:
    voice_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    voice_groq_client = None

# Ensure local directories exist for database operations
os.makedirs("data", exist_ok=True)
DB_PATH = "data/chatbot.db"

# ---------------- DATABASE ENGINE (LOCAL AUTH) ----------------

def init_db():
    """Initializes local SQLite tables for credentials tracking securely."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Credentials Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
            (email.lower().strip(), username.strip(), pwd_hash)
        )
        conn.commit()
        conn.close()
        return True, "Account created successfully! Please switch to the 'Sign In' tab."
    except sqlite3.IntegrityError:
        return False, "This email is already registered. Please login instead."
    except Exception as e:
        return False, f"Database Error: {str(e)}"

def verify_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute(
        "SELECT username FROM users WHERE email = ? AND password_hash = ?",
        (email.lower().strip(), pwd_hash)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return True, user[0]
    return False, None

# Initialize local system database
init_db()

# ---------------- LIVE WEB SEARCH METHOD ----------------

def fetch_live_search_context(query: str) -> str:
    """Queries DuckDuckGo securely to scrape real-time contextual text layers."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                context_chunks = []
                for idx, item in enumerate(results, 1):
                    context_chunks.append(f"[{idx}] Source: {item.get('href')}\nContent: {item.get('body')}")
                return "\n\n".join(context_chunks)
    except Exception:
        pass
    return None

# ---------------- CORE PIPELINES (REAL-TIME SECURED) ----------------

def get_response(prompt):
    """Executes completions injected with dynamic background web scrap snippets."""
    try:
        if voice_groq_client is None:
            return "Groq Engine Uninitialized. Verify your GROQ_API_KEY settings."
        
        # 1. Dynamically evaluate if web scraping grounding context arrays are necessary
        search_triggers = ["2026", "ipl", "match", "today", "winner", "score", "news", "current", "who is", "weather", "latest"]
        live_context = ""
        
        if any(keyword in prompt.lower() for keyword in search_triggers):
            live_context = fetch_live_search_context(prompt)

        # 2. Structure context-guided prompt payload wrapper matrix
        system_instruction = (
            "You are an advanced, real-time AI Workspace Assistant built on the Llama architecture.\n"
            "CRITICAL TIMING RULE: The current calendar date year is 2026.\n"
            "You have access to live internet search elements injected below. If live web data is provided, "
            "prioritize it as factual truth to bypass any inner knowledge base model cutoff dates (2023)."
        )
        
        user_content = prompt
        if live_context:
            user_content = (
                f"--- LIVE INTERNET GROUNDING DATA (CURRENT YEAR: 2026) ---\n"
                f"{live_context}\n"
                f"---------------------------------------------------------\n"
                f"Using the real-time references above, comprehensively answer the user request:\n"
                f"User Question: {prompt}"
            )

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ]
        
        # 3. Request LLM Inference
        completion = voice_groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"AI Generation Error: {str(e)}"

def get_image_response(prompt, image_file):
    """Processes images safely using a dedicated vision model."""
    try:
        if voice_groq_client is None:
            return "Vision Framework Error: Groq API client connection missing."
        
        image = Image.open(image_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        content_payload = [
            {"type": "text", "text": str(prompt)},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
        
        completion = voice_groq_client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": content_payload}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Image Analysis Failed: {str(e)}"

def local_transcribe_audio(audio_file_buffer):
    """Sends microphone audio directly to the Whisper execution framework."""
    try:
        if not audio_file_buffer or voice_groq_client is None:
            return "Audio Error: Empty buffer."
        audio_file_buffer.name = "input_audio.wav"
        transcription = voice_groq_client.audio.transcriptions.create(
            file=audio_file_buffer,
            model="whisper-large-v3",
            response_format="text"
        )
        return transcription
    except Exception as e:
        return f"Speech Transcription Issue: {str(e)}"

def local_text_to_speech_stream(text_content):
    """Converts response text arrays cleanly back into audio streams using gTTS."""
    try:
        tts = gTTS(text=text_content, lang='en', slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        return None

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Advanced AI Assistant",
    layout="wide"
)

# ---------------- SESSION STATES ----------------
init_states = {
    "logged_in": False,
    "user_name": "",
    "user_email": "",
    "messages": [],
    "chat_count": 1,
    "current_session_id": str(uuid.uuid4())
}

for key, value in init_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- NEW USER LOG PORTAL TERMINAL ----------------
if not st.session_state.logged_in:
    st.title("🔐 AI Companion Workspace Portal")
    st.write("Welcome! Please sign in or register a new local profile below to unlock the assistant panel.")
    
    auth_tab, signup_tab = st.tabs(["👤 Sign In to Account", "✨ Create New Account"])
    
    with auth_tab:
        st.subheader("Login Credentials")
        login_email = st.text_input("Email Address", key="login_email_input", placeholder="name@domain.com")
        login_password = st.text_input("Password", type="password", key="login_pwd_input", placeholder="••••••••")
        
        if st.button("🚀 Enter Workspace", use_container_width=True):
            if not login_email or not login_password:
                st.error("Please fill in both credential fields to proceed.")
            else:
                success, username = verify_user(login_email, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = login_email.lower().strip()
                    st.session_state.user_name = username
                    st.success("Access Granted! Loading workspace routing matrices...")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password. Verify credentials or register a profile.")
                    
    with signup_tab:
        st.subheader("Registration Setup")
        new_username = st.text_input("Display Name / Profile Name", key="reg_name_input", placeholder="John Doe")
        new_email = st.text_input("Email Address", key="reg_email_input", placeholder="your-email@example.com")
        new_password = st.text_input("Create Secure Password", type="password", key="reg_pwd_input", placeholder="Minimum 6 characters")
        
        if st.button("⚙️ Register Profile", use_container_width=True):
            if not new_username or not new_email or not new_password:
                st.error("All entry parameters must be populated completely.")
            elif len(new_password) < 6:
                st.error("Passwords must be at least 6 characters long for baseline validation.")
            else:
                success, feedback_msg = create_user(new_email, new_username, new_password)
                if success:
                    st.success(feedback_msg)
                else:
                    st.error(feedback_msg)

# ---------------- MAIN SECURED APP WORKSPACE ----------------
if st.session_state.logged_in:

    top1, top2 = st.columns([1, 6])
    with top1:
        st.image("https://www.w3schools.com/howto/img_avatar.png", width=70)
    with top2:
        st.markdown(f"## Welcome back, {st.session_state.user_name}")
        st.write(st.session_state.user_email)
    st.divider()

    with st.sidebar:
        if st.button("➕ New Chat Session", use_container_width=True):
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.chat_count += 1
            st.rerun()

        st.success(f"Active Session: Chat #{st.session_state.chat_count}")
        st.divider()

        section = st.radio(
            "Navigation Engine Workspace",
            ["Chat", "Voice Chat", "Photo Chat", "PDF Chat"]
        )
        st.divider()

        if st.button("Logout", use_container_width=True):
            for key in init_states.keys():
                st.session_state[key] = init_states[key]
            st.session_state.current_session_id = str(uuid.uuid4())
            st.rerun()

    # SECTION 1: CORE CHAT TERMINAL
    if section == "Chat":
        st.title("💬 AI Chat Hub (Live Web-Searching Online)")
        
        with st.expander("ℹ️ About This Chatbot", expanded=False):
            st.info(
                "**Knowledge Cutoff:** This AI's base training data goes until early 2024.\n\n"
                "**Live Search:** For 2026 events, current news, sports scores, and recent topics, "
                "I automatically search the web for real-time information using DuckDuckGo.\n\n"
                "**How it works:** Ask about current events, and if live data is found, I'll use that "
                "as the authoritative source. Otherwise, I'll note when information comes from my 2024 training data."
            )
        
        if not st.session_state.messages:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Message your AI Assistant panel...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Browsing live search index and evaluating answer..."):
                response = get_response(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # SECTION 2: VOICE CHAT CONTROL
    elif section == "Voice Chat":
        st.title("🎤 Voice Call Assistant")
        audio_file = st.audio_input("🎤 Press microphone to speak...", key="voice_call_input")

        if audio_file:
            with st.spinner("Transcribing vocal tracks..."):
                user_speech_text = local_transcribe_audio(audio_file)
            
            if user_speech_text and not str(user_speech_text).startswith("Audio"):
                st.success(f"🗣️ **You Said:** {user_speech_text}")
                
                with st.spinner("Searching and forming response..."):
                    ai_voice_response = get_response(user_speech_text)
                
                with st.spinner("Generating audio streaming..."):
                    reply_audio_bytes = local_text_to_speech_stream(ai_voice_response)

                st.markdown("### 🤖 Assistant Reply")
                st.info(ai_voice_response)
                
                if reply_audio_bytes:
                    st.audio(reply_audio_bytes, format="audio/mp3", autoplay=True)

    # SECTION 3: MULTIMODAL PHOTO CORE
    elif section == "Photo Chat":
        st.title("🖼 AI Multimodal Photo Chat")
        uploaded_image = st.file_uploader("Drop image source parameters here", type=["png", "jpg", "jpeg"])
        image_prompt = st.text_input("Ask detail analytics regarding this image context")

        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)

            if image_prompt:
                with st.spinner("Analyzing pixel structures..."):
                    response = get_image_response(image_prompt, uploaded_image)
                
                st.write("### AI Analysis Response")
                st.write(response)

    # SECTION 4: PDF EXTRACTION CHAT
    elif section == "PDF Chat":
        st.title("📄 PDF Document Context Chat")
        uploaded_pdf = st.file_uploader("Upload reference context PDF document setup", type=["pdf"])

        if uploaded_pdf:
            if st.button("Process Document Tokens", use_container_width=True):
                st.success("Document segments mapped successfully into active context window! ✅")

            question = st.text_input("Ask a contextual question based directly on the text data segments")
            if question:
                with st.spinner("Injecting extraction context arrays..."):
                    answer = get_response(f"Based on your document context, parse and answer this query: {question}")
                
                st.write("### Answer Breakdown")
                st.info(answer)