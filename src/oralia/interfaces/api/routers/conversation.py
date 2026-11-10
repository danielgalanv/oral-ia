"""Owned transcript entry point; existing commands and privacy services retain authority."""

import re
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from oralia.application.orchestration.final_output_gate import decide_final_output
from oralia.application.services.screenless_navigation_service import render_navigation, screenless_enabled
from oralia.application.services.session_privacy_service import delete_session_content
from oralia.domain.dialogue.contracts import DialogueContext
from oralia.domain.dialogue.interpretation import normalized
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.db import get_db
from oralia.interfaces.api.deps.interactive_operation import interactive_operation

router = APIRouter(prefix="/api/v1", tags=["conversation"])


class ConversationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(max_length=4000)
    client_request_id: UUID | None = None


@router.post("/sessions/{session_id}/conversation-controls")
async def conversation(
    session_id: str,
    data: ConversationInput,
    request: Request,
    _operation=Depends(interactive_operation, scope="function"),
    db: Session = Depends(get_db, scope="function"),
):
    # The existing /sessions/{id}/... middleware requires this session's owner.
    session = db.get(models.Session, session_id)
    if session is None:
        raise HTTPException(404, "session not found")
    activity = db.get(models.ActivityConfiguration, session.activity_configuration_id)
    if not screenless_enabled(activity, session.participant_code):
        raise HTTPException(409, "La actividad no autoriza el recorrido conversacional sin pantalla.")
    if session.status == "active":
        if activity.mode == "self_study":
            from oralia.interfaces.api.routers.self_study import StudyTurnInput, post_study_turn

            return await post_study_turn(
                session_id=session_id,
                data=StudyTurnInput(text=data.text, client_request_id=data.client_request_id),
                request=request,
                _operation=None,
                db=db,
            )
        from oralia.interfaces.api.routers.oral_defense import DefenseTurnInput, post_defense_turn

        return await post_defense_turn(
            session_id,
            DefenseTurnInput(
                text=data.text,
                client_request_id=data.client_request_id,
            ),
            None,
            db,
        )
    if data.client_request_id is not None:
        raise HTTPException(409, "Los comandos de registro cerrado no crean ni repiten turnos.")
    value = normalized(data.text).strip(" ¡!¿?.,")
    name, index = "closed", None
    if value == "eliminar mi contenido":
        name = "delete_prompt"
    elif value == "confirmo eliminar el contenido de esta sesion":
        name = "deleted"
    elif value in {"estado de conservacion", "que conservaras"}:
        name = "privacy_closed"
    elif match := re.fullmatch(r"revisar intervencion ([0-9]{1,3}|uno|dos|tres|cuatro|cinco)", value):
        word = match[1]
        index = int(word) if word.isdigit() else ["uno", "dos", "tres", "cuatro", "cinco"].index(word) + 1
        name = "review"
    try:
        from oralia.application.services.dialogue_output_catalog import activity_output_catalog

        catalog = activity_output_catalog(activity)
        snapshot, proposal = render_navigation(
            db, session, activity, name, DialogueContext(), [], review_index=index
        )
        decision = decide_final_output(snapshot, proposal, catalog=catalog, allow_operational_attempt=False)
        if decision.output_text is not None and name == "deleted":
            delete_session_content(db, session.id)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    # No Turn, receipt containing text, context, or new consent is created after closure.
    return {
        "output_text": decision.output_text,
        "blocked": decision.blocked,
        "session_status": session.status,
        "deleted": name == "deleted" and not decision.blocked,
        "screenless_text_ready": True,
    }
