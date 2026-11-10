"""Reconstruct reviewed unit plans; the independent final output gate still decides."""

from sqlalchemy.orm import Session

from oralia.application.orchestration.output_authorization_context import (
    AuthorizationReferenceInput,
    build_authorization_snapshot,
)
from oralia.application.orchestration.output_proposal_builder import BoundTemplateSlot, build_output_proposal
from oralia.application.services.dialogue_retrieval_service import authorized_unit
from oralia.domain.dialogue.contracts import DialogueGenerationRequest, ProposalPlan
from oralia.domain.dialogue.semantic_templates import SEMANTIC_GREETING_TEMPLATES, SEMANTIC_RECEIPT
from oralia.domain.policies.output_authorization_contract import ScopeReference
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    GREETED_REVIEWED_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE_2,
    MATERIAL_FRAGMENT_RESPONSE_3,
)
from oralia.infrastructure.db import models


class ReviewedUnitGenerationAdapter:
    def __init__(self, db: Session, *, catalog=DEFAULT_OUTPUT_TEMPLATE_CATALOG):
        self.db = db
        self.catalog = catalog

    def render(self, request: DialogueGenerationRequest):
        session = self.db.get(models.Session, str(request.session_id))
        turn = self.db.get(models.Turn, str(request.turn_id))
        state = self.db.get(models.CognitiveState, str(request.session_id))
        if (
            session is None
            or session.status != "active"
            or turn is None
            or turn.session_id != session.id
            or turn.status != "in_progress"
        ):
            raise ValueError("renderer request is not an active turn of this session")
        if state is None or state.version != request.base_version:
            raise ValueError("renderer request has stale context")
        return render_plan(self.db, session, request.plan, catalog=self.catalog, turn_id=turn.id)


def _validate_receipt(db, session, plan, turn_id):
    from oralia.application.services.dialogue_context_service import _validate_turn_reference
    from oralia.domain.dialogue.contracts import DialogueContext

    if turn_id is None:
        raise ValueError("reviewed receipt requires an explicit active turn identity")
    turn = db.get(models.Turn, str(turn_id), populate_existing=True)
    state = db.get(models.CognitiveState, session.id, populate_existing=True)
    if (
        turn is None
        or turn.session_id != session.id
        or turn.status != "in_progress"
        or state is None
        or not (turn.input_text or "").strip()
    ):
        raise ValueError("reviewed receipt requires the current authenticated message")
    context = DialogueContext.model_validate(state.dialogue_context or {})
    if not context.pending_question_unit_id or not context.pending_question_turn_id:
        raise ValueError("reviewed receipt requires an actual pending question")
    _validate_turn_reference(db, session.id, str(context.pending_question_turn_id))
    scope = ScopeReference(
        topic_ref=SEMANTIC_RECEIPT.topic_ref,
        purpose_ref=SEMANTIC_RECEIPT.purpose_ref,
        action_ref=SEMANTIC_RECEIPT.action_ref,
    )
    question = authorized_unit(
        db, session, str(context.pending_question_unit_id), scope, allow_solution=False
    )
    prior = db.get(models.Turn, str(context.pending_question_turn_id))
    if (
        question.kind != "question"
        or question.reviewed_content not in prior.output_text
        or [str(ref) for ref in plan.unit_refs] != question.relations.get("comparisons", [])
    ):
        raise ValueError("reviewed receipt is not bound to the emitted question feedback")


def render_plan(
    db: Session,
    session: models.Session,
    plan: ProposalPlan,
    *,
    catalog=DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    turn_id=None,
):
    """No candidate text argument, no template created from a candidate or its hash.

    Published teacher units supply trusted values. Their active source references,
    recipient and disclosure rule are revalidated here on every invocation. This
    function returns a proposal, never an approved response or an approval verdict.
    """
    if plan.transformation not in {"select_reviewed_unit", "compose_reviewed_units"}:
        raise ValueError("renderer transformation not supported")
    if plan.template_id == SEMANTIC_RECEIPT.template_id:
        _validate_receipt(db, session, plan, turn_id)
    entries = {
        1: (MATERIAL_FRAGMENT_RESPONSE, ("content",)),
        2: (MATERIAL_FRAGMENT_RESPONSE_2, ("content_0", "content_1")),
        3: (MATERIAL_FRAGMENT_RESPONSE_3, ("content_0", "content_1", "content_2")),
    }
    if len(plan.unit_refs) not in entries or len(set(plan.unit_refs)) != len(plan.unit_refs):
        raise ValueError("renderer requires one to three distinct reviewed units")
    if plan.transformation == "select_reviewed_unit" and len(plan.unit_refs) != 1:
        raise ValueError("select transformation requires exactly one unit")
    entry, placeholders = entries[len(plan.unit_refs)]
    if plan.template_id == GREETED_REVIEWED_RESPONSE.template_id and len(plan.unit_refs) == 1:
        entry = GREETED_REVIEWED_RESPONSE
    greeting = SEMANTIC_GREETING_TEMPLATES[len(plan.unit_refs)]
    if plan.template_id == greeting.template_id:
        entry = greeting
    if plan.template_id == SEMANTIC_RECEIPT.template_id and len(plan.unit_refs) == 1:
        entry = SEMANTIC_RECEIPT
    if (plan.template_id, plan.template_version, plan.template_sha256) != (
        entry.template_id,
        str(entry.version),
        entry.sha256,
    ):
        raise ValueError("renderer template identity not permitted")
    scope = ScopeReference(
        topic_ref=entry.topic_ref, purpose_ref=entry.purpose_ref, action_ref=entry.action_ref
    )
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    state = db.get(models.CognitiveState, session.id)
    study = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity.id)
        .one_or_none()
    )
    protected = activity.mode == "oral_defense" or (
        state is not None
        and state.mode == "practice_questions"
        and not (study and study.practice_reveals_solution)
    )
    units = [
        authorized_unit(db, session, str(ref), scope, allow_solution=not protected) for ref in plan.unit_refs
    ]
    if len({unit.subgoal_ref for unit in units}) != 1:
        raise ValueError("renderer cannot mix pending objectives")
    if sum(len(unit.reviewed_content) for unit in units) + len(units) - 1 > 4000:
        raise ValueError("reviewed composition exceeds the existing turn text bound")
    references = tuple(
        AuthorizationReferenceInput(
            data_ref=f"teaching-unit:{unit.id}:v{unit.version}",
            category="reviewed_teaching_unit",
            provenance="teacher_reviewed",
            recipient=session.participant_code,
            scope=scope,
            value=unit.reviewed_content,
        )
        for unit in units
    )
    snapshot = build_authorization_snapshot(session, activity, data_references=references, catalog=catalog)
    proposal = build_output_proposal(
        snapshot,
        template_id=entry.template_id,
        template_version=entry.version,
        template_sha256=entry.sha256,
        slots=tuple(
            BoundTemplateSlot(placeholder=placeholder, data_ref=ref.data_ref)
            for placeholder, ref in zip(placeholders, references, strict=True)
        ),
        catalog=catalog,
    )
    return snapshot, proposal
