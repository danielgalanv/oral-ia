"""SQLite (WAL mode) engine factory, kept behind this module so the storage engine can
be swapped later without touching domain/application code (Constitution Principio XI).
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

DEFAULT_DB_URL = "sqlite:///./oralia.db"


def _enable_wal(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def build_engine(db_url: str | None = None) -> Engine:
    url = db_url or os.environ.get("ORALIA_DB_URL", DEFAULT_DB_URL)
    engine = create_engine(url, connect_args={"check_same_thread": False} if "sqlite" in url else {})
    if url.startswith("sqlite"):
        event.listen(engine, "connect", _enable_wal)
    return engine


_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = build_engine()
    return _engine


def get_sessionmaker() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _SessionLocal


@contextmanager
def session_scope() -> Iterator[SASession]:
    session = get_sessionmaker()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def reset_engine_for_tests(db_url: str) -> Engine:
    """Rebuild the module-level engine/sessionmaker against a fresh URL (used by tests)."""
    global _engine, _SessionLocal
    _engine = build_engine(db_url)
    _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)
    return _engine
