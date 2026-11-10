# Research: Agencia de defensa oral y voz opcional

Resuelve las decisiones de diseño abiertas tras `/speckit-clarify` (spec.md,
Clarifications, sesión 2026-09-02). Feature estrictamente incremental sobre las
Features 001 (núcleo cognitivo), 002 (materiales/RAG) y 003 (agencia de autoestudio),
ya implementadas, validadas y convergidas. Solo se amplían puntos de integración
documentados y sus regresiones deben conservarse (FR-033, §25).

## 1. Mapa de reutilización — qué se reutiliza sin cambios, qué se extiende, qué es nuevo

**Reutilizado sin ningún cambio** (mismo fichero, mismo comportamiento, mismos tests):

| Componente | Feature | Uso en Feature 004 |
|---|---|---|
| `Session`/`Turn`, ciclo de sesión/turno, bloqueo de sesión única | 001 | Una sesión de defensa **es** un `Session` (mismo `mode` de `ActivityConfiguration` distingue el tipo de actividad) |
| `CognitiveState`/`StatePatch`/`apply_patch`, versionado optimista | 001 | Fuente de verdad del turno de defensa — sin campos nuevos (§11) |
| `ActivityConfiguration`, `RetentionPolicy`, patrón de inmutabilidad (`immutable_since`) | 001 | `DefenseActivityConfig` es 1:1, mismo patrón que `SelfStudyActivityConfig` |
| Puerta final T090 (`ConstitutionalControl`, snapshot, catálogo y persistencia) | 001 | Se reutiliza completa en cada salida visible; Feature 004 añade composición e integración, pero no relaja sus contratos ni duplica su verificador |
| `SafeFallbackAgent`, `execute_agency`, `run_with_deadline`, `AgencyDefinition`/`ExecutionStep` | 001 | Mismo motor de composición y degradación que ya usa `self_study_agency_composer.py` |
| `TraceEvent`/`record_event`/`reconstruct_session_trace` | 001 | Mismo mecanismo genérico por `event_type` — Feature 004 solo añade nuevos `event_type` (§17) |
| `MaterialRetrieverAgent`, aislamiento de autorización documental | 002 | Recuperación de materiales relacionados con la respuesta (FR-013), rechazo de temas fuera de alcance (FR-023/Edge Cases) — idéntico al patrón ya usado por `self_study_agency_composer.py` |
| `GroundingVerifierAgent` | 002 (vía 003) | Verifica fundamentación de la repregunta/pregunta antes de mostrarla |
| `GenerationPort` (Protocol), `OllamaGenerationAdapter`, `DeterministicGenerationAdapter` | 003 | Backend de generación de texto — reutilizado literalmente, sin un tercer adaptador (§2) |
| `CoherenceVerifierAgent` | 003 | Verifica contradicción/repetición de la repregunta frente al turno inmediatamente anterior — mismo umbral y técnica ya validados |
| `PracticeQuestionAgent` | 003 | Reutilizado **sin cambios** para generar la pregunta inicial cuando no hay banco docente (§8) |
| Patrón de `_finalize_turn`/persistencia de `GeneratedProposal`/`VerificationResult`/`DialogueAction` | 003 (patrón, no import) | Feature 004 replica el mismo patrón de cierre de turno en su propio compositor — no se importa código de `self_study_agency_composer.py` (evita acoplar dos features vía un módulo interno no pensado como API pública), pero no se reinventa su diseño |

**Extendido de forma aditiva** (mismo fichero de Feature 003, cambio retrocompatible que
no altera ningún comportamiento ya probado — distinto de "modificar el comportamiento ya
validado", FR-033):

| Componente | Extensión | Por qué es segura |
|---|---|---|
| `GenerationPort.GenerationPurpose` (`infrastructure/generation/generation_port.py`) | Añade únicamente `"repregunta"`; la pregunta inicial reutiliza el propósito existente de `PracticeQuestionAgent` | `Literal` amplía sus valores posibles; ningún valor ni comportamiento existente cambia; los tests de la Feature 003 sobre los propósitos ya existentes siguen pasando sin cambios |
| `DeterministicGenerationAdapter` | Rama adicional para el nuevo `purpose="repregunta"` (mismo patrón extractivo ya usado para `"pregunta_practica"`) | Puramente aditivo — no toca las ramas existentes |

**Genuinamente nuevo de esta feature**:

- `TranscriptionPort`/`SpeechSynthesisPort` (adaptadores de interfaz, §2)
- `FollowUpQuestionAgent` (§8-9) — única pieza cognitiva nueva
- `DefenseActivityConfig`, `Transcript`, `TranscriptCorrection`, `ConsentRecord` (persistencia nueva, §4/§12/§15)
- `defense_agency_composer.py` (orquestador, mismo patrón que `self_study_agency_composer.py`, no lo importa ni lo modifica)
- `defense_session_summary_service.py` (mismo patrón que `study_session_summary_service.py`, fichero propio)
- Router HTTP propio de esta feature

**Rechazado explícitamente tras análisis** (evita crear un componente equivalente a uno
ya existente):

- ~~`OralDefenseAgency`/`TextDefenseAgency` separadas~~ → una única composición dinámica,
  igual que los 5 modos de la Feature 003 comparten una única `self_study_agency_composer.py`
  (§6).
- ~~Entidad persistida `Repregunta`/`FollowUpQuestion`~~ → los metadatos estructurados
  (`purpose`, concepto origen/destino, razón, evidencia) se registran como payload de un
  `TraceEvent` nuevo (`followup_question_generated`) sobre el `GeneratedProposal`/
  `DialogueAction` ya existentes (Feature 001, sin cambios) — no aporta valor un modelo
  de tabla nuevo solo para duplicar lo que la traza ya expresa (§17).
- ~~Acción de diálogo `change_topic`~~ → se reutiliza `ask` con metadata estructurada
  `purpose=deepen_current_topic|switch_topic` (spec.md, Clarifications; §10).
- ~~`SummaryAgent` cognitivo~~ → igual que `study_session_summary_service.py` en la
  Feature 003, el resumen se construye por código determinista a partir de hechos ya
  persistidos (preguntas, conceptos, fuentes, incidencias) — nunca por un LLM, así que no
  hay ninguna responsabilidad cognitiva que justifique un agente (§14).
- ~~Generalizar `purge_expired_self_study_data`/`study_session_summary_service` de la
  Feature 003 para que también entienda tablas de defensa~~ → tocaría un fichero de la
  Feature 003 ya validada (aunque fuera retrocompatible, el riesgo/beneficio no lo
  justifica frente a un fichero propio de ~40 líneas que replica el mismo patrón).

**Nota explícita de deuda técnica aceptada (`defense_session_summary_service.py` y
`purge_expired_defense_data.py`)**: ambos ficheros **reutilizan el mismo patrón
conceptual** que sus equivalentes de la Feature 003 (`study_session_summary_service.py`/
`purge_expired_self_study_data.py`) — misma forma de `PurgeResult`, mismo criterio de
expiración, misma construcción determinista del resumen a partir de hechos persistidos
— pero son ficheros **físicamente separados**, no una librería compartida. Esto **no**
constituye un segundo subsistema cognitivo (ninguno de los dos invoca un LLM ni un
agente; ambos son código determinista sobre filas ya persistidas, exactamente como sus
equivalentes de la Feature 003) — es duplicación de **infraestructura de bajo riesgo**
(consultas SQL deterministas de ~15-40 líneas), aceptada deliberadamente para no tocar
ficheros de la Feature 003 ya validada (FR-033). Esta duplicación **MUST NOT
proliferar**: si una Feature 005 necesitara un tercer resumen/purga con el mismo patrón,
ese sería el punto en el que extraer una función compartida parametrizada por el
conjunto de tablas a purgar/resumir (p. ej. `application/services/purge_service.py`
genérico) pasaría a estar justificado por *tres* usos reales, no por anticipación — la
refactorización se difiere explícitamente hasta ese momento (Principio XI: no
abstracción prematura), no se ejecuta en esta feature ni en la 003.

## 2. STT/TTS como adaptadores de interfaz, no agentes cognitivos

**Decision**: `TranscriptionPort` y `SpeechSynthesisPort` son interfaces (`Protocol`,
mismo patrón que `GenerationPort`) en `infrastructure/speech/`, **no** agentes
registrados en una `AgencyDefinition`. Ninguno de los dos decide, verifica, ni razona
sobre contenido — STT convierte audio en texto con metadatos observables (confianza,
segmentos); TTS reproduce literalmente un texto ya aprobado. Ninguna responsabilidad
cognitiva (interpretar, decidir, verificar) recae en ellos, así que no satisfacen la
definición de "agente" del Principio II — son infraestructura, igual que
`SentenceTransformerEmbeddingAdapter` (Feature 002) no es un agente.

```text
TranscriptionPort (Protocol):
  async def transcribe(audio: bytes, *, language: str) -> TranscriptionOutcome

TranscriptionOutcome:
  text: str
  segments: list[{text, start_ms, end_ms, confidence}]
  overall_confidence: float
  low_confidence: bool   # true si algún segmento cae bajo el umbral configurado

SpeechSynthesisPort (Protocol):
  async def synthesize(text: str, *, language: str) -> SynthesisOutcome

SynthesisOutcome:
  audio: bytes
  ok: bool
```

**Implementaciones** (exactamente una cada una para el MVP de esta feature, mismo
patrón "sin tercer adaptador" que `GenerationPort` — research.md §1 de la Feature 003):

- `FasterWhisperTranscriptionAdapter`: local, vía `faster-whisper`
  (`docs/ORAL-IA_SpecKit/11_plan_prompt.md`). Sin red.
- `PiperSpeechSynthesisAdapter`: local, vía Piper. Sin red.

Ambos son **completamente opcionales** — si `ORALIA_STT_MODEL`/`ORALIA_TTS_VOICE` no
están configurados, la actividad simplemente no puede habilitar voz (mismo patrón que
`ORALIA_OLLAMA_MODEL` sin configurar en la Feature 003: el sistema no falla, la
capacidad no se ofrece). No se introduce un tercer mecanismo de "fallback de voz" — el
fallback es siempre "vuelve a texto", ya cubierto por la degradación controlada genérica
de la Feature 001 (`execute_agency`/`SafeFallbackAgent`).

**Rationale**: cumple literalmente la instrucción del usuario ("STT y TTS son
modalidades de interfaz, no capacidades cognitivas independientes") y el Principio XI
(componentes de inferencia/síntesis detrás de interfaces reemplazables).

## 3. Audio efímero

**Decision**: el audio capturado vive **exclusivamente** en memoria de proceso durante
la llamada a `TranscriptionPort.transcribe()` — nunca se escribe a disco, nunca entra en
`CognitiveState`, nunca se adjunta a un `TraceEvent`, nunca se reutiliza tras esa
llamada. El endpoint que recibe el audio lo pasa directamente al adaptador y descarta la
referencia inmediatamente después (éxito o fallo) — no hay tabla, columna ni directorio
de almacenamiento temporal recuperable para audio en esta feature.

**Ante fallo técnico de transcripción** (research.md, aclarado explícitamente):
`audio descartado (ya ocurrió, no hay nada que "descartar" adicionalmente porque nunca
se persistió) → TraceEvent de incidencia técnica (`event_type=transcription_failed`) →
degradación a entrada textual en el mismo turno`, sin ningún reintento sobre ese mismo
audio (spec.md, Clarifications). Si el estudiante quiere volver a intentar por voz, es
una **nueva** captura de audio, no un reintento sobre la anterior.

**Rationale**: cumple FR-011/FR-011a literalmente y el Principio VII ("el audio se
procesa y descarta; no se conserva por defecto"). No introducir almacenamiento temporal
recuperable elimina por construcción cualquier superficie de fuga de audio, sin
necesidad de una política de expiración adicional que vigilar.

## 4. Transcripción provisional y definitiva

**Decision**: modelo explícito de dos entidades (domain_model.md ya las anticipa):

```text
audio (efímero, nunca persistido)
  → Transcript (provisional — texto + segmentos + confianza, almacenado mientras dure la sesión — ver nota de persistencia operativa vs. conservación más abajo)
  → [revisión del estudiante]
  → TranscriptCorrection (opcional — solo si el estudiante edita algo)
  → transcripción definitiva = TranscriptCorrection.corrected_text si existe, si no Transcript.raw_text
  → procesamiento cognitivo (CognitiveState, recuperación, generación, repregunta, decisión de diálogo)
```

Si el estudiante **confirma sin modificar nada**, no se crea ninguna fila
`TranscriptCorrection` — el propio `Transcript.raw_text` pasa a ser la versión
definitiva directamente (spec.md, Clarifications: "esa misma versión pasa a ser
definitiva"). Esto evita una fila redundante idéntica al original y mantiene el modelo
mínimo (Principio XI).

**Persistencia operativa de sesión vs. conservación posterior al cierre** (aclarado
explícitamente tras revisión de consistencia, 2026-09-02 — ver §15 para el modelo
completo de consentimiento): que `Transcript`/`TranscriptCorrection` se guarden en la
base de datos **mientras la sesión está en curso** es una necesidad puramente operativa
— el estudiante debe poder revisar la transcripción completa antes del cierre (FR-020),
y el compositor necesita leer la transcripción definitiva de turnos anteriores para
construir el turno siguiente. Esta persistencia operativa **MUST NOT** interpretarse
como "conservación" en el sentido de FR-028/FR-031 (Principio VII) ni como si implicara
consentimiento alguno — es el mismo tipo de almacenamiento transitorio-durante-la-sesión
que ya usan `Turn.input_text`/`Turn.output_text` (Feature 001, sin cambios) para
cualquier sesión, de autoestudio o de defensa. **Al cerrar la sesión**: si no existe
`ConsentRecord` con `decision="retain"` (porque la actividad no autoriza conservación, o
porque el estudiante eligió `"delete"`), `Transcript`/`TranscriptCorrection` de esa
sesión **MUST** eliminarse en el mismo cierre — no permanecen "por defecto" solo porque
existieron durante la sesión (§15).

**Único punto de verdad para todo lo posterior**: `CognitiveState`, `MaterialRetrieverAgent`,
`FollowUpQuestionAgent`/`ResponseGeneratorAgent`/`PracticeQuestionAgent`, y la decisión
de diálogo **MUST** usar exclusivamente la transcripción definitiva — nunca
`Transcript.raw_text` directamente cuando existe una `TranscriptCorrection`. El
compositor de la agencia de defensa resuelve esto en un único punto (`definitive_text =
correction.corrected_text if correction else transcript.raw_text`) antes de construir
cualquier `AgentRequest`.

**Traza** (research.md, aclarado explícitamente): cada turno de entrada por voz registra
un `TraceEvent transcription_recorded` con `{transcript_id, overall_confidence,
low_confidence_segment_count}`, y — solo si hubo corrección — un
`TraceEvent transcript_corrected` con `{transcript_id, correction_id}`. Ninguno de los
dos incluye el audio ni una referencia a él.

**Rationale**: cumple FR-006/FR-009/FR-010 y evita que una corrección tardía reescriba
silenciosamente una repregunta ya mostrada (Edge Cases: la corrección aplica desde ese
punto en adelante, nunca retroactivamente — porque la repregunta ya persistida referenció
la transcripción definitiva vigente **en el momento en que se generó**).

## 5. Baja confianza STT — comportamiento exacto

**Decision** (spec.md, Clarifications — Q1): cuando `TranscriptionOutcome.low_confidence`
es verdadero, el compositor de defensa:

1. Muestra `Transcript.raw_text` con los segmentos de baja confianza señalados
   (`segments[].confidence` bajo `ORALIA_STT_LOW_CONFIDENCE_THRESHOLD`, configurable,
   default 0.6 — mismo patrón de umbral configurable ya usado en `_DISCLOSURE_OVERLAP_THRESHOLD`
   de la Feature 003).
2. Ofrece corregir el texto de esos segmentos.
3. Ofrece continuar respondiendo por texto desde ese punto (no solo para ese turno —
   cambia la modalidad de entrada del resto de la sesión si el estudiante lo elige).
4. **MUST NOT** ofrecer repetir la grabación de audio.
5. **MUST NOT** enviar la respuesta al pipeline cognitivo (recuperación/generación de
   repregunta) hasta que el estudiante confirme o corrija — el turno permanece en un
   estado `awaiting_confirmation` observable, no se genera ninguna repregunta todavía.

Este comportamiento es una incidencia de **modalidad** — se registra en la traza
(`transcription_recorded.low_confidence_segment_count > 0`) exactamente igual que
cualquier otra incidencia técnica, nunca como una observación sobre el estudiante
(FR-027, Principio I).

**Distinción explícita, corregida tras revisión de consistencia (2026-09-02)**: baja
confianza de STT **no es** `DialogueAction.clarify` y **no es** una decisión de
`DefenseAgency` — es un estado de la capa de captura/transcripción, anterior y externo a
cualquier turno cognitivo. Mientras el turno está en `awaiting_confirmation`:
`DefenseAgency` **MUST NOT** ejecutarse en absoluto — ni `MaterialRetrieverAgent`, ni
`GenerationPort`, ni `FollowUpQuestionAgent`, ni `GroundingVerifierAgent`, ni
`CoherenceVerifierAgent`, ni ninguna decisión de `DialogueAction`. El endpoint de
transcripción (`contracts/api-oral-defense.md`) no devuelve ni implica ningún
`dialogue_action` — solo campos de transcripción (`transcript_id`, `segments`,
`low_confidence`). La agencia cognitiva **solo** arranca tras
`POST /voice/confirm` (confirmación o corrección), con la transcripción ya definitiva
como si fuera una entrada de texto ordinaria (§6). `DialogueAction.clarify` queda
reservado exclusivamente para una ambigüedad **semántica** detectada por la propia
`DefenseAgency` sobre una respuesta **ya definitiva** — ver §9/§10, tabla corregida.

**Rationale**: cumple FR-022/FR-022a literalmente; reutiliza el patrón ya establecido en
la Feature 003 de "no generar contenido sobre una base insuficiente" (Nivel 0,
research.md §2 de la Feature 003) aplicado aquí a la modalidad de entrada en vez de a la
evidencia documental. Mantener la incidencia de modalidad completamente fuera de
`DialogueAction` preserva el Principio IV (separación de responsabilidades) y evita que
una métrica de reconocimiento de voz (una propiedad del adaptador STT) se confunda con
una métrica de calidad del razonamiento del estudiante (Principio I, Assumptions de
spec.md: "confianza de transcripción... no significa confianza en la capacidad del
estudiante", `14_domain_model.md`).

## 6. Equivalencia cognitiva texto/voz — una única `DefenseAgency`

**Decision**: existe **una sola** composición de agencia de defensa
(`defense_agency_composer.py`, análogo estructural a `self_study_agency_composer.py`).
La modalidad de entrada solo decide **qué pasos adicionales, anteriores al pipeline
cognitivo,** se ejecutan:

```text
texto  → [pipeline cognitivo común]
voz    → STT → Transcript → [revisión/corrección] → transcripción definitiva → [pipeline cognitivo común]
```

Una vez obtenida la entrada textual definitiva (directamente si es texto, tras
confirmación si es voz), el resto del turno — recuperación, generación de repregunta,
verificación de fundamentación/coherencia/constitucional, decisión de diálogo,
actualización de `CognitiveState`, persistencia de `Turn`/`GeneratedProposal`/
`DialogueAction` — es **exactamente el mismo código**, sin ninguna rama condicionada por
la modalidad de entrada original. La modalidad de salida (texto siempre; voz además si
`voice_output_allowed`) es igualmente un paso posterior y opcional (TTS, §7) sobre la
misma salida textual ya verificada.

**Rationale**: cumple FR-001/FR-003 literalmente ("no crear arquitectura paralela"); es
la aplicación directa a esta feature del mismo principio que ya demostró la Feature 003
(SC-001: cinco modos, una sola agencia) — aquí son dos modalidades de E/S, una sola
agencia.

## 7. Síntesis de voz — alcance y fallo

**Decision**: `SpeechSynthesisPort.synthesize()` **solo** se invoca sobre el
`output_text` final del turno, **después** de que haya superado fundamentación,
coherencia y control constitucional — nunca sobre un `GeneratedProposal` todavía no
verificado. TTS no recibe evidencia, conceptos, ni ningún contexto adicional — únicamente
la cadena de texto ya aprobada, y **MUST** reproducirla literalmente (FR-023): ningún
adaptador de síntesis puede resumir, ampliar, suavizar, enriquecer ni regenerar.

Si `synthesize()` falla (excepción, timeout vía el mismo `run_with_deadline` de la
Feature 001) o `SynthesisOutcome.ok` es falso: el turno se completa igual, la respuesta
textual ya calculada permanece disponible sin cambios, se registra
`TraceEvent tts_failed`, y el turno **no** se marca como degradado (`Turn.status`
permanece `"completed"`) — a diferencia de un fallo de generación de texto, un fallo de
TTS nunca degrada el contenido del turno, solo su modalidad de presentación (FR-024).

**Rationale**: cumple FR-023/FR-024 y el Principio IX aplicado estrictamente a una
capacidad puramente de presentación — su fallo nunca debe propagarse como si fuera un
fallo del pipeline cognitivo.

## 8. Pregunta inicial, repregunta y aclaración — qué agente genera cada una

**Decision**:

| Tipo | Cuándo | Agente | Contrato clave |
|---|---|---|---|
| Pregunta inicial | Primer turno de la sesión | Si `DefenseActivityConfig.initial_questions` no está vacío: se selecciona una entrada del banco (sin generación). Si está vacío: **`PracticeQuestionAgent` (Feature 003, sin cambios)**, con `objective_ref`/`concepts`/`evidence` de la actividad y `previous_questions=[]` | Reutilizado literalmente — ya produce `question_text` a partir de objetivo/conceptos/evidencia (§1) |
| Repregunta | Tras cada respuesta del estudiante (definitiva) | **`FollowUpQuestionAgent` (nuevo)** | Recibe la pregunta previa, la respuesta definitiva del estudiante, los conceptos mencionados, `concepts_addressed`/`concepts_pending`, evidencia recuperada para esa respuesta, y el objetivo — nunca genera valoración/scoring/diagnóstico (§9) |
| Aclaración cognitiva | Texto definitivo sin conceptos reconocibles o contradicción cognitiva (FR-018b) | Plantilla fija del compositor, sometida a T090 | La baja confianza STT solo activa revisión previa a la cognición, nunca esta acción |

**Por qué `FollowUpQuestionAgent` sí está justificado** (a diferencia de reutilizar
`PracticeQuestionAgent` para todo): el contrato de `PracticeQuestionAgent` no acepta "la
respuesta real del estudiante a la pregunta anterior" como entrada — genera preguntas a
partir de objetivo/conceptos/historial de *preguntas ya formuladas*, no en función de lo
que el estudiante respondió. Una repregunta, por definición (spec.md), **debe**
depender estructuralmente de esa respuesta concreta. Forzar `PracticeQuestionAgent` a
aceptar un campo nuevo (`student_answer`) sería modificar un contrato de la Feature 003
ya validado — exactamente lo que FR-033 prohíbe. Un agente nuevo con un contrato propio,
que internamente delega en el mismo `GenerationPort` (§1), es la solución que respeta
tanto "no reimplementar" como "no modificar lo ya validado".

```text
FollowUpQuestionAgent (nuevo, rol `generator`):
  input:
    previous_question_text: string
    student_answer_text: string          # transcripción definitiva o texto directo
    concepts_mentioned: string[]          # extraídos de la respuesta (FR-012)
    concepts_addressed: string[]          # CognitiveState
    concepts_pending: string[]            # CognitiveState
    evidence: EvidenceItem[]              # de MaterialRetrieverAgent sobre la respuesta
    objective: string
    purpose: "deepen_current_topic" | "switch_topic"   # decidido por el compositor, no por este agente (§10)
  output:
    question_text: string
    followup_type: "justificacion" | "ejemplo" | "comparacion" | "decision_tecnica" | "explicacion_error" | "profundizacion"
    referenced_concept: string            # concepto que motiva la repregunta — trazabilidad (§9)
    generation_trace: { adapter, model, fallback_used }
```

**Rationale**: responde directamente al punto 5/8/9 del encargo — un agente nuevo *solo*
donde la responsabilidad es genuinamente distinta, delegando en la misma infraestructura
de generación para no duplicar nada por debajo del contrato.

**Confirmación explícita de invariantes** (revisión de consistencia, 2026-09-02):

- `FollowUpQuestionAgent` **solo** se invoca una vez existe `student_answer_text` como
  transcripción **definitiva** (§4) o texto directo — nunca durante
  `awaiting_confirmation` (§5). El compositor no lo registra siquiera como paso de la
  `AgencyDefinition` de ese turno hasta ese punto.
- `student_answer_text` (y, por extensión, `previous_question_text`) se pasan siempre
  como **datos** dentro de `GenerationRequest.evidence`/mensaje `user` — nunca
  interpolados en la instrucción `system` fija del agente — mismo tratamiento de
  frontera dato/instrucción ya exigido para el texto de materiales (FR-008b de la
  Feature 003, research.md §3 de la Feature 003, reutilizado sin cambios): la respuesta
  del estudiante tampoco puede alterar el comportamiento del sistema.
- Delega en el mismo `GenerationPort` (§1) — sin un tercer adaptador de generación.
- Toda propuesta pasa por `GroundingVerifierAgent` + `CoherenceVerifierAgent` +
  la puerta final T090, que integra `ConstitutionalControl` con snapshot confiable,
  catálogo y persistencia, antes de mostrarse — el generador
  **nunca** aprueba su propia salida (Principio IV).
- No evalúa la respuesta del estudiante — no produce ni recibe ningún campo de
  valoración; su única salida sobre la respuesta es estructural (`concepts_mentioned`,
  `referenced_concept`), nunca un juicio de calidad.
- `purpose` (`deepen_current_topic`/`switch_topic`) diferencia estructuralmente el
  propósito de la repregunta — el agente lo recibe como parámetro, no lo infiere.
- La decisión final de diálogo (`ask`, `clarify`, `acknowledge_missing_info`, `finish`)
  la toma el **compositor** (`defense_agency_composer.py`), combinando el veredicto de
  los verificadores — nunca el propio `FollowUpQuestionAgent` de forma unilateral
  (Principio IV: generador ≠ decisor).

## 9. Relevancia y no repetición de repregunta — criterio verificable sin comparación literal

**Decision**: la verificación de relevancia/no-repetición combina, igual que la Feature
003 combina fundamentación+coherencia (research.md §5 de la Feature 003):

1. **Fundamentación** (`GroundingVerifierAgent`, sin cambios): la repregunta generada se
   verifica contra la evidencia recuperada para la respuesta del estudiante — igual
   mecanismo que ya usa `self_study_agency_composer.py`.
2. **Repetición** (`CoherenceVerifierAgent`, sin cambios): compara la repregunta contra
   la pregunta/repregunta inmediatamente anterior de la misma sesión — mismo umbral y
   técnica ya validados, sin comparar contra todo el historial.
3. **Relevancia estructural** (nuevo, determinista, en `defense_agency_composer.py`):
   `FollowUpQuestionAgent.output.referenced_concept` **MUST** pertenecer a
   `concepts_mentioned` (extraídos de la respuesta) o a los materiales recuperados para
   ese turno.

**Mapeo corregido de fallos de fundamentación/relevancia a `dialogue_action`** (alineado
con la corrección de §5/§10 — ninguno de estos casos es `clarify`, que queda reservado a
ambigüedad semántica de la respuesta del estudiante, no a un fallo de la repregunta
generada):

- `referenced_concept` no satisfecho, o `GroundingVerifierAgent` no fundamenta la
  repregunta contra la evidencia disponible → **`acknowledge_missing_info`** (mismo
  tratamiento que el veredicto `no_fundamentada`/Nivel 0 de la Feature 003 — no hay
  fundamento suficiente para continuar por esa vía, se reconoce en vez de mostrar una
  repregunta sin respaldo).
- `CoherenceVerifierAgent` detecta repetición literal de la repregunta anterior →
  reintenta la generación (mismo patrón acotado de regeneración ya usado en
  `PracticeQuestionAgent`/`SolutionNonDisclosureVerifierAgent`, Feature 003, research.md
  §4 de la Feature 003) antes de recurrir a `acknowledge_missing_info` si se agotan los
  intentos.

**`DialogueAction.clarify` — disparador cognitivo real** (distinto de todo lo anterior):
se dispara cuando la **respuesta definitiva del estudiante** (no la repregunta generada)
no aporta significado suficiente para decidir el siguiente paso — concretamente, cuando
`concepts_mentioned` (extraídos de esa respuesta) resulta vacío o
`CoherenceVerifierAgent`, aplicado sobre la respuesta definitiva del estudiante frente a
su propia afirmación previa en la misma sesión, detecta una contradicción (mismo agente,
mismo contrato, aplicado al texto del estudiante en vez de a una propuesta del sistema —
sin modificar `CoherenceVerifierAgent`). Es una decisión cognitiva de `DefenseAgency`
sobre contenido ya textual y definitivo — nunca sobre una propiedad de reconocimiento de
voz (§5).

**Rationale**: cumple SC-005 sin introducir un cuarto verificador — reutiliza
exactamente los dos ya existentes (fundamentación + coherencia) más una comprobación
estructural trivial ya expresable con el propio contrato del agente nuevo. La separación
entre "repregunta no fundamentada" (`acknowledge_missing_info`) y "respuesta del
estudiante ambigua" (`clarify`) evita que ambas situaciones, semánticamente distintas,
compartan una misma acción de diálogo.

## 10. Política de diálogo — reutilización de `DialogueAction`

**Decision** (spec.md, Clarifications — Q4): se reutilizan las acciones de
`DialogueAction` ya usadas en la Feature 003 sin ampliar el conjunto:

| Situación de defensa | `dialogue_action` reutilizado |
|---|---|
| Presentar la pregunta inicial | `ask` |
| Profundizar en el mismo tema (repregunta sobre el mismo concepto) | `ask` con metadata `purpose=deepen_current_topic` |
| Cambiar a un tema distinto dentro del alcance autorizado | `ask` con metadata `purpose=switch_topic` |
| La respuesta definitiva del estudiante es semánticamente ambigua/insuficiente para decidir el siguiente paso (§9, disparador cognitivo) | `clarify` |
| No puede fundamentarse una repregunta relevante contra la evidencia disponible (§9) | `acknowledge_missing_info` |
| Fin de sesión (límite alcanzado o voluntario) | `finish` |

**Explícitamente fuera de `DialogueAction`**: la baja confianza de transcripción (§5) y
cualquier otro estado técnico de STT/TTS (fallo de captura, fallo de síntesis) **MUST
NOT** representarse mediante ningún valor de `DialogueAction` — son estados de la capa
de modalidad, observables únicamente a través de los campos de la respuesta de
transcripción y de los `TraceEvent` técnicos dedicados (`transcription_recorded`,
`transcription_failed`, `tts_failed` — data-model.md). Un turno en
`awaiting_confirmation` no tiene todavía ningún `DialogueAction` asociado, porque
`DefenseAgency` aún no se ha ejecutado sobre él (§5).

No se introduce `change_topic`, `re_ask` se considera ya cubierto por `ask` (una
repregunta **es** un nuevo `ask`, distinguible por su metadata, no por su
`dialogue_action`), y `follow_up` no se introduce como acción propia por el mismo
motivo. La metadata estructurada (`purpose`, concepto origen/destino, razón, evidencia
referenciada) se registra en el `TraceEvent followup_question_generated` (§17), no en
`DialogueAction.action_type` — evita ampliar un enum compartido con la Feature 003 para
información que ya tiene un lugar propio en la traza.

**Rationale**: cumple literalmente "no amplíes el enum salvo imposibilidad
demostrada" — no hay imposibilidad: toda la información necesaria (incluida la
distinción profundizar/cambiar de tema) es representable sin un valor nuevo.

## 11. `CognitiveState` — cero campos nuevos

**Decision**: los siete conceptos que la agencia de defensa necesita conocer
estructuralmente (pregunta actual, respuesta definitiva del estudiante, conceptos
tratados, conceptos pendientes, número de preguntas/repreguntas, objetivo actual,
siguiente acción) mapean **directamente** sobre `MINIMUM_FIELDS` ya existente (Feature
001, sin ampliar el esquema — mismo principio ya aplicado por la Feature 003 con
`concepts_pending`/`mode`):

| Concepto de defensa | Campo de `CognitiveState` reutilizado |
|---|---|
| Pregunta/repregunta actual mostrada al estudiante | `participant_response` (ya se usa así en la Feature 003: pese al nombre, almacena la última salida **del sistema**, no del participante) |
| Respuesta definitiva del estudiante | `current_input` |
| Conceptos ya tratados | `concepts_addressed` |
| Conceptos pendientes (temas del banco/materiales aún no cubiertos) | `concepts_pending` |
| Número de preguntas/repreguntas realizadas | `turn_number` (1 turno = 1 ciclo pregunta→respuesta) |
| Objetivo de la actividad | `objective` |
| Siguiente acción decidida | `next_action_proposed` |

No se persiste ningún dato de audio ni de transcripción en `CognitiveState` — esa
información vive en `Transcript`/`TranscriptCorrection` (§4) y en la traza (§17),
consistente con "no conviertas `TraceEvent` en estado operativo" leído en sentido
inverso: tampoco el estado operativo debe cargar con lo que ya es responsabilidad de la
traza/persistencia dedicada.

**Rationale**: cumple literalmente el encargo ("define qué campos existentes pueden
reutilizarse y qué extensiones mínimas son necesarias") con el resultado más fuerte
posible — extensión mínima necesaria: ninguna.

## 12. `DefenseActivityConfig`

**Decision**: mismo patrón que `SelfStudyActivityConfig` (Feature 003) — 1:1 con
`ActivityConfiguration`, creable/actualizable solo mientras
`ActivityConfiguration.immutable_since` es `null` (research.md §7 de la Feature 003,
reutilizado sin cambios). Reutiliza directamente de `ActivityConfiguration` (sin
duplicar): `max_turns`, `max_duration_seconds`, `language`, `general_knowledge_allowed`,
`retention_policy_id`, materiales autorizados (vía la relación ya existente de
`MaterialDocument.activity_configuration_ids`). Campos propios, genuinamente nuevos:

```text
DefenseActivityConfig:
  id, activity_configuration_id (FK, unique)
  initial_questions: string[]        # banco docente; vacío ⇒ generar desde materiales (§8)
  difficulty_hint: "baja"|"media"|"alta"   # orientativa, default "media" — mismo vocabulario que PracticeQuestion
  voice_input_allowed: bool          # default false
  voice_output_allowed: bool         # default false
  summary_authorized: bool           # default false — mismo patrón que SelfStudyActivityConfig
  transcript_retention_authorized: bool   # default false — habilita la opción de conservar al cierre (§15)
```

**Validación** (FR-002a): `initial_questions` vacío **y** sin materiales autorizados
asociados a la actividad ⇒ configuración inválida, rechazada antes de permitir iniciar
sesión — mismo patrón de rechazo que `enabled_modes` vacío en la Feature 003.

## 13. Límites de sesión

**Decision**: se reutiliza **directamente** `ActivityConfiguration.max_turns`/
`max_duration_seconds` (Feature 001, sin cambios) — no se introduce un contador
"máximo de preguntas/repreguntas" separado, porque en este modelo 1 turno = 1 ciclo
pregunta/repregunta→respuesta, exactamente como ya vale para autoestudio. El mismo
patrón de auto-cierre de `submit_study_turn.py` (Feature 003 — comprobación de
límite tras cada turno, cierre si se alcanza) se replica en el propio comando de envío
de turno de defensa. Finalización voluntaria vs. automática se distingue únicamente por
el `status` con el que se cierra la sesión (`closed_voluntary` vs.
`closed_limit_reached`, mismos valores ya usados en Features 001/003) — no hace falta
ninguna distinción adicional.

## 14. Resumen — reutilización directa del patrón de la Feature 003

**Decision**: `defense_session_summary_service.generate_defense_summary(db, session)` —
fichero nuevo, mismo patrón exacto que `study_session_summary_service.py` (construcción
determinista de un `dict` a partir de hechos ya persistidos, nunca generado por LLM,
registrado como `TraceEvent event_type=defense_session_summary`, entregado una única vez
en la respuesta de cierre — FR-021 de la Feature 003, reaplicado aquí). Contenido:
`turn_count`, `duration_seconds`, `questions_asked` (texto de cada pregunta/repregunta,
tomado de `GeneratedProposal`), `topics_covered`/`concepts_mentioned`
(`concepts_addressed` final), `sources_consulted_fragment_ids`, `clarifications_count`,
`incidents` (`{incident_type, recovery_action}` — mismo formato que `CoherenceIncident`
de la Feature 003, incluye incidencias técnicas de voz como `transcription_failed`/
`tts_failed`). Ningún campo de nota/puntuación/nivel/competencia/rendimiento/capacidad
(FR-029/FR-029a) — el propio diseño determinista lo garantiza por construcción, igual
que en la Feature 003.

## 15. Consentimiento y retención

**Decision**: `ConsentRecord` (domain_model.md ya lo anticipa) — tabla nueva, mínima:

```text
ConsentRecord:
  id, session_id (FK, unique)
  decision: "retain" | "delete"
  scope: string[]        # p. ej. ["transcript", "summary"] — qué se conserva si decision=retain
  recorded_at
```

Se registra **una única vez**, al cierre de la sesión (US7/FR-030), solo si
`DefenseActivityConfig.transcript_retention_authorized` es verdadero — si es falso, no
hay decisión que tomar: nada se conserva más allá del cierre, igual que el
comportamiento por defecto de la Feature 003 (FR-031, hereda `RetentionPolicy` de la
Feature 001 sin sistema paralelo). Si `decision=delete`, el compositor elimina
inmediatamente `Transcript`/`TranscriptCorrection` de esa sesión (no espera a la purga
diferida). Si `decision=retain`, esos datos quedan sujetos a la misma
`RetentionPolicy.retention_days` ya usada por la actividad — un comando nuevo,
`purge_expired_defense_data` (fichero propio, mismo patrón que
`purge_expired_self_study_data.py` de la Feature 003, sin generalizar ni tocar ese
fichero — §1), los purga cuando expiran. Invocación manual, sin scheduler (mismo límite
ya fijado por la Feature 003, Principio VI).

**Regla de cierre unificada** (corrige/precisa la lógica anterior): en el momento del
cierre, para cada dato sujeto a consentimiento (`Transcript`, `TranscriptCorrection`, el
`TraceEvent defense_session_summary`):

- Si la actividad **no** autoriza conservación (`transcript_retention_authorized=false`)
  **o** el participante elige `decision="delete"` → se elimina **inmediatamente** en el
  propio cierre, sin esperar a `purge_expired_defense_data`.
- Si la actividad autoriza conservación **y** el participante elige `decision="retain"`
  → permanece, acotado por `scope` (p. ej. `["transcript"]` sin `"summary"`, o ambos), y
  queda sujeto a `RetentionPolicy.retention_days` hasta que expire y
  `purge_expired_defense_data` lo elimine.

**`ConsentRecord` no es un permiso para procesar la sesión** (aclarado explícitamente):
`ConsentRecord` **MUST NOT** interpretarse como una condición para que el estudiante
pueda interactuar con la agencia de defensa — el disclosure inicial (FR-004) ya cubre el
consentimiento para **participar**, igual que en las Features 001/003, y ninguna sesión
requiere una fila `ConsentRecord` para completarse con normalidad. `ConsentRecord`
únicamente registra la decisión, tomada **al cierre**, sobre si los datos ya generados
durante la sesión (que existieron por necesidad puramente operativa, §4) se conservan o
se eliminan **después** de ese cierre. Sin `transcript_retention_authorized`, esta
distinción es moot: no hay nada que decidir, y el resultado es idéntico al de la Feature
003 (nada se conserva).

**Nota sobre `scope=["summary"]`**: conservar el `TraceEvent defense_session_summary`
más allá del cierre habilita su reconstrucción posterior **únicamente** vía
`GET /defense-trace` (área técnica, FR-021 ya establece que el resumen no tiene vía de
consulta para el propio participante) — no reabre ni reintroduce la "visualización única
y efímera" que FR-021 exige para el estudiante; esa regla no cambia independientemente
de `scope`.

**Distinción explícita**: "consentir participar" (disclosure inicial, FR-004 — mismo
patrón de banner ya usado en Features 001/003, no requiere una fila nueva, es
información mostrada antes del primer turno) es un momento distinto de "consentir
conservar" (`ConsentRecord`, al cierre) — ambos existen, ninguno sustituye al otro.

**No se construye en esta feature** (alcance explícitamente excluido, FR-034): panel
avanzado de privacidad, automatización de purga (scheduler), infraestructura
longitudinal de ningún tipo.

## 16. Despliegue local

Sin cambios respecto al patrón ya establecido: monolito modular único, mismo proceso
FastAPI, SQLite/WAL. `faster-whisper`/Piper son dependencias opcionales — sin
`ORALIA_STT_MODEL`/`ORALIA_TTS_VOICE` configurados, la actividad no puede habilitar voz
(la modalidad textual sigue disponible sin ninguna dependencia adicional, FR-003/FR-036).
Sin microservicios, sin colas, sin Kubernetes, sin servicio cloud obligatorio, sin
robot/vídeo (FR-034).

## 17. Trazabilidad — cadena completa reconstruible

**Decision**: extiende `reconstruct_session_trace` (Feature 001, genérico por
`event_type`, sin cambios) con los `event_type` nuevos de esta feature:
`transcription_recorded`, `transcript_corrected`, `transcription_failed`,
`followup_question_generated` (payload: `purpose`, concepto origen/destino, razón,
`evidence_fragment_ids`), `tts_failed`, `defense_session_summary`,
`consent_recorded`. Junto con los ya reutilizados sin cambios de la Feature
001/003 (`agent_execution`, `generation_call`, `verification_combined`,
`agents_selected`, `turn_completed`, `session_closed`), permite reconstruir la cadena
completa exigida: `pregunta → modalidad de entrada → STT si procede → transcripción
provisional → confianza/segmentos dudosos → corrección/confirmación → transcripción
definitiva → actualización de CognitiveState → recuperación → agentes activados y razón
→ generación → verificadores → decisión de diálogo → repregunta/aclaración/nueva
pregunta/finalización → TTS si procede → resultado final del turno`. Nunca se registra
audio, y la traza sigue siendo **copia de auditoría**, no fuente de verdad —
`CognitiveState` decide, la traza documenta lo ya decidido (mismo principio que
research.md §6 de la Feature 003).

## 18. Pruebas — preparación para `/speckit-tasks`

Deterministas por defecto (sin modelos STT/TTS reales): un `FakeTranscriptionAdapter`/
`FakeSpeechSynthesisAdapter` de pruebas (mismo patrón que
`DeterministicGenerationAdapter` sirve de reserva determinista en producción, aquí sirve
como doble determinista en tests) permite probar todo el flujo de voz sin `faster-whisper`/
Piper instalados. Pruebas reales con los modelos locales quedan en un marcador `speech`
propio (mismo patrón que el marcador `ollama` de la Feature 003 — opcional, omitido por
defecto, requiere `ORALIA_STT_MODEL`/`ORALIA_TTS_VOICE`).

**Cuatro situaciones que `/speckit-tasks` MUST tratar como pruebas distintas**
(no intercambiables — revisión de consistencia, 2026-09-02), directamente derivadas de
la corrección de §5/§9/§10:

- **(A) STT baja confianza**: `POST /voice` con confianza baja → la respuesta no
  contiene ningún `dialogue_action`; ningún `TraceEvent` de `agent_execution`/
  `generation_call`/`verification_combined` se registra para ese turno todavía; el
  estudiante corrige o cambia a texto; solo tras `POST /voice/confirm` arranca
  `DefenseAgency` (se registran esos eventos recién entonces).
- **(B) STT confianza suficiente**: `POST /voice` con confianza alta →
  `low_confidence=false`; `POST /voice/confirm` sin `corrected_text` avanza
  inmediatamente usando `raw_text` como definitiva, sin fila `TranscriptCorrection`.
- **(C) Respuesta textual definitiva semánticamente ambigua**: texto directo (o voz ya
  confirmada) cuyo contenido no permite extraer `concepts_mentioned`, o que
  `CoherenceVerifierAgent` marca como contradictorio frente a una afirmación previa del
  propio estudiante en la sesión → `DefenseAgency` selecciona `dialogue_action=clarify`
  — con `agent_execution`/`verification_combined` sí registrados (a diferencia de (A),
  aquí la agencia **sí** se ejecutó).
- **(D) Fallo técnico de STT**: `TranscriptionPort.transcribe()` devuelve `ok=false` →
  `TraceEvent transcription_failed` registrado; ningún componente cognitivo procesa el
  intento fallido (ni `MaterialRetrieverAgent`, ni `GenerationPort`, ni
  `FollowUpQuestionAgent`); el turno degrada a entrada textual disponible para un nuevo
  intento, sin reintento sobre el audio ya descartado (§3).

Estas cuatro pruebas MUST verificar explícitamente, vía `defense-trace`, qué conjunto de
`event_type` se registró (o no) en cada caso — la ausencia de eventos cognitivos en (A)
y (D) es una aserción tan importante como la presencia de `clarify` en (C).

## 19. Integración obligatoria con la puerta final T090

**Decisión**: la verificación heredada no se reduce a buscar expresiones H02. Cada texto
que pueda llegar al participante usa el flujo estructurado completo de Feature 001:
entrada exacta de `OutputTemplateCatalog`, bindings con cobertura total,
`OutputProposal`, `AuthorizationSnapshot` construido en el límite confiable y
`final_output_gate`. Esto incluye banco inicial, generación normal, repregunta,
`clarify`, falta de evidencia, degradación, cierre y resumen visible.

La identidad de ejecución (`session_id`, configuración de actividad y destinatario), la
política canónica y las referencias autorizadas proceden de filas/contratos confiables.
El generador no puede aportar ni ampliar autoridad. `GeneratedProposal` saneada,
`VerificationResult.authorization_context`, `Turn` y trazas finales se escriben en una
transacción dirigida por el límite exterior. La puerta no hace commit ni cierra sesión.

Un bloqueo persiste `output_text=NULL` y nunca copia el candidato a mensajes internos,
trazas, errores o API. Puede existir un solo intento operativo catalogado (`attempt=1`),
que vuelve a atravesar la misma puerta con `message_type=operational`. Si falla, la
sesión finaliza `closed_error_safe` sin contenido. Esta decisión sustituye cualquier
redacción anterior que prometiera siempre un mensaje seguro visible.

## 20. Cierre concurrente mediante T150

**Decisión**: `end_defense_session` llama a `close_session_with_outcome`, no a una
secuencia local de lectura y cierre. `transition_won=True` es la única autorización para
crear o entregar el resumen, registrar consentimiento, aplicar retención/eliminación,
emitir eventos de cierre y liberar el bloqueo de sesión. Un llamante que pierde devuelve
el estado persistido y `defense_summary=null`; no regenera ni repite efectos.

Las escrituras del ganador comparten la transacción del cierre. Un fallo provoca rollback
de todo el conjunto; una repetición posterior puede ganar sin observar efectos parciales.
La matriz incluye doble llamada secuencial, carrera concurrente y fallo inyectado.

## 21. Ejecución bloqueante de STT/TTS

**Decisión**: Faster Whisper y Piper son llamadas bloqueantes y no se ejecutan sobre el
event loop ni mediante `asyncio.to_thread` sin límite. Un `BoundedBlockingWorker`
dedicado a voz adopta las garantías T086/T100 de Feature 002: ejecutor propio, capacidad
global al proceso, backpressure FIFO cancelable, liberación de permisos ante fallo de
submit y singleton protegido frente a carreras entre bucles.

El trabajo del thread nunca recibe una sesión SQLAlchemy. Devuelve únicamente un valor
de puerto. Tras timeout/cancelación, el coroutine marca el resultado como obsoleto y una
terminación tardía no puede persistir transcripción, audio, traza ni respuesta.

## 22. Audio multipart efímero y acotado

**Decisión**: máximo 10 MiB y 300 segundos por captura. El router consume `UploadFile`
en bloques con contador y rechaza con `413` al superar bytes. Valida WAV/WebM y duración;
formato inválido, duración indeterminable o más de 300 s devuelven `422`. STT no se
invoca en ningún rechazo.

Starlette puede volcar multipart a `SpooledTemporaryFile`; por ello «solo en memoria» no
es una garantía suficiente. El endpoint usa `try/finally` y cierra siempre el
`UploadFile`; las pruebas fuerzan rollover y comprueban que el descriptor está cerrado y
que no existe un artefacto temporal recuperable después de éxito, error, timeout o
cancelación. No se copia el audio a otro archivo nombrado y ningún identificador de
archivo llega a persistencia o trazas.

## 23. Contrato de entrega y replay de TTS

**Decisión**: TTS se expone como
`POST /defense-sessions/{session_id}/defense-turns/{turn_id}/speech`. La respuesta es
WAV binario (`audio/wav`) e incluye la huella UTF-8 del texto en
`X-ORALIA-Text-SHA256`. El endpoint vuelve a comprobar que el turno pertenece a la
sesión, tiene `output_text` y posee un veredicto final aprobado; sintetiza exactamente
ese texto persistido.

Replay significa volver a llamar al endpoint y regenerar, no recuperar audio almacenado.
Un turno sin texto aprobado devuelve `404`. Un fallo o timeout de Piper devuelve `503`;
el turno aprobado y su texto permanecen disponibles. El frontend revoca cada object URL
al reemplazarlo o desmontarse.

## 24. Dependencias locales y modelos

**Decisión**: dependencias opcionales acotadas a `faster-whisper>=1.2.1,<2` y
`piper-tts>=1.8,<2`. Faster Whisper se inicializa con un identificador o ruta local,
dispositivo y `compute_type` configurados, con descarga silenciosa deshabilitada en la
ruta normal: `WhisperModel(model_size_or_path, device=..., compute_type=...,
local_files_only=True)`; `transcribe` recibe un `BinaryIO`/array aceptado por la API y el
idioma. Piper usa `PiperVoice.load(<ruta .onnx>)` y `synthesize_wav(text,
wave.Wave_write)` sobre un buffer acotado. La ausencia de modelo/voz impide habilitar esa
modalidad, pero nunca impide el flujo textual.

Estas versiones reflejan las publicaciones vigentes al 2026-10-16. Los adaptadores
ocultan sus APIs; dominio, compositor y pruebas deterministas solo dependen de los
puertos propios.

## 25. Baseline y alcance de cambios aditivos

**Decisión**: el baseline de Features 001–003 es 608 pruebas deterministas aprobadas y
una prueba Ollama real aprobada al 2026-10-16; el número histórico 239 queda obsoleto.
Feature 004 puede extender de forma aditiva registro de router, propósitos de generación,
catálogo/plantillas, cliente y ruta web. La revisión final verifica ausencia de regresión
en comportamiento, no la condición imposible de que ningún archivo previo haya sido
modificado.

## 26. Cierre de las oleadas W1–W3 (2026-10-16)

La auditoría del código parcial encontró dos fisuras concretas y las cerró sin ampliar
el alcance a consentimiento/purga. Primero, la UI no solicitaba la pregunta inicial:
ahora inicia el pipeline con una entrada vacía, y el compositor selecciona una pregunta
de banco (o una pregunta determinista basada en material) y la somete a una identidad
de catálogo propia antes de mostrarla. El límite de turnos usa igualmente una plantilla
exacta y cierra mediante la transición compartida.

Segundo, el endpoint TTS comprobaba solamente `VerificationResult.verdict`; una mutación
posterior de `Turn.output_text` habría permitido sintetizar un texto distinto al que fue
aprobado. El endpoint exige ahora que el texto coincida exactamente con el contenido de
la `GeneratedProposal` final enlazada al turno antes de invocar Piper.

La evidencia de estas oleadas es: 34 pruebas focales Python, la matriz ampliada de
autorización/catálogo, build TypeScript, un Playwright real de `/defensa`, Ruff JSON sin
hallazgos en los archivos Python de W1–W3 y la regresión determinista completa con 647
pruebas aprobadas, una deseleccionada y el único warning heredado de Starlette/httpx.

## 27. Integración histórica y límites verificados (2026-10-17)

La pregunta inicial sin banco reutiliza ahora `PracticeQuestionAgent` con evidencia de
`MaterialRetrieverAgent`; se retiró la pregunta genérica que evitaba esa ruta. Las
repreguntas usan recuperación, grounding y coherencia independientes. La repetición
semántica se verifica contra la pregunta anterior y la duplicación literal se impide
en toda la sesión, también tras un cambio de tema, con una sola regeneración.

El supuesto de que el control constitucional anterior cubría toda caracterización
personal quedó refutado por pruebas negativas: no detectaba «tu nivel es alto» o
«eres competente». Se añadieron patrones acotados a afirmaciones personales en el
control existente, usando la razón contractual `academic_decision`; no se creó otro
verificador ni se relajó ninguna regla. Las menciones técnicas a capacidad de sistemas
siguen permitidas. Esta extensión aditiva se incluye expresamente en T093.

`participant_response` conserva la salida del sistema y `current_input` el texto
definitivo del participante, conforme a §11. Una aclaración pendiente no convierte la
afirmación ambigua en una premisa definitiva del siguiente turno. Una corrección
posterior a confirmación abre una nueva transcripción/turno; nunca modifica el registro
confirmado anterior.

El resumen se construye sin generación y atraviesa T090 con categoría
`defense_summary`, procedencia `persisted_session_facts` y scope
`activity/oral_defense_summary/respond`. Sin ese permiso explícito se entrega nulo.
La retirada por scope o caducidad borra también su texto de la propuesta auxiliar;
solo permanecen metadatos de autorización, sin los hechos del resumen.

Los endpoints de defensa y las fronteras HTTP compartidas de sesión, actividad,
materiales y autoestudio usan la salida de dependencia de DB
antes de enviar la respuesta. El recorrido HTTP real reprodujo que la salida al final
del request podía devolver el identificador antes del commit y causar un `404` en el
siguiente request. Se conserva una única transacción exterior y se comprueba su
rollback. `uv.lock` incorpora las cinco dependencias opcionales resueltas para voz;
ninguna se instala para ejecutar el flujo textual.

La prueba de fallo de commit (`test_defense_http_transaction_boundary.py`) reprodujo
un `201` incorrecto antes de la corrección y exige ahora `500`, sin identificador ni
fila persistida. La dependencia DB usa scope de función en los routers compartidos;
no cambia la forma de sus respuestas ni sus algoritmos. El presupuesto de cada agente
se limita además al tiempo restante de sesión, y la duración se comprueba de nuevo
antes de construir el candidato final para cerrar también si expira durante generación.


## 28. Conservación finita y copias operativas

La implementación verifica el plazo de retención al configurar y antes del cierre con
consentimiento. Un plazo ausente o negativo se rechaza; no se inventa un valor por defecto.
La eliminación no se limita a Transcript/TranscriptCorrection: retira también contenido
copiado en turnos, propuestas, estado, parches, mensajes y trazas de la misma sesión de
defensa terminal. Los metadatos de identidad, versión y autorización siguen auditables
mediante el mecanismo genérico y el evento adicional `defense_content_erased`.
No se modifica el esquema ni datos de otras sesiones o modos.

Dos pruebas de carrera cierran la sesión desde otra conexión mientras STT/TTS trabaja:
se refresca el recurso antes de aceptar el resultado para impedir recrear texto o entregar
audio de contenido eliminado. El frontend aborta síntesis al terminar. Evidencia:
`test_defense_retention_copies.py`, `test_defense_retention_requires_finite_policy.py`,
`test_defense_stt_after_close.py` y `test_defense_speech_endpoint.py`.

## Corrección de cierre automático y revisión completa (2026-10-17)

Los cuerpos de `POST /defense-turns` y `POST /defense-turns/voice/confirm` aceptan
`closure_consent: {retain: boolean, scope: ["transcript", "summary"]}`. La elección
explícita actual se valida antes del turno y se aplica si ese turno cierra por límite
o cierre seguro. No crea consentimiento anticipado, no cambia la política ni autoriza
conservar por defecto. El único ganador T150 escribe ConsentRecord y ejecuta los scopes;
una llamada repetida no puede cambiar la elección ni restaurar contenido eliminado.
La configuración debe autorizar retención y tener plazo finito no negativo.

`GET /api/v1/defense-sessions/{session_id}/defense-transcript` devuelve, con
`Cache-Control: no-store`, los turnos cronológicos y los originales/correcciones de
voz de esa sesión de defensa. No genera contenido ni agrega otras sesiones. Tras borrar
contenido devuelve listas vacías. La UI permite abrir esta revisión durante la sesión;
el cierre voluntario primero carga el registro completo y después requiere
«Confirmar cierre de sesión». Las selecciones de scope viajan tanto con respuestas de
texto como con confirmaciones de voz para respetarlas al alcanzar límites.

Evidencia: `tests/contract/test_defense_automatic_close_consent.py` (16 combinaciones de
turnos/duración × texto/voz × cuatro elecciones), y recorridos reales Playwright de
cierre voluntario, límite de turnos y duración, conservación selectiva, revisión,
repetición de cierre y purga del almacenamiento aislado de pruebas.
