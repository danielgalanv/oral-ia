"""Post-run integrity/resource audit, preserving original receipts and outcomes."""

import json
from pathlib import Path

from oralia.course_dialogue.finite_schema import finite_json_outputs
from oralia.course_dialogue.scope_control_messages import ScopeControlRequest, build_scope_control_messages
from oralia.course_dialogue.scope_message_profiles import validate_frame_profile
from scripts.diagnose_scope_control import final_resource_review
from scripts.trial_scope_finite import digest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKAGE = EVIDENCE / "scope-control-diagnostic-resource-v2"
RUN = EVIDENCE / "scope-control-diagnostic-resource-run"
OUTPUT = EVIDENCE / "scope-control-diagnostic-post-audit-v1.json"


def main():
    if OUTPUT.exists():
        raise ValueError("preserve post-run audit")
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    revised = []
    for name, expected in manifest.items():
        if digest(ROOT / name) == expected:
            continue
        original = PACKAGE / "artifacts" / name
        if not original.is_file() or digest(original) != expected:
            raise ValueError("frozen package damaged: " + name)
        revised.append(name)
    record = json.loads((RUN / "records.json").read_text(encoding="utf-8"))[0]
    attempt = record["attempts"][0]
    request = ScopeControlRequest.model_validate(attempt["request"])
    data = json.loads(request.student_input)
    raw = json.loads(attempt["exchange"]["raw_worker_response"])
    assert data["question"] == "¿Cuál es el objeto de estudio de la ingeniería del software?"
    assert data["blocks"] == json.loads(
        (EVIDENCE / "course-block-descriptions-v1.json").read_text(encoding="utf-8")
    )
    assert data["policy_sha256"] == digest(EVIDENCE / "course-scope-policy-v1.json")
    messages = build_scope_control_messages(request)
    frame = {
        "messages": messages,
        "message_profile": "scope-control-finite/v1",
        "finite_outputs": finite_json_outputs(request.output_schema),
    }
    assert validate_frame_profile(frame) == raw["message_profile"]
    assert (
        "Responde únicamente usando el contenido de las etiquetas <evidencia>" not in messages[1]["content"]
    )
    assert raw["finite_decoder"] is True and raw["text"] == attempt["outcome"]["text"]
    assert raw["text"] in frame["finite_outputs"]
    assert record["result"]["assessment"]["excluded_block_id"] == json.loads(raw["text"])["block"]
    samples = json.loads((RUN / "gpu-telemetry.json").read_text(encoding="utf-8"))
    early = json.loads((RUN / "resource-review.json").read_text(encoding="utf-8"))
    worker = json.loads((RUN / "worker.json").read_text(encoding="utf-8"))
    baseline = float(samples[0]["gpu"].split(",")[1])
    final = final_resource_review(
        samples, baseline, worker["memory_footprint_bytes"] / 1024**2, set(early["own_pids"])
    )
    budgets = {
        name: json.loads((EVIDENCE / name).read_text(encoding="utf-8"))["used"]
        for name in (
            "scope-classifier-call-budget.json",
            "scope-v2-described-budget.json",
            "scope-finite-capacity-budget.json",
            "scope-control-diagnostic-budget.json",
        )
    }
    assert list(budgets.values()) == [2, 1, 1, 1]
    result = {
        "question_policy_descriptions_consistent": True,
        "reconstructed_messages_match_confirmed_control_contract": True,
        "historical_empty_evidence_conflict_absent": True,
        "backend_choice_is_legal_but_semantically_wrong": True,
        "transport_defect_reproduced_in_this_call": False,
        "original_receipts_overwritten": False,
        "original_resource_review": early,
        "resource_review_from_complete_raw_telemetry": final,
        "resource_summary_was_written_before_pending_monitor_sample": early["pressure_observed"]
        != final["pressure_observed"],
        "post_run_live_changes_originals_preserved": revised,
        "budgets": budgets,
        "new_inferences": 0,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "Original package intact; confirmed control frame has no reproduced transport defect; "
        "resource audit retained separately."
    )


if __name__ == "__main__":
    main()
