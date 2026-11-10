"""US6 Escenario E: after closing the app and restarting it, a maintainer can open a
conserved session and reconstruct its configuration, turns, agents, and state changes.

Simulated by closing every SQLAlchemy connection/session and rebuilding a brand-new
engine + FastAPI app instance against the same on-disk SQLite file — nothing is shared
in-process across the "restart" boundary except the file itself.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine
from tests.t090_policy_helpers import minimal_output_policy_columns


def _make_client(engine):
    from oralia.interfaces.api.app import create_app
    from oralia.interfaces.api.deps.db import get_db

    Session = sessionmaker(bind=engine, expire_on_commit=False)

    def _override():
        db = Session()
        try:
            yield db
            db.commit()
        finally:
            db.close()

    os.environ["ORALIA_ADMIN_SECRET"] = "fictional-restart-installation-secret-005"
    app = create_app()
    app.dependency_overrides[get_db] = _override
    client = TestClient(app)
    assert (
        client.post(
            "/api/v1/auth/login", json={"secret": "fictional-restart-installation-secret-005"}
        ).status_code
        == 200
    )
    return client, Session


@pytest.mark.integration
def test_session_reconstructable_after_simulated_restart(tmp_path: Path):
    db_path = tmp_path / "restart_test.db"
    url = f"sqlite:///{db_path}"

    # --- "before restart": run a full session lifecycle ---
    engine_1 = build_engine(url)
    Base.metadata.create_all(engine_1)
    client_1, Session1 = _make_client(engine_1)

    db = Session1()
    course = models.Course(name="C", subject_code="C1")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db.add_all([course, policy])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Actividad reinicio",
        subject="s",
        objective="o",
        mode="texto",
        language="es",
        max_turns=10,
        max_duration_seconds=600,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(recipients=("part-restart001",)),
    )
    db.add(activity)
    db.commit()
    activity_id = activity.id
    db.close()

    start = client_1.post(
        "/api/v1/sessions",
        json={"participant_code": "part-restart001", "activity_configuration_id": activity_id},
    )
    sid = start.json()["session_id"]
    client_1.post(f"/api/v1/sessions/{sid}/turns", json={"text": "antes del reinicio"})
    client_1.post(f"/api/v1/sessions/{sid}/end")

    before_detail = client_1.get(f"/api/v1/sessions/{sid}").json()
    before_trace = client_1.get(f"/api/v1/sessions/{sid}/trace").json()

    client_1.close()
    engine_1.dispose()

    # --- "after restart": brand-new engine/app instance, same file ---
    engine_2 = build_engine(url)
    client_2, _ = _make_client(engine_2)

    after_detail = client_2.get(f"/api/v1/sessions/{sid}").json()
    after_trace = client_2.get(f"/api/v1/sessions/{sid}/trace").json()

    assert after_detail["session"]["status"] == "closed_voluntary"
    assert after_detail["session"]["status"] == before_detail["session"]["status"]
    assert after_detail["activity_configuration"]["name"] == "Actividad reinicio"
    assert after_detail["turns"] == before_detail["turns"]
    assert after_detail["technical_summary"] == before_detail["technical_summary"]

    assert len(after_trace["trace_events"]) == len(before_trace["trace_events"])
    assert len(after_trace["state_patches"]) == len(before_trace["state_patches"])
    assert [p["applied"] for p in after_trace["state_patches"]] == [
        p["applied"] for p in before_trace["state_patches"]
    ]

    client_2.close()
    engine_2.dispose()
