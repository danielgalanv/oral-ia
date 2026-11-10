"""Human governance: local access, explicit publication and privacy projections."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from oralia.application.commands.create_activity import ActivityConfigurationInput
from oralia.application.services import activity_governance_service as activities
from oralia.application.services import session_privacy_service as privacy
from oralia.application.services.session_export_service import export_sessions
from oralia.domain.policies.output_template_catalog import DEFAULT_OUTPUT_TEMPLATE_CATALOG
from oralia.infrastructure.db import models
from oralia.infrastructure.vector_store.index_status import read_index_status
from oralia.interfaces.api.deps.db import get_db
from oralia.interfaces.api.deps.local_access import request_tokens

router = APIRouter(prefix="/api/v1", tags=["governance"])


class LoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    secret: str = Field(max_length=1000)


@router.post("/auth/login")
def login(data: LoginInput, request: Request, response: Response):
    token = request.app.state.local_access.login(data.secret)
    response.set_cookie(
        request.app.state.local_access.cookie_names[0], token, httponly=True, samesite="strict", max_age=3600
    )
    response.headers["Cache-Control"] = "no-store"
    return {"role": "teacher", "expires_in": 3600, "access_token": token}


@router.post("/auth/logout")
def logout(request: Request, response: Response):
    for token in request_tokens(request):
        request.app.state.local_access.revoke(token)
    response.headers["Cache-Control"] = "no-store"
    for name in request.app.state.local_access.cookie_names:
        response.delete_cookie(name)
    return {"logged_out": True}


@router.get("/auth/me")
def me(request: Request):
    return {"role": request.state.access_grant.role}


class CreateCourseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=200)
    subject_code: str = Field(min_length=1, max_length=50)


@router.post("/governance/courses", status_code=201)
def create_course(data: CreateCourseInput, db: Session = Depends(get_db, scope="function")):
    row = models.Course(**data.model_dump())
    db.add(row)
    db.flush()
    return {"id": row.id, "name": row.name}


class RetentionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    retention_days: int = Field(ge=0, le=36500)
    content_scope: Literal["transcript,summary", "transcript", "summary"] = "transcript,summary"
    access_scope: Literal["local_teacher", "participant_only"] = "local_teacher"


@router.post("/governance/retention-policies", status_code=201)
def create_retention(data: RetentionInput, db: Session = Depends(get_db, scope="function")):
    row = models.RetentionPolicy(**data.model_dump(), purge_rule="manual")
    db.add(row)
    db.flush()
    return {"id": row.id, "version": row.version, "retention_days": row.retention_days}


class ManagedActivityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    activity: ActivityConfigurationInput
    model_id: str = "deterministic"
    material_versions: list[dict] = Field(default_factory=list, max_length=100)
    mode_config: dict = Field(default_factory=dict)


@router.get("/governance/activities")
def list_activities(db: Session = Depends(get_db, scope="function")):
    return [
        activities.activity_view(db, row)
        for row in db.query(models.ActivityConfiguration).order_by(
            models.ActivityConfiguration.created_at.desc()
        )
    ]


@router.post("/governance/activities", status_code=201)
def create_managed(data: ManagedActivityInput, db: Session = Depends(get_db, scope="function")):
    try:
        row = activities.create_managed_activity(
            db,
            data.activity,
            model_id=data.model_id,
            material_versions=data.material_versions,
            mode_config=data.mode_config,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
    return activities.activity_view(db, row)


class DuplicateActivityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    new_family: StrictBool = False
    changes: dict = Field(default_factory=dict)


@router.post("/governance/activities/{activity_id}/duplicate", status_code=201)
def duplicate(
    activity_id: str, data: DuplicateActivityInput, db: Session = Depends(get_db, scope="function")
):
    try:
        row = activities.duplicate_activity(db, activity_id, data.changes, new_family=data.new_family)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
    except (IntegrityError, OperationalError):
        raise HTTPException(409, "activity version conflict; reload before retrying") from None
    return activities.activity_view(db, row)


@router.post("/governance/activities/{activity_id}/activate")
def activate(activity_id: str, db: Session = Depends(get_db, scope="function")):
    try:
        activities.publish_activity(db, activity_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    except (IntegrityError, OperationalError):
        raise HTTPException(409, "activity publication conflict") from None
    return activities.activity_view(db, db.get(models.ActivityConfiguration, activity_id))


@router.post("/governance/activities/{activity_id}/retire")
def retire(activity_id: str, db: Session = Depends(get_db, scope="function")):
    try:
        activities.retire_activity(db, activity_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from None
    return activities.activity_view(db, db.get(models.ActivityConfiguration, activity_id))


@router.get("/governance/catalog")
def catalog(db: Session = Depends(get_db, scope="function")):
    return {
        "index_status": read_index_status(),
        "models": activities.available_models(),
        "output_templates": [
            {
                "template_id": e.template_id,
                "version": e.version,
                "topic_ref": e.topic_ref,
                "purpose_ref": e.purpose_ref,
                "action_ref": e.action_ref,
                "message_type": e.message_type,
            }
            for e in DEFAULT_OUTPUT_TEMPLATE_CATALOG.entries
        ],
        "compositions": activities.COMPOSITIONS,
        "courses": [{"id": r.id, "name": r.name} for r in db.query(models.Course)],
        "retention_policies": [
            {"id": r.id, "version": r.version, "retention_days": r.retention_days}
            for r in db.query(models.RetentionPolicy)
        ],
        "materials": [
            {
                "document_id": r.id,
                "version": r.version,
                "course_id": r.course_id,
                "filename": r.filename,
                "status": r.status,
                "error_code": "processing_failed" if r.error_detail else None,
                "fragments_indexed": db.query(models.MaterialFragment)
                .filter_by(document_id=r.id, indexing_status="indexed")
                .count(),
            }
            for r in db.query(models.MaterialDocument)
        ],
    }


def _session(db, session_id):
    row = db.get(models.Session, session_id)
    if row is None:
        raise HTTPException(404, "session not found")
    return row


class PrivacyInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    retain: StrictBool = False
    scope: list[str] = Field(default_factory=list)


@router.get("/sessions/{session_id}/privacy")
def get_privacy(session_id: str, db: Session = Depends(get_db, scope="function")):
    return privacy.privacy_view(db, _session(db, session_id))


@router.post("/sessions/{session_id}/privacy")
def update_privacy(session_id: str, data: PrivacyInput, db: Session = Depends(get_db, scope="function")):
    row = _session(db, session_id)
    try:
        privacy.set_privacy_preference(db, row, **data.model_dump())
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    return privacy.privacy_view(db, row)


@router.get("/sessions/{session_id}/transcript")
def get_transcript(session_id: str, db: Session = Depends(get_db, scope="function")):
    return privacy.own_transcript(db, _session(db, session_id))


@router.get("/governance/sessions")
def reviewable_sessions(db: Session = Depends(get_db, scope="function")):
    return [
        {
            "session_id": row.id,
            "activity_configuration_id": row.activity_configuration_id,
            "status": row.status,
            "scope": sorted(scope),
            "turn_count": row.turn_count,
        }
        for row in db.query(models.Session)
        .filter(models.Session.ended_at.isnot(None))
        .order_by(models.Session.started_at.desc())
        if (scope := privacy.teacher_retained_scope(db, row))
    ]


@router.get("/governance/sessions/{session_id}")
def review(session_id: str, db: Session = Depends(get_db, scope="function")):
    try:
        return privacy.review_session(db, session_id)
    except ValueError:
        raise HTTPException(404, "session is not reviewable") from None


class ExportInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_ids: list[str] = Field(min_length=1, max_length=100)
    format: str = "json"
    include_free_text: StrictBool = False
    reviewed_free_text: StrictBool = False


@router.post("/governance/exports")
def export(data: ExportInput, db: Session = Depends(get_db, scope="function")):
    if data.format not in {"json", "markdown"}:
        raise HTTPException(422, "format must be json or markdown")
    try:
        bundle, markdown = export_sessions(
            db,
            data.session_ids,
            include_free_text=data.include_free_text,
            reviewed_free_text=data.reviewed_free_text,
        )
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
    extension = "json" if data.format == "json" else "md"
    headers = {
        "Cache-Control": "no-store",
        "Content-Disposition": f'attachment; filename="oralia-export.{extension}"',
    }
    return (
        JSONResponse(bundle, headers=headers)
        if data.format == "json"
        else Response(markdown, media_type="text/markdown", headers=headers)
    )


class DeleteInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirm: StrictBool


@router.delete("/sessions/{session_id}/content")
def delete_content(session_id: str, data: DeleteInput, db: Session = Depends(get_db, scope="function")):
    if data.confirm is not True:
        raise HTTPException(409, "explicit deletion confirmation required")
    try:
        return privacy.delete_session_content(db, session_id)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None


@router.post("/governance/purge")
def purge(db: Session = Depends(get_db, scope="function")):
    return privacy.purge_private_sessions(db)


@router.get("/governance/metrics")
def metrics(db: Session = Depends(get_db, scope="function")):
    turn_count = db.query(models.Turn).count()
    observed = db.query(models.Turn).filter(models.Turn.latency_ms.isnot(None)).count()
    return {
        "scope": "system_aggregate",
        "sessions": db.query(models.Session).count(),
        "turns": turn_count,
        "completed_sessions": db.query(models.Session).filter(models.Session.status != "active").count(),
        "blocked_turns": db.query(models.Turn).filter_by(status="blocked").count(),
        "incidents": db.query(models.TraceEvent)
        .filter(models.TraceEvent.event_type.in_(["transcription_failed", "tts_failed", "agent_failed"]))
        .count(),
        "latency_ms_mean": db.query(func.avg(models.Turn.latency_ms)).scalar(),
        "latency_observations": observed,
        "missing": {
            "turn_latency": turn_count - observed,
            "perceived_usefulness": "not_collected",
            "academic_metrics": "out_of_scope",
        },
    }
