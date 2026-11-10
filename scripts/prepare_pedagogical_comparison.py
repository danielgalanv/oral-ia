"""Freeze three fresh four-turn conversations and one baseline/profile comparison."""

import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.corpus import load_catalog
from oralia.course_dialogue.pedagogical_profile import instruction_for_profile
from oralia.course_dialogue.rag_lab import RAG_INSTRUCTION

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "specs/012-conversational-course-study/evidence/pedagogical-comparison-proposal-v1"


def main():
    OUTPUT.mkdir(exist_ok=False)
    pages = {page["id"]: page for page in load_catalog()}
    cases = [
        {
            "id": "A",
            "block": "ingenieria_requisitos",
            "turns": [
                {
                    "act": "explanation",
                    "question": "¿Cómo distingo la trazabilidad de un requisito de su comprensibilidad?",
                    "references": ["procedure:11", "requirements:76"],
                },
                {
                    "act": "reformulation",
                    "question": "No lo capto todavía: explícalo de otra manera, manteniendo esa distinción.",
                    "references": ["procedure:11", "requirements:76"],
                },
                {
                    "act": "example",
                    "question": (
                        "Muéstrame un ejemplo hipotético de esa distinción, indicando tus "
                        "supuestos y qué observarías para comprobarlo."
                    ),
                    "references": ["procedure:11", "requirements:76"],
                },
                {
                    "act": "nuance",
                    "question": (
                        "¿Qué información faltaría para afirmar que modificar ese "
                        "requisito afectaría poco a los demás?"
                    ),
                    "references": ["requirements:76"],
                },
            ],
        },
        {
            "id": "B",
            "block": "verificacion_validacion_pruebas",
            "turns": [
                {
                    "act": "explanation",
                    "question": (
                        "¿En qué se diferencian detectar defectos y comprobar el uso "
                        "esperado al probar software?"
                    ),
                    "references": ["testing:7", "testing:8"],
                },
                {
                    "act": "reformulation",
                    "question": (
                        "Sigo confundido: ¿cómo puede haber dos ideas de prueba exitosa? "
                        "Usa otra explicación."
                    ),
                    "references": ["testing:7", "testing:8"],
                },
                {
                    "act": "example",
                    "question": (
                        "Dame un ejemplo inventado que contraste ambas finalidades, "
                        "indicando qué supones y qué observarías."
                    ),
                    "references": ["testing:7", "testing:8"],
                },
                {
                    "act": "nuance",
                    "question": (
                        "¿Que esas pruebas no detecten defectos demuestra que el programa "
                        "no tiene errores?"
                    ),
                    "references": ["testing:4"],
                },
            ],
        },
        {
            "id": "C",
            "block": "ingenieria_requisitos",
            "turns": [
                {
                    "act": "explanation",
                    "question": (
                        "¿Qué diferencia hay entre revisar la calidad de una "
                        "especificación y validar que responda a las necesidades de "
                        "quienes la usarán?"
                    ),
                    "references": ["procedure:10", "procedure:12", "requirements:72"],
                },
                {
                    "act": "reformulation",
                    "question": (
                        "No lo capto: cambia la forma de explicarlo para que se entienda " "la diferencia."
                    ),
                    "references": ["procedure:10", "procedure:12"],
                },
                {
                    "act": "example",
                    "question": (
                        "Propón un caso hipotético que muestre por qué esas dos revisiones "
                        "no se sustituyen, con sus supuestos y observaciones."
                    ),
                    "references": ["procedure:10", "procedure:12"],
                },
                {
                    "act": "topic_switch",
                    "question": (
                        "Cambiemos de tema: ¿qué pueden y qué no pueden comprobar las "
                        "inspecciones sin ejecutar el sistema?"
                    ),
                    "references": ["testing:11", "testing:15"],
                    "block": "verificacion_validacion_pruebas",
                },
            ],
        },
    ]
    protocol = {
        "hypothesis": (
            "One general pedagogical extension may improve strategy changes "
            "and assumption/observation consistency without changing answers, "
            "retrieval ranking or semantic gates."
        ),
        "profiles": {
            name: instruction_for_profile(RAG_INSTRUCTION, name) for name in ("baseline", "pedagogy-v1")
        },
        "cases": cases,
        "reference_pages": {
            key: pages[key]
            for key in sorted({key for case in cases for turn in case["turns"] for key in turn["references"]})
        },
        "order": [
            ["A", "baseline"],
            ["A", "pedagogy-v1"],
            ["B", "pedagogy-v1"],
            ["B", "baseline"],
            ["C", "baseline"],
            ["C", "pedagogy-v1"],
        ],
        "fresh_history_per_conversation": True,
        "same_model_worker_for_all_conditions": True,
        "academic_requests_maximum": 24,
        "warmups_maximum": 1,
        "model_generate_maximum": 25,
        "new_tokens_maximum": 12289,
        "per_request_tokens": 512,
        "per_request_deadline_ms": 30000,
        "load_deadline_seconds": 90,
        "total_wall_deadline_seconds": 1020,
        "estimated_minutes": [5, 10],
        "retries": 0,
        "prompt_changes_after_results": False,
        "continuation": {
            "complete_nonempty_candidate": (
                "Show labelled unverified technical preview and append exactly "
                "that shown text; continue fixed next question even after semantic "
                "error; review full conversation afterwards."
            ),
            "semantic_error": (
                "Preserve first error; no correction, repair, invented answer or "
                "silent history replacement."
            ),
            "incomplete_empty_protocol_or_source_failure": (
                "Stop entire experiment; preserve dispatched and unexecuted IDs; "
                "no followup on unshown output."
            ),
            "resource_or_privacy": (
                "Stop on two free-memory samples below 2048 MiB, telemetry "
                "unavailable, or manual STOP file; terminate only owned worker if "
                "needed."
            ),
        },
        "scope": (
            "Prepared control metadata pinned to real policy, not automatic " "scope classifier validation."
        ),
        "retrieval": (
            "Normal unchanged bilingual-v1 retrieval and one planned bounded "
            "expansion from each actual shown history; no fixed-source "
            "generation control."
        ),
        "criteria": {
            "fidelity": (
                "Every academic assertion/premise must be traceable to actual "
                "delivered original passages; record unsupported/rejected/unknown "
                "separately."
            ),
            "relevance": (
                "Answer the present question/act and actually shown referent "
                "rather than substituting a different lesson."
            ),
            "strategy": (
                "On incomprehension, materially change the explanatory route or "
                "relation; synonyms, repeated definition or a list alone are "
                "insufficient."
            ),
            "example": (
                "Identify invented assumptions; observable condition, checking "
                "method and expected result must be coherent with those "
                "assumptions and the documented principle."
            ),
            "limits": (
                "Do not conclude cost, time, exhaustiveness, impact or guarantees "
                "without premises; acknowledge missing information."
            ),
            "coverage": (
                "Review obligations of each question separately from "
                "reference-page hits; a missing source may explain a limitation, "
                "not prove a model failure."
            ),
            "presentation": (
                "Readable host attribution of consulted documents; exact IDs and "
                "output schema not required."
            ),
        },
        "review": (
            "Technical full-output review, not accredited independent semantic "
            "verification or teacher acceptance."
        ),
        "no_predefined_answers": True,
        "publication_allowed": False,
        "reserve_used": False,
        "prior_development": ["R01-R06", "ST01", "L01-L03"],
    }
    path = OUTPUT / "protocol.json"
    path.write_text(json.dumps(protocol, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT / "protocol.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest(), encoding="ascii")
    (OUTPUT / "baseline-instruction.txt").write_text(RAG_INSTRUCTION, encoding="utf-8")
    print(
        "Frozen 3x4 conversations, two fixed profiles, <=24 academic requests +1 warmup, <=12289 new tokens"
    )


if __name__ == "__main__":
    main()
