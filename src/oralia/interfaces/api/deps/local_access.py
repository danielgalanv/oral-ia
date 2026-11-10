"""Local role/session authorization; no identity database or production bypass."""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import os
import re
import secrets
import time
from dataclasses import dataclass
from urllib.parse import urlparse

import structlog
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

_LOG = structlog.get_logger()
_SESSION_PATH = re.compile(r"^/api/v1/(?:defense-sessions|sessions)/([^/]+)(?:/(.*))?$")


@dataclass(frozen=True)
class AccessGrant:
    role: str
    session_id: str | None
    expires_at: float


class LocalAccess:
    def __init__(self):
        namespace = os.environ.get("ORALIA_COOKIE_NAMESPACE", "oralia")
        if namespace not in {"oralia", "oralia_demo"}:
            raise ValueError("unsupported local cookie namespace")
        self.cookie_names = (f"{namespace}_admin", f"{namespace}_participant")
        self._tokens: dict[str, AccessGrant] = {}
        self._login_attempts: list[float] = []

    def issue(self, role: str, session_id: str | None = None, *, ttl: int | None = None) -> str:
        now = time.monotonic()
        self._tokens = {key: value for key, value in self._tokens.items() if value.expires_at > now}
        if len(self._tokens) >= 4096:
            raise HTTPException(503, "local access capacity reached")
        if ttl is None:
            ttl = 3600 if role == "teacher" else 86400
        token = secrets.token_urlsafe(32)
        self._tokens[hashlib.sha256(token.encode()).hexdigest()] = AccessGrant(role, session_id, now + ttl)
        return token

    def resolve(self, token: str) -> AccessGrant | None:
        key = hashlib.sha256(token.encode()).hexdigest()
        grant = self._tokens.get(key)
        if grant is not None and grant.expires_at > time.monotonic():
            return grant
        self._tokens.pop(key, None)
        return None

    def revoke(self, token: str):
        self._tokens.pop(hashlib.sha256(token.encode()).hexdigest(), None)

    def login(self, secret: str) -> str:
        now = time.monotonic()
        self._login_attempts = [stamp for stamp in self._login_attempts if stamp > now - 60]
        if len(self._login_attempts) >= 20:
            raise HTTPException(429, "too many local login attempts")
        expected = os.environ.get("ORALIA_ADMIN_SECRET", "")
        if len(expected) < 24:
            raise HTTPException(503, "local administrator credential is not configured")
        if not hmac.compare_digest(secret.encode(), expected.encode()):
            self._login_attempts.append(now)
            _LOG.info("access_denied", outcome=401, category="local_credential")
            raise HTTPException(401, "invalid local credential")
        return self.issue("teacher")


def request_tokens(request: Request) -> list[str]:
    header = request.headers.get("authorization", "")
    return [
        value
        for value in [
            header[7:] if header.startswith("Bearer ") else "",
            request.cookies.get(request.app.state.local_access.cookie_names[0], ""),
            request.cookies.get(request.app.state.local_access.cookie_names[1], ""),
        ]
        if value
    ]


def _local_transport(request: Request):
    allow_lan = os.environ.get("ORALIA_ALLOW_LAN") == "1"
    hostname = request.url.hostname or ""
    allowed = {"localhost", "127.0.0.1", "::1", "testserver", "test"}
    if hostname not in allowed and not allow_lan:
        raise HTTPException(403, "local host required")
    client_host = request.client.host if request.client else ""
    if client_host not in {"testclient", ""}:
        try:
            if not ipaddress.ip_address(client_host).is_loopback and not allow_lan:
                raise HTTPException(403, "local access required")
        except ValueError:
            raise HTTPException(403, "local access required") from None
    origin = request.headers.get("origin")
    if origin:
        parsed = urlparse(origin)
        trusted = {
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            os.environ.get("ORALIA_LOCAL_UI_ORIGIN", ""),
            str(request.base_url).rstrip("/"),
        }
        if origin not in trusted or parsed.hostname not in allowed and not allow_lan:
            raise HTTPException(403, "request origin denied")


async def access_guard(request: Request, call_next):
    if not request.url.path.startswith("/api/"):
        return await call_next(request)
    try:
        _local_transport(request)
        path = request.url.path
        public = (
            path in {"/api/v1/auth/login", "/api/v1/auth/logout"}
            or path == "/api/v1/sessions"
            and request.method == "POST"
            or re.fullmatch(r"/api/v1/activities/[^/]+", path)
            and request.method == "GET"
        )
        if public:
            response = await call_next(request)
            response.headers["Cache-Control"] = "no-store"
            return response
        manager = request.app.state.local_access
        grants = [grant for token in request_tokens(request) if (grant := manager.resolve(token))]
        # Only the explicit demo entrypoint installs this grant after checking its
        # marked DB boundary. Ordinary create_app never enables anonymous teaching.
        demo_grant = getattr(request.app.state, "demo_teacher_grant", None)
        if demo_grant is not None and demo_grant.expires_at > time.monotonic():
            grants.append(demo_grant)
        match = _SESSION_PATH.match(path)
        suffix = match.group(2) if match else None
        legacy_teacher = bool(match and path.startswith("/api/v1/sessions/") and suffix in {None, "trace"})
        if match and not legacy_teacher:
            grant = next(
                (g for g in grants if g.role == "participant" and g.session_id == match.group(1)), None
            )
            if grant is None and suffix == "content" and request.method == "DELETE":
                grant = next((g for g in grants if g.role == "teacher"), None)
            if grant is None:
                raise HTTPException(403 if grants else 401, "session access denied")
        else:
            grant = next((g for g in grants if g.role == "teacher"), None)
            if grant is None:
                if path.startswith("/api/v1/auth/") and grants:
                    grant = grants[0]
                else:
                    if len(os.environ.get("ORALIA_ADMIN_SECRET", "")) < 24:
                        raise HTTPException(503, "local administrator credential is not configured")
                    raise HTTPException(403 if grants else 401, "teacher access required")
        request.state.access_grant = grant
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response
    except HTTPException as exc:
        _LOG.info("access_denied", outcome=exc.status_code, category="local_authorization")
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.detail}, headers={"Cache-Control": "no-store"}
        )
