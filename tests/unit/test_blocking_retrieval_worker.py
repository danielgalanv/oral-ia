"""T086 — unit tests for `BoundedBlockingWorker`
(`infrastructure/concurrency/blocking_retrieval_worker.py`), in isolation from
`MaterialRetrieverAgent`. Coordination is `threading.Event`-based throughout (a
background release thread where a delay is genuinely needed, otherwise direct,
caller-controlled release), never a bare `sleep` used as the primary synchronization
mechanism — cooperative `await asyncio.sleep(0)` yields appear only to give the event
loop a chance to run already-scheduled callbacks, never to wait out a real duration.
Every blocking wait carries a safety timeout so a broken double fails fast instead of
hanging the suite; blockers/workers are always released and shut down in `finally`.
"""

from __future__ import annotations

import asyncio
import threading

import pytest

from oralia.infrastructure.concurrency.blocking_retrieval_worker import BoundedBlockingWorker

_SAFETY_TIMEOUT_S = 5.0


class _ManualReleaseBlocker:
    """A block the test releases explicitly (`release()`), rather than after a fixed
    delay — used where the test needs to control the exact moment of release relative
    to other events, not just "eventually released"."""

    def __init__(self, safety_timeout_s: float = _SAFETY_TIMEOUT_S) -> None:
        self._entered = threading.Event()
        self._release = threading.Event()
        self._safety_timeout_s = safety_timeout_s

    def block(self) -> str:
        self._entered.set()
        if not self._release.wait(self._safety_timeout_s):
            raise TimeoutError("safety timeout exceeded - broken test double, not a real slow dependency")
        return "done"

    def wait_entered(self) -> bool:
        return self._entered.wait(self._safety_timeout_s)

    def release(self) -> None:
        self._release.set()

    def close(self) -> None:
        self._entered.set()
        self._release.set()


@pytest.mark.integration
async def test_admission_never_exceeds_injected_capacity_under_burst():
    """Deliverable 3: with capacity N injected and far more than N concurrent
    requests, at no point are more than N operations simultaneously admitted/running.
    Structural, not probabilistic: additional requests are gated on `semaphore.acquire()`,
    which cannot succeed until `release_event` is set — so nothing can push
    `concurrent_count` above `capacity` before this test allows it to."""
    capacity = 3
    n_requests = 9
    worker = BoundedBlockingWorker(capacity=capacity)
    lock = threading.Lock()
    concurrent_count = 0
    max_concurrent = 0
    capacity_reached = threading.Event()
    release_event = threading.Event()

    def blocked_op(idx: int) -> int:
        nonlocal concurrent_count, max_concurrent
        with lock:
            concurrent_count += 1
            max_concurrent = max(max_concurrent, concurrent_count)
            if concurrent_count >= capacity:
                capacity_reached.set()
        release_event.wait(_SAFETY_TIMEOUT_S)
        with lock:
            concurrent_count -= 1
        return idx

    try:
        tasks = [asyncio.create_task(worker.run(blocked_op, i)) for i in range(n_requests)]
        # Waited off the event-loop thread (`run_in_executor`), never a direct
        # blocking `.wait()` here — the created tasks above still need the loop
        # itself free to run their first step (admission + submission) while this
        # coroutine waits for `capacity_reached`.
        loop = asyncio.get_running_loop()
        reached = await loop.run_in_executor(None, capacity_reached.wait, _SAFETY_TIMEOUT_S)
        assert reached, "capacity was never reached — broken test setup"
        with lock:
            # No more than `capacity` could have been admitted by this point: the
            # remaining (n_requests - capacity) tasks are all still blocked on
            # `semaphore.acquire()`, which only a `release()` below can unblock.
            observed_before_release = concurrent_count
        release_event.set()
        results = await asyncio.gather(*tasks)
    finally:
        release_event.set()
        worker.shutdown(wait=True)

    assert observed_before_release == capacity
    assert max_concurrent == capacity, (
        f"expected exactly {capacity} concurrent admissions, saw {max_concurrent}"
    )
    assert sorted(results) == list(range(n_requests))


@pytest.mark.integration
async def test_expired_admission_wait_never_submits_to_executor():
    """Deliverable 4: a request cancelled while still waiting for admission MUST
    NEVER have its operation submitted to the executor, not even later once capacity
    frees up."""
    capacity = 1
    worker = BoundedBlockingWorker(capacity=capacity)
    occupy_blocker = _ManualReleaseBlocker()
    waiting_op_called = threading.Event()

    def waiting_op() -> str:
        waiting_op_called.set()
        return "should never run"

    try:
        occupy_task = asyncio.create_task(worker.run(occupy_blocker.block))
        await asyncio.sleep(0)  # let occupy_task reach admission+submit
        assert occupy_blocker.wait_entered(), "occupy() never started — broken test setup"

        waiting_task = asyncio.create_task(worker.run(waiting_op))
        await asyncio.sleep(0)  # let it start (and block on) awaiting admission
        waiting_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiting_task

        occupy_blocker.release()
        assert await occupy_task == "done"
        # Capacity is free again now — give a wrongly-queued waiting_op every
        # remaining chance to run.
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        assert not waiting_op_called.is_set(), (
            "a request cancelled while waiting for admission MUST NOT be submitted later"
        )
    finally:
        occupy_blocker.close()
        worker.shutdown(wait=True)


@pytest.mark.integration
async def test_cancelling_in_flight_work_does_not_release_capacity_early():
    """Deliverable 5: cancelling the `await` on an operation whose worker thread is
    still genuinely running MUST NOT free its capacity slot immediately — the slot
    stays held until the real work finishes."""
    capacity = 1
    worker = BoundedBlockingWorker(capacity=capacity)
    first_blocker = _ManualReleaseBlocker()
    second_entered = threading.Event()

    def second_op() -> str:
        second_entered.set()
        return "second"

    try:
        first_task = asyncio.create_task(worker.run(first_blocker.block))
        await asyncio.sleep(0)
        assert first_blocker.wait_entered(), "first op never started — broken test setup"

        first_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await first_task
        # The underlying thread is still genuinely blocked (first_blocker not
        # released) — capacity MUST still be held despite the await having been
        # cancelled.
        second_task = asyncio.create_task(worker.run(second_op))
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        assert not second_entered.is_set(), (
            "capacity was released before the cancelled worker's real work finished"
        )

        # Only once the real (still-running) work actually completes does capacity
        # free up — Deliverable 6 evidence, same test. Waited off the event-loop
        # thread: the queued `semaphore.release()` callback and `second_task`'s
        # resumed admission both need the loop itself free to run while this
        # coroutine waits.
        first_blocker.release()
        freed = await asyncio.get_running_loop().run_in_executor(None, second_entered.wait, _SAFETY_TIMEOUT_S)
        assert freed, "capacity should free once the real work finishes"
        assert await second_task == "second"
    finally:
        first_blocker.close()
        worker.shutdown(wait=True)


@pytest.mark.integration
async def test_capacity_recovers_after_ordinary_completion_for_a_later_request():
    """Deliverable 6 (non-cancelled path): a request that completes normally frees
    its slot, letting a later request that had to wait for capacity complete too."""
    capacity = 1
    worker = BoundedBlockingWorker(capacity=capacity)
    first_blocker = _ManualReleaseBlocker()
    second_entered = threading.Event()

    def second_op() -> str:
        second_entered.set()
        return "second"

    try:
        first_task = asyncio.create_task(worker.run(first_blocker.block))
        await asyncio.sleep(0)
        assert first_blocker.wait_entered()

        second_task = asyncio.create_task(worker.run(second_op))
        await asyncio.sleep(0)
        assert not second_entered.is_set(), "second op must not start while first still holds capacity"

        first_blocker.release()
        assert await first_task == "done"
        assert second_entered.wait(_SAFETY_TIMEOUT_S)
        assert await second_task == "second"
    finally:
        first_blocker.close()
        worker.shutdown(wait=True)


def test_worker_reusable_across_successive_event_loops():
    """Deliverable 10: the SAME `BoundedBlockingWorker` (and its internal admission
    gate) is used from two independently created/closed event loops
    (`asyncio.run()` creates and tears down a fresh loop each call) with no "bound to
    a different event loop" error — never a single `asyncio.Semaphore` constructed
    once at import time."""
    worker = BoundedBlockingWorker(capacity=2)
    main_thread_id = threading.get_ident()
    try:
        result1 = asyncio.run(worker.run(threading.get_ident))
        result2 = asyncio.run(worker.run(threading.get_ident))
    finally:
        worker.shutdown(wait=True)

    assert result1 != main_thread_id
    assert result2 != main_thread_id


def test_capacity_still_enforced_after_rebinding_to_a_new_event_loop():
    """Deliverable 10, continued: capacity bounding itself (not just "no crash")
    keeps working correctly after the admission gate has rebound to a second event
    loop — a burst run inside the SECOND `asyncio.run()` call still respects
    `capacity`. Event-coordinated (same structural guarantee as the burst test
    above), never a `sleep`-sized operation standing in for real coordination."""
    capacity = 2
    n_requests = 6
    worker = BoundedBlockingWorker(capacity=capacity)

    def _run_gated_burst() -> int:
        lock = threading.Lock()
        concurrent_count = 0
        max_concurrent = 0
        capacity_reached = threading.Event()
        release_event = threading.Event()

        def blocked_op() -> None:
            nonlocal concurrent_count, max_concurrent
            with lock:
                concurrent_count += 1
                max_concurrent = max(max_concurrent, concurrent_count)
                if concurrent_count >= capacity:
                    capacity_reached.set()
            release_event.wait(_SAFETY_TIMEOUT_S)
            with lock:
                concurrent_count -= 1

        async def _burst() -> None:
            tasks = [asyncio.create_task(worker.run(blocked_op)) for _ in range(n_requests)]
            await asyncio.get_running_loop().run_in_executor(
                None, capacity_reached.wait, _SAFETY_TIMEOUT_S
            )
            release_event.set()
            await asyncio.gather(*tasks)

        try:
            asyncio.run(_burst())
        finally:
            release_event.set()
        return max_concurrent

    try:
        first_max = _run_gated_burst()  # first loop — binds the admission gate
        second_max = _run_gated_burst()  # second, independent loop — MUST rebind, not raise
    finally:
        worker.shutdown(wait=True)

    assert first_max == capacity
    assert second_max == capacity
