"""Adaptive real-API continuity acceptance: capture is never an acceptance oracle."""

import json
import os
from pathlib import Path

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.package_fixture import prepare_package, start_package_session

CORPUS = json.loads(
    Path(
        os.environ.get("ORALIA_NATURAL_CORPUS", "tests/dialogue/fixtures/natural-continuity-v1.json")
    ).read_text(encoding="utf-8")
)["cases"]
ORACLES = json.loads(
    Path(
        os.environ.get("ORALIA_NATURAL_ORACLES", "tests/dialogue/fixtures/natural-continuity-oracles-v1.json")
    ).read_text(encoding="utf-8")
)["study"]


@pytest.mark.skipif(not os.environ.get("ORALIA_NATURAL_RUN"), reason="explicit continuity corpus")
def test_adaptive_continuity(app_client):
    directory = Path(os.environ["ORALIA_NATURAL_RUN"])
    directory.mkdir(parents=True, exist_ok=True)
    partition = os.environ.get("ORALIA_NATURAL_PARTITION", "development")
    prepared = {}
    reports = []
    for case in CORPUS:
        if case["partition"] != partition:
            continue
        if case["stream"] not in prepared:
            prepared[case["stream"]] = prepare_package(
                app_client,
                case["stream"],
                technical_publish=True,
                policy_version=int(os.environ.get("ORALIA_NATURAL_POLICY", "3")),
            )
        pack = prepared[case["stream"]]
        sid = start_package_session(app_client, pack, case["mode"])["session_id"]
        report = {
            "case": case,
            "observations": [],
            "violations": [],
            "human_review": "pending",
            "audio_real": False,
        }
        path = directory / (case["case_id"] + ".json")
        assert not path.exists()

        def save(path=path, report=report):
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        def send(text, sid=sid, report=report, save=save):
            response = app_client.post(f"/api/v1/sessions/{sid}/conversation-controls", json={"text": text})
            body = response.json()
            with app_client.__db_sessionmaker__() as db:
                session = db.get(models.Session, sid)
                state = db.get(models.CognitiveState, sid)
                context = state.dialogue_context if state else {}
                row = db.get(models.Turn, body.get("turn_id")) if body.get("turn_id") else None
                verification = (
                    db.get(models.VerificationResult, row.verification_result_id)
                    if row and row.verification_result_id
                    else None
                )
                details = (
                    {
                        c.name: getattr(verification, c.name)
                        for c in models.VerificationResult.__table__.columns
                        if c.name not in {"id", "created_at"}
                    }
                    if verification
                    else None
                )
            obs = {
                "input": text,
                "http_status": response.status_code,
                "response": body,
                "context": context,
                "status": session.status,
                "final_verification": details,
            }
            report["observations"].append(obs)
            save()
            if response.status_code != 200:
                report["violations"].append("HTTP failure")
            return obs

        try:
            last = send(case["opening"]) if case["opening"] else None
            original_question = None
            for step, text in enumerate(case["academic_inputs"]):
                if case["mode"] == "oral_defense":
                    context = last["context"]
                    pending = context.get("pending_question_unit_id")
                    question = pack["published"].get(pending)
                    if not question or question["topic_ref"] != case["topic"]:
                        report["violations"].append(
                            "diverged: no actually emitted current question for adaptive answer"
                        )
                        break
                    if original_question is None:
                        original_question = pending
                    if pending != original_question:
                        report["violations"].append("original pending question changed without confirmation")
                    actual_ids = last["response"].get("dialogue_status", {}).get("rendered_unit_ids", [])
                    actual = next(
                        (
                            pack["published"][ref]
                            for ref in actual_ids
                            if pack["published"][ref]["kind"] == "question"
                        ),
                        None,
                    )
                    if not actual or actual["reviewed_content"] not in (
                        last["response"].get("output_text") or ""
                    ):
                        report["violations"].append(
                            "diverged: no actual current question output for adaptive strategy"
                        )
                        break
                    relations = question["relations_by_key"].get("rephrases", [])
                    role = (
                        0
                        if actual["key"] == question["key"]
                        else relations.index(actual["key"]) + 1 if actual["key"] in relations else None
                    )
                    if role is None or role >= len(case["academic_inputs"]):
                        report["violations"].append(
                            "diverged: emitted question has no frozen synthetic answer strategy"
                        )
                        break
                    text = case["academic_inputs"][role]
                    actual_question = {
                        "unit_id": next(
                            ref for ref in actual_ids if pack["published"][ref]["key"] == actual["key"]
                        ),
                        "text": actual["reviewed_content"],
                        "strategy_role": role,
                    }
                last = send(text)
                status = last["response"].get("dialogue_status", {})
                refs = status.get("rendered_unit_ids", [])
                if case["mode"] == "oral_defense":
                    last["response_to_actual_question"] = actual_question
                    save()
                if (
                    last["response"].get("blocked")
                    or not last["response"].get("output_text")
                    or last["status"] != "active"
                ):
                    report["violations"].append("academic output blocked/empty or session prematurely closed")
                if not refs:
                    report["violations"].append(
                        "academic purpose lacked approved content or useful follow-up: " + text
                    )
                if refs and (
                    status.get("grounding_verdict") != "fundamentada"
                    or status.get("coherence_verdict") != "approved"
                ):
                    report["violations"].append("independent verification not approved")
                if case["mode"] == "self_study" and refs:
                    expected = ORACLES[case["stream"]][partition][step]
                    keys = [pack["published"][u]["key"] for u in refs]
                    if not any(
                        any(key.endswith(suffix) or suffix in key for suffix in expected) for key in keys
                    ):
                        report["violations"].append(
                            "wrong academic purpose: " + repr(keys) + " expected " + repr(expected)
                        )
                if case["mode"] == "oral_defense" and refs:
                    previous = [o["response"].get("output_text") for o in report["observations"][:-1]]
                    if last["response"].get("output_text") in previous:
                        report["violations"].append("follow-up repeats instead of progressing")
                if case["mode"] == "oral_defense" and any(
                    pack["published"][u]["kind"] not in {"question", "hint"} for u in refs
                ):
                    report["violations"].append("protected answer disclosed")
                if (
                    last["input"] == case["academic_inputs"][0]
                    and case["mode"] == "self_study"
                    and "hola" not in last["response"].get("output_text", "").casefold()
                ):
                    report["violations"].append("compound greeting lost greeting")
            if not any("diverged:" in v for v in report["violations"]):
                source = send(case["source_request"])
                if "sección" not in source["response"].get("output_text", ""):
                    report["violations"].append("provenance not verbalizable")
                proposed = send(case["closure_request"])
                if proposed["status"] != "active" or not proposed["context"].get(
                    "close_confirmation_pending"
                ):
                    report["violations"].append("explicit closure not pending without premature close")
                closed = send(case["closure_confirmation"])
                if closed["status"] != "closed_voluntary":
                    report["violations"].append(
                        "natural confirmation failed to close actual pending operation"
                    )
            report["outcome"] = "passed" if not report["violations"] else "failed"
            save()
            reports.append(report)
        finally:
            app_client.post(
                f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"}
            )
    summary = {
        "cases": len(reports),
        "passed": sum(r["outcome"] == "passed" for r in reports),
        "failures": [
            {"case": r["case"]["case_id"], "violations": r["violations"]} for r in reports if r["violations"]
        ],
        "capture_is_acceptance": False,
    }
    (directory / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assert summary["cases"] == 6 and summary["passed"] == 6, summary["failures"]
