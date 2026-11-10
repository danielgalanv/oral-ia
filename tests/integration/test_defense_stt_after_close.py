import pytest
from sqlalchemy.orm import Session

from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.commands.submit_defense_voice_turn import (
    TranscriptionUnavailable,
    submit_defense_voice_turn,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.speech.transcription_port import TranscriptionOutcome
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


async def test_stt_completing_after_close_cannot_recreate_deleted_transcription(db_session):
    session_id, config_id = _seed_active_defense(db_session)
    stale_session = db_session.get(models.Session, session_id)

    class CompletesAfterClose:
        async def transcribe(self, audio, *, language):
            with Session(db_session.get_bind(), expire_on_commit=False) as closer:
                end_defense_session(
                    closer,
                    closer.get(models.Session, session_id),
                    closer.get(models.DefenseActivityConfig, config_id),
                )
                closer.commit()
            return TranscriptionOutcome(ok=True, text="late private transcription")

    with pytest.raises(TranscriptionUnavailable, match="session_closed"):
        await submit_defense_voice_turn(
            db_session, stale_session, b"ephemeral", language="es", transcription_port=CompletesAfterClose()
        )
    assert db_session.query(models.Transcript).filter_by(session_id=session_id).count() == 0
