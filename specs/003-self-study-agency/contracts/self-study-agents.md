# Contrato interno: agentes nuevos de la Feature 003 y `GenerationPort`

Regenerado tras el cierre de requisitos (Clarify, 2026-09-01) y la ronda de corrección
de consistencia arquitectónica (2026-09-02). Todos los agentes implementan el mismo
protocolo `Executable` ya definido en la Feature 001 — el sobre
(`AgentRequest`/`AgentResult`/`AgentError`/`CancellationToken`) no cambia.

## GenerationPort (interfaz, `infrastructure/generation/`) — dos implementaciones

```text
GenerationRequest:
  purpose: "explicacion" | "explicacion_progresiva" | "ejemplo" | "comparacion"
         | "estructura_exposicion" | "pregunta_practica" | "resumen"
  instruction: string            # plantilla fija en código — nunca contiene evidence[].text
  student_input: string = ""     # NUEVO (estabilización 2026-09-10, H01, research.md §13)
                                  # texto literal del turno actual — dato, nunca instrucción
                                  # (mismo principio que evidence[].text, research.md §3);
                                  # valor por defecto "" — no rompe construcciones existentes
                                  # de GenerationRequest (compatibilidad, research.md §13);
                                  # queda en "" cuando no aplica (p. ej. PracticeQuestionAgent,
                                  # que no responde a un texto del estudiante sino que genera una
                                  # pregunta nueva a partir de evidence/concepts)
  evidence: [ { fragment_id: UUID, text: string, document_id: UUID, document_version: int } ]
  concepts_addressed: string[]
  general_knowledge_allowed: bool
  constraints: { max_tokens: int, reveal_solution: bool }

GenerationOutcome:
  ok: bool
  text: string
  internal_expected_answer: string | null   # solo purpose="pregunta_practica" — nunca persistido
  adapter: "ollama" | "deterministic"
  model: string | null
  parameters: { temperature: float, max_tokens: int }
  latency_ms: int
```

**Implementaciones** (research.md §1 — exactamente dos, sin una tercera envoltorio):

- `OllamaGenerationAdapter`: primaria, HTTP local (`httpx`) contra un servidor Ollama.
  `timeout_ms` = 6000 por defecto (`ORALIA_OLLAMA_TIMEOUT_MS`), `temperature` = 0.2
  (`ORALIA_OLLAMA_TEMPERATURE`, `[0.0,1.0]`), `max_tokens` = 256
  (`ORALIA_OLLAMA_MAX_TOKENS`, `[64,512]`), sin modelo por defecto
  (`ORALIA_OLLAMA_MODEL` obligatorio para activarse).
- `DeterministicGenerationAdapter`: reserva, extractiva sobre `evidence` — siempre
  produce una salida válida si `evidence` no está vacío.

**Dónde vive la lógica de "intentar primero, reservar después"**: **no** en un tercer
adaptador — en el propio `ResponseGeneratorAgent`/`PracticeQuestionAgent`, que reciben
ambas implementaciones inyectadas por constructor y las invocan secuencialmente
(research.md §1). El paso 3 de la cadena de degradación (fallo total del agente
generador) es responsabilidad exclusiva de `execute_agency`/`SafeFallbackAgent`
(Feature 001, sin cambios, research.md §2) — no de `GenerationPort`.

**Reglas**:
- El mensaje `system` MUST ser una plantilla fija en código; MUST NOT interpolar nunca
  `evidence[].text` (research.md §3, FR-008b) — la evidencia viaja solo en el mensaje
  `user`, delimitada explícitamente.
- Si `ORALIA_OLLAMA_MODEL` no está configurado, el agente MUST NOT invocar
  `OllamaGenerationAdapter` en absoluto — usa `DeterministicGenerationAdapter`
  directamente.
- Si `general_knowledge_allowed = false`, la instrucción `system` MUST indicar que solo
  puede usarse `evidence` — esto MUST NOT sustituir la verificación posterior de
  `GroundingVerifierAgent` (Feature 002, sin cambios).

## StudyIntentInterpreterAgent

```text
input (AgentRequest.input):
  text: string
  enabled_modes: string[]        # SelfStudyActivityConfig.enabled_modes — modos permitidos
  current_mode: string | null    # CognitiveState.mode actual (data-model.md) — modo activo hasta ahora
  concepts_addressed: string[]

output (AgentResult.output), si status == "ok":
  intent_hypotheses: string[]    # formato "{intent}:{confidence:.2f}"
  primary_intent: string
  primary_confidence: float [0,1]
  requested_mode: "doubt_resolution" | "guided_explanation" | "practice_questions"
                | "presentation_preparation" | "concept_review" | null   # null = continuar current_mode
```

**Reglas**: determinista. `requested_mode` no válido (no está en `enabled_modes`) MUST
ser rechazado/redirigido por el compositor de agencia, sin proponer ningún `StatePatch`
sobre `CognitiveState.mode` y sin invocar agentes de generación (Edge Cases, spec.md).
Si `requested_mode` es válido y distinto de `current_mode`, el compositor propone el
`StatePatch` descrito en `data-model.md` antes de continuar el turno.

## ResponseGeneratorAgent

```text
input (AgentRequest.input):
  purpose: "explicacion" | "explicacion_progresiva" | "ejemplo" | "comparacion"
         | "estructura_exposicion" | "resumen_concepto"
  student_input: string          # NUEVO (H01, research.md §13) — texto literal del turno actual
  evidence: [ { fragment_id, text, document_id, document_version } ]
  concepts_addressed: string[]
  concepts_pending: string[]

output (AgentResult.output), si status == "ok":
  proposal_text: string
  generation_trace: { adapter, model, fallback_used: bool }
```

**Reglas**: rol `generator` — MUST NOT también ser `verifier` de su propia salida
(Principio IV). Recibe `OllamaGenerationAdapter`/`DeterministicGenerationAdapter`
inyectados; implementa la secuencia primaria→reserva descrita arriba. `student_input`
MUST viajar como dato delimitado en el mensaje `user`, igual que `evidence[].text` —
MUST NOT interpolarse en la plantilla `system` fija (FR-008b, research.md §3/§13).

## PracticeQuestionAgent

```text
input (AgentRequest.input):
  evidence: [ { fragment_id, text, document_id, document_version } ]
  objective_ref: string
  concepts: string[]
  previous_questions: [ { question_type, concepts } ]  # filtrado por session_id (FR-011a)
  reveals_solution: bool

output (AgentResult.output), si status == "ok":
  question_type: "explicacion" | "aplicacion" | "comparacion" | "justificacion" | "deteccion_errores"
  question_text: string
  internal_expected_answer: string | null   # null si reveals_solution=true
  difficulty_hint: "baja" | "media" | "alta"
  reveals_solution: bool
  generation_trace: { adapter, model, fallback_used: bool }
```

**Reglas**: `previous_questions` MUST filtrarse siempre por `session_id`. Cuando
`reveals_solution = false`, `internal_expected_answer` MUST poblarse. Igual secuencia
primaria→reserva de `GenerationPort` que `ResponseGeneratorAgent`.

## SolutionNonDisclosureVerifierAgent — independiente de `GroundingVerifierAgent`

```text
input (AgentRequest.input):
  question_text: string
  internal_expected_answer: string
  reveals_solution: bool
  attempt_number: int            # 1..ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS (default 2)

output (AgentResult.output), si status == "ok":
  verdict: "approved" | "block"
  overlap_score: float           # frente a _DISCLOSURE_OVERLAP_THRESHOLD propio (0.3 por defecto)
```

**Reglas** (research.md §4 — independencia explícita frente a `GroundingVerifierAgent`):

- Contrato, umbral (`_DISCLOSURE_OVERLAP_THRESHOLD`,
  `ORALIA_DISCLOSURE_OVERLAP_THRESHOLD`, default 0.3), veredicto (2 valores) y traza
  (`non_disclosure_check`) son propios de este agente — implementa su propia función de
  tokenización/solapamiento en su propio módulo; MUST NOT importar la función privada
  de `grounding_verifier_agent.py` (Feature 002, no modificable — FR-025).
- Rol `verifier`, independiente de `PracticeQuestionAgent` (rol `generator`) — nunca el
  mismo agente (Principio IV).
- MUST NOT activarse cuando `reveals_solution = true` (FR-003).
- MUST NOT evaluar ni calificar la respuesta del estudiante — solo compara dos textos
  producidos por el sistema (FR-013a).
- **Limitación de MVP documentada**: puede producir falsos negativos ante paráfrasis
  complejas sin solapamiento léxico (research.md §4). No se compensa con un segundo LLM
  como juez — riesgo aceptado y documentado, no resuelto en esta feature.
- **Refuerzo pendiente (H04, research.md §4, estabilización 2026-09-10)**: la
  tokenización MUST incluir dígitos y expresiones alfanuméricas cortas como tokens
  significativos (no solo letras ≥4 caracteres) y MUST exigir coincidencia exacta —no
  una proporción de solapamiento— cuando `internal_expected_answer` tokeniza a un único
  token, para no aprobar siempre soluciones puramente numéricas o muy cortas (matriz de
  aceptación N1–N3/T1, variante reservada V1, research.md §4).
- Si `verdict = block`: el compositor reintenta la generación (hasta
  `ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS`, default 2); agotados los intentos, sustituye por
  una pregunta de `DeterministicGenerationAdapter` directamente.

## CoherenceVerifierAgent

```text
input (AgentRequest.input):
  proposal_text: string
  prior_statements: string[]     # solo el output_text del turno inmediatamente anterior
  active_sources: string[]
  concepts_addressed: string[]
  turn_number: int
  max_turns: int

output (AgentResult.output), si status == "ok":
  verdict: "approved" | "block" | "reformulate"
  incident_types: string[]       # nunca incluye fallo_agente/latencia_excesiva (los deriva el compositor)
  recovery_action: string | null
```

**Reglas**: heurística determinista propia (tercera implementación independiente de la
técnica de solapamiento léxico, distinta en umbral/configuración de
`GroundingVerifierAgent` y de `SolutionNonDisclosureVerifierAgent` — research.md §5).
Umbrales configurables (`ORALIA_COHERENCE_NO_PROGRESS_WINDOW` default 3,
`ORALIA_COHERENCE_REPETITION_WINDOW` default 1 turno).

## Combinación de veredictos (`verify-combined`, lógica del compositor, no un agente)

Sin cambios respecto a la iteración anterior — tabla de severidad `block > reformulate
> clarify > acknowledge_missing_info > approved` (research.md §5), registrada como
`TraceEvent verification_combined`.

## Actualización de `CognitiveState.mode` (research.md §6 — no es un agente, es una
regla del compositor)

Tras validar `requested_mode` (StudyIntentInterpreterAgent) contra `enabled_modes`
(SelfStudyActivityConfig), si difiere de `CognitiveState.mode` actual, el compositor
propone un `StatePatch` (Feature 001, `apply_patch`, sin cambios) con
`element_type = "decision"`, `payload = {"mode": requested_mode}`, antes de continuar
con recuperación/generación. Si el patch es rechazado por conflicto de versión
(`applied = false`), el turno se trata como cualquier conflicto de estado ya existente
en la Feature 001 (mismo mecanismo, sin caso especial).

## Registro de razón de activación (US5, FR-003)

Sin cambios de forma — `TraceEvent agents_selected` con `payload.mode` (copia de
auditoría del modo ya fijado en `CognitiveState.mode` por el `StatePatch` anterior,
research.md §6/§9), `activated_steps`, `reasons`, `skipped_modes`.
