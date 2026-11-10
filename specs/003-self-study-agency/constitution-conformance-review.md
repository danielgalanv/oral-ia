# Revisión de conformidad constitucional — Feature 003 (Agencia de autoestudio)

Autoevaluación (T093) contra `.specify/memory/constitution.md` v1.0.0, tras completar
la implementación (T001–T088) y con la suite en verde (239 pruebas, `-m "not ollama"`).

## I. Finalidad y límites institucionales

**Conforme.** `ConstitutionalControl` (Feature 001, reutilizada sin cambios) se ejecuta
en todos los turnos, incluidos los degradados (`self_study_agency_composer.py`,
re-chequeo explícito tras `SafeFallbackAgent`). El sistema nunca asigna nota ni
calificación: `PracticeQuestionAgent`/turnos de `practice_questions` no evalúan la
respuesta del estudiante (FR-014, `test_mode_practice_questions.py` confirma
explícitamente la ausencia de vocabulario de calificación en toda la traza).
`GenerationConstraints`/`OllamaGenerationAdapter` no exponen ninguna vía de acceso a
Internet más allá del servidor Ollama local opcional. Sin robots, sin Moodle, sin
expedientes — ninguno de esos sistemas se referencia en ningún módulo nuevo.

## II. Arquitectura modular basada en contratos

**Conforme.** Cinco agentes nuevos (`StudyIntentInterpreterAgent`,
`ResponseGeneratorAgent`, `PracticeQuestionAgent`, `SolutionNonDisclosureVerifierAgent`,
`CoherenceVerifierAgent`), cada uno con `AgentContractSchema` propio
(`agent_id`/`version`/`purpose`/`input_schema_ref`/`output_schema_ref`/`timeout_ms`/
`confidence_semantics`/`success_criteria`/`trace_fields`) documentado en
`contracts/self-study-agents.md`. Todos implementan el mismo protocolo `Executable`
(`AgentRequest`/`AgentResult`/`CancellationToken`) de la Feature 001, sin extenderlo.
Intercambian datos estructurados (dicts tipados por el contrato), nunca texto libre
entre agentes. Un único proceso, sin microservicios.

## III. Estado cognitivo explícito y memoria diferenciada

**Conforme.** Ningún dato de sesión vive en el contexto del LLM: cada turno construye
`GenerationRequest.evidence`/`concepts_addressed` explícitamente a partir de
`CognitiveState` y los reenvía completos en cada llamada (sin memoria "oculta" del
modelo entre turnos — confirmado por `test_sc005_context_continuity.py`, que verifica
que ningún `generation_call` reconstruible embebe texto íntegro de turnos anteriores).
`CognitiveState.mode` (campo ya existente de la Feature 001) es la fuente de verdad del
modo activo, actualizada exclusivamente vía `StatePatch` versionado
(`base_version`/`resulting_version`, research.md §6). `concepts_pending` (también campo
ya existente) se reutiliza para el mecanismo de progresión por pasos — ningún campo ni
tabla de estado nuevos. Categorías de memoria (`episodic`/`procedural`/`metacognitive`)
etiquetadas en cada `TraceEvent`. Ningún perfil longitudinal: `PracticeQuestion.
previous_questions` y `CoherenceVerifierAgent.prior_statements` se filtran/limitan
estrictamente por `session_id`/turno-inmediatamente-anterior (FR-011a,
`test_session_isolation.py`, `test_longitudinal_aggregation_forbidden.py`).

## IV. Separación entre recuperación, generación, decisión y verificación

**Conforme.** `ResponseGeneratorAgent`/`PracticeQuestionAgent` (rol `generator`) nunca
aprueban su propia salida. Cada propuesta pasa como mínimo por
`GroundingVerifierAgent`+`ConstitutionalControl` (Feature 001/002, sin cambios); las
preguntas de práctica pasan además por `SolutionNonDisclosureVerifierAgent`
(verificador independiente, contrato/umbral/traza propios — research.md §4); las
respuestas de los modos conversacionales pasan además por `CoherenceVerifierAgent`
(tercera implementación independiente de la técnica de solapamiento léxico, research.md
§5). Ningún verificador reutiliza código interno de otro (`SolutionNonDisclosureVerifierAgent`
y `CoherenceVerifierAgent` implementan su propia tokenización en su propio módulo, no
importan la función privada de `grounding_verifier_agent.py`). Los verificadores
producen veredictos estructurados (`approved`/`block`/`reformulate`), nunca
"reflexión verbal" del modelo.

## V. Fundamentación en materiales autorizados

**Conforme.** Nivel 0 (research.md §2): sin evidencia + conocimiento general
desactivado → el sistema reconoce la falta de información en vez de inventar
(`test_no_evidence_acknowledge_missing_info.py`). `general_knowledge_used` se deriva
única y exclusivamente del veredicto de `GroundingVerifierAgent`
(`no_verificable`+`general_knowledge_allowed=true`) — nunca una autodeclaración del
generador (T035, `test_general_knowledge_labeling.py`) — y se etiqueta explícitamente
en la respuesta HTTP y en el frontend (`Autoestudio.tsx`, indicador visible solo cuando
`general_knowledge_used=true`). `sources` conserva `document_id`/`document_version`/
`location_ref`/`fragment_text` en cada respuesta fundamentada.

## VI. Supervisión humana y gobernanza

**Conforme.** `SelfStudyActivityConfig` (`enabled_modes`/`summary_authorized`/
`practice_reveals_solution`) es configuración docente, inmutable tras el primer uso
(mismo patrón que `ActivityConfiguration`, research.md §7,
`test_self_study_config.py`). La purga (`purge_expired_self_study_data`) es de
invocación manual explícita — sin scheduler, sin automatización (T080/T081, research.md
§8). Ningún agente puede modificar `enabled_modes`/umbrales de verificación en tiempo
de ejecución — son leídos, nunca escritos, por los agentes.

## VII. Privacidad, minimización y accesibilidad

**Conforme.** Todo el procesamiento es local (Ollama, si se usa, corre en
`ORALIA_OLLAMA_BASE_URL` local por defecto; sin él, `DeterministicGenerationAdapter` no
requiere red en absoluto). Los participantes se identifican por `participant_code`
(seudónimo, ya establecido en la Feature 001, reutilizado sin cambios). Sin audio en
esta feature. `Autoestudio.tsx`: navegación por teclado nativa (elementos HTML
estándar), etiquetas (`<label htmlFor>` en todos los campos), `aria-live="polite"` en
el log de turnos, `role="alert"`/`role="status"`/`role="note"` para mensajes de
error/estado/indicador de conocimiento general, contraste verificado en
`styles.css` (T089) siguiendo el mismo patrón que `Participante.tsx`/`Tecnica.tsx`. Vía
textual completa — ninguna función de esta feature requiere voz.

## VIII. Trazabilidad y reproducibilidad

**Conforme.** Cada turno registra: modo activo y razón de validación
(`agents_selected.payload.mode_validation`, T057), agentes activados y su rol
(`activated_steps`), generador usado con modelo/parámetros/`fallback_used`
(`generation_call`), verificaciones realizadas y su combinación
(`verification_combined`, T068), intentos de no-revelación (`non_disclosure_check`),
incidencias de coherencia con acción de recuperación (`CoherenceIncident`), y el cierre
de sesión con su resumen (`study_session_summary`) — todo reconstruible vía
`GET /tecnica/sessions/{id}/study-trace` (T082/T084,
`test_sc006_trace_reconstruction_after_limit_close.py`). Ningún `payload` de
`TraceEvent` contiene cadena de razonamiento libre del modelo — solo veredictos,
decisiones estructuradas y códigos de error, conforme al patrón ya establecido en la
Feature 001 (`record_event`, reutilizado sin cambios).

## IX. Degradación controlada y límites de recursos

**Conforme.** Cadena de degradación documentada y probada en tres niveles
(research.md §1/§2): Ollama no disponible/timeout → `DeterministicGenerationAdapter`
dentro del mismo turno (`test_generation_ollama_unavailable.py`); fallo total de ambos
adaptadores → `execute_agency`/`SafeFallbackAgent` (Feature 001, sin cambios,
`test_generation_both_adapters_fail.py`), con re-chequeo constitucional explícito sobre
el texto de reserva. `fallo_agente`/`latencia_excesiva` se derivan directamente de
`AgencyOutcome.steps[].result.status` (nunca inventados por un verificador,
`test_coherence_conditions_fr015.py`). Cada agente declara `timeout_ms` en su
contrato; `run_with_deadline` (Feature 001, sin cambios) lo hace cumplir. Los controles
constitucionales se re-ejecutan explícitamente incluso en el camino degradado — nunca
se omiten por ahorro de recursos.

## X. Calidad, pruebas y evidencia

**Conforme, con una limitación documentada.** 239 pruebas (`-m "not ollama"`): 139 base
(Features 001+002, 0 regresiones — T095) + 100 nuevas de esta feature, cubriendo
contrato por agente nuevo (5), integración por modo (5/5 modos con escenario
diferenciado, SC-001), fallo/degradación/timeout/cancelación (Ollama caído, ambos
adaptadores caídos, conflicto de verificadores, modo no habilitado), datos
insuficientes (Nivel 0), bloqueo constitucional. **Limitación**: esta feature no
incluye por sí sola una comparación cuantitativa con un baseline monolítico — ese
ejercicio está explícitamente reservado a la Feature 6 ("Validación arquitectónica y
comparación con baseline monolítico") según el orden de features acumulativas de esta
misma constitución; no es un incumplimiento de esta feature sino trabajo diferido al
punto del roadmap donde corresponde.

## XI. Simplicidad evolutiva

**Conforme.** Sin frameworks de agentes, colas ni bases de datos nuevas — mismo SQLite/
FastAPI monolítico. `GenerationPort` es la única abstracción de inferencia nueva,
exactamente dos implementaciones sin envoltorio adicional (research.md §1, decisión
explícita documentada de no introducir un tercer adaptador "orquestador"). Única
dependencia nueva: `httpx` (ya presente como dependencia de desarrollo de FastAPI/
TestClient; promovida a dependencia de producción para `OllamaGenerationAdapter` —
alternativa más simple descartada: `requests` no soporta `async`/`await`, necesario para
no bloquear el bucle de eventos de FastAPI). `self_study_agency_composer.py` reutiliza
`execute_agency`/`run_with_deadline`/`apply_patch`/`record_event` (Feature 001) y
`MaterialRetrieverAgent`/`GroundingVerifierAgent` (Feature 002) **sin modificar ninguno
de esos ficheros** (FR-025, verificado — ningún `git diff`/edición tocó rutas de esas
features). El refactor `_finalize_turn`/`_run_practice_questions_turn` (T049) evita
duplicar ~90 líneas de persistencia de `Turn`/`GeneratedProposal`/`VerificationResult`/
`DialogueAction`/`StatePatch` entre las cinco composiciones de modo — reutilización
justificada, no abstracción prematura (ya había 2+ usos reales antes de extraerla).

## Conclusión

**Sin violaciones abiertas de principios MUST.** La única nota (Principio X) es un
trabajo explícitamente diferido a una feature posterior del propio roadmap
constitucional, no una omisión de esta feature. La Feature 003 puede considerarse lista
para el gate final (T096) desde la perspectiva de conformidad constitucional.
