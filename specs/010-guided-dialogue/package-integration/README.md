# Integración controlada del paquete docente —20-10-2026

Se ensayan los cuatro entregables ficticios originales en cursos separados de SQLite/Chroma temporales propios. La política nueva guided-screenless/v3 es optativa para actividades nuevas. El entorno habitual y la demo preparada no reciben material, unidades o cambios de configuración. La generación de estas respuestas es controlada y determinista; la ingestión/consulta usa embeddings locales reales ya preparados. No se presenta un modelo generativo libre como validado. Esta entrega técnica no aprueba calidad docente, utilidad con personas o audio real, ni cierra Feature010.

## Materiales y atribución

Original: materiales/docente/ampliacion-didactica-20261020. receipt.json y original-manifest.json conservan sus21 archivos y el SHA del manifiesto. Se conservan overlays v1/v2/v3 separados, con manifest.json/revision.json y diff detallado en overlay-detailed-diff.json. Los originales nunca se reescriben.

Por dominio: agua85unidades técnicas, programa86, datos85;256 propuestas distintas,342instancias publicadas técnicamente por corrida de cuatro formatos (el programa se prueba dos veces, en cursos diferentes). Las 210 propuestas originales siguen pendientes de revisión humana; la publicación reviewed=True es una acción técnica de pruebas y no una revisión docente.

Word agua/programa contienen las50 unidades académicas originales de cada dominio. El PPTX no sustenta literalmente15 de 50y PDF13 de 50: se cargan ampliaciones Markdown visibles separadas y sus citas se atribuyen a esos archivos. No afirmar que todo procede del PPTX/PDF. Preguntas/pistas usan archivos de práctica separados; apoyos nuevos y repreguntas tienen fuentes participantes explícitas. Guías/oráculos/_build/notas de presentador nunca se ingieren.

Cada vínculo compara texto completo normalizado solo en NFC/espacios con fragmentos reales y persiste UUID/documento/versión/ubicación/testigo en bindings. No usa primer fragmento por defecto ni los UUID de validadores del autor. Los tests adicionales comprueban curso ajeno vacío, versión sucesora, retirada y rechazo de repetir una salida cuya fuente se retiró. Las pruebas previas de tablas conservan007/1000/3,5y celdas nativas; no se convierten en imágenes para ingerirlas.

## Conversaciones y primera ejecución

- Desarrollo:8/8recorridos completos,52,81 s.
- Reserva nueva:8/8 en primera ejecución,52,38 s; congelada antes de ajustes en dialogue-freeze.json. Fuente previa en ../source-package-before-reserve-20261020.json/zip. Tras ejecutarla solo hubo formato/importaciones de producción y pruebas nuevas: post-reserve-diff.json demuestra equivalencia AST de producción excluyendo orden de imports; no hubo ajuste lógico sobre reserva.
- Total:16 conversaciones/348 intervenciones íntegras, cuatro formatos × dos modos × dos elecciones de conservación.
-60 estímulos originales expuestos:80 instancias/80aprobadas por selección/fuentes/verificadores,52,98 s. No son reserva ni80conversaciones completas.
-32pruebas pertinentes de núcleo, política nueva/no revelación y publicación/ciclo de vida:32/32,29,35 s.

Los recorridos incluyen saludo/orientación, qué/por qué/cómo, tres apoyos distintos contextualizados, fuente verbalizable, repetición, posibilidad/condiciones, cambio confirmado de objetivo, pregunta de defensa conservada, petición fuera de fuente y controles de conservación/cierre/revisión/borrado con estado real. Defensa solo emite pregunta/pista autorizadas y verificación independiente. Una pista mal etiquetada que contiene solución sigue bloqueada en v3: no aparece en salida, fuentes, propuestas públicas o revisión docente.

Primeros fallos conservados: development-v2-red, development-v3-all-first (6/8), stimuli-v3-first (69/80), stimuli-v3-second (59/80), stimuli-v3-third (79/80), además de los logs de núcleo. Las causas incluyen elipsis numérica de una metáfora, coordinación nominal, ámbito de negación/modal, listas frente a propiedad escalar y reconocimiento del propósito frente al título del tema. La alternativa original no se elimina: v3aporta un apoyo con cláusulas completas. Los primeros fallos no se renombran ni se ocultan como reserva favorable.

La planificación y coherencia siguen siendo analizadores finitos. Los controles independientes detectan oposiciones reales, propiedades numéricas incompatibles, condiciones ausentes y repetición, sin excepción por copiar el candidato a las fuentes. No garantizan comprensión semántica general o precisión científica completa. Grounding aprobado y coincidencia de unidad no acreditan por sí solos pertinencia o suficiencia: se necesita revisión humana.

## Revisión humana

[Paquete de24 bloques](human-review-current.md): cuatro bloques con16 conversaciones íntegras y veinte con80estímulos. Incluye entradas, salidas sin recorte, fuentes y estado por intervención, más JSON completo para cada comprobación. La revisión humana anterior D01 sigue siendo negativa sobre su versión; los sucesores y otros 23casos siguen pendientes. independent-arithmetic.json verifica por cálculo separado las series ficticias A/B, media6, medianas3/6, rangos16/3y divisor5frente a6intentos con1ausente; no demuestra causalidad.

PowerPoint nativo: native-powerpoint/ conserva13 PNG exportadas en lectura por COM y contact sheet. Se observaron las13 miniaturas y alta resolución de diapositivas5/12, incluyendo tabla nativa. No se guardó la fuente y solo se cerró la instancia/documento propios; SHA fuente intacto. Esto no equivale a aprobación docente o examen exhaustivo de diseño.

## Reproducción

Desde raíz con dependencias/embeddings locales preparados. Cada salida debe ser una carpeta nueva para preservar primeras ejecuciones.

```powershell
$env:ORALIA_PACKAGE_BINDING = 'ruta-nueva-bindings'
uv run --offline --no-sync pytest tests/integration/test_teacher_package_binding.py -q
Remove-Item Env:ORALIA_PACKAGE_BINDING
$env:ORALIA_PACKAGE_STIMULI = 'ruta-nueva-estimulos'
uv run --offline --no-sync pytest tests/integration/test_teacher_package_stimuli.py -q
Remove-Item Env:ORALIA_PACKAGE_STIMULI
$env:ORALIA_PACKAGE_RUN = 'ruta-nueva-conversaciones'
$env:ORALIA_PACKAGE_PARTITION = 'development'
$env:ORALIA_PACKAGE_POLICY = '3'
uv run --offline --no-sync pytest tests/integration/test_teacher_package_dialogues.py -q
Remove-Item Env:ORALIA_PACKAGE_RUN, Env:ORALIA_PACKAGE_PARTITION, Env:ORALIA_PACKAGE_POLICY
```

La reserva usada ya queda expuesta: repetir reserved_first mide regresión, nunca una reserva independiente nueva. El loader rechaza clientes remotos/no propios, falta de publicación técnica explícita y BD fuera del temporal propio con nombre test_. No introducir credenciales en comandos/archivos; el cliente de pruebas conserva autenticación existente y no exporta grants a las evidencias.

Regresión: uv run --offline --no-sync pytest -q; pnpm.cmd --dir apps/web run test:e2e; pnpm.cmd --dir apps/web run build; pnpm.cmd --dir apps/web run lint. Black usa python-files.json; Ruff compara Counter(ruta,código,mensaje) con multiplicidad contra baseline durable de001.

Experimento: uv run --offline --no-sync python -m oralia.validation run --output SALIDA-NUEVA --repetitions 2 --authorize-synthetic-ablations; replay con --package SALIDA-NUEVA. evidence-package-20261020 conserva204 celdas,0 errores y replaycoincidente; experiment-comparison.json verifica protocolo/resultados estructurales de006–009y el paquete anterior de010. Este experimento de arquitectura no es evaluación de utilidad didáctica humana.

[Resultados finales, tareas y preservación](validation/report.md). [Archivos de fuente cubiertos](modified-files.json). [Tabla completa de tareas](task-evidence-complete.md).
