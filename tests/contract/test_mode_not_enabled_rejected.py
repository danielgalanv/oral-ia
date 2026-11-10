"""Contract test: POST /sessions/{id}/study-turns devuelve 409 con requested_mode cuando
el modo no está en enabled_modes."""

from __future__ import annotations

import pytest

from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material
from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_requested_mode_not_enabled_returns_409(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(app_client, self_study_activity, ["doubt_resolution"])
    configure_test_recipients(app_client, activity_id, recipients=("est-modereject-001",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-modereject-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Quiero preparar una exposición sobre el tema"},
    )
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["requested_mode"] == "presentation_preparation"
    assert detail["enabled_modes"] == ["doubt_resolution"]
