# Feature008 — implementación y evidencia

2026-10-18. Ciclo specify→clarify(0preguntas)→plan→checklist→tasks→analyze→implement→converge.
feature.json actualizado mediante flujo SpecKit; sin commits, Reset ni cambios de arquitectura.

## Uso y comportamiento

Desde D:\Proyecto personal\ORALIA:

```powershell
.\scripts\demo.ps1
.\scripts\demo.ps1 -Action Check
.\scripts\demo.ps1 -Action Stop
```

Mensajes en español `[INICIO]`, `[ESPERA]` con tiempo de etapa aproximadamente cada5s,
`[OK]` después de la operación, `[FALLO]` con etapa/causa/acción y `[CANCELADO]` distinto.
Proceso API/interfaz iniciado no significa disponible. DEMO LISTA/URL/Stop/navegador
solo después del nonce de ambos servicios. NoBrowser/puertos/Start/Check/Stop/Reset intactos.
Check no solicita credencial, conserva JSON stdout y añade progreso stderr. TextOnly
omite carga de embeddings y no anuncia fuentes disponibles. UTF-8 también en Python directo.

## Auditoría de duplicación

Antes: CLI start→check completo→supervisor start→check completo, con dos embed en el
mismo proceso. Después: CLI delega callback de credencial; supervisor obtiene bloqueo,
hace un check y luego pide credencial. Seguridad sin ventana de preflight fuera del lock.
Conservados verify_schema/preparación en su hijo y calentamiento API en proceso distinto;
preparación puede indexar si no hay seed, operación distinta de comprobar caché. Validación
ligera Node/Vite justo antes de crear procesos permanece. No se afirma mejora causal de
rendimiento. No cambia el modelo, índice ni proveedor ni se descarga silenciosamente.

## Resultados medidos / comandos

| Comando o ensayo | Resultado | Evidencia |
|---|---|---|
| uv run --no-sync pytest tests/ -q -m "not ollama and not speech" | 863passed,3deselected;121.00s pytest,126.56s comando | validation-deterministic.log / validation-backend.json |
| uv run --no-sync pytest tests/ -q -m speech | 2skipped,864deselected | validation-speech.log |
| uv run --no-sync pytest tests/demo -q | 26passed;74.68s ensayo inicial,17.36s en check-demo | validation-demo-tests.log / validation-check-demo.log |
| .\scripts\check-demo.ps1 | exit0;81.03s;3checks aprobados | check-demo-result.json / validation-check-demo.log |
| pnpm.cmd --dir apps/web build | exit0;4.55s | validation-build.log |
| pnpm.cmd --dir apps/web lint | exit0;23.17s | validation-lint.log |
| pnpm.cmd --dir apps/web test:e2e | 11passed;68.12s comando | validation-test-e2e.log |
| Black --check inventario afectado | 5archivos Python,exit0 | python-files.json / validation-black.log |
| Ruff src/tests Counter(ruta,código,mensaje),multiplicidad | 10heredados,0nuevos | ruff-validation.json;baseline001durable |
| Ruff cinco archivos afectados | 0hallazgos | ruff-affected.json |
| uv lock --check --offline | exit0 | validation-lock.log |
| python -X utf8 -m oralia.validation run --output specs/008-demo-startup-progress/evidence-current --repetitions 2 --seed 42 --authorize-synthetic-ablations | 204celdas actuales | evidence-current / validation-experiment.log |
| python -X utf8 -m oralia.validation replay --package specs/008-demo-startup-progress/evidence-current | matched true,204celdas | validation-replay.log |
| uv run --no-sync python -X utf8 specs/008-demo-startup-progress/rehearse.py | dos arranques PowerShell reales,noReset,centinela vivo | validation-demo.json / rehearsal-start-*.log |

Primer arranque observado preparado:17,875s hasta DEMO LISTA (ciclo19,953s).
Posterior:17,688s hasta DEMO LISTA (ciclo19,547s). Ambos NoBrowser; nonce API/interfaz
comprobados con HTTP real. Primer observado no equivale a caché fría ni instalación:
ya había recursos locales y pruebas previas. Cadencia/etapas medidas en rehearsal-start-
0-events.json y1-events.json. No inferencia de aceleración a partir de estas duraciones.

Conservados18archivos estables demo/habituales, incluyendo DB/índice/material/fixtures;
ningún Reset del entorno preparado. Control de puerto ocupado mantuvo centinela vivo.
Las pruebas TextOnly y de reset existentes usan únicamente workspaces temporales propios.
Credencial ficticia aleatoria solo en entorno de proceso; inspección de consola/logs
sin hallazgos; errores inyectados demuestran redacción y causa no determinada sin
presentarlos como fallos reales. Pruebas previas fallaron antes de añadir progress.py y
la regresión descubrió codificación CP1252 en Python directo; se corrigió en CLI y todas
las regresiones finales pasan. Logs de esos pasos conservados como diagnóstico de trabajo.

## Tabla completa de tareas

| Tarea | Estado | Implementación / evidencia |
|---|---|---|
| T001 | Completada | baseline.json, feature007-original-source.zip, preservation.json; originales006/007 intactos |
| T002 | Completada | test_progress.py: secuencia full/TextOnly/Check, heartbeat y retirada del preflight redundante |
| T003 | Completada | progress.py + launcher.py; rehearsal-start-*-events.json: etapas reales,espera5s,readiness antes de listo |
| T004 | Completada | test_progress.py: error conocido/desconocido,redacción y KeyboardInterrupt; test_supervisor.py timeout/limpieza real |
| T005 | Completada | progress.py + __main__.py: diagnóstico saneado,causa no determinada,avisador cerrado antes de estado terminal |
| T006 | Completada | CLI callback dentro lock; Check stdout JSON; check de API y preparación conservados; auditoría research.md |
| T007 | Completada | validation-demo.json:2arranques full,noReset,18hashes,centinela; check-demo-result.json:3checks exit0; tests26 incluyen TextOnly temporal |
| T008 | Completada | docs/DEMO.md; este informe con guion de mensajes/tiempos/tareas/inventario |
| T009 | Completada | validation-backend.json + validation-frontend.json;863deterministas,11Playwright,Black5,Ruff0nuevos |
| T010 | Completada | evidence-current; validation-replay.log:204 matched; preservation.json:2fuentes modificadas+1nueva |
| T011 | Completada | analysis-report.md sin críticos; converge-report.md sin brechas; cierre documental |

## Archivos modificados o nuevos

- `src/oralia/demo/progress.py`
- `src/oralia/demo/launcher.py`
- `src/oralia/demo/__main__.py`
- `tests/demo/test_progress.py`
- `specs/008-demo-startup-progress/rehearse.py`
- `docs/DEMO.md`
- `.specify/feature.json`

Además, artefactos nuevos bajo specs/008-demo-startup-progress: spec/plan/research/modelo,
contrato/quickstart,2checklists,coverage/tasks,informes/inventarios JSON/logs,
snapshot ZIP y paquete experimental actual. scripts/demo.ps1/check-demo.ps1 y frontend
no cambiados. No esquema/migración nuevos. Las únicas fuentes modificadas del manifiesto
previo son demo/__main__.py y demo/launcher.py; progress.py es nueva. Paquetes originales
006/007 conservan hashes, registrados en baseline.json/preservation.json, y fuente previa
archivada. Nunca editar hashes para aparentar reproducción del código previo.

## Límites y cierre

Los avisos indican operación en curso, no avance interno garantizado ni porcentaje/ETA.
Las bibliotecas pueden emitir sus propios contadores de pesos medidos. El traceback
saneado se guarda solo si raíz demo válida/escribible; no se crean rutas de diagnóstico
fuera del límite. Las operaciones siguen en hilo principal y solo el avisador usa hilo;
no es un nuevo servicio. Timeouts preparación120/readiness90/Stop20 se mantienen.
La cancelación limpia hijos propios; no cierra navegador ni otros procesos. No valida
voz real/LLM/utilidad humana;204celdas siguen siendo evidencia sintética determinista.
La demo queda preparada full y detenida, sin modificar sus datos ni los habituales.
Cierre: analyze sin contradicciones críticas y converge sin brechas obligatorias.
