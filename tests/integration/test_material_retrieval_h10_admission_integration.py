"""T086 — agent-level integration tests: `MaterialRetrieverAgent` +
`BoundedBlockingWorker` + real `run_with_deadline`, going beyond the two T091
reproductions (which stay unmodified — see `test_material_retrieval_h10_reproduction.py`)
to cover late-worker-result discarding, no-SQL-in-a-worker-thread, and the widening
loop still issuing multiple `await`ed store queries within a single valid request.

Coordination is `threading.Event`-based (manual, caller-controlled release — never a
bare `sleep`); every blocking wait carries a safety timeout; blockers/workers are
always released and shut down in `finally`.
"""

from __future__ import annotations

import asyncio
import threading
import uuid

import pytest

from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent
from oralia.infrastructure.concurrency.blocking_retrieval_worker import BoundedBlockingWorker
from oralia.infrastructure.db import models
from oralia.infrastructure.vector_store.chroma_store import VectorMatch

_SAFETY_TIMEOUT_S = 5.0
_UNREACHABLE_TIME_BUDGET_MS = 60_000


class _ManualReleaseBlocker:
    """Same shape as the sibling worker unit tests' helper — a block the test
    releases explicitly, so the exact moment of release relative to other events
    (a timeout already having fired, an assertion already made) is under the test's
    control."""

    def __init__(self, safety_timeout_s: float = _SAFETY_TIMEOUT_S) -> None:
        self._entered = threading.Event()
        self._release = threading.Event()
        self._done = threading.Event()
        self._safety_timeout_s = safety_timeout_s

    def block(self):
        self._entered.set()
        if not self._release.wait(self._safety_timeout_s):
            raise TimeoutError("safety timeout exceeded - broken test double, not a real slow dependency")
        self._done.set()

    def wait_entered(self) -> bool:
        return self._entered.wait(self._safety_timeout_s)

    def wait_done(self) -> bool:
        return self._done.wait(self._safety_timeout_s)

    def release(self) -> None:
        self._release.set()

    def close(self) -> None:
        self._entered.set()
        self._release.set()


def _request(
    *, deadline_ms: int, course_id=None, activity_configuration_id=None, max_fragments: int = 5
) -> AgentRequest:
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": "consulta de prueba T086",
            "course_id": course_id,
            "activity_configuration_id": activity_configuration_id,
            "max_fragments": max_fragments,
            "time_budget_ms": _UNREACHABLE_TIME_BUDGET_MS,
        },
        deadline_ms=deadline_ms,
    )


@pytest.mark.integration
async def test_late_embed_completion_does_not_trigger_a_later_query(db_session):
    """Deliverable 7: if `embed()` finishes only AFTER the turn's deadline already
    expired, `query()` MUST NOT be started afterwards for that turn."""
    blocker = _ManualReleaseBlocker()

    class _BlockingEmbeddingAdapter:
        def embed(self, texts):
            blocker.block()
            return [[0.0] for _ in texts]

    class _RecordingVectorStore:
        def __init__(self):
            self.query_called = False

        def query(self, embedding, filters, k):
            self.query_called = True
            return []

        def add(self, *a, **kw):
            raise NotImplementedError

        def delete(self, *a, **kw):
            raise NotImplementedError

        def rebuild(self, *a, **kw):
            raise NotImplementedError

        def get_index_version(self):
            return "test-version"

    worker = BoundedBlockingWorker(capacity=2)
    store = _RecordingVectorStore()
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=store,
        embedding_adapter=_BlockingEmbeddingAdapter(),
        blocking_retrieval_worker=worker,
    )
    token = CancellationToken()
    try:
        result = await run_with_deadline(agent, _request(deadline_ms=60), token)
        assert result.status == "timeout"
        assert token.is_cancelled()

        # Only NOW let the late embed() actually finish, well after the timeout.
        blocker.release()
        assert blocker.wait_done(), "embed() double never actually finished - broken test setup"
        # Give the (already-cancelled) call chain every remaining opportunity to
        # misbehave and start query() anyway.
        for _ in range(5):
            await asyncio.sleep(0)
        assert store.query_called is False, "a late embed() completion MUST NOT trigger a later query()"
    finally:
        blocker.close()
        worker.shutdown(wait=True)


@pytest.mark.integration
async def test_late_query_completion_triggers_no_sql_conflicts_traces_or_late_results(db_session):
    """Deliverable 8: if `query()` finishes only AFTER the turn's deadline already
    expired, no SQL lookup, conflict detection/recording, trace write, or late result
    publication MUST happen for that turn."""
    blocker = _ManualReleaseBlocker()

    class _ImmediateEmbeddingAdapter:
        def embed(self, texts):
            return [[0.0] for _ in texts]

    class _BlockingVectorStore:
        def __init__(self):
            self.query_called = False

        def query(self, embedding, filters, k):
            self.query_called = True
            blocker.block()
            return []  # even the eventual return value must never reach any caller

        def add(self, *a, **kw):
            raise NotImplementedError

        def delete(self, *a, **kw):
            raise NotImplementedError

        def rebuild(self, *a, **kw):
            raise NotImplementedError

        def get_index_version(self):
            return "test-version"

    sql_calls_before = []
    original_query = db_session.query

    def _spy_query(*a, **kw):
        sql_calls_before.append(threading.get_ident())
        return original_query(*a, **kw)

    db_session.query = _spy_query

    worker = BoundedBlockingWorker(capacity=2)
    store = _BlockingVectorStore()
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=store,
        embedding_adapter=_ImmediateEmbeddingAdapter(),
        blocking_retrieval_worker=worker,
    )
    token = CancellationToken()
    try:
        result = await run_with_deadline(agent, _request(deadline_ms=60), token)
        assert result.status == "timeout"
        assert token.is_cancelled()
        sql_calls_at_timeout = list(sql_calls_before)

        blocker.release()
        assert blocker.wait_done(), "query() double never actually finished - broken test setup"
        for _ in range(5):
            await asyncio.sleep(0)

        assert store.query_called is True, "query() should have been reached before the deadline fired"
        late_sql_calls = sql_calls_before[len(sql_calls_at_timeout) :]
        assert sql_calls_before == sql_calls_at_timeout, (
            "no SQL access MUST occur as a delayed consequence of a query() that "
            f"finished after the turn's deadline - new calls: {late_sql_calls!r}"
        )
        assert db_session.query(models.MaterialConflictRecord).count() == 0
        assert db_session.query(models.TraceEvent).count() == 0
    finally:
        db_session.query = original_query
        blocker.close()
        worker.shutdown(wait=True)


def _make_course_and_document(db, *, activity_configuration_ids: list[str]):
    course = models.Course(name="Curso T086", subject_code="T086")
    db.add(course)
    db.flush()
    document = models.MaterialDocument(
        course_id=course.id,
        filename="t086.pdf",
        content_hash=uuid.uuid4().hex,
        mime_type="application/pdf",
        size_bytes=1,
        status="active",
        activity_configuration_ids=activity_configuration_ids,
    )
    db.add(document)
    db.flush()
    return course, document


def _make_fragment(db, *, document, course_id: str, activity_configuration_ids: list[str]):
    fragment = models.MaterialFragment(
        document_id=document.id,
        document_version=document.version,
        text=f"Fragmento T086 {uuid.uuid4().hex[:8]} sobre el tema del curso.",
        location_ref="p1",
        sequence_index=0,
        embedding_ref=uuid.uuid4().hex,
        course_id=course_id,
        activity_configuration_ids=activity_configuration_ids,
        indexing_status="indexed",
    )
    db.add(fragment)
    db.flush()
    return fragment


@pytest.mark.integration
async def test_sql_access_stays_on_the_event_loop_thread_never_the_worker(db_session):
    """Deliverable 9: `embed()`/`query()` run off the main thread (the worker pool),
    while every SQL access stays on the event-loop (main/test) thread — recorded via
    thread identities, never inferred."""
    main_thread_id = threading.get_ident()
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    fragment = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )

    embed_threads: list[int] = []
    query_threads: list[int] = []

    class _ThreadRecordingEmbeddingAdapter:
        def embed(self, texts):
            embed_threads.append(threading.get_ident())
            return [[0.0] for _ in texts]

    class _ThreadRecordingVectorStore:
        def query(self, embedding, filters, k):
            query_threads.append(threading.get_ident())
            return [VectorMatch(fragment.id, {}, 0.75)]

        def add(self, *a, **kw):
            raise NotImplementedError

        def delete(self, *a, **kw):
            raise NotImplementedError

        def rebuild(self, *a, **kw):
            raise NotImplementedError

        def get_index_version(self):
            return "test-version"

    sql_threads: list[int] = []
    original_query = db_session.query

    def _spy_query(*a, **kw):
        sql_threads.append(threading.get_ident())
        return original_query(*a, **kw)

    db_session.query = _spy_query

    worker = BoundedBlockingWorker(capacity=2)
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=_ThreadRecordingVectorStore(),
        embedding_adapter=_ThreadRecordingEmbeddingAdapter(),
        blocking_retrieval_worker=worker,
    )
    token = CancellationToken()
    try:
        result = await run_with_deadline(
            agent,
            _request(deadline_ms=5000, course_id=course.id, activity_configuration_id="act-1"),
            token,
        )
    finally:
        db_session.query = original_query
        worker.shutdown(wait=True)

    assert result.status == "ok", f"unexpected non-ok result: {result!r}"
    assert not token.is_cancelled()
    assert embed_threads, "embed() was never called"
    assert query_threads, "query() was never called"
    assert all(t != main_thread_id for t in embed_threads), (
        f"embed() MUST run off the event-loop thread, got thread ids {embed_threads!r}"
    )
    assert all(t != main_thread_id for t in query_threads), (
        f"query() MUST run off the event-loop thread, got thread ids {query_threads!r}"
    )
    assert sql_threads, "expected at least one SQL query while fetching the fragment row"
    assert all(t == main_thread_id for t in sql_threads), (
        f"SQL access MUST stay on the event-loop thread, got thread ids {sql_threads!r}"
    )
    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert fragment.id in returned_ids


class _OrderedCandidateVectorStore:
    """Same shape as the T090/H08 reproduction's double (`test_material_retrieval_
    h08_reproduction.py`) — returns the first `k` items of a fixed, pre-ordered
    candidate list; records every `k` it was asked for so the test can confirm more
    than one round actually happened."""

    def __init__(self, candidates: list[VectorMatch]) -> None:
        self._candidates = candidates
        self.queried_k: list[int] = []

    def query(self, embedding, filters, k):
        self.queried_k.append(k)
        return self._candidates[: max(k, 0)]

    def add(self, *a, **kw):
        raise NotImplementedError

    def delete(self, *a, **kw):
        raise NotImplementedError

    def rebuild(self, *a, **kw):
        raise NotImplementedError

    def get_index_version(self):
        return "test-version"


@pytest.mark.integration
async def test_widening_loop_still_issues_multiple_awaited_store_queries(db_session):
    """Deliverable 11: T085's progressive widening algorithm still performs several
    rounds — each its own `await`ed `worker.run(store.query, ...)` call — within a
    single valid (non-timeout) request, and still recovers evidence ranked beyond the
    first round's window (same shape as H08.A, `test_material_retrieval_h08_
    reproduction.py`, just now exercised through the async loop introduced by T086)."""

    class _FixedEmbeddingAdapter:
        def embed(self, texts):
            return [[0.0] for _ in texts]

    course, wrong_activity_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-other"]
    )
    _, valid_document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    valid_document.course_id = course.id
    db_session.add(valid_document)
    db_session.flush()

    candidates: list[VectorMatch] = []
    for i in range(4):  # positions 1-4: wrong activity — excluded
        frag = _make_fragment(
            db_session,
            document=wrong_activity_document,
            course_id=course.id,
            activity_configuration_ids=["act-other"],
        )
        candidates.append(VectorMatch(frag.id, {}, 0.95 - i * 0.01))
    for i in range(4):  # positions 5-8: also excluded
        frag = _make_fragment(
            db_session,
            document=wrong_activity_document,
            course_id=course.id,
            activity_configuration_ids=["act-other"],
        )
        candidates.append(VectorMatch(frag.id, {}, 0.91 - i * 0.01))
    valid_fragment_ids: list[str] = []
    for i in range(3):  # positions 9-11: authorized — beyond the first round's k=8 window
        frag = _make_fragment(
            db_session, document=valid_document, course_id=course.id, activity_configuration_ids=["act-1"]
        )
        valid_fragment_ids.append(frag.id)
        candidates.append(VectorMatch(frag.id, {}, 0.80 - i * 0.01))

    worker = BoundedBlockingWorker(capacity=2)
    store = _OrderedCandidateVectorStore(candidates)
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=store,
        embedding_adapter=_FixedEmbeddingAdapter(),
        blocking_retrieval_worker=worker,
    )
    token = CancellationToken()
    try:
        result = await run_with_deadline(
            agent,
            _request(
                deadline_ms=5000, course_id=course.id, activity_configuration_id="act-1", max_fragments=2
            ),
            token,
        )
    finally:
        worker.shutdown(wait=True)

    assert result.status == "ok"
    assert len(store.queried_k) >= 2, (
        f"expected the widening loop to issue multiple awaited store.query() rounds, got {store.queried_k!r}"
    )
    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert returned_ids == valid_fragment_ids[:2]
