"""Exposed audit-prefix regressions: direct purpose/content oracles, not capture success."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.package_fixture import prepare_package, start_package_session


@pytest.mark.skipif(not os.environ.get("ORALIA_NATURAL_PREFIXES"), reason="explicit natural audit prefixes")
def test_audit_prefixes_with_real_question_and_material(app_client):
    output = Path(os.environ["ORALIA_NATURAL_PREFIXES"])
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for stream, inputs in [
        (
            "agua-docx",
            [
                "¿El agua puede pasar a vapor sin hervir?",
                "¿Por qué sale del líquido?",
                "No lo entiendo. ¿Se rompe el agua en hidrógeno y oxígeno?",
                "Sigo sin verlo. Explícamelo de otra manera.",
            ],
        ),
        ("programa-docx", ["Buenas, ¿qué es validar exactamente?"]),
        ("datos-pdf", ["¿Qué significa mediana?", "¿Y la otra?", "La media"]),
    ]:
        pack = prepare_package(app_client, stream, technical_publish=True, policy_version=4)
        sid = start_package_session(app_client, pack, "self_study")["session_id"]
        observations = []
        failures = []
        try:
            for index, text in enumerate(inputs):
                response = app_client.post(
                    f"/api/v1/sessions/{sid}/conversation-controls", json={"text": text}
                )
                body = response.json()
                status = body.get("dialogue_status") or {}
                value = body.get("output_text") or ""
                observations.append({"input": text, "http_status": response.status_code, "response": body})
                if response.status_code != 200 or not value or body.get("blocked"):
                    failures.append("output unavailable: " + text)
                if stream == "agua-docx" and not status.get("rendered_unit_ids"):
                    failures.append("molecular chain lost reviewed explanation")
                if (
                    stream == "agua-docx"
                    and index == 2
                    and not all(word in value.casefold() for word in ["hidrógeno", "oxígeno"])
                ):
                    failures.append("molecular identity not answered directly")
                if stream == "programa-docx" and not (
                    "comprobar" in value.casefold() and "antes" in value.casefold()
                ):
                    failures.append("definition gives numeric restrictions instead of function and timing")
                if stream == "datos-pdf" and index == 1 and status.get("notice") != "clarify":
                    failures.append("ambiguous alternative not clarified")
                if stream == "datos-pdf" and index == 2 and not status.get("rendered_unit_ids"):
                    failures.append("explicit clarification answer did not resolve referent")
            report = {
                "stream": stream,
                "observations": observations,
                "failures": failures,
                "capture_is_acceptance": False,
                "human_review": "pending",
            }
            path = output / (stream + ".json")
            assert not path.exists()
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            results.append(report)
        finally:
            app_client.post(
                f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"}
            )
    summary = {
        "cases": len(results),
        "passed": sum(not r["failures"] for r in results),
        "failures": [{"stream": r["stream"], "criteria": r["failures"]} for r in results if r["failures"]],
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assert summary["passed"] == 3, summary["failures"]
