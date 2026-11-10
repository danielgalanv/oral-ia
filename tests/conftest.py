from __future__ import annotations

import os
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.infrastructure.db import models  # noqa: F401
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine
from tests.t090_policy_helpers import minimal_output_policy_columns

# Feature 002: never hit the network for embeddings during tests — the model is loaded
# once (cached) and this also works around an unrelated transformers/HF-Hub bug (see
# sentence_transformer_adapter.py docstring).
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


@pytest.fixture(autouse=True)
def _isolated_vector_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Every test gets its own ChromaDB directory (mirrors the per-test SQLite isolation
    below) so materials tests never see another test's indexed fragments."""

    monkeypatch.setenv("ORALIA_VECTOR_STORE_PATH", str(tmp_path / "vector_store"))

    # PersistentClient owns a native system/cache until close(); retaining every
    # temporary client across a large suite leaks systems and file handles. Track
    # only this test's clients. Never clear the global cache or stop foreign paths.
    import chromadb

    factory = chromadb.PersistentClient
    owned = []

    def test_client(*args, **kwargs):
        client = factory(*args, **kwargs)
        path = kwargs.get("path", args[0] if args else "./chroma")
        if Path(path).resolve().is_relative_to(tmp_path.resolve()):
            owned.append(client)
        return client

    monkeypatch.setattr(chromadb, "PersistentClient", test_client)
    yield
    for client in reversed(owned):
        client.close()


@pytest.fixture()
def db_engine(tmp_path: Path):
    db_path = tmp_path / f"test_{uuid.uuid4().hex}.db"
    engine = build_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(db_engine) -> SASession:
    Session = sessionmaker(bind=db_engine, expire_on_commit=False)
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def app_client(db_engine, monkeypatch):
    """A TestClient wired to an isolated per-test SQLite DB via dependency override."""
    from oralia.interfaces.api.app import create_app
    from oralia.interfaces.api.deps.db import get_db

    Session = sessionmaker(bind=db_engine, expire_on_commit=False)

    def _override_get_db():
        db = Session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    monkeypatch.setenv("ORALIA_ADMIN_SECRET", "fictional-installation-secret-005")
    app = create_app()
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        assert (
            client.post(
                "/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"}
            ).status_code
            == 200
        )
        client.__db_sessionmaker__ = Session  # type: ignore[attr-defined]
        yield client


MATERIALS_FIXTURES_DIR = Path(__file__).parent / "fixtures" / "materials"


@pytest.fixture()
def seeded_course(app_client) -> str:
    """Creates a bare Course for materials tests that don't need an ActivityConfiguration."""

    Session = app_client.__db_sessionmaker__
    db = Session()
    course = models.Course(name="Curso materiales", subject_code="MAT101")
    db.add(course)
    db.commit()
    course_id = course.id
    db.close()
    return course_id


@pytest.fixture()
def seeded_activity(app_client) -> str:
    """Creates a Course/RetentionPolicy/ActivityConfiguration; returns the activity id."""

    Session = app_client.__db_sessionmaker__
    db = Session()
    course = models.Course(name="Curso demo", subject_code="DEMO101")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db.add_all([course, policy])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Actividad demo",
        subject="Demo",
        objective="probar el flujo de turno",
        mode="texto",
        language="es",
        max_turns=10,
        max_duration_seconds=900,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(),
    )
    db.add(activity)
    db.commit()
    activity_id = activity.id
    db.close()
    return activity_id


@pytest.fixture()
def self_study_activity(app_client) -> dict:
    """Feature 003: Course/RetentionPolicy/ActivityConfiguration for self-study tests
    (general_knowledge_allowed=False by default — tests override via the HTTP API when
    they need general knowledge on). No SelfStudyActivityConfig/materials yet — tests
    add those explicitly so each can control enabled_modes/materials independently.

    Returns ``{"activity_id": ..., "course_id": ...}`` — tests need both (course_id to
    upload materials, activity_id for sessions/config)."""

    Session = app_client.__db_sessionmaker__
    db = Session()
    course = models.Course(name="Curso autoestudio", subject_code="AUT101")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db.add_all([course, policy])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Autoestudio demo",
        subject="Demo",
        objective="practicar autoestudio",
        mode="self_study",
        language="es",
        max_turns=10,
        max_duration_seconds=1800,
        general_knowledge_allowed=False,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(),
    )
    db.add(activity)
    db.commit()
    result = {"activity_id": activity.id, "course_id": course.id}
    db.close()
    return result
