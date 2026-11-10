# Resultados medidos de aceptación — 19-10-2026

G1 **NO APROBADA**. G0 pendiente de regresión final y operación; G2 no aprobada;
G3/voz real y utilidad con personas no evaluadas. Ningún resultado sintético se
presenta como validación humana ni como inferencia generativa libre.

| Conjunto | Aprobados | Total | Estado |
|---|---:|---:|---|
| Desarrollo inicial | 4 | 12 | 8 fallos conservados |
| Desarrollo 02 | 11 | 12 | Recuperación general pendiente |
| Desarrollo 03 | 12 | 12 | Propiedades medidas, renderer real |
| Primera reserva de diálogos | 11 | 12 | H02 falla recuperación en dos turnos |
| Primera reserva de actos | 37 | 48 | No alcanza 44; 26/36 críticos coinciden |

Los 24 diálogos se ejecutaron mediante API pública y proveedor efectivo
`reviewed-unit-renderer/v1`. Las 48 entradas adicionales se ejecutaron contra el
intérprete v2 real, con contexto sintético tipado; miden clasificación, no 48 ensayos
públicos de autorización. Las matrices públicas de acceso/privacidad son evidencia
separada. Se mantienen todos los resultados por caso, incluyendo fallos, en
`development-runs/` y `holdout-runs/2026-10-19-first-reserved/`.

Las primeras dos ejecuciones de desarrollo descubrieron pérdida de tema al cambiar
modo, repetición parcial de composiciones, avisos idénticos y límites del ranking
léxico. Se añadieron regresiones antes de corregirlos. El tercer desarrollo pasa.
La reserva se ejecutó después y sigue fallando: no se han corregido sus oráculos,
editado los archivos congelados ni vuelto a contar esos fallos como aprobación.
Deben pasar a regresión de desarrollo y sustituirse por casos nuevos revisados,
congelados antes de un nuevo ajuste, conforme a acceptance-matrix.md.

El runner verifica vínculos persistidos de propuesta/veredicto, proveedor, fuente
actual, estabilidad de pregunta, no revelación en contenido/fuentes, presupuesto,
no notas y recuperación efectiva. La salida fija de cierre que se elimina en la
misma transacción se contrasta además con el catálogo manual autorizado y el
veredicto persistido: no se exige conservar texto que la política obliga a borrar.
Una confirmación explícita de tema puede sustituir la pregunta; un control simple
no puede hacerlo. Estos dos límites del oráculo se corrigieron durante desarrollo
y no a partir de reserva. No hay rúbrica de utilidad humana aplicada.

Las 16 conversaciones de herramientas siguen pendientes de ejecución con observación
completa por operación/argumentos/rol/efecto; la presencia de sus JSON no cuenta como
prueba. La comparación pareada v2 y el replay experimental separado también siguen
pendientes. Fuente/entorno de la primera reserva en evaluation-environment.json.


## Segunda reserva — 19-10-2026

Conjunto nuevo congelado antes de modificar gramática/foco/objetivo inicial: 12/12 conversaciones, 30/48 actos y 22/36 críticos. **G1 no aprobado**. Informes originales inmutables en holdout-runs/2026-10-19-second-reserved; denominadores en second-reserved-summary.json. Los 18 fallos de actos se reabrieron como desarrollo. La regresión posterior junto con los 12 casos reabiertos del primer ciclo pasa 72 pruebas en 23,85 s; no se reutiliza como aceptación fresca. Revisión sintética por el implementador, sin validación humana independiente ni utilidad acreditada.


## Tercera y cuarta reservas — resultados conservados

Tercer ciclo: 46/48 actos y 34/36 críticos; G1 no aprobado. Seis diálogos orales
no se registraron por un KeyError del runner: trataba study_mode como obligatorio
incluso en defensa. La corrección inicial cubrió el inicio y otra corrección cubrió
el metadato del informe. Los dos fallos de mapeo se conservan. La regresión completa
posterior pasa 60/60 en 24,00 s; no se cuenta como aceptación nueva.

Cuarto ciclo: **12/12 diálogos y 46/48 actos, 36/36 críticos**. Se cumple el umbral
clasificatorio de 44/48. Fallos ordinarios publicados: saludo compuesto «Hola, buenas
tardes» y «¿Puedes releer la pregunta?». No se declara comprensión general del español.
Las 48 entradas se someten además a una matriz pública de permisos separada; su
resultado y SC-009/suites completas siguen siendo necesarios para aprobar G0/G1.
Anotación sintética por el implementador: no revisión humana independiente ni
validación de utilidad. Las tres reservas anteriores, sus fallos y hashes se conservan.

Las conversaciones de herramientas ya ejecutadas y la comparación pareada original
están documentadas en synthetic-tool-results.md y paired-comparison.md; los párrafos
anteriores que decían pendientes reflejan el estado de aquel punto de control.


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


## Pase de orientación accionable

67/74 tareas completadas.23/23 Playwright actuales,3/3 API dirigida, build/lint y Ruff sin nuevos. Backend intacto: se conserva global1139 y replay204 previos, sin repetirlos. Detalle: [informe](orientation-validation/report.md). [Revisión humana por bloques](human-review-blocks/README.md); pérdida histórica y T067 siguen abiertas.
