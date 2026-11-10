"""Execute the five frozen raw frames once using the existing owned GPU worker."""

import asyncio
import hashlib
import json
import time
from pathlib import Path

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_7B, cached_provider
from oralia.course_dialogue.gpu_resource_policy import preflight
from scripts.trial_course_scope import save, snapshot

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKAGE = EVIDENCE / "minimal-capacity-probe-v1"
OUTPUT = EVIDENCE / "minimal-capacity-probe-run-2026-10-27"


def verify():
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["workspace_files"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    for name, expected in manifest["external_metadata"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, name
    return {
        "verified_files": 49,
        "manifest_sha256": hashlib.sha256((PACKAGE / "manifest.json").read_bytes()).hexdigest(),
    }


async def main():
    verified = verify()
    OUTPUT.mkdir(exist_ok=False)
    save(OUTPUT / "verification.json", verified)
    frames = json.loads((PACKAGE / "frames.json").read_text(encoding="utf-8"))
    expected = {r["id"]: r for r in json.loads((PACKAGE / "cpu-tokenizer-check.json").read_text())["frames"]}
    resources, records = [], []
    budget = {
        "diagnostic_requests_reserved": 0,
        "diagnostic_tokens_reserved": 0,
        "warmup_maximum": 1,
        "warmup_confirmed": 0,
        "total_generate_maximum": 6,
        "new_tokens_maximum": 577,
        "retries": 0,
    }

    async def sample(stage):
        value = await snapshot()
        resources.append({**value, "stage": stage})
        save(OUTPUT / "resources.json", resources)
        return value

    for _ in range(5):
        await sample("before")
        await asyncio.sleep(1)
    decision = preflight(resources)
    save(OUTPUT / "preflight.json", decision)
    if not decision["ready"]:
        print("Resource preflight refused; no weights loaded", flush=True)
        return
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(str(CACHED_MODEL_7B), local_files_only=True)
    prompts = []
    for frame in frames:
        prompt = tokenizer.apply_chat_template(frame["messages"], tokenize=False, add_generation_prompt=True)
        digest = hashlib.sha256(prompt.encode()).hexdigest()
        assert digest == expected[frame["id"]]["prompt_sha256"]
        prompts.append({"id": frame["id"], "prompt": prompt, "sha256": digest})
    save(OUTPUT / "rendered-prompts.json", prompts)
    done = asyncio.Event()

    async def monitor():
        while not done.is_set():
            try:
                await sample("during")
            except Exception as error:
                resources.append({"stage": "during", "error": type(error).__name__})
            try:
                await asyncio.wait_for(done.wait(), timeout=1)
            except TimeoutError:
                pass

    task = asyncio.create_task(monitor())
    try:
        save(OUTPUT / "budget.json", budget)
        async with cached_provider(OUTPUT, source=CACHED_MODEL_7B, quantization="nf4") as provider:
            budget["warmup_confirmed"] = 1
            save(OUTPUT / "budget.json", budget)
            for frame in frames:
                budget["diagnostic_requests_reserved"] += 1
                budget["diagnostic_tokens_reserved"] += frame["max_tokens"]
                assert (
                    budget["diagnostic_requests_reserved"] <= 5
                    and budget["diagnostic_tokens_reserved"] <= 576
                )
                save(OUTPUT / "budget.json", budget)
                record = {
                    "sent_frame": frame,
                    "expected_prompt_sha256": expected[frame["id"]]["prompt_sha256"],
                }
                records.append(record)
                save(OUTPUT / "records.json", records)
                started = time.monotonic()
                provider.process.stdin.write((json.dumps(frame, ensure_ascii=False) + "\n").encode())
                await provider.process.stdin.drain()
                raw = await asyncio.wait_for(provider.process.stdout.readline(), timeout=32)
                record.update(raw_worker_response=raw.decode(), wall_seconds=time.monotonic() - started)
                save(OUTPUT / "records.json", records)
                reply = json.loads(raw)
                assert reply.get("id") == frame["id"] and reply.get("type") == "result", reply
                assert reply["input_tokens"] == expected[frame["id"]]["input_tokens"]
                assert reply["message_profile"] == frame["message_profile"]
                assert reply["finite_decoder"] == (frame["finite_outputs"] is not None)
                assert reply.get("generation_state") is not None
                print(
                    json.dumps(
                        {"id": frame["id"], "text": reply["text"], "finish": reply["finish_reason"]},
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if reply["finish_reason"] != "stop":
                    raise RuntimeError("incomplete response; remaining calls not executed")
    except Exception as error:
        save(OUTPUT / "failure.json", {"type": type(error).__name__, "detail": str(error)})
        raise
    finally:
        done.set()
        await task
        await sample("after")
        save(OUTPUT / "unexecuted.json", [f["id"] for f in frames[len(records) :]])


if __name__ == "__main__":
    asyncio.run(main())
