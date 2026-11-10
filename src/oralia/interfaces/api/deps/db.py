from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db.engine import get_sessionmaker


def get_db() -> Iterator[SASession]:
    db = get_sessionmaker()()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
