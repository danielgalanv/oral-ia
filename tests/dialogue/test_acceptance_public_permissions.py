"""Public safety of every cycle-4 input, separate from act classification."""

import hashlib
import json
import os
from pathlib import Path
from uuid import uuid4

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import prepare_guided

FOLDER = Path(__file__).parent / "fixtures/acceptance-cycle-4"
freeze = json.loads((FOLDER / "freeze.json").read_text(encoding="utf-8"))
assert hashlib.sha256((FOLDER / "inputs.json").read_bytes()).hexdigest() == freeze["sha256"]["inputs.json"]
CASES = json.loads((FOLDER / "inputs.json").read_text(encoding="utf-8"))["entries"]
pytestmark = pytest.mark.skipif(
    os.environ.get("ORALIA_RUN_PUBLIC_INPUT_SAFETY") != "1", reason="explicit 48-input public safety matrix"
)


@pytest.mark.parametrize("index,case", list(enumerate(CASES)), ids=[case["case_id"] for case in CASES])
def test_each_reserved_input_cannot_change_permissions_or_cross_session(app_client, index, case):
    mode = "self_study" if index % 2 == 0 else "oral_defense"
    prepared = prepare_guided(app_client, domain="agua" if index % 4 < 2 else "programa", mode=mode)
    sid = prepared["session"]["session_id"]
    names = app_client.app.state.local_access.cookie_names
    owner = app_client.cookies.get(names[1])
    grant = app_client.app.state.local_access.resolve(owner)
    assert grant and grant.role == "participant"
    app_client.cookies.clear()
    app_client.cookies.set(names[1], owner)
    tables = [
        models.Course,
        models.ActivityConfiguration,
        models.RetentionPolicy,
        models.MaterialDocument,
        models.TeachingUnit,
        models.Session,
        models.ConsentRecord,
    ]
    with app_client.__db_sessionmaker__() as db:
        before = {table.__name__: db.query(table).count() for table in tables}
        activity = db.get(models.ActivityConfiguration, prepared["activity"]["id"])
        policy_before = json.dumps(
            {col.name: getattr(activity, col.name) for col in activity.__table__.columns},
            default=str,
            sort_keys=True,
        )
    path = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    if mode == "oral_defense":
        assert app_client.post(path, json={"text": ""}).status_code == 200
    result = app_client.post(path, json={"text": case["text"]})
    assert result.status_code in {200, 409}, result.text
    assert owner not in result.text
    for source in result.json().get("sources", []):
        assert source["document_id"] == prepared["document"]["id"]
        if mode == "oral_defense":
            assert not source.get("fragment_text")
    assert (
        app_client.post(
            "/api/v1/governance/courses", json={"name": "unauthorized", "subject_code": "NO"}
        ).status_code
        == 403
    )
    assert app_client.post("/api/v1/governance/exports", json={"session_ids": [sid]}).status_code == 403
    assert app_client.get(f"/api/v1/sessions/{uuid4()}/resume").status_code == 403
    assert app_client.app.state.local_access.resolve(owner) == grant
    with app_client.__db_sessionmaker__() as db:
        assert {table.__name__: db.query(table).count() for table in tables} == before
        activity = db.get(models.ActivityConfiguration, prepared["activity"]["id"])
        assert (
            json.dumps(
                {col.name: getattr(activity, col.name) for col in activity.__table__.columns},
                default=str,
                sort_keys=True,
            )
            == policy_before
        )
    folder = (
        Path(__file__).resolve().parents[2]
        / "specs/010-guided-dialogue/public-input-safety"
        / os.environ["ORALIA_DIALOGUE_RUN_ID"]
    )
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / f"{case['case_id']}.json").open("x", encoding="utf-8") as stream:
        json.dump(
            {
                "case_id": case["case_id"],
                "mode": mode,
                "domain": "agua" if index % 4 < 2 else "programa",
                "http_status": result.status_code,
                "scope": (
                    "real participant grant; immutable governance, no extra session/consent, "
                    "foreign resume denied, teacher operations denied; not a classification oracle"
                ),
                "passed": True,
            },
            stream,
            indent=2,
        )
