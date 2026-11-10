# Iteración asistida ejecutada; parada por falta de mejora sustantiva

28-10-2026. **Se ejecutaron tres correcciones completas y el asistente revisó
cada una antes de continuar. No se obtuvo una respuesta que cumpla el criterio
de este caso.** Tras mejoras parciales, las dos últimas iteraciones no redujeron
los defectos sustantivos; se aplicó esa condición de parada expresamente
autorizada. No se agotaron seis llamadas por agotarlas.

[Pregunta, inicial, cada crítica y cada versión íntegra — móvil](transcript-mobile.html)
· [Transcripción íntegra en Markdown](transcript-full.md)
· [Lectura final y rectificación del revisor](final-read-and-reviewer-correction.md)
· [Candidata003 de trabajo, NO aprobada](retained-working-candidate.md).

## Resultado de contenido

Pregunta conservada: «¿Para qué sirve mantener trazabilidad entre necesidades,
requisitos y pruebas? Explica cómo la usarías, con un ejemplo hipotético sencillo,
para analizar qué revisar si cambia una necesidad del cliente, y qué no permite
concluir por sí sola».

La inicial permanece intacta. La entrada a la nueva corrección fue TODO el
resultado parcial de recovery-001, marcado `length`, no una supuesta versión
completa. Se mantuvieron las mismas cinco fuentes íntegras y su solicitud
original, sin repetir búsqueda, seleccionar IDs a mano o añadir contexto.
Se revalidó el corpus v2 completo habilitado, índice existente `build=False`,
encoder CPU y fingerprint v2.1. No hay otra candidata inicial, A3, campaña o modelo.

El asistente releyó pregunta, inicial, parcial histórico y fuentes completas
antes de corregir; después leyó cada salida COMPLETA contra las mismas fuentes.
Críticas con afirmación concreta, explicación y testigos literales validados
en CPU ANTES de cada llamada. Sin autocrítica14B, respuesta académica completa
prefabricada o veredicto autónomo local.

| Versión de esta continuación | Terminación | Resultado de la revisión |
|---|---|---|
|001|stop,708tokens,44,594s|Niega garantía de ausencia de inconsistencias y retira exigencia de origen directo. Mantiene independencia incondicional y omite condiciones relevantes. Pierde el límite útil sobre corrección/cobertura de enlaces.|
|002|stop,761tokens,48,969s|Mantiene los defectos y añade una salvedad sin integrarla al cuerpo. Usa literalmente `[fragment_id]` como cita. No reduce los grupos sustantivos pendientes.|
|003|stop,679tokens,43,343s|Usa IDs reales y elimina notas duplicadas/bibliografía. Conserva los defectos sustantivos. Segunda iteración consecutiva sin reducción: parada.|

Quedan **dos grupos inequívocos**: independencia como necesidad sin «cuando sea
posible» y confusión entre calidad individual/corrección de traza; omisiones
de corrección/cobertura no garantizadas, excepción NASA de auto-derivados
aceptados con conformidad superior y retorno prueba→requisito útil al ejemplo.
NASA142 (impresa132) y Procedimiento11 están presentes: no son fallos por falta
de recuperación, tablas o GPU. Un ID correcto junto a una frase no la respalda:
003 cita NASA pero no conserva su modalidad.

**Rectificación del asistente:** la crítica sobre efectos indirectos era
demasiado categórica. La lectura completa permite entender «no se derivan
directamente» como ausencia de deducción automática. Se rebaja a ambigüedad,
no contradicción inequívoca. Los recuentos provisionales de críticas/decisiones
se conservan; recalibrados sin esa objeción, quedan dos grupos en001, dos en002
y dos en003. La condición de parada sigue cumplida. [Justificación y fuentes](final-read-and-reviewer-correction.md).

Los ejemplos ficticios de pacientes/citas médicas son coherentes y se admiten.
No se evalúa al alumno. No se elimina una excepción por concisión ni se exige
que todo detalle NASA sea obligación universal de la asignatura. No se cuenta
un cambio de palabra como corrección conceptual.003 se conserva como trabajo
con mejor presentación entre las regeneradas, sin superioridad académica global
ni aprobación. No existe una respuesta final local adecuada que entregar.

## Perfil de corrección implementado

Se implementó **`repair-expanded/v1`, optativo y offline**, sobre los puertos y
worker existentes. [Contrato sucesor limitado](../../../../specs/012-conversational-course-study/contracts/expanded-assisted-repair.md).

| Consumidor | Perfil expandido | Perfil histórico |
|---|---|---|
|Tipos y constraints|RepairGenerationRequest, hasta2048tokens/180000ms|Lab768/50000; ordinario sin cambios|
|Serialización/capacidad|Opt-in explícito de proveedor; budget_profile en frame y confirmación worker|Sin flag, no se concede ampliación|
|Validación worker|Validador puro compartido; exige opt-in y rechaza exceso/perfil desconocido|768/50000 como antes|
|Deadline exterior|call aplica180s o resto global; lectura180+2s; rechazo tardío/cancelación|Derivado del deadline histórico|
|Texto/historial/recibo|Tipo exclusivo16000caracteres; rechazo de exceso sin clipping; pipe262144bytes|GenerationMessage4000; DiagnosticStudy4000 intactos|
|Fuentes y presentación|Lista visible del host, IDs internos y evidencia íntegra, renderer offline inerte sin recorte|UI habitual/leases sin ampliar|
|Contabilidad|Presupuesto compartido; crítica y decisión del asistente entre llamadas|Ningún cupo histórico renovado|

Archivos de implementación: lab_request.py, cached_transformers.py,
gpu_worker.py, review_repair.py y nuevo generation_limits.py, más
tests/course_dialogue/test_expanded_repair.py. Copias anteriores de los cuatro
archivos existentes en [before/](before/). No se modificó GenerationPort,
DiagnosticStudy.turn, UI de Materiales, LaboratoryConversation ni rutas de
participante. Este perfil no pasa por el workflow histórico de200s: acepta
etapas de reparación con crítica suministrada, y rechaza autocrítica/draft para
evitar una ampliación accidental del workflow. El contexto worker sigue7000tokens,
con rechazo explícito si excede; no se trunca silenciosamente.

Mejoras CPU posteriores a las tres llamadas medidas: índice de fuentes real
`source_index` en la solicitud expandida, instrucción que excluye el marcador
literal `[fragment_id]`, guard de capacidad de recibo y rechazo expreso de la
vía de autocrítica. Corrigen límites de transporte/uso del perfil observados;
no se les atribuyen resultados GPU retrospectivos ni se inicia otra llamada
después de la parada. El código usado en las llamadas está conservado en
[executed-code/](executed-code/); código final y pruebas quedan hasheados al cierre.
En las llamadas001/002 los IDs ya estaban en los testigos de crítica; en003 se
enumeraron expresamente. Esto mejoró formato y no solucionó la semántica.

Las fuentes visibles las construye el host desde la procedencia comprobada:
[visible-sources-host.json](visible-sources-host.json). La transcripción conserva
incluso las listas/referencias defectuosas generadas; no se corrigen a escondidas.
[Integridad estructural de referencias](reference-integrity.json) no concede
respaldo semántico. Evidencia/pregunta/candidata/crítica/historial siguen siendo
datos no confiables; artefacto con escape, CSP sin scripts y texto íntegro.

## Pruebas y alcance verificado

**96 pruebas CPU pasaron antes de inferir**, en capacidad exacta2048/180000,
rechazo fuera de capacidad, opt-in, serialización íntegra de texto largo,
validación del frame compartida con worker, deadline exterior180s, cancelación,
timeout, salida excesiva y regresión de perfiles históricos. [Log previo](tests-final.log).

Después de las mejoras concretas de metadatos/guard, **109 pruebas correctas**
en5,44s, con una advertencia Starlette/httpx preexistente:
[tests-delivery.log](tests-delivery.log). Ruff y Black correctos. No se presenta
una suite CPU como prueba de corrección académica. No se repite build/UI sin
cambios ni se instalan dependencias para silenciar advertencias.

Comando de validación final:

```text
.venv\Scripts\python.exe -m pytest tests/course_dialogue/test_expanded_repair.py tests/course_dialogue/test_cached_adapter.py tests/course_dialogue/test_output_budget_contract.py tests/course_dialogue/test_review_repair.py tests/unit/test_study_lab.py tests/course_dialogue/test_scope_control_transport.py tests/course_dialogue/test_study_preparation_recovery.py tests/course_dialogue/test_generation_observability.py -q --basetemp docs/audits/2026-10-28-new-study-assistant-review/iteration-002/pytest-temp-004
```

Invocación real, posterior a esas pruebas iniciales:

```text
.venv\Scripts\python.exe -X utf8 docs/audits/2026-10-28-new-study-assistant-review/iteration-002/invoke_loop.py
```

El runner exige los recibos/decisiones externos del asistente; no los produce
el14B ni concede permiso a partir de contenido académico. Las decisiones son
datos de este diagnóstico autorizado, no una API de producto o autoridad docente.

## Presupuesto y GPU

Nuevo presupuesto autorizado:30min desde PRIMER preflight, máximo6correcciones,
hasta2048tokens/180s por llamada; cargas/warmups aparte dentro del mismo reloj.
[Primer preflight](first-preflight.json):28-10-2026 **14:43:55 Europe/Madrid**,
QPC1177007,7743074; deadline1178807,7743074. Incluye preparación de código/pruebas.
No reproducción de inferencia ni reinicio del monotonic. Se propagó a CallBudget
y timeout global. [Protocolo/inputs congelados](protocol.json), [congelación](input-freeze.json).

Consumido: **tres correcciones, una carga y un calentamiento**. Todasstop;
2148tokens nuevos totales,136,906s de generación. Worker listo21,062s.
Hasta limpieza797,132s (13min17s) desde primerpreflight, incluido tiempo de
revisión del asistente mientras el worker propio estaba disponible.
Construcción de transcripción1120,288s desde el mismo origen; sello final
registra la duración de entrega, dentro1800s. El tiempo de revisión del asistente
no se vende como latencia de un revisor autónomo local.

Contabilidad acumulada conservada: inicial1llamada + recuperación7681llamada
incompleta + esta continuación3llamadas =5llamadas académicas;3calentamientos
completados, cada continuación con su autorización. El fallo histórico del
testigo sigue contando cero llamadas al corrector. El reloj no acreditado del
primer ensayo sigue sin acreditarse retrospectivamente por este plazo nuevo.

Mismo Qwen2.5-14B-Instruct NF4 local y snapshot
`cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`; doble cuantización/bfloat16,
sin offload alternativo ni nuevo modelo. Plantilla SHA256
`2e2d2512cfe46af53dc1eed45368ecaab26ac4461c480e6b69fe571cf0ceaa75`.
Worker confirma capacidad expandida y registra configuración efectiva de cada
llamada (`audit_config`); do_sampleFalse explícito, advertencias originales
conservadas. No descargar/instalar/nube.

GPU: primerpreflight1558/32607MiB,0%; antes de carga1567MiB/0%.
Holgura comprobada para el pico14B observado, sin umbral fijo2000MiB como
prueba de actividad ajena.206muestras, pico18482MiB/100%; muestra de cierre
1558MiB/4%, comprobación posterior1558MiB/0%. Memoria reservada no prueba uso
ajeno; rendimiento no es un SLA ni una comparación de modelos.
[Métricas](metrics.json) · [muestras](gpu-samples.json).

Worker55784 y descendientes60864/51284 detenidos, salida0,
[árbol cerrado](worker-cleanup.json). No se tocó ComfyUI, documental8022 u otro
proceso ajeno, no servidor propio ni listener. El primer formateo Black con
paralelismo quedó esperando; se detuvieron solo sus PID propios comprobados y
se ejecutó `--workers 1`. No cambió el reloj/cupo o contenido semántico.

## Preservación, límites y cierre

[Comprobaciones finales](receipt-checks.json): entregas históricas y recovery-001
intactas, fuentes/manifiesto/extracciones rehasheados sin cambios, inputfreeze
exacto, spec/plan/tasks y recuperación/DiagnosticStudy sin cambios. Las cinco
páginas se leyeron también en sus renders originales existentes; NASA142 es
página impresa132. No reindexación, migraciones, commits, Reset, alteración de
reserva/protocolos o regeneración de estados/IDs. Contrato nuevo separado.

Participante/gates T090/T150/G2/SC001 cerrados; unverified/not_assessed,
publicationfalse/participantnull. E2/Feature012 no se cierran. Sin notas,
rúbricas, evaluación del alumno, examen, voz o web del producto. No se amplían
consentimiento, acceso, vigencia, cancelación o leases de producto.

**Qué funciona:** el perfil de capacidad, el transporte/recibos, una respuesta
completa por llamada, críticas asistidas con testigos, preservación, parada por
falta de mejora y limpieza. **Qué no quedó resuelto:** integrar sustantivamente
esas críticas en esta respuesta local. El límite ya no es768tokens: las tres
salidas usaron menos de800 de2048, todas constop.

Para automatizar esta revisión todavía hace falta un revisor que detecte y
justifique esos defectos con fiabilidad y un corrector que los incorpore sin
perder condiciones; ni IDs válidos ni JSON ni más tokens prueban esa capacidad.
Este resultado no demuestra incapacidad universal del14B ni transferencia.

La condición real de parada se ha cumplido y el alcance termina aquí. No otra
llamada, modelo/campaña o fase automática; no reintento del reporte interchat
rechazado. El coordinador puede consultar directamente estos artefactos.
