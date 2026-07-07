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

client = Groq(api_key=GROQ_API_KEY)

# =========================
# GOOGLE SEARCH (SERPER)
# =========================
def search_web(query):
    try:
        if not SERPER_API_KEY:
            return None

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query}

        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code != 200:
            return None

        data = response.json()
        snippets = []
        for item in data.get("organic", [])[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            snippets.append(f"{title}\n{snippet}")

        return "\n\n".join(snippets) if snippets else None
    except Exception:
        return None

# =========================
# WIKIPEDIA FALLBACK
# =========================
def search_wikipedia(query):
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(query, sentences=5, auto_suggest=True)
    except Exception:
        return None

# =========================
# CHAT RESPONSE GENERATOR
# =========================
def get_response(user_input, bypass_search=False):
    try:
        if bypass_search:
            prompt = user_input
        else:
            search_data = search_web(user_input)
            if not search_data:
                search_data = search_wikipedia(user_input)

            if not search_data:
                return "❌ Reference context search failed. Please verify your API setup."

            # Hard constraints to block live news reporting
            prompt = f"""
You are an AI assistant with access to reference information.

REFERENCE CONTEXT DATA:
{search_data}

USER QUESTION:
{user_input}

Rules:
- Provide informational, conceptual, or historical facts from the context data.
- STRICTLY DO NOT provide breaking news, real-time match scores, live updates, or trending current events.
- If the user explicitly asks for current breaking news updates, politely decline, stating you only provide static reference analysis.
- Answer directly without mentioning your knowledge cutoff dates.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that provides factual information while strictly avoiding real-time news reporting."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# IMAGE ANALYSIS
# =========================
def get_image_response(user_input, uploaded_image_file):
    try:
        image_bytes = uploaded_image_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        ext = uploaded_image_file.name.split(".")[-1].lower()
        mime_type = "image/png" if ext == "png" else "image/jpeg"

        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_input},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
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