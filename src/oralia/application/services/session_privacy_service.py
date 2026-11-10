"""Consent-bound projections and content erasure. Never infers participant ability."""

from __future__ import annotations

from datetime import timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from sqlalchemy.orm import Session

from oralia.application.services.technical_metadata import technical_payload
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow

SCOPES = frozenset({"transcript", "summary"})
SUMMARY_EVENTS = frozenset({"defense_session_summary", "study_session_summary"})


class PrivacyChoice(BaseModel):
    model_config = ConfigDict(extra="forbid")
    retain: StrictBool = False
    scope: list[Literal["transcript", "summary"]] = Field(default_factory=list)


def _activity_policy(db: Session, session):
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    policy = db.get(models.RetentionPolicy, activity.retention_policy_id) if activity else None
    return activity, policy


def _authorized(db: Session, session):
    config = (
        db.query(models.DefenseActivityConfig)
        .filter_by(activity_configuration_id=session.activity_configuration_id)
        .one_or_none()
    )
    if config is not None:
        return config.transcript_retention_authorized
    config = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=session.activity_configuration_id)
        .one_or_none()
    )
    return config is not None and config.retention_authorized is True


def policy_retention_scopes(policy):
    if policy is None:
        return frozenset()
    if policy.content_scope in {"session", "transcript,summary"}:
        return SCOPES
    return frozenset({policy.content_scope}) & SCOPES


def teacher_retained_scope(db: Session, session):
    if session is None:
        return frozenset()
    _, policy = _activity_policy(db, session)
    if policy is None or policy.access_scope not in {"local_teacher", "profesor", "teacher", "docente"}:
        return frozenset()
    return valid_retained_scope(db, session)


def validate_privacy_choice(db: Session, session, *, retain=False, scope=None):
    scope = frozenset(scope or [])
    if session.status != "active":
        raise ValueError("privacy choice requires an active session")
    if not scope <= SCOPES or retain != bool(scope):
        raise ValueError("retain and transcript/summary scopes must agree")
    _, policy = _activity_policy(db, session)
    if retain and (
        not _authorized(db, session)
        or policy is None
        or policy.retention_days is None
        or policy.retention_days < 0
    ):
        raise ValueError("retention requires activity authorization and a finite period")
    if not scope <= policy_retention_scopes(policy):
        raise ValueError("selected scopes exceed the activity retention policy")
    return scope


def set_privacy_preference(db: Session, session, *, retain=False, scope=None):
    scope = validate_privacy_choice(db, session, retain=retain, scope=scope)
    pref = db.get(models.SessionPrivacyPreference, session.id)
    if pref is None:
        pref = models.SessionPrivacyPreference(session_id=session.id)
    pref.retain, pref.scope, pref.updated_at = retain, sorted(scope), utcnow()
    db.add(pref)
    db.flush()
    return pref


def privacy_view(db: Session, session):
    _, policy = _activity_policy(db, session)
    pref = db.get(models.SessionPrivacyPreference, session.id)
    closed_scope = valid_retained_scope(db, session) if session.status != "active" else None
    allowed = (
        policy_retention_scopes(policy)
        if _authorized(db, session)
        and policy is not None
        and policy.retention_days is not None
        and policy.retention_days >= 0
        else frozenset()
    )
    return {
        "retention_authorized": bool(allowed),
        "allowed_scopes": sorted(allowed),
        "retention_days": policy.retention_days if policy else None,
        "access_scope": policy.access_scope if policy else None,
        "retain": bool(closed_scope) if closed_scope is not None else bool(pref and pref.retain),
        "scope": sorted(closed_scope) if closed_scope is not None else (pref.scope if pref else []),
        "deleted": db.get(models.SessionDeletionReceipt, session.id) is not None,
        "notice": (
            "Uso local seudónimo. La negativa no impide participar. "
            "Sin consentimiento se elimina contenido al cerrar; audio nunca se conserva."
        ),
    }


def valid_retained_scope(db: Session, session):
    if (
        session is None
        or session.status == "active"
        or session.ended_at is None
        or db.get(models.SessionDeletionReceipt, session.id) is not None
    ):
        return frozenset()
    _, policy = _activity_policy(db, session)
    consent = db.query(models.ConsentRecord).filter_by(session_id=session.id, decision="retain").one_or_none()
    if (
        not _authorized(db, session)
        or policy is None
        or policy.retention_days is None
        or policy.retention_days < 0
        or session.ended_at + timedelta(days=policy.retention_days) <= utcnow()
        or consent is None
    ):
        return frozenset()
    return frozenset(consent.scope) & policy_retention_scopes(policy)


def erase_content(db: Session, session, *, scope: frozenset[str] = SCOPES):
    """Erase only content owned by this terminal session, in the caller's transaction."""
    if session.status == "active":
        raise ValueError("cannot erase an active session")
    counts = {"rows_deleted": 0, "rows_redacted": 0}
    turns = db.query(models.Turn).filter_by(session_id=session.id).all()
    turn_ids = [turn.id for turn in turns]
    if "transcript" in scope:
        counts["rows_deleted"] += (
            db.query(models.TurnRequestReceipt).filter_by(session_id=session.id).delete()
        )
        for turn in turns:
            if turn.input_text or turn.output_text is not None:
                turn.input_text, turn.output_text = "", None
                counts["rows_redacted"] += 1
        for entity in (
            models.TranscriptCorrection,
            models.Transcript,
        ):
            counts["rows_deleted"] += db.query(entity).filter_by(session_id=session.id).delete()
        for message in db.query(models.InternalMessage).filter_by(session_id=session.id):
            message.content = {}
            message.objective = "content erased; structural receipt only"
            counts["rows_redacted"] += 1
        state = db.get(models.CognitiveState, session.id)
        if state is not None:
            state.dialogue_context = None
            for name in ("objective", "current_input", "participant_response", "summarized_history"):
                setattr(state, name, "")
            for name in (
                "permitted_materials",
                "concepts_addressed",
                "concepts_pending",
                "intent_hypotheses",
                "retrieved_info",
                "open_questions",
                "incidents",
            ):
                setattr(state, name, [])
            counts["rows_redacted"] += 1
        for question in db.query(models.PracticeQuestion).filter_by(session_id=session.id):
            question.objective_ref, question.concepts, question.fragment_ids = "", [], []
            counts["rows_redacted"] += 1
        for patch in db.query(models.StatePatch).filter_by(session_id=session.id):
            if patch.payload:
                patch.payload = {
                    key: value
                    for key, value in patch.payload.items()
                    if key in {"mode", "turn_number", "remaining_time", "next_action_proposed"}
                }
                counts["rows_redacted"] += 1
            patch.justification = "content erased by session privacy policy"
            patch.rejected_reason = None
        if turn_ids:
            for grounding in db.query(models.GroundingVerificationResult).filter(
                models.GroundingVerificationResult.turn_id.in_(turn_ids)
            ):
                grounding.supported_claims, grounding.unsupported_claims = [], []
                grounding.proposal_ref = ""
            for proposal in db.query(models.GeneratedProposal).filter(
                models.GeneratedProposal.turn_id.in_(turn_ids)
            ):
                if proposal.generator_agent_id != "defense-summary":
                    proposal.content = technical_payload(proposal.content)
        for event in db.query(models.TraceEvent).filter_by(session_id=session.id):
            if event.event_type not in SUMMARY_EVENTS:
                filtered = technical_payload(event.payload)
                if filtered != event.payload:
                    event.payload = filtered
                    counts["rows_redacted"] += 1
    if "summary" in scope:
        counts["rows_deleted"] += (
            db.query(models.TraceEvent)
            .filter(
                models.TraceEvent.session_id == session.id,
                models.TraceEvent.event_type == "defense_session_summary",
            )
            .delete()
        )
        for event in db.query(models.TraceEvent).filter_by(
            session_id=session.id, event_type="study_session_summary"
        ):
            event.payload = {
                key: value
                for key, value in event.payload.items()
                if key in {"turn_count", "duration_seconds"}
            }
        if turn_ids:
            for proposal in db.query(models.GeneratedProposal).filter(
                models.GeneratedProposal.turn_id.in_(turn_ids),
                models.GeneratedProposal.generator_agent_id == "defense-summary",
            ):
                proposal.content = technical_payload(proposal.content)
    db.flush()
    return counts


def delete_session_content(db: Session, session_id: str, *, reason="user_request"):
    session = db.get(models.Session, session_id)
    if session is None:
        raise ValueError("session not found")
    if session.status == "active":
        raise ValueError("cannot erase an active session")
    prior = db.get(models.SessionDeletionReceipt, session_id)
    if prior is None:
        counts = erase_content(db, session)
        prior = models.SessionDeletionReceipt(session_id=session_id, reason=reason, counts=counts)
        db.add(prior)
        pref = db.get(models.SessionPrivacyPreference, session_id)
        if pref:
            pref.retain, pref.scope = False, []
        db.query(models.ConsentRecord).filter_by(session_id=session_id).delete()
        db.flush()
    return {
        "deleted": True,
        "reason": prior.reason,
        "deleted_at": prior.deleted_at.isoformat(),
        "counts": prior.counts,
    }


def finalize_session_privacy(db: Session, session, *, retained_scope=None):
    """Only T150's winner applies the explicit choice (or its prior preference)."""
    if retained_scope is None:
        preference = db.get(models.SessionPrivacyPreference, session.id)
        retained_scope = frozenset(preference.scope if preference and preference.retain else [])
    retained_scope = frozenset(retained_scope)
    if retained_scope:
        _, policy = _activity_policy(db, session)
        if (
            not _authorized(db, session)
            or policy is None
            or policy.retention_days is None
            or policy.retention_days < 0
            or not retained_scope <= SCOPES
        ):
            raise ValueError("retention requires activity authorization and a finite period")
        if not retained_scope <= policy_retention_scopes(policy):
            raise ValueError("selected scopes exceed the activity retention policy")
        if db.query(models.ConsentRecord).filter_by(session_id=session.id).one_or_none() is None:
            db.add(
                models.ConsentRecord(session_id=session.id, decision="retain", scope=sorted(retained_scope))
            )
            db.flush()
    else:
        return delete_session_content(db, session.id, reason="no_consent")
    erase_content(db, session, scope=SCOPES - retained_scope)
    return None


def own_transcript(db: Session, session):
    """Owner view while active or within retained scope, never a teacher override."""
    visible = session.status == "active" or "transcript" in valid_retained_scope(db, session)
    turns = (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session.id, models.Turn.index >= 0)
        .order_by(models.Turn.index)
        .all()
        if visible
        else []
    )
    transcripts = (
        db.query(models.Transcript)
        .filter_by(session_id=session.id)
        .order_by(models.Transcript.created_at)
        .all()
        if visible
        else []
    )
    return {
        "turns": [
            {"turn_id": t.id, "input_text": t.input_text, "output_text": t.output_text}
            for t in turns
            if t.input_text or t.output_text
        ],
        "transcripts": [
            {
                "transcript_id": t.id,
                "turn_id": t.turn_id,
                "raw_text": t.raw_text,
                "corrections": [
                    c.corrected_text
                    for c in db.query(models.TranscriptCorrection)
                    .filter_by(transcript_id=t.id)
                    .order_by(models.TranscriptCorrection.created_at)
                ],
            }
            for t in transcripts
        ],
    }


def review_session(db: Session, session_id: str):
    session = db.get(models.Session, session_id)
    scopes = teacher_retained_scope(db, session)
    if not scopes:
        raise ValueError("session is not reviewable")
    activity, policy = _activity_policy(db, session)
    events = (
        db.query(models.TraceEvent)
        .filter_by(session_id=session_id)
        .order_by(models.TraceEvent.created_at)
        .all()
    )
    transcript = own_transcript(db, session)
    summary_events = [event for event in events if event.event_type in SUMMARY_EVENTS]
    ids = set()
    if "summary" in scopes and summary_events:
        ids.update(summary_events[-1].payload.get("sources_consulted_fragment_ids", []))
    if "transcript" in scopes:
        for event in events:
            ids.update(event.payload.get("fragment_ids", []))
            ids.update(event.payload.get("evidence_fragment_ids", []))
    sources = []
    for fragment_id in sorted(ids):
        fragment = db.get(models.MaterialFragment, fragment_id)
        if fragment:
            document = db.get(models.MaterialDocument, fragment.document_id)
            sources.append(
                {
                    "document_id": document.id,
                    "document_version": document.version,
                    "location_ref": fragment.location_ref,
                }
            )
    turns = db.query(models.Turn).filter_by(session_id=session_id).all()
    verifications = []
    for turn in turns:
        verification = (
            db.get(models.VerificationResult, turn.verification_result_id)
            if turn.verification_result_id
            else None
        )
        if verification:
            verifications.append(
                {"verdict": verification.verdict, "agent_id": verification.verifier_agent_id}
            )
    return {
        "schema_version": 1,
        "session_id": session.id,
        "status": session.status,
        "scopes": sorted(scopes),
        "configuration": {
            "id": activity.id,
            "family_id": activity.family_id,
            "version": activity.version,
            "mode": activity.mode,
            "language": activity.language,
            "max_turns": activity.max_turns,
            "max_duration_seconds": activity.max_duration_seconds,
            "retention_days": policy.retention_days,
            "policy_sha256": activity.output_authorization_policy_sha256,
        },
        **transcript,
        "summary": summary_events[-1].payload if "summary" in scopes and summary_events else None,
        "sources": sources,
        "agents": sorted({e.agent_id for e in events if e.agent_id}),
        "verifications": verifications,
        "trace": [
            {
                "event_type": e.event_type,
                "agent_id": e.agent_id,
                "latency_ms": e.latency_ms,
                "payload": technical_payload(e.payload),
            }
            for e in events
            if e.event_type not in SUMMARY_EVENTS
        ],
    }


def purge_private_sessions(db: Session):
    result = {"sessions_matching_criteria": 0, "sessions_deleted": 0}
    for session in db.query(models.Session).filter(models.Session.ended_at.isnot(None)):
        if db.get(models.SessionDeletionReceipt, session.id):
            continue
        _, policy = _activity_policy(db, session)
        consent = (
            db.query(models.ConsentRecord).filter_by(session_id=session.id, decision="retain").one_or_none()
        )
        expired = (
            policy
            and policy.retention_days is not None
            and session.ended_at + timedelta(days=policy.retention_days) <= utcnow()
        )
        if consent is None or expired:
            result["sessions_matching_criteria"] += 1
            delete_session_content(db, session.id, reason="expiry" if expired else "no_consent")
            result["sessions_deleted"] += 1
    return result
