"""Explicit tool partitions; reports preserve failed operations and mapping gaps."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.tool_runner import cases, run_tools

PARTITION = os.environ.get("ORALIA_TOOL_PARTITION", "development")
pytestmark = pytest.mark.skipif(
    os.environ.get("ORALIA_RUN_TOOL_CONVERSATIONS") != "1",
    reason="explicit synthetic tool conversation execution",
)


@pytest.mark.parametrize("case", cases(PARTITION), ids=lambda case: case["case_id"])
def test_tool_conversation(app_client, monkeypatch, case):
    result = run_tools(app_client, case, monkeypatch)
    folder = (
        Path(__file__).resolve().parents[2]
        / "specs/010-guided-dialogue/tool-runs"
        / os.environ["ORALIA_DIALOGUE_RUN_ID"]
    )
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / f"{case['case_id']}.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    assert result["passed"], result["failures"]
