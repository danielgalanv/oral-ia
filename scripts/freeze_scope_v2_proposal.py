"""Freeze one new combined v2+descriptions development trial, not an inference run."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-v2-described-proposal-v1-final"


def save(name, value):
    (OUTPUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    OUTPUT.mkdir(exist_ok=False)
    metadata_path = EVIDENCE / "course-block-descriptions-v1.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    included = [row for row in metadata["blocks"] if row["category"] == "included_blocks"]
    positives = [
        "¿Qué estudia en general la Ingeniería del Software?",
        "¿Para qué sirve definir un proceso de desarrollo?",
        "¿Qué caracteriza un enfoque ágil de desarrollo?",
        "¿Cuál es el propósito de especificar los requisitos de un sistema?",
        "¿Para qué se construye un modelo de un sistema?",
        "¿Cómo ayudan las herramientas a las actividades de ingeniería del software?",
        "¿Qué se decide al diseñar la arquitectura de una aplicación?",
        "¿Qué lugar ocupa implementar el software en su desarrollo?",
        "¿Qué finalidad tienen la verificación y la validación del software?",
    ]
    cases, oracle = [], {}

    def add(
        text,
        intent,
        block=None,
        excluded=None,
        history=None,
        referent=None,
        allowed_quote=None,
        excluded_quote=None,
        mention=None,
    ):
        key = f"N{len(cases)+1:02}"
        cases.append({"id": key, "text": text, "history": history or []})
        oracle[key] = {
            "primary_intent": intent,
            "included_block": block,
            "excluded_block": excluded,
            "referent_turn": referent,
            "allowed_quote": allowed_quote,
            "excluded_quote": excluded_quote,
            "supporting_mention": mention,
            "basis": "approved_policy_v1_and_literal_request_purpose",
            "oracle_author": "technical_policy_derived_not_teacher_semantic_acceptance",
        }

    for row, text in zip(included, positives, strict=True):
        add(text, "included_request", row["id"])
    for excluded, standalone_text, auxiliary_text, anchor, mention in [
        (
            "seguridad",
            "Quiero una lección completa de seguridad como asignatura propia.",
            "Ayúdame a especificar un requisito de seguridad de esta aplicación.",
            "ingenieria_requisitos",
            "seguridad",
        ),
        (
            "gestion_configuracion",
            "Quiero estudiar gestión de configuración como unidad independiente.",
            "Al describir una prueba, ¿cómo indico la configuración utilizada?",
            "verificacion_validacion_pruebas",
            "configuración",
        ),
        (
            "tutoria_autonoma_sintaxis_programacion",
            "Necesito un curso independiente de sintaxis de Java.",
            "Para entender esta prueba, aclárame el significado de la condición del código.",
            "verificacion_validacion_pruebas",
            "condición del código",
        ),
        (
            "fiabilidad",
            "Desarrolla fiabilidad como tema autónomo del curso.",
            "¿Cómo redacto un requisito de fiabilidad para este sistema?",
            "ingenieria_requisitos",
            "fiabilidad",
        ),
    ]:
        add(standalone_text, "excluded_standalone_request", excluded=excluded)
        add(auxiliary_text, "included_with_supporting_mention", anchor, mention=mention)
    for text, anchor, excluded, allowed, rejected in [
        (
            "Explica modelos de sistema y prepara aparte un curso de sistemas empotrados.",
            "modelos_sistema",
            "sistemas_empotrados",
            "Explica modelos de sistema",
            "prepara aparte un curso de sistemas empotrados",
        ),
        (
            "Primero un curso de costes; después explícame desarrollo ágil.",
            "desarrollo_agil",
            "estimacion_costes",
            "explícame desarrollo ágil",
            "Primero un curso de costes",
        ),
        (
            "Describe herramientas de ingeniería de software "
            "y enséñame gestión de equipos como bloque propio.",
            "herramientas_ingenieria_software",
            "gestion_equipos_desarrollo",
            "Describe herramientas de ingeniería de software",
            "enséñame gestión de equipos como bloque propio",
        ),
        (
            "Estudiemos reutilización como tema autónomo; "
            "también quiero una explicación de implementación de software.",
            "implementacion_software",
            "reutilizacion_software",
            "quiero una explicación de implementación de software",
            "Estudiemos reutilización como tema autónomo",
        ),
    ]:
        add(
            text,
            "included_and_excluded_standalone_requests",
            anchor,
            excluded,
            allowed_quote=allowed,
            excluded_quote=rejected,
        )
    models = [
        {
            "input": "Quiero entender modelos de sistema",
            "displayed_text": "Vista de laboratorio sobre modelos de sistema.",
            "displayed_kind": "laboratory_preview",
        }
    ]
    add(
        "Muéstrame otro ejemplo del mismo tema",
        "included_request",
        "modelos_sistema",
        history=models,
        referent=0,
    )
    outside = [
        {
            "input": "Quiero estudiar costes como tema autónomo",
            "displayed_text": "Ese bloque autónomo está excluido por esta actividad.",
            "displayed_kind": "operational",
        }
    ]
    add(
        "Explícame ese bloque desde el principio",
        "excluded_standalone_request",
        excluded="estimacion_costes",
        history=outside,
        referent=0,
    )
    ambiguous = [
        {
            "input": "He mencionado procesos y modelos",
            "displayed_text": "Has mencionado dos temas. ¿Cuál quieres tratar?",
            "displayed_kind": "operational",
        }
    ]
    add("¿Y eso cómo se hace?", "unclear_request", history=ambiguous)
    add(
        "Cambiemos de tema: explica requisitos de software",
        "included_request",
        "ingenieria_requisitos",
        history=models,
    )
    add("¿Cómo se forman las galaxias?", "unclear_request")
    add("¿Ese tema entra aquí?", "unclear_request")
    add("/fuentes", "session_operation")
    if len(cases) != 28:
        raise ValueError("expected one new 28-case bank")
    save("bank.json", cases)
    save("oracle.json", oracle)
    save(
        "protocol.json",
        {
            "proposal_version": 1,
            "contract_version": 2,
            "metadata_version": 1,
            "state": "frozen_proposal_not_executed",
            "combined_changes_no_causal_attribution": True,
            "resource": "existing_Qwen2.5-7B_snapshot_a09a3545_nf4_same_worker_no_download",
            "total_new_call_budget": 28,
            "max_calls_per_case": 1,
            "retries": 0,
            "old_budget_reused": False,
            "old_trial_calls_consumed": 2,
            "old_remaining_calls_not_available_for_this_proposal": 18,
            "max_tokens": 256,
            "deadline_ms": 30000,
            "load_deadline_seconds": 90,
            "upper_bound_seconds_excluding_offline_preparation": 930,
            "resource_policy": "five_low_load_samples_vram_sufficient_monitor_before_during_after",
            "resident_context_not_proof_of_active_load": True,
            "uncertain_or_contended_latency": "resource-inconclusive",
            "stop": "first_false_exclusion_mixed_leak_contract_error_or_observed_resource_pressure",
            "continuation_threshold": {
                "false_exclusions": 0,
                "mixed_leaks": 0,
                "contract_errors": 0,
                "decidable_correct_minimum": 23,
                "decidable_cases": 25,
                "positive_blocks_correct": 9,
                "unclear_cases_preserved": 3,
            },
            "unexecuted_cases_are_not_failures": True,
            "historical_reserve_used": False,
            "no_prompt_model_variant_chain": True,
            "publication_allowed": False,
            "next_product_step_only_if_passes": (
                "lab_RAG_integration_with_existing_sufficiency_and_publication_gates_closed"
            ),
        },
    )
    paths = [
        ROOT / name
        for name in (
            "src/oralia/course_dialogue/scope_classifier_v2.py",
            "src/oralia/course_dialogue/scope_classifier_v2_prompt.txt",
            "src/oralia/course_dialogue/scope_block_metadata.py",
            "src/oralia/course_dialogue/scope_classifier.py",
            "src/oralia/course_dialogue/context.py",
            "src/oralia/course_dialogue/rag_lab.py",
            "src/oralia/course_dialogue/cached_transformers.py",
            "src/oralia/course_dialogue/gpu_worker.py",
            "src/oralia/course_dialogue/gpu_resource_policy.py",
            "tests/course_dialogue/test_scope_classifier_v2.py",
            "scripts/build_scope_block_metadata.py",
            "scripts/freeze_scope_v2_proposal.py",
        )
    ]
    paths += [
        metadata_path,
        EVIDENCE / "course-scope-policy-v1.json",
        OUTPUT / "bank.json",
        OUTPUT / "oracle.json",
        OUTPUT / "protocol.json",
    ]
    for path in list(paths):
        copy = OUTPUT / "artifacts" / path.relative_to(ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        paths.append(copy)
    save(
        "manifest.json",
        {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    )
    print("Frozen one new proposal: 28 cases, separate oracle, code and metadata; no calls executed.")


if __name__ == "__main__":
    main()
