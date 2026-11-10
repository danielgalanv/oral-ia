"""Contextual purpose/subject oracles independent of publication and grounding."""

import json
import os
from pathlib import Path

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.package_fixture import prepare_package, start_package_session


@pytest.mark.skipif(not os.environ.get("ORALIA_RELEVANCE_RUN"), reason="explicit contextual corpus")
def test_contextual_relevance(app_client):
    output = Path(os.environ["ORALIA_RELEVANCE_RUN"])
    output.mkdir(parents=True, exist_ok=False)
    cases = json.loads(
        Path(
            os.environ.get("ORALIA_RELEVANCE_CORPUS", "tests/dialogue/fixtures/contextual-relevance-v1.json")
        ).read_text(encoding="utf-8")
    )["cases"]
    prepared = {}
    reports = []
    for case in cases:
        if case["partition"] != os.environ.get("ORALIA_RELEVANCE_PARTITION", "development"):
            continue
        if case["stream"] not in prepared:
            prepared[case["stream"]] = prepare_package(
                app_client, case["stream"], technical_publish=True, policy_version=4
            )
        pack = prepared[case["stream"]]
        mode = case.get("mode", "self_study")
        sid = start_package_session(app_client, pack, mode)["session_id"]
        report = {"case": case, "observations": [], "failures": [], "human_review": "pending"}

        def send(text, sid=sid, report=report):
            response = app_client.post(f"/api/v1/sessions/{sid}/conversation-controls", json={"text": text})
            body = response.json()
            with app_client.__db_sessionmaker__() as db:
                state = db.get(models.CognitiveState, sid)
                session = db.get(models.Session, sid)
                turn = db.get(models.Turn, body.get("turn_id")) if body.get("turn_id") else None
                verifier = (
                    db.get(models.VerificationResult, turn.verification_result_id)
                    if turn and turn.verification_result_id
                    else None
                )
                details = (
                    {
                        c.name: getattr(verifier, c.name)
                        for c in models.VerificationResult.__table__.columns
                        if c.name not in {"id", "created_at"}
                    }
                    if verifier
                    else None
                )
                context = state.dialogue_context if state else {}
                status = session.status
                preference = db.get(models.SessionPrivacyPreference, sid)
                privacy = {
                    "retain": bool(preference and preference.retain),
                    "scope": preference.scope if preference else [],
                }
            obs = {
                "input": text,
                "response": body,
                "http": response.status_code,
                "context": context,
                "status": status,
                "verification": details,
                "privacy": privacy,
            }
            report["observations"].append(obs)
            return obs

        try:
            if case.get("retained"):
                send("conservar resumen y transcripción")
                retained = send("confirmo conservar resumen y transcripción")
                if not retained["privacy"]["retain"]:
                    report["failures"].append("canonical retention not applied")
            for step in case["steps"]:
                obs = send(step["text"])
                body = obs["response"]
                text = body.get("output_text") or ""
                status = body.get("dialogue_status") or {}
                refs = status.get("rendered_unit_ids", [])
                selected = [pack["published"][ref] for ref in refs]
                if step.get("notice"):
                    if status.get("notice") != step["notice"]:
                        report["failures"].append("expected clarification not emitted: " + step["text"])
                    continue
                if obs["http"] != 200 or not refs or body.get("blocked"):
                    report["failures"].append("academic response absent: " + step["text"])
                if refs and (
                    status.get("grounding_verdict") != "fundamentada"
                    or status.get("coherence_verdict") != "approved"
                ):
                    report["failures"].append("independent content verification not approved")
                if any(u["topic_ref"] != step["topic"] for u in selected):
                    report["failures"].append("wrong process/topic: " + step["text"])
                if step.get("suffix") and not any(u["key"].endswith(step["suffix"]) for u in selected):
                    report["failures"].append("wrong purpose/object: " + step["text"])
                for word in step.get("contains", []):
                    if word.casefold() not in text.casefold():
                        report["failures"].append("missing content: " + word)
                for word in step.get("not_contains", []):
                    if word.casefold() in text.casefold():
                        report["failures"].append("foreign process: " + word)
            if mode == "oral_defense":
                last = send("Hola, quiero empezar con la pregunta de defensa.")
                original = last["context"].get("pending_question_unit_id")
                question = pack["published"].get(original)
                if not question or question["topic_ref"] != case["topic"]:
                    report["failures"].append("diverged: no actual current question")
                else:
                    responses = []
                    for index in range(len(case["answers"])):
                        refs = last["response"].get("dialogue_status", {}).get("rendered_unit_ids", [])
                        actual = next(
                            (
                                pack["published"][r]
                                for r in refs
                                if pack["published"][r]["kind"] == "question"
                            ),
                            None,
                        )
                        if not actual or actual["reviewed_content"] not in (
                            last["response"].get("output_text") or ""
                        ):
                            report["failures"].append("diverged: no emitted question to answer")
                            break
                        relations = question["relations_by_key"].get("rephrases", [])
                        role = (
                            0
                            if actual["key"] == question["key"]
                            else relations.index(actual["key"]) + 1 if actual["key"] in relations else None
                        )
                        if role is None or role >= len(case["answers"]):
                            report["failures"].append("diverged: no frozen answer strategy")
                            break
                        last = send(case["answers"][role])
                        last["response_to_actual_question"] = actual["reviewed_content"]
                        body = last["response"]
                        status = body.get("dialogue_status", {})
                        ids = status.get("rendered_unit_ids", [])
                        if index < 3:
                            if not ids or any(pack["published"][r]["kind"] != "question" for r in ids):
                                report["failures"].append("safe follow-up missing")
                            if body.get("output_text") in responses:
                                report["failures"].append("repeated follow-up")
                            responses.append(body.get("output_text"))
                        elif status.get("notice") != "followups_exhausted" or "repreguntas" not in (
                            body.get("output_text") or ""
                        ):
                            report["failures"].append("exhaustion misdiagnosed as permission")
                        if last["context"].get("pending_question_unit_id") != original:
                            report["failures"].append("original question lost")
            source = send("De dónde sale eso")
            if "sección" not in (source["response"].get("output_text") or ""):
                report["failures"].append("source not verbalizable after full experience")
            proposed = send(case["closure"])
            if case.get("retained"):
                if proposed["context"].get("pending_conservation") != "none" or proposed["context"].get(
                    "close_confirmation_pending"
                ):
                    report["failures"].append("revocation and close conflated")
                revoked = send(case.get("revocation_confirmation", "Confirmo."))
                if (
                    revoked["status"] != "active"
                    or revoked["privacy"]["retain"]
                    or revoked["context"].get("close_confirmation_pending")
                ):
                    report["failures"].append("generic confirmation did not revoke separately")
                proposed = send(case["closure"])
            if not proposed["context"].get("close_confirmation_pending") or proposed["status"] != "active":
                report["failures"].append("compound close not proposed")
            closed = send(case["confirmation"])
            if closed["status"] != "closed_voluntary":
                report["failures"].append("pending close not confirmed")
        finally:
            app_client.post(
                f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"}
            )
            (output / (case["id"] + ".json")).write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        reports.append(report)
    summary = {
        "cases": len(reports),
        "passed": sum(not r["failures"] for r in reports),
        "failures": [{"case": r["case"]["id"], "failures": r["failures"]} for r in reports if r["failures"]],
        "capture_is_acceptance": False,
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assert len(reports) == 6 and summary["passed"] == 6, summary
