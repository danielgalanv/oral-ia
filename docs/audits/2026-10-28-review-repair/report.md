# Primer ensayo: autocrítica del14B, no la revisión del asistente

28-10-2026. Se implementó y ejecutó candidata→revisión→una reparación→revisión posterior sobre el puerto existente. **El revisor elegido fue otra llamada al mismo Qwen14B**, no el juicio del asistente que había identificado los errores. Esa sustitución no probaba directamente la propuesta del usuario; tras su corrección se preparó [un control separado con críticas explícitas del asistente](../2026-10-28-agent-assisted-repair/). No se oculta este primer resultado negativo.

[Transcripción literal completa](transcript-full.md) · [Contexto completo](context-full.md) · [Métricas](metrics.json) · [Protocolo ejecutado](protocol-v3.json) · [Recibos originales por etapa](capture-001-a57c94/).

## Resultado observado

8casos:4reproducciones expuestas de E1 y4preguntas nuevas de transferencia cercana, **no reserva ni evaluación ciega**.14llamadas LLM y1calentamiento; todas las llamadas terminaron stop. Una reparación real, en N2;7textos quedaron idénticos. No se corrigieron los dos errores prioritarios conocidos A3/B1. Tampoco se corrigió el desliz de sistema/diseño en A4.

| Caso | Qué hizo el revisor | Resultado de la comparación técnica |
|---|---|---|
| E-A3 |No encontró objeciones.|Pasó por alto la inversión del significado de no funcional. Error intacto.|
| E-B1 |Propuso3omisiones de cobertura, sin identificar validez/estructura.|Informe rechazado por cita no literal. Algunas omisiones propuestas son secundarias, otra ya estaba cubierta; error prioritario intacto.|
| E-A4 |Pidió añadir dominio, diseño y proceso al ejemplo.|Informe rechazado por cita>240caracteres; otros anclajes tampoco conservan las viñetas. No distingue adecuadamente lo necesario para «esas clasificaciones» de todo tema presente en contexto. No objetó las cifras hipotéticas, pero no corrigió qué/cómo.|
| E-B4 |No encontró objeciones.|Conservó correctamente la abstención ante contraseña ausente.|
| N1 |Objetó un ejemplo que sí estaba presente, la conclusión principal y falta de citas directas.|Informe rechazado por overclaim sin testigo; además el informe altera una cita de la candidata. La respuesta inicial resolvía el cruce usuario/funcional-no funcional y el ejemplo. Sin reparación ni mejora.|
| N2 |Pidió información contractual secundaria y una explicación que ya figuraba.|Informe estructuralmente válido, pero las objeciones no justifican corregir la respuesta. La reparación añade632caracteres (23,5 %), redundancia y detalle secundario sin mejorar precisión. El post-revisor dijo «sin objeciones».|
| N3 |No encontró objeciones.|Respuesta inicial con núcleo de origen/vínculos/impactos correcto; mantiene matiz de atribución del marco NASA. Sin cambio.|
| N4 |No encontró objeciones.|Orden análisis→aprobación→implementación correcto, con matiz de ámbito CCB/NASA. Sin cambio.|

Balance exploratorio:0mejoras claras/8;7textos idénticos y1cambio sin ganancia de exactitud, con peor concisión. **No es una estimación general de calidad.** Las valoraciones iniciales N1–N4 se guardaron tras leer solo baseline/fuentes y antes de leer las críticas/finales correspondientes en `baseline-adjudication-N*-before-final.json`. Son juicios técnicos del asistente, no aceptación docente.

## Coste y límites

Presupuesto máximo28llamadas+1warmup,768tokens/50s por llamada,20min globales. Consumido14+1;3980tokens nuevos. Duración global298,921s. Las4preguntas nuevas sumaron99,717s de generación inicial frente a210,559s del flujo completo: **2,11veces el tiempo**, sin mejora observada en esos casos. No se compara tiempo de revisión humana ni se afirma benchmark universal.

De las8revisiones iniciales:4`no_issues_found`,3inválidas para el contrato,1`issues_found` válido. Solo este último disparó reparación y post-revisión. La validación determinista comprueba esquema/IDs/citas y no demuestra semántica. En B1 un testigo omitía la viñeta entre encabezado y pregunta: fallo de anclaje, no prueba de falsedad del contenido. En A4 se excedió el tamaño permitido de una cita; en N1 faltaba evidencia de un overclaim y había críticas infundadas. No se agrupan estos rechazos con un acierto semántico ni se arreglan retrospectivamente para hacer pasar el ensayo.

## Implementación y verificación

`src/oralia/course_dialogue/review_repair.py`: puerto compuesto optativo, revisión estructurada con procedencia comprobable, máximo una reparación y post-revisión sin la crítica anterior, presupuesto por llamada, recibos y limpieza. El revisor sigue siendo falible y `independent_semantics=false`; no emite supported.

`DiagnosticStudy` integra el puerto mediante copia por sesión, guarda inicial/crítica/reparación/final separados, confirma solo lo realmente mostrado para historial y conserva invalidación por permiso/fuente/cierre/cancelación. Presupuesto50s por llamada; solo este flujo optativo dispone de hasta200s por pregunta. Default50s y rutas anteriores intactos. Se corrigió antes de inferir una carrera de timeout temprano de Windows usando `timeout.expired()` además del reloj; `tests-first.log` conserva la reproducción.

UI Materiales informa de la ronda y200s totales y expone trazas como texto inerte, sin que «sin objeciones» sea aprobación. [Comprobación con fixture CPU](ui-fixture.png), [estado](ui-fixture.txt); el fixture no es evidencia de contenido ni de mejora. Servidor propio8028 detenido.108pruebas CPU finales correctas (`tests-final.log`), TypeScript/Vite/ESLint/Ruff/Black correctos en este bloque. Se probaron citas/claims falsos, límites, cancelación absorbida por proveedor, retiro de fuente, retención, aislamiento entre sesiones y que solo el final mostrado entra en historia.

Protocolos v1/v2/v3 preservados: v2 añade selección explícita de protocolo/formato del runner; v3 añade aislamiento de trazas/permiso por sesión antes de cualquier llamada. **Prompts, casos, criterios y presupuesto no cambiaron tras observar resultados.** Snapshot exacto del código ejecutado en `implementation-v3/`, porque el control posterior añade una entrada de crítica aportada sin sustituir este resultado.

La GPU pasó de libre a19,5GB ocupados durante la preparación CPU; no se cargó sobre ella ni se detuvieron procesos ajenos. Tras medición nueva libre se ejecutó:580MiB/0 % antes, pico21423MiB,580MiB/0 % después. Worker70932 y descendientes22968/88560 detenidos, salida0; `worker-cleanup.json` y muestras en carpeta de captura. Sin descargas, nuevo modelo, cambios de corpus/índice, reserva, commits/Reset o publicación participante.

## Decisión

Este candidato de autocrítica no se promueve como verificador de respuestas. El resultado muestra una limitación del revisor elegido y del anclaje, no que el esquema revisión→corrección sea inútil. La rectificación del usuario exige probar otra cosa: que las objeciones concretas ya detectadas por el asistente entren al corrector y que el asistente revise el resultado. Eso se documenta **separadamente**, como revisión asistida por agente y no como un verificador autónomo local validado.
