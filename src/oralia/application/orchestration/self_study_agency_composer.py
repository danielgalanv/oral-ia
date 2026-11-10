"""self_study_agency_composer: builds the `AgencyDefinition` for a self-study turn
dynamically per mode (FR-003), executes it via `execute_agency` (Feature 001,
`agency_composer.py`, **reutilizado sin cambios**), and processes the outcome — state
patches, trace logging, dialogue action selection.

Reutiliza sin modificar: `execute_agency`, `run_with_deadline`, `MaterialRetrieverAgent`,
`GroundingVerifierAgent`, `ConstitutionalControl`, `SafeFallbackAgent`,
`CognitiveState`/`apply_patch`, `TraceEvent`/`record_event` (todos de las Features
001/002). Único fichero que compone la `AgencyDefinition` de autoestudio — extendido en
historias posteriores (T032/T033/T035/T039/T042/T049/T056-T059/T068) sin tocar ninguno
de los componentes anteriores (FR-025).
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.configure_self_study_activity import get_self_study_config
from oralia.application.commands.end_study_session import end_study_session
from oralia.application.orchestration.agency_composer import AgencyOutcome, execute_agency
from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.application.orchestration.final_output_gate import (
    FinalOutputDecision,
    UpstreamStatus,
    decide_final_output,
    persist_final_output,
)
from oralia.application.orchestration.output_authorization_context import (
    AuthorizationReferenceInput,
    InvalidAuthorizationContext,
    build_authorization_snapshot,
)
from oralia.application.orchestration.output_proposal_builder import (
    BoundTemplateSlot,
    ProposalConstructionError,
    build_output_proposal,
)
from oralia.application.services.activity_generation_context import configured_generation
from oralia.application.services.trace_service import record_event
from oralia.domain.agencies.agency import AgencyDefinition, ExecutionStep
from oralia.domain.agents.agent_contract import AgentRequest
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent
from oralia.domain.agents.fallback_agent import SAFE_FALLBACK_TEXT, SafeFallbackAgent
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from oralia.domain.agents.material_retriever_agent import (
    MaterialRetrieverAgent,
    get_currently_valid_fragment,
)
from oralia.domain.agents.practice_question_agent import QUESTION_TYPES, PracticeQuestionAgent
from oralia.domain.agents.response_generator_agent import ResponseGeneratorAgent
from oralia.domain.agents.solution_non_disclosure_verifier_agent import SolutionNonDisclosureVerifierAgent
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.materials.extractive_excerpt import extractive_excerpt
from oralia.domain.policies.constitutional_control import (
    SAFE_BLOCKED_MESSAGE,
    ConstitutionalControl,
    constitutional_verdict_or_block,
)
from oralia.domain.policies.constitutional_control import evaluate as constitutional_evaluate
from oralia.domain.policies.output_authorization_contract import (
    AuthorizationReason,
    ScopeReference,
)
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    MATERIAL_FRAGMENT_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE_2,
    MATERIAL_FRAGMENT_RESPONSE_3,
    OutputTemplateCatalog,
    OutputTemplateEntry,
    output_text_sha256,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.generation import config as generation_config
from oralia.infrastructure.generation.deterministic_adapter import DeterministicGenerationAdapter
from oralia.infrastructure.generation.generation_port import (
    EvidenceItem,
    GenerationConstraints,
    GenerationRequest,
)

_ACKNOWLEDGE_MISSING_INFO_TEXT = (
    "No he encontrado información suficiente en los materiales de la actividad para "
    "responder con precisión a esto. ¿Puedes reformular tu pregunta o consultarlo con "
    "el profesorado?"
)
_CONFLICTIVE_TEXT = (
    "Los materiales de la actividad contienen información que parece contradictoria "
    "sobre esto. Te recomiendo consultarlo con el profesorado."
)
_INCOHERENCE_TEXT = (
    "Antes de continuar, creo que conviene revisar el hilo de la conversación: puede "
    "que ya hayamos tratado esto o que convenga reformularlo. ¿Quieres que lo retomemos "
    "de otra forma?"
)

# research.md §5: fixed severity order shared by grounding and coherence, used to
# combine both verdicts (FR-024) — `block > reformulate > clarify >
# acknowledge_missing_info > approved`.
_SEVERITY_RANK = {"approved": 0, "acknowledge_missing_info": 1, "clarify": 2, "reformulate": 3, "block": 4}

_MAX_CONCEPT_LABEL_CHARS = 60


class ModeNotEnabled(ValueError):
    """T056/FR-003: `requested_mode` is not in `SelfStudyActivityConfig.enabled_modes`
    — caught by the router and surfaced as `409` (contracts/api-self-study.md)."""

    def __init__(self, *, requested_mode: str, enabled_modes: list[str]) -> None:
        self.requested_mode = requested_mode
        self.enabled_modes = enabled_modes
        super().__init__(f"mode {requested_mode!r} is not in enabled_modes {enabled_modes!r}")


@dataclass
class StudyTurnResult:
    turn_id: str
    mode: str
    dialogue_action: str
    output_text: str | None
    blocked: bool
    state_version: int | None
    status: str
    sources: list[dict] = field(default_factory=list)
    general_knowledge_used: bool = False
    session_closed: bool = False
    session_status: str | None = None
    study_summary: dict | None = None
    dialogue_status: dict | None = None


def _concept_label(input_text: str) -> str:
    label = input_text.strip()
    if len(label) > _MAX_CONCEPT_LABEL_CHARS:
        label = label[:_MAX_CONCEPT_LABEL_CHARS].rsplit(" ", 1)[0] + "…"
    return label


def _sources_from_fragments(fragments: list[dict]) -> list[dict]:
    return [
        {
            "document_id": fragment["document_id"],
            "document_version": fragment["document_version"],
            "location_ref": fragment["location_ref"],
            "fragment_text": fragment["text"],
        }
        for fragment in fragments
    ]


# research.md §5 / T033: mapeo (parcial — solo fundamentación; US6/T068 añade
# coherencia) de los 5 veredictos de `GroundingVerifierAgent` (Feature 002, sin
# cambios) a la escala de severidad `block > reformulate > clarify >
# acknowledge_missing_info > approved` compartida con `verify-combined` (US6).
_GROUNDING_SEVERITY = {
    "fundamentada": "approved",
    "parcialmente_fundamentada": "reformulate",
    "no_verificable": "reformulate",
    "conflictiva": "clarify",
    "no_fundamentada": "acknowledge_missing_info",
}


def grounding_verdict_severity(verdict: str) -> str:
    return _GROUNDING_SEVERITY.get(verdict, "acknowledge_missing_info")


# FR-009/T038: sub-intentions that adapt `purpose` within the current mode without
# switching `CognitiveState.mode` (research.md §6).
_INTENT_PURPOSE = {
    "simpler_explanation": "explicacion_progresiva",
    "example": "ejemplo",
    "comparison": "comparacion",
}


def step_role(agency: AgencyDefinition, step_id: str) -> str:
    for step in agency.steps:
        if step.step_id == step_id:
            return step.role
    return ""


def _mode_validation_reasoning(requested_mode: str | None, current_mode: str | None) -> dict:
    """T057: full mode-validation reasoning for `agents_selected.payload`. A rejected
    `requested_mode` never reaches this point (`ModeNotEnabled` is raised earlier), so
    by construction `requested_mode` here is either `None` or already a valid, enabled
    mode (research.md §6)."""

    if requested_mode and requested_mode != current_mode:
        return {
            "requested_mode": requested_mode,
            "switched": True,
            "reason": (
                f"'{requested_mode}' fue solicitado explícitamente, está en "
                "enabled_modes y difiere del modo previo"
            ),
        }
    if requested_mode and requested_mode == current_mode:
        return {
            "requested_mode": requested_mode,
            "switched": False,
            "reason": f"'{requested_mode}' fue solicitado explícitamente pero coincide con el modo ya activo",
        }
    return {
        "requested_mode": None,
        "switched": False,
        "reason": "sin solicitud explícita de cambio de modo — continúa el modo activo",
    }


async def _decide_study_output(
    db: SASession,
    *,
    session: models.Session,
    turn_id: str,
    text: str,
    fragments_used: list[dict],
    general_knowledge_used: bool,
    upstream_status: UpstreamStatus = "ok",
    material_query: str = "",
) -> FinalOutputDecision:
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    policy = None
    context_failure_reason = AuthorizationReason.MISSING_POLICY
    if (
        activity.output_authorization_policy_json is not None
        and activity.output_authorization_policy_sha256 is not None
    ):
        context_failure_reason = AuthorizationReason.INVALID_CONTEXT
        try:
            policy = load_output_authorization_policy(
                activity.output_authorization_policy_json,
                activity.output_authorization_policy_sha256,
            )
        except (TypeError, ValueError):
            policy = None

    entries = list(DEFAULT_OUTPUT_TEMPLATE_CATALOG.entries)
    normal_entry = None
    references: tuple[AuthorizationReferenceInput, ...] = ()
    slots: tuple[BoundTemplateSlot, ...] = ()
    projected_bindings: list[dict] = []
    persisted_template = getattr(activity, "normal_output_template", None)
    if persisted_template and persisted_template.get("text") == text:
        normal_entry = OutputTemplateEntry(
            template_id=persisted_template["template_id"],
            version=persisted_template["template_version"],
            message_type="normal",
            text=persisted_template["text"],
            sha256=persisted_template["sha256"],
            topic_ref=persisted_template["topic_ref"],
            purpose_ref=persisted_template["purpose_ref"],
            action_ref=persisted_template["action_ref"],
        )
        entries = [
            entry
            for entry in entries
            if (entry.template_id, entry.version) != (normal_entry.template_id, normal_entry.version)
        ]
        entries.append(normal_entry)
    elif policy is not None:
        allowed_template_pairs = {
            (reference.template_id, reference.version) for reference in policy.allowed_templates
        }
        normal_entry = next(
            (
                entry
                for entry in entries
                if entry.message_type == "normal"
                and entry.text == text
                and (entry.template_id, entry.version) in allowed_template_pairs
            ),
            None,
        )
        material_templates = (
            (MATERIAL_FRAGMENT_RESPONSE, ("content",)),
            (MATERIAL_FRAGMENT_RESPONSE_2, ("content_0", "content_1")),
            (MATERIAL_FRAGMENT_RESPONSE_3, ("content_0", "content_1", "content_2")),
        )
        material_match = next(
            (
                (entry, placeholders, fragments_used[: len(placeholders)], projected)
                for entry, placeholders in material_templates
                for projected in (False, True)
                if (entry.template_id, entry.version) in allowed_template_pairs
                and len(fragments_used) >= len(placeholders)
                and text
                == " ".join(
                    (
                        extractive_excerpt(str(fragment.get("text", ""))).text
                        if projected
                        else str(fragment.get("text", ""))
                    )
                    for fragment in fragments_used[: len(placeholders)]
                )
            ),
            None,
        )
        query_spans = {}
        if policy.policy_id == "material-self-study/v2":
            material_match = None  # V2 never falls back to whole-fragment/v1 binding.
            from oralia.domain.materials.query_excerpt import select_query_excerpts

            plan = select_query_excerpts(fragments_used, material_query)
            query_spans = {span.fragment_id: span for span in plan}
            if plan and text == " ".join(span.text for span in plan):
                entry, placeholders = material_templates[len(plan) - 1]
                if (entry.template_id, entry.version) in allowed_template_pairs:
                    by_id = {f["fragment_id"]: f for f in fragments_used}
                    material_match = (entry, placeholders, [by_id[span.fragment_id] for span in plan], "v2")
        if normal_entry is None and material_match is not None:
            material_entry, placeholders, matched_fragments, projected = material_match
            scope = ScopeReference(
                topic_ref=material_entry.topic_ref,
                purpose_ref=material_entry.purpose_ref,
                action_ref=material_entry.action_ref,
            )
            scope_allowed = (
                scope.topic_ref in policy.allowed_scopes.topics
                and scope.purpose_ref in policy.allowed_scopes.purposes
                and scope.action_ref in policy.allowed_scopes.actions
            )
            built_references: list[AuthorizationReferenceInput] = []
            built_slots: list[BoundTemplateSlot] = []
            for placeholder, fragment in zip(placeholders, matched_fragments, strict=True):
                fragment_id = fragment.get("fragment_id")
                document_id = fragment.get("document_id")
                document_version = fragment.get("document_version")
                location_ref = fragment.get("location_ref")
                row = (
                    get_currently_valid_fragment(
                        db,
                        fragment_id,
                        course_id=activity.course_id,
                        activity_configuration_id=activity.id,
                    )
                    if isinstance(fragment_id, str)
                    else None
                )
                document = (
                    db.get(models.MaterialDocument, document_id) if isinstance(document_id, str) else None
                )
                metadata_valid = (
                    row is not None
                    and document is not None
                    and row.document_id == document_id
                    and row.document_version == document_version
                    and row.location_ref == location_ref
                    and document.version == document_version
                    and row.text == fragment.get("text")
                )
                category = row.content_type if row is not None else "invalid"
                disclosure_allowed = any(
                    rule.category == category
                    and rule.provenance == "activity_material"
                    and rule.recipient == session.participant_code
                    for rule in policy.allowed_disclosures
                )
                authorized = (
                    metadata_valid
                    and session.participant_code in policy.allowed_recipients
                    and disclosure_allowed
                    and scope_allowed
                )
                # Reconstruct only after DB scope, identity and complete source checks.
                # Candidate text, offsets or hashes never supply trusted values.
                excerpt = None
                if authorized and projected:
                    if projected == "v2":
                        excerpt = query_spans.get(fragment_id)
                        authorized = bool(
                            excerpt is not None
                            and excerpt.source_sha256 == output_text_sha256(row.text)
                            and 0 <= excerpt.start < excerpt.end <= len(row.text)
                            and row.text[excerpt.start : excerpt.end] == excerpt.text
                        )
                    else:
                        excerpt = extractive_excerpt(row.text)
                data_ref = f"fragment:{fragment_id}"
                if excerpt is not None:
                    data_ref += (
                        f":excerpt-{'v2' if projected == 'v2' else 'v1'}:{excerpt.source_sha256}:"
                        f"{excerpt.start}:{excerpt.end}"
                    )
                    projected_bindings.append(
                        {
                            "profile": "material-query-excerpt" if projected == "v2" else "material-excerpt",
                            "version": 2 if projected == "v2" else 1,
                            "fragment_id": fragment_id,
                            "document_id": document_id,
                            "document_version": document_version,
                            "location_ref": location_ref,
                            "source_sha256": excerpt.source_sha256,
                            "start": excerpt.start,
                            "end": excerpt.end,
                            "value_sha256": output_text_sha256(excerpt.text),
                        }
                    )
                reference = AuthorizationReferenceInput(
                    data_ref=data_ref,
                    category=category,
                    provenance="activity_material",
                    recipient=session.participant_code,
                    scope=scope,
                    value=(excerpt.text if excerpt is not None else row.text) if authorized else None,
                )
                built_references.append(reference)
                if authorized:
                    built_slots.append(
                        BoundTemplateSlot(
                            placeholder=placeholder,
                            data_ref=reference.data_ref,
                        )
                    )
            references = tuple(built_references)
            normal_entry = material_entry
            if len(built_slots) == len(placeholders):
                slots = tuple(built_slots)

    catalog = OutputTemplateCatalog(entries=tuple(entries))
    snapshot = None
    proposal = None
    if policy is not None:
        try:
            snapshot = build_authorization_snapshot(
                session,
                activity,
                data_references=references,
                catalog=catalog,
            )
            proposal = (
                build_output_proposal(
                    snapshot,
                    template_id=normal_entry.template_id,
                    template_version=normal_entry.version,
                    template_sha256=normal_entry.sha256,
                    slots=slots,
                    catalog=catalog,
                )
                if normal_entry is not None and (not references or slots)
                else None
            )
        except (InvalidAuthorizationContext, ProposalConstructionError, TypeError, ValueError):
            snapshot = None
            proposal = None

    initial_verdict = None
    if snapshot is not None:
        constitutional = ConstitutionalControl()
        request_input = {
            "proposal_text": text,
            "fallback_attempt": 0,
        }
        if proposal is not None:
            request_input["proposal"] = proposal
        verifier_result = await run_with_deadline(
            constitutional,
            AgentRequest(
                session_id=uuid.UUID(session.id),
                turn_id=uuid.UUID(turn_id),
                input=request_input,
                context={
                    "authorization_snapshot": snapshot,
                    "activity_configuration_id": activity.id,
                    "actual_recipient": session.participant_code,
                },
                deadline_ms=constitutional.contract.timeout_ms,
            ),
        )
        initial_verdict = constitutional_verdict_or_block(verifier_result)

    decision = decide_final_output(
        snapshot,
        proposal,
        initial_verdict=initial_verdict,
        initial_failure_reason=(
            AuthorizationReason.INVALID_CONTEXT
            if upstream_status == "ok" and snapshot is not None and proposal is None
            else None
        ),
        context_failure_reason=context_failure_reason,
        upstream_status=upstream_status,
        catalog=catalog,
        allow_operational_attempt=bool(policy is not None and policy.allowed_operational_messages),
    )
    if projected_bindings and not decision.blocked and decision.final_proposal == proposal:
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="material_excerpt_bound",
            agent_id="self-study-agency-composer",
            payload={"schema_version": 1, "bindings": projected_bindings},
            memory_category="procedural",
        )
    return decision


async def _finalize_turn(
    db: SASession,
    *,
    session: models.Session,
    turn: models.Turn,
    turn_id: str,
    cognitive_state: models.CognitiveState,
    base_version: int,
    active_mode: str,
    input_text: str,
    interpreted: dict,
    text: str,
    blocked: bool,
    status: str,
    dialogue_action: str,
    fragments_used: list[dict],
    generator_agent_id: str,
    started_at: float,
    extra_patches: list[tuple[str, dict]],
    general_knowledge_used: bool = False,
    coherence_incidents: list[dict] | None = None,
) -> StudyTurnResult:
    """Shared tail of `run_study_turn` — persists Turn/GeneratedProposal/
    VerificationResult/DialogueAction (Feature 001 tables, reutilizadas sin cambios),
    applies the common `StatePatch` chain plus each mode's `extra_patches`, and logs the
    turn-level `TraceEvent`s. Every mode composition (doubt_resolution, guided_explanation,
    practice_questions, and — US5 — presentation_preparation/concept_review) converges
    here so this bookkeeping is written once (Principio XI)."""

    proposed_dialogue_action = dialogue_action
    decision = await _decide_study_output(
        db,
        session=session,
        turn_id=turn_id,
        text=text,
        fragments_used=fragments_used,
        general_knowledge_used=general_knowledge_used,
        upstream_status="error" if status in {"degraded", "failed"} else "ok",
        material_query=input_text,
    )
    text = decision.output_text
    blocked = decision.blocked
    status = decision.turn_status
    dialogue_action = (
        proposed_dialogue_action
        if not decision.blocked and decision.dialogue_action == "respond"
        else decision.dialogue_action
    )
    turn.output_text = text
    turn.status = status
    turn.ended_at = utcnow()
    turn.latency_ms = int((time.monotonic() - started_at) * 1000)
    db.add(turn)
    db.flush()

    persisted = persist_final_output(
        db,
        turn,
        decision,
        generator_agent_id=generator_agent_id,
    )
    proposal = db.get(models.GeneratedProposal, persisted.proposal_id)
    verification = db.get(models.VerificationResult, persisted.verification_result_id)

    # T068/data-model.md: CoherenceIncident rows, keyed to the proposal just created.
    for incident in coherence_incidents or []:
        db.add(
            models.CoherenceIncident(
                session_id=session.id,
                turn_id=turn_id,
                incident_type=incident["incident_type"],
                affected_proposal_ref=proposal.id,
                recovery_action=incident["recovery_action"],
                combined_verdict_source=incident["combined_verdict_source"],
            )
        )
    if coherence_incidents:
        db.flush()

    action = models.DialogueAction(
        turn_id=turn_id, action_type=dialogue_action, chosen_by_agent_id="self-study-agency-composer"
    )
    db.add(action)
    db.flush()

    turn.generated_proposal_id = proposal.id
    turn.verification_result_id = verification.id
    turn.dialogue_action_id = action.id
    db.add(turn)
    session.turn_count += 1
    db.add(session)
    db.flush()

    turn_patches = [
        ("participant_statement", {"current_input": input_text}),
        ("hypothesis", {"intent_hypotheses": interpreted.get("intent_hypotheses", [])}),
        ("decision", {"mode": active_mode}),
        ("decision", {"participant_response": text or ""}),
        ("decision", {"next_action_proposed": dialogue_action}),
        ("observation", {"turn_number": session.turn_count}),
        *extra_patches,
    ]
    running_version = base_version
    patch = None
    for element_type, payload in turn_patches:
        patch = apply_patch(
            db,
            session_id=session.id,
            base_version=running_version,
            proposed_by_agent_id="self-study-agency-composer",
            element_type=element_type,
            payload=payload,
            justification=f"self-study turn {turn_id} ({status})",
        )
        if not patch.applied:
            break
        running_version = patch.resulting_version

    record_event(
        db,
        session_id=session.id,
        turn_id=turn_id,
        event_type="turn_completed" if status == "completed" else f"turn_{status}",
        payload={"dialogue_action": dialogue_action, "blocked": blocked, "mode": active_mode},
        latency_ms=turn.latency_ms,
        memory_category="episodic",
    )

    if blocked:
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="constitutional_block",
            agent_id="constitutional-control",
            payload={"reasons": verification.reasons},
            memory_category="metacognitive",
        )

    if turn.output_text is None:
        end_study_session(
            db,
            session,
            get_self_study_config(db, session.activity_configuration_id),
            status="closed_error_safe",
        )

    sources = _sources_from_fragments(fragments_used) if not blocked else []

    return StudyTurnResult(
        turn_id=turn_id,
        mode=active_mode,
        dialogue_action=dialogue_action,
        output_text=turn.output_text,
        blocked=blocked,
        state_version=patch.resulting_version if patch else base_version,
        status=status,
        sources=sources,
        general_knowledge_used=general_knowledge_used if not blocked else False,
    )


async def _run_practice_questions_turn(
    db: SASession,
    *,
    session: models.Session,
    turn: models.Turn,
    turn_id: str,
    activity: models.ActivityConfiguration,
    self_study_config: models.SelfStudyActivityConfig | None,
    cognitive_state: models.CognitiveState,
    base_version: int,
    active_mode: str,
    current_mode: str | None,
    requested_mode: str | None,
    input_text: str,
    interpreted: dict,
    fragments: list[dict],
    activated_steps: list[dict],
    skipped_modes: list[str],
    started_at: float,
) -> StudyTurnResult:
    """T049: composición `practice_questions` — interpret→retrieve (ya hecho por el
    llamante, opcional para este modo)→generate-question→verify-non-disclosure (solo si
    `reveals_solution=false`)→verify-constitutional→decide=`ask`. Regeneración acotada
    (`ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS`) → `DeterministicGenerationAdapter` directo si
    se agotan los intentos (research.md §4)."""

    reveals_solution = bool(self_study_config.practice_reveals_solution) if self_study_config else False
    concepts = list(cognitive_state.concepts_addressed)

    # FR-011a: previous_questions filtrado exclusivamente por session_id.
    previous_rows = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session.id).all()
    )
    previous_questions = [{"question_type": r.question_type, "concepts": r.concepts} for r in previous_rows]

    practice_agent = PracticeQuestionAgent()
    non_disclosure_verifier = SolutionNonDisclosureVerifierAgent()
    practice_question_id = str(uuid.uuid4())
    max_attempts = generation_config.get_practice_regen_max_attempts()

    final_question: dict | None = None
    final_trace: dict = {"adapter": "deterministic", "model": None, "fallback_used": False}
    non_disclosure_attempts = 0
    degraded = False

    for attempt in range(1, max_attempts + 1):
        gen_request = AgentRequest(
            session_id=uuid.UUID(session.id),
            turn_id=uuid.UUID(turn_id),
            input={
                "evidence": fragments,
                "objective_ref": activity.objective,
                "concepts": concepts,
                "previous_questions": previous_questions,
                "reveals_solution": reveals_solution,
            },
            deadline_ms=practice_agent.contract.timeout_ms,
        )
        gen_result = await run_with_deadline(practice_agent, gen_request)
        if gen_result.status != "ok":
            degraded = True
            break

        output = gen_result.output or {}
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="agent_execution",
            agent_id="practice-question-agent",
            payload={"step_id": "generate-question", "status": "ok", "attempt": attempt},
            latency_ms=int((time.monotonic() - started_at) * 1000),
            memory_category="procedural",
        )

        if reveals_solution:
            final_question = output
            final_trace = output.get("generation_trace", final_trace)
            break

        nd_request = AgentRequest(
            session_id=uuid.UUID(session.id),
            turn_id=uuid.UUID(turn_id),
            input={
                "question_text": output.get("question_text", ""),
                "internal_expected_answer": output.get("internal_expected_answer") or "",
                "reveals_solution": reveals_solution,
                "attempt_number": attempt,
            },
            deadline_ms=non_disclosure_verifier.contract.timeout_ms,
        )
        nd_result = await run_with_deadline(non_disclosure_verifier, nd_request)
        non_disclosure_attempts = attempt
        nd_output = nd_result.output or {} if nd_result.status == "ok" else {}
        nd_verdict = nd_output.get("verdict", "block")

        # T051: non_disclosure_check TraceEvent per attempt (data-model.md).
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="non_disclosure_check",
            agent_id="solution-non-disclosure-verifier",
            payload={
                "question_id": practice_question_id,
                "verdict": nd_verdict,
                "overlap_score": nd_output.get("overlap_score"),
                "attempt": attempt,
            },
            memory_category="metacognitive" if nd_verdict == "block" else "procedural",
        )

        if nd_verdict == "approved":
            final_question = output
            final_trace = output.get("generation_trace", final_trace)
            break
    else:
        # Bounded regeneration exhausted without an "approved" verdict — fall back to
        # the deterministic adapter directly (research.md §4: extractive construction
        # separates question_text from internal_expected_answer by design, no leak risk).
        deterministic = DeterministicGenerationAdapter()
        fallback_request = GenerationRequest(
            purpose="pregunta_practica",
            instruction="",
            evidence=[EvidenceItem(**f) for f in fragments],
            concepts_addressed=concepts,
            general_knowledge_allowed=False,
            constraints=GenerationConstraints(reveal_solution=reveals_solution),
        )
        fallback_outcome = await deterministic.generate(fallback_request)
        final_question = {
            "question_type": QUESTION_TYPES[len(previous_questions) % len(QUESTION_TYPES)],
            "question_text": fallback_outcome.text,
            "internal_expected_answer": (
                None if reveals_solution else fallback_outcome.internal_expected_answer
            ),
            "difficulty_hint": "media",
            "reveals_solution": reveals_solution,
        }
        final_trace = {"adapter": "deterministic", "model": None, "fallback_used": True}

    activated_steps.append(
        {"step_id": "generate-question", "agent_id": "practice-question-agent", "role": "generator"}
    )
    if not reveals_solution:
        activated_steps.append(
            {
                "step_id": "verify-non-disclosure",
                "agent_id": "solution-non-disclosure-verifier",
                "role": "verifier",
            }
        )

    if degraded:
        candidate_text = SAFE_FALLBACK_TEXT
        status = "degraded"
        verdict, reasons = constitutional_evaluate(candidate_text)
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="agent_execution",
            agent_id="constitutional-control",
            payload={"step_id": "verify-fallback", "status": "ok", "verdict": verdict},
            memory_category="metacognitive",
        )
        blocked = verdict == "block"
        text = SAFE_BLOCKED_MESSAGE if blocked else candidate_text
        dialogue_action = "clarify"
        if blocked:
            status = "blocked"
    else:
        assert final_question is not None
        activated_steps.append(
            {"step_id": "verify-constitutional", "agent_id": "constitutional-control", "role": "verifier"}
        )
        blocked = False
        text = final_question["question_text"]
        dialogue_action = "ask"
        status = "completed"

        db.add(
            models.PracticeQuestion(
                id=practice_question_id,
                session_id=session.id,
                turn_id=turn_id,
                question_type=final_question["question_type"],
                objective_ref=activity.objective or "",
                concepts=concepts,
                fragment_ids=[f["fragment_id"] for f in fragments],
                difficulty_hint=final_question.get("difficulty_hint", "media"),
                reveals_solution=reveals_solution,
                generator_used=final_trace.get("adapter", "deterministic"),
                non_disclosure_attempts=non_disclosure_attempts,
            )
        )
        db.flush()

        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="generation_call",
            agent_id="practice-question-agent",
            payload={
                "adapter": final_trace.get("adapter"),
                "model": final_trace.get("model"),
                "parameters": {},
                "purpose": "pregunta_practica",
                "fragment_ids": [f["fragment_id"] for f in fragments],
                "fallback_used": final_trace.get("fallback_used", False),
                "general_knowledge_used": False,
            },
            memory_category="metacognitive" if final_trace.get("fallback_used") else "procedural",
        )

    record_event(
        db,
        session_id=session.id,
        turn_id=turn_id,
        event_type="agents_selected",
        payload={
            "mode": active_mode,
            "activated_steps": activated_steps,
            "reasons": {s["step_id"]: f"paso requerido por el modo {active_mode}" for s in activated_steps},
            "skipped_modes": skipped_modes,
            "mode_validation": _mode_validation_reasoning(requested_mode, current_mode),
        },
        memory_category="procedural",
    )

    return await _finalize_turn(
        db,
        session=session,
        turn=turn,
        turn_id=turn_id,
        cognitive_state=cognitive_state,
        base_version=base_version,
        active_mode=active_mode,
        input_text=input_text,
        interpreted=interpreted,
        text=text,
        blocked=blocked,
        status=status,
        dialogue_action=dialogue_action,
        fragments_used=fragments if not blocked else [],
        generator_agent_id="practice-question-agent",
        started_at=started_at,
        extra_patches=[],
        general_knowledge_used=False,
    )


@configured_generation
async def run_study_turn(
    db: SASession, session: models.Session, input_text: str, *, dialogue_control=None, semantic_runtime=None
) -> StudyTurnResult:
    from oralia.application.services.guided_dialogue_service import is_guided, run_guided_turn

    if is_guided(db, session.activity_configuration_id):
        value = await run_guided_turn(
            db,
            session,
            input_text,
            dialogue_control=dialogue_control,
            **({"semantic_runtime": semantic_runtime} if semantic_runtime is not None else {}),
        )
        return StudyTurnResult(
            **{
                key: value[key]
                for key in (
                    "turn_id",
                    "mode",
                    "dialogue_action",
                    "output_text",
                    "blocked",
                    "state_version",
                    "status",
                    "sources",
                    "dialogue_status",
                )
            },
            study_summary=value["summary"],
        )
    started_at = time.monotonic()
    turn_id = str(uuid.uuid4())

    if dialogue_control is not None:
        raise ValueError("Los controles estructurados requieren una actividad con perfil guiado.")
    turn = models.Turn(
        id=turn_id,
        session_id=session.id,
        index=session.turn_count,
        input_text=input_text,
        status="in_progress",
        started_at=utcnow(),
    )
    db.add(turn)
    db.flush()

    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    self_study_config = get_self_study_config(db, session.activity_configuration_id)
    enabled_modes = self_study_config.enabled_modes if self_study_config else []

    cognitive_state = get_or_create(db, session.id, activity_ref=session.activity_configuration_id)
    base_version = cognitive_state.version
    current_mode = cognitive_state.mode or None

    # T068/research.md §5: `prior_statements` for CoherenceVerifierAgent MUST be only
    # the immediately preceding turn's output_text — never the full session history.
    previous_turn = (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session.id, models.Turn.id != turn_id)
        .order_by(models.Turn.started_at.desc())
        .first()
    )
    prior_statements = [previous_turn.output_text] if previous_turn and previous_turn.output_text else []

    activated_steps: list[dict] = []

    # --- 1. Interpret intent (outside execute_agency — it drives composition itself,
    # research.md §6). Reuses run_with_deadline (Feature 001, sin cambios) so timeouts
    # degrade the same way as any other agent call.
    interpreter = StudyIntentInterpreterAgent()
    interpret_request = AgentRequest(
        session_id=uuid.UUID(session.id),
        turn_id=uuid.UUID(turn_id),
        input={
            "text": input_text,
            "enabled_modes": enabled_modes,
            "current_mode": current_mode,
            "concepts_addressed": cognitive_state.concepts_addressed,
        },
        deadline_ms=interpreter.contract.timeout_ms,
    )
    interpret_result = await run_with_deadline(interpreter, interpret_request)
    interpreted = interpret_result.output or {}
    activated_steps.append(
        {"step_id": "interpret", "agent_id": "study-intent-interpreter", "role": "retriever"}
    )

    # research.md §6: `CognitiveState.mode` is the source of truth for the active mode;
    # a valid `requested_mode` (in `enabled_modes`, different from the current one)
    # switches it via the `decision`/`mode` StatePatch applied below with the rest of
    # this turn's patches. T038's non-mode sub-intentions (simpler_explanation/example/
    # comparison/topic_change/finish) leave `requested_mode=None` and never switch mode.
    requested_mode = interpreted.get("requested_mode")

    # T056/FR-003 Edge Cases: a mode explicitly requested but not in `enabled_modes`
    # MUST be rejected before any retrieval/generation agent runs and without proposing
    # any `StatePatch` (research.md §6). The router's `get_db` dependency (Feature 001,
    # unchanged) rolls back the whole request on any raised exception — same pattern
    # already used for every other rejection in this codebase (404/409) — so nothing
    # (not even this Turn's own row) is persisted for a rejected request.
    if requested_mode and enabled_modes and requested_mode not in enabled_modes:
        raise ModeNotEnabled(requested_mode=requested_mode, enabled_modes=enabled_modes)

    if requested_mode and requested_mode in (enabled_modes or ()):
        active_mode = requested_mode
    elif current_mode:
        active_mode = current_mode
    else:
        active_mode = requested_mode or "doubt_resolution"

    primary_intent = interpreted.get("primary_intent")
    if active_mode == "guided_explanation":
        purpose = "explicacion_progresiva"
    elif active_mode == "presentation_preparation":
        purpose = "estructura_exposicion"
    elif active_mode == "concept_review":
        purpose = "resumen"
    else:
        purpose = _INTENT_PURPOSE.get(primary_intent, "explicacion")

    # T059: `concept_review` builds its retrieval query from `concepts_addressed`
    # (research.md §6) — it reviews what the session already covered, it MUST NOT
    # formulate an unrelated new question/topic from the student's free-form text.
    #
    # T085 (Feature 002, H08/research.md §14.2): an adaptation request ("Dame un
    # ejemplo de esto", "Explícamelo más sencillo") — already recognized by
    # `primary_intent`/`_INTENT_PURPOSE` as adapting the SAME topic, not introducing a
    # new one — carries little topical content of its own ("esto" is anaphoric); under
    # the relevance floor this MUST NOT be sent as the retrieval query verbatim, since
    # it can legitimately score below the threshold against every fragment even though
    # the topic it refers to is still fully covered. Reuse the previous turn's input
    # text (the actual topic being adapted) instead — the same principle
    # `concept_review` already applies, generalized to any recognized adaptation
    # intent.
    material_excerpt_version = 1
    try:
        material_policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        )
        if material_policy.policy_id == "material-self-study/v2":
            material_excerpt_version = 2
    except (TypeError, ValueError):
        pass  # The final gate still rejects the invalid policy.
    if active_mode == "concept_review" and cognitive_state.concepts_addressed:
        retrieval_query_text = " ".join(cognitive_state.concepts_addressed)
    elif primary_intent in _INTENT_PURPOSE and previous_turn and previous_turn.input_text:
        retrieval_query_text = previous_turn.input_text
    else:
        retrieval_query_text = input_text

    if material_excerpt_version == 2 and previous_turn and previous_turn.output_text:
        from oralia.domain.materials.query_excerpt import terms

        if len(terms(input_text)) <= 4:
            retrieval_query_text = previous_turn.input_text + " " + input_text

    # --- 2. Retrieve (outside execute_agency too — research.md §2, Nivel 0: whether
    # evidence exists at all decides which agency gets composed for the rest of the
    # turn, so it MUST be known before the agency is built).
    material_retriever = MaterialRetrieverAgent(db)
    retrieve_request = AgentRequest(
        session_id=uuid.UUID(session.id),
        turn_id=uuid.UUID(turn_id),
        input={
            "query_text": retrieval_query_text,
            "course_id": activity.course_id,
            "activity_configuration_id": activity.id,
            "session_id": session.id,
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
        deadline_ms=material_retriever.contract.timeout_ms,
    )
    retrieve_result = await run_with_deadline(material_retriever, retrieve_request)
    retrieve_output = (
        retrieve_result.result if hasattr(retrieve_result, "result") else retrieve_result
    ).output or {}
    fragments = retrieve_output.get("fragments", [])
    activated_steps.append({"step_id": "retrieve", "agent_id": "material-retriever", "role": "retriever"})
    record_event(
        db,
        session_id=session.id,
        turn_id=turn_id,
        event_type="agent_execution",
        agent_id="material-retriever",
        payload={"step_id": "retrieve", "status": retrieve_result.status, "fragment_count": len(fragments)},
        latency_ms=int((time.monotonic() - started_at) * 1000),
        memory_category="procedural",
    )

    skipped_modes = [m for m in enabled_modes if m != active_mode]

    # T049: `practice_questions` es una composición estructuralmente distinta (genera
    # preguntas, no respuestas fundamentadas) — se resuelve en su propio helper en vez
    # de forzarla dentro del pipeline generate/verify-grounding de los demás modos.
    if active_mode == "practice_questions":
        return await _run_practice_questions_turn(
            db,
            session=session,
            turn=turn,
            turn_id=turn_id,
            activity=activity,
            self_study_config=self_study_config,
            cognitive_state=cognitive_state,
            base_version=base_version,
            active_mode=active_mode,
            current_mode=current_mode,
            requested_mode=requested_mode,
            input_text=input_text,
            interpreted=interpreted,
            fragments=fragments,
            activated_steps=activated_steps,
            skipped_modes=skipped_modes,
            started_at=started_at,
        )

    # T039/T058/T059: los modos que progresan turno a turno sobre el mismo material
    # (`guided_explanation`, `presentation_preparation`, `concept_review`) cubren un
    # único fragmento pendiente de `CognitiveState.concepts_pending` (Feature 001,
    # campo ya existente) por turno en vez de toda la evidencia recuperada a la vez —
    # además de evitar repetir contenido ya visto (research.md §5: la comprobación de
    # repetición de `CoherenceVerifierAgent` compara contra el turno inmediatamente
    # anterior, así que reenviar la misma evidencia turno tras turno dispararía falsos
    # positivos precisamente en estos modos).
    #
    # T085 (Feature 002, H08/research.md §14.2): la recuperación de este turno ahora
    # aplica un umbral de relevancia — una consulta de continuación con poco contenido
    # propio ("continúa", "sigue estructurando...") MUST NOT reducirse a "sin
    # evidencia" solo porque su propio texto puntúa bajo; ya existe una cola de
    # material vetado (`concepts_pending`) que justifica seguir. Por eso el `if` de
    # abajo también entra cuando `fragments` viene vacío pero la cola no lo está, y
    # `nivel_0_skip` (más abajo) se decide sobre `active_fragments` ya resuelto, no
    # sobre `fragments` en crudo.
    _PROGRESSIVE_MODES = ("guided_explanation", "presentation_preparation", "concept_review")
    active_fragments = fragments
    guided_pending_after: list[str] = []
    if active_mode in _PROGRESSIVE_MODES and (fragments or cognitive_state.concepts_pending):
        # T085 (Feature 002, H08/research.md §14.2): `fragments` is now filtered by a
        # relevance floor, so a low-content follow-up turn (e.g. "continúa") can
        # legitimately retrieve FEWER fragments than a richer earlier turn — that is
        # correct retrieval behavior, not a sign the queued material is gone.
        #
        # T099 (follow-up to T085): a queued id MUST NOT be trusted as still
        # authorized/current just because it was vetted when it was enqueued — that
        # authorization can go stale between turns (document deactivated/retired,
        # fragment expired/de-indexed/unassigned/moved to another course, or its row
        # deleted outright). Every reuse revalidates fresh against SQL
        # (`get_currently_valid_fragment`). Relevance is the one thing that IS
        # deliberately inherited here — reusing evidence already selected for an
        # anaphoric continuation ("continúa") is the whole point of this queue, so a
        # revalidated entry MUST NOT be re-run through the 0.35 floor. Walk the queue
        # from the head, discarding each entry that fails revalidation and trying the
        # next one (bounded — the queue only shrinks) — never substitute a discarded
        # entry with an unrelated fragment.
        remaining_pending = list(cognitive_state.concepts_pending)
        valid_fragment: models.MaterialFragment | None = None
        while remaining_pending:
            candidate_id = remaining_pending.pop(0)
            valid_fragment = get_currently_valid_fragment(
                db,
                candidate_id,
                course_id=activity.course_id,
                activity_configuration_id=activity.id,
            )
            if valid_fragment is not None:
                break

        if valid_fragment is not None:
            current_fragment_id = valid_fragment.id
            guided_pending_after = remaining_pending
            active_fragments = [f for f in fragments if f["fragment_id"] == current_fragment_id]
            if not active_fragments:
                active_fragments = [
                    {
                        "fragment_id": valid_fragment.id,
                        "document_id": valid_fragment.document_id,
                        "document_version": valid_fragment.document_version,
                        "location_ref": valid_fragment.location_ref,
                        "text": valid_fragment.text,
                        "relevance_score": None,
                    }
                ]
        elif fragments:
            # No queued entry survived revalidation, but this turn's own retrieval —
            # already authorized/current/relevant via `MaterialRetrieverAgent` — found
            # something: reseed the queue from it (first turn on this material, or the
            # entire prior queue has gone stale).
            pending = [f["fragment_id"] for f in fragments]
            current_fragment_id = pending[0]
            guided_pending_after = pending[1:]
            active_fragments = [f for f in fragments if f["fragment_id"] == current_fragment_id]
        else:
            # Nothing valid pending, and nothing retrieved this turn — Nivel 0 below
            # (acknowledge_missing_info, no fabricated evidence).
            active_fragments = []
            guided_pending_after = []

    # research.md §2, Nivel 0: sin evidencia + conocimiento general desactivado → no se
    # inventa contenido, se omite la generación por completo (FR-008a). Decidido sobre
    # `active_fragments` (no el `fragments` en crudo de este turno): para los modos
    # progresivos, una cola ya vetada (`concepts_pending`) resuelta arriba cuenta como
    # evidencia aunque la recuperación de este turno concreto no aportara nada nuevo.
    if material_excerpt_version == 2:
        from oralia.domain.materials.query_excerpt import select_query_excerpts

        selected_spans = select_query_excerpts(active_fragments, input_text)
        selected_ids = {span.fragment_id for span in selected_spans}
        active_fragments = [f for f in active_fragments if f["fragment_id"] in selected_ids]
    nivel_0_skip = not active_fragments and not activity.general_knowledge_allowed
    response_generator = (
        ResponseGeneratorAgent(primary=DeterministicGenerationAdapter())
        if material_excerpt_version == 2
        else ResponseGeneratorAgent()
    )
    if material_excerpt_version == 2:
        response_generator.contract = response_generator.contract.model_copy(
            update={
                "version": "1.1.0",
                "input_schema_ref": "specs/011-real-course-self-study/contracts/self-study.md#extractive-v2",
            }
        )
    grounding_verifier = GroundingVerifierAgent(db)
    coherence_verifier = CoherenceVerifierAgent()
    safe_fallback = SafeFallbackAgent()

    agent_registry = {
        "response-generator": response_generator,
        "grounding-verifier": grounding_verifier,
        "coherence-verifier": coherence_verifier,
        "safe-fallback": safe_fallback,
    }

    if nivel_0_skip:
        steps = [
            ExecutionStep(step_id="fallback", agent_id="safe-fallback", role="presenter"),
        ]
    else:
        steps = [
            ExecutionStep(step_id="generate", agent_id="response-generator", role="generator"),
            ExecutionStep(
                step_id="verify-grounding",
                agent_id="grounding-verifier",
                role="verifier",
                depends_on=["generate"],
            ),
            ExecutionStep(
                step_id="verify-coherence",
                agent_id="coherence-verifier",
                role="verifier",
                depends_on=["generate"],
            ),
            ExecutionStep(step_id="fallback", agent_id="safe-fallback", role="presenter"),
        ]

    agency = AgencyDefinition(
        id="self-study-doubt-resolution",
        name="Resolución de dudas",
        version="1.0.0",
        steps=steps,
        verifiers_required=[s.step_id for s in steps if s.role == "verifier"],
        fallback_step="fallback",
        termination_rule="finish after verify steps (or fallback if a prior step fails)",
    )

    def request_for_step(step: ExecutionStep, outcome: AgencyOutcome) -> AgentRequest:
        if step.step_id == "generate":
            return AgentRequest(
                session_id=uuid.UUID(session.id),
                turn_id=uuid.UUID(turn_id),
                input={
                    "purpose": purpose,
                    "student_input": input_text,
                    "material_excerpt_version": material_excerpt_version,
                    "evidence": active_fragments,
                    "concepts_addressed": cognitive_state.concepts_addressed,
                    "general_knowledge_allowed": activity.general_knowledge_allowed,
                },
                deadline_ms=response_generator.contract.timeout_ms,
            )
        if step.step_id == "verify-grounding":
            generate_outcome = next(s for s in outcome.steps if s.step_id == "generate")
            proposal_text = (generate_outcome.result.output or {}).get("proposal_text", "")
            evidence = [{"fragment_id": f["fragment_id"], "text": f["text"]} for f in active_fragments]
            return AgentRequest(
                session_id=uuid.UUID(session.id),
                turn_id=uuid.UUID(turn_id),
                input={
                    "proposal_text": proposal_text,
                    "evidence": evidence,
                    "general_knowledge_allowed": activity.general_knowledge_allowed,
                },
                deadline_ms=grounding_verifier.contract.timeout_ms,
            )
        if step.step_id == "verify-coherence":
            generate_outcome = next(s for s in outcome.steps if s.step_id == "generate")
            proposal_text = (generate_outcome.result.output or {}).get("proposal_text", "")
            return AgentRequest(
                session_id=uuid.UUID(session.id),
                turn_id=uuid.UUID(turn_id),
                input={
                    "proposal_text": proposal_text,
                    "prior_statements": prior_statements,
                    "active_sources": [f["text"] for f in active_fragments],
                    "concepts_addressed": cognitive_state.concepts_addressed,
                    "turn_number": session.turn_count,
                    "max_turns": activity.max_turns,
                },
                deadline_ms=coherence_verifier.contract.timeout_ms,
            )
        # fallback
        return AgentRequest(
            session_id=uuid.UUID(session.id),
            turn_id=uuid.UUID(turn_id),
            input={},
            deadline_ms=safe_fallback.contract.timeout_ms,
        )

    outcome = await execute_agency(agency, agent_registry, request_for_step)

    activated_steps.extend(
        {"step_id": s.step_id, "agent_id": s.agent_id, "role": step_role(agency, s.step_id)}
        for s in outcome.steps
    )

    # --- agent_execution TraceEvent per remaining step (Constitution III)
    for step_outcome in outcome.steps:
        step_failed = step_outcome.result.status != "ok"
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="agent_execution",
            agent_id=step_outcome.agent_id,
            payload={"step_id": step_outcome.step_id, "status": step_outcome.result.status},
            latency_ms=int((time.monotonic() - started_at) * 1000),
            memory_category="metacognitive" if step_failed else "procedural",
        )

    degraded = outcome.status == "failed" or outcome.fallback_used
    fragments_used: list[dict] = []
    general_knowledge_used = False
    coherence_incidents: list[dict] = []

    if nivel_0_skip and not degraded:
        status = "completed"
        blocked = False
        text = _ACKNOWLEDGE_MISSING_INFO_TEXT
        dialogue_action = "acknowledge_missing_info"
    elif degraded:
        candidate_text = SAFE_FALLBACK_TEXT
        dialogue_action = "clarify"
        status = "degraded" if outcome.status != "failed" else "failed"
        verdict, reasons = constitutional_evaluate(candidate_text)
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="agent_execution",
            agent_id="constitutional-control",
            payload={"step_id": "verify-fallback", "status": "ok", "verdict": verdict},
            memory_category="metacognitive",
        )
        blocked = verdict == "block"
        text = SAFE_BLOCKED_MESSAGE if blocked else candidate_text
        if blocked:
            status = "blocked"

        # T068/FR-015: `fallo_agente`/`latencia_excesiva` derivados directamente de
        # `AgencyOutcome` (Feature 001, `execute_agency`, sin cambios) — nunca vía
        # CoherenceVerifierAgent (research.md §5).
        timed_out = any(s.result.status == "timeout" for s in outcome.steps)
        coherence_incidents.append(
            {
                "incident_type": "latencia_excesiva" if timed_out else "fallo_agente",
                "recovery_action": "reducir_respuesta" if timed_out else "finalizar_de_forma_segura",
                "combined_verdict_source": "coherence",
            }
        )
    else:
        generate_result = next(s for s in outcome.steps if s.step_id == "generate")
        grounding_result = next(s for s in outcome.steps if s.step_id == "verify-grounding")
        coherence_result = next(s for s in outcome.steps if s.step_id == "verify-coherence")

        proposal_text = (generate_result.result.output or {}).get("proposal_text", "")
        generation_trace = (generate_result.result.output or {}).get(
            "generation_trace", {"adapter": "deterministic", "model": None, "fallback_used": False}
        )
        grounding_output = grounding_result.result.output or {}
        grounding_verdict = grounding_output.get("verdict", "no_verificable")
        coherence_output = coherence_result.result.output or {}
        coherence_verdict = coherence_output.get("verdict", "approved")
        coherence_incident_types = coherence_output.get("incident_types", [])
        coherence_recovery_action = coherence_output.get("recovery_action")
        text = proposal_text
        status = "completed"
        fragments_used = active_fragments

        # T068/FR-024, research.md §5: combine the fundamentación severity with
        # CoherenceVerifierAgent's verdict via the shared severity order — the more
        # severe of the two wins; a tie goes to CoherenceVerifierAgent (fuller session
        # context). Computed unconditionally (even when constitutional control blocks
        # the turn) so `verification_combined` always reflects both verifiers.
        severity = grounding_verdict_severity(grounding_verdict)
        grounding_rank = _SEVERITY_RANK[severity]
        coherence_rank = _SEVERITY_RANK.get(coherence_verdict, 0)
        if grounding_rank > coherence_rank:
            combined_label, combined_source = severity, "grounding"
        elif coherence_rank > grounding_rank:
            combined_label, combined_source = coherence_verdict, "coherence"
        else:
            combined_label, combined_source = severity, "both"

        for incident_type in coherence_incident_types:
            coherence_incidents.append(
                {
                    "incident_type": incident_type,
                    "recovery_action": coherence_recovery_action,
                    "combined_verdict_source": combined_source,
                }
            )

        blocked = False
        if combined_label == "approved":
            dialogue_action = "respond"
        elif combined_label == "block":
            blocked = True
            text = SAFE_BLOCKED_MESSAGE
            dialogue_action = "clarify"
            status = "blocked"
            fragments_used = []
        elif combined_label == "clarify":
            text = _CONFLICTIVE_TEXT
            dialogue_action = "clarify"
        elif combined_label == "reformulate" and severity == "reformulate":
            # Nivel 1 acotado: only material-backed claims or explicitly enabled
            # general knowledge remain candidates for the final structured gate.
            if grounding_verdict == "no_verificable" and activity.general_knowledge_allowed:
                general_knowledge_used = True
                dialogue_action = "respond"
            else:
                supported = grounding_output.get("supported_claims", [])
                if supported:
                    text = " ".join(supported)
                    dialogue_action = "respond"
                else:
                    text = _ACKNOWLEDGE_MISSING_INFO_TEXT
                    dialogue_action = "acknowledge_missing_info"
                    fragments_used = []
        elif combined_label == "reformulate":
            text = _INCOHERENCE_TEXT
            dialogue_action = "clarify"
        else:
            text = _ACKNOWLEDGE_MISSING_INFO_TEXT
            dialogue_action = "acknowledge_missing_info"
            fragments_used = []

        if active_mode == "guided_explanation" and dialogue_action == "respond" and guided_pending_after:
            dialogue_action = "ask"
        if active_mode == "presentation_preparation" and dialogue_action == "respond":
            dialogue_action = "ask" if current_mode != "presentation_preparation" else "re_ask"

        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="verification_combined",
            payload={
                "grounding_verdict": grounding_verdict,
                "coherence_verdict": coherence_verdict,
                "combined_outcome": combined_label,
                "recovery_action": coherence_recovery_action if combined_source != "grounding" else None,
                "severity_source": "tie_coherence" if combined_source == "both" else combined_source,
            },
            memory_category="metacognitive" if combined_label != "approved" else "procedural",
        )

        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="generation_call",
            agent_id="response-generator",
            payload={
                "adapter": generation_trace.get("adapter"),
                "model": generation_trace.get("model"),
                "parameters": {},
                "purpose": purpose,
                "fragment_ids": [f["fragment_id"] for f in active_fragments],
                "fallback_used": generation_trace.get("fallback_used", False),
                "general_knowledge_used": general_knowledge_used,
            },
            memory_category="metacognitive" if generation_trace.get("fallback_used") else "procedural",
        )
        if text != proposal_text:
            pre_transform_control = ConstitutionalControl()
            await run_with_deadline(
                pre_transform_control,
                AgentRequest(
                    session_id=uuid.UUID(session.id),
                    turn_id=uuid.UUID(turn_id),
                    input={"proposal_text": proposal_text, "fallback_attempt": 0},
                    deadline_ms=pre_transform_control.contract.timeout_ms,
                ),
            )

    activated_steps.append(
        {
            "step_id": "verify-constitutional",
            "agent_id": "constitutional-control",
            "role": "verifier",
        }
    )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn_id,
        event_type="agents_selected",
        payload={
            "mode": active_mode,
            "activated_steps": activated_steps,
            "reasons": {s["step_id"]: f"paso requerido por el modo {active_mode}" for s in activated_steps},
            "skipped_modes": skipped_modes,
            "mode_validation": _mode_validation_reasoning(requested_mode, current_mode),
        },
        memory_category="procedural",
    )

    # --- CognitiveState patches specific to this mode (mode/turn bookkeeping common to
    # every mode is applied by `_finalize_turn`).
    new_concepts = list(cognitive_state.concepts_addressed)
    concept_label = _concept_label(input_text)
    if not blocked and dialogue_action == "respond" and concept_label not in new_concepts:
        new_concepts.append(concept_label)

    extra_patches: list[tuple[str, dict]] = [("retrieved_info", {"concepts_addressed": new_concepts})]
    if active_mode in _PROGRESSIVE_MODES:
        extra_patches.append(("retrieved_info", {"concepts_pending": guided_pending_after}))

    return await _finalize_turn(
        db,
        session=session,
        turn=turn,
        turn_id=turn_id,
        cognitive_state=cognitive_state,
        base_version=base_version,
        active_mode=active_mode,
        input_text=input_text,
        interpreted=interpreted,
        text=text,
        blocked=blocked,
        status=status,
        dialogue_action=dialogue_action,
        fragments_used=fragments_used,
        generator_agent_id="response-generator",
        started_at=started_at,
        extra_patches=extra_patches,
        general_knowledge_used=general_knowledge_used,
        coherence_incidents=coherence_incidents,
    )
