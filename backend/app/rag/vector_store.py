from dataclasses import dataclass

from app.rag.embeddings import cosine_similarity


@dataclass
class VectorRecord:
    id: str
    source_id: str
    text: str
    vector: list[float]
    metadata: dict


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.records: list[VectorRecord] = []

    def add(self, record: VectorRecord) -> None:
        self.records.append(record)

    def search(self, query_vector: list[float], top_k: int) -> list[tuple[VectorRecord, float]]:
        ranked = [
            (record, cosine_similarity(query_vector, record.vector)) for record in self.records
        ]
        ranked.sort(key=lambda item: item[1], reverse=True)
        return ranked[:top_k]
