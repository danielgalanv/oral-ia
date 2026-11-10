"""T149: fail-closed orchestration and non-fabricated material authority."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from oralia.application.orchestration.self_study_agency_composer import run_study_turn
from oralia.application.orchestration.turn_orchestrator import run_turn
from oralia.infrastructure.db import models
from tests.integration.test_t090_main_turn_red import _local_turn_context
from tests.integration.test_t090_self_study_fallback_red import (
    _EVIDENCE,
    _INITIAL_TEXT,
    _install_pipeline,
    _local_context,
)

_DENIED_SENTINEL = "T149_DENIED_MATERIAL_93A1"


def _assert_closed_result(db, session, result, expected_reason: str) -> models.Turn:
    turn = db.get(models.Turn, result.turn_id)
    assert turn is not None
    verification = db.get(models.VerificationResult, turn.verification_result_id)
    action = db.get(models.DialogueAction, turn.dialogue_action_id)
    assert result.blocked is True
    assert result.output_text is None
    assert turn.status == "blocked"
    assert turn.output_text is None
    assert action.action_type == "finish"
    assert expected_reason in verification.reasons
    db.refresh(session)
    assert session.status == "closed_error_safe"
    assert (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session.id, models.Turn.status == "in_progress")
        .count()
        == 0
    )
    return turn


@pytest.mark.integration
@pytest.mark.parametrize(
    ("configuration", "expected_reason"),
    (("missing", "missing_policy"), ("invalid", "invalid_context"), ("missing_catalog", "invalid_context")),
)
def test_main_turn_closes_safely_for_untrusted_configuration(
    tmp_path: Path,
    configuration: str,
    expected_reason: str,
) -> None:
    policy = None
    if configuration == "missing_catalog":
        from tests.integration.test_t090_main_turn_red import _policy

        policy = _policy()
        policy["allowed_templates"] = [["unregistered-template", 99]]
    with _local_turn_context(tmp_path, policy=policy) as (db, session, _):
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        if configuration == "missing":
            activity.output_authorization_policy_json = None
            activity.output_authorization_policy_sha256 = None
        elif configuration == "invalid":
            activity.output_authorization_policy_json = "{invalid-json"
        db.add(activity)
        db.flush()

        result = asyncio.run(run_turn(db, session, "T149_PRIVATE_INPUT"))
        turn = _assert_closed_result(db, session, result, expected_reason)
        persisted = json.dumps(
            {
                "proposal": db.get(models.GeneratedProposal, turn.generated_proposal_id).content,
                "verification": db.get(
                    models.VerificationResult,
                    turn.verification_result_id,
                ).authorization_context,
                "events": [event.payload for event in db.query(models.TraceEvent).filter_by(turn_id=turn.id)],
            },
            ensure_ascii=False,
        )
        assert "T149_PRIVATE_INPUT" not in persisted


@pytest.mark.integration
def test_missing_policy_turn_rolls_back_as_one_outer_transaction(tmp_path: Path) -> None:
    with _local_turn_context(tmp_path) as (db, session, _):
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        activity.output_authorization_policy_json = None
        activity.output_authorization_policy_sha256 = None
        db.add(activity)
        db.commit()
        session_id = session.id

        result = asyncio.run(run_turn(db, session, "rollback-sensitive"))
        assert result.output_text is None
        db.rollback()

        persisted_session = db.get(models.Session, session_id)
        assert persisted_session.status == "active"
        assert persisted_session.active_lock_token == "ACTIVE"
        assert db.query(models.Turn).filter_by(session_id=session_id).count() == 0
        assert db.query(models.VerificationResult).count() == 0


@pytest.mark.integration
def test_main_turn_has_one_decision_and_one_attempt_evidence(tmp_path: Path) -> None:
    with _local_turn_context(tmp_path) as (db, session, _):
        result = asyncio.run(run_turn(db, session, "ordinary input"))
        attempts = (
            db.query(models.TraceEvent)
            .filter_by(
                turn_id=result.turn_id,
                event_type="output_authorization_attempt",
            )
            .all()
        )
        transports = (
            db.query(models.InternalMessage)
            .filter_by(
                turn_id=result.turn_id,
                receiver_agent_id="constitutional-control",
                type="agent_invocation",
            )
            .all()
        )
        assert result.blocked is False
        assert len(attempts) == 1
        assert attempts[0].payload["attempt"] == 0
        assert len(transports) == 1


@pytest.mark.integration
@pytest.mark.parametrize(
    ("configuration", "expected_reason"),
    (("missing", "missing_policy"), ("invalid", "invalid_context"), ("missing_catalog", "invalid_context")),
)
def test_self_study_closes_safely_for_untrusted_configuration(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    configuration: str,
    expected_reason: str,
) -> None:
    allowed = (
        [["unregistered-template", 99]]
        if configuration == "missing_catalog"
        else [["material-fragment-response", 1]]
    )
    _install_pipeline(monkeypatch, mode="doubt_resolution", fragments=_EVIDENCE)
    with _local_context(
        tmp_path,
        mode="doubt_resolution",
        allowed_templates=allowed,
    ) as (db, session, _, _):
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        if configuration == "missing":
            activity.output_authorization_policy_json = None
            activity.output_authorization_policy_sha256 = None
        elif configuration == "invalid":
            activity.output_authorization_policy_json = "[]"
        db.add(activity)
        db.flush()

        result = asyncio.run(run_study_turn(db, session, "explica el material"))
        _assert_closed_result(db, session, result, expected_reason)


@pytest.mark.integration
@pytest.mark.parametrize("missing_metadata", (False, True))
def test_retrievable_but_non_presentable_material_never_acquires_authority(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    missing_metadata: bool,
) -> None:
    fragment = {**_EVIDENCE[0], "text": _DENIED_SENTINEL}
    if missing_metadata:
        fragment.pop("document_id")
    _install_pipeline(monkeypatch, mode="doubt_resolution", fragments=[fragment])
    with _local_context(
        tmp_path,
        mode="doubt_resolution",
        allowed_templates=[["material-fragment-response", 1]],
        policy_overrides={
            "allowed_disclosures": [
                {
                    "category": "texto",
                    "provenance": "different_provenance",
                    "recipient": "participant-a",
                }
            ]
        },
    ) as (db, session, _, _):
        row = db.get(models.MaterialFragment, "fragment-t096")
        row.text = _DENIED_SENTINEL
        db.add(row)
        db.flush()

        result = asyncio.run(run_study_turn(db, session, "explica"))
        turn = _assert_closed_result(db, session, result, "invalid_context")
        persisted = json.dumps(
            {
                "proposal": db.get(models.GeneratedProposal, turn.generated_proposal_id).content,
                "verification": db.get(
                    models.VerificationResult,
                    turn.verification_result_id,
                ).authorization_context,
                "events": [event.payload for event in db.query(models.TraceEvent).filter_by(turn_id=turn.id)],
            },
            ensure_ascii=False,
        )
        assert _DENIED_SENTINEL not in persisted


@pytest.mark.integration
def test_cataloged_material_slot_with_real_metadata_is_authorized_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agents = _install_pipeline(monkeypatch, mode="doubt_resolution", fragments=_EVIDENCE)
    with _local_context(
        tmp_path,
        mode="doubt_resolution",
        allowed_templates=[["material-fragment-response", 1]],
    ) as (db, session, _, _):
        result = asyncio.run(run_study_turn(db, session, "explica"))
        turn = db.get(models.Turn, result.turn_id)
        verification = db.get(models.VerificationResult, turn.verification_result_id)
        attempts = (
            db.query(models.TraceEvent)
            .filter_by(turn_id=turn.id, event_type="output_authorization_attempt")
            .all()
        )
        assert result.output_text == _INITIAL_TEXT
        assert result.blocked is False
        assert verification.verdict == "approved"
        assert verification.reasons == []
        assert agents["constitutional"].calls == 1
        assert len(attempts) == 1
        assert attempts[0].payload["attempt"] == 0

