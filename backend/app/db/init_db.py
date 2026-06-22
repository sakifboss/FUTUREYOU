from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.models.entities import Source
from app.rag.pipeline import load_seed_documents


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def seed_sources(db: Session) -> None:
    if db.query(Source).first():
        return
    for doc in load_seed_documents():
        db.add(
            Source(
                title=doc["title"],
                url=doc["url"],
                publisher=doc["publisher"],
                source_type=doc["source_type"],
                country=doc.get("country"),
                summary=doc["summary"],
                content=doc["content"],
                tags=doc["tags"],
                reliability_score=doc.get("reliability_score", 0.75),
            )
        )
    db.commit()
