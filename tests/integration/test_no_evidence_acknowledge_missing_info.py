"""Integration test: cero fragmentos recuperados + `general_knowledge_allowed=false` →
`acknowledge_missing_info`; el paso de generación no se activa (research.md §2, Nivel 0)."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _authorize_catalogued_self_study_outputs


@pytest.mark.integration
def test_no_evidence_acknowledges_missing_info_without_generating(app_client, self_study_activity):
    # No materials are uploaded/activated for this activity — retrieval MUST return
    # zero fragments, and general_knowledge_allowed defaults to false (T007 fixture).
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )
    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-noevidence-001")
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-noevidence-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué dice el documento sobre la fotosíntesis?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body.get("blocked") is not True
    assert body["sources"] == []
    assert body["general_knowledge_used"] is False

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    agents_selected = next(e for e in trace["trace_events"] if e["event_type"] == "agents_selected")
    activated_step_ids = {s["step_id"] for s in agents_selected["payload"]["activated_steps"]}
    assert "generate" not in activated_step_ids
    assert "verify-grounding" not in activated_step_ids
    assert {"interpret", "retrieve", "verify-constitutional"}.issubset(activated_step_ids)
