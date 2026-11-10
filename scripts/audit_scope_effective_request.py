"""Reconstruct the frozen adapter frame offline; preserve its original request and response."""

import asyncio
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.infrastructure.generation.generation_port import GenerationRequest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-effective-request-audit-v1.json"


async def main():
    if OUTPUT.exists():
        raise ValueError("preserve original audit")
    record = json.loads((EVIDENCE / "scope-finite-capacity-first/records.json").read_text(encoding="utf-8"))[
        0
    ]
    attempt = record["attempts"][0]
    request = GenerationRequest.model_validate(attempt["request"])
    payload = json.loads(request.student_input)
    assert payload["question"] == "Sitúa la Ingeniería del Software como disciplina."
    assert payload["blocks"] == json.loads(
        (EVIDENCE / "course-block-descriptions-v1.json").read_text(encoding="utf-8")
    )
    assert (
        payload["policy_sha256"]
        == hashlib.sha256((EVIDENCE / "course-scope-policy-v1.json").read_bytes()).hexdigest()
    )
    assert (
        payload["metadata_sha256"]
        == hashlib.sha256((EVIDENCE / "course-block-descriptions-v1.json").read_bytes()).hexdigest()
    )
    assert payload["selected_shown_history"] == [] and request.evidence == []

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
            value = json.loads(attempt["exchange"]["raw_worker_response"])
            value["id"] = self.frame["id"]  # synthetic transport ID, never a new model response
            return json.dumps(value).encode()

        def terminate(self):
            self.returncode = 0

    process = Process()
    await CachedTransformersGenerationAdapter(process).generate(request)
    messages = process.frame["messages"]
    assert [m["role"] for m in messages] == ["system", "user"]
    empty_evidence_rule = "Responde únicamente usando el contenido de las etiquetas <evidencia> anteriores"
    assert empty_evidence_rule in messages[1]["content"]
    assert "<evidencia documento=" not in messages[1]["content"]
    assert len(process.frame["finite_outputs"]) == 120
    result = {
        "kind": "offline_frame_reconstruction_not_original_pipe_capture",
        "frame": process.frame,
        "original_attempt": attempt,
        "frozen_adapter_sha256": hashlib.sha256(
            (ROOT / "src/oralia/course_dialogue/cached_transformers.py").read_bytes()
        ).hexdigest(),
        "question_policy_metadata_match": True,
        "oracle_in_request": False,
        "message_roles": ["system", "user"],
        "history_messages": 0,
        "empty_academic_evidence_constraint_in_control_request": True,
        "conflict_reproduced": True,
        "caused_semantic_error_proved": False,
        "new_inferences": 0,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Offline original frame reconstructed; empty-evidence restriction on scope control reproduced.")


if __name__ == "__main__":
    asyncio.run(main())
