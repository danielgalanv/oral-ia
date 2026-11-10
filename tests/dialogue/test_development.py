"""Development run only. Reserved acceptance is a separate explicit invocation."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.runner import frozen_cases, run_case


@pytest.mark.skipif(
    os.environ.get("ORALIA_RUN_DIALOGUE_DEVELOPMENT") != "1",
    reason="explicit corpus execution; not a substitute for recorded acceptance",
)
@pytest.mark.parametrize("case", frozen_cases("development"), ids=lambda case: case["case_id"])
def test_development_dialogue(app_client, case):
    result = run_case(app_client, case)
    folder = (
        Path(__file__).resolve().parents[2]
        / "specs/010-guided-dialogue/development-runs"
        / os.environ["ORALIA_DIALOGUE_RUN_ID"]
    )
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{case['case_id']}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    assert result["passed_measured_properties"], result["failures"]
