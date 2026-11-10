"""CognitiveState: the "pizarra cognitiva" — always external to any LLM context, always
versioned (FR-008, FR-009, Constitution Principio III)."""

from __future__ import annotations

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session as SASession

from oralia.domain.dialogue.contracts import DialogueContext
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow

# FR-009: minimum set of fields every CognitiveState MUST carry.
MINIMUM_FIELDS = (
    "mode",
    "objective",
    "activity_ref",
    "permitted_materials",
    "current_input",
    "participant_response",
    "concepts_addressed",
    "concepts_pending",
    "intent_hypotheses",
    "retrieved_info",
    "open_questions",
    "summarized_history",
    "remaining_time",
    "turn_number",
    "incidents",
    "confidence",
    "next_action_proposed",
)

# FR-009: the type every StatePatch.payload element must be tagged with.
ELEMENT_TYPES = (
    "instruction",
    "observation",
    "participant_statement",
    "retrieved_info",
    "hypothesis",
    "inference",
    "decision",
    "check_result",
    "configuration",
)

# Constitution Principio III: the five memory categories the system MUST distinguish.
# "working" is CognitiveState itself (not a discrete TraceEvent), and "semantic"
# (materiales) has no real content in this feature (Assumptions: sin materiales
# reales todavía) — TraceEvent tagging in this feature therefore uses episodic/
# procedural/metacognitive, the three categories that have real content here.
MEMORY_CATEGORIES = ("working", "episodic", "semantic", "procedural", "metacognitive")


class CognitiveStateSnapshot(BaseModel):
    session_id: str
    version: int
    mode: str
    objective: str
    activity_ref: str
    permitted_materials: list[str] = Field(default_factory=list)
    current_input: str
    participant_response: str
    concepts_addressed: list[str] = Field(default_factory=list)
    concepts_pending: list[str] = Field(default_factory=list)
    intent_hypotheses: list[str] = Field(default_factory=list)
    retrieved_info: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    summarized_history: str
    remaining_time: int
    turn_number: int
    incidents: list[str] = Field(default_factory=list)
    confidence: float
    next_action_proposed: str
    dialogue_context: DialogueContext | None = None


def get_or_create(db: SASession, session_id: str, activity_ref: str) -> models.CognitiveState:
    row = db.get(models.CognitiveState, session_id)
    if row is not None:
        return row
    row = models.CognitiveState(
        session_id=session_id,
        version=0,
        activity_ref=activity_ref,
        updated_at=utcnow(),
    )
    db.add(row)
    db.flush()
    return row


def to_snapshot(row: models.CognitiveState) -> CognitiveStateSnapshot:
    return CognitiveStateSnapshot(
        session_id=row.session_id,
        version=row.version,
        mode=row.mode,
        objective=row.objective,
        activity_ref=row.activity_ref,
        permitted_materials=row.permitted_materials,
        current_input=row.current_input,
        participant_response=row.participant_response,
        concepts_addressed=row.concepts_addressed,
        concepts_pending=row.concepts_pending,
        intent_hypotheses=row.intent_hypotheses,
        retrieved_info=row.retrieved_info,
        open_questions=row.open_questions,
        summarized_history=row.summarized_history,
        remaining_time=row.remaining_time,
        turn_number=row.turn_number,
        incidents=row.incidents,
        confidence=row.confidence,
        next_action_proposed=row.next_action_proposed,
        dialogue_context=row.dialogue_context,
    )
