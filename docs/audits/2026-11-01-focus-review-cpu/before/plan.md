# Implementation Plan 012 — estado vigente

## Decisión de ampliación web, 30-10-2026

La orden humana permite Internet ante insuficiencia local, con aviso de procedencia externa, contraste de validez y comprobación frente al material docente. La constitución 2.0.0 incorpora la excepción restringida. Implementar posteriormente T114–T118 según [contrato web](contracts/web-evidence-fallback.md), empezando por política/recibos y pruebas CPU con transporte simulado. Separar adquisición, revisión del contenido externo y comparación con material docente; no convertir una descarga correcta en una aprobación semántica. Priorizar fuentes originales identificables, sin imponer un número arbitrario de sitios ni una garantía universal. No iniciar conexiones externas, GPU, cambios de modelos o publicación por esta actualización documental. Los perfiles existentes siguen offline.

## Incremento autorizado I5: recuperación operativa, 29-10-2026

Al continuar tras el recorrido por navegador, implementar solo T110–T113. Reutilizar `StudyFailure`, `DiagnosticStudy`, `studyRuntime.ts` y la sesión temporal existentes. Diferenciar capacidad de pregunta/contexto antes de embeddings y generación; trasladar mensajes seguros a la UI y conservar historial/cupo. Probar negativos y continuación con dobles CPU, y un recorrido de navegador con recuperador real CPU y proveedor fixture explícitamente identificado. No necesita GPU ni valida suficiencia semántica. Si cambia el hash del recuperador, crear únicamente un índice derivado nuevo en el dossier; no reescribir identidades anteriores. Sin cambios de SQL, políticas, modelos o gates. Referencia: [contrato de recuperación](contracts/study-recovery-addendum.md).

Fecha 2026-10-25. Feature en curso, sin publicación ni commits. [Especificación](spec.md) · [tareas pendientes](tasks.md) · [hoja de ruta breve](evidence/verified-conversation-roadmap.md) · [plan detallado](evidence/grounded-tutor-action-plan.md).

## Summary

Mantener el tutor generativo RAG en laboratorio: recuperar evidencia docente vigente desde pregunta e historial mostrado, evaluar suficiencia y conflictos, ampliar búsqueda local de forma acotada si falta información, entregar pasajes trazables al LLM y contrastar sus afirmaciones, pertinencia y cobertura antes de publicar. La respuesta académica depende de la evidencia recuperada, no de contenido docente predefinido ni de memoria del modelo. Conservar todos los gates. La vía web es una extensión restringida autorizada por la constitución 2.0.0, pendiente de política de actividad, implementación y validación; no se activa por este plan.

## Technical Context

Python 3.12, GenerationPort y worker local ya existentes; PDF docentes y catálogo de unidades con páginas originales en un entorno de laboratorio propio. Sin descargas, modelos nuevos, datos de participantes ni cambios de esquema en este bloque de planificación. Qwen3-8B, Qwen2.5-14B y Mistral-24B fueron diagnósticos no comparables para ranking; el último mostró 4/4 turnos pero dos falsas contradicciones. `verification.py` solo comprueba testigos estructurales: `independent_semantics=false`, `publication_allowed=false`. G2/SC001, reserva y publicación cerrados.

## Constitution Check

Principios I/V/VII de la constitución 2.0.0 permiten solo ampliación documental web restringida en autoestudio bajo política versionada, privacidad y contraste previo; no navegación abierta ni red por defecto. Principio IV exige separar generación y verificación. Se conservan arquitectura/contratos, estado explícito, T090/T150, consentimiento, retención, acceso, aislamiento y validación de voz separada. Un `unknown` semántico no autoriza salida. Los ensayos históricos mantienen la constitución y configuración con que se ejecutaron.

## Design / sequence

Decisión de capacidad posterior (27-10-2026): [no continuar ajustando el 7B sobre el banco expuesto; propuesta única 7B/14B](evidence/generator-capacity-decision-v1/decision.md). Comparación propuesta de evidencia fija frente a recuperación normal, con controles nuevos, presupuesto y baseline común; no ejecutada. El 24B disponible no se descarta universalmente ni se activa como fallback. Se deja versión auditable y la implementación quieta durante la auditoría global independiente; gates y reserva cerrados. La [adenda de conclusiones de la auditoría](evidence/generator-capacity-decision-v1/audit-followup.md) enlaza sus informes sin duplicarlos: recuperación híbrida/reranking y verificadores especializados siguen siendo candidatos de investigación, no soluciones adoptadas ni verificadores validados. No se inicia otra inferencia o incorporación de dependencias por esta adenda.

Decisión de presentación del 27-10-2026: usar documentos/títulos/páginas legibles; no pedir IDs por frase. Reutilizar la procedencia recuperada para «Fuentes consultadas» cuando no exista atribución semántica verificada. Mantener el juicio sustantivo separado y conservar ST01 bajo el contrato anterior. Implementación y pruebas CPU preceden a un ensayo nuevo y acotado de seguimiento/ejemplo; no ajustar sus oráculos tras observar respuestas.

Bloque pedagógico posterior: una extensión general optativa frente al baseline literal, sin cambiar ranking ni respuestas predefinidas. La aclaración del usuario permite ficción coherente y exige respaldo al principio/interpretación, no a cada detalle del escenario. Tres conversaciones nuevas de cuatro turnos se congelaron antes de inferir, con ramas y presupuesto. El ensayo terminó parcial por un límite de salida, tras conservar un primer fallo de telemetría y una única recuperación técnica: no se promueve el perfil por pruebas CPU ni por conversaciones incompletas. Ver [comparación y decisión](evidence/pedagogical-comparison-recovery-run-v1/report.md).

1. Versionar fuentes docentes activas, procedencia, retirada y política; mantener web apagada. Registrar el punto de extensión web condicionado, sin red en este bloque.
2. Recuperar unidades desde pregunta e historial realmente mostrado. Si la evidencia es insuficiente o conflictiva, reintentar localmente con presupuesto y trazas limitados; no inferir suficiencia a partir de solapamiento léxico.
3. Entregar al LLM solo evidencia recuperada trazable y obligaciones del turno. Generar explicación; distinguir paráfrasis, inferencia con premisas recuperadas y ejemplo hipotético, cuyo principio requiere fuente.
4. Contrastar afirmaciones, pertinencia y cobertura mediante evaluación separada del generador. Una hipótesis de verificador debe ser distinta de las tres vías fallidas y medir permisos/rechazos falsos y cobertura; un banco finito no garantiza verdad. Mantener publicación cerrada mientras no exista candidato viable.
5. En insuficiencia, conflicto o incertidumbre, conservar estado y expresar límite o pedir aclaración concreta. No usar respuesta académica prefabricada ni sustituir una pregunta difícil por otra lección.
6. Solo después: revisión docente, conversaciones desde estado real, tres repeticiones por caso, reserva no usada para ajuste, gates G2/G3/G4 y regresiones. Ningún ensayo de laboratorio autoriza publicación ni acredita voz o utilidad humana.

Contrato detallado, evidencia y criterios de avance: [plan de acción](evidence/grounded-tutor-action-plan.md). Decisiones históricas A–T, tiempos, presupuestos y alternativas quedan íntegros en el [plan anterior](evidence/speckit-history-2026-10-25/plan.md); el historial no se carga salvo para auditar una decisión concreta.

T063/T064/T071 forman una misma frontera: política vigente de fuente de la aplicación, obligaciones/afirmaciones trazables y entrega citable al generador. El [contrato unido y la hipótesis T072](evidence/rag-independent-evaluation-design.md) registran qué aporta cada módulo existente, qué sigue faltando y cómo descartar una vía semántica inviable. El preview del laboratorio jamás equivale a salida para participante.

El estudio mínimo de T072 descartó H1 (plan proposicional + comprobador determinista) como puerta para texto libre: no detecta por sí mismo cláusulas añadidas ni inversiones al realizar el plan. Se mantiene el RAG generativo en laboratorio, sin construir un compilador simbólico general ni atomizar por defecto toda la asignatura. La elección entre revisión humana de cada salida, lenguaje verificable más acotado o investigación separada de otro evaluador es una decisión material de alcance; ninguna se aplica como sustitución silenciosa.

Antes de recuperación y generación, una decisión de alcance con procedencia docente distingue `in_scope`, `out_of_scope`, `uncertain_scope`, `mixed` y peticiones operativas. La presentación de la asignatura contiene temas declarados, pero advierte que el cronograma puede cambiar y que el examen se basa en lo visto en clase; el catálogo parcial de PDF no define por complemento todo lo excluido. Por ello el laboratorio solo pronuncia «no necesitas estudiarlo» ante una exclusión explícita y vigente, no ante ausencia de resultados. La evaluación de alcance es independiente del juicio de suficiencia documental y del poscontrol semántico.

El usuario confirmó el 25-10-2026 el alcance de la [política v1](evidence/course-scope-policy-v1.json) para la actividad de laboratorio de Ingeniería del Software, sin bloques extra como bloques propios por ahora. La política liga curso/actividad/versión y hashes de fuentes; el [ensayo solo lectura](evidence/course-scope-policy-validation-v3.json) revalidó SQL y tres rutas con selección semántica inyectada. El binding no aprueba respuestas: la selección de bloques desde preguntas libres y el control semántico posterior siguen pendientes.


## Parte 2: implementación documental acotada I0/I1

Paquete nuevo materiales/docente/piloto-requisitos/paquete-v1 con originales, capturas, extracciones y manifiesto. PdfExtractor/PptxExtractor existentes; QA visual focal con herramientas instaladas; sin OCR/modelos. Extensión documental de Materiales en Tecnica.tsx, servida por perfil local separado oralia.documentary desde scripts/demo.ps1 -Documentary, sin SQL ni Chroma. Un único servidor localhost, originales por ID validado, acceso local explícito y cierre/reentrada; raíz habitual intacta. Consulta literal y mapa curado, sin score semántico. No ejecutar el launcher de autoestudio que carga embeddings. Registro en docs/audits/2026-10-27-part2-corpus; pruebas proporcionales de aislamiento/acceso/integridad y recorrido real de navegador si está disponible.

Estado de entrega parte2: corpus v1.1 y perfil documental implementados/verificados; navegador real y launcher con PATH habitual comprobados, servicios propios parados. [Informe](../../docs/audits/2026-10-27-part2-corpus/report.md). INCOSE sigue sin original adquirido; cuarentena y alcance visibles. No activa fases posteriores.

## Ampliación documental v2 autorizada

Reutilizar paquete-v1 y extractores CPU; paquete-v2 independiente con originales por hash, representaciones revisadas y evidencia en docs/audits/2026-10-27-requirements-block. Matriz derivada de las 89+14 páginas principales y examen focal de material docente adyacente, sin trabajos de alumnos. Añadir solo secciones complementarias justificadas. Selección optativa `demo.ps1 -Documentary -DocumentaryPackage v2`, por defecto v1.1, servidor propio en puerto distinto del8022; sin cambio a un servidor ya iniciado. QA de texto/tabla/figura, hashes/enlaces/acceso/HTML inerte y navegador real; no cargar modelos ni iniciar T077. No regenerar IDs/estados históricos.

## Recuperación v2.1 optativa, 27-10-2026

Ejecutar exclusivamente [plan incremental autorizado](../../docs/plans/2026-10-27-retrieval-increment.md), sin regenerar artefactos. Composición única en oralia.documentary.retrieval con adaptadores existentes, CPU explícita/local-only, hashes efectivos y segmentación según tokenizer; índice nuevo fuera del corpus. Rutas documentales anteriores siguen por defecto. Banco/oráculo y protocolo congelados antes del ranking; una pasada por estrategia y adopción sujeta a pérdidas por subtema. Resultado: ninguna candidata supera la tolerancia en contexto final; baseline conservado, sin otro modelo o ajuste. [Entrega y límites](../../docs/audits/2026-10-27-retrieval-increment/report.md). No integra GenerationPort o participante, ni acredita suficiencia/alcance semántico. No modifica los gates o el orden autoestudio→examen.

## E0 del primer diálogo generado autorizado, 27-10-2026

Inventario y contratos según [plan específico](../../docs/plans/2026-10-27-first-generated-study-increment.md), sin sustituir catálogo/binding del laboratorio por v2 silenciosamente. [Informe](../../docs/audits/2026-10-27-first-generated-study/report.md) y [protocolo previo](../../docs/audits/2026-10-27-first-generated-study/protocol-v1.json): helper CPU con recibos exclusivos, estado unverified/not_assessed y presupuesto rechazado antes de worker. No se activa una superficie de inspección nueva; LaboratoryConversation mantiene revisión positiva y participante cerrado. GPU ocupada vigente; no cargar encoder/GPU ni esperar automáticamente. E1/E2 no ejecutados. Corrección futura localizada: coherencia del límite60s lab/worker y nueva disponibilidad antes de inferencia, con congelación prospectiva; no modelo ni prompt alternativos.

## Cableado CPU docente autorizado, 27-10-2026

Implementación directa sobre oralia.documentary.retrieval v2.1 y GenerationPort existente, con binding propio del paquete/actividad diagnóstica y sin mezclar catálogo SQL antiguo. Nuevo estudio de inspección/API y componente Materiales optativo; normal deja proveedor desconectado, fixture explícito rotulado. Control de integridad y acceso antes/después de esperas, recibos separados de publicación, confirmación DOM, épocas/timeout, lease y purga. Protocolo sucesor50s aceptado sin cambiar backend. Índice existente reabierto CPU, sin construir; pruebas de frame del adaptador con pipe doble y recorrido real de navegador con fixture. Runner futuro solo bajo switch/autorización nuevos; no ejecutado con pesos generativos. [Entrega](../../docs/audits/2026-10-27-generated-study-cpu/report.md). T102/T103 mantienen captura/calidad y E2 reales pendientes; esta entrega completa el cableado CPU, no declara feature cerrada.

## E1 real ejecutado y revisado, 28-10-2026

Una candidata14B NF4 y recuperación densa real v2.1 CPU, sin alterar prompt/protocolo/corpus/ranking. Primer arranque del worker agotó90s antes de disponibilidad y warmup;0llamadas académicas. Corrección mecánica mínima: preparación explícita hasta180s (default90), recuperación solo si0llamadas/warmup no iniciado/árbol detenido, reloj original20min preservado. Recuperación confirmó modelo en40,062s;8respuestas completas/un warmup;473,813s desde inicio original hasta limpieza final. Revisión detecta fallos de significado con evidencia presente, no atribuibles a tablas o GPU. [Informe, transcriptos y propuesta acotada sin ejecutar](../../docs/audits/2026-10-28-first-generated-study-real/report.md). T102 diagnóstico real completo; T103 E2 real pendiente y no anunciada correcta. No otra inferencia/campaña o participantes por esta decisión.

## Revisión/reparación diagnóstica optativa, 28-10-2026

Componer el puerto existente con revisión estructurada contra el mismo contexto, una reparación máxima y post-revisión; conservar todos los brutos, fase/coste/terminación y permiso/retención. UI Materiales expone la traza y mantiene participante cerrado. Cada sesión tiene su propia copia de traza/guard; comparte solo transporte/cupo. Autocrítica14B ejecutada con protocolo congelado,8casos(4expuestos+4nuevos cercanos),14llamadas+1warmup:0mejoras claras,7textos idénticos,1más largo sin ganancia,3informes inválidos. No promover esa candidata como verificador.

Rectificación humana posterior: el asistente había reconocido defectos que el14B no detectaba; no eran el mismo revisor. Añadir entrada de crítica suministrada auditable, sin pretender autonomía.4casos E1expuestos, críticas del asistente congeladas con fuentes antes de corregir,4llamadas de reparación+1warmup, revisión posterior del asistente:2objetivos corregidos/2parciales, con errores residuales conservados. [Resultado](../../docs/audits/2026-10-28-agent-assisted-repair/report.md). Son presupuestos/diseños separados, no ajuste retrospectivo del primer ensayo ni comparación ciega. No se automatiza una aprobación semántica o una API externa al producto; no ronda adicional para ocultar fallos. E2 real y gates permanecen pendientes.


## Entrega operativa acotada web — 30-10-2026

Se ejecutaron T114/T115: `WebPolicy` versionada, catálogo público original con búsqueda local sustituible, descarga HTTPS con DNS público fijado, extracción separada y recibos. Sin dependencias nuevas. El proceso necesita `--web-policy` explícito para una actividad de autoestudio nueva; cualquier modificación del archivo revoca el binding anterior, sin modificar sesiones SQL. Presupuestos compartidos por actividad en el proceso, sin renovación por reentrada. Se añadió inspección docente en Materiales con aviso previo y enlaces; no entrega esos documentos al generador ni certifica semántica. `web_review.py` separa contratos de respaldo externo y compatibilidad, pasa todas las páginas disponibles y registra huecos. Los evaluadores reales y la ruta automática continúan pendientes T116–T118/T151–T153. [Informe](../../docs/audits/2026-10-30-web-fallback-runtime/report.md). Sin nueva campaña, modelos, GPU, índice, migraciones ni promoción.


## Plan acotado de decisión de contenido y navegador — 30-10-2026

Se auditó caché: Qwen2.5-1.5B-Instruct snapshot 989aa7980e4cf806f80c7fef2b1adb7bc71aa306 completo. Ensayo de revisión CPU float32, 4 threads, cuatro llamadas greedy, 256 tokens/75s por caso y 600s globales, sin reintentos ni cambios tras observar salida. Reutilizar transformers instalado y comparación externa contra criterios congelados no incluidos en el prompt; separar apoyo externo y compatibilidad. Los resultados son evidencia limitada del candidato, no autoaprobación del generador ni apertura de FR-014. Solo promover integración generativa si la evidencia la justifica; si falla, conservar resultados y completar navegador operativo con fixture y fuentes públicas acotadas. Dossier nuevo: docs/audits/2026-10-30-web-semantic-cpu/. No GPU, descargas de modelos ni reutilización de cuota histórica.

Confirmación única de capacidad posterior al fallo real del 1.5B: Qwen2.5-7B-Instruct snapshot a09a35458c702b33eeacc393d103063234e8bc28 ya completo en caché (~15,2 GB de pesos), CPU float32/4 threads, cuatro controles nuevos cercanos y misma instrucción, 256 tokens/120 s por llamada, 600 s globales, cero reintentos de contenido. Memoria libre observada ~98 GiB frente a ~29 GiB de parámetros float32. Fuentes/oráculo congelados en seven-b-confirmation antes de inferir. No se reabre el banco histórico del 7B ni se ajusta sobre C01–C04; la comparación es diagnóstica, no ranking ni garantía de independencia de errores entre modelos de una misma familia.


Decisión tras los dos ensayos CPU congelados: no integrar estos candidatos como evaluadores habilitantes. 7B tarda 65,7–93,8 s por decisión simple y falla contenido, además de un esquema; reparar JSON no resuelve los veredictos. La cadena autónoma de alcance/suficiencia, adquisición, doble contraste, explicación y revisión final no queda acreditada. Se completó el navegador existente con recuperación real CPU, proveedor de generación fixture y un GET RFC2119; no es una prueba de respuestas académicas ampliadas. No se implementa otra capa de bloqueo ni se carga un tercer candidato por esta entrega. Mantener T116–T118 y T151–T153 abiertos con los fallos precisos, fuentes/oráculos inmutables y outputs completos.


## Incremento prospectivo de rondas web CPU — 30-10-2026

Auditar comparison-003 y perfiles posteriores: hay mejoras bajo crítica del asistente, no evidencia de crítico autónomo. Reutilizar StructuredGenerationRequest/render_messages, Issue/parse_review, ReviewRepairGenerationAdapter.call y CallBudget; añadir composición optativa de dos ejes, no un sistema de publicación. Cuatro casos nuevos y fuentes/criterios congelados antes de inferir. Generador inicial Qwen2.5-1.5B; crítico/corrector Qwen2.5-7B, snapshots locales registrados, variante CPU dynamic-int8 en memoria/oneDNN/8 threads para viabilidad temporal (no comparable al float32 previo). Hasta 28 llamadas y 1800s globales, dos correcciones/caso y un reintento de formato/caso; generación 192tokens/90s, revisión384tokens/150s, corrección256tokens/150s. Preflight neutral 12tokens por modelo, máximo60s cada uno; si no resulta viable no simular semántica. Misma familia no acredita independencia de errores. Sin nuevas dependencias, descargas de pesos, GPU, SQL o activación habitual.


## Ejecución y cierre de rondas CPU, con continuación humana

Incremento posterior autorizado: separar por versión optativa los roles de revisión y
corrección del prompt del tutor, permitiendo IDs internos solo en crítica. Mantener
el contrato de incidencias, fuentes y transporte existentes. Diagnóstico CPU 7B con
borradores expuestos y máximos prospectivos, sin nuevas descargas ni GPU, para observar
crítica, corrección y post-revisión. Preservar v1 y todos los históricos; no acreditar
generalización, integración autónoma o gates con este diagnóstico (T164/T165).

Tras conservar el fracaso de regeneración completa, ensayar una sustitución literal
del primer tramo anclable señalado por el crítico automático; el host conserva lo
que queda fuera del objetivo. Excluir críticas sin anclaje de esa operación, sin
afirmar que son falsas ni que se haya resuelto cobertura. Presupuestos separados:
primera pasada hasta 7 llamadas/1200 s con etapas de 180 s; recuperación CPU directa
de R01 hasta 3 llamadas/1200 s, 512 tokens/420 s por etapa; diagnóstico localizado
hasta 2 llamadas/600 s, parche 192 tokens/180 s y post-revisión 512 tokens/420 s.
Los dos últimos son diagnósticos nativos CPU, no una ampliación del presupuesto
de la aplicación. No se introduce crítica humana en ninguna inferencia. Conservar
los fallos tipográficos, la regeneración que mantiene el error y el tramo realmente
seleccionado, incluso cuando una comilla revele un defecto de segmentación.

Petición posterior de suavizar el revisor: añadir `web-review/v3` optativo, sin
reescribir v1/v2. Revisar adecuación a la pregunta, separar ficción/propuesta de
hechos/conclusiones y limitar reparación a un error material, sin exigir todos los
apartados de un documento para un ejemplo sencillo. Calibración CPU 7B float32/8
hilos, dos versiones expuestas de R01, hasta dos llamadas/900 s incluyendo carga,
512 tokens/420 s por llamada. Oráculo fuera del modelo; medir falsos permisos y
rechazos, no solo menos objeciones. Diagnóstico nativo CPU, sin modificar los plazos
de la aplicación ni autorizar publicación por el juicio del modelo (T170).

Nueva petición de más pruebas CPU con contenidos públicos relacionados con el curso:
adquirir fuentes primarias NASA/GOV.UK/W3C, sin incorporarlas al corpus activo.
Usar unidades contiguas con posiciones/hashes y páginas docentes disponibles, nunca
cuarentena. Respuestas de control sintéticas, no respuestas predefinidas del tutor.
Congelar seis casos de desarrollo sobre historias, trazabilidad y accesibilidad,
y cuatro de transferencia local sobre V&V e entrevistas. Modelo existente 7B CPU
float32/8 hilos; desarrollo hasta seis llamadas/2400 s, 512 tokens/420 s por llamada.
Si los fallos justifican un cambio, permitir un único candidato nuevo, medido en
desarrollo antes de cuatro transferencias no usadas para ajustar. No reabrir la
reserva histórica, no GPU, no corregir los oráculos después de observar salidas y
no afirmar una conversación autónoma por este ensayo del revisor.

Continuación 31-10: un único perfil optativo v4 separa testigos externos y docentes,
condiciones/excepciones y cobertura exigida por la pregunta. Antes de inferir se
amplía la calibración expuesta a D02/D05/D06 y C02 anterior: cuatro llamadas/1200 s,
512 tokens/420 s por llamada, CPU exclusivamente. Se conserva el plan anterior y
la enmienda por separado. Transferencia: cuatro llamadas/1200 s, una sola pasada,
sin reajustar el candidato con sus resultados. El bucle v4 permite un defecto
diferente por ronda aunque el número de objeciones siga siendo uno; conserva máximo
de dos rondas, parada por defecto repetido y versiones antiguas sin cambios.

El primer protocolo cerró15intentos/1531,437s de1800s; recuperaciones/int8/float32 y pérdida de parcial v2 conservadas. La continuación expresa posterior abre un sucesor separado (no reinicio del anterior):12llamadas/1800s, mismos borradores reales/fuentes/criterios ya expuestos, revisión breve y challenge de premisas7B.5+4llamadas, ninguna edición distinta. Con el presupuesto restante se midió14B float32 CPU en un caso: una crítica sin objeciones y un parche basado en todas las críticas automáticas previas, incluso la parcial; no entra la crítica del asistente. El parche no terminó en180s. Total11/12llamadas y1517,625s; no se hizo otra llamada ni post-revisión sobre texto incompleto. No aumento de cuotas históricas, GPU, descargas, UI, SQL o material activo. La composición usa GenerationPort/StructuredGenerationRequest/CallBudget y preserva versiones; el formato breve es una variante experimental de datos, no una validación por etiquetas. [Resultado y coste](../../docs/audits/2026-10-30-web-rounds-successor-cpu/report.md).


Decisión 31-10: perfil optativo web-review/v5 con referencias por localización.
El modelo emite source_id y una descripción de la afirmación, sin quote ni claim
literal. Catálogo del host enlazado por fragment_id, documento y versión; páginas
positivas o URL HTTPS, sin inferir números del nombre del archivo. Presentación
construida por el host; copia inmutable de metadatos en el bucle y comprobación en
cada request. Se mantienen presupuestos, revisión tras reparación, revocación y
salida de laboratorio. Pruebas CPU de contrato/integración simulada; medir después
con modelo real sin trasladar juicios humanos al prompt. No confundir retirar
comprobaciones literales con acreditar respaldo o resolver contradicciones.

Repetición autorizada 31-10: diez controles conocidos D01–D06/H01–H04 bajo v5, con pasajes/oráculos originales y metadatos desde manifiesto/recibos. Qwen7B CPU float32/ocho hilos, máximo diez llamadas/4500 s incluyendo carga, 512 tokens/420 s por llamada; sin cambios de prompt ni reintentos. Medir formato y contenido por separado. Regresión expuesta, no controles nuevos de T175.

Aclaración del usuario durante T176: igual exigencia académica para material docente e Internet; cifras, nombres y escenarios hipotéticos coherentes no requieren apoyo literal, tampoco mejoras opcionales para una respuesta adecuada. Tras completar la medición congelada v5, recuperar el prefijo completo de política v3 conservando solo el contrato de referencias nuevo. Separar el tipo genérico de contradicción con una fuente de una declaración de conflicto con el profesor. Calibración sucesora en CPU Qwen7B float32/ocho hilos: D03/D04/D05/D06, cuatro llamadas/1800 s, 512 tokens/420 s; casos expuestos, sin ajustes durante ejecución ni aprobación general por esta muestra.


Sucesor optativo v7 (31-10): una sola decisión status/issues, sin etiquetas de respaldo o compatibilidad generadas. El host deriva reparación/explicación/límite, dejando explícitamente unknown los juicios semánticos no emitidos. Se mantienen fuentes del host, aislamiento de datos y versiones anteriores. Hipótesis distinta del cambio de checkpoint: eliminar redundancia y distinguir propuesta, atribución y conclusión. Tras 82 pruebas focales, un único Qwen3-8B NF4 no pensante, cuatro casos de desarrollo ya expuestos, 768 tokens/180 s y 1200 s totales, sin ajustes ni reintentos. Solo pasaría a reserva nueva tras cuatro revisiones correctas y válidas; un fallo impide promoción.


T178/T179: transporte dedicado validado en host y worker con huella de mensajes; comparación expuesta Qwen2.5-7B/Qwen3-8B NF4, ocho llamadas completas, ningún candidato supera desarrollo. T181: decisión única v7, cuatro llamadas nuevas completas, formato 4/4 y tres revisiones adecuadas; persiste un falso permiso. No se inicia T180 ni se abre publicación. Esta es medición acotada, no finalización semántica de Feature012.


Medición autorizada generador→revisor→corrector→revisor, 31-10: descargar las cargas GPU según orden expresa; Qwen2.5-14B NF4 genera y corrige, Qwen3-8B NF4 no pensante revisa, manteniendo recibos separados. Cinco preguntas (cuatro del bloque de requisitos y un control técnico W3C separado), fuentes originales seleccionadas y congeladas, ningún borrador preparado ni oráculo en los mensajes. 1536/1024/2048 tokens para generar/revisar/corregir, 180 s por llamada, máximo dos correcciones y un reintento formal, 35 llamadas/2700 s totales. Análisis docente técnico externo al modelo, con errores reales iniciales/finales y falsas críticas separados; no suma estos resultados a controles de fallos inyectados. No valida recuperación dinámica ni interfaz ni abre publicación.
