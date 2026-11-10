"""GenerationPort over a local llama.cpp server (OpenAI-compatible endpoint); loopback only, never a download.

Why: eager Transformers decoding was CPU-bound (~20 tok/s) and the CUDA-graph decoder reached ~100 tok/s on
the 8B. llama.cpp measures 240 tok/s (8B) and 146 tok/s (14B) on the same GPU, with prefix caching, parallel
slots and JSON-schema constrained output (applied to the final answer only, after the reasoning). In the first
test the constrained output removed every contract failure of the reviewer (0 against 15 of 53 cases).

The server is started by the caller (see docs/CONTINUAR.md); this class only talks to it.
"""

import asyncio
import json
import time
from urllib.parse import urlsplit

import httpx

from oralia.infrastructure.generation.generation_port import GenerationError, GenerationOutcome

NO_THINKING_SAMPLING = dict(temperature=0.7, top_p=0.8, top_k=20)
THINKING_SAMPLING = dict(
    temperature=0.6, top_p=0.95, top_k=20
)  # Qwen3 recommended; greedy loops in thinking mode


def review_schemas():
    """Per-request schema builders of the registered review contracts, keyed by prompt version."""
    from oralia.course_dialogue.concept_ledger import COMPACT_VERSION, compact_response_schema
    from oralia.course_dialogue.grounding_review import GROUNDING_VERSION, grounding_response_schema

    return {COMPACT_VERSION: compact_response_schema, GROUNDING_VERSION: grounding_response_schema}


def finite_grammar(alternatives):
    """GBNF accepting exactly one of the given strings."""

    def literal(text):
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'

    return "root ::= " + " | ".join(literal(a) for a in alternatives)


class LlamaServerProvider:
    last_exchange = None

    def __init__(
        self,
        base_url="http://127.0.0.1:8089",
        *,
        model_label,
        thinking,
        seed=42,
        sampling=None,
        schemas=None,
        client=None,
        retries=1,
    ):
        host = urlsplit(base_url).hostname
        if host not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("the llama.cpp server must be on the loopback interface")
        if type(thinking) is not bool or type(seed) is not int:
            raise ValueError("thinking and seed must be explicit")
        self.base_url = base_url.rstrip("/")
        self.model_label, self.thinking, self.seed = model_label, thinking, seed
        self.sampling = dict(sampling or (THINKING_SAMPLING if thinking else NO_THINKING_SAMPLING))
        self.schemas = {} if schemas is None else dict(schemas)
        self.client, self.retries = client, retries

    def _body(self, request):
        constraints = request.constraints
        body = dict(
            messages=request.effective_messages(),
            max_tokens=constraints.max_tokens,
            seed=self.seed,
            chat_template_kwargs={"enable_thinking": self.thinking},
            cache_prompt=True,
            **self.sampling,
        )
        schema = self.schemas.get(getattr(request, "prompt_version", None))
        if callable(schema):
            schema = schema(request)
        finite = (getattr(request, "output_schema", None) or {}).get("x-oralia-finite-outputs")
        if finite:
            # Web controls choose among exact bound alternatives: a grammar of literal strings enforces that.
            body["grammar"] = finite_grammar(finite)
        elif schema is not None:
            body["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "review", "schema": schema, "strict": True},
            }
        return body, schema, finite

    def _deadline_outcome(self, started):
        return GenerationOutcome(
            ok=False,
            text="",
            adapter="llama_server",
            finish_reason="deadline",
            model=self.model_label,
            latency_ms=int((time.monotonic() - started) * 1000),
        )

    async def generate(self, request):
        constraints = request.constraints
        body, schema, finite = self._body(request)
        timeout = max(1.0, constraints.deadline_ms / 1000)
        started = time.monotonic()
        owned = self.client is None
        client = self.client or httpx.AsyncClient()
        try:
            for attempt in range(self.retries + 1):
                try:
                    response = await client.post(
                        f"{self.base_url}/v1/chat/completions", json=body, timeout=timeout
                    )
                    response.raise_for_status()
                    break
                except (httpx.ConnectError, httpx.RemoteProtocolError) as exc:
                    if attempt == self.retries:
                        raise GenerationError(f"llama.cpp server unavailable: {type(exc).__name__}") from exc
                except httpx.TimeoutException:
                    return self._deadline_outcome(started)
                except httpx.HTTPStatusError as exc:
                    # 5xx under load (no free cache space for a moment): one more try before giving up.
                    if exc.response.status_code >= 500 and attempt < self.retries:
                        await asyncio.sleep(2.0)
                        continue
                    raise GenerationError(f"llama.cpp server error {exc.response.status_code}") from exc
        finally:
            if owned:
                await client.aclose()
        return self._outcome(response.json(), constraints, schema, finite, started)

    def _outcome(self, data, constraints, schema, finite, started):
        choice = data["choices"][0]
        message, usage = choice["message"], data.get("usage", {})
        elapsed = int((time.monotonic() - started) * 1000)
        reason = {"stop": "stop", "length": "length"}.get(choice.get("finish_reason"), "stop")
        self.last_exchange = dict(
            stage="complete", latency_ms=elapsed, finish_reason=choice.get("finish_reason")
        )
        return GenerationOutcome(
            ok=True,
            text=message.get("content") or "",
            adapter="llama_server",
            finish_reason=reason,
            model=self.model_label,
            parameters=dict(
                max_tokens=constraints.max_tokens,
                input_tokens=int(usage.get("prompt_tokens", 0)),
                output_tokens=int(usage.get("completion_tokens", 0)),
                reasoning_chars=len(message.get("reasoning_content") or ""),
                cached_tokens=int((usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0)),
                seed=self.seed,
                temperature=self.sampling.get("temperature", 0),
                schema_constrained=int(schema is not None or bool(finite)),
                finite_decoder=int(bool(finite)),
                finite_after_thinking=int(bool(finite)),
                thinking_enabled=int(self.thinking),
            ),
            latency_ms=elapsed,
        )

    async def generate_stream(self, request, on_text):
        """Same contract as `generate`, reading the reply as it is produced; `on_text(text_so_far)` after each piece.

        The caller shows the partial text to the student while the rest is still being written.
        """
        constraints = request.constraints
        body, schema, finite = self._body(request)
        body.update(stream=True, stream_options={"include_usage": True})
        timeout = max(1.0, constraints.deadline_ms / 1000)
        started = time.monotonic()
        owned = self.client is None
        client = self.client or httpx.AsyncClient()
        text, reasoning, finish, usage = [], [], None, {}
        try:
            for attempt in range(self.retries + 1):
                try:
                    async with asyncio.timeout(timeout):
                        async with client.stream(
                            "POST", f"{self.base_url}/v1/chat/completions", json=body, timeout=timeout
                        ) as response:
                            response.raise_for_status()
                            async for line in response.aiter_lines():
                                if not line.startswith("data:"):
                                    continue
                                payload = line[5:].strip()
                                if payload == "[DONE]":
                                    break
                                chunk = json.loads(payload)
                                usage = chunk.get("usage") or usage
                                for choice in chunk.get("choices") or []:
                                    delta = choice.get("delta") or {}
                                    if delta.get("content"):
                                        text.append(delta["content"])
                                        on_text("".join(text))
                                    if delta.get("reasoning_content"):
                                        reasoning.append(delta["reasoning_content"])
                                    finish = choice.get("finish_reason") or finish
                    break
                except (httpx.ConnectError, httpx.RemoteProtocolError) as exc:
                    if text or attempt == self.retries:
                        raise GenerationError(f"llama.cpp server unavailable: {type(exc).__name__}") from exc
                except (httpx.TimeoutException, TimeoutError):
                    return self._deadline_outcome(started)
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code >= 500 and attempt < self.retries and not text:
                        await asyncio.sleep(2.0)
                        continue
                    raise GenerationError(f"llama.cpp server error {exc.response.status_code}") from exc
        finally:
            if owned:
                await client.aclose()
        data = dict(
            choices=[dict(message=dict(content="".join(text), reasoning_content="".join(reasoning)), finish_reason=finish)],
            usage=usage,
        )
        return self._outcome(data, constraints, schema, finite, started)
