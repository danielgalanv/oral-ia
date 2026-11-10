"""T098: red integration coverage for the three final T090 outcomes."""

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

from oralia.application.commands.end_session import end_session_voluntarily
from oralia.application.commands.start_session import StartSessionInput, start_session
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

_SC007_TEXT = "He recibido tu mensaje. Continuemos con la actividad."
_NO_ECHO_SENTINEL = "T090_NO_ECHO_SENTINEL_5A72"
_OPERATIONAL_TEXT = turn_orchestrator.SAFE_FALLBACK_TEXT
_NORMAL_TEMPLATE_ID = "sc007-acknowledgement"
_OPERATIONAL_TEMPLATE_ID = "safe-technical-fallback"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _policy(*, operational_allowed: bool) -> dict[str, Any]:
    return {
        "policy_id": "t098-positive-cycle-policy",
        "policy_version": 1,
        "schema_version": 1,
        "allowed_recipients": ["participant-a"],
        "allowed_templates": [[_NORMAL_TEMPLATE_ID, 1]],
        "allowed_operational_messages": (
            [[_OPERATIONAL_TEMPLATE_ID, 1]] if operational_allowed else []
        ),
        "allowed_disclosures": [
            {
                "category": "activity_public",
                "provenance": "trusted_template",
                "recipient": "participant-a",
            }
        ],
        "allowed_scopes": {
            "topics": ["activity"],
            "purposes": ["acknowledge_turn", "technical_recovery"],
            "actions": ["continue", "clarify"],
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
    operational_allowed: bool,
) -> Iterator[
    tuple[
        SASession,
        models.ActivityConfiguration,
        models.ParticipantCode,
        dict[str, Any],
        _Resources,
    ]
]:
    engine = build_engine(f"sqlite:///{tmp_path / 't098.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = session_factory()
    resources = _Resources()
    policy = _policy(operational_allowed=operational_allowed)

    try:
        course = models.Course(name="T098 course", subject_code="T098")
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
            name="T098 positive cycle",
            subject="Final output authorization",
            objective="Complete the ordinary activity turn",
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
            "template_id": _NORMAL_TEMPLATE_ID,
            "template_version": 1,
            "text": _SC007_TEXT,
            "sha256": _sha256(_SC007_TEXT),
            "topic_ref": "activity",
            "purpose_ref": "acknowledge_turn",
            "action_ref": "continue",
        }
        activity.operational_output_template = {
            "template_id": _OPERATIONAL_TEMPLATE_ID,
            "template_version": 1,
            "text": _OPERATIONAL_TEXT,
            "sha256": _sha256(_OPERATIONAL_TEXT),
            "topic_ref": "activity",
            "purpose_ref": "technical_recovery",
            "action_ref": "clarify",
        }

        assert isinstance(activity.output_authorization_policy_json, str)
        assert json.loads(activity.output_authorization_policy_json) == policy
        assert _canonical_policy(json.loads(canonical)) == canonical
        assert activity.output_authorization_policy_sha256 == _sha256(canonical)
        assert activity.normal_output_template["sha256"] == _sha256(_SC007_TEXT)
        assert activity.operational_output_template["sha256"] == _sha256(_OPERATIONAL_TEXT)
        expected_operational = [[_OPERATIONAL_TEMPLATE_ID, 1]] if operational_allowed else []
        assert policy["allowed_operational_messages"] == expected_operational
        assert policy["allowed_recipients"] == [participant.code]

        db.add(activity)
        db.flush()
        yield db, activity, participant, policy, resources
    finally:
        db.close()
        resources.db_closed = True
        engine.dispose()
        resources.engine_disposed = True


class _ErrorInterpreter:
    contract = SimpleNamespace(agent_id="interpreter", timeout_ms=100)

    def __init__(self) -> None:
        self.calls = 0
        self.last_result: AgentResult | None = None

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        self.last_result = AgentResult(
            status="error",
            error=AgentError(
                code="T098_UPSTREAM_FAILURE",
                message="controlled upstream failure",
                recoverable=True,
            ),
        )
        return self.last_result


class _CountingFallback:
    contract = SimpleNamespace(agent_id="safe-fallback", timeout_ms=100)

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        self.calls += 1
        return AgentResult(status="ok", output={"text": _OPERATIONAL_TEXT}, confidence=1.0)


def _start(db: SASession, activity: models.ActivityConfiguration) -> models.Session:
    session = start_session(
        db,
        StartSessionInput(
            participant_code="participant-a",
            activity_configuration_id=activity.id,
        ),
    )
    assert session.status == "active"
    assert session.active_lock_token == "ACTIVE"
    return session


def _records(
    db: SASession,
    result: TurnResult,
) -> tuple[models.Turn, models.GeneratedProposal, models.VerificationResult]:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
    verification = db.get(models.VerificationResult, turn.verification_result_id)
    assert proposal is not None
    assert verification is not None
    return turn, proposal, verification


def _install_failure_path(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[_ErrorInterpreter, _CountingFallback]:
    interpreter = _ErrorInterpreter()
    fallback = _CountingFallback()
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", interpreter)
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "safe-fallback", fallback)
    return interpreter, fallback


def _assert_direct_operational_attempt(
    db: SASession,
    result: TurnResult,
    interpreter: _ErrorInterpreter,
    fallback: _CountingFallback,
) -> None:
    messages = db.query(models.InternalMessage).filter_by(turn_id=result.turn_id).all()
    fallback_messages = [
        message for message in messages if message.receiver_agent_id == "safe-fallback"
    ]

    assert interpreter.calls == 1
    assert interpreter.last_result is not None
    assert interpreter.last_result.status == "error"
    assert interpreter.last_result.output is None
    assert fallback.calls == 1
    assert len(fallback_messages) <= 1


@pytest.mark.integration
def test_historical_sc007_cycle_remains_operational(tmp_path: Path) -> None:
    with _local_context(tmp_path, operational_allowed=True) as (
        db,
        activity,
        _,
        _,
        resources,
    ):
        session = _start(db, activity)
        result = asyncio.run(run_turn(db, session, "ordinary participant input"))
        turn, proposal, verification = _records(db, result)

        assert result.blocked is False
        assert result.status == "completed"
        assert result.output_text
        assert turn.status == "completed"
        assert turn.output_text == result.output_text
        assert proposal.content.get("text") == result.output_text
        assert verification.verdict == "approved"
        assert turn.generated_proposal_id == proposal.id
        assert turn.verification_result_id == verification.id
        assert verification.proposal_id == proposal.id

        closed = end_session_voluntarily(db, session)
        db.refresh(closed)
        closed_events = (
            db.query(models.TraceEvent)
            .filter_by(session_id=session.id, event_type="session_closed")
            .all()
        )
        assert closed.status == "closed_voluntary"
        assert closed.ended_at is not None
        assert closed.technical_summary_ref is not None
        assert closed.active_lock_token is None
        assert len(closed_events) == 1

    assert resources.db_closed is True
    assert resources.engine_disposed is True


@pytest.mark.integration
def test_authorized_normal_output_uses_sc007_without_echo(tmp_path: Path) -> None:
    with _local_context(tmp_path, operational_allowed=True) as (db, activity, _, _, _):
        session = _start(db, activity)
        result = asyncio.run(run_turn(db, session, _NO_ECHO_SENTINEL))
        turn, proposal, verification = _records(db, result)
        fallback_count = (
            db.query(models.InternalMessage)
            .filter_by(turn_id=turn.id, receiver_agent_id="safe-fallback")
            .count()
        )
        authorization_context = getattr(verification, "authorization_context", None)
        db.refresh(session)

        assert fallback_count == 0
        assert verification.verdict == "approved"
        assert verification.reasons == []
        assert session.status == "active"
        if authorization_context is not None:
            assert authorization_context.get("attempt") == 0
            assert authorization_context.get("message_type") == "normal"
        assert result.blocked is False
        assert result.status == "completed"
        assert result.output_text == _SC007_TEXT
        assert turn.output_text == _SC007_TEXT
        assert proposal.content.get("text") == _SC007_TEXT
        assert _NO_ECHO_SENTINEL not in result.output_text
        assert _NO_ECHO_SENTINEL not in turn.output_text
        assert _NO_ECHO_SENTINEL not in json.dumps(proposal.content, ensure_ascii=False)


@pytest.mark.integration
def test_authorized_operational_fallback_is_visible_and_degraded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter, fallback = _install_failure_path(monkeypatch)
    with _local_context(tmp_path, operational_allowed=True) as (
        db,
        activity,
        _,
        policy,
        _,
    ):
        assert policy["allowed_operational_messages"] == [[_OPERATIONAL_TEMPLATE_ID, 1]]
        session = _start(db, activity)
        result = asyncio.run(run_turn(db, session, "trigger upstream failure"))
        turn, _, verification = _records(db, result)
        _assert_direct_operational_attempt(db, result, interpreter, fallback)
        authorization_context = getattr(verification, "authorization_context", None)
        verification_count = (
            db.query(models.VerificationResult)
            .filter_by(proposal_id=verification.proposal_id)
            .count()
        )
        db.refresh(session)

        assert verification_count == 1
        assert result.output_text == _OPERATIONAL_TEXT
        assert turn.output_text == _OPERATIONAL_TEXT
        assert result.blocked is True
        assert result.status == "degraded"
        assert result.dialogue_action == "clarify"
        assert session.status == "active"
        assert verification.verdict == "approved"
        assert verification.reasons == []
        assert authorization_context is not None
        assert authorization_context.get("attempt") == 1
        assert authorization_context.get("message_type") == "operational"
        assert authorization_context.get("policy_id") == policy["policy_id"]
        assert authorization_context.get("policy_version") == policy["policy_version"]
        assert authorization_context.get("schema_version") == policy["schema_version"]
        assert authorization_context.get("template_id") == _OPERATIONAL_TEMPLATE_ID
        assert authorization_context.get("template_version") == 1
        assert authorization_context.get("template_sha256") == activity.operational_output_template[
            "sha256"
        ]


@pytest.mark.integration
def test_unauthorized_operational_fallback_closes_without_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    interpreter, fallback = _install_failure_path(monkeypatch)
    with _local_context(tmp_path, operational_allowed=False) as (
        db,
        activity,
        _,
        policy,
        _,
    ):
        assert policy["allowed_operational_messages"] == []
        session = _start(db, activity)
        result = asyncio.run(run_turn(db, session, "trigger upstream failure"))
        turn, _, verification = _records(db, result)
        _assert_direct_operational_attempt(db, result, interpreter, fallback)
        authorization_context = getattr(verification, "authorization_context", None)
        verification_count = (
            db.query(models.VerificationResult)
            .filter_by(proposal_id=verification.proposal_id)
            .count()
        )

        assert verification_count == 1
        assert result.blocked is True
        assert result.output_text is None
        assert turn.output_text is None
        assert result.dialogue_action == "finish"
        assert turn.status == "blocked"
        db.refresh(session)
        assert session.status == "closed_error_safe"
        assert session.ended_at is not None
        assert session.technical_summary_ref is not None
        assert session.active_lock_token is None
        closed_events = (
            db.query(models.TraceEvent)
            .filter_by(session_id=session.id, event_type="session_closed")
            .all()
        )
        assert len(closed_events) == 1
        assert verification.verdict == "block"
        assert verification.reasons
        assert verification.reasons[-1] == "unsafe_fallback"
        assert authorization_context is not None
        assert authorization_context.get("attempt") == 1
        assert authorization_context.get("message_type") == "operational"
        assert _OPERATIONAL_TEXT not in (result.output_text or "")
        assert SAFE_BLOCKED_MESSAGE not in (result.output_text or "")
