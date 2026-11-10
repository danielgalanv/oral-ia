"""T115 retention scopes, immediate deletion and isolated expiry purge."""

from __future__ import annotations

from datetime import timedelta

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.commands.purge_expired_defense_data import purge_expired_defense_data
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


def _counts(db, session_id: str) -> tuple[int, int, int]:
    return (
        db.query(models.Transcript).filter_by(session_id=session_id).count(),
        db.query(models.TranscriptCorrection).filter_by(session_id=session_id).count(),
        db.query(models.TraceEvent)
        .filter_by(session_id=session_id, event_type="defense_session_summary")
        .count(),
    )


def test_close_without_retention_authority_deletes_consent_scoped_data(db_session) -> None:
    session_id, config_id = _seed_active_defense(db_session)
    config = db_session.get(models.DefenseActivityConfig, config_id)
    config.transcript_retention_authorized = False
    db_session.flush()

    summary = end_defense_session(
        db_session,
        db_session.get(models.Session, session_id),
        config,
    )

    assert summary is not None
    assert _counts(db_session, session_id) == (0, 0, 0)
    assert db_session.query(models.ConsentRecord).filter_by(session_id=session_id).count() == 0


def test_explicit_delete_needs_no_consent_row_and_deletes_immediately(db_session) -> None:
    session_id, config_id = _seed_active_defense(db_session)

    end_defense_session(
        db_session,
        db_session.get(models.Session, session_id),
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=False,
    )

    assert db_session.query(models.ConsentRecord).filter_by(session_id=session_id).count() == 0
    assert _counts(db_session, session_id) == (0, 0, 0)


def test_retention_scope_keeps_only_selected_data(db_session) -> None:
    session_id, config_id = _seed_active_defense(db_session)

    end_defense_session(
        db_session,
        db_session.get(models.Session, session_id),
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=True,
        scope=["transcript"],
    )

    consent = db_session.query(models.ConsentRecord).filter_by(session_id=session_id).one()
    assert consent.decision == "retain"
    assert consent.scope == ["transcript"]
    assert _counts(db_session, session_id) == (1, 1, 0)


def test_expiry_purge_counts_rows_and_never_crosses_feature_scope(db_session) -> None:
    session_id, config_id = _seed_active_defense(db_session, retention_days=1)
    session = db_session.get(models.Session, session_id)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=True,
        scope=["transcript", "summary"],
    )
    session.ended_at = utcnow() - timedelta(days=2)

    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    other_activity = models.ActivityConfiguration(
        course_id=activity.course_id,
        name="Autoestudio aislado",
        subject="Arquitectura",
        objective="aislar purga",
        mode="self_study",
        language="es",
        max_turns=2,
        max_duration_seconds=120,
        retention_policy_id=activity.retention_policy_id,
    )
    db_session.add(other_activity)
    db_session.flush()
    db_session.add(
        models.SelfStudyActivityConfig(
            activity_configuration_id=other_activity.id,
            enabled_modes=["doubt_resolution"],
        )
    )
    other = models.Session(
        activity_configuration_id=other_activity.id,
        participant_code=session.participant_code,
        status="closed_voluntary",
        ended_at=utcnow() - timedelta(days=2),
    )
    db_session.add(other)
    db_session.flush()
    db_session.add_all(
        [
            models.ConsentRecord(
                session_id=other.id,
                decision="retain",
                scope=["summary"],
            ),
            models.TraceEvent(
                session_id=other.id,
                event_type="defense_session_summary",
                payload={"must": "survive"},
                memory_category="episodic",
            ),
        ]
    )
    db_session.flush()

    first = purge_expired_defense_data(db_session)
    second = purge_expired_defense_data(db_session)

    assert first.sessions_matching_criteria == 1
    assert first.sessions_with_rows_deleted == 1
    assert first.transcripts_deleted == 1
    assert first.transcript_corrections_deleted == 1
    assert first.trace_events_deleted == 1
    assert second.sessions_matching_criteria == 1
    assert second.sessions_with_rows_deleted == 0
    assert _counts(db_session, session_id) == (0, 0, 0)
    assert (
        db_session.query(models.TraceEvent)
        .filter_by(session_id=other.id, event_type="defense_session_summary")
        .count()
        == 1
    )


def test_defense_purge_endpoint_has_stable_counter_shape(app_client) -> None:
    response = app_client.post("/api/v1/tecnica/defense/purge-expired")
    assert response.status_code == 200
    assert response.json() == {
        "sessions_matching_criteria": 0,
        "sessions_with_rows_deleted": 0,
        "transcripts_deleted": 0,
        "transcript_corrections_deleted": 0,
        "trace_events_deleted": 0,
    }
