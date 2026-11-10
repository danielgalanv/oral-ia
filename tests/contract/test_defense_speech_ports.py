import io
import wave

from tests.fixtures.speech_adapters import FakeSpeechSynthesisAdapter, FakeTranscriptionAdapter


async def test_transcription_double_obeys_segment_and_confidence_contract():
    adapter = FakeTranscriptionAdapter()
    result = await adapter.transcribe(b"ephemeral fixture", language="es")
    assert result.ok and result.text and adapter.calls == 1
    assert result.segments[0].start_ms == 0
    assert result.segments[0].end_ms > 0
    assert 0 <= result.segments[0].confidence <= 1
    assert 0 <= result.overall_confidence <= 1
    assert not hasattr(adapter, "execute")


async def test_synthesis_double_obeys_literal_input_and_wav_contract():
    adapter = FakeSpeechSynthesisAdapter()
    text = "¿Cómo justificas la separación?"
    result = await adapter.synthesize(text, language="es")
    assert result.ok and adapter.calls == [text]
    with wave.open(io.BytesIO(result.audio), "rb") as audio:
        assert audio.getnframes() > 0
    assert not hasattr(adapter, "execute")
