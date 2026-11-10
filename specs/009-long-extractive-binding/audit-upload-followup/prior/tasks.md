# Tasks009

## Phase 1: Setup

- [X] T001 Preservar paquetes006/007/008,fuentes,recursos y hash archivo04 en specs/009-long-extractive-binding/baseline.json y prior-source.zip. (FR-007 SC-004)
- [X] T002 Reproducir HTTP archivo04 intacto y ampliar tests/integration/test_teacher_material_pack.py a ambos archivos/modos/scopes con segundo turno. (FR-001 FR-005 SC-001 SC-003)

## Phase 2: US1 — vinculación larga

- [X] T003 [US1] Escribir matriz de límites/Unicode/múltiples en tests/integration/test_long_extractive_binding.py antes de corrección. (FR-002 FR-003 SC-001 SC-002)
- [X] T004 [US1] Añadir helper canónico en src/oralia/domain/materials/extractive_excerpt.py y delegar snippet de infrastructure/generation/deterministic_adapter.py sin cambiar semántica. (FR-002 FR-003)
- [X] T005 [US1] Vincular proyección desde DB autorizada y traza metadata en src/oralia/application/orchestration/self_study_agency_composer.py; conservar T090/plantillas/fallback. (FR-002 FR-003 FR-004 FR-005 SC-002)

## Phase 3: US2 — frontera negativa

- [X] T006 [US2] Probar mutaciones/texto libre/metadata/version/location/scope/procedencia/curso/actividad/fallback/saneamiento en tests/integration/test_long_extractive_binding.py y suites T090/T150. (FR-004 FR-005 SC-002 SC-003)

## Phase 4: US3 — recorrido docente

- [X] T007 [US3] Añadir tests/e2e/test_teacher_long_material.spec.ts:login,carga04 real,activación/publicación,consulta/fuentes,cierre/revisión/exportación/borrado. (FR-006 SC-003)
- [X] T008 [US3] Ejecutar check-demo,suite global/build/lint/Playwright/Black/Ruff durable y confirmar recursos estables en specs/009-long-extractive-binding/validation-*.json. (FR-005 FR-007 FR-008 SC-003 SC-004)

## Phase 5: Gates / cierre

- [X] T009 Generar/reproducir paquete204 actual en specs/009-long-extractive-binding/evidence-current; verificar originales sin editar hashes. (FR-007 SC-004)
- [X] T010 Actualizar materiales/docente/RESULTADO.md y tabla/inventario/causa/límites en specs/009-long-extractive-binding/implementation-evidence.md con resultados reales. (FR-009)
- [X] T011 Ejecutar analyze final y converge hasta0críticos/brechas; archivar informes009 y cerrar sin commits/Reset. (FR-010 SC-004)

## Dependencias / estrategia

T001→T002→T003→T004→T005→T006→T007→T008/T009→T010→T011.
Pruebas antes de implementación; escritor único, sin agentes nuevos. US1 mínimo;entrega
requiere US2/US3/gates. No solapar Playwright/check-demo por puertos compartidos; pueden
correr backend y frontend con DB/índices propios. No alterar material04 ni seed demo.

## Phase 6: Convergence

- [X] T012 Corregir negación agregada entre oraciones en src/oralia/domain/agents/coherence_verifier_agent.py y probar metadata no negando contenido,contradicción real entre fuentes/historial en tests/contract/test_coherence_verifier_agent.py; conservar verificador y bloqueo por contradicción explícita por FR-002,FR-004,SC-001 (partial,HIGH). La traza HTTP004 muestra bloques menores400 y falsa contradicción por «No contiene datos de personas», independiente del binder.

## Phase 7: Convergence

- [X] T013 Habilitar acción Activar para documento processed en apps/web/src/routes/Tecnica.tsx y verificarla en test_teacher_long_material.spec.ts por FR-006/SC-003 (partial,HIGH). El backend ya admite processed; UI solo mostraba control para inactive/active y bloqueaba completar carga/publicación manual sin usar API fuera de la pantalla.

## Phase 8: Convergence

- [X] T014 Aislar índice por ejecución de tests/e2e/run_self_study_api.py sin borrar índices previos ni recursos habituales; repetir Playwright completo conservando aserción100 y archivo04 íntegro por FR-006,FR-007,FR-008/SC-003,SC-004 (partial,HIGH). El harness reiniciaba DB pero reutilizaba índice persistente con288entradas; el recorrido individual pasó y el completo devolvió solo2fuentes sin la afirmación100. No cambiar recuperación/umbral de producción para resolver un entorno de pruebas incoherente.

## Phase 9: Convergence

- [X] T015 Cerrar mediante API pública solo clientes Chroma creados bajo tmp_path de cada prueba en tests/conftest.py; preservar clientes ajenos,aserciones y consultas reales; repetir pruebas de reconstrucción y suite global por FR-007,FR-008/SC-004 (partial,HIGH). Fallo Nothing found on disk reaparece en suite grande,pero6casos aislados pasan;el harness no liberaba clientes persistentes. No ocultar fallo con skip/retry/reordenación ni alterar producción.
