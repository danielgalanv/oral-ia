# Tasks — Demostración local007

Único escritor; sin commits; pruebas antes de cada bloque.

## Phase 1: Setup

- [X] T001 Preservar fuente y paquete006 original, hashes y estado habitual en specs/007-local-demonstration/baseline006.json. (FR-015 SC-006)

## Phase 2: US1

- [X] T002 [US1] Añadir pruebas de ruta/links/puertos/env/propiedad/parada y fallo parcial en tests/demo/test_launcher.py. (FR-001 FR-002 FR-003 FR-004 FR-005 FR-007 SC-001 SC-005)
- [X] T003 [US1] Implementar rutas/lock/entorno/preflight y supervisor con readiness/stop seguro en src/oralia/demo/resources.py y launcher.py. (FR-001 FR-002 FR-003 FR-004 FR-005 FR-008 SC-001 SC-005)
- [X] T004 [US1] Crear CLI y wrapper PowerShell sin secretos persistentes en src/oralia/demo/__main__.py y scripts/demo.ps1. (FR-001 FR-002 FR-003 FR-004 FR-007 FR-008)

## Phase 3: US2

- [X] T005 [US2] Probar esquema/seed dos arranques/perfil/retención/publicación en tests/demo/test_fixtures.py. (FR-005 FR-006 FR-007 FR-008 FR-012 SC-002 SC-005)
- [X] T006 [US2] Implementar migración/fixtures sintéticas idempotentes con servicios existentes en src/oralia/demo/fixtures.py. (FR-005 FR-006 FR-008 FR-012)
- [X] T007 [US2] Implementar reset confirmado y validar centinelas/proceso ajeno/lifecycle en tests/demo/test_lifecycle.py y src/oralia/demo/launcher.py. (FR-004 FR-005 FR-007 FR-014 SC-002 SC-005)

## Phase 4: US3

- [X] T008 [US3] Añadir portada y enlaces activos por modo en apps/web/src/routes/Inicio.tsx, Gobierno.tsx y main.tsx. (FR-009 FR-010 FR-011 SC-003)
- [X] T009 [US3] Inicializar referencias no secretas sin inicio automático en Autoestudio.tsx/DefensaOral.tsx; cache/puertos demo explícitos en apps/web/vite.config.ts. (FR-005 FR-009 FR-010 FR-011)
- [X] T010 [US3] Añadir Playwright real desde portada/login a fuentes/cierre/revisión/exportación/eliminación y defensa en tests/e2e/test_demo_journey.spec.ts usando seed real aislado. (FR-009 FR-010 FR-011 FR-012 FR-014 SC-003 SC-005)

## Phase 5: US4

- [X] T011 [US4] Probar alternativa efímera y offline con sockets externos prohibidos después de preparar recursos en tests/demo/test_offline.py y tests/e2e/test_demo_journey.spec.ts. (FR-008 FR-011 FR-012 FR-014 SC-003 SC-004)
- [X] T012 [US4] Documentar guion10min/preparación/arranque/parada/reset/fallos/limitaciones en docs/DEMO.md y specs/007-local-demonstration/quickstart.md. (FR-001 FR-003 FR-007 FR-008 FR-013)

## Phase 6: Gates

- [X] T013 Ensayar PowerShell/lifecycle real y guardar centinelas/puertos/offline en specs/007-local-demonstration/validation-demo.json. (FR-001 FR-002 FR-004 FR-005 FR-006 FR-007 FR-014 SC-001 SC-002 SC-004 SC-005)
- [X] T014 Regenerar/reproducir204celdas con código actual en specs/007-local-demonstration/evidence006-current y verificar hashes originales006. (FR-015 SC-006)
- [X] T015 Ejecutar suite global/build/lint/Playwright/Black/Ruff Counter y lock en specs/007-local-demonstration/validation-*.json. (FR-016 SC-006)
- [X] T016 Ejecutar analyze final con cobertura/principios/checklists en specs/007-local-demonstration/analysis-report.md. (FR-016)
- [X] T017 Ejecutar converge append-only hasta cero y consolidar tabla de tareas/archivos/resultados/límites en specs/007-local-demonstration/implementation-evidence.md. (FR-013 FR-014 FR-015 FR-016)

## Dependencies / strategy

Setup→US1→US2→US3→US4→gates. Criterio independiente por historia en spec.md.
Pruebas de archivos independientes pueden prepararse separadas, sin delegar escritores;
todo secuencial. Primer hitoUS1; completar todos los bloques obligatorios para cierre.

## Phase 7: Instalación limpia — brecha descubierta en ensayo

- [X] T018 Probar instalación limpia y upgrade005 con todas las tablas/columnas de modelos y lock real en tests/demo/test_migrations.py; añadir migración aditiva src/oralia/infrastructure/db/migrations/versions/t007_index_rebuild_lock.py para tabla existente sin migración por FR-001, FR-006 y FR-016. No cambiar migraciones históricas.

- [X] T019 Aislar cookies de demo y directorio de configuración Vite sin cambiar los nombres/autorización por defecto; probar login/logout cruzados en tests/demo/test_cookie_isolation.py e integrar en local_access.py, governance.py, participante.py y vite.config.ts por FR-003, FR-005, FR-012 y SC-005.
