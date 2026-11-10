# Tasks: Feature 005 — Gobierno docente y privacidad

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/ y constitución.
**Estado**: tareas nuevas de 005, ninguna heredada se considera implementada por existir código previo.
**Ejecución**: único escritor, sin commits. Pruebas antes de implementar cada bloque; actualizar evidencia medida.

## Phase 1: Setup and foundational

- [X] T001 Crear modelos y migración aditiva ActivityGovernance/SessionPrivacyPreference/SessionDeletionReceipt en src/oralia/infrastructure/db/models.py y src/oralia/infrastructure/db/migrations/versions/t005_governance.py. (FR-001 FR-016 FR-025)
- [X] T002 Añadir pruebas de contrato de autenticación/caducidad/ownership/origen/sin secreto en tests/contract/test_governance_access.py antes del guard. (FR-007 FR-008 FR-009 FR-010 FR-011)
- [X] T003 Implementar guard global con credenciales de instalación, tokens hasheados, caducidad y rechazo de origen en src/oralia/interfaces/api/deps/local_access.py; reemplazar auth_stub y registrar en src/oralia/interfaces/api/app.py. (FR-007 FR-008 FR-009 FR-010 FR-011)
- [X] T004 Adaptar explícitamente credenciales ficticias de tests/conftest.py, tests/integration/test_session_reconstruction_after_restart.py, test_defense_http_transaction_boundary.py y tests/e2e/run_self_study_api.py/playwright.config.ts sin bypass de producción. (FR-030 FR-032)

## Phase 2: US1 — versiones publicadas

Objetivo y prueba independiente: escenario US1 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T005 [US1] Añadir pruebas de clonación usada, concurrencia, material/modelo no disponible, retiro y aislamiento de versión en tests/integration/test_activity_governance.py. (FR-001 FR-002 FR-003 FR-004 FR-005 SC-001)
- [X] T006 [US1] Implementar creación/duplicación versionada y copia de configuraciones de modo/política en src/oralia/application/services/activity_governance_service.py. (FR-001 FR-002 FR-016)
- [X] T007 [US1] Exponer edición como nueva versión, catálogos, activación y retiro en src/oralia/interfaces/api/routers/governance.py. (FR-001 FR-002 FR-003 FR-006)
- [X] T008 [US1] Validar/preservar selección de versiones materiales y delegar estado de índice existente en src/oralia/application/services/activity_governance_service.py. (FR-004 FR-006)
- [X] T009 [US1] Conectar selección de modelos/composiciones disponibles al runtime sin editar contratos ni omitir controles en src/oralia/application/services/activity_governance_service.py y puntos de composición/generación existentes. (FR-005 FR-030)
- [X] T010 [US1] Rechazar nuevos inicios de borrador/retirada y resolver versión activa sin alterar sesiones antiguas en src/oralia/application/commands/start_session.py. (FR-002 FR-003)

## Phase 3: US2 — roles y propiedad

Objetivo y prueba independiente: escenario US2 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T011 [US2] Completar matriz de rutas históricas/nuevas, sesión ajena, logout, intentos denegados y expiración en tests/contract/test_governance_access.py. (FR-007 FR-008 FR-009 FR-010 FR-011 SC-002)
- [X] T012 [US2] Exponer login/logout/me y emitir cookie/credencial de propietario en src/oralia/interfaces/api/routers/governance.py y participante.py con respuestas no-store. (FR-007 FR-008 FR-012)
- [X] T013 [US2] Aplicar control real a rutas de configuración/materiales/trazas y conservar solo metadatos permitidos sin consentimiento en src/oralia/interfaces/api/routers/tecnica.py, materials.py, self_study.py y oral_defense.py. (FR-009 FR-017 FR-019)
- [X] T014 [US2] Actualizar cliente web para autenticación y propiedad de sesión sin localStorage ni secretos en apps/web/src/api/client.ts. (FR-007 FR-008 FR-009)
- [X] T015 [US2] Crear login/logout docente y ruta /gobierno con estados accesibles en apps/web/src/routes/Gobierno.tsx y apps/web/src/main.tsx. (FR-007 FR-029)

## Phase 4: US3 — participación y consentimiento

Objetivo y prueba independiente: escenario US3 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T016 [US3] Añadir matriz negativa/retención de scopes/plazo/cierre voluntario-automático/rollback y original-corrección en tests/integration/test_session_privacy.py. (FR-012 FR-013 FR-014 FR-015 FR-016 SC-003)
- [X] T017 [US3] Implementar preferencias previas y avisos con autorización/plazo de actividad en src/oralia/application/services/session_privacy_service.py. (FR-012 FR-013 FR-016)
- [X] T018 [US3] Integrar liquidación de privacidad en cierres ganador genérico/autoestudio, sin borrar estado activo ni alterar salida ya aprobada, en src/oralia/application/commands/end_session.py y end_study_session.py. (FR-013 FR-014 FR-030)
- [X] T019 [US3] Conservar consentimiento explícito existente de defensa y evitar escrituras tardías/resurrección tras eliminar en src/oralia/application/commands/end_defense_session.py y confirm_defense_transcript.py. (FR-014 FR-015 FR-030)
- [X] T020 [US3] Añadir aviso, elección independiente y eliminación propia por texto/teclado a apps/web/src/routes/Participante.tsx, Autoestudio.tsx y DefensaOral.tsx. (FR-012 FR-013 FR-014 FR-029)
- [X] T021 [US3] Reutilizar revisión/corrección de defensa y exponer revisión textual propia de otros modos en src/oralia/interfaces/api/routers/governance.py sin acceso ajeno. (FR-008 FR-015 FR-019)

## Phase 5: US4 — revisión consentida

Objetivo y prueba independiente: escenario US4 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T022 [US4] Probar vistas summary-only/transcript-only, ausencia de consentimiento, caducidad, eliminación y secretos sembrados en tests/contract/test_governance_review.py. (FR-017 FR-018 FR-019 SC-004)
- [X] T023 [US4] Implementar listado/detalle revisable con proyecciones explícitas por scope en src/oralia/application/services/session_privacy_service.py y routers/governance.py. (FR-017 FR-018 FR-019)
- [X] T024 [US4] Sanear consultas históricas de detalle/traza sin perder metadatos técnicos ni reexponer contenido eliminado en src/oralia/application/queries/get_session.py y reconstruct_session_trace.py. (FR-009 FR-018 FR-019 FR-030)
- [X] T025 [US4] Añadir revisión docente con secciones de original/corrección/respuestas/fuentes/verificaciones/incidencias/resumen a apps/web/src/routes/Gobierno.tsx. (FR-018 FR-029 SC-007)

## Phase 6: US5 — exportación

Objetivo y prueba independiente: escenario US5 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T026 [US5] Añadir pruebas JSON/Markdown, lote mixto, texto libre no revisado, alias y ausencia de secretos/audio/razonamiento en tests/contract/test_session_exports.py. (FR-020 FR-021 FR-022 FR-023 SC-004 SC-005)
- [X] T027 [US5] Implementar proyección cerrada, revalidación íntegra y alias por lote en src/oralia/application/services/session_export_service.py. (FR-020 FR-021 FR-022 FR-023)
- [X] T028 [US5] Exponer descarga efímera no-store JSON/Markdown y límites del lote en src/oralia/interfaces/api/routers/governance.py. (FR-020 FR-021 FR-023)
- [X] T029 [US5] Añadir revisión explícita de texto libre, selección de lote y descarga/revocación de Blob en apps/web/src/routes/Gobierno.tsx. (FR-020 FR-022 FR-029 SC-005)

## Phase 7: US6 — eliminación y purga

Objetivo y prueba independiente: escenario US6 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T030 [US6] Probar eliminación completa/recibo/idempotencia, sesión activa, rollback, expiración y aislamiento de materiales/sesiones en tests/integration/test_session_privacy.py. (FR-024 FR-025 FR-026 FR-027 SC-006)
- [X] T031 [US6] Implementar borrado de todas las proyecciones propias y recibo sin contenido, con control propietario/docente, en src/oralia/application/services/session_privacy_service.py. (FR-024 FR-025 FR-027)
- [X] T032 [US6] Implementar purga manual y exclusión de eliminadas/expiradas de revisión/exportación en src/oralia/interfaces/api/routers/governance.py y servicios de privacidad/exportación. (FR-017 FR-021 FR-026)
- [X] T033 [US6] Añadir confirmación accesible de eliminación y recibo verificable a apps/web/src/routes/Gobierno.tsx y cliente participante. (FR-024 FR-025 FR-029 SC-006)

## Phase 8: US7 — sistema y accesibilidad

Objetivo y prueba independiente: escenario US7 de spec.md; completar flujo y negativos antes del siguiente bloque.

- [X] T034 [US7] Probar métricas agregadas/faltantes y catálogo sin notas/perfiles en tests/contract/test_governance_metrics.py. (FR-006 FR-028 FR-031 SC-008)
- [X] T035 [US7] Implementar métricas agregadas disponibles y faltantes explícitos en src/oralia/interfaces/api/routers/governance.py. (FR-028 FR-031)
- [X] T036 [US7] Completar formulario de configuración, modelos/agentes/materiales y estados técnicos en apps/web/src/routes/Gobierno.tsx y styles.css. (FR-001 FR-004 FR-005 FR-006 FR-029)
- [X] T037 [US7] Añadir recorrido Playwright real de login, versión activa, participante/consentimiento, revisión, exportación, eliminación, logout y denegación en tests/e2e/test_governance_flow.spec.ts. (FR-029 FR-032 SC-007)

## Phase 9: Final quality gates

- [X] T038 Ejecutar suite determinista global y registrar cifras/logs reales en specs/005-teacher-governance/validation-backend.json. (FR-030 FR-032)
- [X] T039 Ejecutar frontend build/lint y Playwright completo; registrar en specs/005-teacher-governance/validation-frontend.json. (FR-029 FR-030 FR-032 SC-007)
- [X] T040 Ejecutar Black de inventario tocado y Ruff estructural con Counter contra baseline durable en specs/005-teacher-governance/ruff-validation.json. (FR-030 FR-032)
- [X] T041 Probar migración limpia y desde t004 en bases temporales, DDL histórico y cleanup en specs/005-teacher-governance/validation-migrations.json. (FR-032)
- [X] T042 Ejecutar quickstart real y actualizar límites/evidencia en specs/005-teacher-governance/quickstart.md. (FR-032 SC-001 SC-002 SC-003 SC-004 SC-005 SC-006 SC-007 SC-008)
- [X] T043 Revisar 11 principios y checklists con evidencia en specs/005-teacher-governance/implementation-evidence.md. (FR-030 FR-031 FR-032)
- [X] T044 Ejecutar speckit-analyze de solo lectura y archivar resultado sin hallazgos críticos ni cobertura faltante en specs/005-teacher-governance/analysis-report.md. (FR-032)
- [X] T045 Ejecutar speckit-converge contra código/pruebas/documentos; añadir solo brechas reales al final de specs/005-teacher-governance/tasks.md y repetir implementación hasta cero. (FR-032)
- [X] T046 Consolidar tabla completa de tareas, cobertura y límites medidos en specs/005-teacher-governance/implementation-evidence.md; no iniciar 006 antes del cierre. (FR-032)

## Dependencies and implementation strategy

Setup → guard de acceso → US1/US2 → privacidad común US3 → revisión US4 → exportación US5 y borrado US6 → UI/métricas US7 → puertas finales. Los cambios en archivos compartidos se secuencian. Pruebas de acceso, versiones y exportación pueden redactarse independientemente; no se delegan escritores ni se ejecutan agentes en paralelo.

MVP primero: acceso real y versión publicada, después todos los flujos restantes antes de declarar cierre. No hay tareas opcionales encubiertas; ninguna tarea de voz real bloquea esta feature.
