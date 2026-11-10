# Repetición real con documento/página o URL

31-10-2026. Petición del usuario: repetir las pruebas tras retirar citas literales.
Estado: diez revisiones completadas. **v5 no promovida por rechazos injustificados.**

## Diseño congelado

Diez casos conocidos: D01–D06 y H01–H04 del expediente `2026-10-30-review-web-variety`.
Preguntas, respuestas sintéticas y pasajes idénticos por igualdad de objetos JSON,
con lectura/escritura UTF-8 explícitas. Los antiguos H01–H04 ya están expuestos:
esta repetición es una regresión, no una nueva reserva ni transferencia inédita.
Los oráculos permanecen separados y no se incorporan a los mensajes del modelo.

Perfil `web-review/v5`: el revisor describe el problema y señala la fuente; el host
presenta documento/página o URL. El catálogo se construye desde el manifiesto docente
y los recibos de procedencia web originales, contrastando sus hashes. No se deducen
páginas de nombres ni se inventan enlaces. Los pasajes académicos siguen disponibles.

Qwen2.5-7B local, float32, CPU, ocho hilos, greedy. Hasta diez llamadas, 512 tokens y
420 segundos por llamada, 4500 segundos totales incluyendo carga. No hay GPU, red,
descarga de pesos, ajuste de prompt ni repetición de una salida para hacerla pasar.
Todos los casos caben en 4096 tokens de entrada; medición tensorial previa entre
1003 y 1284 tokens. Se conservó la primera medición previa que contaba las claves
del contenedor del tokenizer en lugar de sus tokens; se corrigió antes de iniciar
inferencia y se congeló el cómputo definitivo. No afectó a ninguna petición enviada.

## Interpretación

Separa contrato válido, referencia correcta, acierto sustantivo de la crítica,
falsas objeciones, respaldo del supuesto conflicto docente y salidas incompletas.
Un identificador existente no demuestra que el pasaje respalde la crítica. Una
paráfrasis de claim ya no es un defecto de formato. No se exige perfección, listas
completas ni existencia literal de cifras ficticias coherentes.

Cambian política y metadatos además del formato: no es una medición causal del
efecto exclusivo de retirar citas. Tampoco acredita conversación completa del tutor
o utilidad con estudiantes. No se incorporan objeciones del asistente al modelo.

## Validación previa

160 pruebas CPU pasan, con un aviso existente de deprecación de Starlette.
Código ejecutado archivado en executed-code, hashes en freeze.json. Versiones y
salidas anteriores intactas. No se cambia ningún gate, corpus activo, dato habitual
ni autorización de participantes. Publicación deshabilitada. Repetir controles
conocidos no completa los controles nuevos de T175.

## Resultado completo

Diez llamadas, diez salidas completas (EOS), 2549,047 segundos incluyendo carga,
sin CUDA. Ninguna repetición ni ajuste de prompt durante esta medición.

| Par | Respuesta correcta | Respuesta defectuosa |
|---|---|---|
| D01/D02, historias | Rechaza indebidamente otro formato permitido y un criterio hipotético sencillo. | Detecta la falsa obligación de plantilla, pero añade una crítica injustificada al criterio ficticio. |
| D03/D04, trazabilidad | Rechaza códigos expresamente ficticios por no aparecer en NASA. | Detecta correctamente que la trazabilidad no se limita al padre y debe contemplar relaciones hacia delante. |
| D05/D06, contraste | Afirma erróneamente que 5:1 contradice un mínimo de 4,5:1. | Identifica el mínimo real de 4,5:1, mejorando el razonamiento anterior; añade una exigencia opcional sobre método/herramienta. |
| H01/H02, V&V | Rechaza injustificadamente distinguir el cumplimiento de especificaciones de la adecuación para usuarios. | Identifica ambas inversiones; crítica académica útil, aunque la redacción «no solo» es imprecisa y el conflicto docente no está acreditado. |
| H03/H04, entrevistas | Rechaza indebidamente el seguimiento abierto «qué ocurrió a continuación» por su foco cronológico. | Detecta que inducir una valoración favorable no es una pregunta neutral. |

**Contenido:** cinco de cinco ejemplos válidos reciben rechazos falsos. En los cinco
defectuosos detecta el problema principal; algunas objeciones adicionales son falsas
o innecesarias. No se resumen como «cero aciertos»: hay correcciones útiles en los
negativos. Tampoco se promueve el perfil por detectar errores cuando rechaza todo.
La v3 anterior había aceptado los cinco positivos y detectado el defecto principal
de cuatro negativos. Hay una mejora localizada en D06 y una regresión clara en los
positivos; la comparación está expuesta y cambia más que el formato de cita.

**Referencias:** los diez resultados usan objetos `source_id` sin `quote`; todos los
identificadores declarados pertenecen a las fuentes recibidas. Sus títulos, páginas
y URLs se resuelven desde el catálogo del host. Esto no equivale a elegir el pasaje
correcto o justificar una afirmación. La comparación muestra esas localizaciones
para inspección incluso cuando el dictamen es inválido, sin cambiar el resultado.

**Contrato completo:** los diez dictámenes fallan primero la regla v5 que reserva
`kind=contradiction` a una referencia docente; todos usan una fuente externa en esa
primera incidencia. Varias críticas también incluyen ambigüedades sin referencia.
No hay fallos de copia literal o de longitud de cita. Ese rechazo tipológico no se
cuenta por sí solo como error académico: las falsas objeciones a los positivos
son identificables aunque se ignore esa regla, y las críticas principales a los
negativos se reconocen por separado. Véanse `semantic-review.json`, `metrics.json`
y la [comparación completa](transcript-full.md).

## Continuación solicitada durante la ejecución

El usuario reafirmó igual exigencia para material docente y web, admitiendo cifras,
nombres y escenarios ficticios coherentes y evitando reparaciones por mejoras
opcionales. Al crear v5 había resumido también la política del revisor, además de
cambiar sus referencias; esa variante no conservó el comportamiento tolerante de
v3. No se atribuye la regresión al mero hecho de retirar citas.

Se conservó y terminó este ensayo sin tocar el prompt. La continuación separada
T177 recupera íntegro el prefijo de criterio v3, mantiene referencias sin citas y
distingue contradicción con una fuente externa de conflicto con el profesor. Su
implementación y calibración están en `../2026-10-31-equal-review-criteria/`;
no reescribe este resultado ni reutiliza su presupuesto. El worker de esta etapa
terminó antes de modificar el código para esa continuación.
