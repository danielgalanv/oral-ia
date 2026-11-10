# Auditoría de capacidades del autoestudio (07-11-2026)

Se probó el sistema completo (arranque por defecto: filtro de alcance, recuperación bge-m3 + reranker, generador 14B, revisor 24B, ampliación web permitida) con una batería de 15 conversaciones / 23 turnos (`probe.py`; resultados en `results-antes.json` y `results-despues.json`) y con pruebas dirigidas sobre el filtro de alcance (`judge_*.py`). Una sola alumna simulada; nada de esto sustituye la valoración del docente sobre calidad académica.

## Qué hace y cómo
1. **Filtro de alcance** (14B, decisión cerrada): la pregunta debe encajar en seis conceptos autorizados; si no, se rechaza o se pide aclaración.
2. **Recuperación**: pasajes del material (9 documentos, 117 páginas) con bge-m3 y reranker; la pregunta anterior se concatena en los seguimientos.
3. **Generación** (14B): respuesta en español, con ejemplos hipotéticos identificados, "Palabras clave" y fuentes; ve los últimos tres intercambios.
4. **Revisión** (24B): contradicciones, conceptos confundidos o atribuciones no respaldadas generan un aviso fijo; la respuesta se muestra siempre.
5. **Ampliación web**: solo si el material no basta, solo páginas permitidas por el docente, con controles de apoyo y compatibilidad.

## Resultados de la batería (después del arreglo del alcance)
| capacidad | resultado |
|---|---|
| Definiciones, comparaciones, preguntas compuestas, resúmenes, preguntas con dato exacto | responde bien y fundamentado en 6–14 s |
| Aplicar a un caso propio (app de pádel) | correcto, con ejemplos de redacción |
| Preguntas en inglés | responde en español |
| Premisa falsa ("¿por qué no importan los no funcionales?") | la corrige con las fuentes |
| Petición de ejemplo, otra explicación, tema nuevo | funciona |
| **Seguimientos** ("¿qué técnicas incluye?", "dame un ejemplo de eso") | **fallaban 2 de 4**; arreglado (ver abajo) |
| Fuera de alcance (Singleton, tortilla, Scrum) e intento de ver el prompt | rechazo correcto y rápido (1 s) |
| Pregunta ambigua ("¿qué significa eso?") | pide aclaración |
| Comprobar la propia comprensión ("¿está bien lo que he dicho?") | 3 de 4 admitidas; una rechazada como fuera de alcance |
| Algo que el material no cubre (blockchain) | se rechaza como "fuera de contenidos"; no dice que el material no lo trata |
| Pedir un ejercicio de test | lo genera, pero sin garantía de que la clave sea correcta (ver riesgos) |

Avisos del revisor en los 23 turnos: ninguno.

## Hallazgo principal y arreglo
Al pasar los controles al 14B (medido con preguntas sueltas: 10/10 dentro y 5/5 fuera) se perdió la comprensión de los seguimientos: con el historial completo, el juez solo admitía el **44 %** (24/54) de seguimientos válidos, frente al 85 % del juez anterior (Qwen3-8B con razonamiento). Corregido en `StudyWebFlow.judge_scope`: se juzga primero la pregunta sola y, solo si "necesita contexto" (`unknown`), la pregunta anterior más la actual sin historial. Medido con el muestreo real del chat: seguimientos admitidos 36/42 (86 %), fuera de alcance admitidas por error 0/42 (incluida "Cambiando de tema: SQL" justo tras un turno válido), preguntas sueltas 10/10 y 5/5. En la batería real, 13 → 15 respuestas útiles de 23. Se añadió además al criterio de alcance que comprobar la propia comprensión de un concepto forma parte del alcance (comprobaciones propias: de 2/4 a 3/4).

## Límites y riesgos que quedan
1. **El filtro de alcance es un modelo sin razonamiento**: en los casos límite es frágil (p. ej. un enunciado incorrecto del alumno se rechazó). Cada rechazo indebido es una frustración que el alumno no puede arreglar.
2. **Mensaje de rechazo único**: "fuera de los contenidos habilitados… no necesitas estudiar ese tema" se usa tanto para un tema ajeno como para un tema válido que el material no cubre; el segundo caso debería decir que el material no lo trata y ofrecer reformular.
3. **Ejercicios generados sin comprobar**: la pregunta de test con cuatro opciones daba como correcta una opción que es un requisito de rendimiento (no funcional), con otras opciones también no funcionales: enunciado ambiguo y clave dudosa, sin aviso del revisor. Los ejercicios no pasan por una verificación propia.
4. **Corpus pequeño y cerrado**: 9 documentos, seis conceptos, tablas y figuras con limitaciones; fuera de ahí el sistema rechaza o no sabe.
5. **Revisor**: cobertura sobre errores reales desconocida (24 respuestas revisadas por el docente, todas buenas salvo inyecciones); falsas alarmas ~2 %.
6. **Fuentes por respuesta, no por afirmación**: el alumno no puede ver qué fuente respalda cada frase.
7. **Memoria**: tres intercambios; no hay seguimiento del progreso ni continuidad entre sesiones (por diseño: sesión efímera).
8. **No evalúa al alumno** por diseño (las instrucciones lo prohíben); la comprobación de comprensión ya se admite, pero la respuesta no está medida.

## Mejoras propuestas (por orden)
1. Mensajes distintos para "tema ajeno" y "tema válido que el material no cubre".
2. Medir el filtro de alcance con un conjunto etiquetado por el docente (preguntas reales de alumnos: dentro, fuera, seguimientos, comprobaciones, límites) y decidir el umbral aceptable de rechazos indebidos.
3. Decidir el papel de los ejercicios: restringirlos, o que el revisor los compruebe contra las fuentes antes de mostrarlos.
4. Medir cuánto del temario real (preguntas de examen o de clase) cubre el corpus.
5. Respuesta en streaming antes de la revisión (ver `docs/audits/2026-11-07-pre-exposure/AUDITORIA.md`, E1), que además es la mejora de experiencia más grande.

## Replanteamientos a considerar
- **Filtro por relevancia en lugar de por lista de conceptos**: usar la puntuación del reranker (ya calculada en cada consulta) para decidir "el material trata esto" frente a "no", y dejar el juez de conceptos solo para casos dudosos. Habría que medirlo; reduciría rechazos indebidos y daría un criterio objetivo para "no cubierto".
- **Postura sobre evaluar al alumno**: hoy el sistema explica pero no corrige lo que el alumno escribe; es la función de estudio más pedida (comprobar si he entendido). Es una decisión docente, no técnica.

## Actualización: mensajes de rechazo (07-11-2026, después de la auditoría)
- `scope_outside` ya no dice "no necesitas estudiar ese tema": «No he encontrado esa cuestión entre los temas de esta actividad: … Si crees que sí encaja, reformula…».
- Nuevo `material_not_covered` («El material de la asignatura que tengo no trata esto. No quiero inventarlo…»): en la primera pregunta de la sesión, si el mejor pasaje recuperado tiene probabilidad del reranker < 0,3, no se genera. Calibración (`calibrate_relevance.py`, `relevance.json`): 215 preguntas respondibles ≥ 0,93; las de la batería real respondibles ≥ 0,77; ajenas ≤ 0,06; en tema pero no cubiertas: 9 de 20 por debajo de 0,5 (el resto obtiene 0,7–0,98 porque hay páginas del tema, p. ej. "blockchain"; esas siguen dependiendo del filtro de alcance). No se aplica a seguimientos: una pregunta como «¿qué técnicas incluye?» recupera mal por sí sola (un primer intento con la puerta en todos los turnos la rechazó y se corrigió).
- Probado en el chat real: seguimientos respondidos, DO-178C → "el material no trata esto", Singleton/tortilla/Scrum/blockchain → mensaje nuevo de alcance.
- Hallazgo: con material recuperado, el flujo actual (modo aviso) nunca amplía con web (`local_first` con evidencia); las respuestas con "nasa-handbook" salen de páginas archivadas en el propio corpus, no de una consulta en vivo. La ampliación web real solo ocurre si no hay evidencia local.

## Estudio de la ampliación web real (07-11-2026)
- **Qué permite la política** (`config/requirements-study-policy.json`): solo 4 páginas concretas (2 del manual NASA —definición de requisitos técnicos y gestión de requisitos—, el suplemento del libro de Sommerville sobre el estándar IEEE de requisitos y el manual STSE de St Andrews sobre elicitación), máximo 2 búsquedas, 3 páginas y 60 s.
- **Lo que el corpus ya tiene**: el manual NASA completo (mismas dos secciones) y una captura de SWE-055. **No tiene** el suplemento IEEE ni el manual STSE: son las dos únicas fuentes que la web aportaría, y el caso del IEEE 830 (atribución errónea) es justo una pregunta que esa página respondería.
- **Hoy no se usa**: con material recuperado no se amplía; sería necesario reencaminar el flujo (decidir cuándo "el material no basta") y conectarlo al modo aviso.
- **Coste de activarla**: red en tiempo de clase, descargas en vivo (la medición histórica fue de ~339 s por ampliación; no medida con la pila actual), y contenido que solo pasa controles automáticos del 14B (probados con datos sintéticos), no la revisión página a página que tiene el corpus.
- **Alternativa recomendada**: capturar esas dos páginas una vez y añadirlas al paquete documental como se hizo con SWE-055 (revisadas por el docente, con hash y sin red en clase). Gana: respuesta correcta a IEEE y elicitación, sin latencia ni dependencia de Internet. Requiere descargar las dos páginas (HTML, tamaño pequeño; necesita tu autorización) y pasar el proceso de construcción del paquete (`scripts/prepare_requirements_corpus.py`, `scripts/review_requirements_corpus.py`, `scripts/assemble_requirements_block.py`) con revisión del docente.
