# Cobertura de requisitos y aceptación

Cobertura de planificación; no evidencia de implementación.

| Requisito | Tareas |
|---|---|
| FR-001 | T023, T049, T054 |
| FR-002 | T005, T006, T014, T015 |
| FR-003 | T007, T008, T009, T014, T016, T019 |
| FR-004 | T010, T014, T015, T016, T019, T049 |
| FR-005 | T014, T015, T017, T019, T034 |
| FR-006 | T014, T018, T020, T024 |
| FR-007 | T014, T017, T020, T022, T024 |
| FR-008 | T012, T020, T022, T024, T029, T033, T049 |
| FR-009 | T016, T017, T019, T021, T024 |
| FR-010 | T020, T021, T024 |
| FR-011 | T020, T023 |
| FR-012 | T014, T015, T017 |
| FR-013 | T014, T016, T018, T024 |
| FR-014 | T010, T011, T019 |
| FR-015 | T010, T011, T034, T049 |
| FR-016 | T017, T022, T025, T026, T028, T034, T055 |
| FR-017 | T005, T006, T012, T013, T025, T027, T028, T029, T032 |
| FR-018 | T005, T006, T011, T012, T013, T018, T029, T032, T049, T051, T054 |
| FR-019 | T004, T028, T030, T031, T032, T039, T047, T050, T055 |
| FR-020 | T025, T026, T027, T034, T050 |
| FR-021 | T035, T036, T039 |
| FR-022 | T037, T038, T052 |
| FR-023 | T030, T033, T039, T042, T048 |
| FR-024 | T008, T009, T038, T040, T041, T042, T049 |
| FR-025 | T004, T013, T040, T042, T049, T054 |
| FR-026 | T009, T037, T038, T043, T044, T049, T054 |
| FR-027 | T001, T006, T007, T008, T025, T027, T035, T041, T044, T052, T053, T056 |
| FR-028 | T001, T030, T044, T045, T047, T051, T053 |
| FR-029 | T002, T003, T031, T045, T046, T048, T055 |
| FR-030 | T003, T032, T045, T046, T047, T050, T051, T054, T055, T056 |
| FR-031 | T004, T031, T048, T050, T052 |
| FR-032 | T001, T007, T008, T031, T052, T053, T056 |

| Criterio | Tareas / verificación |
|---|---|
| SC-001 | T002, T014, T019, T020, T024, T048 |
| SC-002 | T003, T015, T045, T046 |
| SC-003 | T002, T003, T016, T045, T046 |
| SC-004 | T012, T029, T043, T049 |
| SC-005 | T017, T020, T024, T045 |
| SC-006 | T035–T042, T052 |
| SC-007 | T004, T031, T045, T047, T053 |
| SC-008 | T047, T050, T054–T056 |

Los cuatro escenarios de aceptación de cada US se ejecutan respectivamente en T014–T019 (US1), T020–T024 (US2), T025–T034 (US3), T035–T042 (US4) y T043–T050 (US5), con ejecución completa T046/T048 y publicación T047. La matriz acceptance-matrix.md detalla los oráculos y negativos. Requisitos de seguridad sin tolerancia se mantienen aunque el umbral de interpretación sea 44/48.


## Ampliación de herramientas

| Requisito/criterio | Tareas |
|---|---|
| FR-033 | T057, T058, T059, T060 |
| SC-009 | T057, T058, T059, T060 |

FR-026/029 también cubiertos por T057; FR-018 por T058; FR-024/026/028 por T059; FR-029/030 por T060. US5 se amplía con comprobación de llamadas y efectos además de diálogo.


## Convergencia de orientación y revisión

T073: FR005/009/013/014/023/026, US1/AC1, SC001/006; selección por API vigente y confirmación con pregunta conservada. T074: FR028/030/032 y plan G1; bloques humanos y propuesta de disposición, sin aprobar T061/T067. Evidencia actual en orientation-validation/report.md.


FR-034: T075–077/T081–083. FR-035: T075/T076/T078/T081–083. FR-036: T075/T076/T079–083. FR-037/SC-010: T075/T081–083. Decisiones H–J y G1b/G4: T075–083. Cuatro escenarios adicionales: T077/T078/T079/T080, verificados T081/T083.

FR-038 → T084/T085/T089; FR-039 → T084/T086/T087/T089; FR-040 → T086–089; FR-041/SC-011 → T084/T088–090. Decisiones K/L: T084–090.

FR-042 → T091–093/T095; FR-043 → T091/T093–095; SC-012/decisión M/tres escenarios de tablas → T091–095. Trazas002/FR002/006–008/010–011 y010/FR015–020/032/041.

FR-044:T096/T097/T105; FR-045:T097/T098/T104; FR-046:T098/T099; FR-047:T099–102; FR-048:T102; FR-049:T096/T103/T105; FR-050:T100/T101/T104/T105; SC-013:T098–104; SC-014:T096/T103/T105. Decisiones N–Q:T096–105.

FR051:T108/T111/T112;FR052:T108/T109/T112;FR053:T109/T112;FR054:T110/T112;FR055:T106/T107/T112/T114;FR056:T113/T114;SC015:T107–114;decisionesR–T:T106–114.

FR051/052:T116–118/T120;FR053:T119/T120;FR054:T118/T120;FR055/SC015:T115/T120;FR056:T121;decisionesU–V:T115–121.

FR051/052:T124–127;FR053:T127;FR054:T123/T127;FR055/SC015:T122/T127;FR056:T126/T128;decisionesW–X:T122–128.
