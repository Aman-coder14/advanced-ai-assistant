from typing import List


def chunk_text(text: str) -> List[str]:
    """Split `text` into chunks of roughly 500-1000 characters with 100-character overlap.

    The function prefers splitting at sentence or newline boundaries to preserve context.

    Args:
        text: Full extracted text.

    Returns:
        List of text chunks.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    cleaned = " ".join(text.split())
    length = len(cleaned)
    if length == 0:
        return []

    CHUNK_MIN = 500
    CHUNK_TARGET = 800
    CHUNK_MAX = 1000
    OVERLAP = 100

    chunks: List[str] = []
    start = 0

    while start < length:
        # preferred end window
        tentative_end = start + CHUNK_TARGET
        if tentative_end >= length:
            end = length
        else:
            # look for a sentence/newline boundary between CHUNK_MIN and CHUNK_MAX
            min_cut = start + CHUNK_MIN
            max_cut = min(start + CHUNK_MAX, length)
            if min_cut >= length:
                end = length
            else:
                segment = cleaned[min_cut:max_cut]
                cut = None
                for i in range(len(segment) - 1, -1, -1):
                    if segment[i] in ".?!\n":
                        cut = min_cut + i + 1
                        break
                if cut is not None and cut > start:
                    end = cut
                else:
                    # fallback to tentative end
                    end = tentative_end

        # safeguard
        if end <= start:
            end = min(start + CHUNK_TARGET, length)

        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= length:
            break

        # move start forward with overlap
        start = max(end - OVERLAP, 0)

        # prevent infinite loops
        if len(chunks) > 10000:
            break

    return chunks
