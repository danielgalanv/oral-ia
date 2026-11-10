# Ensayo docente de autoestudio por chat

Objetivo: observar si ORALIA ayuda a consultar y comprender el contenido de requisitos de Ingeniería del Software. No examina, puntúa, atribuye aprendizaje ni necesita rúbrica. El profesor estudia después la eficacia con sus propios métodos.

El chat sigue siendo un perfil local de prueba docente; la comprobación integrada con los modelos en GPU (T191) está pendiente. Este material prepara el ensayo, no declara habilitados participantes ni valida utilidad educativa.

## Uso

1. Preparar el corpus e interfaz en CPU y, cuando corresponda probar los modelos, arrancar con GPU disponible. [Guía de operación](../ESTUDIO.md).
2. Explicar que las respuestas pueden contener errores y que Fuentes consultadas permite revisar los originales. Utilizar un código seudónimo de sesión; no guardar audio.
3. Dejar preguntar libremente sobre la asignatura, sin cupo educativo de preguntas. Se puede comenzar por definición/tipos, pedir una explicación distinta, proponer un requisito hipotético y consultar cómo comprobarlo. No hay respuestas docentes predefinidas ni una secuencia obligatoria para el alumno.
4. Observar dudas de manejo, uso de fuentes, aclaraciones y cancelaciones. Ante un problema, registrar qué ocurrió y qué se esperaba, sin convertirlo en una valoración del alumno.
5. Finalizar con confirmación. Revisar los registros y decidir qué cambios hacen falta antes del siguiente ensayo.

## Registros preparados

- [Resumen de sesión](sesiones.csv): conteos descriptivos y temas preguntados.
- [Incidencias](incidencias.csv): reproducción y estado de una dificultad técnica o de contenido, sin notas al alumno.

Las plantillas CSV son **manuales**, no datos ya recogidos. Ahora, al pulsar Finalizar, se puede descargar explícitamente una copia JSON o Markdown con preguntas, respuestas mostradas, fuentes y conteos descriptivos calculados desde la sesión. También incluye repeticiones textuales normalizadas, sin deducir conceptos frecuentes ni resultados de aprendizaje. El profesor puede asignar conceptos posteriormente. Se excluyen audio, borradores no mostrados y razonamiento interno; el proveedor queda identificado para distinguir fixtures de modelos reales.

La descarga no añade persistencia automática en el servidor ni genera más respuestas. Puede descargarse y elegir Seguir estudiando. Al cerrar, el programa descarta su memoria; **la copia descargada permanece y debe conservarse/eliminarse según el ensayo acordado**. Si se cierra sin descargar, no queda un archivo nuevo del programa. No se ha validado aprendizaje ni revisión semántica con esta función. [Evidencia CPU](../audits/2026-11-03-cpu-completion/report.md).

Si se conserva texto de preguntas/respuestas para contraste docente, hacerlo de forma explícita para ese ensayo, junto con documento/página o URL y el código de sesión. Mantenerlo local, sin nombres personales ni audio, durante el periodo acordado para el estudio. No se activa almacenamiento nuevo mediante estas plantillas.

## Lectura de los resultados

Separar problemas de interfaz, fuentes/recuperación, explicación y servicio disponible. Espera o cancelación no equivalen a respuesta académicamente errónea. Un ejemplo ficticio coherente no se rechaza por sus cifras inventadas. Repetir una estructura tampoco demuestra por sí solo una explicación deficiente.

Preguntas, temas, consultas a fuentes y peticiones de aclaración ayudan a describir el uso; no demuestran aprendizaje o eficacia. Una petición de aclaración puede reflejar interés o una explicación insuficiente: no asignar una causa automáticamente.

Las ayudas de examen y su posible límite pertenecen al diseño del examen que indique el profesor; no se aplican a este autoestudio libre.
