"""Read-only classification of self-study retention authorization (FR-028a)."""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models

_STATES = (
    "authorized_expiring",
    "not_authorized_purge_eligible",
    "undecided_preexisting",
    "invalid_authorized_without_policy",
)


def self_study_retention_audit(db: SASession) -> dict[str, list[dict[str, str | int]]]:
    report: dict[str, list[dict[str, str | int]]] = {state: [] for state in _STATES}
    configurations = db.query(models.SelfStudyActivityConfig).all()

    for config in configurations:
        activity = db.get(models.ActivityConfiguration, config.activity_configuration_id)
        policy = db.get(models.RetentionPolicy, activity.retention_policy_id) if activity else None
        finite_policy = policy is not None and policy.retention_days is not None

        if config.retention_authorized is None:
            state = "undecided_preexisting"
        elif config.retention_authorized is False:
            state = "not_authorized_purge_eligible"
        elif finite_policy:
            state = "authorized_expiring"
        else:
            state = "invalid_authorized_without_policy"

        sessions = (
            db.query(func.count(models.Session.id))
            .filter(
                models.Session.activity_configuration_id == config.activity_configuration_id,
                models.Session.ended_at.isnot(None),
            )
            .scalar()
        )
        report[state].append(
            {
                "activity_configuration_id": config.activity_configuration_id,
                "sessions": int(sessions or 0),
            }
        )

    return report
