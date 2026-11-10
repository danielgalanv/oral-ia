# Pruebas integradas con GPU — 3 de noviembre de 2026

**Las pruebas terminaron; el autoestudio autónomo no queda validado.** Se corrigieron incompatibilidades de bibliografía y de tarea del control. El perfil experimental posterior no mejoró el recorrido completo y no se promueve. Persisten bloqueos de formato, una confusión de respondibilidad, un error lógico aceptado por el revisor y un recorrido web que excede el presupuesto.

## Qué se ejecutó

- Navegador Chromium real sobre `/estudio`, RAG e índice de trabajo reales, generador **Qwen2.5-14B NF4** y revisor **Qwen3-8B con razonamiento**. No hubo generadores simulados en estas conversaciones ni inferencias generativas en CPU.
- Tres recorridos de **las mismas doce preguntas aprobadas**, en tres conversaciones de cuatro turnos. Son regresiones sobre un banco expuesto, no 36 preguntas nuevas ni una reserva inédita.
- Política web de laboratorio v2, aviso previo, adquisición autorizada y contraste contra material docente. Presupuestos por etapa sin ampliar: generación 1.536 tokens, revisión 8.192, reparación 2.048; 180 s/etapa y 600 s/turno. Reloj propio de campaña 2.700 s; el lanzador normal conserva 1.800 s.
- Cancelación durante lectura del generador, recarga de ambos modelos y nueva respuesta confirmada; exportaciones JSON/Markdown y cierre. No se reenviaron preguntas automáticamente.

## Resultados observados

| Recorrido | Preguntas enviadas | Respuestas generadas y mostradas | Aclaraciones del host | Sin respuesta mostrada |
|---|---:|---:|---:|---:|
| run-001, configuración inicial | 12 | 4 | 2 | 6 |
| run-002, bibliografía/tarea corregidas | 12 | 10 | 0 | 2 |
| run-003, perfiles optativos v2/v8 | 12 | 7 | 2 | 3 |

Una respuesta mostrada no equivale a respuesta correcta ni a aceptación docente. Las aclaraciones del host tampoco se cuentan como respuestas del modelo. Al fallar B1 en la tercera ejecución, los seguimientos B2/B4 quedaron sin un referente consolidado y recibieron aclaraciones. No son pruebas independientes del conocimiento académico del modelo.

**Para leer las respuestas:** [segunda ejecución, la más completa](transcript-run002-mobile.html) · [tercera ejecución experimental](transcript-mobile.html). Los textos se conservan literalmente; las observaciones de la auditoría están separadas. [Métricas por caso](metrics.json).

## Correcciones y límites

1. **Referencias:** A2/A4/B1 de run-001 se bloqueaban por referencias documento/página en objetos, pese a tener decisión `sufficient`. Se admiten representaciones JSON informativas sin usarlas como permiso, destino de red o prueba semántica. Los tres turnos se mostraron en run-002. [Replay CPU del parser](bibliography-replay.json), identificado como análisis posterior, no nueva inferencia.
2. **Tarea explícita:** se separó en la instrucción del host el vocabulario del control solicitado. No se convirtieron las etiquetas equivocadas del modelo en decisiones válidas.
3. **Sintaxis:** se añadió un único intento adicional para errores JSON, con las mismas fuentes y un recordatorio, sin etiqueta esperada. Incertidumbre, esquema incorrecto, tarea equivocada, truncación y retirada no reciben reintentos para buscar aceptación. En run-003 B1 ambos intentos tuvieron una llave sobrante, aunque ambos clasificaban correctamente el valor ficticio de 0,3 s. La recuperación de formato no ha demostrado resolver ese caso.
4. **Respondibilidad:** C2 pide decidir si la trazabilidad demuestra cumplimiento. El control reconoce que no lo demuestra por sí sola, pero solicita evidencia para confirmar que sí lo hace. El perfil de síntesis optativo no resolvió esta confusión.
5. **Lógica:** C4 vuelve a presentar cifrado y ausencia de autenticación como requisitos incompatibles. El revisor v8 lo acepta. Se verificó que recibió el perfil y las instrucciones nuevas, con hash coincidente y razonamiento activo: [recibo efectivo](c4-effective-review-check.json). No es un fallo explicado por falta de cableado. [Hallazgo y contraste técnico independiente](findings.md).

Los perfiles `web-control/v2` y `web-review/v8` permanecen **optativos de laboratorio**, activados únicamente en el arnés de run-003. El proveedor normal conserva v1/v7. No se promueve el perfil nuevo por dos controles simples: sus etiquetas coincidieron 2/2 con el oráculo separado, pero no transfirió esa capacidad a C4. La recuperación sintáctica y el rechazo de suficiencia con evidencia local vacía son controles operativos, no una acreditación semántica.

## Internet: recorrido real, positivo aún sin completar

El intento T-web-empty de run-002 **no activó el fallo**: el arnés recibió 405 y no lo comprobó. Fue una consulta local y no cuenta como prueba web. Se conserva y se corrige el arnés, sin cambiar la protección del servicio.

En run-003 sí se retiraron los cinco pasajes locales, con activación HTTP comprobada e [inyección registrada](run-003/retrieval-fault.ndjson). No se inyectaron veredictos. El modelo pidió Internet, se adquirió contenido y el control de respaldo devolvió `supported`. Completó **4 de los 7 lotes** de comparación de las **89 páginas docentes disponibles** con `compatible`. Las latencias de esos cuatro contrastes fueron 136,625; 36,827; 156,108 y 152,016 s. Se agotaron los 600 s antes de generar la explicación. No se mostró contenido parcial. Los lotes no completados no se cuentan como contradicciones ni fallos de conocimiento. [Dimensionamiento](teacher-batches.json) · [intento conservado](run-003/browser/case-T-web-empty.json).

Por tanto, esta campaña acredita adquisición, controles ejecutados y parada segura, **no una explicación web autónoma útil entregada de principio a fin**. No se amplió el plazo para hacer pasar el ensayo.

## Verificación y preservación

[Cambios revisables](changes.patch) · [Inventario de archivos](changed-files.json). Producción: `web_control_request.py`, `web_review_frame.py`, `web_review_rounds.py`, `web_review_prompts.py`, `study_web_flow.py` y `reviewed_study.py`. Se añadieron tres archivos de pruebas y se actualizaron plan/tareas y la guía de estudio. Los servidores, control de T y navegadores del dossier son arneses de auditoría, no rutas añadidas al producto.

- **672 pruebas CPU aprobadas**, incluidas regresiones de contratos, rutas web, composición y fronteras del runtime; las 70 pruebas dirigidas se solapan con esa suite. Se conservaron los negativos previos: bibliografía 3 fallos/2 aciertos antes de corregir; recuperación sintáctica 2 fallos/4 aciertos antes de implementar.
- Black conforme en los nueve archivos Python modificados/añadidos; Ruff mantiene **10 hallazgos previos y 0 nuevos**, comparando multiplicidad por archivo/código/mensaje. [Comparación](ruff-comparison.json).
- Sin errores JavaScript registrados por los navegadores. Los textos confirmados se cotejaron con el DOM. Exportaciones y cierres se conservaron por conversación. Esto no prueba preguntas arbitrarias ni calidad general.
- **265 archivos de producción** coinciden con el manifiesto de inicio de run-003. [Comprobación](source-stability.json). Los tres manifiestos históricos comprobados mantienen 308/140/22 archivos sin cambios nuevos ni pérdidas; son conjuntos con posible solapamiento, no una restauración de pérdidas antiguas. [Preservación](preservation-check.json).
- Los picos GPU fueron 31.849, 32.009 y 31.831 MiB de 32.607 MiB. En run-002 una generación tardó 170,562 s. No se atribuye el retardo a una causa no medida ni se evalúa el contenido por el tiempo.
- T se pausó reversiblemente, con autorización expresa, para las dos últimas campañas. ComfyUI no se detuvo. Al terminar, no queda listener en 8071 ni worker GPU propio; T se reanudó inicialmente y volvió a cargar Dolphin. Tras la nueva indicación del usuario se dejó **T pausado de nuevo, sin reanudación automática**, y se descargó únicamente su modelo. El cierre de ORALIA había registrado 1.757 MiB antes de restaurar T. [Cierre](cleanup.json).

Los recibos iniciales y todos los intentos se conservan. La recarga de run-001 acredita recuperación operativa, no una comparación semántica homogénea de código: el host conservaba su parser cargado mientras el worker recargado podía importar la corrección bibliográfica ya escrita. Los frames y configuraciones están preservados. Run-002 y run-003 tienen sus propios manifiestos y copias ejecutadas.

## Siguiente bloque

Primero simplificar y restringir la salida del control, y corregir que evalúe poder responder, no poder confirmar la pregunta. Después medir la revisión de ejemplos con casos que no sean solo C4 y revisar el coste del contraste documental completo. No añadir más rondas al mismo fallo sin resolver estas causas. [Hallazgos y acciones](findings.md).

Se registra T191 como prueba técnica ejecutada, sin convertir su ejecución en aceptación del tutor. T116/T117/T152/T157, G2, SC001, revisión docente y demás pendientes semánticos no se dan por aprobados. Sin Reset, commits, migraciones ni apertura de publicación o participantes.
