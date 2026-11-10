"""V2 adaptation of the existing direct baseline, isolated to synthetic validation.

Same controlled provider, planner, material and mandatory T090/T150 as the agency.
No independent grounding/coherence/disclosure agent calls. Never installed as an
activity model or exposed through a new public endpoint. The harness selects this
actual implementation explicitly; no favorable response is substituted.
"""

import time

from sqlalchemy import update

from oralia.application.orchestration.final_output_gate import decide_final_output, persist_final_output
from oralia.application.orchestration.self_study_agency_composer import ModeNotEnabled
from oralia.application.services.dialogue_context_service import update_context
from oralia.application.services.dialogue_retrieval_service import authorized_fragment
from oralia.application.services.guided_dialogue_service import TURN_BUDGET_MS, _notice, current_units
from oralia.application.services.reviewed_unit_renderer import ReviewedUnitGenerationAdapter
from oralia.application.services.trace_service import record_event
from oralia.domain.agents.agent_contract import CancellationToken
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.dialogue.catalog import GUIDED_CATALOG
from oralia.domain.dialogue.context import after_output, current_context
from oralia.domain.dialogue.contracts import (
    DialogueContext,
    DialogueControl,
    DialogueGenerationRequest,
    ProposalPlan,
)
from oralia.domain.dialogue.interpretation import interpret
from oralia.domain.dialogue.policy import choose
from oralia.domain.policies.output_authorization_contract import ScopeReference
from oralia.domain.policies.output_template_catalog import (
    MATERIAL_FRAGMENT_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE_3,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow


async def run_direct_guided_turn(
    db,
    session,
    text,
    *,
    defense=False,
    closure_retain=False,
    closure_scope=None,
    requested_topic=None,
    dialogue_control=None,
):
    tick = time.monotonic()
    guarded = db.execute(
        update(models.Session)
        .where(models.Session.id == session.id, models.Session.status == "active")
        .values(status="active")
    )
    if guarded.rowcount != 1:
        raise ValueError("baseline session inactive")
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    config = (
        db.query(models.DefenseActivityConfig if defense else models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity.id)
        .one()
    )
    if defense:
        from oralia.application.commands.end_defense_session import validate_defense_retention

        validate_defense_retention(db, session, config, retain=closure_retain, scope=closure_scope)
    state = get_or_create(db, session.id, activity.id)
    context = DialogueContext.model_validate(
        state.dialogue_context or {"effective_profile": "guided_controlled"}
    )
    act = interpret(
        text,
        pending_question=context.pending_question_turn_id is not None,
        referents=context.candidate_referents,
    )
    if dialogue_control is not None:
        if text.strip() or requested_topic is not None:
            raise ValueError("mixed baseline controls")
        act = DialogueControl.model_validate(dialogue_control).as_act()
    if requested_topic is not None:
        if not defense or requested_topic not in config.topics:
            raise ValueError("baseline topic outside scope")
        act = act.model_copy(update={"primary_act": "topic_switch", "requested_topic": requested_topic})
    mode = "oral_defense" if defense else state.mode or config.enabled_modes[0]
    if act.requested_mode:
        if defense or act.requested_mode not in config.enabled_modes:
            raise ModeNotEnabled(
                requested_mode=act.requested_mode, enabled_modes=[] if defense else config.enabled_modes
            )
        mode = act.requested_mode
    if not defense and mode != state.mode and mode != "practice_questions":
        context = context.model_copy(
            update={"pending_question_unit_id": None, "pending_question_turn_id": None, "support_step": 0}
        )
    turn = models.Turn(session_id=session.id, index=session.turn_count, input_text=text, status="in_progress")
    db.add(turn)
    db.flush()
    patch = apply_patch(
        db,
        session_id=session.id,
        base_version=state.version,
        proposed_by_agent_id="direct-baseline-v2",
        element_type="decision",
        payload={"mode": mode},
        justification="synthetic direct baseline explicit mode",
    )
    if not patch.applied:
        raise ValueError("baseline state conflict")
    db.refresh(state)
    units = current_units(db, activity)
    context = current_context(context, units)
    choice = choose(
        units,
        act,
        context,
        text,
        protected=defense or (mode == "practice_questions" and not config.practice_reveals_solution),
        initial_question=config.initial_questions[0] if defense and config.initial_questions else None,
        study_mode=mode,
    )
    notice = choice.notice
    limited = (
        session.turn_count + 1 >= activity.max_turns
        or (utcnow() - session.started_at).total_seconds() >= activity.max_duration_seconds
    )
    if limited or act.primary_act == "finish":
        notice = "finish"
    if not units:
        notice = "unavailable"
        context = DialogueContext(
            effective_profile="degraded", stalled_count=context.stalled_count, last_notice=context.last_notice
        )
    if limited or act.primary_act == "finish":
        notice = "finish"
    selected = next((unit for unit in units if unit.id == choice.unit_id), None) if notice is None else None
    rendered = []
    sources = []
    if selected:
        rendered = [
            selected,
            *[unit for ref in choice.additional_unit_ids for unit in units if unit.id == ref],
        ]
        entry = MATERIAL_FRAGMENT_RESPONSE_3 if len(rendered) == 3 else MATERIAL_FRAGMENT_RESPONSE
        plan = ProposalPlan(
            template_id=entry.template_id,
            template_version=str(entry.version),
            template_sha256=entry.sha256,
            action=act.primary_act,
            unit_refs=tuple(unit.id for unit in rendered),
            transformation="select_reviewed_unit" if len(rendered) == 1 else "compose_reviewed_units",
        )
        snapshot, proposal = ReviewedUnitGenerationAdapter(db).render(
            DialogueGenerationRequest(
                plan=plan, session_id=session.id, turn_id=turn.id, base_version=state.version
            )
        )
        protected = defense or mode == "practice_questions" and not config.practice_reveals_solution
        refs = {ref["fragment_id"]: ref for unit in rendered for ref in unit.source_refs}
        for ref in refs.values():
            fragment = db.get(models.MaterialFragment, ref["fragment_id"])
            visible = ""
            if not protected:
                try:
                    visible = authorized_fragment(
                        db,
                        session,
                        fragment.id,
                        ScopeReference(
                            topic_ref="activity", purpose_ref="material_response", action_ref="respond"
                        ),
                    ).text
                except ValueError:
                    pass
            sources.append(
                {
                    "document_id": fragment.document_id,
                    "document_version": fragment.document_version,
                    "location_ref": fragment.location_ref,
                    "fragment_text": visible,
                    "content_withheld": not bool(visible),
                }
            )
    if int((time.monotonic() - tick) * 1000) >= TURN_BUDGET_MS:
        selected = None
        notice = "verification_failed"
        sources = []
    if not selected:
        notice = notice or "limited"
        if notice == "orientation" and context.stalled_count:
            notice = "clarify"
        if notice == context.last_notice and notice != "finish":
            notice = "unavailable_repeat" if not units else "clarify" if notice == "recovery" else "recovery"
        snapshot, proposal = _notice(db, session, activity, notice)
    decision = decide_final_output(
        snapshot, proposal, catalog=GUIDED_CATALOG, allow_operational_attempt=False
    )
    provider = "reviewed-unit-renderer/v1" if selected else "fixed-dialogue-template/v1"
    persist_final_output(db, turn, decision, generator_agent_id="direct-baseline-v2")
    action = (
        "finish"
        if notice == "finish" or decision.output_text is None
        else (
            "ask"
            if defense and selected and selected.kind == "question"
            else "clarify" if defense else "respond"
        )
    )
    dialogue = models.DialogueAction(
        turn_id=turn.id, action_type=action, chosen_by_agent_id="direct-baseline-v2"
    )
    db.add(dialogue)
    db.flush()
    turn.dialogue_action_id = dialogue.id
    session.turn_count += 1
    turn.ended_at = utcnow()
    turn.latency_ms = int((time.monotonic() - tick) * 1000)
    updated = context.model_dump(mode="json")
    updated["last_notice"] = notice
    if selected:
        updated.update(
            current_topic_ref=selected.topic_ref,
            current_subgoal_ref=selected.subgoal_ref,
            content_query=(
                text[:500]
                if act.primary_act == "content_question"
                else context.content_query or selected.topic_ref
            ),
            last_approved_turn_id=turn.id,
            last_approved_unit_ids=[unit.id for unit in rendered],
            candidate_referents=[{"kind": "topic", "ref": selected.topic_ref}],
            pending_topic_ref=None,
            support_step=choice.support_step,
            relevant_concepts=[selected.topic_ref],
            effective_profile="guided_controlled",
        )
        if choice.is_question and (
            selected.topic_ref != context.current_topic_ref
            or act.primary_act not in {"repeat", "rephrase", "content_answer"}
        ):
            updated.update(pending_question_unit_id=selected.id, pending_question_turn_id=turn.id)
    elif choice.pending_topic:
        updated["pending_topic_ref"] = choice.pending_topic
    next_context = after_output(
        DialogueContext.model_validate(updated),
        action=act.primary_act,
        approved_text=decision.output_text or "",
        evidence_ids=tuple(unit.id for unit in rendered) if selected else (),
        progressed=selected is not None,
    )
    if not units:
        next_context = next_context.model_copy(update={"offered_actions": ("finish",)})
    db.flush()
    db.refresh(state)
    if decision.output_text is not None:
        context_patch = update_context(db, session.id, state.version, next_context, CancellationToken())
        if not context_patch.applied:
            raise ValueError("baseline context conflict")
        patch = apply_patch(
            db,
            session_id=session.id,
            base_version=context_patch.resulting_version,
            proposed_by_agent_id="direct-baseline-v2",
            element_type="decision",
            payload={
                "current_input": text,
                "participant_response": decision.output_text,
                "turn_number": session.turn_count,
                "next_action_proposed": action,
            },
            justification="synthetic direct baseline T090-approved output",
        )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="direct_baseline_decision",
        payload={
            "provider": provider,
            "unit_ids": [unit.id for unit in rendered] if selected else [],
            "notice": notice,
            "independent_verifiers_executed": False,
        },
        memory_category="procedural",
    )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="generation_call",
        payload={
            "adapter": "direct-baseline-v2",
            "provider": provider,
            "model": None,
            "fallback_used": False,
            "fragment_ids": (
                list(dict.fromkeys(ref["fragment_id"] for unit in rendered for ref in unit.source_refs))
                if selected
                else []
            ),
        },
        memory_category="procedural",
    )
    summary = None
    if action == "finish":
        status = (
            "closed_error_safe"
            if decision.output_text is None
            else "closed_limit_reached" if limited else "closed_voluntary"
        )
        if defense:
            from oralia.application.commands.end_defense_session import end_defense_session

            summary = end_defense_session(
                db, session, config, status=status, retain=closure_retain, scope=closure_scope
            )
        else:
            from oralia.application.commands.end_study_session import end_study_session

            summary = end_study_session(db, session, config, status=status)
    return {
        "turn_id": turn.id,
        "output_text": decision.output_text,
        "blocked": decision.blocked,
        "state_version": patch.resulting_version,
        "status": turn.status,
        "sources": sources,
        "mode": mode,
        "dialogue_action": action,
        "session_status": session.status,
        "summary": summary,
        "dialogue_status": {
            "effective_profile": next_context.effective_profile,
            "provider": provider,
            "primary_act": act.primary_act,
            "rendered_unit_ids": [unit.id for unit in rendered] if selected else [],
            "notice": notice,
            "pending_topic": next_context.pending_topic_ref,
            "grounding_verdict": "not_executed_baseline",
            "coherence_verdict": "not_executed_baseline",
            "non_disclosure_verdict": "not_executed_baseline",
            "latency_ms": turn.latency_ms,
            "turn_budget_ms": TURN_BUDGET_MS,
            "available_topics": [] if defense else sorted({unit.topic_ref for unit in units}),
            "offered_actions": list(next_context.offered_actions),
            "architecture": "direct_baseline_v2",
            "llm_calls": 0,
        },
    }
