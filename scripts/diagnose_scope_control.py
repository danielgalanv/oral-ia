"""One bounded corrected-transport diagnostic; no semantic or model variant ladder."""

import asyncio
import json
import sqlite3
import sys
from pathlib import Path

import psutil
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue.cached_transformers import CACHED_MODEL_7B, cached_provider
from oralia.course_dialogue.corpus import SOURCE_ROOT
from oralia.course_dialogue.gpu_resource_policy import gpu_values, resource_period
from oralia.course_dialogue.rag_lab import ActivityScopeBinding
from oralia.course_dialogue.scope_block_metadata import BlockMetadata
from oralia.course_dialogue.scope_finite import literal_span
from scripts.trial_course_scope import compute_pids, save, snapshot
from scripts.trial_scope_finite import digest, run_questions

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
PACKAGE = EVIDENCE / "scope-control-diagnostic-resource-v2"
OUTPUT = EVIDENCE / "scope-control-diagnostic-resource-run"
BUDGET = EVIDENCE / "scope-control-diagnostic-budget.json"


def build_inputs():
    cases, oracle = [], {}

    def add(
        text,
        status,
        block=None,
        excluded=None,
        *,
        history=None,
        referent=None,
        witness_terms=None,
        excluded_terms=None,
    ):
        key = f"C{len(cases)+1:02}"
        cases.append({"id": key, "text": text, "history": history or []})
        oracle[key] = {
            "status": status,
            "included_block": block,
            "excluded_block": excluded,
            "referent_turn": referent,
            "witness_terms": witness_terms or [],
            "excluded_terms": excluded_terms or [],
            "author": "technical_policy_derived_development_oracle",
        }

    add(
        "¿Cuál es el objeto de estudio de la ingeniería del software?",
        "in_scope",
        "introduccion_ingenieria_software",
    )
    add("¿Para qué se representan los sistemas con modelos?", "in_scope", "modelos_sistema")
    add(
        "Me interesa la implementación dentro del desarrollo de software.",
        "in_scope",
        "implementacion_software",
    )
    add("Quiero cursar seguridad como materia independiente.", "out_of_scope", excluded="seguridad")
    add(
        "Ayúdame a escribir un requisito de seguridad.",
        "in_scope",
        "ingenieria_requisitos",
        witness_terms=["seguridad"],
    )
    add(
        "Deseo un curso separado de sintaxis de C++.",
        "out_of_scope",
        excluded="tutoria_autonoma_sintaxis_programacion",
    )
    add(
        "Para seguir la prueba, aclara el significado del bucle del ejemplo.",
        "in_scope",
        "verificacion_validacion_pruebas",
        witness_terms=["bucle"],
    )
    add(
        "Explica desarrollo ágil y, aparte, un tema autónomo de fiabilidad.",
        "mixed",
        "desarrollo_agil",
        "fiabilidad",
        witness_terms=["desarrollo", "ágil"],
        excluded_terms=["fiabilidad"],
    )
    add(
        "Quiero un curso independiente de costes; después explica requisitos.",
        "mixed",
        "ingenieria_requisitos",
        "estimacion_costes",
        witness_terms=["requisitos"],
        excluded_terms=["costes"],
    )
    history = [
        {
            "input": "modelos de sistema",
            "displayed_text": "Vista previa sobre modelos de sistema.",
            "displayed_kind": "laboratory_preview",
        }
    ]
    add("Repite eso con otras palabras", "in_scope", "modelos_sistema", history=history, referent=0)
    add("¿En qué consiste la tectónica de placas?", "uncertain_scope")
    add("/fuentes", "operational")
    protocol = {
        "diagnostic_only_not_nine_block_coverage_or_transfer": True,
        "new_questions": 12,
        "new_call_limit": 48,
        "maximum_calls_per_question": 4,
        "shared_deadline_per_question_ms": 30000,
        "shared_tokens_per_question": 512,
        "step_token_caps": {"target": 128, "referent": 32, "each_literal": 176},
        "message_profile": "scope-control/v1",
        "model": "existing_Qwen2.5-7B_a09a3545_nf4",
        "changed_variable": "corrected_control_transport_not_semantic_logic_or_model",
        "retries": 0,
        "repairs": 0,
        "old_budgets_used": False,
        "stop": "first_false_exclusion_mixed_leak_protocol_error_or_observed_resource_pressure",
        "required_profiles": ["scope-control-finite/v1", "scope-control-literal/v1"],
        "finite_decoder_required_for_target_and_referent": True,
        "witness_oracle": "unique_literal_with_frozen_required_terms_not_full_semantic_proof",
        "resource_policy": (
            "five_low_load_samples_sufficient_VRAM_residency_not_active_load_monitor_before_during_after"
        ),
        "resource_attribution": "unattributed_pressure_or_uncertainty_is_not_proof_of_foreign_activity",
        "resource_stop": "free_VRAM_below_2048_MiB_or_telemetry_unavailable_not_peak_over_estimate",
        "preflight_max_utilization_percent": 10,
        "preflight_samples": 5,
        "preflight_min_free_mib": 10000,
        "preflight_max_memory_range_mib": 256,
        "resource_only_revision": (
            "old_5_percent_checks_deferred_without_weights_or_calls; semantics_unchanged"
        ),
        "diagnostic_success": (
            "all_12_correct_zero_exclusion_leak_protocol_resource_failures_all_profiles_confirmed"
        ),
        "publication_allowed": False,
        "reserve_used": False,
    }
    return cases, oracle, protocol


def freeze():
    PACKAGE.mkdir(exist_ok=False)
    bank, oracle, protocol = build_inputs()
    original = EVIDENCE / "scope-control-diagnostic-v1-final"
    if original.exists():
        if bank != json.loads((original / "bank.json").read_text(encoding="utf-8")) or (
            oracle != json.loads((original / "oracle.json").read_text(encoding="utf-8"))
        ):
            raise ValueError("resource revision must not change bank or oracle")
    for name, value in (("bank.json", bank), ("oracle.json", oracle), ("protocol.json", protocol)):
        save(PACKAGE / name, value)
    names = [
        "scripts/diagnose_scope_control.py",
        "scripts/trial_scope_finite.py",
        "scripts/trial_course_scope.py",
        "tests/course_dialogue/test_scope_control_diagnostic.py",
        "src/oralia/course_dialogue/cached_transformers.py",
        "src/oralia/course_dialogue/gpu_worker.py",
        "src/oralia/course_dialogue/scope_finite.py",
        "src/oralia/course_dialogue/scope_message_profiles.py",
        "src/oralia/course_dialogue/scope_control_messages.py",
        "src/oralia/course_dialogue/finite_schema.py",
        "src/oralia/course_dialogue/scope_block_metadata.py",
        "src/oralia/course_dialogue/gpu_resource_policy.py",
        "src/oralia/course_dialogue/context.py",
        "src/oralia/course_dialogue/owned_worker.py",
        "specs/012-conversational-course-study/evidence/course-scope-policy-v1.json",
        "specs/012-conversational-course-study/evidence/course-block-descriptions-v1.json",
    ]
    paths = [ROOT / name for name in names] + [
        PACKAGE / name for name in ("bank.json", "oracle.json", "protocol.json")
    ]
    for path in list(paths):
        copy = PACKAGE / "artifacts" / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        paths.append(copy)
    save(PACKAGE / "manifest.json", {p.relative_to(ROOT).as_posix(): digest(p) for p in paths})


def load(package=PACKAGE, root=ROOT):
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        if digest(root / name) != expected:
            raise ValueError("diagnostic artifact changed: " + name)
    bank = json.loads((package / "bank.json").read_text(encoding="utf-8"))
    oracle = json.loads((package / "oracle.json").read_text(encoding="utf-8"))
    protocol = json.loads((package / "protocol.json").read_text(encoding="utf-8"))
    if [c["id"] for c in bank] != [f"C{i:02}" for i in range(1, 13)] or set(oracle) != {
        c["id"] for c in bank
    }:
        raise ValueError("exactly twelve diagnostic IDs required")
    if protocol["new_call_limit"] != 48 or protocol["message_profile"] != "scope-control/v1":
        raise ValueError("wrong diagnostic budget/profile")
    return bank, oracle, protocol, manifest


def unsafe_resources(sample):
    # A peak above a footprint estimate can be the worker's own prefill. It is
    # logged as unattributed, not used as evidence of a shortage or foreign load.
    return gpu_values(sample)[2] < 2048


def diagnostic_preflight(samples):
    values = [gpu_values(sample) for sample in samples]
    ready = (
        len(values) >= 5
        and all(use <= 10 and free >= 10000 for use, _, free in values)
        and (max(used for _, used, _ in values) - min(used for _, used, _ in values) <= 256)
    )
    return {
        "ready": ready,
        "reason": "observed_low_load" if ready else "observed_load_or_memory",
        "exclusive_gpu_claimed": False,
        "max_utilization_percent": max(v[0] for v in values),
        "utilization_limit_percent": 10,
    }


def final_resource_review(samples, baseline, own_mib, own_pids):
    valid = [s for s in samples if "gpu" in s]
    return {
        "pressure_observed": any(unsafe_resources(s) for s in valid) or any("error" in s for s in samples),
        "minimum_free_mib": min((gpu_values(s)[2] for s in valid), default=None),
        "unattributed_peak_over_estimate_observed": (
            any(resource_period([s], baseline, own_mib) == "resource-pressure-observed" for s in valid)
            if own_mib is not None
            else None
        ),
        "own_pids": sorted(own_pids),
        "foreign_compute_pids": sorted(
            {pid for s in samples if "process_table" in s for pid in compute_pids(s)} - own_pids
        ),
        "memory_peak_proves_foreign_activity": False,
        "exclusive_gpu_claimed": False,
        "performance_status": "resource-inconclusive",
    }


def evaluate(case, expected, result):
    actual = result.assessment
    finite = [step for step in result.receipts if step["request"]["output_schema"] is not None]
    raw = [
        json.loads((step.get("exchange") or {}).get("raw_worker_response") or "{}")
        for step in result.receipts
    ]
    confirmed = sum(
        r.get("message_profile")
        == ("scope-control-finite/v1" if s["request"]["output_schema"] else "scope-control-literal/v1")
        for s, r in zip(result.receipts, raw, strict=True)
    )
    enforced = sum(
        r.get("finite_decoder") is True
        for s, r in zip(result.receipts, raw, strict=True)
        if s["request"]["output_schema"] is not None
    )
    complete = sum((s.get("outcome") or {}).get("finish_reason") == "stop" for s in finite)
    target = next(
        (
            json.loads(s["outcome"]["text"])
            for s in result.receipts
            if s["step"] == "target" and s.get("outcome")
        ),
        {},
    )
    quotes = [
        (s.get("outcome") or {}).get("text", "")
        for s in result.receipts
        if s["step"] in {"supporting_mention", "included_part", "excluded_standalone_part"}
    ]
    witness_valid = all(literal_span(case["text"], quote) is not None for quote in quotes)
    scope_correct = (
        actual.status == expected["status"]
        and actual.block_id == expected["included_block"]
        and (actual.excluded_block_id == expected["excluded_block"])
    )
    semantic_witness = True
    if expected["witness_terms"]:
        semantic_witness = (
            bool(quotes)
            and witness_valid
            and all(term in quotes[0].casefold() for term in expected["witness_terms"])
        )
        if expected["status"] == "mixed":
            semantic_witness = (
                semantic_witness
                and len(quotes) == 2
                and all(
                    term in quotes[1].casefold() and term not in quotes[0].casefold()
                    for term in expected["excluded_terms"]
                )
            )
        else:
            semantic_witness = semantic_witness and target.get("intent") == "auxiliary"
    false_exclusion = actual.status in {"out_of_scope", "mixed"} and (
        expected["status"] not in {"out_of_scope", "mixed"}
        or actual.excluded_block_id != expected["excluded_block"]
        or (actual.status == "out_of_scope" and expected["status"] == "mixed")
    )
    mixed_leak = (
        expected["status"] == "mixed"
        and result.rag_question is not None
        and (actual.status != "mixed" or not semantic_witness or result.rag_history != ())
    )
    formal = len(finite) == enforced == complete and confirmed == len(result.receipts)
    return {
        "id": case["id"],
        "expected": expected["status"],
        "actual": actual.status,
        "scope_correct": scope_correct,
        "witness_oracle_correct": semantic_witness,
        "reference_correct": result.referent_turn == expected["referent_turn"],
        "correct": formal
        and scope_correct
        and semantic_witness
        and result.referent_turn == expected["referent_turn"],
        "formal_correct": formal,
        "profile_steps": len(result.receipts),
        "profiles_confirmed": confirmed,
        "finite_steps": len(finite),
        "finite_enforced": enforced,
        "finite_complete": complete,
        "literal_steps": len(quotes),
        "unique_literals": sum(literal_span(case["text"], q) is not None for q in quotes),
        "false_abstention": actual.status == "uncertain_scope" and expected["status"] != "uncertain_scope",
        "false_exclusion": false_exclusion,
        "mixed_leak": mixed_leak,
        "critical": false_exclusion or mixed_leak or not formal,
        "error_kind": None,
    }


def summarize(bank, oracle, rows):
    matrix = {}
    for row in rows:
        label = row["expected"] + " -> " + row["actual"]
        matrix[label] = matrix.get(label, 0) + 1
    result = {
        "executed": len(rows),
        "not_executed": len(bank) - len(rows),
        "not_executed_ids": [c["id"] for c in bank if c["id"] not in {r["id"] for r in rows}],
        "matrix": matrix,
        "correct": sum(r["correct"] for r in rows),
        "protocol_errors": sum(r["error_kind"] == "protocol" for r in rows),
        "resource_errors": sum(r["error_kind"] == "resource" for r in rows),
    }
    for name in (
        "false_exclusion",
        "mixed_leak",
        "false_abstention",
        "profile_steps",
        "profiles_confirmed",
        "finite_steps",
        "finite_enforced",
        "finite_complete",
        "literal_steps",
        "unique_literals",
    ):
        result[name] = sum(r.get(name, 0) for r in rows)
    result["passed_diagnostic_only"] = (
        len(rows) == 12
        and result["correct"] == 12
        and result["protocol_errors"] == result["resource_errors"] == 0
    )
    return result


async def main():
    bank, oracle, protocol, manifest = load()
    OUTPUT.mkdir(exist_ok=False)
    samples, rows = [], []
    for _ in range(5):
        samples.append({"phase": "before", **await snapshot()})
        await asyncio.sleep(2)
    readiness = diagnostic_preflight(samples)
    save(OUTPUT / "preflight.json", readiness)
    if not readiness["ready"]:
        samples.append({"phase": "after_not_run", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "not-run.json", {"reason": "observed_load_or_memory"})
        save(OUTPUT / "metrics.json", summarize(bank, oracle, []))
        return
    baseline = gpu_values(samples[-1])[1]
    database = ROOT / ".oralia-course-study/course.db"
    engine = create_engine(
        "sqlite://", creator=lambda: sqlite3.connect("file:" + database.as_posix() + "?mode=ro", uri=True)
    )
    db = Session(engine)
    policy_path = EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    binding = ActivityScopeBinding(
        engine,
        policy["activity_id"],
        policy["activity_version"],
        policy["course_id"],
        policy_path,
        digest(policy_path),
        SOURCE_ROOT,
    )
    metadata_path = EVIDENCE / "course-block-descriptions-v1.json"
    metadata = BlockMetadata(metadata_path, manifest[metadata_path.relative_to(ROOT).as_posix()])
    metadata.revalidate(binding, binding.revalidate(db))
    stop, pressure = asyncio.Event(), asyncio.Event()
    own_mib = None
    own_pids = set()
    reason = "preparation_incomplete"

    async def monitor():
        while not stop.is_set():
            try:
                sample = await snapshot()
                samples.append(sample)
                if unsafe_resources(sample):
                    pressure.set()
            except Exception as error:
                samples.append({"error": type(error).__name__})
                pressure.set()
            save(OUTPUT / "gpu-telemetry.json", samples)
            try:
                await asyncio.wait_for(stop.wait(), 2)
            except TimeoutError:
                pass

    monitor_task = asyncio.create_task(monitor())
    try:
        async with cached_provider(
            OUTPUT, source=CACHED_MODEL_7B, quantization="nf4", message_profile="scope-control/v1"
        ) as provider:
            worker = json.loads((OUTPUT / "worker.json").read_text(encoding="utf-8"))
            own_mib = worker["memory_footprint_bytes"] / 1024**2
            process = psutil.Process(provider.process.pid)
            own_pids = {process.pid, *(p.pid for p in process.children(recursive=True))}

            async def resources():
                sample = await snapshot()
                samples.append({"phase": "between_questions", **sample})
                return not pressure.is_set() and not unsafe_resources(sample)

            _, rows, reason = await run_questions(
                bank,
                oracle,
                protocol,
                provider=provider,
                binding=binding,
                db=db,
                metadata=metadata,
                output=OUTPUT,
                budget_path=BUDGET,
                proposal_hash=digest(PACKAGE / "manifest.json"),
                resource_check=resources,
                stop_requested=pressure.is_set,
                evaluate_fn=evaluate,
                summarize_fn=summarize,
            )
    finally:
        stop.set()
        await monitor_task
        samples.append({"phase": "after", **await snapshot()})
        save(OUTPUT / "gpu-telemetry.json", samples)
        save(OUTPUT / "resource-review.json", final_resource_review(samples, baseline, own_mib, own_pids))
        save(OUTPUT / "metrics.json", summarize(bank, oracle, rows))
        save(OUTPUT / "termination.json", {"reason": reason, "publication_allowed": False})
        db.close()
        engine.dispose()


if __name__ == "__main__":
    if sys.argv[1:] == ["--freeze"]:
        freeze()
    elif not sys.argv[1:]:
        asyncio.run(main())
    else:
        raise ValueError("no diagnostic overrides")
