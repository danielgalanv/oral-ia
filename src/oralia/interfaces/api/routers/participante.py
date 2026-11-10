"""Área de participante — contracts/api-participante.md."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session as SASession

from oralia.application.commands.end_session import CONFIRMATION_MESSAGE, end_session_voluntarily
from oralia.application.commands.start_session import (
    AI_DISCLOSURE,
    ActivityNotFound,
    InvalidParticipantCode,
    SessionPreflightFailure,
    StartSessionInput,
    start_session,
)
from oralia.application.commands.submit_turn import SessionNotActive, submit_turn
from oralia.application.services.session_lock_service import SessionAlreadyActive
from oralia.application.services.session_privacy_service import (
    PrivacyChoice,
    set_privacy_preference,
    validate_privacy_choice,
)
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.db import get_db

router = APIRouter(prefix="/api/v1", tags=["participante"])


class TurnInput(BaseModel):
    text: str
    closure_consent: PrivacyChoice | None = None


@router.post("/sessions", status_code=201)
def post_session(
    data: StartSessionInput,
    request: Request,
    response: Response,
    db: SASession = Depends(get_db, scope="function"),
):
    try:
        session = start_session(db, data)
    except ActivityNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidParticipantCode as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SessionAlreadyActive as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "interactive_session_active",
                "message": (
                    "Ya hay una sesión activa. Si conservas su acceso, retómala; "
                    "si lo perdiste, solicita un cierre docente confirmado."
                ),
            },
        ) from exc
    except SessionPreflightFailure as exc:
        raise HTTPException(status_code=409, detail={"code": exc.code, "message": exc.message}) from None
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    token = request.app.state.local_access.issue("participant", session.id)
    response.set_cookie(
        request.app.state.local_access.cookie_names[1], token, httponly=True, samesite="strict", max_age=86400
    )
    response.headers["Cache-Control"] = "no-store"
    return {
        "session_id": session.id,
        "access_token": token,
        "privacy_notice": (
            "Uso local con código seudónimo. Audio efímero. Conservar requiere autorización, "
            "elección explícita y plazo finito; puedes completar sin conservar."
        ),
        "ai_disclosure": AI_DISCLOSURE,
        "activity": {
            "name": activity.name,
            "objective": activity.objective,
            "max_turns": activity.max_turns,
            "max_duration_seconds": activity.max_duration_seconds,
            "capabilities": _capabilities(db, activity),
        },
    }


@router.post("/sessions/{session_id}/turns")
async def post_turn(session_id: str, data: TurnInput, db: SASession = Depends(get_db, scope="function")):
    session = db.get(models.Session, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")

    try:
        if data.closure_consent is not None:
            set_privacy_preference(db, session, **data.closure_consent.model_dump())
        result = await submit_turn(db, session, data.text)
    except SessionNotActive as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None

    response = {
        "session_status": session.status,
        "turn_id": result.turn_id,
        "dialogue_action": result.dialogue_action,
        "output_text": result.output_text,
        "state_version": result.state_version,
    }
    if result.blocked:
        response["blocked"] = True
    return response


@router.post("/sessions/{session_id}/end")
def post_end_session(
    session_id: str, db: SASession = Depends(get_db, scope="function"), data: PrivacyChoice | None = None
):
    session = db.get(models.Session, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    selected_scope = None
    if session.status == "active":
        if data is not None:
            try:
                selected_scope = validate_privacy_choice(db, session, **data.model_dump())
            except ValueError as exc:
                raise HTTPException(409, str(exc)) from None
        end_session_voluntarily(db, session, retained_scope=selected_scope)
    return {
        "session_id": session.id,
        "status": session.status,
        "confirmation_message": CONFIRMATION_MESSAGE,
    }


@router.get("/activities/{activity_id}")
def get_activity_public(activity_id: str, db: SASession = Depends(get_db, scope="function")):
    activity = db.get(models.ActivityConfiguration, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="activity not found")
    governance = db.get(models.ActivityGovernance, activity.id)
    if governance is not None and governance.status != "active":
        raise HTTPException(404, "activity not available")
    return {
        "id": activity.id,
        "name": activity.name,
        "objective": activity.objective,
        "mode": activity.mode,
        "language": activity.language,
        "capabilities": _capabilities(db, activity),
    }


def _capabilities(db, activity):
    from oralia.application.services.guided_dialogue_service import activity_capabilities

    return activity_capabilities(db, activity)
