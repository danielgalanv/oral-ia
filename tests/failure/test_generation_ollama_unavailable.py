"""Failure test: Ollama no disponible/timeout degrada a DeterministicGenerationAdapter
dentro del mismo turno — el turno se completa igualmente (research.md §1/§2)."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.failure
def test_turn_completes_when_ollama_unreachable(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("ORALIA_OLLAMA_MODEL", "some-model")
    monkeypatch.setenv("ORALIA_OLLAMA_BASE_URL", "http://127.0.0.1:1")  # nothing listens here
    monkeypatch.setenv("ORALIA_OLLAMA_TIMEOUT_MS", "500")

    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-ollama-down-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-ollama-down-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["output_text"]

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert generation_events
    payload = generation_events[0]["payload"]
    assert payload["adapter"] == "deterministic"
    assert payload["fallback_used"] is True
