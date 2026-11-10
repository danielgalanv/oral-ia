"""Take turns on the GPU between the llama.cpp servers.

Two servers decoding at the same time on one GPU (two processes, two CUDA contexts) slow each other down by an
order of magnitude (measured: 4 parallel requests on each server alone 350 and 290 tok/s, both at once 25 tok/s
each). Several students are handled by letting many calls of the SAME group run together (the server batches
them) and making the other group wait until the batch ends. Waiting groups are served before new arrivals of
the active group, so nobody starves.
"""

import asyncio
from collections import Counter
from contextlib import asynccontextmanager


class GroupExclusion:
    def __init__(self):
        self._cond = asyncio.Condition()
        self._active = None
        self._count = 0
        self._waiting = Counter()

    def _can_enter(self, group):
        if self._active is None:
            return True
        return self._active == group and not any(n for g, n in self._waiting.items() if g != group)

    @asynccontextmanager
    async def use(self, group):
        async with self._cond:
            self._waiting[group] += 1
            try:
                await self._cond.wait_for(lambda: self._can_enter(group))
            finally:
                self._waiting[group] -= 1
            self._active = group
            self._count += 1
        try:
            yield
        finally:
            async with self._cond:
                self._count -= 1
                if self._count == 0:
                    self._active = None
                self._cond.notify_all()


class TurnTakingProvider:
    """A generation provider whose calls run inside one group of a GroupExclusion."""

    def __init__(self, provider, exclusion, group):
        self._provider, self._exclusion, self._group = provider, exclusion, group

    async def generate(self, request):
        async with self._exclusion.use(self._group):
            return await self._provider.generate(request)

    async def generate_stream(self, request, on_text):
        async with self._exclusion.use(self._group):
            return await self._provider.generate_stream(request, on_text)

    def __getattr__(self, name):
        return getattr(self._provider, name)
