"""SQLAlchemy models for every entity in specs/001-core-cognitive-runtime/data-model.md.

Field-level comments intentionally omitted where the column name already matches the
data-model.md documentation; consult that file for the authoritative field list.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    text as sql_text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.timeutil import utcnow


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return utcnow()


class Course(Base):
    __tablename__ = "course"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200))
    subject_code: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class RetentionPolicy(Base):
    __tablename__ = "retention_policy"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    version: Mapped[int] = mapped_column(Integer, default=1)
    content_scope: Mapped[str] = mapped_column(String(50))
    retention_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    access_scope: Mapped[str] = mapped_column(String(50))
    purge_rule: Mapped[str] = mapped_column(String(200))


class ActivityConfiguration(Base):
    __tablename__ = "activity_configuration"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    family_id: Mapped[str] = mapped_column(String(36), default=_uuid)
    version: Mapped[int] = mapped_column(Integer, default=1)
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("course.id"))
    name: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(200))
    objective: Mapped[str] = mapped_column(String(1000))
    mode: Mapped[str] = mapped_column(String(50))
    language: Mapped[str] = mapped_column(String(10))
    max_turns: Mapped[int] = mapped_column(Integer)
    max_duration_seconds: Mapped[int] = mapped_column(Integer)
    general_knowledge_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    required_agent_ids: Mapped[list] = mapped_column(JSON, default=list)
    optional_agent_ids: Mapped[list] = mapped_column(JSON, default=list)
    retention_policy_id: Mapped[str] = mapped_column(String(36), ForeignKey("retention_policy.id"))
    output_authorization_policy_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_authorization_policy_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    immutable_since: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class ParticipantCode(Base):
    __tablename__ = "participant_code"

    code: Mapped[str] = mapped_column(String(100), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class AgentContract(Base):
    __tablename__ = "agent_contract"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    agent_id: Mapped[str] = mapped_column(String(100))
    version: Mapped[str] = mapped_column(String(20))
    purpose: Mapped[str] = mapped_column(String(500))
    input_schema_ref: Mapped[str] = mapped_column(String(200))
    output_schema_ref: Mapped[str] = mapped_column(String(200))
    preconditions: Mapped[list] = mapped_column(JSON, default=list)
    postconditions: Mapped[list] = mapped_column(JSON, default=list)
    allowed_sources: Mapped[list] = mapped_column(JSON, default=list)
    allowed_tools: Mapped[list] = mapped_column(JSON, default=list)
    permissions: Mapped[list] = mapped_column(JSON, default=list)
    timeout_ms: Mapped[int] = mapped_column(Integer)
    expected_cost: Mapped[str] = mapped_column(String(200), default="")
    possible_errors: Mapped[list] = mapped_column(JSON, default=list)
    confidence_semantics: Mapped[str] = mapped_column(String(500), default="")
    success_criteria: Mapped[list] = mapped_column(JSON, default=list)
    cancellation_policy: Mapped[str] = mapped_column(String(200), default="")
    trace_fields: Mapped[list] = mapped_column(JSON, default=list)


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200))
    version: Mapped[str] = mapped_column(String(20))
    contract_id: Mapped[str] = mapped_column(String(36), ForeignKey("agent_contract.id"))
    capabilities: Mapped[list] = mapped_column(JSON, default=list)
    availability_status: Mapped[str] = mapped_column(String(20), default="available")
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    contract: Mapped[AgentContract] = relationship(AgentContract)


class Agency(Base):
    __tablename__ = "agency"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200))
    version: Mapped[str] = mapped_column(String(20))
    steps: Mapped[list] = mapped_column(JSON, default=list)
    verifiers_required: Mapped[list] = mapped_column(JSON, default=list)
    fallback_step: Mapped[str | None] = mapped_column(String(36), nullable=True)
    termination_rule: Mapped[str] = mapped_column(String(200), default="")
    # FR-003: the catalog exposes availability status for agentes y agencias alike.
    availability_status: Mapped[str] = mapped_column(String(20), default="available")


class Session(Base):
    """FR-012a: at most one interactive session may hold ``active_lock_token``.

    ``active_lock_token`` is a fixed sentinel string (``"ACTIVE"``) while the session is
    the single active interactive session, and ``NULL`` once closed. SQLite (and every
    other engine we might target — research.md §3) treats multiple ``NULL`` values as
    distinct under a UNIQUE constraint, so any number of closed/historical sessions may
    coexist while at most one row may hold the sentinel at a time.
    """

    __tablename__ = "session"
    __table_args__ = (UniqueConstraint("active_lock_token", name="uq_session_single_active_lock"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    activity_configuration_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("activity_configuration.id")
    )
    participant_code: Mapped[str] = mapped_column(String(100), ForeignKey("participant_code.code"))
    status: Mapped[str] = mapped_column(String(30), default="active")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    turn_count: Mapped[int] = mapped_column(Integer, default=0)
    active_lock_token: Mapped[str | None] = mapped_column(String(10), nullable=True)
    technical_summary_ref: Mapped[str | None] = mapped_column(String(36), nullable=True)


class Turn(Base):
    __tablename__ = "turn"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    index: Mapped[int] = mapped_column(Integer)
    input_text: Mapped[str] = mapped_column(String(4000))
    generated_proposal_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    verification_result_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    dialogue_action_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    output_text: Mapped[str | None] = mapped_column(String(4000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="completed")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resource_usage: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class InternalMessage(Base):
    __tablename__ = "internal_message"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    turn_id: Mapped[str] = mapped_column(String(36), ForeignKey("turn.id"))
    sender_agent_id: Mapped[str] = mapped_column(String(36))
    receiver_agent_id: Mapped[str] = mapped_column(String(36))
    type: Mapped[str] = mapped_column(String(50))
    objective: Mapped[str] = mapped_column(String(500))
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    evidences: Mapped[list] = mapped_column(JSON, default=list)
    sources: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_response: Mapped[str] = mapped_column(String(200), default="")
    success_condition: Mapped[str] = mapped_column(String(200), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class CognitiveState(Base):
    """The 'current' materialized cognitive state — one row per session (research.md §1)."""

    __tablename__ = "cognitive_state"

    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"), primary_key=True)
    version: Mapped[int] = mapped_column(Integer, default=0)
    mode: Mapped[str] = mapped_column(String(50), default="")
    objective: Mapped[str] = mapped_column(String(1000), default="")
    activity_ref: Mapped[str] = mapped_column(String(36), default="")
    permitted_materials: Mapped[list] = mapped_column(JSON, default=list)
    current_input: Mapped[str] = mapped_column(String(4000), default="")
    participant_response: Mapped[str] = mapped_column(String(4000), default="")
    concepts_addressed: Mapped[list] = mapped_column(JSON, default=list)
    concepts_pending: Mapped[list] = mapped_column(JSON, default=list)
    intent_hypotheses: Mapped[list] = mapped_column(JSON, default=list)
    retrieved_info: Mapped[list] = mapped_column(JSON, default=list)
    open_questions: Mapped[list] = mapped_column(JSON, default=list)
    summarized_history: Mapped[str] = mapped_column(String(4000), default="")
    remaining_time: Mapped[int] = mapped_column(Integer, default=0)
    turn_number: Mapped[int] = mapped_column(Integer, default=0)
    incidents: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    next_action_proposed: Mapped[str] = mapped_column(String(200), default="")
    dialogue_context: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class TeachingUnit(Base):
    __tablename__ = "teaching_units"
    __table_args__ = (UniqueConstraint("family_id", "version", name="uq_teaching_unit_family_version"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    family_id: Mapped[str] = mapped_column(String(36), default=_uuid)
    version: Mapped[int] = mapped_column(Integer, default=1)
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("course.id"))
    status: Mapped[str] = mapped_column(String(20), default="draft")
    kind: Mapped[str] = mapped_column(String(20))
    topic_ref: Mapped[str] = mapped_column(String(100))
    subgoal_ref: Mapped[str] = mapped_column(String(100))
    reviewed_content: Mapped[str] = mapped_column(Text)
    source_refs: Mapped[list] = mapped_column(JSON, default=list)
    relations: Mapped[dict] = mapped_column(JSON, default=dict)
    reveal_policy: Mapped[str] = mapped_column(String(30), default="study_only")
    activity_refs: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class TurnRequestReceipt(Base):
    __tablename__ = "turn_request_receipts"
    __table_args__ = (UniqueConstraint("session_id", "client_request_id", name="uq_turn_request_receipt"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    client_request_id: Mapped[str] = mapped_column(String(36))
    payload_sha256: Mapped[str] = mapped_column(String(64))
    turn_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("turn.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class StatePatch(Base):
    """Append-only log — the source of truth for reconstruction and conflict audit."""

    __tablename__ = "state_patch"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    base_version: Mapped[int] = mapped_column(Integer)
    resulting_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proposed_by_agent_id: Mapped[str] = mapped_column(String(36))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    element_type: Mapped[str] = mapped_column(String(30))
    justification: Mapped[str] = mapped_column(String(500), default="")
    applied: Mapped[bool] = mapped_column(Boolean, default=False)
    rejected_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class GeneratedProposal(Base):
    __tablename__ = "generated_proposal"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    turn_id: Mapped[str] = mapped_column(String(36), ForeignKey("turn.id"))
    generator_agent_id: Mapped[str] = mapped_column(String(36))
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class VerificationResult(Base):
    __tablename__ = "verification_result"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    proposal_id: Mapped[str] = mapped_column(String(36), ForeignKey("generated_proposal.id"))
    verifier_agent_id: Mapped[str] = mapped_column(String(36))
    verdict: Mapped[str] = mapped_column(String(20))
    reasons: Mapped[list] = mapped_column(JSON, default=list)
    authorization_context: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class DialogueAction(Base):
    __tablename__ = "dialogue_action"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    turn_id: Mapped[str] = mapped_column(String(36), ForeignKey("turn.id"))
    action_type: Mapped[str] = mapped_column(String(30))
    chosen_by_agent_id: Mapped[str] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class MaterialDocument(Base):
    """specs/002-materials-rag/data-model.md → MaterialDocument."""

    __tablename__ = "material_document"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    family_id: Mapped[str] = mapped_column(String(36), default=_uuid)
    version: Mapped[int] = mapped_column(Integer, default=1)
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("course.id"))
    activity_configuration_ids: Mapped[list] = mapped_column(JSON, default=list)
    filename: Mapped[str] = mapped_column(String(300))
    content_hash: Mapped[str] = mapped_column(String(64))
    mime_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column(Integer)
    language: Mapped[str] = mapped_column(String(10), default="es")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    error_detail: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duplicate_of_document_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class MaterialFragment(Base):
    """specs/002-materials-rag/data-model.md → MaterialFragment."""

    __tablename__ = "material_fragment"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    document_id: Mapped[str] = mapped_column(String(36), ForeignKey("material_document.id"))
    document_version: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String(8000))
    location_ref: Mapped[str] = mapped_column(String(200))
    sequence_index: Mapped[int] = mapped_column(Integer)
    embedding_ref: Mapped[str] = mapped_column(String(64))
    content_type: Mapped[str] = mapped_column(String(30), default="texto")
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("course.id"))
    activity_configuration_ids: Mapped[list] = mapped_column(JSON, default=list)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    indexing_status: Mapped[str] = mapped_column(String(20), default="indexed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Evidence(Base):
    """specs/002-materials-rag/data-model.md → Evidence."""

    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    fragment_id: Mapped[str] = mapped_column(String(36), ForeignKey("material_fragment.id"))
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0)
    supports_claim: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class GroundingVerificationResult(Base):
    """specs/002-materials-rag/data-model.md → GroundingVerificationResult.

    Deliberately independent of ``VerificationResult`` (Feature 001, constitutional) —
    neither table is read or written by the other's code path (FR-030).
    """

    __tablename__ = "grounding_verification_result"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    turn_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    proposal_ref: Mapped[str] = mapped_column(String(200), default="")
    verdict: Mapped[str] = mapped_column(String(30))
    supported_claims: Mapped[list] = mapped_column(JSON, default=list)
    unsupported_claims: Mapped[list] = mapped_column(JSON, default=list)
    evidence_ids: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class MaterialConflictRecord(Base):
    """specs/002-materials-rag/data-model.md → MaterialConflictRecord."""

    __tablename__ = "material_conflict_record"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    document_ids: Mapped[list] = mapped_column(JSON, default=list)
    fragment_ids: Mapped[list] = mapped_column(JSON, default=list)
    conflicting_claims: Mapped[list] = mapped_column(JSON, default=list)
    detected_by_query: Mapped[str] = mapped_column(String(1000), default="")
    review_status: Mapped[str] = mapped_column(String(20), default="pending_review")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class IndexRebuildLock(Base):
    """Single-writer lock for material index rebuilds (research.md §9) — same
    unique-constraint-on-a-sentinel-token pattern as ``Session.active_lock_token``, just
    scoped to the vector index instead of interactive sessions."""

    __tablename__ = "index_rebuild_lock"
    __table_args__ = (UniqueConstraint("active_lock_token", name="uq_index_rebuild_single_active_lock"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    active_lock_token: Mapped[str | None] = mapped_column(String(10), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class TraceEvent(Base):
    __tablename__ = "trace_event"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    turn_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    event_type: Mapped[str] = mapped_column(String(50))
    agent_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    resource_usage: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    memory_category: Mapped[str] = mapped_column(String(20), default="episodic")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class SelfStudyActivityConfig(Base):
    """specs/003-self-study-agency/data-model.md → SelfStudyActivityConfig.

    1:1 with ActivityConfiguration (Feature 001, not modified). Only creatable/updatable
    while ActivityConfiguration.immutable_since is null (research.md §7 of Feature 003).
    """

    __tablename__ = "self_study_activity_config"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    activity_configuration_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("activity_configuration.id"), unique=True
    )
    enabled_modes: Mapped[list] = mapped_column(JSON, default=list)
    summary_authorized: Mapped[bool] = mapped_column(Boolean, default=False)
    practice_reveals_solution: Mapped[bool] = mapped_column(Boolean, default=False)
    retention_authorized: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class PracticeQuestion(Base):
    """specs/003-self-study-agency/data-model.md → PracticeQuestion.

    Acotada a session_id (FR-011/FR-011a) — nunca consultada por participant_code.
    """

    __tablename__ = "practice_question"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    turn_id: Mapped[str] = mapped_column(String(36), ForeignKey("turn.id"))
    question_type: Mapped[str] = mapped_column(String(30))
    objective_ref: Mapped[str] = mapped_column(String(500), default="")
    concepts: Mapped[list] = mapped_column(JSON, default=list)
    fragment_ids: Mapped[list] = mapped_column(JSON, default=list)
    difficulty_hint: Mapped[str] = mapped_column(String(10), default="media")
    reveals_solution: Mapped[bool] = mapped_column(Boolean, default=False)
    generator_used: Mapped[str] = mapped_column(String(20), default="deterministic")
    non_disclosure_attempts: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class CoherenceIncident(Base):
    """specs/003-self-study-agency/data-model.md → CoherenceIncident."""

    __tablename__ = "coherence_incident"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    turn_id: Mapped[str] = mapped_column(String(36), ForeignKey("turn.id"))
    incident_type: Mapped[str] = mapped_column(String(40))
    affected_proposal_ref: Mapped[str | None] = mapped_column(String(36), nullable=True)
    recovery_action: Mapped[str] = mapped_column(String(30))
    combined_verdict_source: Mapped[str] = mapped_column(String(20), default="coherence")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class DefenseActivityConfig(Base):
    """Immutable-after-use configuration for one oral-defense activity."""

    __tablename__ = "defense_activity_config"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    activity_configuration_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("activity_configuration.id"), unique=True
    )
    initial_questions: Mapped[list] = mapped_column(JSON, default=list)
    topics: Mapped[list] = mapped_column(JSON, default=list)
    difficulty_hint: Mapped[str] = mapped_column(String(10), default="media")
    voice_input_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    voice_output_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    summary_authorized: Mapped[bool] = mapped_column(Boolean, default=False)
    transcript_retention_authorized: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Transcript(Base):
    """Provisional local-STT text; source audio is never represented in this schema."""

    __tablename__ = "transcript"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    turn_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("turn.id"), nullable=True)
    raw_text: Mapped[str] = mapped_column(String(4000))
    segments: Mapped[list] = mapped_column(JSON, default=list)
    overall_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    low_confidence: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(30), default="awaiting_confirmation")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class TranscriptCorrection(Base):
    __tablename__ = "transcript_correction"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    transcript_id: Mapped[str] = mapped_column(String(36), ForeignKey("transcript.id"), unique=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"))
    corrected_text: Mapped[str] = mapped_column(String(4000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class ConsentRecord(Base):
    __tablename__ = "consent_record"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"), unique=True)
    decision: Mapped[str] = mapped_column(String(10))
    scope: Mapped[list] = mapped_column(JSON, default=list)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


from oralia.infrastructure.db.ddl.t090_activity_policy_trigger import (  # noqa: E402
    register_activity_policy_trigger,
)

register_activity_policy_trigger(ActivityConfiguration.__table__)


class ActivityGovernance(Base):
    __tablename__ = "activity_governance"
    __table_args__ = (
        UniqueConstraint("family_id", "version", name="uq_governance_family_version"),
        Index(
            "uq_governance_active_family",
            "family_id",
            unique=True,
            sqlite_where=sql_text("status = 'active'"),
        ),
    )

    activity_configuration_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("activity_configuration.id"), primary_key=True
    )
    family_id: Mapped[str] = mapped_column(String(36))
    version: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    model_id: Mapped[str] = mapped_column(String(100), default="deterministic")
    source_activity_configuration_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("activity_configuration.id"), nullable=True
    )
    material_versions: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class SessionPrivacyPreference(Base):
    __tablename__ = "session_privacy_preference"

    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"), primary_key=True)
    retain: Mapped[bool] = mapped_column(Boolean, default=False)
    scope: Mapped[list] = mapped_column(JSON, default=list)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class SessionDeletionReceipt(Base):
    __tablename__ = "session_deletion_receipt"

    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("session.id"), primary_key=True)
    reason: Mapped[str] = mapped_column(String(30))
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    counts: Mapped[dict] = mapped_column(JSON, default=dict)
