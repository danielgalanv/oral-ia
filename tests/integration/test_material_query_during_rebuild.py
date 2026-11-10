"""US7 integration test: a query executed during an in-progress rebuild is served
against the last complete index version — never a partially-rebuilt one (Edge Case,
research.md §9).

Simulates the "in-progress" window deterministically: the new collection is populated
exactly as ``ChromaVectorStore.rebuild()`` would, but the version pointer is not yet
flipped — mirroring the exact state the store is in mid-rebuild, without needing real
thread interleaving.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from pathlib import Path
from types import MethodType

import pytest
from chromadb.errors import NotFoundError
from sqlalchemy.orm import sessionmaker

from oralia.application.commands import ingest_material as ingest_module
from oralia.application.commands import rebuild_material_index as rebuild_module
from oralia.application.commands.ingest_material import process_material
from oralia.application.commands.rebuild_material_index import rebuild_material_index
from oralia.infrastructure.db import models
from oralia.infrastructure.vector_store import chroma_store
from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore

_SAFETY_TIMEOUT_S = 5.0


def _collection_names(store: ChromaVectorStore) -> set[str]:
    return {collection.name for collection in store._client.list_collections()}


def test_query_mid_rebuild_sees_old_collection_until_the_swap_completes(tmp_path: Path):
    path = str(tmp_path / "vector_store")
    store = ChromaVectorStore(path)
    store.add("old-1", [1.0, 0.0, 0.0], {"course_id": "c1"})
    assert store.get_index_version() == "1"

    before = store.query([1.0, 0.0, 0.0], {"course_id": "c1"}, 5)
    assert [m.fragment_id for m in before] == ["old-1"]

    # Simulate a rebuild that has populated the new collection but not yet swapped the
    # version pointer — reads through a *fresh* store instance (as every request does)
    # must still resolve to the old, complete collection.
    new_collection = store._client.create_collection(
        "material_fragments_v2", metadata={"hnsw:space": "cosine"}
    )
    new_collection.upsert(ids=["new-1"], embeddings=[[0.0, 1.0, 0.0]], metadatas=[{"course_id": "c1"}])

    mid_rebuild_store = ChromaVectorStore(path)
    mid_results = mid_rebuild_store.query([1.0, 0.0, 0.0], {"course_id": "c1"}, 5)
    assert [m.fragment_id for m in mid_results] == ["old-1"]
    assert mid_rebuild_store.get_index_version() == "1"

    # Now complete the swap (what rebuild() does after populating): flip the version
    # pointer. A subsequent fresh store instance must see the new collection.
    (Path(path) / "index_version.json").write_text('{"version": 2}')
    after_swap_store = ChromaVectorStore(path)
    assert after_swap_store.get_index_version() == "2"
    after_results = after_swap_store.query([0.0, 1.0, 0.0], {"course_id": "c1"}, 5)
    assert [m.fragment_id for m in after_results] == ["new-1"]


def test_rebuild_retains_current_and_previous_then_retires_n_minus_2(tmp_path: Path):
    path = str(tmp_path / "vector_store")
    first = ChromaVectorStore(path)
    first.add("v1", [1.0, 0.0, 0.0], {"course_id": "c1"})

    assert first.rebuild([("v2", [0.0, 1.0, 0.0], {"course_id": "c1"})]) == "2"
    assert _collection_names(first) == {"material_fragments_v1", "material_fragments_v2"}

    second = ChromaVectorStore(path)
    assert second.rebuild([("v3", [0.0, 0.0, 1.0], {"course_id": "c1"})]) == "3"
    assert _collection_names(second) == {"material_fragments_v2", "material_fragments_v3"}


def test_rebuild_swaps_version_pointer_with_same_directory_temporary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = ChromaVectorStore(str(tmp_path / "vector_store"))
    store.add("v1", [1.0, 0.0, 0.0], {"course_id": "c1"})
    swaps: list[tuple[Path, Path, dict]] = []
    real_replace = chroma_store.os.replace

    def observed_replace(source, destination) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        assert source_path.exists()
        assert source_path.parent == destination_path.parent
        swaps.append(
            (
                source_path,
                destination_path,
                json.loads(source_path.read_text(encoding="utf-8")),
            )
        )
        real_replace(source, destination)

    monkeypatch.setattr(chroma_store.os, "replace", observed_replace)

    store.rebuild([("v2", [0.0, 1.0, 0.0], {"course_id": "c1"})])

    assert len(swaps) == 1
    temporary_path, destination_path, payload = swaps[0]
    assert destination_path.name == "index_version.json"
    assert payload == {"version": 2}
    assert not temporary_path.exists()
    assert json.loads(destination_path.read_text(encoding="utf-8")) == {"version": 2}


def test_query_reloads_pointer_retries_and_reports_version_actually_read(tmp_path: Path) -> None:
    path = str(tmp_path / "vector_store")
    writer = ChromaVectorStore(path)
    writer.add("v1", [1.0, 0.0, 0.0], {"course_id": "c1"})
    reader = ChromaVectorStore(path)
    writer.rebuild([("v2", [0.0, 1.0, 0.0], {"course_id": "c1"})])
    original_collection = reader._collection
    calls = 0

    def missing_then_current(self_store: ChromaVectorStore):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise NotFoundError("resolved collection does not exist")
        return original_collection()

    reader._collection = MethodType(missing_then_current, reader)

    results = reader.query([0.0, 1.0, 0.0], {"course_id": "c1"}, 5)

    assert [match.fragment_id for match in results] == ["v2"]
    assert reader.get_index_version() == "2"
    assert calls == 2


def test_query_not_found_retry_is_bounded_and_event_coordinated(tmp_path: Path) -> None:
    store = ChromaVectorStore(str(tmp_path / "vector_store"))
    entered = [threading.Event(), threading.Event()]
    proceed = [threading.Event(), threading.Event()]
    calls = 0
    captured: list[BaseException] = []

    def always_missing(self_store: ChromaVectorStore):
        nonlocal calls
        attempt = calls
        calls += 1
        assert attempt < 2, "query exceeded its fixed two-attempt budget"
        entered[attempt].set()
        if not proceed[attempt].wait(_SAFETY_TIMEOUT_S):
            raise TimeoutError("test failed to release bounded query attempt")
        raise NotFoundError(f"missing attempt {attempt + 1}")

    store._collection = MethodType(always_missing, store)

    def run_query() -> None:
        try:
            store.query([1.0, 0.0, 0.0], {"course_id": "c1"}, 5)
        except BaseException as exc:  # noqa: BLE001 - the thread reports its exact terminal result
            captured.append(exc)

    thread = threading.Thread(target=run_query)
    try:
        thread.start()
        assert entered[0].wait(_SAFETY_TIMEOUT_S)
        proceed[0].set()
        assert entered[1].wait(_SAFETY_TIMEOUT_S)
        proceed[1].set()
        thread.join(_SAFETY_TIMEOUT_S)
    finally:
        for event in proceed:
            event.set()
        thread.join(_SAFETY_TIMEOUT_S)

    assert not thread.is_alive()
    assert calls == 2
    assert len(captured) == 1
    assert isinstance(captured[0], NotFoundError)


@dataclass
class _EmbeddingStub:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0, 0.0] for _ in texts]


class _RebuildStoreStub:
    def __init__(self, entered: threading.Event, proceed: threading.Event) -> None:
        self._entered = entered
        self._proceed = proceed

    def rebuild(self, items) -> str:
        self._entered.set()
        if not self._proceed.wait(_SAFETY_TIMEOUT_S):
            raise TimeoutError("test failed to release rebuild")
        return "2"


class _IngestStoreStub:
    def __init__(self, added: threading.Event) -> None:
        self._added = added

    def add(self, fragment_id, embedding, metadata) -> None:
        self._added.set()


def test_ingest_add_waits_for_the_same_rebuild_lock(
    db_engine,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session_factory = sessionmaker(bind=db_engine, expire_on_commit=False)
    setup_db = session_factory()
    course = models.Course(name="Lock course", subject_code="LOCK101")
    setup_db.add(course)
    setup_db.flush()
    document = models.MaterialDocument(
        family_id="lock-family",
        version=1,
        course_id=course.id,
        activity_configuration_ids=[],
        filename="locked.txt",
        content_hash="0" * 64,
        mime_type="text/plain",
        size_bytes=40,
        status="pending",
    )
    setup_db.add(document)
    setup_db.commit()
    document_id = document.id
    setup_db.close()

    shared_lock = threading.Lock()
    acquire_count_lock = threading.Lock()
    acquire_count = 0
    ingest_waiting = threading.Event()

    def acquire(_db):
        nonlocal acquire_count
        with acquire_count_lock:
            acquire_count += 1
            ordinal = acquire_count
        if ordinal == 2:
            ingest_waiting.set()
        shared_lock.acquire()
        return object()

    def release(_db, _token) -> None:
        shared_lock.release()

    monkeypatch.setattr(rebuild_module.index_rebuild_lock_service, "acquire", acquire)
    monkeypatch.setattr(rebuild_module.index_rebuild_lock_service, "release", release)
    assert ingest_module.index_rebuild_lock_service is rebuild_module.index_rebuild_lock_service

    rebuild_entered = threading.Event()
    allow_rebuild_finish = threading.Event()
    ingest_added = threading.Event()
    failures: list[BaseException] = []

    def run_rebuild() -> None:
        db = session_factory()
        try:
            rebuild_material_index(
                db,
                vector_store=_RebuildStoreStub(rebuild_entered, allow_rebuild_finish),
                embedding_adapter=_EmbeddingStub(),
            )
        except BaseException as exc:  # noqa: BLE001 - report failures to the parent thread
            failures.append(exc)
        finally:
            db.close()

    def run_ingest() -> None:
        db = session_factory()
        try:
            process_material(
                db,
                db.get(models.MaterialDocument, document_id),
                b"Material with enough readable content for indexing.",
                vector_store=_IngestStoreStub(ingest_added),
                embedding_adapter=_EmbeddingStub(),
            )
        except BaseException as exc:  # noqa: BLE001 - report failures to the parent thread
            failures.append(exc)
        finally:
            db.close()

    rebuild_thread = threading.Thread(target=run_rebuild)
    ingest_thread = threading.Thread(target=run_ingest)
    try:
        rebuild_thread.start()
        assert rebuild_entered.wait(_SAFETY_TIMEOUT_S)
        ingest_thread.start()
        assert ingest_waiting.wait(_SAFETY_TIMEOUT_S)
        assert not ingest_added.is_set()
        allow_rebuild_finish.set()
        rebuild_thread.join(_SAFETY_TIMEOUT_S)
        ingest_thread.join(_SAFETY_TIMEOUT_S)
    finally:
        allow_rebuild_finish.set()
        rebuild_thread.join(_SAFETY_TIMEOUT_S)
        ingest_thread.join(_SAFETY_TIMEOUT_S)

    assert not rebuild_thread.is_alive()
    assert not ingest_thread.is_alive()
    assert failures == []
    assert ingest_added.is_set()
    assert acquire_count == 2
