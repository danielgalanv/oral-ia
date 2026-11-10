# Arquitectura recomendada y transición

No se recomienda reemplazar el proyecto. Mantener el monolito modular, contratos y almacenamiento local. La arquitectura debe hacer fácil medir una conversación útil y difícil publicar fuera de permiso; no convertir cada hipótesis cognitiva en otro agente obligatorio.

## Flujo propuesto

1. El host autentica, limita recursos y crea una operación idempotente ligada a sesión, actividad y versión. Resuelve controles explícitos y operaciones pendientes sin modelo académico. La memoria distingue intención declarada del alumno de hipótesis de dificultad; estas últimas son locales a la sesión y no son diagnóstico de capacidad.
2. Obtiene una instantánea autorizada de fuentes y política. El alcance determina qué se puede estudiar; el catálogo determina qué material está disponible. Una consulta incierta puede, en la variante experimental propuesta, recuperar de ese catálogo autorizado antes de decidir si genera. Nunca se consulta fuera de permiso ni se toma vacío como exclusión.
3. Un puerto de recuperación devuelve candidatos y trazas con IDs estables y fingerprint de representación. Estrategias léxica, densa y unión híbrida son comparables sobre las mismas unidades. La autorización final sigue en SQL/política, no en metadatos del índice. Medir pérdidas de cada filtro antes de reranking.
4. La planificación de respuesta registra pocas obligaciones observables: pregunta concreta, referente, qué explicar y qué límite expresar. No necesita un plan simbólico exhaustivo del curso. La evidencia entregada conserva encabezado, ubicación y relación de tabla/lista; las adiciones contextuales derivadas se etiquetan separadamente del texto original.
5. GenerationPort recibe una configuración validada: identidad exacta del modelo/tokenizer/plantilla, dtype/cuantización, presupuesto efectivo de entrada/salida y deadline. No recortes silenciosos por tipo de request. La política pedagógica favorece explicación y ejemplo cuando ayudan, ofrece pistas o práctica a petición y cambia estrategia ante dificultad; no exige una fórmula rígida por turno.
6. Una revisión separada combina controles deterministas de permisos/procedencia con señales semánticas calibradas de fidelidad, pertinencia y cobertura. Premisas ficticias pueden ser libres; conclusiones y principios necesitan apoyo suficiente. Registrar qué no ha podido verificar. Prevención por recuperación/prompt y evaluación posterior son defensas diferentes.
7. Una decisión de publicación versionada identifica exactamente el contenido revisado, configuración, fuentes y vigencia. Un contrato sucesor de T090 debe definir esta autoridad antes de integrarse: no se obtiene permiso creando un campo `trusted_text`. Los controles constitucionales, consentimiento y cierre siguen fuera del LLM. `unknown/rejected` conservan la recuperación de estado y muestran solo el límite autorizado.
8. Preparación y confirmación de entrega usan un identificador estable y un recibo inmutable o copia defensiva. Revalidar antes de confirmar, definir la ventana de validez y guardar solo lo confirmado como mostrado. La reproducción reconstruye decisiones; no promete identidad textual universal. Cancelar o repetir la petición no duplica estado ni revive contenido retirado.

## Reutilización y diferencias

| Componente actual | Reutilizar | Cambio propuesto |
|---|---|---|
| SQL de permisos, actividad y versiones; T150 | Sí, controles transaccionales y cierre ganador | Ensayar intercalaciones con conexiones separadas y recuperación tras caída; no confiar únicamente en lock de proceso. |
| Autorización T090 | Preservar contrato y perfiles existentes | Contrato sucesor optativo para generación revisada, con revisión humana de diseño y rollback al perfil cerrado; ninguna ranura de texto libre confiable por etiqueta. |
| Unidades y posiciones de012 | Sí, representación rica y originales intactos | Añadir identidad de extracción y esquema; snapshots inmutables y materialización por hash. Evitar mutabilidad compartida y cachear por bytes/configuración. |
| Embeddings/Chroma002 | Sí, adaptadores existentes | Corregir identidad antes de reutilizar; fingerprint de encoder/revisión/normalización y dimensión en índice. Mismatch rechaza y propone reconstrucción autorizada, no la ejecuta solo. |
| Léxico bilingüe012 | Sí, baseline y conceptos generales | Convertirlo en estrategia del puerto común; no tabla de respuestas. Controlar el peso total de historial y registrar candidatos filtrados. |
| ExtractoresPDF/PPTX/DOCX | Sí, texto/tablas nativas | QA por página/slide; OCR o parser estructural solo para huecos demostrados, con licencia/modelos/recursos aprobados. No equivalencia automática PDF/PPTX. |
| Ledger y evidencia por afirmación | Sí, trazabilidad de revisión | No tomar etiquetas como juicio de verdad. Medir omisiones del extractor y contenido final, incluida la conclusión del ejemplo. |
| Worker y telemetría | Sí, procesos propios y transporte | Configuración solicitada/efectiva, offline explícito, cap negociado, cierre del monitor antes del resumen; no atribuciones de memoria sin prueba. |
| Privacidad/exportación | Sí, scopes y controles de acceso | Payload tipado por evento, eliminación lógica documentada y recuperación operativa. Decisión separada sobre residuos/WAL/backups según amenaza. |
| Demo y perfil extractivo | Sí como compatibilidad y referencia histórica | Etiquetar capacidad efectiva; no anunciar ese modo como tutor generativo. Nuevo flujo de estudio solo tras gates. |

## Migración compatible y rollback

Primero corregir identidad/offline/configuración con pruebas CPU; conservar interfaces o versionarlas si cambia semántica. Inventariar índices existentes y comprobar su identidad sin modificar sus datos. Si falta identidad, marcarlos como no acreditados para una comparación nueva; no afirmar que están corruptos. Un índice nuevo requiere raíz/carpeta y presupuesto explícitos, con validación antes de cambiar un puntero de versión.

Las estrategias nuevas y el flujo retrieval-first quedan optativos en laboratorio. Los perfiles001–011 y sus contratos no cambian por migrar el laboratorio. Registrar configuración completa y demostrar que apagar la opción recupera el baseline; no reemplazar silenciosamente fuentes o preguntas. Reversión significa seleccionar versión anterior compatible y cerrar nuevas publicaciones; una retirada no se revierte para reconstruir un turno.

Antes del contrato sucesor generativo: análisis de amenazas, autoridad que emite el permiso, firma/huella del contenido exacto o mecanismo equivalente, vigencia, invalidación tras cambios y consecuencias de error. Un hash identifica bytes, no certifica semántica. No se prescribe criptografía innecesaria dentro de un mismo proceso: lo obligatorio es impedir que el generador emita su propio permiso y que un permiso se reutilice para otro texto/sesión.

No implementar todavía GraphRAG, atomización formal completa, un equipo adicional de LLM por turno, memoria longitudinal, acceso web, multiusuarioLAN o voz. Tampoco fine-tuning antes de demostrar que los datos y la señal de evaluación distinguen los errores relevantes. Si una de esas capacidades se justifica más adelante, se autoriza y evalúa separadamente.
