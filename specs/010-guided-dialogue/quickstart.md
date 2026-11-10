# Guía operativa 010 — estado actual

Implementación y validación técnica realizadas. No es cierre: faltan restauración
exacta de seis salidas históricas (T061) y revisión humana del sistema exigida por
plan.md para G1. G2 no aprobado; utilidad con personas y voz real pendientes.
No se hicieron commits ni Reset. La demo personal y su base no se migraron ni reiniciaron.

## Abrir el entorno guiado aislado ya preparado

Desde D:\Proyecto personal\ORALIA, con dependencias locales preparadas y Node en PATH:

```powershell
uv run --offline --no-sync python -X utf8 -m oralia.demo start --workspace ".claude-scratch/feature010-normal-shell" --api-port 8026 --web-port 5196
```

El launcher abre navegador solo tras verificar ambos servicios. Para no abrirlo,
añadir --no-browser. Si falta Node en una terminal normal, preparar su PATH de proceso
con la instalación existente antes de arrancar; no se descarga ni instala automáticamente.
No cambiar puertos si están ocupados: resolver el conflicto indicado o elegirlos explícitamente.

En http://127.0.0.1:5196, Área docente, localizar las dos actividades «Diálogo sintético»
y abrir la correspondiente de autoestudio o defensa. Sus destinatarios ficticios autorizan
synthetic-010: introducir ese código, no un nombre. No es autenticación; la sesión requiere
su autorización propietaria emitida por el backend. Las actividades iniciales 007 son distintas.

Ensayo breve: consultar un objetivo, repetir, pedir otra forma y pista, cambiar de tema
con confirmación; cerrar con elección explícita de ámbitos. Revisar/exportar solo lo
consentido, eliminar y comprobar indisponibilidad. Repetir sin conservación. No probar voz
como si estuviera validada ni presentar el compositor controlado como un LLM libre.

Parada exclusiva del entorno propio:

```powershell
uv run --offline --no-sync python -X utf8 -m oralia.demo stop --workspace ".claude-scratch/feature010-normal-shell" --api-port 8026 --web-port 5196 --no-browser
```

El entorno se entrega preparado y detenido. No usar Reset para este recorrido.
El comando habitual .\scripts\demo.ps1 conserva su comportamiento y la demo personal.

## Evidencia y revisión

- implementation-evidence.md y task-evidence.md: comandos, medidas y tabla completa.
- human-system-review.md: 24 diálogos ficticios y rúbrica, pendiente de evaluación humana.
- source-checkpoint-20261019.zip/json: código y fixtures archivados, sin bases ni secretos.
- fourth-reserved-summary.json, public-input-safety y tool-runs: resultados separados.
- paired-verified-summary.json y evidence-verified-20261019: comparación y replay.
- preservation-incident/incident.json: archivos originales exactos requeridos; no reconstruir hashes.

Las reservas se ejecutan solo con sus flags explícitos y directorios nuevos. No sobrescribir
informes ni reutilizar casos ajustados como reserva nueva. 1080 pruebas globales y 21 de
navegador pasan; las 471 omisiones globales son evaluaciones explícitas, no aprobaciones.


Actualización semántica 19-10-2026: paquete vigente [24 diálogos completos](human-system-review-current.md) y [auditoría técnica de IA](technical-dialogue-audit-current.md). El paquete anterior se conserva como histórico; T067 no está aprobado.


Revisión humana organizada en [seis bloques de cuatro diálogos](human-review-blocks/README.md). Responder por bloque con IDs aceptables o caso/paso/motivo de corrección; no se atribuye aprobación por continuar. La selección de temas junto a la conversación es una mejora de interfaz: no modifica los textos de las transcripciones API ni convierte avisos en prueba de utilidad.


Último pase de interfaz: [orientación accionable y23/23 Playwright](orientation-validation/report.md), [analyze/converge actual](analysis-convergence-orientation-current.md), [tabla completa67/74](task-evidence.md). La API y sus transcripciones no cambian. La demo aislada permanece preparada y detenida.

## Recorrido conversacional sin pantalla (actualización 20-10-2026)

El texto anterior conserva resultados históricos. La nueva capacidad requiere una actividad **nueva** con política optativa `guided_policy(recipient, screenless=True)`; no cambia las actividades ya usadas ni el entorno demo preparado. No basta con seleccionar un tema en pantalla para aceptar D01.

Demostración reproducible aislada de integración: `uv run --offline --no-sync pytest tests/integration/test_screenless_dialogue.py -q` (los ocho recorridos congelados requieren flags explícitos y carpeta nueva). Demostrador en navegador real: `pnpm.cmd --dir apps/web run test:e2e`. Los dos casos `test_screenless_conversation.spec.ts` preparan actividades ficticias optativas en el servidor E2E propio; ocultan paneles y realizan navegación/conservación/cierre/revisión/borrado exclusivamente con texto transcrito y respuestas. No requieren ni modifican el perfil personal de demo.

Guion: «hola» → «qué temas hay» → «más opciones» → «elijo condensación» → «confirmo» → «de dónde sale eso» → «ayuda» → «conservar resumen y transcripción» → «confirmo conservar resumen y transcripción» → «terminar la sesión» → «confirmo cerrar» → «revisar intervención 1» → «confirmo eliminar el contenido de esta sesión» → «revisar intervención 1». La alternativa efímera propone y confirma «no conservar nada»; al cerrar no queda registro para revisar. Usar un tema realmente ofrecido y respetar las restricciones de defensa.

Véanse [matriz actual](screenless-matrix-current.md), [24 transcripciones](human-system-review-screenless-current.md), [bloques de revisión](human-review-screenless-blocks/README.md) y [G4 de audio pendiente](G4-audio-gate.md). El endpoint conversacional no implementa STT/TTS. No se valida voz real ni utilidad humana mediante estos ensayos.

Validación vigente20-10-2026: [1166 pruebas Python y25 Playwright](screenless-validation/report.md); [tabla76/83](task-evidence.md); [analyze/converge sin cierre](analysis-convergence-screenless-current.md). Los totales anteriores de esta guía son históricos.

## Sucesor didáctico para revisión de D01

D01 fue revisado por el usuario y requiere corrección en la versión observada. Los anteriores encabezados No evaluado se refieren a aprobación pendiente de sucesores, no anulan ese rechazo. La selección sin pantalla por sí sola no corrige la didáctica.

El sucesor se prepara explícitamente con `guided_policy(recipient, screenless=True, pedagogy=True)` y materiales ficticios agua-v2/programa-v2 en actividades nuevas. Los originales v1 y el perfil personal preparado no se modifican. El helper de pruebas `prepare_api.py --mode self_study --domain agua --screenless --pedagogy` solo funciona sobre el servidor E2E propio y comprueba su identidad; no usarlo contra la demo personal.

`uv run --offline --no-sync pytest tests/integration/test_didactic_quality.py -q` comprueba propósito, variantes, literalidad, política incompleta y protección. Los corpus se activan explícitamente mediante ORALIA_DIDACTIC_RUN (carpeta nueva) y ORALIA_DIDACTIC_PARTITION (development/reserved/reserved_cycle_2). La primera reserva3/4 falló y se conserva; los casos expuestos no vuelven a ser reserva nueva. El navegador completo añade dos recorridos reales `test_didactic_dialogue.spec.ts`: D01 completo y proceso del segundo dominio sin paneles visuales. La publicación sigue siendo independiente de suficiencia didáctica y aprobación humana.

Entrega didáctica actual: [D01 completo corregido](D01-corrected-for-human-review.md), [validación1185Python/27Playwright](didactic-validation/report.md), [tabla83/90](task-evidence.md). La revisión humana previa de D01 exige corrección; la aprobación del sucesor y los otros23 está pendiente. No se cierra la feature por esos totales.

Lectura de tablas nativas: [alcance, notas excluidas y versionado explícito](../../docs/LECTURA-DE-MATERIALES.md). Pruebas relevantes: tests/unit/test_native_table_extraction.py y tests/integration/test_native_table_materials.py. Ensayo externo explícito por copias congeladas: ORALIA_TABLE_REHEARSAL=carpeta nueva y tests/integration/test_external_table_materials.py; no se activa ese corpus por defecto ni se publica el paquete en la demo.

Validación vigente de tablas: [1198Python/27Playwright y17pruebas pertinentes](table-extraction-validation/report.md), [tabla88/95](task-evidence.md), [analyze/converge](analysis-convergence-tables-current.md). El paquete externo sigue borrador; no se incorpora a la demo por estos ensayos.


## Secuencias completas tras auditoría v4/v8 —21-10-2026

La continuidad optativa v4 usa ahora la propuesta material v10 en el fixture aislado. V9 amplía relaciones y contenido; v10 solo repara el alias de suplemento PPTX. Ninguna se publica en la demo personal. El actor ficticio de pruebas publica técnicamente; no representa revisión humana de D01 ni de los materiales.

Para repetir desarrollo con una carpeta nueva desde PowerShell:

```powershell
$env:ORALIA_RELEVANCE_RUN = ".claude-scratch/sequence-review-$(Get-Date -Format yyyyMMdd-HHmmss)"
$env:ORALIA_RELEVANCE_CORPUS = "tests/dialogue/fixtures/sequence-continuity-v1.json"
$env:ORALIA_RELEVANCE_PARTITION = "development"
uv run --offline --no-sync pytest tests/integration/test_contextual_relevance.py -q
Remove-Item Env:ORALIA_RELEVANCE_RUN, Env:ORALIA_RELEVANCE_CORPUS, Env:ORALIA_RELEVANCE_PARTITION
```

La repetición de una reserva ya ejecutada es regresión expuesta. La corrida nueva de seis experiencias v6 obtuvo5/6 y se conserva; tras reparar pasa6/6 como regresión. La última v7 pasa6/6 con dos experiencias nuevas de agua/datos y cuatro controles reutilizados. No afirmar que sus seis sean nuevas ni aceptación general.

Véanse [transcriptos actuales íntegros](sequence-continuity/human-review-sequence-current.md), [primeras ejecuciones](sequence-continuity/human-review-sequence-first-runs.md), [validación](sequence-continuity/validation/report.md), [tabla de128tareas](sequence-continuity/task-evidence-complete.md) y [análisis/convergencia](sequence-continuity/analysis-convergence-current.md). T061 crítico y G1 humano siguen pendientes. No voz real ni utilidad con personas validadas.
