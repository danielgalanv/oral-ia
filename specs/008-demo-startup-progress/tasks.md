# Tasks008 — progreso del arranque

## Phase 1: Setup

- [X] T001 Preservar fuentes/paquetes006–007 y hashes de recursos en specs/008-demo-startup-progress/baseline.json. (FR-008 SC-004)

## Phase 2: US1 — progreso real

- [X] T002 [US1] Probar etapas/heartbeat/full/TextOnly/Check/duplicación en tests/demo/test_progress.py. (FR-001 FR-002 FR-003 FR-005 FR-007 SC-001 SC-002 SC-003)
- [X] T003 [US1] Añadir contextos/avisos en src/oralia/demo/progress.py e integrar preflight/preparación/procesos/readiness en launcher.py. (FR-001 FR-002 FR-003 SC-001 SC-002)

## Phase 3: US2 — fallo/cancelación

- [X] T004 [US2] Probar causa desconocida, secretos y cancelación en tests/demo/test_progress.py y regresión test_supervisor.py. (FR-004 FR-006 FR-009 SC-003)
- [X] T005 [US2] Diagnosticar/sanear fallos y cancelación con cierre del avisador en progress.py y __main__.py conservando limpieza del supervisor. (FR-004 FR-006 SC-003)

## Phase 4: US3 — compatibilidad

- [X] T006 [US3] Eliminar solo preflight CLI duplicado mediante callback de credencial en __main__.py/launcher.py; conservar calentamiento API y controles separados. (FR-005 FR-006 FR-007 SC-001 SC-003)
- [X] T007 [US3] Ensayar PowerShell dos arranques sin Reset, Check/puerto ocupado/TextOnly temporal/Stop y check-demo.ps1; guardar tiempos/hashes/secretos en specs/008-demo-startup-progress/validation-demo.json. (FR-005 FR-006 FR-008 FR-009 SC-003 SC-004)
- [X] T008 [US3] Actualizar docs/DEMO.md con mensajes/carga inicial/espera/fallos y registrar archivos/tareas en specs/008-demo-startup-progress/implementation-evidence.md. (FR-010)

## Phase 5: Gates

- [X] T009 Ejecutar suite global, Playwright completo, Black afectado y Ruff Counter frente a baseline durable; guardar validation-*.json en specs/008-demo-startup-progress. (FR-009 SC-003 SC-004)
- [X] T010 Generar y reproducir204celdas actuales en specs/008-demo-startup-progress/evidence-current y verificar originales006/007. (FR-008 SC-004)
- [X] T011 Ejecutar analyze final read-only y converge append-only; archivar informes y cerrar tabla solo sin críticos/brechas. (FR-010 SC-004)

## Dependencias y estrategia

T001→T002→T003→T004→T005→T006→T007/T008→T009/T010→T011.
US1 mínimo útil; completar US2/US3/gates para entrega. Un escritor, sin subagentes.
Pruebas de consola y hashes pueden ejecutarse independientemente; no mutar mismos recursos
ni ejecutar dos ensayos sobre demo preparada simultáneamente. Sin cambios de esquema.
