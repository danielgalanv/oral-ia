"""T092 — baseline reproduction for T087 (H09, research.md §13), before any fix is
implemented. `chroma_store.py` is NOT modified by this task.

The existing `tests/integration/test_material_query_during_rebuild.py` only fabricates
an intermediate on-disk state by hand (creates the new collection, upserts into it,
then checks a *fresh* store instance before and after manually flipping the version
pointer) — it never interleaves a real, in-flight `query()` call with a concurrent,
completing `rebuild()`. That test is re-run below, unmodified, as a regression
baseline; it is NOT a substitute for the coordinated reproductions this file adds.

The real race (H09): `ChromaVectorStore` caches `self._version` at construction and
never refreshes it. A reader instance resolves version N (cached since construction,
re-read again — but only from its own cached attribute — inside `query()`); a
`rebuild()` on a DIFFERENT instance completes in the meantime, moving the version
pointer to N+1 and (current, unfixed code) synchronously deleting N; the SAME reader
instance then continues its already-in-flight `query()` against the name it already
resolved. `_collection()` calls `self._client.get_or_create_collection(...)` — since
"get_or_create" recreates a deleted collection as empty rather than raising, the
reader silently gets `[]` back instead of either N's real content or a re-resolved
N+1.

Coordination is `threading.Event`-based, never `sleep`-based: a real `query()` call,
running on a background thread against the REAL `ChromaVectorStore`/real on-disk
Chroma storage in `tmp_path`, is paused via an instance-level override of
`ChromaVectorStore._collection` (installed on ONE instance only) that signals
"version already resolved" and then blocks until released — but always defers to the
UNMODIFIED, real `ChromaVectorStore._collection` once released, never a fake that
already simulates the expected result. Every wait carries a safety timeout; threads
are joined and events released in `finally`.
"""

from __future__ import annotations

import threading
from pathlib import Path

import chromadb
import pytest

from oralia.infrastructure.vector_store.chroma_store import ChromaVectorStore

_SAFETY_TIMEOUT_S = 5.0

# Captured once, before any per-instance override — this is what actually runs once
# a paused instance is released, so the reproduction exercises real, unmodified
# production logic, never a fake standing in for it.
_ORIGINAL_COLLECTION = ChromaVectorStore._collection


class _PausedCollectionAccess:
    """Pauses ONE `ChromaVectorStore` instance's next `_collection()` call exactly
    between "the version to use is already resolved" (`self._version`, fixed since
    construction, untouched by this pause) and "the underlying Chroma `Collection` is
    actually obtained" (`self._client.get_or_create_collection(...)`) — the precise
    window research.md §13 (H09) identifies as the real, unclosed race. Installed via
    an instance-level method override (never a class-wide monkeypatch, so other
    `ChromaVectorStore` instances in the same test are completely unaffected)."""

    def __init__(self, safety_timeout_s: float = _SAFETY_TIMEOUT_S) -> None:
        self.resolved = threading.Event()
        self.proceed = threading.Event()
        self._safety_timeout_s = safety_timeout_s

    def install(self, store: ChromaVectorStore) -> None:
        pause = self

        def _paused_collection(self_store: ChromaVectorStore):
            pause.resolved.set()
            if not pause.proceed.wait(pause._safety_timeout_s):
                raise TimeoutError(
                    "safety timeout exceeded waiting to be released - broken test coordination, "
                    "not a real slow dependency"
                )
            return _ORIGINAL_COLLECTION(self_store)

        store._collection = _paused_collection.__get__(store, ChromaVectorStore)

    def release(self) -> None:
        self.proceed.set()

    def close(self) -> None:
        # Unblocks a still-paused call even if an assertion above already failed,
        # so the background thread can always exit and be joined.
        self.resolved.set()
        self.proceed.set()


class _QueryRun:
    """Runs one `store.query(...)` call on a background thread, capturing its result
    OR any exception (never letting either escape unnoticed) — used to assert
    afterward, from the main thread, on exactly what the paused-then-released query
    actually observed."""

    def __init__(self) -> None:
        self.result: list | None = None
        self.exception: BaseException | None = None
        self._done = threading.Event()

    def run(self, store: ChromaVectorStore, embedding: list[float], filters: dict, k: int) -> None:
        try:
            self.result = store.query(embedding, filters, k)
        except BaseException as exc:  # noqa: BLE001 - capturing everything is the point of this reproduction
            self.exception = exc
        finally:
            self._done.set()

    def wait_done(self, timeout_s: float = _SAFETY_TIMEOUT_S) -> bool:
        return self._done.wait(timeout_s)


def _collection_names(store: ChromaVectorStore) -> set[str]:
    return {c.name for c in store._client.list_collections()}


@pytest.mark.integration
def test_A_reader_paused_mid_resolution_survives_one_concurrent_rebuild(tmp_path: Path):
    """Reproduction A. A reader resolves N=1, is paused exactly before obtaining the
    collection, a REAL `rebuild()` completes on a different instance (creates N+1,
    flips the pointer, and — current, unfixed code — retires N synchronously), then
    the reader is released and its already-in-flight `query()` continues.

    Every assertion below states the CORRECT required future behavior (research.md
    §13, T087's contract) — never a restatement of today's bug. Against the CURRENT
    code this MUST fail: `get_or_create_collection` silently recreates the deleted
    `material_fragments_v1` as empty, so `query()` returns `[]` instead of either N's
    real content or a re-resolved N+1."""
    path = str(tmp_path / "vector_store")
    writer = ChromaVectorStore(path)
    writer.add("frag-v1", [1.0, 0.0, 0.0], {"course_id": "c1"})
    assert writer.get_index_version() == "1"

    # A second instance, constructed while v1 is current, caches version=1 - exactly
    # the H09 scenario ("una instancia construida antes del rebuild()").
    reader = ChromaVectorStore(path)
    assert reader.get_index_version() == "1"

    pause = _PausedCollectionAccess()
    pause.install(reader)
    run = _QueryRun()
    thread = threading.Thread(target=run.run, args=(reader, [1.0, 0.0, 0.0], {"course_id": "c1"}, 5))
    try:
        thread.start()
        resolved = pause.resolved.wait(_SAFETY_TIMEOUT_S)
        assert resolved, "reader never reached the pause point - broken test setup"

        # A REAL rebuild(), on a different instance, runs to completion while the
        # reader is paused - this is the actual interleaving under test, not a
        # hand-fabricated intermediate state.
        rebuilder = ChromaVectorStore(path)
        rebuilder.rebuild([("frag-v2", [0.0, 1.0, 0.0], {"course_id": "c1"})])
        assert rebuilder.get_index_version() == "2"

        pause.release()
        assert run.wait_done(_SAFETY_TIMEOUT_S), "reader query never finished - broken test setup/hung"
    finally:
        pause.close()
        thread.join(_SAFETY_TIMEOUT_S)

    assert run.exception is None, (
        f"query() MUST NOT let an uncontrolled error escape during this interleaving - got {run.exception!r}"
    )
    results = run.result
    assert results is not None, "query() thread finished without setting a result or an exception"
    returned_ids = {m.fragment_id for m in results}
    reported_version = reader.get_index_version()

    assert results != [], (
        "H09/T087 (research.md §13): query() MUST NOT silently return [] because "
        "get_or_create_collection() recreated the retired version N as an empty "
        f"collection instead of either serving N or re-resolving to N+1 - got "
        f"{results!r} (reported_version={reported_version!r})"
    )
    assert returned_ids in ({"frag-v1"}, {"frag-v2"}), f"unexpected fragment set returned: {returned_ids!r}"
    if returned_ids == {"frag-v1"}:
        assert reported_version == "1", (
            f"reported index_version must match the generation actually read (N) - got {reported_version!r}"
        )
    else:
        assert reported_version == "2", (
            "reported index_version must match the generation actually read (N+1, "
            f"after re-resolving) - got {reported_version!r}"
        )

    # Never a silently recreated, empty N: if "material_fragments_v1" exists at all
    # on disk afterward, it MUST still hold its original content, never be empty
    # (empty would mean get_or_create_collection fabricated it from scratch).
    if "material_fragments_v1" in _collection_names(reader):
        v1 = reader._client.get_collection("material_fragments_v1")
        assert v1.count() > 0, (
            "material_fragments_v1 exists but is empty - it was silently recreated, not preserved"
        )


@pytest.mark.integration
def test_B_reader_paused_survives_two_concurrent_rebuilds_needs_retry(tmp_path: Path):
    """Reproduction B. Same pause point as A, but TWO real, consecutive `rebuild()`
    calls complete while the reader is paused (N=1 -> N+1=2 -> N+2=3) — N is now
    genuinely gone, two generations behind the newest, so retiring it is correct even
    under T087's future two-generation retention policy (research.md §13, point 1).
    The only correct outcome is a successful re-resolution to N+2 (T087's retry,
    point 2) — never a silent empty result, never an uncontrolled exception, and
    these assertions MUST NOT change once T087 implements that retry.

    Against the CURRENT code (no retry, no retention policy) this MUST fail: both N
    and N+1 are deleted synchronously by the two rebuilds, so the reader's paused
    resolution (still pointing at N) gets a freshly recreated, empty N back."""
    path = str(tmp_path / "vector_store")
    writer = ChromaVectorStore(path)
    writer.add("frag-v1", [1.0, 0.0, 0.0], {"course_id": "c1"})
    assert writer.get_index_version() == "1"

    reader = ChromaVectorStore(path)
    assert reader.get_index_version() == "1"

    pause = _PausedCollectionAccess()
    pause.install(reader)
    run = _QueryRun()
    thread = threading.Thread(target=run.run, args=(reader, [1.0, 0.0, 0.0], {"course_id": "c1"}, 5))
    try:
        thread.start()
        resolved = pause.resolved.wait(_SAFETY_TIMEOUT_S)
        assert resolved, "reader never reached the pause point - broken test setup"

        rebuilder_1 = ChromaVectorStore(path)
        rebuilder_1.rebuild([("frag-v2", [0.0, 1.0, 0.0], {"course_id": "c1"})])
        assert rebuilder_1.get_index_version() == "2"

        # A SECOND, independent instance re-reads the pointer (now 2) and rebuilds
        # again - two full, real, consecutive reconstructions, not a doubled call on
        # the same stale instance.
        rebuilder_2 = ChromaVectorStore(path)
        assert rebuilder_2.get_index_version() == "2"
        rebuilder_2.rebuild([("frag-v3", [0.0, 0.0, 1.0], {"course_id": "c1"})])
        assert rebuilder_2.get_index_version() == "3"

        pause.release()
        assert run.wait_done(_SAFETY_TIMEOUT_S), "reader query never finished - broken test setup/hung"
    finally:
        pause.close()
        thread.join(_SAFETY_TIMEOUT_S)

    assert run.exception is None, (
        f"query() MUST NOT let an uncontrolled error escape even once N is genuinely retired - "
        f"got {run.exception!r}"
    )
    results = run.result
    assert results is not None, "query() thread finished without setting a result or an exception"
    returned_ids = {m.fragment_id for m in results}
    reported_version = reader.get_index_version()

    assert returned_ids == {"frag-v3"}, (
        "H09/T087 (research.md §13): once N is genuinely retired (two rebuilds "
        "completed while this instance was paused), query() MUST re-resolve and "
        f"recover using the actually-current version (N+2) - got {returned_ids!r}, "
        f"results={results!r}, reported_version={reported_version!r}"
    )
    assert reported_version == "3", (
        f"reported index_version must be N+2 (the version actually read) - got {reported_version!r}"
    )

    if "material_fragments_v1" in _collection_names(reader):
        v1 = reader._client.get_collection("material_fragments_v1")
        assert v1.count() > 0, (
            "material_fragments_v1 exists but is empty - it was silently recreated, not preserved"
        )


def _observe(fn):
    """Captures either the return value or the exact exception a callable raises —
    never lets either escape unnoticed. Used only by the empirical probe below."""
    try:
        return {"kind": "value", "value": fn()}
    except BaseException as exc:  # noqa: BLE001 - capturing everything is the point
        return {
            "kind": "exception",
            "exception_type": f"{type(exc).__module__}.{type(exc).__name__}",
            "message": str(exc),
        }


def test_empirical_chroma_behavior_on_a_deleted_collection_object(tmp_path: Path):
    """Non-gating empirical measurement (research.md §13: "límite que sigue
    dependiendo de verificación empírica, no asumible") — NOT a T087 correctness
    gate, and intentionally does not pin to a specific exception type or message
    (chromadb-version-dependent): what does the INSTALLED chromadb actually do when
    `.count()`/`.query()` is called on a real `Collection` object whose underlying
    collection was deleted, by a DIFFERENT client instance, after the object was
    obtained? Captured and printed for research.md/tasks.md evidence, and to let
    T087 design its specific `except` clause around the REAL behavior instead of a
    blanket `except Exception`."""
    path = str(tmp_path / "vector_store")
    client_a = chromadb.PersistentClient(path=path)
    collection = client_a.create_collection("probe_v1", metadata={"hnsw:space": "cosine"})
    collection.upsert(ids=["a"], embeddings=[[1.0, 0.0, 0.0]], metadatas=[{"x": 1}])
    assert collection.count() == 1

    client_b = chromadb.PersistentClient(path=path)
    client_b.delete_collection("probe_v1")

    count_outcome = _observe(collection.count)
    query_outcome = _observe(lambda: collection.query(query_embeddings=[[1.0, 0.0, 0.0]], n_results=1))

    print(f"[T092 empirical] chromadb=={chromadb.__version__}")
    print(f"[T092 empirical] count() on a deleted-collection object -> {count_outcome!r}")
    print(f"[T092 empirical] query() on a deleted-collection object -> {query_outcome!r}")

    for label, outcome in (("count()", count_outcome), ("query()", query_outcome)):
        assert outcome["kind"] in ("exception", "value"), (
            f"{label}: no observable outcome was captured at all"
        )
        if outcome["kind"] == "exception":
            assert outcome["exception_type"], (
                f"{label}: an exception occurred but its type was not captured"
            )
