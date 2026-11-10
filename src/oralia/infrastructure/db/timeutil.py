"""SQLite has no native datetime type — it round-trips ``DateTime(timezone=True)``
values as tz-naive. To avoid "can't subtract offset-naive and offset-aware datetimes"
bugs when comparing a freshly-created value against one read back from the DB, every
persisted timestamp in this codebase is naive UTC, produced only via ``utcnow()``.
"""

from __future__ import annotations

from datetime import UTC, datetime


def utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)
