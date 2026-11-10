"""Explicit pytest-only synthetic vectors for privacy/permission wiring regressions.

Identical vectors deliberately provide no relevance signal. Never use these results
as embedding quality, retrieval quality, model capacity or pedagogical evidence.
The separate audit_cpu_test_guard still forbids any real model load.
"""

import pytest


@pytest.fixture(autouse=True)
def synthetic_vectors_for_structural_integration(monkeypatch):
    from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
        SentenceTransformerEmbeddingAdapter,
    )

    monkeypatch.setattr(
        SentenceTransformerEmbeddingAdapter, "embed", lambda self, texts: [[1.0, 0.0] for _ in texts]
    )
