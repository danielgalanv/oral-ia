"""Actual semantic plans + explicit controlled draft preview; never approved model prose."""

import argparse
import asyncio
import json
import time
import uuid
from dataclasses import asdict
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import (
    CACHED_MODEL_7B,
    CACHED_MODEL_14B,
    CACHED_MODEL_QWEN3_8B,
    cached_provider,
)
from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.course_dialogue.evaluation import observe_controlled
from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
from oralia.course_study.__main__ import owned_lock
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent


async def run(args, output, scenarios):
    curriculum = DraftCurriculum()
    source = (
        CACHED_MODEL_QWEN3_8B
        if args.model == "qwen3-8b-nf4"
        else CACHED_MODEL_14B if args.model == "14b-nf4" else CACHED_MODEL_7B
    )
    async with cached_provider(
        output,
        source=source,
        quantization="nf4",
        enable_thinking=False if args.model == "qwen3-8b-nf4" else None,
    ) as port:
        planner = LocalSemanticPlanner(port)
        agent = StudyIntentInterpreterAgent(semantic_planner=planner, semantic_version=args.semantic_version)
        for scenario in scenarios:
            for repeat in range(args.repetitions):
                state = DraftState()
                turns = []
                session_id = uuid.uuid4()
                for stage in ["first", "followup", "correction", "repeat", "switch"]:
                    if stage not in scenario:
                        continue
                    text = scenario[stage]
                    if turns and not turns[-1].get("actual_preview"):
                        text = "No he recibido una explicación. " + text
                    pending = next(
                        (
                            u["draft_content"]
                            for u in curriculum.units
                            if u["id"] == state.pending_question_id
                        ),
                        None,
                    )
                    context = {
                        **asdict(state),
                        "pending_question_text": pending,
                        "last_actual_preview": (
                            turns[-1].get("actual_preview", {}).get("candidate_text") if turns else None
                        ),
                    }
                    request = AgentRequest(
                        session_id=session_id,
                        turn_id=uuid.uuid4(),
                        input={
                            "semantic_planning_version": args.semantic_version,
                            "text": text,
                            "goals": curriculum.goals,
                            "correction_options": curriculum.corrections,
                            "relations": curriculum.relations,
                            "context": context,
                        },
                        deadline_ms=30000,
                    )
                    before = asdict(state)
                    started = time.perf_counter()
                    planner.last_trace = None
                    result = await agent.execute(request, CancellationToken())
                    row = {
                        "stage": stage,
                        "input": text,
                        "state_before": before,
                        "agent_result": result.model_dump(mode="json"),
                        "planner_trace": planner.last_trace,
                        "elapsed_seconds": time.perf_counter() - started,
                        "participant_publication": False,
                    }
                    if result.status == "ok":
                        try:
                            actual, next_state = curriculum.render_preview(
                                result.output["semantic_plan"], state, current_input=text
                            )
                            row["actual_preview"] = actual
                            state = next_state
                        except ValueError as exc:
                            row["preview_error"] = str(exc)
                    row["state_after"] = asdict(state)
                    if args.observations is not None:
                        expected = args._observations[scenario["id"]][stage]
                        row["independent_observations"] = observe_controlled(
                            row, expected, prior=turns[-1] if turns else None
                        )
                    turns.append(row)
                    save(
                        output / f"{scenario['id']}-{repeat}.json",
                        {
                            "case": scenario,
                            "turns": turns,
                            "synthetic_student_inputs": True,
                            "local_model_configured": True,
                            "provider_outcomes_received": sum(
                                phase.get("outcome") is not None
                                for item in turns
                                for phase in (item.get("planner_trace") or {}).get("phases", [])
                            ),
                            "actual_renderer": "technically_authored_controlled_drafts",
                            "teacher_review": "pending",
                            "not_free_model_responses": True,
                        },
                    )
                    print(
                        scenario["id"],
                        repeat,
                        stage,
                        result.status,
                        round(row["elapsed_seconds"], 2),
                        flush=True,
                    )
                    if port.process.returncode is not None or not getattr(port, "usable", True):
                        save(
                            output / "experiment-interrupted.json",
                            {
                                "case": scenario["id"],
                                "repetition": repeat,
                                "stage": stage,
                                "reason": (
                                    "owned worker transport unavailable; "
                                    "remaining planned inputs were not executed"
                                ),
                                "worker_returncode": port.process.returncode,
                                "provider_usable": getattr(port, "usable", True)
                                and port.process.returncode is None,
                                "automatic_retry": False,
                                "publication_authority": False,
                            },
                        )
                        print(
                            "Ensayo interrumpido: proveedor local no disponible; "
                            "no se simulan respuestas posteriores.",
                            flush=True,
                        )
                        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--partition", choices=["development", "reserved", "transfer"], default="development")
    parser.add_argument("--repetitions", type=int, choices=[1, 2, 3], default=3)
    parser.add_argument("--model", choices=["7b-nf4", "14b-nf4", "qwen3-8b-nf4"], default="7b-nf4")
    parser.add_argument("--semantic-version", type=int, choices=[1, 2, 3, 4, 5, 6, 7], default=1)
    parser.add_argument("--observations", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT):
        parser.error("Output must be inside workspace")
    output.mkdir(parents=True, exist_ok=False)
    args._observations = None
    if args.observations is not None:
        args._observations = json.loads(args.observations.read_text(encoding="utf8"))["scenarios"]
        save(output / "observations-frozen.json", json.loads(args.observations.read_text(encoding="utf8")))
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    save(output / "cases.json", cases)
    freeze_sources(output)
    scenarios = cases["scenarios"] if args.partition == "transfer" else cases[args.partition]
    scenarios = [
        {**case, "first": case["input"]} if "input" in case and "first" not in case else case
        for case in scenarios
    ]
    with owned_lock(lab_root(ROOT)):
        completed = asyncio.run(run(args, output, scenarios))
    if completed is False:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
