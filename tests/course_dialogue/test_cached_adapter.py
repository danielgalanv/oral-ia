"""Pipe transport cannot turn a deadline or mismatched frame into success."""

import json
from types import SimpleNamespace

import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.infrastructure.generation.generation_port import GenerationError, GenerationRequest


class Process:
    returncode = None

    def __init__(self, reason="stop", bad_id=False):
        self.reason = reason
        self.bad_id = bad_id
        self.payload = None
        self.stdin = SimpleNamespace(write=self.write, drain=self.drain)
        self.stdout = SimpleNamespace(readline=self.readline)

    def write(self, data):
        self.payload = json.loads(data)

    async def drain(self):
        pass

    async def readline(self):
        return json.dumps(
            {
                "type": "result",
                "id": "wrong" if self.bad_id else self.payload["id"],
                "text": "partial candidate",
                "finish_reason": self.reason,
                "latency_ms": 10,
                "input_tokens": 20,
                "output_tokens": 3,
            }
        ).encode()

    def terminate(self):
        self.returncode = -15


@pytest.mark.asyncio
async def test_registered_tuple_decoder_choices_do_not_expand_the_model_prompt():
    process = Process()
    alternatives = ['{"act":"ask","goal_ref":"a"}']
    await CachedTransformersGenerationAdapter(process).generate(
        GenerationRequest(
            purpose="explicacion",
            instruction="synthetic tuple protocol",
            output_schema={
                "type": "object",
                "properties": {"act": {"type": "string"}},
                "x-oralia-finite-outputs": alternatives,
            },
        )
    )
    assert process.payload["finite_outputs"] == alternatives
    assert "x-oralia-finite-outputs" not in process.payload["messages"][0]["content"]


@pytest.mark.asyncio
async def test_worker_deadline_is_not_success_or_publication():
    process = Process("deadline")
    result = await CachedTransformersGenerationAdapter(process).generate(
        GenerationRequest(purpose="explicacion", instruction="Explain")
    )
    assert result.ok is False
    assert result.finish_reason == "deadline"
    assert process.payload["deadline_ms"] == 6000
    assert "partial candidate" == result.text


@pytest.mark.asyncio
async def test_out_of_sequence_frame_is_rejected():
    process = Process(bad_id=True)
    adapter = CachedTransformersGenerationAdapter(process)
    with pytest.raises(GenerationError, match="secuencia"):
        await adapter.generate(GenerationRequest(purpose="explicacion", instruction="Explain"))
    assert process.returncode is not None
    assert adapter.last_exchange["failure_type"] == "wrong_id"
    assert adapter.last_exchange["returncode_before_cleanup"] is None
    assert '"id": "wrong"' in adapter.last_exchange["raw_worker_response"]


@pytest.mark.asyncio
async def test_eof_diagnostic_precedes_owned_cleanup_and_contains_no_prompt():
    process = Process()

    async def eof():
        return b""

    process.stdout.readline = eof
    adapter = CachedTransformersGenerationAdapter(process)
    with pytest.raises(GenerationError, match="sin respuesta"):
        await adapter.generate(
            GenerationRequest(
                purpose="explicacion", instruction="secret-instruction", student_input="secret-input"
            )
        )
    assert adapter.last_exchange["stage"] == "read"
    assert adapter.last_exchange["failure_type"] == "eof"
    assert adapter.last_exchange["returncode_before_cleanup"] is None
    assert adapter.last_exchange["raw_worker_response"] is None
    assert "secret" not in json.dumps(adapter.last_exchange)


@pytest.mark.asyncio
async def test_invalidated_transport_cannot_be_reused_while_process_exit_is_pending():
    process = Process(bad_id=True)
    writes = []
    stops = []
    original = process.stdin.write

    def capture(data):
        writes.append(data)
        original(data)

    process.stdin.write = capture
    adapter = CachedTransformersGenerationAdapter(process, terminate_owned=lambda: stops.append("signal"))
    request = GenerationRequest(purpose="explicacion", instruction="synthetic delayed-exit race")
    with pytest.raises(GenerationError, match="secuencia"):
        await adapter.generate(request)
    assert process.returncode is None
    with pytest.raises(GenerationError, match="disponible"):
        await adapter.generate(request)
    assert len(writes) == 1 and len(stops) == 1


@pytest.mark.asyncio
async def test_only_fixed_system_and_actual_messages_are_sent():
    process = Process()
    request = GenerationRequest(
        purpose="explicacion",
        instruction="fixed system",
        student_input="current question",
        conversation_history=[{"role": "assistant", "content": "actual previous candidate"}],
    )
    result = await CachedTransformersGenerationAdapter(process).generate(request)
    assert result.ok
    assert process.payload["messages"][0] == {"role": "system", "content": "fixed system"}
    assert process.payload["messages"][1] == {"role": "assistant", "content": "actual previous candidate"}
    assert "current question" in process.payload["messages"][-1]["content"]


@pytest.mark.asyncio
async def test_closed_enum_alternatives_are_explicitly_sent_to_worker():
    process = Process()
    await CachedTransformersGenerationAdapter(process).generate(
        GenerationRequest(
            purpose="explicacion",
            instruction="synthetic enum protocol",
            output_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["scope"],
                "properties": {"scope": {"enum": ["a", "b"]}},
            },
        )
    )
    assert [json.loads(text) for text in process.payload["finite_outputs"]] == [
        {"scope": "a"},
        {"scope": "b"},
    ]


def test_longer_candidate_budget_is_bounded_and_legacy_default_unchanged():
    from pydantic import ValidationError

    from oralia.infrastructure.generation.generation_port import GenerationConstraints

    assert GenerationConstraints().deadline_ms == 6000
    assert GenerationConstraints(deadline_ms=30000).deadline_ms == 30000
    with pytest.raises(ValidationError):
        GenerationConstraints(deadline_ms=30001)
    from oralia.domain.agents.response_generator_agent import CONTRACT

    assert CONTRACT.timeout_ms == 8000


@pytest.mark.asyncio
async def test_cancelled_inference_discards_only_owned_worker():
    import asyncio

    process = Process()
    entered = asyncio.Event()

    async def waiting():
        entered.set()
        await asyncio.Event().wait()

    process.stdout.readline = waiting
    task = asyncio.create_task(
        CachedTransformersGenerationAdapter(process).generate(
            GenerationRequest(purpose="explicacion", instruction="synthetic test only")
        )
    )
    await entered.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert process.returncode == -15


@pytest.mark.asyncio
async def test_cancellation_during_pipe_write_also_invalidates_and_stops_owned_worker():
    import asyncio

    process = Process()
    entered = asyncio.Event()

    async def blocked_drain():
        entered.set()
        await asyncio.Event().wait()

    process.stdin.drain = blocked_drain
    adapter = CachedTransformersGenerationAdapter(process)
    task = asyncio.create_task(
        adapter.generate(GenerationRequest(purpose="explicacion", instruction="synthetic pipe cancellation"))
    )
    await entered.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert adapter.usable is False and process.returncode == -15


@pytest.mark.asyncio
@pytest.mark.parametrize("preparation_seconds", [90, 180])
async def test_worker_does_not_inherit_or_log_installation_credentials(
    tmp_path, monkeypatch, preparation_seconds
):
    from oralia.course_dialogue.cached_transformers import cached_provider

    credential = "FICTITIOUS-PRIVATE-INSTALLATION-012"
    monkeypatch.setenv("ORALIA_ADMIN_SECRET", credential)
    monkeypatch.setenv("UNRELATED_PROVIDER_TOKEN", credential)
    runtime = tmp_path / "runtime.exe"
    runtime.touch()
    source = tmp_path / "model"
    source.mkdir()
    (source / "config.json").write_text("{}")
    output = tmp_path / "output"
    output.mkdir()
    captured = {}
    process = Process()
    process.pid = 123

    async def ready():
        return b'{"type":"ready","schema_hint_only":true}\n'

    async def wait():
        process.returncode = 0
        return 0

    process.stdout.readline = ready
    process.wait = wait

    async def launch(*args, **kwargs):
        captured.update({"args": args, "env": kwargs["env"]})
        return process

    monkeypatch.setattr("oralia.course_dialogue.cached_transformers.asyncio.create_subprocess_exec", launch)
    monkeypatch.setattr(
        "oralia.course_dialogue.cached_transformers.OwnedWorkerTree",
        lambda pid: SimpleNamespace(capture=lambda: None, terminate=process.terminate, finish=lambda: []),
    )
    async with cached_provider(
        output, python=runtime, source=source, preparation_seconds=preparation_seconds
    ):
        pass
    assert credential not in json.dumps(captured)
    assert captured["env"]["HF_HUB_OFFLINE"] == "1"
    assert credential not in "".join(f.read_text() for f in output.iterdir())
    assert json.loads((output / "worker-cleanup.json").read_text())["own_process_stopped"] is True
