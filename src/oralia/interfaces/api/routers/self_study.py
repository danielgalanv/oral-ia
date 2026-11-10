"""Agencia de autoestudio — contracts/api-self-study.md (Feature 003).

Ningún endpoint de las Features 001/002 se modifica (FR-025) — este router es nuevo,
registrado por separado en `app.py`.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session as SASession

from oralia.application.commands.configure_self_study_activity import (
    ActivityConfigurationImmutable,
    ActivityNotFound,
    SelfStudyActivityConfigInput,
    configure_self_study_activity,
    get_self_study_config,
)
from oralia.application.commands.end_study_session import end_study_session
from oralia.application.commands.purge_expired_self_study_data import purge_expired_self_study_data
from oralia.application.commands.submit_study_turn import SessionNotActive, submit_study_turn
from oralia.application.orchestration.self_study_agency_composer import ModeNotEnabled
from oralia.application.queries.reconstruct_session_trace import reconstruct_session_trace
from oralia.application.queries.self_study_retention_audit import self_study_retention_audit
from oralia.application.services.session_privacy_service import (
    PrivacyChoice,
    set_privacy_preference,
    validate_privacy_choice,
)
from oralia.application.services.turn_request_service import begin_request, complete_request
from oralia.domain.dialogue.contracts import DialogueControl
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.auth_stub import tecnica_access_control
from oralia.interfaces.api.deps.db import get_db
from oralia.interfaces.api.deps.interactive_operation import interactive_operation

router = APIRouter(prefix="/api/v1", tags=["self-study"])


class StudyTurnInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    closure_consent: PrivacyChoice | None = None
    client_request_id: UUID | None = None
    dialogue_control: DialogueControl | None = None


@router.post("/sessions/{session_id}/study-turns")
async def post_study_turn(
    session_id: str,
    data: StudyTurnInput,
    request: Request,
    _operation=Depends(interactive_operation, scope="function"),
    db: SASession = Depends(get_db, scope="function"),
):
    session = db.get(models.Session, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    try:
        if data.dialogue_control is not None and data.text.strip():
            raise ValueError(
                "Envía texto o un control estructurado, sin órdenes simultáneas contradictorias."
            )
        receipt, replay = begin_request(
            db, session, data.client_request_id, data.model_dump(mode="json", exclude={"client_request_id"})
        )
        if replay is not None:
            return replay
        if data.closure_consent is not None:
            set_privacy_preference(db, session, **data.closure_consent.model_dump())
        result = await submit_study_turn(
            db,
            session,
            data.text,
            **({"dialogue_control": data.dialogue_control} if data.dialogue_control is not None else {}),
            **(
                {"semantic_runtime": request.app.state.semantic_runtime}
                if getattr(request.app.state, "semantic_runtime", None) is not None
                else {}
            ),
        )
        complete_request(db, receipt, result.turn_id)
    except SessionNotActive as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ModeNotEnabled as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "message": (
                    "Ese modo no está habilitado en esta actividad. Continúa en e"
                    "l modo actual o elige uno permitido."
                ),
                "requested_mode": exc.requested_mode,
                "enabled_modes": exc.enabled_modes,
            },
        ) from exc

    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None

    response = {
        "turn_id": result.turn_id,
        "mode": result.mode,
        "dialogue_action": result.dialogue_action,
        "output_text": result.output_text,
        "state_version": result.state_version,
        "sources": result.sources,
        "general_knowledge_used": result.general_knowledge_used,
    }
    if result.blocked:
        response["blocked"] = True
    from oralia.application.services.guided_dialogue_service import legacy_turn_capabilities

    response["dialogue_status"] = result.dialogue_status or legacy_turn_capabilities(
        db, session, result.turn_id, blocked=result.blocked
    )
    if result.session_closed:
        response["session_closed"] = True
        response["session_status"] = result.session_status
        response["study_summary"] = result.study_summary
    return response


@router.post("/sessions/{session_id}/study-end")
def post_study_end(
    session_id: str,
    _operation=Depends(interactive_operation, scope="function"),
    db: SASession = Depends(get_db, scope="function"),
    data: PrivacyChoice | None = None,
):
    session = db.get(models.Session, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    study_summary = None
    selected_scope = None
    if session.status == "active":
        if data is not None:
            try:
                selected_scope = validate_privacy_choice(db, session, **data.model_dump())
            except ValueError as exc:
                raise HTTPException(409, str(exc)) from None
        self_study_config = get_self_study_config(db, session.activity_configuration_id)
        study_summary = end_study_session(
            db, session, self_study_config, status="closed_voluntary", retained_scope=selected_scope
        )

    return {
        "session_id": session.id,
        "status": session.status,
        "study_summary": study_summary,
    }


tecnica_router = APIRouter(
    prefix="/api/v1/tecnica",
    tags=["self-study-tecnica"],
    dependencies=[Depends(tecnica_access_control)],
)


def _config_response(config: models.SelfStudyActivityConfig, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "id": config.id,
            "activity_configuration_id": config.activity_configuration_id,
            "enabled_modes": config.enabled_modes,
            "summary_authorized": config.summary_authorized,
            "practice_reveals_solution": config.practice_reveals_solution,
            "retention_authorized": config.retention_authorized,
        },
    )


@tecnica_router.post("/activities/{activity_id}/self-study-config")
def post_self_study_config(
    activity_id: str,
    data: SelfStudyActivityConfigInput,
    db: SASession = Depends(get_db, scope="function"),
):
    existing_before = get_self_study_config(db, activity_id)
    try:
        config = configure_self_study_activity(db, activity_id, data)
    except ActivityNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ActivityConfigurationImmutable as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    status_code = 200 if existing_before is not None else 201
    return _config_response(config, status_code)


@tecnica_router.get("/sessions/{session_id}/study-trace")
def get_study_trace(session_id: str, db: SASession = Depends(get_db, scope="function")):
    return reconstruct_session_trace(db, session_id)


@tecnica_router.post("/self-study/purge-expired")
def post_purge_expired(db: SASession = Depends(get_db, scope="function")):
    result = purge_expired_self_study_data(db)
    return {
        "sessions_matching_criteria": result.sessions_matching_criteria,
        "sessions_with_rows_deleted": result.sessions_with_rows_deleted,
        "practice_questions_deleted": result.practice_questions_deleted,
        "coherence_incidents_deleted": result.coherence_incidents_deleted,
        "trace_events_deleted": result.trace_events_deleted,
    }


@tecnica_router.get("/self-study/retention-audit")
def get_retention_audit(db: SASession = Depends(get_db, scope="function")):
    return self_study_retention_audit(db)
