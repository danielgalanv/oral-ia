# Interfaz de autoestudio — campo accesible, espera y cierre seguro

Se implementan las tres mejoras priorizadas, sin cambiar modelos, prompts, criterios académicos o backend de sesiones. T200 es una mejora de interfaz comprobada con simulaciones, no la validación real pendiente T191.

## Cambios

- **Campo de pregunta accesible:** la conversación ocupa un área desplazable y el formulario permanece en pantalla. Se puede leer historial sin saltos automáticos; Ver últimos mensajes permite volver al final. Enviar sigue siendo la confirmación explícita; Intro inserta líneas. El texto no se recorta ni se convierte en HTML.
- **Espera comprensible:** Preparando la respuesta muestra segundos transcurridos desde el envío, con reloj monotónico. No se inventan fases de generación/revisión que el servidor no comunica. El temporizador no provoca anuncios de lector de pantalla cada segundo. Cancelar conserva historial confirmado y borrador; la recuperación de conexión usa un mensaje distinto, sin confundirla con generación.
- **Cierre seguro:** Finalizar se separa del envío y abre confirmación nativa accesible. Seguir estudiando recibe el foco inicial; esa opción y Escape conservan mensajes y borrador y no envían cierre ni nueva pregunta. Finalizar y descartar cancela una petición pendiente, cierra la sesión y limpia la vista. El cierre de pestaña y la caducidad mantienen sus políticas previas; no se añade persistencia ni se renuevan cuotas/plazos.

Solo cambian en producción `DiagnosticStudy.tsx` y `styles.css`. Se amplía el test de interfaz y se actualiza [la guía](../../ESTUDIO.md). Se conservan los archivos anteriores en `DiagnosticStudy-before.tsx` y `styles-before.css`, y las fuentes finales en `release-source`.

## Evidencia

- **55 pruebas Python** aprobadas: [regresión operativa](http-regression.log). Cubren recuperación, cuotas, cancelación, sesiones extensas y composición revisada con proveedores simulados. Una advertencia existente de Starlette/httpx, sin fallos. No se repite ni se suma aquí la campaña de 716 pruebas anterior.
- **16 pruebas de interfaz** aprobadas: [resultado](ui-unit-final.log). [TypeScript](typescript-final.log), [ESLint](lint-final.log) y la construcción Vite aislada conformes. No se alteran módulos Python de producción.
- [Recorrido final del navegador](browser-1793650705889/result.json), con ocho respuestas largas simuladas, continuación tras cancelación y cierre durante otra petición. Verifica móvil 390×844, tamaños reducidos 390×420 y 320×400, y escritorio 1280×800. Comprueba campo/Enviar dentro de pantalla, lectura de mensajes anteriores, retorno al final, foco seguro del diálogo, Escape, seis segundos reales de espera y ausencia de nuevas generaciones por abrir/cancelar la confirmación.
- La [primera ampliación a 320×400](browser-1793650650000/result.json) detectó Enviar por debajo de pantalla. Se corrigió evitando que Ver últimos mensajes consumiera una fila adicional del área de lectura; la ejecución final pasa. El intento fallido y sus capturas permanecen intactos.
- [Regresión de cortes de red](network-1793650816870/result.json): confirmación perdida, respuesta preparada perdida, pregunta no recibida y purga local a los dieciséis segundos siguen pasando sin generaciones duplicadas.

En las pruebas de navegador hubo once envíos explícitos, dos cancelaciones/descartes de peticiones lentas simuladas y un único cierre confirmado. Se conservaron nueve respuestas confirmadas hasta ese cierre. No hubo errores JavaScript ni solicitudes externas. Los proveedores fueron fixtures explícitas del circuito de revisión; no se cargaron modelos generativos, revisores o embeddings, ni se usó GPU.

## Capturas

- [Móvil](browser-1793650705889/mobile-chat.png).
- [Vista reducida](browser-1793650705889/short-viewport.png).
- [Escritorio](browser-1793650705889/desktop-chat.png).
- [Espera cancelable](browser-1793650705889/waiting.png).
- [Confirmación de cierre](browser-1793650705889/confirm-close.png).

La reducción de altura es una comprobación de distribución, no una validación con teclados físicos de todos los móviles. No constituye una auditoría WCAG completa ni una prueba con lector de pantalla real. Las respuestas visibles son texto de prueba; no acreditan calidad académica. Los avisos anticipados de cuota/plazo y una presentación adicional por autor no forman parte de estas tres mejoras.

## Cierre y límites

Los servicios propios en 8055 están detenidos y el puerto libre. Se verifican los hashes de los grupos históricos de 308, 140 y 22 archivos; no se suman como archivos únicos. Sin cambios de datos habituales, corpus, modelo, instalación, Reset, commits, gates o publicación. Las [comprobaciones finales](final-checks.json) y el [manifiesto de fuentes](release-manifest.json) registran el alcance.

T200 se completa. La validación del chat con modelos reales se mantiene para GPU; no se repite inferencia lenta en CPU como sustituto.
