"""Closing summaries obey the same trusted authorization boundary as turns."""

import pytest

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.infrastructure.db import models
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


@pytest.mark.parametrize(
    "text", ["Tu comprensión es insuficiente.", "Tu rendimiento es excelente.", "Tu nota es 8."]
)
def test_closing_summary_cannot_republish_personal_characterization(db_session, text):
    session_id, config_id = _seed_active_defense(db_session)
    db_session.query(models.Turn).one().output_text = text
    summary = end_defense_session(
        db_session,
        db_session.get(models.Session, session_id),
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=True,
        scope=["summary"],
    )
    assert summary is None
    assert db_session.query(models.TraceEvent).filter_by(event_type="defense_session_summary").count() == 0
    assert all(text not in str(row.content) for row in db_session.query(models.GeneratedProposal))


def test_summary_without_policy_is_not_published_or_retained(db_session):
    session_id, config_id = _seed_active_defense(db_session)
    session = db_session.get(models.Session, session_id)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    activity.output_authorization_policy_json = None
    activity.output_authorization_policy_sha256 = None
    summary = end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=True,
        scope=["summary"],
    )
    assert summary is None
    assert (
        db_session.query(models.TraceEvent)
        .filter_by(session_id=session_id, event_type="defense_session_summary")
        .count()
        == 0
    )
    assert session.status == "closed_voluntary"


def test_empty_session_summary_has_an_authorization_receipt_without_a_cognitive_turn(db_session):
    session_id, config_id = _seed_active_defense(db_session)
    db_session.query(models.TranscriptCorrection).delete()
    db_session.query(models.Transcript).delete()
    db_session.query(models.Turn).delete()
    session = db_session.get(models.Session, session_id)
    result = end_defense_session(
        db_session,
        session,
        db_session.get(models.DefenseActivityConfig, config_id),
        retain=True,
        scope=["summary"],
    )
    assert result["turn_count"] == session.turn_count == 0
    assert result["questions_asked"] == []
    receipt = db_session.query(models.Turn).filter_by(session_id=session_id, index=-1).one()
    proposal = db_session.query(models.GeneratedProposal).filter_by(turn_id=receipt.id).one()
    assert (
        db_session.query(models.VerificationResult).filter_by(proposal_id=proposal.id).one().verdict
        == "approved"
    )
