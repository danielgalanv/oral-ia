---

description: "Task list for Materiales autorizados y RAG trazable"
---

# Tasks: Materiales autorizados y RAG trazable

**Input**: Design documents from `specs/002-materials-rag/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: incluidas. La constitución (Principio X) y `docs/ORAL-IA_SpecKit/13_definition_of_done.md`
exigen pruebas de contrato por agente, integración por agencia/flujo, y pruebas de fallo
para cada escenario de degradación — mismo criterio ya aplicado en la Feature 001.

**Organization**: Tareas agrupadas por historia de usuario (US1–US7 de `spec.md`).
Extiende el monolito modular ya existente de la Feature 001 — Setup/Foundational aquí
añaden a esa base, no la recrean.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias pendientes)
- **[Story]**: Historia de usuario a la que pertenece (US1–US7)
- Cada tarea incluye la ruta de archivo exacta

## Path Conventions

Extiende `src/oralia/` (Feature 001) — ver `plan.md` → Project Structure para el árbol
completo de módulos nuevos de esta feature.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: añadir las dependencias y la estructura de esta feature al proyecto ya
existente

- [X] T001 Add `chromadb`, `sentence-transformers`, `pdfplumber`, `python-docx`, `python-pptx` to `pyproject.toml` and run `uv sync`
- [X] T002 Create module skeleton (`src/oralia/domain/materials/`, `src/oralia/infrastructure/documents/`, `src/oralia/infrastructure/embeddings/`, `src/oralia/infrastructure/vector_store/`) with `__init__.py` files, per `plan.md` → Project Structure
- [X] T003 [P] Configure the local persistent ChromaDB directory path via `ORALIA_VECTOR_STORE_PATH` env var (default under the project's data directory), in `src/oralia/infrastructure/vector_store/config.py`
- [X] T004 [P] Add `tests/contract`, `tests/integration`, `tests/failure`, `tests/unit` fixtures scaffolding for this feature's test documents (small sample PDF/DOCX/PPTX/TXT/MD fixtures) under `tests/fixtures/materials/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: infraestructura central que MUST estar completa antes de cualquier historia
de usuario (esquema de datos, adaptadores de extracción/embeddings/índice, segmentador,
bloqueo de reconstrucción)

**⚠️ CRITICAL**: ninguna historia de usuario puede empezar hasta completar esta fase

- [X] T005 Add SQLAlchemy models for `MaterialDocument`, `MaterialFragment`, `Evidence`, `GroundingVerificationResult`, `MaterialConflictRecord` per `data-model.md` to `src/oralia/infrastructure/db/models.py`
- [X] T006 Generate and apply the Alembic migration for the five new tables in `src/oralia/infrastructure/db/migrations/versions/`
- [X] T007 [P] Implement the `VectorStore` interface and its ChromaDB adapter (`add`, `query`, `delete`, `rebuild`) in `src/oralia/infrastructure/vector_store/chroma_store.py` per research.md §2
- [X] T008 [P] Implement the `EmbeddingAdapter` interface and its `sentence-transformers` adapter in `src/oralia/infrastructure/embeddings/sentence_transformer_adapter.py` per research.md §3
- [X] T009 [P] Implement the deterministic, reproducible text segmenter (configurable chunk size/overlap, paragraph/sentence-aware) in `src/oralia/domain/materials/segmenter.py` per research.md §5 (FR-007)
- [X] T010 [P] Implement the `DocumentExtractor` interface plus PDF (`pdfplumber`) and DOCX (`python-docx`) adapters, including not-processable detection for near-empty extracted text, in `src/oralia/infrastructure/documents/` per research.md §4 (FR-003, FR-006)
- [X] T011 [P] Implement PPTX (`python-pptx`), TXT and Markdown extractor adapters in `src/oralia/infrastructure/documents/` per research.md §4 (FR-002, FR-006)
- [X] T012 Implement the single-writer index-rebuild lock service (reusing the `session_lock_service.py` unique-constraint pattern from Feature 001) in `src/oralia/application/services/index_rebuild_lock_service.py` per research.md §9
- [X] T013 Create the `materials` router skeleton bound to the área técnica's existing auth-stub dependency chain, registered in `src/oralia/interfaces/api/app.py`, in `src/oralia/interfaces/api/routers/materials.py`

**Checkpoint**: infraestructura fundacional lista — las historias de usuario pueden empezar

---

## Phase 3: User Story 1 - Incorporar y activar un documento autorizado (Priority: P1)

**Goal**: un profesor carga un documento, el sistema lo valida/procesa/indexa, y el
profesor revisa su estado y lo activa para una actividad

**Independent Test**: cargar un documento de prueba, verificar su estado de
procesamiento y activarlo, sin que exista todavía ninguna consulta de recuperación

### Tests for User Story 1

- [X] T014 [P] [US1] Contract test for `POST /api/v1/materials/documents` (incl. `409` possible-duplicate response) in `tests/contract/test_materials_documents_post.py`
- [X] T015 [P] [US1] Contract test for `GET /api/v1/materials/documents` / `/{id}` in `tests/contract/test_materials_documents_get.py`
- [X] T016 [P] [US1] Contract test for `POST /materials/documents/{id}/activate` / `/deactivate` (incl. `409` when not processed) in `tests/contract/test_materials_activate.py`
- [X] T017 [P] [US1] Contract test for `POST /materials/documents/{id}/duplicate-resolution` in `tests/contract/test_materials_duplicate_resolution.py`

### Implementation for User Story 1

- [X] T018 [US1] Implement the `ingest_material` command (format/size validation, hash computation, extraction, segmentation, embeddings, indexing) in `src/oralia/application/commands/ingest_material.py` (FR-001..FR-010)
- [X] T019 [US1] Implement the duplicate-hash detection and two-step resolution flow (`link_existing` / `proceed_new`) in `src/oralia/application/commands/resolve_material_duplicate.py` (FR-005a)
- [X] T020 [US1] Implement the `activate_material` / `deactivate_material` commands, enforcing FR-011 (not-processed rejection), FR-013 (reversible deactivation) and FR-013a (reject assigning a retired/inactive version) in `src/oralia/application/commands/activate_material.py`
- [X] T021 [US1] Implement the material catalog query (list/detail with processing status) in `src/oralia/application/queries/get_material_catalog.py`
- [X] T022 [US1] Implement `POST /materials/documents`, `GET /materials/documents`, `GET /materials/documents/{id}`, `POST .../activate`, `.../deactivate`, `.../duplicate-resolution` endpoints in `src/oralia/interfaces/api/routers/materials.py`
- [X] T023 [US1] Build área técnica UI for document upload, processing status, and activation in `apps/web/src/routes/Tecnica.tsx` (new "Materiales" section)
- [X] T024 [US1] Integration test: full upload → processed → activate flow for a real PDF/DOCX/PPTX/TXT/MD fixture in `tests/integration/test_material_ingestion.py`
- [X] T025 [US1] Integration test: a scanned/no-text PDF is marked `not_processable`, never silently indexed, in `tests/integration/test_material_not_processable.py`
- [X] T026 [US1] Failure test: activation rejected when a document is not yet processed or is in error, in `tests/failure/test_material_activation_rejected.py`
- [X] T027 [US1] Integration test: uploading a duplicate hash returns `409`, and both `link_existing`/`proceed_new` resolutions behave per FR-005a in `tests/integration/test_material_duplicate_resolution.py`

**Checkpoint**: User Story 1 funcional y probable de forma independiente

---

## Phase 4: User Story 2 - Recuperar fragmentos autorizados con procedencia (Priority: P1) 🎯 MVP

**Goal**: un agente de recuperación devuelve fragmentos con procedencia completa para una
consulta autorizada, respetando límites de tamaño y tiempo, de forma repetible

**Independent Test**: con al menos un documento activo (US1), enviar una consulta y
verificar que los fragmentos devueltos incluyen procedencia completa y trazable

### Tests for User Story 2

- [X] T028 [P] [US2] Contract test for `POST /api/v1/materials/query` (happy path: fragments with full provenance) in `tests/contract/test_materials_query.py`

### Implementation for User Story 2

- [X] T029 [US2] Implement `MaterialRetrieverAgent` (the `Executable`/`AgentContract` protocol from Feature 001) per `contracts/material-retriever-agent.md` in `src/oralia/domain/agents/material_retriever_agent.py` (FR-017, FR-018)
- [X] T030 [US2] Implement query embedding + `VectorStore.query()` invocation with `max_fragments`/`time_budget_ms` honored in `src/oralia/domain/agents/material_retriever_agent.py`
- [X] T031 [US2] Implement `POST /materials/query` endpoint (direct-invocation demo/test surface per research.md §1) in `src/oralia/interfaces/api/routers/materials.py`
- [X] T032 [US2] Integration test: identical query + config + index version returns the same fragments in the same order in `tests/integration/test_material_retrieval_repeatable.py` (FR-020)
- [X] T033 [US2] Failure test: `time_budget_ms` exhausted returns partial results with an explicit warning, not a timeout status, in `tests/failure/test_material_retrieval_budget.py` (Edge Case)
- [X] T034 [US2] Integration test: `max_fragments` limit is respected in `tests/integration/test_material_retrieval_limits.py`

**Checkpoint**: User Stories 1–2 (MVP) funcionales de forma conjunta e independiente

---

## Phase 5: User Story 3 - Detectar evidencia insuficiente y clasificar la fundamentación (Priority: P2)

**Goal**: un verificador de fundamentación clasifica una propuesta frente a la evidencia
recuperada en una de cinco categorías, y el sistema reconoce cuando la evidencia es
insuficiente en vez de inventar una respuesta

**Independent Test**: enviar una consulta sin cobertura en los materiales autorizados y
verificar que el sistema señala la limitación en vez de inventar una respuesta

### Tests for User Story 3

- [X] T035 [P] [US3] Contract test for the five `GroundingVerifierAgent` verdicts (fundamentada, parcialmente_fundamentada, no_fundamentada, conflictiva, no_verificable) in `tests/contract/test_grounding_verifier.py`

### Implementation for User Story 3

- [X] T036 [US3] Implement `GroundingVerifierAgent` (`Executable`/`AgentContract`) per `contracts/material-retriever-agent.md` in `src/oralia/domain/agents/grounding_verifier_agent.py` (FR-023, FR-023a)
- [X] T037 [US3] Implement general-knowledge labeling honoring `ActivityConfiguration.general_knowledge_allowed` (Feature 001) in `src/oralia/domain/agents/grounding_verifier_agent.py` (FR-024, FR-025)
- [X] T038 [US3] Integration test: a query with no coverage in authorized materials yields `no_fundamentada`/`no_verificable`, never a confident answer, in `tests/integration/test_grounding_insufficient_evidence.py` (Escenario C)
- [X] T039 [US3] Integration test: general knowledge used when permitted is labeled distinctly from grounded content in `tests/integration/test_grounding_general_knowledge_label.py`
- [X] T040 [US3] Unit test: a proposal with only some claims supported is classified `parcialmente_fundamentada`, naming the unsupported claims, in `tests/unit/test_grounding_partial.py`
- [X] T041 [US3] Unit test: grounding verdicts are never aggregated or persisted as a cross-session participant signal in `tests/unit/test_grounding_no_aggregation.py` (FR-023a)

**Checkpoint**: User Stories 1–3 funcionales de forma conjunta e independiente

---

## Phase 6: User Story 4 - Aislar materiales por asignatura, actividad y sesión (Priority: P2)

**Goal**: ninguna consulta recupera fragmentos de una asignatura/actividad no
autorizada, ni de materiales inactivos, retirados o caducados; los intentos fuera de
alcance quedan bloqueados y trazados

**Independent Test**: crear materiales en dos actividades distintas y verificar que una
consulta de una de ellas nunca recupera fragmentos de la otra

### Tests for User Story 4

- [X] T042 [P] [US4] Contract test: a query requesting an out-of-scope activity/course returns empty fragments, never an error leaking existence of other materials, in `tests/contract/test_materials_query_isolation.py`

### Implementation for User Story 4

- [X] T043 [US4] Implement authorization filtering (course/activity/session scope, FR-019) in `MaterialRetrieverAgent`'s `VectorStore.query()` metadata filters, in `src/oralia/domain/agents/material_retriever_agent.py`
- [X] T044 [US4] Implement vigencia-expiry exclusion (FR-019a) in the same filtering path
- [X] T045 [US4] Implement blocked out-of-scope attempt logging (FR-026) via `trace_service.record_event`, using a `metacognitive` `memory_category` per Constitution §III, in `src/oralia/domain/agents/material_retriever_agent.py`
- [X] T046 [US4] Integration test: a query for activity A never returns fragments belonging to activity B in `tests/integration/test_material_isolation_cross_activity.py`
- [X] T047 [US4] Integration test: an out-of-scope retrieval attempt is blocked and produces a traceable `TraceEvent` in `tests/integration/test_material_isolation_blocked_trace.py`
- [X] T048 [US4] Failure test: an inactive, retired, or vigencia-expired material is never returned regardless of query in `tests/failure/test_material_isolation_excluded_states.py`

**Checkpoint**: User Stories 1–4 funcionales de forma conjunta e independiente

---

## Phase 7: User Story 5 - Sustituir y retirar versiones de materiales (Priority: P2)

**Goal**: sustituir un documento por una nueva versión retira la anterior sin borrarla;
las sesiones nuevas solo ven la versión activa, las históricas conservan su referencia

**Independent Test**: sustituir la versión de un documento de prueba y verificar que una
sesión nueva solo recupera la versión activa mientras una sesión histórica conserva su
referencia original

### Tests for User Story 5

- [X] T049 [P] [US5] Contract test for `POST /materials/documents/{id}/versions` in `tests/contract/test_materials_versions_post.py`

### Implementation for User Story 5

- [X] T050 [US5] Implement the `replace_material_version` command (new version creation, `retired_at` on the previous version, format-change allowed) in `src/oralia/application/commands/replace_material_version.py` (FR-014, FR-015)
- [X] T051 [US5] Implement `POST /materials/documents/{id}/versions` endpoint in `src/oralia/interfaces/api/routers/materials.py`
- [X] T052 [US5] Integration test: after replacing a version, new sessions only retrieve fragments from the active version in `tests/integration/test_material_version_replacement.py`
- [X] T053 [US5] Integration test: a session that used a now-retired version still exposes its historical fragment references via `GET /sessions/{id}` (Feature 001) in `tests/integration/test_material_version_history_audit.py`
- [X] T054 [US5] Unit test: a retired version cannot be reactivated (rejects `activate`), while a merely-deactivated one can, in `tests/unit/test_material_retirement_vs_deactivation.py` (FR-013, FR-015)

**Checkpoint**: User Stories 1–5 funcionales de forma conjunta e independiente

---

## Phase 8: User Story 6 - Señalar conflictos entre fuentes activas (Priority: P3)

**Goal**: cuando dos materiales activos contienen afirmaciones incompatibles, la
recuperación devuelve ambas evidencias marcadas como conflictivas, y el conflicto queda
registrado de forma persistente para revisión docente

**Independent Test**: activar dos documentos de prueba con afirmaciones contradictorias
y verificar que una consulta relacionada devuelve ambas evidencias marcadas como
conflictivas

### Tests for User Story 6

- [X] T055 [P] [US6] Contract test for `GET /materials/conflicts` / `POST /materials/conflicts/{id}/review` in `tests/contract/test_materials_conflicts.py`

### Implementation for User Story 6

- [X] T056 [US6] Implement the deterministic conflict-detection heuristic (keyword/negation-based, research.md §7) in `src/oralia/domain/materials/conflict_detector.py` (FR-022)
- [X] T057 [US6] Wire conflict detection into `MaterialRetrieverAgent`'s result construction, creating a `MaterialConflictRecord` per detected conflict and a `TraceEvent` with a `metacognitive` `memory_category` per Constitution §III, in `src/oralia/domain/agents/material_retriever_agent.py` (FR-022a)
- [X] T058 [US6] Implement the `review_material_conflict` command in `src/oralia/application/commands/review_material_conflict.py`
- [X] T059 [US6] Implement `GET /materials/conflicts` and `POST /materials/conflicts/{id}/review` endpoints in `src/oralia/interfaces/api/routers/materials.py`
- [X] T060 [US6] Build área técnica UI for reviewing pending `MaterialConflictRecord`s in `apps/web/src/routes/Tecnica.tsx`
- [X] T061 [US6] Integration test: two contradictory active materials produce both evidences plus a flagged conflict on a related query, in `tests/integration/test_material_conflict_detection.py` (Escenario D)
- [X] T062 [US6] Integration test: an unreviewed conflict keeps appearing as conflictive on subsequent matching queries in `tests/integration/test_material_conflict_persistence.py` (FR-022b)
- [X] T063 [US6] Integration test: `GroundingVerifierAgent` classifies a proposal touching a detected conflict as `conflictiva` in `tests/integration/test_grounding_conflict_verdict.py`

**Checkpoint**: User Stories 1–6 funcionales de forma conjunta e independiente

---

## Phase 9: User Story 7 - Degradar de forma controlada ante un fallo de indexación (Priority: P3)

**Goal**: un fallo de extracción/indexación produce un error accionable sin activar el
documento y sin afectar al índice ya existente; la reconstrucción del índice es segura
ante solicitudes concurrentes y preserva referencias existentes

**Independent Test**: forzar el fallo de extracción de un archivo de prueba y verificar
que el índice existente sigue respondiendo consultas con normalidad

### Implementation for User Story 7

- [X] T064 [US7] Implement extraction/indexing failure handling (`status=error`/`not_processable`, `error_detail`, no activation, existing index untouched) in `src/oralia/application/commands/ingest_material.py` (FR-027)
- [X] T065 [US7] Implement the `rebuild_material_index` command using `index_rebuild_lock_service` (T012) in `src/oralia/application/commands/rebuild_material_index.py` (FR-016, FR-016a)
- [X] T066 [US7] Implement `POST /materials/index/rebuild` endpoint (`409` if a rebuild is already in progress) in `src/oralia/interfaces/api/routers/materials.py`
- [X] T067 [US7] Ensure retrieval queries during an in-progress rebuild are served against the last fully-built index version, not a partially-rebuilt one, in `src/oralia/infrastructure/vector_store/chroma_store.py`
- [X] T068 [US7] Failure test: a corrupt or unextractable file ends in `error`/`not_processable` with an actionable message, and the existing index keeps serving queries normally, in `tests/failure/test_material_indexing_failure.py` (Escenario F)
- [X] T069 [US7] Failure test: two simultaneous index-rebuild requests — one succeeds, the other gets `409` — in `tests/failure/test_material_index_rebuild_conflict.py`
- [X] T070 [US7] Integration test: after a rebuild, existing `Evidence`/`GroundingVerificationResult`/`MaterialConflictRecord` references remain valid (no orphaned fragment ids) in `tests/integration/test_material_index_rebuild_integrity.py` (FR-016a)
- [X] T071 [US7] Integration test: a query executed during an in-progress rebuild is served against the last complete index version in `tests/integration/test_material_query_during_rebuild.py`

**Checkpoint**: todas las historias de usuario funcionales de forma independiente

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: mejoras que afectan a varias historias de usuario

- [X] T072 [P] Accessibility pass on the new área técnica materials screens (keyboard nav, labels, contrast, non-color-only errors) in `apps/web/src/routes/Tecnica.tsx` (FR-032)
- [X] T073 [P] Unit tests for the deterministic segmenter's reproducibility across repeated runs with the same config in `tests/unit/test_segmenter_reproducible.py` (FR-007)
- [X] T074 [P] Unit tests for document-content-hash duplicate detection in `tests/unit/test_document_hash_duplicate.py` (FR-005)
- [X] T075 Write installation/configuration/execution/testing/limitations documentation for this feature (new dependencies, ChromaDB data directory, model download) extending `docs/001_core_runtime_instalacion.md` or a new `docs/002_materials_rag_instalacion.md`
- [X] T076 Run full `quickstart.md` validation (Escenarios A–G) and record evidence in `specs/002-materials-rag/quickstart-validation-evidence.md`
- [X] T077 Constitutional conformance self-review against `.specify/memory/constitution.md`, documented in `specs/002-materials-rag/constitution-conformance-review.md`
- [X] T078 Code cleanup and refactoring pass across `src/oralia/domain/materials/`, `infrastructure/documents/`, `infrastructure/embeddings/`, `infrastructure/vector_store/`

---

## Phase 11: Analyze Remediation (closes /speckit-analyze findings E1, F1, F3, F4)

**Purpose**: cierra huecos de cobertura detectados por `/speckit-analyze` entre `spec.md`
y `tasks.md` — ningún hallazgo era CRITICAL, pero los cuatro dejaban un requisito con FR
propio sin tarea dedicada

- [X] T079 [P] [US1] Failure test: assigning a retired or inactive material version to a new activity is rejected in `tests/failure/test_material_version_assignment_rejected.py` (FR-013a)
- [X] T080 [US1] Extend `get_material_catalog` (T021) to compute and expose a coverage/error summary (documents processed vs. `not_processable`/`error`) per course, surfaced via `GET /materials/documents/{id}`, in `src/oralia/application/queries/get_material_catalog.py` (FR-010)
- [X] T081 [P] [US1] Integration test: the coverage/error summary for a course's material set matches the actual processing outcomes in `tests/integration/test_material_coverage_report.py` (FR-010)
- [X] T082 [P] Unit test: extracted `MaterialFragment.text` is only ever passed as structured data/content to downstream agents, never interpolated into an instruction/prompt string, in `tests/unit/test_material_text_never_instruction.py` (FR-028, Edge Case)
- [X] T083 Run the complete Feature 001 test suite (`tests/` excluding this feature's new test files) after this feature's implementation and record a 0-regressions confirmation in `specs/002-materials-rag/quickstart-validation-evidence.md` (FR-030)

**Checkpoint**: cobertura de tareas para FR-013a, FR-010, FR-028 y FR-030 cerrada

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias — puede empezar de inmediato
- **Foundational (Phase 2)**: depende de Setup — BLOQUEA todas las historias de usuario
- **User Story 1 (Phase 3)**: depende solo de Foundational
- **User Story 2 (Phase 4)**: depende de Foundational; requiere al menos un documento activo de US1 para probarse de extremo a extremo, aunque su implementación (el agente de recuperación en sí) no depende del código de US1
- **User Story 3 (Phase 5)**: depende de Foundational; usa la evidencia que produce US2 para evaluarla, pero su agente (`GroundingVerifierAgent`) es un archivo distinto e independiente
- **User Story 4 (Phase 6)**: extiende el mismo archivo que crea US2 (`material_retriever_agent.py`) — requiere US2 completada primero
- **User Story 5 (Phase 7)**: depende de Foundational y de que exista al menos un documento de US1
- **User Story 6 (Phase 8)**: extiende el mismo archivo que crean US2/US4 (`material_retriever_agent.py`) — requiere US2 y US4 completadas primero
- **User Story 7 (Phase 9)**: depende de Foundational (T012, el servicio de bloqueo) y de US1 (el comando `ingest_material` que extiende)
- **Polish (Phase 10)**: depende de todas las historias que se quieran pulir
- **Analyze Remediation (Phase 11)**: T079 depende de US1 (T020); T080–T081 dependen de US1 (T021); T082 es independiente (puede ejecutarse en cualquier momento tras Foundational); T083 depende de que todas las historias de esta feature estén implementadas

### User Story Dependencies

- **US1 (P1)**: sin dependencias de otras historias de esta feature
- **US2 (P1) 🎯 MVP**: independiente en su propio código; su prueba de extremo a extremo requiere un documento activo de US1
- **US3 (P2)**: agente independiente de US2, pero su prueba de extremo a extremo consume evidencia producida por US2
- **US4 (P2)**: extiende el archivo de US2 — secuencial respecto a US2
- **US5 (P2)**: independiente de US2/US3/US4 en código; solo depende de US1
- **US6 (P3)**: extiende el archivo de US2/US4 — secuencial respecto a ambas
- **US7 (P3)**: extiende el comando de US1 (`ingest_material`) y usa el servicio de Foundational (T012)

### Within Each User Story

- Tests antes de la implementación correspondiente
- Modelos/adaptadores de Foundational ya disponibles antes de cualquier historia
- Comandos de aplicación antes de endpoints de la API
- Endpoints antes de la UI que los consume
- Lógica principal antes de pruebas de integración/fallo

### Parallel Opportunities

- Todas las tareas [P] de Setup (T003–T004) en paralelo
- T007–T011 de Foundational en paralelo (adaptadores en archivos distintos)
- Dentro de US1: T014–T017 (contract tests) en paralelo
- US3 y US5 pueden implementarse en paralelo por desarrolladores distintos una vez
  completada US2 (US3 no toca `material_retriever_agent.py`; US5 no lo toca tampoco)
- US4 y US6 NO pueden paralelizarse entre sí ni con US2 (los tres tocan el mismo
  archivo `material_retriever_agent.py` en secuencia: US2 → US4 → US6)
- US1 (T023) y US6 (T060) tocan el mismo archivo frontend `apps/web/src/routes/Tecnica.tsx`
  — si se desarrollan en paralelo (ver Parallel Team Strategy), T060 debe secuenciarse
  después de que T023 esté mergeada, aunque US1 y US6 sean independientes en el backend

---

## Parallel Example: Foundational

```bash
# Lanzar los adaptadores de Foundational en paralelo (archivos distintos):
Task: "Implement the VectorStore interface and ChromaDB adapter in src/oralia/infrastructure/vector_store/chroma_store.py"
Task: "Implement the EmbeddingAdapter interface and sentence-transformers adapter in src/oralia/infrastructure/embeddings/sentence_transformer_adapter.py"
Task: "Implement the deterministic text segmenter in src/oralia/domain/materials/segmenter.py"
Task: "Implement the DocumentExtractor interface plus PDF/DOCX adapters in src/oralia/infrastructure/documents/"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational (CRÍTICO — bloquea todas las historias)
3. Completar Phase 3: User Story 1 (necesaria para tener un documento activo)
4. Completar Phase 4: User Story 2 — **STOP y VALIDAR**: ejecutar Escenario A de
   `quickstart.md` de forma independiente
5. Demostrar el MVP (incorporación + recuperación con procedencia trazable)

### Incremental Delivery

1. Setup + Foundational → base lista
2. US1 → materiales incorporables y activables
3. US2 → MVP demostrable (Escenario A completo)
4. US3 → fundamentación e insuficiencia de evidencia verificables (Escenario C)
5. US4 → aislamiento de autorización verificable (Escenario E)
6. US5 → sustitución/retirada de versiones verificable (Escenario B)
7. US6 → conflicto entre fuentes verificable (Escenario D)
8. US7 → fallo de indexación y reconstrucción de índice verificables (Escenario F)
9. Polish → accesibilidad, documentación, revisión de conformidad constitucional

### Parallel Team Strategy

Con más de un desarrollador:

1. El equipo completa Setup + Foundational en conjunto
2. Una vez lista Foundational:
   - Desarrollador A: US1, después US5 (ambas independientes de
     `material_retriever_agent.py`)
   - Desarrollador B: US2, después US4, después US6 (secuencial — mismo archivo backend;
     además, la UI de US6/T060 debe esperar a que la UI de US1/T023 esté mergeada en
     `Tecnica.tsx` — ver Parallel Opportunities)
   - Desarrollador C: US3 (independiente, consume evidencia de US2 solo para probar)
   - Tras US1: cualquiera libre toma US7 (extiende `ingest_material` de US1)

---

## Notes

- [P] = archivos distintos, sin dependencias pendientes
- [Story] = mapea la tarea a su historia de usuario para trazabilidad
- Cada historia de usuario debe quedar completable y probable de forma independiente
- Verificar que los tests fallan antes de implementar
- Confirmar (checkpoint) cada historia de usuario de forma independiente antes de seguir
- Evitar: tareas vagas, conflictos de archivo entre tareas [P], dependencias entre
  historias que rompan su independencia — nótese la excepción documentada arriba
  (US2/US4/US6 comparten un archivo por diseño, ya que las tres extienden el mismo
  agente de recuperación)

---

## Phase 12: Convergence

- [X] T084 **[Implementada en esta ronda, 2026-09-12 — ver diff abajo; dependía de
  T089 — reproducción ejecutada antes de corregir]** Implemented in
  `src/oralia/domain/agents/grounding_verifier_agent.py`: `_claim_is_supported`
  replaces the raw lexical-overlap check with four chained comparisons (research.md
  §11) — (1) lexical overlap, unchanged; (2) clause alignment
  (`_best_aligned_clauses`, new — splits evidence into clauses by sentence and by
  bounded conjunctions "y"/";"/"pero", preferring the clause that shares an
  entity label — `_entity_labels`, single-uppercase-letter tokens — with the claim,
  so a multi-entity evidence text doesn't let one entity's number validate another
  entity's claim); (3) polarity (`_is_negated` — a lexical negation-marker set, {no,
  nunca, tampoco, jamás}, compared between claim and aligned clause); (4) numeric
  value (`_extract_value` — digits/decimals or simple+compound Spanish cardinal words
  cero–diez/veinte–noventa/cien, with a bounded recognized-unit list) — mismatched
  value or incompatible declared units MUST classify as `no_fundamentada`.
  `_split_claims` additionally separates a provenance/attribution clause ("como se
  explica en"/"según"/"de acuerdo con" + a concrete reference noun — página, capítulo,
  sección, apartado, anexo, tabla, figura) into its own claim. `ORALIA_GROUNDING_
  NUMERIC_TOLERANCE` — decided as `0` (exact match), a fixed constant, not yet exposed
  as an env var (no evidence of need beyond the fixed default). Per the acceptance
  matrix in `research.md` §11 (S1/C1/C2/C3/NEG1/NEG2/NEG-unrelacionada/I1/I2/V1/V2/
  CIEN/MULTI/UNIT — all with defined expected outcomes, verified against the real
  agent) per FR-023 (contradicts)

  **Evidencia**: matriz 19/19 en verde (`tests/contract/test_grounding_verifier.py`);
  pruebas de integración/unit ya existentes sin cambios y en verde (conflictiva,
  evidencia vacía + conocimiento general, mapeo de veredicto, no-agregación, parcial —
  6/6); nueva prueba de integración con autoestudio real (`tests/integration/
  test_grounding_blocks_contradicting_proposal_in_self_study.py`, verificador real, sin
  mock del veredicto) — 1/1. Regresión completa 001+002+003: 281 passed, 1 deselected
  (antes: 266; +15 = 14 casos/pruebas nuevas de la matriz + 1 prueba de integración
  nueva, 0 regresiones). Ruff: 49 → 50 (transitorio, una línea larga propia, corregida)
  → 49 (estado final, igual que la referencia previa a H03). Se detectó y corrigió
  durante la implementación (no un hallazgo separado, parte de esta misma tarea) una
  regresión propia: separar cualquier "según X" sin exigir un sustantivo de referencia
  concreto rompía `test_query_outside_coverage_never_yields_fundamentada` (un "según el
  documento" genérico coincidía por azar con cualquier evidencia que mencionara
  "documento") — corregido exigiendo el sustantivo de referencia, ver research.md §11.
- [X] T085 **[Implementada y validada en esta ronda, 2026-09-12g]** Replace the fixed
  `over_fetch = max(max_fragments * 4, max_fragments)` candidate window in
  `src/oralia/domain/agents/material_retriever_agent.py` with progressive widening that
  stops on the first of four conditions: `max_fragments` authorized/current candidates
  collected, `time_budget_ms` exhausted, the store returns fewer candidates than
  requested (corpus exhausted), or two successive widenings return no new candidate
  ids — per the corrected design in `research.md` §14.1 (the first-round design lacked
  the last two stopping conditions and could re-query the same exhausted set until the
  budget ran out). Also add a relevance-floor check on `relevance_score` — value not
  fixed here, left to this task, justified by the new Escenario C.1 (`quickstart.md`,
  research.md §14.2) — retracts the first round's absolute "MUST NOT apply any
  threshold" per FR-017/FR-019/FR-019a (partial)

  **Algoritmo final** (`_run_widening_search`, `research.md §14.1a/§14.2a` para el
  detalle completo): ventana inicial `k = max(max_fragments*4, max_fragments)`,
  duplicada cada ronda (`_WIDENING_FACTOR=2`); cada ronda reconstruye `selected`
  desde cero a partir del orden de esa ronda (nunca se acumula sobre rondas
  anteriores, garantizando deduplicación y que el orden más reciente del almacén
  nunca quede subordinado a uno más antiguo); `seen_ids`/`fragment_rows_cache`
  evitan volver a consultar SQL por ids ya vistos. Condición (d) implementada como
  contador de rondas consecutivas sin ids nuevos (`stale_rounds`,
  `_STALE_ROUNDS_LIMIT=2`), no como comparación de conjuntos — corrige la redacción
  de `research.md` §14.1 vigente hasta esta ronda. Umbral de relevancia:
  `_DEFAULT_RELEVANCE_THRESHOLD=0.35`, constante con nombre, configurable solo al
  construir `MaterialRetrieverAgent` (parámetro `relevance_threshold`), nunca
  expuesto en `MaterialQueryInput`; comparación `math.isfinite(score) and score >=
  threshold` (límite inclusivo, no finitos descartados de forma segura).

  **Reproducción T090, antes/después**: contra el código pre-T085,
  `test_h08a_authorized_fragment_beyond_fixed_window_is_not_lost` y
  `test_h08b_irrelevant_query_over_nonempty_authorized_corpus_yields_no_fragments`
  fallaban (2/3); `test_h08b_relevant_fragment_above_threshold_is_kept` ya pasaba.
  Tras T085, mismas aserciones sin cambios: 3/3 en verde
  (`tests/integration/test_material_retrieval_h08_reproduction.py`, archivo
  byte-a-byte idéntico al de T090 — hash SHA-256 verificado sin cambios).

  **Pruebas estructurales nuevas** (`tests/integration/
  test_material_retrieval_widening_structural.py`, 13 pruebas): cobertura de las
  cuatro condiciones de parada, deduplicación intra-ronda (defecto real encontrado y
  corregido durante esta tarea — un `fragment_id` repetido dentro de una misma
  ronda no se deduplicaba; se añadió `used_ids` en `_claim`... en
  `_run_widening_search`), orden final por relevancia de la última ronda útil,
  bloqueo/conflictos una sola vez sobre la selección final, umbral en el límite
  (0.35 aceptado, 0.349999 rechazado), valores no finitos, contraste mixto explícito
  del umbral (0.70 incluido, 0.20/0.10 excluidos, sin tocar la aserción histórica de
  T090), y `max_fragments <= 0` sin consultar el almacén (`_SpyVectorStore`).

  **Descubrimiento y corrección cross-feature (autorizada explícitamente durante
  esta tarea)**: la regresión completa reveló 4 pruebas de Feature 003 rotas por un
  acoplamiento implícito no documentado previamente — `self_study_agency_composer.py`
  asumía que la recuperación siempre devolvía el conjunto completo de fragmentos
  autorizados/vigentes. Diagnosticado con precisión (revirtiendo temporalmente el
  umbral a 0.0 para confirmar la causa antes de corregir nada) y corregido en ese
  archivo — ver research.md §14.2a para el detalle completo de la causa y los 4
  puntos de corrección aplicados (rotación de `concepts_pending` ya no se invalida
  contra el conjunto reducido de la ronda; fragmento en cola resuelto por SQL directo
  si no aparece en la ronda actual; `nivel_0_skip` decidido sobre `active_fragments`;
  consultas de adaptación reutilizan `previous_turn.input_text`). Las 4 pruebas antes
  rotas pasan tras la corrección.

  **Efectos laterales verificados una sola vez, solo sobre la selección final**:
  `_log_blocked_attempt` — un único `trace_service.record_event` pese a candidatos
  no autorizados en múltiples rondas
  (`test_blocked_out_of_scope_attempt_is_logged_once_across_several_widenings`).
  `_detect_and_record_conflicts` — recibe exclusivamente `selected`, nunca
  candidatos descartados por autorización/vigencia/relevancia
  (`test_discarded_candidates_never_reach_conflict_detection`, con un espía sobre
  `detect_conflicts`).

  **`max_fragments <= 0`**: `fragments = []` sin invocar `store.query(...)` en
  absoluto (`test_max_fragments_zero_or_negative_returns_empty_without_querying_store`,
  valores 0/-1/-5). Corrige la fisura documentada por T090 (el suelo `max(k,1)` de
  `ChromaVectorStore.query` combinado con el corte posterior al append del bucle
  anterior podía devolver hasta 1 fragmento). El esquema HTTP
  (`MaterialQueryInput`) sigue sin validar este ni `time_budget_ms` — no convertido
  en `422` en esta tarea.

  **Regresión y análisis estático**: 345 passed, 1 deselected (antes de esta tarea,
  con las reproducciones T090 deliberadamente rojas: 330 passed + 2 failed + 1
  deselected; +16 nuevos entre T090 ya en verde + 13 estructurales + 1 test fijado
  en Feature 003, 0 regresiones tras la corrección cross-feature). Ruff: 0 errores en
  los 4 archivos modificados/creados
  (`material_retriever_agent.py`, `self_study_agency_composer.py`,
  `test_material_retrieval_h08_reproduction.py` —sin cambios, solo releído—,
  `test_material_retrieval_widening_structural.py` —23 errores transitorios
  corregidos por reformateo, no por relajar ninguna aserción—); recuento global sin
  cambios, 49 (45 E501, 2 F401, 1 F541, 1 F841 — idénticos a la referencia previa,
  todos heredados). Comandos: `PYTHONPATH=src uv run pytest
  tests/integration/test_material_retrieval_h08_reproduction.py -v`; `PYTHONPATH=src
  uv run pytest tests/integration/test_material_retrieval_widening_structural.py -v`;
  `PYTHONPATH=src uv run pytest tests/ -q -m "not ollama and not speech"`; `uv run
  ruff check src/ tests/ --statistics`; `uv run ruff check
  src/oralia/domain/agents/material_retriever_agent.py
  src/oralia/application/orchestration/self_study_agency_composer.py
  tests/integration/test_material_retrieval_widening_structural.py
  tests/integration/test_material_retrieval_h08_reproduction.py --statistics`.

  **No corregido en esta tarea, registrado por separado**: la revalidación de
  `MaterialFragment.course_id` contra el `course_id` solicitado en SQL — ver T098
  más abajo (nueva tarea de seguimiento entonces; implementada y validada
  posteriormente, ver T098 para su evidencia).
- [X] T086 **[Implementada y validada en esta ronda, 2026-09-13 — depende de T091,
  ejecutada primero]** Make the blocking
  `self._embedder.embed(...)`/`self._store.query(...)` calls inside
  `MaterialRetrieverAgent.execute`/`_run_widening_search` (same file as T085) run
  through a NEW, capacity-bounded, process-wide `BoundedBlockingWorker`
  (`src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py`) — not a bare
  `asyncio.to_thread(...)` (research.md §12, corrected in T091: the default executor's
  bounded worker count does not bound its own pending-work queue, so `to_thread` alone
  gives no real backpressure) — so `run_with_deadline`'s `asyncio.wait_for` (Feature
  001, unchanged) can actually preempt the wait at the turn's `deadline_ms`.
  `execute()` does NOT catch the resulting `asyncio.CancelledError` to fabricate a
  `status = "ok"` partial result. `self._db` access (fragment lookup, conflict
  recording, trace logging) stays on the main/event-loop thread only — never inside
  the worker thread (verified by thread-identity instrumentation, not assumed). Per
  `research.md` §12/§12.1 (implemented) per FR-018/Constitution Principio IX
  (resolved) — evidence below. **Cierre efectivo: ver T100 más abajo** — una revisión
  posterior encontró que el mecanismo de admisión de esta entrada (`_LoopScopedSemaphore`)
  no era realmente process-wide entre bucles de eventos simultáneos, además de una
  fuga de permiso y un singleton sin exclusión mutua; T100 corrige las tres sin
  reabrir ni reescribir la evidencia de esta entrada.
- [X] T100 **[Corrección de convergencia, implementada y validada en esta ronda,
  2026-09-13 — depende de T086]** Fix three structural admission bugs found in T086's
  `BoundedBlockingWorker`: (R1) `_LoopScopedSemaphore` rebuilt a full, fresh semaphore
  per event loop instead of sharing one pool, silently multiplying capacity across
  concurrent loops in different threads; (R2) `run()` leaked the admission permit if
  `executor.submit()` itself raised; (R3) `default_blocking_retrieval_worker()`'s lazy
  singleton had no mutual exclusion. Replaces `_LoopScopedSemaphore` with
  `_ProcessWideAdmission` (one shared pool of permits behind a single `threading.Lock`,
  waiters tied to their own event loop, correctly handling waiter cancellation, waiter
  loop closure, and cross-thread release races). Per `research.md` §12.2 (implemented)
  — evidence below
- [X] T087 **[Corregida en la 2ª ronda — ver diff abajo; depende de T092 —
  reproducción antes de corregir]** Implement the two combined
  mechanisms in `research.md` §13 (corrected — releasing the version at `query()` start
  alone does not close the race, it only shrinks it): (a) bounded retirement — `rebuild()`
  keeps the current and immediately-previous generations, deleting only `N-2` once `N`
  completes; (b) `query()` catches a "collection not found" error, re-reads
  `index_version.json`, and retries against the actually-current version (bounded
  attempts), reporting the version it actually used — MUST NOT silently recreate a
  deleted collection as empty via `get_or_create_collection`; (c) atomic version-pointer
  write (`temp file` + `os.replace`). Also make `ingest_material.py`'s
  `store.add(...)` call acquire the same `index_rebuild_lock_service` lock
  `rebuild_material_index.py` already uses (first round incorrectly claimed
  `add`/`delete`/`rebuild` were "all protected" — only `rebuild` was; `delete()` has no
  caller today). Extend `tests/integration/test_material_query_during_rebuild.py` with
  a genuinely coordinated interleaving (event/barrier-based, not `sleep`-based): a
  reader resolves version N, the pointer/retirement change happens, the reader
  continues — per FR-016/FR-016a (missing)
- [X] T088 [P] Regression: run the existing Feature 002 suite covering these two agents
  (`tests/contract/test_grounding_verifier.py`,
  `tests/integration/test_grounding_conflict_verdict.py`,
  `tests/integration/test_grounding_general_knowledge_label.py`,
  `tests/integration/test_grounding_insufficient_evidence.py`,
  `tests/integration/test_grounding_verdict_mapping.py`,
  `tests/unit/test_grounding_no_aggregation.py`, `tests/unit/test_grounding_partial.py`,
  `tests/integration/test_material_query_during_rebuild.py`,
  `tests/integration/test_material_retrieval_limits.py`,
  `tests/integration/test_material_retrieval_repeatable.py`,
  `tests/failure/test_material_retrieval_budget.py`) after T084–T087 and confirm no
  prior passing case (S1 in particular) changes verdict, per FR-030 (missing)

---

## Phase 13: Convergence

- [X] T089 **[Corregida y ejecutada en esta ronda, 2026-09-12 — precisión documental]**
  [P] Reproduction for T084 — extend `tests/contract/test_grounding_verifier.py` (real
  code path: `GroundingVerifierAgent().execute()`, never a copy of its logic) with
  parametrized cases asserting the **CORRECT** required behavior per FR-023 and
  `research.md` §11's matrix — case C1 MUST assert `verdict == "no_fundamentada"` for
  claim "El agua hierve a 20 grados." against evidence "El agua hierve a 100 grados."
  The assertion MUST be `"no_fundamentada"` — never `"fundamentada"` re-described as
  "the failing reproduction" (the previous wording of this task was ambiguous exactly
  this way and is corrected here, same error already fixed once for 001/T089). Run
  against the current (unreinforced) agent and confirm it **fails** (returns
  `fundamentada`) — that failure is the reproduction; assertions MUST NOT change
  between the failing and the passing run. MUST run and fail before T084 per FR-023
  (missing)

  **Evidencia**: ejecutada contra el `GroundingVerifierAgent` sin reforzar — 9 fallos
  (C1, C2, C3, V1, V2, NEG1, MULTI, UNIT del caso único, más el caso de procedencia
  parcial I2) sobre 19 casos nuevos totales; 5 pruebas previas del archivo ya en verde.
  Tras T084, los 19 casos nuevos con las mismas aserciones: 19/19 en verde (24 en total
  con las 5 previas).
- [X] T090 **[Ejecutada en esta ronda, 2026-09-12g — reproducción previa a T085; T085
  SIGUE SIN IMPLEMENTARSE]** [P] Baseline reproduction for T085 — write and run, against the current
  `MaterialRetrieverAgent`, a test with a course where over 75% of the candidates
  within the fixed `over_fetch` window are unauthorized/expired, confirming an
  authorized fragment beyond that window is currently dropped — record the failing
  baseline before T085 changes the widening strategy. MUST run and fail before T085 per
  FR-019/FR-019a (missing)

  **Alcance ejecutado (H08, dos defectos independientes, `research.md` §14.1 y §14.2)**:
  nuevo archivo `tests/integration/test_material_retrieval_h08_reproduction.py`, tres
  pruebas contra el `MaterialRetrieverAgent` real, con un doble `VectorStore`
  (`_OrderedCandidateVectorStore`, devuelve los primeros `k` de una lista de
  candidatos preordenada, ignora `embedding`/`filters`) y un doble `EmbeddingAdapter`
  (`_FixedEmbeddingAdapter`, vector fijo — el contenido del vector es irrelevante
  porque el doble de `VectorStore` no lo usa). `MaterialRetrieverAgent` no se modifica.
  Filas SQL reales (`Course`/`MaterialDocument`/`MaterialFragment`) vía `db_session`,
  igual que `tests/unit/test_material_retirement_vs_deactivation.py`.

  **H08.A — ventana fija (`test_h08a_authorized_fragment_beyond_fixed_window_is_not_lost`)**:
  `max_fragments=2` → `over_fetch = max(2*4, 2) = 8` (confirmado leyendo
  `material_retriever_agent.py:72`, no asumido). 11 candidatos: posiciones 1-4 con
  `activity_configuration_ids=["act-other"]` (excluidos por `_authorized`), 5-8 con
  `valid_until` en el año 2000 (excluidos por `_is_retrievable`/FR-019a), 9-11
  autorizados/activos/indexados/vigentes (relevancia 0.80/0.79/0.78, muy por encima de
  cualquier umbral futuro). Todos comparten `course_id` (mide solo el filtrado
  posterior, no aislamiento por asignatura). Aserción: `fragments` debe contener los
  fragmentos de las posiciones 9 y 10 (los dos primeros autorizados, `max_fragments=2`)
  — nunca que se pierdan. **Fallo observado contra el código actual**: `fragments = []`;
  diagnóstico capturado (no acoplado a la aserción): `store.queried_k == [8]` — el
  agente nunca llegó a pedir las posiciones 9-11 porque la única consulta al almacén
  pidió k=8.

  **H08.B — ausencia de umbral de relevancia, negativo
  (`test_h08b_irrelevant_query_over_nonempty_authorized_corpus_yields_no_fragments`)**:
  corpus autorizado/vigente no vacío, 4 candidatos con `relevance_score` en
  [0.06, 0.22] (por debajo del umbral propuesto de 0.35, justificado abajo). Aserción:
  `fragments == []`, con una advertencia que mencione pertinencia/relevancia,
  distinguible de `"presupuesto temporal agotado"` y de `"agotado para esta consulta"`
  (corpus agotado, research.md §14.1). **Fallo observado contra el código actual**:
  `fragments` contiene los 4 candidatos irrelevantes — hoy no existe ningún filtro de
  relevancia (`material_retriever_agent.py:96`, `selected.append(...)` incondicional).

  **H08.B — contraste positivo
  (`test_h08b_relevant_fragment_above_threshold_is_kept`)**: un candidato a 0.70
  (dentro del rango positivo medido) junto a ruido irrelevante a 0.20/0.10 — el
  fragmento relevante MUST seguir en `fragments`. **Ya pasa hoy** (comportamiento ya
  correcto, sin necesitar T085) — incluido para compartir exactamente el mismo montaje
  que la reproducción negativa.

  **Medición previa del umbral (research.md §14.2 — "sin un valor fijado aquí,
  justificado por un escenario real")**: antes de fijar 0.35, se midió la distribución
  real de `relevance_score` con el modelo (`SentenceTransformerEmbeddingAdapter`,
  `paraphrase-multilingual-MiniLM-L12-v2`) y el almacén (`ChromaVectorStore`,
  `hnsw:space=cosine`, `relevance_score = 1 - distancia_coseno`) configurados por el
  proyecto — script exploratorio ejecutado desde el scratchpad de la sesión contra un
  índice Chroma temporal (`tempfile.mkdtemp`, borrado al finalizar) — **no se añadió
  ningún archivo, modelo, caché ni resultado de benchmark al repositorio**. Corpus: 4
  temas (Python, fotosíntesis, Revolución Francesa, digestión), 9 fragmentos
  parafraseados. 5 consultas positivas (2 literales, 3 parafraseadas) + 4 negativas
  claramente ajenas (tortilla de patatas, clima en la Antártida, fútbol, viajes) — no
  solo el par programación/tortilla. Resultado: positivas
  `[0.8130, 0.6212, 0.7187, 0.6593, 0.7705]` (mínimo 0.6212, la parafraseada sobre
  Python); negativas `[0.2162, 0.1535, 0.1189, 0.0583]` (máximo 0.2162, "receta de
  tortilla de patatas" — coincide con el propio ejemplo de Escenario C.1). Separación
  limpia: hueco de 0.4050 entre el mínimo positivo y el máximo negativo.

  **Umbral propuesto: 0.35** (no implementado en código esta ronda — T085 sigue sin
  tocarse). Justificación cuantitativa: 0.134 por encima del negativo más alto
  observado (0.2162) y 0.271 por debajo del positivo más débil observado (0.6212) —
  deliberadamente más cerca del lado negativo que del positivo: el riesgo de rechazar
  una afirmación genuinamente respaldada (falso positivo de "sin pertinencia",
  pedagógicamente peor — el sistema negaría tener información que sí tiene) se
  considera más costoso que el de aceptar un fragmento marginalmente relacionado
  (falso negativo de "sin pertinencia"), así que el margen de seguridad se concentra
  del lado de no rechazar contenido relevante. Riesgo documentado: la medición cubre
  solo 9 fragmentos/9 consultas — un corpus real más diverso podría producir
  paráfrasis más débiles que 0.6212 o negativos más fuertes que 0.2162; 0.35 es un
  punto de partida conservador para T085, no un valor definitivo, y MUST revalidarse
  con datos de producción o un corpus de referencia más amplio antes de considerarlo
  cerrado. Si la separación no hubiera sido limpia (huecos solapados), el umbral fijo
  no sería defendible y T085 debería considerar una señal relativa (p. ej. margen
  entre el primer y segundo candidato) en vez de un valor absoluto — no aplica aquí,
  dado el hueco de 0.4050.

  **Resultados separados (por instrucción explícita — no se esperó verde en un único
  run con las reproducciones deliberadamente rojas incluidas)**:
  1. Suite previa excluyendo el archivo nuevo: `PYTHONPATH=src uv run pytest tests/ -q
     -m "not ollama and not speech" --ignore=tests/integration/
     test_material_retrieval_h08_reproduction.py` → 329 passed, 1 deselected (idéntico
     a la referencia previa a esta ronda, 0 regresiones).
  2. Nuevas reproducciones: `PYTHONPATH=src uv run pytest tests/integration/
     test_material_retrieval_h08_reproduction.py -v` → **2 failed** (H08.A, H08.B
     negativo — las causas esperadas, descritas arriba), **1 passed** (contraste
     positivo H08.B).
  3. Ruff: `uv run ruff check tests/integration/
     test_material_retrieval_h08_reproduction.py --statistics` → 0 errores (una
     advertencia B007 inicial por una variable de bucle no usada, corregida antes de
     esta entrega). `uv run ruff check src/ tests/ --statistics` → 49 errores globales,
     idénticos a la referencia previa (45 E501, 2 F401, 1 F541, 1 F841, todos
     heredados).

  **Condiciones y fisuras revisadas para el futuro diseño de T085 (analizadas, NO
  corregidas esta ronda)**:
  - *Detención al reunir `max_fragments` válidos / al agotar `time_budget_ms` /
    `len(matches) < k` / dos ampliaciones sin ids nuevos* (research.md §14.1): ninguna
    existe hoy porque no hay bucle (una sola llamada a `store.query`) — sin fisura
    detectada en el diseño ya documentado, solo pendiente de implementarse en T085.
  - *Deduplicación por `fragment_id` entre ampliaciones*: **riesgo real para T085**:
    una ampliación posterior con `k` mayor vuelve a pedir desde el principio y puede
    reincluir ids ya vistos en una ronda anterior — T085 MUST llevar un conjunto
    `seen_ids` y filtrar duplicados entre rondas; no existe hoy (no hay rondas).
  - *Orden determinista de los resultados* (FR-020): **riesgo real para T085**: cada
    llamada a `store.query` devuelve su propio top-k reordenado por Chroma; concatenar
    ingenuamente los resultados de sucesivas ampliaciones sin reordenar por
    `relevance_score` al final podría producir un orden no estrictamente decreciente
    en el conjunto acumulado. T085 MUST reordenar (o garantizar el orden) del conjunto
    final antes de truncar a `max_fragments`.
  - *No ejecutar detección de conflictos sobre candidatos descartados*: confirmado que
    hoy `_detect_and_record_conflicts` solo recibe `selected` (ya filtrado) — T085 MUST
    preservar esto: la detección de conflictos se ejecuta una única vez, tras terminar
    el bucle de ampliación completo, nunca por ronda.
  - *No registrar varias veces el mismo intento fuera de alcance*: confirmado que hoy
    `_log_blocked_attempt` se invoca una sola vez por `execute()` (después del bucle de
    selección, no dentro de él) — **riesgo real para T085**: si el futuro bucle de
    ampliación llama a esta función dentro de cada ronda en vez de una vez al final,
    registraría el mismo intento varias veces; T085 MUST mantener una única llamada
    por `execute()`.
  - *No acceder a SQL desde un hilo de trabajo (T086 aún no se implementa)*: confirmado
    — hoy todo el acceso a `self._db` ocurre en el hilo principal (no existe
    `asyncio.to_thread` todavía). Nota de compatibilidad futura, no una fisura de esta
    ronda: T085 MUST diseñar el bucle de ampliación de forma que, cuando T086 mueva
    `embed`/`store.query` a un hilo, el acceso a SQL (autorización, vigencia, registro
    de intentos bloqueados) siga ocurriendo exclusivamente en el hilo principal.
  - *`max_fragments <= 0`*: **fisura de comportamiento confirmada, no corregida**: el
    contrato (`contracts/material-retriever-agent.md`) y la API
    (`MaterialQueryInput.max_fragments: int = 5`, sin `Field(gt=0)`,
    `src/oralia/interfaces/api/routers/materials.py:182`) no lo validan. Con
    `max_fragments=0` (o negativo), `over_fetch = max(0, 0) = 0`, pero
    `ChromaVectorStore.query` fuerza `n_results=min(max(k, 1), collection.count())` —
    un suelo de 1 incluso pidiendo k=0 — y el bucle del agente comprueba
    `len(selected) >= max_fragments` **después** de añadir un candidato, así que
    `max_fragments=0` devuelve hasta 1 fragmento, no 0 como cabría esperar. No
    corregido aquí (no forma parte de H08 tal como está definido); documentado para
    que T085 lo tenga en cuenta si su nuevo bucle interactúa con este límite, o para
    registrarlo como un hallazgo propio si se decide corregirlo.
  - *`time_budget_ms <= 0`*: ya validado por
    `tests/failure/test_material_retrieval_budget.py` con `time_budget_ms=-1` — no
    rechazado por el contrato/API, pero el comportamiento resultante (advertencia de
    presupuesto agotado, `status="ok"`) ya es el esperado y está probado — no es una
    fisura para T085, solo confirma que tampoco hay validación de rango aquí.
  - *Aislamiento por `course_id` — SQL vs. filtro vectorial*: **riesgo separado,
    documentado, NO añadido a T090**: `MaterialFragment.course_id` existe como columna
    SQL (`models.py:312`), pero `_authorized`/`_is_retrievable` nunca la comparan
    contra el `course_id` de la petición — el aislamiento por asignatura depende
    EXCLUSIVAMENTE del filtro `where={"course_id": ...}` enviado a Chroma
    (`chroma_store.py` docstring: "Callers over-fetch by course_id and apply the
    remaining filters against SQL rows" — en la práctica, course_id nunca se
    revalida contra SQL, solo activity/vigencia/retirada). FR-019 menciona
    explícitamente "asignatura" como alcance que no debe filtrarse, así que este
    hallazgo pertenece potencialmente a FR-019 — pero es un defecto DISTINTO de los
    dos de H08 (ventana fija, umbral de relevancia), y ninguna prueba existente lo
    cubre (`test_query_for_activity_a_never_returns_activity_b_fragments`/
    `test_out_of_scope_activity_returns_empty_fragments_not_an_error` usan siempre el
    mismo `course_id` en ambos lados). No se amplía T090 con una reproducción para
    esto sin decisión explícita — se registra aquí como un hallazgo nuevo candidato a
    su propio hallazgo/tarea, fuera del alcance de T090.
- [X] T091 **[Ejecutada en esta ronda, 2026-09-13 — reproducción previa a T086; T086
  SIGUE SIN IMPLEMENTARSE]** [P] Baseline reproduction for T086 — write and run, with a controlled slow
  double of `EmbeddingAdapter`/`VectorStore` (deterministic delay, not a real model) and
  a `deadline_ms` shorter than that delay, confirming `run_with_deadline` currently
  returns `status = "ok"` (not `status = "timeout"`) for `MaterialRetrieverAgent` —
  record the failing baseline before T086 moves the blocking calls to a thread. MUST
  run and fail before T086 per FR-018 (missing) — evidence below
- [X] T092 **[Ejecutada en esta ronda, 2026-09-14 — reproducción previa a T087; T087
  SIGUE SIN IMPLEMENTARSE]** [P] Baseline reproduction for T087 — write and run, forcing the interleaving
  research.md §13 describes (a `ChromaVectorStore` instance resolving version N,
  followed by a `rebuild()` that completes and retires N under the current — pre-fix —
  synchronous-delete behavior), confirming the subsequent query on that instance
  currently fails or misbehaves — record the failing baseline before T087 changes the
  retirement/retry mechanism. MUST run and fail before T087 per FR-016/FR-016a
  (missing) — evidence below

---

## Phase 14: Convergence (seguimiento de H03 — 7 falsos positivos/negativos, 2026-09-12b)

**Contexto**: una revisión independiente ejecutó `GroundingVerifierAgent.execute()`
real sobre el código de T084 (seguimiento anterior) y encontró siete casos (F1–F7) mal
clasificados — cuatro falsos positivos por causas de extracción numérica ("un"/"una"
como valor, solo el primer valor de la cláusula, división de cláusulas rompiendo
numerales compuestos, signo no incluido en el valor) y dos falsos negativos por
manejo incorrecto de empates entre cláusulas de evidencia duplicada. Se registra como
regresión adicional de H03 — no como ampliación de T085/T086/T087 (recuperación/
timeout/reconstrucción), que siguen sin implementarse.

- [X] T093 **[Implementada y validada en esta ronda, 2026-09-12b]** Corrige, en
  `src/oralia/domain/agents/grounding_verifier_agent.py`: (1) `_extract_values`
  (renombrada desde `_extract_value`) devuelve **todos** los valores de una cláusula,
  no solo el primero, y ya NO trata "un"/"una" como numeral independiente (solo como
  prefijo de artículo ante un numeral real o inmediatamente ante una unidad
  reconocida); captura el signo `+`/`-` adyacente al dígito como parte del valor; (2)
  `_split_on_y` sustituye la división ciega por " y " — protege un numeral compuesto
  (decena + "y" + unidad 1-9) de partirse en dos cláusulas; (3)
  `_claim_is_supported`/`_claim_is_supported_by_clause` evalúan **cada** cláusula
  alineada por separado (polaridad + todos los valores, vía `_values_are_consistent`)
  en vez de aplicar un atajo fijo ante un empate — un empate ya NO se resuelve
  devolviendo `True` sin comprobar nada, ni `False` solo por existir; y distinguen
  explícitamente los tres casos de research.md §11 (a: sin afirmación numérica; b: con
  valor comparable; c: con valor pero sin contrapartida interpretable — nunca
  "fundamentada" por defecto). Sin excepciones literales para F1–F7 — verificado con
  contrastes propios (PROP-SEGUNDO-VALOR, PROP-MAGNITUD-NEGATIVA, reordenar
  evidencia). Per FR-023 (contradicts)

  **Reproducción**: ejecutados los 7 casos (F1–F7) más 2 propiedades contra el
  `GroundingVerifierAgent` de T084 (previo a esta corrección) — **8 fallos**
  (F1/F2/F3/F4/F7 del caso único, F5, F6, y la propiedad de reordenar evidencia — que
  depende de la misma corrección que F5), 22 aciertos (los 19 casos ya establecidos
  más F5/F6 marcados como fallo se cuentan aparte). Tras T093, mismas aserciones:
  30/30 en el archivo completo.

  **Integración**: nueva prueba con F1
  (`tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py::
  test_f1_contradicting_duration_never_reaches_participant_as_grounded`) — propuesta y
  evidencia controladas mediante dobles en sus fronteras (adaptador de generación,
  paso de recuperación), `GroundingVerifierAgent` real sin mock de veredicto; confirma
  que "20 minutos" no llega al participante y que `grounding_verdict` queda trazado
  como `no_fundamentada`.

  **Regresión y análisis estático**: 293 passed, 1 deselected (antes de esta tarea:
  281; +12 = 11 casos/pruebas nuevas de contrato + 1 prueba de integración nueva, 0
  regresiones). Ruff sobre los 3 archivos modificados: 2 líneas largas nuevas,
  corregidas; recuento global 49 → 51 (transitorio) → 49 (estado final, igual que la
  referencia previa a esta ronda).

  **Recuento preciso (corrige la entrega anterior)**: `tests/contract/
  test_grounding_verifier.py` tiene, tras esta tarea, 30 pruebas en total — 5 previas
  a H03, 14 de la primera ronda de H03 (12 parametrizadas + 2 de contrato), y 11 de
  esta ronda (7 del caso único F1/F2/F3/F4/F7 + 2 propiedades en el caso único +
  F5/F6/reordenar/lista-coherente como pruebas separadas). Comandos ejecutados esta
  ronda: `PYTHONPATH=src uv run pytest tests/contract/test_grounding_verifier.py -v`;
  `PYTHONPATH=src uv run pytest tests/integration/
  test_grounding_blocks_contradicting_proposal_in_self_study.py -v`; `PYTHONPATH=src
  uv run pytest tests/ -q -m "not ollama and not speech"`; `uv run ruff check src/
  tests/ --statistics`.

**No se declara toda la Feature 002 completada** — T085/T086/T087 (recuperación,
timeout, reconstrucción del índice) siguen pendientes, sin tocar ni duplicar.

## Phase 15: Convergence (seguimiento de H03 — R1-R3, defectos estructurales, 2026-09-12c)

**Contexto**: una revisión independiente confirmó que F1–F7 (T093) ya cumplen sus
resultados esperados, y ejecutando `GroundingVerifierAgent.execute()` real reprodujo
dos defectos estructurales adicionales dentro del mismo objetivo H03 — no una
ampliación de T085/T086/T087, que siguen sin implementarse. Se conserva sin
modificar la evidencia histórica de T084/T089/T093.

- [X] T094 **[Implementada y validada en esta ronda, 2026-09-12c]** Corrige, en
  `src/oralia/domain/agents/grounding_verifier_agent.py`: (1) introduce `_tag_roles`,
  que etiqueta `role="origin"`/`role="destination"` sobre la pareja de valores que
  encaja en el patrón "de VALOR ... a VALOR"; `_values_are_consistent` pasa a exigir,
  para un valor de la propuesta con `role` definido, un candidato de evidencia con el
  **mismo** `role` — ya no basta con que el número exista en algún punto de la
  evidencia (corrige R1, origen/destino intercambiados); un valor sin `role` declarado
  se sigue comparando de forma permisiva contra cualquier valor de la evidencia
  (conserva REL-SIMPLE-PARTIAL); (2) sustituye la distinción a/b/c basada en "lista de
  valores vacía o no" por una clasificación explícita de tres vías
  (`_analyze_numeric` → `NONE_KIND`/`PARSED_KIND`/`INCOMPLETE_KIND`): encontrar un
  disparador de `_INCOMPLETE_NUMBER_TRIGGERS` (mil, millón, cualquier centena
  distinta de "cien"), una fracción (`_FRACTION_PATTERN`) o notación científica
  (`_SCIENTIFIC_PATTERN`) en una cláusula la marca entera como `INCOMPLETE_KIND` —
  nunca se aprueba por el resto de su solapamiento léxico, ni siquiera con texto
  idéntico al de la evidencia (corrige R2 "mil", R3 "ciento veinte" ya no se degrada a
  "veinte" aislado). Sin excepciones literales para R1/R2/R3 — verificado con
  contrastes propios construidos independientemente de esas tres frases
  (REL-IDENTICAL, REL-ONE-END-CHANGES, REL-SIMPLE-PARTIAL, INCOMPLETE-MIL-IDENTICAL,
  INCOMPLETE-FRACTION, INCOMPLETE-SCIENTIFIC, PREFIX-DOES-NOT-LEAK-SUFFIX). Per FR-023
  (contradicts), research.md §11.

  **Reproducción**: ejecutados los 7 casos nuevos (R1, R2, R3,
  INCOMPLETE-MIL-IDENTICAL, INCOMPLETE-FRACTION, INCOMPLETE-SCIENTIFIC,
  PREFIX-DOES-NOT-LEAK-SUFFIX) contra el `GroundingVerifierAgent` de T093 (previo a
  esta corrección) — **7 fallos** de 40 casos totales del archivo (los otros 33,
  incluidos REL-IDENTICAL/REL-ONE-END-CHANGES/REL-SIMPLE-PARTIAL, ya se comportaban
  como se esperaba antes de esta corrección, verificado empíricamente, no asumido).
  Tras T094, mismas aserciones: 40/40 en el archivo completo.

  **Integración**: nueva prueba con R1
  (`tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py::
  test_r1_swapped_origin_destination_never_reaches_participant_as_grounded`) —
  propuesta ("de 100 a 20 grados") y evidencia ("de 20 a 100 grados") controladas
  mediante dobles en sus fronteras (adaptador de generación, paso de recuperación),
  `GroundingVerifierAgent` real sin mock de veredicto; confirma que "de 100 a 20
  grados" no llega al participante y que `grounding_verdict` queda trazado como
  `no_fundamentada`.

  **Regresión y análisis estático**: 304 passed, 1 deselected (antes de esta tarea:
  293; +11 = 10 casos nuevos de contrato — 7 reproducción + 3 contrastes REL-* — más 1
  prueba de integración nueva, 0 regresiones). Ruff sobre los 3 archivos modificados
  (`grounding_verifier_agent.py`, `test_grounding_verifier.py`,
  `test_grounding_blocks_contradicting_proposal_in_self_study.py`): 0 errores;
  recuento global sin cambios, 49 (igual que la referencia previa a esta ronda: 45
  E501, 2 F401, 1 F541, 1 F841).

  **Recuento preciso**: `tests/contract/test_grounding_verifier.py` tiene, tras esta
  tarea, 40 pruebas en total (30 previas a esta ronda + 10 nuevas: R1, R2, R3,
  REL-IDENTICAL, REL-ONE-END-CHANGES, REL-SIMPLE-PARTIAL, INCOMPLETE-MIL-IDENTICAL,
  INCOMPLETE-FRACTION, INCOMPLETE-SCIENTIFIC, PREFIX-DOES-NOT-LEAK-SUFFIX — todas
  parametrizadas en `_H03_SINGLE_VERDICT_MATRIX`).
  `tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py`
  tiene 3 pruebas (2 previas + 1 nueva de esta ronda). Comandos ejecutados esta ronda:
  `PYTHONPATH=src uv run pytest tests/contract/test_grounding_verifier.py -v`;
  `PYTHONPATH=src uv run pytest tests/integration/
  test_grounding_blocks_contradicting_proposal_in_self_study.py -v`; `PYTHONPATH=src
  uv run pytest tests/ -q -m "not ollama and not speech"`; `uv run ruff check src/
  tests/ --statistics`; `uv run ruff check src/oralia/domain/agents/
  grounding_verifier_agent.py tests/contract/test_grounding_verifier.py
  tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py
  --statistics` (0 errores en los archivos modificados).

**No se declara toda la Feature 002 completada** — T085/T086/T087 (recuperación,
timeout, reconstrucción del índice) siguen pendientes, sin tocar ni duplicar. La
distinción entre "esta ronda no encontró más fallos en la suite" y "no existen más
defectos en `GroundingVerifierAgent`" se mantiene explícita — no se declara lo
segundo.

## Phase 16: Convergence (corrección semántica de H03 — no_fundamentada→no_verificable, 2026-09-12d)

**Contexto**: T094 (Fase 15) resolvió R1–R3, pero aplicó una regla demasiado fuerte —
toda propuesta con análisis numérico `INCOMPLETE_KIND` se clasificaba
`no_fundamentada`, incluso cuando la evidencia contenía exactamente la misma
afirmación ("La sesión dura mil minutos." frente a sí misma). Una revisión
independiente señaló que una coincidencia literal normalizada SÍ constituye respaldo
documental, y que la incapacidad del analizador numérico para interpretar un valor no
permite afirmar que la evidencia no lo respalda. Se conserva sin modificar la
evidencia histórica de T084/T089/T093/T094 — esta tarea corrige una decisión de T094
que resultó incorrecta, documentado expresamente, no la sustituye en el registro.

- [X] T095 **[Implementada y validada en esta ronda, 2026-09-12d]** Corrige, en
  `src/oralia/domain/agents/grounding_verifier_agent.py`: (1) añade
  `_normalize_literal` (minúsculas, puntuación superficial de una lista fija,
  colapso de espacios — MUST NOT eliminar dígitos, `+`/`-`, "/", ni letras); (2)
  sustituye el booleano de `_claim_is_supported_by_clause`/`_claim_is_supported`
  (renombrada `_claim_outcome`) por una clasificación de tres resultados
  (`_SUPPORTED_OUTCOME`/`_CONTRADICTED_OUTCOME`/`_UNVERIFIABLE_OUTCOME`,
  `_combine_clause_outcomes` para empates): cuando la propuesta analiza
  `INCOMPLETE_KIND`, una coincidencia literal normalizada con la cláusula de
  evidencia alineada produce `_SUPPORTED_OUTCOME`; sin coincidencia, produce
  `_UNVERIFIABLE_OUTCOME` (nunca `_CONTRADICTED_OUTCOME`, reservado para una
  diferencia realmente interpretada — polaridad, o valores ambos parseados que
  difieren); (3) `GroundingVerifierAgent.execute` deriva el veredicto agregado
  distinguiendo, cuando ninguna afirmación está soportada, `no_fundamentada` (al
  menos una `_CONTRADICTED_OUTCOME`) de `no_verificable` (todas las no soportadas son
  `_UNVERIFIABLE_OUTCOME`) — sin cambiar el contrato publicado de
  `supported_claims`/`unsupported_claims` (siguen siendo `string[]`, sin un tercer
  valor: cambio interno de agregación, no de esquema, evaluado y descartado por
  innecesario antes de implementar, según lo pedido). Sin excepciones literales a las
  frases de la propuesta — verificado con contrastes de signo, unidad, negación,
  entidad distinta, y diferencias solo de espacios/puntuación, todos construidos
  independientemente de R2/R3. Per FR-023, research.md §11.

  **Modelo de decisión (examinado antes de implementar, per lo pedido)**: de los
  cinco veredictos documentados (`spec.md` FR-023, Key Entities), `no_verificable` ya
  se usaba para "el mecanismo no tiene evidencia para verificar" (evidencia vacía +
  conocimiento general permitido); `no_fundamentada` para "se determinó activamente
  que la propuesta no está respaldada o la contradice". Una afirmación con expresión
  numérica no interpretada y sin coincidencia literal encaja semánticamente en el
  primero, no en el segundo — el mecanismo no determina una contradicción, determina
  su propia incapacidad de verificar. Se descartó introducir un tercer valor en
  `supported_claims`/`unsupported_claims` (p. ej. `unverifiable_claims`) por
  innecesario: la distinción de tres vías solo afecta al campo `verdict`, ya de por sí
  derivado (no primitivo) de las dos listas existentes.

  **Reproducción**: ejecutadas las expectativas corregidas (identidad textual →
  `fundamentada`; texto distinto → `no_verificable`, nunca `fundamentada`; R2/R3;
  PREFIX-DOES-NOT-LEAK-SUFFIX) contra el `GroundingVerifierAgent` de T094 (previo a
  esta corrección) — **6 fallos** de 41 casos del archivo (INCOMPLETE-MIL-IDENTICAL,
  INCOMPLETE-FRACTION, INCOMPLETE-SCIENTIFIC esperaban `fundamentada` y T094 daba
  `no_fundamentada`; R2, R3, PREFIX-DOES-NOT-LEAK-SUFFIX esperaban `no_verificable` y
  T094 daba `no_fundamentada`). Tras T095, mismas aserciones: 47/47 (40 previas a
  esta ronda + 7 nuevas: INCOMPLETE-FRACTION-DIFFERENT-VALUE,
  INCOMPLETE-SCIENTIFIC-DIFFERENT-VALUE, INCOMPLETE-SIGN-DIFFERENT,
  INCOMPLETE-UNIT-DIFFERENT, INCOMPLETE-NEGATION-DIFFERENT,
  INCOMPLETE-WHITESPACE-PUNCTUATION-ONLY, INCOMPLETE-SAME-FIGURE-DIFFERENT-ENTITY).

  **No debilita lo ya resuelto**: H03 original (S1/C1-C3/I1/V1-V2/CIEN/NEG1-NEG2/
  MULTI/UNIT), F1–F7, R1 (sin cambio de verdict — sigue `no_fundamentada`, una
  contradicción interpretada de valores ambos `PARSED_KIND`), relaciones
  origen/destino (REL-*), duplicación/reordenación de evidencia, polaridad, y
  clasificación parcial/procedencia — 40 casos previos del archivo de contrato, todos
  verificados en verde tras el cambio (ver reproducción).

  **Integración**: nueva prueba con R2
  (`tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py::
  test_r2_unrecognized_numeral_never_reaches_participant_as_grounded`) — propuesta
  ("mil minutos") y evidencia distinta ("cien minutos") controladas mediante dobles en
  sus fronteras, `GroundingVerifierAgent` real sin mock de veredicto; confirma
  explícitamente `grounding_verdict == "no_verificable"` en el trace (no
  `no_fundamentada`), verificando la corrección semántica de principio a fin. Las 3
  pruebas de integración previas (original, F1, R1) siguen en verde sin cambio de
  aserciones.

  **Regresión y análisis estático**: 312 passed, 1 deselected (antes de esta tarea:
  304; +8 = 7 casos nuevos de contrato + 1 prueba de integración nueva, 0
  regresiones). Ruff sobre los 3 archivos modificados
  (`grounding_verifier_agent.py`, `test_grounding_verifier.py`,
  `test_grounding_blocks_contradicting_proposal_in_self_study.py`): 0 errores;
  recuento global sin cambios, 49 (45 E501, 2 F401, 1 F541, 1 F841). Comandos
  ejecutados esta ronda: `PYTHONPATH=src uv run pytest
  tests/contract/test_grounding_verifier.py -v`; `PYTHONPATH=src uv run pytest
  tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py
  -v`; `PYTHONPATH=src uv run pytest tests/ -q -m "not ollama and not speech"`;
  `uv run ruff check src/ tests/ --statistics`; `uv run ruff check
  src/oralia/domain/agents/grounding_verifier_agent.py
  tests/contract/test_grounding_verifier.py
  tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py
  --statistics` (0 errores en los archivos modificados).

  **Limitación documentada, no corregida esta ronda**: `self_study_agency_composer.py`
  (Feature 003) contiene un comentario que ya no es exacto ("única situación en la que
  GroundingVerifierAgent produce `no_verificable`") tras esta corrección — el
  comportamiento observable no cambia cuando `general_knowledge_allowed = false`
  (verificado con la integración de R2 arriba), pero con
  `general_knowledge_allowed = true` el compositor etiquetaría esta respuesta como
  conocimiento general en vez de reconocer la falta de evidencia interpretable. Fuera
  del alcance autorizado de esta ronda (Feature 002 acotada, sin trabajo de 003) —
  documentado en research.md §11 como riesgo conocido para una ronda posterior de 003.

**No se declara toda la Feature 002 completada** — T085/T086/T087 (recuperación,
timeout, reconstrucción del índice) siguen pendientes, sin tocar ni duplicar. Tampoco
se declara que `GroundingVerifierAgent` reconozca cualquier expresión numérica del
español ni que la interacción con Feature 003 bajo `general_knowledge_allowed = true`
esté ya corregida — ambos límites quedan documentados explícitamente, no resueltos.

## Phase 17: Convergence

**Contexto**: `/speckit-analyze` sobre esta feature (2026-09-12e) encontró que la
corrección de T095 introdujo una asimetría no cubierta: `_claim_is_supported_by_clause`
(caso c) devuelve `_CONTRADICTED_OUTCOME` cuando la propuesta es `PARSED_KIND` y la
cláusula de evidencia alineada es `INCOMPLETE_KIND`, sin verificar que AMBOS valores
hayan podido interpretarse — contradice la propia regla que research.md §11 ya
declaraba tras T095 ("una diferencia activamente interpretada... dos valores ambos
comparables que no coinciden"). Reproducido: "La sesión dura 1000 minutos." (propuesta)
frente a "La sesión dura mil minutos." (evidencia) → `no_fundamentada`; invertido →
`no_verificable` — la dirección de la comparación decide el veredicto sin que exista
asimetría semántica en la relación expresada. Se conserva sin modificar la evidencia
histórica de T084/T089/T093/T094/T095 — esta tarea corrige una omisión de T095, no la
sustituye en el registro.

- [X] T096 **[Implementada y validada en esta ronda, 2026-09-12e]** Corrige, en `src/oralia/domain/agents/grounding_verifier_agent.py`,
  `_claim_is_supported_by_clause` para que el análisis numérico sea simétrico:
  analiza `_analyze_numeric` tanto de la propuesta como de la cláusula de evidencia
  alineada ANTES de decidir el resultado (en vez de solo de la propuesta, como hasta
  T095). Reglas, en orden: (1) diferencia de polaridad interpretada →
  `_CONTRADICTED_OUTCOME` (sin cambio); (2) si cualquiera de los dos lados es
  `INCOMPLETE_KIND`, una coincidencia literal normalizada (`_normalize_literal`) de la
  afirmación completa con la cláusula → `_SUPPORTED_OUTCOME`; sin coincidencia →
  `_UNVERIFIABLE_OUTCOME` (nunca `_CONTRADICTED_OUTCOME` — no hay dos valores ambos
  interpretados que comparar); (3) si ambos lados son `PARSED_KIND`, comparar con
  `_values_are_consistent` como hasta ahora (coincide → `_SUPPORTED_OUTCOME`, difiere →
  `_CONTRADICTED_OUTCOME`); (4) `PARSED_KIND` (propuesta) vs `NONE_KIND` (evidencia) se
  conserva sin cambio como `_CONTRADICTED_OUTCOME` (caso F2, T093 — el análisis previo
  a esta tarea no encontró justificación contractual para cambiarlo: `NONE_KIND` no es
  una expresión numérica no interpretada, es la ausencia de una, y la cifra concreta de
  la propuesta sigue sin tener con qué contrastarse). Regla estructural, sin
  excepciones para las frases concretas de reproducción. Per research.md §11 (regla
  citada arriba), FR-023.

  **Decisión contractual pendiente, documentada y NO corregida en esta tarea**
  (hallazgo F2 del `/speckit-analyze` de esta ronda): `spec.md` (Key Entities,
  `GroundingVerificationResult`) dice *""Parcialmente fundamentada" significa que al
  menos una afirmación carece de soporte en la evidencia recuperada, sin que ninguna la
  contradiga activamente; "conflictiva" significa que al menos una afirmación es
  contradicha por la evidencia recuperada o por otra fuente autorizada (Escenario D)."*
  — la anotación `(Escenario D)` es sintácticamente ambigua sobre si acota todo el
  disyunto de `conflictiva` (lectura implementada: `conflictiva` exige un
  `MaterialConflictRecord` entre fuentes distintas, `research.md §7` — "fragmentos de
  documentos distintos... se marcan como conflictivos") o si una contradicción con un
  único fragmento de evidencia también encajaría literalmente en "contradicha por la
  evidencia recuperada". El código y las pruebas actuales (`C1`, `F1-F7`, `R1-R3`,
  T095) usan `no_fundamentada` para toda contradicción de un único fragmento, sin
  registro de conflicto — consistente con la segunda mitad de la implementación, no
  inequívocamente con la letra aislada de `spec.md:422-423`. Esta tarea NO cambia
  `spec.md`, código ni veredictos por esta ambigüedad — se registra para que una ronda
  separada decida, antes de cerrar H03 por completo, si aclarar `spec.md` (acotando
  explícitamente `(Escenario D)` a todo el disyunto) o si ampliar deliberadamente
  `conflictiva` y entonces sí actualizar código/tests.

  **Reproducción**: prototipo aislado (`proto_grounding5.py`, scratchpad de sesión)
  verificado con 42/42 casos y 7/7 pruebas de simetría antes de tocar el código real.
  Contra el código real de T095 (revertido temporalmente para esta comprobación):
  ejecutados los 8 casos nuevos (`T096-1000-VS-MIL`, `T096-MIL-VS-1000`,
  `T096-20-VS-MIL`, `T096-MIL-VS-20`, `T096-05-VS-FRACTION`, `T096-FRACTION-VS-05`,
  `T096-SCIENTIFIC-VS-FULL`, `T096-FULL-VS-SCIENTIFIC`) — **8 fallos** de 62 casos del
  archivo (exactamente las 4 combinaciones donde la propuesta es `PARSED_KIND` y la
  evidencia `INCOMPLETE_KIND`, más sus 4 pruebas de simetría correspondientes; las 4
  combinaciones inversas — propuesta `INCOMPLETE_KIND`, evidencia `PARSED_KIND` — ya
  pasaban antes de esta tarea, verificado empíricamente). Tras reaplicar la corrección:
  mismas aserciones, 62/62 en el archivo completo (47 previas a esta ronda + 8 nuevos
  + 7 de la prueba de propiedad de simetría). **F1-F7/R1-R3/T095 no requirieron ningún
  cambio de aserción** — las 47 pruebas previas pasaron sin modificación antes y
  después del cambio de código, confirmando que la corrección es puramente aditiva.

  **Integración**: nueva prueba
  (`tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py::
  test_t096_digit_proposal_vs_word_evidence_never_reaches_participant_as_grounded`) —
  propuesta ("1000 minutos", dígito) y evidencia ("mil minutos", palabra) controladas
  mediante dobles en sus fronteras, `GroundingVerifierAgent` real sin mock de
  veredicto; confirma `grounding_verdict == "no_verificable"` en el trace, la
  dirección exacta que quedaba rota tras T095. Las 4 pruebas de integración previas
  (original, F1, R1, R2) siguen en verde sin cambio de aserciones.

  **Regresión y análisis estático**: 328 passed, 1 deselected (antes de esta tarea:
  312; +16 = 8 casos nuevos de contrato + 7 de la prueba de propiedad de simetría + 1
  prueba de integración nueva, 0 regresiones). Ruff sobre los 3 archivos modificados
  (`grounding_verifier_agent.py`, `test_grounding_verifier.py`,
  `test_grounding_blocks_contradicting_proposal_in_self_study.py`): 0 errores;
  recuento global sin cambios, 49 (45 E501, 2 F401, 1 F541, 1 F841 — idénticos a la
  referencia previa, todos heredados, ninguno nuevo). Comandos ejecutados esta ronda:
  `PYTHONPATH=src uv run pytest tests/contract/test_grounding_verifier.py -v`;
  `PYTHONPATH=src uv run pytest tests/integration/
  test_grounding_blocks_contradicting_proposal_in_self_study.py -v`; `PYTHONPATH=src
  uv run pytest tests/ -q -m "not ollama and not speech"`; `uv run ruff check src/
  tests/ --statistics`; `uv run ruff check src/oralia/domain/agents/
  grounding_verifier_agent.py tests/contract/test_grounding_verifier.py
  tests/integration/test_grounding_blocks_contradicting_proposal_in_self_study.py
  --statistics` (0 errores en los archivos modificados).

**No se declara toda la Feature 002 completada** — T085/T086/T087 (recuperación,
timeout, reconstrucción del índice) siguen pendientes, sin tocar ni duplicar. Tampoco
se declara resuelta la ambigüedad contractual `parcialmente_fundamentada`/`conflictiva`
documentada arriba — queda explícitamente pendiente para una decisión separada.

## Phase 18: Convergence (resolución de la ambigüedad parcialmente_fundamentada/no_fundamentada/no_verificable/conflictiva, 2026-09-12f)

**Contexto**: T096 (Fase 17) documentó, sin corregir, una ambigüedad sintáctica en la
definición de `GroundingVerificationResult` de `spec.md` sobre el alcance de
`"conflictiva"`. Esta fase la resuelve formalmente mediante `/speckit-clarify`,
propaga la decisión a los artefactos contractuales, y confirma mediante pruebas las
seis precedencias entre los cinco veredictos. No es una ampliación de
T085/T086/T087, que siguen sin implementarse.

- [X] T097 **[Verificada y cerrada en esta ronda, 2026-09-12f]** Formaliza, mediante `/speckit-clarify`, la resolución de la ambigüedad
  registrada por T096 entre `parcialmente_fundamentada`, `no_fundamentada`,
  `no_verificable` y `conflictiva`. Decisión fijada en `spec.md` § Clarifications
  (Session 2026-09-12): la anotación `"(Escenario D)"` en la definición anterior de
  `GroundingVerificationResult` acota **todo** el disyunto de `"conflictiva"` — se
  reserva exclusivamente al conflicto pendiente y registrado entre fuentes
  (`MaterialConflictRecord` con `review_status = "pending_review"`, User Story 6),
  con **precedencia** sobre los otros cuatro veredictos cuando ese conflicto existe.
  Una contradicción entre una propuesta y un único fragmento de evidencia NO
  constituye un conflicto entre fuentes ni genera un `MaterialConflictRecord`
  sintético — se clasifica `no_fundamentada` o `parcialmente_fundamentada` según
  corresponda. Actualiza de forma coherente `spec.md` (definición de
  `GroundingVerificationResult` en Key Entities, reescrita con los cinco veredictos y
  su precedencia; Acceptance Scenarios de User Story 3 —dos escenarios nuevos— y User
  Story 6 —dos escenarios nuevos—), `contracts/material-retriever-agent.md` (nueva
  regla de precedencia), y `research.md §11` (corrige el encabezado inexacto que
  describía T095 como "no_fundamentada→no_verificable" cuando la regla real es
  "`INCOMPLETE_KIND` con coincidencia literal → `fundamentada`; sin coincidencia y sin
  contradicción interpretable → `no_verificable`"; sustituye la sección "decisión
  contractual pendiente" de T096 por la resolución final con la tabla de los cinco
  veredictos). Per FR-023, Clarifications Session 2026-09-12.

  **Código de producción**: NO requirió ningún cambio — `GroundingVerifierAgent`
  (T093-T096) ya implementaba exactamente esta semántica (`_touches_unreviewed_conflict`
  ya exige `review_status == "pending_review"`, nunca se dispara por un único
  fragmento; el veredicto agregado ya distingue `no_fundamentada`/`no_verificable`
  exactamente según `_CONTRADICTED_OUTCOME`/`_UNVERIFIABLE_OUTCOME`). Esta tarea es de
  formalización contractual y de cobertura de pruebas, no de corrección de código.

  **Pruebas existentes reutilizadas (verificadas contra las seis precedencias exigidas,
  sin duplicar)**: (1) afirmación soportada + una sin respaldo → parcialmente_fundamentada:
  `test_parcialmente_fundamentada_when_some_claims_unsupported`
  (`tests/contract/test_grounding_verifier.py`). (2) afirmación soportada + una
  contradicha por una única fuente no conflictiva → parcialmente_fundamentada:
  `test_h03_property_partial_claim_lists_stay_coherent` (mismo archivo — "El agua
  hierve a 100 grados. El agua hierve a 20 grados." frente a "El agua hierve a 100
  grados.": la segunda afirmación es una contradicción numérica interpretada, no una
  simple falta de solapamiento léxico). (3) ninguna soportada + contradicha por una
  única fuente → no_fundamentada: matriz `C1`/`F1`-`F7` (mismo archivo). (4) ninguna
  soportada + todas no verificables → no_verificable: matriz `R2`/`T096-*` (mismo
  archivo). (5) evidencia que toca un `MaterialConflictRecord` pendiente →
  conflictiva, aunque la afirmación aislada coincide literalmente con una de las dos
  fuentes en conflicto (por tanto parecería soportada sin la precedencia):
  `test_proposal_touching_conflict_is_classified_conflictiva`
  (`tests/integration/test_grounding_conflict_verdict.py`).

  **Prueba nueva (único requisito no cubierto)**: (6) un conflicto revisado no debe
  seguir forzando conflictiva — `test_reviewed_conflict_no_longer_forces_conflictiva`
  (`tests/integration/test_grounding_conflict_verdict.py`): activa el mismo par de
  documentos en conflicto, confirma `verdict == "conflictiva"` antes de revisar,
  marca el conflicto como revisado vía `POST /materials/conflicts/{id}/review`, y
  confirma `verdict != "conflictiva"` en una evaluación posterior sobre la misma
  evidencia — **pasó en la primera ejecución, sin ningún cambio de código**,
  confirmando que `_touches_unreviewed_conflict` ya filtraba correctamente por
  `review_status == "pending_review"`.

  **Regresión y análisis estático**: 329 passed, 1 deselected (antes de esta tarea:
  328; +1 = la prueba nueva de conflicto revisado, 0 regresiones). Ruff sobre el
  archivo modificado (`test_grounding_conflict_verdict.py`): 0 errores; recuento
  global sin cambios, 49 (45 E501, 2 F401, 1 F541, 1 F841 — idénticos a la referencia
  previa, todos heredados). Comandos ejecutados esta ronda: `PYTHONPATH=src uv run
  pytest tests/integration/test_grounding_conflict_verdict.py -v`; `PYTHONPATH=src uv
  run pytest tests/ -q -m "not ollama and not speech"`; `uv run ruff check src/
  tests/ --statistics`; `uv run ruff check
  tests/integration/test_grounding_conflict_verdict.py --statistics` (0 errores).

**H03 (fundamentación de respuestas) queda cerrado tras T097** — las siete rondas de
esta feature sobre `GroundingVerifierAgent` (T084, T089, T093, T094, T095, T096,
T097) cubren: fundamentación básica, negación, comparación numérica con roles
relacionales, distinción explícita de tres vías del análisis numérico, simetría
estructural, y ahora la semántica no ambigua de los cinco veredictos con su
precedencia — verificado exhaustivamente y sin contradicciones pendientes conocidas
dentro del alcance de `GroundingVerifierAgent`.

**No se declara toda la Feature 002 completada** — T085/T086/T087 (recuperación,
timeout, reconstrucción del índice, hallazgo H08) siguen pendientes, sin tocar ni
duplicar. El cierre de H03 no implica el cierre de la feature.

## Phase 19: Convergence (T085/H08 implementada; nueva tarea de seguimiento — revalidación de course_id, 2026-09-12g)

**Contexto**: T090 reprodujo, y T085 implementó, la corrección de los dos defectos
de H08 (ventana fija, ausencia de umbral de relevancia) — ver evidencia completa en
T085 arriba. Durante el análisis de T090 se identificó un hallazgo **distinto**, no
parte de H08: el aislamiento por `course_id` no se revalida contra SQL, solo
depende del filtro `where` enviado al almacén vectorial. Se registra aquí como
tarea de seguimiento separada, explícitamente NO implementada ni declarada
corregida en esta ronda.

- [X] T098 **[Implementada y validada en esta ronda, 2026-09-12i]** Confirmada
  como brecha real de FR-019 (no solo teórica) y corregida la revalidación de
  `MaterialFragment.course_id`/`MaterialDocument.course_id` contra el `course_id`
  solicitado en `MaterialRetrieverAgent.execute`/`_authorized`. Antes, `_authorized`
  solo comparaba `activity_configuration_id`; el aislamiento por asignatura
  dependía exclusivamente de que `ChromaVectorStore.query` recibiera y respetara
  `filters={"course_id": ...}` — un almacén que lo ignorase, o cuya metadata
  estuviera desincronizada, podía devolver un fragmento de otra asignatura sin que
  ninguna capa SQL lo detectase, siempre que compartiera `activity_configuration_id`
  con la consulta.

  **Diseño implementado**: dos funciones puras nuevas, module-level, sin efectos
  secundarios (`_fragment_authorized_for_scope`, `_fragment_currently_retrievable`,
  `src/oralia/domain/agents/material_retriever_agent.py`) son ahora la única fuente
  de la política de asignatura/actividad/ciclo de vida. `course_id`, cuando está
  presente, exige `fragment.course_id == course_id` **y**
  `document.course_id == course_id` — una discrepancia entre ambas filas también
  causa rechazo. El filtro `where` del `VectorStore` se conserva como prefiltrado
  barato, nunca como autorización; `VectorMatch.metadata` no se consulta para
  autorizar. Un candidato de otra asignatura cuenta como `blocked_out_of_scope`
  (mismo cubo que un `activity_configuration_id` incorrecto): el ensanchamiento
  progresivo sigue buscando candidatos válidos posteriores, y el bloqueo se
  registra como máximo una vez por `execute()` aunque aparezca en varias rondas.
  `_authorized`/`_is_retrievable` cambian de firma para aceptar `document`
  (y `_authorized` también `course_id`) y delegan en las funciones puras;
  `_run_widening_search` añade `document_rows_cache`, poblado por lotes
  (`db.query(MaterialDocument).filter(id.in_(...))`) igual que ya se hacía para
  `MaterialFragment` — ningún `db.get` adicional por candidato.
  **Sin políticas divergentes**: `get_currently_valid_fragment` (T099, reutilización
  de `concepts_pending` en Feature 003) se refactorizó para delegar en las MISMAS
  dos funciones puras, en vez de duplicar las comprobaciones inline — el bucle
  propio del agente y la reutilización de cola de Feature 003 ya no pueden divergir
  en la política aplicada. `ChromaVectorStore`'s docstring corregido: ya no sugiere
  que SQL solo revalida "las comprobaciones restantes" tras el prefiltrado por
  `course_id` — SQL revalida `course_id` mismo, explícitamente. No se cambia el
  contrato HTTP (`course_id` sigue obligatorio en `MaterialQueryInput`); no se
  introduce ningún `422` nuevo. Per FR-019, research.md §14.1a→§14.1b (riesgo
  documentado por T085/T090, corregido por T098).

  **Reproducción**: 8 pruebas nuevas
  (`tests/integration/test_material_retrieval_course_isolation.py`). Contra el
  código previo a T098, 7/8 fallan de forma discriminante: un `VectorStore` que
  ignora el filtro `course_id` y devuelve primero un fragmento de otra asignatura
  con relevancia 0.90 se filtraba hasta `fragments`; un `fragment.course_id`
  incorrecto con `document.course_id` correcto (o viceversa) también se aceptaba;
  una metadata de `VectorMatch` que afirmaba el curso correcto no evitaba la fuga
  (el fallo real era no consultar SQL en absoluto). El contraste positivo (ambos
  correctos) ya pasaba. Tras T098, mismas aserciones sin cambios: 8/8 en verde —
  incluye ensanchamiento progresivo que encuentra el candidato correcto tras 16
  candidatos de otra asignatura (`len(store.queried_k) >= 2`), un único evento de
  traza de bloqueo pese a 20 candidatos incorrectos en varias rondas
  (`len(calls) == 1`), y verificación explícita (monkeypatch de `detect_conflicts`)
  de que el candidato de otra asignatura nunca llega a la detección de conflictos.

  **Regresión T085/T090/T099**: `test_material_retrieval_widening_structural.py`
  (T085/T090) y `test_self_study_pending_fragment_revalidation.py` +
  `test_material_fragment_revalidation.py` (T099) — 34/34 sin regresión.
  Aislamiento por actividad existente
  (`test_query_for_activity_a_never_returns_activity_b_fragments`,
  `test_out_of_scope_activity_returns_empty_fragments_not_an_error`) — 6/6 sin
  regresión.

  **Regresión completa y análisis estático**: 371 passed, 1 deselected (antes de
  esta tarea: 363; +8, exactamente las nuevas pruebas de aislamiento, 0
  regresiones). Ruff sobre los archivos modificados/nuevos: 0 errores (4 E501
  transitorios corregidos mediante reformateo, sin cambios de lógica); recuento
  global sin cambios, 49 (idéntico a la referencia previa, todos heredados).
  Comandos ejecutados esta ronda: `PYTHONPATH=src uv run pytest
  tests/integration/test_material_retrieval_course_isolation.py -v`; `PYTHONPATH=src
  uv run pytest tests/integration/test_material_retrieval_widening_structural.py
  tests/integration/test_self_study_pending_fragment_revalidation.py
  tests/unit/test_material_fragment_revalidation.py -v`; `PYTHONPATH=src uv run
  pytest tests/ -q -m "not ollama and not speech"`; `uv run ruff check src/ tests/
  --statistics`; `uv run ruff check
  src/oralia/domain/agents/material_retriever_agent.py
  src/oralia/infrastructure/vector_store/chroma_store.py
  tests/integration/test_material_retrieval_course_isolation.py --statistics`.

**No se declara toda la Feature 002 completada** — T086/T087 (presupuesto duro/hilo
de trabajo, reconstrucción del índice) siguen pendientes, sin tocar ni duplicar. H08
queda resuelto para sus dos defectos originales (ventana fija, umbral de
relevancia); el hallazgo de `course_id` (T098) también queda resuelto — era nuevo y
distinto, no una ampliación no autorizada de H08.

## Phase 20: Convergence (corrección del acoplamiento cruzado introducido por T085 — reutilización de cola sin revalidar, 2026-09-12h)

**Contexto**: `/speckit-analyze` (2026-09-12h) confirmó que la corrección de
continuidad de T085 en `self_study_agency_composer.py` (reutilizar
`concepts_pending` cuando la recuperación de este turno no repite el fragmento en
cola) presupone, sin comprobarlo, que la fila de `MaterialFragment` sigue siendo
autorizada y vigente — y sustituye por `fragments[:1]` (una fila arbitraria) si ya
no existe. Es un hallazgo distinto de T098 (que trata la misma revalidación de
`course_id` pero DENTRO del bucle general de `MaterialRetrieverAgent` — resuelto
posteriormente, ver T098): T099 protege específicamente la reutilización de cola
del compositor. Se detectó además, durante el mismo análisis, que
`_run_widening_search` trata el presupuesto temporal como agotado solo con `>`
estricto, no `>=`, permitiendo una ronda adicional exactamente en el límite.

- [X] T099 **[Implementada y validada en esta ronda, 2026-09-12h]** Revalida cada entrada de `cognitive_state.concepts_pending` contra SQL
  en el momento de usarla, en vez de presuponer que sigue siendo válida por haber
  sido autorizada al encolarse. Añade una función nueva, module-level, en
  `src/oralia/domain/agents/material_retriever_agent.py` (sin modificar
  `_authorized`/`_is_retrievable` existentes, cuyos efectos secundarios de
  `blocked_out_of_scope`/trazas FR-026 son propios del bucle de ese agente) que
  revalide: `fragment.course_id == activity.course_id`,
  `document.course_id == activity.course_id`,
  `activity.id in fragment.activity_configuration_ids`,
  `fragment.indexing_status == "indexed"`, `document.status == "active"`,
  `document.retired_at is None`, `fragment.valid_until` nulo o futuro — devolviendo
  la fila solo si pasa todas, o `None` (incluida la fila ya no existente) en caso
  contrario. En `self_study_agency_composer.py`: recorre `concepts_pending` desde la
  cabeza, descarta cada entrada que no revalide y prueba la siguiente (acotado, sin
  sustituir nunca por una fila arbitraria); `guided_pending_after` excluye toda
  entrada descartada; si ninguna entrada pendiente revalida pero `fragments` de esta
  ronda tiene contenido, resiembra la cola desde ahí; si tampoco hay `fragments`,
  cae a Nivel 0 (ya cubierto por la fórmula existente de `nivel_0_skip` sobre
  `active_fragments`, sin cambios ahí). No reaplica el umbral de relevancia 0.35 a
  una entrada de cola ya revalidada — la relevancia inicial se hereda
  deliberadamente para una continuación anafórica; solo autorización/vigencia se
  revalidan siempre. Corrige además, en el mismo archivo de agente,
  `elapsed_ms > time_budget_ms` → `elapsed_ms >= time_budget_ms` en los dos puntos
  de `_run_widening_search` (presupuesto agotado MUST incluir la igualdad). Todo
  acceso SQL permanece en el hilo principal; sin `asyncio.to_thread`. Per FR-019,
  research.md §14.1a/§14.2a (contradicts)

  **Reproducción**: 7 escenarios de invalidación entre turnos, flujo real de
  autoestudio (`tests/integration/test_self_study_pending_fragment_revalidation.py`,
  modo `guided_explanation` con `sample.docx` → 3 fragmentos). Contra el código
  previo a T099: 6/7 fallan de forma discriminante — el texto/id del fragmento
  invalidado (documento inactivo, retirado, fragmento expirado, no indexado,
  desasignado de la actividad, o de otro `course_id`) reaparecía en `output_text`,
  `sources`, la traza `generation_call.fragment_ids`, o sobrevivía en
  `concepts_pending`. El séptimo (fila de fragmento eliminada) no se distingue de
  forma fiable con este fixture concreto — la sustitución arbitraria anterior
  (`fragments[:1]`) podía coincidir por azar con un fragmento *distinto pero
  igualmente válido* del mismo documento pequeño (los 3 fragmentos de `sample.docx`
  comparten `document_id`), así que ninguna aserción basada en texto/documento lo
  distinguía de una reutilización correcta. Cubierto en su lugar, de forma precisa y
  determinista, por `tests/unit/test_material_fragment_revalidation.py` (10 casos:
  1 fragmento válido + los 7 estados inválidos + 2 casos de filtro `None`
  permisivo) — la fila eliminada devuelve `None` sin ambigüedad. Tras T099, mismas
  aserciones: 7/7 en verde en el archivo de integración, 10/10 en el de unidad.

  **Contraste temporal**: cada uno de los 7 casos de integración ES el contraste
  temporal — turno1 encola un fragmento válido, se invalida entre turnos, turno2
  "continúa" no puede usarlo.

  **Límite exacto del presupuesto**: `test_budget_exactly_at_the_limit_does_not_trigger_an_extra_round`
  (`tests/integration/test_material_retrieval_widening_structural.py`) — reproducido
  contra `elapsed_ms > time_budget_ms` (ronda adicional, `queried_k=[4, 8]`),
  corregido contra `>=` (`queried_k=[4]`, una sola advertencia de presupuesto).

  **Continuidad de T085 conservada**: `tests/integration/test_mode_guided_explanation.py`
  (3/3) y `tests/integration/test_coherence_conditions_fr015.py` (5/5) completos, sin
  regresión — ninguna de las 4 correcciones de continuidad de T085 (rotación de
  `concepts_pending`, resolución SQL sin sustitución arbitraria, `nivel_0_skip` sobre
  `active_fragments`, reutilización de `previous_turn.input_text` en adaptaciones) ni
  las 4 regresiones de Feature 003 que las motivaron reaparecen.

  **Regresión y análisis estático**: 363 passed, 1 deselected (antes de esta tarea:
  345; +18 = 7 reproducción de integración + 10 unitarias + 1 límite de presupuesto,
  0 regresiones). Ruff sobre los archivos modificados/nuevos: 0 errores (1 F401
  transitorio corregido, import no usado tras simplificar una prueba); recuento
  global sin cambios, 49 (45 E501, 2 F401, 1 F541, 1 F841 — idénticos a la
  referencia previa, todos heredados). Comandos ejecutados esta ronda:
  `PYTHONPATH=src uv run pytest
  tests/integration/test_self_study_pending_fragment_revalidation.py -v`;
  `PYTHONPATH=src uv run pytest tests/unit/test_material_fragment_revalidation.py -v`;
  `PYTHONPATH=src uv run pytest tests/integration/test_material_retrieval_widening_structural.py -v`;
  `PYTHONPATH=src uv run pytest tests/integration/test_mode_guided_explanation.py
  tests/integration/test_coherence_conditions_fr015.py -v`; `PYTHONPATH=src uv run
  pytest tests/ -q -m "not ollama and not speech"`; `uv run ruff check src/ tests/
  --statistics`; `uv run ruff check src/oralia/domain/agents/material_retriever_agent.py
  src/oralia/application/orchestration/self_study_agency_composer.py
  tests/integration/test_self_study_pending_fragment_revalidation.py
  tests/unit/test_material_fragment_revalidation.py
  tests/integration/test_material_retrieval_widening_structural.py --statistics`.

**No se declara toda la Feature 002 completada** — T086/T087/T091/T092 siguen
pendientes, sin tocar ni duplicar. T098 (revalidación SQL de `course_id`) se
implementó y validó en una ronda posterior — ver su entrada más arriba para la
evidencia completa.

## Phase 21: Convergence (T091 ejecutada — reproducción previa a T086/H10, 2026-09-13)

**Contexto**: T091 es la reproducción previa de T086 (research.md §12, hallazgo H10):
`MaterialRetrieverAgent.execute` no contiene ningún `await` interno hoy, así que un
`request.deadline_ms` (Feature 001, `run_with_deadline`) más corto que un
`EmbeddingAdapter.embed`/`VectorStore.query` bloqueante no lo interrumpe — el turno
corre hasta el final y devuelve `status = "ok"` en vez de `status = "timeout"`. Esta
ronda ejecuta y documenta esa reproducción; `MaterialRetrieverAgent` **NO** se
modifica — T086 (mover `embed`/`query` a `asyncio.to_thread`) sigue sin
implementarse, deliberadamente, a la espera de esta evidencia previa.

**Distinción `time_budget_ms` (blando, interno) vs. `request.deadline_ms` (duro,
externo)** — mantenida estrictamente en las tres reproducciones: `time_budget_ms` se
fija en 60000ms en todas ellas (muy por encima de cualquier bloqueo usado, de
decenas/centenas de ms), de forma que nunca puede ser la causa de un resultado; el
único límite corto en juego es siempre `request.deadline_ms` (80ms en H10.A/H10.B,
5000ms en el contraste positivo).

**Dobles bloqueantes y mecanismo de coordinación** — `tests/failure/
test_material_retrieval_h10_reproduction.py`, clase `_ReleaseThreadBlocker`:
coordinación por `threading.Event` (un hilo auxiliar `daemon` libera el bloqueo tras
un retardo medido desde que el bloqueo realmente empieza, no desde la construcción del
doble), nunca un `sleep` frágil dentro de la llamada bloqueada en sí. Todo `.wait(...)`
lleva un timeout de seguridad (5s) que convierte un doble roto en un fallo rápido y
explícito en vez de una suite colgada. `close()` se invoca siempre desde un bloque
`finally`, incluso si una aserción falla antes.

**H10.A (embedding bloqueante)** —
`test_h10a_blocking_embedding_adapter_is_preempted_by_hard_deadline`: `embed()`
bloquea; el `VectorStore` (`_ImmediateVectorStore`) nunca bloquea y solo se usa como
diagnóstico de que no fue la causa del retraso. Contra el código actual: **FALLA**
según lo exigido — `status='ok'` en vez de `'timeout'` (verificado estable en 3
ejecuciones consecutivas).

**H10.B (VectorStore bloqueante)** —
`test_h10b_blocking_vector_store_is_preempted_by_hard_deadline`: `embed()` devuelve de
inmediato; `query()` bloquea. Misma aserción final
(`status == "timeout"`/`error.code == "AGENT_TIMEOUT"`/`token.is_cancelled()`). Contra
el código actual: **FALLA** por la misma ausencia de un punto `await` (estable en 3
ejecuciones consecutivas).

**Contraste positivo** —
`test_h10_positive_contrast_released_before_generous_deadline_completes_ok`: mismos
dobles, liberados ~50ms después de empezar, `deadline_ms=5000` (holgado). **PASA**
hoy: `status = "ok"`, sin `AGENT_TIMEOUT`, `token` no cancelado, el fragmento
autorizado se conserva y un fragmento de otro `course_id` que el doble del store
también devuelve queda excluido (T098, `research.md` §14.1b) — reglas T085/T098
conservadas.

**Capacidad de respuesta del bucle de eventos** — documentada por separado, como
experimento NO obligatorio (per esta ronda), en
`tests/failure/test_material_retrieval_h10_event_loop_responsiveness_experiment.py`:
mientras `embed()` bloquea, una segunda corutina independiente (`await
asyncio.sleep(0)` × 2, luego registra su propio progreso) queda demostrablemente
retrasada hasta después de que el bloqueo termina — orden `['blocking_retrieval_
finished', 'independent_probe_progressed']`, verificado estable en 5 ejecuciones
consecutivas. La aserción declarada es el orden CORRECTO deseado tras T086 (la
corutina independiente progresa primero); contra el código actual, por tanto,
**FALLA** también, de forma determinista — la causa no es una carrera de tiempos sino
la política de scheduling cooperativo de un único hilo de asyncio (una tarea sin
ningún punto de suspensión interno monopoliza el bucle durante toda su duración),
documentado con el razonamiento completo en el docstring del módulo. Se conserva fuera
de las dos reproducciones obligatorias porque su estado tras T086 (¿progresa la
segunda corutina de forma fiable, o sigue siendo una carrera de tiempos real contra el
hilo del *executor*?) no está garantizado y queda como trabajo de validación de T086,
no de T091.

**`time_budget_ms` no intervino** — verificado por construcción (60000ms frente a
bloqueos de ≤500ms en las tres pruebas) y, adicionalmente, por una aserción
diagnóstica dentro de `_assert_hard_timeout` que confirma que la advertencia de
presupuesto agotado (`"presupuesto temporal agotado, resultado parcial"`) no aparece
en ningún resultado `status = "ok"` observado durante la reproducción.

**Corrección documental — `research.md` §12** (T091): la premisa "el
`ThreadPoolExecutor` por defecto ya aporta contrapresión (cola acotada) frente a una
ráfaga sostenida" queda corregida — el límite de `min(32, os.cpu_count() + 4)` acota
solo los hilos worker simultáneos, no la cola de trabajo pendiente
(`queue.SimpleQueue`, sin límite), y cancelar el `await` no detiene ni libera el
trabajo ya encolado/en curso. Ver `research.md` §12 (párrafo "Corrección (T091,
2026-09-13)") y la nueva subsección §12.1 con el diseño de contrapresión pendiente
que T086 deberá aplicar (límite de capacidad explícito, *executor* dedicado y/o
control de admisión, liberación de capacidad atada a la finalización real del
trabajo — no a la cancelación del `await` —, compatibilidad entre distintos bucles de
eventos de prueba, y cómo observar en pruebas que una ráfaga no crea una cola
ilimitada) — análisis únicamente, nada de esto se implementa en T091.
`contracts/material-retriever-agent.md` no contiene esta misma afirmación incorrecta
sobre contrapresión (verificado por búsqueda) — no se modifica.

**Regresión y análisis estático**: suite completa antes de añadir las reproducciones
de T091: 42/42 en verde en los ficheros de evidencia T085/T098/T099 (`test_material_
retrieval_h08_reproduction.py`, `test_material_retrieval_widening_structural.py`,
`test_material_retrieval_course_isolation.py`,
`test_self_study_pending_fragment_revalidation.py`,
`test_material_fragment_revalidation.py`). Suite completa tras añadir las
reproducciones de T091: `PYTHONPATH=src uv run pytest tests/ -q -m "not ollama and not
speech"` → **372 passed, 1 deselected, 3 failed** — los 3 fallos son exactamente las
reproducciones deliberadamente rojas de T091 (H10.A, H10.B, el experimento de
capacidad de respuesta), 0 regresiones en el resto de la suite. Ruff: `uv run ruff
check tests/failure/test_material_retrieval_h10_reproduction.py tests/failure/
test_material_retrieval_h10_event_loop_responsiveness_experiment.py --statistics` → 0
errores; `uv run ruff check src/ tests/ --statistics` → 49 errores (idéntico al
recuento de referencia previo: 45 E501, 2 F401, 1 F541, 1 F841, todos heredados, 0
nuevos). Comandos: los anteriores más `PYTHONPATH=src uv run pytest tests/failure/
test_material_retrieval_h10_reproduction.py tests/failure/
test_material_retrieval_h10_event_loop_responsiveness_experiment.py -v -s` (ejecutado
3 y 5 veces respectivamente para confirmar estabilidad, sin flakiness observado en
ninguna dirección).

**No se declara toda la Feature 002 completada** — T086/T087/T092 siguen pendientes,
sin tocar ni duplicar. `MaterialRetrieverAgent` no se modificó en esta ronda; T086
implementará `asyncio.to_thread` sobre `embed`/`query` MÁS el control de admisión
explícito documentado en `research.md` §12.1, y deberá dejar en verde, sin modificar
ninguna de sus aserciones, las tres reproducciones de T091.

## Phase 22: Convergence (T086 implementada — contrapresión acotada para el trabajo bloqueante de recuperación, 2026-09-13)

**Contexto**: T086 mueve `EmbeddingAdapter.embed(...)`/`VectorStore.query(...)` fuera
del hilo del bucle de eventos para que `request.deadline_ms` (`run_with_deadline`,
Feature 001) pueda realmente interrumpirlas, cerrando H10 (research.md §12) —
reproducido en rojo por T091 más arriba, sin tocar entonces `MaterialRetrieverAgent`.
Corrección explícita respecto a lo que T091 dejó documentado como pendiente de
análisis: un `asyncio.to_thread(...)` desnudo NO se implementa — se introduce, en su
lugar, `BoundedBlockingWorker` (nuevo módulo,
`src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py`), con
contrapresión explícita.

**1. Diseño del runner/executor y motivo de su alcance compartido**: `BoundedBlockingWorker`
posee un `ThreadPoolExecutor` dedicado (`max_workers=capacity`, nunca el *executor*
por defecto del bucle de eventos) MÁS un semáforo de admisión (`_LoopScopedSemaphore`)
de la MISMA capacidad, adquirido antes de `executor.submit(...)` — nunca se envían más
de `capacity` llamadas a la vez, así que la cola interna (no acotada) del *executor*
nunca llega a usarse. Instancia de proceso compartida por defecto
(`default_blocking_retrieval_worker()`, construida perezosamente, nunca al importar el
módulo) e inyectable vía `MaterialRetrieverAgent(..., blocking_retrieval_worker=...)`
— **compartida porque producción construye una instancia nueva de
`MaterialRetrieverAgent` por petición** (`materials.py`, `self_study_agency_composer.py`):
un semáforo privado por agente no limitaría nada entre peticiones concurrentes. Nunca
expuesta en `MaterialQueryInput`/la API HTTP.

**2. Capacidad predeterminada y justificación honesta**: `DEFAULT_BLOCKING_RETRIEVAL_
CAPACITY = 4`. Corrección explícita pedida en esta ronda: la redacción previa de
`research.md` §12.1 (T091) sugería derivar el límite en parte de un "coste medido en
T090" — **incorrecto y retractado**: T090 midió únicamente `relevance_score`
(pertinencia), nunca latencia/CPU/memoria de `embed`/`query`. `4` es un techo de
seguridad conservador, elegido solo para que exista un límite explícito (Principio
IX) — no una medición; `research.md` §12.1 deja registrada la necesidad de
recalibrarlo con métricas reales de despliegue.

**3. Momento exacto de adquisición y liberación**: adquisición en
`BoundedBlockingWorker.run()`, antes de `executor.submit(...)`. Liberación atada al
`concurrent.futures.Future.add_done_callback` — nunca al `finally` de la corutina que
hace `await` — marshalled al bucle correcto vía `loop.call_soon_threadsafe(semaphore.
release)`.

**4. Comportamiento en cancelación**: esperando admisión → la espera se interrumpe sin
dejar ninguna adquisición fantasma y **sin enviar nunca el trabajo al executor**
(`test_expired_admission_wait_never_submits_to_executor`). Trabajo ya iniciado →
`asyncio.wrap_future` cancela su envoltorio de inmediato (el llamador —
`run_with_deadline` — nunca espera al hilo bloqueado) e intenta, de mejor esfuerzo,
cancelar el `concurrent.futures.Future` subyacente (no-op si ya está corriendo); el
cupo de capacidad permanece retenido hasta que ese hilo termina por sí solo
(`test_cancelling_in_flight_work_does_not_release_capacity_early`).

**5. Evidencia antes/después de T091** — antes del cambio (re-ejecutado en esta
ronda): `tests/failure/test_material_retrieval_h10_reproduction.py`
`tests/failure/test_material_retrieval_h10_event_loop_responsiveness_experiment.py` →
3 failed, 1 passed (H10.A, H10.B, el experimento de capacidad de respuesta rojos; el
contraste positivo en verde), igual que en T091. Después del cambio, MISMOS archivos,
SIN modificar ninguna aserción: **4 passed** — estable en 5 ejecuciones consecutivas de
cada archivo (incluido el experimento de capacidad de respuesta, no exigido como
obligatorio por T091 pero verde también: con el trabajo ya genuinamente suspendido en
un hilo, la segunda corutina progresa primero de forma consistente en las ejecuciones
observadas).

**6. Ráfaga/recuperación de capacidad/ausencia de trabajo tardío/SQL en hilo
principal/bucles de eventos sucesivos** — pruebas nuevas, todas coordinadas por
`threading.Event` (nunca `sleep` como mecanismo principal), con timeout de seguridad y
liberación en `finally`:
`tests/unit/test_blocking_retrieval_worker.py` (6 pruebas) —
`test_admission_never_exceeds_injected_capacity_under_burst` (capacidad N inyectada,
9 peticiones concurrentes, máximo observado == N, de forma estructural, no
probabilística), `test_expired_admission_wait_never_submits_to_executor`,
`test_cancelling_in_flight_work_does_not_release_capacity_early`,
`test_capacity_recovers_after_ordinary_completion_for_a_later_request`,
`test_worker_reusable_across_successive_event_loops` (dos `asyncio.run()` sucesivos
sobre la misma instancia, sin error de afinidad),
`test_capacity_still_enforced_after_rebinding_to_a_new_event_loop` (la capacidad se
sigue exigiendo tras el cambio de bucle) — 6/6 en verde.
`tests/integration/test_material_retrieval_h10_admission_integration.py` (4 pruebas) —
`test_late_embed_completion_does_not_trigger_a_later_query`,
`test_late_query_completion_triggers_no_sql_conflicts_traces_or_late_results` (0 SQL
nuevo, 0 `MaterialConflictRecord`, 0 `TraceEvent` tras el timeout),
`test_sql_access_stays_on_the_event_loop_thread_never_the_worker` (identidades de
hilo registradas explícitamente: `embed`/`query` en un hilo distinto del principal,
SQL siempre en el principal), `test_widening_loop_still_issues_multiple_awaited_
store_queries` (mismo montaje que H08.A, ahora a través del bucle async — ≥2 rondas
`await`-eadas, mismos dos fragmentos recuperados en el mismo orden) — 4/4 en verde.
Estable en 5 ejecuciones consecutivas de cada archivo nuevo.

**7. T085/T098/T099 sin regresión**: `tests/integration/test_material_retrieval_h08_
reproduction.py`, `test_material_retrieval_widening_structural.py`,
`test_material_retrieval_course_isolation.py`,
`test_self_study_pending_fragment_revalidation.py`,
`tests/unit/test_material_fragment_revalidation.py` → **46 passed** (idéntico al
recuento previo a T086), 0 regresiones.

**8. Regresión completa y Ruff**: `PYTHONPATH=src uv run pytest tests/ -q -m "not
ollama and not speech"` → **385 passed, 1 deselected, 0 failed** (antes de T086: 372
passed + 3 failed + 1 deselected; +10 pruebas nuevas, +3 que pasan de rojo a verde, 0
regresiones). `uv run ruff check src/oralia/domain/agents/material_retriever_agent.py
src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py
tests/unit/test_blocking_retrieval_worker.py
tests/integration/test_material_retrieval_h10_admission_integration.py --statistics`
→ 0 errores. `uv run ruff check src/ tests/ --statistics` → **49 errores**, idéntico
al recuento de referencia heredado (45 E501, 2 F401, 1 F541, 1 F841) — 0 nuevos.

**9. Archivos modificados/creados**: `src/oralia/domain/agents/material_retriever_
agent.py` (modificado — `execute`/`_run_widening_search` ahora `async`-conscientes de
las dos llamadas bloqueantes, nuevo parámetro `blocking_retrieval_worker`);
`src/oralia/infrastructure/concurrency/__init__.py` (nuevo, vacío);
`src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py` (nuevo —
`BoundedBlockingWorker`/`_LoopScopedSemaphore`/`default_blocking_retrieval_worker`);
`tests/unit/test_blocking_retrieval_worker.py` (nuevo, 6 pruebas);
`tests/integration/test_material_retrieval_h10_admission_integration.py` (nuevo, 4
pruebas); `specs/002-materials-rag/research.md` (§12/§12.1 actualizadas con el diseño
implementado, corrección de la premisa de coste de T090);
`specs/002-materials-rag/contracts/material-retriever-agent.md` (regla de
`deadline_ms` corregida — ya no cita `asyncio.to_thread` a secas);
`specs/002-materials-rag/tasks.md` (esta entrada). `tests/failure/test_material_
retrieval_h10_reproduction.py` y
`tests/failure/test_material_retrieval_h10_event_loop_responsiveness_experiment.py`
(T091) **NO se modificaron** — mismas aserciones, ahora en verde.

**10. Estado de T086/T087/T092**: T086 **[X]** implementada y validada. T087 y T092
permanecen **[ ]**, sin tocar ni duplicar — ninguna reconstrucción de índice adicional
ni mecanismo de reintento de T087 se implementa aquí.

**11. `.specify/feature.json`** restaurado a `{"feature_directory":
"specs/004-oral-defense-agency"}` al finalizar esta ronda.

**No se declara toda la Feature 002 completada** — T087/T092 (reconstrucción del
índice, recuperación adicional) siguen pendientes, sin tocar ni duplicar. T086 (H10,
tiempo duro frente a trabajo bloqueante) queda resuelto e implementado en esta ronda.

## Phase 23: Convergence (T100 — corrección de tres fisuras estructurales en la admisión de T086, 2026-09-13)

**Contexto**: una revisión posterior a T086 encontró que `BoundedBlockingWorker`
pasaba las pruebas de esa ronda (que nunca ejercitaban dos bucles de eventos
*simultáneos* en hilos distintos, solo sucesivos) pero no era realmente process-wide
frente a ese caso, además de dos fisuras independientes (fuga de permiso, singleton
sin exclusión mutua). Esta ronda corrige las tres — sin modificar
`MaterialRetrieverAgent`, sin tocar T085/T098/T099, sin modificar `run_with_deadline`,
sin avanzar a T087/T092.

**1. Causa confirmada de R1/R2/R3**: ver `research.md` §12.2 para el detalle completo
— R1: `_LoopScopedSemaphore.acquire()` reconstruía un semáforo COMPLETO y lleno cada
vez que veía un bucle de eventos distinto, sin comprobar permisos pendientes del
anterior (reproducido: con un espía sobre `worker._executor.submit`, se confirma
`submit()` invocado para un bucle B mientras un bucle A, en otro hilo, seguía
reteniendo el único permiso de `capacity=1`). R2: `run()` no envolvía
`executor.submit()` en ningún `try`/`except` — un fallo (reproducido literalmente:
`capacity=1` → `shutdown()` → primera `run()` lanza `RuntimeError` → segunda `run()`
cuelga esperando el permiso perdido, confirmado con `asyncio.wait_for(timeout=3)`) no
tenía ningún `Future` sobre el que enganchar la liberación. R3:
`default_blocking_retrieval_worker()` carecía de `threading.Lock` (confirmado por
inspección de código; la ventana de la carrera es demasiado estrecha para forzarla de
forma determinista en una prueba corta bajo el GIL de CPython).

**2. Diseño de la admisión process-wide**: `_ProcessWideAdmission` (nueva clase,
sustituye a `_LoopScopedSemaphore`, retirada por completo) — un único pool de
`capacity` permisos (`_available`/`_waiters`/`_closed`) protegido por un único
`threading.Lock`, jamás reconstruido al cambiar de bucle. Invariante: cada permiso
está siempre en exactamente uno de tres estados (libre, en manos de trabajo admitido,
en tránsito hacia un waiter concreto) — ningún camino de código fuera de
`_grant_next_locked`/el manejador de cancelación de `acquire()` crea o destruye un
permiso. El lock protege solo contabilidad breve y no bloqueante — la espera real de
un permiso sigue siendo `await` sobre un `asyncio.Future` propio del bucle que llama,
nunca `threading.Semaphore.acquire()` (propiedad 12).

**3. Tratamiento de cancelación/bucle cerrado/fallo de submit/shutdown**: cancelación
mientras se espera admisión → se retira de la cola sin dejar adquisición fantasma, sin
enviar nunca el trabajo. Cancelación de trabajo ya iniciado → `wrap_future` propaga la
cancelación al llamador de inmediato, sin esperar al hilo bloqueado; el cupo se
mantiene hasta que ese hilo termina de verdad. Bucle de un waiter cerrado →
`_grant_next_locked` detecta el `RuntimeError` de `call_soon_threadsafe` y ofrece el
permiso al siguiente waiter, sin perderlo. Fallo de `executor.submit()` → `run()` lo
envuelve en `try/except Exception: self._admission.release(); raise` — el permiso se
devuelve antes de propagar la excepción. `shutdown()` → `_ProcessWideAdmission.close()`
es idempotente, rechaza los waiters pendientes en ese instante, y `acquire()`
comprueba `_closed` como lo primero que hace, bajo el lock, antes de tocar ningún
estado — una llamada posterior a `run()` falla de inmediato sin adquirir ni filtrar
nada.

**4. Reproducción antes/después** (`tests/unit/test_blocking_retrieval_worker_
multiloop.py`, 8 pruebas nuevas, coordinación por `threading.Event`/`_LoopThread` —
bucles de eventos reales en hilos propios — nunca `sleep` como mecanismo principal,
salvo una ventana de equidad breve y acotada donde el propio `ThreadPoolExecutor` de
tamaño fijo (`max_workers == capacity` siempre) enmascararía el síntoma observable de
otro modo — documentada explícitamente en cada caso donde aparece):
- **A+D** (`test_A_and_D_second_loop_blocked_until_first_loop_releases_then_completes`):
  contra el código previo, **FALLA** (`submit()` de B ocurre mientras A retiene el
  único permiso); en verde tras T100, confirmando también que B se admite y completa
  al liberar A.
- **B** (`test_B_cancelling_other_loops_waiter_before_release_never_submits_later`):
  contra el código previo, **FALLA**; en verde tras T100.
- **C** (`test_C_several_loops_never_exceed_capacity_structurally`): contra el código
  previo, **FALLA** (3 envíos admitidos con `capacity=2` y 3 bucles, en vez de 2); en
  verde tras T100.
- **E** (`test_E_permit_skips_a_waiter_whose_loop_already_closed`): contra el código
  previo, la suite falla en recolección (`_ProcessWideAdmission` no existe — evidencia
  igualmente válida); en verde tras T100 (probada directamente contra
  `_ProcessWideAdmission`).
- **F1/F2** (submit falla sin fuga / shutdown falla rápido y coherente): contra el
  código previo, **FALLAN AMBAS** — reproducción literal de los pasos dados para R2;
  en verde tras T100.
- **G/H** (shutdown idempotente / singleton thread-safe): en verde antes y después —
  documentado honestamente en `research.md` §12.2: G no diferencia (el
  `ThreadPoolExecutor.shutdown()` subyacente ya era idempotente por sí solo); la
  carrera de H (R3) es real por inspección de código pero no se logró forzar de forma
  determinista en una prueba corta — la corrección (*double-checked locking*) se
  aplica de todas formas.

**5. Resultados de las pruebas multiloop/multihilo**: `PYTHONPATH=src uv run pytest
tests/unit/test_blocking_retrieval_worker_multiloop.py -v` → **8 passed**, estable en
5 ejecuciones consecutivas.

**6. T091 sigue intacto y en verde**: `tests/failure/test_material_retrieval_h10_
reproduction.py` y `tests/failure/test_material_retrieval_h10_event_loop_
responsiveness_experiment.py` — **NO modificados** — 4/4 en verde (los 3 casos
obligatorios de H10.A/H10.B/contraste positivo, más el experimento no obligatorio de
capacidad de respuesta). `tests/unit/test_blocking_retrieval_worker.py` (T086, 6
pruebas, **NO modificado**) y `tests/integration/test_material_retrieval_h10_
admission_integration.py` (4 pruebas, **NO modificado**) — ambos 6/6 y 4/4 en verde.
Total del conjunto T086+T091+T100 ejecutado junto: **22 passed**.

**7. Regresión T085/T098/T099**: `tests/integration/test_material_retrieval_h08_
reproduction.py`, `test_material_retrieval_widening_structural.py`,
`test_material_retrieval_course_isolation.py`,
`test_self_study_pending_fragment_revalidation.py`,
`tests/unit/test_material_fragment_revalidation.py` → **42 passed**, idéntico al
recuento previo, sin regresión.

**8. Regresión completa y Ruff**: `PYTHONPATH=src uv run pytest tests/ -q -m "not
ollama and not speech"` → **393 passed, 1 deselected, 0 failed** (antes de T100: 385
passed, 1 deselected; +8 pruebas nuevas de `test_blocking_retrieval_worker_
multiloop.py`, 0 regresiones). `uv run ruff check
src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py
tests/unit/test_blocking_retrieval_worker_multiloop.py --statistics` → 0 errores; `uv
run ruff check src/ tests/ --statistics` → **49 errores**, idéntico al recuento de
referencia heredado (45 E501, 2 F401, 1 F541, 1 F841) — 0 nuevos.

**9. Archivos modificados**: `src/oralia/infrastructure/concurrency/blocking_
retrieval_worker.py` (reescrito — `_LoopScopedSemaphore` retirada, sustituida por
`_ProcessWideAdmission`/`_Waiter`/`_resolve_waiter`/`_reject_waiter`;
`BoundedBlockingWorker.run`/`shutdown` y `default_blocking_retrieval_worker`
actualizados); `tests/unit/test_blocking_retrieval_worker_multiloop.py` (nuevo, 8
pruebas); `specs/002-materials-rag/research.md` (§12.1 anotada con nota de cierre, sin
reescribir su evidencia histórica; nueva §12.2); `specs/002-materials-rag/tasks.md`
(esta entrada). `MaterialRetrieverAgent`, `contracts/material-retriever-agent.md`
(salvo su referencia genérica ya existente a `BoundedBlockingWorker`, sin cambios),
`cancellation.py`/`run_with_deadline`, T085/T098/T099, y los archivos de T091/T086 de
T086 **NO se modificaron**.

**10. Estado de T100/T086/T087/T092**: T100 **[X]** implementada y validada — cierra
efectivamente T086 (**[X]**, evidencia original conservada sin reescribir en §12.1/
Phase 22, con nota de referencia a esta entrada). T087 y T092 permanecen **[ ]**, sin
tocar ni duplicar.

**11. `.specify/feature.json`** restaurado a `{"feature_directory":
"specs/004-oral-defense-agency"}` al finalizar esta ronda.

**No se declara toda la Feature 002 completada** — T087/T092 (reconstrucción del
índice, recuperación adicional) siguen pendientes, sin tocar ni duplicar.

## Phase 24: Convergence (T092 ejecutada — reproducción previa a T087/H09, 2026-09-14)

**Contexto**: T092 es la reproducción previa de T087 (research.md §13, hallazgo H09):
`ChromaVectorStore` cachea `self._version` en el constructor y nunca la refresca; una
instancia lectora que resolvió la versión N puede, tras una reconstrucción real
concurrente que mueve el puntero y retira N, terminar su consulta contra una colección
ya borrada — `_collection()` usa `get_or_create_collection`, que la recrea vacía en
vez de señalar el problema. El test existente
(`test_material_query_during_rebuild.py`) solo fabricaba un estado intermedio a mano,
sin intercalación real; esta ronda añade la intercalación real coordinada. `chroma_
store.py` **NO se modifica** — T087 (política de retención de dos generaciones +
reintento acotado + escritura atómica del puntero) sigue sin implementarse,
deliberadamente, a la espera de esta evidencia previa.

**1. Test existente de reconstrucción**: `tests/integration/test_material_query_
during_rebuild.py::test_query_mid_rebuild_sees_old_collection_until_the_swap_completes`
— **PASSED**, sin modificar, re-ejecutado de forma aislada.

**2. Reproducción A** (`test_A_reader_paused_mid_resolution_survives_one_concurrent_
rebuild`) — **FAILED**, discriminante, estable en 5 ejecuciones consecutivas:
`query()` devuelve `[]` (`get_index_version()` sigue reportando `"1"`) en vez de
servir `frag-v1` o re-resolver a `frag-v2`/`"2"`. Causa: `material_fragments_v1`,
borrada por un `rebuild()` real concurrente mientras el lector estaba pausado justo
antes de obtener la colección, es recreada vacía por `get_or_create_collection` al
reanudarse el lector.

**3. Reproducción B** (`test_B_reader_paused_survives_two_concurrent_rebuilds_
needs_retry`) — **FAILED**, discriminante, estable en 5 ejecuciones consecutivas:
mismo síntoma tras DOS reconstrucciones reales consecutivas durante la pausa (N=1 →
N+1=2 → N+2=3) — `query()` devuelve `[]` en vez de re-resolver y servir `frag-v3`/
`"3"`, pese a que N está genuinamente retirada incluso bajo la futura política de dos
generaciones.

**4. Excepción concreta observada en Chroma** (`test_empirical_chroma_behavior_on_a_
deleted_collection_object`, no bloqueante — **PASSED**): tanto `.count()` como
`.query(...)` sobre un objeto `Collection` cuya colección subyacente fue borrada por
otra instancia lanzan `chromadb.errors.NotFoundError` (`chromadb==1.5.9`) —
`count()`: `"Collection [<uuid>] does not exist."`; `query()`: `"Error getting
collection: Collection [<uuid>] does not exist."` — nunca un resultado silencioso o
corrupto. T087 MUST capturar específicamente esta excepción, no un `except Exception`
indiscriminado.

**5. Evidencia de recreación silenciosa**: confirmada directamente en ambas
reproducciones — `material_fragments_v1` existe en `list_collections()` tras cada
reproducción, con `count() == 0`, pese a haber contenido originalmente un fragmento.

**6. Archivos añadidos**: `tests/integration/test_material_index_rebuild_race_
reproduction.py` (nuevo — 3 pruebas: A, B, la medición empírica). Ningún archivo de
producción modificado (`chroma_store.py`, comandos de ingestión/rebuild, locks,
contratos — todos intactos).

**7. Regresión y Ruff**: suite previa excluyendo los dos casos rojos nuevos —
`PYTHONPATH=src uv run pytest tests/ -q -m "not ollama and not speech" --deselect
tests/integration/test_material_index_rebuild_race_reproduction.py::
test_A_reader_paused_mid_resolution_survives_one_concurrent_rebuild --deselect
tests/integration/test_material_index_rebuild_race_reproduction.py::
test_B_reader_paused_survives_two_concurrent_rebuilds_needs_retry` → **394 passed, 3
deselected, 0 failed** (antes de T092: 393 passed, 1 deselected; +1 prueba nueva en
verde —la medición empírica—, +2 deselecciones explícitas de las reproducciones
rojas, 0 regresiones). Ruff: `uv run ruff check tests/integration/test_material_
index_rebuild_race_reproduction.py --statistics` → 0 errores; `uv run ruff check
src/ tests/ --statistics` → **49 errores**, idéntico al recuento de referencia
heredado (45 E501, 2 F401, 1 F541, 1 F841) — 0 nuevos.

**8. Estado de T092/T087**: T092 **[X]** ejecutada y documentada. T087 permanece
**[ ]**, sin tocar ni duplicar — `chroma_store.py` no se modificó en esta ronda.

**9. `.specify/feature.json`** restaurado a `{"feature_directory":
"specs/004-oral-defense-agency"}` al finalizar esta ronda.

**No se declara toda la Feature 002 completada** — T087 (política de retención,
reintento, escritura atómica del puntero, lock de ingestión) sigue pendiente, sin
tocar ni duplicar. T092 deja documentado el punto exacto de intercalación y la
excepción específica que T087 deberá capturar.
