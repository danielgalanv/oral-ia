# Contrato interno: Agent / AgentContract / mensajería

Este contrato es el "protocolo" que todo agente registrado en el catálogo MUST implementar
(FR-004, FR-007). Es un contrato interno del proceso, no una API pública externa.

## AgentDescriptor (catálogo)

```text
AgentDescriptor:
  id: UUID
  name: string
  version: string (semver)
  contract: AgentContract
  capabilities: string[]
  availability_status: "available" | "unavailable" | "degraded"
```

## AgentContract

```text
AgentContract:
  agent_id: string
  version: string (semver)
  purpose: string
  input_schema_ref: string
  output_schema_ref: string
  preconditions: string[]
  postconditions: string[]
  allowed_sources: string[]
  allowed_tools: string[]
  permissions: string[]
  timeout_ms: int
  expected_cost: string
  possible_errors: string[]
  confidence_semantics: string
  success_criteria: string[]
  cancellation_policy: string
  trace_fields: string[]
```

## Interfaz asíncrona común de ejecución

Todo agente se invoca mediante la misma forma, independientemente de su implementación
interna (regla determinista, heurística o, en features futuras, un LLM):

```text
async execute(request: AgentRequest, cancellation: CancellationToken) -> AgentResult
```

```text
AgentRequest:
  session_id: UUID
  turn_id: UUID
  input: json                # forma validada contra input_schema_ref
  context: json               # subconjunto mínimo del CognitiveState necesario (nunca el estado completo sin filtrar)
  deadline_ms: int

CancellationToken:
  is_cancelled(): bool
  on_cancel(callback): void

AgentResult:
  status: "ok" | "error" | "timeout" | "cancelled"
  output: json | null         # forma validada contra output_schema_ref si status == "ok"
  confidence: float [0,1] | null
  error: AgentError | null
  trace: json                 # solo campos declarados en trace_fields

AgentError:
  code: string
  message: string
  recoverable: bool
```

**Reglas**:
- Un agente MUST NOT recibir acceso indiscriminado a toda la base de datos o al estado
  completo; solo el `context` que el orquestador decide pasarle.
- Si `deadline_ms` se supera, el orquestador MUST tratar el resultado como `status = "timeout"`
  y aplicar la degradación controlada (FR-018), sin aplicar ningún `output` parcial al estado.
- `AgentResult.trace` MUST NOT contener cadenas de razonamiento privadas del modelo
  (FR-024); solo resultados estructurados y justificaciones observables.

## InternalMessage

```text
InternalMessage:
  id: UUID
  session_id: UUID
  turn_id: UUID
  sender_agent_id: UUID
  receiver_agent_id: UUID
  type: string
  objective: string
  content: json
  evidences: string[]
  sources: string[]
  confidence: float [0,1]
  priority: int
  valid_until: datetime | null
  expected_response: string
  success_condition: string
```

## AgencyDefinition / ExecutionStep

```text
AgencyDefinition:
  id: UUID
  name: string
  version: string
  steps: ExecutionStep[]
  verifiers_required: UUID[]   # subconjunto de steps
  fallback_step: UUID | null
  termination_rule: string

ExecutionStep:
  step_id: UUID
  agent_id: UUID
  role: "retriever" | "generator" | "verifier" | "decider" | "presenter"
  depends_on: UUID[]           # steps previos requeridos
  parallelizable: bool
```

**Regla de separación (Principio IV)**: un `ExecutionStep` con `role = "generator"` MUST NOT
también actuar como `role = "verifier"` para su propia salida dentro de la misma `Agency`.

## VerificationResult

```text
VerificationResult:
  proposal_id: UUID
  verifier_agent_id: UUID
  verdict: "approved" | "reformulate" | "clarify" | "block"
  reasons: string[]
```

## DialogueAction

```text
DialogueAction:
  turn_id: UUID
  action_type: "respond" | "ask" | "re_ask" | "clarify" | "acknowledge_missing_info" | "summarize" | "finish"
  chosen_by_agent_id: UUID
```

## Adenda T090 — especialización de ConstitutionalControl (2026-10-13)

El contrato común `AgentRequest` permanece; para este agente, `input` porta la propuesta final estructurada y `context` una instantánea mínima de autoridad creada por el orquestador, conforme a `constitutional-output.md`. No se entrega un objeto de base de datos ni el estado cognitivo completo. `AgentResult.output` incluye veredicto y códigos de causa estructurados. El llamador debe tratar resultado ausente, error y timeout como bloqueo. La solicitud heredada que solo contiene `input.proposal_text` no puede obtener autorización final FR-014; la función textual `evaluate(str)` queda reservada a H02 y a sus pruebas históricas. El cambio de versión del contrato constitucional es incompatible para sus consumidores y requiere migrar ambas rutas de orquestación y sus fallbacks antes de activarlo.

### Corrección de persistencia T090 (2026-10-13)

`AuthorizationVerdict` es el valor interno devuelto por el control, **no** una entidad nueva. El orquestador escribe exactamente un `VerificationResult` final con `verdict=approved|block`; no altera los cuatro valores permitidos del contrato general (`approved`, `reformulate`, `clarify`, `block`). `reasons` es `list[str]` de códigos de causa en precedencia determinista; una columna nullable `authorization_context` JSON guarda identidad/versión/huella de actividad, política y plantilla del intento final. Los intentos 0 y 1 se trazan por separado en `TraceEvent`; el primer bloqueo no se pierde cuando se autoriza una alternativa. Grounding y coherencia no alimentan este veredicto constitucional. Véase `constitutional-output.md` §«Corrección de diseño T090».
