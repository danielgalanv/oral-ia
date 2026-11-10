"""Compare single-goal and relation draft answers with a separate cached judge."""

import argparse
import asyncio
import hashlib
import json
import time
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_14B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.course_study.__main__ import owned_lock
from oralia.domain.dialogue.contracts import SemanticStudyPlanV2
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationRequest


def _previews(curriculum, case):
    relation = next(r for r in curriculum.relations if r["id"] == case["relation"])
    single, _ = curriculum.render_preview(
        SemanticStudyPlanV2(act="explain", goal_ref=case["single_goal"]),
        DraftState(),
        current_input=case["input"],
    )
    paired, _ = curriculum.render_preview(
        SemanticStudyPlanV2(
            act="explain",
            goal_ref=relation["primary_goal"],
            comparison_goal_ref=relation["secondary_goal"],
        ),
        DraftState(),
        current_input=case["input"],
    )
    return single, paired


async def _run(output, protocol):
    curriculum = DraftCurriculum()
    async with cached_provider(output, source=CACHED_MODEL_14B, quantization="nf4") as port:
        for case in protocol["cases"]:
            single, paired = _previews(curriculum, case)
            request = GenerationRequest(
                purpose="comparacion",
                instruction=(
                    "Eres un revisor de pertinencia de dos borradores, no el tutor. "
                    "Decide cuál responde a la duda concreta sin introducir otro asunto. "
                    "single_sufficient si el borrador A basta; relation_needed solo si "
                    "el B añade una relación que la pregunta necesita realmente; "
                    "neither si ninguno atiende la duda. No prefieras B por ser más largo. "
                    "El contexto anterior no exige conservar una relación si el turno la acota. "
                    "Devuelve solo la decisión, sin explicación ni evaluación del alumno."
                ),
                student_input=json.dumps(
                    {
                        "turno_actual": case["input"],
                        "contexto": case["context"],
                        "borrador_A": single["candidate_text"],
                        "borrador_B": paired["candidate_text"],
                    },
                    ensure_ascii=False,
                ),
                output_schema={
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["decision"],
                    "properties": {
                        "decision": {
                            "type": "string",
                            "enum": ["single_sufficient", "relation_needed", "neither"],
                        }
                    },
                },
                constraints=GenerationConstraints(max_tokens=48, deadline_ms=12000),
            )
            row = {
                "expected_frozen": case["expected"],
                "single_preview": single,
                "relation_preview": paired,
                "participant_publication": False,
            }
            started = time.perf_counter()
            try:
                outcome = await port.generate(request)
                row["outcome"] = outcome.model_dump(mode="json")
                value = json.loads(outcome.text)
                if (
                    not outcome.ok
                    or set(value) != {"decision"}
                    or value["decision"]
                    not in {
                        "single_sufficient",
                        "relation_needed",
                        "neither",
                    }
                ):
                    raise ValueError("incomplete or invalid comparative decision")
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
        / "specs/012-conversational-course-study/evidence"
        / "semantic-counterfactual-verifier-protocol-frozen.json"
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
            "publication_authority": False,
        },
    )
    freeze_sources(output)
    with owned_lock(lab_root(ROOT)):
        completed = asyncio.run(_run(output, protocol))
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
