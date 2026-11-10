import pytest

from oralia.application.commands.confirm_defense_transcript import (
    TranscriptNotConfirmable,
    confirm_defense_transcript,
)
from oralia.application.commands.submit_defense_voice_turn import submit_defense_voice_turn
from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.infrastructure.db import models
from oralia.infrastructure.speech.transcription_port import TranscriptionOutcome, TranscriptionSegment
from tests.integration.test_defense_text_turn import _seed_defense

ANSWER = "La arquitectura separa generación y verificación."


class LowConfidenceSTT:
    async def transcribe(self, audio, *, language):
        return TranscriptionOutcome(
            ok=True,
            text=ANSWER,
            segments=(TranscriptionSegment(text=ANSWER, confidence=0.1),),
            overall_confidence=0.1,
            low_confidence=True,
        )


async def test_provisional_low_confidence_is_only_a_modality_incident(db_session):
    session = _seed_defense(db_session)
    transcript = await submit_defense_voice_turn(
        db_session, session, b"ephemeral", language="es", transcription_port=LowConfidenceSTT()
    )
    assert transcript.status == "awaiting_confirmation" and transcript.low_confidence
    assert session.turn_count == 0
    assert db_session.query(models.Turn).count() == 0
    assert db_session.query(models.CognitiveState).count() == 0
    assert db_session.query(models.TraceEvent).filter_by(event_type="agent_execution").count() == 0
    assert "ephemeral" not in str([event.payload for event in db_session.query(models.TraceEvent)])


@pytest.mark.parametrize("corrected", [None, "La arquitectura separa generación y verificación modular."])
async def test_confirmation_preserves_original_and_uses_only_definitive_text(db_session, corrected):
    session = _seed_defense(db_session)
    transcript = await submit_defense_voice_turn(
        db_session, session, b"ephemeral", language="es", transcription_port=LowConfidenceSTT()
    )
    result = await confirm_defense_transcript(db_session, session, transcript.id, corrected)
    turn = db_session.get(models.Turn, result.turn_id)
    assert turn.input_text == (corrected or ANSWER)
    assert transcript.raw_text == ANSWER
    assert db_session.query(models.TranscriptCorrection).count() == int(corrected is not None)
    assert result.dialogue_action == "ask"  # Low STT confidence cannot trigger cognitive clarify.
    state = db_session.get(models.CognitiveState, session.id)
    assert state.current_input == (corrected or ANSWER)
    assert state.participant_response == result.output_text
    assert state.confidence == 1.0  # Existing cognitive confidence never takes the STT value 0.1.
    old_output = turn.output_text
    old_state_version = state.version
    with pytest.raises(TranscriptNotConfirmable):
        await confirm_defense_transcript(db_session, session, transcript.id, None)
    assert turn.output_text == old_output and state.version == old_state_version


@pytest.mark.parametrize("voice", [False, True])
async def test_definitive_text_and_voice_use_equivalent_cognitive_decisions(db_session, voice):
    session = _seed_defense(db_session)
    if voice:
        transcript = await submit_defense_voice_turn(
            db_session, session, b"ephemeral", language="es", transcription_port=LowConfidenceSTT()
        )
        result = await confirm_defense_transcript(db_session, session, transcript.id, None)
    else:
        result = await run_defense_turn(db_session, session, ANSWER)
    assert result.dialogue_action == "ask"
    assert result.dialogue_purpose == "deepen_current_topic"
    event = db_session.query(models.TraceEvent).filter_by(event_type="followup_question_generated").one()
    assert event.payload["referenced_concept"] == "arquitectura"
    assert db_session.get(models.CognitiveState, session.id).current_input == ANSWER
