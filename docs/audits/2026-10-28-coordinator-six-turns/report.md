# Prueba directa del coordinador: guion de seis pasos

28-10-2026. Navegador integrado real, Qwen2.5-14B NF4, RAG denso CPU, corpusv2 existente. No fixture ni selección manual de fuentes. Seis llamadas con cupo nuevo6 y plazo2700s, límites efectivos768tokens/50s. Servicio propio session4939, runner run.py en este directorio, assets aislados e2-invalidated/web-dist. Se reinició expresamente la sesión previa runtime006, cuyo servidor cerró ordenadamente, sin cambiar su evidencia.

## Resultado operacional

|Paso|Pregunta enviada|Resultado|
|---|---|---|
|1|¿Qué diferencia hay entre verificar y validar los requisitos? Explícamelo de forma sencilla.|Respuesta completa y mostrada, cupo1/6.|
|2|Ponme un ejemplo con una aplicación para pedir cita médica.|incomplete_candidate / generation_length_limit.768tokens,45875ms,2845tokens de entrada. Sin respuesta mostrada ni historial nuevo.|
|3 variante accidental|Ponme un ejemplo con una aplicación para pedir cita médica.No entiendo la diferencia en ese ejemplo. Explícamela con otras palabras.|Completa. Error de entrada del coordinador: typeText anexó al texto conservado después del fallo2. NO cuenta como prueba exacta del paso3.|
|4|¿Cómo podría comprobar que una cita se reserva correctamente?|UI informa límite de tokens; sin respuesta mostrada ni historial nuevo. No se conservó en disco su recibo íntegro antes de enviar5. No inventar latencia/tokens exactos.|
|5, cambio de tema marcado|¿Qué significa que un requisito sea realizable y comprobable? ¿Es lo mismo?|Completa y mostrada, cupo5/6, referente nuevo. No invalidated.|
|6|Dame un ejemplo de un requisito realizable pero difícil de comprobar.|Completa y mostrada, cupo6/6 y Enviar deshabilitado con aviso de agotamiento.|

Cuatro salidas mostradas y dos fallos de entrega por longitud. Cinco entradas exactas y una variante accidental; NO seis pasos exactos satisfactorios. El seguimiento3 tampoco puede evaluarse como aclaración de la respuesta2: la respuesta2 nunca se mostró. No se simuló historia ausente ni se repitieron peticiones para hacerlas pasar.

Recibo2 visible y expandido en UI: id ec5681ac-8cf7-4b27-b3fb-c54f266b68a5, finish_reason length, maximum/requested768, capacidad backend2048, perfilstructured/v1, qwen25-14b, didactic study-dialogue/v1, greedy,seed42. La salida bruta termina «- **Requisito 3**: Verificar», después de repetir listas. Esto reproduce un problema real, no un juicio de estilo. Servidor/modelo siguieron disponibles tras ambos límites de longitud. No se prueban con ello las causas de los fallos humanos antiguos: el mensaje invalidated histórico descartó el motivo específico.

## Revisión proporcionada del contenido mostrado

Paso1 explica actividades útiles pero cierra «verificar se centra en la calidad individual ... validar ... conjunto». Problema específico: Procedimiento10 recibido YA verifica calidad del conjunto, mientras Procedimiento12 y Requisitos72 definen validación con necesidades del cliente y no entraron en los cinco pasajes. No tratarlo como redacción imperfecta únicamente: la regla individual/conjunto puede enseñar una distinción equivocada. Hay mezcla de contenidos y recuperación incompleta de una diferencia solicitada. No demuestra fallo universal de fuentes/modelo.

La variante3 repite esa dicotomía y da como posible contradicción «uno requiere ... buscar antes ... otro no lo menciona». El silencio de otro requisito no establece contradicción por sí solo. No se penaliza el ejemplo ficticio; se señala la relación lógica concreta. Esta salida no se usa para concluir sobre la pregunta3 exacta.

Paso5 distingue capacidad de implementación y posibilidad de comprobar con ejemplo2s; explicación básica aprovechable. La frase «después de que el producto final ha sido implementado» limita innecesariamente el momento de comprobación; precisión mejorable. Paso6 da «fácil de usar» y propone30min como medida hipotética: ejemplo útil y admisible, sin exigir protocolo completo ni considerar la cifra una alucinación.

## Fuentes mostradas

1: Requisitos89; Procedimiento11 y10; Requisitos76; NASA208.

3 variante: Requisitos13; Procedimiento11; Requisitos89; NASA208; Procedimiento10.

5: NASA208 y70; Requisitos4.

6: Requisitos20; NASA208/209; Sommerville76.

Recibo2: Procedimiento11; Requisitos13/89; Procedimiento10; NASA208. Contexto4917caracteres, sin omisiones de empaquetado. Candidatos incluían Procedimiento12/Requisitos72, pero no pasaron al contexto. No equivale a fuente ausente del corpus.

## Decisión

No pedir al usuario que repita este guion todavía. Corregir presupuesto efectivo de entrega y extensión requerida de forma coherente (no solo max_tokens): backend permite2048 pero este recorrido sigue768/50s/4000caracteres. Separar mejora de brevedad de necesidad de completar respuesta; nunca mostrar truncada como completa. Preservar configuración fallida y validar perfil sucesor prospectivo con todos los consumidores/deadlines, sin reajustar fuentes manuales por IDs.

Comprobar recuperación de preguntas comparativas y uso contextual de fuentes para verificación/validación antes de presentar una explicación contrastada. No codificar una respuesta docente fija. Reproducir después guion exacto con reemplazo de campo mediante fill, no append. No atribuir a esta prueba un paso3 exacto que no ocurrió ni regenerar inicial histórica.

Se comunicaron hallazgos al escritor de mantenimiento autorizado; no se inicia otra campaña por este informe. Próximo intento debe declarar presupuesto nuevo, conservar este primero y verificar6pasos exactos. Sin cambios de producción del coordinador: run.py solo selecciona assets aislados para el create_app existente. Sin commits, Reset, fuentes/índices ni procesos ajenos.
