"""replace_material_version command (FR-014, FR-015): create a new document version and
retire the previous one — never deleted, format change allowed.

The previous version is only retired once the new one finishes processing successfully;
if the new upload ends in ``error``/``not_processable``, the previously-working version
stays untouched and active (a processing failure here must not remove the professor's
only usable version — consistent with FR-027's "existing index untouched" degradation
rule).
"""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.commands.ingest_material import (
    UnsupportedFormatError,
    compute_hash,
    process_material,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from oralia.infrastructure.documents.extractor import mime_type_for_filename
from oralia.infrastructure.embeddings.sentence_transformer_adapter import EmbeddingAdapter
from oralia.infrastructure.vector_store.chroma_store import VectorStore


class PreviousVersionNotFoundError(LookupError):
    pass


def replace_material_version(
    db: SASession,
    *,
    previous_document_id: str,
    filename: str,
    content: bytes,
    vector_store: VectorStore | None = None,
    embedding_adapter: EmbeddingAdapter | None = None,
) -> models.MaterialDocument:
    previous = db.get(models.MaterialDocument, previous_document_id)
    if previous is None:
        raise PreviousVersionNotFoundError(previous_document_id)

    mime_type = mime_type_for_filename(filename)
    if mime_type is None:
        raise UnsupportedFormatError(f"unsupported file extension for {filename!r}")

    new_document = models.MaterialDocument(
        family_id=previous.family_id,
        version=previous.version + 1,
        course_id=previous.course_id,
        activity_configuration_ids=list(previous.activity_configuration_ids),
        filename=filename,
        content_hash=compute_hash(content),
        mime_type=mime_type,
        size_bytes=len(content),
        status="pending",
    )
    db.add(new_document)
    db.flush()

    process_material(
        db, new_document, content, vector_store=vector_store, embedding_adapter=embedding_adapter
    )

    if new_document.status == "processed":
        previous.retired_at = utcnow()
        db.add(previous)
        # data-model.md: MaterialFragment.indexing_status → "retired" cuando el
        # documento se retira — the retriever's exclusion filter checks this directly.
        previous_fragments = db.query(models.MaterialFragment).filter_by(document_id=previous.id).all()
        for fragment in previous_fragments:
            fragment.indexing_status = "retired"
            db.add(fragment)
        db.flush()

    return new_document
