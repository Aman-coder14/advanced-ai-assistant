import os
from groq import Groq
from gtts import gTTS
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq Client safely
client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(audio_file_buffer):
    """
    Sends raw audio bytes from Streamlit microphone input straight to Groq Whisper API.
    """
    try:
        if not audio_file_buffer:
            return None
        
        # Give the in-memory binary audio stream a valid file name wrapper so the API reads it cleanly
        audio_file_buffer.name = "input_audio.wav"
        
        # Send payload straight to Whisper model
        transcription = client.audio.transcriptions.create(
            file=audio_file_buffer,
            model="whisper-large-v3",
            response_format="text"
        )
        return transcription
        
    except Exception as e:
        return f"Audio Transcription Error: {str(e)}"

def text_to_speech_stream(text_content):
    """
    Converts text strings into in-memory MP3 audio bytes using gTTS.
    """
    try:
        # Generate the voice payload from the text string
        tts = gTTS(text=text_content, lang='en', slow=False)
        
        # Save it directly into a RAM-backed byte buffer instead of writing to disk
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.getvalue()
    except Exception as e:
        print(f"TTS Synthesis Failure: {str(e)}")
        return None