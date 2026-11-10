"""T097: red persistence/privacy reproductions for constitutional output handling."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.application.orchestration import turn_orchestrator
from oralia.application.orchestration.turn_orchestrator import TurnResult, run_turn
from oralia.domain.agents.agent_contract import AgentError, AgentRequest, AgentResult, CancellationToken
from oralia.domain.policies.constitutional_control import SAFE_BLOCKED_MESSAGE
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine

_APPROVED_TEXT = "Podemos continuar con la actividad."
_REJECTED_MARKER = "T090_REJECTED_SECRET_31C8"
_REJECTED_TEXT = f"Tu nota es 9. {_REJECTED_MARKER}"
_TEMPLATE_ID = "normal-message"
_TEMPLATE_VERSION = 1
_POLICY_ID = "t097-persistence-policy"


def _current_respond_candidate(echo: str) -> str:
    return f"He recibido tu mensaje: «{echo}». (Respuesta de demostración — sin materiales reales todavía.)"


_POSITIVE_CANDIDATE = _current_respond_candidate(_APPROVED_TEXT)
_H02_SIMPLE_CANDIDATE = _current_respond_candidate("Tu nota es 9.")
_H02_MARKER_CANDIDATE = _current_respond_candidate(_REJECTED_TEXT)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _policy(*, operational_allowed: bool = True) -> dict[str, Any]:
    return {
        "policy_id": _POLICY_ID,
        "policy_version": 1,
        "schema_version": 1,
        "allowed_recipients": ["participant-a"],
        "allowed_templates": [[_TEMPLATE_ID, _TEMPLATE_VERSION]],
        "allowed_operational_messages": ([["safe-technical-fallback", 1]] if operational_allowed else []),
        "allowed_disclosures": [
            {
                "category": "activity_public",
                "provenance": "teacher_activity",
                "recipient": "participant-a",
            }
        ],
        "allowed_scopes": {
            "topics": ["activity"],
            "purposes": ["continue"],
            "actions": ["respond"],
        },
        "general_knowledge_allowed": False,
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
    template_text: str,
    operational_allowed: bool = True,
) -> Iterator[tuple[SASession, models.Session, models.ActivityConfiguration, dict[str, Any], _Resources]]:
    engine = build_engine(f"sqlite:///{tmp_path / 't097.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = session_factory()
    resources = _Resources()
    policy = _policy(operational_allowed=operational_allowed)

    try:
        course = models.Course(name="T097 course", subject_code="T097")
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
            name="T097 persistence privacy",
            subject="Constitutional output persistence",
            objective="Continue the activity safely",
            mode="dialogue",
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
        activity.normal_output_template = {
            "template_id": _TEMPLATE_ID,
            "template_version": _TEMPLATE_VERSION,
            "text": template_text,
            "sha256": _sha256(template_text),
            "topic_ref": "activity",
            "purpose_ref": "continue",
            "action_ref": "respond",
        }

        assert isinstance(activity.output_authorization_policy_json, str)
        assert json.loads(activity.output_authorization_policy_json) == policy
        assert _canonical_policy(json.loads(canonical)) == canonical
        assert activity.output_authorization_policy_sha256 == _sha256(canonical)
        assert participant.code == policy["allowed_recipients"][0]
        assert policy["general_knowledge_allowed"] is False

        db.add(activity)
        db.flush()
        session = models.Session(
            activity_configuration_id=activity.id,
            participant_code=participant.code,
            status="active",
            turn_count=0,
            active_lock_token="ACTIVE",
        )
        db.add(session)
        db.flush()

        yield db, session, activity, policy, resources
    finally:
        db.close()
        resources.db_closed = True
        engine.dispose()
        resources.engine_disposed = True


class _OutputInterpreter:
    contract = SimpleNamespace(agent_id="interpreter", timeout_ms=100)

    def __init__(self, echo: str) -> None:
        self.echo = echo
        self.calls = 0

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        return AgentResult(
            status="ok",
            output={"intent": "respond", "echo": self.echo},
            confidence=1.0,
        )


class _ErrorInterpreter:
    contract = SimpleNamespace(agent_id="interpreter", timeout_ms=100)

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        return AgentResult(
            status="error",
            error=AgentError(
                code="T097_UPSTREAM_FAILURE",
                message="controlled upstream failure",
                recoverable=True,
            ),
        )


class _CountingFallback:
    contract = SimpleNamespace(agent_id="safe-fallback", timeout_ms=100)

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        return AgentResult(
            status="ok",
            output={"text": turn_orchestrator.SAFE_FALLBACK_TEXT},
            confidence=1.0,
        )


def _install_interpreter(monkeypatch: pytest.MonkeyPatch, interpreter: Any) -> None:
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", interpreter)


def _persisted_records(
    db: SASession,
    result: TurnResult,
) -> tuple[
    models.Turn,
    models.GeneratedProposal,
    models.VerificationResult,
    list[models.InternalMessage],
    list[models.TraceEvent],
]:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
    verification = db.get(models.VerificationResult, turn.verification_result_id)
    assert proposal is not None
    assert verification is not None
    messages = db.query(models.InternalMessage).filter_by(turn_id=turn.id).all()
    events = db.query(models.TraceEvent).filter_by(turn_id=turn.id).all()
    return turn, proposal, verification, messages, events


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)


def _nested_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in _nested_keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in _nested_keys(item)}
    return set()


def _assert_safe_close(
    db: SASession,
    session: models.Session,
    result: TurnResult,
) -> None:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    assert result.blocked is True
    assert result.output_text is None
    assert turn.output_text is None
    assert result.dialogue_action == "finish"
    db.refresh(session)
    assert session.status == "closed_error_safe"
    assert SAFE_BLOCKED_MESSAGE not in (result.output_text or "")


@pytest.mark.integration
def test_approved_output_keeps_legitimate_text_and_nonsensitive_trace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter = _OutputInterpreter(_APPROVED_TEXT)
    _install_interpreter(monkeypatch, interpreter)

    with _local_context(tmp_path, template_text=_POSITIVE_CANDIDATE) as (
        db,
        session,
        activity,
        _,
        resources,
    ):
        assert _current_respond_candidate(interpreter.echo) == activity.normal_output_template["text"]
        assert activity.normal_output_template["sha256"] == _sha256(activity.normal_output_template["text"])
        result = asyncio.run(run_turn(db, session, "ordinary participant input"))
        turn, proposal, verification, _, events = _persisted_records(db, result)
        policy_json = activity.output_authorization_policy_json

        assert interpreter.calls == 1
        assert result.blocked is False
        assert turn.status == "completed"
        assert result.output_text
        assert turn.output_text == result.output_text
        assert proposal.content.get("text") == result.output_text
        assert verification.verdict == "approved"
        assert verification.reasons == []
        assert turn.generated_proposal_id == proposal.id
        assert turn.verification_result_id == verification.id
        assert verification.proposal_id == proposal.id
        assert any(event.event_type == "agent_execution" for event in events)
        assert any(event.event_type == "turn_completed" for event in events)
        for event in events:
            assert policy_json not in _json(event.payload)
            assert _nested_keys(event.payload).isdisjoint(
                {"reasoning", "private_reasoning", "value", "value_sha256"}
            )

    assert resources is not None
    assert resources.db_closed is True
    assert resources.engine_disposed is True


@pytest.mark.integration
def test_rejected_candidate_is_absent_from_persistence_and_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter = _OutputInterpreter(_REJECTED_TEXT)
    _install_interpreter(monkeypatch, interpreter)

    with _local_context(tmp_path, template_text=_H02_MARKER_CANDIDATE) as (
        db,
        session,
        activity,
        _,
        _,
    ):
        assert _current_respond_candidate(interpreter.echo) == activity.normal_output_template["text"]
        assert activity.normal_output_template["sha256"] == _sha256(activity.normal_output_template["text"])
        assert "Tu nota es 9." in activity.normal_output_template["text"]
        assert _REJECTED_MARKER in activity.normal_output_template["text"]
        result = asyncio.run(run_turn(db, session, "ordinary participant input"))
        _, proposal, verification, messages, events = _persisted_records(db, result)
        authorization_context = getattr(verification, "authorization_context", None)
        transport_messages = [message for message in messages if message.type == "agent_invocation"]
        verifier_messages = [
            message for message in messages if message.receiver_agent_id == "constitutional-control"
        ]

        assert interpreter.calls == 1
        assert result.blocked is True
        assert verification.verdict == "block"
        assert verifier_messages
        assert transport_messages
        assert _REJECTED_MARKER not in _json(proposal.content)
        assert _REJECTED_MARKER not in _json([message.content for message in transport_messages])
        assert _REJECTED_MARKER not in _json([event.payload for event in events])
        assert _REJECTED_MARKER not in _json(authorization_context)


@pytest.mark.integration
def test_blocked_candidate_never_publishes_a_third_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter = _OutputInterpreter("Tu nota es 9.")
    _install_interpreter(monkeypatch, interpreter)

    with _local_context(
        tmp_path,
        template_text=_H02_SIMPLE_CANDIDATE,
        operational_allowed=False,
    ) as (
        db,
        session,
        activity,
        _,
        _,
    ):
        assert _current_respond_candidate(interpreter.echo) == activity.normal_output_template["text"]
        assert activity.normal_output_template["sha256"] == _sha256(activity.normal_output_template["text"])
        assert "Tu nota es 9." in activity.normal_output_template["text"]
        result = asyncio.run(run_turn(db, session, "ordinary participant input"))

        assert interpreter.calls == 1
        _assert_safe_close(db, session, result)


@pytest.mark.integration
def test_blocked_turn_persists_unambiguous_attempt_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter = _OutputInterpreter("Tu nota es 9.")
    _install_interpreter(monkeypatch, interpreter)

    with _local_context(
        tmp_path,
        template_text=_H02_SIMPLE_CANDIDATE,
        operational_allowed=False,
    ) as (
        db,
        session,
        activity,
        _,
        _,
    ):
        assert _current_respond_candidate(interpreter.echo) == activity.normal_output_template["text"]
        assert activity.normal_output_template["sha256"] == _sha256(activity.normal_output_template["text"])
        assert "Tu nota es 9." in activity.normal_output_template["text"]
        result = asyncio.run(run_turn(db, session, "ordinary participant input"))
        _, proposal, verification, _, events = _persisted_records(db, result)
        authorization_context = getattr(verification, "authorization_context", None)
        constitutional_events = [
            event
            for event in events
            if event.event_type == "constitutional_block"
            or event.payload.get("step_id") in {"verify", "verify-fallback"}
        ]

        assert interpreter.calls == 1
        assert result.blocked is True
        assert verification.verdict == "block"
        assert constitutional_events
        assert authorization_context is not None
        expected_context = {
            "activity_configuration_id": activity.id,
            "activity_version": activity.version,
            "policy_id": _POLICY_ID,
            "policy_version": 1,
            "schema_version": 1,
            "policy_sha256": activity.output_authorization_policy_sha256,
            "template_id": _TEMPLATE_ID,
            "template_version": _TEMPLATE_VERSION,
            "template_sha256": activity.normal_output_template["sha256"],
            "attempt": 0,
            "message_type": "normal",
        }
        for key, value in expected_context.items():
            assert authorization_context.get(key) == value
        assert any(
            event.payload.get("attempt") == 0
            and event.payload.get("verdict") == "block"
            and event.payload.get("reason_codes")
            for event in constitutional_events
        )
        assert "text" not in proposal.content
        assert SAFE_BLOCKED_MESSAGE not in _json(proposal.content)


@pytest.mark.integration
def test_upstream_failure_starts_once_at_operational_attempt_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter = _ErrorInterpreter()
    fallback = _CountingFallback()
    _install_interpreter(monkeypatch, interpreter)
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "safe-fallback", fallback)

    with _local_context(
        tmp_path,
        template_text=_POSITIVE_CANDIDATE,
        operational_allowed=False,
    ) as (
        db,
        session,
        _,
        policy,
        _,
    ):
        result = asyncio.run(run_turn(db, session, "trigger controlled upstream failure"))
        _, proposal, verification, messages, events = _persisted_records(db, result)
        authorization_context = getattr(verification, "authorization_context", None)
        fallback_messages = [message for message in messages if message.receiver_agent_id == "safe-fallback"]
        constitutional_attempts = [
            event
            for event in events
            if event.payload.get("attempt") == 1 and event.payload.get("verdict") in {"approved", "block"}
        ]

        assert policy["allowed_operational_messages"] == []
        assert interpreter.calls == 1
        assert fallback.calls == 1
        assert len(fallback_messages) == 1
        assert len(constitutional_attempts) == 1
        assert constitutional_attempts[0].payload["verdict"] == "block"
        assert constitutional_attempts[0].payload.get("reason_codes")
        assert verification.verdict == "block"
        assert verification.reasons
        assert authorization_context is not None
        assert authorization_context.get("attempt") == 1
        assert authorization_context.get("message_type") == "operational"
        persisted_transport = _json(
            {
                "proposal": proposal.content,
                "messages": [message.content for message in messages],
                "events": [event.payload for event in events],
            }
        )
        assert turn_orchestrator.SAFE_FALLBACK_TEXT not in persisted_transport
        assert SAFE_BLOCKED_MESSAGE not in persisted_transport
        _assert_safe_close(db, session, result)
