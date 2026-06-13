import os
import base64
import requests
import wikipedia
import streamlit as st
from groq import Groq

# =========================
# API KEYS CONFIGURATION
# =========================

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)


# =========================
# GOOGLE SEARCH (SERPER)
# =========================

def search_web(query):
    """
    Queries the Serper API to retrieve organic search snippets.
    """
    try:
        if not SERPER_API_KEY:
            print("SERPER API KEY NOT FOUND")
            return None

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

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("SERPER ERROR:", response.text)
            return None

        data = response.json()
        snippets = []

        # Extract up to 5 snippets for reference data
        for item in data.get("organic", [])[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            snippets.append(f"{title}\n{snippet}")

        if snippets:
            return "\n\n".join(snippets)

        return None

    except Exception as e:
        print("SEARCH ERROR:", e)
        return None


# =========================
# WIKIPEDIA FALLBACK
# =========================

def search_wikipedia(query):
    """
    Fallback function to fetch stable summary facts from Wikipedia.
    """
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(
            query,
            sentences=5,
            auto_suggest=True
        )
    except Exception:
        return None


# =========================
# CHAT RESPONSE
# =========================

def get_response(user_input, bypass_search=False):
    """
    Generates text responses using Llama 3.3. 
    Strictly filters out breaking news/live updates to focus on reference facts.
    """
    try:
        if bypass_search:
            prompt = user_input
        else:
            search_data = search_web(user_input)

            if not search_data:
                search_data = search_wikipedia(user_input)

            if not search_data:
                return (
                    "❌ Reference search unavailable.\n\n"
                    "Check:\n"
                    "1. SERPER_API_KEY\n"
                    "2. Serper credits\n"
                    "3. Internet search configuration"
                )

            # Updated prompt format to aggressively reject real-time updates/news style
            prompt = f"""
You are an AI assistant with access to reference information.

REFERENCE CONTEXT DATA:
{search_data}

USER QUESTION:
{user_input}

Rules:
- Provide informational, conceptual, or historical data from the context.
- STRICTLY DO NOT provide the latest news, real-time updates, or trending current events.
- If the user explicitly asks for current breaking news, politely decline, stating you only provide static reference analysis.
- Answer directly without mentioning your knowledge cutoff dates.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that provides factual, structural information while strictly avoiding real-time news reporting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# IMAGE ANALYSIS (FIXED)
# =========================

def get_image_response(user_input, uploaded_image_file):
    """
    Processes images and text using a valid Groq multimodal vision model.
    """
    try:
        image_bytes = uploaded_image_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Dynamically determine the correct MIME type
        ext = uploaded_image_file.name.split(".")[-1].lower()
        if ext in ["jpg", "jpeg"]:
            mime_type = "image/jpeg"
        elif ext == "png":
            mime_type = "image/png"
        else:
            mime_type = f"image/{ext}"

        # Using a certified, functional Groq vision pipeline ID
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_input
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Vision Error: {str(e)}"