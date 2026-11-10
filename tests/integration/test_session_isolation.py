"""Integration test: dos sesiones del mismo participant_code nunca comparten historial
de PracticeQuestion/CoherenceIncident (FR-011)."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.integration
def test_practice_question_history_not_shared_across_sessions_same_participant(
    app_client, self_study_activity
):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["practice_questions"], participant_code="est-iso-001"
    )

    session1_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-iso-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]
    app_client.post(
        f"/api/v1/sessions/{session1_id}/study-turns", json={"text": "Ponme una pregunta de práctica"}
    )
    app_client.post(f"/api/v1/sessions/{session1_id}/study-end")

    # Same participant_code, a brand-new session.
    session2_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-iso-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]
    response2 = app_client.post(
        f"/api/v1/sessions/{session2_id}/study-turns", json={"text": "Ponme una pregunta de práctica"}
    )
    assert response2.status_code == 200

    Session = app_client.__db_sessionmaker__
    db = Session()
    q1 = db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session1_id).all()
    q2 = db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session2_id).all()
    db.close()

    assert len(q1) == 1
    assert len(q2) == 1
    # If session2 could "see" session1's history, its single question would have
    # cycled to the SECOND question_type instead of starting fresh at the first.
    assert q1[0].question_type == q2[0].question_type, (
        "a fresh session for the same participant_code MUST start question_type "
        "rotation from scratch — session1's PracticeQuestion history MUST NOT leak in"
    )


@pytest.mark.integration
def test_coherence_incidents_not_shared_across_sessions_same_participant(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-iso-002"
    )

    session1_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-iso-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]
    app_client.post(
        f"/api/v1/sessions/{session1_id}/study-turns", json={"text": "¿Qué contiene el documento?"}
    )
    app_client.post(f"/api/v1/sessions/{session1_id}/study-end")

    session2_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-iso-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]
    app_client.post(
        f"/api/v1/sessions/{session2_id}/study-turns", json={"text": "¿Qué contiene el documento?"}
    )

    Session = app_client.__db_sessionmaker__
    db = Session()
    incidents_s2 = (
        db.query(models.CoherenceIncident).filter(models.CoherenceIncident.session_id == session2_id).count()
    )
    db.close()
    # A fresh session2 with no prior turn of its own MUST NOT show a repetition
    # incident against session1's output — different sessions never cross-reference.
    assert incidents_s2 == 0
