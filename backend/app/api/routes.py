import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import ChatHistory, Export, Feedback, Source
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.decision import DecisionCreate, DecisionDetail, FeedbackCreate, FeedbackRead
from app.schemas.source import SourceRead
from app.services.decision_service import (
    citation_from_chunk,
    create_decision,
    get_decision,
    list_decisions,
)
from app.services.export_service import build_decision_pdf
from app.services.policy import calculate_reward
from app.services.scenario_engine import ScenarioEngine

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "futureyou-api"}


@router.post("/decisions", status_code=201)
def post_decision(payload: DecisionCreate, db: Session = Depends(get_db)) -> dict:
    decision = create_decision(db, payload)
    return {"id": decision.id, "share_token": decision.share_token, "status": decision.status}


@router.get("/decisions")
def get_decisions(db: Session = Depends(get_db)):
    return list_decisions(db)


@router.get("/decisions/{decision_id}", response_model=DecisionDetail)
def get_decision_detail(decision_id: str, db: Session = Depends(get_db)):
    decision = get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    detail = DecisionDetail.model_validate(decision)
    detail.citations = [citation_from_chunk(chunk) for chunk in decision.retrieved_chunks]
    return detail


@router.post("/decisions/{decision_id}/simulate")
async def simulate_decision(decision_id: str, db: Session = Depends(get_db)):
    decision = get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return await ScenarioEngine().simulate(db, decision)


@router.post("/decisions/{decision_id}/simulate/stream")
async def simulate_decision_stream(decision_id: str, db: Session = Depends(get_db)):
    decision = get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    async def event_stream():
        for event in [
            {"stage": "retrieving", "message": "Retrieving supporting evidence"},
            {"stage": "simulating", "message": "Generating scenario cards"},
            {"stage": "scoring", "message": "Scoring trade-offs"},
        ]:
            yield f"event: progress\ndata: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.2)
        result = await ScenarioEngine().simulate(db, decision)
        yield f"event: complete\ndata: {result.model_dump_json()}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/decisions/{decision_id}/regenerate")
async def regenerate_decision(decision_id: str, db: Session = Depends(get_db)):
    decision = get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return await ScenarioEngine().simulate(db, decision, regenerate=True)


@router.post("/decisions/{decision_id}/feedback", response_model=FeedbackRead)
def post_feedback(decision_id: str, payload: FeedbackCreate, db: Session = Depends(get_db)):
    decision = get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    reward = calculate_reward(
        payload.rating,
        payload.helpful,
        payload.saved_plan,
        payload.shared_result,
    )
    feedback = Feedback(
        decision_id=decision_id,
        scenario_id=payload.scenario_id,
        rating=payload.rating,
        helpful=payload.helpful,
        saved_plan=payload.saved_plan,
        shared_result=payload.shared_result,
        comment=payload.comment,
        reward_score=reward,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return FeedbackRead(
        id=feedback.id,
        reward_score=feedback.reward_score,
        message="Feedback saved and policy reward updated.",
    )


@router.get("/decisions/{decision_id}/export")
def export_decision(decision_id: str, db: Session = Depends(get_db)):
    decision = get_decision(db, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    file_name = f"futureyou-{decision.id}.pdf"
    db.add(Export(decision_id=decision.id, format="pdf", file_name=file_name))
    db.commit()
    return Response(
        content=build_decision_pdf(decision),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@router.get("/sources", response_model=list[SourceRead])
def get_sources(db: Session = Depends(get_db)):
    return db.query(Source).order_by(Source.created_at.desc()).all()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    citations = []
    if payload.decision_id:
        decision = get_decision(db, payload.decision_id)
        if decision:
            citations = [citation_from_chunk(chunk).model_dump() for chunk in decision.retrieved_chunks[:3]]
    answer = (
        "Treat this as scenario simulation, not prediction. Identify the highest-risk "
        "assumption, verify it from primary sources, and run one reversible experiment."
    )
    db.add(ChatHistory(decision_id=payload.decision_id, role="user", content=payload.message))
    db.add(ChatHistory(decision_id=payload.decision_id, role="assistant", content=answer))
    db.commit()
    return ChatResponse(answer=answer, citations=citations)
