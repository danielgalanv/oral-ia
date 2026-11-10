"""Explicit first reserved evaluation, append-only reports; never used for tuning."""

import hashlib
import json
import os
from pathlib import Path
from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.dialogue.contracts import DialogueContext, Referent
from tests.dialogue.runner import FIXTURES, frozen_cases, run_case

pytestmark = pytest.mark.skipif(
    os.environ.get("ORALIA_RUN_DIALOGUE_HOLDOUT") != "1",
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


@pytest.mark.parametrize("case", frozen_cases("holdout"), ids=lambda case: case["case_id"])
def test_reserved_dialogue(app_client, case):
    result = run_case(app_client, case)
    record(case["case_id"], result)
    assert result["passed_measured_properties"], result["failures"]


def reserved_inputs():
    path = FIXTURES / "holdout-inputs.json"
    freeze = json.loads((FIXTURES / "freeze.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(path.read_bytes()).hexdigest() == freeze["sha256"][path.name]
    return json.loads(path.read_text(encoding="utf-8"))["entries"]


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
    actual = (result.output or {}).get("dialogue_act", {}).get("primary_act")
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
            "matched": actual == case["expected_act"],
            "status": result.status,
            "output": result.output,
            "provider": "StudyIntentInterpreterAgent/v2 deterministic",
            "scope": "act contract only; public authorization tested separately",
        },
    )
    assert actual == case["expected_act"]
