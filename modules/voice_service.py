from __future__ import annotations

import io
import re
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4

BASE = Path(__file__).resolve().parents[1]
VOICE_UPLOAD_DIR = BASE / "uploads" / "audio"
VOICE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _import_whisper():
    try:
        import whisper
    except ImportError as exc:
        raise ImportError(
            "openai-whisper is required for voice transcription. "
            "Install it with `pip install openai-whisper`."
        ) from exc
    return whisper


def _import_gtts():
    try:
        from gtts import gTTS
    except ImportError as exc:
        raise ImportError(
            "gTTS is required for text-to-speech. "
            "Install it with `pip install gTTS`."
        ) from exc
    return gTTS


def clean_text_for_speech(text: str) -> str:
    """Removes markdown syntax, code blocks, URLs, and extra symbols for natural speech synthesis."""
    if not text:
        return ""
    # Remove code blocks
    cleaned = re.sub(r"```[\s\S]*?```", " Code snippet omitted. ", text)
    # Remove inline code
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    # Remove markdown bold/italic
    cleaned = re.sub(r"\*+([^\*]+)\*+", r"\1", cleaned)
    cleaned = re.sub(r"_+([^_]+)_+", r"\1", cleaned)
    # Remove headers
    cleaned = re.sub(r"^#+\s+", "", cleaned, flags=re.MULTILINE)
    # Remove links
    cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", cleaned)
    # Remove URLs
    cleaned = re.sub(r"https?://\S+", "", cleaned)
    # Normalize spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def transcribe_audio(uploaded_file: BinaryIO) -> str:
    whisper = _import_whisper()
    model = whisper.load_model("tiny")

    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    if not file_bytes:
        raise ValueError("Uploaded audio file is empty.")

    temp_file = VOICE_UPLOAD_DIR / f"voice_{uuid4().hex}_{uploaded_file.name}"
    temp_file.write_bytes(file_bytes)

    audio = whisper.load_audio(str(temp_file))
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    result = model.transcribe(mel, verbose=False)
    text = result.get("text", "") or ""
    return text.strip()


def synthesize_text_to_speech(text: str) -> bytes:
    spoken_text = clean_text_for_speech(text)
    if not spoken_text:
        raise ValueError("Text must not be empty for speech synthesis.")

    gTTS = _import_gtts()
    tts = gTTS(text=spoken_text, lang="en")
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()
