import base64
import json

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi import HTTPException

from oralia.documentary.public_access import PublicAccess

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
NOW = 1_000_000.0


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def jwk(kid="k1"):
    n = KEY.public_key().public_numbers()
    return {"kid": kid, "n": b64(n.n.to_bytes(256, "big")), "e": b64(n.e.to_bytes(3, "big"))}


def token(email="ana@alumnos.upm.es", aud="AUD", exp=NOW + 100, iss="https://team.cloudflareaccess.com", kid="k1"):
    head = b64(json.dumps({"alg": "RS256", "kid": kid}).encode())
    body = b64(json.dumps({"email": email, "aud": [aud], "exp": exp, "iss": iss}).encode())
    sig = KEY.sign(f"{head}.{body}".encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{head}.{body}.{b64(sig)}"


def access(**kwargs):
    return PublicAccess(["estudio.example.org"], "team.cloudflareaccess.com", "AUD", fetch_keys=lambda: [jwk()],
                        clock=lambda: NOW, **kwargs)


def test_valid_identity():
    assert access().verify(token()) == "ana@alumnos.upm.es"


@pytest.mark.parametrize(
    "bad",
    [
        token(email="ana@gmail.com"),
        token(email="x@alumnos.upm.es.evil.com"),
        token(aud="OTRA"),
        token(exp=NOW - 1),
        token(iss="https://otro.cloudflareaccess.com"),
        token(kid="desconocida"),
        token()[:-4] + "AAAA",
        "",
        "a.b.c",
    ],
)
def test_rejected_identity(bad):
    with pytest.raises(HTTPException) as error:
        access().verify(bad)
    assert error.value.status_code == 401


def test_surface_blocked():
    a = access()
    for path in ("/api/v1/retrieval", "/api/v1/documentary/x/pages", "/api/v1/documentary/x/original",
                 "/api/v1/documentary/x/preview/3", "/tecnica"):
        assert a.blocked(path)
    assert not a.blocked("/api/v1/study-lab/turn") and not a.blocked("/api/v1/documentary")


def test_one_turn_in_flight_and_rate():
    a = access(turns_per_minute=2)
    release = a.admit_turn("t")
    with pytest.raises(HTTPException) as error:
        a.admit_turn("t")
    assert error.value.status_code == 429
    release()
    a.admit_turn("t")()
    with pytest.raises(HTTPException):
        a.admit_turn("t")


def test_global_queue_limit():
    a = access(max_queue=2)
    a.admit_turn("a"), a.admit_turn("b")
    with pytest.raises(HTTPException) as error:
        a.admit_turn("c")
    assert error.value.status_code == 503


def test_one_grant_per_email():
    revoked = []

    class Manager:
        def revoke(self, token):
            revoked.append(token)

    a = access()
    a.register("ana@alumnos.upm.es", "t1", Manager())
    a.register("ana@alumnos.upm.es", "t2", Manager())
    assert revoked == ["t1"] and a.by_email["ana@alumnos.upm.es"] == "t2"


def test_app_public_host(monkeypatch):
    from fastapi.testclient import TestClient

    from oralia.documentary import public_access as module
    from oralia.documentary.__main__ import create_app

    monkeypatch.setenv("ORALIA_PUBLIC_HOSTS", "estudio.example.org")
    monkeypatch.setenv("ORALIA_ACCESS_TEAM", "team.cloudflareaccess.com")
    monkeypatch.setenv("ORALIA_ACCESS_AUD", "AUD")
    monkeypatch.setattr(module.PublicAccess, "_download_keys", lambda self: [jwk()])
    # La caducidad se evalúa con el reloj real: se firma un token vigente.
    import time

    good = token(exp=time.time() + 600)
    with TestClient(create_app(), base_url="https://estudio.example.org") as client:
        assert client.post("/documentary/enter").status_code == 401  # sin identidad
        assert client.post("/documentary/enter", headers={"Cf-Access-Jwt-Assertion": token(email="x@gmail.com", exp=time.time() + 600)}).status_code == 401
        entered = client.post("/documentary/enter", headers={"Cf-Access-Jwt-Assertion": good})
        assert entered.status_code == 200 and "secure" in entered.headers["set-cookie"].lower()
        assert client.get("/api/v1/documentary").status_code == 200
        for path in ("/api/v1/documentary/docente-procedimiento/pages", "/api/v1/documentary/docente-procedimiento/original", "/tecnica"):
            assert client.get(path).status_code == 404
    with TestClient(create_app(), base_url="http://127.0.0.1") as local:  # el docente conserva el acceso local
        assert local.post("/documentary/enter").status_code == 200
        assert local.get("/api/v1/documentary/docente-procedimiento/pages").status_code == 200
    with TestClient(create_app(), base_url="https://otro.example.org") as foreign:
        assert foreign.post("/documentary/enter").status_code == 403
