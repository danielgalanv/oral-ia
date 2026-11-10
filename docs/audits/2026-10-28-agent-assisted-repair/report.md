# Control con la revisión que había identificado los errores

28-10-2026. **La objeción del usuario era acertada:** el primer ensayo sustituyó la revisión del asistente por autocrítica del mismo14B. Eso no comprobaba directamente su propuesta. Aquí se dieron al corrector las objeciones concretas del asistente, ancladas a las fuentes originales, y el asistente revisó después cada respuesta corregida real.

Resultado sobre4respuestas expuestas: **2defectos objetivo corregidos y2mejoras parciales**, conservando problemas residuales. No se observan errores graves nuevos en esta muestra, pero no se certifica ausencia de errores. Esto demuestra que el corrector local puede aprovechar una crítica adecuada; **no demuestra un verificador autónomo equivalente al asistente**.

[Antes/después íntegros](transcript-full.md) · [Lectura móvil](transcript-mobile.html) · [Contextos íntegros](context-full.md) · [Mi revisión posterior](agent-post-review-v1.json) · [Críticas congeladas antes de corregir](supplied-critiques-v1.json) · [Protocolo](protocol-v1.json) · [Métricas](metrics.json).

## Qué mejoró y qué sigue mal

| Caso | Antes | Después real del14B | Revisión posterior |
|---|---|---|---|
| A3 |No funcionales «Impiden que el sistema cumpla ciertas características».|«Establecen propiedades o límites que el sistema debe cumplir».|Objetivo corregido; mantiene los dos ejes y el ejemplo. No se toma como validación exhaustiva.|
| A4 |Requisitos de sistema detallan «cómo se implementará».|«Definen lo que debe implementarse».|Objetivo corregido; conserva2s/1000consultas como ficción admisible. El ejemplo de sistema aún simplifica mucho el nivel de detalle.|
| B1 |Equipara válidos con estructura/contenido.|Cambia ese punto a «Correcta» y añade consistencia con necesidades de interesados.|Mejora parcial: deja de usar esa equivalencia, pero su definición inicial sigue reducida a calidad y conserva «aseguran… que no contengan errores». No se acepta como libre de defectos.|
| B2 |«Trasladables» y cierre «esta revisión asegura…».|«Trazables» y «esta revisión contribuye a asegurar…».|Mejora parcial: corrige el término y suaviza el cierre, pero conserva fusión inicial de validez/estructura y una afirmación demasiado fuerte sobre verificabilidad y satisfacción de necesidades.|

No basta contar cambios de palabras: por eso B1/B2 se califican parciales, aunque las frases señaladas cambien. No se da por corregido lo que la revisión posterior todavía detecta. No se sustituyeron los resultados reales por respuestas reescritas manualmente.

## Cómo se hizo

Mismos candidatos y contexto de E1, con hashes de recibos anteriores. No se eligieron páginas nuevas a mano ni se regeneró la candidata inicial para obtener un resultado más fácil. El control es una **reproducción expuesta con crítica asistida**, no RAG nuevo ni reserva/evaluación ciega.

El asistente redactó antes de generar una lista estructurada de defectos y citas, sin proporcionar una respuesta académica completa prefabricada. El host comprobó que las afirmaciones citadas estuvieran en la candidata y los testigos en el contexto recibido. `repair_with_supplied_review` reutiliza la **misma instrucción general de reparación** del primer ensayo, pero recibe la crítica que realmente identificaba el defecto. No vuelve a pedir al14B que sustituya esa crítica con otra suya. Solo llama una vez al corrector por caso y deja la revisión posterior pendiente, sin inventar un `no_issues_found`.

Después el asistente leyó los cuatro textos generados, los contrastó con sus fuentes y registró los problemas restantes en un archivo posterior separado. Los recibos originales mantienen su estado temporal de revisión externa pendiente; no se reescribieron retrospectivamente. Todo sigue `unverified`, publicationfalse, participante cerrado. No se usa esta revisión técnica como aceptación docente ni evaluación del alumno.

Este camino es ejecutable por inyección explícita de una crítica suministrada y auditable; **obtener automáticamente críticas con esta capacidad sigue pendiente**. No se conecta silenciosamente un servicio externo al producto local ni se presenta al14B como un verificador independiente.

## Recursos y pruebas

Presupuesto nuevo y separado tras la rectificación del usuario:4correcciones máximas+1calentamiento,768tokens/50s por llamada,10min globales; no altera ni oculta el ensayo anterior. Mismo Qwen2.5-14B-Instruct NF4 local, snapshot `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`, encoder CPU, originales/índice existentes y fuentes revalidadas.

Consumido4llamadas+1warmup. Las4terminaron stop, sin truncamiento; tiempos de corrector18,890–32,687s, suma103,294s;1568tokens nuevos. Duración global135,875s, inferior a10min. El coste de la revisión del asistente no se mide como si fuera latencia de un servicio automático. GPU582MiB/0 % antes, pico19244MiB,582MiB/0 % tras limpieza; una medición adicional posterior655MiB/0 %. Worker35156 y descendientes79720/81460 detenidos, salida0. Sin servidores nuevos ni procesos ajenos tocados.

77pruebas CPU del bloque corrector/contratos correctas, incluida validación de críticas suministradas, una sola llamada de reparación, ausencia de falso posveredicto, aislamiento/historial y limpieza. La suite previa de integración/retrieval/UI contaba108correctas; comprobaciones finales consolidan los archivos afectados. Formato/imports corregidos antes de congelar el protocolo. Sin nuevo modelo, descarga, instalación, cambio de corpus/índice o uso de reserva.

Consolidación final: **110pruebas CPU correctas** (`tests-final.log`), Ruff/Black correctos. `changes-final.json` comprueba que los cuatro contextos son exactamente los históricos, las críticas congeladas no cambiaron, cada caso tuvo una sola corrección stop y el snapshot ejecutable del ensayo anterior coincide con su congelación. Estados e IDs históricos de SpecKit preservados, tareas nuevas anexadas. `final-status.json` confirma ausencia de procesos propios de ambos experimentos/fixture restantes. No se enviaron mensajes a otros chats: la autorización anterior de un único reporte ya estaba consumida y esta petición se respondió directamente al usuario.

## Comparación honesta con el primer intento

| Ensayo | Qué revisión recibió el corrector | Resultado |
|---|---|---|
| Autocrítica14B:4casos expuestos+4nuevos |Otra llamada del propio14B;3informes inválidos y defectos prioritarios no detectados.|0mejoras claras;1cambio más largo sin ganancia,7textos idénticos.14llamadas+1warmup.|
| Control asistido:4casos expuestos |Objeciones concretas del asistente, con sus fuentes, escritas antes de corregir.|2objetivos corregidos,2mejoras parciales, con errores residuales identificados después.4llamadas+1warmup.|

Las muestras y funciones no son equivalentes: **no se convierte esta tabla en una tasa general ni una comparación controlada de modelos**. Sí responde a la pregunta concreta: una candidata puede mejorar cuando la revisión que detecta el defecto entra realmente en el bucle; reemplazarla por un revisor que no lo detecta no prueba esa propuesta.

Se conserva la implementación optativa de ambas vías, pero ninguna habilita estudiante/publicación ni se promueve como tutor correcto. Sigue pendiente la capacidad de revisión autónoma y el recorrido E2 real; no se cierra la feature. No se ejecuta otra ronda de reparación para ocultar los problemas que persisten.
