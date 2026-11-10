"""Authorized metadata-only resume and confirmed teacher closure; no recovery by code."""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict, StrictBool
from sqlalchemy import update
from sqlalchemy.orm import Session

from oralia.application.commands.start_session import AI_DISCLOSURE
from oralia.application.services.trace_service import record_event
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.db import get_db
from oralia.interfaces.api.deps.interactive_operation import interactive_operation
from oralia.interfaces.api.deps.local_access import request_tokens

router = APIRouter(prefix="/api/v1", tags=["governance", "participante"])


@router.get("/sessions/{session_id}/requests/{request_id}")
def request_receipt(session_id: str, request_id: UUID, db: Session = Depends(get_db, scope="function")):
    from oralia.application.services.session_privacy_service import valid_retained_scope
    from oralia.application.services.turn_request_service import receipt_view

    session = db.get(models.Session, session_id)
    if (
        session is None
        or session.status != "active"
        and "transcript" not in valid_retained_scope(db, session)
    ):
        raise HTTPException(404, "El recibo ya no está disponible conforme a la conservación de la sesión.")

    receipt = (
        db.query(models.TurnRequestReceipt)
        .filter_by(session_id=session_id, client_request_id=str(request_id))
        .one_or_none()
    )
    if receipt is None:
        raise HTTPException(404, "No hay resultado confirmado para este envío; no se ha vuelto a ejecutar.")
    return receipt_view(receipt)


def session_view(db, session):
    from oralia.application.services.guided_dialogue_service import (
        activity_capabilities,
        is_guided,
        pending_question_view,
    )
    from oralia.domain.dialogue.contracts import DialogueContext

    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    response = {
        "session_id": session.id,
        "mode": activity.mode,
        "activity_configuration_id": activity.id,
        "ai_disclosure": AI_DISCLOSURE,
        "activity": {
            "name": activity.name,
            "objective": activity.objective,
            "max_turns": activity.max_turns,
            "max_duration_seconds": activity.max_duration_seconds,
            "capabilities": activity_capabilities(db, activity),
        },
    }
    state = db.get(models.CognitiveState, session.id)
    if state is not None and state.dialogue_context and is_guided(db, activity.id):
        context = DialogueContext.model_validate(state.dialogue_context)
        response["dialogue_status"] = {
            "effective_profile": context.effective_profile,
            "provider": "fixed-dialogue-template/v1" if context.last_notice else "reviewed-unit-renderer/v1",
            "pending_topic": context.pending_topic_ref,
            "pending_question": pending_question_view(db, session, context),
        }
    return response


@router.get("/auth/owned-session")
def owned_session(request: Request, db: Session = Depends(get_db, scope="function")):
    for token in request_tokens(request):
        grant = request.app.state.local_access.resolve(token)
        if grant and grant.role == "participant":
            session = db.get(models.Session, grant.session_id)
            if session is not None and session.status == "active":
                return {"session": session_view(db, session)}
    return {"session": None}


@router.get("/sessions/{session_id}/resume")
def resume(session_id: str, db: Session = Depends(get_db, scope="function")):
    session = db.get(models.Session, session_id)
    if session is None or session.status != "active":
        raise HTTPException(404, "No hay una sesión activa para retomar con este acceso.")
    # Existing access_guard requires the participant grant for this exact session.
    # Do not replay cached text or create a replacement owner token.
    return session_view(db, session)


@router.get("/governance/active-session")
def active_session(db: Session = Depends(get_db, scope="function")):
    session = db.query(models.Session).filter_by(status="active", active_lock_token="ACTIVE").one_or_none()
    if session is None:
        return {"session": None}
    return {
        "session": {
            "session_id": session.id,
            "activity_configuration_id": session.activity_configuration_id,
            "started_at": session.started_at.isoformat(),
            "turn_count": session.turn_count,
        }
    }


class TeacherCloseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirm: StrictBool
    reason: Literal["abandoned", "owner_access_lost"]


@router.post("/governance/sessions/{session_id}/close")
def teacher_close(
    session_id: str,
    data: TeacherCloseInput,
    _operation=Depends(interactive_operation, scope="function"),
    db: Session = Depends(get_db, scope="function"),
):
    if not data.confirm:
        raise HTTPException(409, "Revisa la sesión y confirma expresamente el cierre docente.")
    session = db.get(models.Session, session_id)
    if session is None:
        raise HTTPException(404, "session not found")
    guarded = db.execute(
        update(models.Session)
        .where(models.Session.id == session_id, models.Session.status == "active")
        .values(status="active")
    )
    if guarded.rowcount != 1:
        db.refresh(session)
        return {"status": session.status, "transition_won": False}
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    status = "closed_teacher_confirmed"
    try:
        if activity.mode == "oral_defense":
            from oralia.application.commands.end_defense_session import end_defense_session

            config = (
                db.query(models.DefenseActivityConfig)
                .filter_by(activity_configuration_id=activity.id)
                .one_or_none()
            )
            preference = db.get(models.SessionPrivacyPreference, session_id)
            retain = bool(preference and preference.retain)
            end_defense_session(
                db, session, config, status=status, retain=retain, scope=preference.scope if retain else []
            )
        elif activity.mode == "self_study":
            from oralia.application.commands.end_study_session import end_study_session

            config = (
                db.query(models.SelfStudyActivityConfig)
                .filter_by(activity_configuration_id=activity.id)
                .one_or_none()
            )
            end_study_session(db, session, config, status=status)
        else:
            from oralia.application.commands.end_session import close_session_with_outcome

            close_session_with_outcome(db, session, status=status)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    record_event(
        db,
        session_id=session.id,
        event_type="teacher_confirmed_close",
        payload={"status": status, "reason_codes": [data.reason], "component": "teacher"},
        memory_category="procedural",
    )
    return {"status": session.status, "transition_won": True}
