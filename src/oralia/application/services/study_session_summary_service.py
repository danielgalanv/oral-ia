"""study_session_summary_service (FR-021/FR-022/FR-022a) — builds the ephemeral,
descriptive-only self-study session summary. Distinct from Feature 001's
`technical_summary_service` (área técnica, persisted/queryable by ref): this summary is
delivered **only** in the `POST /study-end` response body (FR-021) and logged as a
`TraceEvent` (`event_type=study_session_summary`) purely for audit/reconstruction
(SC-006) — the system MUST NOT offer a participant-facing endpoint to fetch it again.

FR-022/FR-022a: content is limited to observable system facts (modes used, concepts
addressed, practice questions generated, sources consulted, incidents as
`{incident_type, recovery_action}`) — never a grade, level diagnosis, personality trait,
capability judgment, or automated academic recommendation."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.services.trace_service import record_event
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.infrastructure.db import models


def generate_study_summary(db: SASession, session: models.Session) -> dict:
    cognitive_state = get_or_create(db, session.id, activity_ref=session.activity_configuration_id)

    agents_selected_events = (
        db.query(models.TraceEvent)
        .filter(
            models.TraceEvent.session_id == session.id,
            models.TraceEvent.event_type == "agents_selected",
        )
        .all()
    )
    modes_used = sorted(
        {
            event.payload.get("mode")
            for event in agents_selected_events
            if event.payload and event.payload.get("mode")
        }
    )

    practice_questions = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session.id).all()
    )
    incidents = (
        db.query(models.CoherenceIncident).filter(models.CoherenceIncident.session_id == session.id).all()
    )

    fragment_ids: set[str] = set()
    for event in (
        db.query(models.TraceEvent)
        .filter(models.TraceEvent.session_id == session.id, models.TraceEvent.event_type == "generation_call")
        .all()
    ):
        fragment_ids.update((event.payload or {}).get("fragment_ids", []))

    duration_seconds = None
    if session.ended_at and session.started_at:
        duration_seconds = int((session.ended_at - session.started_at).total_seconds())

    summary = {
        "turn_count": session.turn_count,
        "duration_seconds": duration_seconds,
        "modes_used": modes_used,
        "concepts_addressed": list(cognitive_state.concepts_addressed),
        "practice_questions_count": len(practice_questions),
        "practice_question_types": sorted({q.question_type for q in practice_questions}),
        "sources_consulted_fragment_ids": sorted(fragment_ids),
        # FR-022a: hechos observables (tipo de incidencia + acción de recuperación) —
        # nunca una caracterización del estudiante.
        "incidents": [
            {"incident_type": incident.incident_type, "recovery_action": incident.recovery_action}
            for incident in incidents
        ],
    }

    record_event(
        db,
        session_id=session.id,
        event_type="study_session_summary",
        payload=summary,
        memory_category="episodic",
    )

    return summary
