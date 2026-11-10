"""Prepare a small original-source review packet, never generate answers."""

import hashlib
import json
from pathlib import Path

from oralia.course_dialogue.corpus import load_catalog

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "specs/012-conversational-course-study/evidence"
OUTPUT = EVIDENCE / "study-review-preparation-v1"


def build_review(pages):
    by_id = {page["id"]: page for page in pages}
    questions = [
        {
            "id": "ST01",
            "act": "explanation",
            "question": "¿En qué se distingue que un requisito sea comprensible de que no sea ambiguo?",
            "reference_ids": ["procedure:11", "requirements:76"],
            "requires_shown_previous": False,
        },
        {
            "id": "ST02",
            "act": "reformulation",
            "question": "Reformúlalo con otras palabras, manteniendo la diferencia que acabas de explicar.",
            "reference_ids": ["procedure:11", "requirements:76"],
            "requires_shown_previous": True,
        },
        {
            "id": "ST03",
            "act": "hypothetical_example",
            "question": (
                "Propón un ejemplo hipotético breve de esa " "diferencia y señala qué datos has inventado."
            ),
            "reference_ids": ["procedure:11", "requirements:76"],
            "requires_shown_previous": True,
        },
        {
            "id": "ST04",
            "act": "topic_switch",
            "question": "Cambiemos de tema: ¿cómo se complementan la inspección de software y las pruebas?",
            "reference_ids": ["testing:11", "testing:15"],
            "requires_shown_previous": True,
        },
    ]
    references = {
        key: {
            field: by_id[key][field]
            for field in (
                "filename",
                "page",
                "original_sha256",
                "version",
                "text",
                "text_sha256",
                "derivation",
            )
        }
        for key in sorted({key for q in questions for key in q["reference_ids"]})
    }
    criteria = {
        "source_support": (
            "Revisar cada afirmación y sus límites contra pasajes "
            "originales vigentes; cita o coincidencia de página no basta."
        ),
        "relevance": (
            "Responder al acto y necesidad informativa actuales; "
            "desconocido si no puede justificarse la correspondencia."
        ),
        "coverage": (
            "Registrar por separado qué partes de la " "pregunta están atendidas, omitidas o no respaldadas."
        ),
        "explanation": (
            "Explicación directa y comprensible de la " "diferencia pedida, sin sustituirla por una pregunta."
        ),
        "reformulation": (
            "Cambiar la formulación conservando significado, límites y "
            "referente realmente mostrado; no repetir sin adaptación."
        ),
        "example": (
            "Marcar la ficción y los datos inventados; justificar el "
            "principio con fuentes sin presentar el escenario como hecho documental."
        ),
        "topic_switch": (
            "Recuperar las fuentes del tema nuevo y " "responder a él sin arrastrar la pregunta anterior."
        ),
        "unknown_or_failure": (
            "Conservar primer fallo; no reparar ni completar una salida "
            "que no se mostró. Un límite no demuestra dominio pedagógico."
        ),
    }
    return {
        "state": "prepared_not_executed_not_validated",
        "questions": questions,
        "reference_passages": references,
        "criteria": criteria,
        "no_predefined_model_answers": True,
        "independent_semantic_evaluator_available": False,
        "not_an_automatic_evaluation_gate": True,
        "publication_allowed": False,
        "separation": {
            "exposed_development": (
                "cpu-rag-progress-v1/R01-R06; " "diagnóstico R04/R05 no usado como validación nueva"
            ),
            "new_review_material": (
                "ST01-ST04, preparado para revisar; sin " "salidas, mediciones ni ajuste de perfil"
            ),
            "historical_reserve": "sin acceso, uso o modificación",
        },
        "execution_rules": [
            (
                "El siguiente ensayo decisivo sigue siendo la prueba mínima del "
                "modelo ya preparada; este paquete no la sustituye ni amplía sus llamadas."
            ),
            (
                "No ejecutar este paquete ni cargar pesos por haber transcurrido tres horas; "
                "avisar antes y esperar confirmación expresa de GPU y un protocolo posterior específico."
            ),
            "Revalidar política, documentos y decisiones antes/después de esperas y antes de mostrar.",
            (
                "Cada seguimiento depende del texto realmente mostrado; si no hay referente "
                "visible o el turno falla, conservar pendientes y no inventar una conversación."
            ),
            (
                "Separar salida cruda, texto mostrado y revisión; registrar "
                "identidad/procedencia del revisor y sus incógnitas sin inventar un evaluador semántico."
            ),
            (
                "Registrar cobertura documental, pertinencia, cobertura de "
                "la pregunta, contexto, omisiones y tiempos por separado."
            ),
        ],
    }


def main():
    OUTPUT.mkdir(exist_ok=False)
    packet = build_review(load_catalog())
    path = OUTPUT / "review.json"
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUT / "review.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest(), encoding="ascii")
    lines = [
        "# Preparación de revisión de estudio — no ejecutada",
        (
            "Fuentes originales; preguntas y criterios sin "
            "respuestas prefabricadas. No demuestra calidad pedagógica."
        ),
    ]
    for question in packet["questions"]:
        lines.append(
            f"## {question['id']} — {question['act']}\n\n{question['question']}\n\nFuentes: "
            + ", ".join(question["reference_ids"])
        )
    lines.append(
        "## Criterios\n\n" + "\n\n".join(f"- {key}: {text}" for key, text in packet["criteria"].items())
    )
    lines.append("## Condiciones\n\n" + "\n\n".join(packet["execution_rules"]))
    (OUTPUT / "review.md").write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    print("Four review questions frozen with original-source references; no answers or inference")


if __name__ == "__main__":
    main()
