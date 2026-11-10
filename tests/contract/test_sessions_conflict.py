"""FR-012a: 409 when a second interactive session is started while one is active."""

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_second_concurrent_session_returns_409(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-aaa111", "part-bbb222"))
    r1 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-aaa111", "activity_configuration_id": seeded_activity},
    )
    assert r1.status_code == 201

    r2 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-bbb222", "activity_configuration_id": seeded_activity},
    )
    assert r2.status_code == 409
    assert r2.json()["detail"]["code"] == "interactive_session_active"
    assert set(r2.json()["detail"]) == {"code", "message"}


@pytest.mark.contract
def test_new_session_allowed_after_previous_one_ends(app_client, seeded_activity):
    configure_test_recipients(app_client, seeded_activity, recipients=("part-ccc333", "part-ddd444"))
    r1 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-ccc333", "activity_configuration_id": seeded_activity},
    )
    sid = r1.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/end")

    r2 = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-ddd444", "activity_configuration_id": seeded_activity},
    )
    assert r2.status_code == 201
