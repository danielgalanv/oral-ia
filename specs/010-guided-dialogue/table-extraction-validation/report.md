# Lectura de tablas nativas — validación20-10-2026

Se corrige una omisión verificable: DOCX solo recorría párrafos y PPTX solo cuadros de texto. Ahora se extraen tablas nativas en orden, con coordenadas de tabla/fila/columna y literalidad. No se modificaron los cuatro documentos originales ni se incorporaron sus propuestas al entorno habitual. Las notas de presentador siguen excluidas; solo notas no hace procesable un archivo.

| Comprobación | Resultado medido |
|---|---|
| Global Python completo |1198 aprobadas,935 omitidas,1 aviso de deprecación;297,39s |
| Playwright completo |27/27;4,1min informados por Playwright |
| Pruebas pertinentes |17/17;13,73s. Diez de extracción, tres de API/ciclo de vida y cuatro archivos externos |
| Word del programa |77párrafos previos conservados;24celdas antes omitidas,101bloques totales actuales |
| PPTX13diapositivas |24celdas nuevas de tabla nativa en diapositiva12;13→37bloques.007=fila3/columna1,1000=fila4/columna1,3,5=fila5/columna1 |
| Word del agua |74párrafos, sin tabla nativa; se conserva íntegro el texto/localización previos |
| PDF textual de datos |7páginas extraídas; código PDF sin cambios, no se reconstruyen celdas |
| Black/Ruff |134rutas Python comprobadas;10incidencias heredadas y0nuevas contra baseline durable49, con multiplicidad por ruta/código/mensaje |
| Frontend |build/lint pasan;1,34s fase Vite, no tiempo total ni mejora medida |
| Experimento |204celdas/0errores y replay coincide; protocolo/resultados estructurales iguales a006–009 y anterior010 |
| Preservación |593archivos de fuente/fixtures congelados sin cambios durante validación final;229históricos vigilados/0cambios nuevos; SHAhabituales iguales |

## Implementación y límites

DocxExtractor usa Paragraph/Table del cuerpo en orden y coordenadas de celdas. Las combinadas se emiten desde su origen; el anidado mantiene el orden hasta cuatro niveles, con error explícito y cero fragmentos si se excede. PptxExtractor recorre shapes/grupos y tablas por filas/columnas, omitiendo las celdas spanned de combinaciones. Los formatos de párrafo/diapositiva previos sin tablas permanecen. No hay dependencias, agentes, DDL o cambios de API nuevos.

El contexto de columna/primera celda de fila se etiqueta como referencia estructural, acotada a160caracteres por referencia; no se infiere que la primera fila sea cabecera semántica. El contenido principal permanece íntegro y los originales completos siguen en sus celdas. Los valores007/1000/3,5 se conservan como texto, sin conversión numérica. Las ubicaciones Word son sección/tabla/fila/columna, no una página aproximada; en el Word programa la tabla aparece antes de referencias, bajo Casos de cantidad y resultado.

Notas docentes/presentador, comentarios y otros elementos no admitidos no se incorporan automáticamente. No se añaden OCR, reconstrucción visual de tablas PDF, gráficos/SmartArt ni CSV. Orden de shapes almacenado no garantiza orden visual; el ensayo OOXML/textual no valida la presentación nativa o recortes de un previsualizador. Véase [política completa](../../../docs/LECTURA-DE-MATERIALES.md).

Processed indica extracción/indexación utilizable dentro de ese alcance, no cobertura visual completa o aprobación docente. Extraer no activa. Versiones ya indexadas no se reescriben: una nueva extracción se incorpora mediante sucesora explícita, conservando historial/retirada de la anterior. Los permisos, aislamiento y fuentes vigentes siguen siendo obligatorios.

## Ensayo real y atribución

Los cuatro entregables ficticios del paquete externo se copiaron por SHA a table-extraction-inputs/, con manifiesto table-extraction-inputs.json. Los originales se leyeron y conservan el mismo SHA que las copias ensayadas. La comparación table-extraction-comparison.json ejecuta también los extractores anteriores archivados sobre esas mismas copias: confirma24celdas omitidas en Word programa y24en PPTX. No se elimina ni convierte ninguna tabla para conseguir un pase.

Los tests usan FastAPI TestClient, SQLite y Chroma persistentes en rutas temporales propias y embeddings locales ya preparados, con modo offline en las fixtures; no sustituyen respuestas o vectores favorables. Verifican activación previa, curso/actividad, UUID/versión/ubicación/texto exactos frente al registro real, consulta tras sucesora, retirada/desactivación y conservación de fragmentos históricos. Notas-only y anidado excesivo no producen fragmentos. Las consultas de los cuatro archivos usan UUID reales y se comprueban contra su MaterialFragment; no se usa el primer fragmento como procedencia ficticia para unidades docentes.

Esos ensayos no publican las210unidades propuestas ni las guías/oráculos del docente, no ejecutan sus60casos o conversaciones del tercer dominio, y no aprueban el contenido del paquete. Incorporarlo requiere fuentes/UUID/versiones reales y validación conversacional por formato/dominio, además de revisión docente independiente. La aprobación humana de D01/otros23, G3 y voz real siguen pendientes.

## Comandos y primeras ejecuciones

Desde raíz: `uv run --offline --no-sync pytest -q`; `pnpm.cmd --dir apps/web run test:e2e`; `pnpm.cmd --dir apps/web run build`; `pnpm.cmd --dir apps/web run lint`. XML/logs finales en esta carpeta. Black usa python-files.json; Ruff compara JSON con specs/001-core-cognitive-runtime/t090-ruff-baseline.json mediante Counter(ruta,código,mensaje) con multiplicidad.

Pruebas de tablas: `uv run --offline --no-sync pytest tests/unit/test_native_table_extraction.py tests/integration/test_native_table_materials.py -q`. Para repetir los cuatro archivos, definir ORALIA_TABLE_REHEARSAL con una carpeta **nueva** y ejecutar también tests/integration/test_external_table_materials.py. Por defecto esos cuatro casos se omiten; no dejar el flag activo al ejecutar la global. Omitido no es aprobado.

La primera ejecución conserva7fallos/1pase: tablas/combinadas/anidado/grupos omitidos; notas ya estaban excluidas. Una prueba posterior asumía incorrectamente que antes de tabla era el primer bloque de Word e ignoraba su título; se corrigió el oráculo para verificar orden relativo. El primer ensayo externo asumía tabla en ambos Word:16pases/1fallo. La estructura real confirmó que el de agua no contiene tabla; se corrigió la expectativa sin alterar documentos. El ensayo final17/17 conserva todos los resultados anteriores.

Experimento: `uv run --offline --no-sync python -m oralia.validation run --output specs/010-guided-dialogue/evidence-tables-20261020 --repetitions 2 --authorize-synthetic-ablations`; `uv run --offline --no-sync python -m oralia.validation replay --package specs/010-guided-dialogue/evidence-tables-20261020`. Usar salida nueva al repetir; no editar hashes antiguos. tables-experiment-comparison.json verifica204/0errores y comparabilidad estructural, sin atribuir utilidad humana.

## Estado de entrega

Fuente congelada en source-tables-verified-20261020.json/zip. tables-modified-files.json enumera13cambios de fuente/fixtures:3archivos de extracción,4de pruebas,1guía,1manifiesto y4copias inmutables. table-extraction-preservation.json conserva SHAhabituales y evidencia histórica. Los extractores anteriores y entradas están archivados; ningún archivo histórico se reescribe.

[Tabla completa](../task-evidence.md):88/95tareas completadas. [Analyze/converge](../analysis-convergence-tables-current.md): sin contradicciones críticas de intención ni nuevas brechas de construcción en este alcance; no converged por T061/T067 y dependencias. Las seis pérdidas históricas anteriores no se restauraron ni exceptuaron. No hubo commits, Reset o modificaciones de datos habituales; procesos ajenos intactos y perfil propio de demo conservado.
