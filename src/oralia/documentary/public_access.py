"""Acceso de alumnos por túnel (Cloudflare Access): identidad, superficie y límites. Desactivado si no hay hosts públicos.

Variables: ORALIA_PUBLIC_HOSTS (hosts públicos separados por comas), ORALIA_ACCESS_TEAM (p. ej. equipo.cloudflareaccess.com),
ORALIA_ACCESS_AUD (audiencia de la aplicación), ORALIA_EMAIL_SUFFIX (por defecto @alumnos.upm.es).
Las peticiones por host local siguen siendo las del docente; solo las que llegan por un host público quedan restringidas.
"""

import base64
import json
import os
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi import HTTPException

BLOCKED = ("/api/v1/retrieval", "/tecnica")  # además de pages/original/preview, ver blocked()
TURN_PATH = "/api/v1/study-lab/turn"
HEADER = "cf-access-jwt-assertion"


def _b64(data):
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


class PublicAccess:
    def __init__(self, hosts, team, audience, suffix="@alumnos.upm.es", fetch_keys=None, clock=time.time,
                 turns_per_minute=6, max_queue=12):
        self.hosts, self.team, self.audience = set(hosts), team, audience
        self.suffix = suffix.lower()
        self.fetch_keys, self.clock = fetch_keys or self._download_keys, clock
        self.turns_per_minute, self.max_queue = turns_per_minute, max_queue
        self._keys, self._keys_at = {}, 0.0
        self.by_email, self.email_of = {}, {}  # email -> token, token -> email
        self.in_flight, self.recent = {}, {}  # token -> bool, token -> [timestamps]
        self.enter_log = {}

    @classmethod
    def from_env(cls):
        hosts = [h.strip().lower() for h in os.environ.get("ORALIA_PUBLIC_HOSTS", "").split(",") if h.strip()]
        if not hosts:
            return None
        team, audience = os.environ.get("ORALIA_ACCESS_TEAM", ""), os.environ.get("ORALIA_ACCESS_AUD", "")
        if not team or not audience:
            raise ValueError("ORALIA_PUBLIC_HOSTS requiere ORALIA_ACCESS_TEAM y ORALIA_ACCESS_AUD")
        return cls(hosts, team, audience, os.environ.get("ORALIA_EMAIL_SUFFIX", "@alumnos.upm.es"))

    def is_public(self, request):
        return (request.url.hostname or "").lower() in self.hosts

    def check_transport(self, request):
        """Host público permitido, cliente local (cloudflared) y origen igual al host público."""
        host = (request.url.hostname or "").lower()
        client = request.client.host if request.client else ""
        if client not in {"127.0.0.1", "::1", "testclient", ""}:
            raise HTTPException(403, "local access required")
        origin = request.headers.get("origin")
        if origin and host in self.hosts and origin.rstrip("/") != f"https://{host}":
            raise HTTPException(403, "request origin denied")

    @staticmethod
    def blocked(path):
        return path in BLOCKED or (path.startswith("/api/v1/documentary/") and path.count("/") >= 5)
    # --- identidad -------------------------------------------------------------------------------------------
    def _download_keys(self):
        import httpx

        response = httpx.get(f"https://{self.team}/cdn-cgi/access/certs", timeout=10)
        response.raise_for_status()
        return response.json()["keys"]

    def _key(self, kid):
        if kid not in self._keys or self.clock() - self._keys_at > 3600:
            if self.clock() - self._keys_at > 60 or kid not in self._keys:
                self._keys = {k["kid"]: k for k in self.fetch_keys()}
                self._keys_at = self.clock()
        jwk = self._keys.get(kid)
        if jwk is None:
            raise HTTPException(401, "Identidad no válida")
        return rsa.RSAPublicNumbers(
            int.from_bytes(_b64(jwk["e"]), "big"), int.from_bytes(_b64(jwk["n"]), "big")
        ).public_key()

    def verify(self, token):
        """Devuelve el correo si el JWT de Access es válido (firma RS256, audiencia, vigencia, correo del dominio)."""
        try:
            head, body, signature = token.split(".")
            header, claims = json.loads(_b64(head)), json.loads(_b64(body))
            if header.get("alg") != "RS256":
                raise ValueError("alg")
            self._key(header.get("kid")).verify(
                _b64(signature), f"{head}.{body}".encode(), padding.PKCS1v15(), hashes.SHA256()
            )
            audience = claims.get("aud")
            if self.audience not in (audience if isinstance(audience, list) else [audience]):
                raise ValueError("aud")
            if claims.get("exp", 0) <= self.clock() or claims.get("iss") != f"https://{self.team}":
                raise ValueError("exp/iss")
            email = str(claims.get("email", "")).lower()
            if not email.endswith(self.suffix) or email == self.suffix:
                raise ValueError("email")
            return email
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(401, "Identidad no válida") from None

    def identity(self, request):
        return self.verify(request.headers.get(HEADER, ""))

    # --- concesiones y límites ---------------------------------------------------------------------------------
    def register(self, email, token, manager):
        """Un alumno, una concesión: la anterior del mismo correo se revoca."""
        now = self.clock()
        log = [t for t in self.enter_log.get(email, []) if t > now - 60]
        if len(log) >= 10:
            raise HTTPException(429, "Demasiados accesos; espera un minuto")
        self.enter_log[email] = log + [now]
        old = self.by_email.get(email)
        if old and old != token:
            manager.revoke(old)
            self.forget(old)
        self.by_email[email], self.email_of[token] = token, email

    def forget(self, token):
        email = self.email_of.pop(token, None)
        if email and self.by_email.get(email) == token:
            del self.by_email[email]
        self.in_flight.pop(token, None)
        self.recent.pop(token, None)

    def admit_turn(self, token):
        """Un turno en curso por alumno, N por minuto y cola global acotada. Devuelve la función que libera."""
        if self.in_flight.get(token):
            raise HTTPException(429, "Ya tienes una pregunta en curso; espera a que termine")
        now = self.clock()
        recent = [t for t in self.recent.get(token, []) if t > now - 60]
        if len(recent) >= self.turns_per_minute:
            raise HTTPException(429, "Demasiadas preguntas seguidas; espera un momento")
        if sum(1 for busy in self.in_flight.values() if busy) >= self.max_queue:
            raise HTTPException(503, "El servidor está ocupado; vuelve a intentarlo en un minuto")
        self.recent[token] = recent + [now]
        self.in_flight[token] = True
        return lambda: self.in_flight.__setitem__(token, False)
