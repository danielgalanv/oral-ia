# Comparación pareada guiada/directa — 19-10-2026

**No demuestra superioridad educativa ni conversacional.** Ambas condiciones cumplen
las propiedades de contenido medidas en 23/24 casos; H02 sigue fallando recuperación.
La agencia registra sus controles independientes; el comparador directo no los ejecuta.
Esa diferencia de cobertura es parte de la arquitectura y no se cuenta como mejora de
calidad por sí misma. G1 continúa no aprobada.

| Condición | Casos de contenido aprobados | Turnos observados | Mediana backend | Máximo observado |
|---|---:|---:|---:|---:|
| Agencia guiada | 23/24 | 186 | 46 ms | 47 ms |
| Baseline directo adaptado v2 | 23/24 | 186 | 46 ms | 295 ms |

Una ejecución determinista por condición/caso, orden contrabalanceado. No se atribuye
una mejora de rendimiento causal a esas diferencias. El tiempo del backend corresponde
al campo registrado por cada turno; `elapsed_ms` de cada caso incluye además HTTP y
oráculos. El proveedor de unidades revisadas no invoca LLM por diseño; el experimento
no mide tokens de inferencia ni costes de un modelo generativo real.

Se ejecutaron los 24 guiones originales en ambas condiciones con los mismos paquetes,
versiones, políticas, límites (16 turnos/600 s y presupuesto de turno de 10 000 ms),
proveedor controlado e inputs. El harness comprueba igualdad del hash de material.
La selección y renderizado son comunes; cambia el uso de intérprete por puerto de
agente y verificadores independientes frente a la vía directa. La adaptación mantiene
T090, T150, preflight, contexto transaccional, permisos de fuente y borrado. Dos pruebas
públicas verifican que no llama al agente de fundamentación y sí persiste aprobación
T090 vinculada, para después purgar contenido sin conservación.

`src/oralia/validation/guided_baseline.py` es una adaptación del comparador directo al
contrato v2, necesaria para igualar proveedor y contenido. No es un modelo seleccionable
en la aplicación, agente nuevo ni endpoint público. En las pruebas se selecciona esa
implementación real explícitamente; no se reemplazan sus respuestas por resultados
favorables. Las 256 ausencias de verificadores del baseline se publican separadamente
de los fallos de contenido. No acreditan 256 errores de respuesta.

Comando: `ORALIA_RUN_GUIDED_PAIRS=1` y un `ORALIA_DIALOGUE_RUN_ID` nuevo al ejecutar
`uv run --no-sync pytest tests/dialogue/test_paired_comparison.py -q` desde PowerShell.
Las 24 pruebas aprobadas significan que se registraron las parejas y se verificaron
materiales iguales, no que los 48 recorridos cumplieran aceptación. Datos por caso en
paired-runs/2026-10-19-paired-first; resumen en paired-summary.json y código exacto en
paired-source-20261019.zip, con manifiesto separado. La primera reserva original no se
reescribe ni se vuelve a etiquetar como nueva aceptación.


## Repetición sobre código archivado actual

paired-runs/2026-10-19-paired-verified y paired-verified-summary.json:
24/24 casos de contenido aprobados en cada condición, 186 turnos por condición,
misma fuente/material y presupuesto. Agencia: 24/24 propiedades completas;
baseline: ausencias de verificadores independientes separadas, no errores de contenido.
Mediana backend observada 47 ms en ambas; máximos 375/454 ms. Hubo otras validaciones
en el host: no comparación causal de rendimiento ni prueba de superioridad educativa.
Las 24 pruebas de registro pasan en 83,08 s. Código archivado en source-checkpoint-20261019.zip.
El primer resultado 23/24 por condición se conserva y no se sustituye por esta repetición.


## Estado medido tras correcciones semánticas — 19-10-2026

Estado actual: **65/72 tareas completadas**, siete abiertas o parciales: T053/T054/T055/T056/T061/T065/T067. No se declara cierre.

- Global: 1139 aprobadas, 879 omitidas explícitamente (evaluaciones optativas), un aviso Starlette/httpx, 227,65 s.
- Playwright completo: 21/21, 2,4 min; dirigido guiado 6/6, 2,3 min. Build y lint aprobados.
- Black: 114 archivos afectados sin cambios; Ruff Counter(ruta,código,mensaje) con multiplicidad frente al baseline durable: 10 heredados, 0 nuevos, 39 retirados.
- Diálogos públicos actuales: 24/24 D+W; herramientas 16/16. Reserva de clasificación séptima: 48/48, incluidas 36 críticas; permisos públicos 48/48. Ciclos anteriores y primeros fallos permanecen publicados. Ciclos6/7 no añaden diálogos nuevos: los 12W pasaron primero en ciclo5 y se demuestra rama inalterada en 1150 contextos más reproducción pública actual.
- Pareado: contenido 24/24 en ambas condiciones; 186 turnos por condición, mediana32 ms y máximo47 ms en ambas. La cobertura de verificadores independientes es distinta; no se afirma superioridad educativa ni mejora causal de rendimiento. paired-semantic-summary.json.
- Paquete nuevo evidence-semantic-current-20261019: 204 celdas, cero errores y replay coincidente. Los cuatro paquetes originales006–009 siguen íntegros y coinciden en protocolo/resultados estructurales; experimental-reproduction-semantic-current.json.
- Guard de navegador: 229 archivos, cero cambios nuevos. Seis pérdidas históricas anteriores siguen sin restauración; esta cifra no acredita recuperación.
- Fuente congelada: source-semantic-current-20261019.json/zip, 560 archivos verificados; 200 rutas nuevas/modificadas frente al baseline inicial en changed-code-files-semantic-current.json. La última edición de estilo conserva AST idéntico (semantic-format-equivalence.json); replay experimental corresponde a bytes actuales.
- Revisión técnica IA: technical-dialogue-audit-current.md; revisión humana requerida: human-system-review-current.md, 24 diálogos y todos los campos No evaluado. G2 no habilitado; utilidad humana y voz real pendientes.
- Datos habituales, demo personal y fixtures mantienen sus tres SHA. Demo aislada preparada y detenida; puertos8026/5196 libres. Sin Reset, commits ni cierre de procesos ajenos. operational-semantic-final-readonly.json.

Comandos/evidencia: .claude-scratch/feature010-global-semantic.{log,xml}, feature010-playwright-semantic-full.log, feature010-semantic-corpora-verified.{log,xml}, feature010-seventh-public.xml, feature010-paired-semantic.{log,xml}, feature010-experimental-semantic-current{,-replay}.log; format-validation-semantic.json. El ensayo PowerShell aislado previo sigue registrado en operational-rehearsal/result.json: arranques33,687 s y16,141 s, sin acreditar arranque frío ni desconexión física. No se repite la preparación ni se duplican datos.
