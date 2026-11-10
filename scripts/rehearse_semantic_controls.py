"""Frozen synthetic diagnostic controls; never publish candidate prose to participants."""

import argparse
import asyncio
import hashlib
import json
import time
import uuid
from dataclasses import asdict
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_QWEN3_8B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
from oralia.course_study.__main__ import owned_lock
from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent


def _structural_match(result, expected):
    if result.status != "ok":
        return False
    plan = result.output["semantic_plan"]
    actual_pair = {plan["goal_ref"], plan.get("comparison_goal_ref")} - {None}
    expected_pair = {expected["goal_ref"], expected.get("comparison_goal_ref")} - {None}
    allowed = expected.get("allowed_acts", [expected.get("act")])
    return plan["act"] in allowed and actual_pair == expected_pair


async def _turn(agent, planner, curriculum, state, item, session_id, previous=None):
    pending = next(
        (u["draft_content"] for u in curriculum.units if u["id"] == state.pending_question_id),
        None,
    )
    context = {
        **asdict(state),
        "pending_question_text": pending,
        "last_actual_preview": previous,
    }
    request = AgentRequest(
        session_id=session_id,
        turn_id=uuid.uuid4(),
        input={
            "semantic_planning_version": agent._semantic_version,
            "text": item["input"],
            "goals": curriculum.goals,
            "correction_options": curriculum.corrections,
            "relations": curriculum.relations,
            "context": context,
        },
        deadline_ms=30000,
    )
    before = asdict(state)
    planner.last_trace = None
    started = time.perf_counter()
    result = await agent.execute(request, CancellationToken())
    row = {
        "input": item["input"],
        "expected_frozen": item["expected"],
        "state_before": before,
        "agent_result": result.model_dump(mode="json"),
        "planner_trace": planner.last_trace,
        "elapsed_seconds": time.perf_counter() - started,
        "structural_match": _structural_match(result, item["expected"]),
        "act_match": (
            result.status == "ok"
            and result.output["semantic_plan"]["act"]
            in item["expected"].get("allowed_acts", [item["expected"].get("act")])
        ),
        "focus_match": (
            result.status == "ok"
            and {
                result.output["semantic_plan"]["goal_ref"],
                result.output["semantic_plan"].get("comparison_goal_ref"),
            }
            - {None}
            == {item["expected"]["goal_ref"], item["expected"].get("comparison_goal_ref")} - {None}
        ),
        "question_focus_review": "pending_independent_content_review",
        "participant_publication": False,
    }
    if result.status == "ok":
        try:
            actual, state = curriculum.render_preview(
                result.output["semantic_plan"], state, current_input=item["input"]
            )
            row["actual_preview"] = actual
        except ValueError as exc:
            row["preview_error"] = str(exc)
    row["state_after"] = asdict(state)
    return row, state


async def _run(args, output, protocol):
    curriculum = DraftCurriculum()
    async with cached_provider(
        output,
        source=CACHED_MODEL_QWEN3_8B,
        quantization="nf4",
        enable_thinking=False,
    ) as port:
        planner = LocalSemanticPlanner(port)
        agent = StudyIntentInterpreterAgent(semantic_planner=planner, semantic_version=args.semantic_version)
        for control in protocol["diagnostic_controls"]:
            state = DraftState(**control["seed"])
            row, _ = await _turn(agent, planner, curriculum, state, control, uuid.uuid4())
            save(output / f"control-{control['id']}.json", row)
            print(
                "control", control["id"], row["agent_result"]["status"], row["structural_match"], flush=True
            )
            if port.process.returncode is not None or not getattr(port, "usable", True):
                save(
                    output / "experiment-interrupted.json", {"after": control["id"], "automatic_retry": False}
                )
                return False
        for conversation in protocol["complete_conversations"]:
            state = DraftState()
            session_id = uuid.uuid4()
            rows = []
            for item in conversation["turns"]:
                previous = rows[-1].get("actual_preview", {}).get("candidate_text") if rows else None
                row, state = await _turn(agent, planner, curriculum, state, item, session_id, previous)
                row["stage"] = item["stage"]
                rows.append(row)
                save(
                    output / f"conversation-{conversation['id']}.json",
                    {"turns": rows, "real_state_from_empty": True, "participant_publication": False},
                )
                print(
                    "conversation",
                    conversation["id"],
                    item["stage"],
                    row["agent_result"]["status"],
                    row["structural_match"],
                    flush=True,
                )
                if port.process.returncode is not None or not getattr(port, "usable", True):
                    save(
                        output / "experiment-interrupted.json",
                        {"after": f"{conversation['id']}:{item['stage']}", "automatic_retry": False},
                    )
                    return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--semantic-version", type=int, choices=[7, 8, 9, 10], required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT):
        parser.error("Output must be inside workspace")
    output.mkdir(parents=True, exist_ok=False)
    data = args.protocol.read_bytes()
    protocol = json.loads(data)
    save(output / "protocol-frozen.json", protocol)
    runner_bytes = Path(__file__).read_bytes()
    (output / "runner-before.py").write_bytes(runner_bytes)
    save(
        output / "run-manifest.json",
        {
            "protocol_sha256": hashlib.sha256(data).hexdigest(),
            "runner_sha256": hashlib.sha256(runner_bytes).hexdigest(),
            "semantic_version": args.semantic_version,
            "model": "cached qwen3-8b-nf4",
            "participant_publication": False,
            "teacher_review": "pending",
            "structural_check_only": True,
        },
    )
    freeze_sources(output)
    with owned_lock(lab_root(ROOT)):
        completed = asyncio.run(_run(args, output, protocol))
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
