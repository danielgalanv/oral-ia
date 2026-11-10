"""Probe an independent cached local relation judge; no participant authority."""

import argparse
import asyncio
import hashlib
import json
import time
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum
from oralia.course_study.__main__ import owned_lock
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationRequest


async def _run(output, protocol):
    curriculum = DraftCurriculum()
    goals = {goal["id"]: goal for goal in curriculum.goals}
    relations = {relation["id"]: relation for relation in curriculum.relations}
    async with cached_provider(output, source=CACHED_MODEL_14B, quantization="nf4") as port:
        for case in protocol["cases"]:
            relation = relations[case["relation"]]
            request = GenerationRequest(
                purpose="comparacion",
                instruction=(
                    "Eres un verificador independiente de alcance, no un tutor. "
                    "Decide si para responder exactamente al turno actual hace falta "
                    "relacionar los DOS objetivos distintos descritos. "
                    "Responde no si uno solo cubre la pregunta, aunque compare dos ideas "
                    "dentro de ese objetivo. Una relación previa no obliga a repetirla. "
                    "Responde yes solo si ambos ámbitos son necesarios por la pregunta "
                    "actual o un referente inequívoco del contexto. "
                    "No redactes explicación ni evalúes al alumno."
                ),
                student_input=json.dumps(
                    {
                        "turno_actual": case["input"],
                        "contexto_real": case["context"],
                        "primer_objetivo": {
                            "title": goals[relation["primary_goal"]]["title"],
                            "scope": goals[relation["primary_goal"]]["scope"],
                        },
                        "segundo_objetivo": {
                            "title": goals[relation["secondary_goal"]]["title"],
                            "scope": goals[relation["secondary_goal"]]["scope"],
                        },
                        "relacion_candidata": relation["description"],
                    },
                    ensure_ascii=False,
                ),
                output_schema={
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["decision"],
                    "properties": {"decision": {"type": "string", "enum": ["yes", "no"]}},
                },
                constraints=GenerationConstraints(max_tokens=32, deadline_ms=12000),
            )
            started = time.perf_counter()
            row = {"expected_frozen": case["expected"], "participant_publication": False}
            try:
                outcome = await port.generate(request)
                row["outcome"] = outcome.model_dump(mode="json")
                value = json.loads(outcome.text)
                if not outcome.ok or set(value) != {"decision"} or value["decision"] not in {"yes", "no"}:
                    raise ValueError("incomplete or invalid verifier decision")
                row["decision"] = value["decision"]
                row["match"] = value["decision"] == case["expected"]
            except Exception as exc:
                row["error_type"] = type(exc).__name__
                row["transport_before_cleanup"] = port.last_exchange
            row["elapsed_seconds"] = time.perf_counter() - started
            row["worker_returncode_before_cleanup"] = port.process.returncode
            save(output / f"{case['id']}.json", row)
            if "error_type" in row or not port.usable:
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
    source = (
        ROOT
        / "specs/012-conversational-course-study/evidence/semantic-independent-verifier-protocol-frozen.json"
    )
    frozen = source.read_bytes()
    protocol = json.loads(frozen)
    (output / "protocol-frozen.json").write_bytes(frozen)
    runner = Path(__file__).read_bytes()
    (output / "runner-before.py").write_bytes(runner)
    save(
        output / "run-manifest.json",
        {
            "protocol_sha256": hashlib.sha256(frozen).hexdigest(),
            "runner_sha256": hashlib.sha256(runner).hexdigest(),
            "model": "cached Qwen2.5-14B-Instruct NF4",
            "planner_model": "Qwen3-8B NF4; separate worker and weights",
            "publication_authority": False,
        },
    )
    freeze_sources(output)
    with owned_lock(lab_root(ROOT)):
        completed = asyncio.run(_run(output, protocol))
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
