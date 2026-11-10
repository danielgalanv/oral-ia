import pytest
from fastapi.testclient import TestClient

from oralia.demo.access import enable_demo_teacher_access
from oralia.demo.resources import DemoError, DemoPaths, child_environment
from oralia.interfaces.api.app import create_app


def test_demo_teacher_without_login_keeps_session_ownership(tmp_path, monkeypatch):
    paths = DemoPaths(tmp_path)
    paths.initialize()
    for key, value in child_environment(paths, 5180).items():
        monkeypatch.setenv(key, value)
    app = create_app()
    enable_demo_teacher_access(app, paths)
    with TestClient(app) as client:
        assert client.get("/api/v1/auth/me").json()["role"] == "teacher"
        assert (
            client.post("/api/v1/defense-sessions/foreign/defense-turns", json={"text": "x"}).status_code
            == 403
        )
        assert client.get("/api/v1/auth/me", headers={"Origin": "https://foreign.example"}).status_code == 403
    # The same environment alone must not activate the grant in the normal app.
    with TestClient(create_app()) as client:
        assert client.get("/api/v1/auth/me").status_code in {401, 503}


def test_demo_access_refuses_habitual_database(tmp_path, monkeypatch):
    paths = DemoPaths(tmp_path)
    paths.initialize()
    monkeypatch.setenv("ORALIA_DB_URL", "sqlite:///oralia.db")
    with pytest.raises(DemoError):
        enable_demo_teacher_access(create_app(), paths)
