"""ingest_material command (FR-001..FR-010, FR-028): validate, hash, extract, segment,
embed and index a newly uploaded document.

FR-028: extracted text travels exclusively as structured data (``MaterialFragment.text``,
``AgentRequest.input``/``.context``) — this module never concatenates it into an
instruction/prompt string, and no code path in this feature does either.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session as SASession

from oralia.application.services import index_rebuild_lock_service
from oralia.domain.materials.segmenter import segment_blocks
from oralia.infrastructure.db import models
from oralia.infrastructure.documents.extractor import (
    NotProcessableError,
    assert_processable,
    get_extractor,
    mime_type_for_filename,
)
from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    EmbeddingAdapter,
    SentenceTransformerEmbeddingAdapter,
)
from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore, VectorStore

MAX_SIZE_BYTES = 20 * 1024 * 1024  # FR-004 — deliberately deferred exact limit (spec.md Assumptions)


class UnsupportedFormatError(ValueError):
    """FR-002: file extension/MIME is not one of the 5 supported formats."""


class FileTooLargeError(ValueError):
    """FR-004."""


@dataclass
class DuplicateDetected:
    """FR-005a: the caller MUST surface this as a 409 with a resolution token, never
    silently deduplicate or silently proceed."""

    pending_document: models.MaterialDocument
    existing_document: models.MaterialDocument


# Raw bytes for a document parked in "pending_duplicate_review" until the professor
# resolves it (research.md §6) — the duplicate-resolution request carries only a
# resolution choice, never the file content again, so it must be held server-side. A
# local single-instance tool losing this on restart mid-decision is an acceptable
# limitation (Principio XI) rather than new persistent-storage schema for a transient
# few-second window.
_PENDING_UPLOAD_CONTENT: dict[str, bytes] = {}


def take_pending_content(document_id: str) -> bytes:
    return _PENDING_UPLOAD_CONTENT.pop(document_id)


def compute_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def find_duplicate(db: SASession, *, course_id: str, content_hash: str) -> models.MaterialDocument | None:
    return (
        db.query(models.MaterialDocument)
        .filter(
            models.MaterialDocument.course_id == course_id,
            models.MaterialDocument.content_hash == content_hash,
        )
        .order_by(models.MaterialDocument.created_at.desc())
        .first()
    )


def ingest_material(
    db: SASession,
    *,
    course_id: str,
    filename: str,
    content: bytes,
    activity_configuration_ids: list[str] | None = None,
    family_id: str | None = None,
    version: int = 1,
    vector_store: VectorStore | None = None,
    embedding_adapter: EmbeddingAdapter | None = None,
    skip_duplicate_check: bool = False,
) -> models.MaterialDocument | DuplicateDetected:
    mime_type = mime_type_for_filename(filename)
    if mime_type is None:
        raise UnsupportedFormatError(f"unsupported file extension for {filename!r}")
    if len(content) > MAX_SIZE_BYTES:
        raise FileTooLargeError(f"{filename} exceeds the maximum size of {MAX_SIZE_BYTES} bytes")

    content_hash = compute_hash(content)
    existing = None
    if not skip_duplicate_check:
        existing = find_duplicate(db, course_id=course_id, content_hash=content_hash)

    document = models.MaterialDocument(
        family_id=family_id or str(uuid.uuid4()),
        version=version,
        course_id=course_id,
        activity_configuration_ids=activity_configuration_ids or [],
        filename=filename,
        content_hash=content_hash,
        mime_type=mime_type,
        size_bytes=len(content),
        status="pending",
    )
    db.add(document)
    db.flush()

    if existing is not None:
        document.status = "pending_duplicate_review"
        document.error_detail = f"possible duplicate of document {existing.id} (FR-005a)"
        # Tentative candidate — confirmed by `link_existing`, cleared by `proceed_new`
        # (resolve_material_duplicate.py). Lets the resolution endpoint recover which
        # existing document this was flagged against without the professor resubmitting it.
        document.duplicate_of_document_id = existing.id
        db.add(document)
        db.flush()
        _PENDING_UPLOAD_CONTENT[document.id] = content
        return DuplicateDetected(pending_document=document, existing_document=existing)

    process_material(db, document, content, vector_store=vector_store, embedding_adapter=embedding_adapter)
    return document


def process_material(
    db: SASession,
    document: models.MaterialDocument,
    content: bytes,
    *,
    vector_store: VectorStore | None = None,
    embedding_adapter: EmbeddingAdapter | None = None,
) -> None:
    """Extraction → segmentation → embedding → indexing (FR-006..FR-010, FR-027).

    On any extraction failure the document ends in ``error``/``not_processable`` with an
    ``error_detail`` — it is never partially indexed and never reaches ``active``.
    """

    document.status = "processing"
    db.add(document)
    db.flush()

    suffix = os.path.splitext(document.filename)[1]
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(content)

        try:
            extractor = get_extractor(document.mime_type)
            blocks = extractor.extract(tmp_path)
            assert_processable(blocks)
        except NotProcessableError as exc:
            document.status = "not_processable"
            document.error_detail = str(exc)
            db.add(document)
            db.flush()
            return
        except Exception as exc:  # noqa: BLE001 — FR-027: any extraction failure degrades safely
            document.status = "error"
            document.error_detail = str(exc)
            db.add(document)
            db.flush()
            return
    finally:
        os.unlink(tmp_path)

    segments = segment_blocks(blocks)
    embedder = embedding_adapter or SentenceTransformerEmbeddingAdapter()
    store = vector_store or ChromaVectorStore()
    texts = [segment.text for segment in segments]
    vectors = embedder.embed(texts) if texts else []

    if segments:
        index_lock = index_rebuild_lock_service.acquire(db)
        try:
            for segment, vector in zip(segments, vectors, strict=True):
                fragment = models.MaterialFragment(
                    document_id=document.id,
                    document_version=document.version,
                    text=segment.text,
                    location_ref=segment.location_ref,
                    sequence_index=segment.sequence_index,
                    embedding_ref="",
                    content_type="texto",
                    course_id=document.course_id,
                    activity_configuration_ids=document.activity_configuration_ids,
                    priority=0,
                    indexing_status="indexed",
                )
                db.add(fragment)
                db.flush()
                fragment.embedding_ref = fragment.id
                db.add(fragment)
                store.add(fragment.id, vector, {"course_id": document.course_id})
        finally:
            index_rebuild_lock_service.release(db, index_lock)

    document.status = "processed"
    db.add(document)
    db.flush()
