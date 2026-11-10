"""T091 — baseline reproduction for T086 (H10, research.md §12), before any fix is
implemented. `MaterialRetrieverAgent` itself is NOT modified by this task — only its
input boundaries (`EmbeddingAdapter`/`VectorStore`) are controlled.

H10 (research.md §12) distinguishes two independent time mechanisms that MUST NOT be
confused with each other:

- `time_budget_ms` (`MaterialRetrieverAgent`'s own input, contracts/material-retriever-
  agent.md): a **soft**, self-checked budget — exhausting it MUST return
  `status = "ok"` with a partial result and a `warnings` entry, never a failure. This
  mechanism already works as documented and is NOT what is being reproduced here.
  Every reproduction below sets it far higher than any delay involved so it never has
  a chance to intervene (Deliverable 6 below).
- `request.deadline_ms` (Feature 001, `run_with_deadline`/`asyncio.wait_for`,
  `cancellation.py`): a **hard** limit meant to turn ANY agent exceeding it into
  `status = "timeout"` (`error.code = "AGENT_TIMEOUT"`) via `run_with_deadline`. This
  is the mechanism under test: `MaterialRetrieverAgent.execute` (and the whole call
  chain it drives — `_run_widening_search`) contains no `await` at all today, so once
  started it runs synchronously to completion regardless of `deadline_ms` —
  `asyncio.wait_for` can only ever observe the deadline at a suspension point, and
  there isn't one before T086 introduces it via `asyncio.to_thread`.

Two independent, deterministic reproductions against the REAL `MaterialRetrieverAgent`
and the REAL `run_with_deadline` (`oralia.application.orchestration.cancellation`):

- Reproduction A: a blocking `EmbeddingAdapter.embed` (the `VectorStore` double returns
  immediately and is never the source of the delay).
- Reproduction B: a blocking `VectorStore.query` (the `EmbeddingAdapter` double returns
  immediately).

Both MUST assert the CORRECT final behavior once T086 is implemented —
`status = "timeout"`, `error.code = "AGENT_TIMEOUT"`, `cancellation.is_cancelled()` —
never a restatement of today's bug as the expected outcome. Against the CURRENT code
both MUST fail (`status` comes back `"ok"` instead). The exact same assertions MUST
still hold, unchanged, once T086 is implemented — this file is not to be edited when
T086 lands, only re-run.

A positive contrast (same doubles, released comfortably before a generous
`deadline_ms`) proves the harness itself is not the reason for a timeout: it MUST
return `status = "ok"`, never `AGENT_TIMEOUT`, and MUST still enforce the T085/T098
authorization and relevance rules — an out-of-scope candidate returned by the store
double alongside the valid one MUST NOT leak into `fragments`.

Coordination is `threading.Event`-based (a background release thread), never a bare
`sleep` racing the test's own assertions — every blocking wait carries a safety
timeout so a broken double fails fast instead of hanging the suite, and every blocker
is released/joined in a `finally` block even if an assertion raises first. Elapsed
wall-clock time is recorded only as a secondary diagnostic (`SlowDouble.entered_at`/
`unblocked_at`); no assertion below depends on exact milliseconds.
"""

from __future__ import annotations

import threading
import time
import uuid

import pytest

from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent
from oralia.infrastructure.vector_store.chroma_store import VectorMatch

# `time_budget_ms` is deliberately far larger than any delay used below (the longest
# blocked call in these reproductions never exceeds a couple of seconds) — Deliverable
# 6: it MUST NOT be the mechanism that decides the outcome of any test in this file.
_UNREACHABLE_TIME_BUDGET_MS = 60_000
_BUDGET_EXHAUSTED_WARNING = "presupuesto temporal agotado, resultado parcial"

# Bounds how long a broken double is allowed to hang a test before failing loudly —
# never how long a *correct* double should take.
_SAFETY_TIMEOUT_S = 5.0


class _ReleaseThreadBlocker:
    """Deterministic, `threading.Event`-based block released by a background OS
    thread — never a `sleep` inside the blocked call itself, and never a race against
    the test's own assertions. `release_after_s` is measured from the moment the
    block actually starts (`entered` is set), not from construction, so the delay is
    exact relative to when the synchronous call begins. A safety timeout bounds the
    wait so a broken release thread cannot hang the suite; `close()` always joins the
    releaser thread and is safe to call more than once."""

    def __init__(self, *, release_after_s: float, safety_timeout_s: float = _SAFETY_TIMEOUT_S) -> None:
        self._entered = threading.Event()
        self._release = threading.Event()
        self._release_after_s = release_after_s
        self._safety_timeout_s = safety_timeout_s
        self.entered_at: float | None = None
        self.unblocked_at: float | None = None
        self._releaser = threading.Thread(target=self._run_releaser, daemon=True)
        self._releaser.start()

    def _run_releaser(self) -> None:
        if not self._entered.wait(self._safety_timeout_s):
            # The blocked call was never entered (e.g. a caller short-circuited
            # before reaching it) — release anyway so nothing can hang.
            self._release.set()
            return
        time.sleep(self._release_after_s)
        self._release.set()

    def block(self) -> None:
        """Call from inside the synchronous method under test."""
        self.entered_at = time.monotonic()
        self._entered.set()
        if not self._release.wait(self._safety_timeout_s):
            raise TimeoutError(
                "safety timeout exceeded waiting for the release event — this is a "
                "broken test double, not a real slow dependency"
            )
        self.unblocked_at = time.monotonic()

    def close(self) -> None:
        self._entered.set()  # unblock the releaser thread if `block()` was never called
        self._release.set()  # unblock a caller mid-`block()` if this runs from a finally
        self._releaser.join(self._safety_timeout_s)


class _BlockingEmbeddingAdapter:
    """Reproduction A: the delay is entirely inside `embed()`."""

    def __init__(self, blocker: _ReleaseThreadBlocker) -> None:
        self._blocker = blocker

    def embed(self, texts: list[str]) -> list[list[float]]:
        self._blocker.block()
        return [[0.0] for _ in texts]


class _ImmediateVectorStore:
    """Never blocks — proves the `VectorStore` is not the source of the delay in
    Reproduction A. `query_called` is a diagnostic only (whether it is ever reached
    differs between the current, fully-synchronous code — which reaches it regardless
    of the exceeded deadline — and the future T086 behavior — where cancellation may
    preempt `execute()` before this point); no assertion in this file depends on it."""

    def __init__(self) -> None:
        self.query_called = False

    def query(self, embedding, filters, k):  # noqa: ANN001 - matches VectorStore Protocol
        self.query_called = True
        return []

    def add(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def rebuild(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def get_index_version(self) -> str:
        return "test-version"


class _ImmediateEmbeddingAdapter:
    """Reproduction B: returns instantly — proves the delay is entirely inside
    `VectorStore.query`."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]


class _BlockingVectorStore:
    """Reproduction B: the delay is entirely inside `query()`."""

    def __init__(self, blocker: _ReleaseThreadBlocker, matches: list[VectorMatch] | None = None) -> None:
        self._blocker = blocker
        self._matches = matches or []
        self.query_called = False

    def query(self, embedding, filters, k):  # noqa: ANN001 - matches VectorStore Protocol
        self.query_called = True
        self._blocker.block()
        return self._matches

    def add(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def rebuild(self, *args, **kwargs):
        raise NotImplementedError("not used by this reproduction")

    def get_index_version(self) -> str:
        return "test-version"


def _request(*, deadline_ms: int, time_budget_ms: int = _UNREACHABLE_TIME_BUDGET_MS) -> AgentRequest:
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": "consulta de prueba H10",
            "course_id": None,
            "activity_configuration_id": None,
            "max_fragments": 5,
            "time_budget_ms": time_budget_ms,
        },
        deadline_ms=deadline_ms,
    )


def _assert_hard_timeout(result, *, token: CancellationToken) -> None:
    assert result.status == "timeout", (
        "H10/T086 (research.md §12): request.deadline_ms MUST preempt a blocking "
        "embed()/query() call via run_with_deadline once the blocking work is moved "
        "off the event loop (asyncio.to_thread) - got "
        f"status={result.status!r}, output={result.output!r}. Against the CURRENT "
        "code this is the expected failure: execute() has no internal `await`, so "
        "the whole synchronous call chain runs to completion before asyncio.wait_for "
        "ever gets a suspension point at which to observe the expired deadline."
    )
    assert result.error is not None and result.error.code == "AGENT_TIMEOUT", (
        f"expected error.code='AGENT_TIMEOUT', got {result.error!r}"
    )
    assert token.is_cancelled(), "run_with_deadline MUST cancel the token on a hard timeout"
    # Deliverable 6 — time_budget_ms (60s) never had a chance to intervene: the only
    # way `status` could be "ok" here is deadline_ms failing to preempt, never the
    # soft budget's own, differently-worded degradation path.
    if result.status == "ok":
        warnings = (result.output or {}).get("warnings", [])
        assert _BUDGET_EXHAUSTED_WARNING not in warnings, (
            "time_budget_ms must not be the reason this reproduction returned 'ok' - "
            f"got warnings={warnings!r}"
        )


@pytest.mark.failure
async def test_h10a_blocking_embedding_adapter_is_preempted_by_hard_deadline(db_session):
    """Reproduction A. `EmbeddingAdapter.embed` blocks deterministically for longer
    than `request.deadline_ms` (`VectorStore` is an `_ImmediateVectorStore` — never
    the cause of the delay). `time_budget_ms=60000` is far larger than the block and
    MUST NOT be what determines the outcome."""
    deadline_ms = 80
    blocker = _ReleaseThreadBlocker(release_after_s=(deadline_ms / 1000) + 0.4)
    store = _ImmediateVectorStore()
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=store,
        embedding_adapter=_BlockingEmbeddingAdapter(blocker),
    )
    token = CancellationToken()
    try:
        result = await run_with_deadline(agent, _request(deadline_ms=deadline_ms), token)
        _assert_hard_timeout(result, token=token)
    finally:
        blocker.close()
        # Diagnostic only (Deliverable 2 evidence) - not an assertion: how long the
        # embed() double actually blocked for, vs. the configured deadline_ms.
        if blocker.entered_at is not None and blocker.unblocked_at is not None:
            elapsed_ms = (blocker.unblocked_at - blocker.entered_at) * 1000
            print(f"[H10.A] embed() blocked for ~{elapsed_ms:.0f}ms, deadline_ms={deadline_ms}")


@pytest.mark.failure
async def test_h10b_blocking_vector_store_is_preempted_by_hard_deadline(db_session):
    """Reproduction B. `EmbeddingAdapter.embed` returns immediately; `VectorStore.query`
    blocks deterministically for longer than `request.deadline_ms`. Same
    `time_budget_ms=60000` ceiling and same final assertion as Reproduction A - the
    only boundary that moved is which double is slow."""
    deadline_ms = 80
    blocker = _ReleaseThreadBlocker(release_after_s=(deadline_ms / 1000) + 0.4)
    store = _BlockingVectorStore(blocker)
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=store,
        embedding_adapter=_ImmediateEmbeddingAdapter(),
    )
    token = CancellationToken()
    try:
        result = await run_with_deadline(agent, _request(deadline_ms=deadline_ms), token)
        _assert_hard_timeout(result, token=token)
    finally:
        blocker.close()
        if blocker.entered_at is not None and blocker.unblocked_at is not None:
            elapsed_ms = (blocker.unblocked_at - blocker.entered_at) * 1000
            print(f"[H10.B] query() blocked for ~{elapsed_ms:.0f}ms, deadline_ms={deadline_ms}")


def _make_course_and_document(db, *, activity_configuration_ids: list[str]):
    from oralia.infrastructure.db import models

    course = models.Course(name="Curso H10", subject_code="H10")
    db.add(course)
    db.flush()
    document = models.MaterialDocument(
        course_id=course.id,
        filename="h10.pdf",
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
    from oralia.infrastructure.db import models

    fragment = models.MaterialFragment(
        document_id=document.id,
        document_version=document.version,
        text=f"Fragmento H10 {uuid.uuid4().hex[:8]} sobre el tema del curso.",
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


@pytest.mark.failure
async def test_h10_positive_contrast_released_before_generous_deadline_completes_ok(db_session):
    """Positive contrast: identical doubles, but released well before a generous
    `deadline_ms` (5000ms vs. a ~50ms block) - `status` MUST be "ok", `AGENT_TIMEOUT`
    MUST NOT appear anywhere, and the T085 (relevance floor)/T098 (SQL course_id
    revalidation) rules MUST still hold: an out-of-scope candidate the store double
    also returns MUST NOT leak into `fragments` alongside the valid one."""
    course, document = _make_course_and_document(db_session, activity_configuration_ids=["act-1"])
    other_course, other_document = _make_course_and_document(
        db_session, activity_configuration_ids=["act-1"]
    )
    valid_fragment = _make_fragment(
        db_session, document=document, course_id=course.id, activity_configuration_ids=["act-1"]
    )
    out_of_scope_fragment = _make_fragment(
        db_session,
        document=other_document,
        course_id=other_course.id,
        activity_configuration_ids=["act-1"],
    )

    blocker = _ReleaseThreadBlocker(release_after_s=0.05)
    store = _BlockingVectorStore(
        blocker,
        matches=[
            VectorMatch(valid_fragment.id, {}, 0.75),
            VectorMatch(out_of_scope_fragment.id, {}, 0.74),
        ],
    )
    agent = MaterialRetrieverAgent(
        db_session, vector_store=store, embedding_adapter=_ImmediateEmbeddingAdapter()
    )
    token = CancellationToken()
    request = AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": "consulta de prueba H10 contraste positivo",
            "course_id": course.id,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": _UNREACHABLE_TIME_BUDGET_MS,
        },
        deadline_ms=5000,
    )
    try:
        result = await run_with_deadline(agent, request, token)
    finally:
        blocker.close()

    assert result.status == "ok", f"expected status='ok', got {result!r}"
    assert result.error is None
    assert not token.is_cancelled()
    returned_ids = [f["fragment_id"] for f in result.output["fragments"]]
    assert valid_fragment.id in returned_ids, f"valid, authorized fragment missing: {returned_ids!r}"
    assert out_of_scope_fragment.id not in returned_ids, (
        "T098 (research.md §14.1b): an out-of-scope course_id fragment MUST be "
        f"rejected by SQL revalidation even though the store double returned it: {returned_ids!r}"
    )
