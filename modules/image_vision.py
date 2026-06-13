import io
import os
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError as exc:
    raise ImportError(
        "google-generativeai is required for image vision support. "
        "Install it with `pip install google-generativeai`."
    ) from exc

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "Missing GEMINI_API_KEY environment variable. "
        "Set GEMINI_API_KEY in .env or the process environment."
    )

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as exc:
    raise RuntimeError(f"Failed to configure Gemini Vision API: {exc}") from exc

MODEL_NAME = "vision-bison"


def analyze_image(question: str, image_bytes: bytes) -> str:
    """Send image and question to Gemini Vision and return the text answer."""
    if not question or not question.strip():
        raise ValueError("Question must not be empty")

    if not image_bytes:
        raise ValueError("Image bytes must be provided")

    try:
        model = genai.ImageModel(MODEL_NAME)
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize Gemini Vision model: {exc}") from exc

    try:
        image_buffer = io.BytesIO(image_bytes)
        response = model.predict(question.strip(), image=image_buffer)
    except Exception as exc:
        raise RuntimeError(f"Gemini Vision API request failed: {exc}") from exc

    answer = ""
    if hasattr(response, "text") and response.text:
        answer = response.text
    elif hasattr(response, "output"):
        outputs = getattr(response, "output")
        if isinstance(outputs, (list, tuple)) and outputs:
            fragments = []
            for item in outputs:
                if hasattr(item, "content") and item.content:
                    fragments.append(item.content)
                elif isinstance(item, dict) and item.get("content"):
                    fragments.append(item["content"])
            answer = "\n".join(fragments)
    elif isinstance(response, dict):
        answer = response.get("output_text") or response.get("text", "")

    return answer.strip() or "No answer could be extracted from the image response."
