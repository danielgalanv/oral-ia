"""Freeze fresh follow-up/example controls under readable source presentation."""

import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.corpus import load_catalog
from oralia.course_dialogue.rag_lab import RAG_INSTRUCTION

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "specs/012-conversational-course-study/evidence/readable-reference-proposal-v1"


def main():
    OUTPUT.mkdir(exist_ok=False)
    pages = {p["id"]: p for p in load_catalog()}
    cases = [
        {
            "id": "L01",
            "act": "explanation",
            "question": "¿Qué significa que un requisito sea comprobable con tiempo y coste razonables?",
        },
        {
            "id": "L02",
            "act": "followup_reformulation",
            "question": "Sigo sin verlo: explícalo de otra manera, manteniendo ese requisito como referente.",
        },
        {
            "id": "L03",
            "act": "hypothetical_example",
            "question": (
                "Dame un ejemplo hipotético de ese requisito comprobable y explica cómo lo comprobarías. "
                "Indica qué detalles son inventados."
            ),
        },
    ]
    protocol = {
        ("" "hypothesis"): (
            "Readable host attribution removes exact-ID presentation burden; assess follow-up "
            "and example content separately, without claiming semantic improvement from formatting."
        ),
        "cases": cases,
        "references": [pages[key] for key in ("procedure:11", "requirements:76")],
        "criteria": {
            ("" "explanation"): (
                "Address checkability and reasonable cost/time "
                "from the original passage; no unsupported guarantees."
            ),
            ("" "followup"): (
                "Preserve the actually shown referent and meaning while changing "
                "the explanation; mere repetition is not adequate reformulation."
            ),
            ("" "example"): (
                "Explicitly hypothetical with invented details marked; concrete way to check the "
                "requirement, with no unsupported general guarantee or literal attribution to the PDF."
            ),
            ("" "presentation"): (
                "Readable consulted-document attribution by host; "
                "no requirement for unit IDs or citations per phrase."
            ),
            ("" "support"): (
                "Technical clause review against delivered originals, recorded "
                "separately; no automatic semantic evaluator or teacher acceptance inferred."
            ),
        },
        "instruction": RAG_INSTRUCTION,
        "model": "Qwen2.5-7B-Instruct@a09a3545/nf4",
        "diagnostic_requests_maximum": 3,
        "warmup_maximum": 1,
        "generate_invocations_maximum": 4,
        "new_tokens_maximum": 1537,
        "per_request_tokens": 512,
        "per_request_deadline_ms": 30000,
        "load_deadline_seconds": 90,
        "retries": 0,
        "prompt_or_oracle_adaptation": False,
        "stop": "incomplete_generation_protocol_or_source_failure; absent_technical_IDs_not_a_stop",
        "semantic_review": "after_fixed_three_turn_diagnostic; unverified_technical_console_only",
        "history": "only_actually_shown_technical_preview; incomplete_unshown_output_never_added",
        "retrieval": "unchanged_bilingual-v1_one_planned_expansion_not_a_sufficiency_verdict",
        "scope": "new_prepared_controls_bound_to_real_policy; not_semantic_scope_classifier_validation",
        "development_exposed": ["R01-R06", "ST01"],
        "new_controls": ["L01", "L02", "L03"],
        "historical_reserve_used": False,
        "publication_allowed": False,
        "old_ST01_result": "preserved_under_prior_contract_not_reclassified_as_pass",
    }
    path = OUTPUT / "protocol.json"
    path.write_text(json.dumps(protocol, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT / "protocol.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest(), encoding="ascii")
    print("Three new controls and independent criteria frozen before inference; no answer templates")


if __name__ == "__main__":
    main()
