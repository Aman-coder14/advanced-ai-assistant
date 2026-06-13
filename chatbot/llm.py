"""
Language Model Integration with Search Context
Handles AI responses using Groq LLM with integrated web and Wikipedia search.
Provides current event awareness and knowledge base augmentation.
"""

from groq import Groq
from dotenv import load_dotenv
from chatbot.search import get_search_context, format_search_context
import os

# Load environment variables
load_dotenv()

# ==========================================
# GROQ CLIENT INITIALIZATION
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client with error handling
try:
    client = Groq(api_key=GROQ_API_KEY)
    print("✅ Groq client initialized successfully")
except Exception as e:
    print(f"❌ Groq Client Error: {e}")
    client = None

# ==========================================
# SYSTEM INSTRUCTIONS
# ==========================================

SYSTEM_INSTRUCTION_WITH_SEARCH = (
    "You are an advanced AI Assistant with access to real-time information.\n\n"
    "KNOWLEDGE CONTEXT:\n"
    "- Your base training data has a knowledge cutoff in early 2024.\n"
    "- Current date is 2026 (June 12, 2026).\n"
    "- You have access to live web search and Wikipedia data.\n\n"
    "INSTRUCTIONS:\n"
    "1. If live web search results are provided, treat them as AUTHORITATIVE for current events.\n"
    "2. Always cite sources when using search data.\n"
    "3. For historical or general knowledge questions, you can use your training data.\n"
    "4. Prioritize real-time data over training data for 2026 events, news, and current topics.\n"
    "5. If information is unavailable, be honest and suggest what data would help.\n"
    "6. Provide concise, accurate, and helpful responses.\n"
)

SYSTEM_INSTRUCTION_NO_SEARCH = (
    "You are an advanced AI Assistant.\n\n"
    "KNOWLEDGE CONTEXT:\n"
    "- Your training data has a knowledge cutoff in early 2024.\n"
    "- Current date is 2026.\n"
    "- No real-time search data is available for this query.\n\n"
    "INSTRUCTIONS:\n"
    "1. Use your training knowledge to answer the question.\n"
    "2. Acknowledge if information might be outdated (pre-2024).\n"
    "3. Be honest about limitations of your knowledge.\n"
    "4. Provide helpful and accurate responses based on available information.\n"
)

# ==========================================
# MAIN RESPONSE GENERATION
# ==========================================

def get_response(user_input: str) -> str:
    """
    Generates AI responses with integrated search context.
    
    Process:
    1. Determines if web search is needed
    2. Retrieves relevant context from DuckDuckGo or Wikipedia
    3. Combines context with the original question
    4. Sends enriched prompt to Groq LLM
    5. Returns concise answer
    
    Args:
        user_input (str): User's question or statement
        
    Returns:
        str: AI-generated response with context
    """
    try:
        if client is None:
            return (
                "❌ Groq Engine Initialization Error\n"
                "Please ensure GROQ_API_KEY is set in your .env file"
            )
        
        if not user_input or not isinstance(user_input, str):
            return "❌ Invalid input: Please provide a valid question."
        
        print(f"\n🤖 Processing query: {user_input}")
        
        # Step 1: Determine if search is needed and get context
        search_results, search_type = get_search_context(user_input)
        
        # Step 2: Format search context
        search_context = format_search_context(search_results, search_type)
        
        # Step 3: Build the enriched user message
        if search_context:
            system_instruction = SYSTEM_INSTRUCTION_WITH_SEARCH
            enriched_prompt = (
                f"{search_context}"
                f"User's Question:\n{user_input}"
            )
        else:
            system_instruction = SYSTEM_INSTRUCTION_NO_SEARCH
            enriched_prompt = user_input
        
        # Step 4: Create messages array
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": enriched_prompt}
        ]
        
        print(f"📤 Sending to Groq (Search Type: {search_type})")
        
        # Step 5: Call Groq API
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3,
            max_tokens=1024,
            top_p=0.9
        )
        
        response = completion.choices[0].message.content
        print(f"✅ Response generated successfully")
        
        return response
        
    except Exception as e:
        error_message = f"⚠️ AI Generation Error: {str(e)}"
        print(error_message)
        return (
            f"{error_message}\n\n"
            "Please try again or rephrase your question."
        )


# ==========================================
# IMAGE ANALYSIS
# ==========================================

def get_image_response(prompt: str, image_file) -> str:
    """
    Analyzes images using Groq's vision model.
    
    Args:
        prompt (str): User's question about the image
        image_file: Streamlit uploaded image file
        
    Returns:
        str: AI analysis of the image
    """
    try:
        if client is None:
            return "❌ Groq Engine not initialized"
        
        import base64
        from io import BytesIO
        from PIL import Image
        
        # Load and process image
        image = Image.open(image_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Convert to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Create vision prompt
        content_payload = [
            {"type": "text", "text": str(prompt)},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
        
        # Call vision model
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": content_payload}],
            temperature=0.3,
            max_tokens=512
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"❌ Image Analysis Error: {str(e)}"


# ==========================================
# AUDIO PROCESSING
# ==========================================

def transcribe_audio(audio_file_buffer) -> str:
    """
    Transcribes audio using Groq's Whisper model.
    
    Args:
        audio_file_buffer: Audio file from Streamlit
        
    Returns:
        str: Transcribed text
    """
    try:
        if client is None:
            return "❌ Groq Engine not initialized"
        
        if not audio_file_buffer:
            return "❌ No audio file provided"
        
        audio_file_buffer.name = "input_audio.wav"
        
        transcription = client.audio.transcriptions.create(
            file=audio_file_buffer,
            model="whisper-large-v3",
            response_format="text"
        )
        
        return transcription
        
    except Exception as e:
        return f"❌ Transcription Error: {str(e)}"


def text_to_speech(text_content: str):
    """
    Converts text to speech using gTTS.
    
    Args:
        text_content (str): Text to convert to speech
        
    Returns:
        bytes: Audio file bytes or None if failed
    """
    try:
        from gtts import gTTS
        from io import BytesIO
        
        tts = gTTS(text=text_content, lang='en', slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.getvalue()
        
    except Exception as e:
        print(f"❌ Text-to-Speech Error: {str(e)}")
        return None


# ==========================================
# BACKWARD COMPATIBILITY FUNCTIONS
# ==========================================

def search_web(query):
    try:
        print("=" * 50)
        print("SEARCHING:", query)
        print("SERPER KEY FOUND:", bool(SERPER_API_KEY))

        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text[:1000])

        if response.status_code != 200:
            return None

        data = response.json()

        snippets = []

        if "organic" in data:
            for item in data["organic"][:5]:

                title = item.get("title", "")
                snippet = item.get("snippet", "")

                snippets.append(
                    f"{title}\n{snippet}"
                )

        if snippets:
            return "\n\n".join(snippets)

        return None

    except Exception as e:
        print("SEARCH ERROR:", e)
        return None


def search_web_only(query: str) -> str:
    """
    Performs web search without LLM processing.
    Useful for getting raw search results.
    
    Args:
        query (str): Search query
        
    Returns:
        str: Raw search results
    """
    from chatbot.search import web_search, wiki_search
    
    # Try web search first
    web_results = web_search(query)
    if web_results:
        return web_results
    
    # Fall back to Wikipedia
    wiki_results = wiki_search(query)
    if wiki_results:
        return wiki_results
    
    return "No search results found"


if __name__ == "__main__":
    # Test the module
    print("=== Testing LLM Module ===\n")
    
    test_queries = [
        "What are the latest cricket scores?",
        "Tell me about artificial intelligence",
        "What's trending today?",
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        response = get_response(query)
        print(f"🤖 Response: {response[:200]}...\n")
