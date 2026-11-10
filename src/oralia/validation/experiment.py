"""Sequential, synthetic-only experiments over the real application compositor.

Scoped substitutions are confined to this offline module, never imported by the API.
The deterministic model and lexical fixture retriever are declared experimental ports,
not measurements of an LLM or the production vector index.
"""

from __future__ import annotations

import asyncio
import hashlib
import re
import time
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import psutil
from sqlalchemy.orm import Session

from oralia.application.commands.confirm_defense_transcript import confirm_defense_transcript
from oralia.application.commands.end_study_session import end_study_session
from oralia.application.commands.start_session import StartSessionInput, start_session
from oralia.application.commands.submit_defense_voice_turn import (
    TranscriptionUnavailable,
    submit_defense_voice_turn,
)
from oralia.application.commands.submit_study_turn import submit_study_turn
from oralia.application.orchestration import agency_composer
from oralia.application.orchestration import defense_agency_composer as defense_composer
from oralia.application.orchestration import self_study_agency_composer as composer
from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.application.queries.reconstruct_session_trace import reconstruct_session_trace
from oralia.application.services.session_privacy_service import delete_session_content
from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.material_retriever_agent import get_currently_valid_fragment
from oralia.domain.cognitive_state.cognitive_state import get_or_create
from oralia.domain.cognitive_state.state_patch import apply_patch
from oralia.domain.policies.constitutional_control import evaluate
from oralia.domain.policies.output_authorization_policy import (
    AllowedScope,
    DisclosureRule,
    OutputAuthorizationPolicy,
    TemplateReference,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import DEFAULT_OUTPUT_TEMPLATE_CATALOG
from oralia.infrastructure.concurrency.blocking_retrieval_worker import BoundedBlockingWorker
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine
from oralia.infrastructure.generation.deterministic_adapter import DeterministicGenerationAdapter
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationError, GenerationRequest
from oralia.infrastructure.speech.transcription_port import TranscriptionOutcome
from oralia.validation.protocol import CORPUS, SCENARIOS, Protocol, Scenario


def measure(value, unit, source, missing_reason=None):
    return {"value": value, "unit": unit, "source": source, "missing_reason": missing_reason}


def _rank_keys(scenario):
    words = set(re.findall(r"\w+", scenario.query.lower()))
    return sorted(
        scenario.documents, key=lambda k: (-len(words & set(re.findall(r"\w+", CORPUS[k].lower()))), k)
    )


def _setup(db, scenario, condition):
    course = models.Course(id="synthetic-course", name="Synthetic validation", subject_code="SYN")
    retention = models.RetentionPolicy(
        id="synthetic-retention",
        content_scope="session",
        retention_days=1,
        access_scope="participant_only",
        purge_rule="delete after synthetic run",
    )
    db.add_all([course, retention])
    db.flush()
    if scenario.id == "conflicting_sources":
        # Prepared conflict annotation, not a claim of automatic semantic discovery.
        db.add(
            models.MaterialConflictRecord(
                document_ids=["water", "cold"],
                fragment_ids=["water", "cold"],
                conflicting_claims=[CORPUS["water"], CORPUS["cold"]],
                detected_by_query="synthetic labeled fixture",
            )
        )
        db.flush()
    entries = DEFAULT_OUTPUT_TEMPLATE_CATALOG.entries
    policy = OutputAuthorizationPolicy(
        schema_version=1,
        policy_id="synthetic-protocol",
        policy_version=1,
        allowed_recipients=("synthetic-006",),
        allowed_disclosures=(
            DisclosureRule(category="texto", provenance="activity_material", recipient="synthetic-006"),
        ),
        allowed_scopes=AllowedScope(
            topics=tuple(dict.fromkeys(e.topic_ref for e in entries)),
            purposes=tuple(dict.fromkeys(e.purpose_ref for e in entries)),
            actions=tuple(dict.fromkeys(e.action_ref for e in entries)),
        ),
        general_knowledge_allowed=False,
        allowed_templates=tuple(
            TemplateReference(e.template_id, e.version) for e in entries if e.message_type == "normal"
        ),
        allowed_operational_messages=(("safe-technical-fallback", 1),),
    )
    raw = canonical_policy_json(policy)
    activity = models.ActivityConfiguration(
        id="synthetic-activity",
        family_id="synthetic-family",
        course_id=course.id,
        name="Synthetic validation",
        subject="water",
        objective="Explicar materiales autorizados",
        mode="self_study",
        language="es",
        max_turns=1 if scenario.fault == "limit" else 20,
        max_duration_seconds=300,
        retention_policy_id=retention.id,
        output_authorization_policy_json=raw,
        output_authorization_policy_sha256=canonical_policy_sha256(raw),
    )
    db.add(activity)
    db.flush()
    db.add(
        models.SelfStudyActivityConfig(
            activity_configuration_id=activity.id,
            enabled_modes=["doubt_resolution", "presentation_preparation"],
            retention_authorized=False,
        )
    )
    if scenario.fault == "correction":
        activity.mode = "oral_defense"
        db.add(
            models.DefenseActivityConfig(
                activity_configuration_id=activity.id,
                initial_questions=["¿Cómo explicas el agua?", "¿Cómo justificas la explicación?"],
                topics=["water"],
                transcript_retention_authorized=True,
            )
        )
    for i, key in enumerate(scenario.documents):
        db.add(
            models.MaterialDocument(
                id=key,
                course_id=course.id,
                activity_configuration_ids=[activity.id],
                filename=f"{key}.txt",
                content_hash=hashlib.sha256(CORPUS[key].encode()).hexdigest(),
                mime_type="text/plain",
                size_bytes=len(CORPUS[key].encode()),
                status="active",
            )
        )
        db.flush()
        db.add(
            models.MaterialFragment(
                id=key,
                document_id=key,
                document_version=1,
                text=CORPUS[key],
                location_ref="line1",
                sequence_index=i,
                embedding_ref=key,
                course_id=course.id,
                activity_configuration_ids=[activity.id],
                indexing_status="indexed",
            )
        )
    db.flush()
    # Explicitly select deterministic model, independent of the developer's environment.
    db.add(
        models.ActivityGovernance(
            activity_configuration_id=activity.id,
            family_id=activity.family_id,
            version=1,
            status="active",
            model_id="deterministic",
            material_versions=[{"document_id": k, "version": 1} for k in scenario.documents],
        )
    )
    db.flush()
    session = start_session(
        db, StartSessionInput(participant_code="synthetic-006", activity_configuration_id=activity.id)
    )
    state = get_or_create(db, session.id, activity_ref=activity.id)
    if condition == "presentation":
        state.mode = "presentation_preparation"
    if scenario.prior:
        db.add(
            models.Turn(
                session_id=session.id,
                index=0,
                input_text="Synthetic prior",
                output_text=scenario.prior,
                status="completed",
            )
        )
        session.turn_count = 1
    db.commit()
    return session


class FixtureRetriever:
    contract = composer.MaterialRetrieverAgent.contract

    def __init__(self, db, scenario, condition):
        self.db, self.scenario, self.condition = db, scenario, condition
        self.selected = []

    async def execute(self, request, cancellation):
        if self.scenario.fault == "index":
            raise ConnectionError("synthetic index unavailable")
        if self.scenario.fault == "resources":
            worker = BoundedBlockingWorker(capacity=1)
            worker.shutdown()
            await worker.run(lambda: None)  # Real closed-admission failure; never a global worker.
        keys = _rank_keys(self.scenario)
        self.selected = keys[: 1 if self.condition == "top1" else 3]
        fragments = []
        for key in self.selected:
            fragment = get_currently_valid_fragment(
                self.db, key, course_id="synthetic-course", activity_configuration_id="synthetic-activity"
            )
            if fragment:
                fragments.append(
                    {
                        "fragment_id": key,
                        "document_id": key,
                        "document_version": 1,
                        "location_ref": "line1",
                        "text": fragment.text,
                        "relevance_score": 1.0,
                    }
                )
        return AgentResult(
            status="ok",
            output={
                "fragments": fragments,
                "index_version": "synthetic-lexical-v1",
                "warnings": [],
                "conflicts": [],
            },
            trace={"index_version": "synthetic-lexical-v1", "fragment_count": len(fragments)},
        )


class AblatedGrounding:
    contract = composer.GroundingVerifierAgent.contract

    def __init__(self, db=None):
        pass

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "verdict": "fundamentada",
                "supported_claims": [],
                "unsupported_claims": [],
                "evidence_ids": [],
            },
            trace={"synthetic_ablation": True},
        )


class AblatedCoherence:
    contract = composer.CoherenceVerifierAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={"verdict": "approved", "incident_types": [], "recovery_action": None},
            trace={"synthetic_ablation": True},
        )


async def run_cell(protocol: Protocol, scenario: Scenario, condition: str, repetition: int):
    # Revalidate even callers bypassing CLI; only immutable built-in scenario values.
    protocol = Protocol.model_validate(protocol.model_dump())
    if condition not in protocol.conditions or scenario not in SCENARIOS:
        raise ValueError("only authorized built-in conditions/scenarios")
    components = []
    original_generate = DeterministicGenerationAdapter.generate
    original_gate = composer.decide_final_output

    def timed_gate(*args, **kwargs):
        tick = time.perf_counter()
        result = original_gate(*args, **kwargs)
        components.append(
            {
                "agent_id": "final-output-gate",
                "kind": "policy",
                "status": "ok",
                "latency_ms": (time.perf_counter() - tick) * 1000,
                "verdict": result.final_verdict.verdict,
                "incident_types": [],
            }
        )
        return result

    async def generate(adapter, request):
        result = await original_generate(adapter, request)
        return result.model_copy(update={"text": scenario.proposal}) if scenario.proposal else result

    async def timed(agent, request, cancellation=None):
        start = time.perf_counter()
        aid = agent.contract.agent_id
        if scenario.fault == "agent_timeout" and aid == "response-generator":

            class TimeoutAgent:
                contract = agent.contract

                async def execute(self, req, token):
                    await asyncio.sleep(0.05)

            result = await run_with_deadline(TimeoutAgent(), request.model_copy(update={"deadline_ms": 1}))
        else:
            result = await run_with_deadline(agent, request, cancellation)
        components.append(
            {
                "agent_id": aid,
                "status": result.status,
                "latency_ms": (time.perf_counter() - start) * 1000,
                "verdict": (result.output or {}).get("verdict"),
                "incident_types": (result.output or {}).get("incident_types", []),
            }
        )
        return result

    async def unavailable_model(adapter, request):
        raise GenerationError("synthetic model unavailable")

    started, cpu = time.perf_counter(), time.process_time()
    rss = psutil.Process().memory_info().rss
    error = None
    output, action, grounding, coherence = None, None, None, None
    before = after = 0
    session_status = "active"
    retrieval_ids = []
    output_sources = []
    recovery = None
    event_types = []
    deleted = None
    conflict_rejected = None
    transcription = None
    reconstruction = None
    runtime_fallback = False
    with TemporaryDirectory(prefix="oralia-synthetic-") as temp:
        engine = build_engine(f"sqlite:///{(Path(temp) / 'experiment.db').as_posix()}")
        Base.metadata.create_all(engine)
        try:
            with Session(engine, expire_on_commit=False) as db:
                session = _setup(db, scenario, condition)
                before = db.get(models.CognitiveState, session.id).version
                retriever = FixtureRetriever(db, scenario, condition)
                with ExitStack() as stack:
                    stack.enter_context(patch.object(composer, "decide_final_output", timed_gate))
                    stack.enter_context(patch.object(defense_composer, "decide_final_output", timed_gate))
                    stack.enter_context(patch.object(DeterministicGenerationAdapter, "generate", generate))
                    stack.enter_context(
                        patch.object(composer, "MaterialRetrieverAgent", lambda db: retriever)
                    )
                    stack.enter_context(patch.object(composer, "run_with_deadline", timed))
                    stack.enter_context(patch.object(agency_composer, "run_with_deadline", timed))
                    stack.enter_context(
                        patch.object(defense_composer, "MaterialRetrieverAgent", lambda db: retriever)
                    )
                    if condition == "no_grounding":
                        stack.enter_context(
                            patch.object(composer, "GroundingVerifierAgent", AblatedGrounding)
                        )
                        stack.enter_context(
                            patch.object(defense_composer, "GroundingVerifierAgent", AblatedGrounding)
                        )
                    if condition == "no_coherence":
                        stack.enter_context(
                            patch.object(composer, "CoherenceVerifierAgent", AblatedCoherence)
                        )
                        stack.enter_context(
                            patch.object(defense_composer, "CoherenceVerifierAgent", AblatedCoherence)
                        )
                    if scenario.fault == "model":
                        # Fail the existing primary adapter. Real reserve/degradation is observed.
                        from oralia.infrastructure.generation.ollama_adapter import OllamaGenerationAdapter

                        stack.enter_context(
                            patch.object(OllamaGenerationAdapter, "generate", unavailable_model)
                        )
                    try:
                        if scenario.fault in {"stt", "correction"}:

                            class SyntheticSTT:
                                async def transcribe(self, audio, *, language):
                                    if scenario.fault == "stt":
                                        raise RuntimeError("synthetic STT failure")
                                    return TranscriptionOutcome(
                                        ok=True,
                                        text="El agua hierve a 20 grados.",
                                        low_confidence=True,
                                        overall_confidence=0.2,
                                    )

                            try:
                                transcript = await submit_defense_voice_turn(
                                    db,
                                    session,
                                    b"synthetic-not-real-audio",
                                    language="es",
                                    transcription_port=SyntheticSTT(),
                                )
                            except TranscriptionUnavailable:
                                recovery = "text_after_observed_stt_failure"
                            else:
                                result = await confirm_defense_transcript(
                                    db,
                                    session,
                                    transcript.id,
                                    CORPUS["water"],
                                    closure_retain=True,
                                    closure_scope=["transcript"],
                                )
                                db.flush()
                                turn = db.get(models.Turn, transcript.turn_id)
                                transcription = {
                                    "original_preserved": transcript.raw_text
                                    == "El agua hierve a 20 grados.",
                                    "corrected_input_used": turn is not None
                                    and turn.input_text == CORPUS["water"],
                                    "correction_count": db.query(models.TranscriptCorrection)
                                    .filter_by(session_id=session.id)
                                    .count(),
                                    "effect": "definitive input changed; previous output immutable",
                                }
                                output, action = result.output_text, result.dialogue_action
                                output_sources = result.sources
                        if condition == "baseline":
                            retrieval_ids = list(_rank_keys(scenario)[:3])
                            req = GenerationRequest(
                                purpose="explicacion",
                                instruction="Synthetic direct baseline",
                                student_input=scenario.query,
                                evidence=[
                                    EvidenceItem(
                                        fragment_id=k, document_id=k, document_version=1, text=CORPUS[k]
                                    )
                                    for k in retrieval_ids
                                ],
                            )
                            tick = time.perf_counter()
                            outcome = await DeterministicGenerationAdapter().generate(req)
                            # Constitutional check remains mandatory even for synthetic baseline.
                            verdict = evaluate(outcome.text)
                            output = outcome.text if verdict[0] == "approved" else None
                            action = "respond" if verdict[0] == "approved" else "block"
                            components.append(
                                {
                                    "agent_id": "direct-model",
                                    "status": "ok",
                                    "latency_ms": (time.perf_counter() - tick) * 1000,
                                    "verdict": None,
                                    "incident_types": [],
                                }
                            )
                            event_types = ["direct_generation", "constitutional_check"]
                        elif scenario.fault != "correction":
                            result = await submit_study_turn(db, session, scenario.query)
                            output, action = result.output_text, result.dialogue_action
                            output_sources = result.sources
                            retrieval_ids = list(retriever.selected)
                            db.flush()
                            for event in (
                                db.query(models.TraceEvent)
                                .filter_by(session_id=session.id)
                                .order_by(models.TraceEvent.created_at)
                            ):
                                event_types.append(event.event_type)
                                if event.event_type == "verification_combined":
                                    grounding = event.payload.get("grounding_verdict")
                                    coherence = event.payload.get("coherence_verdict")
                        if scenario.fault == "state":
                            state = db.get(models.CognitiveState, session.id)
                            stale = apply_patch(
                                db,
                                session_id=session.id,
                                base_version=state.version - 1,
                                proposed_by_agent_id="synthetic-concurrent-writer",
                                element_type="decision",
                                payload={"next_action_proposed": "respond"},
                                justification="Synthetic stale update",
                            )
                            conflict_rejected = not stale.applied
                        if scenario.fault == "delete":
                            if session.status == "active":
                                end_study_session(
                                    db,
                                    session,
                                    db.query(models.SelfStudyActivityConfig)
                                    .filter_by(activity_configuration_id=session.activity_configuration_id)
                                    .one(),
                                    status="closed_by_participant",
                                )
                            deleted = delete_session_content(db, session.id)
                        db.commit()
                    except Exception as exc:
                        db.rollback()
                        error = type(exc).__name__  # No arbitrary exception text or prompts in reports.
                    state = db.get(models.CognitiveState, session.id)
                    after = state.version if state else None
                    session_status = db.get(models.Session, session.id).status
                    trace = reconstruct_session_trace(db, session.id)
                    patches = [p for p in trace["state_patches"] if p["applied"]]
                    reconstruction = {
                        "event_count": len(trace["trace_events"]),
                        "applied_patch_count": len(patches),
                        "patch_chain": [
                            {
                                k: p[k]
                                for k in (
                                    "base_version",
                                    "resulting_version",
                                    "proposed_by_agent_id",
                                    "element_type",
                                    "applied",
                                )
                            }
                            for p in trace["state_patches"]
                        ],
                        "state_chain_valid": all(
                            p["resulting_version"] == p["base_version"] + 1 for p in patches
                        )
                        and after is not None
                        and sorted(p["base_version"] for p in patches) == list(range(before, after)),
                    }
                    for event in db.query(models.TraceEvent).filter_by(session_id=session.id):
                        if event.event_type not in event_types:
                            event_types.append(event.event_type)
                        if event.event_type == "verification_combined":
                            grounding = event.payload.get("grounding_verdict")
                            coherence = event.payload.get("coherence_verdict")
                        if event.event_type == "generation_call":
                            runtime_fallback = runtime_fallback or bool(event.payload.get("fallback_used"))
                    if scenario.fault == "model" and condition != "baseline" and error is None:
                        recovery = "reserve_or_safe_output"
                    if scenario.fault == "index" and condition != "baseline" and error is None:
                        recovery = "missing_evidence_or_safe_output"
                    if scenario.fault == "resources" and condition != "baseline" and error is None:
                        recovery = "missing_evidence_after_closed_worker"
                    if any(c["status"] == "timeout" for c in components) and error is None:
                        recovery = "safe_fallback"
        finally:
            engine.dispose()
    relevant, selected = set(scenario.relevant), set(retrieval_ids)
    elapsed = (time.perf_counter() - started) * 1000
    return {
        "scenario": scenario.id,
        "condition": condition,
        "repetition": repetition,
        "model": "deterministic",
        "parameters": {},
        "index": "synthetic-lexical-v1",
        "fault": scenario.fault,
        "injection_applied": scenario.fault in {"state", "delete", "limit", "stt", "correction"}
        or (condition != "baseline" and scenario.fault in {"model", "index", "agent_timeout", "resources"}),
        "ablations": (
            ["grounding-verifier"]
            if condition == "no_grounding"
            else ["coherence-verifier"] if condition == "no_coherence" else []
        ),
        "components": components,
        "event_types": event_types,
        "output_text": output,
        "action": action,
        "grounding_verdict": grounding,
        "coherence_verdict": coherence,
        "retrieved_ids": retrieval_ids,
        "output_sources": output_sources,
        "state": {"before": before, "after": after, "stale_update_rejected": conflict_rejected},
        "status": session_status,
        "error": error,
        "recovery": recovery,
        "deleted": deleted is not None,
        "transcription": transcription,
        "reconstruction": reconstruction,
        "runtime_fallback_observed": runtime_fallback,
        "fully_traced": condition != "baseline"
        and error is None
        and bool(components)
        and "output_authorization_attempt" in event_types
        and bool({"turn_completed", "turn_degraded", "turn_blocked"} & set(event_types))
        and bool(reconstruction and reconstruction["state_chain_valid"]),
        "metrics": {
            "latency_ms": measure(elapsed, "ms", "perf_counter; includes isolated DB setup/cleanup"),
            "cpu_seconds": measure(time.process_time() - cpu, "s", "process_time"),
            "rss_before_mb": measure(rss / 2**20, "MiB", "psutil process RSS; not peak"),
            "rss_after_mb": measure(
                psutil.Process().memory_info().rss / 2**20, "MiB", "psutil process RSS; not peak"
            ),
            "gpu_memory_mb": measure(None, "MiB", None, "no GPU monitor; deterministic CPU provider"),
            "context_chars": measure(
                len(scenario.query) + sum(len(CORPUS[k]) for k in retrieval_ids),
                "characters",
                "input plus selected evidence; no hidden prompts",
            ),
            "context_tokens": measure(None, "tokens", None, "no model tokenizer configured"),
            "retrieval_precision": measure(
                len(selected & relevant) / len(selected) if selected else None,
                "ratio",
                "labeled fixture IDs",
                None if selected else "zero selected denominator",
            ),
            "retrieval_recall": measure(
                len(selected & relevant) / len(relevant) if relevant else None,
                "ratio",
                "labeled fixture IDs",
                None if relevant else "zero relevant denominator",
            ),
        },
    }
