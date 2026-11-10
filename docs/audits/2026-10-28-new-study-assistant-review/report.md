# Resultado parcial: candidata nueva revisada, corrección no ejecutada

28-10-2026. Se generó **una candidata nueva completa** sobre trazabilidad desde
RAG real y el asistente la revisó antes de entregarla. La revisión identifica
una omisión conceptual con fuentes. **No se completó la reparación/contraste
de dos versiones**: una cita del asistente no conservaba un guion de la
extracción y el validador la rechazó antes de llamar al corrector. No hay demo
correcta anunciada, segunda candidata ni aprobación semántica.

[Transcripción íntegra, con fuentes](transcript-full.md) ·
[Lectura móvil estática](transcript-mobile.html) ·
[Revisión previa](review-before.md) · [Contraste final y límites](review-after.md).

## Qué se ejecutó

Pregunta: «¿Para qué sirve mantener trazabilidad entre necesidades, requisitos
y pruebas? Explica cómo la usarías, con un ejemplo hipotético sencillo, para
analizar qué revisar si cambia una necesidad del cliente, y qué no permite
concluir por sí sola». Es un objetivo nuevo de trazabilidad y sus límites;
no reproduce A3/A4/B1/B2, no continúa una respuesta histórica ni repite la
campaña retirada. No es transferencia demostrada o experimento ciego: el
asistente conoce el proyecto.

Se congelaron propósito/criterios/instrucción en [protocolo](protocol.json),
[solicitud](request.json), [recuperación íntegra](retrieval.json) y
[hashes previos](pre-generation-freeze.json). La configuración efectiva y la
plantilla completa se registraron en [worker.json](worker.json) antes de
enviar la petición académica. La candidata original completa/bruto/transporte
están en [initial.json](initial.json), con [congelación aparte](initial-freeze.json).

Recorrido mínimo: Retrieval v2.1 existente `build=False`, corpus v2 completo
habilitado (117 páginas), encoder CPU, rama densa **experimental**, evidencia
comprobada por DiagnosticStudy, LabGenerationRequest y GenerationPort con
CachedTransformersGenerationAdapter, worker propio por pipes/OwnedWorkerTree.
Invocación exclusiva en [invoke.py](invoke.py); no framework nuevo ni código
de producto cambiado. No servidor o UI adicional, no sesión humana realizada.

Qwen2.5-14B-Instruct NF4, snapshot
`cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`; runtime existente
`D:\ai-toolkit\venv\Scripts\python.exe`, torch2.13.0+cu130/transformers5.5.3.
NF4 double quant/bfloat16, CUDA0, sin offload alternativo. Plantilla SHA256
`2e2d2512cfe46af53dc1eed45368ecaab26ac4461c480e6b69fe571cf0ceaa75`.
`do_sample=False` explícito en gpu_worker; el generation_config original y
su advertencia de flags permanecen registrados, no se confunden con el valor
informativo temperature0 del adaptador.

Una petición académica, 2098 tokens entrada/576 salida, **stop**, 36,891s.
Un calentamiento interno de un token. Cero autocríticas, cero llamadas de
reparación, cero segunda candidata. Máximos768tokens/50.000ms intactos.

## Hallazgo y fallo mecánico

El asistente leyó pregunta, texto íntegro y los cinco pasajes completos. No
recibió tarjetas históricas ni salida corregida/autocrítica del 14B como
entrada de revisión. La cadena necesidad→requisito→prueba y la aplicación al
cambio son útiles. La ficción de citas médicas pasadas es admisible.

Omisión fundada: no explica el recorrido inverso ni que disponer de enlaces
no prueba por sí solo corrección/cobertura de la traza. NASA142 exige
bidireccionalidad y evaluar que la traza sea correcta y atienda su requisito
superior. Además faltan fuentes enumeradas en la respuesta, aunque sí están
en el contexto. No se cuenta como error el mero uso de «asegurar» para un
propósito ni se inventan defectos para forzar reparación.

La [crítica original](assistant-review.json) se entregó a
`repair_with_supplied_review`. Su testigo decía «parent requirements» donde
el contexto extraído dice «parent require-\nments». La normalización admitida
solo cambia espacios. [Error íntegro](failure.json):
`foreign or nonliteral source witness`. No llegó al corrector y no existe
resultado reparado. La validación evitó transmitir una cita no literal.

La [corrección mecánica de la cita](assistant-review-cpu-corrected.json) se
reprodujo exclusivamente en CPU: [parse_review correcto](cpu-witness-check.log).
Se acorta el testigo a una subcadena literal sin cambiar la crítica semántica,
pregunta o fuentes. El original rechazado no se sobrescribe. **Validar la cita
no corrige la candidata ni valida semántica.** El worker ya había cerrado al
propagarse el error. Recargarlo consumiría un segundo calentamiento; no se
amplía ese cupo ni se crea una vía alternativa para eludirlo.

El asistente releyó la candidata completa y las mismas fuentes al cerrar.
La omisión persiste; no hay defectos corregidos acreditados ni versión nueva
que permita comparar pérdida de información o errores nuevos. La crítica
conceptual sigue fundada; el error demostrable del revisor fue la transcripción
del testigo. [Contraste final](review-after.md). No basta un contrato JSON ni
un cambio de palabras para declarar éxito.

## Fuentes, selección y preservación

Cinco páginas/5467caracteres: Procedimiento11, Requisitos13,
Procedimiento10, NASA142 y Requisitos20. El ranking se ejecutó sin selección
manual por ID, contexto fijo ni cambio de consulta para aprobar. Hay veinte
candidatos configurados y hasta cinco páginas/6000caracteres; el recibo guarda
los candidatos efectivos y `omitted_context=[]`. No hay pérdida por empaquetado
registrada en este caso. Que otra página no aparezca en el ranking no demuestra
ausencia del concepto en la asignatura.

El defecto señalado está respaldado por texto presente en NASA142: no se
atribuye a ranking, tablas o GPU. El tratamiento de tablas y ciertas estructuras
gráficas sigue limitado; algunas preguntas requieren consultar el original o
pueden carecer de evidencia suficiente. Esta muestra textual no resuelve esa
limitación ni acredita todo el corpus.

Fingerprint e índice existentes preservados:
`c2756d3c78fd3dd9237b5a6aaa5fe63513a38747bf8894635bdb9e44143cf51a`.
[Verificación](receipt-checks.json): originales/extracciones/manifiesto v2
rehasheados y sin cambios; solicitud/candidata/contexto congelados intactos;
código de producto y spec/plan/tasks intactos. Sin regeneración de IDs,
reindexación, migraciones, commits, Reset, eliminación de evidencia o reserva.

## Recursos, reloj y pruebas

Disponibilidad inicial comprobada:1560/32607MiB,0%. Antes de cargar:1560MiB/0%.
Se comprobó holgura concreta para el pico observado previamente del14B,
sin imponer2000MiB como umbral universal de competencia. Memoria reservada no
demuestra actividad ajena. Muestreo durante/después:93muestras, pico14047MiB
y59%, final1559MiB/0%. [Métricas](metrics.json), [muestras](gpu-samples.json).

Worker72440 y descendientes25952/80456 detenidos, salida0, árbol propio
cerrado: [recibo](worker-cleanup.json). No se tocaron ComfyUI, documental8022
ni otros procesos ajenos. Sin descargas, instalaciones o servicios nuevos.

Preparación efectiva del worker61,766s, dentro del máximo explícito180s.
La invocación registrada duró190,125s incluyendo encoder, generación,
espera de revisión y limpieza. **No es la duración global de la tarea**.
La primera preparación propia13:27:08 quedó sin recibo antes del protocolo;
se detuvo y se reprodujo con traza CPU, que localizó espera en imports de
Transformers. [Nota íntegra](preparation-note.md),
[consola de reproducción y fallo](console-recovery.log).

Limitación de cumplimiento del reloj: el `started` interno se creó de nuevo
en la reproducción; no se trasladó un monotonic original de la primera
preparación. Por tanto la frase de la nota preparatoria sobre «no renovar el
límite» expresa intención, no una garantía instrumentada. Se registra esta
desviación y no se usa190,125s para acreditar20min extremo a extremo. Solo se
consumió una petición y se detuvo el GPU tras el fallo, sin usar el tiempo
interno renovado para más llamadas. La preparación documental anterior a
13:27 tampoco tiene cronómetro propio. No se afirma una medición global exacta.

24 pruebas CPU del corrector/preflight correctas en2,51s,
[log](tests.log). Primer intento de tests falló en setup por temporal
predeterminado; se repitió con ruta exclusiva de workspace. La corrección
literal se validó después con CPU. No se repite build/UI ajeno al cambio ni
se presentan pruebas de contrato como validación académica.

## Estado y siguiente paso

Funciona en esta muestra: recuperación real, generación completa, congelación,
revisión sustantiva del asistente previa a entrega, rechazo de cita no literal
y cierre del árbol propio. No completado: corrección local y contraste real
antes/después. Ninguna capacidad de revisor autónomo local queda resuelta.

Inspección docente offline identificada, `unverified`/`not_assessed`,
`participant_display=null`, `publication_allowed=false`. Evidencia autorizada
para este reporte separada de memoria efímera producto. Fuentes/pregunta/
candidata/crítica son datos; HTML móvil usa escape y CSP sin scripts. No se
modifica LaboratoryConversation, consentimiento/acceso/retirada/cancelación o
cierre. No se abrió sesión adicional ni gate. T103/E2, T072/T077global y
Feature012 siguen abiertos; T090/T150/G2/SC001/participante cerrados.

Próximo paso concreto, sin ejecutarlo: validar en CPU todos los testigos antes
de mantener abierto el worker y conservar un deadline global desde el primer
arranque; con un presupuesto nuevo que autorice otro calentamiento, aplicar
una sola reparación a esta candidata/contexto congelados y revisar ambas
versiones completas. No regenerar la candidata ni iniciar otra campaña para
ocultar este resultado parcial.
