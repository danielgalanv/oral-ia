"""Contract test for POST /sessions/{id}/study-end (study_summary nulo/no nulo)."""

from __future__ import annotations

import pytest

from tests.access_helpers import own_session
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material
from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_study_end_returns_null_summary_when_not_authorized(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(app_client, self_study_activity, ["doubt_resolution"])
    configure_test_recipients(app_client, activity_id, recipients=("est-end-001",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-end-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(f"/api/v1/sessions/{session_id}/study-end")
    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == session_id
    assert body["status"] == "closed_voluntary"
    assert body["study_summary"] is None


@pytest.mark.contract
def test_study_end_returns_summary_when_authorized(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": True,
            "practice_reveals_solution": False,
        },
    )
    configure_test_recipients(app_client, activity_id, recipients=("est-end-002",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-end-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(f"/api/v1/sessions/{session_id}/study-end")
    assert response.status_code == 200
    body = response.json()
    assert body["study_summary"] is not None
    for key in ("turn_count", "modes_used", "concepts_addressed", "incidents"):
        assert key in body["study_summary"]


@pytest.mark.contract
def test_study_end_unknown_session_404(app_client):
    own_session(app_client, "does-not-exist")
    response = app_client.post("/api/v1/sessions/does-not-exist/study-end")
    assert response.status_code == 404
