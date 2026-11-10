# Evidencia de implementación — Feature 006

Estado: **cerrada y convergida; 18/18 tareas verificadas**.
Constitución1.0.0 intacta; único escritor, sin commits ni delegación.

## Entrega

CLI local `python -m oralia.validation run/replay`, protocolo cerrado, catálogo sintético,
compositor real, baseline GenerationPort directo, dos ablaciones aisladas, top1/top3,
modo presentación y fallos controlados. Código en src/oralia/validation/; tests en
 tests/validation/. No se modifica código productivo001–005, no se añaden dependencias,
API de ablación, tablas ni migraciones. Las sustituciones scoped viven solo en el proceso
experimental; no se importa el módulo desde interfaces ni UI.

## Evidencia medida

- **837 pruebas deterministas aprobadas**,3deseleccionadas, una advertencia Starlette/httpx.
- **19 pruebas específicas** incluyen contrato, compositor/ablaciones reales, fallos,
  procedencia/faltantes, integridad/cambio de código, replay y subprocess CLI E2E.
- **10 Playwright aprobadas**; build/lint correctos (un aviso ESLint preexistente).
- Black114 archivos acumulados de integración, sin diferencias. Ruff0nuevos/10heredados,
  Counter por ruta/código/mensaje contra baseline001. Lock offline correcto.
- Voz real2skipped: no se cuenta como pasada ni se descargan modelos.

Resultados y comandos: validation-backend.json, validation-frontend.json, ruff-validation.json
 y validation-*.log. Feature006 no cambia esquema; las migraciones limpia/t004→t005
forman parte de la suite y tienen evidencia específica en005.

## Experimento y reproducción

Paquete final `evidence/`: protocol.json, results.json, report.md, manifest.json.
**204 celdas =17escenarios ×6condiciones ×2repeticiones**, semilla42,0errores inesperados.
Replay **matched=true para204celdas**. Logs: experiment-run.log/experiment-replay.log.
El manifiesto registra156archivos de código/lock y valida las entradas antes de reejecutar.
Cada celda lleva modelo/params, componentes/orden, fuentes, decisiones, estado,
recuperación y métricas con fuente/unidad/motivo. Corpus con versión/ubicación/hash.
Hardware observado y límites se incluyen; código no tiene Git y usaSHA256.

El baseline comparte consulta/evidencia/proveedor determinista, sin coordinador de agencia.
Las sondas STT/corrección son auxiliares y se declaran no comparables como latencia de
modelo directo. Fallos sin puerto equivalente en baseline quedan injection_applied=false.
No se interpreta comparación de celdas heterogéneas como efecto causal.

- no_grounding: 34 pares; 6 veredictos y 6 salidas distintas. Coste del verificador completo: media 0.562525ms, n=24; variabilidad registrada.
- no_coherence: 34 pares; 6 veredictos y 6 salidas distintas. Coste del verificador completo: media 0.028642ms, n=26; variabilidad registrada.

Estas diferencias son observaciones sobre fixtures preparadas; no prevalencia de errores
ni prueba de superioridad. Hay bloqueos y fallos inyectados, salidas sin citas y falta de
medición humana. report.md distingue observaciones, métricas, inferencias y evolución.
Se propone conservar controles, ampliar etiquetas y medir modelos/índice reales y un
piloto consentido antes de optimizar. No se activan cambios automáticamente.

## Definiciones y resultados negativos

Trazabilidad completa exige componentes, autorización, final completed/degraded/blocked,
ningún error y cadena continua de parches. El primer cálculo excluía finales bloqueados/
degradados; prueba negativa y corrección documentan la fórmula, sin borrar fallos.
Las cinco condiciones de agencia tienen34/34 trazas y34/34 cadenas reconstruibles en
este catálogo. Baseline tiene porcentaje/reconstrucción null con motivo, sin contar
su fixture vacía como coordinación: corrección T018 surgida en converge.

Retrieval precision/recall usa etiquetas de IDs; denominador cero es null. Ranking
lexical no mide Chroma ni embeddings. Fuentes conflictivas incluyen anotación preparada:
se mide su verificación, no descubrimiento semántico. Los contadores sin citas se basan
en fuentes entregadas, separadas de recuperadas. Reformulación cuenta acciones/veredictos.
Latencias de componentes incluyen transporte de ablation; agentes/composiciones excluyen
sustitutos y puerta final de política. CPU es tiempo del proceso; RSS es muestra, no pico.
Contexto chars no es tokens. GPU/tokenizer/LLM/voz reales y opiniones humanas faltan con
motivo. Reutilización observada: material-retriever, grounding-verifier y coherence-verifier
entre autoestudio y la sonda de defensa. La corrección observa entrada original/corregida
y su uso por el comando real, sin inferencias sobre capacidad de personas.

## Cobertura / constitución

16 FR +6 SC =22/22 requisitos con tareas.5 historias/10escenarios,28/28 ítems de requisitos.
18tareas tras añadir una brecha real en converge (T018). Sin excepciones constitucionales.

| Principio | Evidencia |
|---|---|
| I | Solo métricas de sistema; nota sintética bloqueada aun con ablaciones. |
| II | Agentes/contratos y puertos existentes, sin agentes paralelos ni código generado en runtime. |
| III | Base temporal y StatePatch real; conflicto rechazado y cadena registrada. |
| IV | Compositor y T090 reales; baseline con regla constitucional y diferencia explícita. |
| V | Corpus autorizado/versionado, filtros existentes, grounding independiente; límites del ranking claros. |
| VI | Protocolo manual, flag explícito sintético; ninguna nueva opción de producción. |
| VII | Fixtures incorporadas, sin base real/audio persistente/identidad/secreto; CLI textual. |
| VIII | Hashes, orden/semilla, código, corpus, hardware, decisiones y replay con integridad. |
| IX | Contratos con plazos, timeout1ms de prueba, worker cerrado, modelo/índice/STT caídos y recuperación. |
| X | Contrato/integración/fallos/CLI E2E y regresión global, ambos verificadores ablacionados y negativos. |
| XI | Herramienta local modular, dependencias existentes; sin nuevos servicios/frameworks. |

## Definition of Done del MVP

Autoestudio/defensa comparten execute_agency, contratos, estado/parches y T090/T150;
reutilización observada y probada. El estado no depende de un contexto privado del modelo.
Recuperación autorizada, conocimiento general etiquetado y ausencia de evidencia cubiertos
por regresiones001–005. Salida visible requiere controles independientes. Sesiones se
reconstruyen a partir de configuración/eventos/parches; eliminación conserva solo prueba
operativa mínima según consentimiento. Fallos de generación/RAG/voz degradan o cierran.
Añadir agentes por contrato está cubierto por pruebas del núcleo;006 no modifica orquestador.
Baseline/comparación/replay reales, informe prudente y perfil observado completan validación
arquitectónica. Instalación/demostración/privacidad en docs/MVP.md y README.md.

Voz real y piloto humano son límites explícitos, no tareas obligatorias disimuladas.
No se afirma calidad LLM ni funcionamiento de hardware no probado. Sesiones locales no
requieren Internet; instalación inicial sí necesita dependencias/modelos preparados.

## Registro completo de tareas

| Tarea | Entrega y referencia |
|---|---|
| T001 | Añadir contrato negativo de protocolo/sintético/condiciones/límites en tests/validation/test_protocol.py. (FR-002 FR-003 FR-015 SC-006) |
| T002 | Crear catálogo15 y protocolo validado en src/oralia/validation/protocol.py. (FR-004 FR-005 FR-011 FR-015) |
| T003 | [US1] Añadir pruebas reales baseline/agencia y precisión/trace en tests/validation/test_experiment.py. (FR-001 FR-007 FR-008 SC-001 SC-002) |
| T004 | [US1] Implementar fixtures aisladas, baseline directo y compositor real con instrumentación en src/oralia/validation/experiment.py. (FR-001 FR-003 FR-004 FR-007 FR-008 FR-011) |
| T005 | [US2] Probar autorización y efecto real de ambas ablaciones sin mutación posterior en tests/validation/test_experiment.py. (FR-002 FR-003 SC-006) |
| T006 | [US2] Implementar sustituciones scoped de verificador solo en runner sintético en src/oralia/validation/experiment.py. (FR-002 FR-003 FR-004) |
| T007 | [US3] Añadir matriz de fallos, rollback/recuperación/estado y borrado en tests/validation/test_failures.py. (FR-005 FR-006 FR-009 SC-004) |
| T008 | [US3] Implementar inyecciones reales y métricas con procedencia/faltantes en src/oralia/validation/experiment.py. (FR-005 FR-006 FR-007 FR-008 FR-009 FR-010 SC-002) |
| T009 | [US4] Probar integridad, límites, cambio código y replay estructural en tests/validation/test_reporting.py. (FR-011 FR-014 SC-003) |
| T010 | [US4] Implementar paquetes/manifiesto/replay con hashes en src/oralia/validation/reporting.py. (FR-011 FR-012 FR-014 FR-015) |
| T011 | [US5] Probar indicadores humanos ausentes, denominadores y prudencia en tests/validation/test_reporting.py. (FR-010 FR-012 FR-013 SC-005) |
| T012 | [US5] Implementar informes comparativos/agregados/propuesta evolución en src/oralia/validation/reporting.py. (FR-007 FR-008 FR-009 FR-010 FR-012 FR-013 SC-005) |
| T013 | [US5] Añadir CLI textual y prueba subprocess E2E en src/oralia/validation/__main__.py y tests/validation/test_cli.py. (FR-015 FR-016 SC-006) |
| T014 | Ejecutar catálogo completo/replay y archivar paquete real en specs/006-architecture-validation/evidence/ y quickstart.md. (FR-001 FR-002 FR-004 FR-005 FR-006 FR-011 FR-014 SC-001 SC-002 SC-003 SC-004 SC-005) |
| T015 | Ejecutar suite global, Black/Ruff Counter, lock y frontend build/lint/Playwright en specs/006-architecture-validation/validation-*.json. (FR-016) |
| T016 | Revisar principios/checklists/cobertura y análisis final en specs/006-architecture-validation/analysis-report.md. (FR-003 FR-016 SC-006) |
| T017 | Ejecutar convergencia append-only y consolidar evidencia completa en specs/006-architecture-validation/implementation-evidence.md. (FR-016) |
| T018 | Marcar reconstrucción arquitectónica del baseline como no aplicable con motivo, sin contar la cadena vacía de la fixture; probar en tests/validation/test_reporting.py y corregir src/oralia/validation/reporting.py; regenerar paquete/replay e informe con medidas actuales por FR-009 y SC-002 (partial, HIGH). |

Cierre confirmado tras la última regresión:837passed en103.63s, replay204matched,
paquete íntegro con hashes de código actuales. Análisis y dos pasadas de convergencia
archivados en analysis-report.md. El único hallazgo F1 quedó resuelto mediante T018.
