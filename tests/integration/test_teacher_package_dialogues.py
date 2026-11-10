"""Explicit complete development/reserved package conversations, never default acceptance."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.package_fixture import prepare_package
from tests.dialogue.package_runner import run_conversation

CASES = json.loads(
    (Path(__file__).parents[1] / "dialogue/fixtures/package-dialogues-v1.json").read_text(encoding="utf-8")
)["cases"]


@pytest.mark.skipif(
    not os.environ.get("ORALIA_PACKAGE_RUN"), reason="explicit package conversation evaluation"
)
def test_complete_package_conversations(app_client):
    partition = os.environ.get("ORALIA_PACKAGE_PARTITION", "development")
    output = Path(os.environ["ORALIA_PACKAGE_RUN"])
    output.mkdir(parents=True, exist_ok=True)
    prepared = {}
    reports = []
    for case in CASES:
        if (
            case["partition"] != partition
            or os.environ.get("ORALIA_PACKAGE_CASE")
            and os.environ["ORALIA_PACKAGE_CASE"] not in case["case_id"]
        ):
            continue
        if case["stream"] not in prepared:
            prepared[case["stream"]] = prepare_package(
                app_client,
                case["stream"],
                technical_publish=True,
                policy_version=int(os.environ.get("ORALIA_PACKAGE_POLICY", "3")),
            )
            target = output / (case["stream"] + "-bindings.json")
            assert not target.exists()
            target.write_text(
                json.dumps(
                    {k: v for k, v in prepared[case["stream"]].items() if k != "published"},
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        reports.append(
            run_conversation(app_client, prepared[case["stream"]], case, output / (case["case_id"] + ".json"))
        )
    assert reports
    summary = {
        "cases": len(reports),
        "passed": sum(r["outcome"] == "passed" for r in reports),
        "outcomes": [
            {"case_id": r["case"]["case_id"], "outcome": r["outcome"], "violations": r["violations"]}
            for r in reports
        ],
        "human_review": "pending",
        "audio_real": False,
    }
    target = output / "summary.json"
    assert not target.exists()
    target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert summary["passed"] == summary["cases"], summary["outcomes"]
