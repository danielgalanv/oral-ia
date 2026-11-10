# Incremento de recuperación del autoestudio sobre corpus v2

Estado: autorizado por el usuario para planificar y encargar en una nueva tarea. Alcance: recuperación verificable y consultable; no generación, examen, voz ni apertura de participantes. Una sola tarea escritora, reporte al coordinador al terminar y parada del alcance.

## Objetivo visible

El docente escribe una pregunta en lenguaje natural y ve qué pasajes del corpus v2 recupera ORALIA, con texto, documento, página/sección y acceso al original. No ve una respuesta académica redactada, un score de verdad o una falsa promesa de suficiencia. Esta entrega permite probar recuperación antes de conectarla al generador.

Se conserva el corpus completo del bloque en su cobertura actual, no una selección para las dos preguntas iniciales. Las unidades no habilitadas, las figuras incompletas e INCOSE ausente mantienen sus límites. No se presume aceptación académica de v2 por existir un manifiesto técnico.

Antecedentes: [entrega v2](../audits/2026-10-27-requirements-block/report.md), [matriz de cobertura](../audits/2026-10-27-requirements-block/coverage-matrix.md), [parte 1](../audits/2026-10-27-part1-foundations/report.md), [selección técnica](2026-10-27-technology-and-workflow-decisions.md), [plan general](2026-10-27-consolidated-action-plan.md). Seguir SpecKit sobre artefactos existentes sin perder IDs/estados; este bloque no cierra la feature ni sus gates.

## Trabajo por dependencias

### R0. Fijar contrato, recursos y banco antes de cambiar ranking

Registrar versiones/hashes efectivos del corpus v2, módulos que se tocarán, modelo/tokenizer local, configuración y recursos protegidos. Inventariar lo ya implementado; no repetir correcciones de caché, offline o Chroma demostradas. El puerto de recuperación debe devolver evidencia, no autorización o juicios sobre alumnos.

Congelar una comparación pequeña antes de ejecutar: como referencia de alcance, dos preguntas nuevas por cada uno de los doce subtemas (24), más seis controles de paráfrasis bilingüe, referente/cambio y ausencia/distractor. Ajustar y documentar el banco antes del primer resultado si algún control solapa; no modificarlo para aprobar. Separar desarrollo de evaluación por escenario, no solo por distinta redacción. Las dos preguntas del demostrador son regresión expuesta y no se cuentan como reserva nueva.

El oráculo recoge pasajes o conjuntos alternativos pertinentes y su motivo, no respuestas académicas para el generador. Debe contrastarse con documentos, sin escoger referencias mirando el ranking. La relevancia técnica inicial es una propuesta auditable, no revisión docente inferida. No hacer llamadas LLM para etiquetar este banco.

### R1. Identidad efectiva común

Resolver snapshot o hashes locales concretos del encoder y tokenizer; dimensión real, pooling, normalización, límite efectivo, representación y versiones de extracción/fragmentación. Una única composición usa esa configuración para construcción, consulta y reconstrucción del índice nuevo. No inventar revisión por el nombre del modelo ni confiar en dimensión coincidente. Reutilizar adaptadores con opción explícita de dispositivo CPU y carga local.

Índice aislado, nunca el habitual. Un desajuste rechaza antes de consultar o escribir; una identidad desconocida se informa, sin reindexar legado. No ampliar T077 como cumplida globalmente si solo se conecta el perfil nuevo; informar cada consumidor aún pendiente.

### R2. Representación para búsqueda y contexto

Fragmentar unidades disponibles según el tokenizer real y su límite con tokens especiales. No resolverlo truncando silenciosamente. IDs y offsets estables hacia la representación revisada, y vínculo explícito a `raw_text`/original cuando la representación es derivada. Preservar continuaciones, títulos, estructura de tablas y procedencia.

Separar fragmento de búsqueda de contexto que después recibirá el generador: recuperar el primero y ampliar al pasaje/sección pertinente dentro de un presupuesto explícito. Tablas grandes necesitan filas/encabezados y contexto, no columnas concatenadas sin relaciones. Rechazar rutas o unidades ajenas al paquete. No reconstruir hechos de figuras en cuarentena ni traducir mediante modelo.

### R3. Comparación limitada de estrategias

Reutilizar el léxico actual como baseline; conectar recuperación densa mediante Sentence Transformers/Chroma existentes y una variante híbrida por RRF. Máximo tres estrategias en esta entrega. Si existe una biblioteca BM25 instalada y mantenida, puede sustituir la rama léxica de la variante híbrida, declarando el cambio; si no, mantener la rama léxica y dejar BM25 como propuesta, sin instalar ni construir un framework propio para cumplir una etiqueta.

Congelar tamaños de candidatos, constante RRF, presupuesto de contexto, tratamiento de historial y orden determinista de empates antes de medir. RRF combina posiciones, no scores incompatibles. El historial sirve solo para el referente mostrado; el cambio explícito lo descarta. No incorporar bruto rechazado o historial del examen.

No añadir reranker o nuevos checkpoints en este bloque. Su utilidad se decidirá después de ver si los pasajes pertinentes llegan a candidatos. No aumentar iterativamente parámetros hasta que pase el banco ni usar IDs/palabras de los tests como reglas de contenido.

### R4. Medición y decisión

Separar recall de candidatos, orden final (MRR/nDCG si el oráculo lo permite), referencias complementarias cubiertas, contexto irrelevante/volumen, tiempos de carga/consulta y finalización. Reportar datos por pregunta y subtema, no solo media. Vacío no significa fuera del temario; score no significa verdad ni suficiencia.

Antes de comparar, escribir criterios concretos de adopción y pérdida tolerable basados en el propósito del banco. Para promoción técnica: ningún acceso a unidad retirada/ajena o identidad incompatible, ninguna truncación oculta y ninguna regresión funcional del perfil anterior. Los criterios semánticos son evidencia finita, no garantía universal. Si no hay variante mejor, entregar baseline y resultado negativo; no iniciar otro modelo.

Banco y comparación acotados, máximo una pasada de medición por estrategia; errores mecánicos pueden corregirse con reproducción y nuevo recibo, conservando el intento inicial y sin cambiar oráculo. Registrar exposición. No consumir reserva o presupuestos históricos.

### R5. Prueba docente

Integrar la consulta como opción explícita en el recorrido existente, sin modificar el perfil documental en uso ni construir un panel técnico nuevo. Un selector de estrategia puede quedar solo para laboratorio si ayuda a comparar; el usuario necesita ver pasajes y originales, no configurar hiperparámetros.

Verificar navegador real: definición, tipos y una pregunta de otro subtema, ausencia de evidencia suficiente, referente/cambio cuando esté disponible y cierre/reentrada. La interfaz indica «pasajes recuperados», no «respuesta verificada». Si no hay candidata suficiente, mostrar el límite; nunca responder con texto escrito a mano como si lo generara ORALIA.

Entregar guion corto y comando exacto, con paquete/configuración fijos, después de comprobarlo de extremo a extremo. La prueba del usuario no sustituye a los tests ni cuenta como validación del generador. Mantener manifiestos y consulta v1.1/v2 anteriores intactos o compatibles, y demostrar cómo volver al modo documental.

## Recursos y límites

Se autoriza cargar únicamente el encoder y tokenizer YA INSTALADOS, en CPU explícita, para embeddings de este paquete y consultas del banco. No CUDA, detección que active GPU, generación LLM, downloads de pesos, nuevas instalaciones, nube o procesos ajenos. Fijar modo offline y verificar configuración efectiva. Si el recurso local no puede cargarse de forma segura, entregar preparación y bloqueo preciso; no sustituir por vectores simulados presentados como búsqueda real.

No SQL/migración o reindexación habitual por defecto. La autorización del perfil de prueba deriva de su paquete local y acceso docente; no fingir que reemplaza la política SQL de actividad/participante. Si se integra con esa ruta, preservar y probar su revalidación real. Cambios/retirada/integridad después de esperas deben bloquear entrega de evidencia obsoleta.

Tests: identidad y mismatch, texto relevante al final del fragmento, cobertura/offsets, tablas, cuarentena, duplicados/equivalencias, reconstrucción segura e idempotencia. Usar dobles para fallos y encoder real CPU para acreditar recuperación. Regresión por impacto y estilo/build cuando corresponda; no repetir 204 celdas ajenas.

Sin commits, Reset, sobreescritura de fuentes/evidencia/reserva/presupuestos, cierre de tareas humanas o apertura de T090/T150/G2/SC001. No parar el servidor documental del coordinador ni sesiones del usuario; puertos propios y parada solo de procesos acreditados. Reporte final al coordinador y no continuación automática.

## Cierre del incremento

**Decisión humana posterior a la entrega v2.1:** se acepta continuar con tablas como limitación documentada, sin exigir resolverlas por completo antes del primer autoestudio. Ver [alcance, causa observada y continuación permitida](../audits/2026-10-27-retrieval-increment/accepted-table-limitation.md). Los resultados y criterios congelados de este incremento no se reescriben; la selección de contexto tiene además limitaciones no exclusivamente tabulares. La aceptación no abre gates ni acredita generación.

Entregar implementación/consumidores efectivos, índice y representación versionados, banco/oráculo congelados, métricas/resultados, errores conservados y límites, pruebas y guion docente. Indicar si recupera evidencia suficiente para el primer ensayo generativo o qué carencia concreta lo impide. No confundir eso con que el LLM ya explique correctamente. El siguiente trabajo, si se autoriza, será conectar y observar una conversación real breve, no seguir optimizando indefinidamente el recuperador.
