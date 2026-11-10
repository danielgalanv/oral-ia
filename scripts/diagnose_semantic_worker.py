"""Reproduce one frozen synthetic worker failure without replacing its first run."""

import argparse
import asyncio
import hashlib
import json
import time
import uuid
from pathlib import Path

from rehearse_course_dialogue import ROOT, freeze_sources, save
from rehearse_semantic_controls import _turn

from oralia.course_dialogue.__main__ import lab_root
from oralia.course_dialogue.cached_transformers import CACHED_MODEL_QWEN3_8B, cached_provider
from oralia.course_dialogue.draft_dialogue import DraftCurriculum, DraftState
from oralia.course_dialogue.semantic_planner import LocalSemanticPlanner
from oralia.course_study.__main__ import owned_lock
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent

SOURCE = ROOT / "specs/012-conversational-course-study/evidence/semantic-v10-scope-first"


async def _reproduce(output, protocol):
    curriculum = DraftCurriculum()
    async with cached_provider(
        output,
        source=CACHED_MODEL_QWEN3_8B,
        quantization="nf4",
        enable_thinking=False,
    ) as port:
        planner = LocalSemanticPlanner(port)
        agent = StudyIntentInterpreterAgent(semantic_planner=planner, semantic_version=10)
        for case in protocol["cases"]:
            started = time.perf_counter()
            row, _ = await _turn(
                agent,
                planner,
                curriculum,
                DraftState(**case["state_before"]),
                {"input": case["input"], "expected": case["expected_frozen"]},
                uuid.uuid4(),
                case.get("previous_preview"),
            )
            save(output / f"{case['id']}.json", row)
            exchange = dict(port.last_exchange or {})
            exchange.update(
                case=case["id"],
                elapsed_seconds=time.perf_counter() - started,
                adapter_usable_before_cleanup=port.usable,
                process_returncode_before_cleanup=port.process.returncode,
                agent_status=row["agent_result"]["status"],
            )
            save(output / f"{case['id']}-transport-before-cleanup.json", exchange)
            if row["agent_result"]["status"] != "ok" or not port.usable:
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
    short = json.loads((SOURCE / "control-empty-quality.json").read_text(encoding="utf-8"))
    conversation = json.loads(
        (SOURCE / "conversation-new-scope-techniques.json").read_text(encoding="utf-8")
    )["turns"]
    failed = conversation[-1]
    if failed["stage"] != "repeat" or failed["agent_result"]["status"] == "ok":
        raise ValueError("Frozen source no longer identifies the failed repeat turn")
    protocol = {
        "source_package": str(SOURCE.relative_to(ROOT)),
        "purpose": "diagnose transport only; no semantic retry or publication",
        "cases": [
            {
                "id": "short-control",
                "input": short["input"],
                "state_before": short["state_before"],
                "expected_frozen": short["expected_frozen"],
            },
            {
                "id": "exact-failed-repeat",
                "input": failed["input"],
                "state_before": failed["state_before"],
                "expected_frozen": failed["expected_frozen"],
                "previous_preview": conversation[-2].get("actual_preview", {}).get("candidate_text"),
            },
        ],
    }
    save(output / "protocol-frozen.json", protocol)
    runner = Path(__file__).read_bytes()
    (output / "runner-before.py").write_bytes(runner)
    save(
        output / "run-manifest.json",
        {
            "runner_sha256": hashlib.sha256(runner).hexdigest(),
            "protocol_sha256": hashlib.sha256((output / "protocol-frozen.json").read_bytes()).hexdigest(),
            "first_run_preserved": True,
            "participant_publication": False,
        },
    )
    freeze_sources(output)
    with owned_lock(lab_root(ROOT)):
        completed = asyncio.run(_reproduce(output, protocol))
    return 0 if completed else 2


if __name__ == "__main__":
    raise SystemExit(main())
