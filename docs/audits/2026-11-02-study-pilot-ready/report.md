# Autoestudio libre, fuentes y preparación reutilizable — CPU

Se completan T201–T204: eliminación del cupo educativo del chat, autores y referencias legibles, reutilización verificada de preparación y materiales manuales del piloto. No se ejecutaron generadores/revisores en CPU ni GPU. La preparación y una consulta de prueba sí utilizan el encoder local de embeddings en CPU.

## Preguntas sin cupo educativo

El proveedor revisado normal no limita el número de preguntas ni las llamadas acumuladas del revisor. Los presupuestos aceptan máximo ausente y API/cliente lo interpretan como ausencia de cupo. No se oculta un corte de backend detrás de la interfaz.

El flujo `/estudio` y el proveedor revisado por defecto usan este modo. `-ExperimentalLimits`/`--experimental-limits` activan explícitamente los cupos del ensayo revisado (12 preguntas/84 llamadas). Los diagnósticos históricos no revisados conservan sus presupuestos anteriores. Un test de ensayo declara ahora ese modo expresamente; no se cambian sus resultados archivados.

Se mantienen los límites técnicos: plazo global del proceso (30 minutos en el lanzador actual), plazos por petición, tamaño del contexto/salida, rondas máximas de corrección y disponibilidad de recursos. No son cuotas educativas ni límites de ayudas del examen. No se promete servicio indefinido ni conversación académicamente validada.

La prueba HTTP confirma quince preguntas y continuidad al reentrar; otra prueba inicia después de los antiguos umbrales de 12 preguntas/84 llamadas internas y termina una respuesta revisada simulada (13/86). Los presupuestos sin cupo siguen rechazando tiempo agotado. Los ensayos finitos mantienen su comportamiento.

## Mensajes y referencias

La conversación identifica **Tú** y **ORALIA**. Fuentes consultadas agrupa por URL de documento, conserva páginas y elimina enlaces idénticos. Dos documentos con el mismo nombre y URL distinta no se fusionan. Los enlaces conservan nombre accesible con documento y página; el texto académico y los brutos no se reescriben.

[Resultado final del navegador](browser-1793652769816/result.json): quince respuestas simuladas confirmadas y Enviar aún habilitado; páginas 4/5 agrupadas en un documento y visibles en el área de lectura. Sin errores JavaScript ni peticiones externas. [Captura móvil](browser-1793652769816/mobile-sources.png) · [Escritorio](browser-1793652769816/desktop.png). Los puertos de generación/revisión son fixtures explícitas, no modelos.

## Preparación reutilizable

```powershell
.\scripts\study-chat.ps1 -PrepareOnly -NoBrowser
# Copiar la carpeta que imprime el comando anterior:
.\scripts\study-chat.ps1 -PrepareOnly -NoBrowser -PreparedRun '<carpeta-preparada>'
# Cuando se vaya a realizar la prueba GPU autorizada:
.\scripts\study-chat.ps1 -PreparedRun '<carpeta-preparada>'
```

`study_preparation.py` crea un recibo exclusivo y valida código, fuentes autorizadas, recursos locales/versiones del encoder y hashes de interfaz/índice. La validación no carga pesos. Cambios de entradas, artefactos eliminados/modificados/añadidos, recibos ajenos o rutas no propias se rechazan; no se reconstruye ni repara silenciosamente una preparación obsoleta. Los directorios antiguos sin recibo requieren prepararse de nuevo una vez.

La primera comprobación real detectó que Chroma modifica sus archivos al consultar: [registro del índice original](prepared-query.json). Por eso cada arranque materializa una **copia de trabajo nueva y verificada** dentro de `launches`, separada de la plantilla y sin recalcular embeddings. La consulta real sobre esa copia dejó intacta la plantilla: [consulta](working-query.json) y [validación posterior al cierre del proceso](reuse-after-query.json). La consulta es una comprobación operativa; no se presenta como evaluación de la pertinencia o del contenido del tutor.

Un primer montaje manual pasó una ruta relativa al helper interno que requiere raíz validada absoluta; se corrigió el montaje antes de consultar. No se reinterpretó el rechazo como fallo del recuperador.

Las pruebas de copia rechazan destino ajeno y sobrescritura, y muestran que escrituras en la copia no invalidan la preparación. El lanzador usa ruta nueva para runtime e índice de trabajo. La conexión al arranque GPU queda cableada, pero no se ejecutó una carga GPU para validarla.

## Piloto docente

[Guía y plantillas](../../piloto/README.md): resumen de sesión e incidencias con códigos seudónimos, conteos y temas. Son registros **manuales**, sin datos inventados, estadísticas automáticas, calificación ni rúbrica. No se añade persistencia de conversaciones o telemetría al backend. No se guarda audio. El profesor realiza la evaluación de aprendizaje por sus propios métodos.

## Validación y trazabilidad

- [Regresión amplia](regression.log): **715 pruebas aprobadas**, una omitida optativa y una advertencia existente Starlette/httpx. Alcance de diálogo, proveedor, API, presupuestos y preparación; no toda la suite del proyecto.
- [Dirigidas finales](copy-tests.log): **29 aprobadas** tras separar la copia de trabajo y dejar sin cupo el proveedor revisado por defecto. Son ámbitos superpuestos con la regresión amplia; no se suman como casos únicos.
- [Preparación/reutilización real final](final-preparation-tests.log): **6 aprobadas**, incluidas dependencias, errores con entorno ausente/vacío/definido y preparación/reutilización sin reconstrucción ni carga de modelos generativos. El montaje solo CPU no abre servidor ni carpeta de runtime.
- [Interfaz](ui-final.log): **18 aprobadas**; TypeScript, ESLint, Vite, Black y Ruff focal conformes. Ruff global conserva diez diagnósticos existentes y cero nuevos frente al baseline, con multiplicidad.

Los ensayos CPU no acreditan calidad académica, eficacia con estudiantes o validación GPU. T191 y los gates sustantivos siguen pendientes. El guion histórico de doce preguntas sigue siendo un banco experimental aprobado, no un límite del alumno; no se reescriben sus evidencias.

El [manifiesto](release-manifest.json) conserva fuentes y pruebas finales en `release-source`. Las [comprobaciones finales](final-checks.json) verifican los tres grupos históricos de 308/140/22 archivos (sin sumarlos como únicos), servicios propios detenidos y puerto 8057 libre. Sin Reset, commits, cambios de corpus o procesos ajenos detenidos.
