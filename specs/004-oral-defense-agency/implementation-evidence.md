# Evidencia de implementación — Feature 004

Fecha: 2026-10-17. Workspace compartido sin Git; no se realizaron commits.

Estado: 117/117 tareas obligatorias; 117/119 totales. T094/T118 son opcionales y permanecen sin marcar porque la voz real se omitió.

## Pruebas y puertas medidas

| Puerta | Resultado | Evidencia |
|---|---|---|
| Deterministas | 766 passed, 3 deselected, 1 warning in 84.48s (0:01:24) | [Log](validation-deterministic.log) |
| Voz real opcional | 2 skipped, 767 deselected, 1 warning in 0.93s | [Log](validation-speech.log) |
| Black | 71 files would be left unchanged. | [Inventario Python](python-files.json), [log](validation-black.log) |
| Ruff estructural | 11 heredados; 0 nuevos | [JSON](ruff-validation.json) |
| Build TypeScript/Vite | exit 0 | [Log](validation-build.log) |
| ESLint | exit 0; 0 errores, 1 warning en Tecnica.tsx:286 | [Log](validation-lint.log) |
| Playwright completo | 9 passed (25.6s) | [Log](validation-playwright.log) |
| Migraciones | limpia y upgrade desde t114_retention_auth PASS; 28 tablas de aplicación más alembic_version; head t004_oral_defense; cuatro tablas añadidas; DDL previo idéntico | [JSON](validation-migrations.json) |
| Lock | 151 paquetes resueltos; check offline PASS | [Log](validation-lock.log) |

Ruff se compara por `(ruta, código, mensaje)` con multiplicidad mediante `Counter`, contra `specs/001-core-cognitive-runtime/t090-ruff-baseline.json`; no se comparan solo totales. El warning ESLint en Tecnica.tsx ya se observó en el primer lint de esta conversación antes de editar frontend; ese archivo no fue modificado. El warning Python es Starlette/httpx, también observado en la focal inicial.

## Implementación y archivos

El núcleo usa MaterialRetrieverAgent, FollowUpQuestionAgent, PracticeQuestionAgent para la inicial sin banco, GroundingVerifierAgent y CoherenceVerifierAgent. La resolución conserva el grounding prioritario, una regeneración como máximo, contradicción cognitiva, cambio de tema autorizado y veto de duplicados literales en toda la sesión. El estado usa los campos existentes y StatePatch.

T090 autoriza preguntas, aclaraciones, degradación y resumen con snapshot confiable y catálogo exacto. La propuesta y el veredicto del resumen no sobrescriben el turno anterior; el borrado por scope/expiración retira su texto y conserva solo metadatos. T150 mantiene un único ganador de cierre y efectos en la transacción exterior. Los commits de los endpoints de defensa y el inicio de sesión terminan antes de enviar la respuesta.

Los turnos textuales y confirmaciones de voz transportan la elección explícita de conservación hasta el cierre automático ganador. Un endpoint de revisión por sesión muestra turnos, originales y correcciones; el cierre voluntario exige revisar y confirmar.

La voz permanece fuera de la agencia cognitiva: confirmación previa, revisiones tardías como turnos nuevos, WAV literal y replay efímero, worker global acotado, límites de entrada y cierre de spool incluso ante timeout/cancelación. La UI permite pausa, ritmo, repetición, revisión/corrección, continuidad textual y elección de conservación.

La eliminación por consentimiento o caducidad también retira copias de contenido en turnos, propuestas, estado, parches, mensajes y trazas, únicamente para la sesión terminal de defensa. Retención exige plazo finito; STT/TTS tardíos se descartan tras el cierre. No se alteran filas de otras sesiones.

Inventario Python completo: [python-files.json](python-files.json). Frontend: `DefensaOral.tsx`, `client.ts`, `main.tsx`, `styles.css`; pruebas Playwright de defensa y ajustes del harness compartido. La fixture WAV es voz sintética, sin datos de participantes.

## Integraciones históricas revisadas — T093

| Archivo | Extensión o corrección | Validación |
|---|---|---|
| [models.py](../../src/oralia/infrastructure/db/models.py) | Cuatro clases añadidas; ninguna tabla histórica alterada | Suite completa y Playwright |
| [generation_port.py](../../src/oralia/infrastructure/generation/generation_port.py) | Propósito repregunta aditivo | Suite completa y Playwright |
| [deterministic_adapter.py](../../src/oralia/infrastructure/generation/deterministic_adapter.py) | Rama repregunta extractiva; datos del tema fuera de instrucciones | Suite completa y Playwright |
| [output_template_catalog.py](../../src/oralia/domain/policies/output_template_catalog.py) | Identidades exactas de plantillas de defensa | Suite completa y Playwright |
| [constitutional_control.py](../../src/oralia/domain/policies/constitutional_control.py) | Patrones personales adicionales bajo academic_decision; términos técnicos permitidos | Suite completa y Playwright |
| [app.py](../../src/oralia/interfaces/api/app.py) | Registro aditivo de routers de defensa | Suite completa y Playwright |
| [participante.py](../../src/oralia/interfaces/api/routers/participante.py) | Commit antes de responder; inicio, turno y cierre | Suite completa y Playwright |
| [tecnica.py](../../src/oralia/interfaces/api/routers/tecnica.py) | Commit de configuración/actividad antes de publicar identificadores | Suite completa y Playwright |
| [materials.py](../../src/oralia/interfaces/api/routers/materials.py) | Commit de carga/activación antes de continuar la recuperación | Suite completa y Playwright |
| [self_study.py](../../src/oralia/interfaces/api/routers/self_study.py) | Frontera transaccional de autoestudio antes de respuesta | Suite completa y Playwright |
| [client.ts](../../apps/web/src/api/client.ts) | Contratos de defensa y Blob efímero | Suite completa y Playwright |
| [main.tsx](../../apps/web/src/main.tsx) | Ruta /defensa explícita | Suite completa y Playwright |
| [styles.css](../../apps/web/src/styles.css) | Accesibilidad y marcas de baja confianza | Suite completa y Playwright |
| [playwright.config.ts](../../tests/e2e/playwright.config.ts) | Ejecución serial acorde con el único bloqueo de sesión activa | Suite completa y Playwright |
| [test_scenario_a.spec.ts](../../tests/e2e/test_scenario_a.spec.ts) | Fixtures de curso/retención/política válidas y selección por sesión exacta | Suite completa y Playwright |
| [run_self_study_api.py](../../tests/e2e/run_self_study_api.py) | Ollama real excluido del harness determinista y vector store de pruebas aislado | Suite completa y Playwright |

## Revisión constitucional

| Principio | Resultado | Evidencia observable |
|---|---|---|
| I. Finalidad y límites | PASS | Bloqueo de notas, aprobado/suspenso y caracterización personal; matrix/no_evaluation/summary_authorization |
| II. Contratos | PASS | Puertos cerrados e inmutables; contract/test_defense_speech_ports y test_followup_question_agent |
| III. Estado y memoria | PASS | CognitiveState sin campos nuevos; current_input/participant_response correctos; StatePatch en voice_lifecycle |
| IV. Separación de responsabilidades | PASS | Recuperador, generador, verificadores y T090 independientes; dialogue_contract y matriz de autorización |
| V. Materiales autorizados | PASS | MaterialRetrieverAgent original y sus regresiones; initial_material_question y recorrido HTTP con material activado |
| VI. Supervisión | PASS | Config inmutable después de iniciar, consentimiento explícito y purga manual; config/end_consent/retention_and_purge |
| VII. Privacidad y accesibilidad | PASS | Spools cerrados, scopes sin audio, borrado inmediato y controles de teclado; rolled_spool/retention/Playwright |
| VIII. Trazabilidad | PASS | agent_execution/generation_call/verification_combined/followup/turn_completed, referencias y versiones; full_session y endpoint trace |
| IX. Degradación y límites | PASS | Reserva original y SafeFallbackAgent; límites exactos; worker_request_lifetime y bloqueo/cancelación |
| X. Calidad y evidencia | PASS | Contratos, fallos, integración, migraciones y navegador reales; resultados y logs enlazados |
| XI. Simplicidad evolutiva | PASS | Un nuevo agente cognitivo, dos puertos de voz, mismo núcleo y cuatro tablas nuevas; sin servicios distribuidos |

## Tabla T001–T119

Las pruebas se agruparon por archivos y escenarios compartidos; la tabla conserva la numeración histórica. La mera existencia de un archivo no sustituye los resultados enlazados.

| Tarea | Estado | Evidencia agrupada |
|---|---|---|
| T001 | [X] | [pyproject.toml](../../pyproject.toml), [uv.lock](../../uv.lock) |
| T002 | [X] | [__init__.py](../../src/oralia/infrastructure/speech/__init__.py) |
| T003 | [X] | [__init__.py](../../tests/speech/__init__.py) |
| T004 | [X] | [models.py](../../src/oralia/infrastructure/db/models.py), [validation-migrations.json](../../specs/004-oral-defense-agency/validation-migrations.json) |
| T005 | [X] | [t004_oral_defense_tables.py](../../src/oralia/infrastructure/db/migrations/versions/t004_oral_defense_tables.py) |
| T006 | [X] | [test_defense_config.py](../../tests/contract/test_defense_config.py), [test_defense_policy_and_catalog.py](../../tests/unit/test_defense_policy_and_catalog.py) |
| T007 | [X] | [test_defense_config.py](../../tests/contract/test_defense_config.py), [test_defense_policy_and_catalog.py](../../tests/unit/test_defense_policy_and_catalog.py) |
| T008 | [X] | [test_defense_config.py](../../tests/contract/test_defense_config.py), [test_defense_policy_and_catalog.py](../../tests/unit/test_defense_policy_and_catalog.py) |
| T009 | [X] | [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T010 | [X] | [test_defense_turns_endpoint.py](../../tests/contract/test_defense_turns_endpoint.py), [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts) |
| T011 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T012 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T013 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T014 | [X] | [test_defense_dialogue_contract.py](../../tests/integration/test_defense_dialogue_contract.py), [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T015 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T016 | [X] | [test_defense_dialogue_contract.py](../../tests/integration/test_defense_dialogue_contract.py), [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T017 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T018 | [X] | [test_defense_dialogue_contract.py](../../tests/integration/test_defense_dialogue_contract.py), [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T019 | [X] | [test_defense_generation_degradation.py](../../tests/failure/test_defense_generation_degradation.py) |
| T020 | [X] | [test_defense_generation_degradation.py](../../tests/failure/test_defense_generation_degradation.py) |
| T021 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T022 | [X] | [test_defense_relevance_structural.py](../../tests/unit/test_defense_relevance_structural.py) |
| T023 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T024 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T025 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T026 | [X] | [generation_port.py](../../src/oralia/infrastructure/generation/generation_port.py), [validation-deterministic.log](../../specs/004-oral-defense-agency/validation-deterministic.log) |
| T027 | [X] | [generation_port.py](../../src/oralia/infrastructure/generation/generation_port.py), [validation-deterministic.log](../../specs/004-oral-defense-agency/validation-deterministic.log) |
| T028 | [X] | [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T029 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T030 | [X] | [test_defense_generation_degradation.py](../../tests/failure/test_defense_generation_degradation.py), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T031 | [X] | [test_defense_turns_endpoint.py](../../tests/contract/test_defense_turns_endpoint.py), [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts) |
| T032 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T033 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T034 | [X] | [test_defense_text_full_session.py](../../tests/integration/test_defense_text_full_session.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T035 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log) |
| T036 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T037 | [X] | [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py), [test_defense_no_evaluation.py](../../tests/failure/test_defense_no_evaluation.py) |
| T038 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T039 | [X] | [test_defense_speech_ports.py](../../tests/contract/test_defense_speech_ports.py) |
| T040 | [X] | [test_defense_speech_ports.py](../../tests/contract/test_defense_speech_ports.py) |
| T041 | [X] | [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py), [test_defense_voice_and_speech.py](../../tests/contract/test_defense_voice_and_speech.py) |
| T042 | [X] | [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py), [test_defense_voice_and_speech.py](../../tests/contract/test_defense_voice_and_speech.py) |
| T043 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T044 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T045 | [X] | [test_defense_correction_not_retroactive.py](../../tests/integration/test_defense_correction_not_retroactive.py) |
| T046 | [X] | [test_defense_rolled_spool_lifecycle.py](../../tests/contract/test_defense_rolled_spool_lifecycle.py), [test_defense_voice_upload_limits.py](../../tests/contract/test_defense_voice_upload_limits.py) |
| T047 | [X] | [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py), [test_defense_voice_and_speech.py](../../tests/contract/test_defense_voice_and_speech.py) |
| T048 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T049 | [X] | [test_faster_whisper_real.py](../../tests/speech/test_faster_whisper_real.py) |
| T050 | [X] | [test_piper_real.py](../../tests/speech/test_piper_real.py) |
| T051 | [X] | [test_defense_speech_ports.py](../../tests/contract/test_defense_speech_ports.py) |
| T052 | [X] | [test_defense_speech_ports.py](../../tests/contract/test_defense_speech_ports.py) |
| T053 | [X] | [config.py](../../src/oralia/infrastructure/speech/config.py), [test_defense_speech_timeout_late_results.py](../../tests/failure/test_defense_speech_timeout_late_results.py) |
| T054 | [X] | [config.py](../../src/oralia/infrastructure/speech/config.py), [test_defense_speech_timeout_late_results.py](../../tests/failure/test_defense_speech_timeout_late_results.py) |
| T055 | [X] | [config.py](../../src/oralia/infrastructure/speech/config.py), [test_defense_speech_timeout_late_results.py](../../tests/failure/test_defense_speech_timeout_late_results.py) |
| T056 | [X] | [test_defense_speech_ports.py](../../tests/contract/test_defense_speech_ports.py) |
| T057 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T058 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T059 | [X] | [test_defense_turns_endpoint.py](../../tests/contract/test_defense_turns_endpoint.py), [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts) |
| T060 | [X] | [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py), [test_defense_voice_and_speech.py](../../tests/contract/test_defense_voice_and_speech.py) |
| T061 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log) |
| T062 | [X] | [test_defense_speech_exceptions.py](../../tests/failure/test_defense_speech_exceptions.py) |
| T063 | [X] | [test_defense_speech_exceptions.py](../../tests/failure/test_defense_speech_exceptions.py) |
| T064 | [X] | [test_defense_speech_exceptions.py](../../tests/failure/test_defense_speech_exceptions.py) |
| T065 | [X] | [test_defense_speech_exceptions.py](../../tests/failure/test_defense_speech_exceptions.py) |
| T066 | [X] | [test_defense_speech_exceptions.py](../../tests/failure/test_defense_speech_exceptions.py) |
| T067 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T068 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T069 | [X] | [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T070 | [X] | [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T071 | [X] | [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T072 | [X] | [test_defense_voice_lifecycle.py](../../tests/integration/test_defense_voice_lifecycle.py), [test_followup_question_agent.py](../../tests/contract/test_followup_question_agent.py) |
| T073 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log) |
| T074 | [X] | [test_defense_session_isolation.py](../../tests/integration/test_defense_session_isolation.py) |
| T075 | [X] | [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T076 | [X] | [test_defense_end_consent.py](../../tests/contract/test_defense_end_consent.py) |
| T077 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py) |
| T078 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py) |
| T079 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py) |
| T080 | [X] | [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T081 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py) |
| T082 | [X] | [test_defense_end_consent.py](../../tests/contract/test_defense_end_consent.py) |
| T083 | [X] | [test_defense_session_isolation.py](../../tests/integration/test_defense_session_isolation.py) |
| T084 | [X] | [test_defense_remaining_boundaries.py](../../tests/integration/test_defense_remaining_boundaries.py) |
| T085 | [X] | [test_defense_end_consent.py](../../tests/contract/test_defense_end_consent.py), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T086 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py) |
| T087 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py) |
| T088 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T089 | [X] | [validation-backend.json](../../specs/004-oral-defense-agency/validation-backend.json), [validation-frontend.json](../../specs/004-oral-defense-agency/validation-frontend.json) |
| T090 | [X] | [ruff-validation.json](../../specs/004-oral-defense-agency/ruff-validation.json), [validation-black.log](../../specs/004-oral-defense-agency/validation-black.log) |
| T091 | [X] | [quickstart.md](../../specs/004-oral-defense-agency/quickstart.md), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T092 | [X] | [implementation-evidence.md#revisión-constitucional](../../specs/004-oral-defense-agency/implementation-evidence.md#revisión-constitucional) |
| T093 | [X] | [validation-backend.json](../../specs/004-oral-defense-agency/validation-backend.json), [validation-frontend.json](../../specs/004-oral-defense-agency/validation-frontend.json) |
| T094 | Opcional: omitida | [validation-speech.log](../../specs/004-oral-defense-agency/validation-speech.log) |
| T095 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T096 | [X] | [test_defense_config.py](../../tests/contract/test_defense_config.py), [test_defense_policy_and_catalog.py](../../tests/unit/test_defense_policy_and_catalog.py) |
| T097 | [X] | [test_defense_policy_and_catalog.py](../../tests/unit/test_defense_policy_and_catalog.py) |
| T098 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T099 | [X] | [test_defense_output_authorization_matrix.py](../../tests/contract/test_defense_output_authorization_matrix.py), [test_defense_summary_authorization.py](../../tests/integration/test_defense_summary_authorization.py) |
| T100 | [X] | [test_defense_turns_endpoint.py](../../tests/contract/test_defense_turns_endpoint.py), [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T101 | [X] | [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py), [test_defense_voice_and_speech.py](../../tests/contract/test_defense_voice_and_speech.py) |
| T102 | [X] | [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py), [test_defense_voice_and_speech.py](../../tests/contract/test_defense_voice_and_speech.py) |
| T103 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log) |
| T104 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log) |
| T105 | [X] | [test_defense_route.spec.ts](../../tests/e2e/test_defense_route.spec.ts), [validation-build.log](../../specs/004-oral-defense-agency/validation-build.log), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T106 | [X] | [test_blocking_speech_worker.py](../../tests/unit/test_blocking_speech_worker.py) |
| T107 | [X] | [test_blocking_speech_worker.py](../../tests/unit/test_blocking_speech_worker.py) |
| T108 | [X] | [test_defense_rolled_spool_lifecycle.py](../../tests/contract/test_defense_rolled_spool_lifecycle.py), [test_defense_voice_upload_limits.py](../../tests/contract/test_defense_voice_upload_limits.py) |
| T109 | [X] | [test_defense_rolled_spool_lifecycle.py](../../tests/contract/test_defense_rolled_spool_lifecycle.py), [test_defense_voice_upload_limits.py](../../tests/contract/test_defense_voice_upload_limits.py) |
| T110 | [X] | [config.py](../../src/oralia/infrastructure/speech/config.py), [test_defense_speech_timeout_late_results.py](../../tests/failure/test_defense_speech_timeout_late_results.py) |
| T111 | [X] | [config.py](../../src/oralia/infrastructure/speech/config.py), [test_defense_speech_timeout_late_results.py](../../tests/failure/test_defense_speech_timeout_late_results.py) |
| T112 | [X] | [test_defense_worker_request_lifetime.py](../../tests/failure/test_defense_worker_request_lifetime.py), [test_defense_speech_timeout_late_results.py](../../tests/failure/test_defense_speech_timeout_late_results.py), [test_defense_stt_after_close.py](../../tests/integration/test_defense_stt_after_close.py), [test_defense_speech_endpoint.py](../../tests/contract/test_defense_speech_endpoint.py) |
| T113 | [X] | [test_defense_close_transition_outcome.py](../../tests/integration/test_defense_close_transition_outcome.py) |
| T114 | [X] | [test_defense_close_transition_outcome.py](../../tests/integration/test_defense_close_transition_outcome.py), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T115 | [X] | [test_defense_retention_and_purge.py](../../tests/integration/test_defense_retention_and_purge.py), [test_defense_retention_copies.py](../../tests/integration/test_defense_retention_copies.py), [test_defense_retention_requires_finite_policy.py](../../tests/contract/test_defense_retention_requires_finite_policy.py), [defense_retention_service.py](../../src/oralia/application/services/defense_retention_service.py), [test_defense_automatic_close_consent.py](../../tests/contract/test_defense_automatic_close_consent.py), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T116 | [X] | [quickstart.md](../../specs/004-oral-defense-agency/quickstart.md), [test_defense_full_session.spec.ts](../../tests/e2e/test_defense_full_session.spec.ts) |
| T117 | [X] | [validation-backend.json](../../specs/004-oral-defense-agency/validation-backend.json), [validation-frontend.json](../../specs/004-oral-defense-agency/validation-frontend.json) |
| T118 | Opcional: omitida | [validation-speech.log](../../specs/004-oral-defense-agency/validation-speech.log) |
| T119 | [X] | [requirement-coverage.md](../../specs/004-oral-defense-agency/requirement-coverage.md), [checklists](../../specs/004-oral-defense-agency/checklists) |

## Cobertura, checklists y límites

[Cobertura explícita](requirement-coverage.md): 61 requisitos/criterios con tareas. Los ocho checklists conservan 104 ítems; la revalidación de implementación se añade con enlaces a archivos y pruebas. El análisis SpecKit final revisa contradicciones sin alterar la constitución.

Las dos pruebas reales no se ejecutaron contra modelos: ORALIA_STT_MODEL y ORALIA_TTS_VOICE no están configurados; faster-whisper y piper-tts no están instalados. El lock opcional sí resuelve faster-whisper 1.2.1 y piper-tts 1.8.0. No se afirma calidad, latencia ni compatibilidad real de esos modelos a partir de los dobles deterministas. No se descargaron modelos ni se modificó oralia.db durante esta validación.
