"""T100 — convergence fix for three structural admission bugs found in T086's
`BoundedBlockingWorker`/`_LoopScopedSemaphore` (research.md §12.2):

- R1: `_LoopScopedSemaphore.acquire()` rebuilt a FULL, fresh `asyncio.Semaphore`
  whenever it saw a different running event loop, with no check for whether the
  previous semaphore still had permits outstanding — two event loops in two
  different threads, sharing one `BoundedBlockingWorker`, could each get their own
  full `capacity`, multiplying the real limit and feeding the dedicated executor's
  own (otherwise-unused) internal queue.
- R2: `run()` called `self._executor.submit(func, *args)` right after acquiring a
  permit, with no handling for `submit()` itself raising — a failure (e.g. the
  executor already shut down) leaked the permit forever; a subsequent `run()` call
  would hang indefinitely waiting for admission nobody would ever release.
- R3: `default_blocking_retrieval_worker()`'s lazy singleton had no mutual exclusion
  — two threads racing into it for the first time could each construct and keep a
  reference to a DIFFERENT worker instance, splitting the shared capacity.

This file is intentionally separate from `test_blocking_retrieval_worker.py` (T086) —
that file's 6 tests are re-run unmodified as regression evidence (see tasks.md), never
edited here. All tests below are deterministic: coordination is `threading.Event`-based
(with a background release thread only where a real delay is genuinely needed) or
causal/structural (ordering enforced by the admission design itself, never a timing
race), with a bounded safety timeout on every wait so a broken double or a regression
fails fast instead of hanging the suite. Genuinely separate event loops (not just
separate `Task`s on the same loop) are created via `_LoopThread`, each running on its
own background OS thread, to exercise real cross-loop/cross-thread concurrency.
"""

from __future__ import annotations

import asyncio
import threading
from concurrent.futures import Future as ConcurrentFuture

import pytest

from oralia.infrastructure.concurrency import blocking_retrieval_worker as worker_module
from oralia.infrastructure.concurrency.blocking_retrieval_worker import (
    BoundedBlockingWorker,
    _ProcessWideAdmission,
    default_blocking_retrieval_worker,
)

_SAFETY_TIMEOUT_S = 5.0


class _LoopThread:
    """A genuinely separate `asyncio` event loop, running on its own dedicated
    background OS thread — used so the multi-loop tests below exercise real
    concurrent event loops in different threads, not just concurrent `Task`s on one
    shared loop (which the retired per-loop-semaphore design would never have
    exposed R1 against)."""

    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        self._started = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        assert self._started.wait(_SAFETY_TIMEOUT_S), "background loop thread never started"

    def _run(self) -> None:
        asyncio.set_event_loop(self.loop)
        self._started.set()
        self.loop.run_forever()

    def run_coroutine(self, coro) -> ConcurrentFuture:
        """Schedule `coro` on this loop from ANY thread; returns a
        `concurrent.futures.Future` for its result — safe to `.result(timeout=...)`
        from the calling (test) thread."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def close(self) -> None:
        if not self.loop.is_closed():
            self.loop.call_soon_threadsafe(self.loop.stop)
        self._thread.join(_SAFETY_TIMEOUT_S)
        if not self.loop.is_closed():
            self.loop.close()


class _ManualReleaseBlocker:
    """Same shape as the sibling T086 unit tests' helper — a block the test releases
    explicitly, so the exact moment of release relative to other events is under the
    test's control, never a guessed delay."""

    def __init__(self, safety_timeout_s: float = _SAFETY_TIMEOUT_S) -> None:
        self._entered = threading.Event()
        self._release = threading.Event()
        self._safety_timeout_s = safety_timeout_s

    def block(self, label: str = "done") -> str:
        self._entered.set()
        if not self._release.wait(self._safety_timeout_s):
            raise TimeoutError("safety timeout exceeded - broken test double, not a real slow dependency")
        return label

    def wait_entered(self) -> bool:
        return self._entered.wait(self._safety_timeout_s)

    def release(self) -> None:
        self._release.set()

    def close(self) -> None:
        self._entered.set()
        self._release.set()


def _off_loop_wait(event: threading.Event, timeout_s: float = _SAFETY_TIMEOUT_S) -> asyncio.Future[bool]:
    """Await a `threading.Event` without blocking the CALLING coroutine's own event
    loop — used whenever the loop must stay free to keep servicing other tasks (e.g.
    a separately-scheduled `Task`) while this coroutine waits for a real,
    independent OS-thread signal."""
    return asyncio.get_running_loop().run_in_executor(None, event.wait, timeout_s)


class _SubmitSpy:
    """Wraps `worker._executor.submit` to record every submission, in order, under a
    `threading.Lock`. This exists because the dedicated executor's own thread count
    always equals `capacity` by construction — so "did more than `capacity` operations
    actually run CONCURRENTLY" can never observe R1's real harm (over-admission just
    feeds the executor's own internal queue instead; the extra items still only ever
    run `capacity`-at-a-time, serialized by the real OS thread count, regardless of
    how many were wrongly admitted). Watching `submit()` itself — the moment
    admission, not execution, happens — is the only way to see the actual symptom
    research.md describes: a broken gate feeding a queue the design says is never
    used. `submitted_event(label)` gives an `Event`-based (never polled) way to wait,
    bounded, for one specific labelled call's submission."""

    def __init__(self, worker: BoundedBlockingWorker) -> None:
        self._lock = threading.Lock()
        self.events: list[tuple[str, str]] = []
        self._submitted_events: dict[str, threading.Event] = {}
        self._original_submit = worker._executor.submit
        worker._executor.submit = self._spy_submit  # type: ignore[method-assign]

    def _spy_submit(self, func, *args, **kwargs):
        label = getattr(func, "_label", "?")
        with self._lock:
            self.events.append((label, "submitted"))
            self._submitted_events.setdefault(label, threading.Event()).set()
        return self._original_submit(func, *args, **kwargs)

    def submitted_event(self, label: str) -> threading.Event:
        with self._lock:
            return self._submitted_events.setdefault(label, threading.Event())

    def submitted_count(self) -> int:
        with self._lock:
            return len(self.events)


# ---------------------------------------------------------------------------
# A + D: two event loops, two threads, share one worker with capacity=1 — loop B
# cannot be submitted while loop A's work is still holding the only permit, and
# once A finishes, loop B's still-open waiter receives the permit and completes.
# ---------------------------------------------------------------------------


@pytest.mark.integration
async def test_A_and_D_second_loop_blocked_until_first_loop_releases_then_completes():
    """Deliverables A + D. `submit()` is spied (see `_SubmitSpy`) because the
    executor's own thread count always equals `capacity`, so "did b_op's body
    actually run concurrently with a_op" can never observe over-admission when
    `capacity=1` — the only real symptom is `submit()` itself being called for B
    while A still holds the only permit. A short, bounded, `Event`-based fairness
    window (never a poll) confirms that did NOT happen; then A is released and B's
    eventual, correct admission/completion is confirmed (Deliverable D)."""
    worker = BoundedBlockingWorker(capacity=1)
    loop_b = _LoopThread()
    spy = _SubmitSpy(worker)
    b_submitted = spy.submitted_event("b")

    a_entered = threading.Event()
    a_release = threading.Event()

    def a_op():
        a_entered.set()
        a_release.wait(_SAFETY_TIMEOUT_S)
        return "a"

    a_op._label = "a"

    def b_op():
        return "b"

    b_op._label = "b"

    try:
        task_a = asyncio.create_task(worker.run(a_op))
        await asyncio.sleep(0)
        assert a_entered.wait(_SAFETY_TIMEOUT_S), "a never entered - broken test setup"

        fut_b = loop_b.run_coroutine(worker.run(b_op))

        submitted_early = await asyncio.get_event_loop().run_in_executor(None, b_submitted.wait, 0.3)
        assert not submitted_early, (
            "loop B (a different event loop, on a different thread) was submitted "
            "to the executor while loop A still held the only permit (capacity=1)"
        )

        a_release.set()
        result_a = await task_a
        assert result_a == "a"
        result_b = await asyncio.get_event_loop().run_in_executor(None, fut_b.result, _SAFETY_TIMEOUT_S)
        assert result_b == "b"
        assert b_submitted.is_set(), "loop B must be admitted and complete once A releases (Deliverable D)"
    finally:
        a_release.set()
        loop_b.close()
        worker.shutdown(wait=True)


# ---------------------------------------------------------------------------
# B: cancelling loop B's admission wait before A releases means B is never
# submitted later.
# ---------------------------------------------------------------------------


@pytest.mark.integration
async def test_B_cancelling_other_loops_waiter_before_release_never_submits_later():
    """Deliverable B. B's `worker.run(...)` call is started and cancelled AS A TASK
    ON LOOP B ITSELF (a `Task` can only be safely cancelled from its own loop's
    thread) while it should still be waiting for admission (A, capacity=1, has not
    released yet). `submit()` is spied (see `_SubmitSpy`): "did b_op's body run" is
    NOT decisive here on its own — even a wrongly early-submitted `b_op` still
    sitting in the executor's internal queue (not yet started) would be correctly
    prevented from running by the cancellation itself once it reaches the executor
    (`concurrent.futures.Future.cancel()` succeeds on a not-yet-started item). The
    real defect under test is whether `submit()` (i.e. admission) happened AT ALL
    while A still held the only permit — checked right at the moment of
    cancellation, before that masking effect can hide it."""
    worker = BoundedBlockingWorker(capacity=1)
    loop_b = _LoopThread()
    spy = _SubmitSpy(worker)
    b_submitted = spy.submitted_event("b")

    a_entered = threading.Event()
    a_release = threading.Event()

    def a_op():
        a_entered.set()
        a_release.wait(_SAFETY_TIMEOUT_S)
        return "a"

    def b_op():
        return "b"

    b_op._label = "b"

    async def _start_wait_and_cancel_on_b() -> str:
        task_b = asyncio.ensure_future(worker.run(b_op))
        await asyncio.sleep(0)  # let task_b reach (what SHOULD be) the admission wait
        task_b.cancel()
        try:
            await task_b
        except asyncio.CancelledError:
            pass
        return "cancelled"

    try:
        task_a = asyncio.create_task(worker.run(a_op))
        await asyncio.sleep(0)
        assert a_entered.wait(_SAFETY_TIMEOUT_S)

        cancel_fut = loop_b.run_coroutine(_start_wait_and_cancel_on_b())
        cancel_result = await asyncio.get_event_loop().run_in_executor(
            None, cancel_fut.result, _SAFETY_TIMEOUT_S
        )
        assert cancel_result == "cancelled"
        assert not b_submitted.is_set(), (
            "loop B must still be waiting for admission (never actually submitted) "
            "at the moment its own wait is cancelled, while loop A still holds the "
            "only permit (capacity=1)"
        )

        a_release.set()
        assert await task_a == "a"

        # Bounded, real-time, off-loop wait — NOT `sleep(0)` cooperative-yield
        # cycles — a fairness window confirming no late/queued submission surfaces
        # afterward either.
        submitted_anyway = await asyncio.get_event_loop().run_in_executor(None, b_submitted.wait, 0.3)
        assert not submitted_anyway, (
            "a waiter cancelled while waiting for admission must never be submitted later"
        )
    finally:
        a_release.set()
        loop_b.close()
        worker.shutdown(wait=True)


# ---------------------------------------------------------------------------
# C: repeating the scenario with several loops never exceeds capacity or grows the
# internal (otherwise-unbounded) executor queue.
# ---------------------------------------------------------------------------


@pytest.mark.integration
async def test_C_several_loops_never_exceed_capacity_structurally():
    """Deliverable C. Capacity=2, three event loops (this test's own loop A, plus
    loops B and C on their own threads) each submit a blocking op concurrently.
    Two assertions, deliberately at two different levels:

    - `max_concurrent` (via the running-op counter) stays at `capacity` — true
      either way, since the executor's own thread count IS `capacity`, so this
      alone would NOT catch over-admission (see `_SubmitSpy`'s docstring).
    - `spy.submitted_count()`, checked after a short, bounded, real-time fairness
      window (never the test's `await`able primary mechanism, just a generous
      allowance for a genuinely buggy gate to demonstrate itself), is the real
      test: it MUST also be exactly `capacity` — never `3` (one per loop), which is
      what a per-loop-rebuilding gate would allow and is exactly how it would feed
      the executor's own, otherwise-unused, internal queue."""
    capacity = 2
    worker = BoundedBlockingWorker(capacity=capacity)
    loop_b = _LoopThread()
    loop_c = _LoopThread()
    spy = _SubmitSpy(worker)
    lock = threading.Lock()
    concurrent_count = 0
    max_concurrent = 0
    capacity_reached = threading.Event()
    release_event = threading.Event()

    def make_op(label: str):
        def _op():
            nonlocal concurrent_count, max_concurrent
            with lock:
                concurrent_count += 1
                max_concurrent = max(max_concurrent, concurrent_count)
                if concurrent_count >= capacity:
                    capacity_reached.set()
            release_event.wait(_SAFETY_TIMEOUT_S)
            with lock:
                concurrent_count -= 1
            return label

        _op._label = label
        return _op

    try:
        task_a = asyncio.create_task(worker.run(make_op("a")))
        fut_b = loop_b.run_coroutine(worker.run(make_op("b")))
        fut_c = loop_c.run_coroutine(worker.run(make_op("c")))

        reached = await _off_loop_wait(capacity_reached)
        assert reached, "capacity was never reached - broken test setup"

        # Bounded, real-time fairness window: gives a genuinely buggy admission
        # gate every fair chance to also (wrongly) submit the third op before
        # anything is released.
        await asyncio.sleep(0.3)
        submitted = spy.submitted_count()
        assert submitted == capacity, (
            f"expected exactly {capacity} submissions admitted at once across 3 "
            f"loops, but {submitted} were submitted to the executor - {spy.events!r}"
        )

        release_event.set()
        await task_a
        await asyncio.get_event_loop().run_in_executor(None, fut_b.result, _SAFETY_TIMEOUT_S)
        await asyncio.get_event_loop().run_in_executor(None, fut_c.result, _SAFETY_TIMEOUT_S)
    finally:
        release_event.set()
        loop_b.close()
        loop_c.close()
        worker.shutdown(wait=True)

    assert max_concurrent == capacity


# ---------------------------------------------------------------------------
# E: a waiter whose loop has since closed is skipped, never losing the permit —
# tested directly against `_ProcessWideAdmission` (the admission primitive itself)
# for a precise, surgical reproduction of the loop-closed race.
# ---------------------------------------------------------------------------


def test_E_permit_skips_a_waiter_whose_loop_already_closed():
    """Deliverable E. Plain (non-async) test: all the async work happens on loops B
    and C, driven from this thread via `run_coroutine_threadsafe`. Loop A's single
    permit is consumed up front via a throwaway `asyncio.run()` call (this test
    exercises `_ProcessWideAdmission` directly, not through `BoundedBlockingWorker`,
    since the interesting behavior here is purely about admission bookkeeping
    across a loop closing — no actual blocking work needs to run)."""
    admission = _ProcessWideAdmission(capacity=1)
    loop_b = _LoopThread()
    loop_c = _LoopThread()

    try:
        asyncio.run(admission.acquire())  # consumes the only permit up front

        async def _register_b() -> None:
            asyncio.ensure_future(admission.acquire())  # abandoned on purpose below
            await asyncio.sleep(0)  # let it reach the waiting branch
            assert len(admission._waiters) == 1, "loop B's waiter never registered - broken test setup"

        loop_b.run_coroutine(_register_b()).result(_SAFETY_TIMEOUT_S)

        c_granted = threading.Event()

        async def _c_wait() -> None:
            await admission.acquire()
            c_granted.set()

        c_task_fut = loop_c.run_coroutine(_c_wait())

        # Close loop B WHILE its waiter is still queued — the scenario under test.
        loop_b.close()

        # Release the permit "loop A" held — it must skip B's now-dead waiter and
        # grant C's still-open one instead, never losing the permit.
        admission.release()

        assert c_granted.wait(_SAFETY_TIMEOUT_S), "the permit was never handed to loop C's still-open waiter"
        c_task_fut.result(_SAFETY_TIMEOUT_S)
    finally:
        loop_c.close()


# ---------------------------------------------------------------------------
# F: a submit() failure never leaks the permit; a shut-down worker fails every
# call immediately and coherently.
# ---------------------------------------------------------------------------


@pytest.mark.integration
async def test_F1_submit_failure_returns_the_permit_immediately():
    """Deliverable F, part 1 (R2's exact reproduction, isolated from `shutdown()`'s
    own fast path): the underlying executor is shut down directly — bypassing
    `BoundedBlockingWorker.shutdown()` — so `run()`'s admission-closed check stays
    open and the failure is forced to come from `submit()` itself, exactly the path
    `run()`'s `except Exception: self._admission.release(); raise` exists for."""
    worker = BoundedBlockingWorker(capacity=1)
    worker._executor.shutdown(wait=True)

    with pytest.raises(RuntimeError):
        await worker.run(lambda: "unreachable")

    # Structural proof of no leak: if the permit above had leaked, this would hang
    # and `wait_for` would raise `TimeoutError` instead.
    await asyncio.wait_for(worker._admission.acquire(), timeout=_SAFETY_TIMEOUT_S)


@pytest.mark.integration
async def test_F2_shutdown_makes_every_subsequent_call_fail_immediately():
    """Deliverable F, part 2 — the exact reproduction steps given for R2: create a
    `capacity=1` worker, shut it down, then confirm a SECOND `run()` call fails
    immediately too (never hangs waiting for a permit the first call leaked)."""
    worker = BoundedBlockingWorker(capacity=1)
    worker.shutdown(wait=True)

    with pytest.raises(RuntimeError):
        await worker.run(lambda: "unreachable")
    with pytest.raises(RuntimeError):
        await asyncio.wait_for(worker.run(lambda: "unreachable"), timeout=_SAFETY_TIMEOUT_S)


# ---------------------------------------------------------------------------
# G: shutdown() is idempotent.
# ---------------------------------------------------------------------------


def test_G_shutdown_is_idempotent():
    """Deliverable G."""
    worker = BoundedBlockingWorker(capacity=2)
    worker.shutdown(wait=True)
    worker.shutdown(wait=True)
    worker.shutdown(wait=False)  # any combination afterward must stay safe


# ---------------------------------------------------------------------------
# H: the process-wide default singleton is thread-safe.
# ---------------------------------------------------------------------------


def test_H_default_worker_singleton_is_thread_safe():
    """Deliverable H (R3). Resets the module-level singleton to force the race
    (restored in `finally`); a `threading.Barrier` maximizes how many threads hit
    the construction race at the same instant."""
    original_worker = worker_module._default_worker
    worker_module._default_worker = None
    n_threads = 8
    barrier = threading.Barrier(n_threads, timeout=_SAFETY_TIMEOUT_S)
    results: list[BoundedBlockingWorker] = []
    results_lock = threading.Lock()

    def _get() -> None:
        barrier.wait()
        instance = default_blocking_retrieval_worker()
        with results_lock:
            results.append(instance)

    threads = [threading.Thread(target=_get) for _ in range(n_threads)]
    try:
        for t in threads:
            t.start()
        for t in threads:
            t.join(_SAFETY_TIMEOUT_S)
        assert len(results) == n_threads
        assert all(r is results[0] for r in results), (
            "concurrent first-use construction produced more than one singleton instance"
        )
    finally:
        worker_module._default_worker = original_worker
