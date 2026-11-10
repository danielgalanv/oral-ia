# Recuperación de cortes de red — CPU

El chat sencillo puede recuperar la sesión vigente tras un fallo transitorio sin reenviar automáticamente la pregunta, duplicar respuestas ni renovar cuotas.

- [Resultado del navegador móvil](browser-1793624564418/result.json).
- [Captura después de recuperar](browser-1793624564418/recovered-chat.png).
- [Regresión Python](regression.log), [interfaz](ui.log) y [comprobaciones finales](final-checks.json).

## Cambio

Antes, cualquier fallo de red borraba las filas visibles y cerraba la vista local. Ahora la vista del alumno mantiene temporalmente lo ya mostrado y ofrece Recuperar conexión. Ese botón solo consulta estado: no genera una respuesta, no recarga modelos y no vuelve a enviar la pregunta.

El nuevo GET /api/v1/study-lab/resume usa los mismos controles de permiso, fuentes, runtime y lease. Devuelve por separado mensajes confirmados, candidata preparada y generación todavía en curso. En el modo del alumno aplica la misma eliminación de datos técnicos: sin bruto, request, outcome ni transporte. La consulta no confirma candidatas ni consume llamadas. La candidata recuperada solo entra al historial cuando vuelve a mostrarse y confirmarse por el mecanismo existente.

La confirmación shown es ahora idempotente: repetirla para el mismo recibo ya mostrado devuelve éxito sin insertar otra entrada. Sigue rechazando candidatas canceladas o inválidas, y vuelve a comprobar autorización y fuentes. Este cambio evita la carrera en la que el servidor había recibido la confirmación, pero el cliente había perdido su respuesta.

Si una pregunta nunca llegó al servidor, el borrador sigue editable. El alumno decide pulsar Enviar; no hay reintento automático. Si sigue generándose, la recuperación lo indica y permite comprobar más tarde o finalizar. Se conserva la caducidad global. Sin conexión válida, un temporizador local borra los mensajes visibles al alcanzar el lease de quince segundos, comprobado en hasta dieciséis; no se añade almacenamiento persistente. La recuperación de la vista docente anterior mantiene sus políticas existentes.

## Evidencia CPU

77 pruebas Python aprobadas, incluidas cuatro nuevas de snapshot: confirmado/pendiente sin nuevas llamadas, generación en curso sin filtración parcial, retirada de fuentes y runtime caducado. Se verifica además la confirmación repetida sin duplicar historial. Quince pruebas de interfaz aprobadas. TypeScript, Vite, ESLint, Black y Ruff focales conformes; Ruff global conserva diez hallazgos anteriores y cero nuevos con multiplicidad.

El navegador real móvil, con GPU desactivada, ejecutó tres cortes:

1. El servidor confirma la entrega y se pierde la respuesta de confirmación: se recupera la respuesta confirmada una sola vez.
2. El servidor termina la generación y se pierde la respuesta de turn: se recupera la candidata preparada y se confirma después de mostrarla.
3. La pregunta nunca llega: recuperar no genera nada y mantiene el texto; solo un nuevo clic explícito la envía.

Con cuatro preguntas aceptadas por el servidor, la cuota seguía en cuatro. Los puertos simulados no recibieron generaciones adicionales al recuperar. También se comprobó con reloj simulado la purga local tras dieciséis segundos de desconexión. No hubo errores JavaScript ni peticiones externas.

Los generadores/revisores de esta prueba fueron fixtures explícitas del circuito de producción, no modelos. No hay nuevas respuestas académicas evaluadas ni medidas de eficacia humana. La recuperación con inferencia GPU real se conserva dentro de la validación integrada pendiente T191.

## Preservación y cierre

Solo cambian dos módulos de producción Python y el componente de conversación. Se conservan las versiones de entrega anteriores y el snapshot actual en release-source. Los grupos históricos de 308, 140 y 22 archivos conservan sus hashes. No se modificaron los PDF, prompts, modelos o criterios académicos.

El servidor propio en 8049 está detenido y el puerto libre. No se detuvieron servicios ajenos. No hubo GPU, modelos generativos, migraciones, Reset, commits ni apertura de publicación/participantes.

T192 queda completada como mejora y validación CPU. T191 y los pendientes previos de Feature 012 mantienen su estado.
