"""Integration test: study_summary es null si summary_authorized=false; presente solo
en la respuesta de cierre, sin endpoint de consulta posterior (FR-021)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material
from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.integration
def test_summary_null_when_not_authorized(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-ephemeral-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-ephemeral-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(f"/api/v1/sessions/{session_id}/study-end")
    assert response.json()["study_summary"] is None


@pytest.mark.integration
def test_summary_only_delivered_once_at_close_never_again(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": True,
            "practice_reveals_solution": False,
        },
    )
    configure_test_recipients(app_client, activity_id, recipients=("est-ephemeral-002",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-ephemeral-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    first_close = app_client.post(f"/api/v1/sessions/{session_id}/study-end")
    assert first_close.json()["study_summary"] is not None

    # Calling study-end again on an already-closed session MUST NOT re-deliver the
    # summary — there is no participant-facing endpoint to fetch it after the fact.
    second_close = app_client.post(f"/api/v1/sessions/{session_id}/study-end")
    assert second_close.status_code == 200
    assert second_close.json()["study_summary"] is None

    db = app_client.__db_sessionmaker__()
    assert (
        db.query(models.TraceEvent)
        .filter_by(session_id=session_id, event_type="study_session_summary")
        .count()
        == 1
    )
    assert (
        db.query(models.TraceEvent).filter_by(session_id=session_id, event_type="session_closed").count() == 1
    )
    db.close()
