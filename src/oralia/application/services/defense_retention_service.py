"""Erase defense-owned content projections while retaining structural audit metadata."""

from sqlalchemy.orm import Session as SASession

from oralia.application.services.trace_service import record_event
from oralia.infrastructure.db import models

_CONTENT_KEYS = frozenset(
    {
        "text",
        "input_text",
        "output_text",
        "student_answer_text",
        "proposal_text",
        "question_text",
        "raw_text",
        "corrected_text",
        "current_input",
        "participant_response",
        "concepts_mentioned",
        "concepts_addressed",
        "concepts_pending",
        "referenced_concept",
        "source_concept",
        "target_concept",
        "summarized_history",
        "open_questions",
        "trace",
        "content",
    }
)
_PATCH_METADATA = frozenset({"mode", "turn_number", "remaining_time", "next_action_proposed"})


def require_finite_retention(db: SASession, activity: models.ActivityConfiguration) -> None:
    policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
    if policy is None or policy.retention_days is None or policy.retention_days < 0:
        raise ValueError("retention requires a finite non-negative period")


def _without_content(value):
    if isinstance(value, dict):
        return {key: _without_content(item) for key, item in value.items() if key not in _CONTENT_KEYS}
    if isinstance(value, list):
        return [_without_content(item) for item in value]
    return value


def erase_defense_content(db: SASession, session_id: str) -> int:
    """Only terminal oral-defense sessions; no commit and no other session's rows.

    Post-session retention erasure is distinct from cognitive history revision: event
    identities, patch versions and authorization verdicts survive, their content does not.
    Returns actual auxiliary rows deleted, for the existing purge aggregate counter.
    """
    session = db.get(models.Session, session_id)
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id) if session else None
    if session is None or session.status == "active" or activity is None or activity.mode != "oral_defense":
        return 0
    changed = False
    turns = db.query(models.Turn).filter_by(session_id=session_id).all()
    for turn in turns:
        if turn.input_text or turn.output_text is not None:
            turn.input_text = ""
            turn.output_text = None
            db.add(turn)
            changed = True
    turn_ids = [turn.id for turn in turns]
    if turn_ids:
        for proposal in db.query(models.GeneratedProposal).filter(
            models.GeneratedProposal.turn_id.in_(turn_ids),
            models.GeneratedProposal.generator_agent_id != "defense-summary",
        ):
            content = {
                key: item
                for key, item in proposal.content.items()
                if key
                in {
                    "template_id",
                    "template_version",
                    "template_sha256",
                    "message_type",
                    "attempt",
                }
            }
            if content != proposal.content:
                proposal.content = content
                changed = True
    for patch in db.query(models.StatePatch).filter_by(session_id=session_id):
        payload = {key: item for key, item in patch.payload.items() if key in _PATCH_METADATA}
        if payload != patch.payload:
            patch.payload = payload
            patch.justification = "content erased by defense retention policy"
            changed = True
    for event in db.query(models.TraceEvent).filter_by(session_id=session_id):
        if event.event_type == "defense_session_summary":
            continue  # Independent summary scope is applied by the caller.
        payload = _without_content(event.payload)
        if payload != event.payload:
            event.payload = payload
            changed = True
    deleted = db.query(models.InternalMessage).filter_by(session_id=session_id).delete()
    deleted += db.query(models.CognitiveState).filter_by(session_id=session_id).delete()
    if changed or deleted:
        record_event(
            db,
            session_id=session_id,
            event_type="defense_content_erased",
            payload={"reason": "retention_policy", "auxiliary_rows_deleted": deleted},
            memory_category="procedural",
        )
    db.flush()
    return deleted
