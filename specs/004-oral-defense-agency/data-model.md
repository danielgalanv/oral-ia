# Data Model: Agencia de defensa oral y voz opcional

`Course`, `ActivityConfiguration` (incluidos `immutable_since`/`retention_policy_id`),
`RetentionPolicy`, `ParticipantCode`, `Session`, `Turn`, `AgentContract`, `Agent`,
`Agency`, `InternalMessage`, `CognitiveState` (sin campos nuevos — research.md §11),
`StatePatch`, `GeneratedProposal`, `VerificationResult`, `DialogueAction`, `TraceEvent`
(Feature 001) y `MaterialDocument`, `MaterialFragment`, `Evidence`,
`GroundingVerificationResult` (Feature 002) se reutilizan tal como quedaron definidos —
ninguno se modifica (FR-033). `PracticeQuestion`/`CoherenceIncident`/
`SelfStudyActivityConfig` (Feature 003) tampoco se modifican; `PracticeQuestion` se
reutiliza indirectamente vía `PracticeQuestionAgent` (research.md §8) sin crear una fila
para la pregunta inicial de defensa (esa fila pertenece conceptualmente a autoestudio,
no a defensa — la pregunta inicial de defensa queda representada por su propio
`GeneratedProposal`/`TraceEvent`, igual que cualquier otra propuesta de esta feature).

## `CognitiveState` — sin extensión (research.md §11)

Ningún campo nuevo. Ver research.md §11 para el mapeo completo de los siete conceptos de
defensa sobre `MINIMUM_FIELDS` ya existente.

## `DefenseActivityConfig`

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| activity_configuration_id | UUID (FK `ActivityConfiguration`, única) | 1:1, mismo patrón que `SelfStudyActivityConfig` |
| initial_questions | list[string] | banco docente; vacío ⇒ generar desde materiales vía `PracticeQuestionAgent` (research.md §8) |
| topics | list[string] | temas autorizados para una petición explícita de cambio; default vacío |
| difficulty_hint | enum(`baja`,`media`,`alta`) | orientativa, default `media` |
| voice_input_allowed | bool | default `false` |
| voice_output_allowed | bool | default `false` |
| summary_authorized | bool | default `false` |
| transcript_retention_authorized | bool | default `false` — habilita la elección de conservar al cierre (`ConsentRecord`) |
| created_at | datetime | |

**Validación de creación/actualización** (research.md §12, mismo patrón que
`SelfStudyActivityConfig`, research.md §7 de la Feature 003): `409` si
`ActivityConfiguration.immutable_since` no es `null`. `initial_questions` vacío **y**
sin materiales autorizados asociados a la actividad ⇒ `422` (FR-002a).

**Retención**: sin campo propio — hereda `RetentionPolicy` de
`ActivityConfiguration.retention_policy_id`, igual que el resto de esta feature.

## `Transcript`

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK `Session`) | acotado a la sesión (FR-032, ninguna agregación por `participant_code`) |
| turn_id | UUID nullable (FK `Turn`) | nulo mientras la transcripción es provisional; se vincula al confirmar |
| raw_text | string | salida directa de `TranscriptionPort` — provisional por definición (research.md §4) |
| segments | json | `[{text, start_ms, end_ms, confidence}]` |
| overall_confidence | float | |
| low_confidence | bool | `true` si algún segmento cae bajo `ORALIA_STT_LOW_CONFIDENCE_THRESHOLD` |
| status | enum(`awaiting_confirmation`,`confirmed`) | frontera observable previa a la cognición |
| created_at | datetime | |

**No persistido**: el audio de origen — nunca existe una columna ni referencia a él
(research.md §3, Principio VII).

**Persistencia operativa, no conservación**: esta fila existe en la base de datos
mientras la sesión está en curso por necesidad puramente operativa (el estudiante debe
poder revisarla, el compositor debe poder leerla en turnos posteriores) — **no**
implica consentimiento de conservación. Al cerrar la sesión, se elimina salvo que exista
un `ConsentRecord` con `decision="retain"` y `"transcript"` en `scope` (research.md
§4/§15).

## `TranscriptCorrection`

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| transcript_id | UUID (FK `Transcript`, única) | como mucho una corrección por transcripción — la última revisión sustituye a la anterior mientras el turno sigue `awaiting_confirmation`; una vez confirmada (definitiva), es inmutable |
| session_id | UUID (FK `Session`) | |
| corrected_text | string | |
| created_at | datetime | |

**Regla**: no elimina ni sustituye `Transcript.raw_text` (FR-010) — ambos coexisten
cuando la sesión se conserva. `TranscriptCorrection` representa una corrección de
**reconocimiento** (STT), nunca una corrección académica de la respuesta (research.md,
encargo §18 del plan) — el contenido semántico de la respuesta del estudiante es el
mismo antes y después; solo cambia qué tan fielmente el texto refleja lo que dijo.

Una revisión enviada después de la confirmación se registra como una nueva
`Transcript` y una nueva `TranscriptCorrection`, asociadas al siguiente turno. La
transcripción confirmada anterior, su corrección si existía y su repregunta permanecen
inmutables. `transcript_corrected.supersedes_transcript_id` permite auditar el enlace;
la agencia recibe exclusivamente el nuevo texto definitivo, por la misma entrada textual.

## `ConsentRecord`

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK `Session`, única) | una decisión por sesión, al cierre |
| decision | enum(`retain`,`delete`) | |
| scope | list[string] | subconjunto de `["transcript","summary"]` — qué se conserva si `decision=retain` |
| recorded_at | datetime | |

**Regla**: solo se crea si `DefenseActivityConfig.transcript_retention_authorized` es
verdadero **y** el participante elige `decision="retain"` (research.md §15) — no es un
permiso para procesar la sesión, solo una decisión sobre datos que ya existieron por
necesidad operativa (nota de `Transcript` más arriba). Si la actividad no autoriza
conservación, o si `decision=delete`, el compositor elimina de inmediato
`Transcript`/`TranscriptCorrection`/el `TraceEvent defense_session_summary` de esa
sesión en el mismo cierre — no espera a la purga diferida.

## Retención y purga (FR-031, research.md §15)

**Sin tabla ni campo de retención nuevo.** Regla de cierre unificada (research.md §15):
sin `ConsentRecord(decision="retain")` vigente, `Transcript`/`TranscriptCorrection`/el
`TraceEvent` de resumen se eliminan **en el propio cierre** de la sesión — no llegan a
depender de `RetentionPolicy.retention_days` en absoluto. Solo cuando sí existe
`decision="retain"` esos datos heredan transitivamente
`Session.activity_configuration_id → ActivityConfiguration.retention_policy_id →
RetentionPolicy.retention_days` (Feature 001, cadena ya existente) y quedan sujetos a la
purga diferida — mismo mecanismo que la Feature 003, fichero de purga propio
(`purge_expired_defense_data`, no generaliza el de la Feature 003 — research.md §1/§3
del encargo de corrección).

```text
PurgeResult (igual forma que la de la Feature 003, valor de retorno, no tabla):
  sessions_matching_criteria: int
  sessions_with_rows_deleted: int
  transcripts_deleted: int
  transcript_corrections_deleted: int
  trace_events_deleted: int
```

Criterio de expiración: idéntico al de la Feature 003 —
`Session.ended_at` no nulo, `RetentionPolicy.retention_days` no nulo, y
`Session.ended_at + retention_days < now()`. Alcance: únicamente `Transcript`,
`TranscriptCorrection` y los `TraceEvent` de esta feature asociados a esa sesión.

## Eventos de traza nuevos (`TraceEvent`, `event_type`)

Todos siguen el esquema genérico ya existente (`session_id`, `turn_id`, `event_type`,
`agent_id`, `payload`, `memory_category`, `created_at` — Feature 001, sin cambios).

| `event_type` | `payload` | `memory_category` |
|---|---|---|
| `transcription_recorded` | `{transcript_id, overall_confidence, low_confidence_segment_count}` | `procedural` |
| `transcript_corrected` | `{transcript_id, correction_id}` | `procedural` |
| `transcription_failed` | `{reason}` | `metacognitive` |
| `followup_question_generated` | `{purpose: deepen_current_topic\|switch_topic, source_concept, target_concept, reason, evidence_fragment_ids}` | `procedural` |
| `tts_failed` | `{reason}` | `metacognitive` |
| `defense_session_summary` | ver research.md §14 | `episodic` |
| `consent_recorded` | `{decision, scope}` | `episodic` |

## Relaciones clave (resumen)

```text
ActivityConfiguration 1─1 DefenseActivityConfig
ActivityConfiguration N─1 RetentionPolicy (Feature 001; retention_days gobierna la purga de Transcript/TranscriptCorrection/TraceEvent vía Session)
Session 1─N Transcript
Transcript 1─0..1 TranscriptCorrection
Session 1─0..1 ConsentRecord
Turn 1─N TraceEvent (event_type ∈ {transcription_recorded, transcript_corrected, transcription_failed, followup_question_generated, tts_failed, agent_execution, generation_call, verification_combined})
Session 1─0..1 TraceEvent(event_type=defense_session_summary)
Session 1─0..1 TraceEvent(event_type=consent_recorded)
CognitiveState ── sin cambios de esquema ──> reutilizada tal cual (Feature 001)
```

## Reutilización de autorización de salida (T090)

Feature 004 no crea tablas paralelas para autorización. Reutiliza
`GeneratedProposal`, `VerificationResult`, `OutputAuthorizationPolicy`,
`OutputTemplateCatalog` y `AuthorizationSnapshot` de Feature 001. Para cada salida
visible:

```text
Session + ActivityConfiguration + política/catálogo confiables
  └─> AuthorizationSnapshot (efímero, mínimo, no tabla)
Turn 1─N GeneratedProposal
GeneratedProposal 1─1 VerificationResult final
Turn.output_text = propuesta.text solo si verdict=approved
Turn.output_text = NULL si verdict=block
```

La propuesta persiste únicamente la proyección saneada permitida; una referencia
denegada se representa solo mediante metadatos de autorización y su valor no entra en el
snapshot, la propuesta, el veredicto ni la traza. `authorization_context` conserva
identidades/versiones/huellas y `attempt` (`0` normal, `1` único mensaje operativo).

El resumen tiene una propuesta auxiliar y su veredicto, vinculados al último turno,
sin sobrescribir la salida de ese turno. Si la sesión se cierra sin turnos, una fila
`Turn.index=-1` sirve únicamente de recibo de autorización: no incrementa el contador ni
entra en los hechos del resumen. Al eliminar o expirar el resumen se retira también
`GeneratedProposal.content.text`; permanecen solo las identidades y el veredicto, sin
los hechos del resumen. Así se conserva la prueba de autorización sin eludir el scope.

## Estado de cierre y efectos T150

No se añade una tabla de cierre. `close_session_with_outcome` devuelve
`transition_won`. Solo el ganador puede escribir `ConsentRecord`, el evento
`defense_session_summary`, las eliminaciones o conservación y el evento/liberación de
cierre. Los perdedores no construyen resumen y devuelven el estado existente. Estas
escrituras y la transición se confirman juntas o se revierten juntas.

## Audio y síntesis

No existe entidad, columna, URI, ruta temporal ni hash persistido para audio de entrada o
salida. El descriptor de reproducción de la respuesta HTTP se deriva del `Turn` aprobado;
no es una entidad almacenada. Cada reproducción sintetiza desde `Turn.output_text` y
verifica de nuevo su `VerificationResult` final.


## Borrado de proyecciones operativas de defensa

El scope `transcript` cubre también las copias operativas del contenido de la sesión:
`Turn.input_text/output_text`, texto de propuestas, contenido de `StatePatch`, mensajes
internos, `CognitiveState` y claves de contenido de las trazas. Sin consentimiento, o al
expirar el plazo, `defense_retention_service.erase_defense_content` borra esas copias
solo para la sesión terminal de modo `oral_defense`. Conserva IDs, versiones, huellas,
veredictos y metadatos estructurales de auditoría; registra `defense_content_erased`.
El resumen tiene scope separado. No se alteran otras sesiones ni sus estados.
Esta eliminación posterior a la sesión aplica la política de privacidad; una corrección
operativa de transcripción sigue creando una revisión nueva sin reescribir turnos previos.

Autorizar conservación exige `RetentionPolicy.retention_days` finito y no negativo
(también cero es finito). Se valida al configurar y otra vez antes de reclamar el cierre
con `retain=true`; una configuración antigua sin plazo no permite crear consentimiento.
No hay plazo implícito ni conservación indefinida.

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
