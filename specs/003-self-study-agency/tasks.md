---

description: "Task list for Agencia de autoestudio"
---

# Tasks: Agencia de autoestudio

**Input**: Design documents from `specs/003-self-study-agency/` (spec.md cerrado tras
dos rondas de `/speckit-clarify` + una ronda de corrección de consistencia
arquitectónica, 2026-09-01/02; `tasks.md` remediado tras `/speckit-analyze`, 2026-09-02)
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: incluidas — mismo criterio que las Features 001/002 (Principio X,
`docs/ORAL-IA_SpecKit/13_definition_of_done.md`): contrato por agente, integración por
composición de agencia, fallo/degradación por cada punto documentado en `research.md`.
Las pruebas normales (unit/contract/integration/failure) NO requieren un servidor Ollama
— usan `DeterministicGenerationAdapter` o dobles de `GenerationPort`. Las pruebas de
integración real contra Ollama viven en `tests/ollama/`, marcador `pytest` `ollama`,
omitidas por defecto en CI (research.md §1/§10).

**Reutilización explícita — NO se reimplementa** (FR-025): `execute_agency`/
`agency_composer.py`, `MaterialRetrieverAgent`, `GroundingVerifierAgent`,
`ConstitutionalControl`, `SafeFallbackAgent`/`SAFE_FALLBACK_TEXT`, `CognitiveState`/
`StatePatch`/`apply_patch`, `close_session`, `start_session`/`AI_DISCLOSURE`,
`session_lock_service`, `reconstruct_session_trace`, `TraceEvent`/`record_event`,
`RetentionPolicy` (esquema), `ActivityConfiguration` (incl. `immutable_since`,
`retention_policy_id`) — todos de las Features 001/002, importados sin modificar. Cada
tarea de esta lista que solo "conecta"/"usa" uno de estos componentes lo indica
explícitamente; ninguna tarea vuelve a implementarlos.

**Nota de remediación (`/speckit-analyze`, 2026-09-02)**: esta versión cierra los 12
hallazgos (D1, E1–E7, F1–F4) de la última pasada de análisis, más la cobertura parcial
de FR-003 señalada en ese mismo informe. Renumerada de forma consistente desde la
versión anterior (85 → 96 tareas); ninguna tarea de `spec.md`, código fuente,
`research.md`, `data-model.md` o `contracts/` fue modificada — solo este fichero y
`plan.md` → Project Structure.

**Organization**: Tareas agrupadas por historia de usuario (US1–US7 de `spec.md`).
Extiende el monolito modular ya existente de las Features 001/002 — Setup/Foundational
añaden a esa base, no la recrean.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias pendientes)
- **[Story]**: Historia de usuario a la que pertenece (US1–US7)
- Cada tarea incluye la ruta de archivo exacta

## Path Conventions

Extiende `src/oralia/` (Features 001/002) — ver `plan.md` → Project Structure para el
árbol completo de módulos nuevos de esta feature.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: añadir las dependencias y la estructura de esta feature al proyecto ya
existente

- [X] T001 Add `httpx` to main dependencies in `pyproject.toml` (promovido desde dev-only, research.md §1/§11 de la iteración anterior); add pytest marker `ollama` to `[tool.pytest.ini_options] markers`; run `uv sync`
- [X] T002 [P] Create module skeleton (`src/oralia/domain/self_study/`, `src/oralia/infrastructure/generation/`) with `__init__.py` files, per `plan.md` → Project Structure
- [X] T003 [P] Create `tests/ollama/` directory scaffolding (marker-gated, skipped without `ORALIA_OLLAMA_BASE_URL` configured) per research.md §1/§10

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: infraestructura central que MUST estar completa antes de cualquier historia
de usuario (esquema de datos, `GenerationPort` con sus dos adaptadores,
`StudyIntentInterpreterAgent` con su prueba de contrato, configuración docente de modos)

**⚠️ CRITICAL**: ninguna historia de usuario puede empezar hasta completar esta fase

- [X] T004 Add SQLAlchemy models `SelfStudyActivityConfig`, `PracticeQuestion`, `CoherenceIncident` per `data-model.md` to `src/oralia/infrastructure/db/models.py`
- [X] T005 Generate and apply the Alembic migration for the three new tables in `src/oralia/infrastructure/db/migrations/versions/`
- [X] T006 [P] Implement the `GenerationPort` protocol + `GenerationRequest`/`GenerationOutcome` schemas per `contracts/self-study-agents.md` in `src/oralia/infrastructure/generation/generation_port.py`
- [X] T007 [P] Implement `OllamaGenerationAdapter` (httpx; separación estricta de mensaje `system` fijo vs `user` con evidencia delimitada, FR-008b) in `src/oralia/infrastructure/generation/ollama_adapter.py` per research.md §1/§3 — **NUEVO, primaria de `GenerationPort` (2 implementaciones totales, sin envoltorio, research.md §1)**
- [X] T008 [P] Implement `DeterministicGenerationAdapter` (extractiva sobre `evidence`, siempre produce salida válida si hay evidencia) in `src/oralia/infrastructure/generation/deterministic_adapter.py` per research.md §1 — **NUEVO, reserva de `GenerationPort`**
- [X] T009 [P] Implement generation config (`ORALIA_OLLAMA_BASE_URL/MODEL/TIMEOUT_MS/TEMPERATURE/MAX_TOKENS`, `ORALIA_COHERENCE_NO_PROGRESS_WINDOW/REPETITION_WINDOW`, `ORALIA_DISCLOSURE_OVERLAP_THRESHOLD`, `ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS`) in `src/oralia/infrastructure/generation/config.py` per research.md §1/§4/§5
- [X] T010 [P] Implement `StudyIntentInterpreterAgent` (determinista, heurística de palabras clave, detecta los 5 modos canónicos + sub-intenciones de FR-009) per `contracts/self-study-agents.md` in `src/oralia/domain/agents/study_intent_interpreter.py` — **NUEVO, ficheros distintos de `interpreter_agent.py` (Feature 001, no tocado)**
- [X] T011 [P] Contract test for `StudyIntentInterpreterAgent` in `tests/contract/test_study_intent_interpreter.py` — MUST cubrir, como mínimo: (a) el contrato de entrada (`text`, `enabled_modes`, `current_mode`, `concepts_addressed`); (b) el formato de `intent_hypotheses` (`"{intent}:{confidence:.2f}"`, data-model.md); (c) `requested_mode` correcto para cada uno de los 5 modos canónicos; (d) `primary_confidence` en `[0,1]`; (e) forma estructurada completa de `AgentResult.output`; (f) manejo correcto de entrada inválida/vacía (`text=""` → intención de reconocimiento de falta de entrada, sin excepción) — **[Remediación D1/CRITICAL — cierra la ausencia de prueba de contrato para este agente, exigida por Principio X]**. MUST ejecutarse (y pasar) antes de dar por completada la implementación de T010; no modifica el agente ni su contrato, solo añade la cobertura que faltaba.
- [X] T012 Implement `configure_self_study_activity` command (crea/actualiza `SelfStudyActivityConfig`; `409` si `ActivityConfiguration.immutable_since` no es `null`, reutilizando ese campo sin modificar la Feature 001; `422` si `enabled_modes` vacío) in `src/oralia/application/commands/configure_self_study_activity.py` per research.md §7 (FR-002a)
- [X] T013 Create the `self_study` router skeleton registered in `src/oralia/interfaces/api/app.py`; implement `POST /api/v1/tecnica/activities/{activity_id}/self-study-config` in `src/oralia/interfaces/api/routers/self_study.py`
- [X] T014 [P] Contract test for `POST /tecnica/activities/{id}/self-study-config` (`201`/`409`/`422`) in `tests/contract/test_self_study_config.py`

**Checkpoint**: infraestructura fundacional lista — las historias de usuario pueden empezar

---

## Phase 3: User Story 1 - Resolver una duda cubierta por los materiales (Priority: P1) 🎯 MVP

**Goal**: un estudiante formula una duda cubierta por los materiales; el sistema
recupera evidencias (`MaterialRetrieverAgent`, Feature 002, **reutilizado sin
cambios**), genera una explicación fundamentada, la verifica
(`GroundingVerifierAgent`, Feature 002, **reutilizado sin cambios** +
`ConstitutionalControl`, Feature 001, **reutilizado sin cambios**), la muestra con
fuentes, conserva el concepto en el estado, y registra desde este primer flujo qué
agentes se activaron y por qué (FR-003)

**Independent Test**: con una actividad de autoestudio configurada (`enabled_modes`
incluye `doubt_resolution`) y materiales activos (Features 001/002), formular una duda
cubierta y verificar que la respuesta llega fundamentada, con fuentes visibles, con su
traza de activación de agentes, sin necesitar ningún otro modo implementado todavía

### Tests for User Story 1

- [X] T015 [P] [US1] Contract test for `ResponseGeneratorAgent` (usa `GenerationPort` vía doble determinista, sin Ollama) in `tests/contract/test_response_generator_agent.py`
- [X] T016 [P] [US1] Contract test for `POST /sessions/{id}/study-turns` (`200` camino feliz, `404`) in `tests/contract/test_self_study_turns_endpoint.py`

### Implementation for User Story 1

- [X] T017 [US1] Implement `ResponseGeneratorAgent` (`purpose=explicacion`, secuencia `OllamaGenerationAdapter`→`DeterministicGenerationAdapter` dentro del propio agente, research.md §1) per `contracts/self-study-agents.md` in `src/oralia/domain/agents/response_generator_agent.py` — **NUEVO**
- [X] T018 [US1] Implement `self_study_agency_composer.py`: construye la `AgencyDefinition` de `doubt_resolution` (interpret→retrieve→generate-response→verify-grounding→verify-constitutional→decide→state), reutilizando `MaterialRetrieverAgent`/`GroundingVerifierAgent`/`ConstitutionalControl`/`execute_agency` (Features 001/002, sin cambios); fija `CognitiveState.mode="doubt_resolution"` vía `StatePatch` (`apply_patch`, Feature 001, sin cambios) per research.md §6, en `src/oralia/application/orchestration/self_study_agency_composer.py` — **NUEVO** (extendido por T032/T033/T039/T049/T056-T059/T068 en historias posteriores — mismo patrón que `material_retriever_agent.py` en la Feature 002)
- [X] T019 [US1] Implement `study_turn_orchestrator.py`: `run_study_turn(db, session, text)` reutilizando `execute_agency` (Feature 001, sin cambios) in `src/oralia/application/orchestration/study_turn_orchestrator.py` — **NUEVO**
- [X] T020 [US1] Implement `submit_study_turn` command (análogo estructural a `submit_turn.py` de la Feature 001, fichero nuevo — FR-025) in `src/oralia/application/commands/submit_study_turn.py` — **NUEVO** (extendido por T079 en US7 con cierre automático)
- [X] T021 [US1] Implement `POST /sessions/{id}/study-turns` endpoint (`200`/`404`) in `src/oralia/interfaces/api/routers/self_study.py` (extiende el router creado en T013)
- [X] T022 [US1] Implement `generation_call` `TraceEvent` logging (`adapter`/`model`/`parameters`/`fragment_ids`/`fallback_used`/`latency_ms`) per `data-model.md` in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T023 [US1] Implement basic `agents_selected` `TraceEvent` logging (`activated_steps`, `reasons`, `mode`) for the `doubt_resolution` composition, reusing `TraceEvent`/`record_event` (Feature 001, **sin cambios** — no se reimplementa) per `contracts/self-study-agents.md` in `src/oralia/application/orchestration/self_study_agency_composer.py` — **[Remediación FR-003 — cobertura parcial detectada en `/speckit-analyze`: esta capacidad NO se difiere hasta US5; el primer flujo funcional de autoestudio ya registra qué agentes se activaron y por qué]** (extendido por T057 en US5 con `skipped_modes` y razonamiento completo de validación de modo)
- [X] T024 [US1] Build participant UI `Autoestudio.tsx` (entrada de texto, respuesta + panel de fuentes) in `apps/web/src/routes/Autoestudio.tsx`; incluye el renderizado del indicador de conocimiento general: cuando la respuesta HTTP trae `general_knowledge_used=true` (campo ya provisto por la API, T035/US2 — el frontend MUST NOT inferirlo ni recalcularlo por su cuenta), MUST mostrarse una indicación visualmente diferenciada de las fuentes procedentes de materiales autorizados; cuando `general_knowledge_used=false` (o el campo aún no existe en la respuesta, p. ej. antes de que US2 esté implementada), la indicación MUST NOT mostrarse — sin rediseñar el resto de la interfaz ni añadir funcionalidad adicional — **[Remediación F7/MEDIUM — FR-019]**
- [X] T025 [P] [US1] Integration/regression test: una sesión de autoestudio iniciada vía `POST /sessions` sigue presentando `ai_disclosure`, `objective` y los límites de la actividad, reutilizando `start_session`/`AI_DISCLOSURE` (Feature 001, **sin cambios** — no se reimplementa) in `tests/integration/test_self_study_session_start_disclosure.py` — **[Remediación E6/FR-005]**
- [X] T026 [US1] Integration test: flujo completo `doubt_resolution` — duda cubierta → respuesta fundamentada con fuentes, `concepts_addressed` actualizado, `agents_selected` registrado in `tests/integration/test_mode_doubt_resolution.py` (SC-001, Escenario A, FR-003)
- [X] T027 [US1] Integration test: `generation_call` `TraceEvent` registra `adapter`/`model`/`fragment_ids` de un turno in `tests/integration/test_generation_trace.py`
- [X] T028 [US1] Failure test: el texto de materiales usado como evidencia nunca se interpola en la instrucción `system` (defensa de prompt injection) in `tests/failure/test_prompt_injection_from_materials.py` (FR-008b)
- [X] T029 [US1] Failure test: Ollama no disponible/timeout degrada a `DeterministicGenerationAdapter` dentro del mismo turno, el turno se completa igualmente in `tests/failure/test_generation_ollama_unavailable.py` (research.md §1/§2)
- [X] T030 [US1] Failure test: ambos adaptadores de `GenerationPort` fallan de forma inesperada → la red de seguridad genérica ya existente de `execute_agency`/`SafeFallbackAgent` (Feature 001, sin cambios) produce una respuesta segura, turno marcado `degraded` in `tests/failure/test_generation_both_adapters_fail.py` (research.md §2)

**Checkpoint**: User Story 1 (MVP) funcional y probable de forma independiente, incluida su propia trazabilidad de activación de agentes (FR-003)

---

## Phase 4: User Story 2 - Reconocer una duda fuera de los materiales autorizados (Priority: P1)

**Goal**: sin conocimiento general permitido, una duda sin cobertura en los materiales
hace que el sistema reconozca la falta de información en vez de inventar una respuesta;
cuando el conocimiento general SÍ está permitido y se usa, la respuesta lo indica de
forma diferenciada (FR-019)

**Independent Test**: con una actividad `general_knowledge_allowed=false`, formular una
duda deliberadamente fuera de los materiales activos y verificar el reconocimiento
explícito de falta de información

### Tests for User Story 2

- [X] T031 [P] [US2] Integration test: cero fragmentos recuperados + `general_knowledge_allowed=false` → `acknowledge_missing_info`, el paso de generación no se activa in `tests/integration/test_no_evidence_acknowledge_missing_info.py` (research.md §2, Nivel 0)

### Implementation for User Story 2

- [X] T032 [US2] Extend `self_study_agency_composer.py` (T018): comprobación de evidencia (Nivel 0, research.md §2) — si `MaterialRetrieverAgent` devuelve `fragments=[]` con conocimiento general desactivado, omite `generate-response` por completo y fija `dialogue_action=acknowledge_missing_info` in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T033 [US2] Extend `self_study_agency_composer.py` (T018): mapeo (parcial, solo fundamentación — coherencia se añade en US6) de los 5 veredictos de `GroundingVerifierAgent` (Feature 002, sin cambios) a la escala de severidad de research.md §5 (`no_fundamentada`→`acknowledge_missing_info`, `conflictiva`→`clarify`, `parcialmente_fundamentada`/`no_verificable`→`reformulate` acotado, `fundamentada`→`approved`) in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T034 [US2] Integration test: hay evidencia pero no respalda la afirmación (`no_fundamentada`) → `acknowledge_missing_info`, nunca una respuesta inventada in `tests/integration/test_grounding_verdict_mapping.py` (US2 AC1/AC2)
- [X] T035 [US2] Extend `self_study_agency_composer.py`/endpoint (T021, T033): derivar `general_knowledge_used` en la respuesta HTTP a partir del veredicto de `GroundingVerifierAgent` (Feature 002, **sin cambios**) — `true` únicamente cuando el veredicto es `no_verificable` con `general_knowledge_allowed=true` (semántica ya definida en la Feature 002 para "evidencia vacía + conocimiento general permitido"; nunca una auto-declaración del agente generador); `false` en cualquier otro caso (incluidos `fundamentada`/`parcialmente_fundamentada`, que indican uso de materiales); registrar el valor en el `TraceEvent` correspondiente (`generation_call`/`verification_combined`) cuando proceda, sin crear un `event_type` nuevo — in `src/oralia/application/orchestration/self_study_agency_composer.py` — **[Remediación E3/HIGH — FR-019]**
- [X] T036 [US2] Integration test: `general_knowledge_used=true` solo cuando el veredicto de fundamentación indica cobertura por conocimiento general permitido (`no_verificable` + `general_knowledge_allowed=true`); `false` cuando la respuesta está sustentada únicamente en materiales autorizados (`fundamentada`/`parcialmente_fundamentada`) in `tests/integration/test_general_knowledge_labeling.py` — **[Remediación E3/HIGH — FR-019]**

**Checkpoint**: User Stories 1–2 funcionales de forma conjunta e independiente

---

## Phase 5: User Story 3 - Adaptar la explicación a petición del estudiante (Priority: P2)

**Goal**: el estudiante pide un ejemplo, una explicación más sencilla, una comparación,
un cambio de tema o finalizar la sesión; el sistema interpreta el cambio de intención,
genera contenido distinto sin perder el concepto ya tratado, rechaza/redirige un cambio
de tema fuera de alcance reutilizando la autorización de materiales de la Feature 002, y
mantiene continuidad de contexto verificable a lo largo de una conversación de varios
turnos sin reenviar el historial completo (SC-005)

**Independent Test**: completar un primer turno de duda cubierta (US1) y solicitar un
ejemplo o una explicación más sencilla sobre el mismo concepto

### Tests for User Story 3

- [X] T037 [P] [US3] Integration test: pedir "ejemplo"/"más sencillo"/"comparación" tras una respuesta previa produce una propuesta distinta sin repetir literalmente in `tests/integration/test_mode_guided_explanation.py` (SC-001)

### Implementation for User Story 3

- [X] T038 [US3] Extend `StudyIntentInterpreterAgent` (T010): detectar, de las seis solicitudes previstas por FR-009, las sub-intenciones `simpler_explanation`/`example`/`comparison` (mapeadas a `purpose` de `ResponseGeneratorAgent`), y `topic_change`/`finish` (las dos restantes que aún no tenían intención asignada — la sexta, "pregunta de práctica", ya se resuelve como `requested_mode=practice_questions` desde T010) in `src/oralia/domain/agents/study_intent_interpreter.py` — **[Remediación E4/MEDIUM — FR-009, cobertura de las 6 solicitudes sin inventar intenciones fuera de spec.md]**
- [X] T039 [US3] Extend `self_study_agency_composer.py` (T018): composición `guided_explanation` usando `CognitiveState.concepts_pending` (Feature 001, campo ya existente, sin ampliar esquema) como cola de sub-pasos pendientes; `dialogue_action=ask` hasta agotarla, luego `respond`/`summarize` (research.md §6) in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T040 [US3] Integration test: `guided_explanation` progresa por `concepts_pending` con acciones `ask`, y pasa a `respond`/`summarize` al agotarse in `tests/integration/test_guided_explanation_progression.py`
- [X] T041 [P] [US3] Parametrized/consolidated test: `StudyIntentInterpreterAgent` mapea correctamente las 6 solicitudes de FR-009 (`simpler_explanation`, `example`, `comparison`, `practice_question`→`requested_mode=practice_questions`, `topic_change`, `finish`) a la intención/modo esperado, sin ninguna intención adicional no listada en `spec.md` in `tests/unit/test_intent_fr009_coverage.py` — **[Remediación E4/MEDIUM — FR-009]**
- [X] T042 [US3] Extend `self_study_agency_composer.py` (T018, T032): una solicitud `topic_change` reinvoca `MaterialRetrieverAgent` (Feature 002, **sin cambios**) con el nuevo tema; si su filtro de autorización ya existente (reutilizado, no duplicado) no devuelve fragmentos autorizados, la petición se rechaza/redirige (mismo tratamiento que el Nivel 0 de T032 — sin recuperar ni generar contenido fuera de alcance) in `src/oralia/application/orchestration/self_study_agency_composer.py` — **[Remediación E2/HIGH — FR-023]**
- [X] T043 [US3] Integration/failure test: un cambio de tema fuera del alcance autorizado de la actividad se rechaza/redirige, reutilizando el aislamiento de `MaterialRetrieverAgent` (Feature 002, **sin cambios**, sin duplicar su filtro), no se recupera ni genera contenido fuera de alcance, y el intento queda trazado (reutilizando el registro de intentos bloqueados ya existente de la Feature 002) in `tests/failure/test_topic_change_out_of_scope.py` — **[Remediación E2/HIGH — FR-023]**
- [X] T044 [US3] Integration test: conversación de al menos 5 turnos (mezcla de `doubt_resolution`/`guided_explanation`) verificando continuidad de `CognitiveState` entre turnos, acumulación correcta de `concepts_addressed`/`concepts_pending`, que ningún `GenerationRequest` reconstruido a partir de la traza contiene el texto íntegro de turnos anteriores (solo `concepts_addressed`/evidencia del turno actual), y que la traza (`generation_call`, `agents_selected`) permite comprobar esta propiedad — usa exclusivamente `DeterministicGenerationAdapter`, sin comparar literalmente ninguna salida generada, ejecutable en CI sin Ollama in `tests/integration/test_sc005_context_continuity.py` — **[Remediación E1/HIGH — SC-005]**

**Checkpoint**: User Stories 1–3 funcionales de forma conjunta e independiente; SC-005 y FR-023 verificables

---

## Phase 6: User Story 4 - Practicar con preguntas sin calificación (Priority: P2)

**Goal**: el sistema genera preguntas de práctica derivadas de objetivos/conceptos/
materiales/historial de la sesión actual, sin revelar la solución cuando el modo lo
prohíbe y sin calificar al estudiante

**Independent Test**: con el modo `practice_questions` habilitado, solicitar preguntas y
responderlas, verificando que nunca se asigna nota ni se revela la solución indebidamente

### Tests for User Story 4

- [X] T045 [P] [US4] Contract test for `PracticeQuestionAgent` (`question_type`/`internal_expected_answer`/`reveals_solution`) in `tests/contract/test_practice_question_agent.py` — MUST incluir cobertura paramétrica explícita de los 5 valores de `question_type` definidos en `data-model.md`/`contracts/self-study-agents.md` (`explicacion`, `aplicacion`, `comparacion`, `justificacion`, `deteccion_errores`): para cada uno, verificar que el agente cumple su contrato (forma de `AgentResult.output`, `internal_expected_answer` poblado según `reveals_solution`) — nunca evaluar la calidad académica ni la corrección pedagógica de la pregunta generada — **[Remediación F8/LOW — FR-012]**
- [X] T046 [P] [US4] Contract test for `SolutionNonDisclosureVerifierAgent` (`approved`/`block`, umbral y configuración independientes de `GroundingVerifierAgent`) in `tests/contract/test_solution_non_disclosure_verifier.py`

### Implementation for User Story 4

- [X] T047 [US4] Implement `PracticeQuestionAgent` (`previous_questions` filtrado exclusivamente por `session_id`, FR-011a) per `contracts/self-study-agents.md` in `src/oralia/domain/agents/practice_question_agent.py` — **NUEVO**
- [X] T048 [US4] Implement `SolutionNonDisclosureVerifierAgent` (tokenización/umbral `_DISCLOSURE_OVERLAP_THRESHOLD` propios, independientes de `GroundingVerifierAgent` — research.md §4) per `contracts/self-study-agents.md` in `src/oralia/domain/agents/solution_non_disclosure_verifier_agent.py` — **NUEVO, verificador independiente**
- [X] T049 [US4] Extend `self_study_agency_composer.py` (T018): composición `practice_questions` (interpret→retrieve opcional→generate-question→`verify-non-disclosure` solo si `reveals_solution=false`→verify-constitutional→decide=`ask`→state); regeneración acotada (`ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS`, default 2) → `DeterministicGenerationAdapter` si se agotan los intentos in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T050 [US4] Persist `PracticeQuestion` (`generator_used`, `non_disclosure_attempts`) per `data-model.md` in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T051 [US4] Log `non_disclosure_check` `TraceEvent` por cada intento per `data-model.md` in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T052 [US4] Integration test: `practice_questions` genera una pregunta acotada a la sesión, nunca califica la respuesta del estudiante in `tests/integration/test_mode_practice_questions.py` (SC-001, US4 AC1/AC3)
- [X] T053 [US4] Failure test: `reveals_solution=false` y la pregunta generada revela la solución → bloqueada → regenerada → reserva determinista si se agotan los intentos in `tests/failure/test_reveal_solution_false_blocked_and_regenerated.py` (FR-013a)
- [X] T054 [US4] Unit test: el umbral/configuración de `SolutionNonDisclosureVerifierAgent` es independiente del de `GroundingVerifierAgent` (valores y variables de entorno distintos) in `tests/unit/test_solution_non_disclosure_threshold_independent.py` (research.md §4)

**Checkpoint**: User Stories 1–4 funcionales de forma conjunta e independiente

---

## Phase 7: User Story 5 - Componer dinámicamente los agentes según el modo habilitado (Priority: P2)

**Goal**: el orquestador selecciona únicamente los agentes necesarios por turno, valida
el modo solicitado contra los modos habilitados de la actividad, y demuestra al menos
tres composiciones distintas y los 5 modos canónicos; la trazabilidad básica de
activación ya existe desde US1 (T023) — esta historia la completa con el razonamiento
íntegro de validación de modo

**Independent Test**: configurar dos actividades con distintos modos habilitados y
verificar que el orquestador activa subconjuntos de agentes distintos y trazables para
cada una

### Tests for User Story 5

- [X] T055 [P] [US5] Contract test: `POST /sessions/{id}/study-turns` devuelve `409` con `requested_mode` cuando el modo no está en `enabled_modes` in `tests/contract/test_mode_not_enabled_rejected.py`

### Implementation for User Story 5

- [X] T056 [US5] Extend `self_study_agency_composer.py` (T018): validación completa de `requested_mode` contra `enabled_modes`; `StatePatch` sobre `CognitiveState.mode` solo si es válido y distinto del actual; rechazo (sin proponer `StatePatch`, sin invocar agentes de generación) si no es válido, per research.md §6 in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T057 [US5] Extend `agents_selected` `TraceEvent` (T023): añade `skipped_modes` y el razonamiento completo de validación de modo (por qué se rechazó o aceptó `requested_mode`) al payload ya existente desde US1 per `contracts/self-study-agents.md` in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T058 [US5] Extend `self_study_agency_composer.py` (T018): composición `presentation_preparation` (`purpose=estructura_exposicion`, patrón `ask`/`re_ask` dominante) per research.md §6 in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T059 [US5] Extend `self_study_agency_composer.py` (T018): composición `concept_review` (consulta de recuperación construida desde `concepts_addressed`, generador de respuesta o de pregunta según se solicite) per research.md §6 in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T060 [US5] Integration test: el modo cambia de `doubt_resolution` a `practice_questions` dentro de la misma sesión; `CognitiveState.mode` actualizado vía `StatePatch`; `agents_selected` registra ambos in `tests/integration/test_mode_switch_state_patch.py` (research.md §6)
- [X] T061 [US5] Failure test: un modo solicitado fuera de `enabled_modes` se rechaza antes de ejecutar ningún agente de generación (`409`, sin `StatePatch` propuesto) in `tests/failure/test_mode_change_rejected.py` (Edge Cases)
- [X] T062 [US5] Integration test: `presentation_preparation` produce un patrón `ask`/`re_ask` dominante in `tests/integration/test_mode_presentation_preparation.py` (SC-001)
- [X] T063 [US5] Integration test: `concept_review` recupera desde `concepts_addressed`, no formula una pregunta nueva no relacionada in `tests/integration/test_mode_concept_review.py` (SC-001)
- [X] T064 [US5] Integration test: ≥3 composiciones de agencia distintas observadas entre `doubt_resolution`/sin-evidencia/`practice_questions` in `tests/integration/test_agency_composition_variety.py` (SC-003)
- [X] T065 [US5] Integration test: SC-001 verificado para los 5 modos mediante `CognitiveState.mode` + `agents_selected` + `DialogueAction.action_type` — nunca comparando `output_text` in `tests/integration/test_sc001_traceability.py`

**Checkpoint**: User Stories 1–5 funcionales; 5/5 modos y ≥3 composiciones demostrables de forma conjunta e independiente

---

## Phase 8: User Story 6 - Detectar y gestionar fallos de coherencia (Priority: P2)

**Goal**: una propuesta que contradice una afirmación previa o una fuente activa se
bloquea o reformula; el sistema detecta las 9 condiciones de FR-015 (no solo
contradicción/repetición) y aplica una acción de recuperación observable en cada caso

**Independent Test**: forzar una propuesta de prueba que contradiga una afirmación
previa de la sesión y verificar que se bloquea o reformula con la incidencia registrada

### Tests for User Story 6

- [X] T066 [P] [US6] Contract test for `CoherenceVerifierAgent` (`approved`/`block`/`reformulate`, umbrales propios) in `tests/contract/test_coherence_verifier_agent.py`

### Implementation for User Story 6

- [X] T067 [US6] Implement `CoherenceVerifierAgent` (heurística de contradicción/repetición-solo-último-turno/pérdida-de-objetivo/ausencia-de-progreso, constantes de umbral propias en el módulo) per `contracts/self-study-agents.md` in `src/oralia/domain/agents/coherence_verifier_agent.py` per research.md §5 — **NUEVO, tercera implementación independiente de la técnica de solapamiento léxico (distinta de `GroundingVerifierAgent` y `SolutionNonDisclosureVerifierAgent`)**
- [X] T068 [US6] Extend `self_study_agency_composer.py` (T018/T033): activa el paso `verify-coherence`; deriva `fallo_agente`/`latencia_excesiva` directamente de `AgencyOutcome` (Feature 001, `execute_agency`, sin cambios) sin pasar por `CoherenceVerifierAgent`; combina con el veredicto de fundamentación mediante la tabla de severidad completa de research.md §5; persiste `CoherenceIncident`; registra `verification_combined` `TraceEvent` in `src/oralia/application/orchestration/self_study_agency_composer.py`
- [X] T069 [US6] Integration test: una propuesta que contradice una afirmación previa de la sesión se bloquea/reformula, `CoherenceIncident` persistido con `combined_verdict_source` in `tests/integration/test_verification_combined.py` (FR-024)
- [X] T070 [US6] Failure test: fundamentación dice `fundamentada` pero coherencia dice `block` → el resultado combinado es `block` (tabla de severidad) in `tests/failure/test_verifier_conflict_severity.py` (research.md §5)
- [X] T071 [US6] Unit test: la comprobación de repetición compara solo contra el turno inmediatamente anterior, no todo el historial (evita falsos positivos en `concept_review`) in `tests/unit/test_coherence_repetition_window.py` (research.md §5)
- [X] T072 [US6] Unit test: las ventanas de ausencia-de-progreso/repetición son configurables por variable de entorno, por defecto 3/1 in `tests/unit/test_coherence_thresholds.py`
- [X] T073 [US6] Integration test (parametrizado o conjunto mínimo equivalente): demuestra detección real — no solo configurabilidad — y `recovery_action` correcto para las 5 condiciones de FR-015 aún sin prueba conductual: `perdida_objetivo`, `exceso_turnos_mismo_concepto`, `fallo_agente`, `latencia_excesiva`, `ausencia_progreso` (usa los umbrales ya definidos en `research.md §5`/`config.py`, sin fijar cifras nuevas en esta tarea) in `tests/integration/test_coherence_conditions_fr015.py` — **[Remediación E5/MEDIUM — FR-015]**

**Checkpoint**: User Stories 1–6 funcionales de forma conjunta e independiente; las 9 condiciones de FR-015 verificadas conductualmente

---

## Phase 9: User Story 7 - Cerrar la sesión al alcanzar su límite con un resumen descriptivo (Priority: P3)

**Goal**: al alcanzar el límite de turnos/duración, la sesión se cierra de forma
ordenada y, si está autorizado, genera un resumen descriptivo efímero sin evaluación;
los datos derivados heredan retención de la actividad, son purgables bajo demanda, y la
traza de una sesión cerrada por límite es completa y reconstruible (SC-006)

**Independent Test**: configurar un límite bajo de turnos/duración y verificar que la
sesión se cierra de forma ordenada con el resumen correspondiente

### Tests for User Story 7

- [X] T074 [P] [US7] Contract test for `POST /sessions/{id}/study-end` (`study_summary` nulo/no nulo) in `tests/contract/test_study_end_endpoint.py`
- [X] T075 [P] [US7] Contract test for `POST /tecnica/self-study/purge-expired` (forma de `PurgeResult`) in `tests/contract/test_purge_expired_endpoint.py`

### Implementation for User Story 7

- [X] T076 [US7] Implement `study_session_summary_service.generate_study_summary` (`TraceEvent study_session_summary`; incidencias descritas como hechos observables del sistema, FR-022a) in `src/oralia/application/services/study_session_summary_service.py` — **NUEVO**
- [X] T077 [US7] Implement `end_study_session` command (envuelve `close_session`, Feature 001, **sin cambios**, + `generate_study_summary`) in `src/oralia/application/commands/end_study_session.py` — **NUEVO**
- [X] T078 [US7] Implement `POST /sessions/{id}/study-end` endpoint in `src/oralia/interfaces/api/routers/self_study.py`
- [X] T079 [US7] Extend `submit_study_turn` (T020): cierre automático al alcanzar el límite de turnos/duración (mismo patrón que `submit_turn.py` FR-011a de la Feature 001, replicado en fichero propio) + genera el resumen in `src/oralia/application/commands/submit_study_turn.py`
- [X] T080 [US7] Implement `purge_expired_self_study_data` command (`PurgeResult`; expiración vía `RetentionPolicy.retention_days` heredado transitivamente de `ActivityConfiguration`, Feature 001, **sin cambios**) per `data-model.md` in `src/oralia/application/commands/purge_expired_self_study_data.py` per research.md §8 — **NUEVO, único mecanismo de purga; invocación manual, sin scheduler (Feature 005)**
- [X] T081 [US7] Implement `POST /tecnica/self-study/purge-expired` endpoint in `src/oralia/interfaces/api/routers/self_study.py`
- [X] T082 [US7] Implement `GET /tecnica/sessions/{id}/study-trace` endpoint (reutiliza `reconstruct_session_trace`, Feature 001, **sin cambios**, ya genérico por `event_type`) in `src/oralia/interfaces/api/routers/self_study.py`
- [X] T083 [US7] Integration test: una sesión que alcanza el límite de turnos/duración se cierra automáticamente con un resumen descriptivo que solo contiene hechos observables del sistema in `tests/integration/test_session_limit_summary.py` (FR-020/FR-021/FR-022a)
- [X] T084 [US7] Integration test: tras el cierre por límite de T083, consultar `GET /tecnica/sessions/{id}/study-trace` (T082) y verificar que la secuencia completa de eventos de esa sesión (`agents_selected`, `generation_call`, `verification_combined`, cierre de turno, `study_session_summary`) es reconstruible in `tests/integration/test_sc006_trace_reconstruction_after_limit_close.py` — **[Remediación E7/LOW — SC-006]**
- [X] T085 [US7] Integration test: `study_summary` es `null` si `summary_authorized=false`; presente solo en la respuesta de cierre, sin endpoint de consulta posterior in `tests/integration/test_summary_ephemeral.py` (FR-021)
- [X] T086 [US7] Failure test: la purga elimina `PracticeQuestion`/`CoherenceIncident`/`TraceEvent` únicamente de sesiones con `retention_days` expirado, deja intactas las no expiradas, y solo toca las tablas de esta feature in `tests/failure/test_purge_expired_self_study_data.py` (FR-028)
- [X] T087 [US7] Failure test: ningún endpoint/consulta de esta feature acepta `participant_code` como filtro entre sesiones — `session_id` es la única clave in `tests/failure/test_longitudinal_aggregation_forbidden.py` (FR-011a)
- [X] T088 [US7] Integration test: dos sesiones del mismo `participant_code` nunca comparten historial de `PracticeQuestion`/`CoherenceIncident` in `tests/integration/test_session_isolation.py` (FR-011)

**Checkpoint**: todas las historias de usuario funcionales de forma independiente; SC-006 verificado explícitamente

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: mejoras que afectan a varias historias de usuario, y cierre formal de la
feature

- [X] T089 [P] Accessibility pass on `Autoestudio.tsx` (navegación por teclado, etiquetas, contraste) — mismo estándar ya exigido en 001/002 (FR-025 de la Feature 001)
- [X] T090 [P] Optional real-Ollama integration test (marcador `ollama`, omitido sin `ORALIA_OLLAMA_BASE_URL` configurado) validando `OllamaGenerationAdapter` contra un modelo local real in `tests/ollama/test_ollama_generation_real.py`
- [X] T091 Write installation/configuration documentation for this feature (configuración opcional de Ollama, variables de entorno nuevas) extending `docs/` con un nuevo `docs/003_self_study_instalacion.md`
- [X] T092 Run full `quickstart.md` validation (Escenarios A–G + verificación de purga) and record evidence in `specs/003-self-study-agency/quickstart-validation-evidence.md`
- [X] T093 Constitutional conformance self-review against `.specify/memory/constitution.md`, documented in `specs/003-self-study-agency/constitution-conformance-review.md`
- [X] T094 Code cleanup and refactoring pass across `src/oralia/domain/self_study/`, `infrastructure/generation/`, `application/orchestration/self_study_agency_composer.py`
- [X] T095 Run the complete Feature 001+002 test suite (`tests/` excluyendo los ficheros de prueba nuevos de esta feature, marcador `not ollama`) and record a 0-regressions confirmation in `specs/003-self-study-agency/quickstart-validation-evidence.md` (FR-025)
- [X] T096 Final gate: `uv run pytest tests/ -q -m "not ollama"` en verde (139 pruebas base 001/002 + todas las nuevas de esta feature), `quickstart.md` íntegramente ejecutado, `constitution-conformance-review.md` sin violaciones abiertas — condición de "hecho" de la feature (`docs/ORAL-IA_SpecKit/13_definition_of_done.md`)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias — puede empezar de inmediato
- **Foundational (Phase 2)**: depende de Setup — BLOQUEA todas las historias de usuario
- **User Story 1 (Phase 3, MVP)**: depende solo de Foundational
- **User Story 2 (Phase 4)**: extiende `self_study_agency_composer.py` (T018) — requiere US1 completada primero
- **User Story 3 (Phase 5)**: extiende `StudyIntentInterpreterAgent` (T010) y `self_study_agency_composer.py` (T018) — requiere US1 **y US2** completadas (T042 reutiliza el Nivel 0 de evidencia introducido en T032/US2 para el rechazo de `topic_change` fuera de alcance)
- **User Story 4 (Phase 6)**: extiende `self_study_agency_composer.py` (T018) — requiere **US1, US2 y US3** completadas (cadena completa sobre el fichero compartido, ver "User Story Dependencies"); sus agentes nuevos (`PracticeQuestionAgent`, `SolutionNonDisclosureVerifierAgent`) son ficheros propios, desarrollables en paralelo a US2/US3, pero su integración en el compositor (T049) debe esperar su turno en la cadena
- **User Story 5 (Phase 7)**: extiende `self_study_agency_composer.py` (T018) y el `agents_selected` `TraceEvent` ya creado en US1 (T023) — requiere **US1, US2, US3 y US4** completadas (cadena completa; además necesita `practice_questions` ya compuesto por US4 para demostrar el contraste `doubt_resolution`/`practice_questions`); las composiciones `presentation_preparation`/`concept_review` son variantes nuevas dentro del mismo fichero
- **User Story 6 (Phase 8)**: extiende `self_study_agency_composer.py` (T018/T033) — requiere **US1, US2, US3, US4 y US5** completadas (cadena completa; usa y amplía el mapeo de veredictos de fundamentación de T033)
- **User Story 7 (Phase 9)**: extiende `submit_study_turn` (T020) — requiere US1; independiente de US2–US6 en el resto de su código (resumen/purga son ficheros nuevos)
- **Polish (Phase 10)**: depende de todas las historias

### User Story Dependencies

**Cadena real sobre el fichero compartido `self_study_agency_composer.py`** (corregida
tras `/speckit-analyze`, hallazgo F1 — coherente con "Parallel Opportunities" más
abajo, sin cambios de arquitectura para forzar paralelismo artificial):

```text
US1 → US2 → US3 → US4 → US5 → US6
```

US7 es la única historia que NO se inserta en esa cadena (toca `self_study_agency_composer.py`
solo indirectamente a través de la sesión ya cerrada; su extensión real es sobre
`submit_study_turn`, T020, un fichero distinto).

- **US1 (P1) 🎯 MVP**: sin dependencias de otras historias de esta feature
- **US2 (P1)**: secuencial respecto a US1 (mismo fichero, `self_study_agency_composer.py`)
- **US3 (P2)**: secuencial respecto a US1 **y US2** (mismo fichero; T042 reutiliza el Nivel 0 de evidencia de US2/T032 para el rechazo de `topic_change`)
- **US4 (P2)**: secuencial respecto a US1/US2/US3 (mismo fichero); sus agentes nuevos (`PracticeQuestionAgent`, `SolutionNonDisclosureVerifierAgent`) son ficheros propios, desarrollables en paralelo a US2/US3 aunque su integración en el compositor deba esperar su turno
- **US5 (P2)**: secuencial respecto a US1–US4 (mismo fichero; además necesita `practice_questions` ya compuesto, US4, para demostrar la selección dinámica entre modos)
- **US6 (P2)**: secuencial respecto a US1–US5 (mismo fichero; extiende el mapeo de veredictos de T033/US2)
- **US7 (P3)**: secuencial respecto a US1 (`submit_study_turn`, T020); independiente de US2–US6 en el resto de su código

### Within Each User Story

- Tests antes de la implementación correspondiente
- Agentes nuevos (ficheros propios) antes de su integración en `self_study_agency_composer.py`
- Comandos de aplicación antes de endpoints de la API
- Lógica principal antes de pruebas de integración/fallo

### Parallel Opportunities

- Todas las tareas [P] de Setup (T002–T003) en paralelo
- T006–T011 de Foundational en paralelo (adaptadores/agente/contract test en archivos distintos)
- Dentro de US1: T015–T016 (contract tests) en paralelo; T025 (regresión de disclosure) es paralelizable frente al resto una vez completado T018; T028–T030 (failure tests) en paralelo entre sí tras T017–T022
- Dentro de US3: T041 (test paramétrico de intención) es paralelizable frente a T039/T042 (ficheros distintos), aunque debe esperar a que T038 exista
- Dentro de US4: T045–T046 (contract tests) en paralelo; T047–T048 (agentes, ficheros distintos) en paralelo
- **`self_study_agency_composer.py` (T018) NO puede extenderse en paralelo entre historias** — US2 (T032/T033/T035) → US3 (T039/T042) → US4 (T049) → US5 (T056-T059) → US6 (T068) lo tocan en secuencia estricta (cadena completa, ver "User Story Dependencies"), igual que `material_retriever_agent.py` en la Feature 002 (US2→US4→US6). Los agentes nuevos de cada historia (ficheros propios) sí son paralelizables entre sí.
- US7 (resumen/purga, ficheros propios) puede desarrollarse en paralelo a US2/US3/US4/US5/US6 por un desarrollador distinto, siempre que espere a que T020 (US1) exista antes de extender `submit_study_turn`

---

## Parallel Example: Foundational

```bash
# Lanzar los componentes de Foundational en paralelo (archivos distintos):
Task: "Implement GenerationPort protocol in src/oralia/infrastructure/generation/generation_port.py"
Task: "Implement OllamaGenerationAdapter in src/oralia/infrastructure/generation/ollama_adapter.py"
Task: "Implement DeterministicGenerationAdapter in src/oralia/infrastructure/generation/deterministic_adapter.py"
Task: "Implement StudyIntentInterpreterAgent in src/oralia/domain/agents/study_intent_interpreter.py"
Task: "Contract test for StudyIntentInterpreterAgent in tests/contract/test_study_intent_interpreter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational (CRÍTICO — bloquea todas las historias)
3. Completar Phase 3: User Story 1 — **STOP y VALIDAR**: ejecutar Escenario A de
   `quickstart.md` de forma independiente
4. Demostrar el MVP (duda cubierta → respuesta fundamentada con fuentes, con su propia
   traza de activación de agentes)

### Incremental Delivery

1. Setup + Foundational → base lista (config docente de modos disponible, agente de
   intención con su prueba de contrato)
2. US1 → MVP demostrable (Escenario A) con trazabilidad de activación desde el primer
   turno (FR-003)
3. US2 → reconocimiento de falta de información (Escenario B) + etiquetado de
   conocimiento general (FR-019)
4. US3 → adaptación de explicación (Escenario C), rechazo de cambio de tema fuera de
   alcance (FR-023) y continuidad de contexto verificada (SC-005)
5. US4 → práctica sin calificación con no-revelación verificada (Escenario D)
6. US5 → composición dinámica demostrable, 5/5 modos y ≥3 composiciones (SC-001/SC-003)
7. US6 → coherencia y combinación de veredictos, las 9 condiciones de FR-015 verificadas (Escenario F)
8. US7 → cierre de sesión, resumen efímero, retención/purga y traza reconstruible tras cierre por límite (Escenario G, SC-006)
9. Polish → accesibilidad, documentación, regresión 001/002, conformidad constitucional

### Parallel Team Strategy

Con más de un desarrollador:

1. El equipo completa Setup + Foundational en conjunto
2. Una vez lista Foundational:
   - Desarrollador A: US1, después US2, después US3, después US5 (requiere US1 y US4 ya
     mergeadas — coordina con B antes de empezar), después US6 (secuencial — mismo
     archivo `self_study_agency_composer.py` en todo momento)
   - Desarrollador B: US4 (agentes propios, independientes) — espera a que US1/US2/US3
     estén mergeadas antes de tocar `self_study_agency_composer.py` (T049)
   - Desarrollador C: US7 (ficheros propios: resumen, purga) — espera solo a T020 (US1)
   - Ningún desarrollador queda sin historia asignada: US5 se asigna explícitamente a A,
     respetando su dependencia real de US1+US4 (no se reordena la arquitectura para
     equilibrar la carga de trabajo)

---

## Notes

- [P] = archivos distintos, sin dependencias pendientes
- [Story] = mapea la tarea a su historia de usuario para trazabilidad
- Cada historia de usuario debe quedar completable y probable de forma independiente
- Verificar que los tests fallan antes de implementar
- Confirmar (checkpoint) cada historia de usuario de forma independiente antes de seguir
- Evitar: tareas vagas, conflictos de archivo entre tareas [P], dependencias entre
  historias que rompan su independencia — nótese la excepción documentada arriba
  (US2/US3/US4/US5/US6 comparten `self_study_agency_composer.py` por diseño, mismo
  patrón ya usado y validado en la Feature 002 con `material_retriever_agent.py`)
- Fuera de alcance de esta feature (explícitamente, per instrucción de planificación):
  microservicios, colas externas, scheduler de purga automatizado, UI de privacidad
  avanzada — reservado a la Feature 005
- **Remediación `/speckit-analyze` (2026-09-02)**: D1 (T011), E1 (T044), E2 (T042/T043),
  E3 (T035/T036), E4 (T038/T041), E5 (T073), E6 (T025), E7 (T084), F1 (sección
  "Dependencies & Execution Order" corregida), F2 (ver `plan.md`), F3 (ver `plan.md`),
  F4 (sección "Parallel Team Strategy" corregida), y la cobertura parcial de FR-003
  (T023, ya no diferida a US5) — todos cerrados. Ningún hallazgo quedó sin resolver.

---

## Phase 11: Convergence

- [X] T097 **[Depende de T107 — reproducción antes de corregir]** Add
  `student_input: str = ""` to `GenerationRequest`
  (`src/oralia/infrastructure/generation/generation_port.py`) and thread the current
  turn's `input_text` into it from `self_study_agency_composer.py`'s `generate` step
  input, as data delimited in the adapters' `user` message (`_build_user_content`,
  `ollama_adapter.py`) — never interpolated into the fixed `system` instruction.
  `PracticeQuestionAgent`/`DeterministicGenerationAdapter` unchanged (default `""`,
  research.md §13 traversal). Acceptance: capturing-double tests confirm the field
  reaches `GenerationRequest`/the built `user` content distinctly per turn — **not**
  that `output_text` differs (corrected criterion, research.md §13) — per FR-006/FR-008
  (missing)
- [X] T098 **[Depende de T108 — reproducción antes de corregir]** Extend
  `_significant_words`/`_overlap_score` in
  `src/oralia/domain/agents/solution_non_disclosure_verifier_agent.py` to tokenize
  digits/short alphanumeric solutions and to require an exact single-token match when
  `internal_expected_answer` tokenizes to one token, per the corrected design and
  acceptance matrix in `research.md` §4 (cases N1–N4/T1/C1/V1 — all with defined
  expected outcomes, including the accepted N4/V1 over-blocking trade-off) per FR-013a
  (contradicts)
- [X] T099 **[Depende de T109 — reproducción antes de corregir]** Stop discarding
  `end_study_session`'s return value in
  `src/oralia/application/commands/submit_study_turn.py`'s limit-reached branch; add
  `session_closed`/`study_summary` to the response built in
  `post_study_turn`/`self_study.py`, per `contracts/api-self-study.md` (updated this
  round) and `research.md` §11. Consume the atomic close outcome established by Feature
  001 T150: only the caller that wins `active -> closed_limit_reached` may return a
  summary; preserve any prior `closed_error_safe`/terminal status, never regenerate a
  summary, and expose `session_closed` from the final persisted status per
  FR-020/FR-021a (missing)
- [X] T100 **[Depende de T109 — reproducción antes de corregir]** Update
  `apps/web/src/api/client.ts` to add a `studyEnd`/`endStudySession` function calling
  `POST /sessions/{id}/study-end` (not the generic `endSession`/`/end`), and update
  `apps/web/src/routes/Autoestudio.tsx` to call it for voluntary closure, to recognize
  `session_closed`/`study_summary` on the response of `submitStudyTurn`, and to disable
  further turn submission once either signal is seen — without adding any further
  recovery path for the summary, per `research.md` §11 (FR-021b) per FR-021b (missing)
- [X] T101 **[Corregida en la 2ª ronda — ver diff abajo; depende de T110 —
  reproducción antes de corregir]** Add `SelfStudyActivityConfig.retention_authorized:
  bool | None` (new nullable column, migration required — see T114) and its validation
  in `configure_self_study_activity.py` (accepts `true`/`false`/omitted→`null`, never
  defaults preexisting rows to `true`/`false`). Add
  `GET /api/v1/tecnica/self-study/retention-audit` (new, read-only, no side effects) per
  `contracts/api-self-study.md`, classifying activities into the four states
  (`authorized_expiring`/`not_authorized_purge_eligible`/`undecided_preexisting`/
  `invalid_authorized_without_policy`, research.md §12.1). Change the expiration filter
  in `purge_expired_self_study_data.py` so `not_authorized_purge_eligible` sessions are
  purgeable from their first close, and so `undecided_preexisting`/
  `invalid_authorized_without_policy` sessions are **never** purged regardless of how
  many times the endpoint is invoked (retracts the first round's "first run flags,
  second run purges" rule — that rule treated repetition as consent, which is
  explicitly prohibited). Rename `PurgeResult.sessions_evaluated`/`sessions_purged` to
  `sessions_matching_criteria`/`sessions_with_rows_deleted` (research.md §12.5) per
  FR-028a (contradicts)
- [X] T102 **[Depende de T110 — reproducción antes de corregir]** Scope the
  `TraceEvent` deletion in `purge_expired_self_study_data.py` (same file as T101) to
  `event_type IN ("generation_call", "non_disclosure_check", "verification_combined",
  "study_session_summary", "agents_selected")` instead of deleting every `TraceEvent` of
  the session, per the verified inventory in `research.md` §12.3 (H07, unchanged from
  the first round — already correct) per FR-028 (contradicts)
- [X] T103 **[Corregida en la 2ª ronda — acceptance tests only; reproductions moved to
  T107–T110]** Acceptance tests for T097–T102: a session with mixed `TraceEvent` types
  (the five feature-owned `event_type`s above plus `session_started`/`session_closed`/
  `agent_execution` on the same session) purged and confirming only the five are
  removed; a `not_authorized_purge_eligible` session purged from its first close without
  waiting for any plazo; an `undecided_preexisting` session confirmed **never** purged
  across repeated invocations of `purge-expired`, appearing only in
  `retention-audit`; running the purge twice in a row confirming
  `sessions_with_rows_deleted = 0` on the second pass while `sessions_matching_criteria`
  still includes those sessions; a limit-reached turn whose `POST /study-turns` response
  carries `session_closed`/`study_summary` only from the winning atomic close; a prior
  safe close whose terminal status is not replaced; and a repeated `POST /study-end` on
  an already-closed session returning `study_summary: null` without error, per
  `research.md` §11/§12 and Feature 001 T150 (missing)
- [X] T104 [P] Regression: run the existing Feature 003 suite (`tests/` under
  `contract/`, `integration/`, `unit/`, `failure/` for this feature — per the file list
  already exercised by T095/T096) after T097–T103, and separately confirm this feature's
  existing behavior against the already-implemented Feature 001 T090 final gate/H02 and
  Feature 002 T084/T086/T087 grounding/retrieval/index race fixes. Re-run the T090
  contract/privacy matrices and T087 reproductions A/B without changing their
  assertions; Feature 003 must consume those boundaries without weakening or modifying
  them, per FR-025/FR-030 (missing)
- [X] T105 **[Corregida en la 2ª ronda — repurposed as the INITIAL baseline, not final
  validation; MUST run before T097–T103, T107–T114]** Capture a current, reproducible
  baseline in `quickstart-validation-evidence.md` **before any code change of this
  round**: (a) `uv run pytest tests/ -q -m "not ollama and not speech"` — record the
  actual current pass/fail count, do not assume 239 still holds; (b)
  `uv run ruff check src/ tests/` — record the actual current finding count; the "49"
  figure from a prior external audit has no corresponding record in this repository,
  which does not refute it — its current status stays open until this run; (c) confirm
  Node.js availability for `apps/web` (needed by T111/T112). Per Definition of Done
  items 6/7/15 (`docs/ORAL-IA_SpecKit/13_definition_of_done.md`) — no single FR covers
  this (missing)

---

## Phase 12: Convergence

**Orden de ejecución explícito de esta fase** (corrige la primera ronda, que dejaba
toda reproducción agrupada al final): `T105` (baseline) → `T107`/`T108`/`T109`/`T110`
(una reproducción por hallazgo, en paralelo entre sí) → su corrección correspondiente
(`T097`/`T098`/`T099`+`T100`/`T101`+`T102`) → `T103` (aceptación) → `T104` (regresión
001→002→003) → `T111`/`T112`/`T113`/`T114` (frontend, E2E, Ollama real, migración —
pueden empezar en paralelo tras `T101`/`T102` si tocan solo su propia área) → `T106`
(validación final, compara contra el baseline de `T105`).

- [X] T106 Final validation — after T097–T105 and T107–T114 are complete, re-run
  `uv run pytest tests/ -q -m "not ollama and not speech"` and
  `uv run ruff check src/ tests/`, compare against the `T105` baseline, and for every
  new failure/finding introduced by this round's changes: **fix it within this round's
  scope**, or, if it is a pre-existing issue unrelated to T097–T105/T107–T114 (already
  present in the `T105` baseline), **name it explicitly with its origin and why it is
  out of scope** — do not simply report a count. Per Definition of Done item 15
  (missing)
- [X] T107 [P] Baseline reproduction for T097 (H01) — write and run, against the
  current `GenerationRequest`/`ResponseGeneratorAgent`, a test using a capturing double
  of `GenerationPort` confirming that two turns with distinct `input_text` but the same
  `purpose`/`evidence` currently produce **identical** captured `GenerationRequest`
  objects (no field carries the distinct text) — record the failing baseline before
  T097. MUST run and fail before T097 per FR-006/FR-008 (missing)
- [X] T108 [P] Baseline reproduction for T098 (H04) — write and run, against the
  current `SolutionNonDisclosureVerifierAgent`, a test confirming case N1
  (`research.md` §4: question "La respuesta es 4." / answer "4") currently returns
  `approved` — record the failing baseline before T098. MUST run and fail before T098
  per FR-013a (missing)
- [X] T109 [P] Baseline reproduction for T099/T100 (H05) — write and run two checks
  against the current code: (a) a limit-reached turn's `POST /study-turns` response
  currently has no `session_closed`/`study_summary` field; (b)
  `apps/web/src/api/client.ts` currently has no function calling
  `POST /sessions/{id}/study-end` — record both as the failing baseline before T099/
  T100. MUST run and fail before T099/T100 per FR-020/FR-021a/FR-021b (missing)
- [X] T110 [P] Baseline reproduction for T101/T102 (H06/H07) — write and run two
  checks against the current `purge_expired_self_study_data`: (a) a session whose
  activity has no `RetentionPolicy`/a null `retention_days` is currently excluded from
  `sessions_evaluated` entirely (not flagged, not purgeable); (b) a session with mixed
  `TraceEvent` types currently has **all** of them deleted, including
  `session_started`/`session_closed` — record both as the failing baseline before
  T101/T102. MUST run and fail before T101/T102 per FR-028/FR-028a (missing)
- [X] T111 [P] Frontend build and static analysis (H11, `apps/web` never exercised
  before this round per the E2E spec's own comment) — run the project's configured
  build/lint/type-check commands for `apps/web` (`npm run build`, and `npm run lint`/
  `tsc --noEmit` if configured in `apps/web/package.json`; if none is configured, add
  the minimal one needed to compile-check T100's changes) and resolve any error
  introduced by T100 — this is a first-time baseline for the rest of the frontend, not
  a promise to fix pre-existing issues outside T100's change, per Definition of Done
  item 12 (missing)
- [X] T112 [P] E2E — self-study voluntary and automatic closure (extends
  `tests/e2e/`, creating its own `course_id`/`retention_policy_id`/activity fixtures
  via the API instead of assuming pre-existing ones, per H11): (a) voluntary closure —
  start a session, submit a turn, close via the UI, confirm the summary displays once
  and further input is disabled; (b) automatic closure — configure a low `max_turns`,
  exhaust it, confirm the UI recognizes `session_closed` from the turn response,
  displays the summary returned by the winning atomic close, and disables further input,
  without a second call recovering it or replacing a pre-existing terminal status.
  Depends on T099/T100/T111 and Feature 001 T150 per FR-020/FR-021a/FR-021b (missing)
- [X] T113 [P] Ollama real integration, differentiated from mocks/deterministic
  reserve (research.md §1) — run the `ollama`-marked suite (`tests/ollama/`) against an
  actual local Ollama server (not `DeterministicGenerationAdapter`, not a
  `GenerationPort` double) and record pass/fail separately from T106's deterministic
  run — this suite is deselected by default (`-m "not ollama"`) and MUST NOT be
  conflated with T106's baseline/final counts. Per `research.md` §1/§7 (missing)
- [X] T114 Migration for `SelfStudyActivityConfig.retention_authorized` (T101) —
  Alembic migration chained to the current head after Feature 001 T090, adding the
  nullable boolean column; MUST apply cleanly (a) from a clean install (`alembic
  upgrade head` on an empty database) and (b) as an upgrade
  over an existing Feature 003 database (pre-existing `SelfStudyActivityConfig` rows
  get `retention_authorized = NULL`, never `true`/`false`) — test both paths per
  Definition of Done item 5 (missing)
