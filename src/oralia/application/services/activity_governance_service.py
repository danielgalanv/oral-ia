"""Human publication of immutable activity versions, not autonomous policy edits."""

from __future__ import annotations

import json
import os
import uuid
from copy import deepcopy

from sqlalchemy import func
from sqlalchemy.orm import Session

from oralia.application.commands.configure_defense_activity import (
    DefenseActivityConfigInput,
    configure_defense_activity,
)
from oralia.application.commands.configure_self_study_activity import (
    SelfStudyActivityConfigInput,
    configure_self_study_activity,
)
from oralia.application.commands.create_activity import ActivityConfigurationInput, create_activity
from oralia.domain.policies.output_authorization_policy import OutputAuthorizationPolicy
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow

COMPOSITIONS = {
    "oral_defense": [
        "material-retriever",
        "followup-question-agent",
        "practice-question-agent",
        "grounding-verifier",
        "coherence-verifier",
        "constitutional-control",
        "safe-fallback",
    ],
    "self_study": [
        "study-intent-interpreter",
        "solution-non-disclosure-verifier",
        "material-retriever",
        "response-generator",
        "practice-question-agent",
        "grounding-verifier",
        "coherence-verifier",
        "constitutional-control",
        "safe-fallback",
    ],
}


def available_models() -> list[str]:
    model = os.environ.get("ORALIA_OLLAMA_MODEL")
    return ["deterministic", "guided_controlled", *([f"ollama:{model}"] if model else [])]


def _validate_selection(db: Session, activity, model_id: str, materials: list):
    if not isinstance(materials, list) or len(materials) > 100:
        raise ValueError("select at most 100 material versions")
    if model_id not in available_models():
        raise ValueError("selected model is not locally configured")
    if activity.mode not in COMPOSITIONS:
        raise ValueError("managed mode must be self_study or oral_defense")
    if activity.max_turns < 1 or activity.max_duration_seconds < 1:
        raise ValueError("activity limits must be positive")
    allowed_agents = set(COMPOSITIONS[activity.mode])
    if (
        activity.optional_agent_ids
        or activity.required_agent_ids
        and set(activity.required_agent_ids) != allowed_agents
    ):
        raise ValueError("select a complete available composition; mandatory controls cannot be omitted")
    for ref in materials:
        if not isinstance(ref, dict) or set(ref) != {"document_id", "version"}:
            raise ValueError("material reference requires document_id and version")
        if type(ref["version"]) is not int or ref["version"] < 1:
            raise ValueError("material version must be a positive integer")
        document = db.get(models.MaterialDocument, ref["document_id"])
        if (
            document is None
            or document.version != ref["version"]
            or document.course_id != activity.course_id
            or document.status != "active"
            or document.retired_at is not None
        ):
            raise ValueError("selected material version is not active in this course")
        indexed = (
            db.query(models.MaterialFragment)
            .filter(
                models.MaterialFragment.document_id == document.id,
                models.MaterialFragment.document_version == ref["version"],
                models.MaterialFragment.indexing_status == "indexed",
                (
                    models.MaterialFragment.valid_until.is_(None)
                    | (models.MaterialFragment.valid_until >= utcnow())
                ),
            )
            .count()
        )
        if not indexed:
            raise ValueError("selected material has no current indexed fragments")


def _copy_retention(db: Session, source_id: str, days: int | None = None):
    source = db.get(models.RetentionPolicy, source_id)
    if source is None:
        raise ValueError("retention policy not found")
    period = source.retention_days if days is None else days
    if period is None or period < 0:
        raise ValueError("managed retention policy requires a finite non-negative period")
    target = models.RetentionPolicy(
        version=source.version + 1,
        content_scope=source.content_scope,
        retention_days=period,
        access_scope=source.access_scope,
        purge_rule=source.purge_rule,
    )
    db.add(target)
    db.flush()
    return target


def register_governance(
    db: Session,
    activity,
    *,
    model_id="deterministic",
    material_versions=None,
    status="draft",
    source_activity_id=None,
):
    existing = db.get(models.ActivityGovernance, activity.id)
    if existing is not None:
        return existing
    row = models.ActivityGovernance(
        activity_configuration_id=activity.id,
        family_id=activity.family_id,
        version=activity.version,
        status=status,
        model_id=model_id,
        material_versions=deepcopy(material_versions or []),
        source_activity_configuration_id=source_activity_id,
    )
    db.add(row)
    db.flush()
    return row


def _bind_materials(db: Session, activity, material_versions):
    for ref in material_versions:
        document = db.get(models.MaterialDocument, ref["document_id"])
        document.activity_configuration_ids = list(
            dict.fromkeys([*document.activity_configuration_ids, activity.id])
        )
        db.add(document)
        for fragment in db.query(models.MaterialFragment).filter_by(document_id=document.id):
            fragment.activity_configuration_ids = list(
                dict.fromkeys([*fragment.activity_configuration_ids, activity.id])
            )


def create_managed_activity(
    db: Session,
    data: ActivityConfigurationInput,
    *,
    model_id="deterministic",
    material_versions=None,
    mode_config=None,
):
    refs = material_versions or []
    candidate = models.ActivityConfiguration(**data.model_dump(exclude={"output_authorization_policy"}))
    _validate_selection(db, candidate, model_id, refs)
    policy = _copy_retention(db, data.retention_policy_id)
    data = data.model_copy(update={"retention_policy_id": policy.id})
    activity = create_activity(db, data)
    register_governance(db, activity, model_id=model_id, material_versions=refs)
    _bind_materials(db, activity, refs)
    if activity.mode == "oral_defense":
        configure_defense_activity(
            db, activity.id, DefenseActivityConfigInput.model_validate(mode_config or {})
        )
    else:
        configure_self_study_activity(
            db, activity.id, SelfStudyActivityConfigInput.model_validate(mode_config or {})
        )
    db.flush()
    return activity


def duplicate_activity(db: Session, activity_id: str, changes: dict, *, new_family=False):
    source = db.get(models.ActivityConfiguration, activity_id)
    if source is None:
        raise ValueError("activity not found")
    permitted = set(ActivityConfigurationInput.model_fields) | {
        "model_id",
        "material_versions",
        "mode_config",
        "retention_days",
    }
    if set(changes) - permitted:
        raise ValueError("unknown activity field")
    original_meta = db.get(models.ActivityGovernance, source.id)
    legacy_refs = (
        [
            {"document_id": document.id, "version": document.version}
            for document in db.query(models.MaterialDocument).filter_by(status="active")
            if source.id in (document.activity_configuration_ids or [])
        ]
        if original_meta is None
        else []
    )
    legacy_model = (
        f"ollama:{os.environ['ORALIA_OLLAMA_MODEL']}"
        if os.environ.get("ORALIA_OLLAMA_MODEL")
        else "deterministic"
    )
    model_id = changes.get("model_id", original_meta.model_id if original_meta else legacy_model)
    refs = deepcopy(
        changes.get("material_versions", original_meta.material_versions if original_meta else legacy_refs)
    )
    data = {
        name: deepcopy(getattr(source, name))
        for name in ActivityConfigurationInput.model_fields
        if name != "output_authorization_policy"
    }
    data["output_authorization_policy"] = OutputAuthorizationPolicy.model_validate_json(
        source.output_authorization_policy_json
    )
    data.update(
        {key: value for key, value in changes.items() if key in ActivityConfigurationInput.model_fields}
    )
    validated = ActivityConfigurationInput.model_validate(data)
    if validated.general_knowledge_allowed != validated.output_authorization_policy.general_knowledge_allowed:
        raise ValueError("activity and output policy general knowledge permissions must agree")
    candidate = models.ActivityConfiguration(**validated.model_dump(exclude={"output_authorization_policy"}))
    _validate_selection(db, candidate, model_id, refs)
    retention = _copy_retention(db, validated.retention_policy_id, changes.get("retention_days"))
    if original_meta is None:
        another_active = (
            db.query(models.ActivityGovernance).filter_by(family_id=source.family_id, status="active").first()
        )
        register_governance(
            db,
            source,
            status="retired" if another_active else "active",
            model_id=legacy_model,
            material_versions=legacy_refs,
        )
    family = str(uuid.uuid4()) if new_family else source.family_id
    version = (
        1
        if new_family
        else (
            db.query(func.max(models.ActivityConfiguration.version)).filter_by(family_id=family).scalar() or 0
        )
        + 1
    )
    activity = models.ActivityConfiguration(
        **validated.model_dump(exclude={"output_authorization_policy", "retention_policy_id"}),
        family_id=family,
        version=version,
        retention_policy_id=retention.id,
        output_authorization_policy_json=source.output_authorization_policy_json,
        output_authorization_policy_sha256=source.output_authorization_policy_sha256,
    )
    if "output_authorization_policy" in changes:
        from oralia.domain.policies.output_authorization_policy import (
            canonical_policy_json,
            canonical_policy_sha256,
        )

        activity.output_authorization_policy_json = canonical_policy_json(
            validated.output_authorization_policy
        )
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(
            activity.output_authorization_policy_json
        )
    db.add(activity)
    db.flush()
    register_governance(db, activity, model_id=model_id, material_versions=refs, source_activity_id=source.id)
    _bind_materials(db, activity, refs)
    specific_model = (
        models.DefenseActivityConfig if source.mode == "oral_defense" else models.SelfStudyActivityConfig
    )
    old_config = db.query(specific_model).filter_by(activity_configuration_id=source.id).one_or_none()
    mode_data = (
        {
            column.name: deepcopy(getattr(old_config, column.name))
            for column in specific_model.__table__.columns
            if column.name not in {"id", "created_at", "activity_configuration_id"}
        }
        if old_config
        else {}
    )
    if activity.mode != source.mode:
        mode_data = {}
    mode_data.update(changes.get("mode_config", {}))
    if activity.mode == "oral_defense":
        configure_defense_activity(db, activity.id, DefenseActivityConfigInput.model_validate(mode_data))
    else:
        configure_self_study_activity(db, activity.id, SelfStudyActivityConfigInput.model_validate(mode_data))
    db.flush()
    return activity


def publish_activity(db: Session, activity_id: str):
    activity = db.get(models.ActivityConfiguration, activity_id)
    if activity is None:
        raise ValueError("activity not found")
    meta = db.get(models.ActivityGovernance, activity_id)
    if meta is None:
        meta = register_governance(db, activity)
    _validate_selection(db, activity, meta.model_id, meta.material_versions)
    if meta.model_id == "guided_controlled":
        from oralia.application.services.guided_dialogue_service import validate_guided_configuration

        validate_guided_configuration(db, activity)
    retention = db.get(models.RetentionPolicy, activity.retention_policy_id)
    if retention is None or retention.retention_days is None or retention.retention_days < 0:
        raise ValueError("finite retention policy required")
    if not activity.output_authorization_policy_json:
        raise ValueError("explicit output authorization policy required")
    for historical in db.query(models.ActivityConfiguration).filter_by(family_id=activity.family_id):
        if historical.id != activity_id and db.get(models.ActivityGovernance, historical.id) is None:
            register_governance(db, historical, status="retired")
    db.query(models.ActivityGovernance).filter(
        models.ActivityGovernance.family_id == activity.family_id,
        models.ActivityGovernance.activity_configuration_id != activity_id,
        models.ActivityGovernance.status == "active",
    ).update({"status": "retired"})
    meta.status = "active"
    db.add(meta)
    db.flush()
    return meta


def retire_activity(db: Session, activity_id: str):
    activity = db.get(models.ActivityConfiguration, activity_id)
    if activity is None:
        raise ValueError("activity not found")
    meta = db.get(models.ActivityGovernance, activity_id) or register_governance(db, activity)
    meta.status = "retired"
    db.flush()
    return meta


def activity_view(db: Session, activity):
    meta = db.get(models.ActivityGovernance, activity.id)
    policy = db.get(models.RetentionPolicy, activity.retention_policy_id)
    specific = (
        models.DefenseActivityConfig if activity.mode == "oral_defense" else models.SelfStudyActivityConfig
    )
    config = db.query(specific).filter_by(activity_configuration_id=activity.id).one_or_none()
    return {
        "id": activity.id,
        "family_id": activity.family_id,
        "version": activity.version,
        "course_id": activity.course_id,
        "name": activity.name,
        "subject": activity.subject,
        "objective": activity.objective,
        "mode": activity.mode,
        "language": activity.language,
        "max_turns": activity.max_turns,
        "max_duration_seconds": activity.max_duration_seconds,
        "status": meta.status if meta else "legacy",
        "model_id": meta.model_id if meta else "installation-default",
        "source_activity_configuration_id": meta.source_activity_configuration_id if meta else None,
        "material_versions": meta.material_versions if meta else [],
        "retention_days": policy.retention_days if policy else None,
        "retention_content_scope": policy.content_scope if policy else None,
        "retention_access_scope": policy.access_scope if policy else None,
        "policy_sha256": activity.output_authorization_policy_sha256,
        "output_authorization_policy": (
            json.loads(activity.output_authorization_policy_json)
            if activity.output_authorization_policy_json
            else None
        ),
        "mode_config": (
            {
                c.name: getattr(config, c.name)
                for c in specific.__table__.columns
                if c.name not in {"id", "activity_configuration_id", "created_at"}
            }
            if config
            else {}
        ),
        "required_agent_ids": activity.required_agent_ids,
        "optional_agent_ids": activity.optional_agent_ids,
        "general_knowledge_allowed": activity.general_knowledge_allowed,
    }
