# ORALIA: técnicas seleccionadas y ambigüedades restantes

Fecha: 27 de octubre de 2026. Complemento del [plan incremental](2026-10-27-consolidated-action-plan.md). Revisión de fuentes primarias y decisiones de planificación; sin instalaciones, inferencia, implementación o mensajes a otras tareas. La pausa se mantiene.

## Dictamen y regla de adopción

Los objetivos permiten preparar la implementación incremental del autoestudio. No hacen falta más rondas de auditoría global ni volver a decidir actividad, modalidad, quién evalúa, orden de desarrollo o significado del salto.

Preferir componentes y algoritmos existentes con documentación y mantenimiento. Distinguir tres decisiones: seleccionar una técnica establecida; conectarla de forma reversible; activarla si supera criterios prospectivos en ORALIA. Una técnica contrastada no se vuelve automáticamente superior con estos datos, y un paquete instalado no cuenta como capacidad validada. Si funciona y satisface calidad, coste y privacidad, se utiliza; no se reconstruye una alternativa propia equivalente.

## Matriz de decisiones técnicas

| Pieza | Decisión para el desarrollo | Evidencia de funcionamiento necesaria |
|---|---|---|
| FastAPI, Pydantic, SQLAlchemy/Alembic y aplicación actual | Reutilizar. Conservar monolito modular y contratos. | Recorridos nuevos e invariantes afectados, sin migración de plataforma. |
| Extractores PDF/DOCX/PPTX existentes | Reutilizar donde sean fieles; no reprocesar por moda. | QA contra originales en fuentes activadas, con tablas/encabezados y páginas sin texto identificados. |
| Docling/OCR | Adaptador focal para páginas relevantes que los extractores no resuelvan. No desarrollar OCR propio. | Comparación contra original, calidad y coste; revisar código/pesos/condiciones y versiones antes de instalar. |
| Fragmentación | Unidades de búsqueda ajustadas al tokenizer, enlazadas a páginas/secciones completas para ampliar contexto. Conservar posición y tablas. | No truncamiento inadvertido; recuperar información al final del fragmento; trazabilidad y contexto relevante. No tamaño fijo universal ni páginas enteras por obligación. |
| Recuperación léxica | Comparar BM25 existente en biblioteca mantenida frente al conteo léxico propio actual. Este último queda como baseline, no como arquitectura definitiva. | Preguntas técnicas, siglas y términos exactos; omisiones y rankings. No instalar Elasticsearch para un corpus pequeño si basta una biblioteca local. |
| Recuperación semántica | Conectar Sentence Transformers y Chroma ya presentes detrás del puerto común, con fingerprint. | Paráfrasis y español/inglés, referencias relevantes y filtros de acceso equivalentes. El checkpoint actual no queda aprobado por ser multilingüe. |
| Unión de recuperación | Usar Reciprocal Rank Fusion (RRF) como primera combinación estándar a comparar; deduplicar por identidad de unidad. | Mismo corpus/consultas, referencias alcanzables y coste; no sumar scores léxicos y vectoriales incompatibles. Registrar límites de candidatos y constante de fusión. |
| Reranking | CrossEncoder multilingüe como candidato después de medir recall de candidatos. Reutilizar implementación, no crear otro juez por prompts para ordenar pasajes. | Mejora del orden sin perder evidencia complementaria y con latencia tolerable; comprobar licencia/ventana/checkpoint. Si no mejora, se omite. |
| Contexto y elipsis | Mantener la entrada original y construir una consulta de búsqueda con referente explícito de lo mostrado. Separar la consulta de la respuesta al alumno. | «¿Por qué?», rectificaciones y cambio de tema. Si una reescritura requiere LLM, evaluar que no inventa intención; no hacerla obligatoria si reglas de estado bastan. |
| Generador | GenerationPort y runtime actual primero; comparar capacidad con configuración efectiva. No desarrollar o entrenar otro modelo desde cero. | Evidencia fija y RAG por separado; español, conceptos próximos, paráfrasis, ficción coherente y episodios completos. No elegir únicamente por tamaño. |
| Formato estructurado | Host calcula IDs, posiciones y contadores. Decoder finito actual cuando basta; XGrammar/backend mantenido solo si se requieren esquemas generales. Explicación libre sin JSON obligatorio. | Contrato/tokenizer/EOS, ausencia de campos redundantes y no fallback silencioso. Un formato correcto no acredita significado. |
| Revisión del contenido | Política compuesta: autoridad/procedencia deterministas, señales de respaldo calibradas y evaluación de pertinencia/cobertura por separado. LettuceDetect es candidato concreto; RefChecker referencia de diseño. | Positivos y negativos nuevos, transferencias, falsos permisos y rechazos; premisas ficticias permitidas. Ningún detector se adopta como árbitro universal por su benchmark. |
| Estado de sesión y examen | Máquina de estados explícita en el host, transiciones idempotentes y versión de configuración. Reutilizar servicios existentes. | Preguntas pendientes, ronda/vuelta, ayudas, reintentos/cancelación, consentimiento y cierre. El LLM no elige autoridad, cupos ni corrección del alumno. |
| Métricas y datos | Eventos tipados, recuentos y métricas de IR existentes. No construir un clasificador LLM para contar mensajes. | Denominadores y categorías claros; acceso y conservación. Conceptos sin clasificar permitidos; frecuencia no implica aprendizaje. |

## Fuentes primarias verificadas

- [Sentence Transformers: Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html): recuperación de candidatos y CrossEncoder posterior. Se toma el flujo, no sus tamaños de ejemplo como configuración obligatoria.
- [Elasticsearch: similarity settings](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity): BM25 como modelo de ranking con saturación de frecuencia y normalización por longitud. Referencia del algoritmo, no propuesta de desplegar ese servicio.
- [Microsoft: RRF](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking): combinación por posición de rankings. Puede aplicarse localmente; no exige Azure ni abrir red.
- [Sentence Transformers: evaluadores](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html): reutilizar métricas de recuperación cuando corresponda. Calidad de búsqueda no equivale a calidad académica de la respuesta.
- [Docling](https://github.com/docling-project/docling): parser estructural/OCR reutilizable. Sus capacidades declaradas no garantizan extracción correcta de nuestras diapositivas.
- [XGrammar](https://github.com/mlc-ai/xgrammar): infraestructura mantenida de generación restringida; no resuelve veracidad ni pedagogía.
- [LettuceDetect](https://github.com/KRLabsOrg/LettuceDetect) y [checkpoint español EuroBERT](https://huggingface.co/KRLabsOrg/lettucedect-210m-eurobert-es-v1): detector especializado; la ficha española advierte incompatibilidad con Transformers 5 y uso de código remoto. Requiere entorno/versiones revisados y no debe alterar el runtime actual para probarlo.
- [RefChecker](https://github.com/amazon-science/RefChecker): descomposición y contraste con límites publicados de cobertura, contexto y evidencia distribuida. No repetir la restricción de una sola línea por conclusión.

## Flujo de trabajo seleccionado

1. Inventariar y revisar fuentes concretas, metadatos, duplicados, versión y contenido utilizable. Activar solo documentos revisados; cobertura y cuarentena visibles.
2. Crear representaciones de búsqueda con procedencia y espacio vectorial identificados. Índice aislado para cada comparación relevante; no mezclar vectores por compartir dimensión.
3. Resolver controles operativos con el host. Para pregunta académica, mantener original/referente y recuperar solo material autorizado; comparar léxico, denso e híbrido.
4. Reordenar candidatos si el reranker aporta valor, ampliar al contexto necesario y deduplicar. Registrar qué se perdió por filtros, ranking o presupuesto.
5. Resolver alcance/suficiencia sin equiparar ausencia de resultados con fuera del curso. Si hace falta, una ampliación local acotada y registrada; conflictos y falta persistente se explican sin inventar.
6. Generar borrador con contexto y conversación mostrada; diferenciar principio documental y ejemplo ficticio sin obligar a un formato burocrático.
7. Aplicar revisión del texto final y controles de vigencia/permiso. Un fallo produce un límite o intento nuevo conforme a presupuesto, no reparación oculta ni cierre innecesario.
8. Entregar texto autorizado y fuentes legibles; confirmar lo mostrado antes de incorporarlo al historial. Mantener consentimiento, cancelación e idempotencia.
9. Verificar técnicamente y entregar cada incremento al usuario con guion breve y límites. Incorporar su feedback antes de promover o acumular cambios que afecten su prueba.

La evaluación usa baseline, variantes comparables y controles nuevos separados del desarrollo. Para búsqueda: recall de candidatos y métricas de orden como nDCG/MRR cuando el oráculo lo permita, pertinencia, volumen y tiempo. Para generación: fidelidad, cobertura de la duda y utilidad de la explicación. Para revisión: falsos permisos, falsos rechazos y omisiones. Para conversación: continuidad y finalización. No colapsar todo en una puntuación sin interpretación ni usar el mismo modelo como única fuente de verdad.

## Técnicas que no se incorporan ahora

- GraphRAG, grafos ontológicos exhaustivos, equipos adicionales de agentes y arquitecturas distribuidas: sin necesidad demostrada en este piloto.
- HyDE, expansión mediante respuestas hipotéticas y múltiples consultas generadas por defecto: añaden contenido/modelos y dificultan atribuir resultados antes de tener un baseline híbrido medido. No son técnicas refutadas; se aplazan.
- Fine-tuning o entrenamiento de un verificador propio: antes deben existir datos/oráculos fiables y una limitación que lo justifique.
- Autocrítica del generador como único gate, overlap léxico como verdad, citas como certificado, votación de jueces como sustituto de calibración: insuficientes para la función que se pretende.
- Más iteraciones sobre los mismos controles expuestos para ajustar prompt o modelo; sumar repeticiones greedy como observaciones independientes.
- Voz, búsqueda web durante sesiones y nube: no necesarias para la primera versión por chat. La investigación y preparación documental web sí están autorizadas.

## Ambigüedades restantes: no requieren otra auditoría global

| Punto | Tratamiento antes de su incremento |
|---|---|
| Borrador, envío y cambio de respuesta | Decisión confirmada: botón de envío en chat y botón de fin de respuesta también en la futura voz. Texto exacto, sin edición automática; ni silencio ni modelo confirman. Volver a una pregunta aplazada no autoriza modificar una ya confirmada. |
| Límite entre aclaración y solución | Tipos confirmados: reformular; enmarcar en tema/apartado real; nombrar conceptos similares sin explicarlos; proporcionar ejemplo. Mantener propósito de la pregunta, sin resolverla ni evaluar al alumno. Probar los cuatro tipos en I6 y aplicar la configuración docente. |
| Ayuda producida pero no recibida | Conservar identidad de la ayuda válida generada y el consumo una vez; retransmitir esa misma ayuda al reconectar. Si el contenido no puede conservarse por consentimiento, declarar la limitación y no generar/cobrar otra ayuda silenciosamente. |
| Aplazamiento repetido y cierre | Se conserva la cola y la voluntad del alumno de continuar o cerrar; no se marca incorrecta ni se entra en un bucle automático. No añadir un límite de aplazamientos sin decisión docente. |
| Datos descriptivos | Permiso previsto para conservar datos de informes, salvo audio. Definir mensaje/pregunta/concepto, multi-etiqueta y categorías no clasificadas. Materializar consentimiento/configuración de la actividad sin modificar sesiones históricas; no almacenar audio tampoco en logs, temporales o exportaciones de la futura voz. |
| Parámetros experimentales | Fijar checkpoint, revisión, tamaños, umbrales y presupuesto en la ficha del ensayo, antes de ejecutarlo. Son decisiones técnicas prospectivas; no pedir al usuario escoger hiperparámetros ni inventar tolerancias ya aprobadas. |
| Latencia y aceptación humana | Presentar tiempos y límites en las primeras pruebas del autoestudio para decidir tolerancia de uso. No convertir un deadline técnico histórico en requisito pedagógico. |

Estos puntos no impiden preparar corpus, comprobar base ni construir el primer autoestudio de laboratorio. Sí deben resolverse y probarse antes de activar la capacidad afectada. Los gates de publicación y el consentimiento no se reemplazan por la aprobación de una biblioteca.

## Condición concreta para integrar y conservar una técnica

Ficha mínima: problema que resuelve; recurso/biblioteca/revisión; licencia y compatibilidad; baseline y casos nuevos; beneficio esperado y límites aceptables; coste de recursos; criterio de rechazo; raíz aislada; reversión. Comparar una causa por vez cuando sea posible. Si mejora la capacidad requerida sin una regresión material o coste incompatible, se conserva y se entrega en el incremento correspondiente. Si no funciona, se registra el resultado y se omite: no obliga a desarrollar desde cero un reemplazo.
