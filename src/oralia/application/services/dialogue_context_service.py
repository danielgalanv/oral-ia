"""Bounded context updates in the caller's turn transaction; never commits alone."""

from sqlalchemy import update
from sqlalchemy.orm import Session

from oralia.domain.agents.agent_contract import CancellationToken
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.dialogue.contracts import DialogueContext
from oralia.infrastructure.db import models


def _validate_turn_reference(db: Session, session_id: str, turn_id: str):
    turn = db.get(models.Turn, turn_id)
    verdict = db.get(models.VerificationResult, turn.verification_result_id) if turn else None
    proposal = (
        db.get(models.GeneratedProposal, turn.generated_proposal_id)
        if turn and turn.generated_proposal_id
        else None
    )
    if (
        turn is None
        or turn.session_id != session_id
        or not turn.output_text
        or turn.status not in {"completed", "degraded"}
        or verdict is None
        or verdict.verdict != "approved"
        or verdict.verifier_agent_id != "constitutional-control"
        or proposal is None
        or proposal.turn_id != turn.id
        or verdict.proposal_id != proposal.id
    ):
        raise ValueError("dialogue reference is not an approved turn of this session")


def update_context(
    db: Session,
    session_id: str,
    base_version: int,
    context: DialogueContext,
    cancellation: CancellationToken,
):
    if cancellation.is_cancelled():
        raise ValueError("dialogue update cancelled")
    context = DialogueContext.model_validate(context)
    # An UPDATE on the session row serializes against terminal closure in this same
    # transaction (including SQLite). A stale in-memory Session.status is insufficient.
    active = db.execute(
        update(models.Session)
        .where(models.Session.id == session_id, models.Session.status == "active")
        .values(status="active")
    )
    if active.rowcount != 1:
        raise ValueError("dialogue session inactive")
    refs = {str(ref) for ref in (context.pending_question_turn_id, context.last_approved_turn_id) if ref}
    refs.update(r.ref for r in context.candidate_referents if r.kind == "turn")
    if context.selected_referent and context.selected_referent.kind == "turn":
        refs.add(context.selected_referent.ref)
    for turn_id in refs:
        _validate_turn_reference(db, session_id, turn_id)
    session = db.get(models.Session, session_id)
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    unit_refs = {r.ref for r in context.candidate_referents if r.kind == "unit"}
    unit_refs.update(str(ref) for ref in context.last_approved_unit_ids)
    if context.pending_question_unit_id:
        unit_refs.add(str(context.pending_question_unit_id))
    if context.selected_referent and context.selected_referent.kind == "unit":
        unit_refs.add(context.selected_referent.ref)
    units = db.query(models.TeachingUnit).filter_by(course_id=activity.course_id, status="published").all()
    units = [unit for unit in units if activity.id in unit.activity_refs]
    if unit_refs - {unit.id for unit in units}:
        raise ValueError("dialogue unit reference outside activity")
    topic_refs = {r.ref for r in context.candidate_referents if r.kind == "topic"}
    if context.selected_referent and context.selected_referent.kind == "topic":
        topic_refs.add(context.selected_referent.ref)
    if context.current_topic_ref:
        topic_refs.add(context.current_topic_ref)
    if context.pending_topic_ref:
        topic_refs.add(context.pending_topic_ref)
    if topic_refs - {unit.topic_ref for unit in units}:
        raise ValueError("dialogue topic reference outside activity")
    valid_subgoals = {unit.subgoal_ref for unit in units}
    if context.current_subgoal_ref and context.current_subgoal_ref not in valid_subgoals:
        raise ValueError("dialogue subgoal reference outside activity")
    for ref in context.evidence_refs:
        from oralia.domain.agents.material_retriever_agent import get_currently_valid_fragment

        fragment = get_currently_valid_fragment(
            db, str(ref.fragment_id), course_id=activity.course_id, activity_configuration_id=activity.id
        )
        if (
            fragment is None
            or fragment.document_id != str(ref.document_id)
            or fragment.document_version != ref.document_version
        ):
            raise ValueError("dialogue evidence reference outside activity")
    if context.claim_followup:
        anchor = context.claim_followup
        _validate_turn_reference(db, session_id, str(anchor.participant_turn_id))
        claim_turn = db.get(models.Turn, str(anchor.participant_turn_id))
        question = next((u for u in units if u.id == str(anchor.question_unit_id)), None)
        followup = next((u for u in units if u.id == str(anchor.followup_unit_id)), None)
        if (
            not claim_turn.input_text.strip()
            or question is None
            or followup is None
            or question.kind != "question"
            or followup.kind != "question"
            or followup.id not in question.relations.get("rephrases", [])
            or question.subgoal_ref != followup.subgoal_ref
            or anchor.subgoal_ref != question.subgoal_ref
            or {str(ref) for ref in anchor.source_fragment_ids}
            != {ref["fragment_id"] for ref in followup.source_refs}
        ):
            raise ValueError("claim followup outside reviewed question relationship")
    # Context references never authorize publication; the renderer revalidates current
    # source/disclosure policy even when reusing a previously approved turn.
    if cancellation.is_cancelled():
        raise ValueError("dialogue update cancelled")
    return apply_patch(
        db,
        session_id=session_id,
        base_version=base_version,
        proposed_by_agent_id="study-intent-interpreter",
        element_type="decision",
        payload={"dialogue_context": context.model_dump(mode="json")},
        justification="dialogue-context/v1 bounded transactional update",
    )
