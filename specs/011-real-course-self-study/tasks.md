# Tasks:011 — Autoestudio real

Estado: implementación autorizada;17/17 completadas. G1 humano y T061/T067 previos abiertos; no se declara aceptación didáctica.

## Phase1: Setup

- [X] T001 Conservar baseline de fuentes, datos, procesos y evidencias anteriores en evidence/baseline.json y recibo inicial.
- [X] T002 Observar primera consulta con wrappers transparentes y registrar candidato/snapshot/grounding/propuesta en tests/integration/test_real_course_self_study.py y evidence/diagnostic-first/.

## Phase2: Foundational

- [X] T003 Documentar causa demostrada/perfil y contrato elegido en research.md y contracts/self-study.md, conservando primer fallo.
- [X] T004 Crear pruebas negativas de vinculación/proyección en tests/unit/test_material_supported_excerpt.py antes de corregir el contrato.
- [X] T005 Implementar corrección acotada y versionada de selección/vinculación si se necesita en domain/materials y self_study_agency_composer.py, sin modificar verificadores.

## Phase3: US1 — Autoestudio con citas

- [X] T006 [US1] Preparar extractos PDF10–12 y Testing9 si necesario, manifest de procedencia y reproducción en src/oralia/course_study/materials.py.
- [X] T007 [US1] Crear actividad extractiva con política completa y límites propios, sin unidades/repertorio ficticio en src/oralia/course_study/preparation.py.
- [X] T008 [US1] Ejecutar primera conversación real completa y congelar variante antes de ajustes en tests/integration/test_real_course_self_study.py y evidence/.
- [X] T009 [US1] Verificar pertinencia/significado/fuentes/límites de cada turno y conservar primeras divergencias en evidence/conversations/; nunca simular un turno tras cierre.

## Phase4: US2 — Entrada repetible

- [X] T010 [US2] Implementar raíz marcada, lock/idempotencia/migración/auth normal y terminal API en src/oralia/course_study/__main__.py y scripts/course-study.ps1.
- [X] T011 [US2] Probar preparación repetida, cierre/cancelación y recursos/credenciales aislados en tests/integration/test_course_study_cli.py.
- [X] T012 [US2] Documentar comando exacto, perfil/actividad, páginas y uso por terminal en quickstart.md y evidence/report.md.

## Phase5: US3 — Regresión y entrega

- [X] T013 [US3] Ejecutar contratos/negativos/regresiones pertinentes y global si cambia código compartido; build/lint/Playwright completo en evidence/validation/.
- [X] T014 [US3] Ejecutar Black/Ruff estructural por ruta/código/mensaje con multiplicidad y204/replay si cambia manifiesto; conservar originales en evidence/validation/.
- [X] T015 [US3] Verificar hashes originales/entornos/procesos/paquetes históricos; entregar transcriptos reales íntegros y tabla16tareas en evidence/.
- [X] T016 [US3] Ejecutar analyze/converge final de solo lectura y registrar límites/puertas humanas sin cierre o aprobación inferidos en evidence/analysis-convergence.md.

## Dependencies and strategy

T001→T002→T003→T004→T005→T006→T007→T008→T009; T010 tras T007; T011–012 trasT010; T013–016 tras experiencia completa. Revisión de documentos y lectura de contratos pueden hacerse en paralelo, mutaciones secuenciales. MVP US1; después entrada US2 y validación US3. No delegar implementación; investigación de solo lectura ya realizada conforme a plan. Cada historia tiene prueba independiente en spec.md.

## Phase 6: Convergence

- [X] T017 [HIGH] [US1] Corregir selección de tareas con objeto explícito en el contexto del mismo fragmento autorizado (FR-003/004, SC-001, decisión C); conservar followup-first y followup-diagnostic, probar seguimiento real y negativo con objeto ajeno, sin modificar verificadores.
