"""Use each historical adapter snapshot, never attribute later fixes to earlier runs."""

import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

from oralia.course_dialogue.scope_control_messages import ScopeControlRequest
from oralia.infrastructure.generation.generation_port import GenerationRequest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "cpu-effective-scope-traces-v1.json"


async def reconstruct(run, record_index, snapshot):
    records = json.loads((EVIDENCE / run / "records.json").read_text(encoding="utf-8"))
    record = records[record_index]
    attempt = record["attempts"][0] if "attempts" in record else record
    worker = json.loads((EVIDENCE / run / "worker.json").read_text(encoding="utf-8"))
    source = EVIDENCE / snapshot / "src/oralia/course_dialogue/cached_transformers.py"
    worker_source = EVIDENCE / snapshot / "src/oralia/course_dialogue/gpu_worker.py"
    spec = importlib.util.spec_from_file_location("historical_cached_adapter", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    control = "control_step" in attempt["request"]
    request = (ScopeControlRequest if control else GenerationRequest).model_validate(attempt["request"])

    class Process:
        returncode = None

        def __init__(self):
            self.frame = None
            self.stdin = SimpleNamespace(write=self.write, drain=self.drain)
            self.stdout = SimpleNamespace(readline=self.readline)

        def write(self, data):
            self.frame = json.loads(data)

        async def drain(self):
            pass

        async def readline(self):
            reply = json.loads(attempt["exchange"]["raw_worker_response"])
            reply["id"] = self.frame["id"]
            return json.dumps(reply).encode()

        def terminate(self):
            self.returncode = 0

    process = Process()
    options = {"message_profile": "scope-control/v1"} if control else {}
    await module.CachedTransformersGenerationAdapter(process, **options).generate(request)
    data = json.loads(request.student_input)
    question = record["input"]["text"]
    assert data["question"] == question
    policy_path = EVIDENCE / "course-scope-policy-v1.json"
    assert data["policy_sha256"] == hashlib.sha256(policy_path.read_bytes()).hexdigest()
    descriptions = data.get("blocks") or data.get("block_descriptions")
    if descriptions is not None:
        assert descriptions == json.loads(
            (EVIDENCE / "course-block-descriptions-v1.json").read_text(encoding="utf-8")
        )
    if attempt.get("outcome"):
        assert process.frame["max_tokens"] == attempt["outcome"]["parameters"]["max_tokens"]
    assert process.frame["deadline_ms"] == attempt["exchange"]["deadline_ms"]
    interpreted = record.get("result", {}).get("assessment") or record.get("assessment")
    return {
        "run": run,
        "id": record["id"],
        "literal_question": question,
        "adapter_snapshot": str(source.relative_to(ROOT)),
        "worker_snapshot": str(worker_source.relative_to(ROOT)),
        "adapter_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "worker_sha256": hashlib.sha256(worker_source.read_bytes()).hexdigest(),
        "frame": process.frame,
        "original_outcome": attempt.get("outcome"),
        "original_raw_result": json.loads(attempt["exchange"]["raw_worker_response"]),
        "original_raw_backend_response": attempt["exchange"]["raw_worker_response"],
        "original_host_decision": interpreted,
        "original_host_error": record.get("error"),
        "original_selection": record.get("selection"),
        "worker": worker,
        "policy_hash_matches": True,
        "descriptions_present_and_match": descriptions is not None,
        "empty_evidence_rule_in_actual_user": (
            "Responde únicamente usando el contenido de las etiquetas <evidencia>"
            in process.frame["messages"][-1]["content"]
        ),
    }


async def main():
    if OUTPUT.exists():
        raise ValueError("preserve CPU trace audit")
    definitions = [
        ("scope-classifier-resource-v2", 0, "scope-classifier-frozen-v1/code"),
        ("scope-classifier-resource-v2", 1, "scope-classifier-frozen-v1/code"),
        ("scope-v2-described-first", 0, "scope-v2-described-proposal-v1-final/artifacts"),
        ("scope-finite-capacity-first", 0, "scope-finite-capacity-v1/artifacts"),
        ("scope-control-diagnostic-resource-run", 0, "scope-control-diagnostic-resource-v2/artifacts"),
    ]
    rows = [await reconstruct(*definition) for definition in definitions]
    OUTPUT.write_text(
        json.dumps(
            {
                "kind": "historical_snapshot_reconstruction_not_original_pipe_capture",
                "traces": rows,
                "new_model_calls": 0,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Five historical traces reconstructed from their own snapshots.")


if __name__ == "__main__":
    asyncio.run(main())
