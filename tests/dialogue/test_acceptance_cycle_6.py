"""Sixth frozen classification cycle; conversational holdout is separately reproduced."""

import hashlib
import json
import os
from pathlib import Path
from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.dialogue.contracts import DialogueContext, Referent
from tests.dialogue.runner import FIXTURES

pytestmark = pytest.mark.skipif(
    os.environ.get("ORALIA_RUN_DIALOGUE_CYCLE_6") != "1",
    reason="reserved evaluation requires explicit invocation and a new report directory",
)


def record(name, result):
    folder = (
        Path(__file__).resolve().parents[2]
        / "specs/010-guided-dialogue/holdout-runs"
        / os.environ["ORALIA_DIALOGUE_RUN_ID"]
    )
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / f"{name}.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)


def cycle_cases(name, key):
    path = FIXTURES / "acceptance-cycle-6" / name
    freeze = json.loads((path.parent / "freeze.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(path.read_bytes()).hexdigest() == freeze["sha256"][name]
    return json.loads(path.read_text(encoding="utf-8"))[key]


def reserved_inputs():
    return cycle_cases("inputs.json", "entries")


@pytest.mark.parametrize("case", reserved_inputs(), ids=lambda case: case["case_id"])
async def test_reserved_input(case):
    supplied = case["context"]
    references = tuple(
        Referent(kind="topic", ref=f"synthetic-topic-{i}") for i in range(supplied["referent_count"])
    )
    context = DialogueContext(
        candidate_referents=references,
        pending_question_turn_id=uuid4() if supplied["pending_question"] else None,
    )
    agent = StudyIntentInterpreterAgent()
    result = await agent.execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "text": case["text"],
                "dialogue_schema_version": 2,
                "dialogue_context": context.model_dump(mode="json"),
            },
        ),
        CancellationToken(),
    )
    act = (result.output or {}).get("dialogue_act", {})
    actual = act.get("primary_act")
    target_matched = (
        "expected_repeat_target" not in case or act.get("repeat_target") == case["expected_repeat_target"]
    )
    record(
        case["case_id"],
        {
            "case_id": case["case_id"],
            "group": case["group"],
            "critical": case["critical"],
            "input": case["text"],
            "context": supplied,
            "expected_act": case["expected_act"],
            "actual_act": actual,
            "matched": actual == case["expected_act"] and target_matched,
            "expected_repeat_target": case.get("expected_repeat_target"),
            "actual_repeat_target": act.get("repeat_target"),
            "status": result.status,
            "output": result.output,
            "provider": "StudyIntentInterpreterAgent/v2 deterministic",
            "scope": "act contract only; public authorization tested separately",
        },
    )
    assert actual == case["expected_act"]
    assert target_matched
