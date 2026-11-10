"""Integration test: tras el cierre por límite (T083), GET /tecnica/sessions/{id}/
study-trace reconstruye la secuencia completa de eventos de esa sesión (agents_selected,
generation_call, verification_combined, cierre de turno, study_session_summary) —
[Remediación E7/LOW — SC-006]."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.conftest import MATERIALS_FIXTURES_DIR
from tests.integration.test_mode_doubt_resolution import _authorize_catalogued_self_study_outputs


@pytest.mark.integration
def test_full_event_sequence_reconstructible_after_limit_close(app_client, self_study_activity):
    activity_id = self_study_activity["activity_id"]
    course_id = self_study_activity["course_id"]
    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, activity_id)
    activity.max_turns = 1
    db.add(activity)
    db.commit()
    db.close()

    with open(MATERIALS_FIXTURES_DIR / "sample.docx", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id, "activity_configuration_ids": [activity_id]},
            files={
                "file": (
                    "sample.docx",
                    fh,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": True,
            "practice_reveals_solution": False,
        },
    )
    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-sc006-001")

    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-sc006-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Qué contiene el documento?"}
    )
    assert response.status_code == 200

    db = Session()
    session_row = db.get(models.Session, session_id)
    assert session_row.status == "closed_limit_reached"
    db.close()

    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    event_types = [e["event_type"] for e in trace["trace_events"]]
    for expected in (
        "agents_selected",
        "generation_call",
        "verification_combined",
        "turn_completed",
        "session_closed",
        "study_session_summary",
    ):
        assert expected in event_types, f"{expected!r} MUST be reconstructible from the trace"

    # Chronological order: the turn's own events precede the session-close events.
    assert event_types.index("turn_completed") < event_types.index("session_closed")
    assert event_types.index("session_closed") <= event_types.index("study_session_summary")
