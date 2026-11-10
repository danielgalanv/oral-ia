"""Exposed development stimuli; author expectations are independent of planner output."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.package_fixture import prepare_package, start_package_session


@pytest.mark.skipif(not os.environ.get("ORALIA_PACKAGE_STIMULI"), reason="explicit isolated package run")
def test_exposed_author_stimuli(app_client):
    output = Path(os.environ["ORALIA_PACKAGE_STIMULI"])
    output.mkdir(parents=True, exist_ok=True)
    source = Path("materiales/docente/ampliacion-didactica-20261020/docente/casos-desarrollo.json")
    cases = json.loads(source.read_text(encoding="utf-8"))["cases"]
    reports = []
    for stream in ["agua-docx", "programa-docx", "programa-pptx", "datos-pdf"]:
        prepared = prepare_package(app_client, stream, technical_publish=True, policy_version=3)
        for case in cases:
            if case["domain"] != prepared["domain"]:
                continue
            session = start_package_session(app_client, prepared, "self_study")
            sid = session["session_id"]
            try:
                response = app_client.post(
                    f"/api/v1/sessions/{sid}/conversation-controls", json={"text": case["prompt"]}
                )
                body = response.json()
                status = body.get("dialogue_status", {})
                expected = prepared["units"][case["expected_evidence"]]
                report = {
                    "case": case,
                    "stream": stream,
                    "session_id": sid,
                    "http_status": response.status_code,
                    "response": body,
                    "expected_unit_id": expected,
                    "source_witness": prepared["witnesses"][case["expected_evidence"]],
                    "passed": response.status_code == 200
                    and status.get("rendered_unit_ids") == [expected]
                    and status.get("grounding_verdict") == "fundamentada"
                    and status.get("coherence_verdict") == "approved",
                    "human_quality": "pending; selection and source checks alone are insufficient",
                }
                target = output / (stream + "-" + case["id"] + ".json")
                assert not target.exists(), "Preserve the first failure; choose a new output directory"
                target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                reports.append(report)
            finally:
                app_client.post(
                    f"/api/v1/governance/sessions/{sid}/close",
                    json={"confirm": True, "reason": "abandoned"},
                )
    summary = {
        "instances": len(reports),
        "unique_stimuli": len({r["case"]["id"] for r in reports}),
        "passed": sum(r["passed"] for r in reports),
        "failed": [{"stream": r["stream"], "id": r["case"]["id"]} for r in reports if not r["passed"]],
        "partition": "development_exposed",
    }
    target = output / "summary.json"
    assert not target.exists()
    target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert summary["instances"] == 80 and summary["unique_stimuli"] == 60
    assert summary["passed"] == 80, summary["failed"]
