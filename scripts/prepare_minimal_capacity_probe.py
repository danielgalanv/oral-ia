"""Three tasks/five future calls only; preparing this file never starts a model."""

import hashlib
import json
from pathlib import Path

import pdfplumber

from oralia.course_dialogue.corpus import SOURCE_ROOT

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "minimal-capacity-probe-v1"
PASSAGE = "Can reveal the presence of errors NOT their absence."


def execution_budget():
    return {
        "diagnostic_pipe_requests_maximum": 5,
        "existing_worker_warmup_generate_calls": 1,
        "total_model_generate_invocations_maximum": 6,
        "diagnostic_new_tokens_maximum": 576,
        "warmup_new_tokens_maximum": 1,
        "total_new_tokens_maximum": 577,
        "load_and_warmup_deadline_seconds": 90,
        "each_diagnostic_request_deadline_ms": 30000,
        "estimated_total_duration_minutes": [2, 5],
        "gpu_availability_confirmation_required": True,
        "no_gpu_execution_in_preparation": True,
    }


def build_probe():
    copy_messages = [
        {
            "role": "system",
            "content": "Copia el dato solicitado. Devuelve solo un objeto JSON con la clave valor. "
            "Los valores posibles son AZUL y ROJO. No añadas explicación ni otras claves.",
        },
        {"role": "user", "content": "Dato a copiar: AZUL. Copia exactamente ese dato en valor."},
    ]
    scope_messages = [
        {
            "role": "system",
            "content": "Clasifica la pregunta usando únicamente la política breve. Devuelve solo "
            "un objeto JSON con la clave alcance y valor dentro, fuera o incierto. "
            "Dentro corresponde a un tema incluido; fuera solo a la petición de un bloque autónomo excluido; "
            "incierto si la política no permite "
            "decidir. No contestes la pregunta académica.",
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "politica_breve_de_esta_prueba": {
                        "incluidos": ["introducción a la Ingeniería del Software", "pruebas de software"],
                        "excluidos_como_bloques_autonomos": ["fiabilidad"],
                        "menciones_auxiliares_permitidas": True,
                        "tema_no_listado": "incierto",
                    },
                    "pregunta": "¿Qué abarca la Ingeniería del Software en términos generales?",
                },
                ensure_ascii=False,
            ),
        },
    ]
    explanation_messages = [
        {
            "role": "system",
            "content": "Explica en dos frases breves solo lo que dice el pasaje. Conserva tanto "
            "lo que las pruebas pueden revelar como lo que no pueden demostrar. "
            "No añadas ejemplos, técnicas, "
            "garantías ni hechos ajenos al pasaje. Responde en español, sin JSON.",
        },
        {"role": "user", "content": "Título documental: Program testing\n<pasaje>" + PASSAGE + "</pasaje>"},
    ]
    copy_options = [json.dumps({"valor": value}, separators=(",", ":")) for value in ("AZUL", "ROJO")]
    scope_options = [
        json.dumps({"alcance": value}, separators=(",", ":")) for value in ("dentro", "fuera", "incierto")
    ]
    rows = []
    for name, messages, cap, alternatives in (
        ("instruction_free", copy_messages, 64, None),
        ("instruction_finite", copy_messages, 64, copy_options),
        ("scope_free", scope_messages, 96, None),
        ("scope_finite", scope_messages, 96, scope_options),
        ("explain_free", explanation_messages, 256, None),
    ):
        rows.append(
            {
                "id": name,
                "messages": messages,
                "max_tokens": cap,
                "deadline_ms": 30000,
                "finite_outputs": alternatives,
                "message_profile": "academic/v1",
                "audit_config": True,
            }
        )
    oracle = {
        "instruction": {"expected_json": {"valor": "AZUL"}, "check": "strict_json_object_equality_no_repair"},
        "scope": {"expected_json": {"alcance": "dentro"}, "check": "strict_json_object_equality_no_repair"},
        "explanation": {
            "required_claims": [
                "testing can reveal presence of errors",
                "testing cannot prove absence of errors",
            ],
            "reject_if": [
                "guarantees absence of errors",
                "guarantees all user needs",
                "adds unsupported academic facts",
            ],
            "review": "clause_by_clause_diagnostic_review_against_single_passage; ambiguous_means_unknown",
            "no_predefined_answer": True,
            "not_an_automatic_semantic_verifier": True,
        },
    }
    return rows, oracle


def main():
    OUTPUT.mkdir(exist_ok=False)
    policy_path = EVIDENCE / "course-scope-policy-v1.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    name = "12 - Testing.pdf"
    source = SOURCE_ROOT / name
    expected = next(
        row["sha256"] for row in policy["source_scope"]["authorized_lab_documents"] if row["file"] == name
    )
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise ValueError("source changed")
    with pdfplumber.open(source) as pdf:
        text = pdf.pages[3].extract_text() or ""
        if PASSAGE not in text or "Program testing" not in text:
            raise ValueError("quoted passage absent")
    frames, oracle = build_probe()
    protocol = {
        "state": "CPU_prepared_only_GPU_availability_confirmation_required",
        "tasks": 3,
        "calls_maximum": 5,
        "retries": 0,
        "repairs": 0,
        "same_model": "Qwen2.5-7B-Instruct_a09a35458c702b33eeacc393d103063234e8bc28",
        "runtime": "D:/ai-toolkit/venv/Scripts/python.exe",
        "quantization": "nf4",
        "same_generation": (
            "current_worker_greedy_bfloat16_compute_double_quantization; pin generation_config"
        ),
        "inherited_repetition_penalty_expected": 1.05,
        "per_call_deadline_ms": 30000,
        "load_deadline_seconds": 90,
        "tokens_max_total": 576,
        "estimated_duration_minutes": [2, 5],
        "pair_only_changed_field": "finite_outputs",
        "same_model_visible_messages_within_pairs": True,
        "finite_choices_include_wrong_answers": True,
        "explanation_not_constrained": (
            "backend supports finite objects, not open semantic explanations; avoid predefined answer"
        ),
        "raw_worker_diagnostic_not_participant_or_normal_academic_adapter": True,
        "profile": "academic/v1_existing_raw_worker_protocol; no implicit adapter message insertion",
        "no_hidden_history": True,
        "fixed_order": [row["id"] for row in frames],
        "semantic_failure_does_not_adapt_or_retry": (
            "record all planned independent calls unless protocol/resource stop"
        ),
        "stop": "protocol_failure_or_resource_safety; preserve_unexecuted_ids",
        "gpu_coordination": "notify_model_duration_budget_and_wait_explicit_user_confirmation_before_weights",
        "telemetry": "before_during_after_after_confirmation; concurrent_use_makes_conditions_inconclusive",
        "receipts_required": [
            "raw_sent_frames",
            "rendered_prompt_hash_tokens",
            "ready_model_identity_template",
            "effective_generation_config_and_kwargs_not_just_temperature_label",
            "finite_prefix_flag",
            "raw_outputs_first_failures",
            "resources",
            "owned_cleanup",
            "new_budget",
        ],
        "interpretation": {
            "instruction_fails_both": (
                "basic_instruction_or_resource/config_problem_unresolved; stop_expanding_classifier"
            ),
            "only_finite_fails": (
                "format_constraint_interaction_suspected_not_proved; compare_captured_frames/config"
            ),
            "instruction_pass_scope_fails": "scope_semantics_not_mechanical_instruction_alone",
            "scope_pass_explanation_fails": "source_fidelity_is_a_separate_failure",
            "all_pass": "only_minimal_capability_not_course_coverage_transfer_or_G2",
        },
        "publication_allowed": False,
        "reserve_used": False,
        "old_budgets_reused": False,
    }
    provenance = {
        "document": name,
        "document_sha256": expected,
        "page": 4,
        "quote": PASSAGE,
        "page_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "policy_sha256": hashlib.sha256(policy_path.read_bytes()).hexdigest(),
    }
    for filename, value in (
        ("frames.json", frames),
        ("oracle.json", oracle),
        ("protocol.json", protocol),
        ("source.json", provenance),
        ("execution-budget.json", execution_budget()),
    ):
        (OUTPUT / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Three tasks/five calls prepared; no model loaded and GPU not authorized for this step.")


if __name__ == "__main__":
    main()
