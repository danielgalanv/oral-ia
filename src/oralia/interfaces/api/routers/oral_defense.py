"""HTTP boundary for Feature 004 oral-defense sessions."""

import asyncio
import hashlib
import io
import wave
from contextlib import closing
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from sqlalchemy.orm import Session as SASession

from oralia.application.commands.configure_defense_activity import (
    ActivityConfigurationImmutable,
    ActivityNotFound,
    DefenseActivityConfigInput,
    MissingQuestionSource,
    configure_defense_activity,
    get_defense_config,
)
from oralia.application.commands.confirm_defense_transcript import (
    TranscriptNotConfirmable,
    confirm_defense_transcript,
)
from oralia.application.commands.end_defense_session import end_defense_session
from oralia.application.commands.purge_expired_defense_data import purge_expired_defense_data
from oralia.application.commands.submit_defense_turn import (
    SessionNotActive,
    submit_defense_turn,
)
from oralia.application.commands.submit_defense_voice_turn import (
    TranscriptionUnavailable,
    submit_defense_voice_turn,
)
from oralia.application.orchestration.self_study_agency_composer import ModeNotEnabled
from oralia.application.queries.reconstruct_session_trace import reconstruct_session_trace
from oralia.application.services.trace_service import record_event
from oralia.application.services.turn_request_service import begin_request, complete_request
from oralia.domain.dialogue.contracts import DialogueControl
from oralia.infrastructure.db import models
from oralia.infrastructure.speech.config import MAX_AUDIO_BYTES, MAX_AUDIO_DURATION_SECONDS, settings
from oralia.infrastructure.speech.faster_whisper_adapter import FasterWhisperTranscriptionAdapter
from oralia.infrastructure.speech.piper_adapter import PiperSpeechSynthesisAdapter
from oralia.infrastructure.speech.synthesis_port import SynthesisOutcome
from oralia.interfaces.api.deps.auth_stub import tecnica_access_control
from oralia.interfaces.api.deps.db import get_db
from oralia.interfaces.api.deps.interactive_operation import interactive_operation

router = APIRouter(prefix="/api/v1", tags=["oral-defense"])
tecnica_router = APIRouter(
    prefix="/api/v1/tecnica",
    tags=["oral-defense-tecnica"],
    dependencies=[Depends(tecnica_access_control)],
)

_transcription_adapter_factory = FasterWhisperTranscriptionAdapter
_synthesis_adapter_factory = PiperSpeechSynthesisAdapter


def _get_defense_session(db: SASession, session_id: str) -> models.Session | None:
    session = db.get(models.Session, session_id)
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id) if session else None
    return session if activity is not None and activity.mode == "oral_defense" else None


class EndDefenseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    retain: StrictBool = False
    scope: list[str] = Field(default_factory=list)


class DefenseTurnInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    requested_topic: str | None = None
    closure_consent: EndDefenseInput = Field(default_factory=EndDefenseInput)
    client_request_id: UUID | None = None
    dialogue_control: DialogueControl | None = None


class DefenseSpeechOutput(BaseModel):
    available: Literal[True]
    url: str
    media_type: Literal["audio/wav"]
    text_sha256: str


class DefenseTurnOutput(BaseModel):
    turn_id: str
    dialogue_action: Literal["ask", "clarify", "acknowledge_missing_info", "finish"]
    dialogue_purpose: Literal["deepen_current_topic", "switch_topic"] | None
    output_text: str | None
    state_version: int | None
    sources: list[dict]
    general_knowledge_used: bool
    blocked: bool
    speech: DefenseSpeechOutput | None
    defense_summary: dict | None
    session_status: str
    dialogue_status: dict | None = None
    request_replayed: bool = False
    replay_content_withheld: bool = False


class ConfirmTranscriptInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    closure_consent: EndDefenseInput = Field(default_factory=EndDefenseInput)
    transcript_id: str
    corrected_text: str | None = None


@router.get("/defense-sessions/{session_id}/settings")
def get_defense_session_settings(session_id: str, db: SASession = Depends(get_db, scope="function")):
    session = _get_defense_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    config = get_defense_config(db, session.activity_configuration_id)
    if config is None:
        raise HTTPException(status_code=404, detail="defense configuration not found")
    response = {
        name: getattr(config, name)
        for name in (
            "voice_input_allowed",
            "voice_output_allowed",
            "transcript_retention_authorized",
        )
    }
    from oralia.application.services.session_privacy_service import privacy_view

    response["allowed_retention_scopes"] = privacy_view(db, session)["allowed_scopes"]
    response["low_confidence_threshold"] = settings().low_confidence_threshold
    return response


def _turn_response(
    db: SASession,
    session: models.Session,
    result,
) -> dict[str, object]:
    config = get_defense_config(db, session.activity_configuration_id)
    speech = None
    persisted_turn = db.get(models.Turn, result.turn_id)
    if (
        result.output_text is not None
        and persisted_turn is not None
        and persisted_turn.output_text == result.output_text
        and config is not None
        and config.voice_output_allowed
    ):
        speech = {
            "available": True,
            "url": (f"/api/v1/defense-sessions/{session.id}/" f"defense-turns/{result.turn_id}/speech"),
            "media_type": "audio/wav",
            "text_sha256": hashlib.sha256(result.output_text.encode("utf-8")).hexdigest(),
        }
    from oralia.application.services.guided_dialogue_service import legacy_turn_capabilities

    return {
        "turn_id": result.turn_id,
        "dialogue_action": result.dialogue_action,
        "dialogue_purpose": result.dialogue_purpose,
        "output_text": result.output_text,
        "state_version": result.state_version,
        "sources": result.sources,
        "general_knowledge_used": result.general_knowledge_used,
        "blocked": result.blocked,
        "speech": speech,
        "defense_summary": result.defense_summary,
        "session_status": result.session_status,
        "dialogue_status": result.dialogue_status
        or legacy_turn_capabilities(db, session, result.turn_id, blocked=result.blocked),
    }


@router.post("/defense-sessions/{session_id}/defense-turns", response_model=DefenseTurnOutput)
async def post_defense_turn(
    session_id: str,
    data: DefenseTurnInput,
    _operation=Depends(interactive_operation, scope="function"),
    db: SASession = Depends(get_db, scope="function"),
):
    session = _get_defense_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    try:
        if data.dialogue_control is not None and (data.text.strip() or data.requested_topic is not None):
            raise ValueError("Envía una sola orden: texto, tema o control estructurado.")
        receipt, replay = begin_request(
            db, session, data.client_request_id, data.model_dump(mode="json", exclude={"client_request_id"})
        )
        if replay is not None:
            return replay
        if "closure_consent" in data.model_fields_set:
            from oralia.application.services.screenless_navigation_service import screenless_enabled
            from oralia.application.services.session_privacy_service import set_privacy_preference

            activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
            if screenless_enabled(activity, session.participant_code):
                set_privacy_preference(db, session, **data.closure_consent.model_dump())
        result = await submit_defense_turn(
            db,
            session,
            data.text,
            requested_topic=data.requested_topic,
            closure_retain=data.closure_consent.retain,
            closure_scope=data.closure_consent.scope,
            **({"dialogue_control": data.dialogue_control} if data.dialogue_control is not None else {}),
        )
        complete_request(db, receipt, result.turn_id)
    except SessionNotActive as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ModeNotEnabled as exc:
        raise HTTPException(
            409,
            detail={
                "code": "mode_not_enabled",
                "message": (
                    "Ese modo no está habilitado en una defensa. Continúa con la " "pregunta o pide ayuda."
                ),
                "requested_mode": exc.requested_mode,
                "enabled_modes": [],
            },
        ) from None
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _turn_response(db, session, result)


def _audio_duration(audio: bytes, content_type: str) -> float:
    if content_type == "audio/webm":
        try:
            import av

            with closing(av.open(io.BytesIO(audio), mode="r")) as container:
                if container.duration is None:
                    raise ValueError("audio duration cannot be determined")
                return float(container.duration) / 1_000_000
        except (ImportError, OSError, ValueError) as exc:
            raise ValueError("audio duration cannot be determined") from exc
    if content_type != "audio/wav":
        raise ValueError("unsupported or unverifiable audio format")
    try:
        with wave.open(io.BytesIO(audio), "rb") as wav_file:
            rate = wav_file.getframerate()
            if rate <= 0:
                raise ValueError("invalid WAV sample rate")
            return wav_file.getnframes() / rate
    except (EOFError, wave.Error) as exc:
        raise ValueError("audio duration cannot be determined") from exc


async def _read_bounded(upload: UploadFile) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while chunk := await upload.read(64 * 1024):
        total += len(chunk)
        if total > MAX_AUDIO_BYTES:
            raise HTTPException(status_code=413, detail="audio exceeds 10 MiB")
        chunks.append(chunk)
    return b"".join(chunks)


@router.post("/defense-sessions/{session_id}/defense-turns/voice")
async def post_defense_voice_turn(
    session_id: str,
    audio: UploadFile = File(...),
    db: SASession = Depends(get_db, scope="function"),
):
    try:
        session = _get_defense_session(db, session_id)
        if session is None or session.status != "active":
            raise HTTPException(status_code=404, detail="active session not found")
        config = get_defense_config(db, session.activity_configuration_id)
        if config is None or not config.voice_input_allowed:
            raise HTTPException(status_code=409, detail="voice input is not enabled")
        if audio.content_type not in {"audio/wav", "audio/webm"}:
            raise HTTPException(status_code=422, detail="unsupported or unverifiable audio format")
        content = await _read_bounded(audio)
        try:
            duration = _audio_duration(content, audio.content_type)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if duration > MAX_AUDIO_DURATION_SECONDS:
            raise HTTPException(status_code=422, detail="audio exceeds 300 seconds")
        activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
        try:
            transcript = await submit_defense_voice_turn(
                db,
                session,
                content,
                language=activity.language,
                transcription_port=_transcription_adapter_factory(),
            )
        except TranscriptionUnavailable:
            return JSONResponse(
                status_code=503,
                content={"detail": {"code": "transcription_unavailable", "fallback_to_text": True}},
            )
        return {
            "transcript_id": transcript.id,
            "raw_text": transcript.raw_text,
            "segments": transcript.segments,
            "overall_confidence": transcript.overall_confidence,
            "low_confidence": transcript.low_confidence,
        }
    finally:
        await audio.close()


@router.post("/defense-sessions/{session_id}/defense-turns/voice/confirm", response_model=DefenseTurnOutput)
async def post_confirm_defense_transcript(
    session_id: str,
    data: ConfirmTranscriptInput,
    _operation=Depends(interactive_operation, scope="function"),
    db: SASession = Depends(get_db, scope="function"),
):
    session = _get_defense_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    try:
        result = await confirm_defense_transcript(
            db,
            session,
            data.transcript_id,
            data.corrected_text,
            closure_retain=data.closure_consent.retain,
            closure_scope=data.closure_consent.scope,
        )
    except (TranscriptNotConfirmable, SessionNotActive, ValueError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _turn_response(db, session, result)


@router.post("/defense-sessions/{session_id}/defense-turns/{turn_id}/speech")
async def post_defense_speech(
    session_id: str,
    turn_id: str,
    db: SASession = Depends(get_db, scope="function"),
):
    session = _get_defense_session(db, session_id)
    from oralia.application.services.session_privacy_service import valid_retained_scope

    if (
        session is not None
        and session.status != "active"
        and "transcript" not in valid_retained_scope(db, session)
    ):
        raise HTTPException(status_code=404, detail="approved speech not available")
    turn = db.get(models.Turn, turn_id)
    if session is None or turn is None or turn.session_id != session.id or turn.output_text is None:
        raise HTTPException(status_code=404, detail="approved turn output not found")
    config = get_defense_config(db, session.activity_configuration_id)
    if config is None or not config.voice_output_allowed:
        raise HTTPException(status_code=409, detail="voice output is not enabled")
    verification = db.get(models.VerificationResult, turn.verification_result_id)
    if verification is None or verification.verdict != "approved":
        raise HTTPException(status_code=404, detail="approved turn output not found")
    proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
    if (
        proposal is None
        or verification.proposal_id != proposal.id
        or proposal.turn_id != turn.id
        or proposal.content.get("text") != turn.output_text
        or turn.status not in {"completed", "degraded"}
    ):
        raise HTTPException(status_code=404, detail="approved turn output not found")
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    approved_text = turn.output_text
    try:
        outcome = await asyncio.wait_for(
            _synthesis_adapter_factory().synthesize(approved_text, language=activity.language),
            timeout=settings().tts_timeout_ms / 1000,
        )
    except Exception:
        outcome = SynthesisOutcome(ok=False, error_code="synthesis_failed")
    db.refresh(turn)
    if (
        turn.output_text != approved_text
        or turn.generated_proposal_id != proposal.id
        or turn.verification_result_id != verification.id
    ):
        raise HTTPException(status_code=404, detail="approved turn output no longer available")
    if not outcome.ok or outcome.audio is None:
        record_event(
            db,
            session_id=session.id,
            turn_id=turn.id,
            event_type="tts_failed",
            payload={"reason": outcome.error_code or "unknown"},
            memory_category="metacognitive",
        )
        return JSONResponse(status_code=503, content={"detail": "speech synthesis unavailable"})
    digest = hashlib.sha256(approved_text.encode("utf-8")).hexdigest()
    return Response(
        content=outcome.audio,
        media_type="audio/wav",
        headers={"X-ORALIA-Text-SHA256": digest, "Cache-Control": "no-store"},
    )


@router.post("/defense-sessions/{session_id}/defense-end")
def post_defense_end(
    session_id: str,
    data: EndDefenseInput | None = None,
    _operation=Depends(interactive_operation, scope="function"),
    db: SASession = Depends(get_db, scope="function"),
):
    session = _get_defense_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    config = get_defense_config(db, session.activity_configuration_id)
    request = data or EndDefenseInput()
    try:
        summary = end_defense_session(
            db,
            session,
            config,
            retain=request.retain,
            scope=request.scope,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"session_id": session.id, "status": session.status, "defense_summary": summary}


@tecnica_router.get("/defense-sessions/{session_id}/defense-trace")
def get_defense_trace(session_id: str, db: SASession = Depends(get_db, scope="function")):
    if _get_defense_session(db, session_id) is None:
        raise HTTPException(status_code=404, detail="defense session not found")
    return reconstruct_session_trace(db, session_id)


@tecnica_router.post("/defense/purge-expired")
def post_purge_expired_defense(db: SASession = Depends(get_db, scope="function")):
    result = purge_expired_defense_data(db)
    return {
        "sessions_matching_criteria": result.sessions_matching_criteria,
        "sessions_with_rows_deleted": result.sessions_with_rows_deleted,
        "transcripts_deleted": result.transcripts_deleted,
        "transcript_corrections_deleted": result.transcript_corrections_deleted,
        "trace_events_deleted": result.trace_events_deleted,
    }


@tecnica_router.post("/activities/{activity_id}/defense-config")
def post_defense_config(
    activity_id: str,
    data: DefenseActivityConfigInput,
    db: SASession = Depends(get_db, scope="function"),
):
    existed = get_defense_config(db, activity_id) is not None
    try:
        config = configure_defense_activity(db, activity_id, data)
    except ActivityNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ActivityConfigurationImmutable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (MissingQuestionSource, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return JSONResponse(
        status_code=200 if existed else 201,
        content={
            "id": config.id,
            "activity_configuration_id": config.activity_configuration_id,
            "initial_questions": config.initial_questions,
            "topics": config.topics,
            "difficulty_hint": config.difficulty_hint,
            "voice_input_allowed": config.voice_input_allowed,
            "voice_output_allowed": config.voice_output_allowed,
            "summary_authorized": config.summary_authorized,
            "transcript_retention_authorized": config.transcript_retention_authorized,
        },
    )


__all__ = ["router", "tecnica_router"]


@router.get("/defense-sessions/{session_id}/defense-transcript")
def get_defense_transcript(
    session_id: str, response: Response, db: SASession = Depends(get_db, scope="function")
):
    from oralia.application.services.session_privacy_service import own_transcript

    session = _get_defense_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    response.headers["Cache-Control"] = "no-store"
    return own_transcript(db, session)
