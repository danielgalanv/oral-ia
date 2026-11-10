"""Deterministic descriptive summary built only from persisted session facts."""

from __future__ import annotations

import json

from sqlalchemy.orm import Session as SASession

from oralia.application.orchestration.final_output_gate import decide_final_output
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
from oralia.application.services.trace_service import record_event
from oralia.domain.policies.output_authorization_contract import AuthorizationReason, ScopeReference
from oralia.domain.policies.output_template_catalog import DEFENSE_SUMMARY
from oralia.infrastructure.db import models


def generate_defense_summary(db: SASession, session: models.Session) -> dict[str, object] | None:
    turns = (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session.id, models.Turn.index >= 0)
        .order_by(models.Turn.index.asc())
        .all()
    )
    cognitive_state = db.get(models.CognitiveState, session.id)
    fragment_ids: set[str] = set()
    clarification_count = 0
    incident_facts: list[dict[str, str]] = []
    for event in (
        db.query(models.TraceEvent)
        .filter(models.TraceEvent.session_id == session.id)
        .order_by(models.TraceEvent.created_at.asc())
        .all()
    ):
        payload = event.payload or {}
        fragment_ids.update(payload.get("fragment_ids", []))
        fragment_ids.update(payload.get("evidence_fragment_ids", []))
        if event.event_type == "followup_question_generated" and payload.get("dialogue_action") == "clarify":
            clarification_count += 1
        if event.event_type in {"transcription_failed", "tts_failed"}:
            incident_facts.append(
                {
                    "incident_type": event.event_type,
                    "recovery_action": str(payload.get("recovery_action", "safe_fallback")),
                }
            )

    duration_seconds = None
    if session.ended_at and session.started_at:
        duration_seconds = max(0, int((session.ended_at - session.started_at).total_seconds()))
    summary: dict[str, object] = {
        "turn_count": len(turns),
        "duration_seconds": duration_seconds,
        "questions_asked": [
            turn.output_text
            for turn in turns
            if turn.output_text
            and (
                turn.dialogue_action_id is None
                or (action := db.get(models.DialogueAction, turn.dialogue_action_id)) is None
                or action.action_type == "ask"
            )
        ],
        "topics_covered": list(cognitive_state.concepts_addressed) if cognitive_state else [],
        "concepts_mentioned": list(cognitive_state.concepts_addressed) if cognitive_state else [],
        "sources_consulted_fragment_ids": sorted(fragment_ids),
        "clarifications_count": clarification_count,
        "incidents": incident_facts,
        "close_reason": session.status,
    }
    text = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    snapshot = proposal = None
    failure = None
    try:
        snapshot = build_authorization_snapshot(
            session,
            activity,
            data_references=(
                AuthorizationReferenceInput(
                    data_ref="defense-summary-facts",
                    category="defense_summary",
                    provenance="persisted_session_facts",
                    recipient=session.participant_code,
                    scope=ScopeReference(
                        topic_ref="activity", purpose_ref="oral_defense_summary", action_ref="respond"
                    ),
                    value=text,
                ),
            ),
        )
        proposal = build_output_proposal(
            snapshot,
            template_id=DEFENSE_SUMMARY.template_id,
            template_version=DEFENSE_SUMMARY.version,
            template_sha256=DEFENSE_SUMMARY.sha256,
            slots=(BoundTemplateSlot(placeholder="content", data_ref="defense-summary-facts"),),
        )
    except (InvalidAuthorizationContext, ProposalConstructionError, TypeError, ValueError):
        failure = AuthorizationReason.INVALID_CONTEXT
    decision = decide_final_output(snapshot, proposal, initial_failure_reason=failure)
    authorization_turn = (
        turns[-1] if turns else db.query(models.Turn).filter_by(session_id=session.id, index=-1).one_or_none()
    )
    if authorization_turn is None:
        # Index -1 is an authorization receipt for an empty-session close, not a
        # cognitive turn. It never increments session.turn_count or enters the facts.
        authorization_turn = models.Turn(
            session_id=session.id, index=-1, input_text="", output_text=None, status="completed"
        )
        db.add(authorization_turn)
        db.flush()
    if authorization_turn is not None:
        verdict = decision.final_verdict
        context = verdict.model_dump(
            mode="json", exclude_none=True, exclude={"verdict", "reason_codes", "fallback_attempt"}
        )
        context["attempt"] = verdict.fallback_attempt
        persisted_proposal = models.GeneratedProposal(
            turn_id=authorization_turn.id,
            generator_agent_id="defense-summary",
            content={
                "template_id": verdict.template_id,
                "template_version": verdict.template_version,
                "template_sha256": verdict.template_sha256,
                "message_type": verdict.message_type,
                "attempt": verdict.fallback_attempt,
                **({"text": decision.output_text} if decision.output_text is not None else {}),
            },
        )
        db.add(persisted_proposal)
        db.flush()
        verification = models.VerificationResult(
            proposal_id=persisted_proposal.id,
            verifier_agent_id="constitutional-control",
            verdict=verdict.verdict,
            reasons=[reason.value for reason in verdict.reason_codes],
            authorization_context=context,
        )
        db.add(verification)
        db.flush()
    for attempt in decision.attempts:
        record_event(
            db,
            session_id=session.id,
            event_type="output_authorization_attempt",
            agent_id="constitutional-control",
            payload={
                **attempt.model_dump(mode="json"),
                "component": "defense-summary",
                "verification_result_id": (
                    verification.id if attempt.attempt == decision.final_verdict.fallback_attempt else None
                ),
            },
            memory_category="metacognitive",
        )
    # An operational fallback never authorizes disclosure of the structured facts.
    if decision.output_text != text or decision.final_verdict.verdict != "approved":
        return None
    record_event(
        db,
        session_id=session.id,
        event_type="defense_session_summary",
        payload=summary,
        memory_category="episodic",
    )
    return summary


__all__ = ["generate_defense_summary"]
