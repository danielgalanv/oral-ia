"""Integration test: `general_knowledge_used=true` solo cuando el veredicto de
fundamentación es `no_verificable` con `general_knowledge_allowed=true`; `false` cuando
la respuesta se sustenta únicamente en materiales autorizados (`fundamentada`) —
[Remediación E3/HIGH — FR-019]."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import (
    _authorize_catalogued_self_study_outputs,
    _setup_activity_with_material,
)


def _enable_general_knowledge(app_client, activity_id: str) -> None:
    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, activity_id)
    activity.general_knowledge_allowed = True
    db.add(activity)
    db.commit()
    db.close()


@pytest.mark.integration
def test_general_knowledge_used_true_only_for_no_verificable_with_permission(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    _enable_general_knowledge(app_client, activity_id)
    _authorize_catalogued_self_study_outputs(
        app_client,
        activity_id,
        "est-genknow-001",
        general_knowledge_allowed=True,
    )
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-genknow-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Cuál es la capital de Francia?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["general_knowledge_used"] is True
    assert body["dialogue_action"] == "respond"
    assert body["sources"] == []


@pytest.mark.integration
def test_general_knowledge_used_false_when_grounded_in_materials(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-genknow-002"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-genknow-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["general_knowledge_used"] is False
    assert body["sources"]
