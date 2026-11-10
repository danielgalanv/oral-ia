"""Basic CPU/memory/timeout resource monitor (FR-017)."""

from __future__ import annotations

import time
from dataclasses import dataclass

import psutil

_process = psutil.Process()


@dataclass(frozen=True)
class ResourceSnapshot:
    cpu_percent: float
    memory_rss_mb: float
    timestamp: float


def snapshot() -> ResourceSnapshot:
    mem = _process.memory_info().rss / (1024 * 1024)
    cpu = _process.cpu_percent(interval=None)
    return ResourceSnapshot(cpu_percent=cpu, memory_rss_mb=mem, timestamp=time.time())


def as_dict(snap: ResourceSnapshot | None = None) -> dict:
    s = snap or snapshot()
    return {"cpu_percent": s.cpu_percent, "memory_rss_mb": round(s.memory_rss_mb, 2)}
