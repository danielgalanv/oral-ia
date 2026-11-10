# Recorrido de autoestudio en navegador — 29 de octubre de 2026

## Resultado

**La comprobación funcional del incremento está completada:** cuatro preguntas exactas enviadas mediante la interfaz, cuatro respuestas completas realmente visibles, cuatro confirmaciones de mostrado, aclaración con contexto, cambio explícito de tema y apertura visual del PDF original. No hubo `invalidated`, `Failed to fetch` ni truncamientos en las respuestas. No se modificó producción para esta prueba.

El resultado permite cerrar esta comprobación técnica del incremento, conservando las limitaciones de contenido ya observadas. No equivale a aceptación docente, eficacia educativa con estudiantes ni cierre de toda Feature 012.

## Recorrido ejecutado

1. Entrar en consulta documental y en inspección temporal desde el navegador integrado.
2. Preguntar cómo se utilizan las entrevistas para descubrir requisitos. Se muestra explicación con finalidad, métodos y límites, apoyada en las diapositivas 60–61, 52, 54 y 87.
3. Pedir preguntas para el responsable de una biblioteca. Mantiene el tema y ofrece preguntas pertinentes sobre problemas, necesidades y proceso de préstamos.
4. Pedir aclaración sobre por qué esas preguntas no bastan. Conserva el caso de biblioteca, explica conocimiento tácito y ambigüedad, y propone complementar las entrevistas.
5. Activar «Cambiar de tema y descartar referente anterior» y preguntar qué es un requisito no funcional con ejemplo. La petición contiene **cero mensajes anteriores**; responde con propiedades/restricciones y un ejemplo hipotético de tiempo de respuesta inferior a dos segundos. No arrastra la biblioteca.
6. Desplegar «Fuentes consultadas y pasajes recibidos», abrir el enlace del PDF original en la página 15 y comprobar visualmente la diapositiva **Non-functional requirements**. La petición al original devuelve HTTP 200 y `application/pdf`; el visor muestra las páginas 15–16. Cerrar la pestaña del PDF y regresar a la conversación.

Se utilizó el navegador integrado; no se presenta como prueba de Chrome. La primera navegación se intentó mientras el servidor aún preparaba el modelo y agotó el tiempo de navegación; se retomó la misma pestaña tras la confirmación de arranque. No consumió llamadas académicas. Un selector automático de rol no reconoció un `<summary>`; se inspeccionó el DOM y se activó por el texto visible. No fue un fallo del control para el usuario ni una llamada repetida al modelo.

## Valoración del contenido

Las respuestas son útiles para una explicación introductoria: describen el papel de las entrevistas, aplican el ejemplo, justifican sus límites y distinguen correctamente el requisito no funcional del comportamiento funcional en el ejemplo final. No se exige exhaustividad ni un estilo ideal para aceptar su utilidad.

Se conserva la imprecisión ya conocida en el etiquetado de preguntas abiertas/cerradas: varias preguntas exploratorias aparecen bajo un grupo denominado «cerrado». En la explicación también aproxima entrevista formal/informal a guion fijo/exploración; esa equivalencia es simplificadora. El material separa entrevista formal/informal de sus tipos abierta/cerrada. No se afirma que cada frase de las cuatro respuestas esté verificada ni que esos detalles hayan sido corregidos. Tampoco se invalida por ello la pertinencia de las preguntas propuestas para una biblioteca.

La aclaración sí desarrolla el referente anterior: usa préstamos, términos que se dan por supuestos y búsqueda de libros; no cambia a un ejemplo ajeno. La respuesta no funcional es aceptable para la pregunta planteada. Su umbral de dos segundos es hipotético, no una norma atribuida al material.

## Medidas y evidencia

- Cuatro llamadas académicas; quedaron dos de las seis permitidas por el proveedor. Sin reintentos automáticos.
- Todas terminan con `stop`: 721, 406, 565 y 246 tokens, **1938 tokens nuevos** en total.
- Historial recibido: **0, 2, 4 y 0 mensajes**; `focus_change: true` en la cuarta.
- Doce operaciones turn/display/shown, todas HTTP 200. Cuatro confirmaciones de mostrado.
- Mismo Qwen2.5-14B NF4 local, perfil nativo, greedy/semilla 42; límites 2048 tokens y 180 segundos por turno. Tiempos observados de generación: 40,905; 23,735; 32,985 y 14,593 segundos. No se presentan como comparación de rendimiento.
- Se usa el frontend aislado ya compilado y el índice existente, sin reconstrucción ni reescritura de identidad. Los hashes de cuatro módulos y 308 archivos previamente registrados siguen iguales.
- Los recibos del dossier corresponden exclusivamente a las cuatro preguntas de prueba autorizadas. El middleware de este harness no registra cookies ni cabeceras de autenticación; no cambia la política de conservación del producto.

## Cierre de servicios

Después de abrir el original y regresar, la conexión de automatización del navegador dejó de estar disponible al intentar pulsar «Cerrar inspección y descartar». **No se da ese clic por realizado ni se acredita aquí el cierre mediante botón.** Se detuvo el servidor propio desde su consola, eliminando la memoria efímera del proceso. Se verificó la ausencia del servidor PID 19180, del worker PID 58176 y de un listener en 8027. GPU final: 1334 MiB, 0 %.

El proceso de consola terminó con código 1 al interrumpirlo; no produjo `worker-cleanup.json`. Se conserva esta diferencia respecto de un cierre limpio por lifespan y no se inventa un recibo de limpieza. No fue necesario detener procesos ajenos. La prueba de preguntas/cambio/fuentes había terminado antes de esa pérdida de control del navegador.

## Archivos

- [Transcripción completa](transcript-mobile.html)
- [Recibos y controles](execution-checks.json)
- [Respuesta visible al cambiar de tema](verified-response.png)
- [PDF original abierto en la página 15](original-page-15.png)
- [Protocolo previo](protocol.json)
- `api-001.json`–`api-012.json`: peticiones y resultados completos del recorrido real.
