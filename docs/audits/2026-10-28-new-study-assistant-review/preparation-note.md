# Preparación y primer intento conservados

El primer proceso propio arrancó a las 13:27:08 Europe/Madrid (28-10-2026),
PID launcher 53476 / Python 104724. A las 13:29 aproximadamente seguía sin
crear protocolo, recibo, worker ni solicitud académica. Se detuvieron únicamente
esos dos PID propios tras comprobar sus líneas de comando. No hubo worker CUDA,
calentamiento ni llamada académica en ese intento. Se conserva su invocación
exacta en `invoke-first.py`; no hubo salida de consola que archivar.

La invocación idéntica se reprodujo con diagnóstico CPU (`-X importtime` y
faulthandler de 15 segundos), conservado en `console-recovery.log`. La traza
localiza una espera real en la creación de la estructura de imports de
Transformers al cargar SentenceTransformers para el encoder CPU. Es evidencia
de esa reproducción, no una prueba retrospectiva de la pila exacta del primer
proceso. No se modificó código de producto ni se cambió la pregunta o el modelo.
La reproducción progresó al índice existente y congeló la solicitud antes de
cargar el 14B. No se renovaron cupos académicos ni se amplió el límite humano
de 20 minutos. Se eligió un techo interno conservador de 900 segundos para la
invocación; la duración total de la tarea se comprueba además antes de cerrar.

La primera ejecución de pytest falló en setup al no poder crear su temporal
predeterminado (24 errores, ninguna prueba ejecutada). Se repitieron las mismas
24 pruebas con `--basetemp` exclusivo dentro del dossier: 24 correctas, una
advertencia preexistente Starlette/httpx. Resultado íntegro en `tests.log`.
