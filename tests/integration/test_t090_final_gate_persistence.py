"""T125 integration coverage for the T090 final gate and private persistence."""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy import event
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.application.orchestration.final_output_gate import (
    FinalOutputGateError,
    decide_final_output,
    persist_final_output,
)
from oralia.application.orchestration.output_proposal_builder import build_output_proposal
from oralia.domain.agents.fallback_agent import SAFE_FALLBACK_TEXT
from oralia.domain.policies.output_authorization_contract import (
    AuthorizationConfigurationIdentity,
    AuthorizationSnapshot,
    ScopeReference,
    TrustedTemplate,
)
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import (
    SAFE_TECHNICAL_FALLBACK,
    OutputTemplateCatalog,
    OutputTemplateEntry,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine

_SAFE_TEXT = "A safe activity response."
_REJECTED_MARKER = "T090_REJECTED_PRIVATE_125"
_REJECTED_TEXT = f"{_REJECTED_MARKER}: Tu nota es 9."


def _entry(template_id: str, text: str) -> OutputTemplateEntry:
    return OutputTemplateEntry.from_text(
        template_id=template_id,
        version=1,
        message_type="normal",
        text=text,
        topic_ref="activity",
        purpose_ref="inform",
        action_ref="continue",
    )


_SAFE_ENTRY = _entry("normal-safe", _SAFE_TEXT)
_REJECTED_ENTRY = _entry("normal-rejected", _REJECTED_TEXT)
_CATALOG = OutputTemplateCatalog(
    entries=(_SAFE_ENTRY, _REJECTED_ENTRY, SAFE_TECHNICAL_FALLBACK)
)


def _policy(*, allow_operational: bool) -> OutputAuthorizationPolicy:
    return OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": "gate-policy",
            "policy_version": 1,
            "allowed_recipients": ["participant-a"],
            "allowed_disclosures": [],
            "allowed_scopes": {
                "topics": ["activity"],
                "purposes": ["inform", "technical_recovery"],
                "actions": ["continue", "clarify"],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [
                [_SAFE_ENTRY.template_id, 1],
                [_REJECTED_ENTRY.template_id, 1],
            ],
            "allowed_operational_messages": (
                [[SAFE_TECHNICAL_FALLBACK.template_id, 1]] if allow_operational else []
            ),
        }
    )


def _trusted_template(entry: OutputTemplateEntry) -> TrustedTemplate:
    return TrustedTemplate(
        template_id=entry.template_id,
        template_version=entry.version,
        message_type=entry.message_type,
        text=entry.text,
        sha256=entry.sha256,
        scope=ScopeReference(
            topic_ref=entry.topic_ref,
            purpose_ref=entry.purpose_ref,
            action_ref=entry.action_ref,
        ),
    )


def _snapshot(
    session: models.Session,
    activity: models.ActivityConfiguration,
    *,
    allow_operational: bool,
) -> AuthorizationSnapshot:
    policy = _policy(allow_operational=allow_operational)
    raw = canonical_policy_json(policy)
    digest = canonical_policy_sha256(raw)
    activity.output_authorization_policy_json = raw
    activity.output_authorization_policy_sha256 = digest
    return AuthorizationSnapshot(
        configuration=AuthorizationConfigurationIdentity(
            session_id=session.id,
            activity_configuration_id=activity.id,
            activity_version=activity.version,
            policy_id=policy.policy_id,
            policy_version=policy.policy_version,
            schema_version=policy.schema_version,
            policy_sha256=digest,
        ),
        recipient=session.participant_code,
        policy=policy,
        configuration_general_knowledge_allowed=False,
        templates=tuple(_trusted_template(entry) for entry in _CATALOG.entries),
        data_references=(),
    )


def _proposal(snapshot: AuthorizationSnapshot, entry: OutputTemplateEntry):
    return build_output_proposal(
        snapshot,
        template_id=entry.template_id,
        template_version=entry.version,
        template_sha256=entry.sha256,
        catalog=_CATALOG,
    )


@pytest.fixture
def gate_context(
    tmp_path: Path,
) -> Iterator[tuple[SASession, models.Session, models.ActivityConfiguration, models.Turn]]:
    engine = build_engine(f"sqlite:///{tmp_path / 't125.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = factory()
    try:
        course = models.Course(name="T125", subject_code="T125")
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
            name="T125 activity",
            subject="Authorization",
            objective="Test the final gate",
            mode="dialogue",
            language="en",
            max_turns=5,
            max_duration_seconds=300,
            general_knowledge_allowed=False,
            required_agent_ids=[],
            optional_agent_ids=[],
            retention_policy_id=retention.id,
        )
        db.add(activity)
        db.flush()
        session = models.Session(
            activity_configuration_id=activity.id,
            participant_code=participant.code,
            status="active",
            active_lock_token="ACTIVE",
        )
        db.add(session)
        db.flush()
        turn = models.Turn(
            session_id=session.id,
            index=0,
            input_text="participant input",
            status="in_progress",
        )
        db.add(turn)
        db.flush()
        yield db, session, activity, turn
    finally:
        db.close()
        engine.dispose()


@pytest.mark.integration
def test_rejected_attempt_zero_then_approved_operational_attempt_is_persisted_once(
    gate_context,
) -> None:
    db, session, activity, turn = gate_context
    snapshot = _snapshot(session, activity, allow_operational=True)
    decision = decide_final_output(
        snapshot,
        _proposal(snapshot, _REJECTED_ENTRY),
        catalog=_CATALOG,
    )

    assert decision.blocked is True
    assert decision.turn_status == "degraded"
    assert decision.output_text == SAFE_FALLBACK_TEXT
    assert [attempt.attempt for attempt in decision.attempts] == [0, 1]
    assert decision.attempts[0].verdict == "block"
    assert decision.attempts[1].verdict == "approved"

    commit_calls: list[None] = []

    def _record_commit(_session: SASession) -> None:
        commit_calls.append(None)

    event.listen(db, "after_commit", _record_commit)
    try:
        persisted = persist_final_output(
            db,
            turn,
            decision,
            generator_agent_id="safe-fallback",
        )
    finally:
        event.remove(db, "after_commit", _record_commit)
    assert commit_calls == []
    db.refresh(turn)
    assert turn.status == "degraded"
    assert turn.output_text == SAFE_FALLBACK_TEXT
    assert session.status == "active"
    assert session.active_lock_token == "ACTIVE"
    assert db.in_transaction()

    proposals = db.query(models.GeneratedProposal).filter_by(turn_id=turn.id).all()
    verifications = db.query(models.VerificationResult).all()
    events = db.query(models.TraceEvent).filter_by(turn_id=turn.id).all()
    assert len(proposals) == len(verifications) == 1
    assert len(events) == 2
    assert verifications[0].id == persisted.verification_result_id
    assert verifications[0].verdict == "approved"
    assert verifications[0].reasons == []
    assert verifications[0].authorization_context["attempt"] == 1
    assert proposals[0].content["text"] == SAFE_FALLBACK_TEXT

    persisted_payload = json.dumps(
        {
            "proposal": proposals[0].content,
            "verification": verifications[0].authorization_context,
            "events": [event.payload for event in events],
        },
        sort_keys=True,
    )
    assert _REJECTED_MARKER not in persisted_payload
    with pytest.raises(FinalOutputGateError):
        persist_final_output(db, turn, decision, generator_agent_id="safe-fallback")


@pytest.mark.integration
def test_blocked_operational_attempt_has_no_third_attempt_or_visible_text(gate_context) -> None:
    db, session, activity, turn = gate_context
    snapshot = _snapshot(session, activity, allow_operational=False)
    decision = decide_final_output(
        snapshot,
        _proposal(snapshot, _REJECTED_ENTRY),
        catalog=_CATALOG,
    )

    assert [attempt.attempt for attempt in decision.attempts] == [0, 1]
    assert decision.final_verdict.verdict == "block"
    assert [reason.value for reason in decision.final_verdict.reason_codes] == [
        "unauthorized_data",
        "unsafe_fallback",
    ]
    assert decision.output_text is None
    assert decision.dialogue_action == "finish"

    persist_final_output(db, turn, decision, generator_agent_id="safe-fallback")
    db.refresh(turn)
    assert turn.output_text is None
    assert turn.status == "blocked"
    assert session.status == "active"
    assert db.query(models.TraceEvent).filter_by(turn_id=turn.id).count() == 2


@pytest.mark.integration
@pytest.mark.parametrize("upstream_status", ["error", "timeout"])
def test_upstream_error_or_timeout_consumes_direct_operational_attempt(
    gate_context,
    upstream_status: str,
) -> None:
    db, session, activity, turn = gate_context
    snapshot = _snapshot(session, activity, allow_operational=True)
    decision = decide_final_output(
        snapshot,
        None,
        upstream_status=upstream_status,
        catalog=_CATALOG,
    )

    assert [attempt.attempt for attempt in decision.attempts] == [1]
    assert decision.output_text == SAFE_FALLBACK_TEXT
    assert decision.turn_status == "degraded"
    persist_final_output(db, turn, decision, generator_agent_id="safe-fallback")
    assert db.query(models.TraceEvent).filter_by(turn_id=turn.id).count() == 1


@pytest.mark.integration
def test_text_transformed_after_approval_requires_a_new_gate_decision(gate_context) -> None:
    _, session, activity, _ = gate_context
    snapshot = _snapshot(session, activity, allow_operational=True)
    safe = decide_final_output(snapshot, _proposal(snapshot, _SAFE_ENTRY), catalog=_CATALOG)
    transformed = decide_final_output(
        snapshot,
        _proposal(snapshot, _REJECTED_ENTRY),
        catalog=_CATALOG,
    )

    assert safe.output_text == _SAFE_TEXT
    assert safe.blocked is False
    assert transformed.blocked is True
    assert transformed.attempts[0].verdict == "block"
    assert transformed.output_text == SAFE_FALLBACK_TEXT
    assert _REJECTED_MARKER not in transformed.output_text
