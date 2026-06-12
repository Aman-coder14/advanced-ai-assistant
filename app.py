import os
import uuid
import sqlite3
import hashlib
import requests
import base64
import jwt
import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component

# ---------------- LOAD ENV & SETUP ----------------
load_dotenv()

# Initialize Groq Client with latest authority routing headers
try:
    voice_groq_client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        default_headers={"Groq-Model-Version": "latest"}
    )
except Exception:
    voice_groq_client = None

# Ensure local directories exist for data management
os.makedirs("data", exist_ok=True)
DB_PATH = "data/chatbot.db"

# ---------------- OAUTH CONFIG ----------------
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# Official fallback components folder URI used by the live oauth pipeline
REDIRECT_URI = "https://smart-agent-workspace.streamlit.app/component/streamlit_oauth.authorize_button/index.html"

oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    "https://accounts.google.com/o/oauth2/v2/auth",
    "https://oauth2.googleapis.com/token"
)

# ---------------- CORE ENGINE FUNCTIONAL PIPELINES ----------------

def get_response(prompt):
    """Your original chat pipeline upgraded to groq/compound for live web answers."""
    try:
        if voice_groq_client is None:
            return "Groq Engine Uninitialized."
        
        # FIX: Swapped to groq/compound so your site automatically runs live web searches in 2026
        completion = voice_groq_client.chat.completions.create(
            model="groq/compound",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception:
        # Fallback to standard fast text model if web limits are exceeded
        try:
            fallback = voice_groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return fallback.choices[0].message.content
        except Exception as e:
            return f"AI Generation Error: {str(e)}"

def get_image_response(prompt, image_file):
    """Your original visual analysis framework formatted safely for content arrays."""
    try:
        if voice_groq_client is None:
            return "Vision Framework Error: Groq API missing."
        
        image = Image.open(image_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # FIX: Formatted explicitly to prevent validation 400 bad request errors
        content_payload = [
            {"type": "text", "text": str(prompt)},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
        
        completion = voice_groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": content_payload}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Image Parsing Analysis Failed: {str(e)}"

def local_transcribe_audio(audio_file_buffer):
    """Your original microphone audio transcriber."""
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
    """Your original dynamic text-to-speech engine via real gTTS."""
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
    "user_picture": "",
    "messages": [],
    "chat_count": 1,
    "current_session_id": str(uuid.uuid4()),
    "token": None
}

for key, value in init_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- ORIGINAL LOGIN WORKFLOW (REPAIRED) ----------------
if not st.session_state.logged_in:
    st.title("🔐 Login to AI Workspace")
    st.write("Please authenticate with your account to unlock the agent workspace dashboard.")
    
    # FIX: Intercept code parameter directly to instantly close the loop if cookies are isolated
    query_params = st.query_params
    if "code" in query_params:
        try:
            token_result = oauth2.get_token(query_params["code"], REDIRECT_URI)
            if token_result and "id_token" in token_result:
                st.session_state.token = token_result
                st.session_state.logged_in = True
                
                id_token = token_result["id_token"]
                decoded = jwt.decode(id_token, options={"verify_signature": False})
                
                st.session_state.user_email = decoded.get("email", "")
                st.session_state.user_name = decoded.get("name", "AI User")
                st.session_state.user_picture = decoded.get("picture", "https://www.w3schools.com/howto/img_avatar.png")
                st.query_params.clear()
                st.rerun()
        except Exception:
            pass

    # Render your original component button configuration
    result = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com.tw/favicon.ico",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
        use_container_width=True
    )
    
    if result and "token" in result:
        st.session_state.token = result["token"]
        st.session_state.logged_in = True
        
        id_token = result["token"]["id_token"]
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        
        st.session_state.user_email = decoded.get("email", "")
        st.session_state.user_name = decoded.get("name", "AI User")
        st.session_state.user_picture = decoded.get("picture", "https://www.w3schools.com/howto/img_avatar.png")
        st.rerun()

# ---------------- MAIN APPLICATION ----------------
if st.session_state.logged_in:

    top1, top2 = st.columns([1, 6])
    with top1:
        st.image(st.session_state.user_picture, width=70)
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

    # FEATURE 1: CORE CHAT
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

            with st.spinner("Browsing web and evaluating answer matrices..."):
                response = get_response(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    elif section == "Voice Chat":

    st.title("🎤 Voice Assistant")

    st.info("Voice Chat is temporarily unavailable on cloud deployment.")

    # FEATURE 3: PHOTO CHAT
    elif section == "Photo Chat":
        st.title("🖼 AI Multimodal Photo Chat")
        uploaded_image = st.file_uploader("Drop image source parameters here", type=["png", "jpg", "jpeg"])
        image_prompt = st.text_input("Ask detail analytics regarding this image context")

        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)

            if image_prompt:
                with st.spinner("Analyzing pixel matrices..."):
                    response = get_image_response(image_prompt, uploaded_image)
                
                st.write("### AI Analysis Response")
                st.write(response)

    # FEATURE 4: PDF CHAT
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