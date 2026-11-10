"""One new finite-scope capacity proposal; freezes inputs without running inference."""

import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.finite_schema import finite_json_outputs
from oralia.course_dialogue.scope_finite import compile_targets

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-finite-capacity-v1"


def main():
    policy = json.loads((EVIDENCE / "course-scope-policy-v1.json").read_text(encoding="utf-8"))
    tokenizer_input = json.loads(
        (EVIDENCE / "scope-finite-tokenizer-input-v1.json").read_text(encoding="utf-8")
    )
    if tokenizer_input["targets"] != finite_json_outputs(compile_targets(policy)):
        raise ValueError("tokenizer check did not exercise the current compiled alternatives")
    OUTPUT.mkdir(exist_ok=False)
    bank, oracle = [], {}

    def add(text, status, block=None, excluded=None, history=None, referent=None, witnesses=None):
        key = f"F{len(bank)+1:02}"
        bank.append({"id": key, "text": text, "history": history or []})
        oracle[key] = {
            "status": status,
            "included_block": block,
            "excluded_block": excluded,
            "referent_turn": referent,
            "witnesses": witnesses or [],
            "basis": "policy_v1_and_literal_request_intention",
            "review": "technical_development_oracle_not_teacher_acceptance",
        }

    positives = [
        ("introduccion_ingenieria_software", "Sitúa la Ingeniería del Software como disciplina."),
        ("procesos_desarrollo", "Quiero entender las etapas de un proceso de desarrollo de software."),
        ("desarrollo_agil", "Centremos el estudio en los enfoques ágiles del desarrollo."),
        ("ingenieria_requisitos", "Necesito una explicación del trabajo con requisitos de software."),
        ("modelos_sistema", "Quiero comprender cómo representar un sistema mediante modelos."),
        (
            "herramientas_ingenieria_software",
            "Estudiemos las herramientas que apoyan la ingeniería del software.",
        ),
        ("diseno_arquitectura_patrones", "Mi duda trata del diseño y la arquitectura del software."),
        ("implementacion_software", "Explícame la implementación como actividad del desarrollo de software."),
        ("verificacion_validacion_pruebas", "Céntrate en comprobar y probar el software desarrollado."),
    ]
    for block, text in positives:
        add(text, "in_scope", block)
    add(
        "Desarrolla un curso propio de sistemas distribuidos.",
        "out_of_scope",
        excluded="sistemas_distribuidos",
    )
    add(
        "Quiero estudiar gestión de calidad como un bloque independiente.",
        "out_of_scope",
        excluded="gestion_calidad",
    )
    add(
        "Al explicar pruebas, aclara la condición del fragmento de código para que pueda seguir la prueba.",
        "in_scope",
        "verificacion_validacion_pruebas",
        witnesses=["condición del fragmento de código"],
    )
    add(
        "Dentro del diseño de requisitos, ayúdame con la mención de seguridad del sistema.",
        "in_scope",
        "ingenieria_requisitos",
        witnesses=["seguridad del sistema"],
    )
    add(
        "Presenta procesos de desarrollo; aparte, imparte fiabilidad como bloque propio.",
        "mixed",
        "procesos_desarrollo",
        "fiabilidad",
        witnesses=["Presenta procesos de desarrollo", "imparte fiabilidad como bloque propio"],
    )
    add(
        "Estudia costes como curso autónomo y también explica modelos de sistema.",
        "mixed",
        "modelos_sistema",
        "estimacion_costes",
        witnesses=["explica modelos de sistema", "Estudia costes como curso autónomo"],
    )
    previous = [
        {
            "input": "Quiero estudiar desarrollo ágil",
            "displayed_text": "Vista previa del tema ágil.",
            "displayed_kind": "laboratory_preview",
        }
    ]
    add(
        "No lo entiendo, muéstralo de otra forma", "in_scope", "desarrollo_agil", history=previous, referent=0
    )
    ambiguous = [
        {
            "input": "procesos de desarrollo y modelos de sistema",
            "displayed_text": "Has planteado dos asuntos. ¿Sobre cuál quieres preguntar?",
            "displayed_kind": "operational",
        }
    ]
    add("¿Por qué?", "uncertain_scope", history=ambiguous)
    add("¿Cómo se interpreta un poema medieval?", "uncertain_scope")
    if len(bank) != 18:
        raise ValueError("one 18-question proposal required")
    protocol = {
        "state": "proposal_only_no_gpu_inference",
        "contract": "finite_scope_lab_v1",
        "new_questions": 18,
        "new_call_limit": 72,
        "maximum_calls_per_question": 4,
        "shared_deadline_per_question_ms": 30000,
        "shared_tokens_per_question": 512,
        "call_token_caps": {"target": 128, "referent": 32, "each_literal": 176},
        "each_call_deadline": "remaining shared wall time, at most 30000ms; no start below 1000ms",
        "minimum_call_shape": "one finite target for explicit standalone question",
        "conditional_steps": (
            "referent only for contextual planning; one literal for auxiliary, two for mixed"
        ),
        "load_deadline_seconds": 90,
        "upper_wall_bound_seconds_excluding_preparation": 630,
        "retries": 0,
        "repairs": 0,
        "fallback_to_hint": "forbidden_for_finite_steps",
        "literals_fully_constrained": False,
        "automatic_literal_semantics_verified": False,
        "model": "existing_Qwen2.5-7B_a09a3545_nf4_no_download",
        "old_call_budgets_reused": False,
        "stop": "first_false_exclusion_mixed_leak_finite_fallback_protocol_error_or_resource_pressure",
        "format_metrics": [
            "finite_flag_raw",
            "alternative_membership",
            "literal_unique_match",
            "step_receipts",
        ],
        "semantic_metrics": [
            "scope_status",
            "policy_block",
            "auxiliary_relation",
            "reference",
            "mixed_boundary",
        ],
        "coverage_metrics": ["decidable_answered", "unknown_false_abstentions", "unexecuted_ids"],
        "resource_metrics": [
            "gpu_before_during_after",
            "wall_and_tokens_per_step",
            "pressure",
            "resource_inconclusive",
        ],
        "continuation_threshold": {
            "false_exclusions": 0,
            "mixed_leaks": 0,
            "finite_fallbacks": 0,
            "positive_blocks_correct": 9,
            "cases_correct_minimum": 15,
        },
        "resource_policy": "low_load_samples_and_sufficient_VRAM_residence_alone_does_not_block",
        "memory_peak_does_not_prove_foreign_activity": True,
        "scope_eval_does_not_verify_academic_answers": True,
        "publication_allowed": False,
        "reserve_used": False,
        "if_passes": "connect_scope_to_lab_RAG_only_with_existing_source_and_publication_gates",
    }
    for name, value in (("bank.json", bank), ("oracle.json", oracle), ("protocol.json", protocol)):
        (OUTPUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    names = [
        "src/oralia/course_dialogue/scope_finite.py",
        "src/oralia/course_dialogue/finite_schema.py",
        "src/oralia/course_dialogue/context.py",
        "src/oralia/course_dialogue/scope_block_metadata.py",
        "src/oralia/course_dialogue/cached_transformers.py",
        "src/oralia/course_dialogue/gpu_worker.py",
        "tests/course_dialogue/test_scope_finite.py",
        "scripts/check_scope_tokenizer.py",
        "scripts/freeze_scope_finite_capacity.py",
        "specs/012-conversational-course-study/evidence/course-block-descriptions-v1.json",
        "specs/012-conversational-course-study/evidence/course-scope-policy-v1.json",
        "specs/012-conversational-course-study/evidence/scope-finite-tokenizer-input-v1.json",
        "specs/012-conversational-course-study/evidence/scope-finite-tokenizer-check-v1.json",
    ]
    paths = [ROOT / name for name in names] + [
        OUTPUT / name for name in ("bank.json", "oracle.json", "protocol.json")
    ]
    for path in list(paths):
        copy = OUTPUT / "artifacts" / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        paths.append(copy)
    (OUTPUT / "manifest.json").write_text(
        json.dumps(
            {
                path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in paths
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Frozen one new 18-question proposal; zero model inferences.")


if __name__ == "__main__":
    main()
