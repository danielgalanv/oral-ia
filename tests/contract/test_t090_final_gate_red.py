"""T094: red contract reproductions for the missing final constitutional gate."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.application.orchestration import turn_orchestrator
from oralia.application.orchestration.turn_orchestrator import run_turn
from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import (
    AgentError,
    AgentRequest,
    AgentResult,
    CancellationToken,
)
from oralia.domain.policies.constitutional_control import ConstitutionalControl
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine
from tests.t090_authorization_contract_helpers import trusted_snapshot_from_dict

_ORDINARY_TEXT = "Continuemos con la actividad."
_SESSION_ID = "00000000-0000-0000-0000-000000000094"
_TURN_ID = "00000000-0000-0000-0000-000000000095"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _policy() -> dict:
    return {
        "policy_id": "final-gate-policy",
        "policy_version": 1,
        "schema_version": 1,
        "allowed_recipients": ["participant-a"],
        "general_knowledge_allowed": False,
        "allowed_templates": [["normal-message", 1]],
        # No operational message is authorized: every failed attempt must close
        # without visible text instead of falling through to a canned response.
        "allowed_operational_messages": [],
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
    }


def _snapshot(*, policy: dict | None = None) -> dict:
    effective_policy = _policy() if policy is None else policy
    return {
        "configuration": {
            "activity_configuration_id": "activity-1",
            "activity_version": 1,
            "policy_id": "final-gate-policy",
            "policy_version": 1,
        },
        "recipient": "participant-a",
        "policy": effective_policy,
        "templates": {
            "normal-message": {
                "template_id": "normal-message",
                "template_version": 1,
                "text": _ORDINARY_TEXT,
                "sha256": _sha256(_ORDINARY_TEXT),
                "scope": {
                    "topic_ref": "activity",
                    "purpose_ref": "continue",
                    "action_ref": "respond",
                },
            }
        },
        "data_references": {},
    }


def _proposal(text: str = _ORDINARY_TEXT) -> dict:
    return {
        "text": text,
        "message_type": "normal",
        "template_id": "normal-message",
        "template_version": 1,
        "template_sha256": _sha256(text),
        "segments": [
            {
                "start": 0,
                "end": len(text),
                "expected_text": text,
                "kind": "fixed",
                "data_ref": None,
                "topic_ref": "activity",
                "purpose_ref": "continue",
                "action_ref": "respond",
            }
        ],
    }


def _request(*, proposal: dict | None, snapshot: dict | None) -> AgentRequest:
    text = _ORDINARY_TEXT if proposal is None else proposal["text"]
    request_input = {"proposal_text": text}
    if proposal is not None:
        request_input["proposal"] = proposal
    trusted_snapshot = snapshot
    if snapshot is not None and snapshot.get("policy"):
        configuration = snapshot["configuration"]
        policy = snapshot["policy"]
        identity_matches = (
            configuration.get("policy_id", policy.get("policy_id")) == policy.get("policy_id")
            and configuration.get("policy_version", policy.get("policy_version"))
            == policy.get("policy_version")
        )
        if identity_matches:
            trusted_snapshot = trusted_snapshot_from_dict(
                snapshot,
                session_id=_SESSION_ID,
            )
    context = (
        {}
        if snapshot is None
        else {
            "activity_configuration_id": (
                trusted_snapshot.configuration.activity_configuration_id
                if hasattr(trusted_snapshot, "configuration")
                else snapshot["configuration"]["activity_configuration_id"]
            ),
            "actual_recipient": "participant-a",
            "authorization_snapshot": trusted_snapshot,
        }
    )
    return AgentRequest(
        session_id=_SESSION_ID,
        turn_id=_TURN_ID,
        input=request_input,
        context=context,
    )


def _execute_control(request: AgentRequest) -> AgentResult:
    return asyncio.run(ConstitutionalControl().execute(request, CancellationToken()))


@pytest.mark.contract
def test_structured_authorized_proposal_remains_approved() -> None:
    result = _execute_control(_request(proposal=_proposal(), snapshot=_snapshot()))

    assert result.status == "ok"
    assert result.output is not None
    assert result.output["verdict"] == "approved"
    assert result.output["reasons"] == []


@pytest.mark.contract
def test_text_only_request_closes_on_missing_policy() -> None:
    result = _execute_control(_request(proposal=None, snapshot=None))

    assert result.status == "ok"
    assert result.output is not None
    assert result.output["verdict"] == "block"
    assert result.output["reasons"] == ["missing_policy"]


@pytest.mark.contract
@pytest.mark.parametrize(
    "case_id,proposal,snapshot,expected_reason",
    [
        (
            "missing_policy_precedes_malformed_proposal",
            {**_proposal(), "segments": []},
            _snapshot(policy={}),
            "missing_policy",
        ),
        (
            "invalid_context_precedes_malformed_proposal",
            {**_proposal(), "segments": []},
            {
                **_snapshot(),
                "configuration": {
                    **_snapshot()["configuration"],
                    "policy_version": 999,
                },
            },
            "invalid_context",
        ),
        (
            "invalid_proposal_precedes_invented_reference",
            {
                **_proposal(),
                "segments": [
                    {
                        **_proposal()["segments"][0],
                        "start": 1,
                        "data_ref": "invented-reference",
                    }
                ],
            },
            _snapshot(),
            "invalid_proposal",
        ),
    ],
    ids=lambda value: value if isinstance(value, str) and "_precedes_" in value else None,
)
def test_early_gate_reason_short_circuits_later_failures(
    case_id: str,
    proposal: dict,
    snapshot: dict,
    expected_reason: str,
) -> None:
    result = _execute_control(_request(proposal=proposal, snapshot=snapshot))

    assert result.status == "ok", case_id
    assert result.output is not None, case_id
    assert result.output["verdict"] == "block", case_id
    assert result.output["reasons"] == [expected_reason], case_id


@pytest.mark.contract
def test_authorization_scope_and_h02_reasons_are_complete_and_ordered() -> None:
    text = "Tu nota es 9."
    proposal = _proposal(text)
    proposal["segments"][0].update(
        {
            "kind": "slot",
            "data_ref": "denied-record",
            "topic_ref": "outside-activity",
            "value_sha256": _sha256(text),
        }
    )
    snapshot = _snapshot()
    snapshot["templates"]["normal-message"].update(
        {"text": text, "sha256": _sha256(text)}
    )
    snapshot["data_references"] = {
        "denied-record": {
            "category": "private_record",
            "provenance": "internal_record",
            "recipient": "participant-a",
            "scope": {
                "topic_ref": "outside-activity",
                "purpose_ref": "continue",
                "action_ref": "respond",
            },
        }
    }
    denied_reference = snapshot["data_references"]["denied-record"]
    assert proposal["template_sha256"] == snapshot["templates"]["normal-message"]["sha256"]
    assert "value" not in denied_reference
    assert "value_sha256" not in denied_reference

    result = _execute_control(_request(proposal=proposal, snapshot=snapshot))

    assert result.status == "ok"
    assert result.output is not None
    assert result.output["verdict"] == "block"
    assert result.output["reasons"] == [
        "unauthorized_data",
        "out_of_scope",
        "assigns_grade",
    ]


def _contract(agent_id: str, *, timeout_ms: int = 100) -> AgentContractSchema:
    return AgentContractSchema(
        agent_id=agent_id,
        version="1.0.0",
        purpose="local T094 behavioral double",
        input_schema_ref="AgentRequest",
        output_schema_ref="AgentResult",
        timeout_ms=timeout_ms,
    )


class _NoOutputVerifier:
    contract = _contract("no-output-verifier")

    async def execute(
        self, request: AgentRequest, cancellation: CancellationToken
    ) -> AgentResult:
        return AgentResult(status="ok", output=None, confidence=1.0)


class _EventBlockedVerifier:
    contract = _contract("event-blocked-verifier", timeout_ms=10)

    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def execute(
        self, request: AgentRequest, cancellation: CancellationToken
    ) -> AgentResult:
        self.started.set()
        await self.release.wait()
        return AgentResult(status="ok", output={"verdict": "approved", "reasons": []})


class _ErrorInterpreter:
    contract = _contract("error-interpreter")

    async def execute(
        self, request: AgentRequest, cancellation: CancellationToken
    ) -> AgentResult:
        return AgentResult(
            status="error",
            output=None,
            error=AgentError(code="UPSTREAM_FAILURE", message="controlled failure"),
        )


class _CountingFallback:
    contract = _contract("counting-fallback")

    def __init__(self, text: str) -> None:
        self.text = text
        self.calls = 0

    async def execute(
        self, request: AgentRequest, cancellation: CancellationToken
    ) -> AgentResult:
        self.calls += 1
        return AgentResult(status="ok", output={"text": self.text}, confidence=1.0)


@pytest.fixture
def local_turn_context(tmp_path: Path) -> Iterator[tuple[SASession, models.Session]]:
    engine = build_engine(f"sqlite:///{tmp_path / 't094.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = session_factory()

    course = models.Course(name="T094 course", subject_code="T094")
    retention = models.RetentionPolicy(
        content_scope="session",
        access_scope="teacher",
        purge_rule="manual",
    )
    participant = models.ParticipantCode(code="participant-a")
    db.add_all([course, retention, participant])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="T094 activity",
        subject="Contract verification",
        objective="Exercise the current final output path",
        mode="dialogue",
        language="en",
        max_turns=5,
        max_duration_seconds=300,
        general_knowledge_allowed=False,
        required_agent_ids=[],
        optional_agent_ids=[],
        retention_policy_id=retention.id,
    )
    policy = _policy()
    canonical_policy_json = json.dumps(
        policy,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    activity.output_authorization_policy_json = canonical_policy_json
    activity.output_authorization_policy_sha256 = _sha256(canonical_policy_json)
    assert isinstance(activity.output_authorization_policy_json, str)
    assert json.loads(activity.output_authorization_policy_json) == policy
    assert activity.output_authorization_policy_sha256 == _sha256(
        activity.output_authorization_policy_json
    )
    assert participant.code == "participant-a"
    db.add(activity)
    db.flush()
    active_session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="active",
        turn_count=0,
        active_lock_token="ACTIVE",
    )
    db.add(active_session)
    db.flush()

    yield db, active_session

    db.close()
    engine.dispose()


@pytest.mark.contract
def test_missing_verifier_output_cannot_implicitly_approve(
    local_turn_context: tuple[SASession, models.Session],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db, session = local_turn_context
    monkeypatch.setitem(
        turn_orchestrator.AGENT_REGISTRY,
        "constitutional-control",
        _NoOutputVerifier(),
    )

    result = asyncio.run(run_turn(db, session, "ordinary participant input"))
    persisted_turn = db.get(models.Turn, result.turn_id)

    assert persisted_turn is not None
    assert result.blocked is True
    assert result.output_text is None
    assert result.dialogue_action == "finish"
    db.refresh(session)
    assert session.status == "closed_error_safe"


@pytest.mark.contract
def test_verifier_timeout_closes_without_publishing_or_retry_race(
    local_turn_context: tuple[SASession, models.Session],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db, session = local_turn_context
    verifier = _EventBlockedVerifier()
    fallback = _CountingFallback("A single operational alternative.")
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "constitutional-control", verifier)
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "safe-fallback", fallback)

    result = asyncio.run(run_turn(db, session, "original proposal must remain hidden"))
    persisted_turn = db.get(models.Turn, result.turn_id)

    assert verifier.started.is_set()
    assert fallback.calls == 1
    assert persisted_turn is not None
    assert "original proposal must remain hidden" not in (result.output_text or "")
    assert result.output_text is None
    assert result.blocked is True
    assert result.dialogue_action == "finish"
    db.refresh(session)
    assert session.status == "closed_error_safe"


@pytest.mark.contract
def test_blocked_single_fallback_never_emits_a_third_message(
    local_turn_context: tuple[SASession, models.Session],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db, session = local_turn_context
    blocked_alternative = "Tu nota es 9."
    fallback = _CountingFallback(blocked_alternative)
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "interpreter", _ErrorInterpreter())
    monkeypatch.setitem(turn_orchestrator.AGENT_REGISTRY, "safe-fallback", fallback)
    monkeypatch.setattr(turn_orchestrator, "SAFE_FALLBACK_TEXT", blocked_alternative)

    result = asyncio.run(run_turn(db, session, "trigger controlled upstream failure"))
    persisted_turn = db.get(models.Turn, result.turn_id)

    assert fallback.calls == 1
    assert persisted_turn is not None
    assert persisted_turn.output_text is None
    assert result.blocked is True
    assert result.output_text is None
    assert result.dialogue_action == "finish"
    db.refresh(session)
    assert session.status == "closed_error_safe"
