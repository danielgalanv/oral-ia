# Contrato API: área técnica / docente

API HTTP local (`127.0.0.1` — FR-022), consumida por `apps/web` (`/tecnica`). En esta
feature NO exige credencial (FR-021a): el punto de extensión de autenticación existe pero
está deshabilitado por defecto; su activación llega con la feature de configuración
docente, revisión y privacidad. Un middleware de autenticación no-op MUST quedar ya
conectado en la cadena de peticiones para que activarlo después no requiera reestructurar
rutas.

## `POST /api/v1/activities`

Crea una nueva versión de configuración de actividad (FR-001, FR-002).

**Request**: campos de `ActivityConfiguration` (ver `data-model.md`), sin `id`, `version`
(se asigna automáticamente) ni `immutable_since`.

**Response `201`**: la fila `ActivityConfiguration` creada, con `version = 1` (o
`version + 1` si `family_id` se reutiliza explícitamente para editar un borrador aún no
inmutable).

**Errores**:
- `409` — se intenta modificar una `ActivityConfiguration` con `immutable_since` no nulo
  (FR-002); el cliente MUST crear una nueva versión en su lugar.

## `GET /api/v1/catalog/agents`

Lista el catálogo de agentes (FR-003).

**Response `200`**: `AgentDescriptor[]` (ver `contracts/agent-contract.md`).

## `GET /api/v1/catalog/agencies`

Lista el catálogo de agencias (FR-003, FR-006).

**Response `200`**: `AgencyDefinition[]` (ver `contracts/agent-contract.md`) más
`availability_status` (`available`/`unavailable`/`degraded`) por agencia — FR-003 exige
exponer el estado de disponibilidad tanto de agentes como de agencias (ver
`data-model.md` → Agency).

## `GET /api/v1/sessions`

Lista sesiones, activas e históricas (US6, FR-020).

**Query params**: `status` (opcional), `activity_id` (opcional).

**Response `200`**: lista resumida de `Session` (sin el detalle completo de turnos).

## `GET /api/v1/sessions/{session_id}`

Detalle completo de una sesión, incluida si está activa (Edge Case: inspección sin
interrumpir).

**Response `200`**:
```json
{
  "session": { "...": "campos de Session" },
  "activity_configuration": { "...": "versión exacta usada" },
  "turns": [ { "...": "campos de Turn, DialogueAction, VerificationResult" } ],
  "technical_summary": { "...": "solo si status != active" }
}
```

## `GET /api/v1/sessions/{session_id}/trace`

Reconstrucción completa de trazabilidad (FR-016, FR-020, SC-004).

**Response `200`**: `TraceEvent[]` y `StatePatch[]` (incluidos los rechazados por
conflicto — US5), ordenados cronológicamente, suficientes para reconstruir la secuencia
completa de un turno o de la sesión entera tras un reinicio de la aplicación.
