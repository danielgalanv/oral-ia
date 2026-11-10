"""Pure context decisions; publication requires independent current authorization."""

import hashlib
import json

from oralia.domain.dialogue.contracts import DialogueActName, DialogueContext, Referent


def current_context(context: DialogueContext, units) -> DialogueContext:
    """Drop revoked active anchors; never partially repeat a former composition."""
    valid_ids = {unit.id for unit in units}
    topics = {unit.topic_ref for unit in units}
    goals = {unit.subgoal_ref for unit in units}
    if (
        context.current_topic_ref is not None
        and context.current_topic_ref not in topics
        or context.current_subgoal_ref is not None
        and context.current_subgoal_ref not in goals
    ):
        return DialogueContext(
            effective_profile="degraded",
            stalled_count=context.stalled_count,
            last_notice=context.last_notice,
            schema_version=context.schema_version,
            navigation_page=context.navigation_page,
            pending_conservation=context.pending_conservation,
            close_confirmation_pending=context.close_confirmation_pending,
        )
    values = context.model_dump(mode="json")
    if context.pending_question_unit_id and str(context.pending_question_unit_id) not in valid_ids:
        values.update(pending_question_unit_id=None, pending_question_turn_id=None)
    if any(str(ref) not in valid_ids for ref in context.last_approved_unit_ids):
        values.update(last_approved_unit_ids=[], last_approved_turn_id=None, effective_profile="degraded")
    if context.pending_topic_ref is not None and context.pending_topic_ref not in topics:
        values["pending_topic_ref"] = None
    if context.claim_followup and (
        str(context.claim_followup.question_unit_id) not in valid_ids
        or str(context.claim_followup.followup_unit_id) not in valid_ids
    ):
        values["claim_followup"] = None
    live_turns = {
        ref
        for ref in [values["last_approved_turn_id"], values["pending_question_turn_id"]]
        if ref is not None
    }
    values["candidate_referents"] = [
        ref.model_dump(mode="json")
        for ref in context.candidate_referents
        if ref.kind == "topic"
        and ref.ref in topics
        or ref.kind == "unit"
        and ref.ref in valid_ids
        or ref.kind == "turn"
        and ref.ref in live_turns
    ]
    if context.selected_referent and context.selected_referent not in tuple(
        Referent.model_validate(ref) for ref in values["candidate_referents"]
    ):
        values["selected_referent"] = None
    return DialogueContext.model_validate(values)


def resolve_referent(context: DialogueContext) -> Referent | None:
    if context.selected_referent is not None:
        return context.selected_referent if context.selected_referent in context.candidate_referents else None
    return context.candidate_referents[0] if len(context.candidate_referents) == 1 else None


def after_output(
    context: DialogueContext,
    *,
    action: DialogueActName,
    approved_text: str,
    evidence_ids: tuple[str, ...],
    progressed: bool,
) -> DialogueContext:
    """Count structural failure to advance, never a participant capability score.

    The caller supplies only an already approved output and a structural progress
    result (new subgoal/evidence/action). Hashing detects identity, not grounding.
    Requested repetition preserves the counter; it cannot erase prior stagnation.
    """
    if action == "repeat":
        return context
    signature = hashlib.sha256(
        json.dumps(
            [action, context.current_topic_ref, evidence_ids, approved_text],
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    stalled = 0 if progressed else min(context.stalled_count + 1, 2)
    offered = (
        ()
        if stalled == 0
        else ("rephrase", "topic_switch") if stalled == 1 else ("help", "topic_switch", "finish")
    )
    return DialogueContext.model_validate(
        {
            **context.model_dump(mode="json"),
            "stalled_signature": signature,
            "stalled_count": stalled,
            "offered_actions": offered,
        }
    )
