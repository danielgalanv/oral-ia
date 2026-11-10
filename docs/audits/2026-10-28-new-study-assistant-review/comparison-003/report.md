# Reparación localizada frente a generación limpia: resultado mixto

28-10-2026. **La reparación localizada produjo una respuesta que cumple los
criterios mínimos del caso de trazabilidad, tras revisión completa del asistente.**
También corrigió la primera pregunta nueva. En la segunda pregunta nueva,
ninguna rama logró una salida adecuada. No hay ganador general ni revisión
autónoma local acreditada.

[Respuesta íntegra revisada, sin jerga técnica](final-answer.md) ·
[Móvil: respuesta destacada e historial íntegro](transcript-mobile.html) ·
[Markdown íntegro: preguntas, críticas, requests, respuestas y fuentes](transcript-full.md).

## Decisión por estrategia

|Caso|Reparación localizada L|Generación limpia R|
|---|---|---|
|Trazabilidad, caso expuesto|L2 adecuada para revisión docente: corrige modalidad/objeto de revisión y retira atribuciones erróneas.|R2 no adecuada: conserva garantías de satisfacción/alineación que contradice después.|
|T1 nueva: meta de usabilidad frente a requisito verificable|Corrige la garantía de que formular una medida demuestra satisfacción de una meta.|Mantiene la inferencia de cumplimiento garantizado pese a cambiar el ejemplo.|
|T2 nueva: ambigüedad de «buscar» sin prefijar diseño|Conserva la frase defectuosa y añade una salvedad contraria; no integra la corrección.|Aclara el alcance, pero añade garantías de óptimo técnico/satisfacción y una regla demasiado general sobre decisiones del cliente.|

L fue útil con críticas focalizadas en el caso expuesto y T1. Eso no demuestra
superioridad universal: L falla en T2 y R corrige allí parte del problema,
introduciendo otros. No se premió longitud, cambio de ejemplo o mera presencia
de palabras correctas. [Contraste expuesto](review-exposed-final.md),
[T1](T1-review-final.md), [T2](T2-review-final.md).

La respuesta elegida conserva el ejemplo médico hipotético, explica relaciones
necesidad/requisito/prueba y qué revisar ante un cambio. Elimina la obligación
incondicional de revisión independiente de calidad individual atribuida a NASA;
distingue comprobar trazas de calidad de cada requisito. Su párrafo de impactos
admite una lectura limitada por «automáticamente»: queda como ambigüedad de
redacción, no falsedad demostrada. No detecté error sustantivo en la lectura
completa con el criterio mínimo congelado. Esa revisión permite **revisión
docente de este caso**, no aceptación humana, supported ni ausencia universal
de errores. La respuesta se muestra EXACTA, sin reescritura académica del asistente.

## Qué se comparó y qué se depuró

Pregunta original completa en la entrega destacada. Obligaciones congeladas:
explicar utilidad, aplicar un cambio de necesidad con ejemplo coherente y
explicar un límite relevante de los enlaces. No se exige exhaustividad NASA.
[Criterios e incidencias tipificadas](criteria.json).

La crítica inicial nueva contiene **un solo error prioritario**: obligación
incondicional de revisión independiente y confusión de su objeto (traza frente
a calidad individual). Se retiraron las exigencias anteriores de excepción
auto-derivada obligatoria, exhaustividad y falsedad demostrada de impactos.
La excepción solo sería necesaria si se afirmara origen directo universal.
No se pidieron IDs al modelo; fuentes consultadas construidas por el host.
Las críticas históricas y iteration-002/parada siguen intactas: esta depuración
es una decisión prospectiva, no aprobación retrospectiva.

Misma pregunta, mismas cinco páginas COMPLETAS y orden original, mismo Qwen2.5-14B
NF4/snapshot/configuración y límites2048tokens/180s en ambas ramas. **L** recibe
borrador003 completo y crítica fundada. **R** recibe pregunta/fuentes/criterios
y advertencia conceptual equivalente, sin borrador defectuoso, citas de ese
borrador ni historial. No se filtró una respuesta académica prefabricada.
[Requests congelados L](exposed-L-request.json) y [R](exposed-R-request.json),
[validación CPU de serialización](cpu-serialization.json).

Primero R1→L1; ambas salidas congeladas antes de evaluar. L1 corrigió el error
conceptual pero conservó una atribución errónea; R1 añadió una garantía de
resultado. Segunda y última llamada simétrica por rama, L2→R2, con críticas
actualizadas. R siguió sin recibir textos defectuosos. [Primera revisión](review-exposed-first.md),
[pureza de R y validación CPU de segundos requests](second-cpu-validation.json).

Ramas conocidas y orden alternado declarado, no ciego/aleatorio. Inputs distintos:
L1/L2,3236/3302tokens; R1/R2,2282/2347. El mismo techo no implica el mismo trabajo.
El estudio compara recorridos asistidos con crítica depurada, no aísla
estadísticamente una variable ni demuestra transferencia independiente.

## Dos preguntas nuevas y sus límites

[Preguntas T1/T2](transfer-questions.json) fijadas ANTES de ver los resultados
del caso expuesto. Son otros conceptos: verificabilidad de metas y aclaración
de ambigüedad, no retoques cosméticos de A3/A4/B1/B2 ni reserva. Se activaron
al observar mejora conceptual clara en L, y sus iniciales comunes se revisaron
antes de decidir correcciones.

Ambas iniciales tenían un defecto preciso fundamentado: garantía de cumplimiento
en T1 y clasificación de posible alcance funcional como diseño innecesario en
T2. No se penalizaron cifras ficticias2/3minutos o campos del ejemplo por no
aparecer literalmente. Tampoco se exigió un protocolo de usabilidad exhaustivo,
todos los filtros o toda técnica de elicitación. [Revisiones iniciales T1](T1-review-initial.md)
y [T2](T2-review-initial.md). Cada una tuvo inicial+L+R, mismo máximo por caso.
No hubo techo de inicial ya adecuada que justificara omitir artificialmente
una reparación; tampoco se inventó un segundo defecto para consumir más llamadas.

Cada pregunta tuvo una sola recuperación densa real desde corpusv2 completo,
encoder CPU, índice existente `build=False`, sin seleccionar IDs. El mismo
contexto íntegro se compartió dentro de cada par. T1:cinco páginas/4766caracteres,
sin omisiones de empaquetado. T2:cinco páginas/5937caracteres y siete omisiones
de página completa, incluida Requisitos13. No se añadió esa página manualmente:
NASA64/Requisitos5 aportaban las premisas pertinentes. No se atribuyen los
errores a tablas o a aquella omisión por defecto. Tratamiento general de tablas
sigue limitado. [Contexto T1](T1-context.json), [T2](T2-context.json).

Se leyeron completos todos los contextos y salidas; también se inspeccionaron
los renders originales existentes de NASA64, Requisitos5 y36 para comprobar
modalidades, restricciones y tabla de notaciones. No se cambió extracción.
No se agregaron grupos heterogéneos como una sola métrica de calidad.

## Pruebas, ejecución y recursos

Solo se escribieron archivos nuevos exclusivos de este diagnóstico. **Cero
cambios de código de producto/defaults/UI**, sin otro framework, modelo o
dependencias. Se reutilizan RepairGenerationRequest/repair-expanded/v1,
GenerationPort, ReviewRepairGenerationAdapter.call, CallBudget, Retrieval,
DiagnosticStudy para vigencia/pertenencia y cached_provider/OwnedWorkerTree.
La rama R y las iniciales son generación académica nueva sobre ese mismo
transporte offline; su papel real figura en cada job, no se simulan reparaciones.

Preflight CPU antes de cargar: tipos/perfil, presupuesto exacto, serialización
real con pipe fixture sin modelo, fuentes completas sin clipping, crítica con
testigos literales, ausencia de borrador/historial en R y hashes congelados.
Las críticas posteriores pasaron parse_review antes de enviar. Guardas de
capacidad/deadline/recibo existentes siguen activas. No se repitieron suites109
de la implementación anterior sin cambios; se comprobó que su código final
permanece idéntico. [Pruebas/preservación focales](receipt-checks.json).

Primer intento CPU de preparación falló al importar el fixture `tests` por
sys.path del script independiente. Se preservó `prepare-first.py`, se añadió
la raíz del workspace al import local y se reprodujo en CPU: cero cargas,
calentamientos o llamadas en ese fallo. No se reinició el reloj.

Nuevo plazo desde primerpreflight **16:18:58 Europe/Madrid**, QPC1182710,3905046,
deadline1184510,3905046;30min incluidos preparación, revisión y limpieza.
Máximo10llamadas académicas, hasta2048tokens/180s cada una; cargas/warmups aparte
dentro del mismo reloj. Consumido exactamente10, distribuidas4expuesto+3T1+3T2,
porque ambas iniciales nuevas tenían incidencias precisas. Una carga y un
calentamiento técnico de1token. No llamada11 ni fase posterior.

**10/10stop**,4901tokens de salida,309,152s de generación total. Nada se recortó
ni se completó manualmente. Ciclo GPU hasta limpieza1063,734s (17min44s);
construcción de entrega1260,515s desde el mismo preflight. Sello final registra
duración total de entrega dentro1800s. No se usa esta medición para subsanar
relojes históricos no acreditados. [Métricas y todos los costes de entrada](metrics.json).

Modelo local único Qwen2.5-14B-Instruct NF4, snapshot
`cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`; misma plantilla, do_sampleFalse
explícito y configuración efectiva por llamada conservada. Sin downloads,
instalaciones, nube, offload alternativo ni reindexación.

GPU antes1562/32607MiB,0%; antes de carga1567MiB/0%. Holgura verificada para
el pico observado, sin guard2000MiB como prueba de actividad ajena.402muestras,
pico20820MiB/100%; cierre1561MiB/0%. [Muestras](gpu-samples.json).
Memoria reservada no demuestra concurrencia ajena; no se culpa a GPU de calidad.
Worker56500 y descendientes100748/100188 detenidos, salida0,
[árbol propio cerrado](worker-cleanup.json). Sin tocar ComfyUI, documental8022
u otros procesos; sin servidores propios/listeners.

## Cierre

Fuentes, manifiestos, extracciones, índices/identidad, reserva, protocolos y
evidencia previa conservados; sin commits/Reset/migraciones. Requests/respuestas,
críticas y fuentes exactas íntegros en la transcripción y recibos. Renderer
inerte con escape/CSP sin scripts; fuentes/críticas/candidatas son datos,
nunca instrucciones ejecutadas. No evaluación de alumnos, notas/rúbricas,
examen, voz o web del producto.

Salida siempre unverified/not_assessed, publicationfalse/participantnull.
La revisión sustantiva sigue siendo del asistente, no una capacidad local
autónoma. T090/T150/G2/SC001/participante cerrados; E2/Feature012 no cerradas.
No reintento interchat rechazado: el coordinador lee estos archivos.

Decisión útil: conservar L2 de trazabilidad y L de T1 como respuestas revisadas
de estos casos; registrar T2 y las salidas R no adecuadas sin ganador artificial.
La falta pendiente para automatizar incluye detectar errores con fiabilidad
y lograr que el corrector integre la crítica en el cuerpo sin introducir
garantías nuevas. No se anuncia otro ensayo automático ni superioridad general.
