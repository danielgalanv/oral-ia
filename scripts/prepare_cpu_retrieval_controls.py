"""Freeze six new retrieval controls from original authorized pages, no model."""

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from oralia.course_dialogue.document_evidence import load_authorized_units

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "specs/012-conversational-course-study/evidence/cpu-rag-progress-v1"


def main():
    OUTPUT.mkdir(exist_ok=False)
    pages, units = load_authorized_units()
    cases = [
        {
            "id": "R01",
            "question": (
                "¿Cómo compruebo que un requisito es realizable "
                "con la tecnología y el presupuesto disponibles?"
            ),
            "references": ["procedure:11", "requirements:73"],
        },
        {
            "id": "R02",
            "question": (
                "¿Cómo distingo comprobar la especificación de validar "
                "las necesidades reales de clientes y usuarios?"
            ),
            "references": ["procedure:12", "testing:9"],
        },
        {
            "id": "R03",
            "question": (
                "¿Por qué aparecen requisitos incompatibles entre interesados "
                "y cambios durante el análisis?"
            ),
            "references": ["requirements:53"],
        },
        {
            "id": "R04",
            "question": (
                "¿Qué limita las inspecciones estáticas frente a ejecutar pruebas "
                "y observar el comportamiento?"
            ),
            "references": ["testing:11", "testing:15"],
        },
        {
            "id": "R05",
            "question": "¿Por qué?",
            "references": ["procedure:11", "requirements:73"],
            "history_from": "R01",
        },
        {
            "id": "R06",
            "question": (
                "Cambiemos de tema: ¿qué significa éxito en pruebas de validación "
                "y en pruebas de defectos?"
            ),
            "references": ["testing:7", "testing:8"],
            "history_from": "R01",
            "explicit_focus_change": True,
        },
    ]
    by_id = {p["id"]: p for p in pages}
    for case in cases:
        case["reference_passages"] = [
            {
                "page_id": key,
                "file": by_id[key]["filename"],
                "page": by_id[key]["page"],
                "original_sha256": by_id[key]["original_sha256"],
                "text": by_id[key]["text"],
                "text_sha256": by_id[key]["text_sha256"],
            }
            for key in case["references"]
        ]
    packet = {
        "cases": cases,
        "pages": pages,
        "units": [asdict(u) for u in units],
        "history_is_explicit_retrieval_fixture_not_generated_conversation": True,
        "reference_page_hit_is_not_semantic_support": True,
        "publication_allowed": False,
        "no_models_or_inference": True,
        "control_count": 6,
    }
    path = OUTPUT / "controls.json"
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT / "controls.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest(), encoding="ascii")
    print("Frozen six controls and original reference passages before retrieval evaluation")


if __name__ == "__main__":
    main()
