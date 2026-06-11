import requests
import os
from dotenv import load_dotenv

load_dotenv()

def search_web(query):

    url = "https://google.serper.dev/search"

    payload = {
        "q": query
    }

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    data = response.json()

    if "organic" in data:

        results = []

        for item in data["organic"][:5]:

            results.append(
                item.get("snippet", "")
            )

        return "\n".join(results)

    return None