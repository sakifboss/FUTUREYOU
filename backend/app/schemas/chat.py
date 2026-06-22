from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    decision_id: str | None = None
    message: str = Field(min_length=2, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    citations: list[dict] = []
