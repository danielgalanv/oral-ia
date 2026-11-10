from oralia.application.commands.confirm_defense_transcript import confirm_defense_transcript
from oralia.application.commands.submit_defense_voice_turn import submit_defense_voice_turn
from oralia.infrastructure.db import models
from tests.integration.test_defense_text_turn import _seed_defense
from tests.integration.test_defense_voice_lifecycle import LowConfidenceSTT


async def test_post_confirmation_revision_is_a_new_turn_and_preserves_previous_artifacts(db_session):
    session = _seed_defense(db_session)
    original = await submit_defense_voice_turn(
        db_session, session, b"discard", language="es", transcription_port=LowConfidenceSTT()
    )
    first = await confirm_defense_transcript(db_session, session, original.id, None)
    old_turn = db_session.get(models.Turn, first.turn_id)
    old_output = old_turn.output_text
    old_input = old_turn.input_text
    correction = "La arquitectura modular separa responsabilidades."
    second = await confirm_defense_transcript(db_session, session, original.id, correction)
    assert second.turn_id != first.turn_id
    assert old_turn.output_text == old_output and old_turn.input_text == old_input
    assert original.status == "confirmed"
    assert db_session.query(models.TranscriptCorrection).filter_by(transcript_id=original.id).count() == 0
    revised_turn = db_session.get(models.Turn, second.turn_id)
    assert revised_turn.input_text == correction
    assert db_session.get(models.CognitiveState, session.id).current_input == correction
