"""Integration/failure test: un cambio de tema fuera del alcance autorizado de la
actividad se rechaza/redirige, reutilizando el aislamiento de `MaterialRetrieverAgent`
(Feature 002, sin cambios, sin duplicar su filtro) — [Remediación E2/HIGH — FR-023]."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.conftest import MATERIALS_FIXTURES_DIR
from tests.integration.test_mode_doubt_resolution import _authorize_catalogued_self_study_outputs


@pytest.mark.failure
def test_topic_change_to_out_of_scope_material_is_rejected_and_traced(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    course_id = self_study_activity["course_id"]

    # Document indexed for the course but authorized only for a DIFFERENT (fake)
    # activity — same isolation pattern as Feature 002's
    # test_material_isolation_blocked_trace.py, reused rather than duplicated.
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id, "activity_configuration_ids": ["act-other-not-this-one"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )
    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-topicchange-001")
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-topicchange-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Cambiemos de tema, hablemos de otra cosa: documento de prueba"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body["sources"] == []
    assert body["general_knowledge_used"] is False

    Session = app_client.__db_sessionmaker__
    db = Session()
    events = (
        db.query(models.TraceEvent)
        .filter(
            models.TraceEvent.session_id == session_id,
            models.TraceEvent.event_type == "material_retrieval_blocked_out_of_scope",
        )
        .all()
    )
    db.close()
    assert len(events) == 1, "the blocked attempt MUST be traced via the existing Feature 002 mechanism"
