"""Observe real public controlled dialogues; independent persisted safety checks.

Reports are synthetic engineering evidence. A failed property is retained, never
replaced by an expected response, and semantic/human usefulness is not inferred.
"""

import hashlib
import json
import re
import time
from pathlib import Path
from uuid import uuid4

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures"


def frozen_cases(partition):
    freeze = json.loads((FIXTURES / "freeze.json").read_text(encoding="utf-8"))
    path = FIXTURES / f"{partition}.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == freeze["sha256"][path.name]
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def run_case(client, case, *, condition="agency"):
    prepared = prepare_guided(
        client, domain=case["domain"], mode=case["mode"], study_mode=case.get("study_mode")
    )
    sid = prepared["session"]["session_id"]
    study = case["mode"] == "self_study"
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns" if study else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    observed = []
    failures = []
    previous_pending = None
    started = time.perf_counter()
    steps = case["steps"] if study else [{"actor": "system", "text": ""}, *case["steps"]]
    previous_notice = None
    for index, step in enumerate(steps):
        result = client.post(endpoint, json={"text": step["text"], "client_request_id": str(uuid4())})
        if result.status_code != 200:
            failures.append(
                {
                    "step": index,
                    "property": "public_turn_available",
                    "http_status": result.status_code,
                    "detail": result.json(),
                }
            )
            break
        response = result.json()
        status = response.get("dialogue_status") or {}
        notice = status.get("notice")
        with client.__db_sessionmaker__() as db:
            session = db.get(models.Session, sid)
            state = db.get(models.CognitiveState, sid)
            context = state.dialogue_context or {} if state else {}
            turn = db.get(models.Turn, response["turn_id"])
            verdict = db.get(models.VerificationResult, turn.verification_result_id)
            proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
            from oralia.domain.dialogue.catalog import GUIDED_NOTICES

            erased_finish = (
                session.status != "active"
                and response["output_text"] == GUIDED_NOTICES["finish"].text
                and proposal is not None
                and "text" not in proposal.content
            )
            if response["output_text"] is not None and not (
                verdict
                and verdict.verdict == "approved"
                and proposal
                and proposal.turn_id == turn.id
                and (proposal.content.get("text") == response["output_text"] or erased_finish)
            ):
                failures.append({"step": index, "property": "authorized_current_evidence"})
            if status.get("rendered_unit_ids") and status.get("grounding_verdict") != "fundamentada":
                failures.append({"step": index, "property": "independent_grounding"})
            protected = not study or response.get("mode") == "practice_questions"
            if protected and status.get("rendered_unit_ids"):
                if status.get("non_disclosure_verdict") != "approved":
                    failures.append({"step": index, "property": "independent_non_disclosure"})
                if any(source.get("fragment_text") for source in response["sources"]):
                    failures.append({"step": index, "property": "no_solution_disclosure"})
                goals = {db.get(models.TeachingUnit, uid).subgoal_ref for uid in status["rendered_unit_ids"]}
                solution_numbers = {
                    number
                    for unit in db.query(models.TeachingUnit)
                    .filter_by(course_id=prepared["activity"]["course_id"])
                    .all()
                    if unit.subgoal_ref in goals and unit.reveal_policy in {"study_only", "solution"}
                    for number in re.findall(r"\b\d+(?:[.,]\d+)?\b", unit.reviewed_content)
                }
                if solution_numbers & set(
                    re.findall(r"\b\d+(?:[.,]\d+)?\b", response.get("output_text") or "")
                ):
                    failures.append(
                        {
                            "step": index,
                            "property": "no_solution_disclosure",
                            "reason": "solution_numeric_anchor_in_visible_content",
                        }
                    )
            if notice is not None and notice == previous_notice:
                failures.append(
                    {"step": index, "property": "no_consecutive_identical_generic_alerts", "notice": notice}
                )
            pending = context.get("pending_question_unit_id")
            confirmed_topic = step["text"].casefold().startswith(("confirmo", "elijo ")) and bool(
                observed and (observed[-1]["response"].get("dialogue_status") or {}).get("pending_topic")
            )
            if (
                session.status == "active"
                and previous_pending
                and not confirmed_topic
                and status.get("primary_act") in {"help", "repeat", "rephrase", "content_answer"}
                and previous_pending != pending
            ):
                failures.append({"step": index, "property": "stable_pending_objective"})
            if status.get("latency_ms", 0) > status.get("turn_budget_ms", 10000):
                failures.append({"step": index, "property": "finite_budget"})
            if re.search(
                r"(?:tu nota|te califico|tu capacidad académica)", response.get("output_text") or "", re.I
            ):
                failures.append({"step": index, "property": "no_grades_or_participant_profile"})
            observed.append(
                {
                    "step": index,
                    "actor": step["actor"],
                    "input": step["text"],
                    "response": response,
                    "pending_question_unit_id": pending,
                    "topic_ref": context.get("current_topic_ref"),
                    "session_status": session.status,
                }
            )
            previous_pending = pending
            previous_notice = notice
            terminal = session.status != "active"
        if terminal:
            if index < len(steps) - 1:
                failures.append({"step": index, "property": "premature_close"})
            break
    for index, turn in enumerate(observed):
        status = turn["response"].get("dialogue_status") or {}
        if status.get("notice") and index + 2 < len(observed):
            following = observed[index + 1 : index + 3]
            if not any(
                (item["response"].get("dialogue_status") or {}).get("rendered_unit_ids")
                or item["session_status"] != "active"
                for item in following
            ):
                failures.append({"step": index, "property": "executable_recovery_within_two_turns"})
    close_endpoint = (
        f"/api/v1/sessions/{sid}/study-end" if study else f"/api/v1/defense-sessions/{sid}/defense-end"
    )
    checked(client.post(close_endpoint))
    return {
        "case_id": case["case_id"],
        "partition": case["partition"],
        "domain": case["domain"],
        "mode": case["mode"],
        "study_mode": case.get("study_mode"),
        "seed": case["seed"],
        "profile": "guided_controlled",
        "condition": condition,
        "provider": "reviewed-unit-renderer/v1",
        "source_sha256": hashlib.sha256(
            (ROOT / "materiales/docente/dialogue" / f"{case['domain']}-v1.md").read_bytes()
        ).hexdigest(),
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "observations": observed,
        "failures": failures,
        "content_property_failures": [
            item
            for item in failures
            if item["property"] not in {"independent_grounding", "independent_non_disclosure"}
        ],
        "passed_measured_properties": not failures,
        "human_utility": "not_evaluated",
    }
