"""Real benign Python descendants, cancellation/timeout and an unrelated witness."""

import asyncio
import subprocess
import sys

import psutil
import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.owned_worker import OwnedWorkerTree
from oralia.infrastructure.generation.generation_port import (
    GenerationConstraints,
    GenerationError,
    GenerationRequest,
)


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["cancel", "timeout"])
async def test_real_worker_descendants_stop_but_unrelated_process_survives(failure):
    witness = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    process = None
    tree = None
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-u",
            "-c",
            "import subprocess,sys,time; "
            "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
            "print(p.pid,flush=True); time.sleep(60)",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        tree = OwnedWorkerTree(process.pid)
        child_pid = int(await asyncio.wait_for(process.stdout.readline(), timeout=10))
        tree.capture()
        assert child_pid in tree.owned and witness.pid not in tree.owned
        adapter = CachedTransformersGenerationAdapter(process, terminate_owned=tree.terminate)
        task = asyncio.create_task(
            adapter.generate(
                GenerationRequest(
                    purpose="explicacion",
                    instruction="synthetic transport test",
                    constraints=GenerationConstraints(deadline_ms=1),
                )
            )
        )
        if failure == "cancel":
            await asyncio.sleep(0.05)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        else:
            with pytest.raises(GenerationError, match="plazo"):
                await task
        await asyncio.wait_for(process.wait(), timeout=10)
        receipt = await asyncio.to_thread(tree.finish)
        assert len(receipt) >= 2 and all(row["stopped"] for row in receipt)
        assert not psutil.pid_exists(child_pid)
        assert witness.poll() is None
    finally:
        if tree is not None:
            await asyncio.to_thread(tree.finish)
        if process is not None:
            await asyncio.wait_for(process.wait(), timeout=10)
        witness.terminate()
        witness.wait(timeout=10)
