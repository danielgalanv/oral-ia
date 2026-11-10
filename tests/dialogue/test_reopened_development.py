"""Failed first-reserve cases are development regressions, never fresh acceptance."""

import json
from uuid import uuid4

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.study_intent_interpreter import StudyIntentInterpreterAgent
from oralia.domain.dialogue.contracts import DialogueContext, Referent
from tests.dialogue.runner import FIXTURES, frozen_cases, run_case

FAILED_IDS = {"I09", "I23", "I27", "I28", "I30", "I31", "I34", "I35", "I36", "I37", "I38"}
REGRESSIONS = [
    item
    for item in json.loads((FIXTURES / "holdout-inputs.json").read_text(encoding="utf-8"))["entries"]
    if item["case_id"] in FAILED_IDS
]


@pytest.mark.parametrize("case", REGRESSIONS, ids=lambda case: case["case_id"])
async def test_first_reserved_failure_is_now_development(case):
    values = case["context"]
    context = DialogueContext(
        pending_question_turn_id=uuid4() if values["pending_question"] else None,
        candidate_referents=tuple(
            Referent(kind="topic", ref=f"synthetic-{i}") for i in range(values["referent_count"])
        ),
    )
    result = await StudyIntentInterpreterAgent().execute(
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
    assert result.status == "ok" and result.output["dialogue_act"]["primary_act"] == case["expected_act"]


def test_first_H02_failure_is_now_development(app_client):
    case = next(case for case in frozen_cases("holdout") if case["case_id"] == "H02")
    result = run_case(app_client, case)
    assert result["passed_measured_properties"], result["failures"]
