"""Study provider whose generator and reviewer are local llama.cpp servers; no model is loaded in-process.

The reviewer (default Mistral-Small-24B, no reasoning) runs with schema-constrained output. Startup is immediate (the servers keep the models resident) and decoding is 2-3x faster than the in-process
runtime. Same session contract as RealStudyProvider, always in the reviewed runtime with the notice mode
(the answer plus a fixed notice when the review finds an error).
"""

import asyncio
import json
import time
from pathlib import Path
from contextlib import asynccontextmanager

import httpx

from oralia.course_dialogue.llama_server_provider import LlamaServerProvider, review_schemas
from oralia.documentary.gpu_turns import GroupExclusion, TurnTakingProvider
from oralia.documentary.real_study_provider import RealStudyProvider

NOTICE_LOG = Path(__file__).resolve().parents[3] / "registro-avisos/avisos.jsonl"
GREEDY = dict(temperature=0.0, top_p=1.0, top_k=1)
# Reviewer configuration measured overnight (06-11-2026): Mistral-Small-24B, no reasoning, schema-constrained.
REVIEWER_SAMPLING = dict(temperature=0.15, top_p=1.0, top_k=0)


class LlamaStudyProvider(RealStudyProvider):
    MAX_RUNTIME_SECONDS = 4 * 3600  # a class shift; the services keep the models resident
    diagnostic_label = "LLAMA_CPP_QWEN25_14B_MISTRAL24B_NOTICE_REVIEW"

    def __init__(
        self,
        output,
        *,
        generator_url="http://127.0.0.1:8090",
        reviewer_url="http://127.0.0.1:8089",
        notice_log=NOTICE_LOG,
        concurrency=4,
        reviewer_label="mistral24b-q4",
        reviewer_thinking=False,
        reviewer_sampling=REVIEWER_SAMPLING,
        client=None,
        **kwargs,
    ):
        kwargs.setdefault("reviewed", True)
        kwargs["notice_review"] = True
        super().__init__(output, **kwargs)
        # Several students at once: up to `concurrency` turns in flight (the servers need that many slots).
        self.review_lock = asyncio.Semaphore(concurrency)
        self.concurrency = concurrency
        self.generator_url, self.reviewer_url, self.client = generator_url, reviewer_url, client
        self.notice_log = notice_log
        self.reviewer_options = dict(
            model_label=reviewer_label, thinking=reviewer_thinking, sampling=reviewer_sampling
        )
        self.diagnostic_label = LlamaStudyProvider.diagnostic_label

    async def _healthy(self, url):
        client = self.client or httpx.AsyncClient()
        try:
            response = await client.get(url.rstrip("/") + "/health", timeout=5)
            return response.status_code == 200
        except httpx.HTTPError:
            return False
        finally:
            if self.client is None:
                await client.aclose()

    async def coverage(self, question, texts):
        """SI / PARCIAL / NO (or None if it could not be decided): do the passages hold what was asked?"""
        from oralia.documentary import coverage_check

        client = self.client or httpx.AsyncClient()
        url = self.reviewer_url.rstrip("/") + "/v1/chat/completions"

        async def ask(prompt):
            body = {"messages": coverage_check.messages(question, texts, prompt), "temperature": 0, "max_tokens": 6}
            response = await client.post(url, json=body, timeout=60)
            return response.json()["choices"][0]["message"]["content"]

        try:
            async with self.exclusion.use("reviewer"):
                general = coverage_check.parse(await ask(coverage_check.PROMPT))
                central = coverage_check.absent(await ask(coverage_check.PROMPT_CENTRAL))
            return "NO" if general == "NO" or central else general
        except (httpx.HTTPError, KeyError, ValueError, IndexError):
            return None
        finally:
            if self.client is None:
                await client.aclose()

    async def health_report(self):
        """Estado de los dos servidores llama.cpp para `/health`."""
        return {
            "generator": await self._healthy(self.generator_url),
            "reviewer": await self._healthy(self.reviewer_url),
        }

    async def _prepare(self, revalidate):
        async with self._lock:
            revalidate()
            if self.ready:
                return
            for name, url in (("generator", self.generator_url), ("reviewer", self.reviewer_url)):
                if not await self._healthy(url):
                    raise ValueError(f"llama.cpp {name} server is not available at {url}")
            self.adapter = LlamaServerProvider(
                self.generator_url,
                model_label="qwen25-14b-q4",
                thinking=False,
                seed=42,
                sampling=GREEDY,
                client=self.client,
            )
            self.critic_adapter = LlamaServerProvider(
                self.reviewer_url,
                **self.reviewer_options,
                seed=42,
                schemas=review_schemas(),
                client=self.client,
            )
            # Scope and web controls: Qwen2.5-14B judged 10/10 in-scope and 5/5 out-of-scope questions; the
            # 24B reviewer rejected 3 of 10 in-scope ones (docs/audits/2026-11-07-false-alarms/judge_scope.py).
            self.control_adapter = LlamaServerProvider(
                self.generator_url,
                model_label="qwen25-14b-q4",
                thinking=False,
                seed=42,
                sampling=GREEDY,
                client=self.client,
            )
            exclusion = self.exclusion = GroupExclusion()  # generator and web controls share the 14B server; the reviewer is the 24B
            self.adapter = TurnTakingProvider(self.adapter, exclusion, "generator")
            self.control_adapter = TurnTakingProvider(self.control_adapter, exclusion, "generator")
            self.critic_adapter = TurnTakingProvider(self.critic_adapter, exclusion, "reviewer")
            self._loads += 1
            revalidate()

    async def _close_worker(self):
        self.adapter = self.critic_adapter = self.control_adapter = None

    @asynccontextmanager
    async def lifespan(self, app):
        self.output.mkdir(parents=True, exist_ok=False)

        async def expire():
            await asyncio.sleep(max(0, self.deadline - time.monotonic()))
            app.state.request_shutdown()

        task = asyncio.create_task(expire())
        try:
            async with asyncio.timeout_at(self.deadline):
                await self._prepare(lambda: None)
            (self.output / "llama-servers.json").write_text(
                json.dumps({"generator": self.generator_url, "reviewer": self.reviewer_url}), encoding="utf8"
            )
            yield
        finally:
            task.cancel()
            if self._preparation is not None:
                self._preparation.cancel()
                await asyncio.gather(self._preparation, return_exceptions=True)
            await asyncio.gather(task, return_exceptions=True)
            await self._close_worker()
