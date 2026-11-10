# Propuestas, verificación y capacidades — 010

1. Renderer confiable resuelve unidades publicadas y fuentes actuales de la actividad.
2. ProposalPlan referencia (template_id,version,sha256), bindings con procedencia/
destinatario/scope y operaciones admitidas por versión. Transformaciones v1:
select_reviewed_unit, compose_reviewed_units, material_excerpt/v1 y copy_approved_question.
No se admiten substring libre, sinónimos arbitrarios ni texto del proveedor como valor
confiable. Las unidades docentes no se convierten en material vigente por autoclasificación.
3. Grounding y coherencia independientes comprueban contenido y objetivo; la intención
repeat permite coincidencia exacta deliberada, no omite autorización ni controles de fuentes.
4. No revelación considera pregunta/pista/ejemplo/fuentes/summary según política.
5. Snapshot T090 construido desde DB y política publicada; nuevo permiso explícito de
categoría/procedencia solo mediante versión docente. Cada transformación crea propuesta
y veredicto propios. Candidato rechazado = output_text null sin texto en logs/propuestas.
Se conserva el único fallback operativo permitido y se muestra su alcance real.
6. El generador no puede crear templates de su propio candidato ni declarar que este
está aprobado. Hash/similitud léxica/etiqueta de LLM no prueba entailment.

## Perfiles y gates

- extractive_limited: semántica existente, puede presentar fragmentos; no anunciado como explicación adaptativa.
- guided_controlled: selección/composición desde contenido revisado con referentes y
  diálogo completo, apoyo/preguntas. Gate G1 obligatorio.
- generative_local_candidate: solo sandbox sintético sin usuarios hasta contrato
  suficiente de afirmaciones derivadas y gate G2. Tarea de viabilidad termina con
  decisión medida de habilitar o no; ningún modelo ausente cuenta como aprobado.
- degraded: proveedor original no disponible; capabilities_changed y acciones restantes
  visibles; consentimiento no cambia y la sesión no hereda texto nuevo no aprobado.

No se modifica el principio constitucional para hacer pasar una conversación. Si una
explicación deseada no cabe en este contrato, se limita explícitamente hasta diseñar y
validar otra versión; nunca se hace pasar la frase libre por extracto.

