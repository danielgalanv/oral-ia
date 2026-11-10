"""T096: red reproductions for final authorization bypasses in self-study."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.application.orchestration import self_study_agency_composer as composer
from oralia.application.orchestration.study_turn_orchestrator import run_study_turn
from oralia.domain.agents.agent_contract import AgentError, AgentRequest, AgentResult, CancellationToken
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
)
from oralia.domain.policies.output_authorization_verifier import verify_output_authorization
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine
from oralia.infrastructure.generation.generation_port import GenerationOutcome

_INITIAL_TEXT = "El agua hierve a cien grados a nivel del mar."
_TRANSFORMED_H02_TEXT = "Tu nota es 9."
_NORMAL_QUESTION = "¿Por qué cambia el punto de ebullición con la presión?"
_FALLBACK_QUESTION = "Explica la idea principal del fragmento."
_EVIDENCE = [
    {
        "fragment_id": "fragment-t096",
        "document_id": "document-t096",
        "document_version": 1,
        "location_ref": "p. 1",
        "text": _INITIAL_TEXT,
        "relevance_score": 1.0,
    }
]


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _policy(*, allowed_templates: list[list[str | int]]) -> dict[str, Any]:
    return {
        "policy_id": "t096-self-study-policy",
        "policy_version": 1,
        "schema_version": 1,
        "allowed_recipients": ["participant-a"],
        "allowed_templates": allowed_templates,
        "allowed_disclosures": [
            {
                "category": "texto",
                "provenance": "activity_material",
                "recipient": "participant-a",
            }
        ],
        "allowed_scopes": {
            "topics": ["activity"],
            "purposes": ["material_response"],
            "actions": ["respond"],
        },
        "general_knowledge_allowed": False,
        "allowed_operational_messages": [],
    }


def _canonical_policy(policy: dict[str, Any]) -> str:
    canonical = canonical_policy_json(OutputAuthorizationPolicy.model_validate(policy))
    policy.clear()
    policy.update(json.loads(canonical))
    return canonical


@dataclass
class _Resources:
    db_closed: bool = False
    engine_disposed: bool = False


@contextmanager
def _local_context(
    tmp_path: Path,
    *,
    mode: str,
    allowed_templates: list[list[str | int]],
    policy_overrides: dict[str, Any] | None = None,
) -> Iterator[tuple[SASession, models.Session, dict[str, Any], _Resources]]:
    engine = build_engine(f"sqlite:///{tmp_path / 't096.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = session_factory()
    resources = _Resources()
    policy = _policy(allowed_templates=allowed_templates)
    if policy_overrides:
        policy.update(policy_overrides)

    try:
        course = models.Course(name="T096 course", subject_code="T096")
        retention = models.RetentionPolicy(
            content_scope="session",
            access_scope="teacher",
            purge_rule="manual",
        )
        participant = models.ParticipantCode(code="participant-a")
        db.add_all([course, retention, participant])
        db.flush()

        canonical = _canonical_policy(policy)
        activity = models.ActivityConfiguration(
            course_id=course.id,
            name="T096 self-study",
            subject="Contextual output authorization",
            objective="Comprender la ebullición",
            mode="self_study",
            language="es",
            max_turns=5,
            max_duration_seconds=300,
            general_knowledge_allowed=False,
            required_agent_ids=[],
            optional_agent_ids=[],
            retention_policy_id=retention.id,
        )
        activity.output_authorization_policy_json = canonical
        activity.output_authorization_policy_sha256 = _sha256(canonical)

        assert isinstance(activity.output_authorization_policy_json, str)
        assert json.loads(activity.output_authorization_policy_json) == policy
        assert _canonical_policy(json.loads(canonical)) == canonical
        assert activity.output_authorization_policy_sha256 == _sha256(canonical)
        assert policy["allowed_recipients"] == [participant.code]
        assert policy["general_knowledge_allowed"] is False
        assert policy["allowed_operational_messages"] == []

        db.add(activity)
        db.flush()
        document = models.MaterialDocument(
            id="document-t096",
            family_id="family-t096",
            version=1,
            course_id=course.id,
            activity_configuration_ids=[activity.id],
            filename="t096.txt",
            content_hash=_sha256(_INITIAL_TEXT),
            mime_type="text/plain",
            size_bytes=len(_INITIAL_TEXT.encode("utf-8")),
            language="es",
            status="active",
        )
        fragment = models.MaterialFragment(
            id="fragment-t096",
            document_id=document.id,
            document_version=1,
            text=_INITIAL_TEXT,
            location_ref="p. 1",
            sequence_index=0,
            embedding_ref="embedding-t096",
            content_type="texto",
            course_id=course.id,
            activity_configuration_ids=[activity.id],
            indexing_status="indexed",
        )
        db.add_all([document, fragment])
        db.flush()
        db.add(
            models.SelfStudyActivityConfig(
                activity_configuration_id=activity.id,
                enabled_modes=[mode],
                summary_authorized=False,
                practice_reveals_solution=False,
            )
        )
        session = models.Session(
            activity_configuration_id=activity.id,
            participant_code=participant.code,
            status="active",
            turn_count=0,
            active_lock_token="ACTIVE",
        )
        db.add(session)
        db.flush()

        yield db, session, policy, resources
    finally:
        db.close()
        resources.db_closed = True
        engine.dispose()
        resources.engine_disposed = True


class _StaticAgent:
    def __init__(
        self,
        agent_id: str,
        result: AgentResult | Callable[[AgentRequest], AgentResult],
        *,
        deadline_ms: int = 100,
    ) -> None:
        self.contract = SimpleNamespace(agent_id=agent_id, timeout_ms=deadline_ms)
        self._result = result
        self.calls = 0
        self.requests: list[AgentRequest] = []

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        self.requests.append(request)
        if callable(self._result):
            return self._result(request)
        return self._result


class _TimeoutGenerator:
    contract = SimpleNamespace(agent_id="response-generator", timeout_ms=5)

    def __init__(self) -> None:
        self.calls = 0
        self.started = asyncio.Event()
        self.release_gate = asyncio.Event()
        self.released = asyncio.Event()

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        self.started.set()
        try:
            await self.release_gate.wait()
        finally:
            self.release_gate.set()
            self.released.set()
        return AgentResult(status="ok", output={"proposal_text": _INITIAL_TEXT})


class _FallbackAdapter:
    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, request: Any) -> GenerationOutcome:
        self.calls += 1
        return GenerationOutcome(
            ok=True,
            text=_FALLBACK_QUESTION,
            internal_expected_answer="La presión modifica el punto de ebullición.",
            adapter="deterministic",
        )


def _ok(output: dict[str, Any]) -> AgentResult:
    return AgentResult(status="ok", output=output, confidence=1.0)


def _structured_constitutional_result(request: AgentRequest) -> AgentResult:
    verdict = verify_output_authorization(
        request.input.get("proposal"),
        request.context.get("authorization_snapshot"),
        actual_session_id=str(request.session_id),
        actual_activity_configuration_id=request.context.get("activity_configuration_id"),
        actual_recipient=request.context.get("actual_recipient"),
        fallback_attempt=request.input.get("fallback_attempt", 0),
        h02_evaluator=composer.constitutional_evaluate,
    )
    return _ok(
        {
            "verdict": verdict.verdict,
            "reasons": [reason.value for reason in verdict.reason_codes],
            "authorization_context": verdict.model_dump(
                mode="json",
                exclude={"verdict", "reason_codes"},
                exclude_none=True,
            ),
        }
    )


def _install_pipeline(
    monkeypatch: pytest.MonkeyPatch,
    *,
    mode: str,
    fragments: list[dict[str, Any]],
    generator: Any | None = None,
    grounding: Any | None = None,
    coherence: Any | None = None,
    constitutional: Any | None = None,
    fallback: Any | None = None,
    practice: Any | None = None,
    non_disclosure: Any | None = None,
) -> dict[str, Any]:
    interpreter = _StaticAgent(
        "study-intent-interpreter",
        _ok(
            {
                "intent_hypotheses": [f"{mode}:1.00"],
                "primary_intent": mode,
                "primary_confidence": 1.0,
                "requested_mode": mode,
            }
        ),
    )
    retriever = _StaticAgent("material-retriever", _ok({"fragments": fragments}))
    generator = generator or _StaticAgent(
        "response-generator",
        _ok(
            {
                "proposal_text": _INITIAL_TEXT,
                "generation_trace": {
                    "adapter": "deterministic",
                    "model": None,
                    "fallback_used": False,
                },
            }
        ),
    )
    grounding = grounding or _StaticAgent(
        "grounding-verifier",
        _ok(
            {
                "verdict": "fundamentada",
                "supported_claims": [_INITIAL_TEXT],
                "unsupported_claims": [],
            }
        ),
    )
    coherence = coherence or _StaticAgent(
        "coherence-verifier",
        _ok({"verdict": "approved", "incident_types": [], "recovery_action": None}),
    )
    constitutional = constitutional or _StaticAgent(
        "constitutional-control",
        _structured_constitutional_result,
    )
    fallback = fallback or _StaticAgent(
        "safe-fallback",
        _ok({"text": composer.SAFE_FALLBACK_TEXT}),
    )
    practice = practice or _StaticAgent(
        "practice-question-agent",
        _ok(
            {
                "question_type": "explicacion",
                "question_text": _NORMAL_QUESTION,
                "internal_expected_answer": "La presión cambia la temperatura de ebullición.",
                "difficulty_hint": "media",
                "reveals_solution": False,
                "generation_trace": {
                    "adapter": "deterministic",
                    "model": None,
                    "fallback_used": False,
                },
            }
        ),
    )
    non_disclosure = non_disclosure or _StaticAgent(
        "solution-non-disclosure-verifier",
        _ok({"verdict": "approved", "overlap_score": 0.0}),
    )

    monkeypatch.setattr(composer, "StudyIntentInterpreterAgent", lambda: interpreter)
    monkeypatch.setattr(composer, "MaterialRetrieverAgent", lambda db: retriever)
    monkeypatch.setattr(composer, "ResponseGeneratorAgent", lambda: generator)
    monkeypatch.setattr(composer, "GroundingVerifierAgent", lambda db: grounding)
    monkeypatch.setattr(composer, "CoherenceVerifierAgent", lambda: coherence)
    monkeypatch.setattr(composer, "ConstitutionalControl", lambda: constitutional)
    monkeypatch.setattr(composer, "SafeFallbackAgent", lambda: fallback)
    monkeypatch.setattr(composer, "PracticeQuestionAgent", lambda: practice)
    monkeypatch.setattr(composer, "SolutionNonDisclosureVerifierAgent", lambda: non_disclosure)
    return {
        "interpreter": interpreter,
        "retriever": retriever,
        "generator": generator,
        "grounding": grounding,
        "coherence": coherence,
        "constitutional": constitutional,
        "fallback": fallback,
        "practice": practice,
        "non_disclosure": non_disclosure,
    }


def _turn_and_verification(
    db: SASession,
    result: composer.StudyTurnResult,
) -> tuple[models.Turn, models.VerificationResult]:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    verification = db.get(models.VerificationResult, turn.verification_result_id)
    assert verification is not None
    return turn, verification


def _assert_safe_close(
    db: SASession,
    session: models.Session,
    result: composer.StudyTurnResult,
) -> None:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    assert result.blocked is True
    assert result.output_text is None
    assert turn.output_text is None
    assert result.dialogue_action == "finish"
    db.refresh(session)
    assert session.status == "closed_error_safe"


@pytest.mark.integration
def test_authorized_self_study_turn_remains_visible(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agents = _install_pipeline(monkeypatch, mode="doubt_resolution", fragments=_EVIDENCE)
    with _local_context(
        tmp_path,
        mode="doubt_resolution",
            allowed_templates=[["material-fragment-response", 1]],
    ) as (db, session, _, resources):
        result = asyncio.run(run_study_turn(db, session, "¿A qué temperatura hierve el agua?"))
        turn, verification = _turn_and_verification(db, result)
        db.refresh(session)

        assert agents["generator"].calls == 1
        assert agents["grounding"].calls == 1
        assert agents["constitutional"].calls == 1
        assert result.blocked is False
        assert result.status == "completed"
        assert result.output_text
        assert turn.output_text == result.output_text
        assert verification.verdict == "approved"
        assert session.status == "active"

    assert resources is not None
    assert resources.db_closed is True
    assert resources.engine_disposed is True


@pytest.mark.integration
def test_upstream_error_fallback_closes_without_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    generator = _StaticAgent(
        "response-generator",
        AgentResult(
            status="error",
            error=AgentError(code="T096_UPSTREAM_ERROR", message="controlled", recoverable=True),
        ),
    )
    fallback = _StaticAgent("safe-fallback", _ok({"text": composer.SAFE_FALLBACK_TEXT}))
    agents = _install_pipeline(
        monkeypatch,
        mode="doubt_resolution",
        fragments=_EVIDENCE,
        generator=generator,
        fallback=fallback,
    )
    with _local_context(tmp_path, mode="doubt_resolution", allowed_templates=[]) as (
        db,
        session,
        policy,
        _,
    ):
        result = asyncio.run(run_study_turn(db, session, "Explica la ebullición"))

        assert policy["allowed_operational_messages"] == []
        assert generator.calls == 1
        assert fallback.calls == 1
        assert agents["grounding"].calls == 0
        _assert_safe_close(db, session, result)


@pytest.mark.integration
def test_upstream_timeout_fallback_closes_without_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def exercise(
        db: SASession,
        session: models.Session,
    ) -> tuple[composer.StudyTurnResult, _TimeoutGenerator]:
        generator = _TimeoutGenerator()
        fallback = _StaticAgent("safe-fallback", _ok({"text": composer.SAFE_FALLBACK_TEXT}))
        agents = _install_pipeline(
            monkeypatch,
            mode="doubt_resolution",
            fragments=_EVIDENCE,
            generator=generator,
            fallback=fallback,
        )
        try:
            result = await run_study_turn(db, session, "Explica la ebullición")
        finally:
            generator.release_gate.set()

        assert generator.started.is_set()
        assert generator.released.is_set()
        assert generator.calls == 1
        assert fallback.calls == 1
        assert agents["grounding"].calls == 0
        timeout_events = (
            db.query(models.TraceEvent)
            .filter(models.TraceEvent.turn_id == result.turn_id)
            .all()
        )
        assert any(
            event.payload.get("step_id") == "generate" and event.payload.get("status") == "timeout"
            for event in timeout_events
        )
        return result, generator

    with _local_context(tmp_path, mode="doubt_resolution", allowed_templates=[]) as (
        db,
        session,
        policy,
        _,
    ):
        result, generator = asyncio.run(exercise(db, session))

        assert policy["allowed_operational_messages"] == []
        assert generator.released.is_set()
        _assert_safe_close(db, session, result)


@pytest.mark.integration
def test_exhausted_practice_generation_fallback_is_finally_authorized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    practice = _StaticAgent(
        "practice-question-agent",
        _ok(
            {
                "question_type": "explicacion",
                "question_text": _NORMAL_QUESTION,
                "internal_expected_answer": "respuesta",
                "difficulty_hint": "media",
                "reveals_solution": False,
                "generation_trace": {"adapter": "deterministic", "fallback_used": False},
            }
        ),
    )
    non_disclosure = _StaticAgent(
        "solution-non-disclosure-verifier",
        _ok({"verdict": "block", "overlap_score": 1.0}),
    )
    deterministic = _FallbackAdapter()
    monkeypatch.setattr(composer.generation_config, "get_practice_regen_max_attempts", lambda: 2)
    monkeypatch.setattr(composer, "DeterministicGenerationAdapter", lambda: deterministic)
    _install_pipeline(
        monkeypatch,
        mode="practice_questions",
        fragments=_EVIDENCE,
        practice=practice,
        non_disclosure=non_disclosure,
    )
    with _local_context(tmp_path, mode="practice_questions", allowed_templates=[]) as (
        db,
        session,
        _,
        _,
    ):
        result = asyncio.run(run_study_turn(db, session, "Ponme una pregunta de práctica"))
        question = db.query(models.PracticeQuestion).filter_by(turn_id=result.turn_id).one()
        generation_event = (
            db.query(models.TraceEvent)
            .filter(
                models.TraceEvent.turn_id == result.turn_id,
                models.TraceEvent.event_type == "generation_call",
            )
            .one()
        )

        assert practice.calls == 2
        assert non_disclosure.calls == 2
        assert question.non_disclosure_attempts == 2
        assert deterministic.calls == 1
        assert generation_event.payload["fallback_used"] is True
        _assert_safe_close(db, session, result)


@pytest.mark.integration
def test_normal_practice_question_is_finally_authorized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    deterministic = _FallbackAdapter()
    monkeypatch.setattr(composer, "DeterministicGenerationAdapter", lambda: deterministic)
    agents = _install_pipeline(monkeypatch, mode="practice_questions", fragments=_EVIDENCE)
    with _local_context(tmp_path, mode="practice_questions", allowed_templates=[]) as (
        db,
        session,
        _,
        _,
    ):
        result = asyncio.run(run_study_turn(db, session, "Ponme una pregunta de práctica"))
        question = db.query(models.PracticeQuestion).filter_by(turn_id=result.turn_id).one()
        generation_event = (
            db.query(models.TraceEvent)
            .filter(
                models.TraceEvent.turn_id == result.turn_id,
                models.TraceEvent.event_type == "generation_call",
            )
            .one()
        )

        assert agents["practice"].calls == 1
        assert agents["non_disclosure"].calls == 1
        assert question.non_disclosure_attempts == 1
        assert deterministic.calls == 0
        assert generation_event.payload["fallback_used"] is False
        _assert_safe_close(db, session, result)


@pytest.mark.integration
def test_missing_evidence_message_is_finally_authorized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agents = _install_pipeline(monkeypatch, mode="doubt_resolution", fragments=[])
    with _local_context(tmp_path, mode="doubt_resolution", allowed_templates=[]) as (
        db,
        session,
        policy,
        _,
    ):
        result = asyncio.run(run_study_turn(db, session, "Explica un material inexistente"))
        selected = (
            db.query(models.TraceEvent)
            .filter(
                models.TraceEvent.turn_id == result.turn_id,
                models.TraceEvent.event_type == "agents_selected",
            )
            .one()
        )
        selected_steps = [step["step_id"] for step in selected.payload["activated_steps"]]

        assert policy["general_knowledge_allowed"] is False
        assert agents["generator"].calls == 0
        assert "generate" not in selected_steps
        assert agents["constitutional"].calls == 1
        proposal_text = agents["constitutional"].requests[0].input["proposal_text"]
        assert proposal_text == composer._ACKNOWLEDGE_MISSING_INFO_TEXT
        _assert_safe_close(db, session, result)


@pytest.mark.integration
def test_text_transformed_after_approval_is_reverified(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    grounding = _StaticAgent(
        "grounding-verifier",
        _ok(
            {
                "verdict": "parcialmente_fundamentada",
                "supported_claims": [_TRANSFORMED_H02_TEXT],
                "unsupported_claims": ["detalle no sustentado"],
            }
        ),
    )
    constitutional = _StaticAgent(
        "constitutional-control",
        _ok({"verdict": "approved", "reasons": []}),
    )
    agents = _install_pipeline(
        monkeypatch,
        mode="doubt_resolution",
        fragments=_EVIDENCE,
        grounding=grounding,
        constitutional=constitutional,
    )
    with _local_context(tmp_path, mode="doubt_resolution", allowed_templates=[]) as (
        db,
        session,
        _,
        _,
    ):
        result = asyncio.run(run_study_turn(db, session, "Explica la ebullición"))
        turn = db.get(models.Turn, result.turn_id)

        assert turn is not None
        assert _EVIDENCE
        assert agents["retriever"].calls == 1
        assert agents["generator"].calls == 1
        assert agents["generator"].requests[0].input["evidence"] == _EVIDENCE
        assert grounding.calls == 1
        constitutional_texts = [
            request.input["proposal_text"] for request in constitutional.requests
        ]
        assert _INITIAL_TEXT in constitutional_texts
        assert _TRANSFORMED_H02_TEXT in constitutional_texts
        _assert_safe_close(db, session, result)
