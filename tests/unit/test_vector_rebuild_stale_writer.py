"""Serialized rebuilds through long-lived stores must preserve blue-green safety."""

import pytest

from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore


def test_stale_rebuilder_advances_from_committed_version(tmp_path):
    first = ChromaVectorStore(str(tmp_path))
    first.add("one", [1.0, 0.0], {"course_id": "c"})
    stale = ChromaVectorStore(str(tmp_path))
    assert first.rebuild([("two", [0.0, 1.0], {"course_id": "c"})]) == "2"
    assert stale.rebuild([("three", [1.0, 0.0], {"course_id": "c"})]) == "3"
    # The previous committed generation remains intact for in-flight readers.
    assert first.query([0.0, 1.0], {}, 1)[0].fragment_id == "two"
    fresh = ChromaVectorStore(str(tmp_path))
    assert fresh.query([1.0, 0.0], {}, 1)[0].fragment_id == "three"


def test_failed_stale_rebuild_preserves_active_collection_and_pointer(tmp_path, monkeypatch):
    first = ChromaVectorStore(str(tmp_path))
    first.add("one", [1.0, 0.0], {"course_id": "c"})
    stale = ChromaVectorStore(str(tmp_path))
    first.rebuild([("two", [0.0, 1.0], {"course_id": "c"})])

    def fail_create(*args, **kwargs):
        raise RuntimeError("synthetic create failure")

    monkeypatch.setattr(stale._client, "create_collection", fail_create)
    with pytest.raises(RuntimeError, match="synthetic create failure"):
        stale.rebuild([("three", [1.0, 0.0], {"course_id": "c"})])
    fresh = ChromaVectorStore(str(tmp_path))
    assert fresh.get_index_version() == "2"
    assert fresh.query([0.0, 1.0], {}, 1)[0].fragment_id == "two"
