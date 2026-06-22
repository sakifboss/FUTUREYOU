import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-zA-Z0-9+#.]+")


class HashEmbeddingModel:
    """Small deterministic embedding fallback for CPU-only demos.

    It is not a semantic model, but it gives stable lexical retrieval without downloads.
    The vector-store interface is intentionally compatible with replacing this by
    sentence-transformers, OpenAI embeddings, or pgvector embeddings later.
    """

    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_RE.findall(text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))
