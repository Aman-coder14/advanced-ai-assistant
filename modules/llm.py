"""
AI response generation with visible provider errors.

Provider order:
1. Groq, when GROQ_API_KEY exists.
2. Gemini, when GEMINI_API_KEY exists.
3. OpenAI, when OPENAI_API_KEY exists and the openai package is installed.

The module intentionally does not fail at import time. Streamlit can render the
debug panel and show a useful error even when a key/package is missing.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()
else:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "").strip()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

CURRENT_EVENT_KEYWORDS = [
    "latest news",
    "current events",
    "today",
    "this week",
    "recent updates",
    "2026",
]


def get_ai_debug_status() -> dict[str, Any]:
    return {
        "groq_key": bool(GROQ_API_KEY),
        "gemini_key": bool(GEMINI_API_KEY),
        "openai_key": bool(OPENAI_API_KEY),
        "serper_key": bool(SERPER_API_KEY),
        "provider": _available_providers()[0] if _available_providers() else None,
        "available_providers": _available_providers(),
    }


def generate_response(prompt: str) -> str:
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string")
    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    print("[AI] generate_response started")
    print(f"[AI] prompt length: {len(prompt)}")

    providers = _available_providers()
    if not providers:
        raise RuntimeError(
            "No AI API key found. Add GROQ_API_KEY, GEMINI_API_KEY, or "
            "OPENAI_API_KEY in your deployment secrets or local .env file."
        )

    search_context = _get_optional_search_context(prompt)
    final_prompt = _with_search_context(prompt, search_context)

    errors = []
    answer = ""
    used_provider = ""
    for provider in providers:
        try:
            print(f"[AI] trying provider: {provider}")
            if provider == "groq":
                answer = _generate_with_groq(final_prompt)
            elif provider == "gemini":
                answer = _generate_with_gemini(final_prompt)
            elif provider == "openai":
                answer = _generate_with_openai(final_prompt)
            else:
                raise RuntimeError(f"Unsupported AI provider: {provider}")

            answer = (answer or "").strip()
            if not answer:
                raise RuntimeError(f"{provider} returned an empty response.")
            used_provider = provider
            break
        except Exception as exc:
            errors.append(f"{provider}: {exc}")
            print(f"[AI] provider failed: {provider}: {exc}")

    if not answer:
        raise RuntimeError("All configured AI providers failed. " + " | ".join(errors))

    if search_context:
        answer = f"{answer}\n\nSearch context was used for this answer."

    print(f"[AI] generate_response finished with provider: {used_provider}")
    return answer


def _available_providers() -> list[str]:
    providers = []
    if GROQ_API_KEY:
        providers.append("groq")
    if GEMINI_API_KEY:
        providers.append("gemini")
    if OPENAI_API_KEY:
        providers.append("openai")
    return providers


def _is_current_event_query(prompt: str) -> bool:
    normalized = prompt.lower()
    return any(keyword in normalized for keyword in CURRENT_EVENT_KEYWORDS)


def _get_optional_search_context(prompt: str) -> str:
    if not _is_current_event_query(prompt):
        print("[AI] search not needed")
        return ""

    if not SERPER_API_KEY:
        print("[AI] search skipped: SERPER_API_KEY missing")
        return ""

    try:
        print("[AI] search started")
        from modules.web_search import search_google

        results = search_google(prompt)
        print(f"[AI] search results: {len(results)}")
        return _build_search_context(results)
    except Exception as exc:
        print(f"[AI] search failed: {exc}")
        return ""


def _build_search_context(results: List[Dict[str, Any]]) -> str:
    if not results:
        return ""

    lines = ["Search results:"]
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


def _with_search_context(prompt: str, search_context: str) -> str:
    if not search_context:
        return prompt
    return (
        "Use the following search results to answer the question. "
        "If the question is about current events, base your answer on the results.\n\n"
        f"{search_context}\n\nQuestion: {prompt}"
    )


def _generate_with_groq(prompt: str) -> str:
    try:
        from groq import Groq
    except ImportError as exc:
        raise RuntimeError("Groq SDK is missing. Install it with: pip install groq") from exc

    client = Groq(api_key=GROQ_API_KEY, timeout=45)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer clearly and directly.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    if response is None:
        raise RuntimeError("No response received from Groq.")

    try:
        return str(response.choices[0].message.content).strip()
    except Exception as exc:
        raise RuntimeError("Groq response did not contain assistant text.") from exc


def _generate_with_gemini(prompt: str) -> str:
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "Gemini SDK is missing. Install it with: pip install google-generativeai"
        ) from exc

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)

    if response is None:
        raise RuntimeError("No response received from Gemini.")
    if not hasattr(response, "text"):
        raise RuntimeError("Gemini response has no text attribute.")

    return str(response.text or "").strip()


def _generate_with_openai(prompt: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("OpenAI SDK is missing. Install it with: pip install openai") from exc

    client = OpenAI(api_key=OPENAI_API_KEY, timeout=45)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer clearly and directly.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    if response is None:
        raise RuntimeError("No response received from OpenAI.")

    try:
        return str(response.choices[0].message.content).strip()
    except Exception as exc:
        raise RuntimeError("OpenAI response did not contain assistant text.") from exc
