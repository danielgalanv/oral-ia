"""Small, unpublished free-form scope diagnostic against frozen synthetic turns."""

import argparse
import asyncio
import hashlib
import json
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_QWEN3_8B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum
from oralia.course_study.__main__ import owned_lock
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationRequest

SOURCE = ROOT / "specs/012-conversational-course-study/evidence/semantic-v10-scope-first"
CONTROL_IDS = ("empty-techniques", "explicit-technique-link")


async def _run(output, protocol):
    curriculum = DraftCurriculum()
    async with cached_provider(
        output, source=CACHED_MODEL_QWEN3_8B, quantization="nf4", enable_thinking=False
    ) as port:
        for case in protocol["cases"]:
            request = GenerationRequest(
                purpose="explicacion",
                instruction=(
                    "Diagnóstico privado de interpretación, no respuesta al alumno. "
                    "Describe con tus propias palabras la duda concreta y qué conceptos "
                    "de las descripciones proporcionadas bastan para atenderla. "
                    "Indica si hace falta relacionar dos objetivos distintos y por qué. "
                    "No uses identificadores, no inventes contenidos ni afirmes aprobación."
                ),
                student_input=json.dumps(
                    {
                        "input": case["input"],
                        "context": case["state_before"],
                        "goals": [
                            {"title": g["title"], "scope": g["scope"], "description": g["description"]}
                            for g in curriculum.goals
                        ],
                        "relations": [r["description"] for r in curriculum.relations],
                    },
                    ensure_ascii=False,
                ),
                constraints=GenerationConstraints(max_tokens=220, deadline_ms=30000),
            )
            try:
                outcome = await port.generate(request)
                save(output / f"{case['id']}.json", {"outcome": outcome.model_dump(mode="json")})
            except Exception as exc:
                save(
                    output / f"{case['id']}.json",
                    {"error_type": type(exc).__name__, "transport": port.last_exchange},
                )
                return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT):
        parser.error("Output must be inside workspace")
    output.mkdir(parents=True, exist_ok=False)
    cases = []
    for control_id in CONTROL_IDS:
        row = json.loads((SOURCE / f"control-{control_id}.json").read_text(encoding="utf-8"))
        cases.append(
            {
                "id": control_id,
                "input": row["input"],
                "state_before": row["state_before"],
                "expected_frozen": row["expected_frozen"],
                "restricted_first_result": row["agent_result"],
            }
        )
    protocol = {
        "purpose": "diagnose model understanding versus restricted catalog selection; not acceptance",
        "cases": cases,
        "publication_authority": False,
        "teacher_review": "pending",
    }
    save(output / "protocol-frozen.json", protocol)
    runner = Path(__file__).read_bytes()
    (output / "runner-before.py").write_bytes(runner)
    save(
        output / "run-manifest.json",
        {
            "runner_sha256": hashlib.sha256(runner).hexdigest(),
            "protocol_sha256": hashlib.sha256((output / "protocol-frozen.json").read_bytes()).hexdigest(),
            "participant_publication": False,
        },
    )
    freeze_sources(output)
    with owned_lock(lab_root(ROOT)):
        completed = asyncio.run(_run(output, protocol))
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
