"""Área técnica — gestión de materiales y RAG (contracts/material-retriever-agent.md)."""

from __future__ import annotations

import uuid
from typing import Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session as SASession

from oralia.application.commands.activate_material import (
    DocumentNotProcessedError,
    DocumentRetiredError,
    MaterialDocumentNotFoundError,
    activate_material,
    deactivate_material,
)
from oralia.application.commands.ingest_material import (
    DuplicateDetected,
    FileTooLargeError,
    UnsupportedFormatError,
    ingest_material,
)
from oralia.application.commands.rebuild_material_index import rebuild_material_index
from oralia.application.commands.replace_material_version import (
    PreviousVersionNotFoundError,
    replace_material_version,
)
from oralia.application.commands.resolve_material_duplicate import (
    NotPendingDuplicateReviewError,
    PendingDocumentNotFoundError,
    link_existing,
    proceed_new,
)
from oralia.application.commands.review_material_conflict import (
    ConflictNotFoundError,
    list_conflicts,
    review_material_conflict,
)
from oralia.application.queries.get_material_catalog import get_material_detail, list_materials
from oralia.application.services.index_rebuild_lock_service import IndexRebuildAlreadyInProgress
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent
from oralia.infrastructure.db import models
from oralia.interfaces.api.deps.auth_stub import tecnica_access_control
from oralia.interfaces.api.deps.db import get_db

router = APIRouter(
    prefix="/api/v1/materials",
    tags=["materials"],
    dependencies=[Depends(tecnica_access_control)],
)


def _document_response(document: models.MaterialDocument) -> dict:
    return {
        "id": document.id,
        "family_id": document.family_id,
        "version": document.version,
        "course_id": document.course_id,
        "activity_configuration_ids": document.activity_configuration_ids,
        "filename": document.filename,
        "content_hash": document.content_hash,
        "mime_type": document.mime_type,
        "size_bytes": document.size_bytes,
        "status": document.status,
        "error_detail": document.error_detail,
        "retired_at": document.retired_at,
        "duplicate_of_document_id": document.duplicate_of_document_id,
        "created_at": document.created_at,
    }


@router.post("/documents", status_code=201)
async def post_document(
    file: UploadFile = File(...),
    course_id: str = Form(...),
    activity_configuration_ids: list[str] = Form(default_factory=list),
    db: SASession = Depends(get_db, scope="function"),
):
    content = await file.read()
    try:
        result = ingest_material(
            db,
            course_id=course_id,
            filename=file.filename or "documento",
            content=content,
            activity_configuration_ids=activity_configuration_ids,
        )
    except (UnsupportedFormatError, FileTooLargeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if isinstance(result, DuplicateDetected):
        return JSONResponse(
            status_code=409,
            content={
                "detail": "possible duplicate",
                "existing_document_id": result.existing_document.id,
                "conflict_token": result.pending_document.id,
            },
        )
    return _document_response(result)


class DuplicateResolutionInput(BaseModel):
    resolution: Literal["link_existing", "proceed_new"]


@router.post("/documents/{document_id}/duplicate-resolution")
def post_duplicate_resolution(
    document_id: str, data: DuplicateResolutionInput, db: SASession = Depends(get_db, scope="function")
):
    try:
        if data.resolution == "link_existing":
            document = link_existing(db, pending_document_id=document_id)
        else:
            document = proceed_new(db, pending_document_id=document_id)
    except PendingDocumentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="document not found") from exc
    except NotPendingDuplicateReviewError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _document_response(document)


@router.post("/documents/{document_id}/activate")
def post_activate(document_id: str, db: SASession = Depends(get_db, scope="function")):
    try:
        document = activate_material(db, document_id)
    except MaterialDocumentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="document not found") from exc
    except (DocumentNotProcessedError, DocumentRetiredError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return _document_response(document)


@router.post("/documents/{document_id}/deactivate")
def post_deactivate(document_id: str, db: SASession = Depends(get_db, scope="function")):
    try:
        document = deactivate_material(db, document_id)
    except MaterialDocumentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="document not found") from exc
    return _document_response(document)


@router.get("/documents")
def get_documents(course_id: str | None = None, db: SASession = Depends(get_db, scope="function")):
    return [_document_response(d) for d in list_materials(db, course_id=course_id)]


@router.get("/documents/{document_id}")
def get_document(document_id: str, db: SASession = Depends(get_db, scope="function")):
    detail = get_material_detail(db, document_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="document not found")
    return {
        **_document_response(detail["document"]),
        "course_coverage": detail["course_coverage"],
    }


@router.post("/documents/{document_id}/versions", status_code=201)
async def post_version(
    document_id: str, file: UploadFile = File(...), db: SASession = Depends(get_db, scope="function")
):
    content = await file.read()
    try:
        new_document = replace_material_version(
            db, previous_document_id=document_id, filename=file.filename or "documento", content=content
        )
    except PreviousVersionNotFoundError as exc:
        raise HTTPException(status_code=404, detail="document not found") from exc
    except UnsupportedFormatError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _document_response(new_document)


class MaterialQueryInput(BaseModel):
    query_text: str
    course_id: str
    activity_configuration_id: str
    session_id: str | None = None
    max_fragments: int = 5
    time_budget_ms: int = 5000


@router.post("/query")
async def post_query(data: MaterialQueryInput, db: SASession = Depends(get_db, scope="function")):
    """Direct-invocation demo/test surface for MaterialRetrieverAgent (research.md §1) —
    NOT part of a real conversational turn, that composition belongs to Feature 003."""

    agent = MaterialRetrieverAgent(db)
    agent_request = AgentRequest(
        session_id=uuid.UUID(data.session_id) if data.session_id else uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": data.query_text,
            "course_id": data.course_id,
            "activity_configuration_id": data.activity_configuration_id,
            "session_id": data.session_id,
            "max_fragments": data.max_fragments,
            "time_budget_ms": data.time_budget_ms,
        },
        deadline_ms=data.time_budget_ms,
    )
    result = await agent.execute(agent_request, CancellationToken())
    return result.output


def _conflict_response(record: models.MaterialConflictRecord) -> dict:
    return {
        "id": record.id,
        "document_ids": record.document_ids,
        "fragment_ids": record.fragment_ids,
        "conflicting_claims": record.conflicting_claims,
        "detected_by_query": record.detected_by_query,
        "review_status": record.review_status,
        "created_at": record.created_at,
        "reviewed_at": record.reviewed_at,
    }


@router.post("/index/rebuild")
def post_rebuild_index(db: SASession = Depends(get_db, scope="function")):
    try:
        new_version = rebuild_material_index(db)
    except IndexRebuildAlreadyInProgress as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"index_version": new_version}


@router.get("/conflicts")
def get_conflicts(
    review_status: str | None = "pending_review", db: SASession = Depends(get_db, scope="function")
):
    return [_conflict_response(c) for c in list_conflicts(db, review_status=review_status)]


@router.post("/conflicts/{conflict_id}/review")
def post_review_conflict(conflict_id: str, db: SASession = Depends(get_db, scope="function")):
    try:
        record = review_material_conflict(db, conflict_id)
    except ConflictNotFoundError as exc:
        raise HTTPException(status_code=404, detail="conflict not found") from exc
    return _conflict_response(record)
