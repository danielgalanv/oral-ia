"""Integration test: una sesión que alcanza el límite de turnos/duración se cierra
automáticamente con un resumen descriptivo que solo contiene hechos observables del
sistema (FR-020/FR-021/FR-022a)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _authorize_catalogued_self_study_outputs

_FORBIDDEN_TERMS = ("nota", "calificaci", "nivel del estudiante", "capacidad", "personalidad", "diagnóstico")


@pytest.mark.integration
def test_session_auto_closes_at_turn_limit_with_descriptive_summary(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, activity_id)
    activity.max_turns = 2
    db.add(activity)
    db.commit()
    db.close()

    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": True,
            "practice_reveals_solution": False,
        },
    )
    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-limit-001")
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-limit-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    first = app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Qué es esto?"})
    assert first.status_code == 200

    db = Session()
    session_row = db.get(models.Session, session_id)
    assert session_row.status == "active"
    db.close()

    second = app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Y esto otro?"})
    assert second.status_code == 200

    db = Session()
    session_row = db.get(models.Session, session_id)
    assert session_row.status == "closed_limit_reached"
    db.close()

    summary_event = None
    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    for event in trace["trace_events"]:
        if event["event_type"] == "study_session_summary":
            summary_event = event
    assert summary_event is not None, (
        "reaching the turn limit MUST produce a study_session_summary TraceEvent"
    )

    summary_text = str(summary_event["payload"]).lower()
    for forbidden in _FORBIDDEN_TERMS:
        assert forbidden not in summary_text, f"summary MUST NOT contain {forbidden!r} (FR-022)"
