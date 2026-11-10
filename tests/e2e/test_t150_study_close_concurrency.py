"""T150 regression coverage for atomic self-study close ownership."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from oralia.application.commands import end_session, end_study_session
from oralia.application.commands.end_study_session import end_study_session as close_study_session
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_test_recipients


def _configure_and_open(app_client, self_study_activity, *, authorized: bool) -> str:
    activity_id = self_study_activity["activity_id"]
    configure_test_recipients(
        app_client,
        activity_id,
        recipients=(f"t150-{'authorized' if authorized else 'denied'}",),
    )
    response = app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": authorized,
            "practice_reveals_solution": False,
        },
    )
    assert response.status_code == 201
    opened = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": f"t150-{'authorized' if authorized else 'denied'}",
            "activity_configuration_id": activity_id,
        },
    )
    assert opened.status_code == 201
    return opened.json()["session_id"]


def _event_count(db, session_id: str, event_type: str) -> int:
    return db.query(models.TraceEvent).filter_by(session_id=session_id, event_type=event_type).count()


@pytest.mark.e2e
@pytest.mark.parametrize(
    ("winner_status", "loser_status"),
    [
        ("closed_error_safe", "closed_limit_reached"),
        ("closed_limit_reached", "closed_voluntary"),
        ("closed_voluntary", "closed_error_safe"),
    ],
)
def test_only_atomic_close_winner_generates_authorized_study_summary(
    app_client,
    self_study_activity,
    monkeypatch: pytest.MonkeyPatch,
    winner_status: str,
    loser_status: str,
) -> None:
    session_id = _configure_and_open(app_client, self_study_activity, authorized=True)
    session_factory = app_client.__db_sessionmaker__
    winner_db = session_factory()
    loser_db = session_factory()
    winner_view = winner_db.get(models.Session, session_id)
    loser_view = loser_db.get(models.Session, session_id)
    winner_config = (
        winner_db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=winner_view.activity_configuration_id)
        .one()
    )
    loser_config = (
        loser_db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=loser_view.activity_configuration_id)
        .one()
    )

    summary_calls = 0
    release_calls = 0
    real_summary = end_study_session.generate_study_summary
    real_release = end_session.session_lock_service.release

    def counted_summary(*args, **kwargs):
        nonlocal summary_calls
        summary_calls += 1
        return real_summary(*args, **kwargs)

    def counted_release(*args, **kwargs):
        nonlocal release_calls
        release_calls += 1
        return real_release(*args, **kwargs)

    monkeypatch.setattr(end_study_session, "generate_study_summary", counted_summary)
    monkeypatch.setattr(end_session.session_lock_service, "release", counted_release)

    winner_summary = close_study_session(
        winner_db,
        winner_view,
        winner_config,
        status=winner_status,
    )
    winner_db.commit()
    loser_summary = close_study_session(
        loser_db,
        loser_view,
        loser_config,
        status=loser_status,
    )
    loser_db.commit()
    winner_db.close()
    loser_db.close()

    assert winner_summary is not None
    assert loser_summary is None
    assert summary_calls == 1
    assert release_calls == 1

    db = session_factory()
    persisted = db.get(models.Session, session_id)
    assert persisted.status == winner_status
    assert persisted.active_lock_token is None
    assert persisted.technical_summary_ref is not None
    assert _event_count(db, session_id, "technical_summary") == 1
    assert _event_count(db, session_id, "session_closed") == 1
    assert _event_count(db, session_id, "study_session_summary") == 1
    db.close()


@pytest.mark.e2e
def test_unauthorized_summary_is_never_generated_by_winner_or_loser(
    app_client,
    self_study_activity,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session_id = _configure_and_open(app_client, self_study_activity, authorized=False)
    session_factory = app_client.__db_sessionmaker__
    winner_db = session_factory()
    loser_db = session_factory()
    winner_view = winner_db.get(models.Session, session_id)
    loser_view = loser_db.get(models.Session, session_id)
    config = (
        winner_db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=winner_view.activity_configuration_id)
        .one()
    )
    summary_calls = 0

    def unexpected_summary(*args, **kwargs):
        nonlocal summary_calls
        summary_calls += 1
        raise AssertionError("unauthorized study summary generation")

    monkeypatch.setattr(end_study_session, "generate_study_summary", unexpected_summary)

    assert close_study_session(winner_db, winner_view, config, status="closed_limit_reached") is None
    winner_db.commit()
    assert close_study_session(loser_db, loser_view, None, status="closed_error_safe") is None
    loser_db.commit()
    winner_db.close()
    loser_db.close()

    assert summary_calls == 0
    db = session_factory()
    assert db.get(models.Session, session_id).status == "closed_limit_reached"
    assert _event_count(db, session_id, "study_session_summary") == 0
    db.close()


@pytest.mark.e2e
def test_sequential_repeat_does_not_redeliver_study_summary(
    app_client,
    self_study_activity,
) -> None:
    session_id = _configure_and_open(app_client, self_study_activity, authorized=True)
    session_factory = app_client.__db_sessionmaker__
    db = session_factory()
    session = db.get(models.Session, session_id)
    config = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=session.activity_configuration_id)
        .one()
    )

    first = close_study_session(db, session, config, status="closed_voluntary")
    second = close_study_session(db, session, config, status="closed_limit_reached")

    assert first is not None
    assert second is None
    assert session.status == "closed_voluntary"
    assert _event_count(db, session_id, "technical_summary") == 1
    assert _event_count(db, session_id, "session_closed") == 1
    assert _event_count(db, session_id, "study_session_summary") == 1
    db.rollback()
    db.close()


@pytest.mark.e2e
def test_outer_rollback_restores_claim_summaries_event_and_lock(
    app_client,
    self_study_activity,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session_id = _configure_and_open(app_client, self_study_activity, authorized=True)
    session_factory = app_client.__db_sessionmaker__
    db = session_factory()
    session = db.get(models.Session, session_id)
    config = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=session.activity_configuration_id)
        .one()
    )
    real_summary: Callable = end_study_session.generate_study_summary

    def fail_after_summary(*args, **kwargs):
        real_summary(*args, **kwargs)
        raise RuntimeError("T150 after persisted study summary")

    monkeypatch.setattr(end_study_session, "generate_study_summary", fail_after_summary)

    with pytest.raises(RuntimeError, match="T150 after persisted study summary"):
        close_study_session(db, session, config, status="closed_error_safe")
    db.rollback()
    db.close()

    verification_db = session_factory()
    persisted = verification_db.get(models.Session, session_id)
    assert persisted.status == "active"
    assert persisted.ended_at is None
    assert persisted.technical_summary_ref is None
    assert persisted.active_lock_token == "ACTIVE"
    assert _event_count(verification_db, session_id, "technical_summary") == 0
    assert _event_count(verification_db, session_id, "session_closed") == 0
    assert _event_count(verification_db, session_id, "study_session_summary") == 0
    verification_db.close()
