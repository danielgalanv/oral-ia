# Feature007 — implementación y evidencia

Fecha2026-10-18. Ciclo specify→clarify(0 preguntas)→plan→checklist→tasks→analyze→implement→converge.
feature.json apunta a007 mediante flujo previsto. Sin commits ni reinicio del proyecto.
Demo preparada con perfil full, servicios detenidos; ningún dato personal real.

## Arranque y presentación

Desde D:\Proyecto personal\ORALIA:

```powershell
.\scripts\demo.ps1
```

Elegir credencial oculta de24 caracteres o más y usarla al entrar en Área docente.
API8010/web5180; apertura automática solo con ambos preparados. Preparación, parada,
Reset confirmado BORRAR DEMO, recursos y problemas en [DEMO.md](../../docs/DEMO.md).
Guion: portada/acceso(1min), material/actividad(1), autoestudio con pregunta del agua y
fuentes reales/elección de conservación(3), cierre/revisión(1), exportaciones(2),
borrado(1), defensa textual efímera/límites(1). Total aproximado10min.

## Resultados medidos

| Puerta | Resultado | Evidencia |
|---|---|---|
| Suite determinista global | 853 passed,3 deselected;114.21s pytest/120.33s comando | validation-deterministic.log, validation-backend.json |
| Voz opcional | 2 skipped; ninguna validación real de voz | validation-speech.log |
| Frontend build/lint | ambos exit0;2.08s/1.15s | validation-frontend.json y logs |
| Playwright completo | 11 passed;67.49s comando;demo2.1s | validation-test-e2e.log |
| Black afectado | 17 archivos .py;exit0 | validation-black-final.log |
| Ruff estructural | Counter(ruta,código,mensaje), multiplicidad:10 heredados,0 nuevos | ruff-validation.json; baseline001 durable |
| Lock dependencias | uv lock --check --offline exit0 | validation-lock.log |
| Migraciones | Limpia y desde005;32 tablas aplicación/columnas y lock real | tests/demo/test_migrations.py incluido en853 |
| PowerShell real | 3 ciclos;cancelar/borrar/repetir/apertura browser/parar | validation-demo.json y rehearsal-start-*.log |
| Aislamiento | 7 hashes habituales iguales, proceso ajeno vivo;sin secretos en argumentos/logs | validation-demo.json |
| Offline preparado | embeddings/Chroma reales, sockets externos prohibidos;HTTP navegador externo bloqueado | test_offline.py + Playwright |
| Experimento actual | 204 celdas;replay matched true | evidence006-current;validation-replay.log |
| Original006 | 4 archivos conservan SHA256;fuente original archivada | baseline006.json;preservation006.json |

Los valores cycle_seconds18.375/6.703/32.625 incluyen operaciones de cada ciclo, no son
latencias de arranque. Hardware y recursos del experimento están en results.json.
El primer inventario Black incluyó por error12 archivos pyc; se corrigió a17 fuentes y
se repitió Black correctamente. Se mantiene el diagnóstico inicial, sin ocultar el fallo.

## Tabla completa de tareas

| Tarea | Estado | Implementación / evidencia |
|---|---|---|
| T001 | Completada | baseline006.json; feature006-original-source.zip; preservation006.json |
| T002 | Completada | tests/demo/test_launcher.py y test_supervisor.py; suite853 |
| T003 | Completada | src/oralia/demo/resources.py, launcher.py; validation-demo.json |
| T004 | Completada | src/oralia/demo/__main__.py; scripts/demo.ps1; ensayo PowerShell3 ciclos |
| T005 | Completada | tests/demo/test_fixtures.py; test_offline.py; IDs iguales en rearranque |
| T006 | Completada | fixtures.py: ingest/activate/publish reales, dos modos y retención1día |
| T007 | Completada | test_lifecycle.py y test_supervisor.py: cancelación, junction, recibo ajeno, fallo parcial y reset activo |
| T008 | Completada | Inicio/Gobierno/main; Playwright11 aprobado |
| T009 | Completada | Autoestudio/DefensaOral/vite.config; links por modo y config/cache propios |
| T010 | Completada | test_demo_journey.spec.ts; validation-test-e2e.log: recorrido2.1s |
| T011 | Completada | test_offline.py: socket externo prohibido, embeddings/Chroma reales; defensa efímera404 en navegador |
| T012 | Completada | docs/DEMO.md; quickstart.md; contrato CLI |
| T013 | Completada | validation-demo.json: tres ciclos, centinela vivo, siete hashes habituales iguales |
| T014 | Completada | preservation006.json; evidence006-current; validation-replay.log:204 matched |
| T015 | Completada | validation-backend.json; validation-frontend.json; ruff-validation.json |
| T016 | Completada | analysis-report.md:22/22 requisitos,19 tareas,0 contradicciones críticas |
| T017 | Completada | implementation-evidence.md; converge-report.md; tabla e inventario |
| T018 | Completada | test_migrations.py: instalación limpia y upgrade005;32 tablas y lock acquire/release reales |
| T019 | Completada | test_cookie_isolation.py: login/logout cruzado; nombres por app, Vite envDir aislado |

## Archivos afectados

Inventario de código/configuración/documentación fuera de este paquete (sin Git, no un
diff de repositorio); todos los archivos de specs/007 son artefactos nuevos de la feature.

- `tests/demo/test_supervisor.py`
- `tests/demo/test_offline.py`
- `tests/demo/test_migrations.py`
- `tests/demo/test_lifecycle.py`
- `tests/demo/test_launcher.py`
- `tests/demo/test_fixtures.py`
- `tests/demo/test_cookie_isolation.py`
- `src/oralia/demo/__main__.py`
- `src/oralia/demo/__init__.py`
- `src/oralia/demo/resources.py`
- `src/oralia/demo/launcher.py`
- `src/oralia/demo/fixtures.py`
- `tests/e2e/run_demo.py`
- `src/oralia/interfaces/api/deps/local_access.py`
- `src/oralia/interfaces/api/routers/governance.py`
- `src/oralia/interfaces/api/routers/participante.py`
- `src/oralia/infrastructure/db/migrations/versions/t007_index_rebuild_lock.py`
- `scripts/demo.ps1`
- `.gitignore`
- `.specify/feature.json`
- `README.md`
- `docs/DEMO.md`
- `apps/web/src/routes/Inicio.tsx`
- `apps/web/src/routes/Gobierno.tsx`
- `apps/web/src/routes/Autoestudio.tsx`
- `apps/web/src/routes/DefensaOral.tsx`
- `apps/web/src/main.tsx`
- `apps/web/src/vite-env.d.ts`
- `apps/web/vite.config.ts`
- `tests/e2e/playwright.config.ts`
- `tests/e2e/test_demo_journey.spec.ts`

El paquete007 añade spec, plan, research, modelo, contrato, quickstart, cobertura,
4checklists, tareas, análisis, convergencia, inventarios JSON, logs de validación,
snapshot ZIP y evidencia experimental actual. Scratch y datos demo están ignorados.
Los únicos3 archivos fuente modificados del manifiesto006 son local_access.py,
governance.py y participante.py: aislamiento de nombres de cookies. Se registran
6 nuevas fuentes del manifiesto (demo y migración); se generó/run/replay un paquete nuevo,
sin editar hashes del antiguo ni alterar contratos cognitivos.

## Limitaciones y decisiones

Generación determinista extractiva; embeddings y recuperación local reales en full.
El experimento204 usa fixtures sintéticas y ranking léxico: no mide rendimiento de
LLM/Chroma ni utilidad humana. Voz real y utilidad con personas siguen sin validar.
TextOnly es degradación sin fuentes, probada con fallo inyectado explícitamente;
no se presenta como recuperación ni como evidencia real de voz. Dependencias y caché de
embeddings deben prepararse antes de desconectar. No descarga automática ni bypass.
El ensayo bloquea red externa a nivel socket/navegador; no afirma una desconexión física
del equipo completo. Una sesión interactiva activa. Las exportaciones descargadas al
navegador no se borran por eliminar datos del servidor. Cookies y recursos están aislados,
pero un administrador del sistema local sigue pudiendo inspeccionar procesos/archivos.
Bloques JSON y rediseño general quedan posteriores; no se añaden agentes ni arquitectura.

Cierre completado: analyze sin críticos y converge sin brechas obligatorias. 19/19 tareas completadas.
