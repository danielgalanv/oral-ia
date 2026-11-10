# Reutilización y estado del arte para el piloto ORALIA

Fecha: 27 de octubre de 2026. Revisión nueva de fuentes primarias y contraste con el código local. Documento de decisión técnica; no modifica requisitos, producción, aceptación docente ni permisos de publicación. No se instalaron dependencias, descargaron pesos ni usó GPU.

## Conclusión

Conservar ORALIA como monolito modular local. Reutilizar bibliotecas existentes para recuperación, extracción y, si se necesita, decodificación estructurada. Refactorizar el recorrido experimental de recuperación y sustituir sus supuestos de verificación por candidatos medidos. No reescribir todo ni construir un modelo de lenguaje o un motor genérico de inferencia desde cero.

El objetivo es un piloto acotado con estudiantes, no una plataforma de explotación. La prioridad es obtener conversaciones completas, útiles y suficientemente fiables bajo una configuración identificada, con consentimiento, límites y parada. La evidencia consultada no ofrece un verificador universal listo para autorizar cualquier explicación pedagógica en español.

## Qué conservar, integrar o cambiar

| Área | Lo comprobado en ORALIA | Decisión |
|---|---|---|
| Aplicación y datos | FastAPI, Pydantic, SQLAlchemy/Alembic, almacenamiento local y adaptadores. | Conservar. No se ha identificado una necesidad del piloto que justifique sustituirlos por una plataforma multiagente o distribuida. |
| Permisos, procedencia y entrega | Política versionada, posiciones y hashes de fuentes, revalidación y distinción entre borrador y texto mostrado. | Conservar y corregir las brechas de la auditoría. Estas defensas no certifican verdad, pero siguen siendo necesarias con cualquier biblioteca externa. |
| Recuperación experimental | `document_evidence.retrieve_units` puntúa `4 × query_hits + history_hits`; también elimina candidatos por coincidencias y presupuesto. | Refactorizar detrás de un puerto común. Mantener el léxico como baseline; comparar recuperación densa y unión léxica/densa, seguida de reranking si aporta mejora medida. No añadir un framework entero para hacerlo. |
| Embeddings | Sentence Transformers y Chroma ya están en el proyecto. El adaptador leído ahora identifica modelo/revisión y carga con `local_files_only=True`. | Reutilizar estas piezas, sin presentar como vigente el antiguo fallo de caché ya corregido. Comprobar fingerprints de índices y segmentación antes de comparar estrategias. |
| Fragmentación | Segmentador de 800 caracteres y solapamiento de 100; el MiniLM por defecto declara 128 tokens. | Medir tokens y recortes efectivos en el corpus. Separar unidades cortas para búsqueda de unidades completas para contexto. No concluir que 800 caracteres siempre caben ni que todos los ensayos anteriores perdieron texto. |
| PDF y Office | Extractores nativos con preservación de tablas; quedan páginas visuales en cuarentena. | Mantener lo que extrae correctamente. Ensayar Docling/OCR solo en huecos relevantes para la actividad, con revisión visual y procedencia nueva. No regenerar todo el archivo histórico. |
| Formato de salida | Decoder finito propio aplicado realmente; ya produjo JSON válido con una decisión semántica falsa. | Conservar para su uso pequeño y probado. Si aparecen esquemas generales, evaluar XGrammar o un backend mantenido con soporte de schema. No confundir formato válido con decisión correcta. |
| Generación | Puerto y worker locales; presupuestos y transporte auditados; múltiples fallos conceptuales observados. | Reutilizar el puerto. Comparar candidatos de capacidad con contexto y condiciones iguales. No seguir acumulando variantes de prompt del mismo modelo como estrategia principal. Cambiar de motor puede reducir mantenimiento, no demostrar mejor comprensión. |
| Verificación | Ledger, offsets y contratos estructurales propios; los jueces ensayados no demostraron transferencia suficiente. | Reutilizar trazas y contratos. Evaluar un detector especializado disponible antes de desarrollar otro juez genérico. Ningún resultado de benchmark externo sustituye calibración local. |
| Pedagogía y evaluación | Instrucción general `pedagogy-v1`; la comparación conservada no mostró una mejora suficiente. | Mantenerla como hipótesis experimental, no como capacidad acreditada. Medir explicaciones, reformulación, ejemplos y transferencia del alumno en episodios completos. |

## Soluciones existentes que merece la pena probar

### Recuperación: Sentence Transformers antes que otro sistema propio

La documentación oficial presenta recuperación de candidatos seguida de un `CrossEncoder` que los reordena. Es una referencia implementable aprovechando la dependencia existente. Un reranker no puede rescatar una página excluida antes de llegar al conjunto de candidatos. La unión léxica/densa propuesta para ORALIA es una hipótesis de ingeniería que debe compararse, no una mejora garantizada. [Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html).

La ficha del MiniLM actual muestra 384 dimensiones y `max_seq_length=128`. Antes de reutilizarlo con páginas o unidades largas hay que registrar qué texto llega al encoder. La selección debe devolver posiciones del original, permitiendo ampliar el contexto sin exigir que el embedding represente una página completa. [Ficha oficial del modelo](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2).

Aceptación propuesta: banco nuevo de consultas y seguimientos, referencias docentes relevantes fijadas por separado, recall de candidatos, calidad del orden, contexto irrelevante y latencia. No reajustar y aprobar sobre los mismos R04/R05 expuestos. No elegir solamente por mayor cantidad de páginas recuperadas.

### Extracción: Docling para las páginas que realmente faltan

Docling ofrece conversión estructurada y OCR, con soporte de documentos Office y PDF. Puede evitar desarrollar un parser visual propio. Su existencia no acredita fidelidad de las fórmulas, esquemas o tablas de esta asignatura. [Repositorio oficial](https://github.com/docling-project/docling).

Propuesta: seleccionar unas pocas páginas en cuarentena necesarias para la primera actividad; comparar original renderizado, extracción actual y nueva extracción. Mantener número de página, regiones y versión de extractor. Revisar licencias de código y pesos por separado, disponibilidad local y coste. Si un PPTX autorizado resuelve mejor una diapositiva, usar esa representación y evitar duplicarla con su PDF.

### Verificación: candidato nuevo concreto en español

LettuceDetect publica detectores de fragmentos no respaldados y una variante EuroBERT específica para español. Es una alternativa concreta al desarrollo de otro juez general por prompts. Su ficha advierte incompatibilidad con Transformers 5 y requiere código remoto de EuroBERT: no debe instalarse sobre el runtime actual ni ejecutarse sin revisar y fijar ese código. Se propone un entorno separado y un adaptador de laboratorio. [Ficha española y advertencia de compatibilidad](https://huggingface.co/KRLabsOrg/lettucedect-210m-eurobert-es-v1).

También existe una variante v2 basada en mmBERT. Su ficha declara soporte multilingüe y clasificación de spans; no demuestra por sí sola eficacia en conversaciones docentes españolas. Además, la descripción de entrada incluye pregunta, pero el ejemplo simplificado de Transformers usa un par contexto/respuesta: verificar el preprocesamiento efectivo antes de copiarlo. La licencia de esta ficha es Apache 2.0; no extender automáticamente la licencia de una variante a toda la familia. [Ficha v2](https://huggingface.co/KRLabsOrg/lettucedect-v2-mmbert-base).

El repositorio separa sus métricas por benchmark y modelo. Eso respalda tratarlos como candidatos empíricos y no como una solución universal. [Repositorio y protocolos](https://github.com/KRLabsOrg/LettuceDetect).

Condiciones locales imprescindibles: incluir paráfrasis válidas, afirmaciones falsas con palabras de la fuente, negaciones, evidencia distribuida, citas correctas con conclusión falsa, preguntas no respondidas y ejemplos ficticios coherentes. Separar los datos inventados del ejemplo del principio académico y de sus conclusiones. Un detector de respaldo no decide automáticamente pertinencia, cobertura ni valor didáctico. No usar sus etiquetas para autorizar participantes sin demostrar sensibilidad a los errores relevantes y tasa de falsos rechazos aceptable.

RefChecker es otra referencia útil para extracción, contraste y agregación de afirmaciones. Sus autores explican problemas de cobertura, pérdida de contexto y evidencia repartida entre varios pasajes. Esto coincide con nuestras limitaciones observadas y desaconseja volver a imponer una sola línea documental por conclusión. Reutilizar su planteamiento o componentes locales es preferible a reconstruirlos ciegamente; sus límites impiden presentarlo como garantía. [Código y limitaciones oficiales](https://github.com/amazon-science/RefChecker).

### Estructura e inferencia: componentes mantenidos, sin migración automática

XGrammar proporciona generación estructurada reutilizable. Ollama documenta salidas con JSON Schema. Son opciones para reducir mantenimiento cuando exista una necesidad concreta de estructura. No sustituyen evaluación semántica; tampoco hay evidencia aquí para afirmar que cambiar NF4/Transformers por otro motor resolverá los errores conceptuales. [XGrammar](https://github.com/mlc-ai/xgrammar), [Ollama Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs).

Para el piloto, preservar `GenerationPort`, configuración solicitada/efectiva y recibos. Una eventual comparación de motores debe fijar pesos, cuantización, plantilla, contexto y criterios; las diferencias restantes se registran. No migrar simultáneamente recuperación, modelo y runtime porque impediría atribuir el cambio.

## Qué requiere trabajo específico de ORALIA

No hace falta construir desde cero algoritmos genéricos de OCR, embeddings, reranking, inferencia o gramáticas. Sí hace falta desarrollar o adaptar:

1. El vínculo entre curso, actividad, fuentes vigentes, permisos y política de alcance. No decidir exclusión por ausencia de recuperación ni delegar consentimiento o borrado al LLM.
2. La memoria de lo realmente mostrado y la gestión de operaciones pendientes, con reintentos y cancelación coherentes. Un framework de memoria no resuelve nuestro contrato de entrega por sí solo.
3. El tratamiento de ejemplos: ficción coherente permitida, interpretación académica contrastada y conclusiones que dependan de premisas suficientes.
4. Un conjunto de evaluación español de esta asignatura, con revisión docente y casos nuevos. Los fixtures verifican cableado; no son sustitutos del juicio semántico real.
5. Un contrato de autorización de texto generativo que preserve las defensas históricas sin exigir reconstrucción por plantillas de toda explicación. Es una decisión de diseño pendiente, no un campo `trusted_text`.
6. El protocolo de un piloto acotado: actividad, resultado de aprendizaje, medidas previas/posteriores y transferencia sin ayuda, registro de incidentes, consentimiento y parada. No requiere construir una plataforma de explotación.

Un preprint de septiembre de 2026 estudia un tutor estructurado y vinculado al curso con 86 estudiantes; distingue pedagogía y modalidad, y no encuentra una ventaja de aprendizaje atribuible a voz en ese contexto. Es evidencia contextual, no aceptación de ORALIA ni prueba de equivalencia universal. Permite seguir un planteamiento experimental y mantener voz aplazada. [Estudio original, resumen consultado](https://arxiv.org/abs/2609.23958).

## Orden de ejecución recomendado

1. Terminar las correcciones CPU de fundamentos ya asignadas. Evitar interferir con el único escritor de producción.
2. Unificar recuperación del laboratorio con los adaptadores existentes; instrumentar tokens y fingerprint, y comparar estrategias sin cambiar el generador. Conservar el baseline.
3. Preparar una evaluación aislada de un detector especializado: primero compatibilidad y preprocesamiento en CPU, después una única calibración congelada con recursos anunciados. Seleccionar checkpoint y licencia concretos; no descargar por el mero hecho de aparecer en este informe.
4. Ejecutar la comparación de capacidad del generador ya delimitada, evitando otro ciclo indefinido sobre controles expuestos. Separar fidelidad documental, utilidad pedagógica y formato.
5. Evaluar conversaciones completas de la actividad seleccionada. No confundir una batería de pruebas de código, una puntuación agregada ni una coincidencia de replay con que un alumno aprenda.
6. Solo después, decidir preparación del piloto bajo criterios empíricos revisables. Los límites no resueltos se documentan y se evita exponer al alumno a la capacidad afectada.

No priorizar GraphRAG, nuevos equipos de agentes, fine-tuning, voz, cobertura de toda la asignatura o una nueva plataforma. No se ha mostrado una necesidad del piloto que justifique ahora esos costes. Esta es una recomendación de proporcionalidad, no una afirmación de que esas técnicas nunca sean útiles.

## Límites de esta revisión

Lectura de código y documentación; no benchmarking nuevo ni instalación. No se ha demostrado compatibilidad de los candidatos externos en esta máquina. Las páginas web reflejan lo publicado al consultar; una integración exige fijar revisiones. Los resultados negativos propios delimitan configuraciones y casos concretos, no prueban imposibilidad de todo modelo local. Los componentes externos tampoco garantizan éxito fuera de sus bancos publicados.

Se preservan las auditorías anteriores y los ensayos fallidos. La propuesta no cierra Feature 012 ni abre G2, SC001 o publicación.
