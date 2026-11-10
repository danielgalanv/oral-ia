# Incremento didáctico acotado: implementado, resultado insuficiente

Se ejecutó el banco expuesto del usuario con cuatro llamadas reales y un calentamiento. El cableado nuevo funciona, pero **la tercera respuesta todavía no aclara el último ejemplo mostrado**. No se declara corregida la incidencia didáctica ni se considera aceptada la prueba humana. No hubo otro ajuste, reparación o repetición después de observar este resultado.

[Antes y después íntegros para móvil](transcript-mobile.md) · [HTML adaptable con fuentes completas](transcript-mobile.html) · [Comparación estructurada](observed-comparison.json).

## Qué está comprobado y qué es hipótesis

La ruta inspeccionada es DiagnosticStudy.INSTRUCTION → RealStudyProvider.for_session → structured_request → StructuredGenerationRequest.effective_messages → render_messages → frame de cached_transformers → validate_structured_frame/native_tokens en el worker.

Hecho comprobado: structured_request sustituye base.instruction por «Host renderer structured/v1» y no pasa la instrucción de StudyLab al system. El system anterior se reconstruía exclusivamente con BASE+TASKS. Algunas reglas de evidencia, límites y ficción estaban duplicadas en BASE; otras se perdían. La propia INSTRUCTION anterior tampoco contenía una política específica de brevedad/reformulación, así que conservarla sin más no habría demostrado resolver esta incidencia.

Hecho comprobado: TASKS.generate pedía una explicación «pertinente y completa» y un ejemplo, pero no distinguía la extensión de una petición sencilla ni el acto de aclarar el último referente. Es hipótesis —no causa aislada probada— que esa formulación, las fichas/checklists recuperadas y la estructura previa del historial favorezcan respuestas largas y repetitivas. Las fuentes reales del primer turno incluyen NASA70 y208; no se cambiaron para favorecer la prueba.

Se añadió una política registrada, **study-dialogue/v1**, activada únicamente en el camino real optativo de inspección docente. No se copian instrucciones arbitrarias del request al system. Los perfiles genéricos sin opt-in, review y repair conservan su comportamiento anterior. El frame declara el perfil y el worker reconstruye/valida exactamente el mensaje esperado. No hay comparación de cadenas de las preguntas, ejemplos prefabricados, selección manual de sourceIDs, clasificador de tres casos o prohibición universal de fichas/listas.

La política pide extensión proporcionada, otro ejemplo del mismo concepto, aclaración del último contenido realmente mostrado con enfoque más sencillo, ampliación cuando se pide detalle/ficha y ausencia de certificación de consistencia/completitud/validación de un proyecto no recibido. Permite valorar el carácter académico del propio ejemplo y usar ficción coherente. No se aplican filtros por vocablos aislados.

## Ejecución y resultado observado

Original humano leído completo y copiado sin alterar sus bytes a baseline-human.txt; hash en baseline-source-hash.json. Los tres ejemplos originales son funcionales aceptables. La ficha larga no solicitada y la falta de aclaración son problemas didácticos; la certificación de propiedades de un proyecto desconocido es una afirmación localizada sin base, no prueba de que los ejemplos funcionales sean conceptualmente incorrectos.

Después: Qwen2.5-14B-Instruct NF4, greedy/v1, seed42, plantilla nativa, política nueva y corpusv2 con recuperación densa CPU/build=False. Las tres preguntas exactas se enviaron consecutivamente en navegador real, con lo realmente mostrado en el historial. Se añadió únicamente la pregunta de cambio de tema congelada en protocol.json. Los cuatro frames reales y recibos display/shown están conservados; build_evidence.py verifica correspondencia exacta frame↔request, salida completa↔preview, ACK de mostrado y restricciones768tokens/50s.

|Petición|Contenido académico|Objetivo didáctico|
|---|---|---|
|pon un requisito funcional|Ejemplo funcional de búsqueda/reserva de vuelos aceptable.|Más corto que la ficha original y sin certificar el proyecto, pero todavía añade cuatro criterios no pedidos. Mejora parcial.|
|pon otro ejemplo|Conserva el concepto y ofrece un caso diferente: inventario tras venta.|Repite la lista/estructura. No se alcanza la brevedad prevista.|
|explicalo de otra manera|Otro ejemplo funcional aceptable, ahora de gestión de tareas.|No aclara el inventario anterior: cambia sustantivos/ejemplo y repite plantilla. Objetivo NO alcanzado.|
|Ahora cambiamos de tema: ¿qué es la trazabilidad de requisitos?|Responde sobre trazabilidad, sin arrastrar el inventario; frame sin historial.|Explicación básica aprovechable. El cierre que atribuye al trazado requisitos necesarios, únicos y verificables es demasiado fuerte: necesita un matiz localizado, sin condenar toda la respuesta por una palabra.|

El cambio de tema se marcó explícitamente en el control existente. Los frames contienen0/2/4/0mensajes de historial y la tercera llamada recibe exactamente las respuestas1y2 reales. No se inyectó una respuesta ideal. Las cuatro terminaron con stop y fueron mostradas/confirmadas. Fuentes y omisiones completas en api-*.json y capturas turn-01..04-ui.txt.

El antes/después es **observacional**, no una comparación causal: el adjunto humano no conserva aquí sus frames, pasajes desplegados ni configuración completa. Este banco es regresión expuesta, no reserva o transferencia. Las pruebas de cableado no acreditan mejora semántica; el resultado real impide afirmar que esta política ya resuelve la aclaración.

## CPU, interfaz y caducidad

62pruebas CPU aprobadas: perfil optativo y frame efectivo, preservación de límites, datos adversarios/control tokens, separación de roles, referente mostrado, descarte de candidata no confirmada/cambio de tema, cierre/cancelación y caducidad. Ruff y Black correctos. Son pruebas técnicas con fixtures; sus respuestas sintéticas no se cuentan como contenido académico.

Se reutilizó el build aislado de runtime-expiry-ui, previamente compilado/lintado, copiándolo al dossier propio e incorporando un aviso visible de captura autorizada. Se verificó ese frontend real con los cambios Python: contador decreciente y deadline fijo20:26:26 en los cuatro turnos, límite por pregunta separado del global, permiso temporal y cierre/descarte. El vencimiento/red simulados permanecen cubiertos por las pruebas fake-clock/API/SSR del dossier anterior; no se finge que se hayan repetido manualmente con GPU en este ensayo. No se sustituyó apps/web/dist ni se publicó la interfaz en la sesión del coordinador.

La captura persistente es exclusivamente del harness de prueba autorizado, anunciado en la página; no se añade escritura de conversaciones a la aplicación ordinaria. Los recibos no guardan cookies ni cabeceras de autenticación. Todas las candidatas siguen unverified/not_assessed, publication_allowed=false y participant_display=null.

## Recursos y parada

El coordinador comunicó que había detenido su propio user-runtime-005. Antes de cargar se comprobó GPU2225/32607MiB,0%, y ausencia del PID77592 que figuraba en su worker-ownership. No se terminaron procesos ajenos ni se usó8027. No se inventó un recibo de limpieza para ese proceso anterior.

La prueba propia usó únicamente8028 con directorio exclusivo y reloj desde first-preflight.json,19:56:26 hora Madrid. Cuatro llamadas+unwarmup; ningún reintento, revisión o reparación. Se cerró la inspección y se activó finish.flag para cierre normal del servidor propio. server.log registra Application shutdown complete / Finished41724; worker-cleanup registra PID68884 y dos descendientes detenidos, returncode0. El cierre GPU medido se produjo369,734s después del preflight, dentro de1800s. GPU final2052/32607MiB,2%; sin listener8028. No se deja modelo o servidor preparado.

La fase termina aquí. El código experimental optativo y su resultado quedan revisables, **sin proclamarlo una corrección didáctica conseguida ni iniciar una nueva iteración**. La prueba/aceptación del usuario sigue pendiente; no se modifican estados históricos, Feature012, T103 como aceptada ni gates/participante/examen/voz. No hubo descargas, instalaciones, reindexado, commits, Reset, delegación o mensajes interchat.
