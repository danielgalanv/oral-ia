import json

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.commands.submit_defense_voice_turn import submit_defense_voice_turn
from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.application.services.defense_session_summary_service import generate_defense_summary
from oralia.infrastructure.db import models
from tests.access_helpers import own_session
from tests.contract.test_defense_output_authorization_matrix import _CandidateAgent, _permit_template
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense
from tests.integration.test_defense_text_turn import _seed_defense
from tests.integration.test_defense_voice_lifecycle import LowConfidenceSTT


async def test_abandoning_low_confidence_voice_does_not_require_another_recording(db_session):
    session = _seed_defense(db_session)
    transcript = await submit_defense_voice_turn(
        db_session, session, b"unused", language="es", transcription_port=LowConfidenceSTT()
    )
    result = await run_defense_turn(db_session, session, "arquitectura")
    assert result.dialogue_action == "ask"
    assert transcript.status == "awaiting_confirmation"
    assert db_session.query(models.Transcript).count() == 1


async def test_short_text_does_not_create_stt_confirmation(db_session):
    session = _seed_defense(db_session)
    result = await run_defense_turn(db_session, session, "arquitectura")
    assert result.dialogue_action == "ask"
    assert db_session.query(models.Transcript).count() == 0


async def test_low_confidence_and_cognitive_empty_text_are_distinct(db_session):
    session = _seed_defense(db_session)
    await submit_defense_voice_turn(
        db_session, session, b"unused", language="es", transcription_port=LowConfidenceSTT()
    )
    assert db_session.query(models.DialogueAction).count() == 0
    session.turn_count = 1
    result = await run_defense_turn(db_session, session, "   ")
    assert result.dialogue_action == "clarify"


async def test_unsupported_reference_never_becomes_visible_followup(db_session):
    session = _seed_defense(db_session)
    agent = _CandidateAgent("¿Cómo explicas un tema inventado?")
    result = await run_defense_turn(db_session, session, "arquitectura", followup_agent=agent)
    assert result.dialogue_action == "acknowledge_missing_info"
    assert "tema inventado" not in result.output_text


def test_summary_is_reproducible_and_limited_to_observable_fields(db_session):
    session_id, config_id = _seed_active_defense(db_session)
    session = db_session.get(models.Session, session_id)
    config = db_session.get(models.DefenseActivityConfig, config_id)
    # Reconstruction requires retained source facts; summary-only consent erases them.
    first = end_defense_session(db_session, session, config, retain=True, scope=["transcript", "summary"])
    second = generate_defense_summary(db_session, session)
    assert first == second
    assert set(first) == {
        "turn_count",
        "duration_seconds",
        "questions_asked",
        "topics_covered",
        "concepts_mentioned",
        "sources_consulted_fragment_ids",
        "clarifications_count",
        "incidents",
        "close_reason",
    }
    assert not any(
        word in json.dumps(first).lower() for word in ("grade", "score", "competence", "performance")
    )


def test_topic_outside_scope_is_http_409_and_does_not_write_a_turn(app_client):
    with app_client.__db_sessionmaker__() as db:
        session = _seed_defense(db)
        session_id = session.id
        db.commit()
    own_session(app_client, session_id)
    result = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns",
        json={"text": "arquitectura", "requested_topic": "outside"},
    )
    assert result.status_code == 409
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.Turn).count() == 0


def test_purge_endpoint_has_current_counter_contract(app_client):
    result = app_client.post("/api/v1/tecnica/defense/purge-expired")
    assert result.status_code == 200
    assert result.json() == {
        "sessions_matching_criteria": 0,
        "sessions_with_rows_deleted": 0,
        "transcripts_deleted": 0,
        "transcript_corrections_deleted": 0,
        "trace_events_deleted": 0,
    }


async def test_reaching_turn_limit_closes_on_boundary_not_next_request(db_session):
    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    _permit_template(activity, "defense-limit-close", "oral_defense_close", "finish")
    session.turn_count = activity.max_turns - 1
    result = await run_defense_turn(db_session, session, "arquitectura")
    assert result.dialogue_action == "finish"
    assert result.session_status == "closed_limit_reached"
    assert session.turn_count == activity.max_turns
