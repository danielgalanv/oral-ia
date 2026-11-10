"""Explicit teacher access for the disposable, loopback-only demo launcher."""

import os
import time

from oralia.demo.resources import DemoError
from oralia.interfaces.api.deps.local_access import AccessGrant


def enable_demo_teacher_access(app, paths):
    paths.validate()
    if (
        os.environ.get("ORALIA_DB_URL") != paths.db_url
        or os.environ.get("ORALIA_ALLOW_LAN") != "0"
        or os.environ.get("ORALIA_COOKIE_NAMESPACE") != "oralia_demo"
    ):
        raise DemoError("Acceso docente demo requiere base aislada y acceso exclusivamente local.")
    app.state.demo_teacher_grant = AccessGrant("teacher", None, time.monotonic() + 86400)
