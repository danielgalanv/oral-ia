# Auditoría y rectificación de la evaluación de respuestas

28-10-2026. Auditoría del coordinador tras objeción docente. Sin GPU, producción ni cambio de estados SpecKit. Este documento rectifica conclusiones; no modifica recibos históricos.

## Alcance leído

comparison-003: criterios expuestos/transferencia, revisiones iniciales T1/T2, contraste final expuesto, final-verdict y respuesta final. iteration-002: review-after-001 y rectificación final. structured-prompts: renderer, contrato, mensajes/solicitud nueva, respuesta completa, revisión y final-selection. Constructor/validador review_repair. No revisión retrospectiva exhaustiva de toda Feature012 ni adjudicación automática de todos los rechazos anteriores.

## Conclusión

Los mínimos de pregunta no son imposibles: existen respuestas aceptadas por el mismo procedimiento. Sin embargo, la aplicación del criterio fue excesivamente severa, cambiante y sin calibrar. En varios puntos se exigió más que una explicación docente útil. El revisor contribuyó al bloqueo experimental; las conclusiones negativas sobre el modelo basadas en esos juicios no quedan acreditadas por esa evaluación.

## Defectos comprobados

1. Falta de gravedad/materialidad. Issue tiene kind/claim/explanation/evidence, pero no diferencia error que altera aprendizaje de ambigüedad leve o mejora opcional. issues_found dispara reparación en la vía automática, aunque el tipo sea ambiguity. Esto es una política de reparación, no una demostración de que todo hallazgo deba bloquear la respuesta. La aprobación experimental la decidió el asistente, no ese validador por sí solo.
2. Exhaustividad sobrevenida. iteration-002/review-after-001 exige excepción NASA auto-derivada y vuelta prueba→requisito aun después de retirar la afirmación universal que justificaba la excepción. comparison-003 luego retira esa exigencia. El criterio fue ampliado durante la revisión y relajado más tarde: no se puede comparar el número de fallos como si el umbral hubiera permanecido fijo.
3. Contextualización desigual. En expuesto L2 se lee «asegurando ... origen claro» como finalidad, no garantía universal; en R2 se leen otras fórmulas como garantía literal. Algunas diferencias pueden justificarse por contexto, pero faltó una regla explícita y una valoración simétrica. No aceptar/rechazar por las palabras «asegura» o «garantiza» aisladas.
4. Lectura adversarial. En T2 se convirtió «detalles de diseño innecesarios, como filtros...» en regla universal sobre todo filtro, sin ponderar suficientemente el ejemplo donde ya se había delimitado buscar por nombres/descripciones. La lectura docente razonable permite entender «no añadir funcionalidades no solicitadas». Es terminología mejorable, no falsedad académica demostrada del conjunto.
5. Prueba de apoyo desigual. Una cita literal valida procedencia, no demuestra contradicción ni que algo sea indispensable. Una fuente que admite entradas/salidas no prueba por sí sola que el cierre del ejemplo tenga la interpretación universal imputada.
6. Sesgo de confirmación en reparación. El revisor buscó que desapareciera la frase señalada. Cambiar la ubicación del texto se contó como persistencia de error sin volver a comprobar que la crítica inicial fuera necesaria para la pregunta. No se había calibrado el falso rechazo del propio revisor.
7. Confusión entre aceptable y excelente. Repetición, precisión terminológica fina y falta de detalles avanzados contribuyeron a juicios binarios sobre adecuación. Una explicación breve no necesita cubrir todo el documento ni anticipar todos los contraejemplos.

## Rectificaciones prospectivas y retrospectivas acotadas

- T2 structured-prompts/new: aceptable para la pregunta bajo lectura contextual del ejemplo, con mejora opcional de terminología en cierre. Es la adjudicación actual del coordinador apoyada en la observación docente. No equivale a validación general del tutor ni a respuesta perfecta.
- Se retira «fallo conceptual persistente demostrado» como conclusión de ese caso. La parada y las llamadas ocurrieron y se conservan; su motivación dependió de una adjudicación demasiado severa. No se declara ahora demostrada superioridad de la estructura nueva ni se inventa transferencia no ejecutada.
- comparison-003/T2 y sus iniciales requieren nueva lectura contextual antes de contabilizarse como fallos. No se convierten todos automáticamente en éxitos: cada versión tiene texto distinto.
- T1 garantía de cumplimiento y expuesto independencia/objeto de revisión siguen siendo objeciones plausibles de contenido; no quedan confirmadas simplemente por esta auditoría. Deben juzgarse con materialidad y contexto. En T1, definir medida no demuestra cumplimiento: si el cierre realmente enseña esa inferencia, hay motivo de corrección; si solo expresa finalidad, mejora de redacción.
- Falta de IDs, longitud/formato o fallo de transporte se registra separado de corrección académica. Una salida truncada puede ser incompleta, pero no se convierte por ello en falso contenido.

## Política propuesta: aceptación proporcionada al piloto

Evaluar la respuesta de ORALIA, nunca al estudiante. Sin notas ni rúbricas del alumno.

Estados distintos:
- Aceptable: responde lo principal y es utilizable; admite mejoras menores.
- Necesita corrección: error material o carencia esencial identificada.
- No determinable: evidencia insuficiente/conflicto o duda del revisor; no etiquetar falsa.

Anotar calidad didáctica aparte: claridad, extensión, continuidad, ejemplos. No exigir excelencia para aceptar corrección académica.

Para bloquear por contenido, el revisor debe identificar: texto/contexto completo; interpretación que realmente transmite; evidencia o razonamiento que la refuta; impacto concreto en comprensión; y por qué una lectura razonable del conjunto no resuelve la objeción. La falta de certeza del revisor no demuestra error. Una afirmación académica central sin apoyo suficiente puede exigir cautela/recuperación, pero no se debe decir que es falsa solo por ausencia en el pasaje.

Una omisión bloquea solo si impide contestar una parte esencial solicitada o vuelve engañosa la explicación. Ejemplo ficticio plausible no requiere detalle exhaustivo ni literalidad documental. Matices opcionales y excepciones no activadas por lo afirmado no son cobertura obligatoria.

Evaluar primero el conjunto en lectura docente natural y después afirmaciones específicas. Considerar las salvedades del conjunto; una salvedad no salva una contradicción inequívoca, pero sí puede aclarar una formulación general de finalidad. No buscar interpretaciones rebuscadas para aprobar ni para rechazar.

Corregir lo necesario; no entrar en bucle por estilo. Si una crítica se retira, preservar antes/después y revisar conclusiones derivadas. La comparación debe usar el mismo umbral en todas las ramas y señalar cuando cambió.

## Calibración antes de otro ensayo de mejora

Revisar a CPU los textos existentes con esta política: respuestas correctas imperfectas, errores centrales claros (p.ej. invertir qué/cómo), ambigüedades de contexto, ficción admisible y desconocimiento. Registrar falso rechazo y falsa aceptación, además de incertidumbre. Las observaciones del docente son referencia contextual, no etiquetas para entrenar y volver a vender esos mismos casos como transferencia.

El siguiente bloque útil es re-adjudicar las respuestas ya generadas y actualizar mediante un addendum las conclusiones afectadas. No nueva inferencia hasta saber si estábamos intentando corregir respuestas ya aceptables. Implementación posterior de gravedad/materialidad solo con pruebas y sin convertir la estructura del contrato en verdad semántica.

Separar aceptación local para revisión docente, permiso del experimento, requisitos de privacidad y publicación: mantener estados de producto no es prueba de incorrección académica ni implica exigir garantía universal para el piloto. Replantear cualquier gate que se interprete así en su propio alcance documental, no abrirlo automáticamente con este informe.
