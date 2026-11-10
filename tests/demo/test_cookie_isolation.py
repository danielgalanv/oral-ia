from fastapi.testclient import TestClient

from oralia.interfaces.api.app import create_app


def test_demo_login_logout_do_not_replace_or_revoke_habitual_cookies(app_client, monkeypatch):
    habitual = app_client.cookies.get("oralia_admin")
    monkeypatch.setenv("ORALIA_COOKIE_NAMESPACE", "oralia_demo")
    with TestClient(create_app()) as demo:
        demo.cookies.update(dict(app_client.cookies))
        assert demo.get("/api/v1/auth/me").status_code == 401
        response = demo.post("/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"})
        assert response.status_code == 200
        assert demo.cookies.get("oralia_admin") == habitual
        assert demo.cookies.get("oralia_demo_admin")
        assert demo.get("/api/v1/auth/me").status_code == 200
        assert demo.post("/api/v1/auth/logout").status_code == 200
        assert demo.cookies.get("oralia_admin") == habitual
        assert app_client.get("/api/v1/auth/me").status_code == 200
