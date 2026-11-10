# Tasks: 010 — Conversación guiada y recuperación

Estado: implementación en curso; **76/83 completadas**. Las rutas siguientes son relativas a esta carpeta. Las carpetas de integración existentes se concretarán por símbolo al implementar, sin inventar módulos paralelos. Implementación autorizada el 18-10-2026; evidencia y cierre se registran por tarea.


## Base

- [X] T001 Congelar hashes y estado inicial, separando fallos observados de validaciones anteriores en `evidence-baseline.json`. (FR-027, FR-028, FR-032)
- [X] T002 Crear corpus de desarrollo con las dos secuencias observadas y oráculos por propiedades en `../../../tests/dialogue/fixtures/development.json`. (FR-029)
- [X] T003 Congelar 12 diálogos reservados y 48 entradas independientes con protocolo de revisión sin ajuste sobre aceptación en `../../../tests/dialogue/fixtures/holdout.json`. (FR-029, FR-030)
- [X] T004 Medir proveedores, recursos, tiempos y presupuestos existentes sin instalar modelos en `capability-baseline.json`. (FR-019, FR-025, FR-031)

## Fundación

- [X] T005 Escribir pruebas de contratos v1/v2, actos, negación y propuestas no autorizadas en `../../../tests/contract/test_dialogue_contract.py`. (FR-002, FR-017, FR-018)
- [X] T006 Implementar contratos de diálogo versionados y adaptación compatible del puerto de generación en `../../../src/oralia/domain/dialogue/contracts.py`. (FR-002, FR-017, FR-018, FR-027)
- [X] T007 Escribir pruebas de migración limpia, upgrade, rollback y snapshots antiguos en `../../../tests/integration/test_dialogue_context_migration.py`. (FR-003, FR-027, FR-032)
- [X] T008 Añadir contexto tipado, snapshots y migración aditiva de contexto, unidades y recibos en `../../../src/oralia/infrastructure/db/migrations/versions/t010_dialogue_context.py`. (FR-003, FR-024, FR-027, FR-032)
- [X] T009 Aplicar contexto mediante StatePatch transaccional, control de versión y cancelación en `../../../src/oralia/application/services/dialogue_context_service.py`. (FR-003, FR-024, FR-026)
- [X] T010 Escribir pruebas de referente, recuperación contextual y revocación entre turnos en `../../../tests/unit/test_dialogue_retrieval.py`. (FR-004, FR-014, FR-015)
- [X] T011 Implementar recuperación contextual revalidando destinatario, versión y alcance en `../../../src/oralia/application/services/dialogue_retrieval_service.py`. (FR-014, FR-015, FR-018)
- [X] T012 Escribir negativos de autorización, transformaciones y filtrado de pistas en `../../../tests/contract/test_dialogue_authorization.py`. (FR-008, FR-017, FR-018)
- [X] T013 Integrar plantillas y bindings cerrados sin modificar las garantías T090/T150 en `../../../src/oralia/domain/dialogue/policy.py`. (FR-017, FR-018, FR-025)

## US1

- [X] T014 [US1] Escribir pruebas de conversación de estudio completa con intérprete y proveedor efectivos en `../../../tests/integration/test_dialogue_study.py`. (FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-012, FR-013)
- [X] T015 [US1] Evolucionar intérprete compartido: acto separado de modo, negación, ambigüedad y confianza en `../../../src/oralia/domain/dialogue/contracts.py`. (FR-002, FR-004, FR-005, FR-012)
- [X] T016 [US1] Implementar resolución de referentes y política de recuperación con límite de estancamiento en `../../../src/oralia/domain/dialogue/context.py`. (FR-003, FR-004, FR-009, FR-013)
- [X] T017 [US1] Integrar política en compositor de autoestudio y cubrir los cinco modos habilitables en `../../../tests/integration/test_dialogue_study.py`. (FR-005, FR-007, FR-009, FR-012, FR-016)
- [X] T018 [US1] Ajustar coherencia para repetición solicitada sin exceptuar seguridad ni fundamentación en `../../../tests/unit/test_dialogue_coherence.py`. (FR-006, FR-013, FR-018)
- [X] T019 [US1] Validar saludos, consultas amplias, «dímelo», referentes ambiguos y cambio confirmado de tema en `../../../tests/integration/test_dialogue_study.py`. (FR-003, FR-004, FR-005, FR-009, FR-014)

## US2

- [X] T020 [US2] Escribir secuencia oral completa, pistas sin solución y discrepancias condicionadas en `../../../tests/integration/test_dialogue_defense.py`. (FR-006, FR-007, FR-008, FR-010, FR-011)
- [X] T021 [US2] Extraer objetivos desde material y pregunta pendiente evitando partículas y números aislados en `../../../src/oralia/domain/dialogue/policy.py`. (FR-009, FR-010)
- [X] T022 [US2] Implementar escalera de ayuda con límites de no revelación en todas las superficies en `../../../src/oralia/domain/dialogue/policy.py`. (FR-007, FR-008, FR-016)
- [X] T023 [US2] Implementar tratamiento neutral de discrepancias, unidades y condiciones documentadas en `../../../src/oralia/domain/dialogue/policy.py`. (FR-001, FR-011)
- [X] T024 [US2] Integrar defensa con pregunta pendiente, repregunta ligada a afirmación y recuperación en `../../../tests/integration/test_dialogue_defense.py`. (FR-006, FR-007, FR-008, FR-009, FR-010, FR-013)

## US3

- [X] T025 [US3] Escribir pruebas de unidades docentes: borrador/publicación/retiro, versión y autorización en `../../../tests/contract/test_dialogue_teaching_units.py`. (FR-016, FR-017, FR-020, FR-027)
- [X] T026 [US3] Crear dos paquetes docentes revisables con cinco objetivos, dos ejemplos, dos contrastes y tres preguntas con pistas por dominio en `../../../materiales/docente/dialogue/README.md`. (FR-016, FR-020)
- [X] T027 [US3] Implementar gestión y publicación de unidades docentes mediante permisos existentes y edición docente en `../../../src/oralia/application/services/teaching_unit_service.py`. (FR-017, FR-020, FR-027)
- [X] T028 [US3] Implementar planificador y renderer controlados con transformaciones cerradas y perfil declarado en `../../../src/oralia/domain/dialogue/contracts.py`. (FR-016, FR-017, FR-019)
- [X] T029 [US3] Validar independientemente fundamentación y no revelación del resultado renderizado en `../../../tests/integration/test_dialogue_authorization.py`. (FR-008, FR-017, FR-018)
- [X] T030 [US3] Exponer proveedor y capacidades efectivos, avisando de degradación y reservas en `../../../apps/web/src/`. (FR-019, FR-023, FR-028)
- [X] T031 [US3] Realizar estudio reproducible de viabilidad de generación local; registrar falta de recursos como límite sin descarga automática en `local-generation-feasibility.md`. (FR-019, FR-029, FR-031, FR-032)
- [X] T032 [US3] Definir y ejecutar negativos del protocolo G2 en entorno aislado; impedir publicación libre si no pasa verificación en `generative-gate.md`. (FR-017, FR-018, FR-019, FR-030)
- [X] T033 [US3] Comprobar que panel de fuentes, ejemplos y resumen no revelan soluciones prohibidas en `../../../tests/e2e/`. (FR-008, FR-023)
- [X] T034 [US3] Mostrar suficiencia del material y alternativas concretas; conservar el material corto como prueba de límites en `../../../apps/web/src/`. (FR-005, FR-015, FR-016, FR-020)

## US4

- [X] T035 [US4] Escribir negativos de preflight sin creación de sesión ni consumo de bloqueo en `../../../tests/integration/test_dialogue_preflight.py`. (FR-021, FR-027)
- [X] T036 [US4] Implementar preflight de actividad y destinatario antes de adquirir sesión en `../../../src/oralia/application/services/`. (FR-021)
- [X] T037 [US4] Escribir matriz de propietario, acceso perdido, sesión ajena y cierre administrativo confirmado en `../../../tests/integration/test_dialogue_recovery.py`. (FR-022, FR-026)
- [X] T038 [US4] Implementar recuperación autorizada y cierre administrativo confirmado con política vigente en `../../../apps/web/src/`. (FR-022, FR-024, FR-026)
- [X] T039 [US4] Mejorar modalidad textual, orientación de actividad y fuentes accesibles por teclado en `../../../apps/web/src/`. (FR-019, FR-021, FR-023)
- [X] T040 [US4] Escribir pruebas de doble envío, desconexión, cancelación y resultado tardío o desconocido en `../../../tests/failure/test_dialogue_requests.py`. (FR-024, FR-025)
- [X] T041 [US4] Implementar recibos idempotentes atómicos, reconciliación y cliente versionado en `../../../src/oralia/application/services/`. (FR-024, FR-027)
- [X] T042 [US4] Verificar ocupado, errores, teclado, presupuestos y cierre ganador único en `../../../tests/e2e/`. (FR-023, FR-024, FR-025)

## US5

- [X] T043 [US5] Escribir matriz de privacidad del nuevo contexto y recibos para todos los scopes y cierres en `../../../tests/integration/test_dialogue_privacy.py`. (FR-026)
- [X] T044 [US5] Integrar purga, retención, revisión y exportación del estado nuevo sin reconstruir datos borrados en `../../../src/oralia/application/services/`. (FR-026, FR-027, FR-028)
- [X] T045 [US5] Implementar runner de diálogos completos con proveedor real y oráculos estructurales independientes en `../../../tests/dialogue/runner.py`. (FR-028, FR-029, FR-030)
- [X] T046 [US5] Ejecutar corpus reservado y 48 entradas una vez congelados; publicar fallos por caso y reabrir desarrollo si falla en `acceptance-results.md`. (FR-029, FR-030)
- [X] T047 [US5] Publicar denominadores y resultados separados por dominio, modo, perfil y puerta de calidad en `acceptance-results.md`. (FR-019, FR-028, FR-030)
- [X] T048 [US5] Añadir recorridos de navegador originales sin sustituir respuestas del generador en `../../../tests/e2e/`. (FR-023, FR-029, FR-031)
- [X] T049 [US5] Ejecutar matriz adversarial: revocación, inyección, límites, ausencia de recursos y fallos de proveedor en `acceptance-results.md`. (FR-001, FR-004, FR-008, FR-015, FR-018, FR-024, FR-025, FR-026)
- [X] T050 [US5] Actualizar guía docente y operación con capacidades, costes, recuperación y utilidad humana pendiente en `../../../docs/DEMO.md`. (FR-019, FR-020, FR-030, FR-031)

## Conversaciones sintéticas de herramientas — US5

- [X] T057 [US5] Definir esquema, ocho familias y 16 guiones sintéticos revisados (8 desarrollo/8 reserva), con operaciones esperadas/prohibidas, roles, scopes y efectos en `../../../tests/dialogue/fixtures/tools/`, conforme synthetic-tool-conversations.md. (FR-026, FR-029, FR-033)
- [X] T058 [US5] Escribir pruebas negativas del runner con oráculos independientes: operación equivocada, argumentos indebidos, estado inconsistente y falso éxito en `../../../tests/contract/test_synthetic_tool_runner.py`. (FR-018, FR-033)
- [X] T059 [US5] Ampliar runner y recorridos públicos de API/navegador, observar operaciones reales, aislar almacenamiento e inyectar fallos etiquetados sin sustituir resultados favorables en `../../../tests/dialogue/runner.py`. (FR-024, FR-026, FR-028, FR-033)
- [X] T060 [US5] Ejecutar los 16 escenarios, comprobar propiedades y publicar resultados por familia/rol/perfil con fallos y semillas en `synthetic-tool-results.md`; incorporar regresión de nuevos defectos sin contaminar reserva. (FR-029, FR-030, FR-033; SC-009)

T057 depende de T002/T003 y precede a las implementaciones de herramientas que valida; T058 precede a T059. T059 depende de T045 y de los contratos implementados pertinentes; T060 requiere T057–T059 y precede al cierre T051–T056. Los IDs nuevos preservan referencias existentes; el orden numérico no sustituye estas dependencias.

## Cierre

- [X] T051 Ejecutar suites completas, build/lint/Black y Ruff estructural con multiplicidad y baseline en `implementation-evidence.md`. (FR-018, FR-028, FR-030)
- [X] T052 Verificar upgrade, rollback y arranque desde PowerShell normal sin PATH heredado, offline y sin tocar procesos ajenos en `implementation-evidence.md`. (FR-022, FR-027, FR-031, FR-032)
- [ ] T053 Reproducir experimentos anteriores en paquete separado y comparar los 24 diálogos nuevos de forma pareada contra el baseline monolítico existente, con condiciones iguales y métricas por caso; preservar hashes 006–009 y archivo 04 en `implementation-evidence.md`. (FR-027, FR-028, FR-029, FR-032)
- [ ] T054 Auditar constitución, T090/T150, privacidad y todas las listas antes de marcar tareas con evidencia en `implementation-evidence.md`. (FR-001, FR-018, FR-025, FR-026, FR-030)
- [ ] T055 Resolver puertas G0/G1 obligatorias y estado G2; mantener G3 humano pendiente sin afirmar utilidad acreditada en `implementation-evidence.md`. (FR-016, FR-019, FR-029, FR-030)
- [ ] T056 Ejecutar analyze y converge postimplementación, resolver brechas obligatorias y publicar límites y tareas realmente cerradas en `implementation-evidence.md`. (FR-027, FR-030, FR-032)

## Dependencias y ejecución

Base T001–T004 → Fundación T005–T013 → US1 T014–T019 → US2 T020–T024 → US3 T025–T034 → US4 T035–T042 → US5 T043–T050 → ampliación sintética T057–T060 (con diseño T057 anticipado) → cierre T051–T056. Las pruebas de cada bloque se escriben antes de su implementación y deben fallar por la causa esperada. T025–T027 preceden a T028–T029; T040 precede a T041; T043 precede a T044. Cada tarea de integración incluye el código de los símbolos existentes afectados y sus pruebas, aunque se indique una ruta de pruebas como punto de entrada.

No se marca [P]: estado, políticas, composer y frontend comparten archivos. Un responsable por archivo; no ejecutar bloques simultáneos sin resolver dependencias. El incremento mínimo demostrable requiere fundamentos + US1 + US2 + contenido autorizado de US3; no constituye cierre hasta G0/G1 y operación/privacidad completas.

T031 es un estudio obligatorio con resultado positivo o negativo verificable. No obliga a descargar modelos ni a habilitar generación libre; G2 solo autoriza esa capacidad si pasa todos sus controles. T032 puede concluir capacidad bloqueada con negativos y razones documentadas. La evaluación humana G3 y voz real no se presentan como realizadas. Ninguna tarea se cierra solo por existir el documento o por pasar dobles de prueba.


## Phase 1: Convergence

Revisión intermedia: 33 FR, 9 SC, decisiones A–G y 11 principios. Resultado tasks_appended, no converged: 2 CRITICAL/4 HIGH; 1 contradicción, 2 ausencias y 3 parciales. Las tareas originales pendientes no se sustituyen ni se dan por terminadas con esta sección.

- [ ] T061 CRITICAL Restaurar por copia exacta los seis PNG/JSON históricos sobrescritos por el test de subida, verificar contra los hashes originales de evidence-baseline.json y documentar recuperación en preservation-incident/incident.json; si no hay copia, mantener pérdida y bloqueo explícitos sin fabricar archivos ni editar hashes. Origen: FR-027/028/032, Constitución VIII/X, T053 (contradicts).
- [X] T062 CRITICAL Completar e integrar el diálogo guiado en los dos compositores con proveedor efectivo, cinco modos, pregunta/objetivo persistentes, repetición y reformulación autorizadas, pistas y discrepancias; completar T013–T024/T028–T034 y demostrar las dos secuencias históricas reales sin dobles decisivos. Origen: FR-002–020, SC-001/003/004/005, US1/US2 (missing).
- [X] T063 HIGH Completar disponibilidad de actividad, recuperación con propietario/cierre docente confirmado, recibos idempotentes públicos, reconciliación y capacidades/modalidad/accesibilidad; cerrar T036–T042 y documentación operativa T050/T052 con API/UI reales y datos aislados. Origen: FR-021–025/031, SC-006/008 (partial).
- [X] T064 HIGH Completar la matriz de conservación transcript/summary/efímera, exportación, caducidad/purga, cancelación/cierre y no resurrección del contexto/recibos/nuevas superficies en ambos modos; completar T033/T043/T044. Origen: FR-008/026/027, SC-004/006/009, Constitución VII (partial).
- [ ] T065 HIGH Ejecutar el runner real de 24 diálogos, 48 entradas y 16 conversaciones de herramientas con oráculos por operación/argumentos/rol/efecto/respuesta, publicar primera reserva y fallos, comparación pareada y replay separado; completar T045–T060 pendientes, G0/G1 y analyze/converge finales. Origen: FR-029/030/032/033, SC-001–009, Constitución X (missing).
- [X] T066 HIGH Validar que la regresión completa de navegador no cambia ningún archivo histórico 006–009: usar salidas nativas por ejecución y comparar hashes antes/después con tests/e2e/preservation_guard.ts; preservar informe y diferenciar cero nuevas mutaciones de la restauración todavía pendiente T061. Origen: FR-027/028/032, T053, Constitución VIII/X (partial).


## Phase 2: Convergence

Revisión postimplementación: 33 FR, 9 SC, 20 escenarios, 7 decisiones del plan y
11 principios; dos brechas obligatorias (1 CRITICAL, 1 HIGH). La preservación crítica
ya está cubierta por T061 y mantiene abiertos T053/T054/T055/T056/T065; no se duplica
su restauración ni se declara converged. Se explicita la revisión humana de sistema,
que no puede sustituirse por asserts o por anotación del implementador automático.

- [ ] T067 HIGH Obtener y registrar revisión humana de los 24 diálogos sintéticos y de la rúbrica preparada en human-system-review.md; conservar resultado, casos/pasos y correcciones requeridas sin atribuir revisión humana a una evaluación automática ni declarar utilidad G3 o voz real. Origen: plan G1 (línea 128), FR-016/030, SC-001–008 y T055 (partial).


## Phase 3: Convergence

Auditoría técnica de IA de las 24 conversaciones, separada de T067. Se detectan
brechas semánticas observables que los oráculos estructurales previos no advertían.
Resultado tasks_appended, no converged; siguen pendientes T061 y revisión humana.

- [X] T068 HIGH Distinguir el objeto de una repetición de una segunda orden («repite la comparación/el ejemplo/la pista»), conservando ambigüedad ante órdenes realmente coordinadas o negadas; cubrir releer, ayudas conjugadas y saludos compuestos mediante regresiones antes de corregir. Origen: FR-002/004/006, D10 y V-H06, V-I01/V-I04 (partial).
- [X] T069 HIGH Conservar el objetivo vigente al pedir comparación con otro tema y corregir el falso bloqueo de coherencia ante predicados distintos sin exceptuar repetición ni contradicciones reales; demostrar D02 y D06 con unidades/fuentes actuales, verificador independiente y T090. Origen: FR-007/009/018, plan C/E (partial).
- [X] T070 HIGH Ante solicitud de ejemplo/comparación protegidos sin unidad docente autorizada de ese tipo, devolver un límite específico en vez de sustituirla por la pregunta o provocar verification_failed; mantener autorización y no revelación. Origen: FR-007/008/015, D08 y D11 (partial).
- [X] T071 HIGH Publicar auditoría técnica por cada uno de los 24 casos y sus correcciones, actualizar paquete de revisión humana sin atribuirle aprobación, y validar cambios con regresiones pertinentes, Black/Ruff estructural, evidencia experimental separada y reserva nueva no usada para ajustes; conservar resultados anteriores. Origen: FR-028/029/030/032, SC-001–009 y plan G1 (partial).


## Phase 4: Convergence

Primera quinta reserva: 12/12 diálogos y 46/48 entradas, pero 35/36 críticas:
no aprueba G1. Se conserva íntegra y sus fallos pasan a desarrollo.

- [X] T072 HIGH Resolver referencias deícticas con cortesía y complementos nominales de continuación sin convertirlos en otra orden, conservando aclaración con cero o varios referentes y ambigüedad de órdenes coordinadas; congelar y ejecutar nueva reserva de clasificación, demostrar que no se ajustó sobre los 12 diálogos W ya aprobados y verificar su reproducción actual. Origen: FR-002/003/004/029/030, W-I09/W-I31 y SC-002 (partial).


## Phase 5: Convergence

Análisis33 FR/9 SC/20 escenarios/7 decisiones/11 principios, sin contradicciones críticas entre artefactos. D01 recibe aclaración genérica; available_topics ya está en API y panel de capacidades. Brecha parcial de orientación accionable junto a la conversación; no se afirma que faltasen todas las opciones ni que fallase la clasificación. T061/T067 continúan sin duplicación.

- [X] T073 HIGH Ofrecer selección explícita de temas vigentes junto a la aclaración/orientación de autoestudio y confirmación antes de cambiar, reutilizando available_topics y controles existentes; demostrar D01 y variante de otro dominio con Playwright real, teclado, pregunta pendiente conservada, permisos/retirada y borrado sin caché residual; no alterar salidas autorizadas ni reservas de interpretación. Origen: FR-005/009/013/014/023/026, US1/AC1 y SC-001/006 (partial).
- [X] T074 HIGH Dividir los24 diálogos actuales de T067 en bloques de revisión humana manejables con casos/pasos y respuesta exacta requerida; preparar propuesta explícita de disposición de pérdida histórica sin atribuir aprobación ni restauración; registrar evidencia de T073, validaciones pertinentes, analyze/converge y tabla íntegra actual. Origen: plan G1, FR-028/030/032 y T061/T067 (partial).


## Ampliación aclarada — conversación sin pantalla

La aclaración humana vuelve a abrir la aceptación de orientación; T073 fue una mejora visual y no se cuenta como paridad verbal. G1/T067 continúan sin aprobar. Se conserva el historial; las tareas siguientes son aditivas y dependientes en este orden.

- [X] T075 Registrar ampliación spec/clarify/plan/checklist y matriz24 casos sin interfaz, con fuente humana y gate G4 separado. FR-034–037, SC-010.
- [X] T076 Implementar contratos de contexto/nav y plantillas/política optativa versionadas; validar publicación/permisos y compatibilidad v1 sin reescribir actividades usadas. FR-017/018/027/034–036, plan H/I.
- [X] T077 Implementar orientación verbal, opciones máximo tres/paginación/repetición, elección/confirmación y aclaración sin ofrecer pregunta inexistente, con revalidación y negativos. FR-005/013/034, SC-010.
- [X] T078 Implementar procedencia audible y orientación de modos/ayudas/recuperación desde referencias vigentes, sin citas prohibidas ni bypass de SDV/T090. FR-008/014/015/035.
- [X] T079 Implementar conservación explícita propuesta/confirmada/cancelable y cierre conversacional, misma transacción/recibo y T150/límites; no inferir consentimiento de sí. FR-024/025/026/036.
- [X] T080 Implementar revisión/eliminación conversacionales posteriores al cierre solo para propietario, con scopes/caducidad/borrado existentes y sin nuevo contexto/turno ni resurrección. FR-026/036.
- [X] T081 Congelar y ejecutar recorridos nuevos de navegación sin interfaz en dos dominios/ambos modos, oráculos de siguiente acción/estado/permiso/consentimiento/fuentes; conservar primera ejecución y fallos, sin llamar voz real a transcripciones. FR-029/030/037, SC-010.
- [X] T082 Integrar recorrido textual sin pantalla en demostrador y documentar contrato/gate posterior G4, manteniendo vía accesible y límites de audio real pendientes. FR-023/034–037, plan J/G4.
- [X] T083 Ejecutar regresiones pertinentes/global/build/lint/Playwright/Black/Ruff estructural y regenerar/reproducir evidencia experimental separada al cambiar manifiesto; actualizar matriz y paquete humano sin aprobarlo, tabla completa, analyze/converge finales. FR-028/030/032/037, SC-010.
