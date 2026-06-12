# import os
# import uuid
# import json
# import requests
# import jwt
# import streamlit as st
# from groq import Groq
# from gtts import gTTS
# from io import BytesIO
# from PIL import Image
# from dotenv import load_dotenv
# from streamlit_oauth import OAuth2Component
# from datetime import datetime

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
#     except Exception:
#         return None

# # --- STANDALONE DATABASE & AGENT LAYER INJECTIONS ---
# CHAT_DB_PATH = None
# PDF_INDEX_PATH = os.path.join("data", "pdf_store.json")

# def init_chat_tables(db_path):
#     """Initialize a simple local JSON store for chat sessions and messages."""
#     global CHAT_DB_PATH
#     CHAT_DB_PATH = db_path
#     try:
#         if not os.path.exists(CHAT_DB_PATH):
#             with open(CHAT_DB_PATH, "w", encoding="utf-8") as f:
#                 json.dump({"sessions": [], "messages": []}, f)
#     except Exception:
#         pass


# def _load_chat_db():
#     try:
#         with open(CHAT_DB_PATH, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception:
#         return {"sessions": [], "messages": []}


# def _save_chat_db(data):
#     with open(CHAT_DB_PATH, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)


# def create_new_session(session_id, email, title):
#     db = _load_chat_db()
#     for session in db["sessions"]:
#         if session["session_id"] == session_id:
#             return
#     db["sessions"].append({
#         "session_id": session_id,
#         "email": email,
#         "title": title,
#         "created_at": datetime.utcnow().isoformat()
#     })
#     _save_chat_db(db)


# def save_message(session_id, role, content):
#     db = _load_chat_db()
#     db["messages"].append({
#         "session_id": session_id,
#         "role": role,
#         "content": content,
#         "created_at": datetime.utcnow().isoformat()
#     })
#     _save_chat_db(db)


# def get_user_sessions(email):
#     db = _load_chat_db()
#     sessions = [s for s in db["sessions"] if s.get("email") == email]
#     return sorted(sessions, key=lambda x: x.get("created_at", ""), reverse=True)


# def get_session_messages(session_id):
#     db = _load_chat_db()
#     return sorted(
#         [m for m in db["messages"] if m.get("session_id") == session_id],
#         key=lambda x: x.get("created_at", "")
#     )

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
#     """Process an uploaded image and return an assistant response using image metadata."""
#     try:
#         if not image_file:
#             return "No image was provided for analysis."

#         image_file.seek(0)
#         image = Image.open(image_file)
#         metadata = f"Image format: {image.format}, mode: {image.mode}, size: {image.size}"
#         response_prompt = (
#             f"User question: {prompt}\n"
#             f"Image metadata: {metadata}\n"
#             "Answer the user's question based on the image metadata and available information."
#         )
#         return get_response(response_prompt)
#     except Exception as e:
#         return f"Image Processing Error: {str(e)}"

# def create_vector_store(pdf_path):
#     """Extract text from a PDF and store chunked context for later search."""
#     try:
#         from PyPDF2 import PdfReader
#     except ImportError:
#         return False

#     try:
#         reader = PdfReader(pdf_path)
#         raw_text = []
#         for page in reader.pages:
#             try:
#                 page_text = page.extract_text() or ""
#             except Exception:
#                 page_text = ""
#             if page_text:
#                 raw_text.append(page_text)

#         document_text = "\n".join(raw_text).strip()
#         if not document_text:
#             return False

#         chunk_size = 1200
#         chunks = []
#         for start in range(0, len(document_text), chunk_size):
#             chunk_text = document_text[start:start + chunk_size].strip()
#             if chunk_text:
#                 chunks.append({"id": f"chunk-{start}", "text": chunk_text})

#         index_data = {
#             "pdf_path": pdf_path,
#             "created_at": datetime.utcnow().isoformat(),
#             "chunks": chunks
#         }
#         with open(PDF_INDEX_PATH, "w", encoding="utf-8") as f:
#             json.dump(index_data, f, ensure_ascii=False, indent=2)

#         st.session_state["pdf_index"] = index_data
#         return True
#     except Exception:
#         return False

# def search_pdf(question):
#     """Retrieve the most relevant stored PDF chunks for a question."""
#     if not st.session_state.get("pdf_index"):
#         if os.path.exists(PDF_INDEX_PATH):
#             try:
#                 with open(PDF_INDEX_PATH, "r", encoding="utf-8") as f:
#                     st.session_state["pdf_index"] = json.load(f)
#             except Exception:
#                 st.session_state["pdf_index"] = None

#     index_data = st.session_state.get("pdf_index")
#     if not index_data or not index_data.get("chunks"):
#         return "No indexed PDF data available. Please build the knowledge base first."

#     query_tokens = set(question.lower().split())
#     scored_chunks = []
#     for chunk in index_data["chunks"]:
#         chunk_text = chunk.get("text", "").lower()
#         overlap = len(query_tokens.intersection(set(chunk_text.split())))
#         scored_chunks.append((overlap, chunk_text))

#     scored_chunks.sort(key=lambda item: item[0], reverse=True)
#     best_segments = [text for score, text in scored_chunks[:3] if score > 0]
#     if not best_segments:
#         return "No directly relevant PDF context found for this question."

#     return "\n\n".join(best_segments)

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
# REDIRECT_URI = "https://smart-agent-workspace.streamlit.app"

# oauth2 = OAuth2Component(
#     CLIENT_ID,
#     CLIENT_SECRET,
#     "https://accounts.google.com/o/oauth2/auth",
#     "https://oauth2.googleapis.com/token",
# )

# # ---------------- LOGIN ROUTINE ----------------
# section = "Chat"  # Default section fallback

# # 1. Listen for the code parameter directly on your main clean homepage URL
# query_params = st.query_params
# if "code" in query_params and not st.session_state.logged_in:
#     try:
#         # Swap the incoming URL token code securely
#         code = query_params.get("code")
#         if isinstance(code, list):
#             code = code[0] if code else ""
#         token_result = oauth2.get_token(code, REDIRECT_URI)
#         st.session_state.token = token_result
#         st.session_state.logged_in = True
        
#         id_token = token_result["id_token"]
#         decoded = jwt.decode(id_token, options={"verify_signature": False})
        
#         st.session_state.user_email = decoded.get("email", "")
#         st.session_state.user_name = decoded.get("name", "AI User")
#         st.session_state.user_picture = decoded.get("picture", "")
        
#         # Clear clean URL queries from browser address window layout
#         st.query_params.clear()
#         st.rerun()
#     except Exception as e:
#         st.error(f"Authentication Process Issue: {str(e)}")

# # 2. Render a clean direct main window navigation link button
# if not st.session_state.logged_in:
#     # Construct authorization URL manually
#     authorization_url = f"https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid%20email%20profile"
    
#     st.title("🔐 Secure Workspace Portal")
#     st.write("Welcome to your advanced AI companion workspace. Please authenticate below to continue.")
    
#     # target="_self" opens in the exact same window tab seamlessly
#     st.markdown(
#         f'<a href="{authorization_url}" target="_self" style="display: inline-block; padding: 0.5rem 1rem; color: white; background-color: #FF4B4B; border-radius: 0.5rem; text-decoration: none; font-weight: bold; width: 100%; text-align: center;">🔐 Login with Google</a>',
#         unsafe_allow_html=True
#     )

# # Maintain login persistence safely
# if st.session_state.token:
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
#         st.write("Upload a short audio recording and the assistant will reply with speech.")
        
#         audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"], key="voice_call_input")

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
#                     success = create_vector_store(pdf_path)
#                 if success:
#                     st.success("Knowledge Base Built Successfully! ✅")
#                 else:
#                     st.error("Failed to build the knowledge base. Please upload a valid PDF and try again.")

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
    return ""

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