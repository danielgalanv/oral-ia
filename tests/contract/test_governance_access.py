import pytest
from fastapi.testclient import TestClient


def test_existing_teacher_routes_fail_closed_without_installation_secret(monkeypatch):
    from oralia.interfaces.api.app import create_app

    monkeypatch.delenv("ORALIA_ADMIN_SECRET", raising=False)
    with TestClient(create_app()) as client:
        for url in ("/api/v1/sessions", "/api/v1/catalog/agents", "/api/v1/materials/documents"):
            response = client.get(url)
            assert response.status_code == 503


def test_local_login_logout_and_wrong_role_are_enforced(monkeypatch):
    from oralia.interfaces.api.app import create_app

    monkeypatch.setenv("ORALIA_ADMIN_SECRET", "fictional-installation-secret-005")
    with TestClient(create_app()) as client:
        assert client.get("/api/v1/catalog/agents").status_code == 401
        assert (
            client.get(
                "/api/v1/catalog/agents",
                headers={"Authorization": "Bearer fictional-installation-secret-005"},
            ).status_code
            == 401
        )
        assert client.post("/api/v1/auth/login", json={"secret": "wrong"}).status_code == 401
        result = client.post("/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"})
        assert result.status_code == 200
        assert "httponly" in result.headers["set-cookie"].lower()
        assert result.headers["cache-control"] == "no-store"
        assert client.get("/api/v1/auth/me").json()["role"] == "teacher"
        assert client.post("/api/v1/auth/logout").status_code == 200
        assert client.get("/api/v1/auth/me").status_code == 401
        assert client.post("/api/v1/auth/logout").status_code == 200
        participant = client.app.state.local_access.issue("participant", "owned-session")
        client.headers["Authorization"] = f"Bearer {participant}"
        for url in ("/api/v1/catalog/agents", "/api/v1/sessions", "/api/v1/tecnica/defense/purge-expired"):
            assert client.get(url).status_code == 403
        assert (
            client.post(
                "/api/v1/defense-sessions/another-session/defense-turns", json={"text": "private"}
            ).status_code
            == 403
        )


def test_origin_and_expired_token_never_reveal_secrets(monkeypatch, caplog):
    from oralia.interfaces.api.app import create_app

    secret = "fictional-installation-secret-005"
    monkeypatch.setenv("ORALIA_ADMIN_SECRET", secret)
    with TestClient(create_app()) as client:
        assert (
            client.post(
                "/api/v1/auth/login", headers={"Origin": "https://hostile.example"}, json={"secret": secret}
            ).status_code
            == 403
        )
        token = client.app.state.local_access.issue("teacher", ttl=-1)
        assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
        assert secret not in caplog.text and token not in caplog.text


@pytest.mark.parametrize(
    "method,path",
    [
        ("GET", "/api/v1/sessions"),
        ("GET", "/api/v1/catalog/agents"),
        ("GET", "/api/v1/materials/documents"),
        ("POST", "/api/v1/materials/index/rebuild"),
        ("POST", "/api/v1/activities"),
        ("GET", "/api/v1/tecnica/sessions/other/study-trace"),
        ("GET", "/api/v1/tecnica/defense-sessions/other/defense-trace"),
        ("GET", "/api/v1/governance/catalog"),
        ("GET", "/api/v1/governance/sessions"),
        ("POST", "/api/v1/governance/exports"),
        ("POST", "/api/v1/governance/purge"),
        ("GET", "/api/v1/governance/metrics"),
        ("DELETE", "/api/v1/sessions/other/content"),
    ],
)
def test_route_inventory_denies_anonymous_and_participant_roles(monkeypatch, method, path, capsys):
    from oralia.interfaces.api.app import create_app

    monkeypatch.setenv("ORALIA_ADMIN_SECRET", "fictional-installation-secret-005")
    with TestClient(create_app()) as client:
        assert client.request(method, path).status_code == 401
        token = client.app.state.local_access.issue("participant", "owned")
        assert client.request(method, path, headers={"Authorization": f"Bearer {token}"}).status_code == 403
    logged = capsys.readouterr().out
    assert "access_denied" in logged
    assert token not in logged and "fictional-installation-secret-005" not in logged


async def test_non_loopback_is_denied_until_explicit_administrative_opt_in(monkeypatch):
    import httpx

    from oralia.interfaces.api.app import create_app

    monkeypatch.setenv("ORALIA_ADMIN_SECRET", "fictional-installation-secret-005")
    monkeypatch.delenv("ORALIA_ALLOW_LAN", raising=False)
    app = create_app()
    token = app.state.local_access.issue("teacher")
    transport = httpx.ASGITransport(app=app, client=("192.0.2.2", 1234))
    async with httpx.AsyncClient(
        transport=transport, base_url="http://127.0.0.1", headers={"Authorization": f"Bearer {token}"}
    ) as client:
        assert (await client.get("/api/v1/auth/me")).status_code == 403
        monkeypatch.setenv("ORALIA_ALLOW_LAN", "1")
        assert (await client.get("/api/v1/auth/me")).status_code == 200
