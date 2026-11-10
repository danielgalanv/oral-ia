# Contrato del piloto

Entrada humana por terminal → autenticación local existente → endpoints de curso/material/actividad/sesión/study-turns y cierre existentes. API ASGI en proceso, sin puerto abierto. No emisión manual de tokens ni override de acceso; no dependencia de tests. Perfil extractive_limited/deterministic; selección material declarada. Semántica didáctica basada en documentos, no reglas de cantidades.

Respuesta: conservar output_text real, sources/version/location, blocked, effective_profile/status, verificaciones y latencias; un HTTP200 no constituye aceptación. La terminal identifica claramente cita extractiva y correspondencia de páginas; no sustituye texto por una explicación propuesta.

Si se amplía proyección: identificador/version separados de material-excerpt/v1, transformaciones cerradas/límites explícitos, offsets/hash del fragmento original y valor. Revalidar fragmentos actuales/curso/actividad/política/recipiente antes de snapshot. Rechazar texto ajeno, fuentes antiguas/desactivadas, exceso de fragmentos, cambios semánticos y falta de permiso. Grounding no se exime. Consentimiento/cierre no dependen de lo que el alumno diga en una respuesta académica.

Documentación de material: cada PDF derivado identifica archivo/hashes, páginas seleccionadas y mapeo local→original. Los textos extraídos no son unidades reviewed. Ejemplos ausentes se anuncian; no generar otros para cubrir una frase.

## extractive-v2

ResponseGeneratorAgent instancia1.1.0 del mismo agente; input opcional material_excerpt_version=2 y student_input real. GenerationConstraints enum1/2 con default1 conserva clientes anteriores. Política material-self-study/v2 opta explícitamente por adaptador determinista primario, sin invocar Ollama aunque esté configurado; v1 no cambia. La proyección identifica bloques literales por etiquetas estructurales/solapamiento; no crea respuestas ni temas académicos por coincidencia con validación numérica.

Comparación cita contexto completo de las dos operaciones (criterios/tareas/riesgos documentados), aportando información distinta en vez de repetir solo la definición. Coherencia/grounding siguen v1 sin modificaciones ni exenciones. Etiquetas de contenido específicas se comparan con palabras completas para no confundir comprensible y comprobable. Consulta corta puede ampliar recuperación con la entrada anterior realmente aprobada; la selección/binder usan la consulta actual y el retriever conserva su umbral y todas las validaciones. Solo las fuentes seleccionadas pasan a generador/verificadores/citas. La política v2 rechaza fallback de vinculación a fragmento entero/proyecciónv1; pruebas negativas lo verifican.
