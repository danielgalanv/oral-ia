"""FR-001, FR-002: create/version ActivityConfiguration; enforce immutability once used."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session as SASession

from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


class ActivityAlreadyImmutable(ValueError):
    """FR-002: raised when attempting to edit an ActivityConfiguration already in use."""


class GeneralKnowledgePolicyMismatch(ValueError):
    """Raised when configuration and policy disagree on general-knowledge permission."""


class ActivitySuccessionNotAllowed(ValueError):
    """Raised when a source cannot be succeeded without rewriting history."""


class ActivityNotFound(LookupError):
    """Raised when an administrative succession source does not exist."""


def _validated_policy_storage(
    policy: OutputAuthorizationPolicy,
    *,
    general_knowledge_allowed: bool,
) -> tuple[str, str]:
    if policy.general_knowledge_allowed is not general_knowledge_allowed:
        raise GeneralKnowledgePolicyMismatch(
            "activity and output policy general_knowledge_allowed values must match"
        )
    policy_json = canonical_policy_json(policy)
    return policy_json, canonical_policy_sha256(policy_json)


def replace_activity_output_authorization_policy(
    db: SASession,
    activity: models.ActivityConfiguration,
    policy: OutputAuthorizationPolicy,
) -> None:
    """Replace a draft policy while rejecting every write after first use."""

    if activity.immutable_since is not None:
        raise ActivityAlreadyImmutable(
            f"activity family {activity.family_id} version {activity.version} is immutable"
        )
    policy_json, policy_sha256 = _validated_policy_storage(
        policy,
        general_knowledge_allowed=activity.general_knowledge_allowed,
    )
    activity.output_authorization_policy_json = policy_json
    activity.output_authorization_policy_sha256 = policy_sha256
    db.add(activity)
    db.flush()


class ActivityConfigurationInput(BaseModel):
    course_id: str
    name: str
    subject: str
    objective: str
    mode: str
    language: str
    max_turns: int
    max_duration_seconds: int
    retention_policy_id: str
    general_knowledge_allowed: bool = False
    output_authorization_policy: OutputAuthorizationPolicy
    required_agent_ids: list[str] = Field(default_factory=list)
    optional_agent_ids: list[str] = Field(default_factory=list)


class ActivitySuccessionInput(BaseModel):
    output_authorization_policy: OutputAuthorizationPolicy


def create_activity(
    db: SASession,
    data: ActivityConfigurationInput,
    *,
    family_id: str | None = None,
) -> models.ActivityConfiguration:
    """Create a new ActivityConfiguration version.

    If ``family_id`` is omitted, a brand-new activity family is started at version 1.
    If provided, the caller is explicitly editing a draft — this MUST fail (FR-002) if
    the latest version in that family is already immutable.
    """

    policy_json, policy_sha256 = _validated_policy_storage(
        data.output_authorization_policy,
        general_knowledge_allowed=data.general_knowledge_allowed,
    )

    version = 1
    if family_id is not None:
        latest = (
            db.query(models.ActivityConfiguration)
            .filter(models.ActivityConfiguration.family_id == family_id)
            .order_by(models.ActivityConfiguration.version.desc())
            .first()
        )
        if latest is not None:
            if latest.immutable_since is not None:
                raise ActivityAlreadyImmutable(
                    f"activity family {family_id} version {latest.version} is immutable; "
                    "create a new version instead of editing in place"
                )
            version = latest.version + 1

    activity = models.ActivityConfiguration(
        family_id=family_id or str(uuid.uuid4()),
        version=version,
        course_id=data.course_id,
        name=data.name,
        subject=data.subject,
        objective=data.objective,
        mode=data.mode,
        language=data.language,
        max_turns=data.max_turns,
        max_duration_seconds=data.max_duration_seconds,
        general_knowledge_allowed=data.general_knowledge_allowed,
        required_agent_ids=data.required_agent_ids,
        optional_agent_ids=data.optional_agent_ids,
        retention_policy_id=data.retention_policy_id,
        output_authorization_policy_json=policy_json,
        output_authorization_policy_sha256=policy_sha256,
        immutable_since=None,
    )
    db.add(activity)
    db.flush()
    return activity


def mark_immutable_if_needed(db: SASession, activity: models.ActivityConfiguration) -> None:
    """Called the first time a Session references this ActivityConfiguration (FR-002)."""
    if activity.immutable_since is None:
        activity.immutable_since = utcnow()
        db.add(activity)
        db.flush()


def succeed_activity_configuration(
    db: SASession,
    source_activity_id: str,
    data: ActivitySuccessionInput,
) -> models.ActivityConfiguration:
    """Create a policy-bearing successor without modifying the immutable source."""

    source = db.get(models.ActivityConfiguration, source_activity_id)
    if source is None:
        raise ActivityNotFound(f"activity configuration {source_activity_id} not found")
    if source.immutable_since is None:
        raise ActivitySuccessionNotAllowed("only an immutable activity can be succeeded")

    latest = (
        db.query(models.ActivityConfiguration)
        .filter(models.ActivityConfiguration.family_id == source.family_id)
        .order_by(models.ActivityConfiguration.version.desc())
        .first()
    )
    if latest is None or latest.id != source.id:
        raise ActivitySuccessionNotAllowed("only the latest activity version can be succeeded")

    policy_json, policy_sha256 = _validated_policy_storage(
        data.output_authorization_policy,
        general_knowledge_allowed=source.general_knowledge_allowed,
    )
    successor = models.ActivityConfiguration(
        family_id=source.family_id,
        version=source.version + 1,
        course_id=source.course_id,
        name=source.name,
        subject=source.subject,
        objective=source.objective,
        mode=source.mode,
        language=source.language,
        max_turns=source.max_turns,
        max_duration_seconds=source.max_duration_seconds,
        general_knowledge_allowed=source.general_knowledge_allowed,
        required_agent_ids=list(source.required_agent_ids),
        optional_agent_ids=list(source.optional_agent_ids),
        retention_policy_id=source.retention_policy_id,
        output_authorization_policy_json=policy_json,
        output_authorization_policy_sha256=policy_sha256,
        immutable_since=None,
    )
    db.add(successor)
    db.flush()
    return successor


def get_activity(db: SASession, activity_id: str) -> models.ActivityConfiguration | None:
    return db.get(models.ActivityConfiguration, activity_id)
