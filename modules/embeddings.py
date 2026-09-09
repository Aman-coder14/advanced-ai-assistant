from pathlib import Path
import json
from typing import List, Dict, Any, Optional

import numpy as np

try:
    import faiss
except Exception as exc:  # pragma: no cover - informative error
    raise ImportError(
        "faiss is required for modules.embeddings. "
        "Install faiss (e.g. `pip install faiss-cpu`)"
    ) from exc


BASE = Path(__file__).resolve().parents[1]
VECTOR_INDEX_DIR = BASE / "vector_db" / "faiss_index"
METADATA_DIR = BASE / "vector_db" / "metadata"
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_INDEX_DIR / "index.faiss"
META_PATH = METADATA_DIR / "chunks.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def _load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:
        raise RuntimeError(
            "sentence-transformers is not installed correctly."
        ) from exc

    return SentenceTransformer(MODEL_NAME)


def _load_metadata() -> List[Dict[str, Any]]:
    if META_PATH.exists():
        try:
            with open(META_PATH, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return []
    return []


def _save_metadata(meta: List[Dict[str, Any]]) -> None:
    with open(META_PATH, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)


def load_faiss_index() -> Optional[faiss.Index]:
    """Load and return FAISS index if exists, otherwise None."""
    if INDEX_PATH.exists():
        try:
            index = faiss.read_index(str(INDEX_PATH))
            return index
        except Exception as exc:
            raise RuntimeError(f"Failed to load FAISS index: {exc}") from exc
    return None


def save_faiss_index(index: faiss.Index) -> None:
    """Persist FAISS index to disk."""
    try:
        faiss.write_index(index, str(INDEX_PATH))
    except Exception as exc:
        raise RuntimeError(f"Failed to save FAISS index: {exc}") from exc


def create_embeddings(text_chunks: List[str]) -> List[int]:
    """Create embeddings for provided text chunks and add them to the FAISS index.

    Returns the list of integer IDs assigned to the new vectors.
    """
    if not text_chunks:
        return []

    model = _load_model()
    try:
        vectors = model.encode(text_chunks, convert_to_numpy=True, show_progress_bar=False)
    except Exception as exc:
        raise RuntimeError(f"Failed to create embeddings: {exc}") from exc

    vectors = np.asarray(vectors, dtype=np.float32)
    # normalize for cosine-similarity with inner-product index
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    vectors = vectors / norms

    # load existing index or create new
    index = load_faiss_index()
    dim = vectors.shape[1]

    if index is None:
        flat = faiss.IndexFlatIP(dim)
        index = faiss.IndexIDMap(flat)

    # load metadata to compute start id
    meta = _load_metadata()
    existing_ids = [m["id"] for m in meta] if meta else []
    start_id = max(existing_ids) + 1 if existing_ids else 0

    n = vectors.shape[0]
    ids = np.arange(start_id, start_id + n, dtype=np.int64)

    try:
        index.add_with_ids(vectors, ids)
    except Exception as exc:
        raise RuntimeError(f"Failed to add vectors to FAISS index: {exc}") from exc

    # persist index and metadata
    try:
        save_faiss_index(index)
    except Exception as exc:
        raise

    # update metadata
    for i, txt in enumerate(text_chunks):
        meta.append({"id": int(ids[i]), "text": txt})
    _save_metadata(meta)

    return [int(i) for i in ids]


def search_similar_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search the FAISS index for chunks similar to the query.

    Returns a list of dicts: {"id": int, "text": str, "score": float}
    """
    if not query:
        return []

    index = load_faiss_index()
    if index is None:
        return []

    model = _load_model()
    try:
        q_vec = model.encode([query], convert_to_numpy=True)
    except Exception as exc:
        raise RuntimeError(f"Failed to embed query: {exc}") from exc

    q_vec = np.asarray(q_vec, dtype=np.float32)
    q_vec = q_vec / (np.linalg.norm(q_vec, axis=1, keepdims=True) + 1e-10)

    try:
        scores, ids = index.search(q_vec, top_k)
    except Exception as exc:
        raise RuntimeError(f"FAISS search failed: {exc}") from exc

    ids = ids[0].tolist()
    scores = scores[0].tolist()

    meta = _load_metadata()
    meta_map = {m["id"]: m["text"] for m in meta}

    results: List[Dict[str, Any]] = []
    for _id, score in zip(ids, scores):
        if int(_id) == -1:
            continue
        text = meta_map.get(int(_id), "")
        results.append({"id": int(_id), "text": text, "score": float(score)})

    return results
