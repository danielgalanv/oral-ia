"""Integration test: presentation_preparation produce un patrón ask/re_ask dominante
(SC-001)."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_presentation_preparation_ask_then_re_ask_pattern(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["presentation_preparation"], participant_code="est-preso-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-preso-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    first = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Quiero preparar una exposición sobre el documento de prueba"},
    ).json()
    assert first["mode"] == "presentation_preparation"
    assert first["dialogue_action"] in ("ask", "re_ask", "acknowledge_missing_info", "clarify")

    second = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Sigue estructurando la exposición sobre el documento de prueba"},
    ).json()
    assert second["mode"] == "presentation_preparation"

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    dialogue_actions = [
        e["payload"]["dialogue_action"] for e in trace["trace_events"] if e["event_type"] == "turn_completed"
    ]
    assert dialogue_actions, "at least one completed turn expected"
    assert all(a in ("ask", "re_ask") for a in dialogue_actions), (
        "presentation_preparation MUST follow an ask/re_ask dominant pattern, never respond"
    )
    assert "ask" in dialogue_actions and "re_ask" in dialogue_actions, (
        "MUST show ask on entry, re_ask on continuation"
    )
