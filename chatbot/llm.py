# from groq import Groq
# from dotenv import load_dotenv
# import requests
# import wikipedia
# import os

# # Load .env
# load_dotenv()

# # API Keys
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# print("GROQ KEY FOUND:", bool(GROQ_API_KEY))
# print("SERPER KEY FOUND:", bool(SERPER_API_KEY))

# # Groq Client
# client = Groq(
#     api_key=GROQ_API_KEY
# )

# # -----------------------------
# # GOOGLE SEARCH (SERPER)
# # -----------------------------
# def search_web(query):

#     try:

#         print("Searching Google:", query)

#         url = "https://google.serper.dev/search"

#         headers = {
#             "X-API-KEY": SERPER_API_KEY,
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "q": query
#         }

#         response = requests.post(
#             url,
#             headers=headers,
#             json=payload,
#             timeout=10
#         )

#         data = response.json()

#         print("SERPER RESPONSE:", data)

#         snippets = []

#         if "organic" in data:

#             for item in data["organic"][:5]:

#                 title = item.get("title", "")
#                 snippet = item.get("snippet", "")

#                 snippets.append(
#                     f"{title}\n{snippet}"
#                 )

#         if snippets:

#             return "\n\n".join(snippets)

#         return None

#     except Exception as e:

#         print("Search Error:", e)

#         return None


# # -----------------------------
# # WIKIPEDIA SEARCH
# # -----------------------------
# def search_wikipedia(query):

#     try:

#         wikipedia.set_lang("en")

#         result = wikipedia.summary(
#             query,
#             sentences=5,
#             auto_suggest=True
#         )

#         return result

#     except Exception as e:

#         print("Wikipedia Error:", e)

#         return None


# # -----------------------------
# # MAIN AI FUNCTION
# # -----------------------------
# def get_response(user_input):

#     try:

#         # STEP 1 → Google Search
#         search_data = search_web(user_input)

#         # STEP 2 → Wikipedia Backup
#         if not search_data:

#             search_data = search_wikipedia(
#                 user_input
#             )

#         # STEP 3 → Build Prompt
#         if search_data:

#             prompt = f"""
# Use the information below to answer accurately.

# Information:
# {search_data}

# Question:
# {user_input}

# Rules:
# - Prefer the provided information.
# - Give the latest answer possible.
# - Do not mention knowledge cutoff.
# - If information is unavailable, say so.
# """

#         else:

#             prompt = user_input

#         # STEP 4 → Ask Groq
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
# You are an intelligent AI assistant.

# Always use provided search information
# before relying on your own knowledge.

# Never mention knowledge cutoff dates.
# """
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,
#             max_tokens=1024
#         )

#         return response.choices[0].message.content

#     except Exception as e:

#         return f"Error: {str(e)}"


import os
import requests
import wikipedia
from groq import Groq
from dotenv import load_dotenv

# Load .env
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

print("GROQ KEY FOUND:", bool(GROQ_API_KEY))
print("SERPER KEY FOUND:", bool(SERPER_API_KEY))

# Groq Client
client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# GOOGLE SEARCH (SERPER)
# -----------------------------
def search_web(query):
    try:
        print("Searching Google:", query)
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query}
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        snippets = []
        if "organic" in data:
            for item in data["organic"][:5]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                snippets.append(f"{title}\n{snippet}")
                
        if snippets:
            return "\n\n".join(snippets)
        return None
    except Exception as e:
        print("Search Error:", e)
        return None

# -----------------------------
# WIKIPEDIA SEARCH
# -----------------------------
def search_wikipedia(query):
    try:
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=5, auto_suggest=True)
        return result
    except Exception as e:
        print("Wikipedia Error:", e)
        return None

# -----------------------------
# MAIN AI FUNCTION (FIXED)
# -----------------------------
def get_response(user_input, bypass_search=False):
    """
    Args:
        user_input (str): The prompt or query from the user.
        bypass_search (bool): If True, treats user_input as a fully prepared 
                              system/context prompt (e.g. for PDF RAG or Photo Chat)
                              and skips Google/Wikipedia lookups.
    """
    try:
        # If bypass is True (e.g., from PDF/Photo Chat), use the user_input exactly as built
        if bypass_search:
            prompt = user_input
        else:
            # STEP 1 → Google Search for normal chat
            search_data = search_web(user_input)

            # STEP 2 → Wikipedia Backup
            if not search_data:
                search_data = search_wikipedia(user_input)

            # STEP 3 → Build Prompt with Web Data
            if search_data:
                prompt = f"""
Use the information below to answer accurately.

Information:
{search_data}

Question:
{user_input}

Rules:
- Prefer the provided information.
- Give the latest answer possible.
- Do not mention knowledge cutoff.
- If information is unavailable, say so.
"""
            else:
                prompt = user_input

        # STEP 4 → Ask Groq using Llama-3.3
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an intelligent, helpful AI assistant."
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

        # Replace your get_image_response inside chatbot/llm.py with this final, active model ID:

import base64

def get_image_response(user_input, uploaded_image_file):
    """
    Sends both an image and a text prompt to Groq's active Vision LLM.
    """
    try:
        # 1. Read the bytes from the uploaded Streamlit file buffer
        image_bytes = uploaded_image_file.getvalue()
        
        # 2. Encode the raw bytes into a Base64 string
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        # 3. Determine the correct MIME type based on file extension
        file_extension = uploaded_image_file.name.split(".")[-1].lower()
        mime_type = f"image/{file_extension}"
        if file_extension == "jpg":
            mime_type = "image/jpeg"

        # 4. Request a completion from Groq's active Llama 4 Vision architecture
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", # Updated to the active vision model ID
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
        return f"Vision Analysis Error: {str(e)}"