# Revisión de conformidad constitucional (T077)

Revisión de la **implementación real** (no solo del plan) de la Feature 001 frente a
cada principio de `.specify/memory/constitution.md`. `plan.md` ya contiene una
Constitution Check previa al diseño; este documento la revalida después de escribir el
código.

| Principio | Evidencia en el código | Estado |
|---|---|---|
| I. Finalidad y límites institucionales | `AI_DISCLOSURE` se muestra antes del primer turno (`start_session.py`); `ConstitutionalControl` bloquea notas/decisiones académicas (`constitutional_control.py`); sin robots/Moodle/Internet en ninguna dependencia. | PASS |
| II. Arquitectura modular basada en contratos | `AgentContractSchema` con todos los campos exigidos (`agent_contract.py`, `agent.py`); un único proceso Python, sin microservicios. | PASS |
| III. Estado cognitivo explícito y memoria diferenciada | `CognitiveState`/`StatePatch` fuera del contexto de ningún LLM (no hay LLM en esta feature); `memory_category` en `TraceEvent` distingue las 5 categorías mínimas. | PASS |
| IV. Separación recuperación/generación/decisión/verificación | `ExecutionStep.role` valida que un mismo agente no sea generador y verificador (`agency.py`, `_no_agent_is_both_generator_and_verifier_for_itself`); `ConstitutionalControl` es un agente separado, nunca el propio generador. | PASS |
| V. Fundamentación en materiales autorizados | No aplica todavía (sin materiales reales); `general_knowledge_allowed` por defecto `False`. | PASS (alcance diferido, según lo previsto) |
| VI. Supervisión humana y gobernanza | Configuración de actividad creada manualmente vía API por el profesor/administrador; ningún agente puede modificar `ActivityConfiguration` una vez inmutable (`create_activity.py`). | PASS |
| VII. Privacidad, minimización y accesibilidad | `127.0.0.1` por defecto (`app.py`, `main.py`); `ParticipantCode` rechaza apariencia de identidad real (`_looks_like_real_identity`); FR-025 implementado en `styles.css`/JSX (teclado, etiquetas, contraste, mensajes comprensibles) — sin auditoría automatizada (sin Node en este entorno, ver `docs/001_core_runtime_instalacion.md`). | PASS (con limitación documentada) |
| VIII. Trazabilidad y reproducibilidad | `TraceEvent` + `StatePatch` append-only permiten reconstrucción completa incluso tras un reinicio simulado (`test_session_reconstruction_after_restart.py`); ningún campo almacena razonamiento privado de modelo (no hay LLM). | PASS |
| IX. Degradación controlada y límites de recursos | `deadline_ms` por agente honra el contrato del agente realmente registrado (no uno hardcodeado — corregido durante la implementación); el control constitucional se re-evalúa explícitamente en el camino degradado/fallback, nunca se omite (`turn_orchestrator.py`, FR-018a). | PASS |
| X. Calidad, pruebas y evidencia | 66 pruebas automatizadas (unit/contract/integration/failure) cubren cada historia de usuario, además de escenarios de fallo, timeout, conflicto y bloqueo constitucional; evidencia de `quickstart.md` registrada en `quickstart-validation-evidence.md`. | PASS |
| XI. Simplicidad evolutiva | Componentes de la pila propuesta no usados en esta feature (ChromaDB, embeddings, adaptadores LLM, STT/TTS, Docker Compose) deliberadamente no instalados (`research.md` §6); SQLite + proceso único; toda dependencia añadida está en `pyproject.toml` y se justifica en `research.md`. | PASS |

## Hallazgo corregido durante la implementación (no una violación final)

Durante la escritura de las pruebas de la Historia de Usuario 4 se detectó que el flujo
degradado (`fallback`) omitía el control constitucional sobre el texto de reserva,
delegando en el resultado (obsoleto) del paso "verify" evaluado contra una salida vacía.
Esto habría violado el Principio IX. Se corrigió en `turn_orchestrator.py` y
`agency_composer.py` para que el control constitucional se re-evalúe siempre sobre el
texto que realmente se va a mostrar, con su propio `TraceEvent` — ver
`tests/failure/test_degradation_constitutional_check.py`.

## Resultado

Sin violaciones abiertas. Una limitación documentada (auditoría de accesibilidad
automatizada pendiente por falta de Node.js en este entorno) — no bloquea el Principio
VII porque los requisitos funcionales (FR-025) sí están implementados, solo no
verificados con herramienta automatizada.
