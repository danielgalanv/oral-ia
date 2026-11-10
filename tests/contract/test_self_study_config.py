"""Contract test for POST /tecnica/activities/{id}/self-study-config — 201/409/422
(FR-002, FR-002a, research.md §7)."""

from __future__ import annotations

import pytest

from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.contract
def test_post_self_study_config_created(app_client, seeded_activity):
    response = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution", "practice_questions"],
            "summary_authorized": True,
            "practice_reveals_solution": False,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["enabled_modes"] == ["doubt_resolution", "practice_questions"]
    assert body["summary_authorized"] is True
    assert body["retention_authorized"] is None


@pytest.mark.contract
def test_post_self_study_config_update_returns_200(app_client, seeded_activity):
    payload = {
        "enabled_modes": ["doubt_resolution"],
        "summary_authorized": False,
        "practice_reveals_solution": False,
    }
    first = app_client.post(f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config", json=payload)
    assert first.status_code == 201

    payload["enabled_modes"] = ["doubt_resolution", "concept_review"]
    second = app_client.post(f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config", json=payload)
    assert second.status_code == 200
    assert second.json()["enabled_modes"] == ["doubt_resolution", "concept_review"]


@pytest.mark.contract
def test_post_self_study_config_empty_modes_rejected(app_client, seeded_activity):
    response = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config",
        json={"enabled_modes": [], "summary_authorized": False, "practice_reveals_solution": False},
    )
    assert response.status_code == 422


@pytest.mark.contract
def test_post_self_study_config_immutable_activity_rejected(app_client, seeded_activity):
    payload = {
        "enabled_modes": ["doubt_resolution"],
        "summary_authorized": False,
        "practice_reveals_solution": False,
    }
    app_client.post(f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config", json=payload)

    # Start a session on this activity — Feature 001's start_session marks the
    # ActivityConfiguration immutable on first use (reused unchanged).
    configure_test_recipients(app_client, seeded_activity, recipients=("est-config-001",))
    session_response = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-config-001", "activity_configuration_id": seeded_activity},
    )
    assert session_response.status_code == 201

    second = app_client.post(f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config", json=payload)
    assert second.status_code == 409


@pytest.mark.contract
def test_post_self_study_config_unknown_activity_404(app_client):
    response = app_client.post(
        "/api/v1/tecnica/activities/does-not-exist/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )
    assert response.status_code == 404


@pytest.mark.contract
def test_retention_authorization_accepts_only_explicit_booleans_or_null(app_client, seeded_activity):
    base = {
        "enabled_modes": ["doubt_resolution"],
        "summary_authorized": False,
        "practice_reveals_solution": False,
    }
    rejected = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config",
        json={**base, "retention_authorized": 1},
    )
    assert rejected.status_code == 422

    accepted = app_client.post(
        f"/api/v1/tecnica/activities/{seeded_activity}/self-study-config",
        json={**base, "retention_authorized": False},
    )
    assert accepted.status_code == 201
    assert accepted.json()["retention_authorized"] is False
