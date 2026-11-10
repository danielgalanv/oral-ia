"""Frozen, unpublished atomic-goal-first mechanism probe."""

import argparse
import asyncio
import hashlib
import json
import time
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_QWEN3_8B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.course_study.__main__ import owned_lock
from oralia.domain.dialogue.contracts import SemanticStudyPlanV2
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationRequest


async def _choose(port, field, choices, instruction, student_input):
    request = GenerationRequest(
        purpose="explicacion",
        instruction=instruction,
        student_input=json.dumps({"question": student_input, "choices": choices}, ensure_ascii=False),
        output_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [field],
            "properties": {field: {"type": "integer", "enum": list(range(len(choices)))}},
        },
        constraints=GenerationConstraints(max_tokens=32, deadline_ms=12000),
    )
    outcome = await port.generate(request)
    if not outcome.ok or outcome.finish_reason in {"deadline", "length"}:
        raise ValueError("incomplete bounded choice")
    selected = json.loads(outcome.text)
    if not isinstance(selected, dict) or set(selected) != {field}:
        raise ValueError("invalid bounded choice")
    index = selected[field]
    if type(index) is not int or index not in range(len(choices)):
        raise ValueError("choice outside declared range")
    return index, outcome.model_dump(mode="json")


async def _run(output, protocol):
    curriculum = DraftCurriculum()
    async with cached_provider(
        output, source=CACHED_MODEL_QWEN3_8B, quantization="nf4", enable_thinking=False
    ) as port:
        for case in protocol["cases"]:
            started = time.perf_counter()
            row = {"input": case["input"], "expected_frozen": case["expected"], "publication": False}
            try:
                atomic_choices = [
                    {"title": goal["title"], "scope": goal["scope"], "definition": goal["description"]}
                    for goal in curriculum.goals
                ]
                goal_index, first = await _choose(
                    port,
                    "goal_index",
                    atomic_choices,
                    "Selecciona un solo objetivo atómico que mejor cubra la duda actual. "
                    "Aún no hay relaciones entre objetivos disponibles. Devuelve solo el índice; "
                    "no redactes respuesta, no inventes fuente ni permisos.",
                    case["input"],
                )
                goal = curriculum.goals[goal_index]
                candidates = [
                    relation
                    for relation in curriculum.relations
                    if goal["id"] in {relation["primary_goal"], relation["secondary_goal"]}
                ]
                relation_choices = [
                    {"option": "no_relation", "meaning": "El objetivo elegido basta por sí solo."}
                ] + [
                    {
                        "option": "authored_relation",
                        "description": relation["description"],
                        "other_goal": next(
                            g["title"]
                            for g in curriculum.goals
                            if g["id"]
                            == (
                                relation["secondary_goal"]
                                if relation["primary_goal"] == goal["id"]
                                else relation["primary_goal"]
                            )
                        ),
                    }
                    for relation in candidates
                ]
                relation_index, second = await _choose(
                    port,
                    "relation_index",
                    relation_choices,
                    "Decide si la pregunta actual exige además vincular el objetivo elegido "
                    "con otro objetivo distinto. Elige no_relation si los conceptos pedidos "
                    "caben en el objetivo atómico, aunque compare dos nociones internas. "
                    "Una relación exige responder a una conexión concreta entre ambos ámbitos. "
                    "Devuelve solo el índice; no redactes respuesta.",
                    case["input"],
                )
                relation = candidates[relation_index - 1] if relation_index else None
                plan = SemanticStudyPlanV2(
                    act="explain",
                    goal_ref=relation["primary_goal"] if relation else goal["id"],
                    comparison_goal_ref=relation["secondary_goal"] if relation else None,
                )
                preview, _ = curriculum.render_preview(plan, DraftState(), current_input=case["input"])
                actual_pair = {plan.goal_ref, plan.comparison_goal_ref} - {None}
                expected_pair = {
                    case["expected"]["goal_ref"],
                    case["expected"]["comparison_goal_ref"],
                } - {None}
                row.update(
                    status="ok",
                    atomic_goal=goal["id"],
                    relation=relation["id"] if relation else None,
                    plan=plan.model_dump(mode="json"),
                    focus_match=actual_pair == expected_pair,
                    preview=preview,
                    first_outcome=first,
                    second_outcome=second,
                )
            except Exception as exc:
                row.update(status="error", error_type=type(exc).__name__, transport=port.last_exchange)
            row["elapsed_seconds"] = time.perf_counter() - started
            save(output / f"{case['id']}.json", row)
            if row["status"] != "ok" or not port.usable:
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
    source = ROOT / "specs/012-conversational-course-study/evidence/semantic-goal-first-mechanism-freeze.json"
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
