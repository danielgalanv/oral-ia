"""FR-002, FR-002a: create/update SelfStudyActivityConfig for an activity.

Only creatable/updatable while ActivityConfiguration.immutable_since is null — same
pattern as ActivityConfiguration's own immutability (Feature 001, create_activity.py,
reused unchanged, research.md §7 of Feature 003)."""

from __future__ import annotations

from pydantic import BaseModel, Field, StrictBool
from sqlalchemy.orm import Session as SASession

from oralia.infrastructure.db import models

CANONICAL_MODES = (
    "doubt_resolution",
    "guided_explanation",
    "practice_questions",
    "presentation_preparation",
    "concept_review",
)


class ActivityNotFound(ValueError):
    pass


class EmptyEnabledModes(ValueError):
    """FR-002a: enabled_modes MUST NOT be empty."""


class ActivityConfigurationImmutable(ValueError):
    """research.md §7: no create/update once ActivityConfiguration.immutable_since is set."""


class SelfStudyActivityConfigInput(BaseModel):
    enabled_modes: list[str] = Field(min_length=1)
    summary_authorized: bool = False
    practice_reveals_solution: bool = False
    retention_authorized: StrictBool | None = None


def get_self_study_config(
    db: SASession, activity_configuration_id: str
) -> models.SelfStudyActivityConfig | None:
    return (
        db.query(models.SelfStudyActivityConfig)
        .filter(models.SelfStudyActivityConfig.activity_configuration_id == activity_configuration_id)
        .one_or_none()
    )


def configure_self_study_activity(
    db: SASession, activity_configuration_id: str, data: SelfStudyActivityConfigInput
) -> models.SelfStudyActivityConfig:
    activity = db.get(models.ActivityConfiguration, activity_configuration_id)
    if activity is None:
        raise ActivityNotFound(f"activity {activity_configuration_id} not found")

    if not data.enabled_modes:
        raise EmptyEnabledModes("enabled_modes MUST NOT be empty (FR-002a)")

    if activity.immutable_since is not None:
        raise ActivityConfigurationImmutable(
            f"activity {activity_configuration_id} configuration is immutable since "
            f"{activity.immutable_since}"
        )

    existing = get_self_study_config(db, activity_configuration_id)
    if existing is not None:
        existing.enabled_modes = data.enabled_modes
        existing.summary_authorized = data.summary_authorized
        existing.practice_reveals_solution = data.practice_reveals_solution
        existing.retention_authorized = data.retention_authorized
        db.add(existing)
        db.flush()
        return existing

    config = models.SelfStudyActivityConfig(
        activity_configuration_id=activity_configuration_id,
        enabled_modes=data.enabled_modes,
        summary_authorized=data.summary_authorized,
        practice_reveals_solution=data.practice_reveals_solution,
        retention_authorized=data.retention_authorized,
    )
    db.add(config)
    db.flush()
    return config
