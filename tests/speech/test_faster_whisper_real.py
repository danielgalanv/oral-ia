"""Optional local STT smoke; fixture is synthetic Windows speech, never participant audio."""

import os
from pathlib import Path

import pytest

from oralia.infrastructure.speech.faster_whisper_adapter import FasterWhisperTranscriptionAdapter

pytestmark = pytest.mark.speech


@pytest.mark.skipif(not os.getenv("ORALIA_STT_MODEL"), reason="ORALIA_STT_MODEL not configured")
async def test_local_whisper_transcribes_synthetic_fixture():
    pytest.importorskip("faster_whisper")
    audio = (Path(__file__).parents[1] / "fixtures" / "defense_voice.wav").read_bytes()
    result = await FasterWhisperTranscriptionAdapter().transcribe(audio, language="en")
    assert result.ok, result.error_code
    assert result.text.strip() and result.segments
    assert any(word in result.text.lower() for word in ("system", "generation", "verification"))
