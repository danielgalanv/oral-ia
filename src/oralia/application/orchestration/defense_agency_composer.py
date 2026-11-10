"""Single oral-defense composition with retrieval, independent verifiers and T090."""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.end_defense_session import end_defense_session, validate_defense_retention
from oralia.application.orchestration.agency_composer import execute_agency
from oralia.application.orchestration.final_output_gate import (
    FinalOutputDecision,
    decide_final_output,
    persist_final_output,
)
from oralia.application.orchestration.output_authorization_context import (
    AuthorizationReferenceInput,
    InvalidAuthorizationContext,
    build_authorization_snapshot,
)
from oralia.application.orchestration.output_proposal_builder import (
    BoundTemplateSlot,
    ProposalConstructionError,
    build_output_proposal,
)
from oralia.application.services.activity_generation_context import configured_generation
from oralia.application.services.trace_service import record_event
from oralia.domain.agencies.agency import AgencyDefinition, ExecutionStep
from oralia.domain.agents.agent_contract import AgentRequest
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent
from oralia.domain.agents.fallback_agent import SafeFallbackAgent
from oralia.domain.agents.followup_question_agent import FollowUpQuestionAgent
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent
from oralia.domain.agents.practice_question_agent import PracticeQuestionAgent
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.policies.output_authorization_contract import AuthorizationReason, ScopeReference
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    DEFENSE_CLARIFICATION,
    DEFENSE_DYNAMIC_OUTPUT,
    DEFENSE_INITIAL_QUESTION,
    DEFENSE_LIMIT_CLOSE,
    DEFENSE_MISSING_INFORMATION,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.generation import config as generation_config


@dataclass(slots=True)
class DefenseTurnResult:
    turn_id: str
    dialogue_action: str
    dialogue_purpose: str | None
    output_text: str | None
    blocked: bool
    state_version: int | None
    status: str
    sources: list[dict] = field(default_factory=list)
    general_knowledge_used: bool = False
    defense_summary: dict | None = None
    session_status: str = "active"
    dialogue_status: dict | None = None


def _concepts(text: str) -> list[str]:
    words = [word.strip(".,;:!?¡¿()[]").lower() for word in text.split()]
    stopwords = {
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
        "de",
        "del",
        "que",
        "por",
        "con",
        "para",
        "es",
        "se",
        "en",
    }
    significant = [word for word in words if len(word) >= 2 and word not in stopwords]
    return list(dict.fromkeys(significant[:6]))


def _structurally_relevant(
    referenced_concept: str,
    concepts_mentioned: list[str],
    evidence: list[dict],
) -> bool:
    needle = referenced_concept.strip().lower()
    if not needle:
        return False
    if any(needle == concept.lower() or needle in concept.lower() for concept in concepts_mentioned):
        return True
    return any(needle in str(item.get("text", "")).lower() for item in evidence)


def _combined_action(grounding_verdict: str, coherence_verdict: str, relevant: bool) -> str:
    if not relevant or grounding_verdict not in {"fundamentada", "parcialmente_fundamentada"}:
        return "acknowledge_missing_info"
    if coherence_verdict == "approved":
        return "ask"
    if coherence_verdict == "reformulate":
        return "regenerate"
    return "acknowledge_missing_info"


def _generation_metadata(result) -> dict:
    trace = (result.output or {}).get("generation_trace", {})
    if not isinstance(trace, dict):
        trace = {}
    adapter = trace.get("adapter")
    if not isinstance(adapter, str) or adapter not in {"ollama", "deterministic"}:
        adapter = None
    return {
        "status": result.status,
        "adapter": adapter,
        "model": generation_config.get_ollama_model() if adapter == "ollama" else None,
        "fallback_used": trace.get("fallback_used") is True,
        "parameters": (
            {
                "max_tokens": generation_config.get_ollama_max_tokens(),
                "temperature": generation_config.get_ollama_temperature(),
            }
            if adapter == "ollama"
            else {}
        ),
    }


def _deadline_request(session_id: str, turn_id: str, payload: dict, deadline_ms: int) -> AgentRequest:
    return AgentRequest(
        session_id=uuid.UUID(session_id),
        turn_id=uuid.UUID(turn_id),
        input=payload,
        deadline_ms=deadline_ms,
    )


def _trace_agent(db: SASession, session_id: str, turn_id: str, agent, result) -> None:
    contract = getattr(agent, "contract", None)
    agent_id = getattr(contract, "agent_id", type(agent).__name__)
    record_event(
        db,
        session_id=session_id,
        turn_id=turn_id,
        event_type="agent_execution",
        agent_id=agent_id,
        payload={
            "status": result.status,
            "agent_version": getattr(contract, "version", None),
            "error_code": result.status if result.error else None,
            # Agent-controlled free text may contain the rejected candidate.
            # Only the status and typed error identity cross this persistence boundary.
        },
        memory_category="procedural",
    )


def _prepare_gate(session, activity, candidate, entry):
    if candidate is None:
        try:
            return build_authorization_snapshot(session, activity), None, None
        except InvalidAuthorizationContext:
            return None, None, AuthorizationReason.INVALID_CONTEXT
    references: tuple[AuthorizationReferenceInput, ...] = ()
    slots: tuple[BoundTemplateSlot, ...] = ()
    if entry in {DEFENSE_DYNAMIC_OUTPUT, DEFENSE_INITIAL_QUESTION}:
        references = (
            AuthorizationReferenceInput(
                data_ref="defense-candidate",
                category="generated_defense",
                provenance="defense-agency",
                recipient=session.participant_code,
                scope=ScopeReference(topic_ref="activity", purpose_ref="oral_defense", action_ref="ask"),
                value=candidate,
            ),
        )
        slots = (BoundTemplateSlot(placeholder="content", data_ref="defense-candidate"),)
    try:
        snapshot = build_authorization_snapshot(
            session, activity, data_references=references, catalog=DEFAULT_OUTPUT_TEMPLATE_CATALOG
        )
        proposal = build_output_proposal(
            snapshot,
            template_id=entry.template_id,
            template_version=entry.version,
            template_sha256=entry.sha256,
            slots=slots,
        )
        return snapshot, proposal, None
    except (InvalidAuthorizationContext, ProposalConstructionError, TypeError, ValueError):
        return None, None, AuthorizationReason.INVALID_CONTEXT


def _duration_limit_reached(session: models.Session, activity: models.ActivityConfiguration) -> bool:
    return _remaining_duration_ms(session, activity) <= 0


def _remaining_duration_ms(session: models.Session, activity: models.ActivityConfiguration) -> int:
    started = session.started_at
    now = utcnow()
    if started.tzinfo is None and now.tzinfo is not None:
        now = now.replace(tzinfo=None)
    return max(0, int((activity.max_duration_seconds - (now - started).total_seconds()) * 1000))


async def _run_agent(db, session, turn, agent, payload):
    agent_id = getattr(agent.contract, "agent_id", type(agent).__name__)
    role = (
        "retriever"
        if agent_id == "material-retriever"
        else ("verifier" if "verifier" in agent_id else "generator")
    )
    fallback = SafeFallbackAgent()
    agency = AgencyDefinition(
        id="defense-agency",
        name="DefenseAgency",
        version="1.0.0",
        steps=[
            ExecutionStep(step_id="current", agent_id=agent_id, role=role),
            ExecutionStep(step_id="safe", agent_id="safe-fallback", role="presenter"),
        ],
        fallback_step="safe",
        verifiers_required=["current"] if role == "verifier" else [],
        termination_rule="one bounded step, independently verified before publication",
    )
    registry = {agent_id: agent, "safe-fallback": fallback}
    outcome = await execute_agency(
        agency,
        registry,
        lambda step, _: _deadline_request(
            session.id,
            turn.id,
            payload if step.step_id == "current" else {},
            min(
                registry[step.agent_id].contract.timeout_ms,
                _remaining_duration_ms(
                    session, db.get(models.ActivityConfiguration, session.activity_configuration_id)
                ),
            ),
        ),
    )
    for step in outcome.steps:
        _trace_agent(db, session.id, turn.id, registry[step.agent_id], step.result)
    if outcome.steps[0].result.status == "cancelled":
        raise asyncio.CancelledError
    return outcome.steps[0].result


@configured_generation
async def run_defense_turn(
    db: SASession,
    session: models.Session,
    input_text: str,
    *,
    followup_agent=None,
    material_retriever_agent=None,
    grounding_verifier_agent=None,
    coherence_verifier_agent=None,
    requested_topic: str | None = None,
    practice_question_agent=None,
    closure_retain: bool = False,
    closure_scope: list[str] | None = None,
    dialogue_control=None,
) -> DefenseTurnResult:
    from oralia.application.services.guided_dialogue_service import is_guided, run_guided_turn

    if is_guided(db, session.activity_configuration_id):
        value = await run_guided_turn(
            db,
            session,
            input_text,
            defense=True,
            closure_retain=closure_retain,
            closure_scope=closure_scope,
            requested_topic=requested_topic,
            dialogue_control=dialogue_control,
        )
        return DefenseTurnResult(
            **{
                key: value[key]
                for key in (
                    "turn_id",
                    "dialogue_action",
                    "output_text",
                    "blocked",
                    "state_version",
                    "status",
                    "sources",
                    "session_status",
                    "dialogue_status",
                )
            },
            dialogue_purpose="deepen_current_topic" if value["dialogue_action"] == "ask" else None,
            defense_summary=value["summary"],
        )
    if dialogue_control is not None:
        raise ValueError("Los controles estructurados requieren una actividad con perfil guiado.")
    if session.status != "active":
        raise ValueError("defense session is not active")
    started = time.monotonic()
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    config = (
        db.query(models.DefenseActivityConfig).filter_by(activity_configuration_id=activity.id).one_or_none()
    )
    validate_defense_retention(db, session, config, retain=closure_retain, scope=closure_scope)
    if requested_topic is not None and (config is None or requested_topic not in config.topics):
        raise ValueError("requested topic is outside authorized scope")
    turn = models.Turn(
        session_id=session.id,
        index=session.turn_count,
        input_text=input_text,
        status="in_progress",
        started_at=utcnow(),
    )
    db.add(turn)
    db.flush()
    state = get_or_create(db, session.id, activity_ref=activity.id)
    concepts = _concepts(input_text)
    prior_turns = (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session.id, models.Turn.id != turn.id)
        .order_by(models.Turn.index.asc())
        .all()
    )
    prior_answers = [
        item.input_text
        for item in prior_turns
        if item.input_text
        and (
            not item.dialogue_action_id
            or db.get(models.DialogueAction, item.dialogue_action_id).action_type != "clarify"
        )
    ]
    prior_questions = [item.output_text for item in prior_turns if item.output_text]

    requested_action = "ask"
    purpose: str | None = None
    candidate: str | None = None
    entry = DEFENSE_DYNAMIC_OUTPUT
    upstream = "ok"
    evidence: list[dict] = []
    combined_payload: dict[str, object] = {}

    limit_reached = session.turn_count + 1 >= activity.max_turns or _duration_limit_reached(session, activity)
    if limit_reached:
        candidate = DEFENSE_LIMIT_CLOSE.text
        requested_action = "finish"
        purpose = None
        entry = DEFENSE_LIMIT_CLOSE
    elif session.turn_count == 0 and not input_text.strip():
        entry = DEFENSE_INITIAL_QUESTION
        if config and config.initial_questions:
            candidate = config.initial_questions[0]
        else:
            retriever = material_retriever_agent or MaterialRetrieverAgent(db)
            retrieval = await _run_agent(
                db,
                session,
                turn,
                retriever,
                {
                    "query_text": activity.objective,
                    "course_id": activity.course_id,
                    "activity_configuration_id": activity.id,
                    "session_id": session.id,
                    "max_fragments": 5,
                    "time_budget_ms": min(retriever.contract.timeout_ms, 3000),
                },
            )
            evidence = (
                list(retrieval.output.get("fragments", []))
                if retrieval.status == "ok" and retrieval.output
                else []
            )
            if evidence:
                initial_agent = practice_question_agent or PracticeQuestionAgent()
                generated = await _run_agent(
                    db,
                    session,
                    turn,
                    initial_agent,
                    {
                        "objective_ref": activity.objective,
                        "concepts": config.topics if config else [],
                        "evidence": evidence,
                        "previous_questions": [],
                        "reveals_solution": False,
                    },
                )
                record_event(
                    db,
                    session_id=session.id,
                    turn_id=turn.id,
                    event_type="generation_call",
                    agent_id="practice-question-agent",
                    payload={**_generation_metadata(generated), "purpose": "pregunta_practica"},
                    memory_category="procedural",
                )
                if generated.status == "ok" and generated.output:
                    candidate = str(generated.output.get("question_text", ""))
                    grounding = await _run_agent(
                        db,
                        session,
                        turn,
                        grounding_verifier_agent or GroundingVerifierAgent(db),
                        {
                            "proposal_text": candidate,
                            "evidence": evidence,
                            "general_knowledge_allowed": False,
                        },
                    )
                    coherence = await _run_agent(
                        db,
                        session,
                        turn,
                        coherence_verifier_agent or CoherenceVerifierAgent(),
                        {
                            "proposal_text": candidate,
                            "prior_statements": [],
                            "active_sources": [item.get("text", "") for item in evidence],
                        },
                    )
                    if not (
                        grounding.status == "ok"
                        and grounding.output
                        and grounding.output.get("verdict") in {"fundamentada", "parcialmente_fundamentada"}
                        and coherence.status == "ok"
                        and coherence.output
                        and coherence.output.get("verdict") == "approved"
                    ):
                        candidate = None
                    combined_payload = {
                        "grounding_verdict": (
                            grounding.output.get("verdict") if grounding.output else "not_run"
                        ),
                        "coherence_verdict": (
                            coherence.output.get("verdict") if coherence.output else "not_run"
                        ),
                        "dialogue_action": "ask" if candidate else "acknowledge_missing_info",
                    }
            if not candidate:
                candidate = DEFENSE_MISSING_INFORMATION.text
                entry = DEFENSE_MISSING_INFORMATION
                requested_action = "acknowledge_missing_info"
                purpose = None
                combined_payload = {
                    **combined_payload,
                    "dialogue_action": requested_action,
                    "reason": "initial_continuation_unavailable",
                }
    elif not concepts:
        candidate = DEFENSE_CLARIFICATION.text
        requested_action = "clarify"
        purpose = None
        entry = DEFENSE_CLARIFICATION
        combined_payload = {"reason": "empty_concepts", "dialogue_action": requested_action}
    else:
        coherence_agent = coherence_verifier_agent or CoherenceVerifierAgent()
        answer_coherence = await _run_agent(
            db,
            session,
            turn,
            coherence_agent,
            {
                "proposal_text": input_text,
                "prior_statements": prior_answers,
                "active_sources": [],
                "concepts_addressed": list(state.concepts_addressed),
                "turn_number": session.turn_count,
                "max_turns": activity.max_turns,
            },
        )
        answer_incidents = (
            list(answer_coherence.output.get("incident_types", []))
            if answer_coherence.status == "ok" and answer_coherence.output
            else []
        )
        if "contradiccion" in answer_incidents:
            candidate = DEFENSE_CLARIFICATION.text
            requested_action = "clarify"
            purpose = None
            entry = DEFENSE_CLARIFICATION
            combined_payload = {
                "reason": "cognitive_contradiction",
                "dialogue_action": requested_action,
            }
        else:
            retriever = material_retriever_agent or MaterialRetrieverAgent(db)
            retrieval = await _run_agent(
                db,
                session,
                turn,
                retriever,
                {
                    "query_text": f"{requested_topic} {input_text}" if requested_topic else input_text,
                    "course_id": activity.course_id,
                    "activity_configuration_id": activity.id,
                    "session_id": session.id,
                    "max_fragments": 5,
                    "time_budget_ms": min(retriever.contract.timeout_ms, 3000),
                },
            )
            evidence = (
                list(retrieval.output.get("fragments", []))
                if retrieval.status == "ok" and retrieval.output
                else []
            )
            record_event(
                db,
                session_id=session.id,
                turn_id=turn.id,
                event_type="generation_call",
                agent_id="material-retriever",
                payload={
                    "status": retrieval.status,
                    "fragment_ids": [item.get("fragment_id") for item in evidence],
                },
                memory_category="procedural",
            )
            if not evidence and not activity.general_knowledge_allowed:
                candidate = DEFENSE_MISSING_INFORMATION.text
                requested_action = "acknowledge_missing_info"
                purpose = None
                entry = DEFENSE_MISSING_INFORMATION
                combined_payload = {
                    "grounding_verdict": "no_fundamentada",
                    "coherence_verdict": "not_run",
                    "dialogue_action": requested_action,
                }
            else:
                purpose = "switch_topic" if requested_topic is not None else "deepen_current_topic"
                generator = followup_agent or FollowUpQuestionAgent()
                grounding = grounding_verifier_agent or GroundingVerifierAgent(db)
                previous_question = prior_questions[-1] if prior_questions else ""
                for attempt in range(2):
                    generated = await _run_agent(
                        db,
                        session,
                        turn,
                        generator,
                        {
                            "previous_question_text": previous_question,
                            "student_answer_text": input_text,
                            "concepts_mentioned": concepts,
                            "concepts_addressed": list(state.concepts_addressed),
                            "concepts_pending": list(state.concepts_pending),
                            "evidence": evidence,
                            "objective": activity.objective,
                            "purpose": purpose,
                            "target_topic": requested_topic,
                            "general_knowledge_allowed": activity.general_knowledge_allowed,
                        },
                    )
                    record_event(
                        db,
                        session_id=session.id,
                        turn_id=turn.id,
                        event_type="generation_call",
                        agent_id="followup-question-agent",
                        payload={**_generation_metadata(generated), "attempt": attempt},
                        memory_category="procedural",
                    )
                    if generated.status != "ok" or not generated.output:
                        candidate = DEFENSE_MISSING_INFORMATION.text
                        requested_action = "acknowledge_missing_info"
                        purpose = None
                        entry = DEFENSE_MISSING_INFORMATION
                        upstream = "ok"
                        combined_payload = {
                            "generation_status": generated.status,
                            "recovery_action": requested_action,
                        }
                        break
                    generated_text = str(generated.output.get("question_text", ""))
                    referenced = str(generated.output.get("referenced_concept", ""))
                    grounded = await _run_agent(
                        db,
                        session,
                        turn,
                        grounding,
                        {
                            "proposal_text": generated_text,
                            "evidence": evidence,
                            "general_knowledge_allowed": activity.general_knowledge_allowed,
                        },
                    )
                    coherent = await _run_agent(
                        db,
                        session,
                        turn,
                        coherence_agent,
                        {
                            "proposal_text": generated_text,
                            "prior_statements": prior_questions,
                            "active_sources": [item.get("text", "") for item in evidence],
                            "concepts_addressed": list(state.concepts_addressed),
                            "turn_number": session.turn_count,
                            "max_turns": activity.max_turns,
                        },
                    )
                    grounding_verdict = (
                        str(grounded.output.get("verdict"))
                        if grounded.status == "ok" and grounded.output
                        else "no_verificable"
                    )
                    coherence_verdict = (
                        str(coherent.output.get("verdict"))
                        if coherent.status == "ok" and coherent.output
                        else "block"
                    )
                    relevant = _structurally_relevant(referenced, concepts, evidence)
                    resolution = _combined_action(grounding_verdict, coherence_verdict, relevant)
                    if resolution == "ask" and generated_text.strip() in {
                        question.strip() for question in prior_questions
                    }:
                        resolution = "regenerate"
                    combined_payload = {
                        "grounding_verdict": grounding_verdict,
                        "coherence_verdict": coherence_verdict,
                        "referenced_concept": (
                            referenced
                            if referenced in concepts
                            else (concepts[0] if relevant and concepts else None)
                        ),
                        "structurally_relevant": relevant,
                        "attempt": attempt,
                        "dialogue_action": resolution,
                    }
                    if resolution == "regenerate" and attempt == 0:
                        continue
                    if resolution == "ask":
                        candidate = generated_text
                        requested_action = "ask"
                        entry = DEFENSE_DYNAMIC_OUTPUT
                    else:
                        candidate = DEFENSE_MISSING_INFORMATION.text
                        requested_action = "acknowledge_missing_info"
                        purpose = None
                        entry = DEFENSE_MISSING_INFORMATION
                    break

    if _duration_limit_reached(session, activity):
        candidate = DEFENSE_LIMIT_CLOSE.text
        requested_action = "finish"
        purpose = None
        entry = DEFENSE_LIMIT_CLOSE
        combined_payload = {**combined_payload, "dialogue_action": "finish", "reason": "duration_limit"}
    if combined_payload:
        record_event(
            db,
            session_id=session.id,
            turn_id=turn.id,
            event_type="verification_combined",
            agent_id="defense-agency",
            payload=combined_payload,
            memory_category="metacognitive",
        )
    snapshot, proposal, failure = _prepare_gate(session, activity, candidate, entry)
    decision: FinalOutputDecision = decide_final_output(
        snapshot,
        proposal,
        initial_failure_reason=failure,
        upstream_status=upstream,
    )
    persist_final_output(db, turn, decision, generator_agent_id="followup-question-agent")
    action = (
        requested_action
        if decision.output_text is not None and not decision.blocked
        else decision.dialogue_action
    )
    dialogue = models.DialogueAction(
        turn_id=turn.id,
        action_type=action,
        chosen_by_agent_id="defense-agency",
    )
    db.add(dialogue)
    db.flush()
    turn.dialogue_action_id = dialogue.id
    turn.ended_at = utcnow()
    turn.latency_ms = int((time.monotonic() - started) * 1000)
    session.turn_count += 1
    db.add_all([turn, session])

    state_version = None
    if decision.output_text is not None:
        patch = apply_patch(
            db,
            session_id=session.id,
            base_version=state.version,
            proposed_by_agent_id="defense-agency",
            element_type="decision",
            payload={
                "mode": "oral_defense",
                "objective": activity.objective,
                "current_input": input_text,
                "participant_response": decision.output_text,
                "concepts_addressed": list(dict.fromkeys([*state.concepts_addressed, *concepts])),
                "concepts_pending": [
                    topic
                    for topic in (config.topics if config else [])
                    if topic not in concepts and topic not in state.concepts_addressed
                ],
                "retrieved_info": [item["fragment_id"] for item in evidence],
                "open_questions": [decision.output_text] if action == "ask" else [],
                "turn_number": session.turn_count,
                "remaining_time": _remaining_duration_ms(session, activity) // 1000,
                "next_action_proposed": action,
            },
            justification="defense turn completed after independent verification and authorization",
        )
        state_version = patch.resulting_version
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="followup_question_generated",
        agent_id="defense-agency",
        payload={
            "dialogue_action": action,
            "purpose": purpose,
            "blocked": decision.blocked,
            "referenced_concept": combined_payload.get("referenced_concept") if action == "ask" else None,
            "source_concept": state.concepts_addressed[-1] if state.concepts_addressed else None,
            "target_concept": requested_topic or (concepts[0] if concepts else None),
            "reason": "new_authorized_concept" if purpose == "switch_topic" else purpose,
            "evidence_fragment_ids": [item.get("fragment_id") for item in evidence],
        },
        memory_category="procedural",
    )
    record_event(
        db,
        session_id=session.id,
        turn_id=turn.id,
        event_type="turn_completed",
        agent_id="defense-agency",
        payload={"dialogue_action": action, "state_version": state_version},
        memory_category="episodic",
    )
    summary = None
    if decision.output_text is None:
        end_defense_session(
            db, session, config, status="closed_error_safe", retain=closure_retain, scope=closure_scope
        )
    elif requested_action == "finish" and entry is DEFENSE_LIMIT_CLOSE:
        summary = end_defense_session(
            db, session, config, status="closed_limit_reached", retain=closure_retain, scope=closure_scope
        )
    sources = [
        {
            "document_id": item["document_id"],
            "document_version": item["document_version"],
            "location_ref": item["location_ref"],
            "fragment_text": item["text"],
        }
        for item in evidence
    ]
    return DefenseTurnResult(
        turn_id=turn.id,
        dialogue_action=action,
        dialogue_purpose=purpose if action == "ask" else None,
        output_text=decision.output_text,
        blocked=decision.blocked,
        state_version=state_version,
        status=turn.status,
        sources=sources if decision.output_text else [],
        general_knowledge_used=bool(
            action == "ask"
            and entry is DEFENSE_DYNAMIC_OUTPUT
            and not evidence
            and activity.general_knowledge_allowed
        ),
        defense_summary=summary,
        session_status=session.status,
    )


__all__ = [
    "DefenseTurnResult",
    "_combined_action",
    "_structurally_relevant",
    "run_defense_turn",
]
