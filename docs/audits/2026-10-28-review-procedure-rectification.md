# Rectificación del procedimiento previo a la entrega

2026-10-28. Seguimiento documental; cero inferencias nuevas. No cambia código,
fuentes, índice, participantes ni gates. No se reescriben recibos históricos.

## Retirada registrada

Se retira la preparación de la campaña de 12 casos/Mistral. En este seguimiento
se habían creado un script `scripts/prepare_distinct_reviewer_bank.py`, un banco
sintético de 12 entradas, un oráculo separado, una copia de 26 páginas de contexto
y copias de spec/plan/tasks en `docs/audits/2026-10-28-distinct-reviewer/`.
Esos archivos nuevos fueron eliminados antes de recibir la instrucción posterior
de conservar una nota de retirada. No se cargaron pesos ni se ejecutaron llamadas
de inferencia. Esta nota conserva qué preparación se retiró; sus contenidos ya
no están disponibles en disco. No se eliminó evidencia histórica de experimentos.

La preparación no comprobaba el fallo señalado: omitir antes de entregar la
revisión que el propio asistente pudo hacer después.

## Procedimiento mínimo, con responsables explícitos

1. Congelar pregunta, candidata completa, solicitud original y mismas fuentes
   disponibles, con hashes. La candidata inicial nunca se sobrescribe.
2. El asistente revisa pregunta, candidata y ese contexto íntegro. La entrada de
   revisión no incorpora etiquetas, objeciones anteriores ni respuesta corregida.
   Se registran autor, entradas, defectos concretos y justificación en fuentes.
   Si se reutiliza un caso expuesto, esa separación de entradas no borra lo que
   el asistente ya conoce: no es una evaluación ciega ni de transferencia.
3. Solo una crítica justificada permite proponer una corrección. El corrector
   recibe la candidata, pregunta, mismas fuentes y crítica registrada; conserva
   lo correcto. Un contrato JSON válido no demuestra que una crítica sea cierta.
4. El asistente contrasta las dos versiones completas con las fuentes. Registra
   defectos corregidos, persistentes, nuevos, omisiones y críticas equivocadas.
   Guarda este contraste aparte; no convierte los recibos previos en aprobados.
   No publica ni declara correcta una salida por el mero cambio de redacción.

## Qué ya existe y qué no automatiza

`src/oralia/course_dialogue/review_repair.py` ya ofrece
`review_request(request, candidate)` y `repair_with_supplied_review(request,
initial, supplied_review)`. Esta última realiza como máximo una corrección y
deja la revisión posterior externa pendiente. Se pueden reutilizar directamente
con `CallBudget(maximum=1, seconds=300)`, un registro exclusivo y revalidación
de las fuentes originales. No hace falta añadir otro harness.

`scripts/run_agent_assisted_repair.py` ilustra esa integración y guarda solicitudes
y resultados, pero ejecuta cuatro casos: **no debe lanzarse sin cambios para la
propuesta de un solo caso**. La integración mínima consiste en invocar el método
existente una vez, después de registrar la revisión del asistente.

La revisión sustantiva inicial y el contraste posterior requieren aquí al
asistente. El corrector local automatiza la reescritura, no ese juicio. En cambio,
`process(request, initial)` pide autocrítica al mismo modelo y además un
post-review; no es el recorrido de una revisión del asistente y una corrección
propuesto aquí. No se sustituye silenciosamente una vía por otra.

## Propuesta congelable de un caso; sin ejecución

Usar la candidata histórica A3 y exactamente su solicitud/contexto archivados,
identificados por `receipt` y `sha256` en
`2026-10-28-agent-assisted-repair/supplied-critiques-v1.json`. Comprobar el hash
antes de leerlos y registrar una nueva revisión del asistente sin inyectar la
tarjeta histórica de críticas. A3 ya está expuesto: esto solo ilustraría el
procedimiento, no mediría descubrimiento independiente de errores ni mejora
general. No generar otra candidata ni seleccionar fuentes nuevas.

Presupuesto propuesto, pendiente de aprobación: una revisión del asistente,
como máximo una llamada de corrección al Qwen14B local existente, 768 tokens,
50 segundos por llamada; como máximo un calentamiento técnico de un token y
cinco minutos globales, incluida preparación y limpieza. Sin llamada de
autocrítica ni segunda reparación. Si no hay defecto justificado, cero llamadas
de corrección. Disponibilidad GPU comprobada de nuevo antes de cualquier carga;
solo procesos propios. El contraste posterior del asistente se registra por
separado y no se contabiliza como una llamada del corrector local.

No se ejecutó este presupuesto. No se abrió otra campaña o modelo.

## Evidencia y revisión de esta entrega

Se contrastó esta descripción con los métodos actuales y ambos informes:
`2026-10-28-review-repair/report.md` y
`2026-10-28-agent-assisted-repair/report.md`. El primero documenta autocrítica
del 14B sin mejora clara; el segundo, críticas aportadas por el asistente con
dos defectos objetivo corregidos y dos resultados parciales en cuatro casos
expuestos. Ese resultado no prueba una solución general ni revisión autónoma.

La omisión procedimental y la capacidad limitada de un revisor particular son
cuestiones distintas. Una revisión previa puede fallar, pero debe aplicarse y
registrarse si se pretende afirmar que una candidata pasó por ese recorrido.
Esta entrega no afirma que una segunda pasada encuentre todos los errores.
Se revisaron el alcance, las atribuciones de revisión y los límites de la
evidencia; no se añadieron aprobaciones retrospectivas. Solo cambió este
documento: no corresponde repetir pruebas de código ni inferencias.
