from statistics import mean

from sqlalchemy.orm import Session

from app.models.entities import Decision, RetrievedChunk, Scenario, ScenarioMetric
from app.rag.pipeline import RagPipeline
from app.schemas.decision import (
    DecisionSummary,
    RecommendationRead,
    ScoreRead,
    SimulationResponse,
)
from app.services.decision_service import citation_from_chunk
from app.services.policy import option_policy_score


class ScenarioEngine:
    def __init__(self) -> None:
        self.rag = RagPipeline()

    async def simulate(
        self, db: Session, decision: Decision, regenerate: bool = False
    ) -> SimulationResponse:
        if regenerate:
            for scenario in list(decision.scenarios):
                db.delete(scenario)
            for chunk in list(decision.retrieved_chunks):
                db.delete(chunk)
            db.flush()

        if not decision.scenarios:
            query = self._build_query(decision)
            chunks = self.rag.retrieve(db, query, decision.id)
            for chunk in chunks:
                db.add(chunk)
            db.flush()

            for payload in self._deterministic(decision):
                scenario = Scenario(**payload)
                db.add(scenario)
                db.flush()
                for name, value in {
                    "risk": scenario.risk_level,
                    "opportunity": scenario.opportunity_level,
                    "effort": scenario.effort_level,
                    "probability": scenario.probability,
                }.items():
                    db.add(
                        ScenarioMetric(
                            scenario_id=scenario.id,
                            metric_name=name,
                            metric_value=value,
                        )
                    )

        decision.status = "simulated"
        db.commit()
        db.refresh(decision)
        return self._response(db, decision)

    def _response(self, db: Session, decision: Decision) -> SimulationResponse:
        scores = self._scores(db, decision)
        best_score = max(scores, key=lambda item: item.weighted_score) if scores else None
        confidence = round(min(0.92, 0.5 + len(decision.retrieved_chunks) * 0.06), 2)

        recommendations = [
            RecommendationRead(
                option_id=best_score.option_id if best_score else None,
                title=(
                    f"Prioritize a validation sprint for {best_score.option_label}"
                    if best_score
                    else "Prioritize a validation sprint"
                ),
                rationale=(
                    "This route has the strongest current trade-off score, but the right "
                    "move is to reduce uncertainty before committing."
                ),
                action_items=[
                    "Verify official deadlines, costs, and eligibility.",
                    "Interview 3 people who recently chose a similar path.",
                    "Run a 14-day reversible experiment and rescore the options.",
                ],
            )
        ]

        return SimulationResponse(
            decision_summary=DecisionSummary(
                id=decision.id,
                title=decision.title,
                goal=decision.goal,
                current_age=decision.current_age,
                country_location=decision.country_location,
                risk_tolerance=decision.risk_tolerance,
                time_horizon=decision.time_horizon,
                status=decision.status,
                share_token=decision.share_token,
            ),
            options=[
                {
                    "id": option.id,
                    "label": option.label,
                    "description": option.description,
                    "policy_score": option_policy_score(db, decision, option),
                }
                for option in decision.options
            ],
            scenarios=decision.scenarios,
            scores=scores,
            recommendations=recommendations,
            citations=[citation_from_chunk(chunk) for chunk in decision.retrieved_chunks],
            confidence=confidence,
            disclaimers=[
                "FutureYou simulates plausible futures; it does not predict guaranteed outcomes.",
                "Source-backed claims use retrieved evidence where available; unsupported claims are inference.",
            ],
            next_steps=[
                "Choose the riskiest assumption in each option.",
                "Collect primary-source evidence.",
                "Take one low-regret action this week.",
            ],
        )

    def _scores(self, db: Session, decision: Decision) -> list[ScoreRead]:
        scores: list[ScoreRead] = []
        for option in decision.options:
            option_scenarios = [item for item in decision.scenarios if item.option_id == option.id]
            if not option_scenarios:
                continue
            risk = mean(item.risk_level for item in option_scenarios)
            opportunity = mean(item.opportunity_level for item in option_scenarios)
            effort = mean(item.effort_level for item in option_scenarios)
            cost = 0.65 if "high" in " ".join(s.estimated_cost.lower() for s in option_scenarios) else 0.42
            timeline = 0.55 if "delay" in " ".join(s.estimated_timeline.lower() for s in option_scenarios) else 0.38
            policy = option_policy_score(db, decision, option)
            weighted = (opportunity * 0.4) + ((1 - risk) * 0.25) + ((1 - effort) * 0.15)
            weighted += ((1 - cost) * 0.1) + ((1 - timeline) * 0.05) + (policy * 0.05)
            scores.append(
                ScoreRead(
                    option_id=option.id,
                    option_label=option.label,
                    risk=round(risk, 2),
                    opportunity=round(opportunity, 2),
                    effort=round(effort, 2),
                    cost=round(cost, 2),
                    timeline=round(timeline, 2),
                    confidence=round(0.64 + len(decision.retrieved_chunks) * 0.03, 2),
                    weighted_score=round(weighted, 2),
                )
            )
        return sorted(scores, key=lambda item: item.weighted_score, reverse=True)

    def _build_query(self, decision: Decision) -> str:
        return " ".join(
            [
                decision.country_location,
                decision.current_situation,
                decision.goal,
                " ".join(option.label for option in decision.options),
                " ".join(decision.skills or []),
                decision.budget_constraints or "",
            ]
        )

    def _deterministic(self, decision: Decision) -> list[dict]:
        risk_base = {"low": 0.34, "medium": 0.5, "high": 0.62}.get(decision.risk_tolerance, 0.5)
        scenario_defs = [
            ("best_case", 0.24, -0.14, 0.2, "Momentum compounds"),
            ("realistic_case", 0.52, 0.0, 0.0, "Progress with trade-offs"),
            ("worst_case", 0.24, 0.18, -0.18, "Stress test outcome"),
        ]
        generated: list[dict] = []
        for option_index, option in enumerate(decision.options):
            text = f"{option.label} {option.description or ''}".lower()
            ambition = 0.1 if any(word in text for word in ["startup", "abroad", "freelanc"]) else 0.0
            stability = 0.08 if any(word in text for word in ["job", "study", "local", "stable"]) else 0.0
            for scenario_type, probability, risk_delta, opportunity_delta, title_prefix in scenario_defs:
                risk = min(max(risk_base + risk_delta + ambition - stability + option_index * 0.025, 0.08), 0.92)
                opportunity = min(max(0.58 + opportunity_delta + ambition + stability / 2, 0.12), 0.95)
                effort = min(max(0.46 + ambition + (0.08 if "abroad" in text else 0.0), 0.18), 0.9)
                generated.append(
                    {
                        "decision_id": decision.id,
                        "option_id": option.id,
                        "scenario_type": scenario_type,
                        "title": f"{title_prefix}: {option.label}",
                        "narrative": self._narrative(decision, option.label, scenario_type),
                        "probability": probability,
                        "risk_level": round(risk, 2),
                        "opportunity_level": round(opportunity, 2),
                        "effort_level": round(effort, 2),
                        "estimated_cost": self._cost_label(text, decision.budget_constraints),
                        "estimated_timeline": self._timeline_label(decision.time_horizon, scenario_type),
                        "major_risks": [
                            f"Underestimating the real cost and time required for {option.label}.",
                            "Relying on outdated or non-official information.",
                            "Losing momentum if the plan lacks weekly checkpoints.",
                        ],
                        "major_opportunities": [
                            f"Use existing skills as leverage while testing {option.label}.",
                            "Build a reusable portfolio of evidence, contacts, and applications.",
                            "Choose reversible steps that help across several future paths.",
                        ],
                        "action_path": [
                            f"Write the top 5 assumptions behind choosing {option.label}.",
                            "Verify official deadlines, costs, and requirements.",
                            "Interview 3 people with recent experience.",
                            "Run a 14-day pilot project or application sprint.",
                            "Rescore the decision based on evidence.",
                        ],
                    }
                )
        return generated

    def _narrative(self, decision: Decision, option_label: str, scenario_type: str) -> str:
        if scenario_type == "best_case":
            return (
                f"{option_label} aligns with {decision.goal}. With disciplined validation, "
                "the path builds evidence early and compounds skills toward a stronger position."
            )
        if scenario_type == "worst_case":
            return (
                f"{option_label} becomes difficult if costs, eligibility, market demand, or "
                "personal energy are misread. Fallback triggers reduce the downside."
            )
        return (
            f"{option_label} is plausible but mixed. Progress depends on consistent execution, "
            "source verification, and adjusting when evidence challenges assumptions."
        )

    def _cost_label(self, option_text: str, constraints: str | None) -> str:
        if constraints:
            return f"Constrained by: {constraints[:80]}"
        if any(word in option_text for word in ["abroad", "university", "startup"]):
            return "Medium to high upfront cost"
        if "freelanc" in option_text:
            return "Low upfront cost, variable income risk"
        return "Moderate opportunity cost"

    def _timeline_label(self, horizon: str, scenario_type: str) -> str:
        if scenario_type == "best_case":
            return f"Early traction within {horizon}"
        if scenario_type == "worst_case":
            return f"Delay risk beyond {horizon}"
        return horizon
