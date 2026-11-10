"""FR-020, US6: list/detail queries for active and historical sessions."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.services.session_privacy_service import teacher_retained_scope
from oralia.infrastructure.db import models


def list_sessions(db: SASession, *, status: str | None = None) -> list[dict]:
    query = db.query(models.Session)
    if status is not None:
        query = query.filter(models.Session.status == status)
    return [
        {
            "id": s.id,
            "activity_configuration_id": s.activity_configuration_id,
            "participant_code": s.participant_code if teacher_retained_scope(db, s) else None,
            "status": s.status,
            "started_at": s.started_at,
            "ended_at": s.ended_at,
            "turn_count": s.turn_count,
        }
        for s in query.order_by(models.Session.started_at.desc()).all()
    ]


def get_session_detail(db: SASession, session_id: str) -> dict | None:
    session = db.get(models.Session, session_id)
    if session is None:
        return None

    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    turns = (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session_id)
        .order_by(models.Turn.index.asc())
        .all()
    )

    retained_scope = teacher_retained_scope(db, session)
    turn_payload = []
    for turn in turns:
        verification = (
            db.get(models.VerificationResult, turn.verification_result_id)
            if turn.verification_result_id
            else None
        )
        dialogue_action = (
            db.get(models.DialogueAction, turn.dialogue_action_id) if turn.dialogue_action_id else None
        )
        turn_payload.append(
            {
                "id": turn.id,
                "index": turn.index,
                "input_text": turn.input_text if "transcript" in retained_scope else "",
                "output_text": turn.output_text if "transcript" in retained_scope else None,
                "status": turn.status,
                "dialogue_action": dialogue_action.action_type if dialogue_action else None,
                "verification_verdict": verification.verdict if verification else None,
                "latency_ms": turn.latency_ms,
                "resource_usage": turn.resource_usage,
            }
        )

    technical_summary = None
    if session.status != "active" and session.technical_summary_ref:
        from oralia.application.services.technical_summary_service import get_summary

        technical_summary = get_summary(db, session.technical_summary_ref)

    return {
        "session": {
            "id": session.id,
            "status": session.status,
            "started_at": session.started_at,
            "ended_at": session.ended_at,
            "turn_count": session.turn_count,
            "participant_code": session.participant_code if retained_scope else None,
        },
        "activity_configuration": (
            {
                "id": activity.id,
                "name": activity.name,
                "version": activity.version,
                "objective": activity.objective,
            }
            if activity
            else None
        ),
        "turns": turn_payload,
        "technical_summary": technical_summary,
    }
