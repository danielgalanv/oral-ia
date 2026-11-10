import asyncio
import threading

import pytest

from oralia.infrastructure.speech import blocking_speech_worker as worker_module
from oralia.infrastructure.speech.blocking_speech_worker import (
    BoundedSpeechWorker,
    default_blocking_speech_worker,
)


async def test_capacity_and_fifo_backpressure() -> None:
    worker = BoundedSpeechWorker(capacity=1)
    entered = threading.Event()
    release = threading.Event()
    order: list[str] = []

    def first() -> str:
        entered.set()
        release.wait(3)
        order.append("first")
        return "first"

    def second() -> str:
        order.append("second")
        return "second"

    try:
        first_task = asyncio.create_task(worker.run(first))
        assert await asyncio.get_running_loop().run_in_executor(None, entered.wait, 3)
        second_task = asyncio.create_task(worker.run(second))
        await asyncio.sleep(0)
        assert order == []
        release.set()
        assert await first_task == "first"
        assert await second_task == "second"
        assert order == ["first", "second"]
    finally:
        release.set()
        worker.shutdown()


async def test_cancelled_waiter_is_never_submitted() -> None:
    worker = BoundedSpeechWorker(capacity=1)
    entered = threading.Event()
    release = threading.Event()
    called = threading.Event()

    def blocking() -> None:
        entered.set()
        release.wait(3)

    try:
        active = asyncio.create_task(worker.run(blocking))
        assert await asyncio.get_running_loop().run_in_executor(None, entered.wait, 3)
        waiting = asyncio.create_task(worker.run(called.set))
        await asyncio.sleep(0)
        waiting.cancel()
        with pytest.raises(asyncio.CancelledError):
            await waiting
        release.set()
        await active
        await asyncio.sleep(0)
        assert not called.is_set()
    finally:
        release.set()
        worker.shutdown()


async def test_cancelled_running_work_holds_capacity_until_real_completion() -> None:
    worker = BoundedSpeechWorker(capacity=1)
    entered = threading.Event()
    release = threading.Event()
    next_called = threading.Event()

    def blocking() -> None:
        entered.set()
        release.wait(3)

    try:
        active = asyncio.create_task(worker.run(blocking))
        assert await asyncio.get_running_loop().run_in_executor(None, entered.wait, 3)
        active.cancel()
        with pytest.raises(asyncio.CancelledError):
            await active
        following = asyncio.create_task(worker.run(next_called.set))
        await asyncio.sleep(0)
        assert not next_called.is_set()
        release.set()
        assert await asyncio.get_running_loop().run_in_executor(None, next_called.wait, 3)
        await following
    finally:
        release.set()
        worker.shutdown()


async def test_submit_failure_does_not_leak_permit() -> None:
    worker = BoundedSpeechWorker(capacity=1)
    worker._worker._executor.shutdown(wait=True)
    with pytest.raises(RuntimeError):
        await worker.run(lambda: None)
    await asyncio.wait_for(worker._worker._admission.acquire(), timeout=1)


def test_worker_is_reusable_across_successive_event_loops() -> None:
    worker = BoundedSpeechWorker(capacity=1)
    try:
        assert asyncio.run(worker.run(lambda: 1)) == 1
        assert asyncio.run(worker.run(lambda: 2)) == 2
    finally:
        worker.shutdown()


def test_default_worker_is_a_locked_singleton(monkeypatch) -> None:
    monkeypatch.setattr(worker_module, "_default_worker", None)
    found: list[BoundedSpeechWorker] = []
    threads = [
        threading.Thread(target=lambda: found.append(default_blocking_speech_worker())) for _ in range(8)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len({id(worker) for worker in found}) == 1
    found[0].shutdown()
    monkeypatch.setattr(worker_module, "_default_worker", None)


def test_capacity_is_shared_by_concurrent_event_loops():
    worker = BoundedSpeechWorker(capacity=1)
    entered = threading.Event()
    release = threading.Event()
    second_requested = threading.Event()
    second_entered = threading.Event()
    failures = []

    def blocking():
        entered.set()
        assert release.wait(3)

    def run_first():
        try:
            asyncio.run(worker.run(blocking))
        except BaseException as error:
            failures.append(error)

    def run_second():
        async def operation():
            second_requested.set()
            await worker.run(second_entered.set)

        try:
            asyncio.run(operation())
        except BaseException as error:
            failures.append(error)

    first = threading.Thread(target=run_first)
    second = threading.Thread(target=run_second)
    try:
        first.start()
        assert entered.wait(2)
        second.start()
        assert second_requested.wait(2)
        assert not second_entered.wait(0.05)
        release.set()
        first.join(3)
        second.join(3)
        assert not first.is_alive() and not second.is_alive()
        assert second_entered.is_set() and not failures
    finally:
        release.set()
        worker.shutdown()
