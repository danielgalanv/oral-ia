# ORALIA: contraste arquitectónico y del proceso de desarrollo

Fecha: 24 de octubre de 2026. Revisión independiente, documental y de código; no se ha ejecutado un nuevo ensayo de capacidad ni modificado producción, configuración, tareas o aceptación.

## Dictamen

La base de contratos, estado explícito, fuentes autorizadas, privacidad y autorización independiente es defendible. El principal desajuste observado está entre la flexibilidad conversacional requerida y el mecanismo actual que selecciona y concatena unidades cerradas. Se ha desarrollado mucha infraestructura antes de demostrar el recorrido educativo central con material real. Más selectores o verificadores no compensan automáticamente ese desajuste.

Esto no demuestra que una arquitectura sencilla funcione mejor: falta una comparación controlada con el mismo modelo, materiales, restricciones y conversaciones. Tampoco demuestra que el despliegue local sea inviable. Las fuentes públicas no permiten reconstruir toda la infraestructura interna de los servicios comerciales.

## Comparadores y qué permiten concluir

| Referencia primaria | Diseño o evaluación documentados | Implicación para ORALIA |
|---|---|---|
| [LearnLM-Tutor, informe técnico, versión 4](https://arxiv.org/html/2407.12687v4), especialmente apéndice E y secciones 3–6 | El tutor recibe instrucciones pedagógicas, material y conversación previa; el envoltorio conserva contexto relevante. Combina evaluación humana por turno y conversación con evaluaciones automáticas. Describe límites de prompting y adaptación del modelo. | La conversación real y su evaluación deben ser capacidades centrales. Un plan con referencias válidas no sustituye la calidad de la respuesta. No se puede extrapolar su rendimiento a nuestros modelos locales. |
| [Khanmigo, aprendizajes de desarrollo de Khan Academy](https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/) | Evalúa latencia, transferencia al siguiente problema y participación cognitiva; usa verificaciones matemáticas especializadas y mide cuándo conviene invocarlas. | Conservar verificadores concretos útiles, pero medir su contribución y coste. Los tests de integración no acreditan aprendizaje. Sus perfiles históricos del alumno no son un requisito que debamos copiar. |
| [AutoTutor, investigación de sus autores](https://pmc.ncbi.nlm.nih.gov/articles/PMC3748232/) | Usa guiones con respuestas esperadas, errores previsibles, pistas, preguntas y feedback adaptado a la intervención. | El contenido preparado no es por sí mismo un error. Su valor depende de reconocer lo que el alumno expresa y elegir feedback pertinente; no basta cambiar el bloque mostrado. |
| [Dify, documentación oficial de recuperación](https://docs.dify.ai/en/cloud/use-dify/nodes/knowledge-retrieval) | Documenta una base sencilla: pregunta, recuperación de fragmentos, generación con ese contexto y respuesta. | Sirve como comparación mínima para medir qué aporta la orquestación adicional. No constituye por sí solo un tutor ni garantiza veracidad. |
| [NotebookLM/Gemini Notebook, ayuda oficial](https://support.google.com/notebooklm/answer/16179559?hl=en) | Documenta preguntas sobre fuentes elegidas y citas inspeccionables. | La consulta documental permite contrastar la experiencia básica de pregunta y fuente. Esta documentación de producto no prueba un mecanismo interno de verificación semántica independiente. |
| [Tutor CoPilot, artículo de sus autores](https://arxiv.org/html/2410.03017v3) | La IA asiste a un tutor humano durante la interacción; el estudio evalúa ese sistema humano–IA. | Sus resultados no validan un tutor autónomo. Revisar antes un catálogo tampoco equivale a tener supervisión humana en cada turno. |
| [Ragas: faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) y [response relevancy](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/answer_relevance/) | Separa apoyo de las afirmaciones en el contexto de pertinencia de la respuesta a la pregunta. Sus métricas basadas en modelos son evaluaciones falibles. | Necesitamos medir ambas dimensiones, además de cobertura y continuidad. Una puntuación automática no se convierte por sí sola en permiso de publicación. |
| [Anthropic, patrones de agentes](https://www.anthropic.com/research/building-effective-agents) | Recomienda empezar por la solución más sencilla y añadir complejidad con beneficio medido; el patrón evaluador–optimizador requiere criterios claros y un evaluador que produzca feedback útil. | No añadir otra etapa simplemente porque la anterior falla. La modularidad de ORALIA puede conservarse sin multiplicar las llamadas al modelo. |
| [Pipecat, recuperación de turnos de voz vacíos](https://reference-server.pipecat.ai/en/latest/api/pipecat.turns.empty_user_turn.html) | Distingue ruido mientras espera del caso en que una intervención sin transcripción interrumpe al asistente; contempla recuperación y contexto de lo realmente oído. | La voz requiere gestión de turnos e interrupciones, además de STT/TTS. Es una referencia de diseño, no una indicación de instalar este framework. |

## Hallazgos sobre nuestra implementación

### 1. Desajuste entre conversación abierta y composición cerrada — prioridad alta

Evidencia: [spec de 012](../../specs/012-conversational-course-study/spec.md), FR-001/002 y SC-001; [renderer experimental](../../src/oralia/course_dialogue/draft_dialogue.py), líneas 181–208 y método `_render_relation`.

En el prototipo de 012, `explain` selecciona definición, causa y proceso del objetivo y concatena sus textos. `respond` recupera el feedback asociado a la pregunta, de rol comparación/corrección; no redacta una respuesta nueva condicionada a la afirmación concreta del alumno. En las relaciones, numerosos actos comparten definición, ejemplo y pregunta. La entrada sirve para interpretación y comprobaciones de vinculación; no determina libremente el contenido final.

Consecuencia: acertar objetivo y acto puede seguir produciendo una contestación demasiado general, repetitiva o ajena al matiz qué/por qué/cómo. Es una limitación verificable del mecanismo, no solo un problema del último prompt. Este código es un preview bloqueado, no el tutor público.

Propuesta: mantener unidades revisadas como recursos y referencias; comparar su uso con una candidata de respuesta adaptada al turno y al historial. Si se mantiene una rama de tutor estructurado, debe demostrar adaptación del feedback a errores concretos y un alcance explícito. No reemplazar una rama por otra sin ensayo.

### 2. Las categorías del catálogo se han convertido en un paso obligatorio demasiado delicado — prioridad alta

Evidencia: [contratos de planificación](../../specs/012-conversational-course-study/contracts/semantic-planning.md), variantes v3–v10; [decisión de viabilidad](../../specs/012-conversational-course-study/evidence/semantic-viability-decision.md).

La selección entre siete objetivos y tres relaciones precede a la respuesta. Una clasificación errónea puede imponer otro contenido y otra pregunta. Que realizable/comprobable pertenezcan a un objetivo y ambigüedad a otro es una decisión de autoría; no debería convertirse en la medida única de si una respuesta ayuda. Las salidas observadas sí presentan desvíos sustantivos, pero una etiqueta diferente no basta para declarar un fallo si el texto atiende bien la duda.

Propuesta: evaluar primero el texto efectivo. En el ensayo alternativo, recuperar evidencia con la duda e historial, usando objetivos como ayudas de alcance y trazabilidad. Mantener obligatorios los límites reales de actividad, permisos y fuentes; una categoría pedagógica no tiene por qué actuar como una frontera de autorización.

### 3. Procedencia, verdad, pertinencia y permiso son controles diferentes — prioridad alta

Evidencia: [verificación de candidatas](../../src/oralia/course_dialogue/verification.py), [grounding existente](../../src/oralia/domain/agents/grounding_verifier_agent.py), [T090](../../src/oralia/domain/policies/output_authorization_verifier.py), [ensayo de verificadores](../../specs/012-conversational-course-study/evidence/semantic-independent-verifier-assessment.md).

El inspector de 012 comprueba existencia de una cita y literalidad cuando corresponde; declara honestamente que no verifica semántica y deniega publicación. El grounding histórico incluye comprobaciones léxicas, numéricas y de negación acotadas: no es un verificador general de implicación semántica. T090 verifica autorización estructurada; no certifica que una explicación sea didácticamente adecuada.

Los dos procedimientos recientes obtuvieron 3/6 tomando una decisión constante: admitir todas las relaciones o elegir siempre la respuesta simple. Eso no demuestra discriminación. Un segundo modelo es un componente separado, pero puede conservar sesgos y errores; su separación no prueba fiabilidad.

Propuesta: panel separado de procedencia, respaldo de afirmaciones, contradicción, pertinencia, cobertura, continuidad y autorización. Calibrar evaluadores frente a juicios humanos, incluyendo falsos positivos, falsos negativos y abstención. La verificación por proposiciones es una hipótesis útil para respaldo, no una garantía universal ni la solución automática de la pertinencia. Esta precisión corrige también el énfasis de mi recomendación anterior.

No se propone abrir G2 ni rebajar T090. Si la interpretación actual del requisito exige certidumbre semántica que el mecanismo no puede ofrecer, documentar el conflicto y una propuesta explícita de contrato; nunca alterar su aceptación silenciosamente.

### 4. La validación del producto llegó demasiado tarde — prioridad alta

Evidencia: [validación arquitectónica 006](../../specs/006-architecture-validation/evidence/report.md), [revisión real de 011](../../materiales/docente/asignatura-real-20261021/REVISION-FEATURE011-20261022.md), resultados posteriores de 012.

El informe 006 ya limita sus conclusiones: muestra sintética, modelo determinista, recuperación léxica y ninguna demostración de superioridad arquitectónica. Reproducir sus 204 celdas sigue siendo útil como regresión; no añade evidencia nueva de tutoría con un LLM. Lo mismo sucede con contar pruebas Python o navegador: acreditan lo que comprueban, no que un estudiante entienda una explicación.

El historial muestra un coste real: infraestructura y cierres técnicos precedieron a la detección de problemas centrales al usar la demo y el material de la asignatura. Las revisiones recientes mejoran el proceso, pero hace falta poner el recorrido educativo por delante de más ampliaciones.

Propuesta: tres resultados separados en cada entrega: integridad técnica, calidad de conversaciones nuevas y aceptación/utilidad humana. Probar cambios con conversaciones completas que reaccionen a lo efectivamente contestado; incluir reserva y criterios de abandono. La revisión de contenido puede ser breve y por muestras seleccionadas; no cargar al docente con revisar 83 borradores antes de demostrar que el mecanismo puede usarlos bien.

### 5. Riesgo de confundir ausencia de notas con ausencia de feedback — prioridad media-alta

La [constitución](../../.specify/memory/constitution.md) prohíbe notas, decisiones académicas e inferencias de capacidad. Esa restricción es adecuada para este producto. No impide señalar un error concreto de contenido y explicarlo con evidencia. El mecanismo `respond` del preview no demuestra esa capacidad por el hecho de acusar recibo y mostrar una comparación.

Propuesta: feedback sobre la proposición y la pregunta actual, sin atribuir al alumno creencias que no expresó ni asignarle nivel o dominio. Registrar solo hechos de sesión necesarios: qué se preguntó, qué contestó, qué explicación recibió y qué pidió aclarar. No copiar perfiles longitudinales de otros servicios.

### 6. El objetivo hablado exige decisiones arquitectónicas desde ahora — prioridad alta para la aceptación final

La especificación histórica trató la voz como modalidad opcional; el usuario ha precisado después que el uso final será hablado y sin pantalla. Mantener texto accesible es compatible, pero la prioridad de producto ha cambiado y debe reflejarse explícitamente.

Las variantes de planificación admiten varias llamadas dentro de 30 segundos. Es un presupuesto máximo experimental, no una latencia observada de todos los turnos ni un objetivo satisfactorio de conversación hablada. Las cargas del verificador midieron 42,31 y 23,72 segundos: preparación y turno deben medirse por separado.

Propuesta: medir p50/p95 de respuesta completa y primer audio autorizado; preparar modelos fuera del turno; validar silencios, rectificaciones, interrupciones y la diferencia entre texto generado y texto que el usuario llegó a oír. No emitir audio docente aún no autorizado para mejorar artificialmente la latencia. Validar qué/por qué/cómo y recuperación por voz; las pruebas textuales actuales no lo acreditan.

## Qué conservar

Contratos y adaptadores sustituibles; estado y trazas explícitos; fuentes y versiones; aislamiento de actividades; controles de acceso, consentimiento, retención y purga; autorización independiente; cancelación y descarte de resultados tardíos; evidencias de fallos. Las fuentes revisadas no justifican tirar esa base ni convertir el proyecto en microservicios o añadir más agentes.

La composición cerrada puede seguir sirviendo para controles, operación, citas literales, ejercicios preparados y reserva declarada. No debe presentarse su disponibilidad como prueba de explicación conversacional general.

## Próximo experimento recomendado a SpecKit

No es una nueva aceptación ni una orden de cambiar producción. Mantener la rama actual y diseñar una comparación aislada:

1. **A: mecanismo actual** de selección y renderer.
2. **B: base documental sencilla**, con pregunta, evidencia e historial pertinente, sin selección obligatoria entre relaciones pedagógicas.
3. **C: misma base con estrategia docente explícita**, feedback sobre la intervención y salida estructurada con fuentes/afirmaciones. Añadir solo controles cuya aportación pueda medirse.

Usar el mismo proveedor local, documentos, condiciones de preparación y presupuesto comparable. Registrar diferencias inevitables de prompts, tokens y llamadas. No mezclar una mejora de modelo con una de arquitectura sin identificar el factor. Todo resultado es candidato de laboratorio y conserva denegada la publicación hasta satisfacer el contrato vigente.

Propuesta de matriz, que debe congelarse antes de medir: 12 conversaciones de desarrollo y 12 de reserva, de 8–12 turnos, repartidas entre dudas de requisitos y pruebas. Cubrir saludo compuesto, qué/por qué/cómo, error concreto, repetición, referencia implícita, vínculo solicitado y no solicitado, cambio de foco y falta de evidencia. Hacer tres ejecuciones por caso conforme al criterio actual, sin contar repeticiones como alumnos independientes. Un guion permite varias respuestas y actos válidos; el oráculo examina contenido y continuidad, no solo etiquetas.

Medir conversaciones satisfactorias completas, turnos pertinentes, cobertura, afirmaciones sin apoyo, recuperaciones, rechazos erróneos, latencia y coste de autoría. Revisar a ciegas una muestra manejable con el docente. Los umbrales exactos deben acordarse/documentarse antes; estas cantidades son una propuesta de diseño, no un estándar externo.

Condición de parada: si la base sencilla tampoco mantiene una conversación aceptable con el recurso disponible, investigar proveedor, contexto y capacidad del modelo antes de añadir otra capa de selección. Si B/C mejoran, integrar el camino mínimo con los contratos y controles existentes y ejecutar las regresiones pertinentes. Ningún resultado sintético sustituye la posterior prueba de utilidad con personas o de voz real.

## Límites de esta revisión

Se inspeccionaron archivos y resultados conservados, no se reejecutaron las suites ni se certificaron de nuevo los hashes históricos. La auditoría se centra en autoestudio y en los requisitos compartidos de conversación/voz; no es una nueva auditoría exhaustiva de defensa oral. No se subió material docente, código ni conversaciones a servicios externos: las consultas web usaron nombres de productos y temas técnicos públicos.

Las conclusiones sobre ORALIA son inferencias de diseño apoyadas en el código y experimentos citados. Las prestaciones publicadas de otros sistemas no constituyen un ensayo comparativo de ORALIA ni garantizan que sus métodos funcionen con nuestros recursos locales.
