"""Process-wide bounded admission for blocking STT and TTS calls."""

import threading
from collections.abc import Callable
from typing import TypeVar

from oralia.infrastructure.concurrency.blocking_retrieval_worker import BoundedBlockingWorker
from oralia.infrastructure.speech.config import settings

_T = TypeVar("_T")


class BoundedSpeechWorker:
    def __init__(self, capacity: int = 1) -> None:
        self.capacity = capacity
        self._worker = BoundedBlockingWorker(capacity=capacity)

    async def run(self, func: Callable[..., _T], *args: object) -> _T:
        return await self._worker.run(func, *args)

    def shutdown(self, *, wait: bool = True) -> None:
        self._worker.shutdown(wait=wait)


_default_worker: BoundedSpeechWorker | None = None
_default_worker_lock = threading.Lock()


def default_blocking_speech_worker() -> BoundedSpeechWorker:
    global _default_worker
    if _default_worker is None:
        with _default_worker_lock:
            if _default_worker is None:
                _default_worker = BoundedSpeechWorker(settings().worker_capacity)
    return _default_worker


__all__ = ["BoundedSpeechWorker", "default_blocking_speech_worker"]
