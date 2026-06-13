import os
from pathlib import Path
from typing import Tuple

from PyPDF2 import PdfReader


def _uploads_dir() -> Path:
    base = Path(__file__).resolve().parents[1]
    uploads = base / "uploads" / "pdfs"
    uploads.mkdir(parents=True, exist_ok=True)
    return uploads


def save_uploaded_file(uploaded_file) -> str:
    """Save a Streamlit uploaded file to uploads/pdfs and return the file path.

    uploaded_file: Streamlit UploadedFile-like object with .name and .read()
    """
    try:
        uploads = _uploads_dir()
        filename = Path(uploaded_file.name).name
        dest = uploads / filename
        # write bytes
        with open(dest, "wb") as f:
            f.write(uploaded_file.read())
        return str(dest)
    except Exception as exc:
        raise RuntimeError(f"Failed to save uploaded file: {exc}") from exc


def extract_pdf_text(file_path: str) -> Tuple[int, str]:
    """Extract text from a PDF file using PyPDF2.

    Returns (number_of_pages, full_text). Raises on failure.
    """
    try:
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        texts = []
        for page in reader.pages:
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            if text:
                texts.append(text)

        full_text = "\n".join(texts)
        return num_pages, full_text
    except Exception as exc:
        raise RuntimeError(f"Failed to extract PDF text: {exc}") from exc
