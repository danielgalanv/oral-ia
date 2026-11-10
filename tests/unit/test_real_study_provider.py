from contextlib import asynccontextmanager

import pytest

from oralia.course_dialogue.lab_request import LabGenerationRequest
from oralia.documentary.real_study_provider import RealStudyProvider
from oralia.infrastructure.generation.generation_port import GenerationOutcome


async def test_live_binding_uses_structured_native_profile_without_expanding_budget(tmp_path):
    provider = RealStudyProvider(tmp_path / "exclusive")

    class Adapter:
        last_exchange = {"fixture": True}

        async def generate(self, request):
            assert request.prompt_task == "generate" and request.model_profile == "qwen25-14b"
            assert request.didactic_profile == "study-dialogue/v2"
            assert request.constraints.max_tokens == 768 and request.constraints.deadline_ms == 50000
            assert request.effective_messages()[-1]["role"] == "user"
            return GenerationOutcome(
                ok=True, text="fixture only", adapter="deterministic", finish_reason="stop"
            )

    provider.adapter = Adapter()
    checks = []
    bound = provider.for_session(lambda: checks.append(True))
    result = await bound.generate(
        LabGenerationRequest(purpose="explicacion", instruction="historical", student_input="question")
    )
    assert result.ok and len(checks) == 2
    assert bound.last_exchange["effective_request"]["question"] == "question"
    assert provider.trial_budget.maximum == 6
    with pytest.raises(ValueError):
        await provider.generate(None)


async def test_withdrawal_prevents_transport_before_real_generation(tmp_path):
    provider = RealStudyProvider(tmp_path / "exclusive")

    def withdrawn():
        raise ValueError("withdrawn")

    with pytest.raises(ValueError, match="withdrawn"):
        await provider.for_session(withdrawn).generate(None)


async def test_explicit_reload_preserves_deadline_and_used_budget(monkeypatch, tmp_path):
    import oralia.documentary.real_study_provider as live

    closed = []

    @asynccontextmanager
    async def cached(output, **settings):
        class Adapter:
            usable = True

        try:
            yield Adapter()
        finally:
            closed.append(output.name)

    monkeypatch.setattr(live, "cached_provider", cached)
    monkeypatch.setattr(live, "gpu", lambda: {"total_mib": 32000, "used_mib": 1000})
    provider = RealStudyProvider(tmp_path, academic_calls_used=4)
    deadline = provider.deadline
    await provider._prepare(lambda: None)
    provider.adapter.usable = False
    provider.request_prepare(lambda: None)
    assert provider.preparing and not provider.ready
    await provider._preparation
    assert provider.ready and closed == ["worker-001"]
    assert provider.deadline == deadline and provider.trial_budget.used == 4
    provider.adapter.usable = False
    with pytest.raises(ValueError, match="budget exhausted"):
        provider.request_prepare(lambda: None)
    await provider._close_worker()
    assert closed == ["worker-001", "worker-002"]


async def test_reload_requires_current_teacher_authority(tmp_path):
    provider = RealStudyProvider(tmp_path)

    def revoked():
        raise ValueError("revoked")

    with pytest.raises(ValueError, match="revoked"):
        provider.request_prepare(revoked)
    assert not provider.preparing and provider._loads == 0


async def test_runtime_watchdog_requests_shutdown_before_lifespan_cleanup(monkeypatch, tmp_path):
    import asyncio
    import time
    from types import SimpleNamespace

    import oralia.documentary.real_study_provider as live

    provider = RealStudyProvider(tmp_path / "finite")
    provider.deadline = time.monotonic() + 0.03
    stopped = asyncio.Event()

    async def prepared(revalidate):
        revalidate()

    monkeypatch.setattr(provider, "_prepare", prepared)
    monkeypatch.setattr(live, "gpu", lambda: {"total_mib": 32000, "used_mib": 1000})
    app = SimpleNamespace(state=SimpleNamespace(request_shutdown=stopped.set))
    async with provider.lifespan(app):
        await asyncio.wait_for(stopped.wait(), timeout=0.5)
    assert (provider.output / "gpu-after.json").is_file()


async def test_bound_rejects_result_crossing_global_deadline(monkeypatch, tmp_path):
    import time
    from types import SimpleNamespace

    import oralia.documentary.real_study_provider as live

    clock = [time.monotonic()]
    monkeypatch.setattr(live, "time", SimpleNamespace(monotonic=lambda: clock[0], time=time.time))
    provider = RealStudyProvider(tmp_path)

    class Adapter:
        last_exchange = None
        usable = True

        async def generate(self, request):
            clock[0] = provider.deadline + 1
            return GenerationOutcome(ok=True, text="late", adapter="deterministic", finish_reason="stop")

    provider.adapter = Adapter()
    expiry = provider.runtime_status()["expires_at_unix_ms"]
    with pytest.raises(TimeoutError, match="Global teacher runtime"):
        await provider.for_session(lambda: None).generate(
            LabGenerationRequest(purpose="explicacion", instruction="historical", student_input="question")
        )
    assert provider.runtime_status()["expired"] and provider.runtime_status()["remaining_seconds"] == 0
    assert provider.runtime_status()["expires_at_unix_ms"] == expiry
