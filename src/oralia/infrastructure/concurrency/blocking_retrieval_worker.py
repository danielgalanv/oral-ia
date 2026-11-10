"""Process-wide, capacity-bounded worker for `MaterialRetrieverAgent`'s blocking
`EmbeddingAdapter.embed`/`VectorStore.query` calls (T086, research.md §12/§12.1;
admission redesign T100, research.md §12.2).

Shared across every `MaterialRetrieverAgent` instance — production constructs a new
agent per request (`materials.py`, `self_study_agency_composer.py`), so a private
per-agent semaphore would bound nothing across concurrent requests. This is
deliberately NOT `asyncio.to_thread` (which dispatches to the event loop's default
executor): research.md §12 (corrected in T091) documents that the default
`ThreadPoolExecutor`'s bounded worker count does not bound its own pending-work
queue, so `asyncio.to_thread` alone gives no real backpressure against a sustained
burst. `BoundedBlockingWorker` instead gates admission itself, BEFORE submission, so
its own dedicated executor's internal queue is never relied upon to bound anything.

T100 (research.md §12.2) replaces the first round's per-event-loop semaphore
(`_LoopScopedSemaphore`, retired — it rebuilt a FULL, fresh semaphore whenever a
different running loop showed up, silently multiplying capacity across concurrently
live loops in different threads) with `_ProcessWideAdmission`: ONE shared pool of
permits, protected by a single `threading.Lock`, with waiters tracked individually
(each tied to its own loop) rather than pooled per loop — see that class's docstring
for the concurrency invariants and the specific races it resolves.
"""

from __future__ import annotations

import asyncio
import threading
from collections import deque
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import TypeVar

_T = TypeVar("_T")

# Deliberately conservative, NOT derived from any measured cost — T090 (research.md
# §14.2) measured `relevance_score` distributions only, never latency, CPU or memory;
# no such measurement exists for this agent. This is a safe internal ceiling chosen to
# exist at all (Principio IX: explicit resource limits), not a tuned value — it MUST
# be revisited against real deployment metrics (concurrent request volume, actual
# embed()/query() latency under the real model/store) before being treated as final.
DEFAULT_BLOCKING_RETRIEVAL_CAPACITY = 4


@dataclass
class _Waiter:
    """One pending `acquire()` call. `consumed` is mutated ONLY while holding the
    owning `_ProcessWideAdmission._lock` — by either side of the handoff race
    (the releaser marking it granted, or the waiter's own cancellation handler
    discovering it was granted after all) — never read or written outside that
    lock, so the two sides can never disagree about who owns the permit."""

    loop: asyncio.AbstractEventLoop
    fut: asyncio.Future
    consumed: bool = False


def _resolve_waiter(waiter: _Waiter) -> None:
    """Runs on `waiter.loop`'s own thread (scheduled via `call_soon_threadsafe` from
    `_ProcessWideAdmission._grant_next_locked`). The future may already be done
    (cancelled) if the awaiting task's own cancellation raced ahead of this callback
    on the same loop — in that case this is a no-op: `acquire()`'s own
    `except CancelledError` handler (guarded by the same lock, via `waiter.consumed`)
    is responsible for returning the stranded permit to the pool instead."""
    if not waiter.fut.done():
        waiter.fut.set_result(None)


def _reject_waiter(waiter: _Waiter, exc: BaseException) -> None:
    """Best-effort: used only by `shutdown()` to fail waiters still pending at that
    moment. Silently gives up if the waiter's own loop is already closed — nothing
    left that could ever observe the rejection anyway."""

    def _do_reject() -> None:
        if not waiter.fut.done():
            waiter.fut.set_exception(exc)

    try:
        waiter.loop.call_soon_threadsafe(_do_reject)
    except RuntimeError:
        pass


class _ProcessWideAdmission:
    """A single, cross-event-loop-safe pool of `capacity` permits — never rebuilt or
    rebound per event loop (T100/R1: the retired `_LoopScopedSemaphore` did exactly
    that, silently granting a FULL fresh set of permits to every new event loop it
    saw, even while an older loop's admitted work was still outstanding). All
    bookkeeping (`_available`, `_waiters`, `_closed`) lives behind one
    `threading.Lock`, held only for brief, non-blocking bookkeeping — never across an
    `await` or a blocking wait (so it never blocks the event loop: the actual WAIT for
    a permit is always `await fut`, a plain cooperative `asyncio.Future`, never
    `threading.Semaphore.acquire()`).

    Invariant: at any instant, every one of the `capacity` permits is in exactly one
    of three states — free (counted in `_available`), held by admitted work (tracked
    by the caller of `acquire()`, released via `release()`), or in transit to a
    specific waiter (`waiter.consumed = True`, between `_grant_next_locked` handing
    it off and that waiter's `acquire()` either returning normally or discovering,
    under the lock, that it must hand the permit onward instead). No code path
    outside `_grant_next_locked`/`acquire`'s cancellation handler ever creates or
    destroys a permit, so the total is conserved by construction.

    Handles three races around handing a freed permit to the next waiter, all
    resolved under `_lock` so at most one side ever "wins":
    - the waiter's own task is cancelled around the same time a permit is handed to
      it (`acquire`'s `except CancelledError` checks `waiter.consumed` and returns
      the permit via `_grant_next_locked` again if a releaser had already granted it);
    - the waiter's event loop has since closed (`_grant_next_locked` skips it —
      `call_soon_threadsafe` raises `RuntimeError` on a closed loop — and tries the
      next waiter, never losing the permit);
    - a release fires concurrently from a worker thread (`release()` is plain
      thread-safe code, callable from any thread with no special marshalling needed
      at that outer level — only the final per-waiter wakeup is marshalled, via
      `call_soon_threadsafe`, onto that specific waiter's own loop)."""

    def __init__(self, capacity: int) -> None:
        self._lock = threading.Lock()
        self._available = capacity
        self._waiters: deque[_Waiter] = deque()
        self._closed = False

    async def acquire(self) -> None:
        """Cancelable, non-blocking-to-the-event-loop: either returns immediately (a
        free permit was available) or awaits a plain `asyncio.Future` created on the
        CALLER's own running loop — no polling, no `threading.Semaphore.acquire()`.
        Raises `RuntimeError` immediately, without ever touching `_available` or
        `_waiters`, once `close()` has been called."""
        loop = asyncio.get_running_loop()
        with self._lock:
            if self._closed:
                raise RuntimeError("admission is closed — the worker was shut down")
            if self._available > 0:
                self._available -= 1
                return
            fut: asyncio.Future = loop.create_future()
            waiter = _Waiter(loop=loop, fut=fut)
            self._waiters.append(waiter)
        try:
            await fut
        except asyncio.CancelledError:
            with self._lock:
                if waiter.consumed:
                    # A releaser already handed (or was in the middle of handing)
                    # this waiter a permit — it was never actually used, so it MUST
                    # go back to the pool rather than being silently lost.
                    self._grant_next_locked()
                else:
                    # Not granted yet — a concurrent release() may already have
                    # popped us from the queue in the instant before this branch
                    # runs (in which case `consumed` would be True and we would not
                    # be here) — `remove` on a deque already missing the item is
                    # guarded defensively regardless.
                    try:
                        self._waiters.remove(waiter)
                    except ValueError:
                        pass
            raise

    def release(self) -> None:
        """Thread-safe and non-blocking: safe to call directly from the event-loop
        thread (a `submit()` failure) or from a worker thread (a
        `concurrent.futures.Future` done-callback) alike — no `call_soon_threadsafe`
        needed at this outer level, only inside `_grant_next_locked` for the specific
        waiter being woken."""
        with self._lock:
            self._grant_next_locked()

    def _grant_next_locked(self) -> None:
        """Caller MUST hold `self._lock`. Hands the just-freed permit to the next
        waiter whose loop is still open, skipping — never losing the permit for —
        any waiter whose loop already closed; returns it to `_available` if no
        waiter remains."""
        while self._waiters:
            waiter = self._waiters.popleft()
            waiter.consumed = True
            try:
                waiter.loop.call_soon_threadsafe(_resolve_waiter, waiter)
            except RuntimeError:
                # That waiter's loop is already closed — the permit was never
                # actually delivered; undo and try the next waiter instead.
                waiter.consumed = False
                continue
            return
        self._available += 1

    def close(self) -> list[_Waiter]:
        """Idempotent: marks admission closed and returns the waiters still pending
        at that moment (for the caller to reject) exactly once — a second call
        returns an empty list and changes nothing."""
        with self._lock:
            if self._closed:
                return []
            self._closed = True
            pending = list(self._waiters)
            self._waiters.clear()
            return pending


class BoundedBlockingWorker:
    """Runs a synchronous callable off the event loop thread, gated by an explicit,
    named capacity (T086/T100, research.md §12.1/§12.2) shared across every caller of
    this instance — and, per `_ProcessWideAdmission`, across every event loop that
    caller runs on, concurrently or in succession. Never creates a thread per call:
    `func` is submitted to a small, dedicated `ThreadPoolExecutor` sized to exactly
    `capacity` — combined with the admission gate checked before submission, this
    guarantees the executor's own (otherwise unbounded) pending-work queue is never
    actually used, since no more than `capacity` calls are ever in flight through
    this worker at once, from however many event loops are using it."""

    def __init__(self, capacity: int = DEFAULT_BLOCKING_RETRIEVAL_CAPACITY) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")
        self.capacity = capacity
        self._executor = ThreadPoolExecutor(max_workers=capacity, thread_name_prefix="material-retrieval")
        self._admission = _ProcessWideAdmission(capacity)

    async def run(self, func: Callable[..., _T], *args: object) -> _T:
        """Await admission (cancelable — a caller whose own deadline expires while
        waiting for capacity is cancelled HERE, before `func` is ever submitted: the
        `await` below happens strictly before `self._executor.submit(...)`). If
        `submit()` itself raises (T100/R2 — e.g. the executor was shut down
        independently of this worker's own `shutdown()`), the just-acquired permit is
        returned immediately, before the exception propagates — never leaked.
        Once submitted, the admission slot is released exactly when that
        `concurrent.futures.Future` reaches a terminal state (finished, raised, or
        actually cancelled) — bound to the future's own `add_done_callback`, never to
        this coroutine's own cancellation, so already-admitted/running work keeps
        counting against capacity until it genuinely finishes, even once nobody is
        still awaiting its result. Cancelling this `await` itself (e.g.
        `run_with_deadline`'s `asyncio.wait_for` firing) propagates immediately —
        `asyncio.wrap_future` cancels its wrapper future synchronously and only
        best-effort-attempts to cancel the underlying `concurrent.futures.Future`
        afterwards (a no-op once the worker thread has already started running it);
        it never waits for the worker thread itself to finish."""
        loop = asyncio.get_running_loop()
        await self._admission.acquire()
        try:
            cf_future = self._executor.submit(func, *args)
        except Exception:
            self._admission.release()
            raise

        cf_future.add_done_callback(lambda _future: self._admission.release())
        return await asyncio.wrap_future(cf_future, loop=loop)

    def shutdown(self, *, wait: bool = True) -> None:
        """Test-only lifecycle hook — the process-wide default instance (below) is
        never shut down during normal operation. Idempotent: a second (or later)
        call is a no-op. Any `run()` call still waiting for admission at the moment
        of the call is rejected immediately with a `RuntimeError`; any `run()` call
        made afterward fails immediately too (`_ProcessWideAdmission.acquire`'s own
        closed check), never acquiring or leaking a permit. Waits for the dedicated
        executor's worker threads to actually terminate (once any blockers they are
        holding have been released by the caller) so a test suite never finishes
        with live worker threads still running."""
        pending = self._admission.close()
        exc = RuntimeError("admission is closed — the worker was shut down")
        for waiter in pending:
            _reject_waiter(waiter, exc)
        self._executor.shutdown(wait=wait)


_default_worker: BoundedBlockingWorker | None = None
_default_worker_lock = threading.Lock()


def default_blocking_retrieval_worker() -> BoundedBlockingWorker:
    """The process-wide singleton `MaterialRetrieverAgent` uses unless a test injects
    its own instance. Constructed lazily on first use (never at import time, so
    importing this module never spawns a thread as a side effect), guarded by a
    module-level `threading.Lock` (T100/R3: the first round's lazy check had no
    mutual exclusion at all — two threads racing into this function for the first
    time could each construct and keep a reference to a DIFFERENT worker, splitting
    the shared capacity in two). Double-checked: the common case (already
    constructed) never pays the lock."""
    global _default_worker
    if _default_worker is None:
        with _default_worker_lock:
            if _default_worker is None:
                _default_worker = BoundedBlockingWorker()
    return _default_worker
