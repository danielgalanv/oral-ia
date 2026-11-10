import json

import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.infrastructure.db import models
from tests.integration.test_defense_retention_copies import _seed_copies


def test_export_requires_text_review_and_aliases_identifiers(db_session):
    from oralia.application.services.session_export_service import export_sessions

    sid, cfgid, marker = _seed_copies(db_session)
    session = db_session.get(models.Session, sid)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, cfgid),
        retain=True,
        scope=["transcript", "summary"],
    )
    db_session.add(
        models.TraceEvent(
            session_id=sid,
            event_type="injected_secret",
            payload={"secret": "SENSITIVE-005", "chain_of_thought": "PRIVATE-005", "audio": "AUDIO-005"},
        )
    )
    db_session.flush()
    with pytest.raises(ValueError, match="review"):
        export_sessions(db_session, [sid], include_free_text=True)
    bundle, markdown = export_sessions(db_session, [sid], include_free_text=True, reviewed_free_text=True)
    serialized = json.dumps(bundle) + markdown
    assert marker in serialized
    assert sid not in serialized and session.participant_code not in serialized
    assert all(value not in serialized for value in ["SENSITIVE-005", "PRIVATE-005", "AUDIO-005"])
    assert bundle["schema_version"] == 1 and "Transcripción" in markdown
    without_text, _ = export_sessions(db_session, [sid])
    assert marker not in json.dumps(without_text)


def test_mixed_export_fails_without_partial_bundle(db_session):
    from oralia.application.services.session_export_service import export_sessions

    sid, cfgid, _ = _seed_copies(db_session)
    session = db_session.get(models.Session, sid)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, cfgid),
        retain=True,
        scope=["summary"],
    )
    with pytest.raises(ValueError, match="reviewable"):
        export_sessions(db_session, [sid, "missing"])


def test_known_pseudonym_and_session_ids_are_replaced_even_in_reviewed_free_text(db_session):
    from oralia.application.services.session_export_service import export_sessions

    sid, cfgid, _ = _seed_copies(db_session)
    session = db_session.get(models.Session, sid)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, cfgid),
        retain=True,
        scope=["transcript"],
    )
    turn = db_session.query(models.Turn).filter_by(session_id=sid).first()
    turn.input_text = f"Texto ficticio: código {session.participant_code}, sesión {sid}."
    db_session.flush()
    bundle, markdown = export_sessions(db_session, [sid], include_free_text=True, reviewed_free_text=True)
    serialized = json.dumps(bundle) + markdown
    assert session.participant_code not in serialized and sid not in serialized
    assert "participant-1" in serialized
