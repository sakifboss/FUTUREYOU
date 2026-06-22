from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.entities import Decision, DecisionOption, Feedback, Scenario


def calculate_reward(
    rating: int | None,
    helpful: bool,
    saved_plan: bool,
    shared_result: bool,
) -> float:
    reward = 0.0
    if helpful:
        reward += 10
    if rating:
        reward += {1: -8, 2: -3, 3: 1, 4: 5, 5: 8}[rating]
    if saved_plan:
        reward += 5
    if shared_result:
        reward += 5
    if not helpful and not rating:
        reward -= 2
    return reward


def option_policy_score(db: Session, decision: Decision, option: DecisionOption) -> float:
    feedback_reward = (
        db.query(func.coalesce(func.avg(Feedback.reward_score), 0.0))
        .join(Scenario, Feedback.scenario_id == Scenario.id, isouter=True)
        .filter(Scenario.option_id == option.id)
        .scalar()
    )
    risk_bias = {"low": -0.08, "medium": 0.0, "high": 0.08}.get(decision.risk_tolerance, 0.0)
    keyword_bonus = 0.0
    text = f"{option.label} {option.description or ''}".lower()
    if "startup" in text or "freelanc" in text:
        keyword_bonus += risk_bias
    if "study" in text or "stable" in text or "job" in text:
        keyword_bonus -= risk_bias / 2
    return round(0.5 + keyword_bonus + min(max(float(feedback_reward) / 100, -0.2), 0.2), 3)
