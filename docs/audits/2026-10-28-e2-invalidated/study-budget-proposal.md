# Presupuesto de estudio: propuesta optativa, no activada

Actualización29-10: la adaptación fue implementada y probada exclusivamente en CPU,
con defaults históricos intactos. Véase ../2026-10-29-study-cpu/report.md desde el
directorio de auditorías. Las secciones siguientes conservan la propuesta anterior;
no se ha ejecutado una nueva validación GPU ni activado el perfil en un servicio.

## Hallazgo nuevo comunicado por el coordinador

Prueba en curso: docs/audits/2026-10-28-coordinator-six-turns/run.py, servicio propio del coordinador en8027, ejecución4939. P1 completa. P2 devuelve generation_length_limit: finish_reason=length, salida768tokens, latencia45875ms, entrada2845tokens; worker listo y cupo2/6 consumido. Se registra este dato comunicado, sin modificar ni consultar la sesión Chrome, su GPU o su servidor.

Aquí la causa observable de la falta de respuesta completa es el límite de salida de768tokens, cerca del plazo histórico de50s. No equivale a comprobar que el paso5 del ensayo humano anterior agotara cupo, tuviera el mismo límite o invalidara fuentes. No se atribuye un error académico a P2 por terminar truncada.

El coordinador continúa el guion y ha documentado un error propio de entrada en P3: typeText añadió texto a P2, cuyo borrador permanecía retenido. No anunciar seis preguntas exactas si los recibos no lo acreditan. El tratamiento de esa ejecución corresponde a su dossier, que no se modifica aquí.

## Recomendación concreta

Mantener el perfil histórico por defecto durante el ensayo actual. Si se decide otro ensayo posterior, preparar un perfil de estudio ampliado **explícito y optativo**, con2048tokens/180s y16000caracteres por candidata/historial, aprovechando la capacidad ya existente de RepairGenerationRequest/StructuredGenerationRequest y del worker NF4. No basta con cambiar max_tokens en el proveedor ni con usar un deadline180 frente a consumidores que siguen limitados a4000caracteres/50s.

Esta ampliación puede evitar el truncamiento observado; **no corrige por sí sola las fichas repetidas o una aclaración que cambia de referente**. La didáctica y la terminación de transporte deben evaluarse separadas. Tampoco garantiza una respuesta completa bajo cualquier contexto: siguen rigiendo el plazo global, los límites de salida y la posibilidad de finalizar incompleta.

Cambios mínimos necesarios, todos restringidos al nuevo opt-in:

1. Registrar un perfil de presupuesto de estudio en la composición local. Mantener768/50s/4000 en el histórico; rechazar perfiles desconocidos. Selección de perfil en arranque, no a través de texto libre del usuario o fuentes.
2. DiagnosticStudy debe construir RepairGenerationRequest/RepairGenerationMessage solo para el perfil ampliado, conservar pregunta2000 y máximo tres pares mostrados, admitir16000caracteres por candidata y mensaje de historial. No truncar lo realmente mostrado al reutilizarlo como referente. Mantener los límites históricos en los demás caminos.
3. RealStudyProvider y su binding deben declarar el deadline180 coherente y conservar el opt-in de capacidad ampliada del worker ya disponible. El frame debe registrar max_tokens2048/deadline180000 y el perfil explícito. El transporte puede seguir denominando su capacidad repair-expanded/v1; eso no activa revisión/reparación automática ni concede autoridad semántica.
4. El timeout efectivo sigue siendo min(plazo por pregunta, tiempo global restante). Ninguna recarga, reentrada o selección de perfil reinicia el reloj global ni el cupo compartido. Cancelación/retirada siguen invalidando y deteniendo la entrega tardía.
5. Catálogo/open/state/turn deben exponer el perfil y el plazo efectivo. La UI debe anunciar180s antes del envío, mantener contador global/cupo y mostrar candidatas completas hasta16000caracteres. Sus guards de display/shown, mensaje de espera y advertencia de tiempo insuficiente deben usar el mismo perfil. La UI actual ya acepta deadline dinámico, pero la rama Python rechaza180 y el historial/candidata mantienen4000: hay que cablear ambos.
6. Pruebas CPU focalizadas: default768/50/4000 intacto; perfil ampliado declarado y frame2048/180000; respuesta de más de4000 íntegra en display/shown e historial siguiente; límite16000 y perfil inválido rechazados; global restante menor que180, cupo agotado, cancelación y fuentes retiradas sin entrega tardía. No repetir una regresión general ni inferir mejora semántica de estos mocks.

## Estado de esta entrega

**Es una recomendación preparada, no una modificación activa de presupuesto.** No se han cambiado defaults, código de generación, límites, assets o parámetros del servicio en curso. No se ha iniciado otra GPU, servicio o campaña. No se solicita renovar ni gastar el cupo actual. El coordinador puede completar primero su observación real y decidir sobre esta adaptación acotada con evidencia íntegra.

Las correcciones ya entregadas de failure_code, cupo, preparación y caducidad siguen disponibles; no se pierden ni se relajan para hacer pasar una respuesta larga. Prueba humana y aceptación continúan pendientes.
