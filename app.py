# import jwt
# import streamlit as st
# from streamlit_oauth import OAuth2Component
# from dotenv import load_dotenv
# import os
# import PyPDF2

# from chatbot.llm import get_response
# from chatbot.rag import create_vector_store
# from chatbot.rag import search_pdf
# # ---------------- LOAD ENV ----------------

# load_dotenv()

# CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# # ---------------- PAGE CONFIG ----------------

# st.set_page_config(
#     page_title="Advanced AI Assistant",
#     layout="wide"
# )

# # ---------------- SESSION STATES ----------------

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if "token" not in st.session_state:
#     st.session_state.token = None

# if "user_picture" not in st.session_state:
#     st.session_state.user_picture = ""

# if "user_name" not in st.session_state:
#     st.session_state.user_name = ""

# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "search_history" not in st.session_state:
#     st.session_state.search_history = []

# if "all_chats" not in st.session_state:
#     st.session_state.all_chats = []

# if "chat_count" not in st.session_state:
#     st.session_state.chat_count = 1

# # ---------------- OAUTH ----------------

# oauth2 = OAuth2Component(
#     CLIENT_ID,
#     CLIENT_SECRET,
#     "https://accounts.google.com/o/oauth2/auth",
#     "https://oauth2.googleapis.com/token",
# )

# # ---------------- LOGIN ----------------

# # ---------------- LOGIN ----------------
# section = None
# if not st.session_state.logged_in:

#     result = oauth2.authorize_button(
#         "🔐 Login with Google",
#         redirect_uri="http://localhost:8501/component/streamlit_oauth.authorize_button/index.html",
#         scope="openid email profile",
#     )

#     if result:

#         st.session_state.token = result

#         st.session_state.logged_in = True

#         # Decode Google Token
#         id_token = result["token"]["id_token"]

#         decoded = jwt.decode(
#             id_token,
#             options={"verify_signature": False}
#         )

#         # Real User Info
#         st.session_state.user_email = decoded.get("email")

#         st.session_state.user_name = decoded.get("name")

#         st.session_state.user_picture = decoded.get("picture")

#         st.rerun()

# # Restore Login
# if st.session_state.token:

#     st.session_state.logged_in = True

# # ---------------- MAIN APP ----------------

# if st.session_state.logged_in:

#     # ---------------- TOP PROFILE BAR ----------------

#     top1, top2 = st.columns([1, 6])

#     with top1:

#         import requests
# from PIL import Image
# from io import BytesIO

# if st.session_state.user_picture:

#     response = requests.get(
#         st.session_state.user_picture
#     )

#     image = Image.open(
#         BytesIO(response.content)
#     )

#     st.image(
#         image,
#         width=70
#     )

#     with top2:

#         st.markdown(
#             f"## Welcome, {st.session_state.user_name}"
#         )

#         st.write(
#             st.session_state.user_email
#         )
#         st.write("Picture URL:")
#         st.write(st.session_state.user_picture)
#     st.divider()

#     # ---------------- SIDEBAR ----------------

# with st.sidebar:

#     # ---------------- NEW CHAT ----------------

#     if st.button(
#         "➕ New Chat",
#         use_container_width=True
#     ):

#         if st.session_state.messages:

#             st.session_state.all_chats.append(
#                 st.session_state.messages.copy()
#             )

#         st.session_state.messages = []

#         st.session_state.chat_count += 1

#         st.rerun()

#     st.success(
#         f"Chat #{st.session_state.chat_count}"
#     )

#     # Profile Image
#     if st.session_state.user_picture:

#         st.write("Picture URL:")
#         st.write(st.session_state.user_picture)

#     else:

#         import requests
# from PIL import Image
# from io import BytesIO

# if st.session_state.user_picture:

#     response = requests.get(
#         st.session_state.user_picture
#     )

#     image = Image.open(
#         BytesIO(response.content)
#     )

#     st.image(
#         image,
#         width=80
#     )
#     # User Name
#     st.write(
#         f"### {st.session_state.user_name or 'AI User'}"
#     )

#     # Email
#     st.write(
#         st.session_state.user_email or "Logged In User"
#     )

#     st.divider()

#     # Navigation
#     section = st.radio(
#         "Navigation",
#         [
#             "Chat",
#             "History",
#             "Voice Chat",
#             "Photo Chat",
#             "PDF Chat",
#             "Search",
#             "Profile",
#             "Settings"
#         ]
#     )

#     st.divider()

#     # Logout
#     if st.button("Logout"):

#         st.session_state.logged_in = False
#         st.session_state.token = None
#         st.session_state.user_email = ""
#         st.session_state.user_name = ""
#         st.session_state.user_picture = ""
#         st.session_state.messages = []
#         st.session_state.search_history = []

#         st.rerun()

#     # ---------------- CHAT ----------------

#     # ---------------- CHAT ----------------

# if section == "Chat":

#     st.title("💬 AI Chat")

#     # Display previous messages
#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):

#             st.markdown(message["content"])

#     # User input
#     prompt = st.chat_input(
#         "Message AI Assistant"
#     )

#     if prompt:

#         # Save in search history
#         # st.session_state.search_history.append(
#         #     prompt
#         # )

#         # Save user message
#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         )

#         # Show user message
#         with st.chat_message("user"):

#             st.markdown(prompt)

#         # Get AI response
#         response = get_response(prompt)

#         # Show AI response
#         with st.chat_message("assistant"):

#             st.markdown(response)

#         # Save AI response
#         st.session_state.messages.append(
#             {
#                 "role": "assistant",
#                 "content": response
#             }
#         )
#     # ---------------- HISTORY ----------------

# elif section == "History":

#     st.title("🕘 Chat History")

#     if st.session_state.all_chats:

#         for i, chat in enumerate(
#             reversed(st.session_state.all_chats),
#             start=1
#         ):

#             with st.expander(
#                 f"Chat {i}"
#             ):

#                 for msg in chat:

#                     st.write(
#                         f"{msg['role']} : {msg['content']}"
#                     )

#     else:

#         st.info(
#             "No previous chats found."
#         )

# # ---------------- VOICE CHAT ----------------

# elif section == "Voice Chat":

#     st.title("🎤 Voice Assistant")

#     st.write(
#         "Voice assistant coming soon 🚀"
#     )

# # ---------------- PHOTO CHAT ----------------

# elif section == "Photo Chat":

#     st.title("🖼 AI Photo Chat")

#     uploaded_image = st.file_uploader(
#         "Upload Image",
#         type=["png", "jpg", "jpeg"]
#     )

#     image_prompt = st.text_input(
#         "Ask something about image"
#     )

#     if uploaded_image:

#         st.image(uploaded_image)

#         if image_prompt:

#             response = get_response(
#                 f"""
#                 User uploaded an image.

#                 User Question:
#                 {image_prompt}
#                 """
#             )

#             st.write(response)

# # ---------------- PDF CHAT ----------------

# elif section == "PDF Chat":

#     st.title("📄 PDF RAG Chat")

#     uploaded_pdf = st.file_uploader(
#         "Upload PDF",
#         type=["pdf"]
#     )

#     if uploaded_pdf:

#         pdf_path = os.path.join(
#             "data",
#             uploaded_pdf.name
#         )

#         with open(
#             pdf_path,
#             "wb"
#         ) as f:

#             f.write(
#                 uploaded_pdf.getbuffer()
#             )

#         if st.button(
#             "Create Knowledge Base"
#         ):

#             with st.spinner(
#                 "Building Vector Database..."
#             ):

#                 create_vector_store(
#                     pdf_path
#                 )

#             st.success(
#                 "Knowledge Base Created Successfully ✅"
#             )

#         question = st.text_input(
#             "Ask a question from PDF"
#         )

#         if question:

#             context = search_pdf(
#                 question
#             )

#             prompt = f"""
# You are an AI assistant.

# Answer ONLY from the PDF content below.

# PDF Content:
# {context}

# Question:
# {question}
# """

#             answer = get_response(
#                 prompt
#             )

#             st.write(
#                 "### Answer"
#             )

#             st.write(
#                 answer
#             )
# At the top of your app.py
# Look for this line at the top of app.py and add get_image_response
# ========================================================
# PASTE THIS AT THE VERY TOP OF YOUR APP.PY FILE
# ========================================================
import os
from groq import Groq
from gtts import gTTS
from io import BytesIO

# Initialize a clean Groq Client instance for voice calls
try:
    voice_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    voice_groq_client = None

def local_transcribe_audio(audio_file_buffer):
    """Sends raw audio bytes directly to Groq Whisper API."""
    try:
        if not audio_file_buffer or voice_groq_client is None:
            return "Audio Error: Groq client not initialized or empty buffer."
        
        audio_file_buffer.name = "input_audio.wav"
        transcription = voice_groq_client.audio.transcriptions.create(
            file=audio_file_buffer,
            model="whisper-large-v3",
            response_format="text"
        )
        return transcription
    except Exception as e:
        return f"Audio Transcription Error: {str(e)}"

def local_text_to_speech_stream(text_content):
    """Converts text strings into in-memory MP3 audio bytes using gTTS."""
    try:
        tts = gTTS(text=text_content, lang='en', slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        return None
# ========================================================
from chatbot.llm import get_response, get_image_response
import os
import jwt
import uuid
import requests
import PyPDF2
import streamlit as st
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component

# Import custom chatbot database routines
from chatbot.database import (
    init_chat_tables, 
    create_new_session, 
    save_message, 
    get_user_sessions, 
    get_session_messages
)

# Import custom chatbot modules
from chatbot.llm import get_response
from chatbot.rag import create_vector_store, search_pdf

# ---------------- LOAD ENV & SETUP ----------------
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Ensure local storage directories exist
os.makedirs("data", exist_ok=True)

# Initialize the chat logging tables inside your database file path
init_chat_tables("data/chatbot.db")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Advanced AI Assistant",
    layout="wide"
)

# ---------------- SESSION STATES ----------------
init_states = {
    "logged_in": False,
    "token": None,
    "user_picture": "",
    "user_name": "",
    "user_email": "",
    "messages": [],
    "search_history": [],
    "all_chats": [],
    "chat_count": 1,
    "current_session_id": str(uuid.uuid4()) # Generates a stable starting transaction tracking id
}

for key, value in init_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- OAUTH CONFIG ----------------
oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    "https://accounts.google.com/o/oauth2/auth",
    "https://oauth2.googleapis.com/token",
)

# ---------------- LOGIN ROUTINE ----------------
section = "Chat"  # Default section fallback

if not st.session_state.logged_in:
    result = oauth2.authorize_button(
        "🔐 Login with Google",
        redirect_uri="http://localhost:8501/component/streamlit_oauth.authorize_button/index.html",
        scope="openid email profile",
    )

    if result:
        st.session_state.token = result
        st.session_state.logged_in = True

        # Decode Google Token securely without signature verification for client-side routing
        id_token = result["token"]["id_token"]
        decoded = jwt.decode(id_token, options={"verify_signature": False})

        # Cache User Information
        st.session_state.user_email = decoded.get("email", "")
        st.session_state.user_name = decoded.get("name", "AI User")
        st.session_state.user_picture = decoded.get("picture", "")
        st.rerun()

# Restore session state if token is still preserved
if st.session_state.token:
    st.session_state.logged_in = True

# ---------------- MAIN APPLICATION ----------------
if st.session_state.logged_in:

    # ---------------- TOP PROFILE BAR ----------------
    top1, top2 = st.columns([1, 6])
    
    with top1:
        if st.session_state.user_picture:
            try:
                response = requests.get(st.session_state.user_picture, timeout=5)
                image = Image.open(BytesIO(response.content))
                st.image(image, width=70)
            except Exception:
                st.image("https://www.w3schools.com/howto/img_avatar.png", width=70) # Fallback profile image placeholder

    with top2:
        st.markdown(f"## Welcome, {st.session_state.user_name}")
        st.write(st.session_state.user_email)
    st.divider()

    # ---------------- SIDEBAR NAVIGATION ----------------
    with st.sidebar:
        # New Chat Initialization
        if st.button("➕ New Chat", use_container_width=True):
            # Roll a completely unique session ID for database splits
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.chat_count += 1
            st.rerun()

        st.success(f"Active Session: Chat #{st.session_state.chat_count}")
        st.divider()

        # Navigation Menu
        section = st.radio(
            "Navigation",
            [
                "Chat",
                "History",
                "Voice Chat",
                "Photo Chat",
                "PDF Chat",
                "Search",
                "Profile",
                "Settings"
            ]
        )
        st.divider()

        # Logout Execution
        if st.button("Logout", use_container_width=True):
            for key in init_states.keys():
                st.session_state[key] = init_states[key]
            # Refresh UUID token to disconnect state tracking
            st.session_state.current_session_id = str(uuid.uuid4())
            st.rerun()

    # ---------------- APP ROUTING LOGIC ----------------

    # FEATURE 1: CORE CHAT
    if section == "Chat":
        st.title("💬 AI Chat")
        
        # Ensure a base conversation tracking row row exists in our SQLite log
        create_new_session(
            st.session_state.current_session_id, 
            st.session_state.user_email, 
            f"General Chat Session {st.session_state.chat_count}"
        )

        # Sync temporary app layout data to database logs if fresh session state
        if not st.session_state.messages:
            st.session_state.messages = get_session_messages(st.session_state.current_session_id)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Message AI Assistant")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            save_message(st.session_state.current_session_id, "user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Thinking..."):
                response = get_response(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_message(st.session_state.current_session_id, "assistant", response)

    # FEATURE 2: PERMANENT DATABASE HISTORY
    elif section == "History":
        st.title("🕘 Saved Chat History")
        
        # Pull records belonging to the active Google user profile
        user_history = get_user_sessions(st.session_state.user_email)

        if user_history:
            for row in user_history:
                with st.expander(f"📁 {row['title']} — ({row['created_at'][:10]})"):
                    # Extract logs tied specifically to the transaction session ID
                    history_messages = get_session_messages(row['session_id'])
                    
                    for msg in history_messages:
                        role_label = "👤 User" if msg['role'] == "user" else "🤖 Assistant"
                        st.markdown(f"**{role_label}**:\n{msg['content']}")
                        st.divider()
        else:
            st.info("No saved chat logs found associated with your profile email.")

    # FEATURE 3: VOICE CHAT (SPEECH-TO-SPEECH LOOP)
    elif section == "Voice Chat":
        st.title("🎤 Voice Call Assistant")
        st.write("Talk hands-free! Record your question, and the assistant will speak its answer out loud.")
        
        # Native safe audio widget
        audio_file = st.audio_input("🎤 Press the microphone icon to speak...", key="voice_call_input")

        if audio_file:
            with st.spinner("Processing your voice..."):
                # Using the local function we pasted at the top of app.py
                user_speech_text = local_transcribe_audio(audio_file)
            
            if user_speech_text and not user_speech_text.startswith("Audio Transcription Error:") and not user_speech_text.startswith("Audio Error:"):
                st.success(f"🗣️ **You Said:** {user_speech_text}")
                
                with st.spinner("Thinking..."):
                    ai_voice_response = get_response(user_speech_text)
                
                with st.spinner("Speaking reply..."):
                    # Using the local gTTS function from the top of app.py
                    reply_audio_bytes = local_text_to_speech_stream(ai_voice_response)
                
                # --- DATABASE LOGGING ---
                create_new_session(
                    st.session_state.current_session_id, 
                    st.session_state.user_email, 
                    f"Voice Chat: {user_speech_text[:15]}..."
                )
                save_message(st.session_state.current_session_id, "user", user_speech_text)
                save_message(st.session_state.current_session_id, "assistant", ai_voice_response)
                # ------------------------

                st.markdown("### 🤖 Assistant Reply")
                st.info(ai_voice_response)
                
                # This plays the voice file automatically through your speakers!
                if reply_audio_bytes:
                    st.audio(reply_audio_bytes, format="audio/mp3", autoplay=True)
            else:
                st.error("Could not process speech. Please click the trash icon on the mic widget and try again.")

    # FEATURE 4: PHOTO CHAT
    elif section == "Photo Chat":
        st.title("🖼 AI Photo Chat")
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        image_prompt = st.text_input("Ask something about this image")

        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)

            if image_prompt:
                with st.spinner("Analyzing image pixels and generating insights..."):
                    # Execute the Groq Vision model call
                    response = get_image_response(image_prompt, uploaded_image)
                
                # Clean strings to strip bad spacing characters before saving to SQLite
                clean_prompt = str(image_prompt).strip()
                clean_response = str(response).strip()

                # 1. Create session mapping row
                create_new_session(
                    st.session_state.current_session_id, 
                    st.session_state.user_email, 
                    f"Photo: {uploaded_image.name[:12]}..."
                )
                
                # 2. Append directly to SQLite columns
                save_message(st.session_state.current_session_id, "user", clean_prompt)
                save_message(st.session_state.current_session_id, "assistant", clean_response)

                st.write("### AI Analysis")
                st.write(response)
    # FEATURE 5: PDF RAG CHAT
    elif section == "PDF Chat":
        st.title("📄 PDF RAG Chat")
        uploaded_pdf = st.file_uploader("Upload PDF Data Source", type=["pdf"])

        if uploaded_pdf:
            pdf_path = os.path.join("data", uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())

            if st.button("Build Knowledge Base", use_container_width=True):
                with st.spinner("Parsing text and building Vector Embeddings..."):
                    create_vector_store(pdf_path)
                st.success("Knowledge Base Built Successfully! ✅")

            question = st.text_input("Ask a question based directly on the document context")
            
            if question:
                with st.spinner("Searching document context..."):
                    context = search_pdf(question)
                    
                    prompt = f"""
You are an expert conversational AI assistant.

Here is the retrieved context from the uploaded document:
{context}

User Question:
{question}

Instructions:
1. If the answer can be found in the document context above, use it to provide a highly accurate, grounded answer.
2. If the user is asking a general knowledge question, a coding problem, or something completely unrelated to the document, bypass the context and answer to the best of your general knowledge.
3. Keep your tone helpful, clear, and direct.
"""
                    answer = get_response(prompt, bypass_search=True)
                
                # --- NEW SYSTEM LOGGING SAVES PDF CHAT TO PERSISTENT SQL RECORDS ---
                create_new_session(
                    st.session_state.current_session_id, 
                    st.session_state.user_email, 
                    f"PDF Chat: {uploaded_pdf.name[:15]}..."
                )
                save_message(st.session_state.current_session_id, "user", question)
                save_message(st.session_state.current_session_id, "assistant", answer)
                # ------------------------------------------------------------------

                st.write("### Answer")
                st.info(answer)



# ----------------------- THIS NOT WORKING PROPER SO COMMENT LINE ----------------

# import os
# import streamlit as st
# import sqlite3
# from datetime import datetime
# from uuid import uuid4
# from groq import Groq
# from gtts import gTTS
# from io import BytesIO
# import base64
# from PIL import Image

# # ========================================================
# # 1. PAGE CONFIG & HIGH-END THEME INJECTION
# # ========================================================
# st.set_page_config(page_title="Advanced AI Multi-Agent Studio", layout="wide")

# def inject_custom_design():
#     """Injects high-end, responsive modern CSS styling into the Streamlit layout."""
#     st.markdown(
#         """
#         <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
#         <style>
#             /* Apply premium font across the app */
#             * {
#                 font-family: 'Plus Jakarta Sans', sans-serif !important;
#             }
            
#             /* Main Background styling */
#             .stApp {
#                 background: radial-gradient(circle at 50% 50%, #121824 0%, #0b0f19 100%);
#             }
            
#             /* Sidebar Styling Overhaul */
#             [data-testid="stSidebar"] {
#                 background-color: #0d131f !important;
#                 border-right: 1px solid #1e293b;
#             }
            
#             /* High-end Glassmorphism Card Panels for content containers */
#             div.stButton > button, div[data-testid="stExpander"], .stTextInput > div > div, .stAudioInput, .stFileUploader {
#                 background: rgba(255, 255, 255, 0.03) !important;
#                 backdrop-filter: blur(12px) !important;
#                 border: 1px solid rgba(255, 255, 255, 0.08) !important;
#                 border-radius: 12px !important;
#                 color: #f8fafc !important;
#                 transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#             }
            
#             /* Interaction Hover states */
#             div.stButton > button:hover {
#                 border-color: #6366f1 !important;
#                 box-shadow: 0 0 20px rgba(99, 102, 241, 0.25) !important;
#                 transform: translateY(-2px);
#                 background: rgba(99, 102, 241, 0.1) !important;
#             }
            
#             /* Center Login Form Layout styling */
#             .login-container {
#                 max-width: 450px;
#                 margin: 80px auto;
#                 padding: 40px;
#                 background: rgba(255, 255, 255, 0.02);
#                 border: 1px solid rgba(255, 255, 255, 0.08);
#                 border-radius: 16px;
#                 text-align: center;
#                 backdrop-filter: blur(20px);
#                 box-shadow: 0 20px 40px rgba(0,0,0,0.4);
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Apply global premium frontend UI theme wrapper
# inject_custom_design()

# # ========================================================
# # 2. DATABASE & MODEL BACKENDS INITIALIZATION
# # ========================================================
# DB_FILE = "chatbot.db"

# def init_db():
#     with sqlite3.connect(DB_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS sessions (
#                 session_id TEXT PRIMARY KEY,
#                 user_email TEXT,
#                 title TEXT,
#                 created_at TEXT
#             )
#         """)
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS messages (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 session_id TEXT,
#                 role TEXT,
#                 content TEXT,
#                 timestamp TEXT,
#                 FOREIGN KEY (session_id) REFERENCES sessions(session_id)
#             )
#         """)
#         conn.commit()

# init_db()

# # Core Database Hooks
# def create_new_session(session_id, email, title):
#     with sqlite3.connect(DB_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT 1 FROM sessions WHERE session_id = ?", (session_id,))
#         if not cursor.fetchone():
#             cursor.execute("INSERT INTO sessions VALUES (?, ?, ?, ?)", 
#                            (session_id, email, title, datetime.now().isoformat()))
#             conn.commit()

# def save_message(session_id, role, content):
#     with sqlite3.connect(DB_FILE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
#                        (session_id, role, content, datetime.now().isoformat()))
#         conn.commit()

# def get_user_sessions(email):
#     with sqlite3.connect(DB_FILE) as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM sessions WHERE user_email = ? ORDER BY created_at DESC", (email,))
#         return cursor.fetchall()

# def get_session_messages(session_id):
#     with sqlite3.connect(DB_FILE) as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
#         return cursor.fetchall()

# # Initialize core model routing backends
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# def get_response(user_input):
#     try:
#         if not groq_client: return "API connection key missing."
#         completion = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{"role": "user", "content": user_input}],
#             temperature=0.5
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         return f"AI Generation Error: {str(e)}"

# # Voice Helpers
# def local_transcribe_audio(audio_file_buffer):
#     try:
#         if not audio_file_buffer or groq_client is None:
#             return "Audio Error: Groq client not initialized or empty buffer."
#         audio_file_buffer.name = "input_audio.wav"
#         transcription = groq_client.audio.transcriptions.create(
#             file=audio_file_buffer,
#             model="whisper-large-v3",
#             response_format="text"
#         )
#         return transcription
#     except Exception as e:
#         return f"Audio Transcription Error: {str(e)}"

# def local_text_to_speech_stream(text_content):
#     try:
#         tts = gTTS(text=text_content, lang='en', slow=False)
#         audio_buffer = BytesIO()
#         tts.write_to_fp(audio_buffer)
#         audio_buffer.seek(0)
#         return audio_buffer.getvalue()
#     except Exception as e:
#         return None

# # Vision Helper
# def get_image_response(user_input, uploaded_image_file):
#     try:
#         if not groq_client: return "API configuration missing."
#         image_bytes = uploaded_image_file.getvalue()
#         base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
#         file_extension = uploaded_image_file.name.split(".")[-1].lower()
#         mime_type = f"image/{file_extension}"
#         if file_extension == "jpg": mime_type = "image/jpeg"

#         response = groq_client.chat.completions.create(
#             model="meta-llama/llama-4-scout-17b-16e-instruct",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": user_input},
#                         {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
#                     ]
#                 }
#             ],
#             temperature=0.2,
#             max_tokens=1024
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"Vision Analytics Error: {str(e)}"

# # ========================================================
# # 3. AUTHENTICATION & LOGIN GATE PHASE
# # ========================================================
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'user_email' not in st.session_state:
#     st.session_state.user_email = ""

# # Display Login Screen if user is not verified yet
# if not st.session_state.logged_in:
#     st.markdown(
#         """
#         <div class="login-container">
#             <h1 style="color: #6366f1; margin-bottom: 10px;">🔒 Workspace Portal</h1>
#             <p style="color: #94a3b8; margin-bottom: 30px;">Sign in with your verified profile to unlock agent workspaces</p>
#         </div>
#         """, 
#         unsafe_allow_html=True
#     )
    
#     # Render interactive portal fields centered nicely
#     col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
#     with col_l2:
#         input_email = st.text_input("User Access Email Address", placeholder="name@domain.com")
#         input_password = st.text_input("Access Security Key / Password", type="password")
        
#         if st.button("🚀 Authorize Session Connection", use_container_width=True):
#             if input_email and len(input_password) >= 4:
#                 st.session_state.logged_in = True
#                 st.session_state.user_email = input_email
#                 st.session_state.current_session_id = str(uuid4())
#                 st.rerun()
#             else:
#                 st.error("Invalid Credentials. Please ensure password length requirements are satisfied.")
#     st.stop() # Prevents non-authenticated users from loading background dashboards

# # ========================================================
# # 4. APP DASHBOARD LAYOUT (POST-AUTHENTICATION ONLY)
# # ========================================================
# with st.sidebar:
#     st.markdown("<h2 style='text-align: center; color: #6366f1;'>🚀 AI Studio</h2>", unsafe_allow_html=True)
#     st.write(f"👤 **Session:** `{st.session_state.user_email}`")
#     st.divider()
    
#     section = st.radio(
#         "Navigate Dashboard Modules",
#         ["Core Text Chat", "History Log", "Voice Chat", "Photo Chat"]
#     )
    
#     st.divider()
#     if st.button("➕ Start Fresh Session", use_container_width=True):
#         st.session_state.current_session_id = str(uuid4())
#         st.success("New interaction token created!")
    
#     if st.button("🚪 Terminate Session / Logout", use_container_width=True):
#         st.session_state.logged_in = False
#         st.session_state.user_email = ""
#         st.rerun()

# # ========================================================
# # 5. MODULE APP ROUTING
# # ========================================================

# # FEATURE 1: CORE TEXT CHAT
# if section == "Core Text Chat":
#     st.markdown("<h1>💬 <span style='color: #6366f1;'>AI Core</span> Chat Hub</h1>", unsafe_allow_html=True)
#     chat_prompt = st.text_input("Converse with the foundational knowledge model")
    
#     if chat_prompt:
#         with st.spinner("Thinking..."):
#             text_reply = get_response(chat_prompt)
        
#         create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Chat: {chat_prompt[:15]}...")
#         save_message(st.session_state.current_session_id, "user", chat_prompt)
#         save_message(st.session_state.current_session_id, "assistant", text_reply)
        
#         st.write("### AI Response")
#         st.write(text_reply)

# # FEATURE 2: HISTORICAL MESSAGE VIEWER
# elif section == "History Log":
#     st.markdown("<h1>🕘 <span style='color: #94a3b8;'>Saved Chat</span> Logs</h1>", unsafe_allow_html=True)
#     user_history = get_user_sessions(st.session_state.user_email)

#     if user_history:
#         for row in user_history:
#             with st.expander(f"📁 {row['title']} — ({row['created_at'][:10]})"):
#                 history_messages = get_session_messages(row['session_id'])
#                 for msg in history_messages:
#                     if msg['role'] == "user":
#                         st.markdown(f"👤 **User:** {msg['content']}")
#                     else:
#                         st.markdown("🤖 **Assistant:**")
#                         st.write(msg['content'])
#                     st.divider()
#     else:
#         st.info("No saved chat database tracks found linked to this profile context.")

# # FEATURE 3: VOICE CALL CHAT (SPEECH-TO-SPEECH LOOP)
# elif section == "Voice Chat":
#     st.markdown("<h1>🎤 <span style='color: #10b981;'>Voice Call</span> Assistant</h1>", unsafe_allow_html=True)
#     st.write("Talk hands-free! Record your question, and the assistant will speak its answer out loud.")
    
#     audio_file = st.audio_input("🎤 Press the microphone icon to speak...", key="voice_call_input")

#     if audio_file:
#         with st.spinner("Processing your voice..."):
#             user_speech_text = local_transcribe_audio(audio_file)
        
#         if user_speech_text and not user_speech_text.startswith("Audio Transcription Error:") and not user_speech_text.startswith("Audio Error:"):
#             st.success(f"🗣️ **You Said:** {user_speech_text}")
            
#             with st.spinner("Thinking..."):
#                 ai_voice_response = get_response(user_speech_text)
            
#             with st.spinner("Speaking reply..."):
#                 reply_audio_bytes = local_text_to_speech_stream(ai_voice_response)
            
#             create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Voice: {user_speech_text[:15]}...")
#             save_message(st.session_state.current_session_id, "user", user_speech_text)
#             save_message(st.session_state.current_session_id, "assistant", ai_voice_response)

#             st.markdown("### 🤖 Assistant Reply")
#             st.info(ai_voice_response)
            
#             if reply_audio_bytes:
#                 st.audio(reply_audio_bytes, format="audio/mp3", autoplay=True)
#         else:
#             st.error("Could not process speech. Please clear the recording widget asset and try again.")

# # FEATURE 4: PHOTO CHAT (VISION MODEL INTERACTION)
# elif section == "Photo Chat":
#     st.markdown("<h1>🖼️ <span style='color: #f59e0b;'>Vision</span> Analytics</h1>", unsafe_allow_html=True)
#     uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
#     image_prompt = st.text_input("Ask something about this image")

#     if uploaded_image:
#         st.image(uploaded_image, use_container_width=True)

#         if image_prompt:
#             with st.spinner("Analyzing image pixels..."):
#                 vision_response = get_image_response(image_prompt, uploaded_image)
            
#             clean_prompt = str(image_prompt).strip()
#             clean_response = str(vision_response).strip()

#             create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Photo: {uploaded_image.name[:12]}...")
#             save_message(st.session_state.current_session_id, "user", clean_prompt)
#             save_message(st.session_state.current_session_id, "assistant", clean_response)

#             st.write("### AI Analysis")
#             st.write(vision_response)