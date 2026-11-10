import asyncio
import io
import os
import tempfile
import wave

import pytest
from fastapi import HTTPException
from starlette.datastructures import Headers, UploadFile

from oralia.infrastructure.db import models
from tests.contract.test_defense_voice_and_speech import _STT, _wav
from tests.contract.test_defense_voice_upload_limits import _long_wav
from tests.integration.test_defense_text_turn import _seed_defense


@pytest.mark.parametrize(
    ("kind", "status"),
    [
        ("success", 200),
        ("exact_limit", 200),
        ("oversize", 413),
        ("duration", 422),
        ("malformed", 422),
        ("unknown", 422),
        ("timeout", 503),
        ("disabled", 409),
        ("missing", 404),
    ],
)
async def test_rolled_multipart_is_closed_on_every_exit(db_session, monkeypatch, kind, status):
    from oralia.interfaces.api.routers import oral_defense

    session = _seed_defense(db_session)
    config = db_session.query(models.DefenseActivityConfig).one()
    config.voice_input_allowed = kind != "disabled"
    payload = _wav()
    if kind == "exact_limit":
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(1)
            audio.setframerate(48000)
            audio.writeframes(b"\0" * (10 * 1024 * 1024 - 44))
        payload = buffer.getvalue()
        assert len(payload) == 10 * 1024 * 1024
    elif kind == "oversize":
        payload = b"x" * (10 * 1024 * 1024 + 1)
    elif kind == "duration":
        payload = _long_wav()
    elif kind == "malformed":
        payload = b"broken"
    spool = tempfile.SpooledTemporaryFile(max_size=1)
    spool.write(payload)
    spool.seek(0)
    descriptor = spool.fileno()
    assert spool._rolled
    upload = UploadFile(
        file=spool,
        filename="answer.wav",
        headers=Headers(
            {
                "content-type": "application/octet-stream" if kind == "unknown" else "audio/wav",
            }
        ),
    )
    _STT.calls = 0
    monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", _STT)
    if kind == "timeout":

        class Hanging:
            async def transcribe(self, audio, *, language):
                await asyncio.Event().wait()

        monkeypatch.setenv("ORALIA_STT_TIMEOUT_MS", "5")
        monkeypatch.setattr(oral_defense, "_transcription_adapter_factory", Hanging)
    try:
        result = await oral_defense.post_defense_voice_turn(
            "missing" if kind == "missing" else session.id,
            upload,
            db_session,
        )
        assert getattr(result, "status_code", 200) == status
    except HTTPException as error:
        assert error.status_code == status
    assert spool.closed
    with pytest.raises(OSError):
        os.fstat(descriptor)
    assert _STT.calls == int(kind in {"success", "exact_limit"})
    assert db_session.query(models.Transcript).count() == int(kind in {"success", "exact_limit"})
