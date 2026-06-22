import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.entities import RetrievedChunk, Source
from app.rag.chunking import chunk_text
from app.rag.embeddings import HashEmbeddingModel
from app.rag.vector_store import InMemoryVectorStore, VectorRecord


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "knowledge_sources.json"


def load_seed_documents() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


class RagPipeline:
    def __init__(self) -> None:
        settings = get_settings()
        self.embedder = HashEmbeddingModel(settings.embedding_dimensions)
        self.top_k = settings.rag_top_k

    def retrieve(self, db: Session, query: str, decision_id: str) -> list[RetrievedChunk]:
        store = InMemoryVectorStore()
        sources = db.query(Source).all()
        source_map = {source.id: source for source in sources}

        for source in sources:
            for chunk in chunk_text(source.id, source.content):
                store.add(
                    VectorRecord(
                        id=f"{source.id}:{chunk.index}",
                        source_id=source.id,
                        text=chunk.text,
                        vector=self.embedder.embed(chunk.text),
                        metadata={"chunk_index": chunk.index},
                    )
                )

        results = store.search(self.embedder.embed(query), self.top_k)
        retrieved: list[RetrievedChunk] = []
        for index, (record, score) in enumerate(results, start=1):
            source = source_map[record.source_id]
            retrieved.append(
                RetrievedChunk(
                    decision_id=decision_id,
                    source_id=source.id,
                    chunk_text=record.text,
                    relevance_score=round(max(score, 0.0), 4),
                    citation_label=f"S{index}",
                    chunk_metadata=record.metadata,
                )
            )
        return retrieved
