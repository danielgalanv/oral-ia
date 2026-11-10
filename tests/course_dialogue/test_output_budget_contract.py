"""No real worker/model: requested budgets must be accepted exactly or rejected."""

from types import SimpleNamespace

import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.lab_request import LabGenerationRequest
from oralia.infrastructure.generation import config
from oralia.infrastructure.generation.generation_port import GenerationError, GenerationRequest
from oralia.infrastructure.generation.ollama_adapter import OllamaGenerationAdapter
from tests.course_dialogue.test_cached_adapter import Process


@pytest.mark.parametrize("tokens", [256, 512, 768, 1024, 2048])
async def test_cached_budget_is_never_silently_clipped(tokens):
    process = Process()
    adapter = CachedTransformersGenerationAdapter(process)
    request = GenerationRequest(
        purpose="explicacion", instruction="synthetic", constraints={"max_tokens": tokens}
    )
    if tokens > 512:
        with pytest.raises(GenerationError, match="presupuesto"):
            await adapter.generate(request)
        assert process.payload is None
        assert adapter.last_exchange["token_budget"]["status"] == "rejected"
    else:
        result = await adapter.generate(request)
        assert process.payload["max_tokens"] == tokens
        assert result.parameters["requested_max_tokens"] == tokens
        assert adapter.last_exchange["token_budget"]["effective"] == tokens


@pytest.mark.parametrize("tokens", [0, -1, 1024, 2048])
def test_ollama_configuration_rejects_invalid_budget(monkeypatch, tokens):
    monkeypatch.setenv("ORALIA_OLLAMA_MAX_TOKENS", str(tokens))
    with pytest.raises(ValueError, match="64.*512"):
        config.get_ollama_max_tokens()


async def test_length_remains_incomplete():
    result = await CachedTransformersGenerationAdapter(Process("length")).generate(
        GenerationRequest(purpose="explicacion", instruction="synthetic")
    )
    assert result.finish_reason == "length"
    assert result.ok is False


@pytest.mark.parametrize("tokens", [256, 512, 768])
async def test_lab_budget_matches_sent_frame(tokens):
    process = Process()
    outcome = await CachedTransformersGenerationAdapter(process).generate(
        LabGenerationRequest(
            purpose="explicacion", instruction="synthetic", constraints={"max_tokens": tokens}
        )
    )
    assert process.payload["max_tokens"] == tokens
    assert outcome.parameters["max_tokens_capacity"] == 768


@pytest.mark.parametrize("tokens", [256, 512, 768, 1024, 2048])
async def test_ollama_budget_matches_sent_payload_or_rejects(monkeypatch, tokens):
    from oralia.infrastructure.generation import ollama_adapter

    monkeypatch.setenv("ORALIA_OLLAMA_MODEL", "synthetic-model")
    monkeypatch.setenv("ORALIA_OLLAMA_MAX_TOKENS", "512")
    sent = []

    class Client:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, json):
            sent.append(json)
            return SimpleNamespace(
                raise_for_status=lambda: None,
                json=lambda: {"message": {"content": "synthetic"}, "done_reason": "length"},
            )

    monkeypatch.setattr(ollama_adapter.httpx, "AsyncClient", Client)
    adapter = OllamaGenerationAdapter()
    request = GenerationRequest(
        purpose="explicacion", instruction="synthetic", constraints={"max_tokens": tokens}
    )
    if tokens > 512:
        with pytest.raises(GenerationError, match="presupuesto"):
            await adapter.generate(request)
        assert sent == []
    else:
        outcome = await adapter.generate(request)
        assert sent[0]["options"]["num_predict"] == tokens
        assert outcome.ok is False and outcome.finish_reason == "length"
    assert adapter.last_token_budget["requested"] == tokens
