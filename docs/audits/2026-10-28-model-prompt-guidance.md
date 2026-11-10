# Guías oficiales y estrategia de prompts para modelos locales

28-10-2026. Investigación documental y lectura de configuración local; sin pesos, GPU ni modificaciones de producto.

## Fuentes primarias

- Qwen2.5-14B: https://huggingface.co/Qwen/Qwen2.5-14B-Instruct
- Qwen3-8B: https://huggingface.co/Qwen/Qwen3-8B
- Mistral Small 2501: https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501
- Plantillas Transformers: https://huggingface.co/docs/transformers/chat_templating
- Uso Qwen: https://qwen.readthedocs.io/en/latest/inference/transformers.html
- Self-Refine: https://arxiv.org/abs/2303.17651
- RARR: https://aclanthology.org/2023.acl-long.910/
- Límites de autocorrección: https://deepmind.google/research/publications/48252/

Las fichas de los checkpoints exactos prevalecen sobre ejemplos genéricos o modelos recientes del mismo fabricante. Son recomendaciones, no garantía de calidad en español, NF4 o este corpus.

## Comprobación por familia

Qwen2.5 Instruct (1.5/7/14B disponibles): usar plantilla nativa y mensajes system/user/assistant; no añadir tokens de control manualmente. No necesita instrucciones Qwen3 de thinking. El checkpoint local 14B incluye do_sample=true, temperatura0.7, top_p0.8, top_k20 y repetition_penalty1.05. El worker sobrescribe do_sample=false: no debe presentarse como configuración de fábrica. Greedy es un baseline legítimo y reproducible, no un bug demostrado para Qwen2.5; comparar muestreo configurado explícitamente después de depurar el prompt, con semillas/repeticiones y sin seleccionar solo la mejor salida.

Qwen3-8B: ficha distingue thinking y non-thinking. Thinking recomienda temperatura0.6/top_p0.95/top_k20/min_p0 y advierte no usar greedy. Non-thinking recomienda0.7/0.8/20/0. El worker permite únicamente enable_thinking ausente o false; no ofrece perfil thinking explícito. Configuración ausente puede dejar activo el valor por defecto del tokenizer: vincular modo a identidad de modelo y confirmar plantilla efectiva antes de inferir. El worker impone greedy a todas las llamadas, por lo que no sigue la recomendación de muestreo de Qwen3. Esto NO explica automáticamente fallos históricos ni los del14B reciente. El presupuesto de thinking y su salida requieren tratamiento propio; no trasladar ciegamente la recomendación genérica de32768tokens al piloto.

Mistral Small24B2501: plantilla propia V7-Tekken; no reutilizar el formato ChatML de Qwen. La ficha recomienda system adaptado y temperatura baja, por ejemplo0.15. No copiar fechas/identidad del ejemplo general al tutor. Verificar tokenizer/plantilla del snapshot y parche regex existente por separado. No afirmar que se ha evaluado con muestreo0.15: el worker actual fuerza greedy. No activar otro modelo solo por esta investigación.

Transformers: apply_chat_template y add_generation_prompt son apropiados. Cuando se renderiza texto y después se tokeniza, comprobar que no se duplican tokens especiales; usar tokenize=True o add_special_tokens=False según equivalencia del tokenizer. El worker actual usa render→tokenizer sin explicitar false. Es una comprobación CPU pendiente por checkpoint, NO duplicación demostrada. Mantener pruebas de IDs finales, roles, BOS/EOS y prefijo assistant.

## Arquitectura recomendada de instrucciones

1. System estable, breve y específico: tutor de asignatura, base documental, condiciones y límites, ejemplos hipotéticos coherentes, idioma, no calificación del estudiante, seguridad. Definir positivamente cómo tratar evidencia insuficiente y observaciones falibles. No acumular relato del laboratorio, presupuestos o informes dentro de la tarea académica.
2. User con campos inequívocos: pregunta real y referente mostrado si hace falta; fuentes completas pertinentes delimitadas; en corrección, borrador y observaciones atómicas. No envolver todo como pregunta_actual con JSON anidado. JSON no es intrínsecamente malo ni XML universalmente mejor: importa contrato, consistencia y pruebas del mensaje efectivo. Proteger delimitadores y no promover documentos/críticas arbitrarios a system.
3. Una acción por perfil: explicar, revisar o corregir. Generación libre de texto académico; formato estructurado solo para controles/metadatos que lo requieran. Decoder restringido garantiza formato, no pertinencia ni verdad.
4. Corrección: contrastar observaciones con fuentes; sustituir/eliminar el pasaje erróneo, ajustar frases dependientes, preservar contenido correcto y devolver texto coherente completo. No mantener una afirmación falsa y añadir su negación al final. No exigir correcciones opcionales como condiciones de aceptación ni una respuesta docente prefabricada.
5. Revisión posterior completa: cobertura de pregunta, respaldo de afirmaciones, modalidades, coherencia interna, ejemplo/premisas y nuevos errores. Registrar incertidumbre del revisor. Self-Refine/RARR motivan evaluación y revisión, pero no acreditan un verificador local autónomo ni garantizan convergencia.
6. Fuentes visibles desde el host; no obligar al modelo a producir IDs/bibliografía mientras explica. Mantener procedencia exacta interna y no confundir lista de documentos con prueba de respaldo de todas las frases.

## Estrategias a contrastar, no asumir ganadoras

- Zero-shot claro como base; después uno o dos ejemplos de la OPERACIÓN de reparación sobre temas distintos si no incorpora la corrección. No ejemplos con respuesta objetivo ni casos de reserva; su coste y transferencia se miden.
- Reparación localizada cuando el defecto es acotado; generación limpia cuando el borrador ancla errores o la estructura es mala. La comparación003 favoreció L en dos casos, no universalmente.
- Contexto pertinente con condiciones completas, no todo el corpus ni una sola línea. Priorizar fuentes relevantes sin reducir apoyo distribuido; separar omisión de recuperación de mala interpretación.
- No pedir una cadena de razonamiento extensa como garantía de corrección. Solicitar justificación pedagógica y ejemplo útiles; revisión/evidencias internas separadas.
- No variar prompt, muestreo, modelo y recuperación a la vez. No declarar superioridad por un solo caso o por un único muestreo afortunado.

## Orden propuesto

Primero CPU: renderer único optativo de generación/reparación y pruebas del frame/tokenizer real por familia, sin alterar protocolos históricos. Después GPU: mismo14B y configuración greedy para aislar el cambio de prompt, sobre T2 expuesto. Si hay señal útil, comprobar preguntas nuevas. Solo después contrastar el perfil de muestreo propio del modelo con repeticiones y recursos explícitos. Qwen3/Mistral quedan como comparaciones posteriores, con perfiles correctos, sin atribuir su calidad a una configuración común incorrecta. Producto y gates permanecen sin aprobación por esta revisión.
