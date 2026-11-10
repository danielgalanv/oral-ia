"""Capture actual adapter serialization over simulated pipes, never model inference."""

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.scope_control_messages import ScopeControlRequest
from oralia.course_dialogue.scope_message_profiles import INSTRUCTIONS, validate_frame_profile
from oralia.infrastructure.generation.generation_port import EvidenceItem, GenerationRequest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-control-transport-frames-v1.json"


class Pipe:
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
        profile = validate_frame_profile(self.frame)
        return json.dumps(
            {
                "type": "result",
                "id": self.frame["id"],
                "text": "simulated transport only",
                "finish_reason": "stop",
                "input_tokens": 1,
                "output_tokens": 1,
                "latency_ms": 0,
                "finite_decoder": self.frame["finite_outputs"] is not None,
                "message_profile": profile,
            }
        ).encode()

    def terminate(self):
        self.returncode = 0


async def main():
    if OUTPUT.exists():
        raise ValueError("preserve frames")
    audit = json.loads((EVIDENCE / "scope-effective-request-audit-v1.json").read_text(encoding="utf-8"))
    target = ScopeControlRequest.model_validate(
        {**audit["original_attempt"]["request"], "control_step": "target"}
    )
    ref = ScopeControlRequest(
        purpose="explicacion",
        control_step="referent",
        instruction=INSTRUCTIONS["referent"],
        student_input=json.dumps({"question": "¿Por qué?", "shown_history": []}),
        output_schema={"type": "object", "x-oralia-finite-outputs": ['{"referent":"none"}']},
    )
    literal = ScopeControlRequest(
        purpose="explicacion",
        control_step="literal",
        instruction=INSTRUCTIONS["literal"],
        student_input=json.dumps(
            {
                "question": "pruebas y seguridad",
                "selected_target": {"intent": "mixed"},
                "role": "included_part",
            }
        ),
    )
    academic = GenerationRequest(
        purpose="explicacion",
        instruction="Academic fixture using authorized evidence",
        student_input="Synthetic question",
        evidence=[
            EvidenceItem(
                fragment_id="fixture", text="Synthetic passage", document_id="fixture", document_version=1
            )
        ],
    )
    records = []
    for label, request, profile in [
        ("target", target, "scope-control/v1"),
        ("referent", ref, "scope-control/v1"),
        ("literal", literal, "scope-control/v1"),
        ("academic", academic, "academic/v1"),
    ]:
        pipe = Pipe()
        adapter = CachedTransformersGenerationAdapter(pipe, message_profile=profile)
        await adapter.generate(request)
        records.append({"label": label, "frame": pipe.frame, "exchange": adapter.last_exchange})
    OUTPUT.write_text(
        json.dumps(
            {
                "kind": "actual_adapter_frames_simulated_transport_no_model",
                "frames": records,
                "model_inferences": 0,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Four serialized frames captured; no model called.")


if __name__ == "__main__":
    asyncio.run(main())
