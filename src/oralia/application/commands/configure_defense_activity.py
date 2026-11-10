"""Create or update an oral-defense configuration before first use."""

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from sqlalchemy.orm import Session as SASession

from oralia.application.services.defense_retention_service import require_finite_retention
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.infrastructure.db import models


class ActivityNotFound(ValueError):
    pass


class ActivityConfigurationImmutable(ValueError):
    pass


class MissingQuestionSource(ValueError):
    pass


class DefenseActivityConfigInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    initial_questions: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    difficulty_hint: str = "media"
    voice_input_allowed: StrictBool = False
    voice_output_allowed: StrictBool = False
    summary_authorized: StrictBool = False
    transcript_retention_authorized: StrictBool = False
    output_authorization_policy: OutputAuthorizationPolicy | None = None


def get_defense_config(db: SASession, activity_configuration_id: str) -> models.DefenseActivityConfig | None:
    return (
        db.query(models.DefenseActivityConfig)
        .filter(models.DefenseActivityConfig.activity_configuration_id == activity_configuration_id)
        .one_or_none()
    )


def _has_authorized_material(db: SASession, activity_id: str) -> bool:
    documents = db.query(models.MaterialDocument.activity_configuration_ids).filter(
        models.MaterialDocument.status == "active"
    )
    return any(activity_id in (ids or []) for (ids,) in documents)


def configure_defense_activity(
    db: SASession, activity_configuration_id: str, data: DefenseActivityConfigInput
) -> models.DefenseActivityConfig:
    activity = db.get(models.ActivityConfiguration, activity_configuration_id)
    if activity is None:
        raise ActivityNotFound(f"activity {activity_configuration_id} not found")
    if activity.immutable_since is not None:
        raise ActivityConfigurationImmutable(
            f"activity {activity_configuration_id} configuration is immutable"
        )
    if data.transcript_retention_authorized:
        require_finite_retention(db, activity)
    questions = [question for question in data.initial_questions if question.strip()]
    if not questions and not _has_authorized_material(db, activity_configuration_id):
        raise MissingQuestionSource("an initial question or authorized material is required")
    if data.difficulty_hint not in {"baja", "media", "alta"}:
        raise ValueError("difficulty_hint must be baja, media, or alta")
    if (data.voice_input_allowed or data.voice_output_allowed) and not _voice_configured(
        input_enabled=data.voice_input_allowed,
        output_enabled=data.voice_output_allowed,
    ):
        raise ValueError("local speech model/voice is not configured")
    existing = get_defense_config(db, activity_configuration_id)
    values = data.model_dump()
    policy = values.pop("output_authorization_policy")
    values["initial_questions"] = questions
    if policy is not None:
        parsed_policy = OutputAuthorizationPolicy.model_validate(policy)
        raw_policy = canonical_policy_json(parsed_policy)
        activity.output_authorization_policy_json = raw_policy
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(raw_policy)
        activity.general_knowledge_allowed = parsed_policy.general_knowledge_allowed
        db.add(activity)
    if existing is None:
        existing = models.DefenseActivityConfig(activity_configuration_id=activity_configuration_id, **values)
    else:
        for name, value in values.items():
            setattr(existing, name, value)
    db.add(existing)
    db.flush()
    return existing


def _voice_configured(*, input_enabled: bool, output_enabled: bool) -> bool:
    from oralia.infrastructure.speech.config import settings

    return (not input_enabled or settings().stt_model is not None) and (
        not output_enabled or settings().tts_voice is not None
    )


__all__ = [
    "ActivityConfigurationImmutable",
    "ActivityNotFound",
    "DefenseActivityConfigInput",
    "MissingQuestionSource",
    "configure_defense_activity",
    "get_defense_config",
]
