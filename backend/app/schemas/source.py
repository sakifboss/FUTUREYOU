from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SourceRead(BaseModel):
    id: str
    title: str
    url: str
    publisher: str
    source_type: str
    country: str | None
    summary: str
    tags: list[str]
    reliability_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
