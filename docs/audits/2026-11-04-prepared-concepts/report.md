# Catálogo preparado de conceptos — cierre del incremento

Iniciado 04-11 y terminado 05-11-2026. **Mecanismo de preparación implementado; no se promueve el revisor conceptual al chat estable.** Se siguió el AGENTS.md de raíz al reanudar.

## Cambios y alcance

- Catálogo persistente por documento, versión y hash, con texto literal, posiciones, título/página y cobertura temática existente. Archivos de documento inmutables y manifiesto derivado confirmado atómicamente. Actualizar un documento conserva los otros archivos y las versiones anteriores.
- Preparación automática en `study-chat.ps1 -PrepareOnly`; el recibo `oralia-study-preparation/v2` incluye el catálogo. Los recibos anteriores se rechazan y requieren preparar de nuevo. No hay migraciones SQL.
- `ConceptLedgerReviewer.review(..., prepared=...)` enlaza la evidencia recuperada exacta con el catálogo y evita la planificación LLM de ese turno. Pregunta e historial mantienen su vínculo nuevo; no se guardan respuestas prefabricadas ni se reutilizan veredictos.
- Original alterado, versión/texto diferente, retirada de fuente, manipulación del caché o revocación antes de confirmar se rechazan. La autorización vigente sigue revalidándose por el llamador y el adaptador; el caché no concede permisos.
- Los sinónimos/traducciones opcionales quedan como propuestas, no aprobación docente. Esta preparación CPU conserva nombres originales; no ha generado un glosario semántico completo.

El corpus actual tiene **9 documentos y 117 pasajes disponibles**. El extractor detecta **40 candidatos literales a definición**, no 40 definiciones validadas: al inspeccionarlos aparecen también instrucciones o escenarios. Se conserva el contexto completo y no se declara cobertura exhaustiva del curso ni se incorpora cuarentena. El catálogo aún necesita depurar esas clases antes de tratarlo como glosario aprobado.

## Comparación real

Mismos modelos locales, fuentes y candidatas; condiciones alternadas, una pasada, sin reparaciones ni nuevas respuestas. Se compara **v4 con planificación en turno frente a v4 con catálogo preparado**, no contra el chat estable v8. No intervino la guardia de términos específicos. Oráculo separado, no enviado al modelo.

| Caso | En turno: s / llamadas | Preparado: s / llamadas | Resultado |
|---|---:|---:|---|
| REG_FIXED | 43.80 / 3 | 40.44 / 2 | Ambos aceptan trazabilidad/trazado. |
| HISTORICAL_EXCERPT | 40.42 / 2 | 28.39 / 2 | En turno: incertidumbre. Preparado: detecta el encabezado erróneo Complejidad. Es un fragmento histórico, no conversación nueva. |
| REG_FICTION | 44.62 / 2 | 50.55 / 1 | Ambos aceptan las cifras ficticias coherentes. |
| LIVE_GENERATED | 150.72 / 5 | 396.19 / 9 | Ambos emiten críticas demasiado literales sobre conjunto/especificación y completo/completa; no se cuentan como detecciones correctas. |

**26 llamadas de revisión completas**, dentro del presupuesto nuevo de 36; no incluye calentamientos de los trabajadores. No se consumió reserva ni se retocaron prompts, controles o respuestas durante el ensayo. El caso largo preparado requirió tres reducciones de lote para recuperar cobertura de unidades: terminó con 9 llamadas frente a 5. Por ello no afirmo una mejora general de latencia ni promuevo esta revisión. La preparación del catálogo no resuelve por sí sola la cobertura formal ni la materialidad de las críticas.

La llamada CPU de preparación del catálogo completo midió **0,38 s**, excluidos arranque e indexación general. Cargarlo midió 8,4 ms y proyectar los cuatro subconjuntos 0,5–2,3 ms, sin modelos. Son mediciones puntuales de esa operación, no tiempos de respuesta al alumno.

## Validación y estado

- **38 pruebas dirigidas distintas aprobadas**: 37 en `cpu-final.log`, más el nuevo negativo de revocación antes del commit incluido en `cpu-race.log`; no se suman ejecuciones repetidas como pruebas nuevas.
- Preparación docente real completada, con build, índice CPU y catálogo en `.claude-scratch/study-chat-20261105-113833-e84d8be1`; recibo v2 con diez artefactos de catálogo. Ver `teacher-preparation.log`. No arrancó servidor ni modelo generativo.
- Black: seis archivos conformes; Ruff: sin hallazgos en los seis archivos afectados. No se repitieron suites generales ajenas al cambio.
- 467 archivos históricos comprobados sin cambios; originales del ensayo revalidados por llamada. No hubo commits, Reset ni cambios de datos habituales.
- Los intentos previos fallaron antes de cargar modelos por indentación del ejecutor y falta de `structlog` en el entorno GPU. Se conservaron los logs y se usó el Python del proyecto como coordinador, sin instalar dependencias; los trabajadores CUDA existentes hicieron las inferencias.
- Con autorización expresa se detuvo el llama-server residente y se pausó su supervisor T, que lo recargaba. No se reinició T. Ambos árboles de trabajadores ORALIA quedaron cerrados; no hay inferencias propias pendientes.

T224/T225 y la medición T226 completadas; T219/T223 y los gates históricos siguen pendientes. T227 registra la depuración semántica del catálogo candidato. El chat estable conserva generación v4 y revisión v8; crear el catálogo en preparación no equivale a activar el revisor experimental ni a acelerar ya ese chat.

## Evidencias para continuar

- [Métricas resumidas](summary.json), [resultados íntegros](run-001/results.json), [protocolo](run-001/protocol.json), [proyección CPU](cpu-projection.json).
- Implementación: `src/oralia/course_dialogue/prepared_concepts.py`, `src/oralia/documentary/concepts.py`, `concept_review_loop.py`, `study_preparation.py` y sus pruebas.
- Siguiente trabajo acotado: depurar qué entradas son definiciones y controlar falsas objeciones/cobertura del revisor. No iniciar otra campaña por defecto para intentar obtener mejores números.
