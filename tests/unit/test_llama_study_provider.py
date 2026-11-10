"""CPU composition test: the study session runs on llama.cpp servers (simulated), with the notice review."""

import json
import uuid

import httpx
import pytest

from oralia.documentary.llama_study_provider import LlamaStudyProvider
from oralia.documentary.study_lab import DiagnosticStudy
from tests.unit.test_study_lab import RetrievalFixture


def chat(content, reasoning=""):
    return {
        "choices": [
            {"message": {"content": content, "reasoning_content": reasoning}, "finish_reason": "stop"}
        ],
        "usage": {"prompt_tokens": 50, "completion_tokens": 20},
    }


def servers(verdict, seen):
    def handler(request):
        url = str(request.url)
        if url.endswith("/health"):
            return httpx.Response(200, json={"status": "ok"})
        body = json.loads(request.content)
        seen.append((request.url.port, body))
        if request.url.port == 8090:
            if body.get("stream"):  # the answer is streamed so the student can read it while it is written
                pieces = ["Una respuesta", " del generador."]
                events = [{"choices": [{"delta": {"content": t}, "finish_reason": None}]} for t in pieces]
                events += [{"choices": [{"delta": {}, "finish_reason": "stop"}]}, {"choices": [], "usage": {"prompt_tokens": 50, "completion_tokens": 5}}]
                data = "".join(f"data: {json.dumps(e)}\n\n" for e in events) + "data: [DONE]\n\n"
                return httpx.Response(200, content=data.encode(), headers={"content-type": "text/event-stream"})
            return httpx.Response(200, json=chat("Una respuesta del generador."))
        return httpx.Response(200, json=chat(json.dumps(verdict), reasoning="razonamiento interno"))

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


async def turn(tmp_path, verdict, seen):
    provider = LlamaStudyProvider(
        tmp_path / "runtime", client=servers(verdict, seen), seconds=600, notice_log=tmp_path / "avisos.jsonl"
    )
    await provider._prepare(lambda: None)
    assert provider.ready and provider.diagnostic_label.startswith("LLAMA_CPP")
    # Web controls run on the generator server, not on the reviewer (the 24B misjudged scope).
    assert provider.control_adapter.base_url == provider.adapter.base_url != provider.critic_adapter.base_url
    lab = DiagnosticStudy(
        RetrievalFixture(),
        provider,
        authority=lambda: True,
        budget=provider.trial_budget,
        course="t",
        activity="t",
    )
    row = await lab.turn("Explica el requisito", str(uuid.uuid4()))
    return lab, row, provider


@pytest.mark.asyncio
async def test_a_turn_runs_on_the_two_servers_and_shows_the_notice_for_a_verified_kind(tmp_path):
    issue = dict(
        use_id="U1", kind="contradiction", card_ids=["C1"], verdict="incorrect", reason="solo docente"
    )
    seen = []
    lab, row, provider = await turn(tmp_path, {"issues": [issue]}, seen)
    receipt = lab.display(row["id"])
    assert receipt["diagnostic_preview"] == "Una respuesta del generador."
    assert [i["kind"] for i in receipt["review_notice"]["items"]] == ["contradiction"]
    ports = [p for p, _ in seen]
    assert ports == [8090, 8089]  # one generation, one review: no repair, no retry
    generation, review = seen[0][1], seen[1][1]
    assert generation["temperature"] == 0.0 and generation["chat_template_kwargs"] == {
        "enable_thinking": False
    }
    assert review["chat_template_kwargs"] == {"enable_thinking": False} and "response_format" in review
    assert review["temperature"] == 0.15
    assert "razonamiento interno" not in json.dumps(receipt["review_notice"])
    entries = [json.loads(line) for line in (tmp_path / "avisos.jsonl").read_text(encoding="utf8").splitlines()]
    assert len(entries) == 1 and entries[0]["notice_kinds"] == ["contradiction"]
    assert entries[0]["question"] == "Explica el requisito" and entries[0]["answer"] == "Una respuesta del generador."
    assert entries[0]["reviewer_findings"][0]["reason"] == "solo docente"


@pytest.mark.asyncio
async def test_a_clean_review_shows_no_notice_and_an_unavailable_server_blocks_startup(tmp_path):
    lab, row, _ = await turn(tmp_path, {"issues": []}, [])
    assert lab.display(row["id"])["review_notice"] is None
    assert not (tmp_path / "avisos.jsonl").exists()  # nothing to tell, nothing logged

    def down(request):
        return httpx.Response(503)

    provider = LlamaStudyProvider(
        tmp_path / "other", client=httpx.AsyncClient(transport=httpx.MockTransport(down))
    )
    with pytest.raises(ValueError, match="not available"):
        await provider._prepare(lambda: None)
    assert not provider.ready
