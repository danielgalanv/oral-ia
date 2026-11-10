# Contrato API: área de participante

API HTTP local (vinculada a `127.0.0.1` por defecto — FR-022), consumida por `apps/web`
(`/participante`). Sin autenticación (Principio VII: sin identidad real; solo código
seudónimo). Content-Type `application/json` salvo que se indique otra cosa.

## `POST /api/v1/sessions`

Inicia una sesión (FR-010, FR-012a).

**Request**:
```json
{
  "participant_code": "string (patrón seudónimo)",
  "activity_configuration_id": "uuid"
}
```

**Response `201`**:
```json
{
  "session_id": "uuid",
  "ai_disclosure": "string — aviso explícito de que es un sistema automático",
  "activity": { "name": "string", "objective": "string", "max_turns": 0, "max_duration_seconds": 0 }
}
```

**Errores**:
- `404` — actividad no existe o no autorizada (Edge Case).
- `409` — ya existe una sesión interactiva activa en esta instancia (FR-012a).
- `422` — `participant_code` no es un seudónimo válido o parece identificar a una persona
  real (Edge Case, FR-023).

## `POST /api/v1/sessions/{session_id}/turns`

Envía un turno de texto (FR-012, FR-013).

**Request**:
```json
{ "text": "string" }
```

**Response `200`** (no bloqueado):
```json
{
  "turn_id": "uuid",
  "dialogue_action": "respond | ask | re_ask | clarify | acknowledge_missing_info | summarize | finish",
  "output_text": "string",
  "state_version": 0
}
```

**Response `200`** (bloqueado por control constitucional — FR-015):
```json
{
  "turn_id": "uuid",
  "dialogue_action": "clarify",
  "output_text": "string — mensaje seguro, sin revelar contenido prohibido",
  "blocked": true
}
```

**Errores**:
- `404` — sesión inexistente o ya cerrada.
- `409` — conflicto de versión de estado detectado y no resuelto en reintentos internos
  (caso extremo de US5; el servicio reintenta antes de exponer este error).
- `503` — fallo/timeout de agente no recuperable en este turno tras degradación (US4); la
  sesión puede continuar o queda cerrada con `status = closed_error_safe`.

## `POST /api/v1/sessions/{session_id}/end`

Finaliza la sesión voluntariamente (FR-012, FR-012b).

**Response `200`**:
```json
{ "session_id": "uuid", "status": "closed_voluntary", "confirmation_message": "string" }
```

No devuelve el resumen técnico completo (FR-012b) — ese resumen solo es accesible vía la
API técnica (`contracts/api-tecnica.md`).

## `GET /api/v1/activities/{activity_id}`

Consulta pública mínima de una actividad autorizada (para mostrar objetivo/idioma antes de
iniciar sesión). No expone campos administrativos internos (agentes obligatorios/opcionales,
política de conservación).

**Response `200`**:
```json
{ "id": "uuid", "name": "string", "objective": "string", "mode": "string", "language": "string" }
```

## Adenda T090 — finalización segura sin contenido (2026-10-13)

La respuesta histórica de bloqueo muestra un mensaje seguro; FR-015 aclarado admite `output_text: null` cuando la única alternativa operativa no pasa la verificación independiente. En el contrato de respuesta de turno T090, `output_text` pasa a `string | null`: `string` solo si el texto final se autorizó; `null` en cierre seguro sin contenido. `blocked: true` y un `dialogue_action` de finalización siguen indicando el resultado sin exponer la causa sensible. Clientes y pruebas deben aceptar ambos estados. Esta adenda planifica un cambio de contrato; la API actual aún no lo implementa.

### Corrección de compatibilidad T090 (2026-10-13)

La columna persistida `Turn.output_text` **ya admite SQL `NULL`**; el cambio afecta a `TurnResult.output_text`, `StudyTurnResult.output_text`, la respuesta de ambos routers de turno, tipos TypeScript y vistas que hoy presuponen `string`. `output_text: null` se emite solo si el único fallback no se autoriza; no se sustituye por `SAFE_BLOCKED_MESSAGE` ni una cadena vacía. Si la propuesta inicial se bloquea pero la alternativa operativa se aprueba, `blocked: true` describe el rechazo inicial, `output_text` contiene exclusivamente la alternativa autorizada y la verificación constitucional final es `approved`. La salida normal autorizada lleva texto visible y no necesita un eco libre del participante. El cliente no crea una burbuja de respuesta cuando recibe `null`.
