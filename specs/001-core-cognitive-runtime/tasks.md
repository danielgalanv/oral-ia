---

description: "Task list for Núcleo cognitivo y ejecución local"
---

# Tasks: Núcleo cognitivo y ejecución local

**Input**: Design documents from `specs/001-core-cognitive-runtime/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: incluidas. Aunque la especificación no las pide de forma explícita, la
constitución (Principio X) y `docs/ORAL-IA_SpecKit/13_definition_of_done.md` exigen pruebas
de contrato por agente, integración por agencia, un extremo a extremo por flujo prioritario,
y pruebas de fallo/timeout/conflicto/bloqueo como condición de "hecho" de la feature.

**Organization**: Tareas agrupadas por historia de usuario (US1–US6 de `spec.md`) para
permitir implementación y prueba independientes de cada una.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias pendientes)
- **[Story]**: Historia de usuario a la que pertenece (US1–US6)
- Cada tarea incluye la ruta de archivo exacta

## Path Conventions

Estructura de `plan.md` → Project Structure: monolito modular `src/oralia/` (domain /
application / infrastructure / interfaces), `apps/api` (entrypoint), `apps/web` (cliente
mínimo), `tests/{unit,contract,integration,e2e,failure}`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: inicialización del proyecto y estructura básica

- [X] T001 Create repository project skeleton (`apps/api/`, `apps/web/`, `src/oralia/`, `tests/`) per `plan.md` → Project Structure
- [X] T002 Initialize Python 3.12 project with `uv` in `pyproject.toml` (FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, `structlog`, `psutil`, `pytest`, `pytest-asyncio`)
- [X] T003 [P] Configure Python linting/formatting (ruff + black) in `pyproject.toml`
- [X] T004 [P] Initialize `apps/web` with Vite + React + TypeScript, configure eslint/prettier
- [X] T005 [P] Configure `pytest`/`pytest-asyncio` markers and test discovery in `pyproject.toml`
- [X] T006 [P] Configure Playwright for e2e tests in `tests/e2e/playwright.config.ts`
- [X] T007 Configure Alembic pointing at the SQLite WAL engine in `src/oralia/infrastructure/db/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: infraestructura central que MUST estar completa antes de cualquier historia de
usuario (persistencia, contratos de agente, versionado de estado, trazabilidad)

**⚠️ CRITICAL**: ninguna historia de usuario puede empezar hasta completar esta fase

- [X] T008 Define SQLAlchemy models for all entities in `data-model.md` in `src/oralia/infrastructure/db/models.py`
- [X] T009 Generate initial Alembic migration for all entities in `src/oralia/infrastructure/db/migrations/versions/0001_initial.py`
- [X] T010 [P] Define `AgentRequest`/`AgentResult`/`AgentError`/`CancellationToken` Pydantic schemas per `contracts/agent-contract.md` in `src/oralia/domain/agents/agent_contract.py`
- [X] T011 [P] Define `AgentContract`/`AgentDescriptor` Pydantic schemas in `src/oralia/domain/agents/agent.py`
- [X] T012 [P] Define `InternalMessage` Pydantic schema in `src/oralia/domain/messages/internal_message.py`
- [X] T013 [P] Define `AgencyDefinition`/`ExecutionStep` Pydantic schemas in `src/oralia/domain/agencies/agency.py`
- [X] T014 Implement async agent execution wrapper with timeout/cancellation in `src/oralia/application/orchestration/cancellation.py`
- [X] T015 Implement `CognitiveState`/`StatePatch` optimistic-versioning apply engine (compare base_version, atomic write) in `src/oralia/domain/cognitive_state/cognitive_state.py` and `state_patch.py` (research.md §1)
- [X] T016 Implement `TraceEvent` logging service (structlog-backed) in `src/oralia/application/services/trace_service.py`
- [X] T017 Implement single-active-session lock service in `src/oralia/application/services/session_lock_service.py` (research.md §3, FR-012a)
- [X] T018 Implement resource monitor (CPU/memory/timeouts via `psutil`) in `src/oralia/infrastructure/telemetry/resources.py`
- [X] T019 Create FastAPI app skeleton bound to `127.0.0.1`, with router registration and a no-op auth middleware extension point in `src/oralia/interfaces/api/app.py` and `src/oralia/interfaces/api/deps/auth_stub.py` (FR-021a, FR-022)
- [X] T020 Wire `apps/api/main.py` entrypoint (uvicorn) importing `src/oralia/interfaces/api/app.py`

**Checkpoint**: infraestructura fundacional lista — las historias de usuario pueden empezar

---

## Phase 3: User Story 1 - Configurar una actividad y consultar el catálogo (Priority: P1)

**Goal**: un profesor/administrador crea una configuración de actividad versionada y
consulta el catálogo de agentes y agencias disponibles

**Independent Test**: crear una configuración de actividad de prueba y consultar el
catálogo, sin que exista todavía ninguna sesión de participante

### Tests for User Story 1

- [X] T021 [P] [US1] Contract test for `POST /api/v1/activities` in `tests/contract/test_activities_post.py`
- [X] T022 [P] [US1] Contract test for `GET /api/v1/catalog/agents` in `tests/contract/test_catalog_agents.py`
- [X] T023 [P] [US1] Contract test for `GET /api/v1/catalog/agencies` in `tests/contract/test_catalog_agencies.py`

### Implementation for User Story 1

- [X] T024 [P] [US1] Create `RetentionPolicy` repository/service in `src/oralia/domain/sessions/retention_policy.py`
- [X] T025 [US1] Create `ActivityConfiguration` service with immutability enforcement (FR-002) in `src/oralia/application/commands/create_activity.py`
- [X] T026 [P] [US1] Create `Agent` catalog registration service in `src/oralia/application/commands/register_agent.py`
- [X] T027 [US1] Create `Agency` composition service (reuse existing agents only, no new code — FR-006) in `src/oralia/application/commands/register_agency.py`
- [X] T028 [US1] Implement catalog query service in `src/oralia/application/queries/get_catalog.py`
- [X] T029 [US1] Implement `POST /api/v1/activities` endpoint in `src/oralia/interfaces/api/routers/tecnica.py`
- [X] T030 [US1] Implement `GET /api/v1/catalog/agents` and `/agencies` endpoints in `src/oralia/interfaces/api/routers/tecnica.py`
- [X] T031 [US1] Write seed script creating ≥5 test agents under one `AgentContract` and ≥2 `Agency` compositions in `src/oralia/scripts/seed_demo.py` (SC-001, SC-002)
- [X] T032 [US1] Integration test: activity becomes immutable after first session use in `tests/integration/test_activity_immutability.py`
- [X] T033 [US1] Integration test: 5 agents under the same contract registered without orchestrator changes in `tests/integration/test_agent_catalog.py`
- [X] T034 [US1] Integration test: 2 agencies reuse the same agents in different order in `tests/integration/test_agency_composition.py`
- [X] T034a [US1] Integration test: swap a registered Agent for a contract-compatible replacement in an existing Agency, assert zero changes required in Agency or orchestrator code in `tests/integration/test_agent_substitution.py` (SC-008)
- [X] T035 [US1] Build área técnica UI screens for activity creation and catalog browsing in `apps/web/src/routes/Tecnica.tsx`

**Checkpoint**: User Story 1 funcional y probable de forma independiente

---

## Phase 4: User Story 2 - Completar una sesión con un turno trazable (Priority: P1) 🎯 MVP

**Goal**: un participante inicia sesión, envía un turno de texto, el sistema ejecuta el
flujo mínimo y registra todo, y finaliza voluntariamente

**Independent Test**: iniciar una sesión sobre una actividad ya configurada (US1), enviar
un turno y verificar que la sesión finaliza con confirmación y registro reconstruible

### Tests for User Story 2

- [X] T036 [P] [US2] Contract test for `POST /api/v1/sessions` in `tests/contract/test_sessions_post.py`
- [X] T036a [P] [US2] Contract test for `409` when starting a second interactive session while one is active in `tests/contract/test_sessions_conflict.py` (FR-012a)
- [X] T037 [P] [US2] Contract test for `POST /api/v1/sessions/{id}/turns` in `tests/contract/test_turns_post.py`
- [X] T038 [P] [US2] Contract test for `POST /api/v1/sessions/{id}/end` in `tests/contract/test_sessions_end.py`
- [X] T039 [P] [US2] Contract test for `GET /api/v1/activities/{id}` in `tests/contract/test_activities_get.py`

### Implementation for User Story 2

- [X] T040 [US2] Implement deterministic `Interpreter` agent behind `AgentContract` in `src/oralia/domain/agents/interpreter_agent.py` (research.md §2, no LLM real)
- [X] T041 [US2] Implement `DialogueAction` selector agent in `src/oralia/domain/validation/dialogue_action.py` (FR-013)
- [X] T042 [US2] Implement `TurnOrchestrator` (gestión de turno: interpretación → control constitucional → presentación) in `src/oralia/application/orchestration/turn_orchestrator.py`
- [X] T043 [US2] Implement Session lifecycle commands (`start_session`, `submit_turn`, `end_session`, enforcing FR-012a via `session_lock_service`) in `src/oralia/application/commands/start_session.py`, `submit_turn.py`, `end_session.py`
- [X] T043a [US2] Implement automatic session closure at turn/duration limit (`status = closed_limit_reached`) in `src/oralia/application/commands/end_session.py` (FR-011a)
- [X] T044 [US2] Implement technical summary generation (FR-012b, visible solo en área técnica) in `src/oralia/application/services/technical_summary_service.py`
- [X] T045 [US2] Implement participant-area API endpoints in `src/oralia/interfaces/api/routers/participante.py`
- [X] T046 [US2] Build área de participante UI (aviso de sistema automático, envío de turno, confirmación de cierre) in `apps/web/src/routes/Participante.tsx`
- [X] T047 [US2] Integration test: full turn round-trip increments `CognitiveState.version` (FR-008) in `tests/integration/test_turn_state_update.py`
- [X] T048 [US2] Integration test: turn sequence fully reconstructable from trace (FR-016) in `tests/integration/test_turn_trace_reconstruction.py`
- [X] T049 [US2] E2E test: Escenario A completo (inicio, turno, cierre, resumen técnico) per `quickstart.md` in `tests/e2e/test_scenario_a.spec.ts`
- [X] T049a [US2] Failure test: session auto-closes and still produces a technical summary when the turn/duration limit is reached in `tests/failure/test_session_limit_reached.py` (FR-011a)

**Checkpoint**: User Story 1 y 2 (MVP) funcionales de forma conjunta e independiente

---

## Phase 5: User Story 3 - Bloquear una salida académicamente prohibida (Priority: P2)

**Goal**: el control constitucional bloquea una salida que asigna nota, suplanta al
profesor o emite una decisión académica, antes de que llegue al participante

**Independent Test**: inyectar un agente de prueba que genere una propuesta prohibida y
verificar que nunca llega al participante

### Tests for User Story 3

- [X] T050 [P] [US3] Contract test for blocked `VerificationResult` shape in `tests/contract/test_verification_block.py`

### Implementation for User Story 3

- [X] T051 [US3] Implement `ConstitutionalControl` verifier agent (bloquea notas, decisiones académicas, datos no autorizados o fuera de alcance) in `src/oralia/domain/policies/constitutional_control.py` (FR-014)
- [X] T052 [US3] Wire `ConstitutionalControl` as a mandatory verifier step before presentation (Principio IV: el generador no aprueba su propia salida) in `src/oralia/application/orchestration/turn_orchestrator.py`
- [X] T053 [US3] Implement safe blocked-response generation (FR-015) in `src/oralia/domain/policies/constitutional_control.py`
- [X] T054 [US3] Failure test: agente de prueba propone nota/decisión académica → bloqueada antes de llegar al participante (Escenario B) in `tests/failure/test_constitutional_block.py`
- [X] T055 [US3] Failure test: causa del bloqueo queda registrada de forma trazable in `tests/failure/test_constitutional_block_trace.py`

**Checkpoint**: User Stories 1–3 funcionales de forma conjunta e independiente

---

## Phase 6: User Story 4 - Degradar de forma controlada ante el fallo de un agente (Priority: P2)

**Goal**: un timeout o una salida inválida de un agente se convierte en degradación
controlada, sin corromper el estado ni bloquear la sesión indefinidamente

**Independent Test**: forzar a un agente de prueba a superar su timeout o devolver un
objeto inválido, y verificar que el estado permanece consistente

### Implementation for User Story 4

- [X] T056 [US4] Implement per-agent timeout/deadline enforcement using `AgentRequest.deadline_ms` in `src/oralia/application/orchestration/cancellation.py`
- [X] T057 [US4] Implement output-schema validation and invalid-output handling in `src/oralia/application/orchestration/turn_orchestrator.py`
- [X] T058 [US4] Implement fallback/terminación segura per `AgencyDefinition.fallback_step` in `src/oralia/application/orchestration/agency_composer.py`
- [X] T059 [US4] Failure test: agente supera timeout → sin cambios parciales al estado (FR-018) in `tests/failure/test_agent_timeout.py`
- [X] T060 [US4] Failure test: agente devuelve salida inválida → incidencia trazable, última versión válida conservada in `tests/failure/test_agent_invalid_output.py`
- [X] T061 [US4] Failure test: sesión continúa o cierra de forma segura tras fallo gestionado in `tests/failure/test_session_safe_close.py`
- [X] T061a [US4] Failure test: constitutional control still runs on the fallback/degraded output path, never bypassed for resource savings in `tests/failure/test_degradation_constitutional_check.py` (FR-018a)

**Checkpoint**: User Stories 1–4 funcionales de forma conjunta e independiente

---

## Phase 7: User Story 5 - Evitar conflictos de escritura sobre el estado cognitivo (Priority: P3)

**Goal**: dos parches de estado concurrentes contra la misma versión no se sobrescriben
silenciosamente

**Independent Test**: disparar dos parches de estado concurrentes contra la misma versión
conocida y verificar que el sistema resuelve el conflicto sin pérdida silenciosa

### Implementation for User Story 5

- [X] T062 [US5] Implement `StatePatch` conflict-rejection path (`base_version` mismatch → persisted with `rejected_reason`, not applied) in `src/oralia/domain/cognitive_state/state_patch.py` (extiende T015)
- [X] T063 [US5] Failure test: dos patches con el mismo `base_version` simultáneos → solo uno aplicado, el otro rechazado y trazado in `tests/failure/test_state_conflict.py`
- [X] T064 [US5] Integration test: el historial de patches expone ambas operaciones (aplicada + rechazada) in `tests/integration/test_state_patch_history.py`

**Checkpoint**: User Stories 1–5 funcionales de forma conjunta e independiente

---

## Phase 8: User Story 6 - Reconstruir una sesión cerrada tras un reinicio (Priority: P3)

**Goal**: un investigador o mantenedor reconstruye configuración, turnos, agentes
ejecutados, decisiones y cambios de estado de una sesión cerrada tras reiniciar la app

**Independent Test**: reiniciar la aplicación después de haber cerrado al menos una
sesión y verificar que toda su secuencia se puede reconstruir desde los registros

### Tests for User Story 6

- [X] T065 [P] [US6] Contract test for `GET /api/v1/sessions` in `tests/contract/test_sessions_list.py`
- [X] T066 [P] [US6] Contract test for `GET /api/v1/sessions/{id}` in `tests/contract/test_sessions_get.py`
- [X] T067 [P] [US6] Contract test for `GET /api/v1/sessions/{id}/trace` in `tests/contract/test_sessions_trace.py`

### Implementation for User Story 6

- [X] T068 [US6] Implement session listing/detail/trace queries in `src/oralia/application/queries/get_session.py` and `reconstruct_session_trace.py`
- [X] T069 [US6] Implement `GET /api/v1/sessions`, `/{id}`, `/{id}/trace` endpoints in `src/oralia/interfaces/api/routers/tecnica.py`
- [X] T070 [US6] Build área técnica UI for historical session listing and detail in `apps/web/src/routes/Tecnica.tsx`
- [X] T071 [US6] Integration test: restart process and reconstruct a closed session (Escenario E) in `tests/integration/test_session_reconstruction_after_restart.py`

**Checkpoint**: todas las historias de usuario funcionales de forma independiente

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: mejoras que afectan a varias historias de usuario

- [X] T072 [P] Implement and verify keyboard navigation, accessible labels, contrast, and comprehensible error messages across `apps/web` (FR-025) per `checklists/accessibility.md`
- [X] T073 [P] Unit tests for `CognitiveState`/`StatePatch` versioning edge cases in `tests/unit/test_cognitive_state.py`
- [X] T074 [P] Unit tests for `ActivityConfiguration` immutability rules in `tests/unit/test_activity_configuration.py`
- [X] T075 Write installation/configuration/execution/testing/limitations documentation in `docs/` (Definition of Done)
- [X] T076 Run full `quickstart.md` validation end-to-end and record evidence
- [X] T077 Constitutional conformance self-review against `.specify/memory/constitution.md` Principios I–XI, documented in `specs/001-core-cognitive-runtime/`
- [X] T078 [P] Resource monitor smoke check (`psutil`-based) in `tests/unit/test_resource_monitor.py`
- [X] T079 Code cleanup and refactoring pass across `src/oralia`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias — puede empezar de inmediato
- **Foundational (Phase 2)**: depende de Setup — BLOQUEA todas las historias de usuario
- **User Story 1 (Phase 3)**: depende solo de Foundational
- **User Story 2 (Phase 4)**: depende de Foundational; usa `ActivityConfiguration`/catálogo de US1 en tiempo de ejecución (no en tiempo de compilación) — se recomienda completar US1 primero
- **User Story 3 (Phase 5)**: depende de Foundational y del `TurnOrchestrator` de US2
- **User Story 4 (Phase 6)**: depende de Foundational y del `TurnOrchestrator` de US2
- **User Story 5 (Phase 7)**: depende de Foundational (motor de versionado de T015); independiente de US2–US4 en el código, aunque conceptualmente se prueba sobre una sesión
- **User Story 6 (Phase 8)**: depende de Foundational y de que existan sesiones cerradas (US2) para tener algo que reconstruir
- **Polish (Phase 9)**: depende de todas las historias que se quieran pulir

### User Story Dependencies

- **US1 (P1)**: sin dependencias de otras historias
- **US2 (P1) 🎯 MVP**: funcionalmente requiere que exista al menos una `ActivityConfiguration` (US1) para poder iniciar sesión
- **US3 (P2)**: se integra en el `TurnOrchestrator` de US2; requiere US2 completada
- **US4 (P2)**: se integra en el `TurnOrchestrator` de US2; requiere US2 completada
- **US5 (P3)**: extiende el motor de estado de Foundational; se prueba sobre una sesión de US2
- **US6 (P3)**: consulta sesiones ya creadas por US2

### Within Each User Story

- Tests antes de la implementación correspondiente
- Modelos/servicios de dominio antes de comandos de aplicación
- Comandos de aplicación antes de endpoints de la API
- Endpoints antes de la UI que los consume
- Lógica principal antes de pruebas de integración/e2e/fallo

### Parallel Opportunities

- Todas las tareas [P] de Setup (T003–T006) en paralelo
- T010–T013 de Foundational en paralelo (esquemas Pydantic en archivos distintos)
- Dentro de US1: T021–T023 (contract tests) en paralelo; T024 y T026 en paralelo
- Dentro de US2: T036–T039 (contract tests) en paralelo
- Dentro de US6: T065–T067 (contract tests) en paralelo
- US3 y US4 pueden implementarse en paralelo por desarrolladores distintos una vez
  completada US2 (ambas extienden `TurnOrchestrator` pero en puntos distintos — coordinar
  el archivo compartido)
- US5 puede implementarse en paralelo con US3/US4 (toca `state_patch.py`, no
  `turn_orchestrator.py`)

---

## Parallel Example: User Story 1

```bash
# Lanzar los contract tests de US1 juntos:
Task: "Contract test for POST /api/v1/activities in tests/contract/test_activities_post.py"
Task: "Contract test for GET /api/v1/catalog/agents in tests/contract/test_catalog_agents.py"
Task: "Contract test for GET /api/v1/catalog/agencies in tests/contract/test_catalog_agencies.py"

# Lanzar los servicios independientes de US1 juntos:
Task: "Create RetentionPolicy repository/service in src/oralia/domain/sessions/retention_policy.py"
Task: "Create Agent catalog registration service in src/oralia/application/commands/register_agent.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational (CRÍTICO — bloquea todas las historias)
3. Completar Phase 3: User Story 1 (necesaria para tener una actividad sobre la que abrir
   sesión)
4. Completar Phase 4: User Story 2 — **STOP y VALIDAR**: ejecutar Escenario A de
   `quickstart.md` de forma independiente
5. Demostrar el MVP (catálogo + sesión trazable end-to-end)

### Incremental Delivery

1. Setup + Foundational → base lista
2. US1 → catálogo y actividades verificables
3. US2 → MVP demostrable (Escenario A)
4. US3 → bloqueo constitucional verificable (Escenario B)
5. US4 → degradación controlada verificable (Escenario C)
6. US5 → resolución de conflictos verificable (Escenario D)
7. US6 → reconstrucción tras reinicio verificable (Escenario E)
8. Polish → accesibilidad, documentación, revisión de conformidad constitucional

### Parallel Team Strategy

Con más de un desarrollador:

1. El equipo completa Setup + Foundational en conjunto
2. Una vez lista Foundational:
   - Desarrollador A: US1, después US6 (ambas giran en torno al catálogo/consulta)
   - Desarrollador B: US2 (bloqueante para US3/US4)
   - Tras completar US2: Desarrollador B continúa con US3, Desarrollador C toma US4
   - US5 puede asignarse a cualquiera libre tras Foundational (toca un archivo distinto)

---

## Notes

- [P] = archivos distintos, sin dependencias pendientes
- [Story] = mapea la tarea a su historia de usuario para trazabilidad
- Cada historia de usuario debe quedar completable y probable de forma independiente
- Verificar que los tests fallan antes de implementar
- Confirmar (checkpoint) cada historia de usuario de forma independiente antes de seguir
- Evitar: tareas vagas, conflictos de archivo entre tareas [P], dependencias entre
  historias que rompan su independencia

---

## Phase 10: Convergence

- [X] T080 Assign the correct `memory_category` (trabajo/episódica/semántica/procedimental/metacognitiva) per event type at every `record_event(...)` call site in `src/oralia/application/orchestration/turn_orchestrator.py` and `src/oralia/application/services/technical_summary_service.py`, instead of relying on the hardcoded `"episodic"` default per Constitution III (contradicts)
- [X] T081 Create and persist structured `InternalMessage` records for agent/orchestrator exchanges during `run_turn` in `src/oralia/application/orchestration/turn_orchestrator.py`, using the schema already defined in `src/oralia/domain/messages/internal_message.py`, per FR-007 (missing)
- [X] T082 Tag each element of a turn's `StatePatch` payload with its specific FR-009 element type (e.g. `participant_statement` for the input, `decision` for the response, `configuration`/`observation` for counters) instead of a single hardcoded `"decision"` in `src/oralia/application/orchestration/turn_orchestrator.py` per FR-009 (partial)
- [X] T083 Wire `oralia.infrastructure.telemetry.resources.snapshot()` into the real turn execution path in `src/oralia/application/orchestration/turn_orchestrator.py` so `TraceEvent.resource_usage` and `Turn.resource_usage` are populated with actual CPU/memory readings per agent and per session per FR-017 (partial)
- [X] T084 Add an `availability_status` field to the `Agency` model (`src/oralia/infrastructure/db/models.py`, with an accompanying migration) and expose it from `list_agency_summaries()` in `src/oralia/application/queries/get_catalog.py` so `GET /api/v1/catalog/agencies` reports it alongside agents per FR-003 (partial)

---

## Phase 11: Convergence

- [X] T085 Include `resource_usage` in the trace-event and turn dicts returned by `reconstruct_session_trace()` in `src/oralia/application/queries/reconstruct_session_trace.py` and by `get_session_detail()` in `src/oralia/application/queries/get_session.py`, so `GET /sessions/{id}` and `GET /sessions/{id}/trace` expose the CPU/memory data captured in T083 per Constitution VIII (partial)
- [X] T086 Add `availability_status` to the `AgencySummary` interface in `apps/web/src/api/client.ts` and render it in the agencies list in `apps/web/src/routes/Tecnica.tsx`, matching how the agents list already shows it, per FR-003 (partial)
- [X] T087 Route the degraded-path constitutional re-check in `src/oralia/application/orchestration/turn_orchestrator.py` (the direct `constitutional_evaluate(candidate_text)` call) through the same `InternalMessage`-generating path as normal agent steps, so it produces an `InternalMessage` in addition to its `TraceEvent`, per FR-007 (partial)

---

## Phase 12: Convergence

- [X] T088 **[Implementada en la 3ª ronda de estabilización, 2026-09-11 — retira la obligación de
  usar la regex literal `\b\d{1,3}\s*/\s*10\b` sin contexto; ver diff abajo]** Reinforce
  the pattern set in `evaluate()`/`_PROHIBITED_PATTERNS`
  (`src/oralia/domain/policies/constitutional_control.py`) with three independent
  rules per the corrected design in `research.md` §8: **Rule A** (`assigns_grade`,
  noun-anchored) — `(nota|calificación|puntuación)` + up to 4 filler words + a
  copulative verb (`es`/`será`/`queda en`) + a value (digit, simple cardinal number
  word cero–diez with optional "un/una", qualitative grade word, or an "N/10"
  fraction) — plus the existing immediate adjacent form unchanged; **Rule B**
  (`assigns_grade`, verb-anchored) — a granting verb (`otorgo`/`otorga`/`concedo`/
  `concede`/`asigno`/`asigna`) + up to 3 filler words + the same value set — covers P2
  without a "nota"/"calificación"/"puntuación" trigger; **Rule C**
  (`assigns_score_fraction`) — an "N/10" fraction **only** when within 4 words of an
  evaluated-item noun ("práctica"/"examen"/"trabajo"/"ejercicio"/"tarea"/"prueba") in
  either direction — **MUST NOT block a bare "N/10" unconditionally** (a context-free
  version of this rule was considered and rejected before implementation: it would
  also block L6/L7, which are not grades). MUST pass matrix cases P1–P7/L1–L8/V1 per
  FR-014 (contradicts)

  **Evidencia (recuento corregido en la ronda 4 — ver `research.md` §8.1/punto 4)**:
  16/16 casos de la matriz H02 pasan tras la corrección
  (`tests/contract/test_verification_block.py::test_h02_matrix_block_cases` — 7 casos
  P1–P7 — + `::test_h02_matrix_approved_cases` — 9 casos L1–L8/V1); el archivo completo
  suma 21 pruebas en verde (16 de la matriz + 5 previas ya existentes en el archivo:
  `test_prohibited_proposals_are_blocked` ×3, `test_ordinary_proposal_is_approved`,
  `test_verdict_is_one_of_the_four_closed_values`) — **21 no es "el número de casos de
  la matriz", es el total del archivo**; integración (`tests/failure/
  test_constitutional_block.py`, 2/2) y camino de fallback (`tests/failure/
  test_degradation_constitutional_check.py`, 1/1) sin cambios y en verde; regresión
  completa 001+002+003: 255 passed, 1 deselected (antes: 239 passed, 1 deselected —
  +16 son los casos nuevos de esta matriz, 0 regresiones: la suite no detectó ningún
  fallo en esos 239 casos previos, lo cual acota pero no equivale a "no existen
  defectos funcionales" — ver `quickstart-validation-evidence.md`); Ruff sobre
  `constitutional_control.py`: "All checks passed!" (limpio antes y después); Ruff
  global: 49 → 49 (sin hallazgos nuevos).

---

## Phase 13: Convergence

- [X] T089 **[Corregida y ejecutada en la 3ª ronda, 2026-09-11 — precisión documental de implementación]** [P]
  Reproduction for T088 — extend `tests/contract/test_verification_block.py` (real
  code path: `from oralia.domain.policies.constitutional_control import evaluate`,
  never a copy of the regex) with parametrized cases asserting the **CORRECT**
  required behavior per FR-014 and `research.md` §8's matrix — `evaluate("Tu nota es 9
  sobre 10.") == ("block", ...)` and `evaluate("Te otorgo un sobresaliente.") ==
  ("block", ...)`, among the rest of the matrix (P1–P4/L1–L5/V1/V2 plus this round's
  N/10-context contrasts). The assertion MUST be `verdict == "block"` — never
  `verdict == "approved"` re-described as "the failing reproduction". Run it against
  the current (unreinforced) `evaluate()` and confirm it **fails** (today's code
  returns `approved` for these two cases) — that failure, observed and recorded, is
  the reproduction; the test file's assertions themselves MUST NOT change between this
  failing run and the passing run after T088. MUST run and fail before T088 is
  implemented per FR-014 (missing)

  **Evidencia**: ejecutada contra el `evaluate()` sin reforzar — 6 fallos (P1, P2, P4,
  P5, P6, P7 devolvían `approved`), 15 aciertos (P3 y los 9 casos `approved` de la
  matriz, ya correctos antes de tocar el código, más las 5 pruebas previas del
  archivo). Tras T088, el archivo completo (16 casos de la matriz + 5 previas = 21 en
  total — no "21 casos de la matriz") con las mismas aserciones: 21/21 en verde.

  **Precisión documental (3ª ronda)**: la redacción anterior de esta tarea decía
  "a test asserting matrix cases P1/P2 currently return `approved`" — una frase
  ambigua que podía leerse como "escribe una aserción `== approved`". Se corrige: la
  aserción siempre exige el comportamiento correcto (`block`); lo que "falla hoy" es
  la propia aserción al ejecutarse contra el código actual, no una aserción distinta
  que espere `approved`.

---

## Phase 14: Convergence (speckit-converge sobre 001, 2026-09-11 — post-H02)

**Alcance de esta pasada**: evalúa 001 frente a su propio spec/plan/tasks tras
implementar H02 (T088/T089) — no evalúa 002/003. Hallazgo nuevo, no implementado en
esta ronda (autorización limitada a H02):

- [X] T090 `FR-014` exige que el control constitucional sea "capaz de bloquear
  mensajes que ... revelen datos no autorizados o se salgan del alcance de la
  actividad" — `_PROHIBITED_PATTERNS`
  (`src/oralia/domain/policies/constitutional_control.py`) no tiene ningún patrón para
  ninguna de esas dos categorías (solo cubre `assigns_grade`,
  `assigns_score_fraction`, `academic_decision`, `impersonates_professor`) — el
  docstring del módulo y `CONTRACT.purpose` ya afirman esa capacidad sin que exista
  código que la respalde. No confundir con el aislamiento de autorización de
  materiales (Feature 002, capa de recuperación, mecanismo distinto) — FR-014 describe
  esto como una responsabilidad del propio control constitucional sobre la salida
  generada, no de la recuperación de evidencia. Pendiente de diseño y matriz de
  aceptación propios, fuera del alcance de esta ronda (H02) per FR-014 (missing)

**No se declara toda la Feature 001 conforme a FR-014** por haber resuelto H02 — T090
queda como trabajo pendiente explícito, no absorbido silenciosamente en T088.

---

## Phase 15: Convergence (seguimiento de H02 — 3 falsos positivos, ronda 4, 2026-09-11)

**Contexto**: una revisión independiente ejecutó `evaluate()` sobre el código de T088
(ronda 3) y encontró tres falsos positivos — "Asigna un valor a la variable x.",
"La nota es una observación sobre el experimento." y "En este ejercicio la
probabilidad es 9/10." — los tres bloqueaban indebidamente. Se registra como regresión
adicional de H02, no como una ampliación de T090 (que sigue siendo un hallazgo distinto,
sin tocar).

- [X] T091 **[Implementada y validada en esta ronda, 2026-09-11]** Corrige las tres
  causas concretas en `src/oralia/domain/policies/constitutional_control.py`
  (`research.md` §8.1): (a) `_NUMBER_WORDS` deja de admitir `un`/`una` como numerales
  independientes (solo como prefijo de artículo ante un numeral real); (b) la Regla B
  (verbo de otorgamiento) deja de aceptar un dígito suelto como valor
  (`_VALUE_GRANT`, sin la alternativa `\d+` de la Regla A); (c) la Regla C
  (`assigns_score_fraction`) exige una conexión preposicional directa ("en"/"de" +
  artículo opcional) entre la fracción y el sustantivo de ítem evaluado, no solo
  cercanía. Sin excepciones literales para las tres frases — verificado con 5
  contrastes nuevos y sin cambiar el resultado esperado de ningún caso P1–P7/L1–L8/V1
  ya establecido. Per FR-014 (contradicts)

  **Reproducción**: los tres falsos positivos (más los contrastes C3–C5) añadidos a
  `tests/contract/test_verification_block.py::test_h02_matrix_approved_cases` con
  `verdict == "approved"` — ejecutados contra el código de T088 (previo a esta
  corrección): **6 fallos** (FP1, FP2, FP3, C3, C4, C5 devolvían `block`), 23 aciertos.
  Tras la corrección: **29/29** en verde, mismas aserciones.

  **Integración**: nuevas `tests/failure/test_constitutional_block.py::
  test_h02_reinforced_phrase_blocked_in_integration` ("Te otorgo un sobresaliente." vía
  el pipeline completo, no solo `evaluate()`) y `::test_h02_legitimate_phrase_not_blocked_in_integration`
  ("En este ejercicio la probabilidad es 9/10." no bloqueado en integración). Fallback:
  nueva `tests/failure/test_degradation_constitutional_check.py::
  test_misbehaving_fallback_proposal_never_reaches_participant` — sustituye el agente
  `safe-fallback` por un doble que propone "Tu nota es un nueve." y fuerza el fallo del
  agente principal; confirma que esa propuesta nunca llega al participante. **Hallazgo
  documentado en la propia prueba**: `turn_orchestrator.py` usa el texto fijo
  `SAFE_FALLBACK_TEXT` tanto para lo mostrado como para la re-verificación en la ruta
  degradada — nunca lee el resultado real del paso `fallback` — así que el veredicto
  correcto ahí es `approved` (nada que bloquear, el texto verificado es el fijo), no
  `block`; la garantía real y verificada es más fuerte de lo pedido: el contenido del
  agente de fallback nunca llega a evaluarse ni a mostrarse, se descarta por diseño.

  **Regresión y análisis estático**: 266 passed, 1 deselected (antes de esta tarea:
  255; +11 = 8 casos de matriz + 3 pruebas de integración/fallback, 0 regresiones).
  Ruff sobre los 4 archivos modificados: 1 línea larga nueva, corregida; recuento
  global 49 → 50 (transitorio) → 49 (tras corregirla) — sin hallazgos nuevos en el
  estado final.

---

## Phase 16: T090 — autorización constitucional contextual (2026-10-13)

**Objetivo**: ejecutar el desglose de T090 (FR-014/FR-015/FR-018a) sin reabrir H02 ni modificar grounding de Feature 002; conservar un recorrido normal visible SC-007 y cerrar sin contenido cuando la única alternativa no se autorice.

**Dependencias**: T090 es el hallazgo padre aún pendiente; T088/T089/T091 y sus reglas H02 permanecen cerradas. Las decisiones vinculantes están en specs/001-core-cognitive-runtime/plan.md, research.md §§9–10, data-model.md y contracts/constitutional-output.md. Los cambios en self_study_agency_composer.py y study_turn_orchestrator.py pertenecen a la integración constitucional de T090 con Feature 003, sin alterar su verificador de grounding ni sus veredictos.

**Criterio de finalización**: las reproducciones rojas conductuales previas se vuelven verdes sin cambiar sus aserciones congeladas; la matriz FR-014/FR-015, las rutas normales y todos los fallbacks, SC-007, H02, Feature 002 y Feature 003 pasan; política y trazas son versionadas y privadas; suite y Ruff se contrastan por caso/hallazgo con la línea base durable. El cierre seguro persiste turno y verificación antes de la transición de sesión, todo en una transacción exterior sin commits internos. La matriz léxica H02 queda literalmente intacta; solo se adaptan expectativas de integración ligadas al antiguo eco libre, conservando su contraste semántico. Cada hija se marca tras su propia evidencia; T147 audita el conjunto antes de marcar T090.

**Precondición de las reproducciones**: antes de cualquier cambio de código, T092 crea y conserva specs/001-core-cognitive-runtime/t090-ruff-baseline.json como evidencia durable entre sesiones, con huella del manifiesto registrada en quickstart-validation-evidence.md; no depende de Git, memoria conversacional ni scratch temporal. T092–T098 importan solo puntos de entrada existentes y usan diccionarios/protocolos/dobles locales para contratos futuros; un ImportError, módulo ausente, fixture roto o error de colección nunca cuenta como rojo válido. Cada archivo incluye un control positivo que pasa con el código previo, un fallo de aserción observable, liberación de dobles bloqueantes y recursos temporales, y aserciones congeladas antes de implementar. T097 reproduce solo defectos actuales; T125 demuestra por primera vez la secuencia nueva 0/1.

### Reproducciones discriminantes previas (escribir y ejecutar en rojo antes de implementar)

- [X] T092 [US3] Antes de modificar código, crear y conservar specs/001-core-cognitive-runtime/t090-ruff-baseline.json con versión de Ruff, comando exacto, alcance src/ tests/, ruta normalizada, código, mensaje, línea/columna originales, total y agrupación por código; registrar SHA-256 del contenido del manifiesto en specs/001-core-cognitive-runtime/quickstart-validation-evidence.md sin borrar el JSON entre sesiones. Después reproducir por aserción autorización/denegación de categoría/procedencia/destinatario, categoría desconocida y política ausente/inválida mediante ConstitutionalControl.execute y dobles locales en tests/contract/test_t090_policy_authorization_red.py; conservar positivo previo y no tocar tests/contract/test_verification_block.py.
- [X] T093 [P] [US3] Reproducir por aserción con ConstitutionalControl.execute actual y estructuras locales las referencias inventadas, etiquetas falsificadas, hueco de un carácter, solapamiento, espacio/puntuación, índices Unicode y normalización prohibida, más un control positivo previo, en tests/contract/test_t090_output_binding_red.py; no importar tipos futuros.
- [X] T094 [P] [US4] Ejercitar ConstitutionalControl.execute y la orquestación actuales con diccionarios/dobles definidos en tests/contract/test_t090_final_gate_red.py para reproducir por aserción texto solo frente a propuesta, precedencia, causas, timeout/ausencia de resultado, un único fallback y cierre sin texto; incluir control positivo previo y no importar final_output_gate.py ni tipos futuros.
- [X] T095 [P] [US3] Reproducir por aserción mediante run_turn actual salida de dato no autorizado, destinatario real distinto y tema/propósito/acción fuera de alcance, más turno positivo previo, en tests/integration/test_t090_main_turn_red.py; usar solo puntos de entrada existentes y liberar recursos.
- [X] T096 [P] [US4] Reproducir por aserción mediante run_study_turn y rutas actuales los bypass de fallback técnico/generativo, pregunta práctica, falta de evidencia, error/timeout upstream y texto transformado tras aprobación; incluir control positivo previo y liberar dobles bloqueantes en tests/integration/test_t090_self_study_fallback_red.py.
- [X] T097 [P] [US3] Provocar con los orquestadores actuales en tests/integration/test_t090_persistence_privacy_red.py rechazo que persiste texto bruto indebido, publicación directa de SAFE_BLOCKED_MESSAGE, alternativa histórica sin puerta estructurada o metadatos insuficientes para distinguir propuesta y salida; inspeccionar GeneratedProposal, InternalMessage y TraceEvent reales, con positivos de salida aprobada legítima/traza no sensible. El rojo es una aserción observable, sin inventar rechazo constitucional inicial → fallback aprobado (esa secuencia empieza en T125), importar módulos futuros ni alterar producción; liberar recursos.
- [X] T098 [P] [US2] Congelar en tests/integration/test_t090_positive_cycle_red.py aserciones observables de salida normal autorizada sin eco, fallback aprobado y cierre con output_text=null mediante el flujo actual; conservar control positivo del ciclo SC-007 ya funcional, obtener el rojo por comportamiento y liberar recursos.

### Política, catálogo y representación persistente

- [X] T099 [P] Modelar OutputAuthorizationPolicy con Pydantic v2 congelado y esquema cerrado, triples categoría/procedencia/destinatario, alcance, conocimiento general y permisos de plantillas normales/operativas en src/oralia/domain/policies/output_authorization_policy.py.
- [X] T100 Implementar serialización JSON canónica, ordenación de colecciones, SHA-256 y carga inmutable que rechace NaN, campos extra, duplicados y schema_version desconocida en src/oralia/domain/policies/output_authorization_policy.py.
- [X] T101 [P] Implementar catálogo interno inmutable de plantillas normales y mensajes operativos con identidad (id, version, sha256), dos versiones coexistentes, acuse normal SC-007 y alternativa mínima en src/oralia/domain/policies/output_template_catalog.py; conservar en el paquete las versiones referenciadas por configuración, sesión o traza.
- [X] T102 Probar en tests/unit/test_t090_output_template_catalog.py dos versiones del mismo template_id, actualización del catálogo que conserva la antigua, configuración y sesión históricas que resuelven exactamente su versión/huella, y bloqueo por versión retirada, par ID/versión reutilizado con otro contenido, huella discordante o sustitución silenciosa por la versión nueva.
- [X] T103 Probar canonicidad, hash, esquema cerrado, NaN, duplicados, versión desconocida, colecciones inmutables y ausencia de mutación compartida de la política en tests/unit/test_t090_output_authorization_policy.py.
- [X] T104 Añadir solo declaraciones ORM de output_authorization_policy_json Text nullable, output_authorization_policy_sha256 String(64) nullable y VerificationResult.authorization_context JSON nullable en src/oralia/infrastructure/db/models.py; no implementar persistencia final aquí ni migrar Turn.output_text, ya nullable.
- [X] T105 Crear en src/oralia/infrastructure/db/migrations/versions/t090_output_authorization.py revisión Alembic con down_revision="8df2dd196803", upgrade aditivo de las tres columnas y downgrade completo, sin backfill permisivo; preservar base histórica y clasificar NULL/NULL como missing_policy y estado parcial como invalid_context. Reservar la integración del trigger a T106, que usará exclusivamente src/oralia/infrastructure/db/ddl/t090_activity_policy_trigger.py antes de ejecutar la revisión completa.
- [X] T106 Crear en src/oralia/infrastructure/db/ddl/t090_activity_policy_trigger.py la única definición canónica e inmutable del trigger SQLite T090: nombre estable, SQL CREATE con IF NOT EXISTS y SQL DROP con IF EXISTS, cuerpo compartido sin copias; congelar este módulo t090 para la revisión actual y crear otro módulo versionado para cambios futuros. Hacer que upgrade/downgrade de src/oralia/infrastructure/db/migrations/versions/t090_output_authorization.py consuman esa definición, retirando trigger antes que columnas; registrar evento DDL SQLAlchemy o bootstrap de Base.metadata.create_all con la misma definición para tests/conftest.py y src/oralia/scripts/seed_demo.py, más guardia de escritura en src/oralia/application/commands/create_activity.py.
- [X] T107 Validar y serializar la política obligatoria de configuraciones nuevas antes del flush en ActivityConfigurationInput/create_activity de src/oralia/application/commands/create_activity.py, con rechazo de JSON/hash/esquema inválidos y coherencia de conocimiento general.
- [X] T108 Crear operación administrativa explícita de sucesión de una ActivityConfiguration histórica inmutable, copiando solo campos permitidos a una nueva versión con política docente explícita y dejando intacta la fila/sesiones anteriores, en src/oralia/application/commands/create_activity.py y src/oralia/interfaces/api/routers/tecnica.py.
- [X] T109 Actualizar políticas explícitas mínimas de fixtures/factories en tests/conftest.py, tests/unit/test_cognitive_state.py, tests/integration/test_agency_composition_variety.py, tests/integration/test_sc001_traceability.py, tests/integration/test_session_reconstruction_after_restart.py y tests/integration/test_state_patch_history.py; en tests/failure/test_session_limit_reached.py usar política válida para medir límite de turnos; en tests/failure/test_state_conflict.py documentar y comprobar NULL histórico sin salida; en tests/unit/test_activity_configuration.py y tests/integration/test_activity_immutability.py aportar política en casos válidos y casos negativos de ausente/inválida; no convertir NULL histórico en allow-all y repetir búsqueda global ActivityConfiguration( y ActivityConfigurationInput( antes de completar.
- [X] T110 Actualizar el seed de demostración con política y plantilla normal de SC-007 en src/oralia/scripts/seed_demo.py; conservar actividad histórica sin política solo en fixtures específicos de migración/fallo.
- [X] T111 Probar por separado en tests/integration/test_t090_policy_migration.py upgrade desde 8df2dd196803, downgrade con desaparición del trigger y nuevo upgrade, base nueva vía Alembic y vía Base.metadata.create_all: mismo nombre/cuerpo normalizado en sqlite_master desde src/oralia/infrastructure/db/ddl/t090_activity_policy_trigger.py, protección y error equivalentes tras immutable_since, creación idempotente y cero duplicados. Cubrir también NULL/NULL, columna parcial, JSON/hash alterado, mutación de dict decodificado, sucesión que conserva configuración/sesiones antiguas y reconstrucción histórica.

### Contratos, instantánea y verificador

- [X] T112 Definir tipos cerrados de AuthorizationSnapshot, OutputProposal, segmentos Unicode, referencias confiables, AuthorizationVerdict y códigos ordenables en src/oralia/domain/policies/output_authorization_contract.py, alineados con specs/001-core-cognitive-runtime/contracts/constitutional-output.md.
- [X] T113 Construir instantánea mínima en src/oralia/application/orchestration/output_authorization_context.py desde Session y ActivityConfiguration validadas, vinculando destinatario y configuración/política a esa sesión concreta y solo metadatos de referencias denegadas; el verificador no accede globalmente a la base de datos.
- [X] T114 Construir propuestas únicamente desde plantillas confiables y ranuras autorizables, sin convertir texto libre ni etiquetas del generador en autoridad, en src/oralia/application/orchestration/output_proposal_builder.py.
- [X] T115 Implementar solo identidad de política/catálogo, reconstrucción exacta y cobertura contigua [0,len(text)) por puntos de código Python sin normalización en src/oralia/domain/policies/output_authorization_verifier.py; antes de cerrar, probar cada frontera, hueco, espacio, puntuación y forma Unicode en tests/unit/test_t090_output_authorization_verifier.py.
- [X] T116 Añadir autorización de referencias existentes/compatibles y triples categoría-procedencia-destinatario antes de leer valores denegados en src/oralia/domain/policies/output_authorization_verifier.py; probar en tests/unit/test_t090_output_authorization_verifier.py referencias inventadas/denegadas, destinatario distinto del real y política/configuración de otra sesión.
- [X] T117 Añadir tema, propósito, acción y conocimiento general como conjunción de OutputAuthorizationPolicy.general_knowledge_allowed y ActivityConfiguration.general_knowledge_allowed en src/oralia/domain/policies/output_authorization_verifier.py, sin sustituir grounding Feature 002; probar cada combinación y material recuperable pero no presentable en tests/unit/test_t090_output_authorization_verifier.py.
- [X] T118 Integrar sin alterar patrones H02 la función evaluate(str) como subclasificador léxico del texto final en src/oralia/domain/policies/constitutional_control.py; prohibir que ella sola autorice la salida.
- [X] T119 Integrar, sin duplicar T115–T117, precedencia missing_policy → invalid_context → invalid_proposal → unverified_binding → unauthorized_data → out_of_scope → H02 → unsafe_fallback, deduplicación y cortocircuitos seguros en src/oralia/domain/policies/output_authorization_verifier.py; probar orden, múltiples causas y ausencia de lectura de valores denegados/acceso global a BD en tests/unit/test_t090_output_authorization_verifier.py.
- [X] T120 Versionar el contrato de ConstitutionalControl para exigir OutputProposal y AuthorizationSnapshot mediante AgentRequest.input/context y bloquear llamada solo textual, error, timeout o resultado ausente en src/oralia/domain/policies/constitutional_control.py; conservar los cuatro valores del contrato general.
- [X] T121 Confirmar sin cambiar aserciones congeladas que T092 y T093 pasan completas, que pasan solo los seis casos puramente contractuales/estructurales de tests/contract/test_t090_final_gate_red.py (test_structured_authorized_proposal_remains_approved, test_text_only_request_closes_on_missing_policy, los tres casos parametrizados de test_early_gate_reason_short_circuits_later_failures y test_authorization_scope_and_h02_reasons_are_complete_and_ordered), y que tests/contract/test_verification_block.py conserva H02 intacto. Añadir en tests/contract/test_t090_output_binding_red.py, tests/contract/test_t090_policy_authorization_red.py y esos seis casos de tests/contract/test_t090_final_gate_red.py positivos/negativos de Unicode, categoría, procedencia, destinatario real frente a snapshot falso, sesión/configuración ajena, alcance y conjunción de conocimiento general. Los tres casos de T094 que llaman a run_turn quedan excluidos de T121 y dependen expresamente de T126.

### Puerta final y persistencia privada

- [X] T122 Crear en src/oralia/application/orchestration/final_output_gate.py puerta única de intento 0 y máximo un intento operativo 1 catalogado sin reutilizar texto rechazado; fallo/error/timeout upstream consume directamente intento 1 y toda transformación posterior exige reverificación. La puerta solo decide/devolverá resultado final (si bloquea: texto NULL y acción finish): no persiste el cierre, no llama a close_session/end_study_session, no hace commit y no duplica lógica transaccional; T126/T129 persisten y solicitan cierre después.
- [X] T123 Usar las columnas ya declaradas por T104 para persistir desde src/oralia/application/orchestration/final_output_gate.py exactamente un VerificationResult constitucional final approved/block, reasons ordenados y authorization_context de identidad/versión/huella; preservar veredictos independientes de grounding/coherencia sin redefinir esquema en src/oralia/infrastructure/db/models.py.
- [X] T124 Registrar por intento en src/oralia/application/orchestration/final_output_gate.py y src/oralia/application/services/trace_service.py solo IDs/versiones/huellas, longitud no identificadora, tipo, intento, veredicto y causas del rechazo; excluir texto bruto rechazado y valores sensibles de GeneratedProposal.content, InternalMessage de transporte, TraceEvent, authorization_context, logs y errores, sin interpolar política completa. Conservar texto final aprobado según retención y mensajes internos ajenos al transporte, más metadatos procedimentales no sensibles suficientes para reconstruir componente, política/plantilla, rechazo inicial y resultado final sin recuperar contenido prohibido.
- [X] T125 Probar por primera vez, después de implementar la puerta, en tests/integration/test_t090_final_gate_persistence.py rechazo constitucional del intento 0 → fallback aprobado del intento 1, dos eventos trazados, único VerificationResult final approved, Turn.degraded, blocked=true y texto operativo visible; además fallback bloqueado sin tercer intento, inicio directo por error/timeout upstream, transformación reverificada y privacidad, sin trasladar esta secuencia a T097.

### Integración de todas las salidas

- [X] T126 [US2] Sustituir ambas ramas normal/degradada de src/oralia/application/orchestration/turn_orchestrator.py por la puerta estructurada y mantener acuse SC-007; ante fallo del único intento operativo, persistir primero Turn.blocked/output_text=NULL, GeneratedProposal saneada, VerificationResult final y DialogueAction.finish, luego solicitar cierre mediante primitiva activa→cerrada atómica/idempotente de src/oralia/application/commands/end_session.py. Coordinar src/oralia/application/commands/submit_turn.py y cierre voluntario de src/oralia/interfaces/api/routers/participante.py para que límite/voluntario/seguro usen la misma primitiva sin cambiar closed_error_safe ni duplicar resumen/evento/liberación; src/oralia/interfaces/api/deps/db.py hace el único commit exterior y rollback total ante excepción. Como criterio de aceptación explícito, cerrar entonces los tres casos orquestados de T094: test_missing_verifier_output_cannot_implicitly_approve, test_verifier_timeout_closes_without_publishing_or_retry_race y test_blocked_single_fallback_never_emits_a_third_message.
- [X] T127 [US3] Integrar en src/oralia/application/orchestration/self_study_agency_composer.py toda salida normal de duda, explicación guiada, revisión y preparación de presentación: proposal_text del generador, propuesta con conocimiento general, " ".join(supported_claims) y transformaciones posteriores; reautorizar texto final y conservar cambios de dialogue_action de guided_explanation/presentation_preparation, grounding/coherencia Feature 003 y veredictos Feature 002.
- [X] T128 [US3] Integrar en src/oralia/application/orchestration/self_study_agency_composer.py pregunta práctica normal, fallback determinista de generación, verificador de no divulgación, llamada directa a constitutional_evaluate de esa rama y asignaciones de SAFE_FALLBACK_TEXT/SAFE_BLOCKED_MESSAGE; no publicar pregunta libre no vinculada, solución interna ni alternativa de generación sin la puerta.
- [X] T129 [US4] Integrar en la rama de duda de src/oralia/application/orchestration/self_study_agency_composer.py nivel 0 y _ACKNOWLEDGE_MISSING_INFO_TEXT, grounding sin supported_claims, no_fundamentada, _CONFLICTIVE_TEXT, _INCOHERENCE_TEXT, SAFE_FALLBACK_TEXT, SAFE_BLOCKED_MESSAGE y su llamada directa a constitutional_evaluate; ninguna asignación visible elude la puerta. Si falla el único intento, persistir primero Turn.blocked/output_text=NULL, propuesta saneada, verificación final y DialogueAction.finish, luego solicitar transición activa→closed_error_safe atómica/idempotente por src/oralia/application/commands/end_study_session.py y src/oralia/application/commands/end_session.py. Coordinar límite y voluntario en src/oralia/application/commands/submit_study_turn.py y src/oralia/interfaces/api/routers/self_study.py: solo el ganador fija ended_at, resumen técnico, un session_closed y libera el bloqueo; resumen de estudio máximo una vez solo si summary_authorized, con repetición recuperable o estado cerrado documentado. Único commit exterior en src/oralia/interfaces/api/deps/db.py; excepción previa hace rollback total.
- [X] T130 [US4] Verificar delegaciones de src/oralia/application/orchestration/study_turn_orchestrator.py y cada consumo de src/oralia/domain/agents/fallback_agent.py, incluido SAFE_FALLBACK_TEXT y errores/timeouts upstream: no hay publicación sin puerta, transformación posterior sin reverificar ni segundo fallback encadenado en src/oralia/application/orchestration/self_study_agency_composer.py.
- [X] T131 [US3] Cerrar persistencia final compartida de cada rama de src/oralia/application/orchestration/self_study_agency_composer.py (pregunta, propuesta normal, conocimiento general, supported_claims, nivel 0, conflicto, incoherencia, falta de evidencia y fallback): texto aprobado según retención, propuesta rechazada saneada, único VerificationResult final, intentos trazados, Turn.output_text NULL solo al bloquear y causas no vacías; no basta adaptar una rama.
- [X] T132 Exigir matriz parametrizada con al menos un caso por cada rama visible de T127–T131 o grupo estrictamente equivalente, sin cambiar aserciones rojas T095–T097, en tests/integration/test_t090_self_study_fallback_red.py y tests/integration/test_t090_main_turn_red.py. Cubrir pregunta/fallback determinista, propuesta normal/general, supported_claims, nivel 0, grounding sin soporte/no_fundamentada, conflicto/incoherencia, cambios de dialogue_action, constantes de bloqueo/fallback, error/timeout upstream y transformación tras verificación. Buscar al final en src/oralia/application/orchestration/self_study_agency_composer.py constitutional_evaluate(, SAFE_BLOCKED_MESSAGE, SAFE_FALLBACK_TEXT, _ACKNOWLEDGE_MISSING_INFO_TEXT, _CONFLICTIVE_TEXT, _INCOHERENCE_TEXT, asignaciones a text y retornos output_text; cada coincidencia pasa por puerta, es interna no publicada o tiene prueba de imposibilidad de bypass.

### Contratos públicos y cliente

- [X] T133 Después de cerrar la semántica en T126–T131, adaptar solo TurnResult.output_text y StudyTurnResult.output_text a str | None y propagar degraded/blocked sin SAFE_BLOCKED_MESSAGE en src/oralia/application/orchestration/turn_orchestrator.py y src/oralia/application/orchestration/self_study_agency_composer.py.
- [X] T134 Adaptar serialización de output_text:null, texto operativo aprobado y blocked=true con turno degradado en src/oralia/interfaces/api/routers/participante.py y src/oralia/interfaces/api/routers/self_study.py.
- [X] T135 Actualizar tipos de respuesta del cliente web a string | null en apps/web/src/api/client.ts.
- [X] T136 Omitir burbuja cuando output_text sea null y mostrar solo texto operativo autorizado en apps/web/src/routes/Participante.tsx y apps/web/src/routes/Autoestudio.tsx.
- [X] T137 Probar en tests/contract/test_t090_turn_api.py ambos endpoints y consumidores src/oralia/application/queries/get_session.py y src/oralia/application/services/technical_summary_service.py: normal, cierre null y rechazo inicial → fallback aprobado con VerificationResult.approved, Turn.degraded, blocked=true inmediato, texto operativo, traza inicial, detalle coherente e incidencia en resumen. Verificar que los routers src/oralia/interfaces/api/routers/participante.py y src/oralia/interfaces/api/routers/self_study.py no sustituyen closed_error_safe en un cierre voluntario repetido y que src/oralia/interfaces/api/deps/db.py conserva un solo commit exterior; validar cliente con apps/web/package.json y apps/web/src/api/client.ts.

### Validación final y cierre de T090

- [X] T138 Aceptar integralmente, sin segunda implementación ni duplicar T121/T125, la matriz positiva/negativa FR-014/FR-015, causas ordenadas y rutas normal/fallback con pruebas de contrato, integración y fallo en tests/contract/test_t090_policy_authorization_red.py, tests/contract/test_t090_output_binding_red.py y tests/integration/test_t090_final_gate_persistence.py.
- [X] T139 Comprobar separadamente en tests/integration/test_t090_persistence_privacy_red.py GeneratedProposal.content, cada tipo de InternalMessage, TraceEvent, authorization_context, API, logs y errores: rechazo sin texto/valores/política; aprobado con texto visible conforme a retención; mensajes ajenos intactos; reconstrucción de componente, plantilla/política, intento y veredicto solo con metadatos seguros.
- [X] T140 Ejecutar intactas frases, patrones y aserciones léxicas H02 de tests/contract/test_verification_block.py; en tests/failure/test_constitutional_block.py y tests/failure/test_degradation_constitutional_check.py conservar bloqueo de frase prohibida y ausencia de falso positivo para «En este ejercicio la probabilidad es 9/10.» mediante plantilla/catálogo confiable de prueba con cobertura estructural completa, sustituyendo arnés de eco libre y adaptando solo sus aserciones dependientes del eco; documentar equivalencia contractual sin autorizar texto arbitrario del generador.
- [X] T141 Ejecutar regresión de grounding/admisión Feature 002 sin cambiar sus veredictos y añadir caso de fragmento recuperable pero prohibido por política de salida en tests/contract/test_grounding_verifier.py, tests/integration/test_grounding_verdict_mapping.py y tests/integration/test_material_isolation_blocked_trace.py.
- [X] T142 Ejecutar regresión de Feature 003 en tests/integration/test_mode_practice_questions.py, tests/integration/test_grounding_insufficient_evidence.py y tests/integration/test_t090_self_study_fallback_red.py, reenumerando y probando ausencia de bypass para pregunta normal/fallback determinista y no divulgación; proposal_text normal/general y supported_claims transformados; nivel 0, grounding sin soporte/no_fundamentada, conflicto, incoherencia; SAFE_FALLBACK_TEXT/SAFE_BLOCKED_MESSAGE y cada constitutional_evaluate directo; cambios de dialogue_action guiado/presentación, errores/timeouts y todo texto modificado tras verificación. Comparar inventario con búsqueda estática T132.
- [X] T143 Demostrar en tests/integration/test_t090_positive_cycle_red.py y tests/e2e/test_t090_sc007_cycle.py SC-007 inicio → turno autorizado visible → cierre voluntario → resumen; y cierre seguro con Turn.blocked/output_text=NULL/DialogueAction.finish, Session.closed_error_safe/ended_at/technical_summary_ref, un session_closed, bloqueo liberado una vez y nueva sesión. Probar repetición secuencial, cierre seguro concurrente/intercalado con límite, voluntario tras cerrado sin reemplazar estado, exactamente un resumen técnico y un evento; provocar excepción tras persistir turno/verificación y antes del único commit de src/oralia/interfaces/api/deps/db.py: rollback elimina turno, verificación, resumen, evento y liberación parcial. Repetir en autoestudio con resumen de estudio máximo una vez según summary_authorized y sin commits internos en src/oralia/application/commands/end_session.py, src/oralia/application/commands/end_study_session.py, src/oralia/application/commands/submit_turn.py y src/oralia/application/commands/submit_study_turn.py.
- [X] T144 Ejecutar suite tests/ con marcadores externos `-m "not ollama and not speech"` y --deselect solo tests/integration/test_material_index_rebuild_race_reproduction.py::test_A_reader_paused_mid_resolution_survives_one_concurrent_rebuild y tests/integration/test_material_index_rebuild_race_reproduction.py::test_B_reader_paused_survives_two_concurrent_rebuilds_needs_retry; conservar ejecutado tests/integration/test_material_index_rebuild_race_reproduction.py::test_empirical_chroma_behavior_on_a_deleted_collection_object, sin excluir archivo ni marcadores más amplios. Ejecutar aisladamente los tres casos para confirmar A/B FAILED deliberados y experimento PASSED, sin contar sus fallos como regresión T090. Registrar passed/deselected/warnings/fallos inesperados de la suite y resultados individuales en specs/001-core-cognitive-runtime/quickstart-validation-evidence.md.
- [X] T145 Ejecutar uv run ruff check src/ tests/ --output-format json y recuento --statistics; verificar SHA-256 de specs/001-core-cognitive-runtime/t090-ruff-baseline.json registrado en specs/001-core-cognitive-runtime/quickstart-validation-evidence.md y comparar con su versión/comando/alcance. Identidad estable = ruta normalizada + código + mensaje con multiplicidad; ubicación anterior/posterior distingue heredados sin mover y desplazados, sin tratarlos como nuevos. Informar heredados eliminados y realmente nuevos por separado, exigir cero nuevos en archivos T090 creados/modificados y no compensar altas con bajas; 49 es referencia secundaria y el manifiesto persiste entre sesiones.
- [X] T146 Documentar exclusivamente resultados ya validados de contrato, migración, privacidad, H02/Feature 002/003 y SC-007 en specs/001-core-cognitive-runtime/quickstart-validation-evidence.md y specs/001-core-cognitive-runtime/contracts/constitutional-output.md, sin reimplementar T121/T125/T138 ni declarar conformidad anticipada.
- [X] T147 Auditar evidencia y marcado progresivo ya realizado de cada T092–T146, sin marcar tareas en bloque; solo después marcar T090 en specs/001-core-cognitive-runtime/tasks.md y registrar vínculo a sus verificaciones.

### Grafo breve de dependencias de Phase 16

T092 (manifiesto Ruff durable y rojo por entrada actual) → T093–T098 (rojos independientes; T097 solo defectos presentes) → T099–T103 (política/catálogo) → T104–T111 (ORM, T105 revisión de columnas, T106 módulo canónico/trigger compartido, T111 equivalencia Alembic/create_all) → T112–T121 (tipos, snapshot, verificador y solo los seis casos estructurales de T094) → T122–T125 (puerta que decide sin cerrar/commit, persistencia propia y primera prueba completa 0/1) → T126 (integración de turn_orchestrator y cierre de los tres casos T094 que llaman a run_turn) → T127–T131 (resto de orquestadores, cierre transaccional compartido e inventario de Feature 003) → T132 (matriz y búsqueda estática) → T133–T137 (tipos/API/web y consumidores) → T138–T142 (aceptación y regresión exhaustiva) → T143 (E2E, idempotencia y rollback) → T144–T146 (suite, Ruff contra manifiesto y documentación) → T147 (solo auditoría de hijas ya marcadas y cierre de T090).

**Paralelización real**: tras conservar el manifiesto de T092, T093–T098 pueden escribirse en archivos distintos sin tocar fixtures compartidos, con dobles locales y entradas existentes; T097 no presupone la secuencia nueva 0/1 y ningún fallo de colección cuenta. T099 y T101 ocupan módulos distintos. T135 (tipos TS) puede prepararse sin editar Python de T133/T134, pero su validación depende del contrato backend. T115–T119 comparten verificador y se completan secuencialmente; T126/T133 y T127–T131/T133 comparten compositores, y T132/T142 dependen del inventario completo y del cierre transaccional.

## Phase 17: Convergence

- [X] T148 Corregir como prerrequisito bloqueante de T126 y T147 las fisuras restantes de la frontera de confianza constitucional: exigir y comparar exactamente `actual_session_id`, `actual_activity_configuration_id` y `actual_recipient`; validar `OutputProposal` y sus segmentos mediante contratos Pydantic cerrados; resolver plantillas solo por `(template_id, template_version, template_sha256)`; permitir referencias denegadas metadata-only y prohibir que aporten valor o huella; y proyectar/validar estrictamente todo resultado de `ConstitutionalControl`, bloqueando contexto, causas, precedencia, intento, identidad o tipo ambiguos. Añadir contraejemplos independientes y demostrar que ningún dato denegado alcanza snapshot, propuesta, traza, error o salida, sin alterar H02 ni Features 002/003, per FR-014, FR-015, Constitution II, IV y VII (partial).

- [X] T149 Corregir como convergencia bloqueante previa a T138 y T147 el cierre seguro sin política/contexto y la autoridad de materiales: hacer que participante y autoestudio persistan block con output_text=NULL, DialogueAction.finish, causas missing_policy/invalid_context y unsafe_fallback cuando corresponda, trazas saneadas y cierre idempotente sin excepción ni turno in_progress; construir referencias de fragmento solo desde filas MaterialFragment/MaterialDocument y configuración reales, usar exclusivamente una plantilla de ranura ya catalogada por triple exacto, bloquear metadatos ausentes o políticas que no autoricen el material sin copiar su valor; y eliminar la doble decisión constitucional de cada intento conservando inyección, timeout y exactamente una evidencia output_authorization_attempt por intento. Añadir contraejemplos de política ausente/inválida/catálogo ausente, material recuperable no presentable, procedencia ausente y positivo catalogado, más rollback/privacidad. T149 debe completarse antes de T138 y T147; no modifica H02 ni los veredictos de grounding/coherencia.

## Phase 18: Convergence

- [X] T150 Corregir como prerrequisito bloqueante de T144 y T147 la carrera del cierre de autoestudio: hacer que la primitiva compartida exponga mediante resultado tipado si el llamador ganó realmente la transición atómica `active -> terminal`, conservando la API pública de `close_session`; generar y devolver el resumen de estudio solo para el ganador y solo con `summary_authorized`; probar con dos `SASession` que el primer estado terminal prevalece, existe exactamente un resumen técnico, un `session_closed`, una liberación y como máximo un resumen de estudio, que el perdedor devuelve `None`, que la repetición secuencial permanece idempotente y que una excepción antes del commit exterior revierte estado, resúmenes, evento y liberación, per T143, FR-012b, FR-015 y SC-007 (partial).

