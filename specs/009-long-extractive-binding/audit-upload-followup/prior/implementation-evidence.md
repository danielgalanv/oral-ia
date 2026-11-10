# Feature 009 — implementación y evidencia

18 de octubre de 2026. Autorización humana «pide corregirlo» verificada leyendo el chat
auditor; estaba idle antes de editar. Ciclo SpecKit completo, feature.json=009.
Sin commits ni Reset de la demo preparada, sin agentes/modelos/dependencias nuevos.

## Causas comprobadas y corrección

Hay dos defectos independientes:

1. El adaptador recorta una ventana de400 caracteres, pero el binder exigía fragmentos
completos. Reproducción en fuente008 archivada: fragmento800→candidato397→salida nula,
invalid_context. Helper cerrado material-excerpt/v1 preserva strip/último espacio/elipsis.
El composer reconstruye desde fila DB vigente tras comprobar curso/asignación/id/doc/
versión/ubicación/texto completo y política/scope/recipient/disclosure. Solo texto completo
o proyección canónica exacta obtiene slots. No subcadenas arbitrarias, ni offsets/hashes
del generador como autoridad. Plantillas, snapshot y verificador T090 sin cambios.
La referencia incluye perfil/hash/rango; solo la propuesta aprobada genera traza metadata.

2. El archivo04 original se extrae por líneas, con fragmentos recuperados menores400.
Su bloqueo concreto era una falsa contradicción: coherencia extendía la negación de
«No contiene datos de personas» a otras oraciones de la fuente. Se compara polaridad
por pares de oraciones, conservando el umbral léxico y las contradicciones explícitas
entre fuentes/historial. Copiar una fuente no exime las demás. No equivale a comprender
toda negación o semántica. No se atribuye el fallo concreto04 solo al recorte.

Archivo04 intacto:659bytes/644puntos Unicode crudos; SHA256
8d9f065a557f2bd274dbe579f19cad4c1523fc3969e04802986a9e76002eeca9.
Un bloque sintético largo adicional por HTTP real aísla el defecto400 de ese caso04.
Se añadió únicamente processed al botón Activar de Área técnica, ya permitido por API.
Sin esquema/migraciones ni cambios de políticas, T090/T150, fallback o límites.

## Resultados medidos / comandos

| Comando o ensayo | Resultado | Evidencia |
|---|---|---|
| pytest tests/integration/test_teacher_material_pack.py -q -k '04-caso and self_study', antes | 2failed,6deselected;8.29s | reproduction-before.log |
| Código008 archivado,fragmento800,candidato397 | blocked/null/invalid_context | reproduction-prior-binding.log;prior-source.zip |
| pytest tests/contract/test_coherence_verifier_agent.py tests/integration/test_teacher_material_pack.py tests/integration/test_long_extractive_binding.py -q | 62passed;17.28s | validation-targeted-final.log |
| pytest tests/integration/test_teacher_material_pack.py -q, aserciones finales | 24passed;16.12s | validation-http-final.log |
| uv run --no-sync pytest tests/ -q -m "not ollama and not speech" | 921 passed, 3 deselected, 1 warning in 113.30s (0:01:53);117.53s comando | validation-deterministic.log/validation-backend.json |
| uv run --no-sync pytest tests/ -q -m speech | 2skipped;voz sin validar | validation-speech.log |
| pnpm.cmd --dir apps/web build / lint | exit0;1.89s/1.08s | validation-build.log/validation-lint.log |
| pnpm.cmd --dir apps/web test:e2e | 12passed(1.3m reportados);04=5.7s | validation-test-e2e-final.log |
| .\scripts\check-demo.ps1 | exit0;67.4s;3checks aprobados | validation-check-demo-final.log/check-demo-result.json |
| Black --check inventario afectado | 9archivos Python,exit0 | validation-black.log/python-files.json |
| Ruff src/tests Counter(ruta,código,mensaje),multiplicidad | 10heredados,0nuevos | ruff-validation.json;baseline001durable |
| uv lock --check --offline | exit0 | validation-lock.log |
| uv run --no-sync python -X utf8 -m oralia.validation run --output specs/009-long-extractive-binding/evidence-current --repetitions 2 --seed 42 --authorize-synthetic-ablations | 204celdas actuales | evidence-current/validation-experiment.log |
| uv run --no-sync python -X utf8 -m oralia.validation replay --package specs/009-long-extractive-binding/evidence-current | matched true,204 | validation-replay.log |

Los primeros tres comandos pytest se ejecutan con uv run --offline --no-sync.
Matriz HTTP24=3materiales×2modos×4scopes:01,04original y bloque largo sintético adicional;
[],transcript,summary,ambos. Ambos modos exigen salida no nula/no bloqueada. Autoestudio
exige100/fuentes y segundo turno utilizable. Cierre, revisión parcial, JSON/Markdown y
borrado404/409. Defensa prueba ciclo textual/control, no utilidad semántica de repreguntas.

Matriz29 de frontera:399/400/401/800×1/2/3/4fragmentos,Unicode/combining/emoji;
12negativos de texto alterado/prefijo arbitrario/texto falseado/doc/versión/ubicación/
curso/actividad/retirada/categoría/scope/procedencia; más offsets/hash exactos. Son fixtures
DB y verificador reales con propuestas sintéticas, no observación de ataques reales.
Coherencia añade5casos nuevos de metadata negada y conflicto explícito real preparado.

Navegador crea asignatura/borrador,carga04 por file input y verifica hash,activa por UI,
publica con material,abre autoestudio,responde100/fuentes,cierra,revisa,exporta ambos
formatos y elimina. Sin respuesta simulada ni activación auxiliar por API. Captura
browser-long-material.png inspeccionada visualmente. No se sustituyó04 por material breve.

## Incidencias de validación y aislamiento

Se conservaron fallos/diagnósticos iniciales. Un Playwright completo dio11passed/1failed
al no recuperar100 con índice E2E reutilizado (288entradas), aunque SQL se reiniciaba.
El harness ahora crea un índice propio por ejecución, sin borrar los anteriores ni
cambiar recuperación/umbrales de producción; los12casos completos pasan sin suavizar100.
Esto no acredita recall universal ni identifica una causa general interna de Chroma.

Dos repeticiones globales dieron920passed/1failed en una prueba preexistente de consulta
durante reconstrucción: Chroma «Nothing found on disk»; sus6casos aislados pasaban.
Se detectaron clientes persistentes de pruebas sin close. Conftest ahora registra solo
clientes bajo tmp_path resuelto propio y los cierra por API pública al terminar el caso;
no clear_system_cache ni cierre de rutas ajenas, ni skip/retry/reordenación de pruebas.
La batería de reconstrucción/docente pasa33en16.29s y el global final pasa921. No se
modificó producción para encubrir ese error ni se garantiza ausencia de carreras nativas.
Logs anteriores:validation-deterministic-concurrent.log y
validation-deterministic-repeat-before-cleanup.log. El reporte previo docente queda
archivado byte por byte en teacher-result-before.md.

## Tabla completa de tareas

| Tarea | Estado | Implementación / evidencia |
|---|---|---|
| T001 | Completada | baseline.json; prior-source.zip; preservation.json: paquetes006–008/18recursos/hash04 intactos |
| T002 | Completada | reproduction-before.log: 2fallos HTTP originales; validation-http-final.log: 24passed,16.12s |
| T003 | Completada | test_long_extractive_binding.py: 16combinaciones longitud/cantidad,12negativos,1offset/Unicode=29casos |
| T004 | Completada | extractive_excerpt.py y deterministic_adapter.py: perfil material-excerpt/v1 idéntico al snippet previo |
| T005 | Completada | composer: fuente DB vigente→proyección→snapshot/slots→T090 intacto; evento metadata autorizado |
| T006 | Completada | 12mutaciones nulas/saneadas/fallback≤1; T090/T150 globales; 24casos HTTP de scopes/cierre/exportación/borrado |
| T007 | Completada | test_teacher_long_material.spec.ts; validation-test-e2e-final.log: caso04 completo5.7s; browser-long-material.png |
| T008 | Completada | validation-backend.json/validation-frontend.json/check-demo-result.json; Black9/Ruff0nuevos;18hashes estables |
| T009 | Completada | evidence-current y validation-replay.log:204matched; preservation.json |
| T010 | Completada | materiales/docente/RESULTADO.md; este informe; modified-files.json; reporte previo archivado |
| T011 | Completada | analysis-report.md sin críticos; converge-report.md sin brechas obligatorias |
| T012 | Completada | coherence_verifier_agent.py compara oraciones;5casos nuevos positivos/negativos; sin eximir texto copiado |
| T013 | Completada | Tecnica.tsx: botón Activar incluye processed; backend ya lo permitía; flujo navegador real |
| T014 | Completada | run_self_study_api.py: índice por ejecución;12Playwright con aserción100 intacta |
| T015 | Completada | conftest.py: close() público solo a clientes de tmp_path propio;33pruebas de reconstrucción/docente y global921 pasan |

## Archivos modificados o nuevos

- `src/oralia/domain/materials/extractive_excerpt.py`
- `src/oralia/infrastructure/generation/deterministic_adapter.py`
- `src/oralia/application/orchestration/self_study_agency_composer.py`
- `src/oralia/domain/agents/coherence_verifier_agent.py`
- `tests/integration/test_teacher_material_pack.py`
- `tests/integration/test_long_extractive_binding.py`
- `tests/contract/test_coherence_verifier_agent.py`
- `tests/e2e/run_self_study_api.py`
- `tests/conftest.py`
- `apps/web/src/routes/Tecnica.tsx`
- `tests/e2e/test_teacher_long_material.spec.ts`
- `materiales/docente/RESULTADO.md`
- `.specify/feature.json`

Además: todos los artefactos009 (spec/plan/research/modelo/contrato/quickstart,2checklists,
cobertura/tareas,informes/inventarios/logs/captura,snapshot y paquete experimental).
Tres fuentes de manifiesto cambiadas:composer,coherence_verifier,deterministic_adapter;
una nueva:extractive_excerpt. Originales006/007/008 byte idénticos; manifiesto actual
verificado, sin hashes editados.18archivos estables demo/habituales iguales. No Reset
real; los harness de prueba gestionan únicamente sus workspaces temporales propios.

## Límites

Ventana400+elipsis: máximo401caracteres por proyección,3fuentes;offsets Python, sin
prometer grafemas o semántica general. Coherencia sigue heurística léxica por oración.
T090/T150 y whitelist técnica intactos: detalle interno de binding sigue minimización
por scopes; revisión/exportación no amplían lista blanca. No reconstruir contenido no
consentido/eliminado.204celdas son evidencia sintética determinista; HTTP/browser usan
embeddings e índice reales con datos ficticios. Voz real,LLM y utilidad humana sin validar.
No acredita documentos arbitrarios ni archivo03 conflictivo/archivo02 o sus extensiones.
Cierre completado:15/15tareas;analyze sin contradicciones críticas y converge sin brechas obligatorias.
