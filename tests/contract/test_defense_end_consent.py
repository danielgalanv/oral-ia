"""T076/T082 contract for oral-defense close retention input."""

from oralia.infrastructure.db import models
from tests.access_helpers import own_session
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


def test_defense_end_accepts_retain_scope_and_repeated_close_is_effect_free(app_client) -> None:
    db = app_client.__db_sessionmaker__()
    session_id, _ = _seed_active_defense(db)
    db.close()
    own_session(app_client, session_id)

    first = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-end",
        json={"retain": True, "scope": ["transcript", "summary"]},
    )
    second = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-end",
        json={"retain": True, "scope": ["transcript", "summary"]},
    )

    assert first.status_code == 200
    assert first.json()["status"] == "closed_voluntary"
    assert first.json()["defense_summary"] is not None
    assert second.status_code == 200
    assert second.json() == {
        "session_id": session_id,
        "status": "closed_voluntary",
        "defense_summary": None,
    }
    check = app_client.__db_sessionmaker__()
    assert check.query(models.ConsentRecord).filter_by(session_id=session_id).count() == 1
    check.close()


def test_defense_end_rejects_audio_or_ambiguous_scope_before_closing(app_client) -> None:
    db = app_client.__db_sessionmaker__()
    session_id, _ = _seed_active_defense(db)
    db.close()
    own_session(app_client, session_id)

    audio = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-end",
        json={"retain": True, "scope": ["audio"]},
    )
    unused = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-end",
        json={"retain": False, "scope": ["transcript"]},
    )

    assert audio.status_code == 422
    assert unused.status_code == 422
    check = app_client.__db_sessionmaker__()
    assert check.get(models.Session, session_id).status == "active"
    assert check.query(models.ConsentRecord).filter_by(session_id=session_id).count() == 0
    check.close()
