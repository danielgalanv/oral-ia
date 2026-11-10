# Contrato HTTP: Agencia de autoestudio

Regenerado tras el cierre de requisitos (Clarify, 2026-09-01) y la ronda de corrección
de consistencia arquitectónica (2026-09-02, añade el endpoint de purga de FR-028).
Identificadores canónicos de modo: `doubt_resolution`, `guided_explanation`,
`practice_questions`, `presentation_preparation`, `concept_review`. Ningún endpoint de
la Feature 001/002 se modifica (FR-025).

## Área de participante

### `POST /api/v1/sessions/{session_id}/study-turns`

**Request**: `{ "text": string }`.

**Response `200`**:
```json
{
  "turn_id": "uuid",
  "mode": "doubt_resolution | guided_explanation | practice_questions | presentation_preparation | concept_review",
  "dialogue_action": "respond | ask | re_ask | clarify | acknowledge_missing_info | summarize | finish",
  "output_text": "string | null",
  "state_version": "int",
  "sources": [
    { "document_id": "uuid", "document_version": "int", "location_ref": "string", "fragment_text": "string" }
  ],
  "general_knowledge_used": "bool",
  "blocked": "bool (solo presente si true)",
  "session_closed": "bool (solo presente si true — estabilización 2026-09-10, FR-021a)",
  "study_summary": "object | null (solo presente si session_closed = true — estabilización 2026-09-10, FR-021a)"
}
```

**Reglas**:
- `mode` es una copia de auditoría, en la respuesta HTTP, del valor que este turno ya
  fijó en `CognitiveState.mode` mediante `StatePatch` (research.md §6, data-model.md) —
  la fuente de verdad es `CognitiveState.mode`, no esta respuesta. Puede variar de un
  turno a otro dentro de la misma sesión si la actividad habilita varios modos.
- `sources` MUST estar vacío si la respuesta no usó materiales; MUST NOT aparecer si
  `blocked = true`.
- `404` si la sesión no existe o no está activa.
- `409` si el turno solicita un modo no habilitado por
  `SelfStudyActivityConfig.enabled_modes` — cuerpo:
  `{ "detail": "mode not enabled for this activity", "requested_mode": "string" }`.
- **`session_closed`/`study_summary`** (research.md §11, FR-020/FR-021a): cuando este
  turno hace que la sesión alcance su límite de turnos/duración (FR-020),
  `session_closed = true` y `study_summary` lleva el mismo valor
  (`object` o `null` según `summary_authorized`) que llevaría una llamada a
  `POST /study-end` inmediatamente después — que en ese caso ya no tiene nada nuevo que
  entregar (ver regla de `study-end` más abajo). Ninguno de los dos campos aparece en un
  turno que no cierra la sesión, para no alterar el esquema ya validado del resto de
  casos. El cliente MUST tratar `session_closed = true` igual que una respuesta de
  `study-end`: deshabilitar el envío de nuevos turnos (FR-021b), sin ofrecer una vía
  adicional para recuperar `study_summary` más tarde.

### `POST /api/v1/sessions/{session_id}/study-end`

Reutiliza `close_session` (Feature 001, sin cambios), añade `study_summary` (`null` si
`summary_authorized = false`, o si la sesión ya estaba cerrada por cualquiera de las dos
vías — ver regla de idempotencia).

**Regla de idempotencia (research.md §11, estabilización 2026-09-10)**: si la sesión ya
está cerrada al recibir esta petición (cierre voluntario repetido, o cierre automático
ya ocurrido en un turno anterior vía `session_closed` de `study-turns`), la respuesta
MUST devolver el `status` ya persistido y `study_summary: null` — **no** un error, y
**no** una regeneración del resumen. El resumen, si se generó, ya fue entregado en la
respuesta que efectivamente cerró la sesión (esta misma, o la de `study-turns`); esta
feature MUST NOT ofrecer una segunda vía para recuperarlo (FR-021). Si la respuesta que
comunicó el cierre se perdió en tránsito, el resumen queda irrecuperable para el
participante — no se garantiza entrega exactamente una vez (research.md §11).

## Área técnica (docente)

### `POST /api/v1/tecnica/activities/{activity_id}/self-study-config`

**Request**:
```json
{
  "enabled_modes": ["doubt_resolution", "practice_questions"],
  "summary_authorized": true,
  "practice_reveals_solution": false,
  "retention_authorized": null
}
```

**Reglas** (research.md §7): **Response `201`** si `ActivityConfiguration.immutable_since`
es `null`; **Response `409`** (`{"detail": "activity configuration is immutable"}`) si
ya no lo es — mismo patrón exacto que `ActivityConfiguration` (Feature 001). **Response
`422`** si `enabled_modes` está vacío (FR-002a).

**`retention_authorized`** (corregido en la segunda ronda de estabilización, FR-028a,
research.md §12.1): `true`/`false`/`null` — representa exclusivamente si está
autorizado *conservar* datos derivados más allá del cierre, independiente de
`summary_authorized` (que solo autoriza *generar* el resumen) y del plazo
(`RetentionPolicy.retention_days`, que solo dice cuánto tiempo). Omitido en la
petición ⟹ `null` ("sin decidir") — este endpoint MUST NOT asumir `true` ni `false`
por omisión.

### `GET /api/v1/tecnica/sessions/{session_id}/study-trace`

Sin cambios de mecanismo respecto a la iteración anterior — reutiliza
`reconstruct_session_trace` (Feature 001, genérico por `event_type`, sin cambios).
Ahora incluye también los `event_type` `non_disclosure_check` y `verification_combined`
(data-model.md, research.md §9).

**Regla explícita (FR-011a, research.md §8)**: este endpoint y cualquier otro de esta
feature toman **únicamente** `session_id` como clave de reconstrucción — ninguna ruta
de esta feature acepta `participant_code` como parámetro de agregación entre sesiones.

### `GET /api/v1/tecnica/self-study/retention-audit` (NUEVO — corregido en la segunda ronda de estabilización, FR-028a, research.md §12.2)

**Consulta de diagnóstico, sin efectos secundarios** — invocarla cualquier número de
veces MUST NOT cambiar ningún dato ni acercar ninguna sesión a ser purgada. Separada
deliberadamente de la acción de purga (ver más abajo): reportar no es lo mismo que
actuar.

**Response `200`**:
```json
{
  "authorized_expiring": [ { "activity_configuration_id": "uuid", "sessions": "int" } ],
  "not_authorized_purge_eligible": [ { "activity_configuration_id": "uuid", "sessions": "int" } ],
  "undecided_preexisting": [ { "activity_configuration_id": "uuid", "sessions": "int" } ],
  "invalid_authorized_without_policy": [ { "activity_configuration_id": "uuid", "sessions": "int" } ]
}
```

`undecided_preexisting` e `invalid_authorized_without_policy` MUST requerir una
decisión humana explícita (fijar `retention_authorized` y/o asociar una
`RetentionPolicy` con plazo finito vía `POST .../self-study-config`) antes de que esas
actividades puedan aparecer en ninguna de las otras dos categorías — nunca por invocar
este endpoint ni el de purga repetidamente.

### `POST /api/v1/tecnica/self-study/purge-expired` (FR-028/FR-028a, research.md §12 — corregido en la segunda ronda de estabilización)

Invocación manual del profesorado/administrador (Principio VI) — MUST NOT programarse
ni ejecutarse automáticamente en esta feature (la automatización/scheduling es Feature
005). Ejecuta `purge_expired_self_study_data` (data-model.md → "Retención y purga")
sobre sesiones en estado `authorized_expiring` (plazo cumplido) o
`not_authorized_purge_eligible` **únicamente** (research.md §12.1/§12.2) — alcance de
eliminación acotado por `event_type` (ver regla más arriba), no la sesión completa.
**MUST NUNCA** purgar una sesión `undecided_preexisting` o
`invalid_authorized_without_policy`, sin importar cuántas veces se invoque este
endpoint — eso sería tratar la repetición de la invocación como si fuera el
consentimiento humano que FR-028a exige, lo cual queda expresamente prohibido.

**Response `200`**:
```json
{
  "sessions_matching_criteria": "int (renombrado desde sessions_evaluated — estable o creciente entre ejecuciones sucesivas)",
  "sessions_with_rows_deleted": "int (renombrado desde sessions_purged — filas eliminadas EN ESTA ejecución; 0 en una repetición no implica que la sesión dejó de cumplir el criterio)",
  "practice_questions_deleted": "int",
  "coherence_incidents_deleted": "int",
  "trace_events_deleted": "int"
}
```

**Regla**: elimina únicamente `PracticeQuestion`, `CoherenceIncident` y los
`TraceEvent` cuyo `event_type` ∈ {`generation_call`, `non_disclosure_check`,
`verification_combined`, `study_session_summary`, `agents_selected`} de las sesiones
expiradas — nunca `session_started`/`session_closed`/`technical_summary` (mecanismo de
sesión de la Feature 001, `turn_id = null`) ni `agent_execution`/`turn_completed`/
`constitutional_block` (`event_type` compartido literalmente con la Feature 001 —
verificación de nombres, research.md §12) ni ninguna tabla propia de la Feature 002
(`GroundingVerificationResult`/`Evidence`/`MaterialConflictRecord`, confirmado sin
escritura desde esta feature). Una sesión cuya actividad no tiene asociada una
`RetentionPolicy` con `retention_days` finito se trata como ya expirada para este
criterio (FR-028a, research.md §12) — no como exenta —, salvo que aparezca primero en el
informe previo de configuraciones preexistentes incompatibles (research.md §12).
