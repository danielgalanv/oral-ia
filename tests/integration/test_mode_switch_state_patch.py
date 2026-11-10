"""Integration test: el modo cambia de doubt_resolution a practice_questions dentro de
la misma sesión; CognitiveState.mode actualizado vía StatePatch; agents_selected
registra ambos (research.md §6)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_mode_switches_via_state_patch_and_is_traced(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution", "practice_questions"],
        participant_code="est-switch-001",
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-switch-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    first = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    ).json()
    assert first["mode"] == "doubt_resolution"

    second = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Ponme una pregunta de práctica"},
    ).json()
    assert second["mode"] == "practice_questions"
    assert second["state_version"] > first["state_version"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    state = db.query(models.CognitiveState).filter(models.CognitiveState.session_id == session_id).one()
    assert state.mode == "practice_questions"
    mode_patches = [
        p
        for p in db.query(models.StatePatch)
        .filter(models.StatePatch.session_id == session_id, models.StatePatch.element_type == "decision")
        .all()
        if "mode" in (p.payload or {})
    ]
    db.close()
    assert any(p.payload["mode"] == "practice_questions" and p.applied for p in mode_patches)

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    agents_selected_events = [e for e in trace["trace_events"] if e["event_type"] == "agents_selected"]
    modes_seen = [e["payload"]["mode"] for e in agents_selected_events]
    assert "doubt_resolution" in modes_seen
    assert "practice_questions" in modes_seen
    switch_event = next(e for e in agents_selected_events if e["payload"]["mode"] == "practice_questions")
    assert switch_event["payload"]["mode_validation"]["switched"] is True
