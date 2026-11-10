"""Closed dialogue contracts, independent of generation and publication authority."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal, Protocol
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_serializer, model_validator

if TYPE_CHECKING:
    from oralia.domain.policies.output_authorization_contract import AuthorizationSnapshot, OutputProposal

DialogueActName = Literal[
    "greeting",
    "content_question",
    "content_answer",
    "repeat",
    "rephrase",
    "help",
    "continue",
    "example",
    "comparison",
    "topic_switch",
    "mode_switch",
    "finish",
    "ambiguous",
]
StudyMode = Literal[
    "doubt_resolution",
    "guided_explanation",
    "practice_questions",
    "presentation_preparation",
    "concept_review",
]
Profile = Literal["extractive_limited", "guided_controlled", "generative_local_candidate", "degraded"]
ConceptReference = Annotated[str, Field(min_length=1, max_length=100)]


class ClosedModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Referent(ClosedModel):
    kind: Literal["turn", "unit", "topic"]
    ref: str = Field(min_length=1, max_length=100)


class DialogueAct(ClosedModel):
    schema_version: Literal[2] = 2
    primary_act: DialogueActName
    confidence_kind: Literal["heuristic", "calibrated", "not_applicable"] = "heuristic"
    reason_code: Literal[
        "explicit_control",
        "content_input",
        "missing_input",
        "conflicting_controls",
        "ambiguous_reference",
        "negated_control",
        "mode_request",
    ]
    referent_candidate_refs: tuple[Referent, ...] = Field(default=(), max_length=4)
    repeat_target: (
        Literal["question", "last_output", "explanation", "example", "comparison", "hint"] | None
    ) = None
    requested_topic: str | None = Field(default=None, max_length=100)
    requested_mode: StudyMode | None = None
    negated_acts: tuple[DialogueActName, ...] = Field(default=(), max_length=14)
    needs_clarification: bool = False

    @model_validator(mode="after")
    def repeat_target_belongs_to_repeat(self):
        if self.repeat_target is not None and self.primary_act != "repeat":
            raise ValueError("repeat_target requires repeat action")
        return self


class DialogueControl(ClosedModel):
    """A participant button choice, never output approval or an access policy."""

    schema_version: Literal[2] = 2
    action: Literal[
        "repeat",
        "rephrase",
        "help",
        "continue",
        "example",
        "comparison",
        "topic_switch",
        "mode_switch",
        "finish",
    ]
    requested_mode: StudyMode | None = None
    requested_topic: str | None = Field(default=None, min_length=1, max_length=100)

    @model_validator(mode="after")
    def validate_arguments(self):
        if (self.action == "mode_switch") != (self.requested_mode is not None):
            raise ValueError("mode argument belongs only to a mode-switch control")
        if self.requested_topic is not None and self.action != "topic_switch":
            raise ValueError("topic argument belongs only to a topic-switch control")
        return self

    def as_act(self):
        return DialogueAct(
            primary_act=self.action,
            requested_mode=self.requested_mode,
            requested_topic=self.requested_topic,
            reason_code="mode_request" if self.action == "mode_switch" else "explicit_control",
        )


class IntentHypothesis(ClosedModel):
    label: DialogueActName
    confidence_kind: Literal["heuristic", "not_applicable"] = "heuristic"
    reason_code: str = Field(max_length=50)


class EvidenceReference(ClosedModel):
    document_id: UUID
    document_version: int = Field(ge=1)
    fragment_id: UUID


class ClaimFollowup(ClosedModel):
    """Owned input reference, never an endorsement or a copy of a participant claim."""

    participant_turn_id: UUID
    question_unit_id: UUID
    followup_unit_id: UUID
    subgoal_ref: str = Field(min_length=1, max_length=100)
    source_fragment_ids: tuple[UUID, ...] = Field(min_length=1, max_length=5)
    assessment: Literal["not_assessed"] = "not_assessed"


class DialogueContext(ClosedModel):
    schema_version: Literal[1, 2] = 1
    current_topic_ref: str | None = Field(default=None, max_length=100)
    content_query: str = Field(default="", max_length=500)
    pending_question_turn_id: UUID | None = None
    pending_question_unit_id: UUID | None = None
    claim_followup: ClaimFollowup | None = None
    last_approved_unit_ids: tuple[UUID, ...] = Field(default=(), max_length=3)
    pending_topic_ref: str | None = Field(default=None, max_length=100)
    last_approved_turn_id: UUID | None = None
    candidate_referents: tuple[Referent, ...] = Field(default=(), max_length=4)
    selected_referent: Referent | None = None
    intent_hypotheses: tuple[IntentHypothesis, ...] = Field(default=(), max_length=3)
    current_subgoal_ref: str | None = Field(default=None, max_length=100)
    relevant_concepts: tuple[ConceptReference, ...] = Field(default=(), max_length=8)
    support_step: int = Field(default=0, strict=True, ge=0, le=3)
    stalled_signature: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    stalled_count: int = Field(default=0, strict=True, ge=0, le=2)
    last_notice: str | None = Field(default=None, max_length=40)
    offered_actions: tuple[DialogueActName, ...] = Field(default=(), max_length=4)
    effective_profile: Profile = "extractive_limited"
    navigation_page: int = Field(default=0, strict=True, ge=0, le=67)
    pending_conservation: Literal["none", "summary", "transcript", "both"] | None = None
    close_confirmation_pending: bool = Field(default=False, strict=True)
    evidence_refs: tuple[EvidenceReference, ...] = Field(default=(), max_length=5)

    @model_serializer(mode="wrap")
    def serialize_context(self, handler):
        data = handler(self)
        if self.schema_version == 1:
            for name in ("navigation_page", "pending_conservation", "close_confirmation_pending"):
                data.pop(name, None)
        return data


class ProposalPlan(ClosedModel):
    """References only. Resolving a plan still requires current DB authorization."""

    schema_version: Literal[1] = 1
    template_id: str = Field(min_length=1, max_length=100)
    template_version: str = Field(min_length=1, max_length=20)
    template_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    action: DialogueActName
    unit_refs: tuple[UUID, ...] = Field(default=(), max_length=5)
    transformation: Literal[
        "select_reviewed_unit",
        "compose_reviewed_units",
        "material_excerpt/v1",
        "copy_approved_question",
    ] = "select_reviewed_unit"


class DialogueGenerationRequest(ClosedModel):
    """V2 wrapper preserves the existing GenerationRequest v1 unchanged."""

    schema_version: Literal[2] = 2
    plan: ProposalPlan
    session_id: UUID
    turn_id: UUID
    base_version: int = Field(ge=0)


class GuidedGenerationPort(Protocol):
    """V2 proposes a bound output, never free text or its own approval."""

    def render(self, request: DialogueGenerationRequest) -> tuple[AuthorizationSnapshot, OutputProposal]: ...


class SemanticStudyPlan(ClosedModel):
    """A proposal of references/actions, never generated teaching text or authority."""

    schema_version: Literal[1] = 1
    act: Literal["explain", "rephrase", "example", "comparison", "ask", "correct", "clarify", "finish"]
    goal_ref: str | None = Field(default=None, max_length=100, pattern=r"^[a-z0-9_]+$")
    greet: bool = False

    @model_validator(mode="after")
    def content_requires_goal(self):
        if self.act not in {"clarify", "finish"} and self.goal_ref is None:
            raise ValueError("content action requires a goal reference")
        return self


class SemanticIntentPlanV2(SemanticStudyPlan):
    """V2 interpretation includes receiving an answer, without judging its quality."""

    schema_version: Literal[2] = 2
    act: Literal[
        "explain", "rephrase", "example", "comparison", "ask", "correct", "clarify", "finish", "respond"
    ]
    comparison_goal_ref: str | None = Field(default=None, max_length=100, pattern=r"^[a-z0-9_]+$")

    @model_validator(mode="after")
    def bounded_comparison(self):
        if self.comparison_goal_ref is not None:
            if self.comparison_goal_ref == self.goal_ref:
                raise ValueError("comparison requires two distinct goals")
            if self.act not in {"explain", "rephrase", "example", "comparison", "ask", "correct"}:
                raise ValueError("comparison references not allowed for this act")
        return self


class SemanticStudyPlanV2(SemanticIntentPlanV2):
    """Traceable correction proposal; a real quote still cannot prove semantics."""

    schema_version: Literal[2] = 2
    correction_ref: UUID | None = None
    claim_quote: str | None = Field(default=None, min_length=1, max_length=4000)
    reply_to_question_id: UUID | None = None
    scope_limit: bool = False

    @model_validator(mode="after")
    def correction_requires_binding(self):
        if self.scope_limit and (self.act != "clarify" or self.goal_ref is not None):
            raise ValueError("scope limit requires clarification without a selected goal")
        if self.act == "respond" and self.reply_to_question_id is None:
            raise ValueError("response requires pending question reference")
        if self.act == "correct" and (self.correction_ref is None or self.claim_quote is None):
            raise ValueError("correction requires an actual claim and correction reference")
        if self.act != "correct" and (self.correction_ref is not None or self.claim_quote is not None):
            raise ValueError("claim binding is only allowed for correction")
        return self


class SemanticPlanningPort(Protocol):
    async def plan(self, request, cancellation) -> SemanticStudyPlan | SemanticStudyPlanV2: ...
