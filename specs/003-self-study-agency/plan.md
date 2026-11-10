# Implementation Plan: Agencia de autoestudio

**Branch**: `003-self-study-agency` | **Date**: 2026-09-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/003-self-study-agency/spec.md` (versión
cerrada tras dos rondas de `/speckit-clarify`, 2026-09-01). Este plan incorpora además
una ronda de corrección de consistencia arquitectónica (2026-09-02) sobre: fuente de
verdad del modo activo, número de adaptadores de `GenerationPort`, independencia de
`SolutionNonDisclosureVerifierAgent` y alcance real de FR-028.

## Summary

Añadir al monolito modular ya existente (Features 001 + 002, ambas validadas y sin
tocar) una agencia de autoestudio por texto con cinco submodos canónicos
(`doubt_resolution`, `guided_explanation`, `practice_questions`,
`presentation_preparation`, `concept_review`) que comparten una única sociedad de
agentes y un único estado cognitivo. El orquestador compone dinámicamente, turno a
turno, un subconjunto de agentes — interpretación de intención (nueva, determinista),
recuperación documental (`MaterialRetrieverAgent`, Feature 002, sin cambios), respuesta
fundamentada y generación de preguntas (nuevas, respaldadas por un `GenerationPort` con
adaptador Ollama real y reserva determinista), comprobación de fundamentación
(`GroundingVerifierAgent`, Feature 002, sin cambios), no-revelación de solución (nueva,
verificador independiente), coherencia conversacional (nueva, heurística determinista),
control constitucional (`ConstitutionalControl`, Feature 001, sin cambios) y resumen de
sesión (nuevo) — registrando por qué activó cada uno. Puramente aditiva: ningún fichero
de las Features 001/002 se modifica (FR-025).

## Technical Context

**Language/Version**: Python 3.12 (mismo proyecto `uv`); TypeScript para pantallas
nuevas de participante/técnica.

**Primary Dependencies**: FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, `structlog`,
`chromadb`, `sentence-transformers` reutilizados. `httpx` promovido a dependencia
principal (research.md §1) para `OllamaGenerationAdapter`. Ningún SDK propietario.

**Storage**: mismo SQLite WAL; tablas nuevas `self_study_activity_config`,
`practice_question`, `coherence_incident` (data-model.md). Resumen de sesión, registro
de generación, `non_disclosure_check` y `verification_combined` se persisten como
`TraceEvent` (sin tabla nueva). Retención heredada transitivamente de
`ActivityConfiguration.retention_policy_id` (Feature 001) — sin sistema de retención
paralelo (research.md §8).

**Testing**: `pytest`/`pytest-asyncio`; marcador nuevo `ollama` para integración real
contra un servidor local, omitido por defecto en CI (research.md §1/§10 iteración
anterior). Suite determinista (sin Ollama) obligatoria en CI.

**Target Platform**: igual que 001/002 — `127.0.0.1` por defecto; Ollama, si se usa,
corre localmente.

**Project Type**: extensión del monolito modular ya existente.

**Performance Goals**: timeout de la llamada a Ollama = 6000 ms por defecto
(`ORALIA_OLLAMA_TIMEOUT_MS`), subordinado al `timeout_ms` del agente; degradación a
`DeterministicGenerationAdapter` sin fallar el turno (research.md §1/§2).

**Constraints**: sin acceso a Internet (Ollama es un servidor local); contexto de
generación construido solo desde `concepts_addressed`/evidencia del turno actual, nunca
el historial completo (FR-010); frontera instrucción/dato estricta entre el mensaje
`system` fijo y la evidencia de materiales (FR-008b, research.md §3); ningún fichero de
las Features 001/002 se modifica (FR-025); ninguna consulta agrega por
`participant_code` entre sesiones (FR-011a, research.md §8).

**Scale/Scope**: 5 modos canónicos, ≥3 composiciones de agencia distintas demostrables
en pruebas (SC-003), 5/5 modos con escenario específico de SC-001, 1 servidor de
inferencia local opcional.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Evaluación | Estado |
|---|---|---|
| I. Finalidad y límites institucionales | Sin robots, Moodle, Internet, expedientes; `AI_DISCLOSURE` (Feature 001) reutilizado sin cambios; el LLM es un servidor local, nunca un proveedor externo; ningún agente asigna notas ni decide académicamente (FR-014, FR-022/FR-022a, FR-026). | PASS |
| II. Arquitectura modular basada en contratos | 5 agentes nuevos (`StudyIntentInterpreterAgent`, `ResponseGeneratorAgent`, `PracticeQuestionAgent`, `SolutionNonDisclosureVerifierAgent`, `CoherenceVerifierAgent`) implementan el mismo `Executable`/`AgentContract` de la Feature 001; `GenerationPort` es una interfaz sustituible propia; un único proceso, sin microservicios (research.md §10). | PASS |
| III. Estado cognitivo explícito y memoria diferenciada | No se amplía el esquema de `CognitiveState`/`StatePatch`; `CognitiveState.mode` (campo ya existente) es la fuente de verdad del modo activo, actualizado exclusivamente vía `StatePatch` versionado (research.md §6) — la traza solo audita esa decisión, nunca la sustituye; `concepts_addressed`/`concepts_pending`/`intent_hypotheses` ya existentes se reutilizan para la diferenciación de modos; `PracticeQuestion` acotado a `session_id`, sin agregación entre sesiones (FR-011a, research.md §8). | PASS |
| IV. Separación recuperación/generación/decisión/verificación | Generadores (`ResponseGeneratorAgent`/`PracticeQuestionAgent`) nunca verifican su propia salida; `GroundingVerifierAgent` (002) + `CoherenceVerifierAgent` + `SolutionNonDisclosureVerifierAgent` (contrato/umbral/veredicto/traza propios, research.md §4) + `ConstitutionalControl` (001) verifican de forma independiente; el LLM nunca es su propio verificador — no se añade un segundo LLM como juez (research.md §4/§9). | PASS |
| V. Fundamentación en materiales autorizados | Evidencia de `MaterialRetrieverAgent` (002) pasa por `GroundingVerifierAgent` (002) sea cual sea el adaptador de generación; sin evidencia suficiente, el sistema reconoce la falta de información en vez de generar (research.md §2, FR-008a). | PASS |
| VI. Supervisión humana y gobernanza | `SelfStudyActivityConfig` inmutable tras el primer uso de la actividad, mismo patrón exacto que `ActivityConfiguration` (research.md §7). | PASS |
| VII. Privacidad, minimización y accesibilidad | Sin datos personales nuevos; `127.0.0.1` heredado; registro de generación excluye prompt/respuesta cruda; retención heredada de `RetentionPolicy` (001, vía `ActivityConfiguration.retention_policy_id`), sin sistema paralelo, más un mecanismo de purga invocable manualmente (research.md §8, nuevo). | PASS |
| VIII. Trazabilidad y reproducibilidad | `TraceEvent` nuevos (`agents_selected`, `generation_call`, `non_disclosure_check`, `verification_combined`, `study_session_summary`) permiten verificar SC-001 sin comparar texto literal (research.md §9); la traza documenta el modo activo, nunca lo decide (`CognitiveState.mode` es la fuente de verdad, research.md §6); ausencia de un job de purga automático documentada con transparencia como dependencia esperada de la Feature 005, no oculta (research.md §8). | PASS |
| IX. Degradación controlada y límites de recursos | Cadena de recuperación en tres niveles y dos mecanismos (research.md §2): sin evidencia → reconocer, no inventar (decisión del compositor); fallo técnico → Ollama → `DeterministicGenerationAdapter` (dentro del propio agente generador, §1); fallo total del agente → red de seguridad genérica ya existente de `execute_agency`/`SafeFallbackAgent` (001, sin cambios) — sin un tercer mecanismo de fallback paralelo. Reintentos de no-revelación acotados (máx. 2, research.md §4). | PASS |
| X. Calidad, pruebas y evidencia | Pruebas de contrato por agente nuevo (5), integración por cada composición de agencia (5/5 modos, SC-001/SC-003), failure para cada punto de degradación de research.md §1/§2/§4 y para la purga de retención, deterministas sin Ollama obligatorias en CI — detalladas en Project Structure. | PASS (a verificar en tasks/implementación) |
| XI. Simplicidad evolutiva | `GenerationPort` reducido a dos implementaciones, sin una tercera envoltorio redundante (research.md §1); `SolutionNonDisclosureVerifierAgent` independiente de `GroundingVerifierAgent` en contrato/umbral/traza, comparte solo la técnica general, no código ni configuración (research.md §4); umbrales de coherencia como constantes configurables (research.md §5); retención reutiliza `RetentionPolicy` sin sistema paralelo, con un único mecanismo de purga nuevo y mínimo, no un scheduler (research.md §8); trazabilidad sin infraestructura nueva, solo `event_type` adicionales sobre `TraceEvent` ya existente (research.md §9). | PASS |

**Resultado**: sin violaciones. No se requiere `Complexity Tracking`.

## Project Structure

### Documentation (this feature)

```text
specs/003-self-study-agency/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── self-study-agents.md
│   └── api-self-study.md
└── tasks.md              # Phase 2 output (/speckit-tasks) — NOT created by /speckit-plan
```

### Source Code (repository root)

```text
src/oralia/
  domain/
    self_study/                       # NUEVO
      self_study_activity_config.py
      practice_question.py
      coherence_incident.py
    agents/
      study_intent_interpreter.py           # NUEVO
      response_generator_agent.py           # NUEVO
      practice_question_agent.py            # NUEVO
      solution_non_disclosure_verifier_agent.py  # NUEVO (research.md §4)
      coherence_verifier_agent.py           # NUEVO
      material_retriever_agent.py           # REUTILIZADO sin cambios (Feature 002)
      grounding_verifier_agent.py           # REUTILIZADO sin cambios (Feature 002)
      interpreter_agent.py                  # NO TOCADO (Feature 001)
    policies/
      constitutional_control.py             # REUTILIZADO sin cambios (Feature 001)
  application/
    commands/
      submit_study_turn.py                  # NUEVO
      end_study_session.py                  # NUEVO — envuelve close_session (001, sin cambios)
      configure_self_study_activity.py       # NUEVO — valida inmutabilidad (research.md §7)
      purge_expired_self_study_data.py       # NUEVO — mecanismo invocable de FR-028 (research.md §8)
    orchestration/
      study_turn_orchestrator.py            # NUEVO — reutiliza execute_agency (001, sin cambios)
      self_study_agency_composer.py         # NUEVO — construye AgencyDefinition dinámica (FR-003)
                                             #   incluye la lógica de "verify-combined" (research.md §5)
                                             #   y la derivación de fallo_agente/latencia_excesiva
                                             #   directamente desde AgencyOutcome (research.md §5)
    services/
      study_session_summary_service.py      # NUEVO
  infrastructure/
    generation/                             # NUEVO
      generation_port.py                    # GenerationRequest/GenerationOutcome/GenerationPort
      ollama_adapter.py                     # OllamaGenerationAdapter (httpx; frontera system/user, research.md §3)
      deterministic_adapter.py              # DeterministicGenerationAdapter (research.md §1 — solo 2 implementaciones, sin envoltorio)
      config.py                             # ORALIA_OLLAMA_*, ORALIA_COHERENCE_*, ORALIA_DISCLOSURE_OVERLAP_THRESHOLD, ORALIA_PRACTICE_REGEN_MAX_ATTEMPTS
    db/
      models.py                             # EXTENDIDO: 3 tablas nuevas (nueva migración Alembic)
  interfaces/
    api/
      routers/
        self_study.py                       # NUEVO — incluye POST /tecnica/self-study/purge-expired (FR-028)
        participante.py                     # NO TOCADO
        materials.py                        # NO TOCADO

apps/web/src/routes/
  Autoestudio.tsx                           # NUEVO
  Tecnica.tsx                               # NO TOCADO directamente; solo enlace mínimo de navegación

tests/
  contract/
    test_study_intent_interpreter.py            # NUEVO — remediación D1 (Principio X)
    test_self_study_config.py                    # NUEVO — 201/409/422, incluye inmutabilidad (research.md §7)
    test_response_generator_agent.py              # NUEVO — determinista, sin Ollama
    test_self_study_turns_endpoint.py              # NUEVO — 200/404 de POST .../study-turns
    test_mode_not_enabled_rejected.py               # NUEVO — 409 de POST .../study-turns
    test_practice_question_agent.py                  # NUEVO
    test_solution_non_disclosure_verifier.py          # NUEVO — casos approved/block
    test_coherence_verifier_agent.py                   # NUEVO
    test_study_end_endpoint.py                          # NUEVO — study_summary nulo/no nulo
    test_purge_expired_endpoint.py                       # NUEVO — forma de PurgeResult
  integration/
    test_self_study_session_start_disclosure.py           # NUEVO — remediación E6 (FR-005, reuso de start_session)
    test_mode_doubt_resolution.py                          # NUEVO — SC-001, FR-003 (agents_selected desde US1)
    test_generation_trace.py                                # NUEVO
    test_no_evidence_acknowledge_missing_info.py             # NUEVO — no inventar (research.md §2)
    test_grounding_verdict_mapping.py                         # NUEVO
    test_general_knowledge_labeling.py                         # NUEVO — remediación E3 (FR-019)
    test_mode_guided_explanation.py                             # NUEVO — SC-001
    test_guided_explanation_progression.py                       # NUEVO
    test_sc005_context_continuity.py                              # NUEVO — remediación E1 (SC-005)
    test_mode_practice_questions.py                                # NUEVO — SC-001
    test_mode_switch_state_patch.py                                 # NUEVO — CognitiveState.mode como fuente de verdad (research.md §6)
    test_mode_presentation_preparation.py                            # NUEVO — SC-001
    test_mode_concept_review.py                                       # NUEVO — SC-001
    test_agency_composition_variety.py                                 # NUEVO — SC-003, ≥3 composiciones distintas
    test_sc001_traceability.py                                          # NUEVO — SC-001 vía CognitiveState.mode + agents_selected + DialogueAction
    test_verification_combined.py                                        # NUEVO — tabla de severidad research.md §5
    test_coherence_conditions_fr015.py                                    # NUEVO — remediación E5 (las 9 condiciones de FR-015)
    test_session_limit_summary.py                                          # NUEVO
    test_sc006_trace_reconstruction_after_limit_close.py                    # NUEVO — remediación E7 (SC-006)
    test_summary_ephemeral.py                                                # NUEVO — FR-021
    test_session_isolation.py                                                 # NUEVO — FR-011
  failure/
    test_prompt_injection_from_materials.py                     # NUEVO — FR-008b
    test_generation_ollama_unavailable.py                        # NUEVO — degradación a DeterministicGenerationAdapter
    test_generation_both_adapters_fail.py                         # NUEVO — red de seguridad genérica execute_agency/SafeFallbackAgent
    test_topic_change_out_of_scope.py                              # NUEVO — remediación E2 (FR-023)
    test_reveal_solution_false_blocked_and_regenerated.py           # NUEVO — FR-013a
    test_mode_change_rejected.py                                      # NUEVO — Edge Cases
    test_verifier_conflict_severity.py                                 # NUEVO — research.md §5
    test_purge_expired_self_study_data.py                               # NUEVO — FR-028
    test_longitudinal_aggregation_forbidden.py                           # NUEVO — FR-011a, ninguna ruta agrega por participant_code
  unit/
    test_intent_fr009_coverage.py                                          # NUEVO — remediación E4 (FR-009, las 6 solicitudes)
    test_solution_non_disclosure_threshold_independent.py                   # NUEVO — umbral propio, distinto del de GroundingVerifierAgent (research.md §4)
    test_coherence_repetition_window.py                                      # NUEVO — research.md §5
    test_coherence_thresholds.py                                              # NUEVO — ventanas configurables (research.md §5)
  ollama/                                                                      # marcador pytest "ollama", omitido por defecto en CI
    test_ollama_generation_real.py                                             # NUEVO — opcional
  # regresión completa 001+002: ejecutar tests/ -q -m "not ollama" sin fallos nuevos (139 pruebas base)
```

**Decisión de remediación (`/speckit-analyze`, hallazgo F2)**: `domain/validation/
study_dialogue_action.py`, predicho en una iteración anterior de este plan, **no se
crea**. La selección de `dialogue_action` no tenía una necesidad demostrable de vivir en
un módulo independiente (Principio XI: evitar abstracción prematura) — queda
correctamente encapsulada dentro de las tareas de `self_study_agency_composer.py`
(T018 y sus extensiones), junto con el resto de la lógica de composición por turno. No
se crea un fichero solo para cumplir una predicción de planificación ya superada.

**Ficheros explícitamente NO tocados** (FR-025): `turn_orchestrator.py`,
`agency_composer.py`, `submit_turn.py`, `interfaces/api/routers/participante.py`,
`cognitive_state.py`, `state_patch.py`, `dialogue_action.py`,
`constitutional_control.py`, `material_retriever_agent.py`,
`grounding_verifier_agent.py`, `retention_policy.py`, y cualquier tabla ya definida en
`specs/001-core-cognitive-runtime/data-model.md` o
`specs/002-materials-rag/data-model.md`. `pyproject.toml` se extiende (añade `httpx` a
dependencias principales), igual que ya hizo la Feature 002.

**Structure Decision**: extensión puramente aditiva del monolito modular ya existente;
`infrastructure/generation/` es el único adaptador de infraestructura genuinamente
nuevo, detrás de `GenerationPort`, mismo patrón que `VectorStore`/`EmbeddingAdapter`
(Feature 002).

## Complexity Tracking

*Sin violaciones de la Constitution Check — tabla no aplicable.*
