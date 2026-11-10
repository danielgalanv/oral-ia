"""T137: nullable turn output at the API and read-model boundaries."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from oralia.application.orchestration.self_study_agency_composer import StudyTurnResult
from oralia.application.orchestration.turn_orchestrator import TurnResult
from oralia.application.queries.get_session import get_session_detail
from oralia.application.services.technical_summary_service import generate_summary, get_summary
from oralia.domain.agents.fallback_agent import SAFE_FALLBACK_TEXT
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.t090_policy_helpers import minimal_output_policy_columns


def _persist_session(db, *, participant: str, status: str = "active") -> models.Session:
    course = models.Course(name="T090 API", subject_code=f"T090-{participant}")
    retention = models.RetentionPolicy(
        content_scope="session",
        access_scope="profesor",
        purge_rule="manual",
    )
    db.add_all([course, retention])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="T090 API activity",
        subject="T090",
        objective="verify nullable output",
        mode="texto",
        language="es",
        max_turns=10,
        max_duration_seconds=900,
        retention_policy_id=retention.id,
        **minimal_output_policy_columns(recipients=(participant,)),
    )
    db.add_all([activity, models.ParticipantCode(code=participant)])
    db.flush()
    session = models.Session(
        activity_configuration_id=activity.id,
        participant_code=participant,
        status=status,
        active_lock_token="ACTIVE" if status == "active" else None,
        ended_at=None if status == "active" else utcnow(),
    )
    db.add(session)
    db.flush()
    return session


def _persist_final_turn(
    db,
    session: models.Session,
    *,
    output_text: str | None,
    turn_status: str,
    verdict: str,
    reasons: list[str],
    attempt: int,
) -> models.Turn:
    turn = models.Turn(
        session_id=session.id,
        index=1,
        input_text="private participant input",
        output_text=output_text,
        status=turn_status,
        ended_at=utcnow(),
    )
    db.add(turn)
    db.flush()
    proposal_content = {
        "template_id": "safe-technical-fallback" if attempt else "sc007-acknowledgement",
        "template_version": 1,
        "message_type": "operational" if attempt else "normal",
        "attempt": attempt,
    }
    if output_text is not None:
        proposal_content["text"] = output_text
    proposal = models.GeneratedProposal(
        turn_id=turn.id,
        generator_agent_id="final-output-gate",
        content=proposal_content,
    )
    db.add(proposal)
    db.flush()
    verification = models.VerificationResult(
        proposal_id=proposal.id,
        verifier_agent_id="constitutional-control",
        verdict=verdict,
        reasons=reasons,
        authorization_context={
            "attempt": attempt,
            "message_type": "operational" if attempt else "normal",
        },
    )
    action = models.DialogueAction(
        turn_id=turn.id,
        action_type="finish" if output_text is None else "clarify",
        chosen_by_agent_id="final-output-gate",
    )
    db.add_all([verification, action])
    db.flush()
    turn.generated_proposal_id = proposal.id
    turn.verification_result_id = verification.id
    turn.dialogue_action_id = action.id
    session.turn_count = 1
    db.add_all([turn, session])
    db.flush()
    return turn


@pytest.mark.contract
def test_both_turn_endpoints_serialize_null_without_a_replacement(
    app_client, seeded_activity, monkeypatch: pytest.MonkeyPatch
) -> None:
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "participant", "activity_configuration_id": seeded_activity},
    )
    session_id = start.json()["session_id"]

    async def fake_turn(*_args, **_kwargs) -> TurnResult:
        return TurnResult("turn-null", "finish", None, True, 1, "blocked")

    async def fake_study(*_args, **_kwargs) -> StudyTurnResult:
        return StudyTurnResult(
            "study-null",
            "doubt_resolution",
            "finish",
            None,
            True,
            1,
            "blocked",
        )

    monkeypatch.setattr("oralia.interfaces.api.routers.participante.submit_turn", fake_turn)
    monkeypatch.setattr("oralia.interfaces.api.routers.self_study.submit_study_turn", fake_study)

    participant = app_client.post(f"/api/v1/sessions/{session_id}/turns", json={"text": "private"})
    study = app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "private"})

    assert participant.status_code == study.status_code == 200
    assert participant.json()["output_text"] is None
    assert study.json()["output_text"] is None
    assert participant.json()["blocked"] is True
    assert study.json()["blocked"] is True


@pytest.mark.contract
def test_both_turn_endpoints_expose_an_approved_operational_degradation(
    app_client, seeded_activity, monkeypatch: pytest.MonkeyPatch
) -> None:
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "participant", "activity_configuration_id": seeded_activity},
    ).json()["session_id"]

    async def fake_turn(*_args, **_kwargs) -> TurnResult:
        return TurnResult("turn-fallback", "clarify", SAFE_FALLBACK_TEXT, True, 1, "degraded")

    async def fake_study(*_args, **_kwargs) -> StudyTurnResult:
        return StudyTurnResult(
            "study-fallback",
            "doubt_resolution",
            "clarify",
            SAFE_FALLBACK_TEXT,
            True,
            1,
            "degraded",
        )

    monkeypatch.setattr("oralia.interfaces.api.routers.participante.submit_turn", fake_turn)
    monkeypatch.setattr("oralia.interfaces.api.routers.self_study.submit_study_turn", fake_study)

    responses = (
        app_client.post(f"/api/v1/sessions/{session_id}/turns", json={"text": "private"}),
        app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "private"}),
    )
    for response in responses:
        assert response.status_code == 200
        assert response.json()["output_text"] == SAFE_FALLBACK_TEXT
        assert response.json()["blocked"] is True


@pytest.mark.contract
def test_session_detail_preserves_null_and_summary_reports_blocked_incident(db_session) -> None:
    session = _persist_session(db_session, participant="participant-null")
    turn = _persist_final_turn(
        db_session,
        session,
        output_text=None,
        turn_status="blocked",
        verdict="block",
        reasons=["unsafe_fallback"],
        attempt=1,
    )
    session.status = "closed_error_safe"
    session.ended_at = utcnow()
    session.active_lock_token = None
    session.technical_summary_ref = generate_summary(db_session, session)
    db_session.flush()

    detail = get_session_detail(db_session, session.id)
    assert detail is not None
    assert detail["turns"][0]["output_text"] is None
    assert detail["turns"][0]["status"] == "blocked"
    assert detail["turns"][0]["verification_verdict"] == "block"
    assert detail["turns"][0]["dialogue_action"] == "finish"
    assert detail["technical_summary"]["incident_types"] == ["blocked"]
    assert turn.output_text is None


@pytest.mark.contract
def test_approved_operational_fallback_remains_degraded_in_detail_and_summary(db_session) -> None:
    session = _persist_session(db_session, participant="participant-fallback")
    turn = _persist_final_turn(
        db_session,
        session,
        output_text=SAFE_FALLBACK_TEXT,
        turn_status="degraded",
        verdict="approved",
        reasons=[],
        attempt=1,
    )
    initial = models.TraceEvent(
        session_id=session.id,
        turn_id=turn.id,
        event_type="output_authorization_attempt",
        agent_id="constitutional-control",
        payload={"attempt": 0, "verdict": "block", "reason_codes": ["invalid_context"]},
        memory_category="metacognitive",
    )
    db_session.add(initial)
    session.status = "closed_limit_reached"
    session.ended_at = utcnow()
    session.active_lock_token = None
    session.technical_summary_ref = generate_summary(db_session, session)
    db_session.flush()

    detail = get_session_detail(db_session, session.id)
    assert detail is not None
    # Administrative detail preserves verdict/status, but no content without consent.
    assert detail["turns"][0]["output_text"] is None
    assert detail["turns"][0]["status"] == "degraded"
    assert detail["turns"][0]["verification_verdict"] == "approved"
    assert get_summary(db_session, session.technical_summary_ref)["incident_types"] == ["degraded"]
    assert initial.payload["attempt"] == 0


@pytest.mark.contract
def test_repeated_voluntary_endpoints_preserve_closed_error_safe(app_client, seeded_activity) -> None:
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "participant", "activity_configuration_id": seeded_activity},
    ).json()["session_id"]
    Session = app_client.__db_sessionmaker__
    db = Session()
    session = db.get(models.Session, session_id)
    session.status = "closed_error_safe"
    session.ended_at = utcnow()
    session.active_lock_token = None
    session.technical_summary_ref = generate_summary(db, session)
    original_ref = session.technical_summary_ref
    db.commit()
    db.close()

    participant = app_client.post(f"/api/v1/sessions/{session_id}/end")
    study = app_client.post(f"/api/v1/sessions/{session_id}/study-end")
    assert participant.json()["status"] == "closed_error_safe"
    assert study.json()["status"] == "closed_error_safe"

    db = Session()
    persisted = db.get(models.Session, session_id)
    summaries = (
        db.query(models.TraceEvent)
        .filter(
            models.TraceEvent.session_id == session_id,
            models.TraceEvent.event_type == "technical_summary",
        )
        .all()
    )
    assert persisted.technical_summary_ref == original_ref
    assert len(summaries) == 1
    db.close()


@pytest.mark.contract
def test_get_db_owns_one_outer_commit_or_one_rollback(monkeypatch: pytest.MonkeyPatch) -> None:
    from oralia.interfaces.api.deps import db as db_dependency

    class FakeSession:
        commits = 0
        rollbacks = 0
        closes = 0

        def commit(self) -> None:
            self.commits += 1

        def rollback(self) -> None:
            self.rollbacks += 1

        def close(self) -> None:
            self.closes += 1

    normal = FakeSession()
    monkeypatch.setattr(db_dependency, "get_sessionmaker", lambda: lambda: normal)
    dependency: Iterator = db_dependency.get_db()
    assert next(dependency) is normal
    with pytest.raises(StopIteration):
        next(dependency)
    assert (normal.commits, normal.rollbacks, normal.closes) == (1, 0, 1)

    failing = FakeSession()
    monkeypatch.setattr(db_dependency, "get_sessionmaker", lambda: lambda: failing)
    dependency = db_dependency.get_db()
    assert next(dependency) is failing
    with pytest.raises(RuntimeError, match="boom"):
        dependency.throw(RuntimeError("boom"))
    assert (failing.commits, failing.rollbacks, failing.closes) == (0, 1, 1)
