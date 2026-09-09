from pathlib import Path
from PIL import Image
import streamlit as st

try:
    import google.generativeai as genai
except ImportError as exc:
    raise ImportError(
        "google-generativeai is required for modules.image_ai. "
        "Install it with `pip install google-generativeai`."
    ) from exc

def _get_gemini_api_key() -> str:
    return str(st.secrets.get("GEMINI_API_KEY", "")).strip()


GEMINI_API_KEY = _get_gemini_api_key()
if not GEMINI_API_KEY:
    raise RuntimeError(
        "Missing GEMINI_API_KEY environment variable. "
        "Set GEMINI_API_KEY in Streamlit Secrets."
    )

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as exc:
    raise RuntimeError(f"Failed to configure Gemini Vision API: {exc}") from exc

MODEL_NAME = "gemini-2.5-flash"


def analyze_image(image_path: str, question: str) -> str:

    image_file = Path(image_path)

    if not image_file.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        uploaded_image = Image.open(image_file)

        response = model.generate_content(
            [
                question,
                uploaded_image
            ]
        )

        return response.text

    except Exception as exc:
        raise RuntimeError(
            f"Gemini Vision request failed: {exc}"
        ) from exc

    try:
        with open(image_file, "rb") as fh:
            image_bytes = fh.read()
    except Exception as exc:
        raise RuntimeError(f"Failed to read image file: {exc}") from exc

    try:
        response = model.generate(
            question.strip(),
            image=image_bytes,
        )
    except TypeError:
        try:
            response = model.generate(
                question.strip(),
                input_image=image_bytes,
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini Vision request failed: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Gemini Vision request failed: {exc}") from exc

    answer = ""
    if hasattr(response, "text") and response.text:
        answer = response.text
    elif hasattr(response, "output"):
        output = getattr(response, "output")
        if isinstance(output, str):
            answer = output
        elif isinstance(output, (list, tuple)) and output:
            parts = []
            for item in output:
                if hasattr(item, "content") and item.content:
                    parts.append(item.content)
                elif isinstance(item, dict) and item.get("content"):
                    parts.append(item.get("content"))
            answer = "\n".join(parts)
    elif isinstance(response, dict):
        answer = response.get("text") or response.get("output_text", "")

    return answer.strip() or "No answer could be extracted from the image."
