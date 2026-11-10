from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.infrastructure.db import models
from tests.contract.test_defense_output_authorization_matrix import _CandidateAgent
from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense


async def test_literal_duplicate_is_rejected_after_an_intervening_topic_switch(db_session):
    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    activity.max_turns = 10
    questions = [
        "¿Cómo separa la arquitectura generación y verificación?",
        "¿Qué decisión modular permite aislar responsabilidades?",
    ]
    for index, question in enumerate(questions):
        result = await run_defense_turn(
            db_session,
            session,
            "arquitectura generación verificación",
            followup_agent=_CandidateAgent(question),
            grounding_verifier_agent=_ApprovedGrounding(),
            requested_topic="activity" if index else None,
        )
        assert result.dialogue_action == "ask"
    repeated = await run_defense_turn(
        db_session,
        session,
        "arquitectura generación verificación",
        followup_agent=_CandidateAgent(questions[0]),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert repeated.dialogue_action == "acknowledge_missing_info"
    published = [turn.output_text for turn in db_session.query(models.Turn) if turn.output_text in questions]
    assert len(published) == len(set(published)) == 2


def test_defense_trace_cannot_aggregate_another_session_of_same_participant(app_client):
    with app_client.__db_sessionmaker__() as db:
        first = _seed_defense(db)
        second = models.Session(
            activity_configuration_id=first.activity_configuration_id,
            participant_code=first.participant_code,
            status="closed_voluntary",
        )
        db.add(second)
        db.flush()
        db.add(
            models.TraceEvent(
                session_id=second.id,
                event_type="isolated-marker",
                payload={"marker": "other-session-only"},
                memory_category="procedural",
            )
        )
        first_id, second_id, participant = first.id, second.id, first.participant_code
        db.commit()
    first_trace = app_client.get(
        f"/api/v1/tecnica/defense-sessions/{first_id}/defense-trace", params={"participant_code": participant}
    )
    second_trace = app_client.get(f"/api/v1/tecnica/defense-sessions/{second_id}/defense-trace")
    assert first_trace.status_code == second_trace.status_code == 200
    assert "other-session-only" not in first_trace.text
    assert "other-session-only" not in second_trace.text  # Raw marker is not technical metadata.
    assert any(event["event_type"] == "isolated-marker" for event in second_trace.json()["trace_events"])
    assert all(event["event_type"] != "isolated-marker" for event in first_trace.json()["trace_events"])
    assert (
        app_client.get(f"/api/v1/tecnica/defense-participants/{participant}/defense-trace").status_code == 404
    )
