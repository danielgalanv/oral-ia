from datetime import timedelta

import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_defense_retention_copies import _seed_copies
from tests.t090_policy_helpers import configure_test_recipients


@pytest.mark.parametrize("scope", [[], ["transcript"], ["summary"], ["transcript", "summary"]])
def test_closed_session_review_and_deletion_follow_scopes(db_session, scope):
    from oralia.application.services.session_privacy_service import delete_session_content, review_session

    sid, cfgid, marker = _seed_copies(db_session)
    session = db_session.get(models.Session, sid)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, cfgid),
        retain=bool(scope),
        scope=scope,
    )
    if scope:
        review = review_session(db_session, sid)
        assert bool(review["turns"]) == ("transcript" in scope)
        assert bool(review["summary"]) == ("summary" in scope)
        # Summary consent may legitimately retain a question containing the marker;
        # raw answers/originals/corrections belong only to transcript scope.
        assert (marker in str([review["turns"], review["transcripts"]])) == ("transcript" in scope)
    else:
        with pytest.raises(ValueError):
            review_session(db_session, sid)
    first = delete_session_content(db_session, sid, reason="user_request")
    second = delete_session_content(db_session, sid, reason="user_request")
    assert first == second
    assert marker not in str(first)
    state = db_session.get(models.CognitiveState, sid)
    assert state is None or (
        state.current_input == "" and state.participant_response == "" and state.concepts_addressed == []
    )
    with pytest.raises(ValueError):
        review_session(db_session, sid)


def test_active_session_cannot_be_deleted_and_expiry_is_not_reviewable(db_session):
    from oralia.application.services.session_privacy_service import (
        delete_session_content,
        purge_private_sessions,
        review_session,
    )

    sid, cfgid, _ = _seed_copies(db_session)
    with pytest.raises(ValueError, match="active"):
        delete_session_content(db_session, sid, reason="user_request")
    session = db_session.get(models.Session, sid)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, cfgid),
        retain=True,
        scope=["transcript", "summary"],
    )
    session.ended_at = utcnow() - timedelta(days=2)
    with pytest.raises(ValueError, match="reviewable"):
        review_session(db_session, sid)
    assert purge_private_sessions(db_session)["sessions_deleted"] == 1
    assert purge_private_sessions(db_session)["sessions_deleted"] == 0


@pytest.mark.parametrize("automatic", [False, True])
@pytest.mark.parametrize("scope", [[], ["transcript"], ["summary"], ["transcript", "summary"]])
def test_self_study_text_and_close_transport_current_consent_atomically(
    app_client, self_study_activity, automatic, scope
):
    from tests.integration.test_mode_doubt_resolution import _authorize_catalogued_self_study_outputs

    aid = self_study_activity["activity_id"]
    factory = app_client.__db_sessionmaker__
    with factory() as db:
        activity = db.get(models.ActivityConfiguration, aid)
        activity.max_turns = 1 if automatic else 5
        db.get(models.RetentionPolicy, activity.retention_policy_id).retention_days = 1
        db.commit()
    participant = "self-study-privacy-owner"
    _authorize_catalogued_self_study_outputs(app_client, aid, participant)
    assert (
        app_client.post(
            f"/api/v1/tecnica/activities/{aid}/self-study-config",
            json={
                "enabled_modes": ["doubt_resolution"],
                "retention_authorized": True,
                "summary_authorized": True,
            },
        ).status_code
        == 201
    )
    opened = app_client.post(
        "/api/v1/sessions", json={"participant_code": participant, "activity_configuration_id": aid}
    )
    sid = opened.json()["session_id"]
    choice = {"retain": bool(scope), "scope": scope}
    turn_choice = choice if automatic else {"retain": True, "scope": ["transcript", "summary"]}
    answered = app_client.post(
        f"/api/v1/sessions/{sid}/study-turns",
        json={"text": "pregunta ficticia sin fuente", "closure_consent": turn_choice},
    )
    assert answered.status_code == 200, answered.text
    if not automatic:
        closed = app_client.post(f"/api/v1/sessions/{sid}/study-end", json=choice)
        assert closed.status_code == 200
        assert closed.json()["study_summary"] is not None
    repeated = app_client.post(f"/api/v1/sessions/{sid}/study-end", json={"retain": False, "scope": []})
    assert repeated.status_code == 200 and repeated.json()["study_summary"] is None
    assert set(app_client.get(f"/api/v1/sessions/{sid}/privacy").json()["scope"]) == set(scope)
    review = app_client.get(f"/api/v1/governance/sessions/{sid}")
    assert review.status_code == (200 if scope else 404)
    if scope:
        assert bool(review.json()["turns"]) == ("transcript" in scope)
        assert bool(review.json()["summary"]) == ("summary" in scope)
    with factory() as db:
        assert db.get(models.Session, sid).status != "active"
        records = db.query(models.ConsentRecord).filter_by(session_id=sid).all()
        assert len(records) == bool(scope)
        if scope:
            assert set(records[0].scope) == set(scope)


def test_failed_privacy_erasure_rolls_back_close_turn_and_preference(
    app_client, self_study_activity, monkeypatch
):
    from oralia.application.services import session_privacy_service

    aid = self_study_activity["activity_id"]
    assert (
        app_client.post(
            f"/api/v1/tecnica/activities/{aid}/self-study-config",
            json={"enabled_modes": ["doubt_resolution"], "summary_authorized": True},
        ).status_code
        == 201
    )
    configure_test_recipients(app_client, aid, recipients=("rollback-privacy",))
    opened = app_client.post(
        "/api/v1/sessions", json={"participant_code": "rollback-privacy", "activity_configuration_id": aid}
    )
    sid = opened.json()["session_id"]

    def fail_erasure(*args, **kwargs):
        raise RuntimeError("injected privacy failure")

    monkeypatch.setattr(session_privacy_service, "erase_content", fail_erasure)
    with pytest.raises(RuntimeError, match="injected privacy failure"):
        app_client.post(f"/api/v1/sessions/{sid}/study-end", json={"retain": False, "scope": []})
    with app_client.__db_sessionmaker__() as db:
        session = db.get(models.Session, sid)
        assert session.status == "active" and session.active_lock_token == "ACTIVE"
        assert db.query(models.SessionDeletionReceipt).filter_by(session_id=sid).count() == 0
        assert db.query(models.ConsentRecord).filter_by(session_id=sid).count() == 0
        assert db.query(models.SessionPrivacyPreference).filter_by(session_id=sid).count() == 0
