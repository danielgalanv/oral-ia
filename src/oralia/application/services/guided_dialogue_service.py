"""Controlled execution inside the existing agencies, using the existing verifier ports."""

import re
import time
import uuid

from sqlalchemy import update

from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.application.orchestration.final_output_gate import decide_final_output, persist_final_output
from oralia.application.orchestration.output_authorization_context import build_authorization_snapshot
from oralia.application.orchestration.output_proposal_builder import build_output_proposal
from oralia.application.services.dialogue_context_service import update_context
from oralia.application.services.dialogue_retrieval_service import authorized_fragment
from oralia.application.services.reviewed_unit_renderer import ReviewedUnitGenerationAdapter, render_plan
from oralia.application.services.screenless_navigation_service import (
    CHOICES,
    navigation_plan,
    render_navigation,
    screenless_enabled,
)
from oralia.application.services.teaching_unit_service import unit_input, validate_sources
from oralia.application.services.trace_service import record_event
from oralia.domain.agents.agent_contract import AgentError, AgentRequest, AgentResult, CancellationToken
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from oralia.domain.agents.solution_non_disclosure_verifier_agent import SolutionNonDisclosureVerifierAgent
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.dialogue.catalog import GUIDED_CATALOG, GUIDED_NOTICES
from oralia.domain.dialogue.context import after_output, current_context
from oralia.domain.dialogue.contracts import (
    DialogueAct,
    DialogueContext,
    DialogueControl,
    DialogueGenerationRequest,
    ProposalPlan,
)
from oralia.domain.dialogue.interpretation import normalized
from oralia.domain.dialogue.policy import GuidedChoice, choose
from oralia.domain.dialogue.semantic_templates import (
    SEMANTIC_GREETING_TEMPLATES,
    SEMANTIC_POLICY_ID,
    SEMANTIC_RECEIPT,
    SEMANTIC_TEMPLATE_CATALOG,
)
from oralia.domain.policies.output_authorization_contract import ScopeReference
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.domain.policies.output_template_catalog import (
    GREETED_REVIEWED_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE_2,
    MATERIAL_FRAGMENT_RESPONSE_3,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow

TURN_BUDGET_MS = 10000  # Controlled profile v1, no change to any existing agent maximum.


def is_guided(db, activity_id):
    meta = db.get(models.ActivityGovernance, activity_id)
    return bool(meta and meta.model_id == "guided_controlled")


def current_units(db, activity):
    rows = (
        db.query(models.TeachingUnit)
        .filter_by(course_id=activity.course_id, status="published")
        .order_by(models.TeachingUnit.created_at, models.TeachingUnit.id)
        .limit(1001)
        .all()
    )
    if len(rows) > 1000:
        raise ValueError("guided teaching catalog exceeds its bounded local capacity")
    valid = []
    for unit in rows:
        if activity.id not in unit.activity_refs:
            continue
        try:
            validate_sources(db, unit_input(unit), activity.id)
        except ValueError:
            continue
        valid.append(unit)
    if len(valid) > 200:
        raise ValueError("guided activity exceeds 200 published units")
    return valid


def validate_guided_configuration(db, activity):
    units = current_units(db, activity)
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    )
    needed = {(entry.template_id, entry.version) for entry in GUIDED_NOTICES.values()} | {
        MATERIAL_FRAGMENT_RESPONSE.identity[:2]
    }
    study = (
        db.query(models.SelfStudyActivityConfig)
        .filter_by(activity_configuration_id=activity.id)
        .one_or_none()
    )
    if study and "presentation_preparation" in study.enabled_modes:
        needed.add(MATERIAL_FRAGMENT_RESPONSE_3.identity[:2])
    if not needed <= {(e.template_id, e.version) for e in policy.allowed_templates}:
        raise ValueError(
            "Falta autorizar una plantilla versionada de contenido, composición o control guiado."
        )
    from oralia.domain.policies.output_template_catalog import NAVIGATION_TEMPLATES

    nav_pairs = {(e.template_id, e.version) for e in NAVIGATION_TEMPLATES.values()}
    if nav_pairs & {(e.template_id, e.version) for e in policy.allowed_templates} and not screenless_enabled(
        activity
    ):
        raise ValueError("La navegación sin pantalla requiere todas sus plantillas y permisos explícitos.")
    from oralia.application.services.screenless_navigation_service import pedagogy_enabled

    if policy.policy_id in {
        "guided-screenless/v2",
        "guided-screenless/v3",
        "guided-screenless/v4",
    } and not pedagogy_enabled(activity):
        raise ValueError("La política didáctica requiere sus plantillas y permisos completos.")
    from oralia.application.services.screenless_navigation_service import continuity_enabled

    if policy.policy_id == "guided-screenless/v4" and not continuity_enabled(activity):
        raise ValueError("La continuidad requiere su plantilla y política explícita completas.")
    from oralia.application.services.screenless_navigation_service import advanced_pedagogy_enabled

    if policy.policy_id == "guided-screenless/v3" and not advanced_pedagogy_enabled(activity):
        raise ValueError("Package dialogue policy requires complete explicit templates")
    if activity.general_knowledge_allowed:
        raise ValueError("El perfil guiado controlado no permite conocimiento general abierto.")
    if not (
        "activity" in policy.allowed_scopes.topics
        and "respond" in policy.allowed_scopes.actions
        and {"guided_control", "material_response"} <= set(policy.allowed_scopes.purposes)
    ):
        raise ValueError("Faltan los alcances explícitos de contenido y control de la actividad.")
    for recipient in policy.allowed_recipients:
        if not any(
            r.category == "reviewed_teaching_unit"
            and r.provenance == "teacher_reviewed"
            and r.recipient == recipient
            for r in policy.allowed_disclosures
        ):
            raise ValueError("Falta autorizar la divulgación del contenido docente al destinatario.")
    goals = {u.subgoal_ref for u in units}
    if len(goals) < 5:
        raise ValueError(
            "Faltan cinco objetivos revisados. Puede prepararse una actividad con perfil extractivo limitado."
        )
    for goal in goals:
        group = [u for u in units if u.subgoal_ref == goal]
        if not {"explanation", "example", "comparison", "question", "hint"} <= {u.kind for u in group}:
            raise ValueError(
                "Un objetivo no tiene explicación, ejemplo, contraste, pregunta o apoyo revisados."
            )
    by_id = {unit.id: unit for unit in units}
    supported = 0
    for unit in units:
        if unit.kind != "question":
            continue
        hints = unit.relations.get("hints", [])
        if (
            len(hints) >= 3
            and len(set(hints)) == len(hints)
            and all(
                ref in by_id
                and by_id[ref].kind == "hint"
                and by_id[ref].reveal_policy == "safe_hint"
                and by_id[ref].subgoal_ref == unit.subgoal_ref
                for ref in hints
            )
        ):
            supported += 1
    if supported < 3:
        raise ValueError(
            "Faltan tres preguntas con tres pistas vigentes, distintas y revisadas para su objetivo."
        )
    return units


def activity_capabilities(db, activity):
    meta = db.get(models.ActivityGovernance, activity.id)
    guided = bool(meta and meta.model_id == "guided_controlled")
    ready = True
    detail = None
    if guided:
        try:
            validate_guided_configuration(db, activity)
        except ValueError as exc:
            ready = False
            detail = str(exc)
    return {
        "available_modes": (
            list(study.enabled_modes)
            if (
                study := db.query(models.SelfStudyActivityConfig)
                .filter_by(activity_configuration_id=activity.id)
                .one_or_none()
            )
            else []
        ),
        "configured_profile": "guided_controlled" if guided else "extractive_limited",
        "effective_profile": (
            "degraded" if not ready else "guided_controlled" if guided else "extractive_limited"
        ),
        "provider": (
            "reviewed-unit-renderer/v1"
            if guided
            else "deterministic" if meta and meta.model_id == "deterministic" else "local_configured"
        ),
        "screenless_text_ready": guided and screenless_enabled(activity),
        "ready_for_entry": ready,
        "readiness_detail": detail,
        "generative_validated": False,
        "human_validation": "pending",
    }


def legacy_turn_capabilities(db, session, turn_id, *, blocked=False):
    """Report the adapter actually observed, without inferring a successful model."""
    calls = (
        db.query(models.TraceEvent)
        .filter_by(session_id=session.id, turn_id=turn_id, event_type="generation_call")
        .order_by(models.TraceEvent.created_at)
        .all()
    )
    metadata = next((event.payload for event in reversed(calls) if event.payload.get("adapter")), None)
    adapter = metadata.get("adapter") if metadata else None
    provider = {"deterministic": "deterministic", "ollama": "ollama_local"}.get(adapter, "no_observado")
    degraded = blocked or bool(metadata and metadata.get("fallback_used"))
    return {
        "configured_profile": "extractive_limited",
        "effective_profile": "degraded" if degraded else "extractive_limited",
        "provider": provider,
        "generative_validated": False,
        "human_validation": "pending",
    }


def _notice(db, session, activity, name, *, context=None, units=None, topic=None, chosen=None):
    from oralia.application.services.dialogue_output_catalog import activity_output_catalog

    catalog = activity_output_catalog(activity)
    if screenless_enabled(activity, session.participant_code):
        from oralia.domain.policies.output_template_catalog import NAVIGATION_TEMPLATES

        current = context or DialogueContext.model_validate(
            db.get(models.CognitiveState, session.id).dialogue_context or {}
        )
        nav_name = (
            name
            if name in NAVIGATION_TEMPLATES
            or name
            in {
                "didactic_greeting",
                "didactic_overview",
                "package_welcome",
                "outside_source",
                "package_topic_confirmed",
                "followups_exhausted",
            }
            else "empty" if name.startswith("unavailable") else "recovery"
        )
        return render_navigation(
            db,
            session,
            activity,
            nav_name,
            current,
            current_units(db, activity) if units is None else units,
            topic=topic,
            chosen=chosen,
        )
    entry = GUIDED_NOTICES[name]
    snapshot = build_authorization_snapshot(session, activity, catalog=catalog)
    return snapshot, build_output_proposal(
        snapshot,
        template_id=entry.template_id,
        template_version=entry.version,
        template_sha256=entry.sha256,
        catalog=catalog,
    )


def pending_question_view(db, session, context):
    """Current authorized projection of an original question, never a text cache."""
    from oralia.application.services.screenless_navigation_service import continuity_enabled

    if (
        session.status != "active"
        or not context.pending_question_unit_id
        or not context.pending_question_turn_id
    ):
        return None
    turn = db.get(models.Turn, str(context.pending_question_turn_id))
    unit = db.get(models.TeachingUnit, str(context.pending_question_unit_id))
    if turn is None or turn.session_id != session.id or unit is None or unit.kind != "question":
        return None
    verdict = db.get(models.VerificationResult, turn.verification_result_id)
    proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
    composed_question = False
    question_catalog = GUIDED_CATALOG
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    if (
        activity
        and str(context.last_approved_turn_id) == turn.id
        and unit.id in [str(ref) for ref in context.last_approved_unit_ids]
    ):
        try:
            from oralia.domain.dialogue.semantic_templates import SEMANTIC_POLICY_ID

            policy = load_output_authorization_policy(
                activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
            )
            if policy.policy_id == SEMANTIC_POLICY_ID:
                question_catalog = SEMANTIC_TEMPLATE_CATALOG
            refs = tuple(str(ref) for ref in context.last_approved_unit_ids)
            if policy.policy_id == SEMANTIC_POLICY_ID and len(refs) in {2, 3}:
                entry = {2: MATERIAL_FRAGMENT_RESPONSE_2, 3: MATERIAL_FRAGMENT_RESPONSE_3}[len(refs)]
                greeting = SEMANTIC_GREETING_TEMPLATES[len(refs)]
                if proposal and proposal.content.get("template_id") == greeting.template_id:
                    entry = greeting
                _, candidate = render_plan(
                    db,
                    session,
                    ProposalPlan(
                        template_id=entry.template_id,
                        template_version=str(entry.version),
                        template_sha256=entry.sha256,
                        action="repeat",
                        unit_refs=refs,
                        transformation="compose_reviewed_units",
                    ),
                    catalog=SEMANTIC_TEMPLATE_CATALOG,
                )
                composed_question = bool(proposal and proposal.content.get("text") == candidate.text)
        except ValueError:
            composed_question = False
    if not (
        verdict
        and verdict.verdict == "approved"
        and proposal
        and verdict.proposal_id == proposal.id
        and proposal.turn_id == turn.id
        and (
            composed_question
            or proposal.content.get("text") == unit.reviewed_content
            or (
                proposal.content.get("text") == "Hola. " + unit.reviewed_content
                and continuity_enabled(
                    db.get(models.ActivityConfiguration, session.activity_configuration_id),
                    session.participant_code,
                )
            )
        )
    ):
        return None
    entry = MATERIAL_FRAGMENT_RESPONSE
    try:
        snapshot, rendered = render_plan(
            db,
            session,
            ProposalPlan(
                template_id=entry.template_id,
                template_version=str(entry.version),
                template_sha256=entry.sha256,
                action="repeat",
                unit_refs=(unit.id,),
            ),
            catalog=question_catalog,
        )
        decision = decide_final_output(
            snapshot, rendered, catalog=question_catalog, allow_operational_attempt=False
        )
    except ValueError:
        return None
    return {"turn_id": turn.id, "text": decision.output_text} if decision.output_text else None


async def run_guided_turn(
    db,
    session,
    text,
    *,
    defense=False,
    closure_retain=False,
    closure_scope=None,
    requested_topic=None,
    dialogue_control=None,
    semantic_runtime=None,
):
    started = time.monotonic()
    configured_runtime = (
        semantic_runtime
        if semantic_runtime is not None and not defense and semantic_runtime.applies(session)
        else None
    )
    if configured_runtime is not None:
        configured_runtime.assert_engine(db)
    turn_budget_ms = TURN_BUDGET_MS
    semantic_result = None
    semantic_base_version = None
    active = db.execute(
        update(models.Session)
        .where(models.Session.id == session.id, models.Session.status == "active")
        .values(status="active")
    )
    if active.rowcount != 1:
        raise ValueError("session is not active")
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    try:
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        )
        semantic_policy = policy.policy_id == SEMANTIC_POLICY_ID
    except ValueError:
        if configured_runtime is not None:
            raise ValueError("La política del perfil semántico no es válida.") from None
        semantic_policy = False
    if semantic_policy and configured_runtime is None:
        raise ValueError("El intérprete local de esta actividad no está configurado; no se usa otro perfil.")
    if configured_runtime is not None and not semantic_policy:
        raise ValueError("El intérprete local requiere su política explícita de actividad.")
    state = get_or_create(db, session.id, activity.id)
    context = DialogueContext.model_validate(
        state.dialogue_context or {"effective_profile": "guided_controlled"}
    )
    config_model = models.DefenseActivityConfig if defense else models.SelfStudyActivityConfig
    config = db.query(config_model).filter_by(activity_configuration_id=activity.id).one()
    if defense:
        from oralia.application.commands.end_defense_session import validate_defense_retention

        validate_defense_retention(db, session, config, retain=closure_retain, scope=closure_scope)
    turn = models.Turn(session_id=session.id, index=session.turn_count, input_text=text, status="in_progress")
    db.add(turn)
    db.flush()

    async def call(agent, payload):
        agent_started = time.monotonic()
        if payload.get("dialogue_schema_version") == 3 and hasattr(agent, "package_contract"):
            agent.contract = agent.package_contract
        elif payload.get("dialogue_schema_version") == 2 and hasattr(agent, "dialogue_contract"):
            agent.contract = agent.dialogue_contract
        remaining = min(
            turn_budget_ms - int((time.monotonic() - started) * 1000),
            int((activity.max_duration_seconds - (utcnow() - session.started_at).total_seconds()) * 1000),
        )
        if remaining <= 0:
            result = AgentResult(
                status="timeout",
                error=AgentError(
                    code="TURN_BUDGET_EXHAUSTED", message="No queda presupuesto para otra operación."
                ),
            )
        else:
            request = AgentRequest(
                session_id=uuid.UUID(session.id),
                turn_id=uuid.UUID(turn.id),
                input=payload,
                deadline_ms=min(agent.contract.timeout_ms, remaining),
            )
            result = await run_with_deadline(agent, request)
        record_event(
            db,
            session_id=session.id,
            turn_id=turn.id,
            event_type="guided_agent_result",
            agent_id=agent.contract.agent_id,
            payload={
                "status": result.status,
                "contract_version": agent.contract.version,
                "verdict": (result.output or {}).get("verdict"),
            },
            latency_ms=int((time.monotonic() - agent_started) * 1000),
            memory_category="procedural",
        )
        if result.status == "cancelled":
            raise ValueError("Operación cancelada; no se ha confirmado un turno nuevo.")
        return result

    interpreted = await call(
        StudyIntentInterpreterAgent(),
        {
            "text": text,
            "dialogue_schema_version": 2,
            "current_mode": state.mode or None,
            "dialogue_context": context.model_dump(mode="json"),
        },
    )
    if interpreted.status != "ok":
        raise ValueError("dialogue interpretation unavailable; no turn committed")
    act = DialogueAct.model_validate(interpreted.output["dialogue_act"])
    if dialogue_control is not None:
        control = DialogueControl.model_validate(dialogue_control)
        if text.strip() or requested_topic is not None:
            raise ValueError("Envía una sola orden de diálogo.")
        act = control.as_act()
    if requested_topic is not None:
        if not defense or requested_topic not in config.topics:
            raise ValueError("requested topic is outside authorized scope")
        act = act.model_copy(update={"primary_act": "topic_switch", "requested_topic": requested_topic})
    units = current_units(db, activity)
    context = current_context(context, units)
    from oralia.application.services.screenless_navigation_service import advanced_pedagogy_enabled

    advanced_active = advanced_pedagogy_enabled(activity, session.participant_code)
    from oralia.application.services.screenless_navigation_service import continuity_enabled

    continuity_active = continuity_enabled(activity, session.participant_code)
    if advanced_active and dialogue_control is None and requested_topic is None:
        from oralia.domain.dialogue.package_dialogue import navigation_text, package_act

        act = package_act(text, act, context, units)
        if continuity_active:
            from oralia.domain.dialogue.continuity import act_for

            act = act_for(text, act, context, units)
    if screenless_enabled(activity, session.participant_code):
        context = context.model_copy(update={"schema_version": 2})
    navigation = (
        navigation_plan(
            db,
            session,
            (navigation_text(text) if advanced_active else text),
            context,
            units,
        )
        if screenless_enabled(activity, session.participant_code)
        and dialogue_control is None
        and requested_topic is None
        else None
    )
    if (
        screenless_enabled(activity, session.participant_code)
        and act.primary_act == "finish"
        and not (navigation and navigation.notice)
    ):
        from oralia.application.services.screenless_navigation_service import NavigationPlan

        navigation = NavigationPlan("close_confirm", {"close_confirmation_pending": True})
    navigation_before_context = context
    if navigation:
        context = context.model_copy(update=navigation.updates)
        if navigation.act is not None:
            act = navigation.act
    previous_mode = state.mode
    mode = "oral_defense" if defense else state.mode or config.enabled_modes[0]
    if (
        screenless_enabled(activity, session.participant_code)
        and act.requested_mode
        and (defense or act.requested_mode not in config.enabled_modes)
    ):
        from oralia.application.services.screenless_navigation_service import NavigationPlan

        navigation = NavigationPlan("disabled_mode")
        act = DialogueAct(primary_act="ambiguous", reason_code="explicit_control")
    if act.requested_mode:
        if defense or act.requested_mode not in config.enabled_modes:
            from oralia.application.orchestration.self_study_agency_composer import ModeNotEnabled

            raise ModeNotEnabled(
                requested_mode=act.requested_mode, enabled_modes=[] if defense else config.enabled_modes
            )
        else:
            mode = act.requested_mode
            choice_notice = None
    else:
        choice_notice = None
    protected = defense or mode == "practice_questions" and not config.practice_reveals_solution
    semantic_study_mode = (
        configured_runtime is not None
        and mode in {"doubt_resolution", "guided_explanation"}
        and not protected
    )
    if mode != previous_mode and mode != "practice_questions" and not defense:
        context = context.model_copy(
            update={"pending_question_unit_id": None, "pending_question_turn_id": None, "support_step": 0}
        )
    # Persist mode before the renderer derives the non-disclosure requirement.
    patch = apply_patch(
        db,
        session_id=session.id,
        base_version=state.version,
        proposed_by_agent_id="self-study-agency-composer" if not defense else "defense-agency",
        element_type="decision",
        payload={"mode": mode},
        justification="explicit guided mode selection",
    )
    if not patch.applied:
        raise ValueError("dialogue state version conflict")
    db.refresh(state)
    if act.requested_topic is not None and act.requested_topic not in {unit.topic_ref for unit in units}:
        raise ValueError("Ese tema no pertenece a las unidades vigentes de la actividad.")
    context = current_context(context, units)
    from oralia.application.services.screenless_navigation_service import pedagogy_enabled

    pedagogy_active = pedagogy_enabled(activity, session.participant_code)
    planning_units = units
    if pedagogy_active and act.primary_act != "repeat":
        from oralia.domain.dialogue.pedagogy import regular_teaching_units

        planning_units = regular_teaching_units(units)
    choice = choose(
        planning_units,
        act,
        context,
        "" if navigation and navigation.act and navigation.act.primary_act == "topic_switch" else text,
        protected=defense or (mode == "practice_questions" and not config.practice_reveals_solution),
        initial_question=config.initial_questions[0] if defense and config.initial_questions else None,
        study_mode=mode,
    )
    from oralia.application.services.screenless_navigation_service import pedagogy_enabled

    pedagogical = None
    if (
        pedagogy_active
        and not semantic_study_mode
        and not advanced_active
        and not (navigation and (navigation.notice or navigation.act))
        and dialogue_control is None
    ):
        from oralia.domain.dialogue.pedagogy import pedagogical_choice

        pedagogical = pedagogical_choice(
            units, act, context, text, protected=protected or mode == "concept_review"
        )
        if pedagogical is not None:
            choice = pedagogical
        if act.primary_act == "greeting":
            choice = choice.__class__(notice="didactic_greeting", topic_ref=context.current_topic_ref)
        elif re.fullmatch(
            (
                "[¿? ]*(?:dime (?:que sabes|lo que sabes)|que sabes|que podemos estudia"
                "r|hablame) (?:sobre|de|del)? ?(?:el agua|agua|el programa|programa|est"
                "a asignatura)[¿? .]*"
            ),
            normalized(text),
        ):
            choice = choice.__class__(notice="didactic_overview", topic_ref=context.current_topic_ref)
    if (
        advanced_active
        and not semantic_study_mode
        and not (navigation and (navigation.notice or navigation.act))
        and dialogue_control is None
    ):
        from oralia.domain.dialogue.package_dialogue import package_choice

        package_selected, package_updates = package_choice(units, act, context, text, protected=protected)
        if continuity_active:
            from oralia.domain.dialogue.continuity import select

            natural_selected, natural_updates = select(
                units,
                act,
                context,
                text,
                protected=protected,
                initial_question=(
                    config.initial_questions[0] if defense and config.initial_questions else None
                ),
            )
            if natural_selected is not None:
                package_selected, package_updates = natural_selected, natural_updates
        if package_selected is not None:
            choice = package_selected
            pedagogical = package_selected if package_selected.unit_id else None
            context = context.model_copy(update=package_updates)
    if (
        configured_runtime is not None
        and mode in {"doubt_resolution", "guided_explanation"}
        and not protected
        and dialogue_control is None
        and requested_topic is None
        and text.strip()
        and act.primary_act not in {"greeting", "mode_switch", "topic_switch", "finish"}
        and not (navigation and (navigation.notice or navigation.act))
    ):
        turn_budget_ms = configured_runtime.turn_budget_ms
        semantic_base_version = state.version
        remaining = min(
            turn_budget_ms - int((time.monotonic() - started) * 1000),
            int((activity.max_duration_seconds - (utcnow() - session.started_at).total_seconds()) * 1000),
        )
        semantic_result = await configured_runtime.propose(db, session, text, context, deadline_ms=remaining)
        db.refresh(state)
        if state.version != semantic_base_version:
            raise ValueError("El estado cambió durante la propuesta semántica; no se confirma el turno.")
        configured_runtime.revalidate(db, session, semantic_result.selection)
        selection = semantic_result.selection
        notice_value = "close_confirm" if selection.notice == "finish" else selection.notice
        if selection.notice == "finish":
            context = context.model_copy(update={"close_confirmation_pending": True})
        refs = selection.unit_ids
        chosen = next((unit for unit in units if refs and unit.id == refs[0]), None)
        choice = GuidedChoice(
            unit_id=refs[0] if refs else None,
            additional_unit_ids=refs[1:],
            topic_ref=chosen.topic_ref if chosen else context.current_topic_ref,
            notice=notice_value,
            support_step=selection.support_step,
        )
        act = DialogueAct(
            primary_act={
                "explain": "content_question",
                "correct": "comparison",
                "respond": "content_answer",
                "ask": "help",
                "finish": "ambiguous",
                "clarify": "ambiguous",
            }.get(semantic_result.act, semantic_result.act),
            reason_code="content_input",
        )
        record_event(
            db,
            session_id=session.id,
            turn_id=turn.id,
            event_type="guided_semantic_proposal",
            agent_id="study-intent-interpreter",
            memory_category="procedural",
            payload={
                "contract_version": semantic_result.contract_version,
                "act": semantic_result.act,
                "proposal_only": True,
            },
        )
    notice = (navigation.notice if navigation else None) or choice_notice or choice.notice
    if not units:
        notice = navigation.notice if navigation and navigation.notice else "unavailable"
        context = DialogueContext(
            effective_profile="degraded",
            stalled_count=context.stalled_count,
            last_notice=context.last_notice,
            schema_version=context.schema_version,
            navigation_page=context.navigation_page,
            pending_conservation=context.pending_conservation,
            close_confirmation_pending=context.close_confirmation_pending,
        )
    elapsed = (utcnow() - session.started_at).total_seconds()
    limited = session.turn_count + 1 >= activity.max_turns or elapsed >= activity.max_duration_seconds
    if limited or act.primary_act == "finish" and not (navigation and navigation.notice != "finish"):
        notice = "finish"
    selected = next((u for u in units if u.id == choice.unit_id), None) if notice is None else None
    grounding = coherence = disclosure = "not_applicable"
    sources = []
    if selected:
        rendered = [selected, *[u for ref in choice.additional_unit_ids for u in units if u.id == ref]]
        entry = {
            1: MATERIAL_FRAGMENT_RESPONSE,
            2: MATERIAL_FRAGMENT_RESPONSE_2,
            3: MATERIAL_FRAGMENT_RESPONSE_3,
        }.get(len(rendered))
        if entry is None:
            raise ValueError("renderer supports one to three distinct reviewed units")
        if continuity_active and len(rendered) == 1:
            from oralia.domain.dialogue.continuity import interpret

            if interpret(text, context, units).greeting:
                entry = GREETED_REVIEWED_RESPONSE
        if semantic_result is not None:
            if semantic_result.selection.response_question_ref is not None:
                entry = SEMANTIC_RECEIPT
            elif semantic_result.greet:
                entry = SEMANTIC_GREETING_TEMPLATES[len(rendered)]
        plan = ProposalPlan(
            template_id=entry.template_id,
            template_version="1",
            template_sha256=entry.sha256,
            action=act.primary_act,
            unit_refs=tuple(u.id for u in rendered),
            transformation="compose_reviewed_units" if len(rendered) > 1 else "select_reviewed_unit",
        )
        try:
            snapshot, proposal = ReviewedUnitGenerationAdapter(
                db, catalog=SEMANTIC_TEMPLATE_CATALOG if semantic_policy else GUIDED_CATALOG
            ).render(
                DialogueGenerationRequest(
                    plan=plan, session_id=session.id, turn_id=turn.id, base_version=state.version
                )
            )
        except TimeoutError:
            selected = None
            notice = "unavailable"
            record_event(
                db,
                session_id=session.id,
                turn_id=turn.id,
                event_type="guided_provider_unavailable",
                payload={"reason_codes": ["renderer_timeout"]},
                memory_category="procedural",
            )
    if selected:
        # A closed greeting prefix is independently authorized by T090; academic
        # verifiers still inspect every academic clause from the bound units.
        verified_text = (
            " ".join(unit.reviewed_content for unit in rendered)
            if entry.template_id in {item.template_id for item in SEMANTIC_GREETING_TEMPLATES.values()}
            or entry.template_id == SEMANTIC_RECEIPT.template_id
            else proposal.text
        )
        evidence = [
            {"unit_id": unit.id, "provenance": "teacher_reviewed", "text": unit.reviewed_content}
            for unit in rendered
        ]
        source_refs = {ref["fragment_id"]: ref for unit in rendered for ref in unit.source_refs}
        for ref in source_refs.values():
            fragment = db.get(models.MaterialFragment, ref["fragment_id"])
            evidence.append({"fragment_id": fragment.id, "text": ""})
            visible_text = ""
            if not protected:
                try:
                    disclosed = authorized_fragment(
                        db,
                        session,
                        fragment.id,
                        ScopeReference(
                            topic_ref="activity", purpose_ref="material_response", action_ref="respond"
                        ),
                    )
                    visible_text = disclosed.text
                except ValueError:
                    pass  # Reviewed-unit permission never implies raw source disclosure.
            sources.append(
                {
                    "document_id": fragment.document_id,
                    "document_version": fragment.document_version,
                    "location_ref": fragment.location_ref,
                    "fragment_text": visible_text,
                    "content_withheld": not bool(visible_text),
                }
            )
        grounded = await call(
            GroundingVerifierAgent(db),
            {
                "dialogue_schema_version": 2,
                "proposal_text": verified_text,
                "evidence": evidence,
                "general_knowledge_allowed": False,
            },
        )
        grounding = (grounded.output or {}).get("verdict", "unavailable")
        prior_id = (
            context.pending_question_turn_id
            if act.primary_act == "repeat"
            and act.repeat_target in {None, "question"}
            and context.pending_question_turn_id
            else context.last_approved_turn_id
        )
        prior = db.get(models.Turn, str(prior_id)) if prior_id else None
        repeated = act.primary_act == "repeat" and prior is not None and prior.output_text == proposal.text
        coherent = await call(
            CoherenceVerifierAgent(),
            {
                "proposal_text": verified_text,
                "prior_statements": [prior.output_text] if prior and prior.output_text else [],
                "active_sources": [u.reviewed_content for u in rendered],
                "concepts_addressed": [selected.topic_ref],
                "turn_number": session.turn_count,
                "max_turns": activity.max_turns,
                "dialogue_schema_version": 3 if advanced_active else 2,
                "intentional_repeat": repeated,
                "requested_focus": (
                    "repeat_component"
                    if act.primary_act == "repeat"
                    and act.repeat_target in {"explanation", "example", "comparison", "hint"}
                    and selected.id in {str(ref) for ref in context.last_approved_unit_ids}
                    and selected.kind == act.repeat_target
                    else act.primary_act
                ),
                "focused_reviewed_unit": rendered[0].reviewed_content if len(rendered) == 1 else None,
                "structural_progress": bool(
                    not context.last_approved_unit_ids
                    or str(context.last_approved_unit_ids[0]) != selected.id
                    or repeated
                ),
            },
        )
        coherence = (coherent.output or {}).get("verdict", "unavailable")
        disclosure = "approved"
        if protected:
            answers = [
                u.reviewed_content
                for u in units
                if u.topic_ref == selected.topic_ref and u.reveal_policy in {"solution", "study_only"}
            ]
            hidden = await call(
                SolutionNonDisclosureVerifierAgent(),
                {
                    "dialogue_schema_version": 2,
                    "question_text": verified_text,
                    "internal_expected_answers": answers,
                },
            )
            disclosure = (hidden.output or {}).get("verdict", "unavailable")
        if grounding != "fundamentada" or coherence != "approved" or disclosure != "approved":
            notice = "verification_failed"
            selected = None
            sources = []
    # Recheck duration after awaited work. A response prepared beyond the session
    # limit cannot escape merely because the limit was checked before verification.
    if (utcnow() - session.started_at).total_seconds() >= activity.max_duration_seconds:
        limited = True
        notice = "finish"
        selected = None
        sources = []
    if not selected:
        notice = notice or "limited"
        # A repeated orientation is replaced by a concrete clarification, never a loop.
        if notice == "orientation" and context.stalled_count and not (navigation and navigation.notice):
            notice = "clarify"
        if notice == context.last_notice and notice != "finish" and not (navigation and navigation.notice):
            notice = "unavailable_repeat" if not units else "clarify" if notice == "recovery" else "recovery"
        snapshot, proposal = _notice(
            db,
            session,
            activity,
            notice,
            context=context,
            units=units,
            topic=choice.pending_topic,
            chosen=navigation.privacy_choice if navigation and notice == "privacy_confirmed" else None,
        )
        if (
            screenless_enabled(activity, session.participant_code)
            and protected
            and notice
            in {
                "orientation",
                "clarify",
                "unknown_topic",
                "confirm_topic",
                "sources",
                "sources_more",
                "didactic_greeting",
                "didactic_overview",
                "package_welcome",
                "outside_source",
                "package_topic_confirmed",
                "followups_exhausted",
            }
        ):
            answers = [u.reviewed_content for u in units if u.reveal_policy in {"solution", "study_only"}]
            hidden = await call(
                SolutionNonDisclosureVerifierAgent(),
                {
                    "dialogue_schema_version": 2,
                    "question_text": proposal.text,
                    "internal_expected_answers": answers,
                },
            )
            disclosure = (hidden.output or {}).get("verdict", "unavailable")
            if disclosure != "approved":
                notice = "recovery" if context.last_notice == "limited" else "limited"
                snapshot, proposal = _notice(db, session, activity, notice, context=context, units=units)
    # Metadata verification is awaited too: it cannot extend the turn/session budget.
    if navigation and (time.monotonic() - started) * 1000 >= turn_budget_ms:
        context = navigation_before_context
        selected, sources, rendered = None, [], []
        navigation = None
        notice = "verification_failed"
        snapshot, proposal = _notice(db, session, activity, notice, context=context, units=units)
    if (
        screenless_enabled(activity, session.participant_code)
        and (utcnow() - session.started_at).total_seconds() >= activity.max_duration_seconds
    ):
        limited = True
        notice = "finish"
        selected, sources, rendered = None, [], []
        snapshot, proposal = _notice(db, session, activity, notice, context=context, units=units)
    if semantic_result is not None:
        db.refresh(state)
        if state.version != semantic_base_version:
            raise ValueError("El estado cambió durante la verificación semántica; no se publica el turno.")
        configured_runtime.revalidate(db, session, semantic_result.selection)
    decision = decide_final_output(
        snapshot,
        proposal,
        catalog=SEMANTIC_TEMPLATE_CATALOG if semantic_policy else GUIDED_CATALOG,
        allow_operational_attempt=False,
    )
    if semantic_result is not None and decision.blocked:
        selected, sources, rendered = None, [], []
        notice = "verification_failed"
    if decision.output_text is not None and navigation and navigation.privacy_choice and not limited:
        from oralia.application.services.session_privacy_service import set_privacy_preference

        scopes = CHOICES[navigation.privacy_choice][2]
        set_privacy_preference(db, session, retain=bool(scopes), scope=scopes)
    if screenless_enabled(activity, session.participant_code):
        preference = db.get(models.SessionPrivacyPreference, session.id)
        closure_retain = bool(preference and preference.retain)
        closure_scope = preference.scope if closure_retain else []
        from oralia.application.services.session_privacy_service import (
            set_privacy_preference,
            validate_privacy_choice,
        )

        try:
            validate_privacy_choice(db, session, retain=closure_retain, scope=closure_scope)
        except ValueError:
            # Revocation can only reduce retention; it never supplies consent.
            closure_retain, closure_scope = False, []
            set_privacy_preference(db, session, retain=False, scope=[])
    effective_provider = "reviewed-unit-renderer/v1" if selected else "fixed-dialogue-template/v1"
    persist_final_output(db, turn, decision, generator_agent_id=effective_provider)
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
        turn_id=turn.id,
        action_type=action,
        chosen_by_agent_id="defense-agency" if defense else "self-study-agency-composer",
    )
    db.add(dialogue)
    db.flush()
    turn.dialogue_action_id = dialogue.id
    session.turn_count += 1
    turn.ended_at = utcnow()
    turn.latency_ms = int((time.monotonic() - started) * 1000)
    updated = context.model_dump(mode="json")
    updated["last_notice"] = notice
    updated["intent_hypotheses"] = [
        {"label": act.primary_act, "confidence_kind": "heuristic", "reason_code": act.reason_code}
    ]
    if selected:
        if selected.subgoal_ref != context.current_subgoal_ref:
            updated["claim_followup"] = None
        updated.update(
            current_topic_ref=selected.topic_ref,
            current_subgoal_ref=selected.subgoal_ref,
            content_query=(
                text[:500]
                if (act.primary_act == "content_question" and act.reason_code != "explicit_control")
                or (pedagogical is not None and act.primary_act not in {"rephrase", "help", "repeat"})
                else context.content_query or selected.topic_ref
            ),
            last_approved_unit_ids=[u.id for u in rendered],
            last_approved_turn_id=turn.id,
            candidate_referents=[{"kind": "topic", "ref": selected.topic_ref}],
            selected_referent=None,
            relevant_concepts=[selected.topic_ref],
            pending_topic_ref=None,
            support_step=choice.support_step,
            effective_profile="guided_controlled",
        )
        if choice.is_question and (
            selected.topic_ref != context.current_topic_ref
            or act.primary_act not in {"repeat", "rephrase", "content_answer"}
        ):
            updated.update(
                pending_question_unit_id=selected.id, pending_question_turn_id=turn.id, claim_followup=None
            )
        if act.primary_act == "rephrase" and context.pending_question_unit_id:
            # Rephrasing changes wording, not the main question or its hint ladder.
            updated["last_approved_unit_ids"] = [selected.id]
        original_question = next((u for u in units if u.id == str(context.pending_question_unit_id)), None)
        if (
            protected
            and act.primary_act == "content_answer"
            and text.strip()
            and original_question is not None
            and selected.id in original_question.relations.get("rephrases", [])
            and selected.subgoal_ref == original_question.subgoal_ref
        ):
            updated["claim_followup"] = {
                "participant_turn_id": turn.id,
                "question_unit_id": original_question.id,
                "followup_unit_id": selected.id,
                "subgoal_ref": selected.subgoal_ref,
                "source_fragment_ids": list(
                    dict.fromkeys(ref["fragment_id"] for ref in selected.source_refs)
                ),
                "assessment": "not_assessed",
            }
        if semantic_result is not None:
            selection = semantic_result.selection
            prior_pair = tuple(context.relevant_concepts) if len(context.relevant_concepts) == 2 else ()
            next_pair = tuple(
                ref for ref in [selection.goal_ref, selection.comparison_goal_ref] if ref is not None
            )
            updated["relevant_concepts"] = list(next_pair)
            if selection.response_question_ref is not None:
                updated.update(
                    pending_question_unit_id=None, pending_question_turn_id=None, claim_followup=None
                )
                record_event(
                    db,
                    session_id=session.id,
                    turn_id=turn.id,
                    event_type="guided_semantic_message_received",
                    memory_category="procedural",
                    payload={
                        "question_unit_id": selection.response_question_ref,
                        "feedback_unit_id": selected.id,
                        "assessment": "not_assessed",
                    },
                )
            elif selection.question_ref is not None:
                updated.update(
                    pending_question_unit_id=selection.question_ref,
                    pending_question_turn_id=turn.id,
                    claim_followup=None,
                )
            elif selection.goal_ref != context.current_subgoal_ref or (
                prior_pair and prior_pair != next_pair
            ):
                updated.update(
                    pending_question_unit_id=None, pending_question_turn_id=None, claim_followup=None
                )
    elif choice.pending_topic and not (navigation and navigation.notice):
        updated["pending_topic_ref"] = choice.pending_topic
    if notice in {"verification_failed", "unavailable", "unavailable_repeat"}:
        updated["effective_profile"] = "degraded"
    next_context = DialogueContext.model_validate(updated)
    next_context = after_output(
        next_context,
        action=act.primary_act,
        approved_text=decision.output_text or "",
        evidence_ids=tuple(u.id for u in [selected] if u),
        progressed=selected is not None and coherence == "approved",
    )
    if not units:
        next_context = next_context.model_copy(update={"offered_actions": ("finish",)})
    db.flush()
    db.refresh(state)
    if semantic_result is not None and state.version != semantic_base_version:
        raise ValueError("Conflicto de estado semántico; no se confirma el turno.")
    if decision.output_text is not None:
        context_patch = update_context(db, session.id, state.version, next_context, CancellationToken())
        if not context_patch.applied:
            raise ValueError("dialogue context conflict")
        patch = apply_patch(
            db,
            session_id=session.id,
            base_version=context_patch.resulting_version,
            proposed_by_agent_id="defense-agency" if defense else "self-study-agency-composer",
            element_type="decision",
            payload={
                "current_input": text,
                "participant_response": decision.output_text,
                "turn_number": session.turn_count,
                "concepts_addressed": (
                    list(dict.fromkeys([*state.concepts_addressed, selected.topic_ref]))[-8:]
                    if selected
                    else state.concepts_addressed
                ),
                "next_action_proposed": action,
            },
            justification="guided approved output",
        )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="guided_dialogue_decision",
        payload={
            "schema_version": 2,
            "primary_act": act.primary_act,
            "repeat_target": act.repeat_target,
            "claim_followup": (
                next_context.claim_followup.model_dump(mode="json") if next_context.claim_followup else None
            ),
            "navigation_command": navigation.notice if navigation else None,
            "control_source": (
                "structured_control"
                if dialogue_control is not None
                else (
                    "conversation_navigation"
                    if navigation and (navigation.notice or navigation.act)
                    else "text_interpretation"
                )
            ),
            "reason_code": act.reason_code,
            "profile": "guided_controlled",
            "provider": effective_provider,
            "unit_ids": [u.id for u in rendered] if selected else [],
            "notice": notice,
            "grounding_verdict": grounding,
            "coherence_verdict": coherence,
            "non_disclosure_verdict": disclosure,
        },
        memory_category="procedural",
    )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="agents_selected",
        payload={
            "mode": mode,
            "activated_steps": [
                {"step_id": name, "agent_id": name}
                for name in [
                    "study-intent-interpreter",
                    *(["grounding-verifier", "coherence-verifier"] if selected else []),
                    "constitutional-control",
                ]
            ],
        },
        memory_category="procedural",
    )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="generation_call",
        payload={
            "adapter": "guided_controlled",
            "provider": effective_provider,
            "model": None,
            "fallback_used": False,
            "fragment_ids": list(
                dict.fromkeys(
                    ref["fragment_id"] for unit in (rendered if selected else []) for ref in unit.source_refs
                )
            ),
        },
        latency_ms=turn.latency_ms,
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
        "sources": sources if decision.output_text is not None else [],
        "mode": mode,
        "dialogue_action": action,
        "session_status": session.status,
        "summary": summary,
        "dialogue_status": {
            "screenless_text_ready": screenless_enabled(activity, session.participant_code),
            "conservation": (
                {"retain": closure_retain, "scope": closure_scope}
                if screenless_enabled(activity, session.participant_code)
                else None
            ),
            "available_modes": [] if defense else list(config.enabled_modes),
            "effective_profile": next_context.effective_profile,
            "provider": effective_provider,
            "primary_act": act.primary_act,
            "repeat_target": act.repeat_target,
            "support_step": next_context.support_step,
            "pending_topic": next_context.pending_topic_ref,
            "claim_followup": (
                next_context.claim_followup.model_dump(mode="json") if next_context.claim_followup else None
            ),
            "pending_question": pending_question_view(db, session, next_context),
            "rendered_unit_ids": [u.id for u in rendered] if selected else [],
            "notice": notice,
            "grounding_verdict": grounding,
            "coherence_verdict": coherence,
            "non_disclosure_verdict": disclosure,
            "latency_ms": turn.latency_ms,
            "turn_budget_ms": turn_budget_ms,
            **(
                {
                    "semantic_candidate": True,
                    "semantic_act": semantic_result.act,
                    "semantic_contract_version": semantic_result.contract_version,
                    "response_received_question_id": (
                        semantic_result.selection.response_question_ref if selected is not None else None
                    ),
                }
                if semantic_result is not None
                else {}
            ),
            "available_topics": [] if protected else sorted({u.topic_ref for u in units}),
            "offered_actions": list(next_context.offered_actions),
        },
    }
