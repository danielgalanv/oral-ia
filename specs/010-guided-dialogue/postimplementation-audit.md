# Auditoría postimplementación — 19-10-2026

Estado: implementación técnica validada; **no cierre ni converged**.

Analyze solo lectura: 33 FR, 9 SC, 20 escenarios, 7 decisiones, 11 principios y
66 tareas iniciales; 100% de requisitos con cobertura, sin tareas huérfanas ni
contradicciones críticas de intención entre spec/plan/tasks. La preservación es una
brecha real de implementación/evidencia, no una excepción constitucional autorizada.

| Hallazgo | Gravedad | Evidencia | Acción |
|---|---|---|---|
| Preservación histórica incompleta | CRITICAL | 6/229 hashes distintos; incident.json conserva originales | T061, restauración exacta pendiente de copia |
| Revisión humana de sistema sin realizar | HIGH | plan.md G1 exige revisión; human-system-review.md tiene 24 diálogos y rúbrica No evaluado | T067 explícita; pendiente de respuesta humana |

Converge revisó el estado actual; añadió solamente Phase 2 / T067 a tasks.md.
No duplicó T061. No modificó spec, plan ni código durante su operación. Resultado:
tasks_appended, no converged. Sin hooks configurados en .specify/extensions.yml.
El registro y conteos posteriores se actualizaron bajo implement; 60/67 completas.

1080 pruebas globales, 21 Playwright, 24 diálogos observados, 48 probes públicos,
16 herramientas y replay204 pasan. El clasificador cumple 46/48 y 36/36 críticos,
con dos fallos ordinarios conservados. Las 471 omisiones globales son evaluaciones
con flags explícitos, cuyos resultados se registran aparte; no aprobaciones inferidas.
Black105, Ruff10 heredados/0 nuevos con multiplicidad; build/lint pasan.
Parejas24: 24/24 propiedades de contenido en ambas condiciones; no superioridad causal.

La revisión del sistema no se sustituye por asserts ni por anotación automática.
G2 permanece no aprobado; utilidad humana y voz real G3 no se han validado.
No se modifican hashes históricos para aparentar restauración. Demo aislada preparada
y detenida; base habitual y demo personal mantienen sus tres hashes; sin commits ni Reset.

Inventarios: changed-code-files-20261019.json y source-checkpoint-20261019.json.
Comandos y límites: quickstart.md e implementation-evidence.md.
Tabla íntegra: task-evidence.md.


Actualización de recuperación: la búsqueda independiente documenta 41.595 archivos, 2.112 candidatos por contenido, 37 comprimidos y 2.990 miembros, cero coincidencias exactas. No hay copia recuperable identificada; no se solicita una ruta desconocida. T061 permanece como pérdida de evidencia sin restauración acreditada, pendiente de disposición explícita de la incidencia. Detalle en preservation-incident/loss-disposition.md. Los hashes originales se conservan intactos.


Revalidación actual, separada de la restauración: preservation-incident/revalidation-20261019-162715/report.md,
**3/3 Playwright aprobados (1,4 min)** para carga normal/lenta/error del archivo04.
Normal201/processed en10.584 ms; lento201/processed en19.155 ms (16.000 ms artificiales,
endpoint3.094 ms); error422 en49 ms. Una petición por caso. Guard229 archivos/0 cambios.
Se verificó el manifiesto SHA nuevo sin discrepancias. Evidencias nuevas agrupadas en evidence/;
no sobrescriben el histórico ni recuperan sus bytes. No prueban G1, voz o utilidad humana.
T061 no se marca restaurada y la revisión humana de sistema sigue independiente.


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
