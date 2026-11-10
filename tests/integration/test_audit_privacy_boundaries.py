"""Synthetic owned database: projection at erase, export and trace boundaries."""

import json

import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.queries.reconstruct_session_trace import reconstruct_session_trace
from oralia.application.services.session_privacy_service import review_session
from oralia.infrastructure.db import models
from tests.integration.test_defense_retention_copies import _seed_copies


@pytest.mark.parametrize("retain", [False, True])
def test_nested_sentinel_cannot_survive_technical_projection(db_session, retain):
    sid, cfgid, _ = _seed_copies(db_session)
    marker = "PRIVATE_SENTINEL_not_a_technical_value"
    event = models.TraceEvent(
        session_id=sid,
        event_type="generation_call",
        memory_category="procedural",
        payload={
            "model": marker,
            "reason_codes": ["invalid_context", marker],
            "authorization_context": {"scope": marker, "reasons": [marker]},
            "status": "ok",
        },
    )
    db_session.add(event)
    end_defense_session(
        db_session,
        db_session.get(models.Session, sid),
        db_session.get(models.DefenseActivityConfig, cfgid),
        retain=retain,
        scope=["summary"] if retain else [],
    )
    db_session.flush()
    assert marker not in json.dumps(event.payload)
    assert marker not in str(reconstruct_session_trace(db_session, sid))
    assert event.payload["status"] == "ok"
    assert event.payload["reason_codes"] == ["invalid_context"]
    if retain:
        assert marker not in json.dumps(review_session(db_session, sid), default=str)
