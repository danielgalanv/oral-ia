# Research — decisiones de diseño 010

Investigación realizada sobre fuentes locales y lectura independiente de dos agentes de investigación según speckit-plan. No se instalaron modelos, no se realizó inferencia ni búsqueda de nuevas bibliotecas. Todos los hallazgos siguientes son observaciones de código o decisiones de diseño, no resultados de implementación.

| Decisión | Evidencia/razón | Alternativa descartada |
|---|---|---|
| Corregir diálogo, no solo demo | 003 exige explicación/ejemplos/contexto;004 repreguntas relacionadas. Los diálogos reales fallan esos objetivos. | Añadir mensajes amables y declarar éxito por 900+ tests. |
| Extender intérprete existente v2 | study_intent_interpreter.py reconoce cinco modos y unas subintenciones; faltan repeat/help/greeting y negación compuesta. | Un intérprete independiente duplicado por compositor, o solo más substrings. |
| Ancla estable versionada | Autoestudio reusa anterior input para tres subintenciones, pero una orden meta destruye el referente. Defensa recupera input actual antes de pasar pregunta anterior al generador. | Afirmar que no existe contexto alguno o enviar historial íntegro al modelo. |
| Política de acciones explícita | _concepts de defensa añade tokens como no/ahora/puedes; el fallback se repite sin evolución. | Interpretar esa repetición como incapacidad del usuario. |
| Repetición según intención | CoherenceVerifier aplica overlap contra salida anterior aunque la fuente esté bien; repetir solicitado no es ausencia de progreso. | Desactivar verificador, subir umbral o ampliar número de regeneraciones sin límite. |
| Propuesta reconstruible controlada primero | _decide_study_output solo autoriza catálogo y extractos completos/canónicos; un LLM puede fallar T090 aun pasando grounding léxico. | Registrar un candidato libre con su hash como «plantilla autorizada». |
| Unidades docentes externas a agentes | Adaptador determinista da el mismo extracto para todos los propósitos y concatenación para repregunta. La fuente de dos frases no cubre explicación. | Hardcodear respuestas del agua o prometer que cualquier modelo lo soluciona. |
| Estudio local LLM condicionado | GenerationPort y Ollama existen; instalación/disponibilidad no prueban entailment ni calidad. | Descargar un modelo y marcar completada la capacidad sin evaluación. |
| Reproducción y corpus reservado | Test de defensa histórica inyecta _CandidateAgent/_ApprovedGrounding; E2E demo solo una pregunta exacta y respuesta100. | Borrar esos tests de contratos o contarlos como evidencia generativa. |
| Entrada/recuperación antes de permiso de sesión | Se observaron código no permitido, sesión huérfana y PATH de agente distinto del usuario. | Ampliar destinatarios, cerrar otra sesión o editar DB por comodidad. |
| Privacidad del contexto nuevo | El ancla puede contener lo mismo que una transcripción. | Guardarla como «metadato técnico» perpetuo para eludir consentimiento. |

## Decisiones que se medirán, sin bloquear la escritura del plan

Modelo local concreto, presupuestos efectivos y alcance de verificación generativa se fijarán por protocolo de viabilidad, no por intuición ni por la disponibilidad histórica de un modelo pequeño. La planificación cierra la decisión de arquitectura: guided_controlled es obligatorio; generative_local_candidate no puede publicarse sin G2. No hay marcador de ambigüedad crítica en las tareas de implementación: si el estudio no pasa, debe entregar informe negativo y dejar esa capacidad desactivada, no reclamar autoestudio libre.

## Compatibilidad y errores previsibles

- V1 sigue accesible para consumidores antiguos; actividades anteriores conservan perfil/política y no se reinterpretan tras migrar.
- Datos de material son datos, incluso si contienen texto parecido a una instrucción; por unidad y por plantilla se valida procedencia y versión.
- Casos99/100 usan magnitud/unidad/condición documentada; incertidumbre real permite aclaración. No comparar números aislados por desigualdad.
- La no revelación se comprueba en el conjunto de respuesta, pistas y fuentes, no solo en la pregunta.
- El corpus humano real no se copia a un dataset sin autorización; se guardan secuencias sintéticas equivalentes y referencias al hallazgo.
- Latencias: frío/preparado/calentado y carga concurrente se registran aparte; no se afirma p95 universal en el equipo del usuario.


## Corrección didáctica20-10-2026

Decisiones K/L y didactic-decision-log.md registran propósito frente a publicación, materiales sucesores y falsos conflictos léxicos. Se mantiene el verificador independiente y se revisa redacción sin cambiar significado o políticas. Las variantes se enlazan por relaciones y se excluyen del fallback genérico; repetir conserva referencias. Cuatro corpus fueron congelados y sus primeras ejecuciones se conservan:3/4,3/4,4/4,4/4, más16regresiones expuestas actuales. No se afirma comprensión general, mejora de rendimiento, aprobación humana, audio o superioridad arquitectónica por esta evidencia.

## Tablas nativas20-10-2026

Decisión M y table-extraction-comparison.json: DOCX/PPTX omitían24celdas cada uno en los ejemplos del programa; aguaWord no contiene tabla yPDF mantiene siete páginas. Contexto estructural acotado y referencias de origen preservan literalidad sin inferir cabeceras. No se leen notas ni se modifica corpus/guías propuestos por la auditoría externa. Nuevo ensayo17/17 con activación/UUID/retirada/aislamiento reales temporales; no constituye validación docente/conversacional o visual.
