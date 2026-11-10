# Reparación ejecutada y revisada: salida incompleta, sin aprobación

28-10-2026. Se completó la invocación pendiente y la revisión del asistente.
**La única reparación real terminó `length` a768tokens**; no produjo una
segunda versión completa. El texto recibido incorpora dos avances parciales
de la objeción original, pero introduce problemas de condiciones y garantías.
No se repite la llamada para lograr que apruebe y no se anuncia demo correcta.

[Transcripción íntegra: pregunta, antes, revisión, salida nueva y fuentes](transcript-full.md)
· [Lectura móvil inerte](transcript-mobile.html)
· [Contraste sustantivo final](review-after.md).

## Entradas y recorrido

Se conserva la pregunta nueva de trazabilidad entre necesidades, requisitos y
pruebas, con ejemplo de cambio y límites de lo que permite concluir. No se
genera otra candidata ni se seleccionan otras fuentes. Se reutilizan exactamente
la [solicitud original](../request.json), [respuesta inicial completa](../initial.json),
[contexto recuperado](../retrieval.json) y [crítica corregida solo en literalidad](../assistant-review-cpu-corrected.json).
La [crítica rechazada](../assistant-review.json) y todos los recibos históricos
permanecen intactos. El [informe anterior](../report.md) describe aquel estado,
no el resultado actualizado de esta continuación.

Antes de cargar: comprobación CPU de todos los hashes de la entrega anterior,
testigos con parse_review, pertenencia/texto/hash/página de cada pasaje vigente,
documento/versión exactos de cada evidencia, terminación de la candidata inicial
y límites768tokens/50.000ms. Se construyó y congeló la
[solicitud de reparación](repair-request-cpu-frozen.json) y se comprobó su
igualdad con la solicitud enviada. [Precondiciones CPU](cpu-preconditions.json).
No se repitió la búsqueda ni se añadió evidencia.

Retrieval v2.1 `build=False` solo para revalidar corpus y pertenencia al índice
existentes; encoder CPU, identidad
`c2756d3c78fd3dd9237b5a6aaa5fe63513a38747bf8894635bdb9e44143cf51a`.
El contexto sigue siendo el resultado denso experimental original de cinco
páginas/5467caracteres, con corpus v2 completo habilitado y sin omisiones de
empaquetado registradas. No promoción del ranking ni garantía sobre tablas.

Una invocación mínima de `repair_with_supplied_review`, usando GenerationPort,
cached_provider y OwnedWorkerTree existentes. Qwen2.5-14B-Instruct NF4 local,
snapshot `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`, preparación180s explícita,
misma plantilla/instrucción de reparación existente. Runtime/quantización
efectivos en [worker.json](worker.json), sin descargas, instalaciones, modelos,
offload o prompts alternativos. No cambios de producto o framework nuevo.

## Resultado y contraste completo de lo recibido

La respuesta inicial completa y las cinco fuentes se releyeron antes de
la corrección. Después el asistente leyó TODO el texto devuelto, incluida su
terminación cortada. No se pidió autocrítica ni revisión posterior al14B.

- **Avances parciales:** añade el recorrido inverso requisito→necesidad y
  declara que la trazabilidad no garantiza corrección/cobertura del trazado.
  Son cambios conceptuales con respaldo en NASA142, no solo otra palabra.
- **Persistencias:** no explica el retorno prueba→requisito; mantiene el matiz
  insuficiente sobre efectos indirectos; la lista de fuentes comienza pero
  queda truncada. Se conserva el ejemplo hipotético, que sigue siendo admisible.
- **Tres hallazgos nuevos localizados:** atribuye al recorrido inverso asegurar
  ausencia de redundancias/inconsistencias; exige universalmente una necesidad
  de origen omitiendo la excepción de requisitos auto-derivados aceptados de
  NASA142; convierte «independently if possible» en necesidad incondicional y
  confunde corrección/cobertura de la traza con precisión/calidad individual.
  [Frases exactas, testigos y justificación](review-after.md).
- **Críticas equivocadas:** ninguna objeción semántica original resultó
  demostrada como errónea; el testigo mal transcrito fue un error mecánico
  previo del asistente y permanece reconocido. No se da por validada la crítica
  por el mero hecho de pasar parse_review.

Se trata de una objeción original de cobertura con dos componentes y dos avances
parciales observados, **cero reparaciones completas aceptables**. Los tres nuevos
hallazgos no constituyen una tasa general de error ni una evaluación del alumno.
No se compara una supuesta versión completa reconstruida desde el fragmento.

El corte fue por **límite de tokens**, no por alcanzar50segundos:3003tokens de
entrada,768de salida,48,078s, `ok=false`, `finish_reason=length`. Final exacto:
«Fuente: 6 - Procedimiento requisitos». No se completa manualmente esa fuente.
No hay fallo de validación de testigos en esta continuación.

Importante para leer [repair.json](repair.json): su `outcome` exterior contiene
el texto INICIAL retenido con estado `repair_incomplete_initial_retained`.
La salida nueva incompleta está íntegra en `trace.calls[0].outcome` y en
[recibo bruto de la llamada](016fc5459561441da2495970c31d5d1e-result.json).
Retener la inicial no implica que sea correcta ni que el corrector no cambiara
nada. La transcripción muestra las dos salidas reales y su distinta terminación.

## Presupuesto, recursos y limpieza

Autorización renovada del usuario, transmitida por el coordinador: nueva carga
y calentamiento necesarios para completar esta reparación; no GPU indefinida.
Reloj de600s persistido en el **primer preflight**, antes de preparar Python:
[first-preflight.json](first-preflight.json),28-10-2026 **14:30:17 Europe/Madrid**.
Inicio QPC1176189,4541006; deadline1176789,4541006. Se propagó al timeout global
y CallBudget; no hubo reproducción ni reinicio. La comprobación inicial de
compatibilidad del monotonic pasó. [Reloj y autorización](authorization-and-clock.json).

Una carga, un calentamiento técnico de1token y una llamada de reparación.
Preparación efectiva20,719s; ciclo hasta limpieza118,546s desde primer
preflight. Construcción de entrega247,327s desde ese mismo origen, dentro600s.
Contabilidad histórica intacta: total acumulado de las dos etapas, dos llamadas
académicas (generación inicial+reparación) y dos calentamientos completados,
el segundo autorizado expresamente ahora. El intento histórico de cita rechazada
sigue contando cero llamadas de reparación. Esta continuación no subsana el
reloj global anterior, que sigue sin acreditación extremo a extremo.

GPU inicial1558/32607MiB,0%; misma disponibilidad antes de cargar. Se comprobó
holgura suficiente respecto al pico14B observado, sin guard fijo2000MiB como
prueba de uso ajeno.36muestras: pico16016MiB y81%; final1558MiB/0%.
[Métricas](metrics.json) · [Muestras](gpu-samples.json).
Memoria reservada no demuestra concurrencia ajena; estos datos no son un SLA.

Worker1324 y descendientes85544/95416 detenidos, salida0,
[árbol propio cerrado](worker-cleanup.json). Confirmación posterior sin esos
PID y GPU1558MiB/0%. No se tocó ComfyUI, documental8022 ni procesos ajenos;
no servidor propio, UI adicional o listener nuevos.

## Evidencia y estado

[Comprobaciones finales](receipt-checks.json): hashes de toda la entrega
histórica intactos; originales/extracciones/manifiesto rehasheados intactos;
código de producto y spec/plan/tasks preservados; solicitud/fuentes/crítica
efectivamente enviadas idénticas a las congeladas; exactamente una llamada;
árbol cerrado y plazo vigente. Validación focal CPU, sin repetir suites o
builds no afectados. Las24pruebas previas no se presentan como pruebas nuevas.

La transcripción móvil contiene pregunta, inicial, revisión previa, crítica,
TODO el resultado nuevo marcado incompleto, contraste y cinco fuentes íntegras.
Escape HTML/CSP sin scripts; contenido académico inerte. Solo inspección docente
offline autorizada, `unverified`/`not_assessed`, `participant_display=null`,
`publication_allowed=false`. Sin notas/rúbricas o evaluación del alumno.
Sin alteración de consentimiento, acceso, vigencia, cancelación, cierre,
LaboratoryConversation, corpus, reserva, gates, commits o Reset.

La revisión sustantiva sigue siendo del asistente; no se ha resuelto un
verificador autónomo local. E2/Feature012 y los gates mantienen su estado.
No se reintenta el envío interchat rechazado ni se solicita permiso para ese
reporte: el coordinador puede leer esta entrega en el workspace.

La causa operativa pendiente es concreta: conservar casi toda la respuesta y
añadir la crítica excedió768tokens. En cualquier futura decisión de diseño
habría que comprobar una reparación más concisa bajo un protocolo nuevo, sin
usar este truncamiento como éxito ni reiterar este caso hasta aprobar.
**No se ejecuta esa fase ni otra llamada ahora.**
