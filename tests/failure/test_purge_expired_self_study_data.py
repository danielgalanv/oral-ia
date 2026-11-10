"""Failure test: la purga elimina PracticeQuestion/CoherenceIncident/TraceEvent
únicamente de sesiones con retention_days expirado, deja intactas las no expiradas, y
solo toca las tablas de esta feature (FR-028)."""

from __future__ import annotations

from datetime import timedelta

import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


@pytest.mark.failure
def test_purge_only_touches_expired_self_study_sessions(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["practice_questions"], participant_code="est-purge-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-purge-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "Ponme una pregunta de práctica"}
    )
    app_client.post(f"/api/v1/sessions/{session_id}/study-end")

    Session = app_client.__db_sessionmaker__
    db = Session()

    # Give this activity's RetentionPolicy a short, finite retention, then push the
    # session's ended_at into the past so it counts as expired.
    activity = db.get(models.ActivityConfiguration, activity_id)
    policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
    policy.retention_days = 1
    db.add(policy)
    config = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity_id)
        .one()
    )
    config.retention_authorized = True
    db.add(config)
    session_row = db.get(models.Session, session_id)
    session_row.ended_at = utcnow() - timedelta(days=5)
    db.add(session_row)
    db.commit()

    questions_before = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).count()
    )
    feature_event_types = {
        "generation_call",
        "non_disclosure_check",
        "verification_combined",
        "study_session_summary",
        "agents_selected",
    }
    trace_before = (
        db.query(models.TraceEvent)
        .filter(
            models.TraceEvent.session_id == session_id,
            models.TraceEvent.event_type.in_(feature_event_types),
        )
        .count()
    )
    turns_before = db.query(models.Turn).filter(models.Turn.session_id == session_id).count()
    assert questions_before > 0
    assert trace_before > 0
    db.close()

    response = app_client.post("/api/v1/tecnica/self-study/purge-expired")
    assert response.status_code == 200
    body = response.json()
    assert body["sessions_with_rows_deleted"] >= 1
    assert body["practice_questions_deleted"] >= questions_before
    assert body["trace_events_deleted"] >= trace_before

    db = Session()
    assert (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).count()
        == 0
    )
    assert (
        db.query(models.TraceEvent)
        .filter(
            models.TraceEvent.session_id == session_id,
            models.TraceEvent.event_type.in_(feature_event_types),
        )
        .count()
        == 0
    )
    # Feature 001 tables (Turn, Session) are explicitly out of scope for this feature's
    # purge mechanism — they MUST remain untouched.
    assert db.query(models.Turn).filter(models.Turn.session_id == session_id).count() == turns_before
    assert db.get(models.Session, session_id) is not None
    db.close()


@pytest.mark.failure
def test_purge_leaves_non_expired_sessions_intact(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["practice_questions"], participant_code="est-purge-002"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-purge-002", "activity_configuration_id": activity_id},
    ).json()["session_id"]
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "Ponme una pregunta de práctica"}
    )
    app_client.post(f"/api/v1/sessions/{session_id}/study-end")

    Session = app_client.__db_sessionmaker__
    db = Session()
    activity = db.get(models.ActivityConfiguration, activity_id)
    policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
    policy.retention_days = 365  # far from expiring
    db.add(policy)
    config = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity_id)
        .one()
    )
    config.retention_authorized = True
    db.add(config)
    db.commit()
    questions_before = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).count()
    )
    assert questions_before > 0
    db.close()

    app_client.post("/api/v1/tecnica/self-study/purge-expired")

    db = Session()
    questions_after = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).count()
    )
    db.close()
    assert questions_after == questions_before
