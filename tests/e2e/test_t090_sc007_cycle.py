"""T143 end-to-end lifecycle coverage for SC-007 and fail-closed turns."""

from __future__ import annotations

import pytest

from oralia.application.commands.end_session import close_session
from oralia.application.orchestration import turn_orchestrator
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
    load_output_authorization_policy,
)
from oralia.domain.policies.output_template_catalog import SC007_ACKNOWLEDGEMENT_TEXT
from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_minimal_output_policy


def _counts(db, session_id: str) -> tuple[int, int, int]:
    summaries = (
        db.query(models.TraceEvent)
        .filter_by(
            session_id=session_id,
            event_type="technical_summary",
        )
        .count()
    )
    closes = (
        db.query(models.TraceEvent)
        .filter_by(
            session_id=session_id,
            event_type="session_closed",
        )
        .count()
    )
    turns = db.query(models.Turn).filter_by(session_id=session_id).count()
    return summaries, closes, turns


@pytest.mark.integration
def test_sc007_turn_voluntary_close_is_idempotent_and_releases_lock(
    app_client,
    seeded_activity,
) -> None:
    configure_minimal_output_policy(
        app_client,
        seeded_activity,
        recipients=("t143-positive", "t143-replacement"),
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": "t143-positive",
            "activity_configuration_id": seeded_activity,
        },
    ).json()["session_id"]

    turn = app_client.post(
        f"/api/v1/sessions/{session_id}/turns",
        json={"text": "continúa"},
    ).json()
    assert turn["output_text"] == SC007_ACKNOWLEDGEMENT_TEXT
    assert turn["dialogue_action"] == "respond"
    assert turn.get("blocked") is not True

    first_close = app_client.post(f"/api/v1/sessions/{session_id}/end").json()
    second_close = app_client.post(f"/api/v1/sessions/{session_id}/end").json()
    assert first_close["status"] == "closed_voluntary"
    assert second_close["status"] == "closed_voluntary"

    db = app_client.__db_sessionmaker__()
    session = db.get(models.Session, session_id)
    assert session.ended_at is not None
    assert session.technical_summary_ref is not None
    assert session.active_lock_token is None
    assert _counts(db, session_id) == (1, 1, 1)
    db.close()

    replacement = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": "t143-replacement",
            "activity_configuration_id": seeded_activity,
        },
    )
    assert replacement.status_code == 201


@pytest.mark.integration
def test_unsafe_turn_closes_once_and_voluntary_close_cannot_replace_status(
    app_client,
    seeded_activity,
) -> None:
    configure_minimal_output_policy(
        app_client,
        seeded_activity,
        recipients=("t143-safe-close",),
    )
    # Entry is authorized; normal and fallback publication are deliberately denied.
    # Author the negative fixture before first use: keep the immutability trigger.
    with app_client.__db_sessionmaker__() as db:
        activity = db.get(models.ActivityConfiguration, seeded_activity)
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        ).model_dump(mode="json")
        policy["allowed_templates"] = []
        checked_policy = OutputAuthorizationPolicy.model_validate(policy)
        activity.output_authorization_policy_json = canonical_policy_json(checked_policy)
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(
            activity.output_authorization_policy_json
        )
        db.commit()
    session_id = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": "t143-safe-close",
            "activity_configuration_id": seeded_activity,
        },
    ).json()["session_id"]

    turn_result = app_client.post(
        f"/api/v1/sessions/{session_id}/turns",
        json={"text": "contenido privado"},
    ).json()
    assert turn_result["blocked"] is True
    assert turn_result["output_text"] is None
    assert turn_result["dialogue_action"] == "finish"

    repeated = app_client.post(f"/api/v1/sessions/{session_id}/end").json()
    assert repeated["status"] == "closed_error_safe"

    db = app_client.__db_sessionmaker__()
    session = db.get(models.Session, session_id)
    turn = db.get(models.Turn, turn_result["turn_id"])
    action = db.get(models.DialogueAction, turn.dialogue_action_id)
    assert session.status == "closed_error_safe"
    assert session.ended_at is not None
    assert session.technical_summary_ref is not None
    assert session.active_lock_token is None
    assert turn.status == "blocked"
    assert turn.output_text is None
    assert action.action_type == "finish"
    assert _counts(db, session_id) == (1, 1, 1)
    db.close()


@pytest.mark.integration
def test_exception_after_final_verification_rolls_back_the_whole_turn(
    app_client,
    seeded_activity,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configure_minimal_output_policy(
        app_client,
        seeded_activity,
        recipients=("t143-rollback",),
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": "t143-rollback",
            "activity_configuration_id": seeded_activity,
        },
    ).json()["session_id"]

    def _raise_after_final_persistence(*args, **kwargs):
        raise RuntimeError("T143 rollback checkpoint")

    monkeypatch.setattr(turn_orchestrator, "apply_patch", _raise_after_final_persistence)
    with pytest.raises(RuntimeError, match="T143 rollback checkpoint"):
        app_client.post(
            f"/api/v1/sessions/{session_id}/turns",
            json={"text": "rollback"},
        )

    db = app_client.__db_sessionmaker__()
    session = db.get(models.Session, session_id)
    assert session.status == "active"
    assert session.active_lock_token == "ACTIVE"
    assert session.technical_summary_ref is None
    assert _counts(db, session_id) == (0, 0, 0)
    assert db.query(models.GeneratedProposal).count() == 0
    assert db.query(models.VerificationResult).count() == 0
    db.close()


@pytest.mark.integration
def test_interleaved_close_claims_preserve_the_first_terminal_status(
    app_client,
    seeded_activity,
) -> None:
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("t143-interleaved",))
    session_id = app_client.post(
        "/api/v1/sessions",
        json={
            "participant_code": "t143-interleaved",
            "activity_configuration_id": seeded_activity,
        },
    ).json()["session_id"]
    session_factory = app_client.__db_sessionmaker__
    first_db = session_factory()
    stale_db = session_factory()
    first_view = first_db.get(models.Session, session_id)
    stale_view = stale_db.get(models.Session, session_id)

    close_session(first_db, first_view, status="closed_error_safe")
    first_db.commit()
    close_session(stale_db, stale_view, status="closed_limit_reached")
    stale_db.commit()
    first_db.close()
    stale_db.close()

    db = session_factory()
    session = db.get(models.Session, session_id)
    assert session.status == "closed_error_safe"
    assert session.active_lock_token is None
    assert _counts(db, session_id) == (1, 1, 0)
    db.close()
