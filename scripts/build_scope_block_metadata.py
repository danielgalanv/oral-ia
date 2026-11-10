"""Build all policy block descriptions from pinned presentation headings and boundaries."""

import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.corpus import SOURCE_ROOT

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "specs/012-conversational-course-study/evidence/course-scope-policy-v1.json"
OUTPUT = ROOT / "specs/012-conversational-course-study/evidence/course-block-descriptions-v1.json"

INCLUDED = [
    (
        "Introducción a la Ingeniería del Software",
        "Fundamentos de la práctica sistemática de construcción de software "
        "y visión general de la disciplina.",
    ),
    (
        "Procesos de Desarrollo de Software",
        "Procesos y actividades de desarrollo de software como objeto principal de la consulta.",
    ),
    (
        "Desarrollo Ágil de Software",
        "Enfoques ágiles del desarrollo de software dentro del contenido previsto de esta actividad.",
    ),
    (
        "Ingeniería de Requisitos",
        "Requisitos del sistema y su tratamiento dentro del desarrollo de software.",
    ),
    (
        "Modelos de Sistema",
        "Representación de sistemas mediante modelos, como parte del estudio de Ingeniería del Software.",
    ),
    (
        "Herramientas de Ingeniería de Software",
        "Herramientas que apoyan las actividades de Ingeniería del Software.",
    ),
    (
        "Diseño, Arquitectura y Patrones de Software",
        "Organización y diseño del software, su arquitectura y sus patrones.",
    ),
    (
        "Implementación de Software",
        "Construcción e implementación del software en el proceso de desarrollo; "
        "no un curso independiente de sintaxis.",
    ),
    (
        "Verificación y Validación",
        "Verificación, validación y pruebas del software como contenido de la actividad.",
    ),
]
EXCLUDED = [
    ("Fiabilidad", "Fiabilidad"),
    ("Seguridad", "seguridad"),
    ("Reutilización de software", "Reutilización de software"),
    ("Ingeniería de sistemas distribuidos", "Ingeniería de sistemas distribuidos"),
    ("Ingeniería de sistemas empotrados", "Ingeniería de sistemas empotrados"),
    ("Estimación de costes", "Estimación de costes"),
    ("Gestión de calidad", "Gestión de calidad"),
    ("Gestión de configuración", "Gestión de configuración"),
    ("Gestión de equipos de desarrollo", "Gestión de equipos de desarrollo"),
    ("Curso independiente de sintaxis de programación", "NO ES UN CURSO DE PROGRAMACIÓN"),
]


def main():
    if OUTPUT.exists():
        raise ValueError("preserve previous version of descriptions")
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    presentation = policy["source_scope"]["presentation"]
    if (
        hashlib.sha256((SOURCE_ROOT / presentation["file"]).read_bytes()).hexdigest()
        != presentation["sha256"]
    ):
        raise ValueError("presentation changed")
    rows = []

    def add(category, index, title, description, page, quote):
        rows.append(
            {
                "id": policy[category][index],
                "category": category,
                "title": title,
                "description": description,
                "provenance": {
                    "policy_pointer": f"/{category}/{index}",
                    "document": presentation["file"],
                    "document_sha256": presentation["sha256"],
                    "page": page,
                    "quote": quote,
                },
            }
        )

    for index, (title, description) in enumerate(INCLUDED):
        add("included_blocks", index, title, description, 8, title)
    for index, (title, quote) in enumerate(EXCLUDED):
        add(
            "excluded_as_standalone_blocks_for_this_activity",
            index,
            title,
            f"Estudio de {title.lower()} como bloque propio excluido por la política de esta actividad. "
            "Las menciones auxiliares para comprender un bloque incluido siguen permitidas.",
            5 if index == 9 else 7,
            quote,
        )
    for index, (title, quote) in enumerate(
        [("Programación de computadores", "Programación de computadores"), ("Inglés", "Inglés")]
    ):
        add(
            "prerequisites_not_extra_study_blocks",
            index,
            title,
            f"{title} figura como prerrequisito recomendado, no como bloque adicional de estudio. "
            "Se permiten aclaraciones necesarias para comprender los bloques incluidos.",
            5,
            quote,
        )
    OUTPUT.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "metadata_version": 1,
                "policy_sha256": hashlib.sha256(POLICY.read_bytes()).hexdigest(),
                "derivation": (
                    "technical_scope_paraphrases_from_teacher_headings_and_approved_policy_not_answer_evidence"
                ),
                "description_review": "technical_not_teacher_acceptance_of_answers",
                "blocks": rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"blocks": len(rows), "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
