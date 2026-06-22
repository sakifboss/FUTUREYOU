import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def new_id() -> str:
    return str(uuid.uuid4())


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)

    decisions: Mapped[list["Decision"]] = relationship(back_populates="user")


class Decision(Base, TimestampMixin):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(180))
    current_age: Mapped[int] = mapped_column(Integer)
    country_location: Mapped[str] = mapped_column(String(120))
    current_situation: Mapped[str] = mapped_column(Text)
    goal: Mapped[str] = mapped_column(Text)
    risk_tolerance: Mapped[str] = mapped_column(String(40))
    time_horizon: Mapped[str] = mapped_column(String(80))
    budget_constraints: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    personality_preferences: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="draft")
    share_token: Mapped[str] = mapped_column(String(36), default=new_id, unique=True)

    user: Mapped[User | None] = relationship(back_populates="decisions")
    options: Mapped[list["DecisionOption"]] = relationship(
        back_populates="decision", cascade="all, delete-orphan"
    )
    scenarios: Mapped[list["Scenario"]] = relationship(
        back_populates="decision", cascade="all, delete-orphan"
    )
    retrieved_chunks: Mapped[list["RetrievedChunk"]] = relationship(
        back_populates="decision", cascade="all, delete-orphan"
    )
    feedback: Mapped[list["Feedback"]] = relationship(
        back_populates="decision", cascade="all, delete-orphan"
    )


class DecisionOption(Base, TimestampMixin):
    __tablename__ = "decision_options"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), index=True)
    label: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)

    decision: Mapped[Decision] = relationship(back_populates="options")
    scenarios: Mapped[list["Scenario"]] = relationship(back_populates="option")


class Scenario(Base, TimestampMixin):
    __tablename__ = "scenarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), index=True)
    option_id: Mapped[str] = mapped_column(ForeignKey("decision_options.id"), index=True)
    scenario_type: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(220))
    narrative: Mapped[str] = mapped_column(Text)
    probability: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[float] = mapped_column(Float)
    opportunity_level: Mapped[float] = mapped_column(Float)
    effort_level: Mapped[float] = mapped_column(Float)
    estimated_cost: Mapped[str] = mapped_column(String(120))
    estimated_timeline: Mapped[str] = mapped_column(String(120))
    major_risks: Mapped[list[str]] = mapped_column(JSON, default=list)
    major_opportunities: Mapped[list[str]] = mapped_column(JSON, default=list)
    action_path: Mapped[list[str]] = mapped_column(JSON, default=list)

    decision: Mapped[Decision] = relationship(back_populates="scenarios")
    option: Mapped[DecisionOption] = relationship(back_populates="scenarios")
    metrics: Mapped[list["ScenarioMetric"]] = relationship(
        back_populates="scenario", cascade="all, delete-orphan"
    )


class ScenarioMetric(Base, TimestampMixin):
    __tablename__ = "scenario_metrics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenarios.id"), index=True)
    metric_name: Mapped[str] = mapped_column(String(80))
    metric_value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str | None] = mapped_column(String(40), nullable=True)

    scenario: Mapped[Scenario] = relationship(back_populates="metrics")


class Source(Base, TimestampMixin):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    title: Mapped[str] = mapped_column(String(240))
    url: Mapped[str] = mapped_column(String(500))
    publisher: Mapped[str] = mapped_column(String(180))
    source_type: Mapped[str] = mapped_column(String(80))
    country: Mapped[str | None] = mapped_column(String(120), nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    reliability_score: Mapped[float] = mapped_column(Float, default=0.75)

    retrieved_chunks: Mapped[list["RetrievedChunk"]] = relationship(back_populates="source")


class RetrievedChunk(Base, TimestampMixin):
    __tablename__ = "retrieved_chunks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), index=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), index=True)
    chunk_text: Mapped[str] = mapped_column(Text)
    relevance_score: Mapped[float] = mapped_column(Float)
    citation_label: Mapped[str] = mapped_column(String(40))
    chunk_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    decision: Mapped[Decision] = relationship(back_populates="retrieved_chunks")
    source: Mapped[Source] = relationship(back_populates="retrieved_chunks")


class ChatHistory(Base, TimestampMixin):
    __tablename__ = "chat_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str | None] = mapped_column(ForeignKey("decisions.id"), nullable=True)
    role: Mapped[str] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(Text)
    chat_metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class Export(Base, TimestampMixin):
    __tablename__ = "exports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), index=True)
    format: Mapped[str] = mapped_column(String(20), default="pdf")
    file_name: Mapped[str] = mapped_column(String(220))


class Feedback(Base, TimestampMixin):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), index=True)
    scenario_id: Mapped[str | None] = mapped_column(ForeignKey("scenarios.id"), nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    helpful: Mapped[bool] = mapped_column(Boolean, default=False)
    saved_plan: Mapped[bool] = mapped_column(Boolean, default=False)
    shared_result: Mapped[bool] = mapped_column(Boolean, default=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    reward_score: Mapped[float] = mapped_column(Float, default=0)

    decision: Mapped[Decision] = relationship(back_populates="feedback")
