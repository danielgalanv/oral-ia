"""Owned terminal lifecycle, normal authentication, repetition and cancellation."""

import json
import os
import sqlite3
import subprocess
import sys
import time

import pytest
from fastapi.testclient import TestClient

from oralia.course_study.__main__ import WORKSPACE, interactive, owned_lock, root_for
from oralia.course_study.preparation import prepare
from oralia.infrastructure.db import models


def test_unmarked_directory_is_not_changed(tmp_path):
    root = tmp_path / ".oralia-course-study"
    root.mkdir()
    witness = root / "keep.txt"
    witness.write_text("untouched")
    with pytest.raises((ValueError, FileNotFoundError)):
        root_for(tmp_path)
    assert witness.read_text() == "untouched"


def test_root_marker_and_operation_lock(tmp_path):
    root = root_for(tmp_path)
    assert root_for(tmp_path) == root
    with owned_lock(root):
        with pytest.raises(ValueError, match="Ya hay"):
            with owned_lock(root):
                pytest.fail("concurrent operation acquired")


@pytest.mark.skipif(
    not os.environ.get("ORALIA_COURSE_CLI_TESTS"), reason="explicit external PDF and subprocess resource test"
)
@pytest.mark.parametrize("cancel", [False, True])
def test_terminal_uses_normal_participant_access_and_closes(app_client, tmp_path, cancel):
    prepared = prepare(app_client)
    output = []
    pending = tmp_path / "pending.json"

    def read(_):
        if cancel:
            raise KeyboardInterrupt
        return "/salir"

    with TestClient(app_client.app) as learner:
        assert learner.get("/api/v1/governance/activities").status_code == 401
        assert not hasattr(learner.app.state, "demo_teacher_grant")
        sid = interactive(learner, prepared, read=read, write=output.append, pending=pending)
        assert learner.get("/api/v1/governance/activities").status_code == 403
    assert not pending.exists()
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "closed_voluntary"
        assert db.get(models.CognitiveState, sid) is None
        assert not db.query(models.Turn).filter_by(session_id=sid).count()
    assert not any("access_token" in line or "fictional-installation-secret" in line for line in output)


@pytest.mark.skipif(
    not os.environ.get("ORALIA_COURSE_CLI_TESTS"), reason="explicit external PDF and subprocess resource test"
)
def test_fresh_process_idempotence_secret_and_database_boundary(tmp_path):
    sentinel = "fictional-parent-secret-DO-NOT-PRINT-011"
    env = {**os.environ, "ORALIA_ADMIN_SECRET": sentinel}
    timings = []
    bootstrap = """
import contextlib, io, pathlib, runpy, secrets, sys
values = []
original = secrets.token_urlsafe
def observed(*args, **kwargs):
    value = original(*args, **kwargs)
    values.append(value)
    return value
secrets.token_urlsafe = observed
workspace = sys.argv[1]
sys.argv = ['oralia.course_study', '--workspace', workspace]
output, errors = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
    try:
        runpy.run_module('oralia.course_study', run_name='__main__')
        status = 0
    except SystemExit as exc:
        status = exc.code or 0
text = output.getvalue() + errors.getvalue()
root = pathlib.Path(workspace) / '.oralia-course-study'
configs = ''.join(p.read_text(encoding='utf-8') for p in (root / 'config').glob('*.json'))
if len(values) < 3 or any(value in text + configs for value in values):
    print('Credential/token scan failed; values intentionally withheld')
    sys.exit(91)
print(output.getvalue())
print(errors.getvalue(), file=sys.stderr)
print('Credential/token scan: no generated value in output/config; count', len(values))
sys.exit(status)
"""
    for _ in range(2):
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-c", bootstrap, str(tmp_path)],
            input="/salir\n",
            text=True,
            encoding="utf-8",
            capture_output=True,
            env=env,
            cwd=WORKSPACE,
            timeout=120,
        )
        timings.append(time.perf_counter() - start)
        assert result.returncode == 0, result.stdout + result.stderr
        assert sentinel not in result.stdout + result.stderr
        assert "Credential/token scan: no generated value" in result.stdout
    root = tmp_path / ".oralia-course-study"
    with sqlite3.connect(root / "course.db") as db:
        assert db.execute("select count(*) from course").fetchone()[0] == 1
        assert db.execute("select count(*) from material_document").fetchone()[0] == 1
        assert db.execute("select count(*) from activity_configuration").fetchone()[0] == 1
        assert db.execute("select count(*) from session where status='active'").fetchone()[0] == 0
    assert sentinel not in json.dumps(json.loads((root / "config/activity.json").read_text(encoding="utf-8")))
    print("Fresh process prepared-resource durations:", timings)


def test_linked_database_is_rejected_without_modifying_target(tmp_path):
    root = root_for(tmp_path)
    original = tmp_path / "usual-data.db"
    original.write_bytes(b"unchanged")
    (root / "course.db").hardlink_to(original)
    with pytest.raises(ValueError, match="enlace duro"):
        root_for(tmp_path)
    assert original.read_bytes() == b"unchanged"
