import json

import httpx
import pytest

from oralia.course_dialogue.concept_ledger import COMPACT_VERSION, ThinkingConceptLedgerRequest
from oralia.course_dialogue.llama_server_provider import LlamaServerProvider, review_schemas
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationError


def evidence():
    return [EvidenceItem(fragment_id="d:1", document_id="d", document_version=1, text="Fuente.")]


def request():
    return ThinkingConceptLedgerRequest(
        purpose="explicacion",
        instruction="t",
        question="Pregunta",
        evidence=evidence(),
        draft="Una respuesta.",
        assigned_units=["U1"],
        prompt_version=COMPACT_VERSION,
    )


def server(handler):
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def reply(content='{"issues":[]}', finish="stop", reasoning="pensando"):
    return {
        "choices": [
            {"message": {"content": content, "reasoning_content": reasoning}, "finish_reason": finish}
        ],
        "usage": {
            "prompt_tokens": 120,
            "completion_tokens": 40,
            "prompt_tokens_details": {"cached_tokens": 100},
        },
    }


@pytest.mark.asyncio
async def test_request_carries_seed_thinking_flag_sampling_and_the_contract_schema():
    seen = {}

    def handler(req):
        seen.update(json.loads(req.content))
        return httpx.Response(200, json=reply())

    provider = LlamaServerProvider(
        model_label="qwen3-8b-q4", thinking=True, seed=7, schemas=review_schemas(), client=server(handler)
    )
    outcome = await provider.generate(request())
    assert seen["seed"] == 7 and seen["chat_template_kwargs"] == {"enable_thinking": True}
    assert seen["temperature"] == 0.6 and seen["top_k"] == 20
    assert seen["max_tokens"] == request().constraints.max_tokens
    schema = seen["response_format"]["json_schema"]["schema"]
    assert schema["properties"]["issues"]["maxItems"] == 5
    objection, other = schema["properties"]["issues"]["items"]["anyOf"]
    assert objection["properties"]["use_id"]["enum"] == ["U1"]  # only the unit ids of this answer
    assert (
        objection["properties"]["card_ids"]["minItems"] == 1
        and other["properties"]["card_ids"]["minItems"] == 0
    )
    assert objection["properties"]["kind"]["enum"] == ["contradiction", "wrong_concept"]
    assert objection["properties"]["card_ids"]["items"]["enum"] == ["C1"]  # only the cards of these sources
    assert outcome.ok and outcome.text == '{"issues":[]}' and outcome.adapter == "llama_server"
    assert outcome.parameters["output_tokens"] == 40 and outcome.parameters["cached_tokens"] == 100
    assert (
        outcome.parameters["schema_constrained"] == 1 and "pensando" not in outcome.text
    )  # reasoning never leaks


@pytest.mark.asyncio
async def test_length_deadline_and_server_failures_are_mapped_not_swallowed():
    def length(req):
        return httpx.Response(200, json=reply(finish="length"))

    out = await LlamaServerProvider(model_label="m", thinking=False, client=server(length)).generate(
        request()
    )
    assert out.finish_reason == "length"

    def slow(req):
        raise httpx.ReadTimeout("late")

    out = await LlamaServerProvider(model_label="m", thinking=False, client=server(slow)).generate(request())
    assert not out.ok and out.finish_reason == "deadline"

    def down(req):
        raise httpx.ConnectError("refused")

    with pytest.raises(GenerationError, match="unavailable"):
        await LlamaServerProvider(model_label="m", thinking=False, client=server(down)).generate(request())

    def broken(req):
        return httpx.Response(500)

    with pytest.raises(GenerationError, match="500"):
        await LlamaServerProvider(model_label="m", thinking=False, client=server(broken)).generate(request())


def test_only_loopback_servers_and_explicit_flags_are_accepted():
    with pytest.raises(ValueError, match="loopback"):
        LlamaServerProvider("http://192.168.1.5:8089", model_label="m", thinking=True)
    with pytest.raises(ValueError):
        LlamaServerProvider(model_label="m", thinking="yes")


@pytest.mark.asyncio
async def test_the_provider_plugs_into_the_compact_reviewer_without_changes():
    from oralia.course_dialogue.concept_review_loop import ConceptLedgerReviewer
    from oralia.course_dialogue.lab_request import RepairGenerationRequest
    from oralia.course_dialogue.review_repair import CallBudget

    def handler(req):
        issue = dict(use_id="U1", kind="contradiction", card_ids=["C1"], verdict="incorrect", reason="x")
        return httpx.Response(200, json=reply(json.dumps({"issues": [issue]})))

    provider = LlamaServerProvider(
        model_label="q", thinking=True, schemas=review_schemas(), client=server(handler)
    )
    reviewer = ConceptLedgerReviewer(
        None, provider, budget=CallBudget(maximum=3), revalidate=lambda: None, prompt_version=COMPACT_VERSION
    )
    base = RepairGenerationRequest(
        purpose="explicacion", instruction="t", student_input="Pregunta", evidence=evidence()
    )
    trace = await reviewer.review(base, "Una respuesta.")
    assert trace["status"] == "issues_found" and trace["calls"][0]["outcome"]["adapter"] == "llama_server"


@pytest.mark.asyncio
async def test_a_finite_web_control_is_forced_to_one_exact_alternative_and_marked_finite():
    seen = {}

    def handler(req):
        seen.update(json.loads(req.content))
        return httpx.Response(200, json=reply('{"status": "unknown", "concept": null}'))

    ask = request().model_copy(
        update={"output_schema": {"type": "object", "x-oralia-finite-outputs": ['{"status": "unknown", "concept": null}']}}
    )
    outcome = await LlamaServerProvider(model_label="m", thinking=False, client=server(handler)).generate(ask)
    assert seen["grammar"] == 'root ::= "{\\"status\\": \\"unknown\\", \\"concept\\": null}"'
    assert "response_format" not in seen
    assert outcome.parameters["finite_decoder"] == 1 and outcome.parameters["finite_after_thinking"] == 1


@pytest.mark.asyncio
async def test_a_busy_server_error_is_retried_once_but_a_client_error_is_not():
    calls = []

    def busy_then_ok(req):
        calls.append(1)
        return httpx.Response(503 if len(calls) == 1 else 200, json=reply())

    provider = LlamaServerProvider(model_label="m", thinking=False, client=server(busy_then_ok), retries=1)
    assert (await provider.generate(request())).ok and len(calls) == 2
    broken = LlamaServerProvider(model_label="m", thinking=False, client=server(lambda r: httpx.Response(400)), retries=1)
    with pytest.raises(GenerationError):
        await broken.generate(request())


def sse(*chunks):
    lines = [f"data: {json.dumps(c)}\n\n" for c in chunks] + ["data: [DONE]\n\n"]
    return "".join(lines).encode()


@pytest.mark.asyncio
async def test_a_streamed_reply_reports_each_piece_and_returns_the_same_outcome_as_a_whole_reply():
    seen_body = {}

    def handler(req):
        seen_body.update(json.loads(req.content))
        body = sse(
            {"choices": [{"delta": {"content": "Hola"}, "finish_reason": None}]},
            {"choices": [{"delta": {"content": " mundo"}, "finish_reason": None}]},
            {"choices": [{"delta": {}, "finish_reason": "stop"}]},
            {"choices": [], "usage": {"prompt_tokens": 120, "completion_tokens": 3}},
        )
        return httpx.Response(200, content=body, headers={"content-type": "text/event-stream"})

    pieces = []
    provider = LlamaServerProvider(model_label="m", thinking=False, client=server(handler))
    outcome = await provider.generate_stream(request(), pieces.append)
    assert pieces == ["Hola", "Hola mundo"] and outcome.text == "Hola mundo" and outcome.ok
    assert seen_body["stream"] is True and seen_body["stream_options"] == {"include_usage": True}
    assert outcome.parameters["input_tokens"] == 120 and outcome.parameters["output_tokens"] == 3


@pytest.mark.asyncio
async def test_a_stream_cut_after_text_arrived_is_an_error_not_a_silent_partial_answer():
    def handler(req):
        raise httpx.RemoteProtocolError("cut")

    provider = LlamaServerProvider(model_label="m", thinking=False, client=server(handler), retries=0)
    with pytest.raises(GenerationError):
        await provider.generate_stream(request(), lambda text: None)
