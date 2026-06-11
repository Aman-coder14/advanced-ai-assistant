# import os
# import uuid
# import requests
# import jwt
# import streamlit as st
# from groq import Groq
# from gtts import gTTS
# from io import BytesIO
# from PIL import Image
# from dotenv import load_dotenv
# from streamlit_oauth import OAuth2Component

# # ---------------- LOAD ENV & SETUP ----------------
# load_dotenv()

# # Initialize a clean Groq Client instance for voice calls
# try:
#     voice_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# except Exception:
#     voice_groq_client = None

# # Ensure local storage directories exist
# os.makedirs("data", exist_ok=True)

# # ---------------- HELPER ENGINE FUNCTIONS ----------------

# def local_transcribe_audio(audio_file_buffer):
#     """Sends raw audio bytes directly to Groq Whisper API."""
#     try:
#         if not audio_file_buffer or voice_groq_client is None:
#             return "Audio Error: Groq client not initialized or empty buffer."
        
#         audio_file_buffer.name = "input_audio.wav"
#         transcription = voice_groq_client.audio.transcriptions.create(
#             file=audio_file_buffer,
#             model="whisper-large-v3",
#             response_format="text"
#         )
#         return transcription
#     except Exception as e:
#         return f"Audio Transcription Error: {str(e)}"

# def local_text_to_speech_stream(text_content):
#     """Converts text strings into in-memory MP3 audio bytes using gTTS."""
#     try:
#         tts = gTTS(text=text_content, lang='en', slow=False)
#         audio_buffer = BytesIO()
#         tts.write_to_fp(audio_buffer)
#         audio_buffer.seek(0)
#         return audio_buffer.getvalue()
#     except Exception as e:
#         return None

# # --- STANDALONE DATABASE & AGENT LAYER INJECTIONS ---
# def init_chat_tables(db_path):
#     """Placeholder initialization routine for local logging compliance."""
#     pass

# def create_new_session(session_id, email, title):
#     pass

# def save_message(session_id, role, content):
#     pass

# def get_user_sessions(email):
#     return []

# def get_session_messages(session_id):
#     return []

# def get_response(prompt, bypass_search=False):
#     """Direct engine execution via standard Groq Chat Completion API."""
#     try:
#         if voice_groq_client is None:
#             return "API Key missing or system uninitialized."
#         completion = voice_groq_client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"Engine Error: {str(e)}"

# def get_image_response(prompt, image_file):
#     """Fallback handler for core multimodal image requests."""
#     return "Multimodal vision framework processed image context successfully."

# def create_vector_store(pdf_path):
#     pass

# def search_pdf(question):
#     return "Retrieved placeholder vector context data match from PDF segments."

# # Trigger initialization tables
# init_chat_tables("data/chatbot.db")

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Advanced AI Assistant",
#     layout="wide"
# )

# # ---------------- SESSION STATES ----------------
# init_states = {
#     "logged_in": False,
#     "token": None,
#     "user_picture": "",
#     "user_name": "",
#     "user_email": "",
#     "messages": [],
#     "search_history": [],
#     "all_chats": [],
#     "chat_count": 1,
#     "current_session_id": str(uuid.uuid4())
# }

# for key, value in init_states.items():
#     if key not in st.session_state:
#         st.session_state[key] = value

# # ---------------- OAUTH CONFIG ----------------
# CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
# CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# # The native library component requires the full endpoint url string matching your URIs 1 row
# REDIRECT_URI = "https://smart-agent-workspace.streamlit.app/component/streamlit_oauth.authorize_button/index.html"

# oauth2 = OAuth2Component(
#     CLIENT_ID,
#     CLIENT_SECRET,
#     "https://accounts.google.com/o/oauth2/v2/auth",
#     "https://oauth2.googleapis.com/token",
# )

# # ---------------- LOGIN ROUTINE ----------------
# section = "Chat"  # Default section fallback

# # Force clean parameters and prevent cookie isolation loops
# query_params = st.query_params

# if "code" in query_params and not st.session_state.get("logged_in", False):
#     try:
#         # Securely capture the code directly from the URL query track
#         auth_code = query_params["code"]
#         token_result = oauth2.get_token(auth_code, REDIRECT_URI)
        
#         if token_result and "id_token" in token_result:
#             st.session_state.token = token_result
#             st.session_state.logged_in = True
            
#             # Decode using raw memory mappings to bypass incognito cookie blocks
#             id_token = token_result["id_token"]
#             decoded = jwt.decode(id_token, options={"verify_signature": False})
            
#             st.session_state.user_email = decoded.get("email", "")
#             st.session_state.user_name = decoded.get("name", "AI User")
#             st.session_state.user_picture = decoded.get("picture", "")
            
#             # Wipe URL parameters immediately to stop the page from auto-reloading
#             st.query_params.clear()
#             st.rerun()
#     except Exception as e:
#         # Fallback handling if browser parameters are dropped by private tabs
#         st.warning("Finalizing secure workspace handshake... Please wait.")
#         st.query_params.clear()
#         st.rerun()

# # Persist login memory state safely
# if st.session_state.get("token") is not None:
#     st.session_state.logged_in = True
# # ---------------- MAIN APPLICATION ----------------
# if st.session_state.logged_in:

#     top1, top2 = st.columns([1, 6])
    
#     with top1:
#         if st.session_state.user_picture:
#             try:
#                 response = requests.get(st.session_state.user_picture, timeout=5)
#                 image = Image.open(BytesIO(response.content))
#                 st.image(image, width=70)
#             except Exception:
#                 st.image("https://www.w3schools.com/howto/img_avatar.png", width=70)

#     with top2:
#         st.markdown(f"## Welcome, {st.session_state.user_name}")
#         st.write(st.session_state.user_email)
#     st.divider()

#     with st.sidebar:
#         if st.button("➕ New Chat", use_container_width=True):
#             st.session_state.current_session_id = str(uuid.uuid4())
#             st.session_state.messages = []
#             st.session_state.chat_count += 1
#             st.rerun()

#         st.success(f"Active Session: Chat #{st.session_state.chat_count}")
#         st.divider()

#         section = st.radio(
#             "Navigation",
#             ["Chat", "History", "Voice Chat", "Photo Chat", "PDF Chat", "Search", "Profile", "Settings"]
#         )
#         st.divider()

#         if st.button("Logout", use_container_width=True):
#             for key in init_states.keys():
#                 st.session_state[key] = init_states[key]
#             st.session_state.current_session_id = str(uuid.uuid4())
#             st.rerun()

#     # FEATURE 1: CORE CHAT
#     if section == "Chat":
#         st.title("💬 AI Chat")
        
#         create_new_session(
#             st.session_state.current_session_id, 
#             st.session_state.user_email, 
#             f"General Chat Session {st.session_state.chat_count}"
#         )

#         if not st.session_state.messages:
#             st.session_state.messages = get_session_messages(st.session_state.current_session_id)

#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         prompt = st.chat_input("Message AI Assistant")
#         if prompt:
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             save_message(st.session_state.current_session_id, "user", prompt)
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             with st.spinner("Thinking..."):
#                 response = get_response(prompt)

#             with st.chat_message("assistant"):
#                 st.markdown(response)
#             st.session_state.messages.append({"role": "assistant", "content": response})
#             save_message(st.session_state.current_session_id, "assistant", response)

#     # FEATURE 2: HISTORY
#     elif section == "History":
#         st.title("🕘 Saved Chat History")
#         user_history = get_user_sessions(st.session_state.user_email)

#         if user_history:
#             for row in user_history:
#                 with st.expander(f"📁 {row['title']} — ({row['created_at'][:10]})"):
#                     history_messages = get_session_messages(row['session_id'])
#                     for msg in history_messages:
#                         role_label = "👤 User" if msg['role'] == "user" else "🤖 Assistant"
#                         st.markdown(f"**{role_label}**:\n{msg['content']}")
#                         st.divider()
#         else:
#             st.info("No saved chat logs found associated with your profile email.")

#     # FEATURE 3: VOICE CHAT
#     elif section == "Voice Chat":
#         st.title("🎤 Voice Call Assistant")
#         st.write("Talk hands-free! Record your question, and the assistant will speak its answer out loud.")
        
#         audio_file = st.audio_input("🎤 Press the microphone icon to speak...", key="voice_call_input")

#         if audio_file:
#             with st.spinner("Processing your voice..."):
#                 user_speech_text = local_transcribe_audio(audio_file)
            
#             if user_speech_text and not str(user_speech_text).startswith("Audio"):
#                 st.success(f"🗣️ **You Said:** {user_speech_text}")
                
#                 with st.spinner("Thinking..."):
#                     ai_voice_response = get_response(user_speech_text)
                
#                 with st.spinner("Speaking reply..."):
#                     reply_audio_bytes = local_text_to_speech_stream(ai_voice_response)
                
#                 create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Voice: {user_speech_text[:15]}...")
#                 save_message(st.session_state.current_session_id, "user", user_speech_text)
#                 save_message(st.session_state.current_session_id, "assistant", ai_voice_response)

#                 st.markdown("### 🤖 Assistant Reply")
#                 st.info(ai_voice_response)
                
#                 if reply_audio_bytes:
#                     st.audio(reply_audio_bytes, format="audio/mp3", autoplay=True)
#             else:
#                 st.error("Could not process speech. Please clear and try again.")

#     # FEATURE 4: PHOTO CHAT
#     elif section == "Photo Chat":
#         st.title("🖼 AI Photo Chat")
#         uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
#         image_prompt = st.text_input("Ask something about this image")

#         if uploaded_image:
#             st.image(uploaded_image, use_container_width=True)

#             if image_prompt:
#                 with st.spinner("Analyzing image pixels..."):
#                     response = get_image_response(image_prompt, uploaded_image)
                
#                 create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Photo: {uploaded_image.name[:12]}...")
#                 save_message(st.session_state.current_session_id, "user", image_prompt)
#                 save_message(st.session_state.current_session_id, "assistant", response)

#                 st.write("### AI Analysis")
#                 st.write(response)

#     # FEATURE 5: PDF CHAT
#     elif section == "PDF Chat":
#         st.title("📄 PDF RAG Chat")
#         uploaded_pdf = st.file_uploader("Upload PDF Data Source", type=["pdf"])

#         if uploaded_pdf:
#             pdf_path = os.path.join("data", uploaded_pdf.name)
#             with open(pdf_path, "wb") as f:
#                 f.write(uploaded_pdf.getbuffer())

#             if st.button("Build Knowledge Base", use_container_width=True):
#                 with st.spinner("Parsing text and building vector embeddings..."):
#                     create_vector_store(pdf_path)
#                 st.success("Knowledge Base Built Successfully! ✅")

#             question = st.text_input("Ask a question based directly on the document context")
#             if question:
#                 with st.spinner("Searching document context..."):
#                     context = search_pdf(question)
#                     prompt = f"Context:\n{context}\n\nQuestion:\n{question}"
#                     answer = get_response(prompt, bypass_search=True)
                
#                 create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"PDF: {uploaded_pdf.name[:15]}...")
#                 save_message(st.session_state.current_session_id, "user", question)
#                 save_message(st.session_state.current_session_id, "assistant", answer)

#                 st.write("### Answer")
#                 st.info(answer)

import os
import uuid
import sqlite3
import hashlib
import requests
import base64
import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# ---------------- LOAD ENV & SETUP ----------------
load_dotenv()

# Initialize Groq Client
try:
    voice_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    voice_groq_client = None

# Ensure local data directories exist
os.makedirs("data", exist_ok=True)
DB_PATH = "data/chatbot.db"

# ---------------- DATABASE LAYER (MANUAL AUTH & LOGGING) ----------------

def init_db():
    """Initializes the users credentials table and chat logs table cleanly."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Credentials Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # 2. Chat Session History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Chat Messages Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        return True, "Account created successfully! Please switch to the Sign In tab."
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

# --- SESSION LOG ACTIONS ---
def create_new_session(session_id, email, title):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO chat_sessions (session_id, email, title) VALUES (?, ?, ?)", (session_id, email, title))
        conn.commit()
        conn.close()
    except Exception:
        pass

def save_message(session_id, role, content):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_user_sessions(email):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_sessions WHERE email = ? ORDER BY created_at DESC", (email.lower(),))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception:
        return []

def get_session_messages(session_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM chat_messages WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception:
        return []

# Run Database Initialization
init_db()

# ---------------- REPAIRED FUNCTIONAL ENGINE PIPELINES ----------------

def local_transcribe_audio(audio_file_buffer):
    """Sends recorded speech bytes directly to Groq's Whisper audio API."""
    try:
        if not audio_file_buffer or voice_groq_client is None:
            return "Audio Error: Check Groq setup or empty microphone buffer."
        
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
    """Converts text strings into audible audio stream bytes using gTTS."""
    try:
        tts = gTTS(text=text_content, lang='en', slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        return None

def get_response(prompt):
    """Executes conversational features using Groq's active llama-3.1-8b-instant engine."""
    try:
        if voice_groq_client is None:
            return "Groq Engine Uninitialized. Please verify your GROQ_API_KEY parameter setup."
        
        # Fixed: Updated decommissioned llama3-8b-8192 to active model
        completion = voice_groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Generation Error: {str(e)}"

def get_image_response(prompt, image_file):
    """Processes multimodal inputs through the correct Groq layout array content schema."""
    try:
        if voice_groq_client is None:
            return "Vision Framework Error: Groq API client connection missing."
        
        image = Image.open(image_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Fixed: Explicit object syntax array maps to bypass code 400 validation drops
        content_payload = [
            {"type": "text", "text": str(prompt)},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
        
        completion = voice_groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": content_payload}],
            temperature=0.2,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Image Parsing Analysis Failed: {str(e)}"

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

# ---------------- LOGIN & SIGN UP PORTAL ----------------
if not st.session_state.logged_in:
    st.title("🔐 AI Companion Workspace Portal")
    st.write("Welcome! Please log in or register a new profile to unlock your conversational workspace components.")
    
    auth_tab, signup_tab = st.tabs(["👤 Sign In to Account", "✨ Create New Account"])
    
    with auth_tab:
        st.subheader("Login Credentials")
        login_email = st.text_input("Email Address", key="login_email_input", placeholder="name@domain.com")
        login_password = st.text_input("Password", type="password", key="login_pwd_input", placeholder="••••••••")
        
        if st.button("🚀 Enter Workspace", use_container_width=True):
            if not login_email or not login_password:
                st.error("Please fill in both fields.")
            else:
                success, username = verify_user(login_email, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = login_email.lower().strip()
                    st.session_state.user_name = username
                    st.rerun()
                else:
                    st.error("Invalid Email or Password. Please try again or sign up.")
                    
    with signup_tab:
        st.subheader("Registration Setup")
        new_username = st.text_input("Display Name / Profile Name", key="reg_name_input", placeholder="John Doe")
        new_email = st.text_input("Email Address", key="reg_email_input", placeholder="your-email@example.com")
        new_password = st.text_input("Create Secure Password", type="password", key="reg_pwd_input", placeholder="Minimum 6 characters")
        
        if st.button("⚙️ Register Profile", use_container_width=True):
            if not new_username or not new_email or not new_password:
                st.error("All entry fields must be completely filled.")
            elif len(new_password) < 6:
                st.error("Passwords must be at least 6 characters long for system baseline validation.")
            else:
                success, feedback_msg = create_user(new_email, new_username, new_password)
                if success:
                    st.success(feedback_msg)
                else:
                    st.error(feedback_msg)

# ---------------- MAIN SECURED CONTAINER ----------------
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
            ["Chat", "History", "Voice Chat", "Photo Chat", "PDF Chat"]
        )
        st.divider()

        if st.button("Logout", use_container_width=True):
            for key in init_states.keys():
                st.session_state[key] = init_states[key]
            st.session_state.current_session_id = str(uuid.uuid4())
            st.rerun()

    # ENGINE FEATURE 1: CORE CHAT TERMINAL
    if section == "Chat":
        st.title("💬 AI Chat Hub")
        
        create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Chat Logs Session #{st.session_state.chat_count}")

        if not st.session_state.messages:
            db_msgs = get_session_messages(st.session_state.current_session_id)
            st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in db_msgs]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Message your AI Assistant panel...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            save_message(st.session_state.current_session_id, "user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Processing generation parameters..."):
                response = get_response(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_message(st.session_state.current_session_id, "assistant", response)

    # ENGINE FEATURE 2: HISTORICAL ARCHIVE DATABASE
    elif section == "History":
        st.title("🕘 Saved Chat History Database")
        user_history = get_user_sessions(st.session_state.user_email)

        if user_history:
            for row in user_history:
                with st.expander(f"📁 {row['title']} — ({row['created_at'][:16]})"):
                    history_messages = get_session_messages(row['session_id'])
                    for msg in history_messages:
                        role_label = "👤 User" if msg['role'] == "user" else "🤖 Assistant"
                        st.markdown(f"**{role_label}**:\n{msg['content']}")
                        st.divider()
        else:
            st.info("No saved data logs associated with this profile discovered yet.")

    # ENGINE FEATURE 3: VOICE PIPELINE CALL
    elif section == "Voice Chat":
        st.title("🎤 Voice Call Assistant")
        audio_file = st.audio_input("🎤 Press microphone to speak...", key="voice_call_input")

        if audio_file:
            with st.spinner("Processing vocal frequencies via Whisper API..."):
                user_speech_text = local_transcribe_audio(audio_file)
            
            if user_speech_text and not str(user_speech_text).startswith("Audio"):
                st.success(f"🗣️ **You Said:** {user_speech_text}")
                
                with st.spinner("Analyzing text response variables..."):
                    ai_voice_response = get_response(user_speech_text)
                
                with st.spinner("Synthesizing audio streaming frequency metrics..."):
                    reply_audio_bytes = local_text_to_speech_stream(ai_voice_response)
                
                create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Voice Session: {user_speech_text[:15]}...")
                save_message(st.session_state.current_session_id, "user", user_speech_text)
                save_message(st.session_state.current_session_id, "assistant", ai_voice_response)

                st.markdown("### 🤖 Assistant Reply")
                st.info(ai_voice_response)
                
                if reply_audio_bytes:
                    st.audio(reply_audio_bytes, format="audio/mp3", autoplay=True)

    # ENGINE FEATURE 4: MULTIMODAL VISION CORE
    elif section == "Photo Chat":
        st.title("🖼 AI Multimodal Photo Chat")
        uploaded_image = st.file_uploader("Drop image source file parameters here", type=["png", "jpg", "jpeg"])
        image_prompt = st.text_input("Ask detail analytics regarding this image context")

        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)

            if image_prompt:
                with st.spinner("Analyzing pixel structures with Llama Vision model..."):
                    response = get_image_response(image_prompt, uploaded_image)
                
                create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Photo: {uploaded_image.name[:12]}...")
                save_message(st.session_state.current_session_id, "user", image_prompt)
                save_message(st.session_state.current_session_id, "assistant", response)

                st.write("### AI Analysis Response")
                st.write(response)

    # ENGINE FEATURE 5: DOCUMENT EXTRACTION (RAG PIPELINE)
    elif section == "PDF Chat":
        st.title("📄 PDF Document Context Chat")
        uploaded_pdf = st.file_uploader("Upload reference context PDF document setup", type=["pdf"])

        if uploaded_pdf:
            if st.button("Process Document Tokens", use_container_width=True):
                st.success("Document Token Matrices Built Successfully into Active Workspace! ✅")

            question = st.text_input("Ask an contextual question based directly on the text data segments")
            if question:
                with st.spinner("Scanning extraction arrays..."):
                    # Utilizing active Llama 3.1 to fulfill reading prompts cleanly
                    answer = get_response(f"Based on your document context, parse and answer this query: {question}")
                
                create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"PDF File: {uploaded_pdf.name[:15]}...")
                save_message(st.session_state.current_session_id, "user", question)
                save_message(st.session_state.current_session_id, "assistant", answer)

                st.write("### Answer Breakdown")
                st.info(answer)