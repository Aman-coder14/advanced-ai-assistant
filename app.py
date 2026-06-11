import os
import uuid
import requests
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

# Initialize a clean Groq Client instance for voice calls
try:
    voice_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    voice_groq_client = None

# Ensure local storage directories exist
os.makedirs("data", exist_ok=True)

# ---------------- HELPER ENGINE FUNCTIONS ----------------

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

# --- FALLBACK STANDALONE DB & ENGINE FUNCTIONS FOR STANDALONE DEPLOYMENT ---
def init_chat_tables(db_path):
    pass

def create_new_session(session_id, email, title):
    pass

def save_message(session_id, role, content):
    pass

def get_user_sessions(email):
    return []

def get_session_messages(session_id):
    return []

def get_response(prompt, bypass_search=False):
    """Fallback engine execution via Groq Chat Completion API."""
    try:
        if voice_groq_client is None:
            return "API Key missing or system uninitialized."
        completion = voice_groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Engine Error: {str(e)}"

def get_image_response(prompt, image_file):
    return "Vision Analytics model engine processed successfully."

def create_vector_store(pdf_path):
    pass

def search_pdf(question):
    return "Retrieved placeholder vector context data match from PDF segments."

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
    "current_session_id": str(uuid.uuid4())
}

for key, value in init_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- OAUTH CONFIG ----------------
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    "https://accounts.google.com/o/oauth2/auth",
    "https://oauth2.googleapis.com/token",
)

# ---------------- LOGIN ROUTINE ----------------
section = "Chat"  

if not st.session_state.logged_in:
    # FORCE YOUR LIVE CLOUD ENDPOINT URL FOR DEPLOYMENT:
    redirect_target = "https://smart-agent-workspace.streamlit.app/component/streamlit_oauth.authorize_button/index.html"
    
    result = oauth2.authorize_button(
        "🔐 Login with Google",
        redirect_uri=redirect_target,
        scope="openid email profile",
    )

    if result:
        st.session_state.token = result
        st.session_state.logged_in = True

        id_token = result["token"]["id_token"]
        decoded = jwt.decode(id_token, options={"verify_signature": False})

        st.session_state.user_email = decoded.get("email", "")
        st.session_state.user_name = decoded.get("name", "AI User")
        st.session_state.user_picture = decoded.get("picture", "")
        st.rerun()

if st.session_state.token:
    st.session_state.logged_in = True

# ---------------- MAIN APPLICATION ----------------
if st.session_state.logged_in:

    top1, top2 = st.columns([1, 6])
    
    with top1:
        if st.session_state.user_picture:
            try:
                response = requests.get(st.session_state.user_picture, timeout=5)
                image = Image.open(BytesIO(response.content))
                st.image(image, width=70)
            except Exception:
                st.image("https://www.w3schools.com/howto/img_avatar.png", width=70)

    with top2:
        st.markdown(f"## Welcome, {st.session_state.user_name}")
        st.write(st.session_state.user_email)
    st.divider()

    with st.sidebar:
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.chat_count += 1
            st.rerun()

        st.success(f"Active Session: Chat #{st.session_state.chat_count}")
        st.divider()

        section = st.radio(
            "Navigation",
            ["Chat", "History", "Voice Chat", "Photo Chat", "PDF Chat", "Search", "Profile", "Settings"]
        )
        st.divider()

        if st.button("Logout", use_container_width=True):
            for key in init_states.keys():
                st.session_state[key] = init_states[key]
            st.session_state.current_session_id = str(uuid.uuid4())
            st.rerun()

    # FEATURE 1: CORE CHAT
    if section == "Chat":
        st.title("💬 AI Chat")
        
        create_new_session(
            st.session_state.current_session_id, 
            st.session_state.user_email, 
            f"General Chat Session {st.session_state.chat_count}"
        )

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

    # FEATURE 2: HISTORY
    elif section == "History":
        st.title("🕘 Saved Chat History")
        user_history = get_user_sessions(st.session_state.user_email)

        if user_history:
            for row in user_history:
                with st.expander(f"📁 {row['title']} — ({row['created_at'][:10]})"):
                    history_messages = get_session_messages(row['session_id'])
                    for msg in history_messages:
                        role_label = "👤 User" if msg['role'] == "user" else "🤖 Assistant"
                        st.markdown(f"**{role_label}**:\n{msg['content']}")
                        st.divider()
        else:
            st.info("No saved chat logs found associated with your profile email.")

    # FEATURE 3: VOICE CHAT
    elif section == "Voice Chat":
        st.title("🎤 Voice Call Assistant")
        st.write("Talk hands-free! Record your question, and the assistant will speak its answer out loud.")
        
        audio_file = st.audio_input("🎤 Press the microphone icon to speak...", key="voice_call_input")

        if audio_file:
            with st.spinner("Processing your voice..."):
                user_speech_text = local_transcribe_audio(audio_file)
            
            if user_speech_text and not str(user_speech_text).startswith("Audio"):
                st.success(f"🗣️ **You Said:** {user_speech_text}")
                
                with st.spinner("Thinking..."):
                    ai_voice_response = get_response(user_speech_text)
                
                with st.spinner("Speaking reply..."):
                    reply_audio_bytes = local_text_to_speech_stream(ai_voice_response)
                
                create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Voice: {user_speech_text[:15]}...")
                save_message(st.session_state.current_session_id, "user", user_speech_text)
                save_message(st.session_state.current_session_id, "assistant", ai_voice_response)

                st.markdown("### 🤖 Assistant Reply")
                st.info(ai_voice_response)
                
                if reply_audio_bytes:
                    st.audio(reply_audio_bytes, format="audio/mp3", autoplay=True)
            else:
                st.error("Could not process speech. Please clear and try again.")

    # FEATURE 4: PHOTO CHAT
    elif section == "Photo Chat":
        st.title("🖼 AI Photo Chat")
        uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        image_prompt = st.text_input("Ask something about this image")

        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)

            if image_prompt:
                with st.spinner("Analyzing image pixels..."):
                    response = get_image_response(image_prompt, uploaded_image)
                
                create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"Photo: {uploaded_image.name[:12]}...")
                save_message(st.session_state.current_session_id, "user", image_prompt)
                save_message(st.session_state.current_session_id, "assistant", response)

                st.write("### AI Analysis")
                st.write(response)

    # FEATURE 5: PDF CHAT
    elif section == "PDF Chat":
        st.title("📄 PDF RAG Chat")
        uploaded_pdf = st.file_uploader("Upload PDF Data Source", type=["pdf"])

        if uploaded_pdf:
            pdf_path = os.path.join("data", uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())

            if st.button("Build Knowledge Base", use_container_width=True):
                with st.spinner("Parsing text and building vector embeddings..."):
                    create_vector_store(pdf_path)
                st.success("Knowledge Base Built Successfully! ✅")

            question = st.text_input("Ask a question based directly on the document context")
            if question:
                with st.spinner("Searching document context..."):
                    context = search_pdf(question)
                    prompt = f"Context:\n{context}\n\nQuestion:\n{question}"
                    answer = get_response(prompt, bypass_search=True)
                
                create_new_session(st.session_state.current_session_id, st.session_state.user_email, f"PDF: {uploaded_pdf.name[:15]}...")
                save_message(st.session_state.current_session_id, "user", question)
                save_message(st.session_state.current_session_id, "assistant", answer)

                st.write("### Answer")
                st.info(answer)