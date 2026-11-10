# Tabla completa de 114 tareas —continuidad natural, 21-10-2026

107 completadas; siete pendientes. Evidencia T001–T105 referida a la raíz de Feature010; evidencia T106–T114 en natural-continuity. Los pases técnicos no aprueban revisión humana ni exceptúan T061.

| Tarea | Estado | Evidencia |
|---|---|---|
| T001 | Completada | evidence-baseline.json; pre-implementation-source.zip; 409 source files and 229 historical package files hashed |
| T002 | Completada | 12 development cases frozen; development-05: 12/12 public conversations, actual provider; original two sequences retained. |
| T003 | Completada | Original 12 dialogues/48 inputs frozen and executed; second 12/48 frozen before subsequent changes. First failures retained; no human utility claim. |
| T004 | Completada | capability-baseline.json; local-generation-study.json (9 real calls); operational-rehearsal/result.json: 33.687 s first observed, 16.141 s subsequent; not verified cold. |
| T005 | Completada | tests/contract/test_dialogue_contract.py; v1 compatibility tests and real T090 binding negatives |
| T006 | Completada | Closed v2 contracts/GuidedGenerationPort plus backward-compatible v1; public typed button controls and negative extra-field contracts. |
| T007 | Completada | tests/integration/test_dialogue_context_migration.py: clean, upgrade, rollback, legacy snapshot |
| T008 | Completada | t010_dialogue_context migration, models and typed snapshot/StatePatch; temporary DB tests only |
| T009 | Completada | dialogue_context_service; five tests: CAS, cancellation, closure, foreign/forged reference, outer rollback and linked T090 |
| T010 | Completada | test_dialogue_retrieval/context/authorization: reference ambiguity, query continuity and source revocation |
| T011 | Completada | dialogue_retrieval_service: original literal separate, current course/version/recipient/scope, cache revocation regression |
| T012 | Completada | test_dialogue_authorization, test_dialogue_generative_gate, public source projection and malicious hint tests; independent T090 rejects free/hash-signed candidates. |
| T013 | Completada | guided_dialogue_service + reviewed_unit_renderer: trusted DB bindings, independent agent gates then T090; existing final gate and T150 retained. |
| T014 | Completada | test_dialogue_study.py public API historical sequence and five modes; development-05 full 12 conversations. |
| T015 | Completada | Fourth first reserved cycle: 46/48 act classifications, all 36 critical correct; 48/48 public permission probes. Two ordinary failures retained; heuristic, not general Spanish comprehension. |
| T016 | Completada | context.py + revoked-context public tests: active reference sanitization, composition retirement, bounded stall count; current grants/material validation. |
| T017 | Completada | Self-study composer integrated; five mode tests and observed public development conversations, no favorable generator stub. |
| T018 | Completada | test_dialogue_coherence.py; exact requested repeat and strict reviewed-unit focus exception preserve contradiction checks; 18 reopened/unit tests pass. |
| T019 | Completada | Public study controls, greeting/deixis, ambiguity and confirmed-topic tests plus development corpus; broader language gate remains T015/T055. |
| T020 | Completada | Historical public defense sequence plus test_dialogue_claim_followup.py: initial 3 expected missing-anchor failures; 9 final cross-domain/condition/unit/forgery/erasure cases pass. |
| T021 | Completada | Published objective references and original pending question drive selection; claim anchor links owned input to reviewed same-goal question. Numeric/control tokens cannot become goals. |
| T022 | Completada | Reviewed question three-hint ladder; malicious labeled safe-hint public test blocks answer disclosure in both modes; independent SDV v2. |
| T023 | Completada | Condition/approximation/Celsius-Fahrenheit and second-domain claims remain separate from reviewed source. Fixed approved condition question, assessment always not_assessed; 9 public cases pass. |
| T024 | Completada | Protected content-answer follow-up linked to participant turn, teacher relationship, same subgoal and current source IDs; validated ownership, pending anchors, recovery and erasure. |
| T025 | Completada | test_dialogue_teaching_units: draft/review/publication/successor/retirement/source and API role negatives |
| T026 | Completada | materiales/docente/dialogue: two editable v1 packs and sources; 5 objectives, 5 examples, 5 comparisons, 5 questions with 3 hints per domain; not installed in prepared demo |
| T027 | Completada | teaching_unit_service and teacher-guarded API; explicit review, immutable successor, source and first-use guards |
| T028 | Completada | GuidedGenerationPort, reviewed-unit adapter and pure policy integrated; actual provider labels, closed references, no free candidate authority. |
| T029 | Completada | Actual independent Grounding/Coherence/SDV v2 execute before T090; source-policy and malicious-hint negatives pass both modes. |
| T030 | Completada | DialogueCapabilities + backend projections expose actual fixed/renderer/legacy adapter, allowed modes, readiness and pending human validation. |
| T031 | Completada | local-generation-study.json: 9 actual local Ollama calls, 3 per case, no fallback/download/publication; G2 NOT_APPROVED |
| T032 | Completada | generative-gate.md; 8 deterministic adversarial candidates tested twice each through T090, 8 pytest pass 1.11 s. Nine real LLM study calls separate; G2 not approved. |
| T033 | Completada | Both modes: malicious safe-hint, source projection and privacy matrix; complete browser review/JSON/Markdown/export/delete flows; 21 Playwright pass on current integration. |
| T034 | Completada | Readiness validates current published objectives/question/hints and policies; UI shows readiness limits and concrete mode/action alternatives; original short material unchanged. |
| T035 | Completada | test_dialogue_preflight.py: recipient/policy errors before participant/session/governance/lock; public closed error code |
| T036 | Completada | Preflight checks current recipient/activity/readiness before participant/session/lock writes; public negative matrix tests. |
| T037 | Completada | test_dialogue_recovery.py: owner, foreign/missing grants, confirmed teacher close, no token reissue/identity disclosure. |
| T038 | Completada | SessionRecovery, owner find/resume and teacher checkbox-close integrated; real Playwright recovery and no extra turn. |
| T039 | Completada | Text route and keyboard-operable DialogueActions, actual capabilities/pending question; both modes exercised through browser. |
| T040 | Completada | test_dialogue_requests.py: duplicate payload, conflict, cancellation/rollback, concurrent same request, expiry and late replay; six cases 12.22 s checkpoint. |
| T041 | Completada | Atomic request receipts, asynchronous operation lease, owner-only GET and current T090 replay; in-memory unknown-result browser reconciliation. |
| T042 | Completada | Failure tests cover cancellation/lease/budget/unique close; public request receipts plus unknown-result keyboard reconciliation; all 21 browser cases pass. |
| T043 | Completada | test_dialogue_privacy.py: 24 scope/mode/closure combinations plus 2 expiry/purge; no new-content reconstruction. |
| T044 | Completada | Privacy purge removes context and receipts; retention/export use existing scopes, UI clears retained caches; public deletion and expired replay negatives. |
| T045 | Completada | runner.py records real public outcomes and independent persisted ownership/proposal/T090/source/state oracles; no favorable response substitution. |
| T046 | Completada | Both reserved cycles executed once and failures published; second 12/12 dialogue, 30/48 acts (22/36 critical). Failed cases reopened as development; G1 remains failed. |
| T047 | Completada | first-reserved-summary.json, second-reserved-summary.json, paired-summary.json and per-case reports distinguish mode/domain/provider/critical denominators. |
| T048 | Completada | test_guided_dialogue.spec.ts (2) + test_guided_privacy.spec.ts (4), actual backend and provider; full rerun in progress. |
| T049 | Completada | 1080 global deterministic tests pass; negative authorization/source/hint injection, revocation, timeout, missing resources, conflicts and stale replay. Real LLM feasibility kept separate. |
| T050 | Completada | docs/DEMO.md updated with controlled provider, authoring, recovery, unknown-result handling, scopes, measured operation and G1/G2/G3 limits. |
| T057 | Completada | 16 frozen reviewed synthetic tool cases (8 development/8 reserve), operation/role/scope/effect oracles and first mapping freeze retained. |
| T058 | Completada | test_synthetic_tool_runner.py: 9 oracle tests; wrong operation, role, arguments, state, response, status and unobserved success rejected; not actual scenario execution |
| T059 | Completada | tool_runner.py observes actual public method/path/payload/role/status and persistent effects; non-replacing renderer/catalog/interpreter spies; labeled fault injection only. |
| T060 | Completada | Original reserve failures and later harness failures preserved; final 8 development + 8 fresh reviewed cross-mode reserve scenarios all pass, 16/16 in 28.31 s, tools-verified-16 reports. |
| T051 | Completada | Última global del mismo backend:1139 aprobadas/879 omitidas/1 aviso,227,65s (sin repetición en pase UI). Playwright actual23/23 en4,5min; build/lint aprobados. Black del test afectado sin cambios; Ruff multiplicidad10 heredados/0 nuevos. orientation-validation/report.md. |
| T052 | Completada | Migration clean/upgrade/rollback/legacy snapshots pass globally; operational-rehearsal/result.json ordinary PowerShell + offline socket guard, own start/stop twice, untouched personal DB/demo, no Reset. |
| T053 | Pendiente / puerta abierta | 204 current cells and replay match all four intact experimental packages; 24 current pairs each condition 24/24 content properties, no superiority claim. Six historical browser files remain lost (T061), so preservation cannot close. |
| T054 | Pendiente / puerta abierta | 33 FR, 9 SC, 11 constitutional principles and 37 checklist items assessed; T090/T150/privacy technical suites pass. Constitutional preservation contradiction remains T061; human system review pending. |
| T055 | Pendiente / puerta abierta | G0 técnico aprobado. Clasificación reservada ciclo7 48/48 y 36/36 críticas; 12W aprobados en primera ejecución ciclo5, ramas sin cambios verificadas y reproducción actual. Revisión humana G1 pendiente, preservación T061 abierta. G2 no aprobado; G3 pendiente. |
| T056 | Pendiente / puerta abierta | Postimplementation analyze/converge cannot be clean while T061 and human system review remain. No completion asserted. |
| T061 | Pendiente / puerta abierta | Búsqueda independiente: 41.595 archivos, 2.112 candidatos por contenido, 37 comprimidos y 2.990 miembros; cero SHA coincidentes. Sin copia recuperable identificada. Revalidación nueva 3/3 (revalidation-20261019-162715), manifiesto nuevo verificado y guard229/0 cambios; no restaura originales. No se pide ruta desconocida; disposición de la pérdida pendiente. |
| T062 | Completada | Both real composers, five modes, independent provider/verifiers/T090, pending question, three hints and claim-linked neutral follow-up integrated. Historical public sequences and cross-domain tests pass. |
| T063 | Completada | Authorized preflight, owner resume/teacher confirmed close, atomic receipts/reconciliation, capabilities and keyboard UI; normal-shell rehearsal and current full browser checks pass. |
| T064 | Completada | 26 privacy scope/mode/closure/expiry cases plus claim erasure and malicious hint tests; current full 23-case browser run includes retained and ephemeral/resumed sessions, JSON/Markdown and deletion. |
| T065 | Pendiente / puerta abierta | 24 diálogos actuales D+W, 48 clasificaciones Y, 48 pruebas públicas de permisos, 16 herramientas y 24 pares reales; contenido 24/24 en ambas condiciones. Replay204 coincide. Revisión humana/preservación impiden cierre. |
| T066 | Completada | Playwright actual23/23; orientation-validation/green-preservation.json verifica229 archivos y cero cambios nuevos. T061 continúa sin restauración. |
| T067 | Pendiente / puerta abierta | D01 anterior requiere corrección según human-review-D01-corrections-2026-10-20.md. El sucesor D01-corrected-for-human-review.md y otros23 esperan revisión humana; no se infiere aprobación de continuar. |
| T068 | Completada | Regresión roja preservada; objeto de repetición, negaciones, órdenes compuestas, ayudas conjugadas y saludo; contratos y API pública. semantic-audit-before-r2.xml / semantic-corpora-verified.xml. |
| T069 | Completada | Comparación conserva objetivo; coherencia distingue sujetos/predicados y mantiene negativos de contradicción. Pruebas nuevas de falsa contradicción y casos D02/D06/W-H06. |
| T070 | Completada | Límite específico ante formatos protegidos; permiso practice_reveals_solution docente respetado, separado de permiso de cita. Matriz API ambos modos/permisos y pruebas de no revelación. |
| T071 | Completada | 24 casos auditados por IA y paquete humano vigente sin aprobación; reserva ciclo7, global1139, browser21, Black114/Ruff0 nuevos, paquete experimental actual y replay204. Primeros fallos preservados. |
| T072 | Completada | Quinta reserva46/48 y sexta47/48 conservadas; séptima nueva48/48 (36 críticas), sin ajustes posteriores; 1150 combinaciones de contexto W equivalentes y 12W reproducidos. 48 pruebas públicas actuales pasan. |
| T073 | Completada | DialogueTopics junto al diálogo: temas actuales, propuesta y confirmación por la orden fija confirmo. Playwright real agua/programa, teclado, pregunta pendiente conservada, cambio y cierre efímero; suite completa23/23 en4,5min. Retirada/controles3/3 en10,99s, build/lint correctos, Black del único Python afectado sin cambios y Ruff estructural10 heredados/0 nuevos. orientation-validation/. |
| T074 | Completada | human-review-blocks/:6 bloques×4 casos, criterios y respuesta requerida, todos No evaluado. Propuesta explícita no aprobada en preservation-incident/loss-disposition.md. Evidencia, inventario y analyze/converge actuales en orientation-validation/report.md y analysis-convergence-orientation-current.md. T061/T067 siguen abiertas. |
| T075 | Completada | spec/plan/checklist ampliados FR034–037/SC010; screenless-baseline preserva intención anterior; screenless-matrix-baseline y human-review-voice-parity registran brecha sin aprobar D01. |
| T076 | Completada | Context schema2 optativo y serializer v1 compatible; guided-screenless/v1, catálogo fijo, publicación negativa de permisos incompletos; tests/integration/test_screenless_dialogue.py. |
| T077 | Completada | Opciones de tres, paginación/repetición, selección/confirmación actual, desconocidos/ambigüedad; confirmación explícita por nombre no sustituye tema pendiente; negativos ambos dominios. |
| T078 | Completada | Fuente de turno propio aprobado y TraceEvent concordante; título/sección/versiones actuales, revocación, SDV independiente bloquea el metadato sintético «100» inyectado y alterna mensajes de límite; sin cita protegida. |
| T079 | Completada | Propuesta/confirmación/cancelación por alcance y plazo; sí no consiente, confirmaciones de tema/cierre/privacidad independientes, rollback y recibos, cierre sin material vigente y T150 preservado. |
| T080 | Completada | Endpoint owner-only cerrado, scope/caducidad, revisión propia, borrado explícito y no reconstrucción; docente403 y sin cookie401; sin crear turno/contexto al revisar cerrado. |
| T081 | Completada | screenless-freeze.json, fuente571 antes de reserva; 4/4 reserva primera y 4/4 desarrollo actual, 14 pasos/caso. Primeros fallos preservados; producción/corpus no cambiaron después de reserva. screenless-reserve-integrity.json. |
| T082 | Completada | Dos casos Playwright reales ocultan paneles y completan recorrido por transcripciones; consola tras cierre elimina texto local, quickstart/contratos/data-model y G4-audio-gate documentan audio pendiente. |
| T083 | Completada | screenless-validation/report.md y summary.json: global1166/911omitidas, navegador25/25, build/lint, Black121, Ruff10 heredados/0 nuevos; experimento comparable204/0 errores y replay coincide. Matriz24/197pasos y seis bloques humanos nuevos, todos No evaluado. Analyze sin contradicciones críticas de intención; converge conserva T061/T067, sin declarar cierre. |
| T084 | Completada | human-review-D01-corrections-2026-10-20.md, didactic-human-review-status.json: D01 humano requiere corrección en versión revisada. FR038–041/SC011, K/L, siete criterios de checklist y cuatro corpus congelados antes de cada cambio. |
| T085 | Completada | guided-screenless/v2 optativa; plantillas aditivas de saludo y visión general, publicación exige permisos completos. V1 y materiales originales permanecen compatibles e intactos. |
| T086 | Completada | pedagogy.py clasifica cláusula/predicado/objeto/contexto de forma acotada; diferencia nombre/causa/proceso/posibilidad/condiciones, negación y coordinación. Aísla variantes del plan genérico; repetición accede a salida íntegra. PH04 regresión demuestra que comprobación anterior a almacenamiento no es almacenamiento. |
| T087 | Completada | Materiales ficticios sucesores agua-v2/programa-v2:21 variantes explicativas nuevas, publicación por API real y relaciones docentes cerradas. Mismos tipos/subobjetivos y cobertura; sin DDL o bypass de fuentes/T090/no revelación. Son propuestas de IA, no revisión didáctica humana. |
| T088 | Completada | 19 pruebas de núcleo: propósito, pasos, cambio de estrategia, literalidad, foco frente a complemento, ausencia de mecanismo, defensa protegida, política incompleta, compatibilidadv1, selección genérica y compatibilidad entre variantes. Calidad se comprueba aparte de publicación; primeros fallos conservados. |
| T089 | Completada | didactic-validation/report.md y summary.json:1185Python/931omitidas,27Playwright,24diálogos/197pasos,20casos didácticos/68pasos. Última reserva4/4 en primera ejecución; primeras3/4 y3/4 conservadas. Black123/Ruff10heredadas/0nuevas; build/lint, paquete204/replaycoincidente. Fuente582 sin cambios durante validación final. |
| T090 | Completada | D01-corrected-for-human-review.md: siete pasos reales completos y matriz de seis criterios humanos. human-system-review-didactic-current.md y seis bloques actuales, sin aprobación inferida. Analyze/converge en analysis-convergence-didactic-current.md mantiene T061/T067 y dependientes. |
| T091 | Completada | FR042/043/SC012, decisión M, checklist y table-extraction-baseline; siete regresiones rojas de ocho y copias SHA de entradas ficticias externas. La comparación con extractores anteriores confirma omisión24celdas en Word programa y24en PPTX12. |
| T092 | Completada | DocxExtractor recorre cuerpo Paragraph/Table en orden, celdas por fila/columna, combinadas desde origen y anidado≤4 con error explícito. Contexto160por referencia, valor íntegro; párrafos/localizaciones previos preservados. |
| T093 | Completada | PptxExtractor recorre shapes/grupos y tablas nativas; coordenadas y texto literal007/1000/3,5. Notas nunca se leen; solo notas no es procesable. La tabla externa sigue nativa y sus24celdas se localizan en diapositiva12. |
| T094 | Completada | 17pruebas pertinentes (13núcleo/API+4archivos externos): SQLite/Chroma/embeddings locales reales aislados, activación requerida, curso/actividad, UUID/texto/cita/versiones, sucesora/retiro/deactivación. docs/LECTURA-DE-MATERIALES.md explicita notas/exclusiones y versionado; no incorpora210propuestas del paquete. |
| T095 | Completada | table-extraction-validation/report.md:1198Python/935omitidas,27Playwright, build/lint, Black134rutas, Ruff10heredadas/0nuevas,204celdas/replaycoincidente. Fuente593sin cambios;229históricos/0nuevos cambios ySHAhabituales iguales. Analyze/converge mantiene T061/T067 y dependencias, no cierre. |
| T096 | Completada | receipt.json/original-manifest.json:21originales SHA iguales; FR044–050/SC013–014/decisiones N–Q/checklist y dialogue-freeze.json antes de ajustes. |
| T097 | Completada | Overlays v1/v2/v3inmutables, manifiestos y overlay-detailed-diff.json;15unidadesPPTX/13PDFcon suplemento explícito; originales intactos. |
| T098 | Completada | bindings-v3-lifecycle-first:4formatos/cursos,18documentos y342instancias de unidades por corrida; UUID/versión/cita íntegros reales, curso ajeno vacío, sucesora/retiro y repetición obsoleta denegada. |
| T099 | Completada | package_fixture.py exige TestClient propio/BD temporal test_/publicación explícita. Práctica separada; sin primer fragmento ficticio, guías u oráculos. Negativos fuente inexistente/cliente no autorizado y no revelación v3. |
| T100 | Completada | package_dialogue.py/política v3optativa: propósito, saludo, objetivo confirmado, tres apoyos distintos ordenados y límite fuera de fuente.8desarrollo/8reserva aprobados sin ajuste lógico sobre reserva; compatibilidad v1/v2. |
| T101 | Completada | coherence_propositions.py/contrato2.2.0 distingue sujetos/predicados/negación/condiciones/valores escalares/repetición. Negativos independientes bloquean contradicción real, candidato copiado, condiciones ausentes y pista con solución. No nuevo agente ni DDL. |
| T102 | Completada | 16conversaciones/348intervenciones APIreales con pregunta pendiente, fuentes y conservación8/efímero8; efectos de cierre/revisión/borrado verificados; sin STT/TTS. |
| T103 | Completada | 60estímulos expuestos/80instancias:80/80;8desarrollo+8reserva nueva:16/16. Primeros69/80,59/80,79/80y6/8preservados; fuente congelada antes de reserva, transcriptos completos. |
| T104 | Completada | validation/summary.json:1224Python/941omitidas,27Playwright,32pertinentes, build/lint, Black144/Ruff10heredadas/0nuevas; PowerPoint nativo13exportadas;204celdas/0errores/replaycoincidente.619fuentes estables,229históricos/0cambios nuevos y6pérdidas previas. |
| T105 | Completada | README.md,24bloques humanos, validation/report.md y task-evidence-complete.md: tabla105tareas/98completadas y análisis/convergencia. No aprobación humana/docente/audio ni excepción de preservación; siete tareas anteriores abiertas. |
| T106 | Completada | audit-receipt.json; spec FR051–056/SC015; plan R–T; checklist72/72. |
| T107 | Completada | corpus-freeze.json; reserve-second-freeze.json; reserve-third-freeze.json; development6 y reservas congeladas. |
| T108 | Completada | continuity.py; unit tests; audit-prefixes0/3→3/3; development-v7-first6/6; reserved-v4-third-first6/6. |
| T109 | Completada | materiales/docente/integracion-controlada-20261020-v7; manifiestos v1–v7; seguimiento específico y alternativas acotadas sin eximir verificadores. |
| T110 | Completada | continuity_navigation.py; test_continuity_pending_controls.py12casos; global1250; estados/efectos reales. |
| T111 | Completada | GREETED_REVIEWED_RESPONSE; renderer/snapshot; test_dialogue_authorization.py;29pruebas dirigidas; global/PW. |
| T112 | Completada | development-v7-first6/6; reserve-first-exposed-v7-regression6/6; reserved-v4-third-first6/6; primeros fallos; human-review-natural-current.md15bloques/98pasos. |
| T113 | Completada | validation/report.md/summary.json;1250Python,27PW,Black151,Ruff0nuevo; evidence-natural-20261021/replay; source-natural-verified-20261021.json/ZIP; preservation-final.json. |
| T114 | Completada | task-evidence-complete.md114filas; validation/modified-files.md; artifact-inventory-natural-current.json; postimplementation-audit.json; analysis-convergence-current.md; revisión humana/pérdida pendientes. |
