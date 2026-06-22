from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


RiskTolerance = Literal["low", "medium", "high"]


class DecisionOptionCreate(BaseModel):
    label: str = Field(min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=1200)


class DecisionCreate(BaseModel):
    title: str | None = Field(default=None, max_length=180)
    current_age: int = Field(ge=13, le=90)
    country_location: str = Field(min_length=2, max_length=120)
    current_situation: str = Field(min_length=10, max_length=4000)
    goal: str = Field(min_length=5, max_length=2000)
    options: list[DecisionOptionCreate] = Field(min_length=2, max_length=6)
    risk_tolerance: RiskTolerance = "medium"
    time_horizon: str = Field(min_length=2, max_length=80)
    budget_constraints: str | None = Field(default=None, max_length=1500)
    skills: list[str] = Field(default_factory=list, max_length=24)
    personality_preferences: str | None = Field(default=None, max_length=1500)


class DecisionOptionRead(BaseModel):
    id: str
    label: str
    description: str | None = None
    position: int

    model_config = ConfigDict(from_attributes=True)


class ScenarioRead(BaseModel):
    id: str
    decision_id: str
    option_id: str
    scenario_type: str
    title: str
    narrative: str
    probability: float
    risk_level: float
    opportunity_level: float
    effort_level: float
    estimated_cost: str
    estimated_timeline: str
    major_risks: list[str]
    major_opportunities: list[str]
    action_path: list[str]

    model_config = ConfigDict(from_attributes=True)


class CitationRead(BaseModel):
    id: str
    label: str
    title: str
    url: str
    publisher: str
    source_type: str
    snippet: str
    relevance_score: float


class ScoreRead(BaseModel):
    option_id: str
    option_label: str
    risk: float
    opportunity: float
    effort: float
    cost: float
    timeline: float
    confidence: float
    weighted_score: float


class RecommendationRead(BaseModel):
    option_id: str | None = None
    title: str
    rationale: str
    action_items: list[str]


class DecisionSummary(BaseModel):
    id: str
    title: str
    goal: str
    current_age: int
    country_location: str
    risk_tolerance: str
    time_horizon: str
    status: str
    share_token: str


class SimulationResponse(BaseModel):
    decision_summary: DecisionSummary
    options: list[dict]
    scenarios: list[ScenarioRead]
    scores: list[ScoreRead]
    recommendations: list[RecommendationRead]
    citations: list[CitationRead]
    confidence: float
    disclaimers: list[str]
    next_steps: list[str]


class DecisionListItem(BaseModel):
    id: str
    title: str
    goal: str
    country_location: str
    risk_tolerance: str
    status: str
    created_at: datetime
    updated_at: datetime
    option_count: int
    scenario_count: int


class DecisionDetail(BaseModel):
    id: str
    title: str
    current_age: int
    country_location: str
    current_situation: str
    goal: str
    risk_tolerance: str
    time_horizon: str
    budget_constraints: str | None
    skills: list[str]
    personality_preferences: str | None
    status: str
    share_token: str
    created_at: datetime
    updated_at: datetime
    options: list[DecisionOptionRead]
    scenarios: list[ScenarioRead]
    citations: list[CitationRead] = []

    model_config = ConfigDict(from_attributes=True)


class FeedbackCreate(BaseModel):
    scenario_id: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    helpful: bool = False
    saved_plan: bool = False
    shared_result: bool = False
    comment: str | None = Field(default=None, max_length=1200)


class FeedbackRead(BaseModel):
    id: str
    reward_score: float
    message: str
