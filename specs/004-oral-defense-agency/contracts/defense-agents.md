# Contrato interno: puertos y agentes nuevos de la Feature 004

Todos los agentes implementan el mismo protocolo `Executable` ya definido en la Feature
001 (`AgentRequest`/`AgentResult`/`AgentError`/`CancellationToken`) — sin cambios. Los
puertos (`TranscriptionPort`/`SpeechSynthesisPort`) no son agentes — no implementan
`Executable`, no se registran en una `AgencyDefinition` (research.md §2).

## `TranscriptionPort` (interfaz, `infrastructure/speech/`) — una implementación local

```text
TranscriptionPort (Protocol):
  async def transcribe(audio: bytes, *, language: str) -> TranscriptionOutcome

TranscriptionOutcome:
  ok: bool
  text: string
  segments: [ { text: string, start_ms: int | null, end_ms: int | null, confidence: float } ]
  overall_confidence: float
  low_confidence: bool
```

**Implementación**: `FasterWhisperTranscriptionAdapter` — local, vía
`faster-whisper>=1.2.1,<2` y modelo local (research.md §2, §16, §24). Si `ok=false`
(error técnico), el compositor descarta el audio de
inmediato y degrada a texto en el mismo turno (research.md §3) — sin reintento sobre el
mismo audio.

**Reglas**:
- El audio nunca se persiste ni se adjunta a un `AgentRequest`/`TraceEvent` — el
  compositor lo mantiene en una variable local y la descarta tras esta llamada.
- El router limita la entrada a 10 MiB/300 s y cierra en `finally` cualquier spool
  multipart. El adaptador se ejecuta en el worker de voz process-wide acotado; un
  resultado posterior a timeout/cancelación se descarta sin persistencia ni traza.
- `low_confidence = true` si algún `segments[].confidence` cae bajo
  `ORALIA_STT_LOW_CONFIDENCE_THRESHOLD` (default `0.6`).
- Si `ORALIA_STT_MODEL` no está configurado, la actividad no puede habilitar
  `voice_input_allowed` — el sistema **MUST NOT** intentar invocar este puerto en
  absoluto.

## `SpeechSynthesisPort` (interfaz, `infrastructure/speech/`) — una implementación local

```text
SpeechSynthesisPort (Protocol):
  async def synthesize(text: string, *, language: str) -> SynthesisOutcome

SynthesisOutcome:
  ok: bool
  audio: bytes | null
```

**Implementación**: `PiperSpeechSynthesisAdapter` — local, vía `piper-tts>=1.8,<2` y
voz `.onnx` local (research.md §2, §16, §24).

**Reglas** (research.md §7):
- MUST recibir únicamente el `output_text` final ya verificado (fundamentación,
  coherencia, control constitucional) — nunca un `GeneratedProposal` sin verificar.
- MUST reproducir el texto literalmente — ninguna implementación puede resumir, ampliar,
  suavizar, enriquecer ni regenerar el contenido.
- Si `ok=false` o la llamada falla/expira (`run_with_deadline`, Feature 001, sin
  cambios): el turno se completa igual con la salida textual ya calculada;
  `Turn.status` permanece `"completed"` — un fallo de TTS nunca degrada el contenido del
  turno.
- Si `ORALIA_TTS_VOICE` no está configurado, la actividad no puede habilitar
  `voice_output_allowed`.
- La llamada bloqueante usa el mismo worker de voz acotado que STT. El puerto no recibe
  una sesión SQLAlchemy ni persiste audio.

## Puerta final de salida (Feature 001 T090, obligatoria)

La combinación de grounding/coherencia no autoriza por sí misma una salida visible.
Cada candidato final se proyecta a `OutputProposal` y se verifica con
`final_output_gate` usando una instancia confiable de `AuthorizationSnapshot` creada
desde la sesión, configuración, política canónica y catálogo exactos. La identidad de
plantilla se resuelve por `(id, version, sha256)` y los bindings cubren el texto completo.

```text
attempt=0, message_type=normal
  approved -> persistir propuesta + veredicto + Turn.output_text
  block    -> Turn.blocked=true, output_text=NULL
              -> opcional: attempt=1, message_type=operational
                   approved -> publicar el mensaje operativo catalogado
                   block    -> finish + closed_error_safe + output_text=NULL
```

La regla cubre pregunta inicial, repregunta, `clarify`, falta de evidencia, degradación,
mensajes de cierre y resumen textual. La puerta no hace commit ni cierra la sesión. TTS
solo consume `Turn.output_text` persistido y vinculado a un veredicto final aprobado.

## `PracticeQuestionAgent` (Feature 003, **sin cambios**) — reutilizado para la pregunta inicial

Ver `specs/003-self-study-agency/contracts/self-study-agents.md#PracticeQuestionAgent`.
Reutilizado literalmente cuando `DefenseActivityConfig.initial_questions` está vacío
(research.md §8) — mismo contrato, mismo fichero, sin extensión.

## `FollowUpQuestionAgent` — nuevo, rol `generator`

```text
input (AgentRequest.input):
  previous_question_text: string
  student_answer_text: string        # transcripción definitiva (research.md §4) o texto directo
  concepts_mentioned: string[]       # extraídos de la respuesta (FR-012)
  concepts_addressed: string[]       # CognitiveState
  concepts_pending: string[]         # CognitiveState
  evidence: [ { fragment_id, text, document_id, document_version } ]
  objective: string
  purpose: "deepen_current_topic" | "switch_topic"

output (AgentResult.output), si status == "ok":
  question_text: string
  followup_type: "justificacion" | "ejemplo" | "comparacion" | "decision_tecnica" | "explicacion_error" | "profundizacion"
  referenced_concept: string         # MUST pertenecer a concepts_mentioned o a evidence — research.md §9
  generation_trace: { adapter: "ollama"|"deterministic", model: string | null, fallback_used: bool }
```

**Reglas**:
- Rol `generator` — MUST NOT también verificar su propia salida (Principio IV). Toda
  salida pasa por `GroundingVerifierAgent` + `CoherenceVerifierAgent` +
  la puerta final T090 (`ConstitutionalControl`, snapshot, catálogo y persistencia) antes
  de mostrarse; la composición es aditiva y conserva los contratos existentes.
- Delega en `GenerationPort` (Feature 003, extendido de forma aditiva con
  `purpose="repregunta"` — research.md §1) con la misma secuencia primaria→reserva que
  `ResponseGeneratorAgent`/`PracticeQuestionAgent` — sin un tercer adaptador.
- `purpose` (`deepen_current_topic`/`switch_topic`) lo decide el compositor **antes**
  de invocar este agente (research.md §10) — el agente no elige por sí mismo si
  profundiza o cambia de tema, solo genera la repregunta acorde al propósito recibido.
- `referenced_concept` MUST estar presente en `concepts_mentioned` o en algún
  `evidence[].text`. Si el agente no puede satisfacerlo, sigue devolviendo
  `status="ok"` con su mejor propuesta — es el **compositor**, no el agente, quien
  decide qué hacer con una repregunta sin `referenced_concept` válido: la trata como no
  fundamentada y resuelve `dialogue_action=acknowledge_missing_info` (research.md §9)
  — nunca `clarify` (ver corrección más abajo) ni un `status="error"` de agente (eso
  queda reservado a fallos técnicos reales del generador, gestionados por
  `execute_agency`/`SafeFallbackAgent`, Feature 001, sin cambios).
- MUST NOT producir valoración, puntuación, diagnóstico de nivel, ni comentario sobre
  rendimiento (FR-025/FR-026) — la instrucción `system` fija en código lo excluye
  explícitamente, igual que el resto de instrucciones de `ResponseGeneratorAgent`/
  `PracticeQuestionAgent`.

## Combinación de veredictos para una repregunta (`verify-combined`, lógica del compositor)

Reutiliza la **técnica** de combinación por severidad ya validada en la Feature 003
(research.md §5 de la Feature 003, `GroundingVerifierAgent` + `CoherenceVerifierAgent`,
sin modificar `self_study_agency_composer.py`), aplicada aquí sobre la **repregunta
generada** — distinto, y corregido tras revisión de consistencia (2026-09-02), del
disparador de `clarify` sobre la **respuesta del estudiante** (research.md §9/§10):

| Señal sobre la repregunta generada | `dialogue_action` resultante |
|---|---|
| `GroundingVerifierAgent`/`referenced_concept` no fundamentan la repregunta | `acknowledge_missing_info` |
| `CoherenceVerifierAgent` detecta repetición de la repregunta anterior | regeneración acotada → `acknowledge_missing_info` si se agotan los intentos (research.md §9) |
| Ambas señales aprueban | `ask` (con `purpose=deepen_current_topic`\|`switch_topic`) |
| `ConstitutionalControl` bloquea (contenido evaluativo u otro) | turno bloqueado (`blocked=true`), mismo tratamiento ya validado en Features 001/003 |

`clarify` **no** forma parte de esta tabla — nunca es resultado de verificar la
repregunta generada. Es una decisión separada, evaluada **antes** de invocar
`FollowUpQuestionAgent`, sobre la respuesta ya definitiva del estudiante
(`concepts_mentioned` vacío, o `CoherenceVerifierAgent` aplicado a esa respuesta frente a
una afirmación previa del propio estudiante detecta contradicción — research.md §9). Si
se dispara `clarify`, el compositor ni siquiera llega a invocar `FollowUpQuestionAgent`
para ese turno.

## `DialogueAction` (Feature 003, **sin cambios**) — reutilizado, sin ampliar el enum

Ver mapeo completo en research.md §10. Ninguna acción nueva se introduce. Los estados
técnicos de STT/TTS (baja confianza, fallo de captura/transcripción/síntesis) **MUST
NOT** representarse mediante ningún valor de `DialogueAction` (research.md §5/§10).
