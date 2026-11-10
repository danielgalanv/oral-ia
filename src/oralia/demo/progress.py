"""Bounded, truthful console progress; no background work except status messages."""

from __future__ import annotations

import sys
import threading
import time
import traceback
from contextlib import contextmanager

from oralia.demo.resources import DemoError

STAGES = {
    "dependencias": (
        "Comprobación de dependencias y puertos",
        "Revise dependencias y elija puertos libres explícitamente; no se cierra ningún proceso ajeno.",
    ),
    "embeddings": (
        "Comprobación o carga de embeddings locales",
        "Prepare los recursos locales o use -TextOnly, sin fuentes; no se descargan modelos.",
    ),
    "esquema": ("Comprobación del esquema demo", "Revise el esquema y el origen de los datos demo."),
    "preparacion": (
        "Preparación de datos e índice demo",
        "Revise .oralia-demo/logs/prepare.log y los recursos locales antes de reintentar.",
    ),
    "texto": (
        "Preparación de datos demo (TextOnly)",
        "Revise .oralia-demo/logs/prepare.log antes de reintentar.",
    ),
    "api": ("Inicio de API", "Revise .oralia-demo/logs/api.log y el puerto API elegido."),
    "interfaz": (
        "Inicio de interfaz",
        "Revise .oralia-demo/logs/web.log y el puerto web elegido.",
    ),
    "espera": (
        "Espera de disponibilidad",
        "Revise .oralia-demo/logs/api.log y web.log; no se ha cambiado ningún puerto.",
    ),
}


class Progress:
    def __init__(self, *, stream=None, interval=5, paths=None):
        self.stream = stream if stream is not None else sys.stderr
        self.interval = interval
        self.paths = paths
        self._secrets = []

    def protect(self, secret):
        if secret:
            self._secrets.append(secret)

    def clean(self, message):
        for secret in self._secrets:
            message = message.replace(secret, "[OCULTO]")
        return message

    def say(self, message):
        print(self.clean(message), file=self.stream, flush=True)

    def diagnostic(self, exc):
        # Do not create directories outside a validated demo boundary on errors.
        if self.paths is None:
            return
        try:
            self.paths.validate()
            detail = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            with (self.paths.root / "logs/startup.log").open("a", encoding="utf-8") as log:
                log.write(self.clean(detail))
        except (DemoError, OSError, ValueError):
            pass

    @contextmanager
    def stage(self, key, *, completion=None, note=""):
        label, action = STAGES[key]
        started = time.monotonic()
        finished = threading.Event()
        self.say(f"[INICIO] {label}." + (f" {note}" if note else ""))

        def heartbeat():
            while not finished.wait(self.interval):
                self.say(
                    f"[ESPERA] {label}: {time.monotonic() - started:.0f}s transcurridos. "
                    "La carga inicial puede tardar; la operación sigue en curso."
                )

        reporter = threading.Thread(target=heartbeat, name="demo-progress", daemon=True)
        reporter.start()
        try:
            try:
                yield
            finally:
                finished.set()
                reporter.join()
        except KeyboardInterrupt:
            self.say(f"[CANCELADO] {label}. Se limpiarán únicamente los procesos propios.")
            raise
        except Exception as exc:
            self.diagnostic(exc)
            cause = str(exc) if isinstance(exc, DemoError) else f"causa no determinada ({type(exc).__name__})"
            self.say(f"[FALLO] {label}: {cause} {action}")
            raise
        else:
            self.say(f"[OK] {label}. {completion or 'Completada.'}")
