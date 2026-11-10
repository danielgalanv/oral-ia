"""Contextual queries and current authorization checks; no candidate text cache."""

from sqlalchemy.orm import Session

from oralia.application.services.teaching_unit_service import unit_input, validate_sources
from oralia.domain.agents.material_retriever_agent import get_currently_valid_fragment
from oralia.domain.dialogue.contracts import ClosedModel, DialogueAct, DialogueContext
from oralia.domain.policies.output_authorization_contract import ScopeReference
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.infrastructure.db import models


class RetrievalQuery(ClosedModel):
    raw_text: str
    query: str | None
    needs_clarification: bool = False


def contextual_query(raw_text: str, act: DialogueAct, context: DialogueContext) -> RetrievalQuery:
    if act.primary_act in {"greeting", "ambiguous", "finish", "topic_switch", "mode_switch"}:
        return RetrievalQuery(raw_text=raw_text, query=None, needs_clarification=act.needs_clarification)
    if act.primary_act in {
        "repeat",
        "rephrase",
        "help",
        "continue",
        "example",
        "comparison",
        "content_answer",
    }:
        return RetrievalQuery(
            raw_text=raw_text,
            query=context.content_query or None,
            needs_clarification=not bool(context.content_query),
        )
    if act.reason_code == "explicit_control":
        return RetrievalQuery(
            raw_text=raw_text,
            query=context.content_query or None,
            needs_clarification=not bool(context.content_query),
        )
    return RetrievalQuery(raw_text=raw_text, query=raw_text.strip()[:500] or None)


def _policy(db: Session, session: models.Session, scope: ScopeReference):
    db.refresh(session)
    if session.status != "active":
        raise ValueError("dialogue session inactive")
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    db.refresh(activity)
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    )
    if session.participant_code not in policy.allowed_recipients:
        raise ValueError("dialogue recipient outside policy")
    if (
        scope.topic_ref not in policy.allowed_scopes.topics
        or scope.purpose_ref not in policy.allowed_scopes.purposes
        or scope.action_ref not in policy.allowed_scopes.actions
    ):
        raise ValueError("dialogue action outside policy scope")
    return activity, policy


def authorized_fragment(db: Session, session: models.Session, fragment_id: str, scope: ScopeReference):
    activity, policy = _policy(db, session, scope)
    current = db.get(models.MaterialFragment, fragment_id, populate_existing=True)
    if current is not None:
        db.get(models.MaterialDocument, current.document_id, populate_existing=True)
    db.get(models.ActivityGovernance, activity.id, populate_existing=True)
    fragment = get_currently_valid_fragment(
        db, fragment_id, course_id=activity.course_id, activity_configuration_id=activity.id
    )
    if fragment is None or not any(
        rule.category == fragment.content_type
        and rule.provenance == "activity_material"
        and rule.recipient == session.participant_code
        for rule in policy.allowed_disclosures
    ):
        raise ValueError("dialogue fragment revoked or not authorized")
    return fragment


def authorized_unit(
    db: Session, session: models.Session, unit_id: str, scope: ScopeReference, *, allow_solution: bool
):
    activity, policy = _policy(db, session, scope)
    unit = db.get(models.TeachingUnit, unit_id)
    if unit is not None:
        db.refresh(unit)
    if (
        unit is None
        or unit.status != "published"
        or unit.course_id != activity.course_id
        or activity.id not in unit.activity_refs
    ):
        raise ValueError("dialogue teaching unit unavailable in activity")
    if not allow_solution and unit.reveal_policy not in {"safe_hint", "question"}:
        raise ValueError("dialogue unit disclosure forbidden")
    if not any(
        rule.category == "reviewed_teaching_unit"
        and rule.provenance == "teacher_reviewed"
        and rule.recipient == session.participant_code
        for rule in policy.allowed_disclosures
    ):
        raise ValueError("dialogue teaching unit disclosure outside policy")
    validate_sources(db, unit_input(unit), activity.id)
    return unit
