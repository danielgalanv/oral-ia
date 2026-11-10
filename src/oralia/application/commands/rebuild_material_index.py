"""rebuild_material_index command (FR-016, FR-016a): reconstruct the vector index from
existing MaterialFragment rows, guarded by the single-writer lock (T012).

Fragment ids are never regenerated — the SQL ``MaterialFragment.id`` is used directly as
the Chroma vector id, so ``Evidence.fragment_id``/``GroundingVerificationResult.
evidence_ids``/``MaterialConflictRecord.fragment_ids`` never go stale across a rebuild.
"""

from __future__ import annotations

from sqlalchemy.orm import Session as SASession

from oralia.application.services import index_rebuild_lock_service
from oralia.infrastructure.db import models
from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
    EmbeddingAdapter,
    SentenceTransformerEmbeddingAdapter,
)
from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore, VectorStore


def rebuild_material_index(
    db: SASession,
    *,
    vector_store: VectorStore | None = None,
    embedding_adapter: EmbeddingAdapter | None = None,
) -> str:
    """Returns the new index_version. Raises IndexRebuildAlreadyInProgress (from
    index_rebuild_lock_service) if another rebuild is already running."""

    lock = index_rebuild_lock_service.acquire(db)
    try:
        store = vector_store or ChromaVectorStore()
        embedder = embedding_adapter or SentenceTransformerEmbeddingAdapter()

        fragments = (
            db.query(models.MaterialFragment)
            .filter(models.MaterialFragment.indexing_status != "retired")
            .order_by(models.MaterialFragment.document_id, models.MaterialFragment.sequence_index)
            .all()
        )
        texts = [fragment.text for fragment in fragments]
        vectors = embedder.embed(texts) if texts else []
        items = [
            (fragment.id, vector, {"course_id": fragment.course_id})
            for fragment, vector in zip(fragments, vectors, strict=True)
        ]
        return store.rebuild(items)
    finally:
        index_rebuild_lock_service.release(db, lock)
