"""Remediación E6/FR-005: una sesión de autoestudio sigue presentando ai_disclosure y
los límites de la actividad, reutilizando start_session/AI_DISCLOSURE (Feature 001, sin
cambios) — no se reimplementa."""

from __future__ import annotations

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.integration
def test_self_study_session_start_shows_disclosure_and_limits(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    configure_test_recipients(app_client, activity_id, recipients=("est-disclosure-001",))
    response = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-disclosure-001", "activity_configuration_id": activity_id},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["ai_disclosure"]
    assert "sistema automático" in body["ai_disclosure"]
    assert body["activity"]["max_turns"] == 10
    assert body["activity"]["max_duration_seconds"] == 1800
    assert body["activity"]["objective"] == "practicar autoestudio"
