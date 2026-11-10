from datetime import timedelta

import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.access_helpers import own_session
from tests.contract.test_defense_output_authorization_matrix import _permit_template
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


@pytest.mark.parametrize("limit", ["turns", "duration"])
@pytest.mark.parametrize("voice", [False, True])
@pytest.mark.parametrize("scope", [[], ["transcript"], ["summary"], ["transcript", "summary"]])
def test_http_limit_executes_current_explicit_consent_once_and_purges(app_client, limit, voice, scope):
    factory = app_client.__db_sessionmaker__
    with factory() as db:
        session_id, _ = _seed_active_defense(db, retention_days=1)
        session = db.get(models.Session, session_id)
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        _permit_template(activity, "defense-limit-close", "oral_defense_close", "finish")
        if limit == "turns":
            activity.max_turns = 1
        else:
            session.started_at = utcnow() - timedelta(seconds=activity.max_duration_seconds)
        transcript = models.Transcript(
            session_id=session_id, raw_text="respuesta final de voz", status="awaiting_confirmation"
        )
        db.add(transcript)
        db.commit()
        transcript_id = transcript.id
    own_session(app_client, session_id)
    review = app_client.get(f"/api/v1/defense-sessions/{session_id}/defense-transcript")
    assert review.status_code == 200
    assert review.json()["turns"][0]["input_text"] == "Una respuesta"
    assert review.json()["transcripts"][0]["corrections"] == ["Una respuesta corregida"]
    consent = {"retain": bool(scope), "scope": scope}
    url = f"/api/v1/defense-sessions/{session_id}/defense-turns"
    body = {"text": "respuesta final", "closure_consent": consent}
    if voice:
        url += "/voice/confirm"
        body = {
            "transcript_id": transcript_id,
            "corrected_text": "respuesta final corregida",
            "closure_consent": consent,
        }
    response = app_client.post(url, json=body)
    assert response.status_code == 200, response.text
    assert response.json()["session_status"] == "closed_limit_reached"
    assert response.json()["defense_summary"] is not None
    with factory() as db:
        records = db.query(models.ConsentRecord).filter_by(session_id=session_id).all()
        assert len(records) == bool(scope)
        if scope:
            assert set(records[0].scope) == set(scope)
        assert bool(db.query(models.Transcript).filter_by(session_id=session_id).count()) == (
            "transcript" in scope
        )
        assert bool(
            db.query(models.TraceEvent)
            .filter_by(session_id=session_id, event_type="defense_session_summary")
            .count()
        ) == ("summary" in scope)
        assert all("audio" not in column.name for column in models.Transcript.__table__.columns)
        before_events = db.query(models.TraceEvent).filter_by(session_id=session_id).count()
    repeated = app_client.post(f"/api/v1/defense-sessions/{session_id}/defense-end", json=consent)
    assert repeated.status_code == 200
    assert repeated.json()["defense_summary"] is None
    with factory() as db:
        assert db.query(models.TraceEvent).filter_by(session_id=session_id).count() == before_events
        db.get(models.Session, session_id).ended_at = utcnow() - timedelta(days=2)
        db.commit()
    assert app_client.post("/api/v1/tecnica/defense/purge-expired").status_code == 200
    after = app_client.get(f"/api/v1/defense-sessions/{session_id}/defense-transcript").json()
    assert after == {"turns": [], "transcripts": []}
    assert app_client.post("/api/v1/tecnica/defense/purge-expired").json()["sessions_with_rows_deleted"] == 0
