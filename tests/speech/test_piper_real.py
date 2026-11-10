"""Optional local Piper contract, separate from deterministic validation."""

import io
import os
import wave

import pytest

from oralia.infrastructure.speech.piper_adapter import PiperSpeechSynthesisAdapter

pytestmark = pytest.mark.speech


@pytest.mark.skipif(not os.getenv("ORALIA_TTS_VOICE"), reason="ORALIA_TTS_VOICE not configured")
async def test_local_piper_produces_readable_wav():
    pytest.importorskip("piper")
    result = await PiperSpeechSynthesisAdapter().synthesize(
        "Explica la separación entre generación y verificación.", language="es"
    )
    assert result.ok, result.error_code
    with wave.open(io.BytesIO(result.audio), "rb") as audio:
        assert audio.getnframes() > 0 and audio.getframerate() > 0
