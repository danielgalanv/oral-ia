"""Start an isolated API with only the foreign-key fixtures E2E cannot create by API."""

from __future__ import annotations

import asyncio
import os
import time
import uuid
from pathlib import Path

import uvicorn

from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import reset_engine_for_tests

COURSE_ID = "30000000-0000-0000-0000-000000000001"
RETENTION_POLICY_ID = "30000000-0000-0000-0000-000000000002"
DB_PATH = Path(".e2e_governance.db").resolve()


def main() -> None:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["ORALIA_LOCAL_UI_ORIGIN"] = "http://127.0.0.1:5175"
    os.environ["ORALIA_ADMIN_SECRET"] = "fictional-e2e-installation-secret-005"
    # Real-model inference has its own optional marker; this harness is deterministic.
    os.environ.pop("ORALIA_OLLAMA_MODEL", None)
    for path in (DB_PATH, Path(f"{DB_PATH}-wal"), Path(f"{DB_PATH}-shm")):
        path.unlink(missing_ok=True)
    db_url = f"sqlite:///{DB_PATH.as_posix()}"
    os.environ["ORALIA_DB_URL"] = db_url
    # A freshly created SQL database must not share a previous run's vector index.
    # Keep old test artifacts; this run owns a new directory, never habitual data.
    os.environ["ORALIA_VECTOR_STORE_PATH"] = str(
        DB_PATH.parent / ".claude-scratch" / f"e2e-vectors-{uuid.uuid4().hex}"
    )
    engine = reset_engine_for_tests(db_url)
    Base.metadata.create_all(engine)

    from sqlalchemy.orm import Session

    with Session(engine) as db:
        db.add(
            models.Course(
                id=COURSE_ID,
                name="Curso E2E autoestudio",
                subject_code="E2E003",
            )
        )
        db.add(
            models.RetentionPolicy(
                id=RETENTION_POLICY_ID,
                content_scope="session",
                retention_days=30,
                access_scope="profesor",
                purge_rule="manual",
            )
        )
        db.commit()

    from oralia.interfaces.api.app import app

    @app.get("/e2e-fixture")
    def e2e_fixture():
        return {"fixture": "oralia-owned-e2e"}

    @app.middleware("http")
    async def measured_material_delivery(request, call_next):
        # Test harness only: pass the original multipart/auth/ingestion unchanged.
        # Delay delivery AFTER the real endpoint has produced its response.
        started = time.monotonic()
        response = await call_next(request)
        if (
            request.method == "POST"
            and request.url.path == "/api/v1/materials/documents"
            and request.headers.get("x-oralia-e2e-delivery") == "slow"
        ):
            response.headers["x-oralia-e2e-ingest-ms"] = str(round((time.monotonic() - started) * 1000))
            response.headers["x-oralia-e2e-delay-ms"] = "16000"
            await asyncio.sleep(16)
        return response

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8005,
        reload=False,
    )


if __name__ == "__main__":
    main()
