"""Public technical reason codes. Never expose arbitrary exception messages."""

MESSAGES = {
    "scope_policy_required": "Falta la política de alcance de la actividad; no se genera una explicación.",
    "scope_outside": (
        "No he encontrado esa cuestión entre los temas de esta actividad: definición, elicitación, "
        "validación y trazabilidad de requisitos y requisitos no funcionales. Si crees que sí encaja, "
        "reformula la pregunta indicando el concepto; si no, consúltalo con tu profesorado."
    ),
    "scope_uncertain": (
        "No he podido relacionar la pregunta con los temas habilitados de esta actividad. "
        "¿Puedes indicar a qué concepto de esta actividad te refieres?"
    ),
    "material_not_covered": (
        "El material de la asignatura que tengo no trata esto. No quiero inventarlo: puedes reformular "
        "la pregunta indicando el concepto o consultarlo con tu profesorado. Esto no significa que el "
        "tema esté fuera de la asignatura."
    ),
    "web_permission_revoked": "Cambió el permiso de Internet; la respuesta externa pendiente no se entrega.",
    "web_scope_uncertain": "No se ha confirmado el alcance o la insuficiencia local; precise la pregunta.",
    "web_no_evidence": "No se ha obtenido información externa utilizable.",
    "web_review_unresolved": "No se ha podido contrastar suficientemente la información de Internet.",
    "web_conflict": (
        "Posible conflicto entre Internet y el material docente; no se incorpora como explicación."
    ),
    "review_unresolved": (
        "No he podido completar una respuesta revisada. "
        "Puedes precisar la pregunta o intentarlo más tarde."
    ),
    "question_too_long": (
        "La pregunta es demasiado larga para buscar en los materiales. "
        "Prueba a dividirla o escribir una pregunta más breve. "
        "La conversación se conserva y no se ha consumido una llamada al modelo."
    ),
    "search_context_too_long": (
        "La pregunta junto con su contexto anterior es demasiado larga para la búsqueda. "
        "Reformula brevemente indicando el concepto al que te refieres, o marca Cambiar de tema "
        "si quieres iniciar una duda independiente. La conversación se conserva "
        "y no se ha consumido una llamada al modelo."
    ),
    "no_passages": (
        "No he encontrado pasajes con los que responder esta consulta. "
        "Puedes reformularla o consultar los documentos. Esto no significa que el tema esté "
        "fuera de la asignatura. La conversación se conserva "
        "y no se ha consumido una llamada al modelo."
    ),
    "budget_exhausted": (
        "Cupo de llamadas agotado. Los reintentos que llegan al proveedor también cuentan; "
        "reabrir no renueva el cupo."
    ),
    "runtime_expired": "El runtime global ha caducado; requiere un nuevo arranque explícito.",
    "model_unavailable": (
        "El modelo está detenido o no disponible. Use Recargar modelo local si queda cupo y tiempo; "
        "no se reenvía la pregunta automáticamente."
    ),
    "source_changed": (
        "Las fuentes cambiaron o se retiraron; inspección cerrada para evitar usar evidencia obsoleta."
    ),
    "context_invalid": (
        "El contexto o la petición no cumple el contrato técnico; "
        "no se ha evaluado la calidad de la pregunta."
    ),
    "retrieval_error": "No se pudieron recuperar los pasajes; no es un error académico de la pregunta.",
    "transport_error": (
        "Falló el transporte con el worker del modelo; no hay una respuesta completa confirmada."
    ),
    "generation_timeout": (
        "La generación alcanzó su plazo. El worker puede haberse detenido; "
        "compruebe su estado antes de recargar."
    ),
    "provider_error": "El proveedor devolvió un error técnico de generación.",
    "permission_expired": "Inspección cerrada o permiso docente caducado.",
    "lease_expired": "La inspección caducó por pérdida de su conexión activa.",
    "invalidated_unknown": (
        "Petición invalidada por una causa técnica no identificada. "
        "No permite concluir que la pregunta o el contenido académico sean incorrectos."
    ),
}


class StudyFailure(ValueError):
    def __init__(self, code, message=None):
        if code not in MESSAGES:
            raise ValueError("Unknown public study failure code")
        self.code = code
        super().__init__(message or MESSAGES[code])

    def detail(self):
        return {"code": self.code, "message": MESSAGES[self.code]}
