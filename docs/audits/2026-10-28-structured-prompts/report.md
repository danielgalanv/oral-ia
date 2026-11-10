# Perfiles estructurales implementados; corrección conceptual todavía fallida

28-10-2026. **Se implementó el renderer optativo por checkpoint/tarea y se
midió con el14B. La nueva estructura cambia la edición del texto, pero no
incorpora la corrección académica del caso expuesto.** Se cumplió la parada
autorizada: dos llamadas completas, sin ejecutar las preguntas nuevas.

[Antes/después completos y revisión — móvil](transcript-mobile.html) ·
[Transcripción íntegra, fuentes y requests](transcript-full.md) ·
[Contraste sustantivo](review-exposed.md). No hay salida final seleccionada
como adecuada ni síntesis académica posterior.

## Qué se implementó

Nuevo `model_prompt_profiles.py`: registro cerrado de cinco checkpoints locales,
constructor único de mensajes y perfiles de sampling. Nuevo
`StructuredGenerationRequest` en structured_request.py: tareas generate/review/
repair con pregunta, fuentes, borrador, observaciones falibles y obligaciones
separadas. `review_repair.repair_request(..., model_profile=...)` y el runner
usan el mismo constructor; cached_transformers lo renderiza y gpu_worker
reconstruye/valida el mismo frame. No basta cambiar una instrucción que el
runner no use. [Contrato](../../../specs/012-conversational-course-study/contracts/model-structured-prompts.md).

El system del host ordena contrastar las observaciones con fuentes, sustituir
o eliminar el error, ajustar frases dependientes y coherencia completa,
preservando lo correcto. Prohíbe conservar error y añadir su negación. No eleva
la crítica externa a autoridad: queda como datos falibles en el user, junto
con las fuentes. No respuesta patrón ni IDs/bibliografía a producir por el
modelo; procedencia visible del host. Generación y revisión tienen contratos
distintos; no se ejecutó autocrítica local como sustituto del asistente.

El user es un objeto de campos separados, sin JSON de corrección dentro de
pregunta_actual. JSON no se declara intrínsecamente mejor que XML: se prueba
ese contrato concreto. Escapes lossless de `< > [ ]` DENTRO de strings impiden
interpretar delimitadores nativos adversarios como control; json.loads recupera
los textos íntegros. Historial mostrado conserva roles user/assistant y contenido
como datos, con rechazo de roles privilegiados inyectados. No se clippea nada.
Tests comprueban los mensajes efectivos con pipes simulados, no solo strings.

No se modifican GenerationPort, defaults académicos, renderer UI habitual,
protocolos previos o gates. Se conserva perfil histórico768/50s y expanded2048/
180s/16000caracteres, input7000tokens con rechazo explícito, budgets, revalidación,
consentimiento/cancelación/cierre y árbol propio. La nueva ruta es optativa.

## Familias, identidad, tokenización y sampling

|Perfil registrado|Construcción y modo|Comprobación CPU|
|---|---|---|
|Qwen2.5 Instruct1.5/7/14B|Roles y plantilla local nativos; sin opciones thinking de Qwen3.|Equivalencia de tokenizaciones en los tres; ruta anterior ya coincidía.|
|Qwen3-8B non-thinking|enable_thinkingFalse explícito; nuevo perfil requiere sampling non-thinking registrado.|Equivalencia y modo explícito; sin pesos ni GPU de ese modelo.|
|Mistral Small24B2501|Plantilla propia del snapshot, system docente adaptado y parche regex local existente explícito.|Equivalencia nueva; default antiguo añade BOS duplicado en la prueba CPU.|

Identidad validada por ruta exacta del snapshot registrado, SHA256 de config y
model_type, no por un model_label arbitrario. Perfil desconocido, snapshot
incompatible o sampling ajeno rechazan antes de cargar. Template siempre viene
del tokenizer, sin ChatML/tokens de control fabricados ni fechas/identidades
copiadas de ejemplos del fabricante.

[Cinco verificaciones CPU completas](tokenizer-verification.json):
apply_chat_template(tokenize=True) coincide con render y tokenización
add_special_tokensFalse. Qwen no tenía duplicación previa: no se ofrece una
corrección inexistente como explicación de su calidad. Mistral, en el caso CPU
actual, da prefijo nativo[1,17,…] frente a[1,1,17,…] con default: BOS1 frente
a2. La nueva ruta usa false explícito; histórica se conserva para reproducción.
[Detalle BOS/EOS](mistral-special-token-detail.json). No se atribuyen errores
históricos de Mistral a esta observación ni se afirma haberlo medido en GPU.

Se registran template completo/hash, clases, archivos de tokenizer, IDs de
inicio/final, BOS/EOS y prefijo de generación. Qwen añade su prefijo assistant;
Mistral no cambia al alternar add_generation_prompt en su plantilla nativa:
no se inventa otro prefijo. Delimitadores adversarios e historial mostrados
se preservan íntegros como datos y no aparecen como especiales en su contenido.

Perfiles de sampling permitidos: greedy explícito para Qwen2.5/Mistral;
Qwen2.5 sampling0.7/0.8/20; Qwen3 non-thinking0.7/0.8/20/min_p0;
Mistral low-temperature0.15 con parámetros explícitos. Semilla validada y
configuración efectiva por llamada. Son opciones preparadas, no mejoras
demostradas. Qwen3 thinking no se activa; no se le asigna un presupuesto implícito.
Greedy histórico queda intacto. El outcome registra parámetros efectivos en
perfiles muestreados en lugar de declarar temperature0 por defecto.

## Comparación real: solo estructura, mismo14B y greedy

Mismo T2 expuesto de comparison-003: borrador inicial completo, crítica
depurada, cinco fuentes COMPLETAS y límites idénticos. Requests y mensajes
efectivos congelados ANTES de GPU: [old](old-request.json), [new](new-request.json),
[frames CPU](effective-frames-cpu.json), [código usado](code-freeze.json).
Primero old→new; se congelaron ambas salidas antes de la revisión. Ramas
conocidas: desarrollo asistido, no evaluación ciega ni superioridad estadística.

Único modelo GPU: Qwen2.5-14B-Instruct NF4, snapshot
`cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`; misma plantilla nativa, greedy y
semilla42 en ambas. No cambio de RAG, modelo o sampling. Qwen14 no duplicaba
especiales con la ruta anterior: se confirma runtime/template frente a CPU.

|Ruta|Entrada/salida|Generación|Resultado de lectura completa|
|---|---|---|---|
|Anterior|2911/480tokens|28,234s,stop|Mantiene la frase errónea y añade su negación al final; contradicción interna. Reproduce exactamente el texto T2-L anterior con nueva llamada.|
|Nueva|2889/436tokens|25,625s,stop|Sustituye parte del cuerpo y elimina aquella salvedad, pero vuelve a llamar diseño innecesario a filtros/otros campos en el cierre. Persiste el defecto.|

La fuente NASA64 pide aclarar entradas/salidas y relaciones con interesados;
Requisitos5 pide no prefijar solución. No justifican descartar potencial alcance
funcional por su tipo. Se leyó pregunta, borrador, crítica, contexto completo
y ambas respuestas. El ejemplo ficticio es admisible y se conserva; no se
exige todo detalle NASA ni una respuesta académica prefabricada.

**Cambió:** operación observable de edición y coherencia formal. **No cambió:**
la clasificación conceptual equivocada. No se declara mejora útil por ser más
corta/rápida: tienen longitud distinta y solo una salida por variante. No se
detecta otro error inequívoco de diferente concepto; persiste el prioritario
en otra ubicación. La crítica se sostiene; no pedía incluir todos los filtros.
[Revisión completa por defecto, omisiones y crítica](review-exposed.md).

Ninguna salida satisface el criterio. Se activa la parada prevista, no se elige
la última por defecto ni se agrega síntesis no revisada. Las dos preguntas nuevas
sobre prototipos y conflictos se fijaron antes de resultados y quedan
[congeladas, sin ejecutar](new-questions.json). No se inicia otra campaña.
El fallo no demuestra que toda configuración sea irrelevante o que el14B sea
incapaz universalmente; demuestra que ESTA adaptación no incorporó esa corrección.

## Pruebas, incidentes conservados y presupuesto

**104 pruebas CPU antes de inferir**: tareas, renderer único, mensajes efectivos,
datos adversarios, historial, identidad/modelo/perfil incompatibles, sampling,
regresión del adaptador, capacidad, timeout/cancelación, review_repair y StudyLab.
[Log previo](tests-frame.log). Black/Ruff correctos. Tokenizadores locales
comprobados sin cargar pesos; no hubo descargas o instalaciones.

Primer check de tokenización falló por comparar BatchEncoding con list, no
porque IDs Qwen fueran diferentes. Se conserva primer intento/traceback y se
normaliza solo input_ids. Un parche no coincidente tras Black fue rechazado
sin editar. [Incidentes y reloj](mechanical-notes.md).

Después de GPU se completó observabilidad de perfiles muestreados para no
presentar temperature0 informativo como dato efectivo; no cambió las dos
llamadas greedy. Se comprobó además compatibilidad del nuevo constructor con
tipos LabGenerationRequest/historial existentes, conservando el presupuesto
solicitado en vez de ampliarlo implícitamente. Código ejecutado se conserva
en [executed-code/](executed-code/) y coincide con code-freeze.
**108 pruebas finales correctas**:
[tests-final-delivery.log](tests-final-delivery.log), una advertencia Starlette/httpx previa.
No se presenta esta mejora CPU posterior como ganancia GPU ni se repite inferencia.

Comando CPU final:

```text
.venv\Scripts\python.exe -m pytest tests/course_dialogue/test_structured_prompts.py tests/course_dialogue/test_expanded_repair.py tests/course_dialogue/test_cached_adapter.py tests/course_dialogue/test_output_budget_contract.py tests/course_dialogue/test_review_repair.py tests/course_dialogue/test_scope_control_transport.py tests/unit/test_study_lab.py tests/course_dialogue/test_generation_observability.py -q --basetemp docs/audits/2026-10-28-structured-prompts/pytest-temp-005
```

Ensayo ejecutado con `.venv\Scripts\python.exe -X utf8 docs/audits/2026-10-28-structured-prompts/invoke.py`.

Nuevo reloj persistido desde primerpreflight17:03:54 Europe/Madrid
(UTC exacta y monotonic en [recibo](first-preflight.json));30min globales/8calls
máximas/2048tokens/180s. Consumidas **2llamadas+1carga+1calentamiento técnico**,
sin reinicio del reloj ante fallos CPU. Ciclo hasta limpieza831,696s, incluida
implementación/pruebas; construcción de entrega1256,805s desde el mismo origen.
Sello final registra duración completa dentro1800s. No se subsanan relojes o
presupuestos históricos retrospectivamente. [Métricas](metrics.json).

Primerpreflight1828MiB/22%, durante preparación CPU y sin cargar pesos.
La disponibilidad se comprobó de nuevo antes de cargar:2045/32607MiB,2%;
no se aplicó un guard2000MiB como verdad
universal; había holgura suficiente frente al pico observado.59muestras,
pico16233MiB/100%; muestra tras cierre1962MiB/10%. Comprobaciones posteriores
1985MiB/1% y valores agregados variables: no prueban propiedad ni actividad
ajena, y no se culpa a GPU del fallo académico. [Muestras](gpu-samples.json).
Worker50424 y descendientes38672/28416 detenidos, salida0,
[árbol propio cerrado](worker-cleanup.json). No se tocó ComfyUI, documental8022
u otro proceso ajeno, ni se abrió servidor/UI adicional.

## Límites y siguiente paso

[Comprobaciones finales](receipt-checks.json): fuentes/manifiesto/extracciones,
tokenizadores, evidencias de comparison-003 e inputs intactos; código ejecutado
congelado; plantilla runtime coincidente con CPU; salida anterior repetida
exacta; ambos textos completos. Sin cambios de corpus, índices/identidad,
reservas, protocolos históricos, commits/Reset o migraciones. Renderer de
artefacto inerte con escape/CSP, cero ejecución de contenido.

Todo unverified/not_assessed, publicationfalse/participantnull. Revisión
semántica del asistente, no verificador autónomo. E2/Feature012/G2/SC001 y
participantes mantienen su estado; sin evaluación de alumnos, notas/rúbricas,
examen, voz o web del producto. No envío interchat ni reintento del rechazado.

Siguiente paso concreto propuesto, **sin ejecutar**: comprobar una demostración
breve de la operación de sustitución sobre un tema distinto, sin respuesta patrón
del objetivo, antes de ampliar a muestreo u otros modelos. Su necesidad y coste
deben decidirse con este fallo visible, no asumir que XML/JSON, más tokens o
una nueva instrucción resolverán la incorporación. No fase automática posterior.
