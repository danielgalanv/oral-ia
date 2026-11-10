"""Owned SQLite and local access only; no abandoned-session policy is introduced."""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from sqlalchemy.orm import sessionmaker

from oralia.application.commands.end_session import close_session_with_outcome
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.local_access import LocalAccess
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


def test_two_connections_and_retry_have_one_close_commit(db_engine):
    factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    with factory() as db:
        sid, _ = _seed_active_defense(db)
        db.commit()
    barrier = Barrier(2)

    def close():
        with factory() as db:
            session = db.get(models.Session, sid)
            barrier.wait(timeout=10)
            outcome = close_session_with_outcome(db, session)
            db.commit()
            return outcome.transition_won

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: close(), range(2)))
    assert sorted(results) == [False, True]
    with factory() as db:
        assert close_session_with_outcome(db, db.get(models.Session, sid)).transition_won is False
        assert db.query(models.TraceEvent).filter_by(session_id=sid, event_type="session_closed").count() == 1
        assert db.get(models.Session, sid).active_lock_token is None


def test_restart_loses_owner_token_but_teacher_can_confirm_close(app_client, seeded_activity):
    opened = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "participant", "activity_configuration_id": seeded_activity},
    )
    assert opened.status_code == 201
    sid = opened.json()["session_id"]
    # Recreate exactly the volatile access component; persisted SQL is retained.
    app_client.app.state.local_access = LocalAccess()
    assert app_client.get(f"/api/v1/sessions/{sid}/resume").status_code == 401
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "active"
    assert (
        app_client.post(
            "/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"}
        ).status_code
        == 200
    )
    endpoint = f"/api/v1/governance/sessions/{sid}/close"
    assert app_client.post(endpoint, json={"confirm": True, "reason": "owner_access_lost"}).json()[
        "transition_won"
    ]
    assert not app_client.post(endpoint, json={"confirm": True, "reason": "owner_access_lost"}).json()[
        "transition_won"
    ]


@pytest.mark.parametrize("commit", [False, True])
def test_owned_process_crash_before_or_after_close_commit(db_engine, commit):
    factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    with factory() as db:
        sid, _ = _seed_active_defense(db)
        db.commit()
    code = """
import os, sys
from sqlalchemy.orm import Session
from oralia.infrastructure.db.engine import build_engine
from oralia.infrastructure.db import models
from oralia.application.commands.end_session import close_session_with_outcome
engine = build_engine(sys.argv[1])
db = Session(engine)
close_session_with_outcome(db, db.get(models.Session, sys.argv[2]))
if sys.argv[3] == 'commit':
    db.commit()
os._exit(23)
"""
    crashed = subprocess.run(
        [sys.executable, "-c", code, str(db_engine.url), sid, "commit" if commit else "rollback"],
        capture_output=True,
        timeout=30,
    )
    assert crashed.returncode == 23, crashed.stderr.decode(errors="replace")
    with factory() as db:
        session = db.get(models.Session, sid)
        assert (session.status == "active") is (not commit)
        count = db.query(models.TraceEvent).filter_by(session_id=sid, event_type="session_closed").count()
        assert count == int(commit)
        assert close_session_with_outcome(db, session).transition_won is (not commit)
        db.commit()
        assert db.query(models.TraceEvent).filter_by(session_id=sid, event_type="session_closed").count() == 1
