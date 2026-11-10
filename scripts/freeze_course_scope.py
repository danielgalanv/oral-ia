"""Freeze separate bank/oracle/prompt/code before the one authorized scope trial."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "scope-classifier-frozen-v1"


def save(name, value):
    (OUTPUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    OUTPUT.mkdir(exist_ok=False)
    proposal = (EVIDENCE / "scope-classifier-proposal-2026-10-25.md").read_text(encoding="utf-8")
    table = [line.split("|")[2].strip() for line in proposal.splitlines() if line.startswith("| S")]
    if len(table) != 20:
        raise ValueError("bank differs from proposed twenty cases")
    texts = list(table)
    texts[7] = "¿Entra eso?"
    texts[11] = "Pon otro ejemplo de eso"
    texts[12] = "Entonces explícame eso desde cero"
    texts[13] = "¿Y eso cómo se hace?"
    texts[18] = "Ahora cambia de tema: ¿para qué sirve un diagrama de secuencia?"
    history = {
        11: [
            {
                "input": "¿Qué es una prueba unitaria?",
                "displayed_text": "Explicación de laboratorio sobre pruebas unitarias.",
                "displayed_kind": "laboratory_preview",
            }
        ],
        12: [
            {
                "input": "Quiero estudiar seguridad como bloque independiente",
                "displayed_text": "Ese bloque está excluido como tema autónomo en esta actividad.",
                "displayed_kind": "operational",
            }
        ],
        13: [
            {
                "input": "Quiero comparar arquitectura y requisitos",
                "displayed_text": "Has mencionado arquitectura y requisitos. ¿A cuál te refieres?",
                "displayed_kind": "operational",
            }
        ],
    }
    history[18] = history[11]
    cases = [
        {"id": f"S{i+1:02}", "text": text, "history": history.get(i, [])} for i, text in enumerate(texts)
    ]
    # No invented academic answer is used as source: histories above are synthetic shown fixtures.
    statuses = [
        "in_scope",
        "out_of_scope",
        "in_scope",
        "out_of_scope",
        "in_scope",
        "mixed",
        "mixed",
        "uncertain_scope",
        "uncertain_scope",
        "operational",
        "in_scope",
        "in_scope",
        "out_of_scope",
        "uncertain_scope",
        "in_scope",
        "out_of_scope",
        "in_scope",
        "out_of_scope",
        "in_scope",
        "out_of_scope",
    ]
    included = {
        0: "ingenieria_requisitos",
        2: "verificacion_validacion_pruebas",
        4: "ingenieria_requisitos",
        5: "verificacion_validacion_pruebas",
        6: "ingenieria_requisitos",
        10: "procesos_desarrollo",
        11: "verificacion_validacion_pruebas",
        14: "verificacion_validacion_pruebas",
        16: "verificacion_validacion_pruebas",
        18: "modelos_sistema",
    }
    excluded = {
        1: "gestion_configuracion",
        3: "seguridad",
        5: "sistemas_distribuidos",
        6: "estimacion_costes",
        12: "seguridad",
        15: "tutoria_autonoma_sintaxis_programacion",
        17: "seguridad",
        19: "fiabilidad",
    }
    oracle = {
        case["id"]: {
            "status": statuses[i],
            "included_block": included.get(i),
            "excluded_block": excluded.get(i),
            "referent_turn": 0 if i in {11, 12} else None,
        }
        for i, case in enumerate(cases)
    }
    oracle["S06"].update(
        included_quote="Explícame pruebas unitarias", excluded_quote="dame un curso de sistemas distribuidos"
    )
    oracle["S07"].update(
        included_quote="cómo recoger requisitos de usuarios",
        excluded_quote="Quiero estudiar estimación de costes",
    )
    save("bank.json", cases)
    save("oracle.json", oracle)
    prompt = ROOT / "src/oralia/course_dialogue/scope_classifier_prompt.txt"
    (OUTPUT / "prompt.txt").write_bytes(prompt.read_bytes())
    paths = [
        prompt,
        ROOT / "src/oralia/course_dialogue/scope_classifier.py",
        ROOT / "src/oralia/course_dialogue/gpu_worker.py",
        ROOT / "src/oralia/course_dialogue/cached_transformers.py",
        ROOT / "scripts/trial_course_scope.py",
        Path(__file__),
        ROOT / "tests/course_dialogue/test_scope_classifier.py",
        ROOT / "tests/course_dialogue/test_scope_trial_metrics.py",
        EVIDENCE / "course-scope-policy-v1.json",
        OUTPUT / "bank.json",
        OUTPUT / "oracle.json",
        OUTPUT / "prompt.txt",
    ]
    for path in list(paths):
        if path.suffix == ".py":
            copy = OUTPUT / "code" / path.relative_to(ROOT)
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(path.read_bytes())
            paths.append(copy)
    save(
        "manifest.json",
        {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    )
    save(
        "protocol.json",
        {
            "max_calls": 20,
            "max_tokens": 256,
            "deadline_ms": 30000,
            "new_development_controls_not_reserve": True,
            "oracle_author": "implementation_agent_policy_derived_not_teacher_review",
            "history_kind": "synthetic_shown_fixture_not_real_conversation",
            "stop": "first_false_exclusion_mixed_leak_or_contract_error",
            "publication_allowed": False,
        },
    )
    print("Frozen twenty cases, separate oracle, prompt and implementation hashes.")


if __name__ == "__main__":
    main()
