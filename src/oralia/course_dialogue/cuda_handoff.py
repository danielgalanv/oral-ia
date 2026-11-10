"""Explicit inter-process memory handoff; never unloads model weights."""

import time


def cuda_handoff(torch, enabled):
    if type(enabled) is not bool:
        raise ValueError("CUDA handoff must be explicit")
    before = dict(allocated=torch.cuda.memory_allocated(), reserved=torch.cuda.memory_reserved())
    started = time.monotonic()
    if enabled:
        torch.cuda.empty_cache()
    after = dict(allocated=torch.cuda.memory_allocated(), reserved=torch.cuda.memory_reserved())
    return dict(
        enabled=enabled, before=before, after=after, elapsed_ms=int((time.monotonic() - started) * 1000)
    )
