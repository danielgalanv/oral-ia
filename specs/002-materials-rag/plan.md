# Implementation Plan: Materiales autorizados y RAG trazable

**Branch**: `002-materials-rag` | **Date**: 2026-07-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-materials-rag/spec.md`

## Summary

Añadir al monolito modular ya existente (Feature 001) la gestión de materiales docentes
autorizados y un sistema local de recuperación documental (RAG) trazable: incorporación
y activación de documentos (PDF textual, DOCX, PPTX, TXT, Markdown), un
`MaterialRetrieverAgent` que devuelve fragmentos con procedencia completa filtrados por
autorización, y un `GroundingVerifierAgent` que clasifica la fundamentación de una
propuesta frente a la evidencia recuperada. Esta feature es puramente aditiva sobre la
Feature 001 (FR-025/FR-030): no modifica `turn_orchestrator.py`, `DEFAULT_AGENCY`, el
`VerificationResult` constitucional, ni ningún otro comportamiento ya validado. La
integración de estos agentes en un turno conversacional real de estudiante es
responsabilidad explícita de la Feature 003.

## Technical Context

**Language/Version**: Python 3.12 (mismo proyecto `uv` de la Feature 001); TypeScript
para las pantallas nuevas del área técnica.

**Primary Dependencies**: `chromadb` (índice vectorial persistente local), `sentence-transformers`
(embeddings locales), `pdfplumber`, `python-docx`, `python-pptx` (extracción por
formato) — todos deliberadamente diferidos en la Feature 001 (research.md §6 de esa
feature) hasta que esta feature los necesitara realmente (research.md §10 de esta
feature). Se reutilizan FastAPI, Pydantic v2, SQLAlchemy 2, Alembic y `structlog` ya
presentes.

**Storage**: SQLite (mismo motor y WAL de la Feature 001) para metadatos/entidades
relacionales; ChromaDB en modo persistente local (directorio propio) para los vectores
de embeddings — dos almacenes, cada uno detrás de su propia interfaz sustituible
(`VectorStore`, research.md §2).

**Testing**: `pytest`/`pytest-asyncio` (unit, contract, integration, failure), mismo
patrón que la Feature 001; sin pruebas de extremo a extremo nuevas por Playwright en
esta feature salvo que se amplíe la UI técnica (`Tecnica.tsx`) con pantallas de
materiales — pendiente de confirmar en `tasks.md`.

**Target Platform**: igual que la Feature 001 — aplicación local de un único
usuario/instancia, `127.0.0.1` por defecto; sin llamadas de red externas (embeddings y
extracción corren en el mismo proceso/máquina).

**Project Type**: extensión del monolito modular ya existente (no es un proyecto nuevo).

**Performance Goals**: sin objetivo de throughput distinto al ya establecido; una
recuperación MUST respetar el `time_budget_ms` de su propia consulta (FR-017),
devolviendo resultados parciales si se agota (research.md, contrato del
`MaterialRetrieverAgent`).

**Constraints**: sin acceso a Internet durante la indexación ni la recuperación
(Principio I); el texto extraído de documentos MUST tratarse siempre como datos, nunca
como instrucciones (FR-028, research.md §8); un único proceso de reconstrucción de
índice a la vez (research.md §9).

**Scale/Scope**: alcance de esta feature: 5 formatos de documento, un índice vectorial
por instancia local, sin límite de asignaturas/actividades distinto al ya soportado por
`Course`/`ActivityConfiguration` (Feature 001).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Evaluación | Estado |
|---|---|---|
| I. Finalidad y límites institucionales | Sin acceso a Internet ni servicios externos; extracción/embeddings/índice 100% locales. | PASS |
| II. Arquitectura modular basada en contratos | `MaterialRetrieverAgent`/`GroundingVerifierAgent` implementan el mismo `Executable`/`AgentContract` de la Feature 001; `VectorStore` y `EmbeddingAdapter` son interfaces sustituibles propias. | PASS |
| III. Estado cognitivo explícito y memoria diferenciada | No se modifica `CognitiveState`/`StatePatch`; los resultados de recuperación se pasan como `AgentRequest.input`/`AgentResult.output`, nunca dentro del contexto de un LLM (que no existe todavía). | PASS |
| IV. Separación recuperación/generación/decisión/verificación | Esta feature es, precisamente, la implementación real del rol "retriever" y añade un verificador de fundamentación independiente del constitucional — ambos roles ya estaban previstos y separados en el contrato de agencia de la Feature 001 (`ExecutionStep.role`). | PASS |
| V. Fundamentación en materiales autorizados | Es el propósito central de esta feature: procedencia completa (FR-029), veredictos de fundamentación (FR-023), conocimiento general etiquetado (FR-025). | PASS |
| VI. Supervisión humana y gobernanza | Toda gestión de materiales (carga, activación, sustitución, resolución de duplicados, revisión de conflictos) requiere una acción explícita del profesor vía API; ninguna decisión se toma de forma automática (FR-005a, FR-022a). | PASS |
| VII. Privacidad, minimización y accesibilidad | Sin datos personales nuevos; `127.0.0.1` heredado; pantallas nuevas del área técnica deben seguir el mismo estándar de accesibilidad ya exigido (FR-025 de la Feature 001) — se verificará en `tasks.md`. | PASS |
| VIII. Trazabilidad y reproducibilidad | Procedencia documento/versión/ubicación en cada fragmento (FR-029); recuperación reproducible por versión de índice (FR-020); `MaterialConflictRecord` persistente. | PASS |
| IX. Degradación controlada y límites de recursos | Presupuesto temporal por consulta con resultado parcial explícito (no fallo silencioso); fallo de indexación no afecta al índice existente (FR-027). | PASS |
| X. Calidad, pruebas y evidencia | Contract tests por endpoint/agente, integration tests por historia de usuario, failure tests para fallo de indexación/conflicto de reconstrucción — a detallar en `tasks.md`; SC-005 exige un conjunto de pruebas preparado para el verificador de fundamentación. | PASS (a verificar en tasks/implementación) |
| XI. Simplicidad evolutiva | Segmentador propio en vez de un framework de chunking; heurística determinista de conflicto en vez de un modelo NLI; se reutiliza el patrón de bloqueo de un solo escritor de la Feature 001 en vez de inventar uno nuevo (research.md §5, §7, §9). | PASS |

**Resultado**: sin violaciones. No se requiere `Complexity Tracking`.

## Project Structure

### Documentation (this feature)

```text
specs/002-materials-rag/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md         # Phase 1 output (/speckit-plan command)
├── quickstart.md         # Phase 1 output (/speckit-plan command)
├── contracts/            # Phase 1 output (/speckit-plan command)
│   └── material-retriever-agent.md
└── tasks.md              # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

Extiende el monolito modular ya existente de la Feature 001 (`src/oralia/`) — no crea
una estructura nueva, añade módulos dentro de la organización ya establecida:

```text
src/oralia/
  domain/
    materials/                    # NUEVO: MaterialDocument, MaterialFragment, Evidence,
                                    #   GroundingVerificationResult, MaterialConflictRecord
    agents/
      material_retriever_agent.py  # NUEVO: MaterialRetrieverAgent (Executable)
      grounding_verifier_agent.py  # NUEVO: GroundingVerifierAgent (Executable)
  application/
    commands/
      ingest_material.py           # NUEVO: carga, validación, hash, duplicados (FR-001..FR-005a)
      activate_material.py         # NUEVO: activar/desactivar/asignar a actividad
      replace_material_version.py  # NUEVO: sustitución de versión (FR-014/FR-015)
      rebuild_material_index.py    # NUEVO: reconstrucción de índice con bloqueo (research.md §9)
      review_material_conflict.py  # NUEVO: marcar MaterialConflictRecord revisado
    queries/
      get_material_catalog.py      # NUEVO: estado de documentos, conflictos pendientes
    orchestration/
      (sin cambios — no se modifica turn_orchestrator.py, ver research.md §1)
  infrastructure/
    db/
      models.py                    # EXTENDIDO: nuevas tablas de esta feature (nueva migración)
    documents/                      # NUEVO: DocumentExtractor por formato (research.md §4)
    embeddings/                     # NUEVO: EmbeddingAdapter (sentence-transformers, research.md §3)
    vector_store/                   # NUEVO: VectorStore (ChromaDB, research.md §2)
  interfaces/
    api/
      routers/
        materials.py                # NUEVO: endpoints de contracts/material-retriever-agent.md

apps/web/src/routes/
  Tecnica.tsx                       # EXTENDIDO: pantallas de materiales (carga, estado, conflictos)

tests/
  contract/    # 1 por endpoint de materials.py y por forma input/output de cada agente
  integration/ # 1 por historia de usuario (US1-US7)
  failure/     # fallo de indexación, conflicto de reconstrucción, presupuesto agotado
  unit/        # segmentador determinista, heurística de conflicto, duplicate-hash
```

**Carpetas deliberadamente no creadas en esta feature**: `infrastructure/speech/` y
cualquier adaptador de generación conversacional (Feature 004+); la composición de
`MaterialRetrieverAgent`/`GroundingVerifierAgent` en una `AgencyDefinition` de diálogo
real pertenece a la Feature 003 (research.md §1).

**Structure Decision**: extensión aditiva del monolito modular ya existente
(`src/oralia/`), sin nueva separación de repos ni servicios; los tres adaptadores nuevos
(documentos, embeddings, índice vectorial) quedan cada uno detrás de su propia interfaz
sustituible, siguiendo el mismo patrón ya usado en la Feature 001 para el motor de
almacenamiento y el monitor de recursos.

## Complexity Tracking

*Sin violaciones de la Constitution Check — tabla no aplicable.*
