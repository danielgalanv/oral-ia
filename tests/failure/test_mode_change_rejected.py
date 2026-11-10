"""Failure test: un modo solicitado fuera de enabled_modes se rechaza antes de ejecutar
ningún agente de generación (409, sin StatePatch propuesto) — Edge Cases."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.failure
def test_out_of_scope_mode_rejected_without_state_patch_or_generation(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-modereject-002"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-modereject-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Ponme una pregunta de práctica"},
    )
    assert response.status_code == 409

    Session = app_client.__db_sessionmaker__
    db = Session()
    patches = db.query(models.StatePatch).filter(models.StatePatch.session_id == session_id).all()
    turns = db.query(models.Turn).filter(models.Turn.session_id == session_id).all()
    trace_events = db.query(models.TraceEvent).filter(models.TraceEvent.session_id == session_id).all()
    db.close()

    assert patches == [], "a rejected mode request MUST NOT propose any StatePatch"
    assert turns == [], "a rejected mode request MUST NOT persist a Turn"
    generation_events = [e for e in trace_events if e.event_type in ("generation_call", "agent_execution")]
    assert generation_events == [], "no generation/retrieval agent MUST run for a rejected mode request"
