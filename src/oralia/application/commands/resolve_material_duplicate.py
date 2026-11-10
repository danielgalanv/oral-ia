"""Two-step duplicate resolution (FR-005a, research.md §6): the professor's explicit
choice — never an automatic heuristic — decides whether a possible duplicate links to the
existing document or proceeds as a new, distinct one."""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.ingest_material import process_material, take_pending_content
from oralia.infrastructure.db import models
from oralia.infrastructure.embeddings.sentence_transformer_adapter import EmbeddingAdapter
from oralia.infrastructure.vector_store.chroma_store import VectorStore


class PendingDocumentNotFoundError(LookupError):
    pass


class NotPendingDuplicateReviewError(ValueError):
    pass


def _load_pending(db: SASession, pending_document_id: str) -> models.MaterialDocument:
    pending = db.get(models.MaterialDocument, pending_document_id)
    if pending is None:
        raise PendingDocumentNotFoundError(pending_document_id)
    if pending.status != "pending_duplicate_review":
        raise NotPendingDuplicateReviewError(
            f"document {pending_document_id} is not awaiting duplicate resolution "
            f"(status={pending.status})"
        )
    return pending


def link_existing(db: SASession, *, pending_document_id: str) -> models.MaterialDocument:
    """The professor confirms the upload IS the same material — link, don't reprocess."""

    pending = _load_pending(db, pending_document_id)
    pending.status = "not_processable"
    pending.error_detail = f"linked to existing document {pending.duplicate_of_document_id} (FR-005a)"
    db.add(pending)
    db.flush()
    take_pending_content(pending.id)  # no longer needed — discard
    return pending


def proceed_new(
    db: SASession,
    *,
    pending_document_id: str,
    vector_store: VectorStore | None = None,
    embedding_adapter: EmbeddingAdapter | None = None,
) -> models.MaterialDocument:
    """The professor confirms this is a genuinely distinct document — process it as such,
    not linked to the pre-existing hash match."""

    document = _load_pending(db, pending_document_id)
    content = take_pending_content(document.id)
    document.duplicate_of_document_id = None
    document.error_detail = None
    process_material(db, document, content, vector_store=vector_store, embedding_adapter=embedding_adapter)
    return document
