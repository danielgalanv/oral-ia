"""Explicit teacher-only local model lifespan, preserving the historical UI budget."""

import asyncio
import copy
import json
import subprocess
import time
from contextlib import asynccontextmanager
from pathlib import Path

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
from oralia.course_dialogue.model_prompt_profiles import snapshot_path
from oralia.course_dialogue.review_repair import CallBudget
from oralia.course_dialogue.structured_request import structured_request
from oralia.documentary.study_budget import study_budget
from oralia.documentary.study_errors import StudyFailure
from oralia.documentary.study_lab import TrialBudget


def gpu():
    row = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=memory.used,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=5,
    ).stdout.strip()
    used, total, utilization = map(int, row.split(","))
    return dict(monotonic=time.monotonic(), used_mib=used, total_mib=total, utilization_percent=utilization)


class RealStudyProvider:
    diagnostic_label = "REAL_QWEN25_14B_NF4_STRUCTURED_TEACHER"
    diagnostic_deadline_seconds = 50

    MAX_RUNTIME_SECONDS = 2700  # a finite teacher runtime; the llama.cpp provider allows a class session

    def __init__(
        self,
        output,
        *,
        started=None,
        seconds=900,
        academic_calls_used=0,
        study_budget_profile="historical/v1",
        reviewed=False,
        experimental_limits=None,
        local_first=False,
        notice_review=False,
    ):
        if type(reviewed) is not bool:
            raise ValueError("Reviewed runtime must be explicitly selected")
        if type(local_first) is not bool or (local_first and not reviewed):
            raise ValueError("Local-first routing requires the reviewed runtime")
        if type(notice_review) is not bool or (notice_review and not reviewed):
            raise ValueError("Notice review requires the reviewed runtime")
        self.notice_review = notice_review
        self.local_first = local_first
        if local_first:
            self.control_prompt_version = "web-control/v5"
            self.study_dialogue_profile = "study-dialogue/v4"
            self.review_prompt_version = "web-review/v8"
        if experimental_limits is None:
            experimental_limits = not reviewed
        if type(experimental_limits) is not bool or (not experimental_limits and not reviewed):
            raise ValueError("Uncapped study requires explicit reviewed runtime")
        if not reviewed and study_budget_profile == "study-reviewed/v1":
            raise ValueError("Reviewed budget requires reviewed runtime")
        self.reviewed = reviewed
        if reviewed:
            study_budget_profile = "study-reviewed/v1"
        self.study_budget_profile = study_budget_profile
        self.diagnostic_deadline_seconds = (
            600 if reviewed else study_budget(study_budget_profile).deadline_seconds
        )
        self.output = Path(output)
        self.started = time.monotonic() if started is None else started
        if not 60 <= seconds <= self.MAX_RUNTIME_SECONDS or not 0 <= time.monotonic() - self.started < seconds:
            raise ValueError("Invalid or expired finite teacher runtime")
        self.deadline = self.started + seconds
        self.expires_at_unix_ms = (time.time() + self.deadline - time.monotonic()) * 1000
        self.adapter = None
        maximum_questions = (12 if reviewed else 6) if experimental_limits else None
        if academic_calls_used < 0 or (
            maximum_questions is not None and academic_calls_used > maximum_questions
        ):
            raise ValueError("Invalid prior academic call count")
        self.trial_budget = TrialBudget(
            used=academic_calls_used, started=self.started, maximum=maximum_questions, seconds=seconds
        )
        self._worker = None
        self._preparation = None
        self._loads = 0
        self._lock = asyncio.Lock()
        self.critic_adapter = self._critic_worker = None
        self.review_lock = asyncio.Lock()
        self.review_budget = CallBudget(
            maximum=(84 if reviewed else 42) if experimental_limits else None, seconds=seconds
        )
        self.review_budget.started = self.started
        if reviewed:
            self.diagnostic_label = "REAL_QWEN14B_QWEN3_THINKING_REVIEWED"

    @property
    def ready(self):
        return (
            self.adapter is not None
            and getattr(self.adapter, "usable", True)
            and time.monotonic() < self.deadline
            and (
                not self.reviewed
                or (self.critic_adapter is not None and getattr(self.critic_adapter, "usable", True))
            )
        )

    @property
    def preparing(self):
        return self._preparation is not None and not self._preparation.done()

    def runtime_status(self):
        remaining = max(0, self.deadline - time.monotonic())
        return {
            "expires_at_unix_ms": self.expires_at_unix_ms,
            "remaining_seconds": remaining,
            "expired": remaining <= 0,
            "renewable": False,
        }

    async def _close_worker(self):
        critic, self._critic_worker = self._critic_worker, None
        self.critic_adapter = None
        worker, self._worker = self._worker, None
        self.adapter = None
        try:
            if critic is not None:
                await critic.__aexit__(None, None, None)
        finally:
            if worker is not None:
                await worker.__aexit__(None, None, None)

    async def _prepare(self, revalidate):
        async with self._lock:
            revalidate()
            if self.ready:
                return
            await self._close_worker()
            revalidate()
            if time.monotonic() >= self.deadline or self._loads >= 2:
                raise ValueError("Finite model preparation budget exhausted")
            before = gpu()
            if before["total_mib"] - before["used_mib"] < (25000 if self.reviewed else 20000) or (
                self.reviewed and before["utilization_percent"] > 10
            ):
                raise ValueError("Insufficient measured free GPU capacity")
            self._loads += 1
            output = self.output / f"worker-{self._loads:03d}"
            output.mkdir(exist_ok=False)
            (output / "gpu-before.json").write_text(json.dumps(before), encoding="utf8")
            worker = cached_provider(
                output,
                source=CACHED_MODEL_14B,
                quantization="nf4",
                preparation_seconds=min(180, max(1, int(self.deadline - time.monotonic()))),
                repair_profile_enabled=True,
                model_prompt_profile="qwen25-14b",
                sampling_profile="greedy/v1",
                generation_seed=42,
                release_cuda_cache=getattr(self, "cuda_cache_handoff", True) if self.reviewed else False,
            )
            self.adapter = await worker.__aenter__()
            self._worker = worker
            try:
                revalidate()
                if self.reviewed:
                    available = gpu()
                    if available["total_mib"] - available["used_mib"] < 10000:
                        raise ValueError(
                            "Insufficient free capacity for reviewer; foreign processes untouched"
                        )
                    critic_folder = self.output / f"critic-{self._loads:03d}"
                    critic_folder.mkdir(exist_ok=False)
                    critic = cached_provider(
                        critic_folder,
                        source=snapshot_path("qwen3-8b-thinking"),
                        quantization="nf4",
                        preparation_seconds=min(180, max(1, int(self.deadline - time.monotonic()))),
                        repair_profile_enabled=True,
                        thinking_review_enabled=True,
                        model_prompt_profile="qwen3-8b-thinking",
                        sampling_profile="qwen3-thinking-sampling/v1",
                        generation_seed=42,
                        release_cuda_cache=getattr(self, "cuda_cache_handoff", True),
                    )
                    self.critic_adapter = await critic.__aenter__()
                    self._critic_worker = critic
                    revalidate()
            except BaseException:
                await self._close_worker()
                raise

    def request_prepare(self, revalidate):
        revalidate()
        if self.ready or self.preparing:
            return
        if time.monotonic() >= self.deadline or self._loads >= 2:
            raise ValueError("Finite model preparation budget exhausted; restart explicitly")

        async def prepare():
            try:
                async with asyncio.timeout_at(self.deadline):
                    await self._prepare(revalidate)
            except (Exception, asyncio.CancelledError) as error:
                (self.output / "preparation-recovery-error.json").write_text(
                    json.dumps({"error_type": type(error).__name__}), encoding="utf8"
                )

        self._preparation = asyncio.create_task(prepare())

    @asynccontextmanager
    async def lifespan(self, app):
        self.output.mkdir(parents=True, exist_ok=False)

        before = gpu()
        (self.output / "gpu-before.json").write_text(json.dumps(before), encoding="utf8")
        if before["total_mib"] - before["used_mib"] < (25000 if self.reviewed else 20000) or (
            self.reviewed and before["utilization_percent"] > 10
        ):
            raise ValueError("Insufficient measured free GPU capacity")

        async def expire():
            await asyncio.sleep(max(0, self.deadline - time.monotonic()))
            app.state.request_shutdown()

        task = asyncio.create_task(expire())
        try:
            async with asyncio.timeout_at(self.deadline):
                await self._prepare(lambda: None)
            yield
        finally:
            task.cancel()
            if self._preparation is not None:
                self._preparation.cancel()
                await asyncio.gather(self._preparation, return_exceptions=True)
            await asyncio.gather(task, return_exceptions=True)
            await self._close_worker()
            (self.output / "gpu-after.json").write_text(json.dumps(gpu()), encoding="utf8")

    def for_session(self, revalidate):
        if self.reviewed:
            from oralia.documentary.reviewed_study import ReviewedStudySession

            return ReviewedStudySession(self, revalidate)
        owner = self

        class Bound:
            diagnostic_label = owner.diagnostic_label
            diagnostic_deadline_seconds = owner.diagnostic_deadline_seconds
            study_budget_profile = owner.study_budget_profile
            last_exchange = None

            def runtime_status(self):
                return owner.runtime_status()

            @property
            def ready(self):
                return owner.ready

            async def generate(self, request):
                revalidate()
                if not owner.ready:
                    raise StudyFailure(
                        "runtime_expired" if time.monotonic() >= owner.deadline else "model_unavailable"
                    )
                adapter = owner.adapter
                actual = structured_request(
                    request,
                    model_profile="qwen25-14b",
                    task="generate",
                    didactic_profile=getattr(owner, "study_dialogue_profile", "study-dialogue/v2"),
                )
                try:
                    async with asyncio.timeout_at(owner.deadline):
                        result = await adapter.generate(actual)
                    revalidate()
                    if time.monotonic() >= owner.deadline:
                        raise TimeoutError("Global teacher runtime expired before delivery")
                    return result
                finally:
                    self.last_exchange = copy.deepcopy(adapter.last_exchange)
                    if self.last_exchange is not None:
                        self.last_exchange["effective_request"] = actual.model_dump()

        return Bound()

    async def generate(self, request):
        raise ValueError("Open an authorized teacher inspection before generation")
