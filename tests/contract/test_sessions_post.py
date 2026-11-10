"""Contract test for POST /api/v1/sessions — contracts/api-participante.md, FR-010."""

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_start_session_returns_201_with_ai_disclosure(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-abc123",))
    r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-abc123", "activity_configuration_id": seeded_activity},
    )
    assert r.status_code == 201
    body = r.json()
    assert "session_id" in body
    assert "sistema automático" in body["ai_disclosure"] or "ai_disclosure" in body
    assert body["activity"]["max_turns"] == 10


@pytest.mark.contract
def test_start_session_with_unknown_activity_returns_404(app_client):
    r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-abc123", "activity_configuration_id": "does-not-exist"},
    )
    assert r.status_code == 404


@pytest.mark.contract
def test_start_session_with_real_looking_name_returns_422(app_client, seeded_activity):
    r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "Juan Perez", "activity_configuration_id": seeded_activity},
    )
    assert r.status_code == 422
