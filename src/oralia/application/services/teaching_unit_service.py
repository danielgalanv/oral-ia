"""Explicit teacher review and immutable published content versions.

This service does not authorize participant output. Callers must use the teacher
API guard; subsequent renderers must revalidate all sources, scope and T090.
"""

from typing import Literal
from uuid import UUID

from pydantic import Field
from sqlalchemy import func, update
from sqlalchemy.orm import Session

from oralia.domain.agents.material_retriever_agent import get_currently_valid_fragment
from oralia.domain.dialogue.contracts import ClosedModel, EvidenceReference
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


class TeachingUnitInput(ClosedModel):
    course_id: UUID
    kind: Literal["fact", "explanation", "example", "comparison", "question", "hint"]
    topic_ref: str = Field(min_length=1, max_length=100)
    subgoal_ref: str = Field(min_length=1, max_length=100)
    reviewed_content: str = Field(min_length=1, max_length=3000)
    source_refs: tuple[EvidenceReference, ...] = Field(min_length=1, max_length=5)
    relations: dict[str, list[UUID]] = Field(default_factory=dict)
    reveal_policy: Literal["study_only", "safe_hint", "question", "solution"]
    activity_refs: tuple[UUID, ...] = Field(default=(), max_length=100)


def _source_is_current(db: Session, ref: EvidenceReference, course_id: str, activity_id: str | None = None):
    fragment = db.get(models.MaterialFragment, str(ref.fragment_id), populate_existing=True)
    document = db.get(models.MaterialDocument, str(ref.document_id), populate_existing=True)
    if (
        fragment is None
        or document is None
        or document.course_id != course_id
        or fragment.course_id != course_id
        or fragment.document_id != document.id
        or document.version != ref.document_version
        or fragment.document_version != ref.document_version
        or document.status != "active"
        or document.retired_at is not None
        or fragment.indexing_status != "indexed"
        or fragment.valid_until is not None
        and fragment.valid_until < utcnow()
    ):
        return False
    if activity_id is not None:
        db.get(models.ActivityGovernance, activity_id, populate_existing=True)
        if (
            get_currently_valid_fragment(
                db, fragment.id, course_id=course_id, activity_configuration_id=activity_id
            )
            is None
        ):
            return False
    return True


def validate_sources(
    db: Session, data: TeachingUnitInput, activity_id: str | None = None, *, authoring=False
):
    if db.get(models.Course, str(data.course_id)) is None:
        raise ValueError("teaching unit course missing")
    for activity_ref in data.activity_refs:
        activity = db.get(models.ActivityConfiguration, str(activity_ref), populate_existing=True)
        if activity is None or activity.course_id != str(data.course_id):
            raise ValueError("teaching unit activity outside course")
        if authoring and activity.immutable_since is not None:
            raise ValueError(
                "used activity requires an explicit successor before publishing new teaching units"
            )
        if authoring:
            # Serialize authoring with first use in the caller's transaction.
            guarded = db.execute(
                update(models.ActivityConfiguration)
                .where(
                    models.ActivityConfiguration.id == activity.id,
                    models.ActivityConfiguration.immutable_since.is_(None),
                )
                .values(immutable_since=None)
            )
            if guarded.rowcount != 1:
                raise ValueError("used activity requires an explicit successor before authoring")
    if any(not _source_is_current(db, ref, str(data.course_id), activity_id) for ref in data.source_refs):
        raise ValueError("teaching unit source missing, revoked or outside scope")
    for activity_ref in data.activity_refs:
        if any(
            not _source_is_current(db, ref, str(data.course_id), str(activity_ref))
            for ref in data.source_refs
        ):
            raise ValueError("teaching unit source outside assigned activity")
    if set(data.relations) - {
        "hints",
        "rephrases",
        "examples",
        "comparisons",
        "next",
        "solution",
        "didactic_definition",
        "didactic_cause",
        "didactic_process",
        "didactic_possibility",
        "didactic_conditions",
    }:
        raise ValueError("unknown teaching unit relation")
    for refs in data.relations.values():
        if len(refs) > 5:
            raise ValueError("too many teaching unit relations")
        for ref in refs:
            related = db.get(models.TeachingUnit, str(ref))
            if related is None or related.course_id != str(data.course_id):
                raise ValueError("teaching unit relation outside course")


def _values(data: TeachingUnitInput):
    values = data.model_dump(mode="json")
    # UUID JSON encoding is intentional; no text candidates are taken from a model.
    return values


def create(db: Session, data: TeachingUnitInput):
    data = TeachingUnitInput.model_validate(data)
    validate_sources(db, data, authoring=True)
    unit = models.TeachingUnit(**_values(data))
    db.add(unit)
    db.flush()
    return unit


def unit_input(unit):
    return TeachingUnitInput.model_validate(
        {name: getattr(unit, name) for name in TeachingUnitInput.model_fields}
    )


def publish(db: Session, unit_id: str, *, reviewed: bool):
    if reviewed is not True:
        raise ValueError("explicit teacher review required")
    unit = db.get(models.TeachingUnit, unit_id)
    if unit is None or unit.status != "draft":
        raise ValueError("only draft teaching units may be published")
    guarded = db.execute(
        update(models.TeachingUnit)
        .where(
            models.TeachingUnit.id == unit_id,
            models.TeachingUnit.status == "draft",
        )
        .values(status="draft")
    )
    if guarded.rowcount != 1:
        raise ValueError("only draft teaching units may be published")
    validate_sources(db, unit_input(unit), authoring=True)
    if (unit.kind == "hint") != (unit.reveal_policy == "safe_hint"):
        raise ValueError("hint requires explicit safe_hint review")
    if (unit.kind == "question") != (unit.reveal_policy == "question"):
        raise ValueError("question requires explicit question review")
    unit.status = "published"
    db.flush()
    return unit


def successor(db: Session, unit_id: str, data: TeachingUnitInput):
    prior = db.get(models.TeachingUnit, unit_id)
    if prior is None or str(data.course_id) != prior.course_id:
        raise ValueError("teaching unit successor outside course")
    validate_sources(db, data, authoring=True)
    version = (
        db.query(func.max(models.TeachingUnit.version)).filter_by(family_id=prior.family_id).scalar() or 0
    )
    unit = models.TeachingUnit(**_values(data), family_id=prior.family_id, version=version + 1)
    db.add(unit)
    db.flush()
    return unit


def retire(db: Session, unit_id: str):
    unit = db.get(models.TeachingUnit, unit_id)
    if unit is None:
        raise ValueError("teaching unit missing")
    unit.status = "retired"
    db.flush()
    return unit
