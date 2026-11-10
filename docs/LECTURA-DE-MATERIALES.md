# Lectura local de materiales y tablas nativas

DOCX: se extraen párrafos y tablas del cuerpo en orden de almacenamiento. Las tablas conservan fila/columna/celda; las celdas combinadas se emiten una vez desde su coordenada de origen. Se conservan tablas anidadas hasta cuatro niveles; una estructura más profunda produce error antes de indexar, sin processed parcial. Los párrafos anteriores mantienen sus referencias habituales. No se reconstruye paginación de Word: citar tabla/fila/columna/sección, no una página aproximada.

PPTX: se extraen cuadros de texto y tablas nativas, incluidos grupos, en orden de shapes almacenado y celdas por filas/columnas. Se conservan número de diapositiva y tabla/fila/columna; celdas combinadas desde origen. El orden de almacenamiento no garantiza el orden visual de lectura. Sin tablas, el texto y referencia de diapositiva mantienen el formato anterior.

Los valores se conservan como texto: `007`, `1000` y `3,5` no se convierten a números. Cada celda puede incorporar una referencia estructural a la primera fila y a la celda inicial de su fila, acotada a160caracteres por referencia. La primera fila puede contener datos: esa referencia no la declara cabecera semántica. El contenido principal de cada celda permanece íntegro; las referencias completas también están en las celdas de origen. Los rangos completos de combinaciones no se reconstruyen: la localización indica el origen.

## Notas y exclusiones

Las notas del presentador no se leen ni se incorporan al índice. Un PPTX con solo notas no es procesable. Las notas docentes o soluciones deben permanecer fuera de las fuentes del participante; si contienen material esencial autorizado, el docente debe trasladarlo al cuerpo, revisarlo y publicar una versión sucesora explícita. No se activa material por extraerlo.

No se incorporan automáticamente comentarios/notas al pie/encabezados/pies de Word, texto de imágenes, OCR, gráficos/SmartArt u objetos vinculados. Los documentos se procesan según su contenido almacenado; ocultar una diapositiva o escribir una solución en el cuerpo no sustituye la revisión de qué se autoriza. PDF textual mantiene citas por página; esta corrección no reconstruye celdas de tablas PDF. CSV sigue siendo complemento, no formato de carga admitido.

Processed indica que se obtuvo texto utilizable y se indexó, no garantiza cobertura visual completa, calidad docente ni ausencia de soluciones. El docente revisa la extracción y activa manualmente el documento; autorización de salida, fuentes vigentes y no revelación siguen siendo independientes. La revisión nativa de un PPTX no se deduce del texto OOXML o de una previsualización.

## Versiones y documentos ya existentes

No se reprocesan ni modifican documentos/fragmentos de la base habitual. Para incorporar una extracción corregida de un documento previo, cargar una sucesora mediante el flujo de versiones (`POST /api/v1/materials/documents/{id}/versions`) y activarla tras revisar; la versión anterior queda retirada con su historial intacto. La consulta conserva UUID/versión/ubicación reales y filtra curso/actividad/estado. Desactivar o retirar vuelve a excluir el documento, sin Reset.

La validación de010 usa archivos ficticios en bases/índices temporales, incluidas copias con SHA de los cuatro entregables del paquete docente separado. No publica sus210propuestas ni las guías/oráculos del profesor y no ejecuta sus60casos o diálogos del tercer dominio. Hace falta esa validación adicional y revisión de fuentes antes de cualquier incorporación docente. Audio real, utilidad con personas y aprobación humana no se demuestran mediante extracción.
