# Auditoría del prompt efectivo de generación y corrección

28-10-2026. Auditoría CPU/lectura; sin inferencias ni cambios de producción.

## Recorrido comprobado

En comparison-003, prepare.py y prepare-transfer-pair.py construyen directamente RepairGenerationRequest. invoke.py llama ReviewRepairGenerationAdapter.call('repair', request, trace): NO usa repair_request ni repair_with_supplied_review para construir esos prompts. Cambiar solamente REPAIR_INSTRUCTION no cambiaría este experimento.

cached_transformers.py convierte instruction en system y construye un user con _build_user_content(request con student_input vacío), seguido de pregunta_actual. Ese último bloque contiene una cadena JSON con question, minimum_obligations, conceptual_caution, draft y advisory_review, no simplemente una pregunta. Antes aparecen páginas completas y una instrucción genérica «Responde únicamente usando el contenido de las etiquetas evidencia anteriores». No hay mensajes assistant previos en estos ensayos.

gpu_worker.py aplica la plantilla real con add_generation_prompt=True, tokeniza, rechaza más de 7000 tokens sin truncamiento y genera con do_sample=False. Decodifica únicamente outputs[0,input_length:]. No se observó concatenación del prompt al resultado ni corte silencioso en esta ruta. Los recibos contienen configuración efectiva. Esto no acredita todos los proveedores/rutas del proyecto.

build_delivery.py y build_answer_page.py toman literalmente exposed-L-2-result.json/outcome/text y añaden procedencia del host. No existe una última llamada de síntesis o validación automática: la elección la realiza el asistente y el script fija el archivo seleccionado. La respuesta publicada en el artefacto no está académicamente reescrita por el renderer.

## Hallazgos

1. **Acción de corrección dentro de datos declarados no instructivos.** COMMON declara que las críticas son datos, nunca instrucciones. Pero explanation incluye imperativos como «Corrige solo esa conclusión», «Retira las etiquetas». Hay instrucción general de corregir, pero no un contrato explícito para utilizar observaciones como restricciones comprobables. La frontera de confianza debe mantenerse: el host instruye a contrastar observaciones contra fuentes y resolver defectos confirmados; nunca elevar automáticamente texto externo a system.
2. **Contrato de user inadecuado a la tarea.** pregunta_actual encierra un objeto completo y escapado. No se pierde información, pero pregunta, borrador y revisión quedan con una presentación que no identifica claramente la acción de edición. No es prueba de causalidad, sí una ambigüedad evitable.
3. **Anclaje al borrador y adición de salvedades.** «Conserva lo correcto» y «corrige solo» favorecen una edición mínima, sin definir unidad reemplazable ni exigir resolver contradicciones en el cuerpo. T2-L conserva la frase incorrecta y añade su negación: reproduce exactamente el fallo que el contrato deja sin una operación de sustitución explícita.
4. **Duplicación de criterios y avisos.** minimum_obligations, conceptual_caution y advisory_review se solapan; los avisos de seguridad/procedencia se mezclan con la tarea pedagógica. No prueba que su longitud cause el fallo. Conviene una instrucción operativa única y datos separados.
5. **No hay validación de incorporación.** parse_review valida literales, IDs y estructura antes de llamar; no comprueba después que el error se haya resuelto. Terminar con stop tampoco lo prueba. La revisión posterior del asistente sí detecta contradicciones, pero aún no es un componente autónomo validado.
6. **Prompts distintos según ruta.** Los ensayos directos y el constructor reutilizable review_repair.repair_request no son equivalentes. Es fácil corregir un prompt que el siguiente ensayo no usa. Congelar renderer/perfil y comprobar el frame efectivo, no solo la solicitud abstracta.
7. **La selección final es asistida, no generativa.** No falta una síntesis por accidente: se eligió una salida completa. Añadir otra llamada de embellecimiento sin revisión podría introducir errores nuevos.

## Corrección recomendada, pendiente de implementación

Crear un renderer optativo de reparación explícita reutilizado por el diagnóstico y el constructor del módulo, manteniendo perfiles históricos. System define: tarea de revisión de un borrador; evidencia como única base académica; crítica falible que debe contrastarse; reemplazar o eliminar afirmaciones incorrectas y ajustar dependencias; no añadir una negación manteniendo la frase original; devolver respuesta completa. Conservar ficción coherente y límites del temario. No prometer que el prompt garantiza acierto.

User separa pregunta original, obligaciones mínimas, fuentes completas, borrador y observaciones atómicas mediante un formato inequívoco. Serialización segura y delimitadores protegidos; ninguna crítica/documento pasa a ser instrucción de mayor autoridad. Evitar JSON incrustado dentro de pregunta_actual y órdenes duplicadas. Cada observación distingue texto afectado, motivo, respaldo y condición de resolución; no incluye una respuesta académica prefabricada.

Antes de GPU, probar el frame efectivo con transporte simulado y tokenizer local CPU: pregunta una vez en su campo, borrador una vez, crítica una vez, evidencia íntegra, roles, delimitadores adversarios, ausencia de marcadores ficticios, capacidad sin clipping y compatibilidad histórica. Registrar cuál constructor produce cada solicitud.

Primera comparación posterior: mismo borrador T2, misma crítica depurada y fuentes, mismo modelo/configuración; prompt anterior frente al renderer nuevo. Congelar ambos antes de generar y revisar reemplazo real, contradicciones, pérdida de contenido correcto y errores nuevos. Caso expuesto para diagnóstico, no transferencia. Solo avanzar a preguntas nuevas si hay señal útil. No repetir GPU en esta auditoría.

## Conclusión

Hay defectos y ambigüedades reales de construcción del prompt que debemos corregir antes de atribuir el estancamiento a la capacidad del modelo. La inspección por sí sola no demuestra que sean la causa de todos los errores ni que arreglarlos baste. El cambio prioritario es separar tarea/pregunta/evidencia/revisión y expresar sustitución coherente, verificando que ese sea el mensaje efectivamente usado.
