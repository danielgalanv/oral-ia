"""T095: red integration reproductions for contextual authorization in ``run_turn``."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.application.orchestration.turn_orchestrator import TurnResult, run_turn
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine

_SC007_TEXT = "He recibido tu mensaje. Continuemos con la actividad."
_PRIVATE_SENTINEL = "T090_PRIVATE_SENTINEL_7F31"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _policy(
    *,
    topics: list[str] | None = None,
    purposes: list[str] | None = None,
    actions: list[str] | None = None,
) -> dict:
    return {
        "policy_id": "t095-main-turn-policy",
        "policy_version": 1,
        "schema_version": 1,
        "allowed_recipients": ["participant-a"],
        "allowed_templates": [["sc007-acknowledgement", 1]],
        "allowed_disclosures": [
            {
                "category": "activity_public",
                "provenance": "trusted_template",
                "recipient": "participant-a",
            }
        ],
        "allowed_scopes": {
            "topics": ["actividad"] if topics is None else topics,
            "purposes": ["acuse_turno"] if purposes is None else purposes,
            "actions": ["continuar"] if actions is None else actions,
        },
        "general_knowledge_allowed": False,
        # No operational message is authorized, so a denied recipient or scope must
        # close safely without displaying fallback content.
        "allowed_operational_messages": [],
    }


def _canonical_policy(policy: dict) -> str:
    canonical = canonical_policy_json(OutputAuthorizationPolicy.model_validate(policy))
    policy.clear()
    policy.update(json.loads(canonical))
    return canonical


@contextmanager
def _local_turn_context(
    tmp_path: Path,
    *,
    participant_code: str = "participant-a",
    policy: dict | None = None,
) -> Iterator[tuple[SASession, models.Session, dict]]:
    engine = build_engine(f"sqlite:///{tmp_path / 't095.db'}")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    db = session_factory()
    effective_policy = _policy() if policy is None else policy

    try:
        course = models.Course(name="T095 course", subject_code="T095")
        retention = models.RetentionPolicy(
            content_scope="session",
            access_scope="teacher",
            purge_rule="manual",
        )
        participant = models.ParticipantCode(code=participant_code)
        db.add_all([course, retention, participant])
        db.flush()

        canonical_policy_json = _canonical_policy(effective_policy)
        activity = models.ActivityConfiguration(
            course_id=course.id,
            name="T095 main turn",
            subject="Contextual output authorization",
            objective="Complete the SC-007 main turn",
            mode="dialogue",
            language="es",
            max_turns=5,
            max_duration_seconds=300,
            general_knowledge_allowed=False,
            required_agent_ids=[],
            optional_agent_ids=[],
            retention_policy_id=retention.id,
        )
        activity.output_authorization_policy_json = canonical_policy_json
        activity.output_authorization_policy_sha256 = _sha256(canonical_policy_json)
        activity.normal_output_template = {
            "template_id": "sc007-acknowledgement",
            "template_version": 1,
            "text": _SC007_TEXT,
            "sha256": _sha256(_SC007_TEXT),
            "topic_ref": "actividad",
            "purpose_ref": "acuse_turno",
            "action_ref": "continuar",
        }

        assert isinstance(activity.output_authorization_policy_json, str)
        assert json.loads(activity.output_authorization_policy_json) == effective_policy
        assert _canonical_policy(json.loads(canonical_policy_json)) == canonical_policy_json
        assert activity.output_authorization_policy_sha256 == _sha256(canonical_policy_json)
        assert effective_policy["allowed_operational_messages"] == []
        assert effective_policy["general_knowledge_allowed"] is False

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
        assert active_session.participant_code == participant_code

        yield db, active_session, effective_policy
    finally:
        db.close()
        engine.dispose()


def _persisted_turn(db: SASession, result: TurnResult) -> models.Turn:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    return turn


def _assert_closed_without_text(
    db: SASession,
    session: models.Session,
    result: TurnResult,
) -> None:
    turn = _persisted_turn(db, result)
    assert result.blocked is True
    assert result.output_text is None
    assert turn.output_text is None
    assert result.dialogue_action == "finish"
    db.refresh(session)
    assert session.status == "closed_error_safe"


@pytest.mark.integration
def test_authorized_sc007_main_turn_remains_visible(tmp_path: Path) -> None:
    with _local_turn_context(tmp_path) as (db, session, _):
        result = asyncio.run(run_turn(db, session, "entrada ordinaria"))
        turn = _persisted_turn(db, result)
        verification = db.get(models.VerificationResult, turn.verification_result_id)

        assert result.blocked is False
        assert result.status == "completed"
        assert result.output_text is not None
        assert turn.output_text == result.output_text
        assert verification is not None
        assert verification.verdict == "approved"
        assert verification.reasons == []


@pytest.mark.integration
def test_private_participant_input_is_not_republished(tmp_path: Path) -> None:
    with _local_turn_context(tmp_path) as (db, session, policy):
        denied_triple = {
            "category": "participant_private",
            "provenance": "participant_input",
            "recipient": "participant-a",
        }
        assert denied_triple not in policy["allowed_disclosures"]

        result = asyncio.run(run_turn(db, session, _PRIVATE_SENTINEL))
        turn = _persisted_turn(db, result)
        verification = db.get(models.VerificationResult, turn.verification_result_id)
        fallback_count = (
            db.query(models.InternalMessage)
            .filter(
                models.InternalMessage.turn_id == turn.id,
                models.InternalMessage.receiver_agent_id == "safe-fallback",
            )
            .count()
        )
        db.refresh(session)

        assert result.blocked is False
        assert result.status == "completed"
        assert session.status == "active"
        assert fallback_count == 0
        assert verification is not None
        assert verification.verdict == "approved"
        assert verification.reasons == []
        assert result.output_text == _SC007_TEXT
        assert turn.output_text == _SC007_TEXT
        assert _PRIVATE_SENTINEL not in result.output_text
        assert _PRIVATE_SENTINEL not in turn.output_text


@pytest.mark.integration
def test_real_recipient_outside_policy_closes_safely(tmp_path: Path) -> None:
    with _local_turn_context(tmp_path, participant_code="participant-b") as (db, session, policy):
        assert policy["allowed_recipients"] == ["participant-a"]
        assert session.participant_code == "participant-b"

        result = asyncio.run(run_turn(db, session, "entrada ordinaria"))

        _assert_closed_without_text(db, session, result)


@pytest.mark.integration
@pytest.mark.parametrize(
    "dimension,policy",
    [
        ("topic", _policy(topics=["tema_distinto"])),
        ("purpose", _policy(purposes=["proposito_distinto"])),
        ("action", _policy(actions=["accion_distinta"])),
    ],
    ids=["topic_out_of_scope", "purpose_out_of_scope", "action_out_of_scope"],
)
def test_each_scope_dimension_is_independently_required(
    tmp_path: Path,
    dimension: str,
    policy: dict,
) -> None:
    with _local_turn_context(tmp_path, policy=policy) as (db, session, stored_policy):
        expected_scope = {
            "topics": ["actividad"],
            "purposes": ["acuse_turno"],
            "actions": ["continuar"],
        }
        changed_key = {"topic": "topics", "purpose": "purposes", "action": "actions"}[
            dimension
        ]
        assert stored_policy["allowed_scopes"][changed_key] != expected_scope[changed_key]
        for key in expected_scope.keys() - {changed_key}:
            assert stored_policy["allowed_scopes"][key] == expected_scope[key]
        assert stored_policy["allowed_recipients"] == ["participant-a"]
        assert stored_policy["allowed_templates"] == [["sc007-acknowledgement", 1]]

        result = asyncio.run(run_turn(db, session, "entrada ordinaria"))

        _assert_closed_without_text(db, session, result)
