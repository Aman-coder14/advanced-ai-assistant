"""
Groq LLM integration with optional real-time search context.

This module loads the Groq API key from .env and uses the Groq Python SDK to
answer prompts. For current event queries, it automatically fetches Google
search results through Serper and passes them to Groq as context.
"""

import os
import re
from typing import Any, Dict, List

from dotenv import load_dotenv

from modules.web_search import search_google

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "Missing GROQ_API_KEY environment variable. "
        "Set GROQ_API_KEY in .env or the process environment."
    )

try:
    from groq import Groq
except ImportError as exc:
    raise ImportError(
        "The Groq SDK is required for modules/llm.py. "
        "Install it with `pip install groq==1.2.0`."
    ) from exc

_MODEL_NAME = "llama-3.3-70b-versatile"
_client = Groq(api_key=GROQ_API_KEY)

_CURRENT_EVENT_KEYWORDS = [
    "latest news",
    "current events",
    "today",
    "this week",
    "recent updates",
    "2026",
]


def _is_current_event_query(prompt: str) -> bool:
    """Detect whether the user prompt requests current or time-sensitive information."""
    normalized = prompt.lower()
    return any(keyword in normalized for keyword in _CURRENT_EVENT_KEYWORDS)


def _build_search_context(results: List[Dict[str, Any]]) -> str:
    """Build a text context from search results for the Groq model."""
    if not results:
        return ""

    lines = ["Search results:" ]
    for idx, result in enumerate(results, start=1):
        title = result.get("title", "").strip()
        link = result.get("link", "").strip()
        snippet = result.get("snippet", "").strip()
        lines.append(f"{idx}. {title}")
        if snippet:
            lines.append(f"   {snippet}")
        if link:
            lines.append(f"   Source: {link}")
    return "\n".join(lines)


def _extract_assistant_text(response: Any) -> str:
    """Extract the assistant message text from a Groq completion response."""
    if response is None:
        return ""

    try:
        return str(response.choices[0].message.content).strip()
    except Exception:
        pass

    if isinstance(response, dict):
        choices = response.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message")
            if isinstance(message, dict):
                return str(message.get("content", "")).strip()

    return ""


def generate_response(prompt: str) -> str:
    """Generate a single assistant response string from a prompt.

    For current event queries, search Google via Serper and supply the results
    as context to Groq. Non-current prompts are answered directly by Groq.
    """
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string")

    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    print("CHECKING_FOR_CURRENT_EVENTS")
    use_search = _is_current_event_query(prompt)
    search_context = ""
    search_results = []

    if use_search:
        print("USING_SEARCH_CONTEXT")
        try:
            search_results = search_google(prompt)
            search_context = _build_search_context(search_results)
        except Exception as exc:
            search_context = ""
    else:
        print("NO_SEARCH_CONTEXT")

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Answer the user clearly and summarize the "
                    "information from the supplied search results when available. Cite the "
                    "source links in your answer."
                ),
            },
        ]

        if search_context:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Use the following search results to answer the question. "
                        "If the question is about current events, base your answer on the results.\n\n"
                        f"{search_context}\n\nQuestion: {prompt}"
                    ),
                }
            )
        else:
            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

        response = _client.chat.completions.create(
            model=_MODEL_NAME,
            messages=messages,
        )
    except Exception as exc:
        raise RuntimeError(
            "Groq API request failed. Check GROQ_API_KEY, network connectivity, "
            "and ensure the Groq service is available."
        ) from exc

    assistant_text = _extract_assistant_text(response)
    if search_results:
        sources = [
            f"{idx}. {result['title']} - {result['link']}"
            for idx, result in enumerate(search_results, 1)
            if result.get("link")
        ]
        if sources:
            assistant_text = (
                f"{assistant_text}\n\nSources used:\n" + "\n".join(sources)
            )

    return assistant_text
