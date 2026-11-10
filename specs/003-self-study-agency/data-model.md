# Data Model: Agencia de autoestudio

Regenerado tras el cierre de requisitos (Clarify, 2026-09-01) y la ronda de corrección
de consistencia arquitectónica (2026-09-02). Identificadores canónicos de modo:
`doubt_resolution`, `guided_explanation`, `practice_questions`,
`presentation_preparation`, `concept_review` (FR-001). `Course`, `ActivityConfiguration`
(incluidos `immutable_since` y `retention_policy_id`), `RetentionPolicy`,
`ParticipantCode`, `Session`, `Turn`, `AgentContract`, `Agent`, `Agency`,
`InternalMessage`, `CognitiveState` (**incluido su campo `mode`, ver más abajo**),
`StatePatch`, `GeneratedProposal`, `VerificationResult`, `DialogueAction`, `TraceEvent`
(Feature 001) y `MaterialDocument`, `MaterialFragment`, `Evidence`,
`GroundingVerificationResult`, `MaterialConflictRecord` (Feature 002) se reutilizan tal
como quedaron definidos — ninguno se modifica (FR-025).

## `CognitiveState.mode` — fuente de verdad del modo activo (research.md §6)

**No es una entidad nueva.** `CognitiveState.mode` (Feature 001, campo `string` ya
existente, sin ampliar el esquema) es la fuente de verdad del modo canónico
(`doubt_resolution` | `guided_explanation` | `practice_questions` |
`presentation_preparation` | `concept_review`) activo **en la sesión, en este
instante**. Distinto de `SelfStudyActivityConfig.enabled_modes` (qué está *permitido*
para la actividad).

**Actualización**: exclusivamente vía `StatePatch` (Feature 001, `apply_patch`, sin
cambios) — `element_type = "decision"`, `payload = {"mode": <nuevo modo>}` — con el
mismo control de versión optimista (`base_version`/`resulting_version`) que cualquier
otro cambio de `CognitiveState`. Ningún componente de esta feature escribe
`CognitiveState.mode` directamente; todos pasan por `apply_patch`.

**Validación**: un `StatePatch` que proponga un `mode` fuera de
`SelfStudyActivityConfig.enabled_modes` de la actividad de la sesión MUST NOT aplicarse
— el compositor de agencia valida `requested_mode` contra `enabled_modes` **antes** de
proponer el patch (rechazo a nivel de aplicación, no de restricción SQL).

**La traza no es la fuente de verdad**: `TraceEvent agents_selected.payload.mode`
registra el mismo valor **después** de que el `StatePatch` lo haya fijado — es una
copia de auditoría para reconstrucción/verificación de SC-001, nunca lo que la
orquestación consulta para decidir.

## SelfStudyActivityConfig

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| activity_configuration_id | UUID (FK ActivityConfiguration, única) | 1:1 |
| enabled_modes | list[enum(5 valores canónicos)] | FR-002 — no vacío (FR-002a); conjunto de modos *permitidos*, no el activo |
| summary_authorized | bool | default `false` — autoriza únicamente *generar* el resumen efímero (FR-021); **no** autoriza conservarlo (ver `retention_authorized`) |
| practice_reveals_solution | bool | default `false` |
| retention_authorized | bool \| null | **NUEVO** (FR-028a, research.md §12, corregido en la segunda ronda de estabilización) — `null` = sin decidir (valor de migración para configuraciones preexistentes, nunca `true`/`false` por defecto); `true`/`false` solo por decisión humana explícita vía este mismo endpoint de configuración. Independiente de `summary_authorized` y de `RetentionPolicy.retention_days` (un plazo expresa cuánto tiempo, nunca si está autorizado conservar) |
| created_at | datetime | |

**Validación de creación/actualización** (research.md §7): `409` si
`ActivityConfiguration.immutable_since` no es `null`. `enabled_modes` MUST NOT estar
vacío (`422`).

**Retención**: el plazo (`retention_days`) sigue heredándose transitivamente del
`RetentionPolicy` de `ActivityConfiguration.retention_policy_id` (Feature 001, sin
cambios) — pero la *autorización* de conservar es `retention_authorized` (este campo),
no la mera existencia de un plazo. Ver "Retención y purga" más abajo para los cuatro
estados resultantes.

## PracticeQuestion

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK Session) | acotado a la sesión (FR-011, FR-011a) |
| turn_id | UUID (FK Turn) | |
| question_type | enum(`explicacion`,`aplicacion`,`comparacion`,`justificacion`,`deteccion_errores`) | FR-012 |
| objective_ref | string | |
| concepts | list[string] | |
| fragment_ids | list[UUID] (FK MaterialFragment, Feature 002) | |
| difficulty_hint | enum(`baja`,`media`,`alta`) | orientativa (FR-014) |
| reveals_solution | bool | copiado de `SelfStudyActivityConfig.practice_reveals_solution` al generar |
| generator_used | enum(`ollama`,`deterministic`) | qué adaptador de `GenerationPort` produjo la pregunta finalmente mostrada (research.md §1) |
| non_disclosure_attempts | int | número de intentos de regeneración por `SolutionNonDisclosureVerifierAgent` hasta `approved` (research.md §4) |
| created_at | datetime | |

**No persistido**: `internal_expected_answer` (research.md §4) — transitorio, solo en
memoria durante el turno; MUST NOT persistirse (Principio VIII).

## CoherenceIncident

Sin cambios respecto a la iteración anterior.

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK Session) | |
| turn_id | UUID (FK Turn) | |
| incident_type | enum(`falta_informacion`,`no_fundamentada`,`contradiccion`,`repeticion`,`perdida_objetivo`,`exceso_turnos_mismo_concepto`,`fallo_agente`,`latencia_excesiva`,`ausencia_progreso`) | FR-015 |
| affected_proposal_ref | UUID (FK GeneratedProposal, Feature 001) | |
| recovery_action | enum(6 valores, FR-016) | |
| combined_verdict_source | enum(`grounding`,`coherence`,`both`) | FR-024, research.md §5 |
| created_at | datetime | |

## `SolutionNonDisclosureVerifierAgent` — registro (no tabla nueva)

`TraceEvent` (`event_type = "non_disclosure_check"`):

| Campo de `payload` | Tipo | Notas |
|---|---|---|
| question_id | UUID (FK PracticeQuestion) | |
| verdict | enum(`approved`,`block`) | veredicto propio, independiente del de `GroundingVerifierAgent` (research.md §4) |
| overlap_score | float | frente a `_DISCLOSURE_OVERLAP_THRESHOLD` propio (default 0.3, `ORALIA_DISCLOSURE_OVERLAP_THRESHOLD`) |
| attempt_number | int | 1..`ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS` (default 2) |

## StudySessionSummary (persistido como `TraceEvent`)

Sin cambios respecto a la iteración anterior (`event_type = "study_session_summary"`;
`incidents` como `{incident_type, recovery_action}`, FR-022a).

## Generación (registro, `TraceEvent event_type = "generation_call"`)

| Campo de `payload` | Tipo | Notas |
|---|---|---|
| adapter | enum(`ollama`,`deterministic`) | **renombrado** desde `template` (research.md §1) — solo dos valores posibles, sin un tercero |
| model | string \| null | |
| parameters | json | `{temperature, max_tokens}` |
| purpose | enum(7 valores, ver contrato) | |
| fragment_ids | list[UUID] | |
| fallback_used | bool | `true` si se usó `deterministic` tras un fallo de `ollama` |
| latency_ms | int | |

## `verification_combined` (registro, `TraceEvent`)

Sin cambios respecto a la iteración anterior.

| Campo de `payload` | Tipo | Notas |
|---|---|---|
| grounding_verdict | enum(Feature 002, 5 valores) | |
| coherence_verdict | enum(`approved`,`block`,`reformulate`) | |
| combined_outcome | enum(`block`,`reformulate`,`clarify`,`acknowledge_missing_info`,`approved`) | |
| recovery_action | enum(igual que `CoherenceIncident.recovery_action`) \| null | |
| severity_source | enum(`grounding`,`coherence`,`tie_coherence`) | |

## Retención y purga (FR-028, research.md §8)

**Un campo nuevo, propio de esta feature** (`SelfStudyActivityConfig.
retention_authorized`, ver más arriba) representa la autorización de conservar — el
plazo sigue heredándose transitivamente de
`Session.activity_configuration_id → ActivityConfiguration.retention_policy_id →
RetentionPolicy.retention_days` (Feature 001, cadena de FKs ya existente, sin cambios
de esquema ahí). **Corregido en la segunda ronda de estabilización**: la versión
anterior de esta sección trataba la mera existencia de un plazo finito como si fuera
la autorización — no lo es (research.md §12.1).

**Cuatro estados de una actividad de autoestudio** (research.md §12.1):

| Estado | `retention_authorized` | `RetentionPolicy.retention_days` | Purgable |
|---|---|---|---|
| `authorized_expiring` | `true` | finito | sí, cuando `ended_at + retention_days < now()` |
| `not_authorized_purge_eligible` | `false` | cualquiera | sí, desde el primer cierre, sin esperar plazo |
| `invalid_authorized_without_policy` | `true` | nulo/sin política | no — combinación inválida, requiere corrección humana (asignar plazo o retirar autorización) |
| `undecided_preexisting` | `null` (valor de migración) | cualquiera | no — requiere decisión humana explícita, nunca deducida del número de invocaciones de la purga |

**Dos operaciones distintas (research.md §12.2)**: `GET .../retention-audit` (nuevo,
solo lectura, sin efectos — lista sesiones/actividades por estado, incluidas
`undecided_preexisting`/`invalid_authorized_without_policy`) frente a
`POST .../purge-expired` (acción, elimina únicamente `authorized_expiring` con plazo
cumplido y `not_authorized_purge_eligible` — MUST NUNCA eliminar las otras dos, sin
importar cuántas veces se invoque).

**Mecanismo de purga (invocable, no automatizado)**: `PurgeResult` — valor de retorno
de `purge_expired_self_study_data` (no persistido como tabla), redefinido en esta
ronda (research.md §12.5):

```text
PurgeResult:
  sessions_matching_criteria: int    # RENOMBRADO desde sessions_evaluated — estable o
                                      # creciente entre ejecuciones, nunca decrece solo
                                      # porque ya no queden filas que borrar
  sessions_with_rows_deleted: int    # RENOMBRADO desde sessions_purged — filas
                                      # efectivamente borradas EN ESTA ejecución; 0 en
                                      # una repetición no implica "ya no expirada"
  practice_questions_deleted: int
  coherence_incidents_deleted: int
  trace_events_deleted: int
```

`sessions_flagged_no_finite_policy` de la primera ronda se retira de `PurgeResult` —
ese diagnóstico vive en `GET .../retention-audit`, no en la acción de purga.

**Alcance de la eliminación (acotado por `event_type`, sin cambios respecto a la
primera ronda — ya era correcto, research.md §12.3)**: `PracticeQuestion`,
`CoherenceIncident`, y únicamente los `TraceEvent` cuyo `event_type` ∈
{`generation_call`, `non_disclosure_check`, `verification_combined`,
`study_session_summary`, `agents_selected`} asociados a esa sesión — **no** todos los
`TraceEvent` de la sesión. Exactamente lo que FR-028 nombra textualmente — **no** el
contenido textual equivalente que persiste en `Turn.input_text`/`Turn.output_text`,
`GeneratedProposal` ni `StatePatch.payload.participant_response` (Feature 001,
reutilizadas sin cambios; duplicación verificada y documentada como contradicción
abierta en research.md §12.4 — no resuelta en esta ronda, fuera del alcance textual de
FR-028 y del alcance de modificación de esta feature sobre la Feature 001).

## Relaciones clave (resumen)

```text
CognitiveState.mode ── actualizado por ──> StatePatch (element_type=decision, Feature 001, sin cambios)
ActivityConfiguration 1─1 SelfStudyActivityConfig
ActivityConfiguration N─1 RetentionPolicy (Feature 001; retention_days gobierna la purga de PracticeQuestion/CoherenceIncident/TraceEvent vía Session)
Session 1─N PracticeQuestion
Turn 1─N PracticeQuestion (opcional)
Session 1─N CoherenceIncident
Turn 1─N CoherenceIncident
GeneratedProposal 1─0..N CoherenceIncident (a través de affected_proposal_ref)
Session 1─0..1 TraceEvent(event_type=study_session_summary)
Turn 1─N TraceEvent(event_type ∈ {agents_selected, generation_call, non_disclosure_check, verification_combined, agent_execution})
```
