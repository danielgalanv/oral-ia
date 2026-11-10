"""T091 — auxiliary, non-gating experiment for H10/T086 (research.md §12).

This file is deliberately SEPARATE from `test_material_retrieval_h10_reproduction.py`
(Deliverable 5, per this round's instruction): the two hard-timeout reproductions in
that other file (`test_h10a_...`/`test_h10b_...`) are the MANDATORY evidence gating
T086 — this file is additional, diagnostic evidence about event-loop responsiveness
specifically and is NOT required to be stable across both the current (pre-T086) and
future (post-T086) code, only documented.

What this proves today (and why it is deterministic, not a wall-clock race): while
`MaterialRetrieverAgent.execute` is inside its (currently synchronous, no internal
`await`) call to a blocking `EmbeddingAdapter.embed`, an independent, concurrently
scheduled coroutine cannot make ANY progress — not because it loses a timing race, but
because Python's asyncio event loop is single-threaded and cooperative: a task that
never suspends (no `await` inside it) monopolizes that thread for its entire
synchronous body. `asyncio.wait_for` wraps `agent.execute(...)` in its own inner Task
(`ensure_future`), so once that inner task starts its one and only step, nothing else
queued on the same loop — including a second task doing nothing but `await
asyncio.sleep(0)` then recording that it ran — can execute until the inner task's
step returns. This is enforced by the ready-queue processing order of a single
`_run_once` loop iteration (CPython `asyncio.base_events`), not by relative durations,
so the ordering recorded in `_events` below is expected to be stable regardless of how
long the block itself lasts.

Once T086 moves `embed`/`query` behind `asyncio.to_thread`, the inner task DOES gain a
genuine suspension point, and the second coroutine could in principle interleave while
the executor thread runs the blocking call in the background — but proving that
reliably introduces a real timing race (whether the second coroutine's `sleep(0)`
cycle happens to be scheduled before the background thread finishes), which is exactly
the kind of "not stable in both states" case this round's instructions call out.
T086's own follow-up work should decide whether/how to re-validate the post-fix side
of this experiment; only the pre-fix (current) side is asserted here.
"""

from __future__ import annotations

import asyncio
import threading
import time
import uuid

import pytest

from oralia.application.orchestration.cancellation import run_with_deadline
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.material_retriever_agent import MaterialRetrieverAgent

_SAFETY_TIMEOUT_S = 5.0


class _CoordinatedBlocker:
    """Same coordination shape as `_ReleaseThreadBlocker` in the sibling reproduction
    file (not imported from there - this file is intentionally self-contained per its
    own "documented separately" status): a background thread releases the block
    shortly after it starts, bounded by a safety timeout. The exact release delay is
    irrelevant to the ordering assertion below (see module docstring) - it only needs
    to be non-zero and finite."""

    def __init__(self, *, release_after_s: float = 0.05, safety_timeout_s: float = _SAFETY_TIMEOUT_S) -> None:
        self._entered = threading.Event()
        self._release = threading.Event()
        self._release_after_s = release_after_s
        self._safety_timeout_s = safety_timeout_s
        self._releaser = threading.Thread(target=self._run_releaser, daemon=True)
        self._releaser.start()

    def _run_releaser(self) -> None:
        if not self._entered.wait(self._safety_timeout_s):
            self._release.set()
            return
        time.sleep(self._release_after_s)
        self._release.set()

    def block(self) -> None:
        self._entered.set()
        if not self._release.wait(self._safety_timeout_s):
            raise TimeoutError("safety timeout exceeded — broken test double, not a real slow dependency")

    def close(self) -> None:
        self._entered.set()
        self._release.set()
        self._releaser.join(self._safety_timeout_s)


class _BlockingEmbeddingAdapter:
    def __init__(self, blocker: _CoordinatedBlocker, events: list[str]) -> None:
        self._blocker = blocker
        self._events = events

    def embed(self, texts: list[str]) -> list[list[float]]:
        self._blocker.block()
        self._events.append("blocking_retrieval_finished")
        return [[0.0] for _ in texts]


class _EmptyVectorStore:
    def query(self, embedding, filters, k):  # noqa: ANN001 - matches VectorStore Protocol
        return []

    def add(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def rebuild(self, *args, **kwargs):
        raise NotImplementedError

    def get_index_version(self) -> str:
        return "test-version"


def _request() -> AgentRequest:
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "query_text": "consulta de prueba H10 responsiveness",
            "max_fragments": 5,
            "time_budget_ms": 60_000,
        },
        # Generous on purpose: this experiment is about event-loop responsiveness
        # during the block, not about the hard-timeout path (that is the sibling
        # file's job) — deadline_ms MUST NOT fire here.
        deadline_ms=5_000,
    )


@pytest.mark.failure
async def test_h10_independent_coroutine_is_delayed_by_synchronous_embed(db_session):
    """Documented, non-gating experiment (see module docstring). Asserts the CORRECT
    eventual behavior an event-loop-friendly retrieval should have — an independent,
    brief coroutine scheduled while retrieval is blocking MUST be able to record its
    own progress before the blocking retrieval finishes - and shows it currently
    fails: against the CURRENT code, `blocking_retrieval_finished` is always recorded
    first, because the event loop's single thread is fully occupied by the
    synchronous `embed()` call for its entire duration."""
    events: list[str] = []
    blocker = _CoordinatedBlocker()
    agent = MaterialRetrieverAgent(
        db_session,
        vector_store=_EmptyVectorStore(),
        embedding_adapter=_BlockingEmbeddingAdapter(blocker, events),
    )
    token = CancellationToken()

    async def _independent_probe() -> None:
        # Two cooperative yields, not a sleep tied to any real duration — see module
        # docstring: the ordering is enforced by the event loop's cooperative
        # scheduling, not by how many cycles this does or how long anything sleeps.
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        events.append("independent_probe_progressed")

    try:
        retrieval_task = asyncio.create_task(run_with_deadline(agent, _request(), token))
        probe_task = asyncio.create_task(_independent_probe())
        result, _ = await asyncio.gather(retrieval_task, probe_task)
    finally:
        blocker.close()

    assert result.status == "ok", f"deadline_ms must not have fired in this experiment: {result!r}"
    assert events == ["independent_probe_progressed", "blocking_retrieval_finished"], (
        "H10 (research.md §12): once T086 moves embed()/query() off the event loop, "
        "an independent coroutine MUST be able to progress while retrieval is still "
        "blocking in its background thread. Against the CURRENT code this MUST fail "
        f"in the opposite order - got {events!r}: the synchronous embed() call "
        "monopolizes the event loop's single thread for its whole duration, so "
        "nothing else scheduled on that loop can run until it returns."
    )
