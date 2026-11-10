"""T109 reproductions for automatic-close delivery and the dedicated web endpoint."""

from __future__ import annotations

from pathlib import Path

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_limit_reached_turn_delivers_close_state_and_summary(app_client, self_study_activity) -> None:
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution"],
        participant_code="t109-limit",
    )
    db = app_client.__db_sessionmaker__()
    activity = db.get(models.ActivityConfiguration, activity_id)
    activity.max_turns = 1
    config = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity_id)
        .one()
    )
    config.summary_authorized = True
    db.commit()
    db.close()

    session_id = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": "t109-limit",
            "activity_configuration_id": activity_id,
        },
    ).json()["session_id"]
    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["session_closed"] is True
    assert body["session_status"] == "closed_limit_reached"
    assert body["study_summary"] is not None


def test_web_client_has_dedicated_study_end_call() -> None:
    client_source = Path("apps/web/src/api/client.ts").read_text(encoding="utf-8")

    assert "endStudySession" in client_source
    assert "/study-end" in client_source

