from datetime import timedelta

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.commands.purge_expired_defense_data import purge_expired_defense_data
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


def _seed_copies(db):
    session_id, config_id = _seed_active_defense(db, retention_days=1)
    marker = "contenido-privado-de-defensa"
    turn = db.query(models.Turn).filter_by(session_id=session_id).one()
    turn.input_text = turn.output_text = marker
    db.add_all(
        [
            models.CognitiveState(
                session_id=session_id,
                current_input=marker,
                participant_response=marker,
                concepts_addressed=[marker],
            ),
            models.StatePatch(
                session_id=session_id,
                base_version=0,
                resulting_version=1,
                proposed_by_agent_id="defense-agency",
                payload={"current_input": marker},
                element_type="participant_statement",
                applied=True,
            ),
            models.GeneratedProposal(
                turn_id=turn.id,
                generator_agent_id="followup-question-agent",
                content={"text": marker, "template_id": "defense-dynamic-output"},
            ),
            models.InternalMessage(
                session_id=session_id,
                turn_id=turn.id,
                sender_agent_id="defense-agency",
                receiver_agent_id="followup-question-agent",
                type="observation",
                objective="defense",
                content={"text": marker},
            ),
            models.TraceEvent(
                session_id=session_id,
                event_type="followup_question_generated",
                payload={"referenced_concept": marker, "purpose": "deepen_current_topic"},
                memory_category="procedural",
            ),
        ]
    )
    db.flush()
    return session_id, config_id, marker


def _assert_erased(db, session_id, marker):
    assert db.get(models.CognitiveState, session_id) is None
    assert all(
        marker not in str(row.payload) for row in db.query(models.StatePatch).filter_by(session_id=session_id)
    )
    assert db.query(models.InternalMessage).filter_by(session_id=session_id).count() == 0
    assert all(
        marker not in str((row.input_text, row.output_text))
        for row in db.query(models.Turn).filter_by(session_id=session_id)
    )
    turn_ids = [row.id for row in db.query(models.Turn).filter_by(session_id=session_id)]
    assert all(
        marker not in str(row.content)
        for row in db.query(models.GeneratedProposal).filter(models.GeneratedProposal.turn_id.in_(turn_ids))
    )
    assert all(
        marker not in str(row.payload) for row in db.query(models.TraceEvent).filter_by(session_id=session_id)
    )


def test_delete_choice_erases_operational_copies_as_well_as_transcript_rows(db_session):
    session_id, config_id, marker = _seed_copies(db_session)
    session = db_session.get(models.Session, session_id)
    other = models.Session(
        activity_configuration_id=session.activity_configuration_id,
        participant_code=session.participant_code,
        status="closed_voluntary",
    )
    db_session.add(other)
    db_session.flush()
    db_session.add(models.CognitiveState(session_id=other.id, current_input="another session survives"))
    db_session.flush()
    end_defense_session(
        db_session,
        db_session.get(models.Session, session_id),
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=False,
    )
    _assert_erased(db_session, session_id, marker)
    assert db_session.get(models.CognitiveState, other.id).current_input == "another session survives"


def test_expiry_erases_retained_copies_and_second_purge_is_idempotent(db_session):
    session_id, config_id, marker = _seed_copies(db_session)
    session = db_session.get(models.Session, session_id)
    end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=True,
        scope=["transcript", "summary"],
    )
    assert marker in db_session.get(models.CognitiveState, session_id).current_input
    session.ended_at = utcnow() - timedelta(days=2)
    first = purge_expired_defense_data(db_session)
    _assert_erased(db_session, session_id, marker)
    assert first.sessions_with_rows_deleted == 1
    assert purge_expired_defense_data(db_session).sessions_with_rows_deleted == 0
