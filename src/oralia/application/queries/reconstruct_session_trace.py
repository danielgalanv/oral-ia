"""FR-016, FR-020, SC-004: full trace reconstruction from TraceEvent + StatePatch logs."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.services.session_privacy_service import (
    SUMMARY_EVENTS,
    teacher_retained_scope,
    technical_payload,
)
from oralia.application.services.trace_service import reconstruct_trace
from oralia.domain.cognitive_state.state_patch import history_for_session
from oralia.infrastructure.db import models


def reconstruct_session_trace(db: SASession, session_id: str) -> dict:
    scopes = teacher_retained_scope(db, db.get(models.Session, session_id))
    events = reconstruct_trace(db, session_id)
    patches = history_for_session(db, session_id)

    return {
        "trace_events": [
            {
                "id": e.id,
                "turn_id": e.turn_id,
                "event_type": e.event_type,
                "agent_id": e.agent_id,
                "payload": (
                    e.payload
                    if e.event_type in SUMMARY_EVENTS and "summary" in scopes
                    else technical_payload(e.payload)
                ),
                "latency_ms": e.latency_ms,
                "resource_usage": e.resource_usage,
                "memory_category": e.memory_category,
                "created_at": e.created_at,
            }
            for e in events
            if e.event_type != "defense_session_summary" or "summary" in scopes
        ],
        "state_patches": [
            {
                "id": p.id,
                "base_version": p.base_version,
                "resulting_version": p.resulting_version,
                "proposed_by_agent_id": p.proposed_by_agent_id,
                "element_type": p.element_type,
                "applied": p.applied,
                "rejected_reason": p.rejected_reason,
                "created_at": p.created_at,
            }
            for p in patches
        ],
    }
