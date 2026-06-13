"""
Serper web search integration for current events queries.

This module loads the Serper API key from the local .env file and exposes a
simple search helper that returns top Google search results.
"""

import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SEARCH_ENDPOINT = "https://google.serper.dev/search"


def search_google(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Search Google via Serper and return the top organic results."""
    print("SEARCH_TRIGGERED", query)
    if not isinstance(query, str):
        raise TypeError("query must be a string")

    if not query.strip():
        return []

    if not SERPER_API_KEY:
        raise RuntimeError(
            "Missing SERPER_API_KEY environment variable. "
            "Set SERPER_API_KEY in .env or the process environment."
        )
    print("SERPER_KEY_FOUND")

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Accept": "application/json",
    }
    params = {
        "q": query,
        "num": num_results,
    }

    try:
        response = requests.get(SEARCH_ENDPOINT, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RuntimeError("Failed to fetch search results from Serper.") from exc

    organic = payload.get("organic", [])
    results: List[Dict[str, Any]] = []
    for item in organic[:num_results]:
        title = item.get("title") or item.get("snippet") or ""
        link = item.get("link") or item.get("source") or ""
        snippet = item.get("snippet") or ""

        results.append(
            {
                "title": title.strip(),
                "link": link.strip(),
                "snippet": snippet.strip(),
            }
        )

    if not results:
        # Fallback to any other result blocks if organic results are missing.
        related = payload.get("related_questions", [])
        for item in related[:num_results]:
            results.append(
                {
                    "title": item.get("question", "").strip(),
                    "link": item.get("link", "").strip(),
                    "snippet": item.get("snippet", "").strip(),
                }
            )

    print("RESULTS_FOUND", len(results))
    return results
