"""Integration test: generation_call TraceEvent registra adapter/model/fragment_ids de
un turno."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_generation_call_trace_recorded(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-gentrace-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-gentrace-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert generation_events, "a generation_call TraceEvent MUST be recorded"
    payload = generation_events[0]["payload"]
    assert payload["adapter"] in ("ollama", "deterministic")
    assert "model" in payload
    assert "fragment_ids" in payload and payload["fragment_ids"]
    assert "fallback_used" in payload
