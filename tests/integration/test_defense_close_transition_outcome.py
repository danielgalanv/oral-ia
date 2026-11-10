"""T113/T150: atomic ownership of oral-defense close side effects."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from oralia.application.commands import end_defense_session, end_session
from oralia.application.commands.end_defense_session import end_defense_session as close_defense
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.infrastructure.db import models


def _seed_active_defense(db: SASession, *, retention_days: int = 7):
    course = models.Course(name="Defensa", subject_code="DEF-T150")
    policy = models.RetentionPolicy(
        content_scope="session",
        retention_days=retention_days,
        access_scope="profesor",
        purge_rule="manual",
    )
    participant = models.ParticipantCode(code="defense-t150")
    db.add_all([course, policy, participant])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Defensa T150",
        subject="Arquitectura",
        objective="defender decisiones",
        mode="oral_defense",
        language="es",
        max_turns=5,
        max_duration_seconds=600,
        retention_policy_id=policy.id,
    )
    db.add(activity)
    db.flush()
    summary_policy = OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": "defense-close-test",
            "policy_version": 1,
            "allowed_recipients": [participant.code],
            "allowed_disclosures": [
                {
                    "category": "defense_summary",
                    "provenance": "persisted_session_facts",
                    "recipient": participant.code,
                }
            ],
            "allowed_scopes": {
                "topics": ["activity"],
                "purposes": ["oral_defense_summary"],
                "actions": ["respond"],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [["defense-summary", 1]],
            "allowed_operational_messages": [],
        }
    )
    activity.output_authorization_policy_json = canonical_policy_json(summary_policy)
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(
        activity.output_authorization_policy_json
    )
    config = models.DefenseActivityConfig(
        activity_configuration_id=activity.id,
        initial_questions=["Explica la decisión."],
        topics=["arquitectura"],
        summary_authorized=True,
        transcript_retention_authorized=True,
    )
    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant.code,
        status="active",
        active_lock_token="ACTIVE",
    )
    db.add_all([config, session])
    db.flush()
    turn = models.Turn(
        session_id=session.id,
        index=1,
        input_text="Una respuesta",
        output_text="¿Por qué?",
        status="completed",
    )
    db.add(turn)
    db.flush()
    transcript = models.Transcript(
        session_id=session.id,
        turn_id=turn.id,
        raw_text="Una respuesta",
        status="confirmed",
    )
    db.add(transcript)
    db.flush()
    db.add(
        models.TranscriptCorrection(
            transcript_id=transcript.id,
            session_id=session.id,
            corrected_text="Una respuesta corregida",
        )
    )
    db.commit()
    return session.id, config.id


def _count(db: SASession, model, **filters) -> int:
    return db.query(model).filter_by(**filters).count()


def test_sequential_duplicate_close_delivers_summary_and_retention_once(db_session) -> None:
    session_id, config_id = _seed_active_defense(db_session)
    session = db_session.get(models.Session, session_id)
    config = db_session.get(models.DefenseActivityConfig, config_id)

    first = close_defense(
        db_session,
        session,
        config,
        retain=True,
        scope=["transcript", "summary"],
    )
    second = close_defense(
        db_session,
        session,
        config,
        status="closed_limit_reached",
        retain=True,
        scope=["transcript", "summary"],
    )

    assert first is not None
    assert second is None
    assert session.status == "closed_voluntary"
    assert _count(db_session, models.ConsentRecord, session_id=session_id) == 1
    assert _count(db_session, models.TraceEvent, session_id=session_id, event_type="session_closed") == 1
    assert (
        _count(db_session, models.TraceEvent, session_id=session_id, event_type="defense_session_summary")
        == 1
    )
    assert _count(db_session, models.Transcript, session_id=session_id) == 1
    assert _count(db_session, models.TranscriptCorrection, session_id=session_id) == 1


def test_stale_competitor_cannot_repeat_any_close_side_effect(
    db_engine,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    seed_db = factory()
    session_id, config_id = _seed_active_defense(seed_db)
    seed_db.close()
    winner_db = factory()
    loser_db = factory()
    winner = winner_db.get(models.Session, session_id)
    loser = loser_db.get(models.Session, session_id)
    winner_config = winner_db.get(models.DefenseActivityConfig, config_id)
    loser_config = loser_db.get(models.DefenseActivityConfig, config_id)
    summary_calls = 0
    release_calls = 0
    real_summary = end_defense_session.generate_defense_summary
    real_release = end_session.session_lock_service.release

    def counted_summary(*args, **kwargs):
        nonlocal summary_calls
        summary_calls += 1
        return real_summary(*args, **kwargs)

    def counted_release(*args, **kwargs):
        nonlocal release_calls
        release_calls += 1
        return real_release(*args, **kwargs)

    monkeypatch.setattr(end_defense_session, "generate_defense_summary", counted_summary)
    monkeypatch.setattr(end_session.session_lock_service, "release", counted_release)
    try:
        assert (
            close_defense(
                winner_db,
                winner,
                winner_config,
                retain=True,
                scope=["transcript", "summary"],
            )
            is not None
        )
        winner_db.commit()
        assert (
            close_defense(
                loser_db,
                loser,
                loser_config,
                status="closed_error_safe",
                retain=True,
                scope=["transcript", "summary"],
            )
            is None
        )
        loser_db.commit()
    finally:
        winner_db.close()
        loser_db.close()
    assert summary_calls == 1
    assert release_calls == 1
    check = factory()
    assert check.get(models.Session, session_id).status == "closed_voluntary"
    assert _count(check, models.ConsentRecord, session_id=session_id) == 1
    assert _count(check, models.TraceEvent, session_id=session_id, event_type="session_closed") == 1
    check.close()


def test_outer_rollback_restores_claim_and_every_defense_side_effect(
    db_engine,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    db = factory()
    session_id, config_id = _seed_active_defense(db)
    session = db.get(models.Session, session_id)
    config = db.get(models.DefenseActivityConfig, config_id)
    real_summary: Callable = end_defense_session.generate_defense_summary

    def fail_after_summary(*args, **kwargs):
        real_summary(*args, **kwargs)
        raise RuntimeError("injected after defense summary")

    monkeypatch.setattr(end_defense_session, "generate_defense_summary", fail_after_summary)
    with pytest.raises(RuntimeError, match="injected after defense summary"):
        close_defense(db, session, config, retain=True, scope=["transcript", "summary"])
    db.rollback()
    db.close()

    check = factory()
    persisted = check.get(models.Session, session_id)
    assert persisted.status == "active"
    assert persisted.ended_at is None
    assert persisted.active_lock_token == "ACTIVE"
    assert persisted.technical_summary_ref is None
    assert _count(check, models.ConsentRecord, session_id=session_id) == 0
    assert _count(check, models.TraceEvent, session_id=session_id, event_type="session_closed") == 0
    assert _count(check, models.TraceEvent, session_id=session_id, event_type="defense_session_summary") == 0
    assert _count(check, models.Transcript, session_id=session_id) == 1
    assert _count(check, models.TranscriptCorrection, session_id=session_id) == 1
    check.close()
