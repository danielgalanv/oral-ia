# Preparación y contabilidad

Primer preflight inicia el único reloj de30min. Ningún incidente CPU lo reinicia.

La primera verificación de tokenización comparó directamente el retorno de
apply_chat_template con una lista. Transformers local devuelve BatchEncoding:
los input_ids eran iguales, pero los tipos no. El fallo se conserva en
tokenizers-first-failure.log y verify_tokenizers-first.py. Se diagnosticaron los
IDs reales y se normalizó únicamente la extracción de input_ids; después pasaron
las cinco equivalencias. No fue duplicación de tokens Qwen ni carga de pesos.

Un primer parche no coincidía con el formato tras Black y se rechazó sin editar;
se leyó el archivo y se aplicó en la línea real. Ruff inicial señaló formato de
strings/imports, corregido antes de congelar código e inferir. Logs conservados.

Tras la comparación GPU se añadió una corrección de observabilidad: parámetros
numéricos del outcome reflejan temperatura efectiva y semilla para los perfiles
muestreados, en vez de presentar el informativo0 histórico. CPU107pruebas finales.
No cambia las dos llamadas medidas: fueron greedy, semilla42, parámetros brutos
conservados. Código realmente ejecutado en executed-code/ coincide con code-freeze.
No se atribuye esa mejora CPU posterior a las respuestas GPU.

No hubo reparación mecánica de una inferencia, segunda carga o calentamiento.
Dos llamadas académicas efectivas, un calentamiento técnico y una carga14B.
Dos preguntas nuevas preparadas sin ejecutar por la condición de parada.

Comprobación final adicional: el builder admite también constraints/historial de
LabGenerationRequest convirtiéndolos por valor, sin aumentar su768/50s. Se añade
regresión focal y108pruebas pasan en tests-final-delivery.log. Las solicitudes
medidas procedían de RepairGenerationRequest; su contenido no cambia por esa
compatibilidad CPU posterior. Ninguna inferencia adicional.
