from sqlalchemy.orm import Session, selectinload

from app.models.entities import Decision, DecisionOption, RetrievedChunk
from app.schemas.decision import CitationRead, DecisionCreate, DecisionListItem


def create_decision(db: Session, payload: DecisionCreate) -> Decision:
    decision = Decision(
        title=payload.title or _derive_title(payload.goal),
        current_age=payload.current_age,
        country_location=payload.country_location,
        current_situation=payload.current_situation,
        goal=payload.goal,
        risk_tolerance=payload.risk_tolerance,
        time_horizon=payload.time_horizon,
        budget_constraints=payload.budget_constraints,
        skills=payload.skills,
        personality_preferences=payload.personality_preferences,
        status="draft",
    )
    for position, option in enumerate(payload.options):
        decision.options.append(
            DecisionOption(label=option.label, description=option.description, position=position)
        )
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision


def get_decision(db: Session, decision_id: str) -> Decision | None:
    return (
        db.query(Decision)
        .options(
            selectinload(Decision.options),
            selectinload(Decision.scenarios),
            selectinload(Decision.retrieved_chunks).selectinload(RetrievedChunk.source),
        )
        .filter(Decision.id == decision_id)
        .first()
    )


def list_decisions(db: Session) -> list[DecisionListItem]:
    decisions = (
        db.query(Decision)
        .options(selectinload(Decision.options), selectinload(Decision.scenarios))
        .order_by(Decision.updated_at.desc())
        .all()
    )
    return [
        DecisionListItem(
            id=decision.id,
            title=decision.title,
            goal=decision.goal,
            country_location=decision.country_location,
            risk_tolerance=decision.risk_tolerance,
            status=decision.status,
            created_at=decision.created_at,
            updated_at=decision.updated_at,
            option_count=len(decision.options),
            scenario_count=len(decision.scenarios),
        )
        for decision in decisions
    ]


def citation_from_chunk(chunk: RetrievedChunk) -> CitationRead:
    return CitationRead(
        id=chunk.source.id,
        label=chunk.citation_label,
        title=chunk.source.title,
        url=chunk.source.url,
        publisher=chunk.source.publisher,
        source_type=chunk.source.source_type,
        snippet=chunk.chunk_text[:420],
        relevance_score=chunk.relevance_score,
    )


def _derive_title(goal: str) -> str:
    return goal.strip().split(".")[0][:80] or "Untitled decision"
