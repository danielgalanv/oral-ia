"""Atomic defense close; only the transition winner may build a summary."""

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.end_session import close_session_with_outcome
from oralia.application.services.defense_retention_service import (
    erase_defense_content,
    require_finite_retention,
)
from oralia.application.services.defense_session_summary_service import generate_defense_summary
from oralia.application.services.trace_service import record_event
from oralia.infrastructure.db import models

_ALLOWED_RETENTION_SCOPES = frozenset({"transcript", "summary"})


def _delete_unretained_data(
    db: SASession,
    session_id: str,
    retained_scope: frozenset[str],
) -> None:
    if "transcript" not in retained_scope:
        erase_defense_content(db, session_id)
        db.query(models.TranscriptCorrection).filter_by(session_id=session_id).delete()
        db.query(models.Transcript).filter_by(session_id=session_id).delete()
    if "summary" not in retained_scope:
        clear_summary_text(db, session_id)
        db.query(models.TraceEvent).filter_by(
            session_id=session_id,
            event_type="defense_session_summary",
        ).delete()


def clear_summary_text(db: SASession, session_id: str) -> None:
    proposals = (
        db.query(models.GeneratedProposal)
        .join(models.Turn, models.GeneratedProposal.turn_id == models.Turn.id)
        .filter(
            models.Turn.session_id == session_id,
            models.GeneratedProposal.generator_agent_id == "defense-summary",
        )
        .all()
    )
    for proposal in proposals:
        proposal.content = {key: value for key, value in proposal.content.items() if key != "text"}
        db.add(proposal)


def validate_defense_retention(db, session, config, *, retain=False, scope=None):
    requested_scope = frozenset(scope or ())
    if not requested_scope <= _ALLOWED_RETENTION_SCOPES:
        raise ValueError("scope may contain only transcript and summary")
    if retain and not requested_scope:
        raise ValueError("retain=true requires a non-empty scope")
    if not retain and requested_scope:
        raise ValueError("scope requires retain=true")
    if retain and (config is None or not config.transcript_retention_authorized):
        raise ValueError("transcript retention is not authorized for this activity")
    if retain:
        require_finite_retention(db, db.get(models.ActivityConfiguration, session.activity_configuration_id))

    if retain:
        from oralia.application.services.session_privacy_service import policy_retention_scopes

        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
        if not requested_scope <= policy_retention_scopes(policy):
            raise ValueError("selected scopes exceed the activity retention policy")
    return requested_scope


def end_defense_session(
    db: SASession,
    session: models.Session,
    config: models.DefenseActivityConfig | None,
    *,
    status: str = "closed_voluntary",
    retain: bool = False,
    scope: list[str] | tuple[str, ...] | None = None,
) -> dict[str, object] | None:
    requested_scope = validate_defense_retention(db, session, config, retain=retain, scope=scope)

    outcome = close_session_with_outcome(db, session, status=status, defer_privacy=True)
    if not outcome.transition_won:
        return None

    summary = None
    if config is not None and config.summary_authorized:
        summary = generate_defense_summary(db, session)

    retained_scope: frozenset[str] = frozenset()
    if config is not None and config.transcript_retention_authorized and retain:
        retained_scope = requested_scope
        db.add(
            models.ConsentRecord(
                session_id=session.id,
                decision="retain",
                scope=sorted(retained_scope),
            )
        )
        db.flush()
        record_event(
            db,
            session_id=session.id,
            event_type="consent_recorded",
            payload={"decision": "retain", "scope": sorted(retained_scope)},
            memory_category="episodic",
        )

    _delete_unretained_data(db, session.id, retained_scope)
    from oralia.application.services.session_privacy_service import finalize_session_privacy

    finalize_session_privacy(db, session, retained_scope=retained_scope)
    db.flush()
    return summary


__all__ = ["end_defense_session"]
