# Data Model: Núcleo cognitivo y ejecución local

Entidades acotadas al alcance de la Feature 001 (ver `spec.md` → Key Entities). Se excluyen
deliberadamente entidades de `docs/ORAL-IA_SpecKit/14_domain_model.md` que pertenecen a
features posteriores: `MaterialDocument`, `MaterialFragment`, `Evidence` (recuperación real),
`Transcript`, `TranscriptCorrection`, `KLine`, `ConsentRecord` (formal), `ExperimentRun`.

Cada entidad indica: campos, tipo, reglas de validación derivadas de los requisitos, y
transiciones de estado cuando aplican. `Memory` no es una tabla propia: se implementa como un
campo `memory_category` (enum: `working | episodic | semantic | procedural | metacognitive`)
en los registros de `CognitiveState`, `StatePatch` y `TraceEvent` que lo requieran.

## Course

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| name | string | |
| subject_code | string | asignatura; no matrícula ni expediente (Principio I) |
| created_at | datetime | |

Relación: 1 Course → N ActivityConfiguration (por `family_id`).

## RetentionPolicy

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| version | int | versionado independiente (FR-001) |
| content_scope | enum | qué contenido cubre |
| retention_days | int \| null | null = indefinido hasta purga manual |
| access_scope | enum | quién puede consultar |
| purge_rule | string | regla operativa de purga |

## ActivityConfiguration

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK de esta versión concreta |
| family_id | UUID | agrupa versiones de "la misma" actividad |
| version | int | monotónico dentro de `family_id` |
| course_id | UUID (FK Course) | |
| name, subject, objective, mode, language | string | FR-001 |
| max_turns | int | FR-001 |
| max_duration_seconds | int | FR-001 |
| general_knowledge_allowed | bool | default `false` (Principio V) |
| required_agent_ids, optional_agent_ids | list[UUID] | referencian Agent.id vigentes |
| retention_policy_id | UUID (FK RetentionPolicy) | |
| immutable_since | datetime \| null | se fija en el primer uso por una Session (FR-002) |
| created_at | datetime | |

**Validación**: no se permite `UPDATE` de una fila con `immutable_since` no nulo; cualquier
cambio crea una nueva fila con `version + 1` sobre el mismo `family_id` (FR-002).

**Transición de estado**: `Draft` (`immutable_since = null`) → `Immutable` (al asociarse a la
primera `Session`).

## ParticipantCode

| Campo | Tipo | Notas |
|---|---|---|
| code | string | PK; patrón seudónimo validado, sin PII (FR-023) |
| created_at | datetime | |

**Validación**: rechazar formatos que parezcan nombre real (heurística simple: sin espacios
múltiples tipo "Nombre Apellido", sin coincidencia con formato de email) — ver Edge Cases.

## AgentContract

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| agent_id | string | identificador lógico del agente |
| version | string (semver) | FR-004 |
| purpose | string | |
| input_schema_ref, output_schema_ref | string | referencia a esquema Pydantic versionado |
| preconditions, postconditions | list[string] | |
| allowed_sources, allowed_tools | list[string] | |
| permissions | list[string] | |
| timeout_ms | int | |
| expected_cost | string | descripción de consumo esperado |
| possible_errors | list[string] | |
| confidence_semantics | string | cómo se interpreta la confianza declarada |
| success_criteria | list[string] | |
| cancellation_policy | string | |
| trace_fields | list[string] | qué campos deben quedar en TraceEvent |

## Agent

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK, catálogo |
| name | string | |
| version | string | |
| contract_id | UUID (FK AgentContract) | |
| capabilities | list[string] | |
| availability_status | enum(`available`,`unavailable`,`degraded`) | FR-003 |
| registered_at | datetime | |

**Validación de éxito (SC-001)**: deben poder coexistir ≥5 registros `Agent` distintos que
referencian contratos con la misma forma (`AgentContract` shape) sin cambios en
`orchestration/`.

## Agency

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| name | string | |
| version | string | |
| steps | list[ExecutionStep] | ver contrato en `contracts/agent-contract.md` |
| verifiers_required | list[UUID] | subconjunto de `steps` marcados obligatorios |
| fallback_step | UUID \| null | paso alternativo ante fallo (FR-018) |
| termination_rule | string | condición de fin de agencia |
| availability_status | enum(`available`,`unavailable`,`degraded`) | FR-003 — expuesto en el catálogo igual que en `Agent` |

**Validación de éxito (SC-002)**: deben poder coexistir ≥2 `Agency` que reutilicen los
mismos `Agent.id` en distinto orden/combinación.

## Session

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| activity_configuration_id | UUID (FK ActivityConfiguration, versión fija) | |
| participant_code | string (FK ParticipantCode) | |
| status | enum(`active`,`closed_voluntary`,`closed_limit_reached`,`closed_error_safe`) | |
| started_at, ended_at | datetime | |
| turn_count | int | |
| is_active_lock | bool | único `true` por instancia (FR-012a) — restricción de unicidad |
| technical_summary_ref | UUID \| null | referencia al resumen técnico (FR-012b), visible solo en área técnica |

**Transición de estado**: `active` → `closed_voluntary` (US2), `active` →
`closed_limit_reached` (Edge Case: límite de turnos/duración), `active` →
`closed_error_safe` (US4, fallo no recuperable).

**Restricción**: a lo sumo una fila `Session` con `is_active_lock = true` en toda la base
(constraint de unicidad parcial), aplicando la decisión de investigación §3.

## Turn

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK Session) | |
| index | int | orden dentro de la sesión |
| input_text | string | |
| generated_proposal_id | UUID \| null (FK GeneratedProposal) | |
| verification_result_id | UUID \| null (FK VerificationResult) | |
| dialogue_action_id | UUID \| null (FK DialogueAction) | |
| output_text | string \| null | solo si no bloqueado |
| status | enum(`completed`,`blocked`,`degraded`,`failed`) | |
| started_at, ended_at | datetime | |
| latency_ms, resource_usage | int, json | métricas (FR-017) |

## InternalMessage

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id, turn_id | UUID (FK) | |
| sender_agent_id, receiver_agent_id | UUID | |
| type, objective | string | |
| content | json | |
| evidences, sources | list[string] | vacío en esta feature (sin materiales reales) |
| confidence | float [0,1] | |
| priority | int | |
| valid_until | datetime \| null | |
| expected_response, success_condition | string | |
| created_at | datetime | |

## CognitiveState

| Campo | Tipo | Notas |
|---|---|---|
| session_id | UUID (FK Session) | PK, 1:1 con la sesión (estado "actual") |
| version | int | contador monotónico (§1 research) |
| mode, objective, activity_ref | string | |
| permitted_materials | list[string] | vacío en esta feature |
| current_input, participant_response | string | |
| concepts_addressed, concepts_pending | list[string] | |
| intent_hypotheses | list[string] | |
| retrieved_info | list[string] | vacío en esta feature |
| open_questions | list[string] | |
| summarized_history | string | |
| remaining_time, turn_number | int | |
| incidents | list[string] | |
| confidence | float [0,1] | |
| next_action_proposed | string | |
| updated_at | datetime | |

Cada elemento anterior se etiqueta, en el `StatePatch` que lo introdujo, con su tipo
(`instruction | observation | participant_statement | retrieved_info | hypothesis |
inference | decision | check_result | configuration`) — FR-009.

## StatePatch

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK Session) | |
| base_version, resulting_version | int \| null | `resulting_version = null` si `applied = false` |
| proposed_by_agent_id | UUID | |
| payload | json (diff) | |
| element_type | enum | ver tipos FR-009 arriba |
| justification | string | |
| applied | bool | |
| rejected_reason | string \| null | obligatorio si `applied = false` (FR-019) |
| created_at | datetime | |

**Regla de conflicto**: `applied = true` únicamente si, en el instante de escritura,
`CognitiveState.version == base_version`; en ese caso `CognitiveState.version` pasa a
`resulting_version` de forma atómica. Toda propuesta se persiste, aplicada o no (US5).

## GeneratedProposal

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| turn_id | UUID (FK Turn) | |
| generator_agent_id | UUID | |
| content | json | candidata, no autorizada todavía |
| created_at | datetime | |

## VerificationResult

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| proposal_id | UUID (FK GeneratedProposal) | |
| verifier_agent_id | UUID | distinto del `generator_agent_id` (Principio IV) |
| verdict | enum(`approved`,`reformulate`,`clarify`,`block`) | |
| reasons | list[string] | observables, no cadenas de razonamiento privadas (FR-024) |
| created_at | datetime | |

**Validación**: si `verdict = block`, `Turn.status = blocked` y `Turn.output_text = null`
(FR-015).

**Limitación técnica documentada (research.md §8, estabilización 2026-09-10)**: el
clasificador constitucional es un detector determinista de patrones léxicos conocidos, no
un verificador semántico — `reasons` refleja qué regla concreta coincidió, no una garantía
de que ninguna salida prohibida pueda evadirlo. La matriz de aceptación de research.md §8
acota qué casos concretos MUST bloquearse tras la tarea de refuerzo pendiente.

## DialogueAction

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| turn_id | UUID (FK Turn) | |
| action_type | enum(`respond`,`ask`,`re_ask`,`clarify`,`acknowledge_missing_info`,`summarize`,`finish`) | FR-013 |
| chosen_by_agent_id | UUID | |
| created_at | datetime | |

## TraceEvent

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| session_id | UUID (FK Session) | |
| turn_id | UUID \| null (FK Turn) | null para eventos a nivel de sesión |
| event_type | enum | ejecución, decisión, cambio de estado, error, bloqueo, recurso |
| agent_id | UUID \| null | |
| payload | json | resultados estructurados, nunca razonamiento privado (FR-024) |
| latency_ms | int \| null | |
| resource_usage | json \| null | CPU/memoria básicos (FR-017) |
| memory_category | enum | working/episodic/semantic/procedural/metacognitive |
| created_at | datetime | |

## Relaciones clave (resumen)

```text
Course 1─N ActivityConfiguration(family_id) N─1 RetentionPolicy
ActivityConfiguration 1─N Session N─1 ParticipantCode
Session 1─N Turn
Session 1─1 CognitiveState
Session 1─N StatePatch
Turn 1─1 GeneratedProposal 1─1 VerificationResult
Turn 1─1 DialogueAction
Session/Turn 1─N InternalMessage
Session/Turn 1─N TraceEvent
AgentContract 1─N Agent
Agent N─N Agency (a través de ExecutionStep, ver contracts/agent-contract.md)
```

## Adenda T090 — modelo lógico (2026-10-13)

Este modelo extiende el histórico sin declarar T090 implementada. El contrato detallado está en `contracts/constitutional-output.md`.

| Concepto | Ubicación lógica | Identidad, relaciones y validaciones |
|---|---|---|
| `OutputAuthorizationPolicy` | Valor embebido en una versión de `ActivityConfiguration` | `policy_id`, `policy_version`, versión de esquema, destinatarios, reglas explícitas categoría/procedencia/destinatario, temas/propósitos/acciones, permiso de conocimiento general y IDs de mensajes operativos; obligatorio para autorizar; congelado con la configuración al usarse. Sin tabla nueva. |
| `AuthorizationSnapshot` | Dato efímero filtrado por el orquestador hacia el control | ID/versión de configuración y política, destinatario real, reglas aplicables y mapa de referencias confiables con tipo, procedencia, valor o huella verificable y alcance. No es una copia de base de datos ni una declaración del generador. |
| `OutputProposal` | Entrada versionada del verificador | Texto exacto final, tipo de mensaje, ID/versión de plantilla confiable, segmentos con intervalos sobre ese texto y referencias de datos/tema/propósito/acción; origen del constructor. Texto sin vinculación completa: bloqueo. |
| `AuthorizationVerdict` | Resultado del control, asociado a `VerificationResult`/`TraceEvent` | `approved`/`block`, códigos de causa, ID/versión de política y configuración, ID de plantilla, número de intento de fallback. Trazas sin valores ni texto sensible. |
| `OperationalMessageCatalog` | Catálogo interno versionado en código | ID estable, texto o plantilla exacta sin datos de sesión, propósito y acción operativos. Solo entradas incluidas explícitamente en política; no constituye autorización por sí mismo. |

**Ciclo**: actividad borrador → política validada → actividad inmutable al primer uso → instantánea filtrada por turno → propuesta normal → veredicto; si bloqueo, registrar y evaluar una sola propuesta operativa; si segundo bloqueo, turno sin `output_text`. Cambiar política requiere nueva versión de actividad. La migración futura añade un valor nullable de política para filas antiguas; `NULL` y esquemas desconocidos producen `missing_policy`/`invalid_context`, nunca permiso implícito. El formato físico elegido se precisa a continuación; su implementación corresponde solo a T090.

### Corrección de representación física T090 (2026-10-13)

`ActivityConfiguration` añade `output_authorization_policy_json: Mapped[str | None]` con SQLAlchemy `Text`, `nullable=True`, persistido como SQLite `TEXT`, y `output_authorization_policy_sha256: Mapped[str | None]` con `String(64)`, `nullable=True`. El JSON es **texto canónico**, no un diccionario mutable del ORM. Incluye `schema_version=1`, `policy_id`, `policy_version`, permisos cerrados y referencias `(id, version)` a plantillas normales y mensajes operativos. El modelo de validación futuro es Pydantic v2 `OutputAuthorizationPolicy` con `ConfigDict(frozen=True, extra='forbid')`, tipos estrictos y colecciones inmutables/normalizadas antes de serializar; comprueba identificadores/versiones, unicidad de reglas, destinatarios, triples y consistencia del permiso de conocimiento general con `ActivityConfiguration.general_knowledge_allowed` (el permiso efectivo es la conjunción). Serialización determinista desde `model_dump(mode='json')` con claves y conjuntos ordenados, separadores fijos, `ensure_ascii=False`, `allow_nan=False`, sin normalizar Unicode; SHA-256 del UTF-8 exacto del texto canónico. Al cargar, volver a validar esquema, canonicidad y hash antes de construir una instantánea; discrepancia → `invalid_context`.

El campo es obligatorio en `ActivityConfigurationInput` para **nuevas** configuraciones tras T090 y se valida antes de `create_activity`/flush; los factories, `seed_demo.py`, fixtures `seeded_activity`/`self_study_activity` y creaciones directas en pruebas deben aportar política mínima explícita. Para filas históricas, Alembic agrega ambas columnas nullable sin backfill permisivo: `NULL`/`NULL` → `missing_policy`; solo una de las dos poblada, JSON inválido, hash erróneo o esquema desconocido → `invalid_context`. No se agrega columna para `Turn.output_text`: ya es nullable en `src/oralia/infrastructure/db/models.py`. Sí se agrega `VerificationResult.authorization_context: Mapped[dict | None]` con SQLAlchemy `JSON`, nullable, para las identidades/versiones/huellas de la evaluación final; `reasons` existente conserva los códigos ordenados como `list[str]`. Las filas históricas mantienen `authorization_context=NULL` sin reinterpretar su veredicto.

La política se expone a lógica de dominio solo como valor Pydantic inmutable recién validado: no se muta el JSON internamente ni se mantiene una referencia compartida a un diccionario. Al iniciar sesión se inmoviliza la configuración según FR-002; un guardia de escritura y un trigger SQLite `BEFORE UPDATE OF output_authorization_policy_json, output_authorization_policy_sha256` rechazan cambio si `OLD.immutable_since IS NOT NULL`, incluso si se reasigna un string entero; la transacción de creación/versionado verifica la regla. Recalcular hash al uso detecta también manipulación posterior o corrupción. Ninguna mutación interna de un dict decodificado cambia la columna persistida ni la instantánea ya congelada; cada evaluación recarga/valida su propio valor. Una nueva política requiere **nueva fila de actividad**, nunca editar la versión utilizada.

Para rehabilitar una actividad histórica sin política: identificar su configuración y sesiones, crear por vía administrativa una **nueva versión** de la misma familia con política docente mínima explícita y referencias de catálogo vigentes, validar/guardar/hash, y dirigir solo sesiones nuevas a su nuevo `id`. Las sesiones existentes siguen ligadas al `activity_configuration_id` anterior y cierran en seguro hasta que haya un proceso autorizado de transición; no se reescribe una configuración ya usada ni se derivan permisos de `objective`. La vía actual `create_activity(family_id=...)` rechaza versionar si la última versión es inmutable, por lo que T090 debe añadir una operación explícita de sucesión inmutable, con copia controlada de los demás campos y nueva versión, sin debilitar la prohibición de editar la fila anterior.

`AuthorizationVerdict` es un valor interno, no una tabla. Un único `VerificationResult` persiste el veredicto constitucional final `approved`/`block`; conserva los otros valores contractuales `reformulate`/`clarify` para otros usos. El intento inicial rechazado y el único fallback se registran como dos `TraceEvent` de evaluación (intentos 0 y 1), nunca como dos veredictos finales del turno. Cuando la alternativa se aprueba, el turno queda `degraded` con texto visible; cuando se bloquea también, `blocked` con `output_text=NULL`. Las identidades finales residen en `authorization_context`, y la traza histórica de cada intento en `TraceEvent.payload`, sin texto rechazado ni valores sensibles.
