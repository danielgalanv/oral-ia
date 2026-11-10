# Guion final de autoestudio: entrega completa, contenido con pendientes

29-10-2026. **Seis preguntas exactas enviadas una vez en navegador real; seis respuestas completas, mostradas y confirmadas.** No invalidated, fetch fallido, truncamientos ni reintentos de preguntas en esta ejecución. No implica aceptación general del tutor ni piloto con estudiantes.

[Preguntas y respuestas íntegras](transcript-mobile.md) · [Lectura móvil HTML](transcript-mobile.html) · [Comprobaciones de ejecución](execution-checks.json) · [Historial exacto y validación final](final-validation.json).

## Preparación y contratiempos conservados

Usuario autorizó expresamente descargar los modelos residentes de ComfyUI y detener Dolphin. Se comprobó PID40912 y ruta/modelo dolphin-venice antes de detenerlo; cola ComfyUI8191 vacía antes de POST/free, sin cerrar su interfaz ni borrar archivos. GPU pasó de21049/32607MiB a2155MiB. No se detuvieron otros servicios del usuario ni se reinician automáticamente sus modelos.

Un diagnóstico CPU inicial en sandbox no terminó y fue interrumpido sin inferencia. Primer arranque fuera del sandbox rechazó identidad del índice antes de cargar Qwen: el hash completo de retrieval.py cambió con la implementación de selección comparativa. check_identity.py confirmó que **solo implementation_sha256 difiere**; fuentes, encoder/configuración/versiones y demás identidad coinciden. Ver identity-difference.json. No se eliminó la guarda ni se reescribió identity.json.

El runner aislado run.py construyó un índice CPU NUEVO en isolated-index/ con código actual y corpus íntegro. Se conserva recuperacion-v2.1 histórica. Es un cambio respecto de la intención inicial de usar build=False; queda declarado, no como reparación retrospectiva del índice. Los incidentes de arranque consumieron cero llamadas académicas. No se modificó código de producto ni assets habituales; se sirvió el build aislado de study-cpu/web-dist.

## Configuración y límites efectivos

Qwen2.5-14B-Instruct NF4 local, snapshot cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8, qwen25-14b/structured/v1 y study-dialogue/v1, greedy/v1 semilla42. Recuperación densa CPU, comparison-coverage/v1, corpusv2; sin IDs manuales de fuentes, nuevos modelos o descargas. Nuevo perfil optativo study-expanded/v1:2048tokens/180s/16000caracteres; runtime2700s y seis llamadas. Contadores visibles en navegador. Protocolo antes de inferir en protocol.json; las seis entradas exactas se introdujeron con fill, no append.

|Turno|Entrega|Tokens de salida|Generación|Historial enviado|
|---|---|---:|---:|---:|
|1 verificar/validar|stop, mostrada|546|33,203s|0mensajes|
|2 ejemplo de cita médica|stop, mostrada|765|46,781s|2|
|3 aclaración exacta|stop, mostrada|776|48,688s|4|
|4 comprobar reserva|stop, mostrada|791|46,781s|6|
|5 realizable/comprobable, cambio marcado|stop, mostrada|298|18,703s|0|
|6 ejemplo difícil de comprobar|stop, mostrada|459|28,108s|2|

Total6llamadas académicas y un calentamiento de preparación del worker;3635tokens nuevos/222,264s de generación. La carga fue más lenta que en arranques anteriores, aproximadamente100s según avisos: no se presenta como comparación de rendimiento. Preguntas/secuencias, texto mostrado y siguiente historial comprobados íntegros a partir de los recibos. Cuota0/6 al final y botón deshabilitado. No se intentó una séptima llamada.

Los turnos3/4 exceden el techo histórico768 y terminan ahora completos. Los dos cambios (presupuesto y cobertura) se aplicaron juntos; no es comparación causal que atribuya toda diferencia solo al presupuesto. El turno2 actual usa765tokens: su terminación no prueba por sí sola que necesitara más de768. Ninguna salida de esta ejecución superó4000caracteres; la propagación de respuestas mayores sigue acreditada por pruebas CPU, no por estos seis ejemplos.

## Contenido: evaluación proporcionada

- **1 y2: necesitan precisión conceptual localizada.** Presentan verificar=individual y validar=conjunto como diferencia definitoria. Procedimiento10 recibido también verifica el conjunto. La validación no se distingue por escala, sino por correspondencia con necesidades/uso previsto, entre otros controles del material. Las explicaciones de calidad son útiles; no se invalidan todos sus ejemplos. «Complejidad» aparece donde la explicación define completitud: error terminológico concreto, no motivo para condenar el conjunto por estilo.
- **3: continuidad comprobada, aclaración poco útil.** Mantiene el ejemplo médico, pero repite prácticamente los contenidos y extensión de2. No falla por repetir encabezados, sino por no ofrecer una explicación sustancialmente más accesible a la duda expresada. Persiste la distinción discutible de1.
- **4: respuesta completa pero pertinencia insuficiente.** Ante «¿Cómo podría comprobar que una cita se reserva correctamente?» vuelve a enumerar calidad del requisito y verificar/validar. No aporta una secuencia concreta de acción/resultado esperado para una reserva. No basta cambiar buscar por reservar. Este es un defecto funcional de respuesta a la petición, no una exigencia de exhaustividad.
- **5: básica y aprovechable.** Distingue implementación con recursos y posibilidad de comprobar. La comprobación no debe limitarse necesariamente a después del producto final; precisión mejorable. No se exige todo un protocolo estadístico al ejemplo de99%.
- **6: ilustrativo y aprovechable.** El95% y las condiciones son ficticios del ejemplo permitido. Se explican muestra/entorno/«uso normal» como dificultades de prueba. Conviene plantear la viabilidad como supuesto del ejemplo, no certificar una tecnología general sin evaluación; no rechazar la cifra por no ser literal en el documento.

## Selección de fuentes

En1 la heurística promueve Procedimiento11 y Requisitos74 (técnicas de validación). Sus facetas registradas son verif y requi/valid; ambas tienen coincidencias léxicas, pero eso NO acredita cobertura semántica de la distinción. Siguen sin entrar Procedimiento12/Requisitos72, que desarrollan la correspondencia con necesidades. Registra «unmatched_facets=[]», pero no equivale a cobertura suficiente. La heurística nueva **no ha demostrado resolver P1**. No se altera para hacer pasar este banco expuesto.

El turno4 recibe Requisitos13, NASA210, Procedimiento11, Requisitos61 y Modelos38; la respuesta arrastra el marco de la conversación anterior. Recuperación y generación deben comprobar qué parte de la pregunta es nueva y cuál referente se conserva; no basta con pasar el historial correcto. Todos los pasajes completos y metadatos se conservan en api-*.json.

## Evidencia y limpieza

La aplicación normal mantiene contenido temporal; el harness de ESTE ensayo autorizado captura exclusivamente respuestas de /turn, /display y /shown de las seis preguntas prefijadas, sin cookies o headers de autenticación. No se añadió persistencia al producto. Texto íntegro generado y fuentes en transcript-mobile y recibos; hashes de recibos en receipt-hashes.json. No síntesis ni corrección académica posterior de textos.

Los hashes de los ocho archivos de implementación/frontend de la entrega CPU coinciden todavía con completion.json original. Se reutiliza su validación67Python/11Node sin atribuirla a este ensayo GPU ni repetir suites sin cambios. El harness fue validado por la interacción real y las aserciones de entrega/historial. No build o lint de producto nuevos, commits, Reset, enmiendas de gates, alumnado, examen o voz.

Al terminar se pulsó Cerrar inspección y descartar, observándose «Inspección cerrada; contenido descartado». Después se interrumpió exclusivamente el servidor propio sesión49210/PID35804. Sin listener8027 ni PID35804/22420 presentes en comprobación final; GPU2256MiB/0%. La interrupción salió1 y no produjo worker-cleanup.json: se acredita desaparición de procesos/retorno de VRAM, no un cierre ordenado ficticio. El índice aislado/evidencia se conservan; no se borraron para ocultar el incidente.

## Decisión

**La entrega técnica del guion está comprobada con estos cambios; la utilidad de toda la conversación todavía no.** No pedir al usuario otra repetición del mismo guion como si ya estuviera resuelto. Próximo incremento debe atender comparación de conceptos y cambio de acto (de explicación a procedimiento de prueba), manteniendo evaluación contextual y sin respuestas académicas prefabricadas. No hace falta cambiar el modelo ni ampliar otra vez el presupuesto basándose solo en estas observaciones. Las mejoras menores no bloquean; los turnos1/4 sí merecen corrección localizada por lo que enseñan o dejan de contestar. No publicación participante ni cierre general de Feature012.
