"""Actual agency/direct pairing; verification coverage is separated from quality."""

import json
import os
from pathlib import Path

import pytest

from oralia.application.services import guided_dialogue_service
from oralia.validation.guided_baseline import run_direct_guided_turn
from tests.dialogue.runner import frozen_cases, run_case

pytestmark = pytest.mark.skipif(
    os.environ.get("ORALIA_RUN_GUIDED_PAIRS") != "1", reason="explicit paired synthetic experiment"
)
CASES = [*frozen_cases("development"), *frozen_cases("holdout")]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_record_actual_pair(app_client, monkeypatch, case):
    # Counterbalance order without changing providers, material or policy.
    order = ["agency", "direct_baseline"] if int(case["case_id"][1:]) % 2 else ["direct_baseline", "agency"]
    results = {}
    for condition in order:
        with monkeypatch.context() as patch:
            if condition == "direct_baseline":
                patch.setattr(guided_dialogue_service, "run_guided_turn", run_direct_guided_turn)
            results[condition] = run_case(app_client, case, condition=condition)
    result = {
        "case_id": case["case_id"],
        "condition_order": order,
        "results": results,
        "same_material_hash": results["agency"]["source_sha256"]
        == results["direct_baseline"]["source_sha256"],
        "same_budget_ms": 10000,
        "provider": "controlled reviewed units; no free generation",
        "human_utility": "not_evaluated",
        "timing_limit": (
            "one paired deterministic execution; no causal performance or" " educational superiority claim"
        ),
    }
    folder = (
        Path(__file__).resolve().parents[2]
        / "specs/010-guided-dialogue/paired-runs"
        / os.environ["ORALIA_DIALOGUE_RUN_ID"]
    )
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / f"{case['case_id']}.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    # Recording does not turn failed content/coverage properties into acceptance.
    assert result["same_material_hash"]
