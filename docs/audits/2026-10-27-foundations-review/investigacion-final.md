# Investigación primaria de fundamentos y alternativas

Consulta realizada el 27 de octubre de 2026. Se buscaron problemas generales y métodos técnicos, sin subir documentos, rutas o conversaciones privadas. No se instalaron dependencias ni descargaron pesos. Los resultados publicados no se presentan como validación de ORALIA.

## Aprender no equivale a recibir ayuda para contestar

[Bastani et al., PNAS, 2025](https://doi.org/10.1073/pnas.2422633122) estudian dos diseños de asistencia en matemáticas. Sus resultados distinguen desempeño con ayuda y desempeño independiente posterior; el diseño pedagógico cambia el efecto. La variante protegida recibe soluciones y errores frecuentes preparados por docentes, por lo que no prueba directamente el tutor local solicitado, que debe generar desde RAG sin respuestas predefinidas. Hay [código y datos de los autores](https://github.com/obastani/GenAICanHarmLearning); no hace falta importar conversaciones estudiantiles para adoptar el diseño experimental. El artículo tiene condiciones CC BY-NC-ND; las licencias de código y datos concretos deben comprobarse antes de reutilizarlos.

[Kestin et al., Scientific Reports, 2025](https://www.nature.com/articles/s41598-025-97652-6.pdf) informa un resultado favorable de un tutor basado en prácticas pedagógicas en un ensayo universitario. El buscador permitió consultar título y resumen; la apertura completa fue rechazada por la pasarela de Nature. No se atribuyen aquí magnitudes o detalles metodológicos no leídos. Estos trabajos cuestionan tanto «cualquier chat enseña» como «la IA no puede enseñar»: la intervención y la evaluación importan.

**Adaptación propuesta:** objetivo puntual, explicación, adaptación a una dificultad y aplicación nueva sin asistencia. Coste bajo o medio de diseño y revisión docente. Evaluar utilidad del episodio sin notas institucionales ni perfiles persistentes. No imponer preguntas socráticas si el alumno pide una explicación directa, ni impedir avanzar por no acertar. Los estudios no validan español de Ingeniería del Software, NF4 o el hardware local.

## Documentos, contexto y recuperación

[Docling oficial](https://github.com/docling-project/docling), con licencia MIT, ofrece extracción estructurada; su [CLI oficial](https://github.com/docling-project/docling/blob/main/docs/reference/cli.md) distingue OCR, tablas, motores y rangos de páginas. Puede utilizar pipelines locales, pero algunos requieren modelos previos y existen opciones remotas. Para ORALIA conviene un ensayo focal sobre páginas en cuarentena, con coordenadas y revisión contra el original. Coste medio de dependencias, pesos y CPU; GPU opcional por autorizar. Obtener texto no acredita que fórmulas o diagramas estén bien interpretados.

[Contextual Retrieval, Anthropic, 2024](https://www.anthropic.com/research/contextual-retrieval) describe contexto añadido al fragmento y combinación de BM25, embeddings y reranking, con resultados en sus evaluaciones. Su receta con un LLM puede introducir contexto incorrecto. La adaptación más conservadora es recuperar encabezados y jerarquía del original, separar cualquier contexto derivado del texto fuente y comparar estrategias. Puede implementarse localmente mediante los puertos existentes; no requiere una API de Claude. Coste medio. Sus cifras no se trasladan a ORALIA ni demuestran que más contexto corrija el error de A1.

[Corrective RAG, 2024](https://arxiv.org/abs/2401.15884) propone un evaluador ligero de recuperación que activa acciones correctivas e incluye búsqueda web. La separación entre recuperación y juicio de calidad es una hipótesis útil; su rama web no es compatible con el MVP vigente. Probar únicamente recuperación local acotada y señal de suficiencia, sin convertir su score en autoridad de alcance o de publicación. No se verificó aquí un checkpoint compatible y su licencia, por lo que no se recomienda descargarlo.

[GraphRAG, 2024–2025](https://arxiv.org/abs/2404.16130) se centra en síntesis global de corpus grandes mediante grafos y resúmenes generados. No demuestra que esa complejidad resuelva distinciones próximas en tres PDF ni errores con fuentes presentes. Su coste de extracción, resúmenes y procedencia sería alto: no es una carencia obligatoria del proyecto y no se prioriza.

La [investigación previa de esta auditoría](../2026-10-27-global-viability/investigacion.md) verificó implementaciones multilingües BGE y reranking, con licencias MIT o Apache 2.0 según artefacto. La nueva condición previa es corregir identidad de encoder e índice y comparar primero el adaptador multilingüe existente. Un modelo nuevo no resuelve una caché que sirve siempre el primero. La latencia y el coste local siguen por medir; no se cargó ninguno.

## Prevención y revisión semántica

[RefChecker, repositorio de autores](https://github.com/amazon-science/RefChecker), Apache 2.0, y su [paper](https://arxiv.org/abs/2405.14486) ofrecen extracción y comprobación de afirmaciones. [ARES](https://arxiv.org/abs/2311.09476) separa relevancia del contexto, fidelidad y relevancia de respuesta, con calibración humana. Son hipótesis medibles con evidencia en sus benchmarks; no garantías universales.

Para ORALIA hace falta comprobar español, negación, modalidad, premisas de ejemplos y omisiones del extractor. La licencia del framework no cubre necesariamente todos sus modelos. Versión, dependencias, pesos y memoria se fijan por candidata. El coste puede ser medio o alto según el checker; no se presupone que quepa junto al generador en GPU. Un permiso agregado de evaluación no autoriza por sí mismo una respuesta individual.

La prevención también reduce errores: fuentes suficientes, historial separado de autoridad académica, menos afirmaciones innecesarias, premisas decisivas claras y presupuesto suficiente para terminar. No sustituye la revisión posterior. Un filtro que rechaza todo falla utilidad; uno que acepta todo falla seguridad. Definir el riesgo residual aceptable requiere decisión humana; este argumento no rebaja SC-006 ni abre G2.

La [documentación de Transformers sobre cuantización](https://huggingface.co/docs/transformers/v4.32.0/en/main_classes/quantization) explica NF4 y dtype de cómputo. Esa versión antigua se consulta para el mecanismo, no para certificar compatibilidad con 5.5.3; la ruta de esa versión intentada no fue accesible. No hay una ablación local que permita culpar a NF4 o a greedy de las confusiones. Un ensayo de precisión debe mantener el mismo modelo, preguntas, contexto y recursos; cambiar de checkpoint no aísla cuantización.

## Seguridad y privacidad

[OWASP Top 10 para LLM, 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) advierte que RAG no elimina la inyección. La [guía oficial de pruebas](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-6-AI-LLM-Application-Security-Testing/) distingue inyección, exposición, salida insegura y agencia excesiva. La adaptación local es probar cada frontera, mantener autorización fuera del prompt y no conceder al LLM capacidades de red o escritura. Coste bajo o medio. Roles y delimitadores reducen ambigüedad, pero no son aislamiento formal. No añadir un «agente de seguridad» que autorice por opinión ni ejecutar ataques contra servicios habituales.

[SQLite: secure_delete](https://www.sqlite.org/pragma.html) distingue eliminación SQL y residuos; también señala límites del mecanismo. La [documentación de WAL](https://sqlite.org/wal.html) explica archivos adicionales y concurrencia. No se comprobaron residuos reales ni se tocaron bases habituales. Definir la promesa de borrado, inventariar copias y probar una base ficticia tiene coste bajo o medio. Cifrado o eliminación forense requieren amenaza y decisión explícitas; VACUUM no es un remedio universal y puede interferir con actividad local.

## Conclusión de la búsqueda

Prácticas consolidadas: identidad de recursos, autorización fuera del LLM, QA de extracción, estrategias recuperadoras comparables y evaluación de aprendizaje separada de ayuda inmediata. Hipótesis prometedoras: búsqueda autorizada antes de decidir alcance incierto, recuperación híbrida y checker especializado calibrado. Límites abiertos: verificación fiable de texto libre y ejemplos a coste local, transferencia de calibración y utilidad docente completa.

No se ha identificado una solución ya validada que combine todas las condiciones actuales. Eso no demuestra imposibilidad ni autoriza una garantía ideal como requisito humano implícito. El próximo avance debe resolver una incertidumbre concreta, con coste y aceptación definidos antes del ensayo.
