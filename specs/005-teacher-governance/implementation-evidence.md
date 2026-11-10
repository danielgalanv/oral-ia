# Evidencia de implementación — Feature 005



Estado: **cerrada y convergida; 46/46 tareas**. Sin commits, sin agentes paralelos.

Constitución 1.0.0 intacta; no se modifican informes de Feature 004.



## Resultados medidos



- Suite determinista: **818 passed, 3 deselected**, una advertencia Starlette/httpx.

- Voz real: **2 skipped**, no cuentan como aprobadas; sin modelos/dependencias configurados.

- Black: **104 archivos sin cambios**; inventario acumulado de integración, no 104 archivos nuevos.

- Ruff: **0 nuevos**, 10 heredados frente al baseline durable 001, comparación Counter por ruta/código/mensaje.

- Lock offline correcto. Build y lint correctos; lint conserva un warning preexistente en Tecnica.tsx.

- Playwright: 10 flujos reales aprobados, incluido gobierno por Enter/Espacio; log durable y JSON frontend anexos.

- Migraciones: 2 pruebas aprobadas, limpia y actualización desde t004 hasta t005; 31 tablas de aplicación, DDL anterior intacto, procedencia e índice único comprobados. Bases temporales.



Fuentes: validation-backend.json, validation-frontend.json, validation-migrations.json,

ruff-validation.json y validation-*.log. El primer intento capturado de Playwright falló

al localizar Chromium; ejecución directa posterior pasa. Se conserva el resultado final

medido, sin atribuir el fallo de entorno a un flujo de aplicación.



## Cambios y compatibilidad



Guard global con contraseña solo para login, tokens temporales hasheados en memoria,

HttpOnly/SameSite y no-store, propiedad secreta de sesión, localhost/origen y cierre de

acceso. Rutas históricas administrativas ahora requieren login real; las fixtures usan

credenciales ficticias y emisión normal de tokens, sin bypass de producción.



Configuraciones: borrador/activa/retirada, duplicación/sucesores inmutables y procedencia,

materiales por versión, modelo fijado y composiciones completas. Pruebas ejercitan el

compositor real y concurrencia de publicación. Versiones históricas se fijan al primer

inicio bajo 005: no se inventa el modelo que usaron previamente.



Privacidad: elección actual llega al único cierre ganador, automática o voluntaria.

Se intersecta con scopes, plazo y acceso de política. participant_only bloquea al docente.

Borrado incluye turnos, originales, correcciones, mensajes, propuestas, grounding,

estado y trazas; quedan filas estructurales sin contenido y recibo mínimo. Rollback

revierte cierre, consentimiento, preferencia y lock. La defensa conserva su contrato 004.

Pruebas históricas de negativos ahora comprueban contenido vacío sin perder versiones,

veredictos y metadatos T090/T150; no se eliminan regresiones para ocultar fallos.



Revisión/exportación usan proyecciones cerradas, verificación actual de permiso y scopes,

lote completo o fallo, alias e inclusión de texto libre solo tras revisión humana. JSON

y Markdown se generan en memoria; Blob del navegador se revoca. Se eliminan identificadores

conocidos también del texto; no se promete detectar todos los datos personales.



Interfaz /gobierno completa y controles textuales de privacidad en los tres modos. Catálogo

material/índice sin inicialización implícita; integrity_verified=false es una limitación

explícita. Se reutiliza reconstrucción de índice existente. Métricas agregadas con faltantes,

sin desglose individual ni inferencias académicas.



## Escenarios y cobertura



40/40 requisitos (32 FR, 8 SC) enlazados a tareas en requirement-coverage.md. US1–US7

cubiertos por test_activity_governance, test_governance_access, test_session_privacy,

test_governance_review, test_session_exports, test_governance_metrics y el recorrido E2E.

Cada historia incluye positivos y denegaciones; privacidad cubre scopes y cierres,

exportación lote mixto y secretos sembrados, borrado/purga aislamiento e idempotencia.

Cuatro checklists de requisitos: 37/37 resueltos; no equivalen a pruebas de producto.



## Constitución



- I: Vistas descriptivas; sin notas ni perfiles.

- II: Servicios separados, contratos existentes y T090 conservados.

- III: Estado/parches versionados; borrado sanea contenido y mantiene solo estructura operativa.

- IV: Selección de modelo llega al compositor real; controles completos obligatorios.

- V: Documento/versión fijados y filtro tanto en recuperación como en cola.

- VI: Login real, publicación manual, sucesores y procedencia; índice único de activa.

- VII: Roles/propiedad, scopes/plazo/acceso, texto, eliminación y exportación revisada.

- VIII: Fuentes/veredictos/traza saneada y recibos; sin secretos ni razonamiento privado.

- IX: TTL, lotes 1–100, capacidad y límite de login, rollback y cierre ganador.

- X: Regresión global, contratos, integración, fallo, navegador y migraciones.

- XI: Monolito local, sin nuevas dependencias ni servicios externos.



## Límites



Una instalación y una sesión interactiva; tokens se invalidan con reinicio y caducan

(1h docente, 24h propietario), sin recuperación institucional. Sin datos reales, nube,

SSO ni descargas de modelos. El permiso de conservar no sustituye consentimiento.

No se ha medido rendimiento de hardware ni utilidad con personas en 005: pertenece a006.

La lectura de versión del índice no certifica integridad. Voz real permanece opcional.



## Registro completo de tareas



| Tarea | Entrega verificada |

|---|---|

| T001 | Crear modelos y migración aditiva ActivityGovernance/SessionPrivacyPreference/SessionDeletionReceipt en src/oralia/infrastructure/db/models.py y src/oralia/infrastructure/db/migrations/versions/t005_governance.py. |

| T002 | Añadir pruebas de contrato de autenticación/caducidad/ownership/origen/sin secreto en tests/contract/test_governance_access.py antes del guard. |

| T003 | Implementar guard global con credenciales de instalación, tokens hasheados, caducidad y rechazo de origen en src/oralia/interfaces/api/deps/local_access.py; reemplazar auth_stub y registrar en src/oralia/interfaces/api/app.py. |

| T004 | Adaptar explícitamente credenciales ficticias de tests/conftest.py, tests/integration/test_session_reconstruction_after_restart.py, test_defense_http_transaction_boundary.py y tests/e2e/run_self_study_api.py/playwright.config.ts sin bypass de producción. |

| T005 | [US1] Añadir pruebas de clonación usada, concurrencia, material/modelo no disponible, retiro y aislamiento de versión en tests/integration/test_activity_governance.py. |

| T006 | [US1] Implementar creación/duplicación versionada y copia de configuraciones de modo/política en src/oralia/application/services/activity_governance_service.py. |

| T007 | [US1] Exponer edición como nueva versión, catálogos, activación y retiro en src/oralia/interfaces/api/routers/governance.py. |

| T008 | [US1] Validar/preservar selección de versiones materiales y delegar estado de índice existente en src/oralia/application/services/activity_governance_service.py. |

| T009 | [US1] Conectar selección de modelos/composiciones disponibles al runtime sin editar contratos ni omitir controles en src/oralia/application/services/activity_governance_service.py y puntos de composición/generación existentes. |

| T010 | [US1] Rechazar nuevos inicios de borrador/retirada y resolver versión activa sin alterar sesiones antiguas en src/oralia/application/commands/start_session.py. |

| T011 | [US2] Completar matriz de rutas históricas/nuevas, sesión ajena, logout, intentos denegados y expiración en tests/contract/test_governance_access.py. |

| T012 | [US2] Exponer login/logout/me y emitir cookie/credencial de propietario en src/oralia/interfaces/api/routers/governance.py y participante.py con respuestas no-store. |

| T013 | [US2] Aplicar control real a rutas de configuración/materiales/trazas y conservar solo metadatos permitidos sin consentimiento en src/oralia/interfaces/api/routers/tecnica.py, materials.py, self_study.py y oral_defense.py. |

| T014 | [US2] Actualizar cliente web para autenticación y propiedad de sesión sin localStorage ni secretos en apps/web/src/api/client.ts. |

| T015 | [US2] Crear login/logout docente y ruta /gobierno con estados accesibles en apps/web/src/routes/Gobierno.tsx y apps/web/src/main.tsx. |

| T016 | [US3] Añadir matriz negativa/retención de scopes/plazo/cierre voluntario-automático/rollback y original-corrección en tests/integration/test_session_privacy.py. |

| T017 | [US3] Implementar preferencias previas y avisos con autorización/plazo de actividad en src/oralia/application/services/session_privacy_service.py. |

| T018 | [US3] Integrar liquidación de privacidad en cierres ganador genérico/autoestudio, sin borrar estado activo ni alterar salida ya aprobada, en src/oralia/application/commands/end_session.py y end_study_session.py. |

| T019 | [US3] Conservar consentimiento explícito existente de defensa y evitar escrituras tardías/resurrección tras eliminar en src/oralia/application/commands/end_defense_session.py y confirm_defense_transcript.py. |

| T020 | [US3] Añadir aviso, elección independiente y eliminación propia por texto/teclado a apps/web/src/routes/Participante.tsx, Autoestudio.tsx y DefensaOral.tsx. |

| T021 | [US3] Reutilizar revisión/corrección de defensa y exponer revisión textual propia de otros modos en src/oralia/interfaces/api/routers/governance.py sin acceso ajeno. |

| T022 | [US4] Probar vistas summary-only/transcript-only, ausencia de consentimiento, caducidad, eliminación y secretos sembrados en tests/contract/test_governance_review.py. |

| T023 | [US4] Implementar listado/detalle revisable con proyecciones explícitas por scope en src/oralia/application/services/session_privacy_service.py y routers/governance.py. |

| T024 | [US4] Sanear consultas históricas de detalle/traza sin perder metadatos técnicos ni reexponer contenido eliminado en src/oralia/application/queries/get_session.py y reconstruct_session_trace.py. |

| T025 | [US4] Añadir revisión docente con secciones de original/corrección/respuestas/fuentes/verificaciones/incidencias/resumen a apps/web/src/routes/Gobierno.tsx. |

| T026 | [US5] Añadir pruebas JSON/Markdown, lote mixto, texto libre no revisado, alias y ausencia de secretos/audio/razonamiento en tests/contract/test_session_exports.py. |

| T027 | [US5] Implementar proyección cerrada, revalidación íntegra y alias por lote en src/oralia/application/services/session_export_service.py. |

| T028 | [US5] Exponer descarga efímera no-store JSON/Markdown y límites del lote en src/oralia/interfaces/api/routers/governance.py. |

| T029 | [US5] Añadir revisión explícita de texto libre, selección de lote y descarga/revocación de Blob en apps/web/src/routes/Gobierno.tsx. |

| T030 | [US6] Probar eliminación completa/recibo/idempotencia, sesión activa, rollback, expiración y aislamiento de materiales/sesiones en tests/integration/test_session_privacy.py. |

| T031 | [US6] Implementar borrado de todas las proyecciones propias y recibo sin contenido, con control propietario/docente, en src/oralia/application/services/session_privacy_service.py. |

| T032 | [US6] Implementar purga manual y exclusión de eliminadas/expiradas de revisión/exportación en src/oralia/interfaces/api/routers/governance.py y servicios de privacidad/exportación. |

| T033 | [US6] Añadir confirmación accesible de eliminación y recibo verificable a apps/web/src/routes/Gobierno.tsx y cliente participante. |

| T034 | [US7] Probar métricas agregadas/faltantes y catálogo sin notas/perfiles en tests/contract/test_governance_metrics.py. |

| T035 | [US7] Implementar métricas agregadas disponibles y faltantes explícitos en src/oralia/interfaces/api/routers/governance.py. |

| T036 | [US7] Completar formulario de configuración, modelos/agentes/materiales y estados técnicos en apps/web/src/routes/Gobierno.tsx y styles.css. |

| T037 | [US7] Añadir recorrido Playwright real de login, versión activa, participante/consentimiento, revisión, exportación, eliminación, logout y denegación en tests/e2e/test_governance_flow.spec.ts. |

| T038 | Ejecutar suite determinista global y registrar cifras/logs reales en specs/005-teacher-governance/validation-backend.json. |

| T039 | Ejecutar frontend build/lint y Playwright completo; registrar en specs/005-teacher-governance/validation-frontend.json. |

| T040 | Ejecutar Black de inventario tocado y Ruff estructural con Counter contra baseline durable en specs/005-teacher-governance/ruff-validation.json. |

| T041 | Probar migración limpia y desde t004 en bases temporales, DDL histórico y cleanup en specs/005-teacher-governance/validation-migrations.json. |

| T042 | Ejecutar quickstart real y actualizar límites/evidencia en specs/005-teacher-governance/quickstart.md. |

| T043 | Revisar 11 principios y checklists con evidencia en specs/005-teacher-governance/implementation-evidence.md. |

| T044 | Ejecutar speckit-analyze de solo lectura y archivar resultado sin hallazgos críticos ni cobertura faltante en specs/005-teacher-governance/analysis-report.md. |

| T045 | Ejecutar speckit-converge contra código/pruebas/documentos; añadir solo brechas reales al final de specs/005-teacher-governance/tasks.md y repetir implementación hasta cero. |

| T046 | Consolidar tabla completa de tareas, cobertura y límites medidos en specs/005-teacher-governance/implementation-evidence.md; no iniciar 006 antes del cierre. |



Revisión final y convergencia: analysis-report.md. Sin brechas accionables; 46/46

tareas cerradas después de las puertas medidas. Se autoriza avanzar a Feature 006.

