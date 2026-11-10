# Auditoría de incorporación del rediseño de chat a ORALIA

Fecha: 24 de octubre de 2026. Alcance autorizado: auditar cómo aplicar los puntos 1–4 de la comparación arquitectónica al sistema existente. La voz queda fuera de este bloque. No se modifica código, configuración, tareas, datos ni aceptación; este archivo es una propuesta para la implementación posterior.

## Resultado ejecutivo

Se puede empezar el experimento comparativo sin rehacer ORALIA. Ya existe una ruta de generación con recuperación e historial, un puerto de inferencia, proveedores locales propios y una CLI de laboratorio. Hay que corregir su contexto, prompts, representación de respuesta y medición antes de compararla con el renderer actual.

No se puede habilitar la generación abierta en el chat de participantes cambiando una bandera. La integración existente con API/T090 está diseñada para seleccionar unidades revisadas y reconstruir sus textos. Necesita un contrato sucesor para candidatas derivadas y su autorización; `reviewed=True`, una plantilla o una cita exacta no pueden dar autoridad al texto nuevo del modelo. Esa dependencia sigue siendo trabajo pendiente de 012, no una autorización concedida por esta auditoría.

## Mapa real de reutilización

| Pieza existente | Uso propuesto | Límite observado |
|---|---|---|
| `course_dialogue/runtime.py:propose` | Base para las variantes documental y pedagógica | Prompt rígido, historial bruto, presupuesto fijo y tratamiento incompleto de finalización |
| `course_dialogue/corpus.py` | Corpus con páginas y versiones; recuperación multilingüe local | 17 páginas elegidas de tres PDF, no toda la asignatura; selección y cobertura requieren evaluación propia |
| `course_dialogue/context.py:plan_context` | Compatibilidad del contexto anterior | Ancla seguimientos en la última consulta académica; no reconstruye por sí mismo una conversación completa |
| `GenerationPort` / `GenerationRequest` | Puerto común de A/B/C, historial y esquema opcional | Ocho mensajes como máximo; diferencias de parámetros efectivos entre proveedores |
| `cached_transformers.py` / `owned_worker.py` | Inferencia local, aislamiento, tiempos y cancelación | Máximo efectivo de 512 tokens de salida en ese adaptador; recursos y capacidad deben medirse |
| `draft_dialogue.py` / `semantic_planner.py` | Variante A de referencia | Contenido cerrado y elección obligatoria de objetivos/relaciones; no usar como núcleo de B/C |
| `contracts.py` / `verification.py` | Contrato candidato e inspección de procedencia | Versión 1 costosa; no acredita semántica ni permite publicación |
| `evaluation.py` | Observaciones auxiliares sobre trazas | Mezcla señales léxicas y etiquetas internas; no sustituye evaluación del texto |
| `rehearse_course_dialogue.py` y runners semánticos | Procedencia, ejecuciones y conservación de primeros fallos | El runner generativo inicial usa etapas y entradas preestablecidas; hace falta un protocolo adaptativo común |
| `ReviewedSemanticRuntime` / `guided_dialogue_service.py` | Revalidación de actividad, estado y fuentes para integración posterior | Contrato de selección de unidades revisadas, no de respuesta generativa libre |
| `final_output_gate.py` / T090 / servicios de privacidad | Autorización y ciclo de vida posterior | Reutilizar sin dar por verificado el contenido nuevo |

Los nombres anteriores son rutas bajo `src/oralia`, salvo el runner bajo `scripts`. Los enlaces precisos aparecen en los hallazgos.

## Hallazgos y cambios necesarios

### H1 — Prioridad alta: reutilizar el runtime no equivale a tener una base neutral

En [runtime.py](../../src/oralia/course_dialogue/runtime.py:14), el prompt estructurado pide explicar qué, por qué y cómo; la rama libre exige tres frases, 60 palabras y una pregunta final. Eso impone una estructura antes de escuchar qué necesita el alumno. La rama libre no constituye una comparación neutral con el tutor actual.

Cambiar de forma optativa/versionada:

- Base documental: contestar la petición concreta con evidencia e historial, sin ejercicio o pregunta de cierre obligatorios.
- Base pedagógica: mismo contexto y recuperación, con adaptación a la petición, incomprensión, ejemplo o error; una pregunta de comprensión solo cuando ayude.
- Conservar la entrada literal y las instrucciones separadas; no usar la clasificación de siete objetivos/tres relaciones como requisito para generar.
- No añadir inicialmente una llamada de planificación previa a B/C. La propuesta de estado del modelo no determina permisos ni hechos sobre el estudiante.

Mantener la versión anterior reproducible como baseline. Un parámetro explícito de variante permite realizar el ensayo sin cambiar defaults de participantes.

### H2 — Prioridad alta: separar historial mostrado, candidata y diagnóstico

En [runtime.py:45](../../src/oralia/course_dialogue/runtime.py:45) se reenvía `raw_candidate` como mensaje assistant. La CLI estructurada muestra `Candidate.render_for_inspection()`, que no es ese JSON completo. Las salidas inválidas o incompletas también pueden entrar en `history` del siguiente turno. Son hechos del laboratorio, pero no deben confundirse con una explicación publicada o con su contenido visible exacto.

Introducir un registro de turno de laboratorio con campos distintos:

| Campo propuesto | Autoridad y significado |
|---|---|
| `input_text`, `turn_id` | Entrada real e identidad asignada por el programa |
| `raw_outcome`, `finish_reason`, `provider_parameters` | Diagnóstico; nunca evidencia docente ni mensaje aprobado |
| `displayed_text`, `display_kind` | Texto exacto que mostró la interfaz; candidato de inspección, recuperación o salida autorizada según el entorno |
| `candidate`, `candidate_hash` | Propuesta parseada y huella calculada por el programa |
| `source_refs`, `verification_results` | Referencias revalidadas y resultados separados |
| `state_before`, `proposed_state`, `committed_state` | Separar propuesta, contexto observado del laboratorio y estado autorizado de sesión |

El historial conversacional usa lo efectivamente mostrado con su estado explícito. Un error técnico o salida rechazada puede producir un mensaje de recuperación registrado; no debe reemplazarse por el texto que el modelo quiso emitir. En producción solo entran como enseñanza los turnos autorizados. No se fabrica un éxito de conversación a partir del raw de una candidata fallida.

La ventana actual es de cuatro filas/ocho mensajes, con recortes por caracteres. Definir presupuesto por tokens y estrategia de retención antes de ampliarla: conservar pregunta pendiente realmente mostrada, rectificación vigente y referentes necesarios. Cualquier resumen es contexto falible de conversación, no fuente documental ni perfil académico.

### H3 — Prioridad alta: recuperación contextual insuficientemente conectada

[runtime.py:35](../../src/oralia/course_dialogue/runtime.py:35) llama a `select_pages` sin historial. [SemanticCatalog.select](../../src/oralia/course_dialogue/corpus.py:74) admite el argumento pero no lo usa. Pasarlo sin más no arreglaría la recuperación. [plan_context](../../src/oralia/course_dialogue/context.py:18) conserva la consulta anterior para ciertos actos de apoyo; eso ayuda en un seguimiento simple, pero no incorpora lo que acaba de decir el asistente ni resuelve todas las referencias.

Preparar una consulta contextual observable con entrada literal, referente reciente y pregunta pendiente, distinguiendo qué es evidencia de conversación y qué es fuente del curso. Probar «eso», «no, me refería a…», cambio explícito de tema y dudas nuevas mientras hay una pregunta pendiente. No copiar todo el historial al buscador ni anclar siempre el objetivo anterior.

Reutilizar inicialmente el corpus actual e índice local para controlar variables. Medir si recupera las páginas necesarias y si introduce ruido antes de añadir reranking o ampliar corpus. Registrar todos los fragmentos y puntuaciones efectivos. Los umbrales actuales no son garantía de pertinencia. Las páginas no extraídas no pueden contarse como evidencia disponible de la asignatura.

### H4 — Prioridad alta: finalización y presupuestos pueden falsear la comparación

En [cached_transformers.py](../../src/oralia/course_dialogue/cached_transformers.py), `length` produce `ok=True`; en [runtime.py:103](../../src/oralia/course_dialogue/runtime.py:103) solo `not outcome.ok` marca generación incompleta. Una respuesta parseable con `finish_reason=length` puede quedar sin señal de posible truncamiento. Una salida JSON válida no prueba cobertura de la pregunta. La publicación del banco permanece denegada.

Definir en el nuevo contrato el tratamiento de `stop`, `length`, `deadline`, error y cancelación. Un límite de longitud debe quedar observado como tal, separado de éxito estructural y éxito conversacional. No contar automáticamente esa fila como respuesta completa; su posible suficiencia debe juzgarse explícitamente. No añadir reintentos silenciosos ni avanzar estado docente con una salida fallida.

El runtime pide 256 tokens, el worker CUDA limita a 512 y Ollama toma timeout/max_tokens de configuración en vez de aplicar directamente todos los límites del request. Un JSON de hasta ocho segmentos, citas y contexto compite con el texto docente por ese espacio. Hay riesgo de confundir fallo de serialización/presupuesto con incapacidad conceptual del modelo.

Para la comparación: mismo proveedor/modelo cargado, registrar presupuesto pedido y efectivo, tokens de entrada/salida y tiempos. Evaluar un contrato compacto antes de aumentar presupuestos. Si se cambia el contrato entre B y C, medir ese factor aparte; de lo contrario no se puede atribuir la diferencia solo a pedagogía.

### H5 — Prioridad alta: separar el contenido candidato de la certificación que se le exige

El [contrato actual](../../src/oralia/course_dialogue/contracts.py:12) obliga a cada segmento a tener un `source_id` y `source_quote`, incluso preguntas de comprensión. Una sola cita por segmento puede ser insuficiente para una explicación compuesta y copiarla consume tokens. La salida incluye un contexto propuesto por el modelo, que no es estado aprobado.

Diseñar `CandidateV2` para laboratorio sin romper V1. Propuesta mínima: bloques de respuesta con tipo y referencias a evidencia suministrada; supuestos explícitos en ejemplos; pregunta opcional; estado propuesto separado. Permitir más de una referencia por bloque. Los saludos y mensajes operativos se distinguen de las afirmaciones sobre la asignatura. Las afirmaciones y sus testigos pueden descomponerse en una fase de evaluación, sin exigir un supuesto certificado semántico autorredactado por el generador.

Usar IDs de fragmento suministrados y resolver página, versión, hash y cita en el programa cuando sea posible. Una referencia correcta o un offset correcto no prueba que la afirmación se deduzca de ella. Los testigos propuestos por el modelo siguen siendo propuestas, no verificación independiente.

### H6 — Prioridad alta: los oráculos actuales no sirven como puntuación común de A/B/C

[observe_controlled](../../src/oralia/course_dialogue/evaluation.py:14) combina grupos de palabras y expectativas de objetivo/par. [inspect_pedagogy](../../src/oralia/course_dialogue/evaluation.py:94) exige ciertas formas para etapas concretas. Son observaciones útiles, con límites honestamente declarados, pero una respuesta B/C no tiene por qué producir los mismos IDs o usar las mismas palabras.

Crear una rúbrica común sobre texto e historial: corrección de contenido, pertinencia, cobertura, continuidad, feedback y recuperación. Separar observaciones estructurales, evaluación semántica automática y revisión humana. Registrar desacuerdos y casos desconocidos; impedir que rechazar todo parezca un verificador satisfactorio por no aprobar errores. Medir también rechazos de respuestas buenas y conversaciones útiles completas.

El runner generativo inicial toma `scenario[stage]` en cinco etapas fijas. Conservarlo como regresión; construir un runner nuevo con decisiones de continuación congeladas antes del ensayo, ramas según salida efectiva y registro de la rama elegida. Una persona puede conducir conversaciones nuevas de laboratorio; un simulador automático debe identificarse como tal, versionarse y no recibir respuestas esperadas. El evaluador tampoco puede modificar respuestas o pasos para simular éxito.

### H7 — Dependencia de integración: la API actual autoriza unidades, no prosa generada

[ReviewedSemanticRuntime](../../src/oralia/application/services/reviewed_semantic_runtime.py:31) devuelve una selección de unidades actuales; [guided_dialogue_service](../../src/oralia/application/services/guided_dialogue_service.py:384) revalida actividad/estado y usa el renderer/política correspondiente antes de persistir el resultado. El catálogo semántico usa plantillas con contenido revisado. Son controles reutilizables, pero su prueba de seguridad no cubre automáticamente otra clase de contenido.

No introducir B/C devolviendo texto desde `semantic_runtime`, creando unidades docentes revisadas a partir de salidas, o introduciendo el texto en una ranura que confíe en él. Primero decidir, en contrato versionado, la representación de una derivación, quién la comprueba, a qué huella y versión de fuentes/estado se vincula el veredicto y cómo se reconstruye la salida final sin sustituciones.

Reutilizar revalidación, autorización, persistencia, privacidad y conflictos de versión; probar retirada de material, cambio de actividad o estado durante inferencia y alteración del texto después de verificar. G2 y T090 permanecen obligatorios. No cambiar el runtime controlado de participantes mientras se compara la capacidad de B/C.

## Comprobaciones realizadas en esta auditoría

Se ejecutaron 21 pruebas existentes, sin proveedor real ni arranque de servicios:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/course_dialogue/test_runtime.py tests/course_dialogue/test_context.py tests/course_dialogue/test_contracts.py tests/course_dialogue/test_structured_generation.py tests/course_dialogue/test_controlled_observations.py -q -p no:cacheprovider
```

Resultado: **21 passed**, una advertencia de deprecación de Starlette/httpx. No se acredita regresión global ni calidad semántica con este resultado.

Además, una sonda en memoria con catálogo sintético y proveedor ficticio invocó el `propose` actual. Observó:

```json
{
  "synthetic_no_model": true,
  "retrieval_history_rows": 0,
  "history_uses_raw_json": true,
  "history_uses_displayed_text": false,
  "finish_reason": "length",
  "row_error": null,
  "parsed": true,
  "source_checks": true,
  "publication_allowed": false,
  "max_tokens": 256
}
```

La sonda confirma comportamiento de cableado, no que el modelo produzca esa salida ni que toda respuesta marcada `length` sea incompleta. El transcript del comando está en esta conversación. No se modificaron tests para obtener el resultado.

## Secuencia de implementación propuesta a SpecKit

| Bloque | Trabajo y archivos | Evidencia de salida |
|---|---|---|
| 0. Replanificación | Actualizar spec/plan/contratos/tasks de 012: chat como alcance de este bloque; variantes, rúbrica, corpus, presupuestos, reserva y stop conditions. Conservar tareas y fallos previos. | Analyze de consistencia; ninguna tarea antigua cerrada por sustitución |
| 1. Datos de conversación y terminación | Versionar contexto/registro en `course_dialogue`; adaptar `runtime.py` y CLI de laboratorio; no tocar API participante. | Tests de historial visible, raw separado, rechazo, length/deadline, rectificación y pregunta pendiente |
| 2. Recuperación y B/C | Conectar consulta contextual; misma recuperación y contrato compacto para B/C; variantes explícitas sin selección obligatoria de relaciones. | Tests de peticiones reales al puerto, corpus aislado y recuperación; protocolo congelado antes de inferencia |
| 3. Comparación y revisión | Runner y rúbrica comunes; reutilizar freeze, proveedor propio y trazas; A como baseline sin reescribir. | Transcriptos completos, resultados por dimensión, intentos iniciales y reserva; decisión de capacidad sustentada |
| 4. Decisión de integración | Solo para una candidata que demuestre mejora: contrato de derivación/autorización y adaptador a servicios existentes. | G2 y pruebas negativas; si falta verificador adecuado, integración pendiente explícita |
| 5. Chat participante | Actividad aislada con política y perfil explícitos; reutilizar API y web si su DTO basta. | Recorrido real de chat, privacidad, cierres, fuentes y recuperación; pruebas API y navegador |

No se prevé migración de base de datos para los bloques de laboratorio 0–3: sus tipos y memoria pueden ser locales al banco. La integración podría requerir migración y extensión de DTO/trazas según el contrato definitivo; debe decidirse con ese diseño, no prometerse que no hará falta. No crear otra aplicación de chat antes de demostrar el backend; comprobar después si la web actual puede representar perfil, fuentes y recuperación.

Las tareas T008–T012 y T018–T023 siguen representando obligaciones de producto; T025–T027 son una hipótesis experimental, no un requisito de acertar esa arquitectura concreta. Proponer tareas nuevas enlazadas y conservar el estado histórico. No encadenar todo el experimento a disponer primero de un evaluador semántico perfecto: se pueden comparar candidatas bloqueadas y revisar resultados sin habilitarlas.

## Pruebas necesarias por bloque

- Contexto: historial exacto de salida mostrada, errores sin enseñanza inventada, pendientes reales, rectificaciones y separación entre estado propuesto y autorizado.
- Generación: misma pregunta con qué/por qué/cómo, ejemplo solicitado o no, respuesta a error concreto, saludos compuestos, sin pregunta final obligatoria ni plantilla general fija.
- Recuperación: páginas esperadas disponibles, referencias cruzadas, cambio de foco, falta de evidencia e inyección en material/historial; identificar qué comprueba código y qué requiere evaluación de contenido.
- Evaluación: respuestas válidas con formulaciones distintas, texto verdadero impertinente, respuesta pertinente sin apoyo, respuesta parcial y rechazo sistemático; las etiquetas del planificador no son el oráculo común.
- Procedencia experimental: modelo/configuración/runner congelados antes, presupuesto efectivo, fallos conservados, reserva no consultada para ajuste y diferencias de información entre A/B/C declaradas. A dispone de contenido authored: comparar pipelines completos no aísla automáticamente el efecto de arquitectura; B/C deben compartir evidencia y diferir solo en la intervención que se estudia.
- Integración posterior: T090 sobre la salida final exacta, fuentes vigentes, estado concurrente, rollback, consentimiento, retención, purga, cierre y ausencia de fallback de perfil silencioso.

Las pruebas sintéticas de contrato prueban transporte y controles, no pedagogía. Regresión global y Playwright cuando se toque código compartido o el recorrido público; no repetir todo por un cambio documental. Revisar Black y Ruff con multiplicidad en el alcance modificado. No tocar voz ni reconstruir históricos.

## Decisiones que quedan concretadas

Se recomienda **reutilizar y corregir el laboratorio generativo existente**, preservar A como comparación y mantener el chat público sin cambios durante los bloques 0–3. La primera decisión útil es si B/C responden mejor con recursos locales, no cuántas unidades nuevas podemos redactar.

Esta auditoría no selecciona un ganador, no valida modelos nuevos, no cambia SC001, no concede revisión docente ni resuelve T061/T067 históricas. No se han reejecutado ni certificado los hashes de todos los paquetes o datos habituales. Los archivos fueron leídos en un workspace compartido; el informe describe las versiones observadas, no una instantánea atómica de toda la implementación.
