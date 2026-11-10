"""Real isolated Chroma, synthetic vectors only; legacy read compatibility."""

import pytest

from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore


def identity(encoder="A"):
    return {
        "encoder": encoder,
        "revision": "local-snapshot-sha",
        "dimension": 2,
        "normalization": "none",
        "representation": "text/pooling-model-config-v1",
        "extraction": "synthetic-v1",
        "chunking": "whole-unit-v1",
    }


def test_same_dimension_different_encoder_is_rejected(tmp_path):
    store = ChromaVectorStore(str(tmp_path), fingerprint=identity())
    store.add("one", [1.0, 0.0], {"course_id": "c"})
    other = ChromaVectorStore(str(tmp_path), fingerprint=identity("B"))
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        other.query([1.0, 0.0], {}, 1)
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        other.add("two", [1.0, 0.0], {"course_id": "c"})
    assert store.query([1.0, 0.0], {}, 1)[0].fragment_id == "one"


def test_legacy_read_preserved_but_not_accredited_for_new_comparison(tmp_path):
    old = ChromaVectorStore(str(tmp_path))
    old.add("one", [1.0, 0.0], {"course_id": "c"})
    current = ChromaVectorStore(str(tmp_path), fingerprint=identity())
    with pytest.raises(ValueError, match="unaccredited legacy index"):
        current.query([1.0, 0.0], {}, 1)
    assert old.query([1.0, 0.0], {}, 1)[0].fragment_id == "one"


def test_dimension_mismatch_rejected_before_mutation(tmp_path):
    store = ChromaVectorStore(str(tmp_path), fingerprint=identity())
    with pytest.raises(ValueError, match="dimension"):
        store.add("one", [1.0], {"course_id": "c"})
    assert store.get_index_version() == "1"


def test_fingerprint_defensive_copy_and_rebuild_version(tmp_path):
    original = identity()
    store = ChromaVectorStore(str(tmp_path), fingerprint=original)
    original["encoder"] = "B"
    store.add("one", [1.0, 0.0], {"course_id": "c"})
    assert store.rebuild([("two", [0.0, 1.0], {"course_id": "c"})]) == "2"
    reopened = ChromaVectorStore(str(tmp_path), fingerprint=identity())
    assert reopened.query([0.0, 1.0], {}, 1)[0].fragment_id == "two"
