# Registro final de informes y evidencias relacionadas

Una entrada documental no equivale a un ensayo independiente. Los extractos siguientes son afirmaciones de los informes originales; la interpretación independiente está en informe.md e inventario-ensayos.md. Enlaces relativos rebasados a la fuente. Copias exactas se agrupan por hash; ensayos semánticamente repetidos se agrupan en el inventario interpretado.

## specs/001-core-cognitive-runtime/constitution-conformance-review.md

[Fuente](../../../specs/001-core-cognitive-runtime/constitution-conformance-review.md)

Revisión de la **implementación real** (no solo del plan) de la Feature 001 frente a
cada principio de `.specify/memory/constitution.md`. `plan.md` ya contiene una
Constitution Check previa al diseño; este documento la revalida después de escribir el
código.

- | VIII. Trazabilidad y reproducibilidad | `TraceEvent` + `StatePatch` append-only permiten reconstrucción completa incluso tras un reinicio simulado (`test_session_reconstruction_after_restart.py`); ningún campo almacena razonamiento privado de modelo (no hay LLM). | PASS |
- automatizada pendiente por falta de Node.js en este entorno) — no bloquea el Principio

Recibos vecinos: 

## specs/001-core-cognitive-runtime/quickstart-validation-evidence.md

[Fuente](../../../specs/001-core-cognitive-runtime/quickstart-validation-evidence.md)

Ejecutado contra una base de datos SQLite temporal, seed de demostración
(`oralia.scripts.seed_demo`), y la app FastAPI real (sin mocks del framework HTTP).
Escenario E se cubre mediante la prueba automatizada
`tests/integration/test_session_reconstruction_after_restart.py`, que sí simula un
reinicio real (motor SQLAlchemy y app completamente nuevos contra el mismo archivo).

- ejecución de referencia (239 passed, 49 errores de Ruff) también corrió, con alta
- **Suite determinista (001+002+003, sin Ollama real)**:
- 239 passed, 1 deselected, 1 warning in 71.23s (0:01:11)
- passed!") — el archivo que esta ronda modifica parte limpio de Ruff.
- que distinguir en esta ejecución (0 de 239 fallaron); el único ruido (el warning de
- falsos positivos de H02 encontrados y corregidos en la ronda 4 (ver más abajo) son
- ## Seguimiento de H02 — 3 falsos positivos corregidos (001/T091, ronda 4, 2026-09-11)
- Antes de esta tarea:  255 passed, 1 deselected

Recibos vecinos: 

## specs/002-materials-rag/constitution-conformance-review.md

[Fuente](../../../specs/002-materials-rag/constitution-conformance-review.md)

Revisión de la **implementación real** de la Feature 002 frente a cada principio de
`.specify/memory/constitution.md`. `plan.md` ya contiene una Constitution Check previa al
diseño; este documento la revalida después de escribir el código.

- | IV. Separación recuperación/generación/decisión/verificación | Esta feature implementa el rol "retriever" real; `GroundingVerifierAgent` es un verificador independiente que nunca decide la acción conversacional final (responsabilidad de la Feature 003). | PASS |
- | XI. Simplicidad evolutiva | Segmentador propio (~80 líneas) en vez de un framework de chunking; heurística determinista de conflicto (solapamiento léxico + marcadores de negación) en vez de un modelo NLI; bloqueo de reconstrucción reutiliza literalmente el patrón ya validado de `session_lock_service.py` en vez de inventar uno nuevo. | PASS |
- accesibilidad automatizada pendiente por falta de Node.js en este entorno) — no bloquea

Recibos vecinos: 

## specs/002-materials-rag/quickstart-validation-evidence.md

[Fuente](../../../specs/002-materials-rag/quickstart-validation-evidence.md)

Ejecutado contra una base de datos SQLite temporal, un directorio ChromaDB persistente
temporal, y la app FastAPI real (sin mocks del framework HTTP ni del motor de embeddings
— se usó el adaptador `sentence-transformers` real, con `HF_HUB_OFFLINE=1` tras la
descarga inicial del modelo).

- la consola de este entorno lo renderiza de forma distinta, verificado independientemente

Recibos vecinos: 

## specs/003-self-study-agency/constitution-conformance-review.md

[Fuente](../../../specs/003-self-study-agency/constitution-conformance-review.md)

Autoevaluación (T093) contra `.specify/memory/constitution.md` v1.0.0, tras completar
la implementación (T001–T088) y con la suite en verde (239 pruebas, `-m "not ollama"`).

- (verificador independiente, contrato/umbral/traza propios — research.md §4); las
- (tercera implementación independiente de la técnica de solapamiento léxico, research.md

Recibos vecinos: 

## specs/003-self-study-agency/quickstart-validation-evidence.md

[Fuente](../../../specs/003-self-study-agency/quickstart-validation-evidence.md)

Ejecutado el 2026-09-02 contra una instancia real (`uvicorn`) con una base de datos
SQLite/ChromaDB efímeras, dedicadas a esta validación (`quickstart_smoke.db` +
`quickstart_smoke_vectors/`, migradas con `alembic upgrade head` y eliminadas al
finalizar). Sin Ollama configurado — `DeterministicGenerationAdapter` en todo momento.

- determinista reutiliza el mismo texto que en el Escenario A, `CoherenceVerifierAgent`
- autorizado, de forma determinista y reproducible, en:
- regeneración con el contenido determinista de este corpus). Fila `PracticeQuestion`
- `CoherenceVerifierAgent`, no reproducible de forma determinista vía curl manual sin
- camino "Ollama caído tras estar configurado" está cubierto de forma determinista y
- `ended_at` retrasado artificialmente) está cubierto de forma determinista y reproducible
- ✅ **239 passed, 0 failed** (ver T095/T096 para el desglose y la confirmación final de
- (A, C, G, purga) y 3 mediante la suite automatizada determinista donde la reproducción

Recibos vecinos: 

## specs/004-oral-defense-agency/analysis-report.md

[Fuente](../../../specs/004-oral-defense-agency/analysis-report.md)

Revisión final: 2026-10-17. Skill `speckit-analyze`; fase de análisis de solo lectura.
Prerequisitos: `check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` PASS.
No hay `.specify/extensions.yml`. Constitución 1.0.0 sin modificaciones.

- | — | Revisión final | — | spec.md, plan.md, tasks.md y constitución | Sin hallazgos pendientes | Cierre de implementación permitido |
- | Ambigüedades pendientes | 0 |
- | Duplicaciones contradictorias pendientes | 0 |
- La cobertura mide escenarios deterministas y contratos de voz con dobles. No acredita
- Siguiente acción: ninguna corrección obligatoria pendiente. La validación opcional de
- ## Revisión tras reapertura por auditoría independiente
- Evidencia final: 16 casos HTTP de límites × modalidad × scopes; 766 pruebas deterministas
- SpecKit posterior conserva 61/61 requisitos cubiertos y cero hallazgos críticos pendientes.

Recibos vecinos: 

## specs/005-teacher-governance/analysis-report.md

[Fuente](../../../specs/005-teacher-governance/analysis-report.md)

Fecha: 2026-10-17. Skill speckit-analyze, revisión de solo lectura finalizada.

- | — | Consistencia | — | spec/plan/tasks/contratos | Sin contradicciones críticas ni hallazgos pendientes | Implementar tareas |
- La revisión final y converge quedan pendientes de código y resultados ejecutados.
- 0 ambigüedades pendientes, 0 duplicaciones bloqueantes y 0 críticos.
- y requirement-coverage.md. Puertas: 818 deterministas, 10 navegador, 2 migraciones,

Recibos vecinos: 

## specs/006-architecture-validation/analysis-report.md

[Fuente](../../../specs/006-architecture-validation/analysis-report.md)

Revisión de solo lectura concluida; documento archivado después. Sin extensions/hooks.
16 FR +6 SC, 17 tareas,5 historias/10 escenarios,11 principios,28 ítems checklist.
Cobertura22/22(100%),0 tareas sin correspondencia,0 críticos/ambigüedades/contradicciones
pendientes. Los riesgos tienen tareas: aislamiento/bypass, mediciones falsas, condiciones
no comparables, hashes/replay, resultados negativos, rollback y fugas. Modelo determinista
y corpus lexical limitan inferencias explícitamente. No se requiere migración ni permiso
nuevo: herramienta local sintética dentro del alcance autorizado. Proceder implement.

- pendientes. Los riesgos tienen tareas: aislamiento/bypass, mediciones falsas, condiciones
- no comparables, hashes/replay, resultados negativos, rollback y fugas. Modelo determinista
- nuevo: herramienta local sintética dentro del alcance autorizado. Proceder implement.
- pendientes; toda tarea tiene requisito o gate. Cobertura en requirement-coverage.md.
- lock offline, build/lint y10Playwright aprobadas. Una advertencia Starlette/httpx y un
- según el alcance local/sintético especificado. La voz real y piloto humano permanecen
- no medidos; tampoco se presenta el proveedor determinista como benchmark de LLM/Chroma.

Recibos vecinos: 

## specs/006-architecture-validation/contracts/validation-cli.md

[Fuente](../../../specs/006-architecture-validation/contracts/validation-cli.md)

`uv run python -m oralia.validation run --output <new-directory> --repetitions 2 --seed 42 --authorize-synthetic-ablations`

- Solo catálogo sintético incorporado. Sin flag, baseline/full; flag autoriza condiciones

Recibos vecinos: 

## specs/006-architecture-validation/evidence/report.md

[Fuente](../../../specs/006-architecture-validation/evidence/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/006-architecture-validation/evidence/protocol.json), [results.json](../../../specs/006-architecture-validation/evidence/results.json)

## specs/007-local-demonstration/analysis-report.md

[Fuente](../../../specs/007-local-demonstration/analysis-report.md)

Análisis de solo lectura completado antes de archivar este informe, 2026-10-18.
Prerequisitos PowerShell resueltos a specs/007-local-demonstration; sin extensions.yml.

- validados y evidencia sintética. Checklists evalúan especificación, no suplantan ensayos.
- Acción siguiente: cerrar converge contra implementación y evidencia, sin remediación pendiente.

Recibos vecinos: 

## specs/007-local-demonstration/converge-report.md

[Fuente](../../../specs/007-local-demonstration/converge-report.md)

Revisión append-only completada antes de archivar este informe. Sin extensions.yml.
Resultado: la implementación satisface spec, plan y tareas;0 brechas obligatorias.

- No se confunde generación determinista ni fallos inyectados con validación humana/voz.
- archiva el cierre. No quedan tareas de implementación pendientes ni commits solicitados.

Recibos vecinos: 

## specs/007-local-demonstration/evidence006-current/report.md

[Fuente](../../../specs/007-local-demonstration/evidence006-current/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/007-local-demonstration/evidence006-current/protocol.json), [results.json](../../../specs/007-local-demonstration/evidence006-current/results.json)

## specs/008-demo-startup-progress/analysis-report.md

[Fuente](../../../specs/008-demo-startup-progress/analysis-report.md)

Análisis read-only completado antes de archivar este informe. Prerequisitos PowerShell:
FEATURE_DIR=specs/008-demo-startup-progress; spec/plan/tasks existentes; sin extensions.yml.

- hashes medidos; timeouts/cancelación reales; regresiones globales y paquete sintético;

Recibos vecinos: 

## specs/008-demo-startup-progress/converge-report.md

[Fuente](../../../specs/008-demo-startup-progress/converge-report.md)

Revisión append-only finalizada antes de archivar este informe; sin extensions.yml.
La implementación satisface spec, plan y tareas;0brechas obligatorias.

- No quedan tareas obligatorias pendientes. Demo preparada full y detenida,puertos libres,

Recibos vecinos: 

## specs/008-demo-startup-progress/evidence-current/report.md

[Fuente](../../../specs/008-demo-startup-progress/evidence-current/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/008-demo-startup-progress/evidence-current/protocol.json), [results.json](../../../specs/008-demo-startup-progress/evidence-current/results.json)

## specs/009-long-extractive-binding/analysis-report.md

[Fuente](../../../specs/009-long-extractive-binding/analysis-report.md)

Revisión read-only completada antes de archivar. Prerequisitos PowerShell correctos,
sin extensions.yml.14requisitos,16tareas,100% cobertura,0huérfanas;3historias/8escenarios
más los casos normal/lento/error de la aclaración FR-006/SC-003;25/25checklists.

- estado externo;verificadores independientes;fuente vigente antes de derivar valor;
- T016 responde al hallazgo de carga inicialmente lenta:observación independiente15s,
- Código Python de producción coincide con manifiesto009:921deterministas y204replay
- Sin remediaciones ni contradicciones críticas pendientes. Proceder converge final.

Recibos vecinos: 

## specs/009-long-extractive-binding/audit-upload-followup/audit-failed-context.md

[Fuente](../../../specs/009-long-extractive-binding/audit-upload-followup/audit-failed-context.md)

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

-       - heading "Conflictos pendientes de revisión (FR-022a)" [level=3] [ref=f1e24]
-       - paragraph [ref=f1e25]: No hay conflictos pendientes.

Recibos vecinos: 

## specs/009-long-extractive-binding/converge-report.md

[Fuente](../../../specs/009-long-extractive-binding/converge-report.md)

Revisión append-only finalizada antes de archivar. Sin extensions.yml.16tareas,
14requisitos,8escenarios base más normal/lento/error,11principios revisados.

- La observación independiente y cierre anterior se preservan;no se inventa causa del
- Cero brechas obligatorias de implementación local;la revisión independiente es separada.

Recibos vecinos: 

## specs/009-long-extractive-binding/evidence-current/report.md

[Fuente](../../../specs/009-long-extractive-binding/evidence-current/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/009-long-extractive-binding/evidence-current/protocol.json), [results.json](../../../specs/009-long-extractive-binding/evidence-current/results.json)

## specs/010-guided-dialogue/analysis-before-implementation.md

[Fuente](../../../specs/010-guided-dialogue/analysis-before-implementation.md)

Análisis de solo lectura de spec, plan, tasks, contratos, matriz, riesgos y constitución 1.0.0. Prerrequisitos: FEATURE_DIR=specs/010-guided-dialogue; research, data-model, contracts, quickstart y tasks disponibles. Sin extensions.yml ni AGENTS.md encontrados.

- Cobertura: 33/33 FR referenciados en tasks y requirement-coverage; 9 SC; 60 tareas únicas pendientes. T057 precede a implementación de herramientas; T058 precede runner; T060 precede cierre. Ningún requisito sin cobertura ni contradicción crítica detectados. G0/G1 obligatorios; G2 estudio puede concluir negativo; G3 pendiente. Autorización T090 sigue independiente y contextual; no permiso por hash del candidato ni cambio constitucional. La revisión documental no acredita cumplimiento del producto.
- Checklists de diseño: requirements 16/16; dialogue-safety 21/21; ninguna pendiente. Implementación sigue incompleta.

Recibos vecinos: 

## specs/010-guided-dialogue/analysis-convergence-didactic-current.md

[Fuente](../../../specs/010-guided-dialogue/analysis-convergence-didactic-current.md)

Estado: **no converged**;83/90tareas completadas. Se comprueban41FR,11SC,30escenarios,12decisiones A–L,11principios y52elementos de checklist completos. Analyze no detecta contradicciones críticas entre artefactos de intención. Esa conclusión no elimina la contradicción de preservación ya registrada contra la constitución.

- | Hallazgo vigente | Tipo | Severidad | Fuente | Evidencia y trabajo pendiente |
- | T067 | partial | HIGH | plan G1; FR016/030/041; SC011 | D01 anterior tiene revisión humana negativa: requiere corrección. Sucesor completo corregido listo, pero revisión humana pendiente; otros23 no aprobados. |
- T053/T054/T055/T056/T065 dependen de esas puertas y permanecen abiertos. La comparación pareada previa se conserva como evidencia de su versión, sin atribuir superioridad al contenido didáctico nuevo. No se detecta una brecha nueva de construcción en la ampliación revisada y no se duplican tareas que ya cubren el trabajo pendiente. No se declara cierre ni converged por acumular tests.
- La selección genérica excluye variantes de propósito salvo repetición, que necesita todas las referencias aprobadas. Los subobjetivos conservan cobertura completa y los tipos de unidad existentes; no hay DDL nuevo ni agente nuevo. Publicación valida permisos completos del sucesor. Cada unidad vuelve a validar curso/tema/actividad/fuentes y el renderer/verificadores/T090 deciden publicación; defensa/práctica protegida no revelan mecanismos study_only. La preparación usa API docente de pruebas explícita y datos ficticios; el contenido nuevo es propuesta de IA, no revisión didáctica humana.
- La revisión pasada D01 ya no se trata como No evaluado: didactic-human-review-status.json registra requires_correction en el predecessor y pending en el sucesor. Las otras23 conversaciones no reciben aprobación por esta corrección. El plan G1 exige literalmente: «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». No se inventa una aprobación automática para sustituir ese requisito.
- -evidence-didactic-verified-20261020:204celdas/0errores y replay coincide. didactic-experiment-comparison.json verifica protocolo/resultados estructurales iguales a006–009 y anteriores010; no demuestra suficiencia didáctica ni voz/utilidad.
- Reconocimiento/repertorio didáctico finitos; no se afirma comprensión general ni calidad para cualquier formulación. Los tests de pertinencia pueden fallar aunque pase publicación, pero no son revisión humana independiente. G2 generativo no se habilita, G3 utilidad y G4audio real siguen pendientes. La corrección textual no prueba STT/TTS, silencios/interrupciones ni audio efímero. No se integra ningún paquete docente de otra auditoría sin revisar fuentes y publicar una sucesora.

Recibos vecinos: 

## specs/010-guided-dialogue/analysis-convergence-orientation-current.md

[Fuente](../../../specs/010-guided-dialogue/analysis-convergence-orientation-current.md)

19-10-2026. Comprobación de solo lectura;33 FR,9 SC,20 escenarios,7 decisiones y11 principios.42 requisitos/criterios con cobertura;74 tareas únicas y tabla completa74 IDs;67 completas. Checklists37/37 (21 seguridad y16 requisitos). Sin requisitos huérfanos ni contradicciones críticas entre los artefactos de intención. Spec, plan y constitución no modificados. No hooks configurados.

- | T061 | contradicts | CRITICAL | FR027/028/032, ConstituciónVIII/X | Seis archivos históricos perdidos; originales no encontrados. SHA originales intactos, revalidación nueva separada. Propuesta de disposición lista, sin decisión ni enmienda normativa inferidas. |
- | T067 | partial | HIGH | plan G1, FR016/030 | Seis bloques de cuatro diálogos preparados con criterios y respuesta requerida; todos No evaluado. La auditoría IA no cumple la revisión humana explícita. |
- Converge: **no converged**. La brecha accionable de orientación se implementó mediante T073; la preparación concreta de decisiones mediante T074. No hay brechas de construcción nuevas identificadas en esta revisión; las dos existentes ya tienen tareas, no se duplican ni se añade una fase vacía. tasks.md no se modifica durante analyze/converge. T053/T054/T055/T056/T065 siguen parciales por preservación y revisión humana.

Recibos vecinos: 

## specs/010-guided-dialogue/analysis-convergence-package-current.md

[Fuente](../../../specs/010-guided-dialogue/analysis-convergence-package-current.md)

Estado: **no converged;98/105 tareas completadas**. Revisados50 FR,14 SC,17 decisionesA–Q,11 principios y65 ítems de checklist completos. Analyze no encuentra contradicciones críticas nuevas de intención. Converge no encuentra una obligación nueva de construcción sin cubrir en T096–105; las siete tareas existentes siguen cubriendo puertas sin resolver. No se añade una fase vacía o tareas duplicadas y no se declara cierre.

- | T067 | partial | HIGH | El plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». D01 anterior requiere corrección; sucesor y otros 23siguen pendientes.16 conversaciones nuevas y60 estímulos expuestos no equivalen a revisión humana. |
- FR044/T096–097/T105: recepción21SHA, sucesoras separadas con diff y fuentes explícitas; originales/manifiesto y datos/procesos habituales conservados. Mantener010 evita abrir otra feature conG1pendiente; no reforma constitucional.
- FR047–048/T099–102: selección v3 optativa por propósito/objetivo/contexto, tres apoyos relacionados y límite fuera de fuente; coherencia v3independiente con negativos de contradicción/condición/copia del candidato. No revelación también rechaza pista mal etiquetada en v3.16 conversaciones/348 intervenciones completas de autoestudio/defensa y estados de conservación/cierre/revisión/borrado reales. No se atribuye audio a transcripciones.
- Los límites del analizador finito, suplementos y revisión docente están explícitos. Una unidad publicada o testigo literal no demuestra suficiencia didáctica. El baseline mantiene las seis pérdidas y el estado humano anterior, sin limpiar o reinterpretar el resultado negativo.

Recibos vecinos: 

## specs/010-guided-dialogue/analysis-convergence-screenless-current.md

[Fuente](../../../specs/010-guided-dialogue/analysis-convergence-screenless-current.md)

Estado: **no converged**, Feature010 abierta. Se inspeccionan37 FR,10 SC,24 escenarios de aceptación,10 decisiones A–J y11 principios constitucionales.45 elementos de checklist completos, cero pendientes;83 tareas únicas,76 completadas. Analyze no encuentra contradicciones críticas **entre artefactos de intención**. Esto no elimina la contradicción de preservación ya registrada contra la constitución.

- Estado: **no converged**, Feature010 abierta. Se inspeccionan37 FR,10 SC,24 escenarios de aceptación,10 decisiones A–J y11 principios constitucionales.45 elementos de checklist completos, cero pendientes;83 tareas únicas,76 completadas. Analyze no encuentra contradicciones críticas **entre artefactos de intención**. Esto no elimina la contradicción de preservación ya registrada contra la constitución.
- | T067 | partial | HIGH | plan G1, FR016/030/037 |24 transcripciones actuales y seis bloques disponibles; todos No evaluado por personas. Obtener revisión humana explícita por caso/paso. |
- FR034 → navigation_catalog/screenless_navigation_service, orientación tres/página, selección pendiente y confirmación, revalidación; T076–077/T081. FR035 → fuentes desde turno propio aprobado y referencias actuales, ayudas/modos/recuperación y SDV independiente; T078. FR036 → preferencias propuestas/confirmadas/cancelables, mismo recibo/transacción/T150, endpoint cerrado autenticado y sin creación de contexto/turno; T079–080. FR037/SC010 → matriz24/197pasos, corpus congelado ocho recorridos, Playwright sin paneles y gate G4 explícito; T075/T081–083.
- - screenless-runs/original-24-final/:24 diálogos y197 pasos originales, no reserva nueva. human-system-review-screenless-current.md y human-review-screenless-blocks/: revisión humana pendiente.

Recibos vecinos: 

## specs/010-guided-dialogue/analysis-convergence-semantic-current.md

[Fuente](../../../specs/010-guided-dialogue/analysis-convergence-semantic-current.md)

19-10-2026. Análisis de solo lectura sobre spec.md, plan.md, tasks.md y constitución. Inventario:33 FR,9 SC,20 escenarios,7 decisiones,11 principios; cobertura de requisitos/tareas100%;72 IDs únicos,65 completados. Sin requisitos huérfanos ni contradicción crítica entre artefactos de intención. Sin hooks configurados.

- | T061 — pérdida histórica | CRITICAL | FR027/028/032, ConstituciónVIII/X | Seis archivos sobrescritos; originales no encontrados. Revalidación nueva aprobada y manifiestos preservados no restauran los bytes perdidos. Disposición explícita de incidencia pendiente. |
- | T067 — revisión de sistema | HIGH | plan G1, FR016/030, SC001–008 | human-system-review-current.md contiene24 transcripciones y rúbrica sin evaluar. La auditoría IA no satisface revisión humana. |
- T068–T072 ejecutadas y evidenciadas en task-evidence.md. G0 técnico pasa con1139 pruebas,21 Playwright, build/lint, Black114/Ruff0 nuevos; clasificación48/48 y36críticas, permisos48/48, diálogos24/24 y herramientas16/16, comparación24 pares, replay204. G1 requiere revisión humana; G2 no disponible y G3/voz real no validados. No se declara finalizada la feature.

Recibos vecinos: 

## specs/010-guided-dialogue/analysis-convergence-tables-current.md

[Fuente](../../../specs/010-guided-dialogue/analysis-convergence-tables-current.md)

Estado: **no converged**;88/95tareas completadas. Se revisan43FR,12SC,33escenarios,13decisiones A–M,11principios y58elementos de checklist completos. Analyze no detecta contradicciones críticas entre artefactos de intención. Converge no detecta una brecha nueva de construcción en la corrección tabular; las tareas existentes siguen cubriendo las puertas pendientes.

- Estado: **no converged**;88/95tareas completadas. Se revisan43FR,12SC,33escenarios,13decisiones A–M,11principios y58elementos de checklist completos. Analyze no detecta contradicciones críticas entre artefactos de intención. Converge no detecta una brecha nueva de construcción en la corrección tabular; las tareas existentes siguen cubriendo las puertas pendientes.
- | Hallazgo vigente | Tipo | Severidad | Fuente | Evidencia pendiente |
- | T067 | partial | HIGH | plan G1; FR016/030/041 | D01 anterior requiere corrección según revisión humana; sucesor y otros23 esperan revisión. La comprobación de extracción no los aprueba. |
- T053/T054/T055/T056/T065 permanecen abiertos por esas dependencias. No se duplican las tareas ni se reinterpretan pérdidas como restauración ni se declara converged por totales de pruebas. El plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema»; esta fase no sustituye ese requisito.
- FR042/T091–093: DOCX/PPTX incorporan tablas nativas, orden documental/fila/columna, coordenadas de origen y literalidad007/1000/3,5. DOCX conserva párrafos anteriores, combinadas/anidado≤4 y error explícito sin indexación parcial. PPTX conserva texto/diapositiva, recorre grupos y omite celdas spanned. Contexto estructural≤160por referencia sin truncar la celda principal ni declarar cabeceras semánticas.

Recibos vecinos: 

## specs/010-guided-dialogue/contextual-relevance/analysis-convergence-current.md

[Fuente](../../../specs/010-guided-dialogue/contextual-relevance/analysis-convergence-current.md)

**No converged; 114/121 tareas completadas.** Revisados 56 FR, 15 SC, 22 decisiones A–V, 11 principios y 77 ítems de checklist. Los seis hallazgos HIGH de construcción de la auditoría v4/v7 se registraron en Phase 10/T115–121; no se redujeron a revisión humana. La conclusión anterior de 107/114 se conserva como histórica y refutada.

- **No converged; 114/121 tareas completadas.** Revisados 56 FR, 15 SC, 22 decisiones A–V, 11 principios y 77 ítems de checklist. Los seis hallazgos HIGH de construcción de la auditoría v4/v7 se registraron en Phase 10/T115–121; no se redujeron a revisión humana. La conclusión anterior de 107/114 se conserva como histórica y refutada.
- | A03/1: lectura perdida tras saludo |T118: ambas cláusulas, valores literales de serieA y plantilla autorizada de saludo. |
- Analyze no detecta contradicciones críticas nuevas de intención. Converge no descubre otra obligación de construcción conocida sin cubrir dentro de los casos auditados y sus variantes. No se añade fase vacía ni duplicados. **Esto no es una afirmación de que todas las conversaciones naturales o los 100 turnos fijos hayan sido aceptados.** Reconocimiento finito y evaluación acotada; G1 humano pendiente. El alcance de las pruebas no demuestra comprensión general o suficiencia didáctica humana.
- | T067 | partial | HIGH | Plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». D01 histórico negativo no se borra; revisión sucesora y bloques adicionales pendientes. |
- T053/T054/T055/T056/T065 permanecen abiertas como tareas dependientes. No aprobación G2 generativa, G3 utilidad o G4 voz. No commits, Reset, activación en demo habitual ni modificación de datos/procesos ajenos. Fuente final de 673 archivos, datos habituales y 229 históricos actuales preservados, con seis pérdidas iniciales todavía registradas.

Recibos vecinos: 

## specs/010-guided-dialogue/contextual-relevance/validation/report.md

[Fuente](../../../specs/010-guided-dialogue/contextual-relevance/validation/report.md)

La auditoría independiente v4/v7 invalidó la conclusión técnica anterior de 107/114. Se conservaron sus 100 capturas y el control v3 separado, se registraron seis hallazgos HIGH y siete tareas de construcción/validación T115–121, y se corrigieron casos reproducibles con pruebas de tema/proceso/propósito/objeto/estado. No se atribuyen 76 fallos independientes a un guion que diverge ni se presenta captura como aceptación.

- La auditoría independiente v4/v7 invalidó la conclusión técnica anterior de 107/114. Se conservaron sus 100 capturas y el control v3 separado, se registraron seis hallazgos HIGH y siete tareas de construcción/validación T115–121, y se corrigieron casos reproducibles con pruebas de tema/proceso/propósito/objeto/estado. No se atribuyen 76 fallos independientes a un guion que diverge ni se presenta captura como aceptación.
- | Global |1260 passed, 944 skipped, 1 warning en 335,81 s |
- La omisión global incluye corridas optativas ejecutadas por separado. La advertencia conocida es Starlette/httpx. Duraciones observadas no son una comparación de rendimiento ni estimación de carga inicial/fría. Las 204 celdas son evidencia arquitectónica determinista; no evalúan suficiencia didáctica humana, aprendizaje ni audio.
- Las respuestas orales sintéticas se eligen por la pregunta efectivamente emitida. Si no hay pregunta reconocible, el runner registra divergencia antes de inventar que el participante ha respondido a otra. Tres preguntas de seguimiento distintas y agotamiento se verifican en los tres dominios; no se divulgan unidades de solución o autoestudio. Permiso incompleto de saludo o agotamiento no habilita continuidad.
- [Lista de 25 rutas de fuente nuevas/modificadas](../../../specs/010-guided-dialogue/contextual-relevance/validation/modified-files.md), respecto a la entrega verificada anterior de 658 archivos. Materiales v1–v7 y originales se conservan. v8 agrega dos unidades de decimal y su suplemento, propuesta pendiente de revisión humana. La publicación técnica solo ocurre en SQLite temporal propia, con testigos literales/UUID/versiones reales. Fuente congelada en source-contextual-before-reserve-20261021.json/ZIP; no se reescribe la fuente natural anterior.
- [Transcriptos íntegros de 12 bloques / 74 pasos](../../../specs/010-guided-dialogue/contextual-relevance/human-review-contextual-current.md), todos pendientes de revisión humana. El resultado negativo histórico de D01 no se borra ni se sustituye por «no evaluado». No se infiere G2 generativo, G3 utilidad o G4 voz.
- Los fallos de pertinencia eran técnicos, no pendientes humanos; preimplementation-findings.json y Phase 10 conservan ese diagnóstico. La primera suite de navegador termina con 26 pases / 1 fallo en 4,7 min: no apareció confirmación de borrado. El contexto se conserva en browser-first-failure. La captura no prueba su causa; el test no esperaba habilitación del botón ni respuesta DELETE antes de verificar el texto. Se añade esa sincronización y assert HTTP 200 real, sin ampliar plazos ni modificar la aplicación. post-reserve-source-diff.json acredita que solo cambia ese archivo E2E, sin cambios de producción/Python/corpus. La reserva semántica permanece sobre la misma producción y no se presenta la repetición como reserva nueva. La suite final y la preservación se registrarán al terminar. T061 CRITICAL conserva seis pérdidas históricas sin restauración ni excepción; T067 HIGH exige revisión humana de G1. Ningún pase de estas correcciones cumple esas puertas. No commits, Reset, descargas ni manipulación de procesos o datos habituales.
- Cuarto intento: gobierno pasa con borrado/logout reales; el escenario básico busca la burbuja a los 5 segundos mientras sigue pendiente el envío. Se conserva el contexto y log interrumpido. El comprobador espera ahora HTTP 200 de turno/cierre/listado y verifica la salida real, además de limpiar solo su sesión temporal ante fallo. No cambia la aplicación ni sus plazos. Ambas pruebas dirigidas pasan 2/2 en 57,3 s con arranque. La suite completa final usa source-contextual-browser4-20261021.json/ZIP; el diff final2 contiene exclusivamente dos archivos E2E, sin cambios de producción/Python/corpus posteriores a la reserva.

Recibos vecinos: 

## specs/010-guided-dialogue/didactic-decision-log.md

[Fuente](../../../specs/010-guided-dialogue/didactic-decision-log.md)

La revisión humana de D01 fue parcial y negativa: requiere corrección. Se conserva el documento fuente y la transcripción revisada. Versiones nuevas siguen pendientes de revisión humana; no volver a presentar la versión defectuosa como No evaluado.

- La revisión humana de D01 fue parcial y negativa: requiere corrección. Se conserva el documento fuente y la transcripción revisada. Versiones nuevas siguen pendientes de revisión humana; no volver a presentar la versión defectuosa como No evaluado.
- La primera prueba independiente detectó insuficiencia en proceso de agua/programa; los primeros tests tenían además una aserción blocked impropia del esquema de autoestudio (corregida sin cambiar salida). Las variantes inicialmente publicadas encontraron falsos conflictos léxicos del verificador independiente: cláusulas compatibles compartían nombres y distinta negación. No se relajó el verificador; se revisó la redacción de los materiales sucesores para expresar con precisión afirmativa el mismo contenido, manteniendo contestación negativa directa cuando procede, alcance y fuentes. Los borradores y resultados previos se conservan. Esto es una limitación del verificador léxico, no prueba de comprensión semántica general.
- Primera reserva didáctica:3/4 aprobadas; PH04 falla al confundir el objeto comprobación con el complemento almacenamiento. No se cuenta como aprobada ni se reutiliza como reserva nueva. Se promueve a regresión y se congela un segundo ciclo nuevo antes de corregir. La aceptación humana y los gates T061/G3/G4 son independientes de estos resultados.
- Segundo ciclo3/4: PJ03 pide definición después de proceso y el verificador bloquea una formulación compatible con negación. Se revisa redacción afirmativa equivalente sin cambiar el agente. Se comprueban por pares las variantes del mismo tema para detectar conflictos léxicos internos antes de otra reserva. El tercer ciclo4/4 se conserva; la regresión posterior PH04 revela que faltaba una alternativa de definición ante una restricción reiterada. Se añade esa unidad publicada, sin sustituirla por ejemplo. Además se aísla la selección genérica de las variantes de propósito, preservando acceso íntegro al repetir literalmente; una primera versión del filtro eliminó referencias necesarias para repetir y falló nueve pruebas. La corrección queda demostrada en16 recorridos expuestos y19 pruebas de núcleo (35aprobadas/4omitidas).
- Un global intermedio detectó correctamente un cambio de manifiesto entre creación y replay experimental mientras se editaba código:1183aprueban/1falla/927omitidas. Es un fallo de coordinación de validación, no se relaja la comprobación de integridad. La validación de entrega se ejecuta con fuente congelada y sin editar código, tests ni materiales hasta terminar. También se conserva el primer global didáctico1179/919omitidas y los pases de27Playwright sobre versiones intermedias; no se cuentan como validación de la última fuente.

Recibos vecinos: 

## specs/010-guided-dialogue/didactic-validation/report.md

[Fuente](../../../specs/010-guided-dialogue/didactic-validation/report.md)

La revisión humana anterior de D01 **requiere corrección**. Se conserva ese resultado; el sucesor espera revisión humana, y los otros23 casos no se consideran aprobados. Se implementan FR038–041/SC011 con política optativa `guided-screenless/v2`, materiales ficticios sucesores y el mismo perfil `guided_controlled`. No se cambia arquitectura, agentes, autenticación, T090/T150, consentimiento o recursos personales.

- La revisión humana anterior de D01 **requiere corrección**. Se conserva ese resultado; el sucesor espera revisión humana, y los otros23 casos no se consideran aprobados. Se implementan FR038–041/SC011 con política optativa `guided-screenless/v2`, materiales ficticios sucesores y el mismo perfil `guided_controlled`. No se cambia arquitectura, agentes, autenticación, T090/T150, consentimiento o recursos personales.
- [**D01 completo, siete pasos, listo para revisión humana**](../../../specs/010-guided-dialogue/D01-corrected-for-human-review.md). [Matriz24](../../../specs/010-guided-dialogue/didactic-matrix-current.md), [transcripciones sucesoras24](../../../specs/010-guided-dialogue/human-system-review-didactic-current.md) y [seis bloques](../../../specs/010-guided-dialogue/human-review-didactic-blocks/README.md).
- | Global Python completo |1185 aprobadas,931 omitidas,1 aviso de deprecación;265,43s |
- | Núcleo y regresiones expuestas |19 pruebas de núcleo y16 recorridos expuestos pasan:35 aprobadas/4 omitidas;44,70s |
- | Última reserva nueva |4/4 en primera ejecución,13 pasos;pytest23aprobadas incluye19núcleo,16omitidas;25,69s |
- Se conservan dos globales intermedios:1179/919omitidas sobre una versión anterior y1183aprobadas/1fallo/927omitidas. El fallo del segundo es code/protocol integrity mismatch porque una edición coincidió con creación/replay del paquete en el test CLI. No se suprime esa protección. El global final se ejecutó sin editar código/tests/materiales y aprobó1185/931omitidas. Los tiempos entre pases no demuestran rendimiento superior ni carga fría.
- Reconocimiento y repertorio didáctico acotados a propósitos, relaciones y materiales publicados; no se demuestra comprensión general del lenguaje natural ni suficiencia para cualquier formulación/asignatura. Las nuevas unidades son propuestas docentes sintéticas de IA publicadas explícitamente en el entorno de pruebas; requieren revisión humana de contenido y didáctica. Los oráculos son independientes de publicación, pero no equivalen a validación humana independiente. La comparación pareada previa corresponde a una versión anterior: no se afirma superioridad del nuevo contenido.
- Perfil guiado controlado, no generativo G2 aprobado. Audio real STT/TTS, silencios/interrupciones y utilidad G3 siguen pendientes; ver G4-audio-gate.md. No hay descargas de modelos, compromisos de rendimiento, Reset ni commits. La demo preparada y los datos habituales se conservan; se entrega detenida. Persisten seis pérdidas históricas anteriores, sin restauración o excepción otorgada. T061/T067 y sus dependencias impiden el cierre de la feature:83/90tareas completadas.

Recibos vecinos: 

## specs/010-guided-dialogue/evidence-checkpoint-20261019/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-checkpoint-20261019/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-checkpoint-20261019/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-checkpoint-20261019/results.json)

## specs/010-guided-dialogue/evidence-contextual-20261021/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-contextual-20261021/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-contextual-20261021/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-contextual-20261021/results.json)

## specs/010-guided-dialogue/evidence-didactic-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-didactic-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-didactic-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-didactic-20261020/results.json)

## specs/010-guided-dialogue/evidence-didactic-current-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-didactic-current-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-didactic-current-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-didactic-current-20261020/results.json)

## specs/010-guided-dialogue/evidence-didactic-verified-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-didactic-verified-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-didactic-verified-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-didactic-verified-20261020/results.json)

## specs/010-guided-dialogue/evidence-integrated-20261019/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-integrated-20261019/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-integrated-20261019/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-integrated-20261019/results.json)

## specs/010-guided-dialogue/evidence-natural-20261021/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-natural-20261021/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-natural-20261021/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-natural-20261021/results.json)

## specs/010-guided-dialogue/evidence-package-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-package-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-package-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-package-20261020/results.json)

## specs/010-guided-dialogue/evidence-screenless-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-screenless-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-screenless-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-screenless-20261020/results.json)

## specs/010-guided-dialogue/evidence-screenless-comparable-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-screenless-comparable-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-screenless-comparable-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-screenless-comparable-20261020/results.json)

## specs/010-guided-dialogue/evidence-screenless-current-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-screenless-current-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-screenless-current-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-screenless-current-20261020/results.json)

## specs/010-guided-dialogue/evidence-semantic-current-20261019/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-semantic-current-20261019/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-semantic-current-20261019/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-semantic-current-20261019/results.json)

## specs/010-guided-dialogue/evidence-semantic-cycle7-20261019/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-semantic-cycle7-20261019/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-semantic-cycle7-20261019/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-semantic-cycle7-20261019/results.json)

## specs/010-guided-dialogue/evidence-sequence-20261021/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-sequence-20261021/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-sequence-20261021/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-sequence-20261021/results.json)

## specs/010-guided-dialogue/evidence-sequence-final-20261021/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-sequence-final-20261021/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-sequence-final-20261021/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-sequence-final-20261021/results.json)

## specs/010-guided-dialogue/evidence-sequence-verified-20261021/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-sequence-verified-20261021/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-sequence-verified-20261021/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-sequence-verified-20261021/results.json)

## specs/010-guided-dialogue/evidence-tables-20261020/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-tables-20261020/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-tables-20261020/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-tables-20261020/results.json)

## specs/010-guided-dialogue/evidence-verified-20261019/report.md

[Fuente](../../../specs/010-guided-dialogue/evidence-verified-20261019/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/010-guided-dialogue/evidence-verified-20261019/protocol.json), [results.json](../../../specs/010-guided-dialogue/evidence-verified-20261019/results.json)

## specs/010-guided-dialogue/manual-browser-audit-2026-10-18.md

[Fuente](../../../specs/010-guided-dialogue/manual-browser-audit-2026-10-18.md)

Observación directa por navegador, 2026-10-18 20:34 UTC. Instancia existente en http://127.0.0.1:5180; no se reinició, migró ni cerró ninguna sesión.

- # Comprobación independiente de la demo abierta
- - Inicio accesible; indica generación determinista, embeddings locales y voz real sin validar.
- Conclusión corregida: acceso web y actividades visibles comprobados. La negativa a abrir una segunda sesión era el funcionamiento esperado del límite de una sesión interactiva, no un defecto de inicio ni prueba de una regresión de Feature 010. La sesión anterior pertenecía a las pruebas del usuario. Separadamente, la demo servida no mostraba recuperación autorizada ni traducción completa del aviso; esa mejora de interfaz sigue relacionada con FR-022/023 y T037–T039/T063, sin justificar cierres automáticos ni ampliar concurrencia. Esta observación no prueba el estado de una build distinta ni acredita G1 ni los corpus sintéticos.
- Resultado verificado: closed_voluntary, bloqueo liberado y cero sesiones activas; se aplicó conservación efímera según la elección existente. No se creó otra sesión para dejar el acceso libre. El bloqueo operativo de esta comprobación queda resuelto; iniciar un diálogo nuevo y validar sus respuestas sigue pendiente. No registrar este caso como fallo de exclusión mutua ni como aceptación conversacional aprobada.

Recibos vecinos: 

## specs/010-guided-dialogue/natural-continuity/analysis-convergence-current.md

[Fuente](../../../specs/010-guided-dialogue/natural-continuity/analysis-convergence-current.md)

**No converged:107/114 tareas completadas.** Revisados56FR,15SC,20decisionesA–T,11principios y72ítems de checklist. Analyze no detecta contradicciones críticas nuevas de intención, duplicación material o obligaciones nuevas sin cobertura. Converge no detecta brechas nuevas de construcción fuera de las tareas existentes; no añade fase vacía ni duplica puertas abiertas.

- | Hallazgo | Tipo | Severidad | Evidencia / trabajo pendiente |
- | T067 | partial | HIGH | Plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». D01 histórico requiere corrección; revisión sucesora y otros bloques siguen pendientes. Los pases automáticos no cumplen este gate. |
- | FR053/T109/T112 | Pregunta original conservada; seguimiento publicado distinto, alumno sintético adaptado a pregunta emitida, sin calificar verdad de su afirmación ni revelar solución. |
- | FR055/SC015/T106–107/T112 |100capturas originales conservadas. Desarrollo, primeras reservas con fallos y tercera nueva6/6 antes de exposición. Oráculos externos de propósito/estado/fuente; stop ante divergencia. Transcriptos completos15bloques/98pasos actuales, revisión humana pendiente. |
- No nueva arquitectura/agente/modelo/DDL. Grounding/coherencia/no revelación y T090 siguen comprobando cada propuesta; no excepción basada en hash ni texto libre autovalidado. Publicación técnica reviewed=True no equivale a revisión didáctica humana. Una fuente literal no certifica suficiencia: los prefijos verifican la función de la definición y el contenido molecular, y la revisión humana permanece obligatoria.

Recibos vecinos: 

## specs/010-guided-dialogue/natural-continuity/validation/report.md

[Fuente](../../../specs/010-guided-dialogue/natural-continuity/validation/report.md)

Implementación técnica v4 en Feature010, con materiales sucesores v7 y API/compositor/verificadores reales. No activada en datos habituales. Los límites del planificador finito, la propuesta docente pendiente y los primeros fallos permanecen visibles.

- Implementación técnica v4 en Feature010, con materiales sucesores v7 y API/compositor/verificadores reales. No activada en datos habituales. Los límites del planificador finito, la propuesta docente pendiente y los primeros fallos permanecen visibles.
- | Global |1250 passed, 943 skipped, 1 warning, 303,47 s |
- | Black |151 archivos sin cambios pendientes |
- | Arquitectura sintética |204 celdas,0 errores; replay coincidente |
- La suite global omite corridas optativas que se ejecutaron por separado con sus variables y salidas nuevas. La advertencia es la deprecación de Starlette/httpx ya registrada; no es un fallo oculto. El experimento de 204 celdas es regresión arquitectónica determinista, no medida de calidad didáctica, aprendizaje, rendimiento mejorado o voz real.
- human-review-summary.json y [paquete íntegro de15 bloques/98 pasos](../../../specs/010-guided-dialogue/natural-continuity/human-review-natural-current.md) conservan salidas, fuentes, estados, verificación y pregunta realmente emitida. Revisión humana pendiente; D01 histórico negativo no se limpia. T061 CRITICAL y T067 HIGH impiden cierre, con cinco tareas dependientes abiertas. No G2 generativo, G3 utilidad ni G4 voz aprobados por estos pases.

Recibos vecinos: 

## specs/010-guided-dialogue/orientation-validation/report.md

[Fuente](../../../specs/010-guided-dialogue/orientation-validation/report.md)

T073/T074 terminadas;67/74 tareas. Se corrige una brecha de interfaz: la API y el panel de capacidades ya enumeraban los temas, pero la aclaración junto a la conversación no permitía seleccionarlos directamente. No se atribuye ausencia de opciones a todo el sistema ni error nuevo a la clasificación.

- DialogueTopics muestra temas actuales devueltos por API junto al diálogo, propone cambio mediante el control topic_switch existente y pide confirmación. Confirmar envía solo la constante «confirmo», nunca una orden generada desde el nombre docente; el servidor resuelve el tema pendiente y vuelve a validar. La pregunta actual se mantiene hasta confirmar. Sin estado local adicional; enviar/resultado desconocido deshabilitan los controles y cierre efímero elimina la superficie. No cambian backend, contratos, plantillas, permisos ni corpus reservado.
- - Playwright completo:23/23 en4,5min. Casos nuevos: agua32,6s, programa9,6s; backend real sin sustitución favorable. Prueban selección por teclado, confirmación, contenido fundamentado/coherente, pregunta pendiente y desaparición tras cierre efímero/404 de revisión.
- - Misma huella backend que evidence-semantic-current-20261019: verify_package pasa204 celdas. Se conserva el replay coincidente previo, sin repetirlo ni regenerarlo al no cambiar sus archivos. Igualmente, global1139 aprobadas/879 omitidas/1 aviso es la ejecución previa del mismo backend; no se presenta como reejecutada en este pase.
- La primera invocación `pnpm.cmd --dir apps/web run test:e2e -- test_guided_orientation.spec.ts --grep agua` no filtró: ejecutó23. Resultado21 aprobados/2 fallidos en5,4min: agua falló correctamente por ausencia de región accionable; programa agotó tiempo por bloqueo de sesión abandonada tras el primer fallo y no cuenta como fallo semántico independiente. Se cerró esa sesión ficticia a través de ruta docente pública confirmada, solo tras comprobar /e2e-fixture en8005; nunca se accedió a la API personal. Se añadió finally a cada caso nuevo para cerrar únicamente su session_id ante fallo. Log y contextos rojos conservados aquí.
- Fuente congelada source-orientation-20261019.json/zip:562 archivos. Documentación: docs/DEMO.md, quickstart.md, seis bloques humanos e índice, propuesta de disposición, tareas/evidencias y análisis actual. Los textos de los24 diálogos API no cambian; su revisión humana sigue pendiente. G2 no habilitado; voz real y G3 no validados. No se afirma mejora de rendimiento ni utilidad educativa.

Recibos vecinos: 

## specs/010-guided-dialogue/package-integration/validation/report.md

[Fuente](../../../specs/010-guided-dialogue/package-integration/validation/report.md)

La ampliación técnica queda implementada y validada en Feature010. **La feature sigue abierta:98/105 tareas completadas**, porT061/T067 y sus dependencias. [Tabla completa105filas](../../../specs/010-guided-dialogue/package-integration/task-evidence-complete.md), [analyze/converge](../../../specs/010-guided-dialogue/analysis-convergence-package-current.md), [detalle y reproducción](../../../specs/010-guided-dialogue/package-integration/README.md), [revisión humana24 bloques](../../../specs/010-guided-dialogue/package-integration/human-review-current.md).

- La ampliación técnica queda implementada y validada en Feature010. **La feature sigue abierta:98/105 tareas completadas**, porT061/T067 y sus dependencias. [Tabla completa105filas](../../../specs/010-guided-dialogue/package-integration/task-evidence-complete.md), [analyze/converge](../../../specs/010-guided-dialogue/analysis-convergence-package-current.md), [detalle y reproducción](../../../specs/010-guided-dialogue/package-integration/README.md), [revisión humana24 bloques](../../../specs/010-guided-dialogue/package-integration/human-review-current.md).
- | Global final, fuente congelada |1224aprobadas,941omitidas,1aviso;276,70 s |
- | Global previo de esta ampliación |1222aprobadas,941omitidas;275,70 s; antes de añadir2 negativos v3 |
- | Reserva independiente congelada |8/8 en primera ejecución;52,38 s. No ajustes lógicos posteriores |
- | Estímulos originales expuestos |60únicos/80 instancias,80/80;52,98 s. Solo desarrollo; calidad humana pendiente |
- La política guided-screenless/v3 se activa solo de forma explícita en actividades nuevas. Planificación acotada por cláusula/propósito/contexto, saludo, cambio confirmado de objetivo, tres apoyos ordenados y límite fuera de fuente. Coherencia2.2.0distingue propiedades/predicados/negación local/condiciones/listas, conserva bloqueos reales y no exime copiar el candidato a fuentes. Grounding corrige coordinación nominal/sujetosA/Bsin cambiar verificación por entidad, números o polaridad. Defensa conserva SDVindependiente: etiqueta safe_hint no autoriza soluciones. No se alteran T090/T150, localhost, autenticación, consentimiento o aislamiento.
- Los materiales y nuevas variantes son propuestas de IA pendientes de revisión docente. Generación de diálogo controlada/determinista, con ingestión/índice/embeddings locales reales ya preparados y API/compositor/verificadores reales. No se valida generación libre, STT/TTS/audio, comprensión semántica general, causalidad de los datos ficticios ni utilidad con personas. La cobertura literal, unidad seleccionada o groundingaprobado no bastan para acreditar calidad didáctica. El control de condiciones/contradicciones tiene vocabulario y reglas finitos documentados en el contrato.
- package-dialogues-v1.json y dialogue-freeze.json congelan8desarrollo/8reserva antes de implementación. [Fuente anterior a reserva](../../../specs/010-guided-dialogue/source-package-before-reserve-20261020.json) y ZIP del mismo nombre conserva el código anterior a la primera reserva. Tras8/8 en primera ejecución solo cambiaron formato/imports de producción y nuevas pruebas de ciclo/no revelación: post-reserve-diff.json acredita equivalenciaAST de producción excluyendo orden de imports. La fuente final619 queda en [congelación final](../../../specs/010-guided-dialogue/source-package-verified-20261020.json) y ZIP del mismo nombre, y no cambió durante global/experimento/replay. Repetir una reserva ya ejecutada mide regresión; no una nueva aceptación independiente.

Recibos vecinos: 

## specs/010-guided-dialogue/postimplementation-audit.md

[Fuente](../../../specs/010-guided-dialogue/postimplementation-audit.md)

Estado: implementación técnica validada; **no cierre ni converged**.

- | Preservación histórica incompleta | CRITICAL | 6/229 hashes distintos; incident.json conserva originales | T061, restauración exacta pendiente de copia |
- | Revisión humana de sistema sin realizar | HIGH | plan.md G1 exige revisión; human-system-review.md tiene 24 diálogos y rúbrica No evaluado | T067 explícita; pendiente de respuesta humana |
- Actualización de recuperación: la búsqueda independiente documenta 41.595 archivos, 2.112 candidatos por contenido, 37 comprimidos y 2.990 miembros, cero coincidencias exactas. No hay copia recuperable identificada; no se solicita una ruta desconocida. T061 permanece como pérdida de evidencia sin restauración acreditada, pendiente de disposición explícita de la incidencia. Detalle en preservation-incident/loss-disposition.md. Los hashes originales se conservan intactos.
- T061 no se marca restaurada y la revisión humana de sistema sigue independiente.
- - Global: 1139 aprobadas, 879 omitidas explícitamente (evaluaciones optativas), un aviso Starlette/httpx, 227,65 s.
- - Pareado: contenido 24/24 en ambas condiciones; 186 turnos por condición, mediana32 ms y máximo47 ms en ambas. La cobertura de verificadores independientes es distinta; no se afirma superioridad educativa ni mejora causal de rendimiento. paired-semantic-summary.json.
- - Revisión técnica IA: technical-dialogue-audit-current.md; revisión humana requerida: human-system-review-current.md, 24 diálogos y todos los campos No evaluado. G2 no habilitado; utilidad humana y voz real pendientes.

Recibos vecinos: 

## specs/010-guided-dialogue/preservation-incident/revalidation-20261019-162715/report.md

[Fuente](../../../specs/010-guided-dialogue/preservation-incident/revalidation-20261019-162715/report.md)

19 de octubre de 2026. Ejecución nueva, no restauración de originales. No se modifican sus hashes ni se declara T061 restaurada.

- Normal y lento comprueban carga del archivo 04 original, actividad docente, pregunta/respuesta con fuentes, cierre, revisión, exportaciones JSON/Markdown y borrado en datos de prueba. El caso lento verifica aviso de carga y rechazo de envíos duplicados. Error utiliza un archivo ficticio no admitido. Se inspeccionaron visualmente las tres capturas generadas. La interfaz muestra proveedor determinista y perfil de capacidad reducida: este recorrido no acredita diálogo guiado, generación libre, voz ni utilidad con personas.
- Esta revalidación aporta evidencia actual para los comportamientos probados. No recupera la ejecución histórica ni decide por el usuario la disposición de su pérdida; la revisión humana de los diálogos de Feature 010 es independiente.

Recibos vecinos: 

## specs/010-guided-dialogue/screenless-validation/report.md

[Fuente](../../../specs/010-guided-dialogue/screenless-validation/report.md)

Se implementan FR034–037 y SC010 mediante política optativa `guided-screenless/v1`, con el mismo perfil `guided_controlled`. Opciones verbales, fuentes, ayuda/modos, conservación confirmada, cierre, revisión propia y eliminación funcionan por texto/transcripción. El código anterior y las actividades usadas conservan su comportamiento. No se habilita un modelo generativo ni audio real.

- | Global Python (incluye diez Python e2e) | 1166 aprobadas, 911 omitidas, un aviso de deprecación; 307,24 s |
- El primer global completo reveló nueve fixtures T090/T150 con destinatarios ficticios no declarados (1154 pasan/9 fallan). Se declararon antes del primer uso, manteniendo pruebas negativas de salida bloqueada e inmutabilidad; no se modificaron los controles de producción. El global1139 anterior excluía los diez Python e2e; no era equivalente a la colección completa actual. Los fallos, reintentos y resultados anteriores se mantienen.
- No se midió una mejora de rendimiento. Los tiempos dependen de concurrencia de verificaciones; no son evidencia de carga fría ni de desconexión física. Los paquetes experimentales son sintéticos y no aprueban calidad conversacional, voz ni utilidad humana.
- Tabla completa en ../task-evidence.md:76/83 completadas. Matriz actual en ../screenless-matrix-current.md y24 transcripciones en ../human-system-review-screenless-current.md, organizadas en seis bloques nuevos. Revisión humana **No evaluado** en todos los casos. G4-audio-gate.md documenta STT/TTS, interrupciones/silencios y audio efímero todavía pendientes; no se descargaron modelos.
- Las bases habituales y fixtures conservan sus SHA; demo preparada y detenida, sin Reset ni commits. G0/G1 no se cierran: T061 conserva pérdida histórica no restaurada y T067 exige revisión humana explícita. No se atribuye esa aprobación a una orden de continuar. Véase ../analysis-convergence-screenless-current.md.

Recibos vecinos: 

## specs/010-guided-dialogue/sequence-continuity/analysis-convergence-current.md

[Fuente](../../../specs/010-guided-dialogue/sequence-continuity/analysis-convergence-current.md)

**No converged; 121/128 tareas completadas.** Se revisaron 56 FR, 15 SC, 24 decisiones A–X, 11 principios y 82 ítems de checklist. El análisis fue de solo lectura: spec, plan, tasks, coverage, quickstart, constitución, feature.json y nueve checklists conservan sus hashes antes/después. Este informe se escribe después como evidencia de implementación.

- | Saludo con aceptación y escritura | T125: cláusula académica conservada; aceptación no demuestra escritura; puente/causa/proceso docentes relacionados, sin afirmar operación ejecutada. |
- | Vinculación de cuatro formatos | T126: v9 primera 3/4 rechazada correctamente; v10 repara solo alias suplementario PPTX, conserva textos; API real 4/4 y 425 instancias; revisión humana pendiente. |
- | T067 | partial | HIGH | Plan G1 exige «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». D01 histórico negativo conservado; sucesores y bloques actuales pendientes. |
- T053/T054/T055/T056/T065 siguen abiertas como dependencias. Las 12 conversaciones actuales / 122 pasos y 36 primeras ejecuciones / 351 pasos están completas, todas pendientes de revisión humana. No se autoriza G2 generativo ni se acredita G3 utilidad con personas o G4 voz real. No commits, Reset o publicación en la demo habitual.

Recibos vecinos: 

## specs/010-guided-dialogue/sequence-continuity/validation/report.md

[Fuente](../../../specs/010-guided-dialogue/sequence-continuity/validation/report.md)

La auditoría v4/v8 refuta la suficiencia técnica de114/121. Se preservan76archivos de captura, las cuatro brechas reportadas y trece hallazgos de construcción S1–S13. Los primeros fallos y regresiones introducidas durante la reparación permanecen visibles; no se rebajan a revisión humana.

- La auditoría v4/v8 refuta la suficiencia técnica de114/121. Se preservan76archivos de captura, las cuatro brechas reportadas y trece hallazgos de construcción S1–S13. Los primeros fallos y regresiones introducidas durante la reparación permanecen visibles; no se rebajan a revisión humana.
- | Pruebas dirigidas / permisos / operaciones / propiedades |154 passed,71,37s |
- | Global final |1364 passed,945 skipped,1 warning,334,73s |
- | Playwright completo |27 passed,3,5min,exit0; guardia229archivos sin cambios |
- Las945omisiones incluyen corridas optativas ejecutadas separadamente. Advertencia conocida de Starlette/httpx. Duraciones observadas con recursos locales preparados y corridas concurrentes de validación: no comparación de rendimiento, carga fría o estimación de voz. Las reservas son sintéticas y de autoría del implementador; no se presentan como revisión humana independiente ni generalización a toda conversación natural. Cada reserva expuesta se identifica como regresión. Las cinco conversaciones que pasaron en una reserva no convierten la experiencia completa fallida en aceptación.
- Transcriptos actuales:12bloques/122pasos. Primeras ejecuciones históricas:36bloques/351pasos. Todos humanos pendientes; el D01 humano negativo anterior sigue vigente. G2 generativo no habilitado; G3 utilidad con personas y G4 voz real pendientes. Las204celdas prueban arquitectura determinista, no suficiencia didáctica ni aprendizaje.
- T061 crítico por seis pérdidas históricas sin copia y T067 por revisión humana siguen abiertos, junto a cinco tareas dependientes. Ninguna preservación nueva restaura esas pérdidas ni aprueba excepción. Feature010 no está cerrada.

Recibos vecinos: 

## specs/010-guided-dialogue/table-extraction-validation/report.md

[Fuente](../../../specs/010-guided-dialogue/table-extraction-validation/report.md)

Se corrige una omisión verificable: DOCX solo recorría párrafos y PPTX solo cuadros de texto. Ahora se extraen tablas nativas en orden, con coordenadas de tabla/fila/columna y literalidad. No se modificaron los cuatro documentos originales ni se incorporaron sus propuestas al entorno habitual. Las notas de presentador siguen excluidas; solo notas no hace procesable un archivo.

- | Global Python completo |1198 aprobadas,935 omitidas,1 aviso de deprecación;297,39s |
- Esos ensayos no publican las210unidades propuestas ni las guías/oráculos del docente, no ejecutan sus60casos o conversaciones del tercer dominio, y no aprueban el contenido del paquete. Incorporarlo requiere fuentes/UUID/versiones reales y validación conversacional por formato/dominio, además de revisión docente independiente. La aprobación humana de D01/otros23, G3 y voz real siguen pendientes.

Recibos vecinos: 

## specs/010-guided-dialogue/technical-dialogue-audit-20261019.md

[Fuente](../../../specs/010-guided-dialogue/technical-dialogue-audit-20261019.md)

AI technical audit of actual synthetic outputs; no human utility, human approval or real voice validation

- Los informes originales y sus propiedades aprobadas se conservan. Esta lectura detecta defectos semánticos adicionales; no sustituye T067 ni acredita utilidad humana.
- | Caso | Resultado de lectura técnica | Hallazgo / decisión humana pendiente |
- | D04 | correction_and_scope | Petición de organización de exposición provocaba repetición rechazada. T070 limita composición idéntica; la cobertura docente de un guion de exposición sigue siendo juicio de revisión humana. |
- | D05 | correction | En revisión conceptual, un ejemplo solicitado se sustituía por pregunta. T070 usa ejemplo revisado cuando los permisos lo permiten y conserva la pregunta pendiente. |
- | V-H02 | correction | «Repite la pregunta» reproducía un contraste cuando no existía pregunta pendiente. T068 orienta sin atribuir categoría de pregunta a una explicación. |
- | V-H03 | review_scope | Composición de tres unidades revisadas y apoyos concretos. Revisión humana de suficiencia; no se acredita generación libre o un guion nuevo. |
- | V-H07 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |
- | V-H08 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |

Recibos vecinos: 

## specs/010-guided-dialogue/technical-dialogue-audit-current.md

[Fuente](../../../specs/010-guided-dialogue/technical-dialogue-audit-current.md)

Implementación dialogue_contract 2.1.2, coherencia 2.1.0, reviewed-unit-renderer/v1. Datos ficticios; llamadas públicas reales al backend determinista. No son personas, voz real, modelos generativos ni evidencia de utilidad educativa.

- # Revisión actual de 24 diálogos sintéticos
- Implementación dialogue_contract 2.1.2, coherencia 2.1.0, reviewed-unit-renderer/v1. Datos ficticios; llamadas públicas reales al backend determinista. No son personas, voz real, modelos generativos ni evidencia de utilidad educativa.
- | Caso | Observación técnica actual | Revisión humana |
- | D04 | Composición docente y repetición verificadas; organizar una exposición y apoyos agotados reciben un límite. Cobertura y utilidad pendientes. | No evaluado |
- | D05 | Repaso conserva pregunta pendiente; ejemplo permitido en concept_review. Comparación con dos referentes pide aclaración. | No evaluado |
- | D06 | Salida y almacenamiento ya no producen falso conflicto por predicados distintos; cambio explícito confirmado. | No evaluado |
- | W-H06 | Comparación conserva entrada; cambio confirmado a almacenamiento y sin falso conflicto entre sujetos distintos. | No evaluado |

Recibos vecinos: 

## specs/011-real-course-self-study/evidence/analysis-convergence.md

[Fuente](../../../specs/011-real-course-self-study/evidence/analysis-convergence.md)

Evaluación de solo lectura de spec/plan/tasks y constitución; este documento se guarda después, como entrega de implementación. La comprobación final no modifica intención ni añade una fase vacía.

- 12FR,4SC,3historias,5decisiones,11principios,10items de checklist y17tareas examinados. Cero contradicciones críticas de011; cero requisitos sin cobertura; ninguna brecha obligatoria de implementación encontrada tras T017. No demuestra suficiencia de conversación general ni aceptación pedagógica.
- Resultado de convergencia técnica: converged para el alcance definido de011. No se añade otra tarea ni una sección vacía. Revisión docente/aceptación humana de esta experiencia y voz real siguen pendientes. T061 CRITICAL histórico (seis contenidos perdidos), T067 humano y el negativoD01 de010 continúan abiertos; no se declara cierre/convergencia global del proyecto ni se acepta automáticamente el material.

Recibos vecinos: 

## specs/011-real-course-self-study/evidence/architecture/report.md

[Fuente](../../../specs/011-real-course-self-study/evidence/architecture/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/011-real-course-self-study/evidence/architecture/protocol.json), [results.json](../../../specs/011-real-course-self-study/evidence/architecture/results.json)

## specs/011-real-course-self-study/evidence/architecture-final/report.md

[Fuente](../../../specs/011-real-course-self-study/evidence/architecture-final/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/011-real-course-self-study/evidence/architecture-final/protocol.json), [results.json](../../../specs/011-real-course-self-study/evidence/architecture-final/results.json)

## specs/011-real-course-self-study/evidence/report.md

[Fuente](../../../specs/011-real-course-self-study/evidence/report.md)

Inicio desde PowerShell: `.\scripts\course-study.ps1`. [Guía](../../../specs/011-real-course-self-study/quickstart.md).

- Actividad propia `f0c7b90d-8e4c-4bc0-ad83-6c342e13e29d`, perfil `extractive_limited` con generador determinista y política `material-self-study/v2`. API ASGI real en proceso, sin servidor TCP, navegador ni acceso anónimo docente. Raíz `.oralia-course-study`; un curso, documento y actividad, cero sesiones activas al finalizar. La entrada conserva el esquema existente: migración limpia a `t010_dialogue_context`, sin migración nueva. Contrato del generador optativo1.1.0; comportamiento v1 y verificadores independientes conservados.
- [Desarrollo final, siete turnos](../../../specs/011-real-course-self-study/evidence/conversations/development-post-followup.md), [variante expuesta final, siete turnos](../../../specs/011-real-course-self-study/evidence/conversations/reserved-post-followup.md), [seguimiento abreviado](../../../specs/011-real-course-self-study/evidence/conversations/followup-fixed.md) y [terminal PowerShell completa](../../../specs/011-real-course-self-study/evidence/validation/logs/feature011-powershell-academic.log). Los JSON enlazados contienen configuración, entrada/salida efectiva, citas, estado y trazas; son ejecuciones del programa. Revisión docente/humana pendiente.
- | Global final |1386 aprobadas,951 omitidas,326.81s; una advertencia de deprecación Starlette/httpx preexistente |
- | Dirigidas finales con CLI real, permisos, cancelación y secretos |26 aprobadas,28.93s |
- | Seguimiento y negativos |20 aprobadas,10.68s |
- | Playwright completo |27 aprobadas,3.8min; guard de preservación sin cambios |
- La funcionalidad es extractiva y limitada a estas páginas: no tutor generativo, comprensión acreditada, evaluación de personas ni voz real. Revisión docente y utilidad humana pendientes. T061 histórico de010 conserva seis contenidos perdidos y T067 conserva revisión humana pendiente y D01 negativo; crear011 no resuelve esas puertas ni declara convergencia global del proyecto.

Recibos vecinos: 

## specs/012-conversational-course-study/checklists/capacity-decision.md

[Fuente](../../../specs/012-conversational-course-study/checklists/capacity-decision.md)

- [X] Is the conclusion from Qwen3-8B NF4 limited to the tested configuration and case?
- [X] Does the spec require a read-only inventory and prohibit implicit downloads or model switching?
- [X] Is the fixed-source condition clearly distinguished from end-to-end retrieval?
- [X] Are the sources selected before generation and tied to original pages and hashes?
- [X] Does the hypothetical-example rule distinguish fictional facts from cited academic principles?
- [X] Are formal compliance, semantics, retrieval and displayed continuity separate outcomes?
- [X] Are the bound, first-display stop, ownership/telemetry and preservation requirements explicit?
- [X] Are G2, SC001, reserve, participant publication and teacher approval unchanged?

- - [X] Is the conclusion from Qwen3-8B NF4 limited to the tested configuration and case?

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/analysis-convergence.md

[Fuente](../../../specs/012-conversational-course-study/evidence/analysis-convergence.md)

Comprobación de requisitos: `.specify/scripts/powershell/check-prerequisites.ps1
-Json -RequireTasks -IncludeTasks` resolvió Feature 012 y `spec.md`, `plan.md`,
`tasks.md`. No hay hooks de extensiones. La lectura cruzada de 12 requisitos
funcionales, cuatro criterios de éxito, tres historias, decisiones de plan y
principios de la constitución no revela una contradicción **entre artefactos**
que impida continuar. Todos los requisitos construibles se trazan a T001–T024.
Las tareas parciales no se interpretan como cumplidas.

- pertinente de foco y acto, tratamiento de error y pregunta pendiente, apoyo
- verificación independiente](../../../specs/012-conversational-course-study/evidence/semantic-independent-verifier-assessment.md)
- rechaza integrar tanto el juicio directo (tres falsos positivos) como el
- comparativo (tres falsos negativos). El plan registra Decision H sin rebajar
- semántica. El trabajo pendiente concreto se descompone en T026/T027,
- dependientes de un evaluador independiente justificable, mientras T020/T021
- el evaluador semántico independiente aún no identificado/calibrado (T026).
- | C1 | partial | CRITICAL para el producto, no contradicción documental | FR001/005/008, SC001 | A no superó la conversación completa; B mejora parcialmente y C no tiene condiciones comparables. Faltan verificador independiente, tres repeticiones/transferencia y revisión docente. Ya trazado en T008–T010, T018–T023 y T026–T027. |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/architecture-chat-comparison/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-chat-comparison/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-chat-comparison/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-chat-comparison/results.json)

## specs/012-conversational-course-study/evidence/architecture-chat-comparison-final/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-chat-comparison-final/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-chat-comparison-final/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-chat-comparison-final/results.json)

## specs/012-conversational-course-study/evidence/architecture-chat-gpu-free-final/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-chat-gpu-free-final/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-chat-gpu-free-final/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-chat-gpu-free-final/results.json)

## specs/012-conversational-course-study/evidence/architecture-context/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-context/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-context/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-context/results.json)

## specs/012-conversational-course-study/evidence/architecture-scoped/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-scoped/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-scoped/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-scoped/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-binding/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-binding/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-binding/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-binding/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-binding-fixed/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-binding-fixed/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-binding-fixed/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-binding-fixed/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-decision/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-decision/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-decision/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-decision/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-final/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-final/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-final/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-final/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-h1h3-v8/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-h1h3-v8/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-h1h3-v8/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-h1h3-v8/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-navigation/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-navigation/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-navigation/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-navigation/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-navigation-formatted/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-navigation-formatted/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-navigation-formatted/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-navigation-formatted/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-v10-scope/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-v10-scope/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-v10-scope/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-v10-scope/results.json)

## specs/012-conversational-course-study/evidence/architecture-semantic-v9-request-gate/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/architecture-semantic-v9-request-gate/report.md)

No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.
Sin valoraciones humanas ni evaluación de personas. Las celdas completadas no son sesiones humanas completadas.

- No demuestra superioridad de la arquitectura. Muestra sintética pequeña, modelo determinista, recuperación lexical; no comparable con un piloto LLM real.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-v9-request-gate/protocol.json), [results.json](../../../specs/012-conversational-course-study/evidence/architecture-semantic-v9-request-gate/results.json)

## specs/012-conversational-course-study/evidence/chat-cited-text-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-cited-text-report.md)

El protocolo `chat-cited-text-protocol.json` y los controles `chat-cited-text-controls-v1.json` se congelaron antes de inferencia. Se ejecutó un caso nuevo de cuatro turnos en B documental y C pedagógica, una repetición, con los tres PDF docentes autorizados, catálogo de laboratorio completo, unidades íntegras y Qwen3-8B NF4 local. No se usó A, reserva ni datos de participantes. La vía es solo de laboratorio y no permite publicación. `source-before.zip` y `frozen-run.json` preservan los bytes exactos de código, protocolo y decisiones del catálogo.

- El protocolo `chat-cited-text-protocol.json` y los controles `chat-cited-text-controls-v1.json` se congelaron antes de inferencia. Se ejecutó un caso nuevo de cuatro turnos en B documental y C pedagógica, una repetición, con los tres PDF docentes autorizados, catálogo de laboratorio completo, unidades íntegras y Qwen3-8B NF4 local. No se usó A, reserva ni datos de participantes. La vía es solo de laboratorio y no permite publicación. `source-before.zip` y `frozen-run.json` preservan los bytes exactos de código, protocolo y decisiones del catálogo.
- **Decisión técnica:** detener esta candidata local de texto citado. El ensayo no repitió la garantía falsa de pruebas que activaba la parada específica, pero cometió un error básico con fuente presente y no pudo mostrar el ejemplo solicitado; la fuente del cambio de tema fue insuficiente para las distinciones añadidas. Otra variante de prompt sobre este paquete expuesto no resolvería la falta de verificación semántica independiente. T037/T040/T048 y los gates G2/SC001 continúan abiertos/cerrados respectivamente: sin reserva, tres repeticiones, segunda revisión independiente, revisión docente ni publicación.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-claim-trial-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-claim-trial-report.md)

25 de octubre de 2026. Ensayo exclusivamente ficticio y diagnóstico, sin publicación, revisión docente ni uso de la reserva experimental de conversaciones.

- El modelo local Qwen2.5-14B-Instruct NF4 completó **una de las 16 afirmaciones centrales preparadas**: la afirmación general «La validación contrasta los requisitos con las necesidades del cliente.» del primer control negativo. Su salida JSON fue sintácticamente válida, 193 tokens en 12,76 s, y marcó `supported`, pero asignó `kind=conclusion`, `source_id="6 - Procedimiento requisitos.pdf"` en lugar del identificador autorizado `procedure:12`, y puso como `premise_quotes` una frase de la página que **no figura en la respuesta**. El validador rechazó la salida con `ValueError: premise must quote this answer`. La primera parada se registra como `invalid_output`, no como un veredicto semántico adjudicado. Quedaron sin ejecutar las otras 15 afirmaciones, los cinco controles derivados restantes y las dos transferencias. No se infiere 0/6 ni una tasa de transferencia.
- Una auditoría posterior precisó que `supported` era la etiqueta correcta para **esa afirmación general**; el fallo probado fue de clase/procedencia. El código de clasificación de resultados se corrigió después de esta captura, con cinco pruebas deterministas: desacuerdo solo de clase → `classification_mismatch`, `unknown` → categoría propia, y falso permiso/rechazo solo cuando difiere la etiqueta en la dirección correspondiente. El `source-before.zip` conserva sin alterar el runner exacto del ensayo. No se recalifica la salida inválida ni se cuenta como falsa aprobación semántica.
- La decisión técnica es **no relanzar este candidato con un prompt retocado sobre los controles expuestos**. El fallo exacto es de alineación de salida/procedencia en el primer tramo, antes de poder medir apoyo semántico, falsos permisos o falsos rechazos. Un siguiente candidato necesitaría demostrar, primero sin GPU, que puede producir identificadores de página y premisas de la respuesta bajo el esquema y pasar controles estructurales nuevos no expuestos; después se congelaría otra prueba y su criterio de abandono. La existencia de esos campos no acreditaría entailment. T037 permanece parcial, G2/SC001 y publicación cerrados; reserva, voz y datos habituales no se tocaron.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-closed-ref-menu-audit.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-closed-ref-menu-audit.md)

25 de octubre de 2026. Inspección sin GPU de `chat-closed-ref-first/`, los menús construidos por `source_options()` y `premise_options()`, y las páginas originales de `load_catalog()`. No modifica solicitudes, salidas, oráculo ni métricas congeladas. Esta lectura técnica no es ciega ni docente.

- El instrumento permitía **una sola línea física de PDF** como `source_ref` y, para una conclusión respaldada, **una sola frase de la respuesta** como `premise_ref`. Validaba que ambas existiesen literalmente, pero no que bastasen para implicar la afirmación. La página completa sí estaba en la solicitud de la etiqueta inicial, de modo que un falso rechazo de etiqueta no puede atribuirse sin más al menú posterior.
- | 7. Misma definición general de completitud en contexto negativo | El modelo respondió `unsupported` y se detuvo por falso rechazo. La misma afirmación había recibido `supported` en tramo5. | `S08` seguía disponible y la etiqueta recibió la **página completa**. El falso rechazo es observación distinta del límite de una sola referencia. |
- **Decisión de viabilidad:** no integrar ni repetir este candidato sobre los controles expuestos. Si se justificase un candidato nuevo, debería permitir un conjunto acotado de pasajes continuos y de premisas, preservar sus posiciones y páginas originales, y comprobar suficiencia proposicional con revisión independiente. Ese cambio de representación resolvería una limitación concreta, pero no el falso rechazo del tramo7 ni el problema general de implicación. Solo cabría evaluarlo con controles nuevos congelados y una única parada previa; no se inicia por defecto otra variante o cadena de prompts. T037, G2, SC001 y publicación permanecen cerrados; la reserva no se toca.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-closed-ref-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-closed-ref-report.md)

25 de octubre de 2026. Laboratorio ficticio, sin autoridad de publicación ni uso de la reserva experimental.

- El [protocolo visible](../../../specs/012-conversational-course-study/evidence/chat-closed-ref-inputs.json) y el [oráculo separado](../../../specs/012-conversational-course-study/evidence/chat-closed-ref-oracle.json) se congelaron antes de inferir. Dos casos de pruebas de defectos no habían sido enviados al modelo en el ensayo anterior; dos casos nuevos sobre completitud forman la transferencia local, ajena a la reserva de conversación. Se fijaron por separado ocho tramos centrales y sus clases (`general`/`conclusion`): el ensayo **no mide descubrimiento exhaustivo ni clasificación automática de afirmaciones**. El modelo Qwen2.5-14B-Instruct NF4 eligió `supported/unsupported/unknown` y, después, referencias a líneas de páginas o frases de la respuesta enumeradas mecánicamente. El programa resolvió offsets, IDs y texto literal; no eligió el testigo correcto con el oráculo ni corrigió etiquetas. Cada decisión usó JSON finito de un solo campo; el paquete `chat-closed-ref-first/` conserva solicitudes y salidas completas, ZIP previo y hashes de entradas, oráculo y siete fuentes.
- Se procesaron **7 de 8 tramos** en 4 casos; 16 elecciones finitas y 12,45 s acumulados medidos por tramo, incluidos sus pasos de programa. Seis etiquetas iniciales coincidieron con el oráculo: dos en el control positivo de pruebas, dos en el negativo, y dos en el primer caso de completitud. La séptima, la misma proposición general de completitud ya aceptada, fue `unsupported` pese a que el oráculo fijaba `supported`: **falso rechazo y parada predeclarada**. El octavo tramo, la conclusión inválida del último caso, quedó sin ejecutar. No se obtiene 4/4 ni una puntuación de transferencia completa.
- Una lectura posterior de los testigos impide llamar éxito semántico a los seis aciertos de etiqueta. En la segunda afirmación, conclusión sobre un fallo en caso raro y el uso habitual, el modelo eligió como premisa «Las pruebas de defectos buscan exponer fallos» y como pasaje una línea sobre casos diseñados para exponer defectos; omitió el supuesto ficticio de que **los casos habituales no se habían ejecutado** y la línea de la fuente sobre que las pruebas de defectos no tienen por qué reflejar el uso normal. En el caso de completitud eligió únicamente «el sistema software a desarrollar» como testigo tanto para la definición general como para la conclusión, y la proposición general como premisa de la conclusión, omitiendo la necesidad ficticia de cancelar reservas. Esos tramos existen literalmente y superan el contrato estructural, pero **no bastan para justificar las conclusiones**. La [auditoría del menú](../../../specs/012-conversational-course-study/evidence/chat-closed-ref-menu-audit.md) distingue lo atribuible al formato de lo atribuible a la elección: la conclusión compuesta del tramo2 no disponía de un testigo documental completo en una sola línea; para los tramos5–6 sí había opciones mejores (`S08` y `P02`) que no se eligieron. La parada automática ocurrió en el tramo7; el primer defecto de suficiencia visible tras revisión manual estaba ya en el tramo2. Esta revisión no fue ciega ni docente y no cubre el tramo no ejecutado.
- Las tres muestras previas mostraron 1% de GPU, 629 MiB usados y 31559 MiB libres. Hubo24 muestras durante el ensayo; ningún PID nuevo de cómputo ajeno al worker propio respecto del preflight. Al cerrar: 0%,629 MiB usados/31559 libres y `owned_tree_stopped=true`. ZIP: entradas/oráculo y7/7 fuentes coincidentes. Black conforme; `pytest -q tests/course_dialogue`: **195 aprobadas** en47,44 s, incluido el caso que separa error de clase de falso permiso. Ruff global:10 hallazgos existentes/0nuevos frente a49T090 con multiplicidad ([detalle](../../../specs/012-conversational-course-study/evidence/chat-closed-ref-ruff-result.json));3279+4hashes históricos/personales intactos.
- El candidato resolvió **formato y procedencia literal**, pero el menú de una sola línea/premisa tampoco podía expresar todos los testigos completos; además hubo elecciones insuficientes y una etiqueta inestable ante contexto diferente. No se ajustará a partir de estos casos expuestos ni se reiniciará para obtener 8/8. Un cambio futuro de representación tendría que admitir conjuntos acotados de pasajes y premisas, seguido de evaluación independiente de implicación por afirmación y controles nuevos. No se puede convertir la selección de líneas en prueba de entailment. T037 parcial; reserva, G2, SC001, revisión docente y publicación permanecen cerrados.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-comparison-gpu-free-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-comparison-gpu-free-report.md)

24 de octubre de 2026. Se ejecutaron dos conversaciones nuevas y completas de ocho turnos por variante, con Qwen3‑8B local/NF4, `enable_thinking=false`, un worker propio por ensayo, sin red ni publicación participante. Cada protocolo, petición, salida bruta y texto realmente mostrado permanece en paquetes nuevos; no se editaron ensayos anteriores. La reserva congelada es idéntica en ambos protocolos y **no se ejecutó**, porque el segundo desarrollo alcanzó su condición de parada. Esto no es G2, transferencia ni revisión docente/humana.

- 24 de octubre de 2026. Se ejecutaron dos conversaciones nuevas y completas de ocho turnos por variante, con Qwen3‑8B local/NF4, `enable_thinking=false`, un worker propio por ensayo, sin red ni publicación participante. Cada protocolo, petición, salida bruta y texto realmente mostrado permanece en paquetes nuevos; no se editaron ensayos anteriores. La reserva congelada es idéntica en ambos protocolos y **no se ejecutó**, porque el segundo desarrollo alcanzó su condición de parada. Esto no es G2, transferencia ni revisión docente/humana.
- El contrato estricto produjo un **retroceso de conversación mostrada**, aunque el raw contenía respuestas posiblemente útiles. Se conservan los avisos operativos que el interlocutor realmente habría visto. Después de esta ejecución se relajó solo esa validación: un ejemplo sigue exigiendo supuestos, mientras que `assumptions` sin ejemplo se ocultan y se señalan en el recibo. [La auditoría poshoc](../../../specs/012-conversational-course-study/evidence/chat-comparison-v2-example-development-first/posthoc-contract-audit.json) observa que 8/8 raws de B y7/8 de C se parsearían con la regla relajada y fin `stop`; **no reconstruye turnos mostrados ni continuaciones y no cuenta como un nuevo ensayo**. La pregunta eco se suprime de la presentación/estado, con raw preservado. Se corrigió además que «Cambio de tema» tras un prefacio que cita la salida previa recupere solo el nuevo foco; prueba determinista, aún sin inferencia real posterior.
- La condición de parada congelada se cumplió: B mostró menos de seis candidatas completas y C tampoco completó seis; no se ejecutaron las tres repeticiones de la reserva. No habrá una cadena adicional de ajustes de prompt basada en estas salidas. La ruta documental merece investigación por sus correcciones y cambio de foco, pero ninguna variante satisface SC001 en conversaciones completas ni dispone de verificador independiente de pertinencia, afirmaciones y cobertura. La API participante, T090/T150, consentimiento, retención y revisión docente no cambiaron. No se marcó ningún borrador como revisado ni se introdujo prosa en la ranura confiable. La voz sigue aplazada.
- Las siguientes decisiones técnicas requerirían un contrato de derivaciones reconstruibles, un evaluador semántico independiente calibrado con positivos/negativos y falsos rechazos, y repetir conversaciones completas sobre la reserva sin usarla para ajustar; tres repeticiones por caso son condición necesaria, no sustituto de validez semántica. El nuevo trabajo se traza en tareas SpecKit, sin cerrar G2/SC001.
- | `CUDA_VISIBLE_DEVICES=-1; .\.venv\Scripts\python.exe -m pytest tests/course_dialogue -q` | 162aprobadas,59,09s en la última repetición; una advertencia Starlette preexistente. Incluye finalización, eco, ejemplo, pendiente y cambio de foco con proveedor falso. |
- | `black --check` en los directorios/archivos afectados | 46archivos sin cambios pendientes en la última repetición. |
- | Nuevo paquete experimental [architecture-chat-gpu-free-final](../../../specs/012-conversational-course-study/evidence/architecture-chat-gpu-free-final) | 204celdas/0errores; replay204/204 coincidentes. Es determinista, no prueba de capacidad humana. |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-comparison-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-comparison-report.md)

24 de octubre de 2026. Resultado técnico: historial visible separado del raw, recuperación contextual y dos variantes documentales V2 implementadas en el banco local. La API/web participante permanece como estaba; G2 y SC001 siguen cerrados. La voz, revisión docente y utilidad con personas no se han validado. No hubo commits, Reset, descargas ni cambios deliberados en datos habituales.

- | [`chat-comparison-first/`](../../../specs/012-conversational-course-study/evidence/chat-comparison-first) | Dos conversaciones breves × A/B/C, Qwen3‑8B/NF4 con thinking no desactivado | A emitió6previews. B/C no dieron candidatas válidas: raw empezaba con `<think>`, con terminaciones por longitud/plazo o JSON inválido. Primeros fallos y congelado limitado conservados. |
- | [`chat-comparison-contract-fix-first/`](../../../specs/012-conversational-course-study/evidence/chat-comparison-contract-fix-first) | Regresión corta iniciada antes de nueva instrucción sobre GPU compartida | A:3turnos persistidos. B primer turno agotó31,8s con solo176MiB libres según snapshot posterior; no hay archivo de B porque se interrumpió la conversación. C no ejecutado. Worker propio y dos descendientes detenidos; ComfyUI ajeno conservado. No se puntúa capacidad. |
- La [revisión independiente de sistema](../2026-10-24-chat-comparison-independent-review.md) leyó los 24turnos completos del segundo paquete. A no resuelve varios seguimientos, rectificación y cambio a casos de prueba. B sí corrige la equivalencia falsa «validar=pasar tests» y responde a casos de prueba, pero incumple el contrato en dos turnos, omite el ejemplo concreto pedido, repite la entrada como pregunta y arrastra un límite obsoleto. C tiene muestra insuficiente para juzgar su estrategia. Esta revisión no es docente ni prueba de utilidad humana. A utiliza 83unidades authored pendientes de revisión que B/C no tienen: las diferencias no aíslan la arquitectura.
- Los seis deadlines C y el deadline B del seguimiento se conservan como errores de ejecución, pero son **no concluyentes para capacidad/rendimiento de modelo o variante** porque la GPU estaba compartida y no hubo aislamiento/telemetría comparable en el ensayo original. Tampoco se puede afirmar que ComfyUI los causó. El raw truncado nunca se mostró ni autorizó. El [diagnóstico](../../../specs/012-conversational-course-study/evidence/chat-timeout-diagnostic-report.md) explica observaciones, límites y la repetición exacta; no se elevó el timeout. La reserva y las tres repeticiones por caso de G2 siguen pendientes.
- - `context.py` y `corpus.py`: el referente académico proviene del último candidato mostrado, conservado tras aviso operativo; respuestas a pregunta pendiente y aclaraciones elípticas mantienen contexto, cambio de tema explícito usa la nueva duda. La selección no mezcla automáticamente el último input en un foco nuevo.
- El cierre público depende de verificar de forma independiente pertinencia de la pregunta, apoyo de cada afirmación y cobertura, enlazar una candidata autorizada a estado/fuente vigentes por los controles normales y obtener revisión docente, tres repeticiones y transferencia. T025 es diseño; T026/T027 permanecen abiertos. Rechazar todo tampoco acreditaría utilidad. No se ha insertado texto libre en la ranura de contenido revisado ni se ha marcado `reviewed=True`.
- | `docs/audits/2026-10-24-chat-comparison-independent-review.md` | Revisión técnica independiente añadida por auditoría paralela, sin aprobación docente. |
- | `python -m pytest tests/course_dialogue -q` | 158aprobadas, 35,24s. |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-fixed-source-14b-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-14b-report.md)

Se inventariaron solo snapshots ya presentes, sin descarga ni instalación: Qwen2.5-7B (4 fragmentos/15,23 GB), Qwen2.5-14B (8/29,54 GB), Qwen3-8B (5/16,38 GB) y Mistral-Small-24B (10/47,14 GB), todos con configuración, tokenizer y fragmentos visibles. El runtime `D:/ai-toolkit/venv` ya había cargado Qwen2.5-14B-Instruct NF4 como juez; ese fracaso de rol no prueba incapacidad para generar explicaciones. Se eligió esa alternativa como hipótesis, sin presumir que por tamaño supera a Qwen3-8B. La GPU RTX5090 tenía 31.656 MiB libres inmediatamente antes.

- Se inventariaron solo snapshots ya presentes, sin descarga ni instalación: Qwen2.5-7B (4 fragmentos/15,23 GB), Qwen2.5-14B (8/29,54 GB), Qwen3-8B (5/16,38 GB) y Mistral-Small-24B (10/47,14 GB), todos con configuración, tokenizer y fragmentos visibles. El runtime `D:/ai-toolkit/venv` ya había cargado Qwen2.5-14B-Instruct NF4 como juez; ese fracaso de rol no prueba incapacidad para generar explicaciones. Se eligió esa alternativa como hipótesis, sin presumir que por tamaño supera a Qwen3-8B. La GPU RTX5090 tenía 31.656 MiB libres inmediatamente antes.
- El worker confirmó Qwen2.5-14B NF4 listo en46,61s desde arranque (carga de pesos19,72s). La primera generación terminó normalmente en **20,34s**, 332tokens de768, entrada466tokens; no agotó presupuesto. El texto bruto explicó correctamente que los requisitos idealmente son completos y consistentes y que la complejidad impide garantizarlo en la práctica. No reprodujo la inversión «completos e inconsistentes» de la prueba Qwen3. Esta observación de un turno bajo fuentes fijas es una señal limitada de capacidad de generación, no una comparación de calidad entre modelos ni una conversación completada.
- **Decisión:** el ensayo no demuestra que Qwen2.5-14B sea inviable como generador; demuestra que este contrato de cita impidió evaluar más de un turno. No se retoca ni repite el paquete expuesto. Para un diagnóstico futuro habría que separar identificador citable y título de fuente en el request, congelar preguntas y controles distintos y volver a medir bajo recursos comparables. Es trabajo nuevo, no un permiso para G2. T037/T040/T048, apoyo semántico independiente, revisión docente y reserva3× siguen pendientes; G2/SC001 y publicación permanecen cerrados.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-fixed-source-transfer-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-transfer-report.md)

Se ejecutaron dos paquetes nuevos, congelados antes de inferencia: [regresión expuesta](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-14b-exposed-regression-first) con las preguntas previas para verificar el arreglo del request, y [capacidad nueva](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-14b-fresh-capacity-first) con preguntas diferentes. Ambos usaron Qwen2.5-14B-Instruct NF4 ya disponible, instrucción idéntica, cinco unidades originales completas fijadas de antemano, `document_id` igual al id citable, 768tokens/50s por turno, GPU local y worker propio offline. El primer paquete **no cuenta como transferencia**; el segundo tampoco mide recuperación end-to-end, porque las fuentes fueron seleccionadas manualmente antes. No hubo ajuste de prompt, fuentes, rúbrica o límites entre salidas.

- Se ejecutaron dos paquetes nuevos, congelados antes de inferencia: [regresión expuesta](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-14b-exposed-regression-first) con las preguntas previas para verificar el arreglo del request, y [capacidad nueva](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-14b-fresh-capacity-first) con preguntas diferentes. Ambos usaron Qwen2.5-14B-Instruct NF4 ya disponible, instrucción idéntica, cinco unidades originales completas fijadas de antemano, `document_id` igual al id citable, 768tokens/50s por turno, GPU local y worker propio offline. El primer paquete **no cuenta como transferencia**; el segundo tampoco mide recuperación end-to-end, porque las fuentes fueron seleccionadas manualmente antes. No hubo ajuste de prompt, fuentes, rúbrica o límites entre salidas.
- | Regresión expuesta | mostrado; 292tokens,17,78s | oculto por falta de cualquier `[id]`; 284tokens,17,69s | no ejecutado por parada | no ejecutado |
- | Capacidad nueva | mostrado; 295tokens,18,86s | mostrado; 438tokens,26,55s | oculto por ausencia de `Ejemplo hipotético:` y `Supuestos ficticios:`; 470tokens,30,36s | no ejecutado por parada |
- | Capacidad nueva primero | Ideal de completitud/consistencia e imposibilidad práctica, con `requirements:14` | Apoyo directo. No aparece la inversión «completos e inconsistentes» del ensayo Qwen3. | Respaldado para el núcleo. |
- La corrección del request resolvió el primer bloqueo **formal**, pero Qwen2.5-14B bajo esta instrucción y estas fuentes no completó la conversación: regresión1/4 y capacidad nueva2/4 turnos académicos mostrados. La generación añadió afirmaciones documentales no sustentadas incluso donde las fuentes completas estaban presentes, y la analogía nueva no estableció con precisión una contradicción. Esto separa fallo de contenido de fallo de recuperación; tampoco demuestra incapacidad general de todos los modelos locales. Se detiene esta línea de prompt y no se promueve al participante. Para otra arquitectura o modelo sería necesaria una hipótesis nueva, controles no expuestos y verificación independiente; no se abre la reserva con estos datos.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-full-teacher-compact-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-full-teacher-compact-report.md)

La autorización documental existente permitió revisar técnicamente los tres PDF docentes. El [manifiesto de decisiones](../../../specs/012-conversational-course-study/evidence/teacher-pdf-decisions.json) contiene 172 decisiones y hashes originales: **139 páginas textuales incluidas**, siete excluidas (tres portadas, un marcador sin contenido, tres duplicados de cuerpo) y **26 en cuarentena** porque la extracción no dio un bloque textual completo, en varios casos esquemas/gráficos. El [catálogo separado](../../../src/oralia/course_dialogue/full_corpus.py) verifica el hash original y cada página; `corpus.SELECTION`, PDF y runtime participante no cambiaron. La revisión técnica no equivale a aprobación docente ni certificación absoluta de privacidad.

- Los fallos del segundo paquete proceden de campos `example`/`assumptions` más largos que los máximos V3, no de falta de fuentes, del límite de 512 tokens ni del plazo GPU. Se conservaron las salidas crudas en el paquete, y ningún JSON inválido se mostró como respuesta. El input medido fue de1434–1721 tokens. La recuperación de testing tras la corrección léxica seleccionó unidades de testing en el control determinista; la captura guarda sus selecciones efectivas para auditoría.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-mistral24b-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-report.md)

Se comprobó read-only el snapshot exacto `9527884be6e5616bdd54de542f9ae13384489724`: configuración `MistralForCausalLM`, 363 tensores indexados, 10/10 fragmentos presentes (47,14GB), tokenizer y chat template locales. El runtime CUDA ya instalado tiene Transformers5.5.3 y bitsandbytes NF4; había30.991MiB libres frente a la estimación conservadora del worker de21.256MiB. No se infirió calidad por tamaño. La opción instalada `fix_mistral_regex=True` falló con `AttributeError` en el tokenizer raw; cargar sin corrección advierte segmentación incorrecta. Se aplicó **solo en memoria y por opt-in** la expresión regular que el código instalado intenta usar, exigiendo la forma esperada `Sequence(Split,ByteLevel)` y comprobando round trips españoles y chat template. No se modificaron pesos, caché ni paquetes instalados. [Inventario y compatibilidad](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-viability.json).

- # Última candidata local inventariada: Mistral-Small-24B (25-10-2026)
- Se comprobó read-only el snapshot exacto `9527884be6e5616bdd54de542f9ae13384489724`: configuración `MistralForCausalLM`, 363 tensores indexados, 10/10 fragmentos presentes (47,14GB), tokenizer y chat template locales. El runtime CUDA ya instalado tiene Transformers5.5.3 y bitsandbytes NF4; había30.991MiB libres frente a la estimación conservadora del worker de21.256MiB. No se infirió calidad por tamaño. La opción instalada `fix_mistral_regex=True` falló con `AttributeError` en el tokenizer raw; cargar sin corrección advierte segmentación incorrecta. Se aplicó **solo en memoria y por opt-in** la expresión regular que el código instalado intenta usar, exigiendo la forma esperada `Sequence(Split,ByteLevel)` y comprobando round trips españoles y chat template. No se modificaron pesos, caché ni paquetes instalados. [Inventario y compatibilidad](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-viability.json).
- El [protocolo nuevo](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-protocol.json), las [cinco unidades docentes completas](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-units.json) y la [rúbrica negativa](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-rubric.md) se congelaron antes de inferencia. Un caso, cuatro turnos, 768tokens/50s por turno, fuentes fijas originales, worker propio offline, sin reserva ni participante. Fuentes fijas controlan disponibilidad; no prueban recuperación end-to-end. El [recibo completo](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-first/conversation.json) contiene peticiones efectivas, texto bruto y mostrado, proveedor y continuidad real.
- | Ejemplo hipotético | Sí | 17,59s/321 | Incluye las marcas `Ejemplo hipotético:` y `Supuestos ficticios:`, una necesidad omitida de ventilación y citas del principio, no de la existencia de la estación. Pero afirma que bloqueo biométrico y combinación numérica son contradictorios: **ambos mecanismos pueden instalarse en la misma taquilla**. No declara ninguna premisa que los haga mutuamente excluyentes. Falla el núcleo del ejemplo solicitado pese al cumplimiento formal. |
- | Cambio a pruebas | Sí | 19,08s/373 | Distingue objetivos y casos de validación/defectos con `testing:7/8` y niega correctamente que pruebas aprobadas demuestren ausencia de errores con `testing:4`. La frase «validación de pruebas, también conocida como validación de requisitos» confunde nombres y no está respaldada por esas unidades; «asegurarse de que funcione correctamente» es más fuerte que demostrar comportamiento en casos dados. El límite final sí queda claro. |
- `worker.json` registra Mistral NF4 y `tokenizer_fix=mistral_regex_local`, 43,20s hasta ready, huella de memoria del modelo13.800.090.112bytes. Tres muestras GPU previas:562MiB usados; 51 durante, pico16.493MiB; posterior562MiB. `source-before.zip` coincide con nueve hashes congelados y `worker-cleanup.json` confirma los tres PID del árbol propio terminados con retorno0. Ningún proceso ajeno detenido. Sin red, descargas, Reset, cambios de participante o commits.
- Validación posterior: [21 pruebas focales](../../../specs/012-conversational-course-study/evidence/chat-mistral24b-tests.log) de adaptador, propiedad, runner y tokenizer pasaron en27,19s; Black dejó cinco archivos conformes; Ruff estructural10 hallazgos actuales/0nuevos frente al baseline T090 por `(ruta,código,mensaje)` con multiplicidad;3279 hashes históricos y cuatro personales coinciden. No se repitió la suite global. El [log de 218 pruebas](../../../specs/012-conversational-course-study/evidence/chat-fixed-source-transfer-tests.log) creado a15:36:23 y modificado a17:05:59 abarca5376,17s, cercano a los5374,95s informados por pytest: la duración de comando fue real, pero el log no identifica qué la causó. No se atribuye a GPU ni al código nuevo.
- | Qwen3-8B NF4 | Texto citado, catálogo docente; B3/4 y C3/4 | En ambos primeros turnos invirtió «completos y consistentes» a «completos e inconsistentes» con fuente presente; ejemplos ocultos. |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-semantic-verifier-calibration-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-semantic-verifier-calibration-report.md)

Fecha: 2026-10-25. Laboratorio exclusivamente ficticio; ninguna salida autoriza publicación a participantes ni acredita G2/SC001.

- Se usó Qwen2.5-14B-Instruct NF4 local y separado del generador Qwen3-8B. El [protocolo de calibración](../../../specs/012-conversational-course-study/evidence/chat-semantic-verifier-calibration-protocol.json) fijó antes de inferir siete controles: tres positivos y cuatro negativos. El primer intento (`chat-semantic-verifier-calibration-first/`) se detuvo antes del primer caso porque `GenerationRequest.purpose` rechazó un valor nuevo. Se conservó el paquete, 0 casos intentados y la limpieza del proceso propio; solo se cambió ese valor por `resumen`, ya admitido por el contrato. No se alteraron controles, respuestas esperadas ni instrucciones semánticas.
- La revisión técnica inicial había señalado que B llama «correcto, completo, verificable» al requisito de perfil sin fijar criterios del escenario, y que C llama claro a «registrar productos con sus características» sin definir esas características. C también afirma categóricamente que una ambigüedad «no se detectaría durante la validación con el cliente»; el material permite contrastar con el cliente mediante reuniones y prototipos, por lo que esa exclusión no se sigue. El verificador aceptó `documental-example`, `pedagogica-example` y `pedagogica-error`. Una [adjudicación técnica posterior](../2026-10-25-semantic-discrepancy-adjudication.md) contrastó los JSON originales con `procedure:10–12` y `requirements:73` y confirmó que esas conclusiones centrales carecen de apoyo bajo los supuestos mostrados. Se trata de falsos permisos respecto de la regla congelada, sin afirmar que todos los ejemplos sean necesariamente falsos. Su 7/7 en controles cortos no demuestra sensibilidad suficiente a esos defectos dentro de respuestas largas. Las lecturas no fueron ciegas ni docentes; sigue faltando revisión independiente por afirmación y resolución humana antes de calificar estas salidas.
- Los textos de entrada capturados contienen caracteres de reemplazo `�` en el prefijo contextual truncado; el cuerpo de la petición y las respuestas siguen legibles. Se conserva ese defecto de fidelidad de la captura, sin reconstruirlo ni usar la revisión como prueba definitiva.
- La reserva sigue sin abrirse; faltan dos pasadas independientes identificables con adjudicación de discrepancias, apoyo por afirmación, cobertura y continuidad, tres repeticiones de transferencia cuando corresponda y revisión docente. T037, G2 y SC001 permanecen abiertos/cerrados respectivamente. No se realizará otra optimización de prompts sobre el desarrollo ya expuesto a partir de estos resultados.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-timeout-diagnostic-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-timeout-diagnostic-report.md)

24 de octubre de 2026. Se conservó íntegro el primer ensayo de ocho turnos. Se lanzó un worker propio nuevo, offline, con el mismo Qwen3‑8B/NF4, `enable_thinking=false`, límite de 30 s y dos `GenerationRequest` exactas copiadas del recibo C: turno 1 completo (1826 tokens de entrada) y turno 3, primer deadline (2134 tokens de entrada). El script/protocolo y hashes de las peticiones quedaron fijados antes de inferir en `chat-timeout-diagnostic-first/`; los resultados, respuestas brutas, telemetría NVIDIA cada ~2 s y recibo de parada se conservan allí.

- 24 de octubre de 2026. Se conservó íntegro el primer ensayo de ocho turnos. Se lanzó un worker propio nuevo, offline, con el mismo Qwen3‑8B/NF4, `enable_thinking=false`, límite de 30 s y dos `GenerationRequest` exactas copiadas del recibo C: turno 1 completo (1826 tokens de entrada) y turno 3, primer deadline (2134 tokens de entrada). El script/protocolo y hashes de las peticiones quedaron fijados antes de inferir en `chat-timeout-diagnostic-first/`; los resultados, respuestas brutas, telemetría NVIDIA cada ~2 s y recibo de parada se conservan allí.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-unified-body-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-unified-body-report.md)

El [protocolo](../../../specs/012-conversational-course-study/evidence/chat-unified-body-protocol.json) y los [controles nuevos](../../../specs/012-conversational-course-study/evidence/chat-unified-body-controls-v1.json) quedaron congelados antes de inferencia. Un caso de cuatro turnos, B/C una repetición, sin A ni reserva. V4 sustituyó los microcampos V3 por `body` (techo de seguridad3500 caracteres), `source_ids`, `modes` y `fictional_assumptions`; V2/V3 permanecen como baselines. Se mantuvieron **512 tokens de salida y30 segundos**: las fallas V3 habían generado189–279tokens, por lo que se probó el margen existente antes de alterarlo. No se truncó texto/JSON ni se reparó la salida después del modelo.

- El [protocolo](../../../specs/012-conversational-course-study/evidence/chat-unified-body-protocol.json) y los [controles nuevos](../../../specs/012-conversational-course-study/evidence/chat-unified-body-controls-v1.json) quedaron congelados antes de inferencia. Un caso de cuatro turnos, B/C una repetición, sin A ni reserva. V4 sustituyó los microcampos V3 por `body` (techo de seguridad3500 caracteres), `source_ids`, `modes` y `fictional_assumptions`; V2/V3 permanecen como baselines. Se mantuvieron **512 tokens de salida y30 segundos**: las fallas V3 habían generado189–279tokens, por lo que se probó el margen existente antes de alterarlo. No se truncó texto/JSON ni se reparó la salida después del modelo.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-v2-context-echo-capture-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-v2-context-echo-capture-report.md)

Fecha local: 2026-10-25. Paquete [chat-comparison-v2-context-echo-capture-first/](../../../specs/012-conversational-course-study/evidence/chat-comparison-v2-context-echo-capture-first), [protocolo congelado](../../../specs/012-conversational-course-study/evidence/chat-comparison-v2-context-echo-capture-protocol.json) SHA-256 `6da661b377b9d242102c9cd2facd1a3c099ec9b6122eb8d720a48bb6a3740d9f`. El ensayo anterior, su raw y su parada permanecen intactos. Esta es **una captura diagnóstica de desarrollo**, nunca una intervención participante, revisión docente ni prueba de utilidad humana. El caso reservado no se ejecutó.

- El turno `example` de B y C produjo un campo `example` y texto mostrado completo. En ambos, `academic_query` fue la pregunta académica inicial sobre calidad de requisitos frente a necesidades, mientras `current_request` fue el pedido actual de ejemplo; la orden previa «Sigo confundido; di…» no entró en la consulta. `switch` cambió ambas consultas a pruebas de defectos frente a validación. En los 16 turnos B/C el modelo rellenó `question` con un eco de una entrada; el filtro lo omitió, mantuvo `raw_parsed_candidate`, y no queda ese eco exacto en el texto mostrado. Esto **no** prueba que el modelo pueda formular preguntas nuevas: el control positivo de pregunta nueva y repetición pedida se verificó solo con proveedor falso en pruebas deterministas.
- Esta primera pasada la realizó el mismo agente que definió la rúbrica V2, después de leer las salidas mostradas y las páginas originales `procedure:10–12`, `requirements:73`, `testing:7–9`. Es independiente del modelo generador, pero **no es una segunda revisión ciega ni revisión docente**. La tabla apunta a primeras afirmaciones/obligaciones críticas; no pretende calificar exhaustivamente cada proposición. Las referencias en el JSON son pistas, no apoyo automático.
- Las alertas de B/C en `followup`, `repeat` y `example`, más el absoluto de C en `error`, impiden tratar 8/8 completitud como éxito didáctico. La rúbrica [V2](../../../specs/012-conversational-course-study/evidence/chat-semantic-review-protocol-v2.md) exige calibrar controles positivos y negativos F/G/C y dos pasadas identificables realmente independientes antes de puntuar la puerta. Ninguna segunda pasada existe; no se declara un porcentaje semántico ni aprobación. La condición de parada semántica formal no se adjudica sin esa revisión; tampoco se abrirá la reserva ni se encadenarán más prompts sobre este caso.
- Se generó el diálogo legible con `scripts/render_chat_transcripts.py --packet ...\chat-comparison-v2-context-echo-capture-first`. La corrección de código previa ya pasó174pruebas dirigidas, Black4 y Ruff estructural sin novedades; este bloque solo ejecutó modelo y escribió evidencia. T037, G2/SC001, revisión docente y voz real permanecen pendientes. No hubo Reset, descargas ni commits.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-v2-context-echo-fix-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-v2-context-echo-fix-report.md)

Fecha local: 2026-10-25. La [captura anterior](../../../specs/012-conversational-course-study/evidence/chat-v2-final-capture-report.md) se preserva íntegra y sigue siendo el **primer resultado real** del V2 final de ese momento. La presente corrección no reconstruye sus turnos, no ejecuta otra inferencia y no concede puntuación semántica ni publicación.

- # Feature 012 — corrección determinista tras captura V2
- Fecha local: 2026-10-25. La [captura anterior](../../../specs/012-conversational-course-study/evidence/chat-v2-final-capture-report.md) se preserva íntegra y sigue siendo el **primer resultado real** del V2 final de ese momento. La presente corrección no reconstruye sus turnos, no ejecuta otra inferencia y no concede puntuación semántica ni publicación.
- El eco observado en B t3 y C t3/t4 estaba en `parsed_candidate.question`, no en `answer`. La antigua regla solo recogía subcadenas interrogativas `¿…?` de las entradas. Las tres peticiones eran imperativas, y en dos casos el modelo copiaba también el prefacio «Sobre lo que acabas de mostrar…». `runtime.py` compara ahora el campo `question` con la entrada íntegra, la petición sin ese prefacio y preguntas interrogativas previas; guarda `raw_parsed_candidate` y omite únicamente la pregunta eco del texto y estado mostrados. **No edita libremente `answer` ni elimina citas didácticas.** Una pregunta nueva se conserva, al igual que la pregunta pendiente cuando el usuario pide expresamente repetirla.
- Antes del cambio, los tests nuevos dieron **6 fallos/15 aprobados** en `test_context.py` y `test_runtime.py`. Tras el cambio, **26/26** en esos archivos; incluyen reproducción con las entradas y `question` exactos preservados de B t3 y C t3/t4, ejemplo tras error operativo, tema nuevo, rectificación, cambio de foco, pregunta nueva y repetición pedida. Regresión completa de `tests/course_dialogue`: **174 aprobadas**, 36,11s, una advertencia Starlette preexistente. Black dejó conformes los cuatro archivos afectados. Ruff de esos cuatro: 0 hallazgos; Ruff estructural `src tests scripts` frente a T090: 10 actuales, **0 nuevos** de 49 baseline por `Counter(path,code,message)` con multiplicidad ([recibo](../../../specs/012-conversational-course-study/evidence/chat-v2-context-echo-ruff-result.json)). SHA-256: 3279 archivos históricos y cuatro recursos personales/habituales sin cambio ([recibo](../../../specs/012-conversational-course-study/evidence/chat-v2-context-echo-preservation.json)).
- No se repitió la suite global: los cambios están limitados a `src/oralia/course_dialogue` y sus tests, sin API, esquema ni flujo participante. Los paquetes experimentales previos no se modificaron. La arquitectura sintética204/replay previa sigue siendo evidencia determinista de su versión, no de esta corrección ni de utilidad real. La reserva de conversación no se consumió y G2/SC001 permanecen cerrados.
- T037 sigue **parcial**: falta una nueva conversación completa congelada bajo estos bytes, control de recursos antes/durante/después y la revisión semántica independiente calibrada con dos pasadas identificables. La condición de parada de la captura previa prohíbe tratarla como éxito o consumir la reserva; no se inicia una cadena de ajustes de prompt.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-v2-final-capture-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-v2-final-capture-report.md)

Fecha local: 2026-10-25. Esta es **una conversación nueva de desarrollo A/B/C**, no una puntuación semántica, un ensayo de la reserva ni una autorización para participantes. El [protocolo de captura](../../../specs/012-conversational-course-study/evidence/chat-comparison-v2-final-capture-protocol.json) y la [rúbrica semántica V2](../../../specs/012-conversational-course-study/evidence/chat-semantic-review-protocol-v2.md) se fijaron antes de inferir; el caso de desarrollo conserva las ocho entradas del ensayo V2 anterior (solo cambia el ID) y la reserva es idéntica. SHA-256 previo: protocolo `63679bd26320352a6aab4f7f593e4a2513e33377b424c9740b47680c2db8594f`; rúbrica `c3ffd9af3b1b8599a88603aa2a5726b2cbdd9a647325318891a0d1c7f1b9653b`. El runner capturó su código y protocolo en `source-before.zip` antes de la primera inferencia; se verificaron los 14 hashes y el hash del protocolo frente a `frozen-run.json`.

- - La entrada de ejemplo en B y C conservó como `academic_query` la petición anterior de repetir la distinción, a pesar de que el input actual pedía un ejemplo. C aun así generó uno; la consulta contextual quedó desfasada y requiere diagnóstico independiente.
- Tres muestras previas: GPU 1%, 636MiB usados y 31552MiB libres. Durante A: 10 muestras, 9342–25603MiB usados. Durante B: 93 muestras, 12003–31107MiB usados y mínimo 1081MiB libres; sus dos deadlines ocurrieron en una ejecución con memoria total variable, pero esta telemetría no demuestra su causa. Durante C: 87 muestras, 17123–21547MiB usados y mínimo 10641MiB libres; su deadline emitió 509 tokens antes de 30s. Tras cerrar el worker propio: GPU 1%, 6462MiB usados y 25726MiB libres. El recibo `worker-cleanup.json` declara `owned_tree_stopped=true`; ComfyUI PID91212 seguía vivo. La memoria persistente después del cierre y el salto durante B impiden afirmar recursos exclusivamente comparables con el ensayo anterior. No se detuvo ni modificó proceso ajeno.
- El ensayo no valida apoyo de afirmaciones, cobertura pedagógica, G2, SC001, revisión docente, utilidad con personas ni voz real. Ninguna candidata obtuvo `publication_allowed`. Falta calibrar los controles de la rúbrica y dos pasadas independientes identificables. El resultado estructural por sí solo ya activa la parada de esta captura; la reserva permanece intacta. T037 sigue abierta para diagnosticar el desfase de consulta/eco y establecer evaluación semántica independiente antes de cualquier nueva puerta.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-v4-causal-audit.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-v4-causal-audit.md)

The frozen V4 request snapshots, not just the model's `source_ids`, were inspected. In the **first** B/C turns `requirements:14` was in the actual provider evidence. B reached 512 output tokens and was not displayed; C returned a complete JSON body with a fiction-mode contract conflict and was not displayed. The source caveat was available, so those first-turn failures cannot be called source absence.


Recibos vecinos: 

## specs/012-conversational-course-study/evidence/chat-whole-unit-diagnostic-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/chat-whole-unit-diagnostic-report.md)

Protocolo nuevo congelado antes de inferencia: `chat-whole-unit-diagnostic-protocol.json`. Un caso de desarrollo, tres turnos, una repetición por B/C, sin A ni reserva. `--whole-units --bc-only` activó solamente el contexto del laboratorio. `source-before.zip` guarda los bytes del runner, runtime, unidad documental, protocolo y demás fuentes en el instante del arranque; el ajuste posterior de traza para el caso sin evidencia no pertenece a esos bytes y no modifica la captura. Modelo local Qwen3-8B NF4 offline, un worker propio. Tres muestras GPU previas, 64 periódicas y una posterior; antes 1%/496 MiB usados, después 1%/607 MiB. El árbol propio de tres PID figura detenido en `worker-cleanup.json`. No se detuvo proceso ajeno.

- Protocolo nuevo congelado antes de inferencia: `chat-whole-unit-diagnostic-protocol.json`. Un caso de desarrollo, tres turnos, una repetición por B/C, sin A ni reserva. `--whole-units --bc-only` activó solamente el contexto del laboratorio. `source-before.zip` guarda los bytes del runner, runtime, unidad documental, protocolo y demás fuentes en el instante del arranque; el ajuste posterior de traza para el caso sin evidencia no pertenece a esos bytes y no modifica la captura. Modelo local Qwen3-8B NF4 offline, un worker propio. Tres muestras GPU previas, 64 periódicas y una posterior; antes 1%/496 MiB usados, después 1%/607 MiB. El árbol propio de tres PID figura detenido en `worker-cleanup.json`. No se detuvo proceso ajeno.
- Las solicitudes efectivas del primer turno llevaron seis unidades completas de tres documentos (2479 caracteres); el cambio de tema llevó cuatro unidades del PDF de testing (1851 caracteres). La traza registró cero omisiones de presupuesto en estos seis turnos. El worker midió entre 1488 y 1791 tokens de entrada, por debajo de su tope explícito de 7000; una entrada que lo supere se rechaza sin truncamiento. El contexto del seguimiento incluía únicamente la respuesta mostrada previa, aunque el fallo de salida impidió mostrar una explicación nueva.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/cpu-pipeline-audit-step1-2026-10-26.md

[Fuente](../../../specs/012-conversational-course-study/evidence/cpu-pipeline-audit-step1-2026-10-26.md)

No se han cargado pesos ni ejecutado inferencias nuevas. La GPU sigue pendiente de aviso y confirmación expresa de disponibilidad. No se han utilizado reserva ni publicación, ni modificado los PDF originales o las salidas históricas.

- No se han cargado pesos ni ejecutado inferencias nuevas. La GPU sigue pendiente de aviso y confirmación expresa de disponibilidad. No se han utilizado reserva ni publicación, ni modificado los PDF originales o las salidas históricas.
- El recurso local es estructuralmente consistente con Qwen2.5-7B-Instruct: cuatro fragmentos, 339 tensores, 28 capas y 7.615.616.512 elementos BF16 en sus cabeceras. Se comprobaron índice, dimensiones, offsets y tamaños, sin leer valores de pesos. Esto **no autentica los pesos frente al proveedor** ni acredita por sí solo toda la configuración efectiva de una carga histórica.
- - Había una laguna reproducible de registro: los recibos históricos no contienen el objeto de configuración de generación del modelo. Se añadió un lector de configuración sin mutación y un recibo por petición activado mediante `audit_config`; el recibo de inicio también registra el estado cargado. No se cambian mensajes ni argumentos de generación. Esta instrumentación solo sirve para futuras ejecuciones: no reconstruye el estado perdido.
- **Sigue sin conocerse la causa de la elección semántica errónea.** No hay logits históricos suficientes para localizarla. El uso concurrente de GPU confirmado en el último ensayo impide comparar sus recursos o rendimiento; no demuestra una causa del error de contenido.
- Mismo **Qwen2.5-7B-Instruct**, instantánea `a09a35458c702b33eeacc393d103063234e8bc28`, cuantización **NF4**, mismo worker y configuración capturada. Tres tareas, cinco peticiones independientes y orden fijo:
- Presupuesto: **5 peticiones + 1 calentamiento = 6 invocaciones máximas de `model.generate`**, hasta **577 tokens nuevos** incluyendo calentamiento; 90 segundos para carga y calentamiento y 30 segundos por petición. Duración estimada total **2–5 minutos**. Cero reintentos, reparaciones o adaptación según resultados. Un fallo semántico se registra sin modificar las siguientes entradas; un fallo de protocolo o recursos detiene la ejecución y deja constancia de lo no ejecutado.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/report.md)

Se implementó y ejecutó el recorrido de conversación de laboratorio sobre el RAG existente, sin cargar pesos, embeddings ni ejecutar inferencias. No se cambia el protocolo de la prueba GPU pendiente ni se inicia automáticamente cuando transcurran las tres horas comunicadas: sigue haciendo falta confirmación expresa de disponibilidad.

- Se implementó y ejecutó el recorrido de conversación de laboratorio sobre el RAG existente, sin cargar pesos, embeddings ni ejecutar inferencias. No se cambia el protocolo de la prueba GPU pendiente ni se inicia automáticamente cuando transcurran las tres horas comunicadas: sigue haciendo falta confirmación expresa de disponibilidad.
- Se reutiliza `ActivityScopeBinding`, sin otro catálogo de autorización. `rag_lab.py` admite evaluadores síncronos o asíncronos y revalida después de esperas, antes/después del proveedor y después de la revisión. Doce controles cruzan cuatro esperas —alcance, primer juicio, juicio tras ampliación y posrevisión— con retirada SQL, cambio de documento y cambio a cuarentena en una copia del manifiesto. Antes de generación impiden llamar al proveedor; después impiden preparar el preview. Se comprueban además conflicto, insuficiencia, desconocimiento, candidato incompleto, error, cancelación y entrega pendiente.
- El comando `python -m scripts.run_cpu_conversation_lab --name NOMBRE-NUEVO` usa política real, SQL de solo lectura y PDF originales. El catálogo `full` contiene **139 páginas vigentes**, con decisiones de inclusión/exclusión/cuarentena fijadas por hash. Generador, clasificador y evaluadores están **simulados explícitamente**: el texto sintético no es una explicación académica ni valida calidad pedagógica.
- [Seis turnos ejecutados](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/conversation-final.json) y [vista legible](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/conversation-final-transcript.md) muestran una salida simulada, una revisión desconocida, continuidad sobre el último referente mostrado, insuficiencia persistente, conflicto y cambio de tema. Incluyen pregunta, texto mostrado, pasajes, procedencia y tiempos de cableado. Los rechazos no se convierten en salidas mostradas. [Primera ejecución](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/conversation.json) y [primera transcripción](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/transcript.md) conservan el fallo del sexto turno, sin sobrescritura.
- 3. Ampliar solo el presupuesto conservaba la misma banda estricta de candidatos y no recuperaba un documento complementario. Un control sintético falló antes de implementar una única ampliación de banda en el perfil optativo; sigue excluyendo el control de ruido de un solo término.
- [Preguntas y pasajes originales congelados](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/controls.json), con [hash previo](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/controls.sha256), antes de la primera medición. Los referentes históricos de este banco son fixtures explícitos de recuperación, no conversaciones generadas. Se conserva el [código base](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/baseline-code) y todas las mediciones. Estos controles ya están expuestos; no son reserva ni una evaluación independiente de generalización.
- - La primera regresión amplia dio 367 correctas y seis rechazos de manifiestos antiguos; [recibo](../../../specs/012-conversational-course-study/evidence/cpu-rag-progress-v1/regression-first-failures.json). Las pruebas ahora verifican copias archivadas en árboles temporales y prueban separadamente que la repetición sobre el código actual sigue rechazada. El recibo simulado del ejecutor finito se actualizó al perfil vigente. No se cambian ejecutores, manifiestos ni resultados históricos.
- - Los **49 hashes** del paquete mínimo GPU pendiente siguen idénticos. Presupuestos históricos: **2/1/1/1**. Cero llamadas nuevas a modelos; no se usa reserva ni publicación. Los originales se revalidan por hash durante el recorrido.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/cpu-retrieval-gap-diagnosis-v1/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/cpu-retrieval-gap-diagnosis-v1/report.md)

Se completan los tres bloques autorizados sin cambiar el recuperador, sus pesos léxicos, su perfil o el banco expuesto. No se cargan pesos ni embeddings, ni se ejecutan inferencias o se inicializa CUDA. No se crea otra interfaz o arquitectura. La prueba mínima GPU anterior sigue siendo el siguiente avance decisivo, pendiente de aviso y confirmación expresa; el transcurso de tres horas no autoriza su inicio.

- Se completan los tres bloques autorizados sin cambiar el recuperador, sus pesos léxicos, su perfil o el banco expuesto. No se cargan pesos ni embeddings, ni se ejecutan inferencias o se inicializa CUDA. No se crea otra interfaz o arquitectura. La prueba mínima GPU anterior sigue siendo el siguiente avance decisivo, pendiente de aviso y confirmación expresa; el transcurso de tres horas no autoriza su inicio.
- En R04 la página 15 no se añade como vecina de la 11 porque la distancia es de cuatro páginas y la regla permite como máximo una. Quitar historial no cambia nada: no había historial. El hueco requiere una perspectiva que la coincidencia léxica actual no recupera; no demuestra que la unidad falte o que el presupuesto sea pequeño.
- En R05 el fixture de historial es la **página docente completa**, no una respuesta generada. La unidad dominante recibe 20 puntos de consulta y 38 de historial; eleva el máximo a 58 y el umbral a 29. La referencia buscada queda en 22. Sin términos históricos, el máximo baja a 20, el umbral a 10 y la referencia de 16 puntos se recupera. Esto demuestra competencia entre términos en este fixture; no demuestra que eliminar historial sea correcto para otros seguimientos o respuestas reales. La ponderación por término 4:1 no acota la contribución total de una respuesta extensa.
- - Descartar una entrega pendiente, preparada o todavía sin preparar, no altera el historial ni el referente previo. Descartarla dos veces es inocuo; confirmarla después se rechaza. El seguimiento conserva el tema efectivamente mostrado y no incorpora la entrega descartada.
- Se reutilizan las pruebas de candidato bloqueado, cancelación durante generación, salida incompleta, errores y cambios de fuentes durante esperas. Incluyen las doce combinaciones de espera y retirada SQL/cambio de documento/cuarentena. **63 pruebas pertinentes correctas**, una advertencia de deprecación Starlette/httpx, 1,47 s observados; [JUnit](../../../specs/012-conversational-course-study/evidence/cpu-retrieval-gap-diagnosis-v1/pytest.xml). Los proveedores y evaluadores de estas pruebas son simulados. No se necesitó cambiar el código de conversación.
- Los criterios separan apoyo de cada afirmación, pertinencia, cobertura, adaptación de la reformulación, supuestos del ejemplo, respeto del cambio de tema y límites. Los seguimientos dependen del texto efectivamente mostrado: ante fallo no se inventa continuidad. El paquete distingue desarrollo expuesto, este material nuevo sin ejecución ni ajuste y la reserva histórica intacta. No demuestra calidad pedagógica y no identifica ni inventa un evaluador semántico viable. Tampoco amplía las llamadas de la prueba mínima pendiente; una ejecución posterior necesitaría su propio protocolo y autorización.
- Black y Ruff correctos en los cuatro archivos nuevos. Se conservan código, controles, resultados y manifiestos anteriores. No se cierran T063/T071/T072/T073/T074, G2 o publicación por estas pruebas. El manifiesto final verifica los 49 hashes de la propuesta GPU pendiente, los consumos 2/1/1/1 y los cuatro originales. Sin commits, Reset, reserva, Internet en sesión ni procesos ajenos.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/dispatch-revalidation-2026-10-25.md

[Fuente](../../../specs/012-conversational-course-study/evidence/dispatch-revalidation-2026-10-25.md)

El chat anterior confirmó cierre y ausencia de operaciones; su estado era idle antes de editar. Checklists: capacity-decision 8/8, final-local-candidate 9/9, requirements 12/12. Sin hooks de implementación registrados.

- Se añadieron seis controles deterministas: retirada de actividad, nueva versión, cambio de bytes de política, sustitución del PDF, alteración del catálogo y control positivo sin cambios. Antes del arreglo: cinco fallos y seis pruebas correctas en test_scope_binding; los cinco negativos detectaban una llamada indebida al proveedor. Después: 11/11. La retirada durante generación conserva la protección posterior existente. Esto no cancela una inferencia que ya está en curso ni hace atómica la lectura de archivos externos frente a modificaciones concurrentes.
- Resultado: Black aplicado; Ruff JSON `[]` (cero incidencias, también por multiplicidad en estos dos archivos); 39 passed, 1 warning heredado de Starlette/httpx, 0.78 s. La ejecución inicial en sandbox falló al crear temporales de pytest; la validación satisfactoria se ejecutó con permiso fuera de sandbox. No hubo inferencia, GPU, descargas ni servicios externos. No se ejecutó suite global ni se afirma validación global de Ruff/preservación de hashes.
- ## Pendientes reales y decisión técnica
- T065/T072 sigue bloqueada técnicamente para publicación autónoma: no existe un evaluador independiente calibrado disponible que demuestre apoyo de todas las afirmaciones, pertinencia y cobertura del texto libre. Los juicios LLM y H1 expuestos no aportan esa garantía. No hay justificación para gastar otra inferencia repitiéndolos. La vía defendible con los recursos actuales es conservar candidatas y revisión humana independiente por salida en laboratorio; no se activa como sustitución del tutor autónomo solicitado.
- Opciones concretas: (1) revisión humana de cada salida, coste recurrente de lectura de pasajes y respuesta, sin compra de modelos pero sin autonomía; (2) investigación separada de un evaluador distinto, que requiere autorizar recurso/modelo y un presupuesto acotado de preparación, calibración y transferencia, sin coste monetario estimable hasta elegir recurso y sin garantía de éxito; (3) lenguaje de salida restringido, que requiere aceptar una reducción explícita del objetivo conversacional. No se aplica ninguna silenciosamente ni se solicita de nuevo aprobación del temario.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/document-evidence-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/document-evidence-report.md)

La decisión humana fue considerar todos los pasajes pertinentes de los documentos **ya ingeridos y autorizados**, combinando perspectivas, sin limitar un testigo a una línea física. El alcance efectivo es 17 páginas seleccionadas de tres PDF docentes, no el curso completo. Los PDF y su selección no cambiaron. Los 17 bloques reales extraídos son listas; no aparecieron tablas ni marcadores de continuidad interfoliar. Las pruebas sintéticas comprueban párrafos envueltos, listas, tablas con caja, unión explícita de páginas y rechazo de una unión injustificada.

- La decisión humana fue considerar todos los pasajes pertinentes de los documentos **ya ingeridos y autorizados**, combinando perspectivas, sin limitar un testigo a una línea física. El alcance efectivo es 17 páginas seleccionadas de tres PDF docentes, no el curso completo. Los PDF y su selección no cambiaron. Los 17 bloques reales extraídos son listas; no aparecieron tablas ni marcadores de continuidad interfoliar. Las pruebas sintéticas comprueban párrafos envueltos, listas, tablas con caja, unión explícita de páginas y rechazo de una unión injustificada.
- `evidence_sets.py` registra una afirmación exacta con hasta cinco testigos y cuatro premisas textuales distintas; comprueba posiciones, procedencia, límites y estado `unknown` para conflicto no resuelto. La existencia de referencias no demuestra implicación. Los [controles nuevos](../../../specs/012-conversational-course-study/evidence/document-evidence-controls-v1.json) quedaron congelados para recuperación/estructura, separados de los dos ensayos expuestos y de la conversación reservada. Los controles no son calibración semántica ni autorizan publicación.
- Verificación: `python -m pytest -q tests/course_dialogue/test_document_evidence.py` dio 7/7; `python -m pytest -q tests/course_dialogue` dio 202/202 en 78,90 s (una advertencia de deprecación Starlette). Black en tres archivos, Ruff focal sin hallazgos; Ruff global 10 hallazgos existentes y 0 nuevos por `(ruta,código,mensaje)` con multiplicidad frente al baseline T090 de 49. Los 3279 hashes históricos y cuatro personales del baseline durable coinciden. No hubo cambio de esquema, API participante, modelos, credenciales, permisos, reserva, paquetes experimentales ni procesos. La GPU quedó libre, pero no existe candidato semántico independiente defendible tras los falsos permisos y el falso rechazo de los ensayos previos; no se lanzó otra inferencia ni se afirma ahorro de tiempo.
- T038 y T039 están completos en el alcance de laboratorio. T040 sigue parcial: falta medir suficiencia mediante juicio semántico independiente sobre controles nuevos y fuentes completas; la cobertura de los 17 folios no equivale a cobertura del curso. T037, G2, SC001 y publicación permanecen cerrados; faltan además dos revisiones independientes, revisión docente, transferencia y repeticiones autorizadas. La reserva está intacta.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/grounding-reuse-viability-audit.md

[Fuente](../../../specs/012-conversational-course-study/evidence/grounding-reuse-viability-audit.md)

| Necesidad de T063–T068 | Recurso existente | Límite observado / trabajo nuevo mínimo |
|---|---|---|
| Fuentes docentes y versiones | `document_evidence.py`, `contracts/document-evidence.md` | Comprueban catálogo, hashes, páginas, spans y recuperación del laboratorio. T063 debe definir activación/retirada vigente para la futura ruta autorizada; no crear otro catálogo paralelo. |
| Referente, acto, objetivo y pregunta | `contracts/semantic-planning.md` | Define obligaciones propuestas y estado real; los clasificadores ensayados no prueban pertinencia. T064 solo debe formalizar trazas que falten. |
| Afirmaciones atómicas | `claim_review.py`, `evidence_sets.py` | Validan spans exactos, testigos, premisas y forma del ledger en laboratorio. Sus etiquetas `supported/unsupported/unknown` son datos aportados por un revisor, no resultados semánticos calculados. Si el contrato futuro usa `rejected`, registrar la conversión explícita de `unsupported`; no cambiar significado silenciosamente. |
| Puerta de publicación | `verification.py`, `contracts/reviewed-session-binding.md` | La comprobación de cita literal declara `independent_semantics=false` y `publication_allowed=false`; autorización, estado y T090/T150 siguen como puertas posteriores. No activar participante para probar un candidato. |

- Tres vías disponibles ya fallaron como verificación semántica independiente: el juicio directo de Qwen2.5-14B aceptó los tres negativos; la comparación de dos previews eligió el objetivo simple en los seis casos y rechazó los tres positivos; embeddings locales no separaron de modo estable corrección de foco y referencia implícita legítima. En ambos protocolos de seis casos el resultado fue 3/6 por decisiones constantes opuestas. Estos controles quedan expuestos para regresión, no son transferencia ciega.
- Mistral-Small-24B completó formalmente cuatro turnos con fuentes fijas y presupuesto observado, pero llamó incompatibles dos pares compatibles (globos azules/rojos y cierre biométrico/numérico) y añadió un término sin respaldo. Eso demuestra capacidad de formato y un fallo semántico material en ese ensayo, no una comparación general entre modelos: las condiciones difieren de las pruebas Qwen. Su propio ledger o una segunda pasada del mismo generador no aportarían independencia.
- **Resultado actual:** no hay un mecanismo autorizado y calibrado capaz de emitir `supported` como juicio semántico. Antes de implementar T065 hay que proponer una señal causalmente distinta de las tres vías fallidas, identificar evaluador y procedencia, congelar nuevos positivos y negativos, y fijar recursos/latencia/abandono. Debe registrar permisos falsos, rechazos falsos y cobertura por separado. Cero permisos falsos en un conjunto finito no promete cero invenciones en uso; un evaluador que rechace todo tampoco cumple el objetivo. Si no aparece candidato viable, conservar la puerta cerrada y el objetivo RAG generativo abierto: el usuario ha descartado sustituirlo por respuestas académicas predefinidas.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/report.md)

Ejecutada tras la autorización expresa de disponibilidad: Qwen2.5-7B-Instruct, snapshot `a09a35458c702b33eeacc393d103063234e8bc28`, NF4, runtime existente. **49 hashes originales verificados** antes de cargar. Frames, criterios y protocolo intactos; cero reintentos o ajustes. [Respuestas crudas](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/records.json), [configuración cargada](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/worker.json), [prompts renderizados](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/rendered-prompts.json), [revisión](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/review.json).

- Ejecutada tras la autorización expresa de disponibilidad: Qwen2.5-7B-Instruct, snapshot `a09a35458c702b33eeacc393d103063234e8bc28`, NF4, runtime existente. **49 hashes originales verificados** antes de cargar. Frames, criterios y protocolo intactos; cero reintentos o ajustes. [Respuestas crudas](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/records.json), [configuración cargada](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/worker.json), [prompts renderizados](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/rendered-prompts.json), [revisión](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/review.json).
- Los cuatro JSON pasan igualdad de objeto estricta sin reparación. La explicación fue: «El programa de prueba puede indicar la existencia de errores, pero no puede demostrar con certeza la ausencia de errores.» La revisión técnica de sus dos cláusulas encuentra apoyo en el pasaje proporcionado; no es un evaluador semántico independiente. **Falla la instrucción formal de dos frases**. No se declara éxito completo ni aceptación docente.
- Las parejas recibieron mensajes idénticos; solo se añadió la restricción finita prevista. Recuentos de entrada y hashes de prompt coinciden con la preparación CPU. El objeto efectivo por petición confirma generación voraz, `repetition_penalty=1.05`, límites 64/64/96/96/256 y restricción finita solo en las dos peticiones previstas. La plantilla efectiva coincide con la congelada. NF4/BF16 y configuración completa están en los recibos, sin inferir retrospectivamente el estado de ensayos anteriores.

Recibos vecinos: [worker.json](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/worker.json), [records.json](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/records.json), [review.json](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/review.json), [rendered-prompts.json](../../../specs/012-conversational-course-study/evidence/minimal-capacity-probe-run-2026-10-27/rendered-prompts.json)

## specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/report.md)

**No se obtuvo la comparación completa de tres conversaciones de cuatro turnos por condición.** Se completó A-baseline (cuatro turnos), se mostraron dos turnos de A-pedagogy-v1 y su tercer turno alcanzó el límite de 512 tokens. Esa salida incompleta se conservó sin mostrar ni añadir al historial; se detuvo todo el ensayo y quedaron 17 IDs no despachados. B y C no se ejecutaron en ninguna condición. No se amplió el límite ni se cambiaron prompts para completar artificialmente las 24 respuestas.

- [Transcripción realmente mostrada](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/transcript.md) · [Todas las salidas crudas, incluida la truncada](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/raw-candidates.md) · [Recibos completos](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/records.json) · [Revisión por cláusulas](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/review.json).
- | A3 Ejemplo | Escenario hipotético admisible; algunas acciones de revisión útiles, pero afirma claridad/no ambigüedad sin justificarla | Señala supuestos y observaciones de forma más explícita, pero sigue mezclando atributos y se trunca: no hay ejemplo completo evaluable |
- | A4 Datos para valorar impacto de cambio | Reconoce que faltan relaciones de trazabilidad; añade heurísticas sobre número de dependencias y menor impacto que las fuentes no establecen | No ejecutado |
- El escenario inventado de un perfil personal, sus enlaces o una propuesta de diseño **no se rechaza por no figurar literalmente en RAG**. El problema material es atribuir a comprensibilidad otros criterios que la fuente presenta por separado, o afirmar consecuencias sin premisas suficientes. En la parte truncada de la mejora hay un indicio positivo de supuestos/observación más explícitos, pero no basta para declarar una mejora global ni suplir la salida que falta.
- La revisión es técnica de salidas completas, no aceptación docente ni un evaluador semántico independiente acreditado. No se calculan tasas sobre B/C como si se hubieran ejecutado. El perfil queda optativo y experimental; **no se promueve y el baseline tampoco se declara correcto**.
- El worker confirmó Qwen2.5-7B-Instruct, NF4 con cómputo BF16 y modo evaluación; los frames auditados confirman generación voraz, `repetition_penalty=1.05`, 512 tokens y ausencia de restricción finita. [Frames reales](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/sent-frames.json), [prompts y hashes](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/rendered-prompts.json) y [configuración efectiva](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/worker.json) conservados. Las pruebas CPU verifican que seleccionar el perfil cambia solo la instrucción cuando las demás entradas son iguales.
- En la recuperación se recibieron seis respuestas `stop` y una `length`; la última generó 512 tokens y quedó sin mostrar. Salidas: 236/257/408/305/311/295/512 tokens. Tiempos observados: 8359/8702/13655/10922/10500/9891/17265 ms. El truncamiento limita el ensayo; no se interpreta como una prueba de incapacidad general ni se oculta como conversación completa.

Recibos vecinos: [worker.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/worker.json), [records.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/records.json), [protocol.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/protocol.json), [review.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/review.json), [sent-frames.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/sent-frames.json), [rendered-prompts.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/rendered-prompts.json)

## specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/report.md)

El preflight permitió cargar el Qwen2.5-7B NF4/BF16 previsto. El [chequeo de configuración efectiva](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/effective-configuration-check.json) confirmó clase, cuantización, tipo de cómputo y modo evaluación antes de las peticiones académicas. Se confirmó un calentamiento y se despachó A-baseline-1, pero no se recibió respuesta.

- El preflight permitió cargar el Qwen2.5-7B NF4/BF16 previsto. El [chequeo de configuración efectiva](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/effective-configuration-check.json) confirmó clase, cuantización, tipo de cómputo y modo evaluación antes de las peticiones académicas. Se confirmó un calentamiento y se despachó A-baseline-1, pero no se recibió respuesta.
- Una consulta de `nvidia-smi` excedió el plazo de cinco segundos del recolector. El monitor original trataba una única ausencia de telemetría como parada y terminó solo el worker propio. Las últimas muestras de memoria indicaban más de 24 GiB libres; esto no demuestra un fallo de capacidad del modelo ni presión de memoria. [Recursos](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/resources.json), [error](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/failure.json), [petición conservada](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/records.json), [ejecutor realmente usado](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/executed-runner.py) y [limpieza](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/worker-cleanup.json) permanecen intactos.
- La [recuperación también se detuvo, por truncamiento](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-recovery-run-v1/report.md). No se presenta este primer intento como fallo semántico ni se reescriben sus recibos.

Recibos vecinos: [worker.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/worker.json), [records.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/records.json), [protocol.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/protocol.json), [sent-frames.json](../../../specs/012-conversational-course-study/evidence/pedagogical-comparison-run-v1/sent-frames.json)

## specs/012-conversational-course-study/evidence/rag-local-expansion-validation.md

[Fuente](../../../specs/012-conversational-course-study/evidence/rag-local-expansion-validation.md)

Se precisó el objetivo de Feature 012: el contenido académico lo formula el LLM desde evidencia recuperada de fuentes autorizadas; respuestas docentes predefinidas no sustituyen ese objetivo. La vía web permanece desactivada por la constitución actual y se trata como punto de extensión condicionado. No se cambió `feature.json`: continúa apuntando a `specs/012-conversational-course-study`.

- | `.venv\Scripts\python.exe -m pytest tests/course_dialogue/test_scope_binding.py tests/course_dialogue/test_rag_lab.py tests/course_dialogue/test_document_evidence.py tests/course_dialogue/test_local_expansion.py tests/course_dialogue/test_runtime.py -q` | 48 passed, 1 warning de deprecación Starlette, 0.68s de pytest en la última ejecución. |
- | `.venv\Scripts\ruff.exe check` sobre esas seis rutas | All checks passed; 0 hallazgos en rutas nuevas, por tanto 0 incrementos frente al baseline durable. |
- El [recibo íntegro](../../../specs/012-conversational-course-study/evidence/rag-local-first/conversation.json) contiene las peticiones efectivas y salidas del Qwen2.5-1.5B cacheado, el contexto documental y las trazas. Preparación observada: 32,16s; inferencias: 1,390s y 1,359s. El primer turno respondió que un test aprobado no demuestra ausencia de errores, pero omitió todos los IDs de cita exigidos y formuló demasiado ampliamente qué puede demostrar. Ante «¿Por qué?» conservó el referente en recuperación, pero el modelo repitió casi lo mismo e introdujo «sistema operativo». Este Qwen2.5-1.5B sirve solo como smoke técnico de cableado; no se compara con ensayos 14B/Mistral ni mide el objetivo conversacional. Los casos insuficiente/conflicto usaron veredictos inyectados: demuestran la ruta operacional, no que un evaluador detecte esos estados. [La limpieza](../../../specs/012-conversational-course-study/evidence/rag-local-first/worker-cleanup.json) registra retorno 0 y tres procesos propios detenidos. **Después** de ese ensayo se añadió `phase` a las trazas, se expuso el ID citable exacto en `<pasaje id>`, se separaron `raw_candidate`, preview y `participant_display=null`, se exigió cambio de foco explícito y se eliminaron recortes silenciosos de historial. Las pruebas actuales cubren esos cambios, pero el recibo real preserva el código y formato anteriores; no se repitió inferencia GPU. No se ejecutó suite global porque no se tocó comportamiento compartido. No hubo red, Reset, commits, reserva ni procesos de demo.
- Análisis cruzado: FR015–FR018 y SC007/SC008 están cubiertos por plan y T069–T074. [El contrato de alcance](../../../specs/012-conversational-course-study/evidence/course-scope-contract.md) registra que `0 - Presentación.pdf` contiene bloques previstos pero no una lista exhaustiva de exclusiones vigente; la frontera de laboratorio usa decisiones inyectadas. [La propuesta revisable](../../../specs/012-conversational-course-study/evidence/course-scope-proposal.md) identifica inclusiones, prerrequisitos, exclusión acotada pendiente y dudas concretas. Las pruebas adicionales ligan una política sintética aprobada a motor, curso, actividad y versión SQL reales, verifican su hash y rechazan un cambio durante el `await`; no aprueban una política docente real. Las pruebas de frontera distinguen fuera confirmado, incierto, evidencia vacía/cuarentena, mezcla, operativa y casos cercanos; no prueban clasificación semántica real. No hay contradicción crítica entre artefactos activos; la publicación permanece cerrada. Convergencia: T063/T064/T071–T074 mantienen brechas de política de fuente/alcance vigente, suficiencia independiente, revisión de apoyo/pertinencia/cobertura y conversación completa. [El estudio mínimo T072](../../../specs/012-conversational-course-study/evidence/rag-independent-evaluation-design.md) descartó H1 como puerta de texto libre. No se usó GPU para esta ampliación. La petición de citar incumplida y el seguimiento improductivo se conservan como primeros fallos; Feature012 **no** ha convergido.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/readable-reference-run-2026-10-27/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/readable-reference-run-2026-10-27/report.md)

Se aplica la decisión expresa del usuario: basta una referencia comprensible al documento, título o página cuando sea útil. El modelo ya no tiene que reproducir IDs entre corchetes ni citas por frase. El host añade **«Fuentes consultadas»** desde los documentos realmente entregados al generador y conserva cómo los seleccionó; no afirma que respalden todo el texto. La procedencia interna mantiene unidades, versiones, posiciones, hashes y trazas. No se habilita Internet; una futura atribución web mediante título/enlace no equivale a permiso para usarla en sesiones.

- Los nuevos controles CPU fallaron antes del cambio por el antiguo bloqueo y pasaron después. Prueban también que referencias legibles no anulan rechazo/desconocimiento y que la deduplicación conserva IDs internos sin mostrarlos. El stream de auditoría conserva exactamente mensajes y presupuestos; solo añade `audit_config=true`, que no altera el prompt.
- [Propuesta congelada](../../../specs/012-conversational-course-study/evidence/readable-reference-proposal-v1/protocol.json), con tres preguntas nuevas y criterios fijados antes de inferir. Son controles nuevos de desarrollo sobre fuentes ya conocidas, no una reserva independiente. Hipótesis concreta: la atribución del host elimina la carga de reproducir IDs; evaluar seguimiento y ejemplo por separado, sin suponer que el nuevo formato mejora su contenido.
- Primer preflight: memoria ocupada pasó de 2029 a 17569 MiB; últimas muestras al 6 % de utilización. No se inició worker, no se cargaron pesos y no hubo inferencias. [Recursos originales](../../../specs/012-conversational-course-study/evidence/readable-reference-run-2026-10-27/resources.json) y [tres casos no ejecutados](../../../specs/012-conversational-course-study/evidence/readable-reference-run-2026-10-27/unexecuted.json) intactos. No se cambió el umbral ni se pidió otra autorización. Tras la regresión CPU se hizo una única recomprobación de recursos, con idénticas preguntas, criterios y presupuesto, conservada en otro directorio. Pasó el preflight y permitió ejecutar el ensayo; no hubo otra repetición.
- La revisión por cláusulas es técnica, **no un evaluador semántico independiente ni aceptación docente**. El ejemplo tiene aciertos parciales, pero no acredita la factibilidad temporal/económica que afirma. No se reescribe el oráculo para darlo por aprobado. El formato nuevo permite mostrar atribución legible; no resuelve automáticamente apoyo, pertinencia o calidad didáctica.
- **Configuración y trazas:** los tres frames realmente enviados, sus prompts y respuestas crudas se conservan; hashes de plantilla y recuentos de entrada 687/846/1153 verificados offline. El worker registra por petición el objeto de configuración y overrides, con NF4/BF16, generación voraz, `repetition_penalty=1.05` y máximo 512 tokens. Ninguna petición usa restricción finita. Tiempos observados 4327/7890/15782 ms, salidas de 96/235/467 tokens; cero truncamientos o reintentos.
- **Decisión:** cambio de presentación implementado y probado, sin otro ensayo o variante para aprobar el ejemplo. Quedan abiertos el apoyo y las condiciones del ejemplo, calidad de la reformulación, clasificación de alcance completa y evaluador semántico independiente. El objetivo sigue siendo RAG generativo autónomo, sin respuestas docentes predefinidas. No se abren participante, publicación ni gates.

Recibos vecinos: [protocol.json](../../../specs/012-conversational-course-study/evidence/readable-reference-run-2026-10-27/protocol.json)

## specs/012-conversational-course-study/evidence/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/report.md)

La integración técnica opcional por API normal y la preparación docente
semántica separada están implementadas y probadas. El tutor del curso real
no está habilitado: SC-001, G2 suficiente y revisión docente siguen pendientes.
No se hicieron commits, Reset, descargas ni cambios en los entornos habituales.

- no está habilitado: SC-001, G2 suficiente y revisión docente siguen pendientes.
- por hipótesis académicas del selector determinista antes de la inferencia.
- pendiente, cierre confirmado sin llamada al modelo, fuentes, conservación y
- | `.venv\Scripts\python.exe -m pytest tests -q --tb=short --junitxml=.claude-scratch/feature012-global-semantic-navigation.xml` | 1530 aprobadas, 951 omitidas, 382,15 s; advertencia de deprecación Starlette existente. |
- | `python -m black --check` sobre las 64 rutas Python cambiadas | 64 sin cambios pendientes de formato. |
- | `pytest tests/course_dialogue/test_semantic_api_binding.py -k 'invalidation or ownership'` | 3 aprobadas, 11,66 s: retirada, estado invalidado y docente sin propiedad. |
- La primera prueba de pregunta pendiente no reconocía una composición de tres
- El ensayo `transfer-readable-goals-qwen3-exposed` completó 30 turnos reales del

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/scope-catalog-binding-validation.md

[Fuente](../../../specs/012-conversational-course-study/evidence/scope-catalog-binding-validation.md)

`ActivityScopeBinding.assert_catalog` contrasta cada página y unidad recibida por el RAG con una extracción independiente de los PDF originales fijados en la política de alcance v1. La primera implementación solo comparaba página y unidad entre sí: aceptaba texto fabricado coherentemente en ambas con metadatos originales. Se corrigió ese fallo y se añadió la prueba de regresión. Para el perfil ampliado se exige además el hash fijado del manifiesto de decisiones, cuyo cargador conserva exclusiones y cuarentenas. La extracción confiable se reutiliza en memoria mientras coinciden hashes de PDF y manifiesto; `revalidate` comprueba los archivos antes y después de `GenerationPort`. La presentación delimita alcance; no se entrega como evidencia académica al generador. El resultado continúa en `laboratory_preview`, con `participant_display=null` y `semantic_support=unverified`.

- `ActivityScopeBinding.assert_catalog` contrasta cada página y unidad recibida por el RAG con una extracción independiente de los PDF originales fijados en la política de alcance v1. La primera implementación solo comparaba página y unidad entre sí: aceptaba texto fabricado coherentemente en ambas con metadatos originales. Se corrigió ese fallo y se añadió la prueba de regresión. Para el perfil ampliado se exige además el hash fijado del manifiesto de decisiones, cuyo cargador conserva exclusiones y cuarentenas. La extracción confiable se reutiliza en memoria mientras coinciden hashes de PDF y manifiesto; `revalidate` comprueba los archivos antes y después de `GenerationPort`. La presentación delimita alcance; no se entrega como evidencia académica al generador. El resultado continúa en `laboratory_preview`, con `participant_display=null` y `semantic_support=unverified`.
- | `pytest test_scope_binding.py test_rag_lab.py test_local_expansion.py test_document_evidence.py test_full_corpus.py -q` | 35 passed; 1 aviso de deprecación Starlette. |
- Las pruebas nuevas rechazan documento ajeno, hash de origen cambiado, unidad discordante, página/unidad fabricadas coherentemente, metadatos de página falsos y catálogo cambiado durante la espera del proveedor. No se hizo inferencia GPU, Reset, commit ni ensayo de publicación. Estas pruebas comprueban **identidad y procedencia estructural**, no apoyo semántico. La suficiencia sigue inyectada como fixture y no existe aún clasificación fiable de preguntas libres a bloques ni verificador independiente de afirmaciones, pertinencia y cobertura. T063/T071 siguen parciales; T065/T072 y G2/SC001 siguen abiertos.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/scope-control-diagnostic-report-2026-10-26.md

[Fuente](../../../specs/012-conversational-course-study/evidence/scope-control-diagnostic-report-2026-10-26.md)

La candidata **no es apta para integrar el alcance al RAG bajo el criterio requerido**. Con el perfil de control corregido y confirmado por el worker, la primera pregunta introductoria fue clasificada como estudio autónomo de fiabilidad, explícitamente excluido. El formato funcionó; la decisión semántica fue incorrecta. Se respetó la parada, sin reparación, reintento ni otra variante. No se abre publicación ni se promete solucionar esto cambiando otro prompt o modelo.

- El chequeo posterior no reprodujo un defecto de transporte en esta llamada: pregunta, política, descripciones, perfil efectivo, confirmación, decoder real y proyección coinciden. El conflicto histórico de evidencia vacía no está presente. No se demuestra causalidad comparando preguntas distintas ni se generaliza a los once casos no ejecutados. El clasificador sigue siendo un bloqueo; el verificador de apoyo/pertinencia/cobertura de respuestas es otro bloqueo independiente. El tutor permanece en laboratorio.
- | Esperado | in_scope | out_of_scope | mixed | uncertain_scope | operational | Error | No ejecutados |
- **Una pregunta ejecutada (C01), once no ejecutadas (C02–C12)**. Acierto semántico: 0/1. Formato completo: 1/1; perfil confirmado: 1/1; decoder finito real: 1/1. Exclusiones falsas: 1; filtraciones mixtas observadas: 0, pero ninguna mixta ejecutada. Referente, testigos y peticiones inciertas no se midieron. No se presenta como cobertura de nueve bloques ni transferencia. Los ceros de categorías no ensayadas no acreditan seguridad o utilidad.
- Presupuesto independiente **1/48 llamadas** consumido, 128 tokens reservados en el único paso, 14 tokens generados. Manifest SHA256 `501154cc1044892afa99718d40c58b11b32ec6950c074daea6a8c873d5824706`. Los anteriores permanecen **2/20, 1/28 y 1/72**; no se reutilizaron sus llamadas restantes. Las 47 llamadas de este diagnóstico tampoco se emplean para ajustar o repetir después de la parada.
- Se usó el mismo Qwen2.5-7B-Instruct local, snapshot `a09a35458c702b33eeacc393d103063234e8bc28`, NF4. El worker anunció y confirmó los perfiles de control. Plantilla efectiva SHA256 `2e2d2512cfe46af53dc1eed45368ecaab26ac4461c480e6b69fe571cf0ceaa75`. Preparación 34.750 s. Request: 4163 tokens de entrada, máximo 128 de salida. Resultado: 14 tokens, **1843 ms registrados**, terminación completa, sin deadline ni error de protocolo.
- Se detectó una carrera en la **agregación del resumen de recursos**, no en el transporte de control: resource-review.json se escribió antes de que acabara una muestra pendiente del monitor y dejó `pressure_observed=false`, aunque la telemetría final sí contiene 512 MiB libres. Se conserva ese recibo original; [auditoría adicional](../../../specs/012-conversational-course-study/evidence/scope-control-diagnostic-post-audit-v1.json) calcula `pressure_observed=true` a partir de las muestras completas. No se cambió la salida del modelo ni la evaluación semántica. La parada por exclusión falsa ya había impedido otra pregunta; no hubo envío después de esa muestra. Se corrigió offline el orden del resumen para escribirlo después de esperar al monitor y se añadió un test que reproduce el caso de muestra tardía. No se repitió la inferencia.
- Antes de cargar pesos: **26 pruebas offline correctas**, un warning heredado Starlette/httpx, 0.67 s. Verifican nuevo límite 48, contabilidad antes del envío, perfiles reales del adaptador por transporte simulado, recibos parciales, oráculo fuera del request, fallo de confirmación, hash alterado, presión frente a pico no atribuido y fuentes/budgets anteriores independientes. Tras corregir el resumen tardío: **27 passed**, mismo warning, 0.64 s. Black y Ruff final `[]` en los cuatro Python de este bloque. La E501 de una cadena larga se corrigió por formato; no se editó ningún valor del protocolo ni input del ensayo.
- La infraestructura local de fuentes, políticas, perfiles, restricciones y recibos queda utilizable para trabajo verificable. El objetivo de tutor autónomo aún no está cumplido: faltan un clasificador de alcance fiable en sus controles y, por separado, un verificador independiente de respuestas. No se sustituyen por contenido académico predefinido o revisión humana en cada turno. Publicación, participante, G2/SC001 y reserva permanecen cerrados. Sin commits, Reset, descargas, cambios de fuentes o procesos ajenos; no se afirma auditoría global de los 3279 hashes históricos.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/scope-decoder-architecture-audit-2026-10-26.md

[Fuente](../../../specs/012-conversational-course-study/evidence/scope-decoder-architecture-audit-2026-10-26.md)

`cached_transformers.py` añade `output_schema` al mensaje de sistema. Separadamente llama a `finite_json_outputs(schema)` y envía su resultado como `frame.finite_outputs`. Si esa función devuelve None, `gpu_worker.py` no recibe una gramática: genera libremente y el código llamador valida después.

- Los schemas completos de ScopeSelection v1 y ScopeSelectionV2 devuelven None porque no son el pequeño esquema de un solo enum ni incluyen alternativas enumeradas. Por eso se usó solo esquema como instrucción: el adaptador tiene ese fallback y estos dos llamadores no exigieron capacidad de decodificación restringida. No se debió confundir la presencia de `output_schema` con enforcement del backend. Debimos verificar esta limitación antes de esas inferencias. Los recibos efectivos lo corroboran: `structured_decoder=false`, `schema_hint_only=true`, `finite_enum_decoder_supported=true`, `finite_decoder=false` en el frame bruto. El campo numérico `0.0` del outcome es serialización del falso; el frame original conserva el booleano.
- Esto explica la superficie formal que quedó expuesta, **no demuestra la causa psicológica o semántica de la respuesta del modelo ni corrige N01**. El primer error sigue siendo el rechazo registrado, con una propuesta primaria coincidente con el oráculo y una representación inválida.
- No hay nuevo presupuesto de evaluación aprobado por este documento y no se ejecuta otra inferencia. La autorización general de trabajo local no se usa para encadenar variantes tras los stops congelados. Antes de considerar un ensayo futuro, la infraestructura deberá probar offline que nunca recae en hint para la decisión finita y que rechaza testigos no literales/ambiguos. Su evaluación semántica y de cobertura deberá ser distinta de pruebas de formato. Se mantienen las fallas históricas como regresión expuesta; la reserva no se usa.
- El pico de 15521 MiB del ensayo previo y el umbral `baseline + huella propia + 2048 MiB` indican consumo total superior a una aproximación conservadora. No separan memoria del proceso ajeno de prefill, KV cache, buffers temporales o allocator propio; no demuestran que el PID ajeno estuviera activo. La presencia de ese proceso tampoco lo demuestra. Se conserva `resource-inconclusive` para rendimiento, sin culpar al proceso ni al modelo por un deadline que no existió. La salida completa inválida permanece observable y separada del juicio de recursos.

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/scope-effective-request-audit-2026-10-26.md

[Fuente](../../../specs/012-conversational-course-study/evidence/scope-effective-request-audit-2026-10-26.md)

El ensayo finito emitió un objeto formalmente válido con una exclusión falsa. La auditoría no encontró desplazamiento de selección, pregunta sustituida, fuente cambiada, truncamiento ni restricción aplicada al prompt. **Sí encontró una incompatibilidad de construcción de mensajes**: el adaptador reutilizó una instrucción de generación académica que exige usar solo etiquetas `<evidencia>` para una solicitud de clasificación que no tenía ninguna etiqueta de evidencia académica. Política y descripciones estaban en el JSON de `<pregunta_actual>`.

- El ensayo finito emitió un objeto formalmente válido con una exclusión falsa. La auditoría no encontró desplazamiento de selección, pregunta sustituida, fuente cambiada, truncamiento ni restricción aplicada al prompt. **Sí encontró una incompatibilidad de construcción de mensajes**: el adaptador reutilizó una instrucción de generación académica que exige usar solo etiquetas `<evidencia>` para una solicitud de clasificación que no tenía ninguna etiqueta de evidencia académica. Política y descripciones estaban en el JSON de `<pregunta_actual>`.
- Se reconstruyó el frame mediante el adaptador congelado y un transporte simulado que devuelve la salida ya registrada. No se volvió a llamar al modelo. Es una reconstrucción del frame desde código/request preservados, **no una captura original del pipe de salida**; el identificador de transporte del simulador es nuevo y no representa otra inferencia. Request original, raw response y parámetros permanecen íntegros dentro del recibo de auditoría.
- | Plantilla | Qwen2Tokenizer real, misma plantilla efectiva del worker, SHA256 `2e2d2512cfe46af53dc1eed45368ecaab26ac4461c480e6b69fe571cf0ceaa75`; `chat_options={}`, `add_generation_prompt=true`. |
- | Contexto | La reconstrucción con tokenizer real da **4189 tokens**, exactamente el número del frame original. Bajo el límite 7000; no se truncó. |
- | Parámetros | Modelo/snapshot y NF4 originales; máximo de salida 128, deadline efectivo 29827 ms, latencia registrada 2155 ms. El worker ejecuta `do_sample=false`, es decir, generación greedy. `temperature=0` en outcome es anotación del adaptador; no se pasan sampling temperature/top_p/top_k al generate de esa llamada. |
- Pruebas: **21 passed**, un warning heredado Starlette/httpx, 0.65 s. Reproducen la regla incorrecta original, prueban el renderer de control y rechazos de uso académico, y ejercitan adaptador/finite schema existentes. Black aplicado y Ruff JSON `[]` en los cuatro archivos nuevos de esta auditoría/corrección offline. No se ejecutó suite global.
- **Comprobado:** procedencia/vigencia de fuentes y metadatos de alcance en el laboratorio, compilación sin truncar, tokenizer real, enforcement finito, presupuestos y trazas, rechazo de testigos ambiguos, parada y limpieza propia. También queda reproducido el conflicto de mensajes y probada una construcción alternativa de control, todavía sin conectar.
- | Completar exclusivamente el arreglo de transporte de control identificado | Un bloque acotado de cableado explícito renderer→adaptador y regresión offline del camino académico. Sin descargas/API/modelo nuevo. Si después se decide medir capacidad, necesitaría un único presupuesto/protocolo nuevo; no estas 71 llamadas. No requiere cambiar permisos para los comandos locales ya autorizados. | No demuestra que el fallo semántico desaparezca. No justifica otro bucle de prompts ni publicación. |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/scope-finite-capacity-first-report-2026-10-26.md

[Fuente](../../../specs/012-conversational-course-study/evidence/scope-finite-capacity-first-report-2026-10-26.md)

La candidata **no supera** el protocolo. La primera decisión fue un objeto legal de las alternativas compiladas y se generó con restricción real de tokens, pero asignó incorrectamente una pregunta introductoria de Ingeniería del Software al bloque excluido `fiabilidad`. El oráculo detectó una exclusión falsa y activó la parada. No hubo reparación, reintento, otro prompt/modelo ni integración al RAG. La decisión de laboratorio no se mostró a un participante: `participant_display=None`, publicación cerrada.

- Se ejecutó **F01**, una pregunta y una llamada. F02–F18 son **17 preguntas no ejecutadas**, no errores ni aciertos. Se reservaron 128 tokens para el único paso target; el modelo generó 14. Presupuesto nuevo **1/72 llamadas** consumido, independiente de los anteriores, que siguen en 2/20 y 1/28. Las 71 restantes no se emplean para otra variante o ajuste después de la parada.
- | Esperado | in_scope | out_of_scope | mixed | uncertain_scope | operational | error | No ejecutados |
- | Procesos de desarrollo | No ejecutado |
- | Desarrollo ágil | No ejecutado |
- | Ingeniería de requisitos | No ejecutado |
- | Modelos de sistema | No ejecutado |
- | Herramientas | No ejecutado |
- | Diseño, arquitectura y patrones | No ejecutado |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/scope-v2-described-first-report-2026-10-26.md

[Fuente](../../../specs/012-conversational-course-study/evidence/scope-v2-described-first-report-2026-10-26.md)

La candidata **no supera** el protocolo congelado. Se detuvo en el primer caso por error de contrato. Se conservaron pregunta, request completo con las 21 descripciones, salida bruta completa, error, telemetría y cierre. No se corrigió la salida ni se ejecutaron variantes, reparaciones o reintentos.

- | No ejecutados: N02–N28 | 27 |
- Es un error textual completo y observable bajo este contrato. No demuestra que el modelo sea incapaz de reconocer el tema, ni que haya fallado semánticamente en los otros veintisiete casos. Tampoco permite atribuir el resultado al contrato o a las descripciones por separado: se evaluaron juntos.
- Cinco muestras de baja carga permitieron arrancar. Primera muestra: 0% uso, 1118 MiB usados, 31070 MiB libres. El proceso residente ajeno 51980 se registró sin bloquear por mera residencia ni modificarlo. El worker fue Qwen2.5-7B-Instruct local, snapshot `a09a35458c702b33eeacc393d103063234e8bc28`, NF4, mismo modelo/prompt/descripciones/umbrales congelados; no hubo descarga o servicio externo.
- Durante las 25 muestras se observó un pico total de 15521 MiB y se activó el umbral conservador de memoria no atribuida respecto a huella propia + baseline + 2048 MiB. **No demuestra actividad del proceso ajeno:** memoria de prefill/KV/allocator del worker también puede contribuir. El rendimiento se registra `resource-inconclusive`, sin aislamiento exclusivo ni comparación causal de latencias. El recibo conserva tanto la presión detectada como el error de contrato: presión no equivale a deadline y no borra el testigo textual incorrecto. La ejecución terminó sin otra llamada.
- - [Request N01](../../../specs/012-conversational-course-study/evidence/scope-v2-described-first/N01.request.json), [outcome N01](../../../specs/012-conversational-course-study/evidence/scope-v2-described-first/N01.outcome.json), [evaluación](../../../specs/012-conversational-course-study/evidence/scope-v2-described-first/evaluations.json) y [métricas con IDs no ejecutados](../../../specs/012-conversational-course-study/evidence/scope-v2-described-first/metrics.json).

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/semantic-v10-scope-partial-report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/semantic-v10-scope-partial-report.md)

El [protocolo congelado](../../../specs/012-conversational-course-study/evidence/semantic-v10-scope-protocol-frozen.json) contiene ocho
controles diagnósticos y dos conversaciones completas de cinco turnos cada una.
La hipótesis v10 era que una decisión independiente, después de proponer un par
de objetivos, retiraría relaciones no pedidas sin perder las relaciones legítimas.
Se fijaron los casos y criterios antes de ejecutar el baseline v9 y editar la
ruta optativa v10. No hay autoridad de publicación ni revisión docente.

- La hipótesis v10 era que una decisión independiente, después de proponer un par
- La comprobación dirigida `test_catalog_planning.py` dio 24 aprobadas y el
- paquete `tests/course_dialogue` dio 151 aprobadas en 150,70 s. Black dejó sin

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/semantic-viability-decision.md

[Fuente](../../../specs/012-conversational-course-study/evidence/semantic-viability-decision.md)

**Decisión:** no integrar otra fase de selección de relación en el tutor. G2 y
SC001 permanecen cerrados. El bloqueo observado no se resuelve con la
reformulación del mismo selector: la ampliación no solicitada persiste cuando
se obliga a escoger primero un objetivo atómico y cuando se pide una
interpretación libre. No se concluye que el modelo sea incapaz en general;
se concluye que el mecanismo actual no ofrece la fiabilidad necesaria para
publicar este curso.

- usó el mismo Qwen3-8B/NF4 local, sin publicar texto. Ante la pregunta solo
- pendiente. La etiqueta correcta en los positivos no compensa la impertinencia
- | Mantener alcance de Feature 012 | Diseñar evidencia semántica independiente por objetivo/relación, con abstención ante duda; revisar las 83 unidades draft y volver a ejecutar transferencia congelada, controles de contenido y regresiones. Hay tres relaciones authored actuales y presupuesto de 30 s/turno. | El coste de autoría/revisión y la tasa de acierto aún no están medidos. No basta añadir un prompt. |
- | Evaluar otro proveedor local | Autorizar investigación/recursos distintos y fijar nuevo protocolo antes de medir; con el modelo actual hay 16,38 GB de pesos cacheados y worker NF4, sin descarga en este ensayo. | Disponibilidad, latencia, memoria y mejora semántica desconocidas; no se debe asumir que un modelo mayor aprobará G2. |

Recibos vecinos: 

## specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/report.md

[Fuente](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/report.md)

Después de interpretar la prueba mínima se ejecutó el paquete preparado ST01–ST04 con el mismo Qwen2.5-7B-Instruct NF4. [Protocolo previo](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/protocol.json): máximo cuatro peticiones y un calentamiento, 2049 tokens nuevos, 30 s por petición, sin reintentos ni ajustes. Generador real, política SQL de solo lectura y fuentes originales vigentes; **sin evaluadores simulados presentados como reales**. El alcance de estas preguntas era metadato de control vinculado a la política, no una medición del clasificador semántico. La ampliación se planificó una vez; no fue un juicio semántico de suficiencia.

- Después de interpretar la prueba mínima se ejecutó el paquete preparado ST01–ST04 con el mismo Qwen2.5-7B-Instruct NF4. [Protocolo previo](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/protocol.json): máximo cuatro peticiones y un calentamiento, 2049 tokens nuevos, 30 s por petición, sin reintentos ni ajustes. Generador real, política SQL de solo lectura y fuentes originales vigentes; **sin evaluadores simulados presentados como reales**. El alcance de estas preguntas era metadato de control vinculado a la política, no una medición del clasificador semántico. La ampliación se planificó una vez; no fue un juicio semántico de suficiencia.
- **Parada en ST01:** «¿En qué se distingue que un requisito sea comprensible de que no sea ambiguo?» La salida finalizó con `stop`, 2065 tokens de entrada, 128 de salida y 5030 ms. No contiene ninguna cita `[id]`; el protocolo detiene la conversación. Se conserva íntegra en [records.json](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/records.json), pero **no se mostró como turno conversacional ni se añadió al historial**. ST02–ST04 quedan no ejecutados: no se inventan reformulación, ejemplo o cambio de tema.
- **Decisión técnica:** detener esta candidata conforme al protocolo. La prueba mínima demuestra capacidades básicas, pero el primer turno RAG no cumple trazabilidad ni justifica su ejemplo. No proceder a seguimientos, banco completo, reserva, publicación o más variantes de prompt para aprobar este caso. Clasificación de alcance completa y verificación semántica independiente continúan pendientes; no se sustituyen por respuestas académicas predefinidas o por un comprobador de citas. La causa interna de la omisión de citas y de la modificación incorrecta del ejemplo no está identificada. No se concluye incapacidad general del modelo.

Recibos vecinos: [worker.json](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/worker.json), [records.json](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/records.json), [protocol.json](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/protocol.json), [review.json](../../../specs/012-conversational-course-study/evidence/study-review-run-2026-10-27/review.json)
