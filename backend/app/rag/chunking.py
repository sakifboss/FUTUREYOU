from dataclasses import dataclass


@dataclass
class TextChunk:
    source_id: str
    text: str
    index: int


def chunk_text(source_id: str, text: str, max_words: int = 120, overlap: int = 24) -> list[TextChunk]:
    words = text.split()
    if not words:
        return []

    chunks: list[TextChunk] = []
    start = 0
    index = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(TextChunk(source_id=source_id, text=" ".join(words[start:end]), index=index))
        if end == len(words):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks
