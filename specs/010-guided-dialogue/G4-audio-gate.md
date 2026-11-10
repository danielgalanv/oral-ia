# Gate G4: audio real pendiente

La aclaración humana requiere conversación hablada sin pantalla. La implementación actual demuestra la lógica con texto/transcripción y plantillas docentes; no demuestra STT, TTS ni autonomía de personas. G1/T067 sigue pendiente de revisión humana, G2 no está habilitado y G3 no está validado.

Antes de aceptar G4 deben probarse con recursos locales preparados y en ambos modos: captura STT real, lectura TTS inteligible de opciones/fuentes/ayudas, corrección de transcripciones, negaciones, confirmación exacta de conservación y cierre, interrupción, pausa/cancelación y descarte de respuestas o confirmaciones tardías. El silencio no debe convertirse en una petición vacía: la petición vacía actual inicializa la orientación autorizada.

Debe verificarse audio efímero de cierre y revisión posterior al cierre. El endpoint TTS existente requiere un turno almacenado; el cierre efímero elimina ese contenido. Por ello no existe todavía un recorrido de audio completo demostrado. No retener audio por defecto ni reconstruir texto borrado para sintetizarlo. Deben conservarse localhost, autenticación del propietario, cookies, consentimiento, scopes, caducidad, T090/T150 y los límites temporales. No descargar modelos ni anunciar fuentes o audio disponibles sin comprobarlos.

Prueba de aceptación futura: recorrido real sin pantalla en ambos modos, con recursos identificados/versionados, tiempos observados, fallos conservados, interrupción/silencio y consentimiento negativo; revisión humana explícita por caso. Mantener siempre la alternativa textual accesible. Las pruebas automatizadas actuales no aprueban este gate.
