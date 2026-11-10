"""Integration test: pedir "ejemplo"/"más sencillo"/"comparación" tras una respuesta
previa produce una propuesta distinta sin repetir literalmente (SC-001)."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
@pytest.mark.parametrize(
    ("follow_up_text", "expected_purpose"),
    [
        ("Dame un ejemplo de esto", "ejemplo"),
        ("Explícamelo de forma más sencilla, no lo entiendo", "explicacion_progresiva"),
        ("Compara los dos conceptos", "comparacion"),
    ],
)
def test_adaptation_request_changes_generation_purpose(
    app_client, self_study_activity, follow_up_text: str, expected_purpose: str
):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-adapt-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-adapt-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    first = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert first.status_code == 200

    second = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": follow_up_text},
    )
    assert second.status_code == 200
    assert second.json()["turn_id"] != first.json()["turn_id"]

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert len(generation_events) == 2
    assert generation_events[-1]["payload"]["purpose"] == expected_purpose
