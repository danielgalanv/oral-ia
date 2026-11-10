"""FR-003..FR-024: submit a self-study text turn on an active session.

Análogo estructural a `submit_turn.py` (Feature 001) — fichero nuevo, no lo modifica
(FR-025)."""

from __future__ import annotations

from dataclasses import replace

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.configure_self_study_activity import get_self_study_config
from oralia.application.commands.end_study_session import end_study_session
from oralia.application.orchestration.study_turn_orchestrator import StudyTurnResult, run_study_turn
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


class SessionNotActive(ValueError):
    pass


async def submit_study_turn(
    db: SASession, session: models.Session, text: str, *, dialogue_control=None, semantic_runtime=None
) -> StudyTurnResult:
    if session.status != "active":
        raise SessionNotActive(f"session {session.id} is not active (status={session.status})")

    result = await run_study_turn(
        db,
        session,
        text,
        **({"dialogue_control": dialogue_control} if dialogue_control is not None else {}),
        **({"semantic_runtime": semantic_runtime} if semantic_runtime is not None else {}),
    )

    # T079/FR-020: auto-close once the turn/duration limit is reached, same pattern as
    # `submit_turn.py` (Feature 001), replicated here in this feature's own file
    # (FR-025 — no Feature 001 file is modified) + generates the self-study summary.
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    elapsed = (utcnow() - session.started_at).total_seconds()
    limit_reached = session.turn_count >= activity.max_turns or elapsed >= activity.max_duration_seconds

    study_summary = result.study_summary
    if limit_reached and session.status == "active":
        self_study_config = get_self_study_config(db, session.activity_configuration_id)
        study_summary = end_study_session(db, session, self_study_config, status="closed_limit_reached")

    session_closed = session.status != "active"
    if not session_closed:
        return result
    return replace(
        result,
        session_closed=True,
        session_status=session.status,
        study_summary=study_summary,
    )
