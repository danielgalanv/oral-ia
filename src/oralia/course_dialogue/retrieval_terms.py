"""Opt-in bilingual lexical vocabulary; no embeddings, answers or verdicts.

Each equivalence class counts once, so bilingual repetitions cannot multiply a
concept's score. Ambiguous vocabulary can retrieve extra passages; every result
still needs separate sufficiency/relevance review.
"""

from oralia.domain.materials.query_excerpt import terms

PROFILE = "bilingual-v1"
VOCABULARY = (
    "requisitos requirements requirement",
    "pruebas prueba testing tests test",
    "presupuesto budget coste cost",
    "tecnologia technology technological",
    "interesados stakeholders stakeholder",
    "conflicto conflicts contradictions contradicciones incompatibles inconsistency",
    "cambios change changing",
    "analisis analysis",
    "especificacion specification",
    "necesidades needs",
    "clientes customer customers client",
    "usuarios user users",
    "estatica static",
    "comportamiento behaviour behavior",
    "ausencia absence",
    "errores errors error",
    "exito successful success",
    "validacion validation validity",
    "verificacion verification",
    "defectos defects defect",
)
ALIASES = {token: f"concept_{index}" for index, group in enumerate(VOCABULARY) for token in terms(group)}


def retrieval_terms(text):
    return {ALIASES.get(token, token) for token in terms(text)}
