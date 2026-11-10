# Feature Specification:012 — Autoestudio conversacional de Ingeniería del Software

Created:2026-10-22. Status:especificación aclarada; implementación autorizada, sin commits. Sucesora de011: no modifica su aceptación extractiva ni sus evidencias.

## User Scenarios & Testing

### User Story1 — Explicación y transferencia (P1)

El participante pregunta con saludo, recibe explicación qué/porqué/cómo pertinente y un ejemplo derivado después de la explicación. Al no entender recibe otra estrategia, conserva el referente y una pregunta concreta para comprobar comprensión. Errores/rectificaciones se tratan sin nota ni inferencia académica.

Independent test: conversación real sobre la asignatura, seguimiento condicionado a la salida realmente emitida, dudas repetidas, error y cambio de foco. Oráculo de pertinencia/contenido/contexto/estado separado de grounding/autorización; puede fallar aunque estos aprueben.

Acceptance: distinguir validación de calidad/pruebas; responder a conflicto de requisitos sin limitarse al objetivo general; no sustituir explicación por cita de otro asunto; decir límite cuando no haya respaldo.

### User Story2 — Fuentes y límites visibles sin pantalla (P1)

Participante escucha/lee controles, orientación y fuentes en lenguaje comprensible, sin cascada de menús. Diferencia cita, paráfrasis y ejemplo hipotético. No se atribuye contenido derivado literalmente a una diapositiva.

Independent test: fuentes originales por página/versiones, preguntas ambiguas con aclaración concreta, instrucción maliciosa en material o entrada, controles y cierre/retención existentes.

### User Story3 — Capacidad local revisable (P1)

Usuario dispone de entorno propio, comando e informe de primeras respuestas completas. Si un recurso o gate impide publicar un tutor se informa de la causa observada; una candidata de laboratorio no se anuncia como salida aprobada al participante.

Independent test: original011/entornos/procesos intactos; candidato local real sin descargas, metadatos del proveedor, intentos congelados y primeros fallos; sin bandera de revisión humana inferida.

## Requirements

- **FR-001**: Explicar qué/porqué/cómo según duda concreta, con ejemplo pertinente después de explicación y pregunta de comprensión no calificadora cuando corresponda.
- **FR-002**: Mantener referente, objetivo/pregunta pendiente/transición; variar estrategia ante incomprensión y responder a errores/rectificaciones sin evaluar capacidad.
- **FR-003**: Atender saludo compuesto y aclarar ambigüedad concreta; orientación/fuentes/controles comprensibles sin pantalla. Texto solo acredita lógica; voz requiere prueba separada.
- **FR-004**: Fundamentar en PDF docente autorizado, un formato por documento; permitir Requisitos/Procedimiento/Testing según objetivos, con páginas originales, incidentes y versiones; excluir datos personales/evaluación histórica y alumnos.
- **FR-005**: Distinguir citas/paráfrasis/ejemplos didácticos derivados y sus testigos de fuente. No confiar en la salida del generador como evidencia ni atribuir revisión docente a validación técnica.
- **FR-006**: Conservar T090/T150, consentimiento/retención/privacidad, acceso y sesiones. No publicar texto libre mediante ranura confiable inventada ni debilitar verificador para pasar caso.
- **FR-007**: Investigar capacidad finita/determinista frente a transferencia; implementar capacidad generativa local y puertas si se necesita, usando recursos realmente instalados sin descargas ni nube. Generador propone, no autoriza.
- **FR-008**: Publicación generativa requiere G2 explícito: contrato/verificación de afirmaciones, proveedor real, tres ejecuciones por caso y revisión independiente. G3/G4 y gates históricos no se infieren. Fallo de gate conserva perfil no disponible y evidencia de candidata separada.
- **FR-009**: Congelar nuevas conversaciones/oráculos antes de ajustar; preservar primeras divergencias, marcar reserva expuesta, continuar según salidas reales y no simular éxitos.
- **FR-010**: Entorno propio utilizable, aislamiento de recursos/procesos/credenciales, operación única, cierre/cancelación y comando claro; no Reset/commits ni activación de material habitual.
- **FR-011**: Entregar transcriptos completos manejables, tabla tarea→evidencia, archivos, comandos/resultados exactos y límites. Preservar011 y paquetes anteriores, T061/T067 abiertos.
- **FR-012**: Regresiones proporcionadas/global si compartido, Black/Ruff estructural con multiplicidad contra baseline durable, paquetes experimentales nuevos cuando cambia manifiesto, sin hashes falsificados.
- **FR-013**: En el laboratorio, recuperar evidencia desde todas las páginas docentes autorizadas **ya ingeridas**, no solo una página o línea preseleccionada. Conservar unidades completas de párrafo, lista y tabla, posiciones y procedencia original; enlazar continuidad entre páginas solo cuando esté justificada. Permitir varios pasajes complementarios y supuestos explícitos dentro de presupuesto, sin equiparar citas repetidas con verificación semántica ni afirmar cobertura de la asignatura completa.

- **FR-014**: En el perfil conversacional, publicar afirmaciones académicas solo si una comprobación semántica independiente acredita apoyo en fuente docente activa y autorizada, pertinencia y cobertura; rechazo o incertidumbre bloquean la afirmación y producen límite o aclaración. Internet permanece desactivado en el MVP; una fase web requiere enmienda constitucional y permiso docente explícito, con política de fuentes y procedencia.
- **FR-015**: La respuesta conversacional se genera a partir de pregunta, historial realmente mostrado y evidencia recuperada vigente mediante RAG. El modelo puede explicar y parafrasear, pero no aportar hechos académicos de memoria como si fueran recuperados. No sustituir el objetivo por respuestas de contenido predefinidas.
- **FR-016**: Ante evidencia insuficiente o conflictiva, ampliar de forma acotada la búsqueda local en documentos autorizados y comprobar procedencia; si continúa insuficiente, pedir aclaración concreta o indicar el límite. La futura ruta web, solo con política y permiso válidos tras enmienda constitucional, entrará en el mismo flujo de recuperación, no eludirá grounding ni obedecerá instrucciones halladas en fuentes.
- **FR-017**: Clasificar el alcance académico frente a temario o delimitación docente vigente antes de generar: distinguir dentro de alcance con evidencia, dentro de alcance con evidencia insuficiente, fuera de alcance confirmado e incierto. Solo un fuera de alcance confirmado permite decir cortésmente que el tema no forma parte de la asignatura y no necesita estudiarse para ella; no responderlo académicamente ni buscarlo en internet. La falta de pasajes, una cuarentena o un score bajo nunca prueban exclusión. En caso incierto pedir precisión sin afirmar que no necesita estudiarlo.
- **FR-018**: En preguntas mixtas, tratar únicamente la parte dentro de alcance con evidencia y señalar la parte excluida; no confundir prerrequisitos o analogías para explicar un tema con exigencias adicionales de estudio. Saludos, fuentes, controles, aclaraciones y gestión de sesión conservan su ruta operativa.
- **FR-019**: Presentar referencias legibles al documento o título, con página cuando sea útil; no exigir al modelo identificadores técnicos ni citas por frase como formato de conversación. El host puede construir la presentación desde la procedencia exacta. Si solo conoce los documentos entregados al generador, debe llamarlos «Fuentes consultadas», sin afirmar que verifican todo el texto. Conservar internamente unidades, versiones, hashes y trazas para revisar apoyo, pertinencia y cobertura; la atribución general no rebaja FR-014 ni valida ejemplos injustificados. La futura atribución web mediante título/enlace no habilita Internet durante sesiones.
- **FR-020**: Atender al acto pedagógico actual; ante incomprensión cambiar la estrategia explicativa sin añadir hechos académicos ajenos a fuentes. Permitir ejemplos o propuestas coherentes con valores, requisitos y escenarios inventados cuando se presentan inequívocamente como hipotéticos; no exigir respaldo literal para sus datos ficticios ni enumerar cada detalle de modo burocrático. Fundamentar el principio académico y su interpretación; hacer claros los supuestos decisivos, la condición observable y el resultado esperado. Distinguir requisito propuesto, criterio de aceptación y viabilidad demostrada. No concluir coste, tiempo, exhaustividad, impacto o garantías sin premisas suficientes; pedir o proponer el contexto que falte sin invalidar una primera formulación del alumno.

## Key Entities

Estado conversacional explícito, fuente/página vigente, candidata de explicación con afirmaciones y tipo, testigo, veredicto independiente, política/publicación y recibo de prueba. Reutilizar entidades/servicios existentes antes de ampliar.

## Success Criteria

- **SC-001**: Conversaciones reales nuevas (desarrollo y variante congelada) cubren saludo/pregunta, explicación, incomprensión repetida, ejemplo, error/rectificación y cambio de foco con oráculos independientes satisfactorios; no basta HTTP200 ni grounding aprobado.
- **SC-002**: Cero afirmaciones publicadas sin procedencia permitida, cero ejemplos atribuidos literalmente a fuente y cero publicación con gate fallido. Mantener evidencia separada de candidatas rechazadas.
- **SC-003**: Repetición/cierre/cancelación propios, sin cambios en originales/entornos históricos ni procesos ajenos; recursos preparados y parada propia.
- **SC-004**: Informe separa cumplimiento técnico, capacidad efectiva y aceptación/voz humana pendientes; gates fallidos son trabajo pendiente y no éxito didáctico.
- **SC-005**: Pruebas deterministas demuestran unidades sin cortes físicos, procedencia exacta, continuidad justificada, recuperación multi-fuente con vecinos, presupuesto y discrepancias conservadas; una revisión por conjuntos puede registrar varios pasajes/premisas sin otorgar aprobación semántica ni publicación. La utilidad conversacional sigue sometida a SC-001/G2 y revisión humana.

- **SC-006**: Ningún caso negativo congelado de contradicción compatible, premisa ausente, fuente retirada, respuesta parcial o inyección obtiene permiso falso; sin evaluador calibrado no se abre G2.
- **SC-007**: El laboratorio conserva trazas de recuperación inicial y ampliación local acotada, evidencia entregada al generador, respuesta completa y revisión separada de procedencia, apoyo, cobertura y continuidad. Insuficiencia persistente o conflicto no termina en afirmación académica inventada; los controles positivos también miden cobertura y rechazos falsos.
- **SC-008**: Casos positivos y negativos de frontera, recuperación vacía, fuente retirada/cuarentena, pregunta mixta, referente elíptico y controles operativos demuestran que solo una autoridad de alcance explícita habilita el aviso «no necesitas estudiarlo»; los demás casos no amplían temario ni inventan respuesta.

## Edge Cases

Fuente insuficiente, material retirado/ajeno/cambiado, objeto ambiguo, inyección, fallo/timeout/modelo ausente, contexto obsoleto, ejemplo numérico no documentado, pregunta protegida de otro modo, error de alumno, repetición improductiva. Nunca usar el vocabulario agua/cantidades como semántica universal de validación de requisitos.

## Estado vigente y decisiones

- Decisión expresa del usuario (27-10-2026): referencia documental general suficiente para presentación; se elimina la obligación visible de reproducir IDs entre corchetes. ST01 conserva su primer resultado y rechazo bajo el contrato anterior; su desambiguación injustificada sigue siendo un problema de contenido, separado del formato. No se reescriben recibos ni se declara aprobado retrospectivamente.
- Aclaración expresa posterior (27-10-2026): la invención coherente en ejemplos no es un fallo por no estar literalmente en RAG. Un umbral de respuesta hipotético puede ilustrar rendimiento sin convertirse en estándar, recomendación universal o prueba de que se alcanza. La comparación pedagógica inicial ya estaba congelada, pero no ejecutada: se conserva y se adjunta una adenda previa a inferencia con esta aclaración, sin cambiar preguntas, prompts, presupuesto ni resultados anteriores.

- Fuente actual: documentación docente activa y autorizada; internet desactivado por la constitución. Permiso docente para web requiere además enmienda constitucional previa.
- Citas/IDs, hashes y similitud no demuestran apoyo semántico. Generador y verificador deben ser independientes; `unknown` bloquea. Ejemplos ficticios se etiquetan y su principio académico se respalda. La salida de contenido debe ser generada desde RAG documental, no de una respuesta docente predefinida.
- La política de alcance v1 de esta actividad referencia cuatro PDF docentes; alcance aprobado no significa respuestas aprobadas. Los ensayos Qwen/Mistral son diagnósticos incompatibles para ranking y no abren G2/SC001. Reserva intacta, perfil participante cerrado.
- Punto de entrada: [hoja de ruta](evidence/verified-conversation-roadmap.md). Detalle: [plan operativo](evidence/grounded-tutor-action-plan.md). Cronología de aclaraciones íntegra: [spec histórico](evidence/speckit-history-2026-10-25/spec.md).


## Parte 2 autorizada: consulta documental I0/I1, 27-10-2026

Incremento limitado por orden humana posterior al plan consolidado: corpus real local de requisitos y consulta documental de solo lectura en perfil aislado, sin vectores, pesos, inferencias ni participantes. Reutiliza FR-010/011/012/013/019 y SC-003/004/005 solo en su dimensión documental. Originales intactos, extracción por página/sección, derechos y edición trazados, deduplicación por contenido, cuarentena visible y mapa concepto→pasajes. La comprobación técnica no equivale a aceptación docente. No habilita FR-014/015, G2, SC-001, T090 o T150.

Resultado I0/I1 del paso2: consulta documental disponible para prueba docente según [informe](../../docs/audits/2026-10-27-part2-corpus/report.md); revisión técnica parcial del corpus, sin aceptación humana ni habilitación generativa. Se preservan los requisitos históricos y gates.

## Ampliación autorizada del bloque de requisitos, 27-10-2026

La orden humana posterior exige cubrir el bloque efectivo de requisitos desde los PDF docentes, no seleccionar solo páginas para definición/tipos. Esas preguntas son un guion inicial de demostración. Versión nueva preservando v1.1; matriz de todos los subtemas reales y huecos, QA integral de los dos documentos principales y complementos pertinentes, sin incorporar toda la asignatura. Diferenciar extracción fallida, no revisado, administrativo, duplicado y fuera del subconjunto. Fuentes oficiales NASA, Sommerville e INCOSE cuando su adquisición y condiciones lo permitan; acceso bloqueado no se simula como incorporación. La consulta selecciona explícitamente versión, sin cambiar sesiones o catálogo habituales. No indexar, generar, examinar ni abrir participante; T077, T090/T150, G2/SC001 conservan estado. Entrega técnica y aceptación docente separadas.

## Incremento autorizado de recuperación v2.1, 27-10-2026

Solo pregunta docente→pasajes recuperados con documento/página/procedencia/original, en perfil optativo. CPU local offline del encoder/tokenizer existente, representación e índice aislados; comparación congelada de léxico/denso/RRF. No generación, evaluación del alumno ni cambio de gates. [Informe y resultado negativo de promoción](../../docs/audits/2026-10-27-retrieval-increment/report.md). La suficiencia sigue no evaluada; una media mejor no compensa una pérdida por subtema superior al criterio prospectivo. No cerrar T077 global ni consumidores históricos por integrar este perfil.

## Primera conversación generativa autorizada, 27-10-2026

Alcance único E0/E1/E2 del [plan auditado](../../docs/plans/2026-10-27-first-generated-study-increment.md): diagnóstico docente local sobre recuperación real v2, candidata densa experimental, Qwen2.5-14B NF4 existente, hasta ocho preguntas/un calentamiento,768 tokens/60s y20min globales. Separar bruto, inspección diagnóstica unverified y participante cerrado; no falsear suficiencia o PostReview para abrir LaboratoryConversation. Sin notas, examen, voz o nuevas candidatas. [E0 y bloqueo vigente](../../docs/audits/2026-10-27-first-generated-study/report.md): GPU ocupada y contrato de50s rechaza60s; cero inferencias, E1/E2 pendientes. Sin aceptación humana ni cierre de feature/gates.

## Seguimiento CPU autorizado del primer diálogo, 27-10-2026

Orden humana «sigamos con cpu»: conexión ejecutable v2.1 densa experimental → GenerationPort → recibo e inspección docente unverified/not_assessed con historial de texto mostrado y participante cerrado. Autoridad de inspección distinta de publicación; no evaluadores supported simulados ni debilitamiento de LaboratoryConversation. API/UI y consentimiento/retención/acceso/cancelación vigentes conforme al contrato [diagnóstico v2](contracts/generated-study-diagnostic-v2.md). [Informe CPU](../../docs/audits/2026-10-27-generated-study-cpu/report.md). Protocolo sucesor50.000ms exactos; v1 rechazado preservado. Cero inferencias LLM en esta continuación; calidad, E1/E2 reales y aceptación humana pendientes.
