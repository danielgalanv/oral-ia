"""FR-012b: descriptive-only technical summary, visible only in the área técnica.

Never includes grades, scores, or any judgment of participant ability (Constitution
Principio I; checklists/no-evaluation.md).
"""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


def generate_summary(db: SASession, session: models.Session) -> str:
    """Build and persist a descriptive technical summary; returns its reference id.

    Content is limited to observable operational facts: turn count, incidents, and
    duration. It MUST NOT contain any grade, score, or capability judgment.
    """

    turns = db.query(models.Turn).filter(models.Turn.session_id == session.id).all()
    incidents = [t.status for t in turns if t.status in {"blocked", "degraded", "failed"}]
    duration_seconds = None
    if session.ended_at and session.started_at:
        duration_seconds = int((session.ended_at - session.started_at).total_seconds())

    summary_id = str(uuid.uuid4())
    event = models.TraceEvent(
        id=summary_id,
        session_id=session.id,
        turn_id=None,
        event_type="technical_summary",
        agent_id=None,
        payload={
            "turn_count": len(turns),
            "incident_count": len(incidents),
            "incident_types": incidents,
            "duration_seconds": duration_seconds,
        },
        memory_category="episodic",
        created_at=utcnow(),
    )
    db.add(event)
    db.flush()
    return summary_id


def get_summary(db: SASession, summary_ref: str) -> dict | None:
    event = db.get(models.TraceEvent, summary_ref)
    if event is None or event.event_type != "technical_summary":
        return None
    return event.payload
