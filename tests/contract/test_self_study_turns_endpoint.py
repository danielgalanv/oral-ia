"""Contract test for POST /sessions/{id}/study-turns (200 camino feliz, 404)."""

from __future__ import annotations

import pytest

from tests.access_helpers import own_session
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material
from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_study_turn_happy_path_200(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(app_client, self_study_activity, ["doubt_resolution"])
    configure_test_recipients(app_client, activity_id, recipients=("est-contract-001",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-contract-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    for key in (
        "turn_id",
        "mode",
        "dialogue_action",
        "output_text",
        "state_version",
        "sources",
        "general_knowledge_used",
    ):
        assert key in body


@pytest.mark.contract
def test_study_turn_unknown_session_404(app_client):
    own_session(app_client, "does-not-exist")
    response = app_client.post(
        "/api/v1/sessions/does-not-exist/study-turns",
        json={"text": "hola"},
    )
    assert response.status_code == 404
