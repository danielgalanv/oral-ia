# Research: Agencia de autoestudio

Regenerado tras el cierre de requisitos de `spec.md` (Clarify, dos rondas, 2026-09-01) y
tras una ronda de corrección de consistencia arquitectónica (2026-09-02) sobre: fuente
de verdad del modo activo, número de adaptadores de `GenerationPort`, independencia de
`SolutionNonDisclosureVerifierAgent`, y alcance real de FR-028. Usa exclusivamente los
identificadores canónicos de modo definidos en `spec.md` FR-001/FR-001a:
`doubt_resolution`, `guided_explanation`, `practice_questions`,
`presentation_preparation`, `concept_review`.

## 1. Generación real mediante LLM local, con reserva determinista — dos adaptadores

**Decision**: `GenerationPort` (Protocol) tiene **exactamente dos** implementaciones:
`OllamaGenerationAdapter` (primaria, HTTP local vía `httpx`) y
`DeterministicGenerationAdapter` (reserva, extractiva sobre los fragmentos ya
recuperados). **No existe un tercer adaptador que envuelva a los dos anteriores.** La
lógica "intenta Ollama, si falla usa el determinista" vive directamente dentro de los
agentes que consumen el puerto (`ResponseGeneratorAgent`, `PracticeQuestionAgent`), que
reciben **ambas** implementaciones inyectadas por constructor (mismo patrón de
inyección ya usado por `MaterialRetrieverAgent` con `VectorStore`/`EmbeddingAdapter`,
Feature 002) y llaman primero a la primaria, capturando error/timeout/conexión antes de
llamar a la secundaria:

```text
try:
    outcome = await self._primary.generate(request)   # OllamaGenerationAdapter
except (TimeoutError, ConnectionError, GenerationError):
    outcome = await self._secondary.generate(request)  # DeterministicGenerationAdapter
```

**Rationale**: una tercera clase que solo reenvía a las otras dos (el
`FallbackGenerationAdapter` de la iteración anterior) no aporta una responsabilidad
propia distinguible — es la misma lógica de dos líneas que cualquier agente que la
necesite puede ejecutar directamente sobre sus dos dependencias, igual que
`MaterialRetrieverAgent` ya combina `VectorStore`+`EmbeddingAdapter` sin una clase
envoltorio intermedia. Eliminarla reduce una capa de indirección sin necesidad
demostrada (Principio XI).

**Parámetros concretos** (sin cambios respecto a la iteración anterior):

| Parámetro | Valor por defecto | Configuración |
|---|---|---|
| Timeout de la llamada a Ollama | 6000 ms | `ORALIA_OLLAMA_TIMEOUT_MS` — subordinado al `timeout_ms` del contrato del agente llamante |
| `temperature` | 0.2 | `ORALIA_OLLAMA_TEMPERATURE`, clamped a `[0.0, 1.0]` |
| `max_tokens` | 256 | `ORALIA_OLLAMA_MAX_TOKENS`, clamped a `[64, 512]` |
| Modelo | sin default — MUST configurarse explícitamente | `ORALIA_OLLAMA_MODEL` |
| Host | `http://127.0.0.1:11434` | `ORALIA_OLLAMA_BASE_URL` |

Si `ORALIA_OLLAMA_MODEL` no está configurado al arrancar el proceso, el agente se
construye con `OllamaGenerationAdapter` como primaria pero **nunca la invoca** —
resuelve directamente a `DeterministicGenerationAdapter` (evita gastar tiempo del turno
en una llamada condenada a fallar); esta comprobación vive en el propio agente
(`ResponseGeneratorAgent.__init__`/`PracticeQuestionAgent.__init__`), no en un tercer
adaptador.

**Pruebas**: marcador `pytest` `ollama` para integración real, omitido por defecto; el
resto de la suite inyecta un doble determinista de `GenerationPort` o
`DeterministicGenerationAdapter` directamente.

## 2. Cadena de degradación controlada (FR-008a) — tres niveles, dos mecanismos

**Decision**: la cadena tiene tres niveles pero **dos mecanismos distintos** — no se
inventa un tercero:

1. **Nivel 0 — fase de evidencia** (antes de invocar generación, decisión del
   compositor de agencia, no de `GenerationPort`): si el modo requiere fundamentación y
   `MaterialRetrieverAgent` (Feature 002, sin cambios) devuelve `fragments = []` con
   `general_knowledge_allowed = false`, el compositor omite el paso de generación por
   completo — acción `acknowledge_missing_info` (US2). No se inventa contenido.
2. **Nivel 1 — dentro de `GenerationPort`** (mecanismo nuevo de esta feature, §1):
   Ollama → `DeterministicGenerationAdapter`, gestionado por el propio agente generador.
3. **Nivel 2 — red de seguridad final** (mecanismo **ya existente**, Feature 001, sin
   cambios): si el agente generador completo devuelve `status != "ok"` (una excepción no
   capturada por el nivel 1, o cualquier otro fallo del paso), `execute_agency`
   (`agency_composer.py`, Feature 001) activa su `fallback_step` ya validado →
   `SafeFallbackAgent`/`SAFE_FALLBACK_TEXT` (Feature 001, sin cambios) — el mismo
   mecanismo que ya protege cualquier paso de cualquier agencia, sin un caso especial
   para generación.

**Rationale**: el Nivel 2 es exactamente el mecanismo de degradación genérico que la
Feature 001 ya implementó y probó (`tests/failure/test_agent_timeout.py`,
`test_degradation_constitutional_check.py`) — reutilizarlo tal cual, en vez de
modelarlo como un tercer `GenerationPort`, evita duplicar la semántica de "red de
seguridad final" en dos sitios (Principio XI, instrucción explícita de esta ronda: "no
un tercer generador paralelo, salvo que exista una razón arquitectónica demostrable").
No existe tal razón: el contrato de `execute_agency` ya admite cualquier agente como
`fallback_step`, generador o no.

## 3. Frontera instrucciones/datos frente a prompt injection documental (FR-008b)

Sin cambios respecto a la iteración anterior: `OllamaGenerationAdapter` separa siempre
un mensaje `system` fijo (sin interpolar `evidence[].text`) de un mensaje `user` con la
evidencia delimitada explícitamente. `DeterministicGenerationAdapter` no tiene este
riesgo por construcción.

## 4. Verificador independiente de no-revelación de solución (FR-013a)

**Decision**: `SolutionNonDisclosureVerifierAgent` es un verificador **completamente
independiente** de `GroundingVerifierAgent` (Feature 002) — contrato propio, umbral
propio, veredicto propio, traza propia, pruebas propias. Únicamente comparte la
**técnica** general (tokenización + solapamiento léxico de palabras significativas), no
código ni configuración: implementa su propia función de tokenización/solapamiento
dentro de su propio módulo (`solution_non_disclosure_verifier_agent.py`) — no importa
ni reutiliza la función privada de `grounding_verifier_agent.py` (que además no se
puede modificar para exportarla sin tocar un fichero de la Feature 002, FR-025).

| | `GroundingVerifierAgent` (Feature 002) | `SolutionNonDisclosureVerifierAgent` (Feature 003) |
|---|---|---|
| Compara | `proposal_text` vs `evidence` (materiales) | `question_text` vs `internal_expected_answer` (interno, nunca mostrado) |
| Constante de umbral | `_SUPPORT_OVERLAP_THRESHOLD = 0.4` (Feature 002, sin cambios) | `_DISCLOSURE_OVERLAP_THRESHOLD = 0.3` (nueva, Feature 003, más sensible — un falso negativo aquí es peor: revela una solución) |
| Configuración | fija en código (Feature 002 no la expone por env var) | `ORALIA_DISCLOSURE_OVERLAP_THRESHOLD` (configurable, Feature 003) |
| Veredicto | 5 valores (`fundamentada`…`no_verificable`) | 2 valores (`approved`/`block`) |
| Traza | `GroundingVerificationResult` (no persistido como tabla propia en esta feature — usado vía `AgentResult`) | `TraceEvent non_disclosure_check` |
| Pruebas | `tests/contract/test_grounding_verifier.py` (Feature 002) | `tests/contract/test_solution_non_disclosure_verifier.py` (Feature 003, nuevo) |

**Cadena si `verdict = block`**: regeneración acotada (hasta
`ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS`, default 2) con la incidencia añadida al contexto
de la siguiente petición → si se agotan los intentos, `PracticeQuestionAgent` produce su
salida final con `DeterministicGenerationAdapter` directamente (construcción
determinista que separa `question_text` de `internal_expected_answer` por diseño, sin
riesgo de fuga). Si `reveals_solution = true`, este verificador **no se activa** (FR-003).

**Limitación documentada del MVP**: una heurística determinista de solapamiento léxico
**puede producir falsos negativos ante paráfrasis complejas** (p. ej. una reformulación
de la solución con sinónimos y sin superposición literal de palabras significativas no
sería detectada). Esta limitación se acepta explícitamente para el MVP — **no se añade
un segundo LLM como juez** de esta comprobación (evitaría exactamente el problema que el
Principio IV ya señala: un modelo de lenguaje evaluando la salida de otro modelo de
lenguaje no es una verificación observable y añadiría una segunda dependencia de
inferencia sin necesidad demostrada, Principio XI). Se documenta como riesgo conocido a
revisar con evidencia real durante `/speckit-implement`/`/speckit-converge`, no como un
requisito nuevo de esta feature.

**Rationale**: contrato, umbral, veredicto y traza independientes cumplen literalmente
la instrucción de esta ronda; la técnica compartida (no el código) es coherente con el
patrón ya establecido en el proyecto (heurísticas deterministas de solapamiento en vez
de modelos de NLI, Feature 002 research.md §7) sin comprometer la independencia real
entre ambos verificadores.

### Refuerzo: soluciones cortas o puramente numéricas (H04, estabilización 2026-09-10)

**Hallazgo de partida**: `_significant_words` tokeniza con `[a-záéíóúñü]+`, que excluye
dígitos por completo. Cuando `internal_expected_answer` es puramente numérico o
demasiado corto para producir palabras de ≥4 letras (p. ej. "4", "12", "x=3"),
`answer_words` queda vacío y `_overlap_score` devuelve `0.0` **sin examinar la
pregunta**, de modo que *"La respuesta es 4"* con solución interna *"4"* se aprueba
siempre — no es un falso negativo ocasional por paráfrasis (el límite ya documentado
arriba), es una ausencia total de comprobación para todo el subconjunto de soluciones
cortas/numéricas.

**Decision — refuerzo determinista, mismo umbral y mismo agente, sin LLM adicional**:

1. **Tokenización ampliada**: además de palabras ≥4 letras, `_significant_words` (en
   `solution_non_disclosure_verifier_agent.py`, sin tocar la función homónima de
   `grounding_verifier_agent.py`, Feature 002, FR-025) MUST tratar como token
   significativo cualquier secuencia de dígitos (`\d+`) y cualquier expresión corta
   alfanumérica de solución (p. ej. `x=3`, `h2o`) mediante un patrón adicional
   `[a-záéíóúñü0-9]+` con longitud mínima 1 para tokens puramente numéricos — evita que
   `answer_words` quede vacío precisamente cuando la solución es más fácil de filtrar
   textualmente (números, fórmulas cortas).
2. **Regla de solución corta**: si `internal_expected_answer` tokenizado (con la regla
   anterior) produce un único token, la comprobación debe exigir coincidencia exacta de
   ese token en `question_text` (no una proporción de solapamiento sobre un conjunto de
   tamaño 1, que degenera trivialmente) para decidir `block` — evita tanto el falso
   negativo (H04) como una posible sobrecorrección que bloquee cualquier pregunta que
   comparta casualmente un carácter con la solución.

**Matriz de aceptación (casos de control — corregida; T1 y V1 tenían errores de oráculo
en la primera ronda)**:

| # | `question_text` | `internal_expected_answer` | Esperado | Motivo |
|---|---|---|---|---|
| N1 | "¿Cuál es el resultado? La respuesta es 4." | "4" | `block` | caso original H04 — solución numérica corta |
| N2 | "¿Cuánto vale la constante de gravitación?" | "9.8" | `approved` | la pregunta no contiene el valor — solución numérica legítima que no debe bloquear indiscriminadamente |
| N3 | "Resuelve la ecuación x=3 para la variable dada." | "x=3" | `block` | solución alfanumérica corta, coincidencia exacta |
| N4 (nuevo — dato legítimo del enunciado) | "Un grupo tiene 4 asignaturas optativas; ¿cuántas ha aprobado el estudiante medio?" | "4" (coincide con el dato del enunciado por azar, no por revelar la respuesta) | `block` (comportamiento del refuerzo, aceptado como conservador — ver nota) | ejercita la sobrecorrección de la regla de token único: "4" aparece en el enunciado por una razón ajena a la solución, y el refuerzo no puede distinguir esto solo por coincidencia léxica |
| T1 (**corregido** — la pregunta original de la primera ronda no compartía ninguna palabra con la solución; el caso no habría bloqueado bajo ningún mecanismo, ni el actual ni el reforzado) | "Explica por qué la presión atmosférica es menor a mayor altitud." | "porque la presión atmosférica es menor" | `block` | solapamiento léxico real (3/4 ≥ 0.3) — caso ya detectado por el mecanismo existente, sirve de referencia positiva |
| C1 (nuevo — negación, fuera del alcance de este refuerzo) | "¿Es correcto que la presión atmosférica NO es menor a mayor altitud?" | "porque la presión atmosférica es menor" | `block` (comportamiento actual por solapamiento léxico, coincide con el resultado correcto aquí solo por casualidad — la negación no se interpreta, el mecanismo no "entiende" que la pregunta niega la afirmación) | se incluye para que quede explícito que la negación no se interpreta, no para prometer que siempre coincide con el resultado deseado |
| V1 (**corregido** — ya no queda "reservada sin resultado esperado"; FR-013a prioriza no revelar una solución sobre evitar un falso positivo raro) | "¿Qué fracción de 12 es 4?" | "4" | `block` | el token único "4" de la solución aparece literalmente en la pregunta — bajo la regla de coincidencia exacta de token único (arriba), esto bloquea aunque "4" sea parte legítima del enunciado (mismo patrón que N4); se acepta como el resultado seguro/conservador dado FR-013a — si en la práctica resulta demasiado disruptivo, la corrección recomendada es que `PracticeQuestionAgent` evite generar preguntas cuyo enunciado coincida textualmente con `internal_expected_answer`, no relajar este verificador |

**Límite documentado**: sigue sin cubrir revelación parafraseada de una solución textual
larga (limitación ya aceptada arriba); el refuerzo es específico del caso "solución
corta/numérica sin cobertura alguna", no una generalización semántica. La
sobrecorrección de N4/V1 (bloquear una coincidencia numérica casual del enunciado) es
un trade-off aceptado explícitamente, no un defecto oculto: FR-013a prioriza no
revelar una solución sobre evitar un falso positivo infrecuente.

## 5. Coherencia y metacognición: umbrales y relaciones operacionales

Sin cambios respecto a la iteración anterior:

- **"Ausencia de progreso"**: ventana configurable `NO_PROGRESS_TURN_WINDOW = 3`
  (`ORALIA_COHERENCE_NO_PROGRESS_WINDOW`) de turnos sin nueva entrada en
  `concepts_addressed`.
- **"Repetición"**: solapamiento léxico (técnica propia de `CoherenceVerifierAgent`,
  igualmente independiente de `GroundingVerifierAgent` y de
  `SolutionNonDisclosureVerifierAgent` — tres implementaciones de la misma técnica
  general, cada una con su propio umbral y responsabilidad, ver §4) contra el
  `output_text` del turno inmediatamente anterior únicamente
  (`REPETITION_WINDOW_TURNS = 1`, `ORALIA_COHERENCE_REPETITION_WINDOW`) — no contra todo
  el historial, para no generar falsos positivos en `concept_review`.
- **"Fallo de agente"/"latencia excesiva"**: derivados directamente por el compositor
  de agencia desde `AgencyOutcome` (Feature 001, `execute_agency`, sin cambios) — no un
  verificador independiente.
- **Combinación de veredictos (FR-024)**: orden de severidad fijo
  `block > reformulate > clarify > acknowledge_missing_info > approved`, aplicado por el
  paso `verify-combined` del compositor. Mapeo `GroundingVerifierAgent` → severidad:
  `no_fundamentada` → `acknowledge_missing_info`; `conflictiva` → `clarify`;
  `parcialmente_fundamentada`/`no_verificable` → `reformulate` (acotado, mismo límite de
  reintentos que §4); `fundamentada` → `approved`. Empate de severidad con
  `CoherenceVerifierAgent` → gana `CoherenceVerifierAgent` (contexto de sesión completo).

## 6. Fuente de verdad del modo activo: `CognitiveState.mode`, no la traza

**Decision**: el campo `mode` de `CognitiveState` (Feature 001, **campo ya existente,
sin ampliar el esquema**) es la fuente de verdad del modo canónico actualmente activo
durante la sesión. `SelfStudyActivityConfig.enabled_modes` (Feature 003) es el conjunto
de modos **permitidos** para la actividad; `CognitiveState.mode` es **cuál de ellos está
activo ahora mismo**, exactamente el mismo tipo de distinción que ya existe entre
`AgentContract` (catálogo de lo posible) y `CognitiveState` (lo que ocurre en esta
sesión).

**Mecanismo de cambio**: el modo **puede cambiar durante una sesión** (US3, US5, US9:
un estudiante con varios modos habilitados puede pedir una duda y después preguntas de
práctica en la misma sesión). Cada turno, `self_study_agency_composer.py`:

1. Lee `CognitiveState.mode` actual (vía `get_or_create`, Feature 001, sin cambios) como
   el modo activo hasta ahora.
2. Obtiene `requested_mode` de `StudyIntentInterpreterAgent` (`null` si el turno
   continúa el modo actual, p. ej. respondiendo una pregunta de práctica ya en curso).
3. Si `requested_mode` no es `null`, lo valida contra `enabled_modes`
   (`SelfStudyActivityConfig`); si es válido y distinto del modo actual, se aplica un
   `StatePatch` (Feature 001, `apply_patch`, **mecanismo ya existente y versionado, sin
   cambios**) con `element_type = "decision"` y `payload = {"mode": requested_mode}`
   sobre `CognitiveState.mode`, con el mismo control de versión optimista
   (`base_version`/`resulting_version`) que cualquier otro cambio de estado.
4. El resto del turno (recuperación, generación, verificación) opera sobre el modo
   resultante de ese patch — nunca sobre un valor leído de `TraceEvent`.

**Papel de la traza**: `TraceEvent agents_selected` sigue registrando `payload.mode`
como **copia de auditoría** de la decisión ya tomada (para reconstrucción y para
verificar SC-001 sin inspeccionar texto) — la orquestación nunca lee el modo activo
desde la traza; la traza documenta una decisión ya persistida en `CognitiveState` a
través de `StatePatch`, no la sustituye ni la duplica como mecanismo de decisión.

**Rationale**: usar el campo `mode` ya existente de `CognitiveState` (en vez de
introducir `active_mode` como campo nuevo) cumple literalmente "no dupliques el estado
ni introduzcas otro mecanismo paralelo" — el campo ya tenía exactamente esta forma
(`string`, versionado, mutable vía `StatePatch`) y ningún otro dato de la Feature 001 lo
usa con un significado incompatible (Feature 001 lo deja como un string libre sin
semántica fijada, `research.md` de esa feature no le asigna un contrato específico).
Corrige el diseño de la iteración anterior, que dejaba el modo activo solo en la traza
— un registro de auditoría no es una fuente de verdad para decisiones de orquestación
(Principio III: el estado que gobierna decisiones debe ser el explícito y versionado,
no un log derivado).

**Diferenciación de modos (FR-001a, SC-001)**: la tabla de composición por modo de la
iteración anterior (pasos activados, generador usado, campo `CognitiveState`
distintivo, patrón de `dialogue_action`) se mantiene sin cambios — solo cambia de dónde
se lee "cuál es el modo de este turno": antes, implícitamente, del resultado del
intérprete en memoria; ahora, explícitamente, de `CognitiveState.mode` tras aplicar el
`StatePatch` del paso 3 anterior.

## 7. Inmutabilidad de la configuración de modos (FR-002a, Edge Cases)

Sin cambios respecto a la iteración anterior: `SelfStudyActivityConfig` solo se
crea/actualiza mientras `ActivityConfiguration.immutable_since` es `null`; `409` en
caso contrario. Nótese la distinción con §6: `enabled_modes` (inmutable tras el primer
uso, gobierna qué está *permitido*) es un concepto distinto de `CognitiveState.mode`
(mutable turno a turno dentro de los límites de `enabled_modes`, gobierna qué está
*activo ahora*) — ambos conceptos, antes posiblemente confundidos, quedan explícitamente
separados por esta ronda de corrección.

## 8. Privacidad y retención: qué garantiza realmente esta feature (FR-011a, FR-028)

**FR-011a — no agregación**: sin cambios. Ninguna consulta/endpoint de esta feature
acepta `participant_code` como filtro de agregación entre sesiones; todo filtra por
`session_id`.

**FR-028 — retención, alcance real de esta feature**:

1. **Qué garantía proporciona realmente Feature 003**: (a) todo dato derivado de
   autoestudio (`PracticeQuestion`, `CoherenceIncident`, `TraceEvent` de esta feature)
   queda asociado, transitivamente vía `Session.activity_configuration_id →
   ActivityConfiguration.retention_policy_id`, al mismo `RetentionPolicy.retention_days`
   (Feature 001, esquema ya existente, `int | null`) que gobierna el resto de datos de
   esa actividad — sin campo ni tabla de retención propia (sin sistema paralelo); (b) un
   **mecanismo invocable** (nuevo, ver punto 2) que, al ejecutarse, elimina
   efectivamente los datos de sesiones cuyo `retention_days` ya expiró.
2. **Qué se construye, porque no existía nada que reutilizar**: no existe en ningún
   punto del código (ni de la Feature 001 ni de ninguna anterior) un mecanismo de
   purga ya implementado — `retention_policy.py` (Feature 001) solo tiene `create`/`get`
   (verificado). Esta feature añade `application/commands/purge_expired_self_study_data.py`:
   una función invocable manualmente (`purge_expired_self_study_data(db, *, now=None) ->
   PurgeResult`) que localiza `Session`es cuya `ActivityConfiguration.retention_policy_id`
   tiene `retention_days` no nulo y `ended_at + retention_days < now`, y elimina sus
   filas de `PracticeQuestion`, `CoherenceIncident` y los `TraceEvent` de tipo
   `generation_call`/`non_disclosure_check`/`verification_combined`/
   `study_session_summary`/`agents_selected` asociados a esa sesión — exactamente el
   alcance de datos que FR-028 nombra explícitamente ("PracticeQuestion,
   CoherenceIncident, resumen de sesión"), no el resto de datos de sesión de la Feature
   001 (fuera del alcance de esta feature). Expuesto vía
   `POST /api/v1/tecnica/self-study/purge-expired` — invocación manual del profesorado/
   administrador (Principio VI: eliminación de datos bajo control humano explícito), sin
   scheduler ni cron.
3. **Qué queda explícitamente aplazado a la Feature 005**: automatización/programación
   de la purga (ejecución periódica sin intervención manual), exportación de datos antes
   de purgar, UI de gestión de retención para el profesorado, y cualquier política de
   purga más granular que "toda la sesión expirada" (p. ej. purga parcial). La
   constitución reserva "revisión, privacidad y exportación" a la Feature 005 —
   `purge_expired_self_study_data` es la pieza mínima invocable que esa feature
   automatizará, no la automatización en sí.

**Rationale**: distingue con precisión la garantía real (dato ya vinculado a una
política finita + mecanismo que la hace efectiva bajo invocación explícita) de la
automatización (fuera de alcance, Feature 005) — evita tanto declarar FR-028
"completamente resuelto" sin mecanismo alguno (como en la iteración anterior) como
construir infraestructura de scheduling no pedida (instrucción explícita de esta
ronda). No se introduce un sistema de retención paralelo: se reutiliza íntegramente el
esquema de `RetentionPolicy` (Feature 001) y solo se añade la operación de purga que
ese esquema necesitaba para ser algo más que una declaración de intención.

## 9. Trazabilidad ampliada

Sin cambios respecto a la iteración anterior salvo el renombrado `template` →
`deterministic` en `generation_call.payload.adapter` (§1) y la precisión de §6 (la
traza registra el modo, no lo decide): `agents_selected`, `generation_call`,
`non_disclosure_check`, `verification_combined` — cuatro `event_type` nuevos sobre la
tabla `TraceEvent` ya existente (Feature 001, sin cambios de esquema), más
`study_session_summary` (sin cambios respecto a la iteración anterior).

**Verificación de SC-001 sin comparar texto**: el conjunto
`{CognitiveState.mode (tras el StatePatch del turno), agents_selected.payload.mode
(copia de auditoría, debe coincidir), agents_selected.payload.activated_steps,
generation_call.payload.purpose, DialogueAction.action_type}` de un turno es suficiente
para afirmar "este turno perteneció al modo X y activó las decisiones estructurales Y"
sin inspeccionar `output_text`.

## 10. Simplicidad arquitectónica (reconfirmación)

Sin cambios: monolito modular, mismo protocolo `Executable`, mismo patrón de
`AgencyDefinition`/`execute_agency`. Eliminar el tercer adaptador de generación (§1) y
evitar un segundo mecanismo de retención (§8) son, precisamente, aplicaciones directas
de este principio en esta ronda de corrección.

## 11. Cierre de autoestudio: dos vías, un único resumen (FR-020/FR-021/FR-021a/FR-021b) — estabilización 2026-09-10

**Hallazgo de partida (H05)**: `Autoestudio.tsx` llama a `endSession` →
`POST /sessions/{id}/end` (Feature 001, genérico) — nunca a `POST /study-turns`... nunca
a `POST /study-end`; no existe ninguna función `study-end` en todo `apps/web/src`.
Además, `submit_study_turn.py` invoca `end_study_session(...)` en el cierre automático
por límite pero descarta su valor de retorno, y la respuesta de `POST /study-turns` no
expone ni el resumen ni un indicador de cierre — con lo que, tras un cierre automático,
`POST /study-end` (si se llegara a invocar) encuentra `session.status != "active"` y
devuelve `study_summary: null` **siempre**: el resumen generado queda irrecuperable para
el participante en ambos frentes (frontend que no pregunta, y contrato que ya no puede
entregarlo si se preguntara).

**Decision adoptada (instrucción explícita de esta ronda)**:

1. **Cierre voluntario** — `POST /sessions/{id}/study-end` comunica el cierre y entrega
   `study_summary` cuando `summary_authorized = true` y se generó (sin cambios respecto
   al contrato ya existente, `contracts/api-self-study.md`).
2. **Cierre automático por límite** — la respuesta de `POST /sessions/{id}/study-turns`
   del turno que hace que se alcance el límite (FR-020) MUST incluir, en esa misma
   respuesta, la comunicación del cierre y el `study_summary` correspondiente (mismo
   campo, misma semántica de nulabilidad que en `study-end`) — `end_study_session(...)`
   ya calcula ese valor hoy (`submit_study_turn.py`); el cambio es dejar de descartarlo y
   añadir los campos correspondientes al `response` de `post_study_turn`
   (`self_study.py`), no generar el resumen dos veces.
3. **Interfaz** — `Autoestudio.tsx` MUST reconocer el cierre en cualquiera de las dos
   respuestas (un campo `session_closed`/`status` no-`"active"` en la respuesta del
   turno, o la propia respuesta de `study-end`) y MUST deshabilitar el envío de nuevos
   turnos en cuanto lo detecta — sin introducir una tercera vía de recuperación del
   resumen (FR-021, FR-021b).
4. **Idempotencia de un cierre repetido** — una segunda llamada a `study-end` sobre una
   sesión ya cerrada (por cualquiera de las dos vías) MUST devolver `status` (el ya
   persistido) y `study_summary: null` — **no** un error, y **no** una regeneración del
   resumen; el resumen ya fue entregado (o, si su respuesta se perdió, ya no es
   recuperable — ver más abajo). Análogamente, si el turno que ya cerró la sesión se
   reenvía (reintento de red), `submit_study_turn` MUST rechazarlo como sesión inactiva
   (mecanismo `SessionNotActive` ya existente, sin cambios) en vez de volver a evaluar el
   límite y regenerar un segundo resumen.
5. **Pérdida de la respuesta de cierre** — ninguna de las dos vías promete una entrega
   garantizada exactamente una vez: si la respuesta HTTP que comunica el cierre (de
   `study-turns` o de `study-end`) no llega al cliente por un fallo de transporte, el
   sistema **no** reintenta ni ofrece una vía alternativa para recuperar ese resumen
   (violaría FR-021 — "visualización única"); el resumen permanece disponible
   únicamente como `TraceEvent event_type=study_session_summary` para el área técnica
   (auditoría, no consulta del participante). Se documenta como límite aceptado, no
   como un defecto a corregir con reintentos/claves de idempotencia — añadir
   infraestructura de entrega garantizada no está justificada por ningún escenario de
   `spec.md` (Principio XI).

**Qué NO cambia**: FR-021 sigue siendo un MAY sobre generar el resumen — esta decisión
no lo convierte en un MUST; solo precisa, cuando sí se genera, en qué respuesta concreta
se entrega en cada uno de los dos cierres posibles (FR-021a) y qué debe hacer la interfaz
al reconocerlo (FR-021b).

**Campos de contrato afectados** (ver `contracts/api-self-study.md`, actualizado en esta
ronda): `POST /study-turns` añade `session_closed: bool` (por defecto `false`;
`true` solo en el turno que cierra por límite) y `study_summary: object | null`
(presente únicamente cuando `session_closed = true`); ninguno de los dos campos existe
en una respuesta de turno normal, para no alterar el esquema ya validado en el resto de
los casos.

## 12. Retención y purga de datos derivados: autorización explícita, alcance y verificación de nombres compartidos (FR-028/FR-028a) — corregido en la segunda ronda de estabilización, 2026-09-10

### 12.1 H06 — autorización de conservación (corregido: un plazo no es una autorización)

**Corrección respecto a la primera ronda**: el texto anterior de esta sección
equiparaba "existe un `RetentionPolicy` con `retention_days` finito" con "hay
autorización para conservar". Esa equivalencia es incorrecta y queda retirada: un
plazo (`retention_days`) expresa **cuánto tiempo**, nunca **si** está autorizado
conservar — una actividad podría tener una política finita asociada por razones
ajenas a una decisión consciente sobre los datos de autoestudio (p. ej. heredada de
otra configuración de la misma actividad), sin que eso implique que alguien decidió
conservar `PracticeQuestion`/`CoherenceIncident`/el resumen.

**Decision (FR-028a corregida)**: se añade `SelfStudyActivityConfig.
retention_authorized: bool | null` — campo nuevo, propio de esta feature (no toca el
esquema de la Feature 001), independiente de `summary_authorized` (que sigue
significando únicamente "autorizado a *generar* el resumen", FR-021) y de
`RetentionPolicy` (que sigue significando únicamente "cuánto tiempo", sin cambiar su
semántica de la Feature 001 — `null` sigue significando allí "indefinido hasta purga
manual" para el resto de sus propios datos). Autorización de conservación efectiva
requiere **ambas** condiciones: `retention_authorized = true` **y**
`RetentionPolicy.retention_days` finito (no nulo) asociado. Ninguna de las dos por sí
sola autoriza nada — ni un plazo sin autorización explícita, ni una autorización sin
plazo que la acote (FR-028: "MUST declarar un periodo... finito").

**Tres estados, no dos**:

1. **Nueva configuración sin autorización** (`retention_authorized = false`, o
   `= true` pero sin política finita asociada — combinación inválida, tratada igual
   que "no autorizada", no como "autorizada sin límite"): sus datos derivados MUST
   tratarse como sin autorización de conservación (FR-028a). Qué ocurre al cerrar sin
   autorización: el cierre de sesión (FR-020) no cambia — no se borra nada de forma
   síncrona en `end_study_session`; lo que cambia es que, desde ese cierre en
   adelante, esos datos ya son candidatos para la purga (§12.2) desde la primera
   invocación manual posterior, sin esperar ningún plazo (no hay uno que esperar).
2. **Configuración autorizada con plazo finito válido** (`retention_authorized = true`
   y `retention_days` finito): sin cambios respecto al mecanismo original — candidata
   a purga cuando `Session.ended_at + retention_days < now()`. Cómo se aplica el
   plazo: exactamente como hoy, sin modificar `RetentionPolicy` ni su semántica
   general.
3. **Configuraciones/datos preexistentes** (creadas antes de que `retention_authorized`
   exista como campo — MUST recibir `null` en la migración, nunca `true` ni `false`
   por defecto): quedan en un estado explícito "sin decidir", excluidas tanto del
   camino 1 como del camino 2 hasta que una persona con permiso (profesorado/
   administrador) fije el campo explícitamente. Esta decisión **es humana y MUST
   identificarse como tal** — MUST NOT deducirse de cuántas veces se invoque
   ningún endpoint (ver §12.2: la eliminación de la regla "primera ejecución avisa,
   segunda purga").

### 12.2 Diagnóstico sin efectos, separado de la acción de purga (corrige la regla implícita de "segunda ejecución")

**Corrección respecto a la primera ronda**: el diseño anterior hacía que una sesión sin
política finita apareciera en un informe en la primera ejecución de
`purge_expired_self_study_data` y se purgara en una ejecución **posterior** de ese
mismo endpoint — es decir, invocar la purga una segunda vez actuaba como si fuera el
consentimiento humano que FR-028a exige. Esa regla queda **eliminada**: ningún número
de invocaciones de la purga sustituye una decisión humana explícita sobre
`retention_authorized`.

**Decision**: dos operaciones distintas, con contratos distintos:

- **`GET /api/v1/tecnica/self-study/retention-audit`** (nuevo, solo lectura, sin
  efectos secundarios — "consulta de diagnóstico"): lista, para cada actividad de
  autoestudio, su estado de autorización (`authorized_expiring` /
  `not_authorized_purge_eligible` / `undecided_preexisting` /
  `invalid_authorized_without_policy`) y cuántas sesiones/filas caerían en cada
  categoría si se ejecutara la purga ahora. No borra nada bajo ninguna circunstancia,
  sin importar cuántas veces se invoque.
- **`POST /api/v1/tecnica/self-study/purge-expired`** (sin cambios de nombre —
  "acción de purga con semántica explícita"): elimina datos **únicamente** de sesiones
  en los estados `authorized_expiring` (plazo cumplido) o
  `not_authorized_purge_eligible` (§12.1, caso 1). **MUST NUNCA** eliminar datos de una
  sesión en estado `undecided_preexisting` o `invalid_authorized_without_policy`,
  sin importar cuántas veces se invoque este endpoint — la única forma de que una
  sesión `undecided_preexisting` se vuelva purgable es que una persona fije
  `retention_authorized` explícitamente (vía el endpoint de configuración de
  `SelfStudyActivityConfig`, no vía la purga).

### 12.3 H07 — alcance de la purga de `TraceEvent` (verificación de nombres compartidos, sin cambios respecto a la primera ronda — ya era correcto)

El criterio por `event_type` (`generation_call`, `non_disclosure_check`,
`verification_combined`, `study_session_summary`, `agents_selected`) y la exclusión de
`session_started`/`session_closed`/`technical_summary` (mecanismo de sesión de la
Feature 001) y de `agent_execution`/`turn_completed`/`constitutional_block`
(compartidos literalmente con la Feature 001, distinguibles solo por `agent_id`/
contexto) se mantienen sin cambios — el inventario completo por inspección de código
(`grep event_type=` sobre `src/oralia`) ya publicado en la primera ronda es correcto y
no se repite aquí.

**El riesgo de `/turns` genérico, separado del criterio (corregido)**: la primera
ronda mezclaba, en la misma frase, el criterio de purga por `event_type` (correcto,
verificado por inspección) con el riesgo — no confirmado — de que
`POST /sessions/{id}/turns` (endpoint genérico de la Feature 001) pudiera invocarse
sobre una sesión con `SelfStudyActivityConfig`. Son dos cuestiones independientes: la
posibilidad teórica de ese endpoint no invalida la lista de `event_type` exclusivos de
003 (que siguen siendo exclusivos de 003 con independencia de qué otro endpoint exista).
Este riesgo se retira de la definición del criterio y se registra únicamente como
**prueba pendiente** (§12.5) — no se trata como un defecto del criterio hasta que una
reproducción concreta demuestre una colisión real (un `Turn`/`TraceEvent` de origen
genuinamente 001 creado dentro de una sesión de autoestudio, y purgado o no
correctamente); sin esa demostración, no se bloquea ni se amplía el criterio.

### 12.4 Duplicación con otros registros (corregido: se encontró duplicación real)

**Corrección respecto a la primera ronda**: la afirmación "sin duplicación
problemática" se basaba únicamente en que `self_study_agency_composer.py` no escribe
directamente `GroundingVerificationResult`/`Evidence`/`MaterialConflictRecord` (Feature
002) — cierto, pero insuficiente: no examinaba las llamadas transitivas a
`StatePatch`/`CognitiveState` (Feature 001) que el propio compositor sí realiza en
cada turno.

**Hallazgo verificado por inspección**: `self_study_agency_composer.py` (función
`_finalize_turn`, patches de turno) incluye, en **todo turno**, un `StatePatch` con
`element_type = "decision"` y `payload = {"participant_response": text}`, donde `text`
es el `output_text` ya generado del turno — que en un turno de modo
`practice_questions` **es el `question_text` de la pregunta de práctica**. Además, el
mismo compositor persiste `GeneratedProposal`/`VerificationResult` (tablas de la
Feature 001, reutilizadas sin cambios) con ese mismo texto, y `Turn.input_text`/
`Turn.output_text` (Feature 001) conservan la pregunta del estudiante y la respuesta
generada de forma literal. Ninguna de estas tablas (`StatePatch`, `GeneratedProposal`,
`VerificationResult`, `Turn`) está en el alcance de la purga de esta feature (§12.3,
correctamente — son de la Feature 001, y FR-028 no las nombra) — pero eso significa que
**purgar `PracticeQuestion`/`CoherenceIncident`/el resumen no elimina el contenido
textual subyacente del sistema**: sigue existiendo, indefinidamente salvo que la
Feature 001 tenga su propio mecanismo de retención/purga para `Turn`/`GeneratedProposal`
/`StatePatch` — mecanismo que, por lo verificado en la ronda de diagnóstico anterior,
**no existe todavía** ("no existe en ningún punto del código un mecanismo de purga ya
implementado" para los datos generales de sesión de la Feature 001).

**Esto no se resuelve en esta ronda** — ampliar la purga de 003 para tocar `Turn`/
`GeneratedProposal`/`StatePatch` (tablas de la Feature 001) excedería el alcance
declarado de esta feature (FR-025: no modificar el comportamiento ya validado de la
Feature 001) y el propio alcance textual de FR-028 (que nombra únicamente
`PracticeQuestion`, `CoherenceIncident` y el resumen de sesión). Se documenta como una
**contradicción abierta entre el objetivo declarado de FR-028** ("MUST NOT
conservarse de forma permanente por defecto") **y su alcance textual** (limitado a
tres artefactos que no son la única copia del contenido) — ver la entrega de esta
ronda, apartado de contradicciones/decisiones abiertas, para la decisión de producto
pendiente (si FR-028 debe interpretarse de forma más amplia, lo que requeriría un
mecanismo de purga propio de la Feature 001, fuera del alcance de 003).

### 12.5 Criterio final de purga y contadores (corregido: `sessions_purged` no implica "sigue expirada" ni "ya no expirada")

**Corrección respecto a la primera ronda**: el criterio de aceptación anterior
afirmaba que ejecutar la purga dos veces seguidas "MUST producir `sessions_purged = 0`
en la segunda ejecución (idempotencia)" — esto es engañoso: una sesión expirada
**sigue expirada** en la segunda ejecución; lo único que puede llegar a cero es
*cuántas filas quedaban por eliminar*, no el número de sesiones que cumplen el
criterio de expiración. Confundir ambas cosas presentaría como "ya no elegible" algo
que simplemente "ya no tiene nada pendiente que borrar".

**Decision — redefinición de `PurgeResult`** (documental, no implementada aún):

```text
PurgeResult:
  sessions_matching_criteria: int   # RENOMBRADO desde sessions_evaluated — sesiones que
                                     # cumplen el criterio de expiración en esta
                                     # ejecución (autorizadas-expiradas o
                                     # no-autorizadas-purgables); estable o creciente
                                     # entre ejecuciones sucesivas, nunca decrece por sí
                                     # solo
  sessions_with_rows_deleted: int   # RENOMBRADO desde sessions_purged — sesiones para
                                     # las que ESTA ejecución eliminó efectivamente ≥1
                                     # fila; naturalmente 0 en una repetición sin datos
                                     # nuevos que purgar, sin que eso signifique que
                                     # esas sesiones dejaron de cumplir el criterio
  practice_questions_deleted: int
  coherence_incidents_deleted: int
  trace_events_deleted: int
```

`sessions_flagged_no_finite_policy` de la primera ronda se retira de `PurgeResult` —
ese diagnóstico vive ahora, sin efectos, en `GET .../retention-audit` (§12.2), no en la
respuesta de la acción de purga.

**Criterio final de purga**: elegible ⟺ (`PracticeQuestion`/`CoherenceIncident` de la
sesión) **o** (`TraceEvent` cuyo `event_type` ∈ {`generation_call`,
`non_disclosure_check`, `verification_combined`, `study_session_summary`,
`agents_selected`}), para sesiones en estado `authorized_expiring` (plazo cumplido) o
`not_authorized_purge_eligible` (§12.1/§12.2) — nunca para sesiones
`undecided_preexisting` o `invalid_authorized_without_policy`.

### 12.6 Criterios de aceptación (corregidos)

- Una sesión con eventos mixtos (los cinco `event_type` de 003 **y**
  `session_started`/`session_closed`/`agent_execution` de 001 en la misma sesión)
  purgada MUST conservar estos tres últimos y eliminar solo los cinco de 003.
- Una sesión no expirada (política finita vigente y autorizada, dentro de plazo) MUST
  NOT verse afectada por ninguna ejecución de la purga.
- Ejecutar la purga dos veces seguidas sobre el mismo estado MUST producir
  `sessions_with_rows_deleted = 0` en la segunda ejecución **y**
  `sessions_matching_criteria` MUST seguir incluyendo esas mismas sesiones (no
  "olvidarlas" por no tener ya filas que borrar).
- Una sesión `undecided_preexisting` MUST aparecer en `GET .../retention-audit` y MUST
  NOT ser purgada por ninguna cantidad de invocaciones de `POST .../purge-expired`;
  MUST volverse purgable únicamente tras fijar `retention_authorized` explícitamente.
- Una sesión `not_authorized_purge_eligible` (`retention_authorized = false`) MUST ser
  purgable desde la primera invocación posterior a su cierre, sin esperar ningún
  plazo.

### 12.7 Prueba pendiente explícita (H07, riesgo de `/turns` genérico)

Reproducir: invocar `POST /sessions/{id}/turns` (Feature 001) sobre una sesión con
`SelfStudyActivityConfig` asociada; confirmar si el endpoint lo permite y, si lo
permite, si el `Turn`/`TraceEvent` resultante queda o no dentro del alcance de purga
por `event_type` de esta feature — solo con este resultado concreto se decide si el
criterio de §12.5 necesita ajustarse.

## 13. El generador no recibe el texto literal de la consulta del turno actual (FR-006/FR-008) — estabilización 2026-09-10

**Hallazgo de partida (H01)**: `GenerationRequest` (`generation_port.py`) solo declara
`purpose`, `instruction`, `evidence`, `concepts_addressed`, `general_knowledge_allowed`,
`constraints` — ningún campo transporta el texto literal que el estudiante escribió en
este turno. El paso `generate` del compositor (`self_study_agency_composer.py`) construye
su `input` con exactamente esos campos; el texto del turno (`input_text`) solo se usa,
tras generar la respuesta, para derivar `concept_label` (un recorte a
`_MAX_CONCEPT_LABEL_CHARS`) que se añade a `concepts_addressed` — demasiado tarde para
influir en la respuesta que se está generando, y sin ser el texto original. El generador
decide qué decir a partir de una intención clasificada (`purpose`) y evidencia
recuperada, nunca de la pregunta concreta formulada.

**Decision — campo nuevo, mismo patrón de frontera datos/instrucciones ya validado
(FR-008b)**: `GenerationRequest` añade `student_input: str = ""` — el texto literal del
turno actual — transportado como **dato**, nunca interpolado en la plantilla `system`
fija (mismo principio ya aplicado a `evidence[].text`, research.md §3): viaja delimitado
explícitamente en el mensaje `user`, igual que la evidencia. No se introduce un tercer
adaptador ni un cambio de `GenerationPort`/`Protocol` más allá de este campo adicional
(con valor por defecto, para no romper construcciones existentes — ver compatibilidad
más abajo).

### Recorrido completo del campo (compositor → agente → `GenerationRequest` → adaptador)

1. **`self_study_agency_composer.py`, función `request_for_step`, rama
   `step.step_id == "generate"`**: añade `"student_input": input_text` al diccionario
   `input` del `AgentRequest` de ese paso — `input_text` ya está disponible en el
   ámbito de esa función (es el texto del turno actual, ya usado para derivar
   `concept_label`).
2. **`ResponseGeneratorAgent.execute`** (`response_generator_agent.py`): lee
   `data.get("student_input", "")` de `request.input` y lo pasa a
   `GenerationRequest(student_input=..., purpose=..., evidence=..., ...)`.
3. **`GenerationRequest`** (`generation_port.py`): nuevo campo
   `student_input: str = Field(default="")`.
4. **`OllamaGenerationAdapter._build_user_content`** (`ollama_adapter.py`): añade, solo
   cuando `request.student_input` no está vacío, un bloque delimitado explícitamente
   (p. ej. `<pregunta_actual>{student_input}</pregunta_actual>`) al mensaje `user` —
   igual patrón que `<evidencia>`, nunca en el mensaje `system`.
5. **`DeterministicGenerationAdapter`** (`deterministic_adapter.py`): **sin cambios en
   su lógica** — sigue siendo puramente extractiva sobre `evidence` (research.md §1: "
   siempre produce una salida válida si evidence no está vacío"), por diseño no
   personaliza su salida a `student_input`. Esto es intencional, no un descuido: es la
   razón por la que el criterio de aceptación no puede ser "`output_text` siempre
   distinto" (ver más abajo).
6. **`PracticeQuestionAgent`** (`practice_question_agent.py`): **no se modifica** — no
   construye `student_input` (queda en su valor por defecto `""`); su entrada ya
   documentada (`contracts/self-study-agents.md`) no incluye el texto del estudiante
   porque genera una pregunta nueva, no responde a una — coherente con el alcance ya
   fijado.

### Compatibilidad de los casos existentes

`student_input` tiene valor por defecto `""` en `GenerationRequest` — ninguna
construcción existente de `GenerationRequest` (incluida la de `PracticeQuestionAgent`,
y cualquier prueba que construya el objeto directamente sin este campo) se rompe.
`_build_user_content` solo añade el bloque nuevo cuando `student_input` no está vacío,
así que las pruebas existentes que fijan el `payload`/mensaje `user` esperado para
`purpose = "pregunta_practica"` (donde `student_input` queda `""`) no cambian su
resultado esperado.

### Criterio de aceptación (corregido — no exige que `output_text` sea siempre distinto)

**Corrección respecto a la primera ronda**: el criterio anterior sugería observar si
la respuesta generada cambia entre dos preguntas distintas — incorrecto, porque (a) con
`OllamaGenerationAdapter` real, la salida de un LLM no es determinista y comparar
`output_text` sería una prueba frágil; (b) con `DeterministicGenerationAdapter` (la
reserva, que este proyecto sí usa en su suite normal, research.md §1), la salida es
**intencionalmente** la misma extracción de `evidence` con independencia de la
pregunta — exigir `output_text` distinto haría fallar el reforzamiento contra su propio
comportamiento correcto y documentado.

**Criterio correcto**: dos turnos con la misma evidencia/estado recuperados pero texto
de pregunta distinto MUST hacer llegar al adaptador (`GenerationRequest.student_input`,
o el `payload`/mensaje `user` construido a partir de él) un valor distinto — verificable
en el propio objeto de la petición o en el `user content` construido, sin necesitar una
llamada real a Ollama ni comparar el texto de salida.

**Pruebas que capturan la petición real, no solo el resultado**:

- Unitaria sobre `request_for_step` (compositor): el `input["student_input"]` del paso
  `generate` MUST ser exactamente `input_text` del turno.
- Unitaria sobre `ResponseGeneratorAgent.execute` con un doble de `GenerationPort` que
  **capture** el `GenerationRequest` recibido (no solo devuelva un resultado fijo):
  `.student_input` MUST coincidir con `request.input["student_input"]`.
- Unitaria sobre `_build_user_content` (función pura, sin red): dos
  `GenerationRequest` con la misma `evidence`/`purpose` y `student_input` distinto MUST
  producir un `user content` con los dos bloques `<pregunta_actual>` distintos entre sí.
- Integración a nivel de compositor: dos turnos `doubt_resolution` con evidencia
  recuperada idéntica (fragmentos forzados vía doble de `MaterialRetrieverAgent`) y
  texto distinto, usando un doble **capturador** de `GenerationPort` en vez del real —
  MUST confirmar que los dos `GenerationRequest` capturados difieren en
  `student_input`. Comprobar pertinencia de la respuesta (si el `output_text` resultante
  realmente atiende la pregunta) es una propiedad distinta, cubierta por research.md
  §14.2 de la Feature 002 (relevancia en recuperación) y por evaluación manual/Ollama
  real (research.md §1 de esta sección) — no por esta prueba de captura de la petición.

**Por qué no se resuelve reordenando `concepts_addressed`**: añadir el turno actual a
`concepts_addressed` *antes* de generar (en vez de un campo nuevo) mezclaría "conceptos ya
tratados en sesiones anteriores del mismo turno" (su propósito documentado, FR-010) con
"la pregunta de este turno concreto" — dos señales de vida distinta que un campo dedicado
mantiene separadas sin sobrecargar la semántica ya establecida de `concepts_addressed`.

**Alcance de la corrección**: propia de esta feature (`GenerationPort`/
`GenerationRequest`/`ResponseGeneratorAgent`/`PracticeQuestionAgent` son código de la
Feature 003, no de la 001/002) — no requiere aprobación de otra feature para
modificarse, a diferencia de H02/H03/H09/H10.

**Consumidor previsto**: la Feature 004 extiende `GenerationPurpose` (mismo archivo,
adición aditiva ya prevista en su propio plan) — su propio `FollowUpQuestionAgent`
debería recibir el mismo campo si reutiliza este puerto sin cambios; queda anotado como
supuesto a revisar antes de implementar 004 (ver entrega, apartado "supuestos de 004"),
sin modificar ahora los documentos de esa feature.
