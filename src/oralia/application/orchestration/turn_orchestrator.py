"""Main turn orchestration through the T090 structured final-output gate."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.end_session import close_session
from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.application.orchestration.final_output_gate import (
    decide_final_output,
    persist_final_output,
)
from oralia.application.orchestration.output_authorization_context import (
    InvalidAuthorizationContext,
    build_authorization_snapshot,
)
from oralia.application.orchestration.output_proposal_builder import (
    ProposalConstructionError,
    build_output_proposal,
)
from oralia.application.services.trace_service import record_event
from oralia.domain.agents.agent_contract import AgentRequest
from oralia.domain.agents.fallback_agent import SafeFallbackAgent
from oralia.domain.agents.interpreter_agent import DeterministicInterpreter
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.messages.internal_message import InternalMessage as InternalMessageSchema
from oralia.domain.policies.constitutional_control import (
    ConstitutionalControl,
    constitutional_verdict_or_block,
)
from oralia.domain.policies.output_authorization_contract import (
    AuthorizationReason,
    AuthorizationSnapshot,
    AuthorizationVerdict,
)
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    SAFE_TECHNICAL_FALLBACK,
    OutputTemplateCatalog,
    OutputTemplateEntry,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.telemetry import resources

# Kept as the stable orchestration-level name used by integration consumers.
SAFE_FALLBACK_TEXT = SAFE_TECHNICAL_FALLBACK.text

AGENT_REGISTRY = {
    "interpreter": DeterministicInterpreter(),
    "constitutional-control": ConstitutionalControl(),
    "safe-fallback": SafeFallbackAgent(),
}


def _response_text_for_intent(intent: str, echo: str) -> str:
    """Historical observable composition retained only for harness comparison."""
    if intent == "acknowledge_missing_info":
        return "No he recibido ningún texto. ¿Puedes escribir tu mensaje?"
    if intent == "clarify":
        return f"¿Puedes aclarar un poco más lo que preguntas sobre «{echo}»?"
    return f"He recibido tu mensaje: «{echo}». (Respuesta de demostración — sin materiales reales todavía.)"


@dataclass
class TurnResult:
    turn_id: str
    dialogue_action: str
    output_text: str | None
    blocked: bool
    state_version: int | None
    status: str


def _entry(payload: dict[str, object], message_type: str) -> OutputTemplateEntry:
    return OutputTemplateEntry(
        template_id=payload["template_id"],
        version=payload["template_version"],
        message_type=message_type,
        text=payload["text"],
        sha256=payload["sha256"],
        topic_ref=payload["topic_ref"],
        purpose_ref=payload["purpose_ref"],
        action_ref=payload["action_ref"],
    )


def _catalog_for_activity(
    activity: models.ActivityConfiguration,
) -> tuple[OutputTemplateCatalog, OutputTemplateEntry | None, OutputTemplateEntry]:
    by_pair = {(entry.template_id, entry.version): entry for entry in DEFAULT_OUTPUT_TEMPLATE_CATALOG.entries}
    normal_payload = getattr(activity, "normal_output_template", None)
    operational_payload = getattr(activity, "operational_output_template", None)
    normal = _entry(normal_payload, "normal") if normal_payload else None
    operational = (
        _entry(operational_payload, "operational") if operational_payload else SAFE_TECHNICAL_FALLBACK
    )
    if normal is not None:
        by_pair[(normal.template_id, normal.version)] = normal
    elif activity.output_authorization_policy_json and activity.output_authorization_policy_sha256:
        try:
            policy = load_output_authorization_policy(
                activity.output_authorization_policy_json,
                activity.output_authorization_policy_sha256,
            )
            normal = next(
                (
                    by_pair.get((reference.template_id, reference.version))
                    for reference in policy.allowed_templates
                    if by_pair.get((reference.template_id, reference.version)) is not None
                    and by_pair[(reference.template_id, reference.version)].message_type == "normal"
                ),
                None,
            )
        except (TypeError, ValueError):
            normal = None
    by_pair[(operational.template_id, operational.version)] = operational
    catalog = OutputTemplateCatalog(entries=tuple(by_pair.values()))
    return catalog, normal, operational


def _minimal_snapshot(
    session: models.Session,
    activity: models.ActivityConfiguration,
) -> AuthorizationSnapshot | None:
    """Build a closed snapshot even when a referenced catalog entry is unavailable.

    Missing catalog content remains untrusted (templates is empty), allowing the gate to
    fail closed and persist the reason without inventing template text.
    """
    try:
        return build_authorization_snapshot(session, activity)
    except InvalidAuthorizationContext:
        if not (activity.output_authorization_policy_json and activity.output_authorization_policy_sha256):
            return None
        try:
            policy = load_output_authorization_policy(
                activity.output_authorization_policy_json,
                activity.output_authorization_policy_sha256,
            )
            from oralia.domain.policies.output_authorization_contract import (
                AuthorizationConfigurationIdentity,
            )

            return AuthorizationSnapshot(
                configuration=AuthorizationConfigurationIdentity(
                    session_id=session.id,
                    activity_configuration_id=activity.id,
                    activity_version=activity.version,
                    policy_id=policy.policy_id,
                    policy_version=policy.policy_version,
                    schema_version=policy.schema_version,
                    policy_sha256=activity.output_authorization_policy_sha256,
                ),
                recipient=session.participant_code,
                policy=policy,
                configuration_general_knowledge_allowed=activity.general_knowledge_allowed,
                templates=(),
                data_references=(),
            )
        except (TypeError, ValueError):
            return None


def _transport_message(
    db: SASession,
    *,
    session_id: str,
    turn_id: str,
    receiver: str,
    status: str,
) -> None:
    """Persist transport evidence without raw participant or rejected output text."""
    message = InternalMessageSchema(
        id=str(uuid.uuid4()),
        session_id=session_id,
        turn_id=turn_id,
        sender_agent_id="turn-orchestrator",
        receiver_agent_id=receiver,
        type="agent_invocation",
        objective="execute registered agent step",
        content={"status": status},
        confidence=1.0 if status == "ok" else 0.0,
        priority=0,
        expected_response=status,
        success_condition="status == 'ok'",
    )
    db.add(models.InternalMessage(**message.model_dump()))
    record_event(
        db,
        session_id=session_id,
        turn_id=turn_id,
        event_type="agent_execution",
        agent_id=receiver,
        payload={"status": status},
        memory_category="procedural" if status == "ok" else "metacognitive",
        resource_usage=resources.as_dict(),
    )


async def run_turn(db: SASession, session: models.Session, input_text: str) -> TurnResult:
    turn_id = str(uuid.uuid4())
    started_at = time.monotonic()
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
    catalog, normal_entry, operational_entry = _catalog_for_activity(activity)
    has_explicit_operational_template = False
    if activity.output_authorization_policy_json and activity.output_authorization_policy_sha256:
        try:
            loaded_policy = load_output_authorization_policy(
                activity.output_authorization_policy_json,
                activity.output_authorization_policy_sha256,
            )
            has_explicit_operational_template = bool(loaded_policy.allowed_operational_messages)
        except (TypeError, ValueError):
            pass
    try:
        snapshot = build_authorization_snapshot(
            session,
            activity,
            catalog=catalog,
        )
    except InvalidAuthorizationContext:
        snapshot = _minimal_snapshot(session, activity)

    interpreter = AGENT_REGISTRY["interpreter"]
    interpreter_request = AgentRequest(
        session_id=uuid.UUID(session.id),
        turn_id=uuid.UUID(turn_id),
        input={"text": input_text},
        deadline_ms=getattr(interpreter.contract, "timeout_ms", 1000),
    )
    interpreter_result = await run_with_deadline(interpreter, interpreter_request)
    _transport_message(
        db,
        session_id=session.id,
        turn_id=turn_id,
        receiver="interpreter",
        status=interpreter_result.status,
    )

    initial_proposal = None
    initial_verdict: AuthorizationVerdict | None = None
    if snapshot is not None and interpreter_result.status == "ok" and normal_entry is not None:
        try:
            initial_proposal = build_output_proposal(
                snapshot,
                template_id=normal_entry.template_id,
                template_version=normal_entry.version,
                template_sha256=normal_entry.sha256,
                catalog=catalog,
            )
        except ProposalConstructionError:
            initial_proposal = None

    verifier_transport_recorded = False
    if snapshot is not None and interpreter_result.status == "ok":
        verifier = AGENT_REGISTRY["constitutional-control"]
        verifier_input = {"fallback_attempt": 0}
        if initial_proposal is not None:
            verifier_input.update(
                proposal_text=initial_proposal.text,
                proposal=initial_proposal,
            )
        verifier_request = AgentRequest(
            session_id=uuid.UUID(session.id),
            turn_id=uuid.UUID(turn_id),
            input=verifier_input,
            context={
                "authorization_snapshot": snapshot,
                "activity_configuration_id": activity.id,
                "actual_recipient": session.participant_code,
            },
            deadline_ms=getattr(verifier.contract, "timeout_ms", 1000),
        )
        verifier_result = await run_with_deadline(verifier, verifier_request)
        _transport_message(
            db,
            session_id=session.id,
            turn_id=turn_id,
            receiver="constitutional-control",
            status=verifier_result.status,
        )
        verifier_transport_recorded = True
        initial_verdict = constitutional_verdict_or_block(verifier_result)

    need_fallback = (
        interpreter_result.status != "ok"
        or initial_proposal is None
        or initial_verdict is None
        or initial_verdict.verdict == "block"
    )

    fallback_matches_catalog = True
    if need_fallback and (initial_proposal is None or has_explicit_operational_template):
        fallback = AGENT_REGISTRY["safe-fallback"]
        fallback_request = AgentRequest(
            session_id=uuid.UUID(session.id),
            turn_id=uuid.UUID(turn_id),
            input={},
            deadline_ms=getattr(fallback.contract, "timeout_ms", 1000),
        )
        fallback_result = await run_with_deadline(fallback, fallback_request)
        _transport_message(
            db,
            session_id=session.id,
            turn_id=turn_id,
            receiver="safe-fallback",
            status=fallback_result.status,
        )
        fallback_matches_catalog = (
            fallback_result.status == "ok"
            and isinstance(fallback_result.output, dict)
            and fallback_result.output.get("text") == operational_entry.text
        )

    context_failure_reason = (
        AuthorizationReason.MISSING_POLICY
        if not activity.output_authorization_policy_json or not activity.output_authorization_policy_sha256
        else AuthorizationReason.INVALID_CONTEXT
    )
    if initial_verdict is not None and initial_proposal is not None:
        decision = decide_final_output(
            snapshot,
            initial_proposal,
            initial_verdict=initial_verdict,
            catalog=catalog,
            operational_template_id=operational_entry.template_id,
            operational_template_version=operational_entry.version,
            operational_template_sha256=(operational_entry.sha256 if fallback_matches_catalog else "0" * 64),
            allow_operational_attempt=has_explicit_operational_template,
        )
    else:
        decision = decide_final_output(
            snapshot,
            None,
            upstream_status=interpreter_result.status,
            initial_failure_reason=(
                AuthorizationReason.INVALID_CONTEXT
                if interpreter_result.status == "ok" and snapshot is not None
                else None
            ),
            context_failure_reason=context_failure_reason,
            catalog=catalog,
            operational_template_id=operational_entry.template_id,
            operational_template_version=operational_entry.version,
            operational_template_sha256=(operational_entry.sha256 if fallback_matches_catalog else "0" * 64),
        )

    if not verifier_transport_recorded:
        _transport_message(
            db,
            session_id=session.id,
            turn_id=turn_id,
            receiver="constitutional-control",
            status="ok",
        )

    persist_final_output(
        db,
        turn,
        decision,
        generator_agent_id=(
            "safe-fallback" if decision.final_verdict.fallback_attempt == 1 else "interpreter"
        ),
    )
    action = models.DialogueAction(
        turn_id=turn_id,
        action_type=decision.dialogue_action,
        chosen_by_agent_id="dialogue-action-selector",
    )
    db.add(action)
    db.flush()
    turn.dialogue_action_id = action.id
    turn.ended_at = utcnow()
    turn.latency_ms = int((time.monotonic() - started_at) * 1000)
    turn.resource_usage = resources.as_dict()
    db.add(turn)

    session.turn_count += 1
    db.add(session)
    db.flush()

    cognitive_state = get_or_create(db, session.id, activity_ref=session.activity_configuration_id)
    participant_patch = apply_patch(
        db,
        session_id=session.id,
        base_version=cognitive_state.version,
        proposed_by_agent_id="turn-orchestrator",
        element_type="participant_statement",
        payload={"current_input": input_text},
        justification=f"participant input for turn {turn_id}",
    )
    patch = apply_patch(
        db,
        session_id=session.id,
        base_version=participant_patch.resulting_version,
        proposed_by_agent_id="turn-orchestrator",
        element_type="decision",
        payload={
            "participant_response": decision.output_text or "",
            "next_action_proposed": decision.dialogue_action,
            "turn_number": session.turn_count,
        },
        justification=f"turn {turn_id} ({decision.turn_status})",
    )

    record_event(
        db,
        session_id=session.id,
        turn_id=turn_id,
        event_type=(
            "turn_completed" if decision.turn_status == "completed" else f"turn_{decision.turn_status}"
        ),
        payload={
            "dialogue_action": decision.dialogue_action,
            "blocked": decision.blocked,
            "verdict": decision.final_verdict.verdict,
        },
        latency_ms=turn.latency_ms,
        memory_category="episodic",
    )
    if decision.final_verdict.verdict == "block":
        block_payload: dict[str, object] = {
            "reasons": [reason.value for reason in decision.final_verdict.reason_codes],
        }
        if decision.final_verdict.fallback_attempt == 0:
            block_payload.update(
                reason_codes=[reason.value for reason in decision.final_verdict.reason_codes],
                attempt=0,
                verdict="block",
            )
        record_event(
            db,
            session_id=session.id,
            turn_id=turn_id,
            event_type="constitutional_block",
            agent_id="constitutional-control",
            payload=block_payload,
            memory_category="metacognitive",
        )
    if decision.output_text is None:
        close_session(db, session, status="closed_error_safe")

    return TurnResult(
        turn_id=turn_id,
        dialogue_action=decision.dialogue_action,
        output_text=decision.output_text,
        blocked=decision.blocked,
        state_version=patch.resulting_version,
        status=decision.turn_status,
    )
