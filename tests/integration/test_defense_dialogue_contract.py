from datetime import timedelta

import pytest

from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.domain.agents.agent_contract import AgentResult
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.contract.test_defense_output_authorization_matrix import _CandidateAgent, _permit_template
from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense


def _events(db, session, name):
    return [
        row.payload for row in db.query(models.TraceEvent).filter_by(session_id=session.id, event_type=name)
    ]


async def test_repetition_has_only_one_regeneration_and_never_becomes_clarify(db_session):
    session = _seed_defense(db_session)
    question = "¿Cómo separa la arquitectura generación y verificación?"
    agent = _CandidateAgent(question)
    first = await run_defense_turn(
        db_session,
        session,
        "arquitectura generación verificación",
        followup_agent=agent,
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert first.dialogue_action == "ask"
    second = await run_defense_turn(
        db_session,
        session,
        "arquitectura generación verificación",
        followup_agent=agent,
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert second.dialogue_action == "acknowledge_missing_info"
    calls = _events(db_session, session, "generation_call")
    assert [row["attempt"] for row in calls if "attempt" in row] == [0, 0, 1]


async def test_cognitive_contradiction_clarifies_then_redecides(db_session):
    session = _seed_defense(db_session)
    agent = _CandidateAgent("¿Cómo separa la arquitectura generación y verificación?")
    await run_defense_turn(
        db_session,
        session,
        "La arquitectura separa generación y verificación.",
        followup_agent=agent,
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    result = await run_defense_turn(
        db_session, session, "La arquitectura no separa generación y verificación."
    )
    assert result.dialogue_action == "clarify"
    assert _events(db_session, session, "verification_combined")[-1]["reason"] == "cognitive_contradiction"
    clarified = await run_defense_turn(
        db_session,
        session,
        "La arquitectura separa generación y verificación.",
        followup_agent=agent,
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert clarified.dialogue_action != "clarify"


async def test_switch_topic_requires_authorized_target_and_trace(db_session):
    session = _seed_defense(db_session)
    before = db_session.query(models.Turn).count()
    with pytest.raises(ValueError, match="outside authorized scope"):
        await run_defense_turn(db_session, session, "arquitectura", requested_topic="inventado")
    assert db_session.query(models.Turn).count() == before
    result = await run_defense_turn(
        db_session,
        session,
        "arquitectura generación verificación",
        requested_topic="activity",
        followup_agent=_CandidateAgent("¿Cómo separa la arquitectura generación?"),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert result.dialogue_action == "ask" and result.dialogue_purpose == "switch_topic"
    event = _events(db_session, session, "followup_question_generated")[-1]
    assert event["target_concept"] == "activity"
    assert event["evidence_fragment_ids"] and event["reason"]


async def test_duration_limit_closes_with_authorized_text(db_session):
    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    _permit_template(activity, "defense-limit-close", "oral_defense_close", "finish")
    session.started_at = utcnow() - timedelta(seconds=activity.max_duration_seconds + 1)
    result = await run_defense_turn(db_session, session, "respuesta")
    assert result.dialogue_action == "finish"
    assert result.output_text
    assert session.status == "closed_limit_reached"
    assert _events(db_session, session, "turn_completed")


async def test_agent_trace_cannot_persist_rejected_free_text(db_session):
    session = _seed_defense(db_session)

    class Leaky(_CandidateAgent):
        async def execute(self, request, cancellation):
            result = await super().execute(request, cancellation)
            return AgentResult(status="ok", output=result.output, trace={"candidate": "nota: 8"})

    await run_defense_turn(
        db_session,
        session,
        "arquitectura generación verificación",
        followup_agent=Leaky("nota: 8"),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert "nota: 8" not in str([row.payload for row in db_session.query(models.TraceEvent)])
