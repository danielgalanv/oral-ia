# Tasks — Feature006

Único escritor, sin agentes/commits; pruebas antes de código.

## Phase 1: Setup

- [X] T001 Añadir contrato negativo de protocolo/sintético/condiciones/límites en tests/validation/test_protocol.py. (FR-002 FR-003 FR-015 SC-006)
- [X] T002 Crear catálogo15 y protocolo validado en src/oralia/validation/protocol.py. (FR-004 FR-005 FR-011 FR-015)

## Phase 2: US1

- [X] T003 [US1] Añadir pruebas reales baseline/agencia y precisión/trace en tests/validation/test_experiment.py. (FR-001 FR-007 FR-008 SC-001 SC-002)
- [X] T004 [US1] Implementar fixtures aisladas, baseline directo y compositor real con instrumentación en src/oralia/validation/experiment.py. (FR-001 FR-003 FR-004 FR-007 FR-008 FR-011)

## Phase 3: US2

- [X] T005 [US2] Probar autorización y efecto real de ambas ablaciones sin mutación posterior en tests/validation/test_experiment.py. (FR-002 FR-003 SC-006)
- [X] T006 [US2] Implementar sustituciones scoped de verificador solo en runner sintético en src/oralia/validation/experiment.py. (FR-002 FR-003 FR-004)

## Phase 4: US3

- [X] T007 [US3] Añadir matriz de fallos, rollback/recuperación/estado y borrado en tests/validation/test_failures.py. (FR-005 FR-006 FR-009 SC-004)
- [X] T008 [US3] Implementar inyecciones reales y métricas con procedencia/faltantes en src/oralia/validation/experiment.py. (FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 SC-002)

## Phase 5: US4

- [X] T009 [US4] Probar integridad, límites, cambio código y replay estructural en tests/validation/test_reporting.py. (FR-011 FR-014 SC-003)
- [X] T010 [US4] Implementar paquetes/manifiesto/replay con hashes en src/oralia/validation/reporting.py. (FR-011 FR-012 FR-014 FR-015)

## Phase 6: US5

- [X] T011 [US5] Probar indicadores humanos ausentes, denominadores y prudencia en tests/validation/test_reporting.py. (FR-010 FR-012 FR-013 SC-005)
- [X] T012 [US5] Implementar informes comparativos/agregados/propuesta evolución en src/oralia/validation/reporting.py. (FR-007 FR-008 FR-009 FR-010 FR-012 FR-013 SC-005)
- [X] T013 [US5] Añadir CLI textual y prueba subprocess E2E en src/oralia/validation/__main__.py y tests/validation/test_cli.py. (FR-015 FR-016 SC-006)

## Phase 7: Gates

- [X] T014 Ejecutar catálogo completo/replay y archivar paquete real en specs/006-architecture-validation/evidence/ y quickstart.md. (FR-001 FR-002 FR-004 FR-005 FR-006 FR-011 FR-014 SC-001 SC-002 SC-003 SC-004 SC-005)
- [X] T015 Ejecutar suite global, Black/Ruff Counter, lock y frontend build/lint/Playwright en specs/006-architecture-validation/validation-*.json. (FR-016)
- [X] T016 Revisar principios/checklists/cobertura y análisis final en specs/006-architecture-validation/analysis-report.md. (FR-003 FR-016 SC-006)
- [X] T017 Ejecutar convergencia append-only y consolidar evidencia completa en specs/006-architecture-validation/implementation-evidence.md. (FR-016)

## Dependencies / strategy

Setup→US1→US2→US3→US4→US5→gates. Pruebas de módulos independientes pueden
redactarse separadamente, pero no se delegan ni ejecutan escritores paralelos. US1 es
primer hito; todos los recorridos y gates obligatorios para terminar. Criterios
independientes: los de cada US en spec.md.

## Phase 8: Convergence

- [X] T018 Marcar reconstrucción arquitectónica del baseline como no aplicable con motivo, sin contar la cadena vacía de la fixture; probar en tests/validation/test_reporting.py y corregir src/oralia/validation/reporting.py; regenerar paquete/replay e informe con medidas actuales por FR-009 y SC-002 (partial, HIGH).
