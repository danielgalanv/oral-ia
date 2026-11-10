from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models


def create(
    db: SASession,
    *,
    content_scope: str,
    access_scope: str,
    purge_rule: str,
    retention_days: int | None = None,
    version: int = 1,
) -> models.RetentionPolicy:
    policy = models.RetentionPolicy(
        content_scope=content_scope,
        access_scope=access_scope,
        purge_rule=purge_rule,
        retention_days=retention_days,
        version=version,
    )
    db.add(policy)
    db.flush()
    return policy


def get(db: SASession, policy_id: str) -> models.RetentionPolicy | None:
    return db.get(models.RetentionPolicy, policy_id)
