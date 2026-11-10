# Ajuste del plan: necesidades, proporcionalidad y límites prácticos

27 de octubre de 2026. Complemento del [plan de ejecución](2026-10-27-oralia-audit-action-plan.md), redactado por el chat coordinador después de contrastar la [revisión de necesidad](../audits/2026-10-27-needs-proportionality/informe-final.md) y su [registro individual](../audits/2026-10-27-needs-proportionality/individual-review-final.md).

Este documento ajusta prioridades. No elimina requisitos, modifica la constitución ni abre gates. Las propuestas de sustitución o retirada necesitan distinguir el cambio de mecanismo de una reducción de garantías o del producto. El plan anterior y su hash se conservan.

## Resultado de la revisión

Se valoró la necesidad de 418 identificadores: 417 requisitos formales y un alias documental (`012/SC001`, referencia a `SC-001`). No se ha certificado su cumplimiento mediante esta valoración.

| Recomendación | Identificadores | Interpretación |
|---|---:|---|
| Conservar por seguridad o permiso | 133 | No simplificar quitando acceso, consentimiento, fuentes vigentes o cierre seguro. |
| Conservar para el uso actual | 98 | Núcleo de experiencia de estudio, operación y trazabilidad útil. |
| Sustituir el mecanismo | 94 | Mantener la necesidad; revisar cómo se satisface. No significa 94 requisitos innecesarios. |
| Aplazar nuevas ampliaciones | 59 | Preservar funciones y seguridad existentes; no ampliarlas antes del chat viable. |
| Separar del criterio del producto actual | 17 | Investigación o evidencia histórica específica; no borrar resultados ni abandonar el objetivo investigador. |
| Fusionar obligaciones equivalentes | 7 | Evitar duplicación; uno de los siete es el alias documental. |
| Resolver una decisión o ambigüedad | 10 | No elegir una interpretación material por cuenta del implementador. |

Los motivos y textos completos están en el registro individual. Las cifras son recomendaciones de auditoría, no tareas completadas ni autorización de cambios masivos.

## Objetivo de producto y objetivo de investigación

El hito de producto debe demostrar que una persona puede estudiar una duda, pedir otra explicación, recibir un ejemplo y aplicar lo explicado, con fuentes y límites comprensibles. El hito investigador debe medir qué aportan los agentes y verificadores frente a alternativas comparables. Son objetivos compatibles, pero no la misma prueba.

Proponemos aceptar hitos e informes separados. Demostrar un número de agentes, composiciones o celdas sintéticas no será una nueva condición propuesta para cada cambio de interacción. Los requisitos investigadores vigentes no se eliminan automáticamente; se prepara su separación formal para revisión.

Mantener el monolito modular y los contratos existentes cuando sirven. No crear un agente, modelo o almacén por cada función o categoría conceptual. Tampoco refactorizar componentes estables únicamente para reducir un conteo de clases.

## Prioridad práctica revisada

### 1. Continuar las correcciones seguras ya iniciadas

Identidad de embeddings e índice, carga local, presupuestos efectivos, privacidad de registros y estado de entrega. Son defectos o fronteras reproducibles relacionados con confianza y operación. No requieren cambiar la necesidad humana ni comprar hardware. Verificar cada corrección sobre el código actual: la auditoría describe una versión anterior, no invalida mejoras posteriores.

No convertir todas las hipótesis de riesgo en una reforma obligatoria antes de otro diagnóstico aislado. Las pruebas sintéticas de laboratorio pueden avanzar con sus límites; la publicación y el uso con personas exigen las garantías correspondientes.

### 2. Medir cobertura antes de prometer el curso completo

Preparar un inventario por los nueve bloques permitidos: fuentes docentes autorizadas disponibles, fuentes activas, extracción útil, páginas en cuarentena y huecos. El catálogo de tres PDF es una selección experimental centrada en requisitos y testing, no la asignatura completa ni la frontera de autorización del usuario.

Se pueden preparar otras diapositivas docentes ya autorizadas, en un formato por documento, sin pedir reautorizar la asignatura. Antes de usarlas, registrar revisión de extracción, versión, selección y activación por la política normal. No incluir alumnos, duplicar representaciones ni levantar cuarentenas por obtener caracteres.

Una actividad piloto puede evaluar objetivos concretos con fuentes suficientes sin reducir permanentemente el temario. La interfaz y los informes deben diferenciar lo permitido de lo respaldado actualmente. Falta de cobertura no significa «no necesitas estudiarlo».

### 3. Priorizar una conversación útil sobre nuevas demostraciones de mecanismos

Con configuración válida, realizar el diagnóstico comparado ya previsto y después un episodio completo si existe una candidata defendible. No esperar a terminar nuevas ampliaciones de todos los modos, formatos, paneles y estudios arquitectónicos. No generar respuestas prefabricadas para cumplir el episodio.

Definir qué debe observarse: fidelidad conceptual, respuesta a la duda, cambio material de estrategia, ejemplo con premisas, continuidad y un pequeño uso de lo explicado. Evaluar utilidad por separado de satisfacción y cantidad de tests, sin calificaciones ni perfiles de capacidad.

La recuperación y la revisión son capacidades separadas. Mejorar ranking no explica un error que aparece con fuentes pertinentes presentes. Una gramática garantiza forma, no interpretación. Una cita identifica una fuente, no aprueba cada afirmación. No invertir primero en otro mecanismo cuando el control ya localiza el fallo en otra capa.

## Simplificaciones que deben proponerse, no aplicarse a ciegas

- Compartir evidencia inmutable y manifiestos en lugar de copiar todos los paquetes en cada prueba. Preservar los primeros fallos y una referencia completa por versión.
- Ejecutar regresiones por impacto. No repetir las 204 celdas o la suite global ante cambios sin relación; ampliar pruebas cuando cambien componentes compartidos o aparezca un riesgo nuevo.
- Separar paradas de entrega conversacional de evaluación de controles independientes. Nunca continuar una conversación desde texto bruto rechazado, pero no descartar automáticamente todos los demás casos diagnósticos presupuestados.
- Sustituir decisiones redundantes del modelo, offsets calculables y campos sin consumidor por estructuras más simples. No borrar controles antes/después de esperas porque tengan nombres parecidos.
- Permitir segmentación semántica trazable. Proteger una unidad de significado no obliga a entregar páginas enteras o listas arbitrariamente grandes.
- Evaluar alcance informado por búsqueda autorizada como variante de laboratorio. La obligación sigue siendo resolver permiso antes de generar; no convertir score o ausencia de resultados en autoridad docente.
- Separar la cantidad de repeticiones de la diversidad y cobertura de casos. Tres salidas greedy idénticas no son tres observaciones independientes de calidad; el requisito vigente de repeticiones se conserva hasta revisar su evolución.

## Necesidades que faltan como criterios concretos

1. Qué significa «listo para estudiar» en una actividad y cómo se observa una explicación útil.
2. Cuánta cobertura real de cada bloque se puede declarar, con mantenimiento de fuentes y modelos.
3. Latencia y frecuencia de límites que resultan tolerables, distinguiendo objetivo de servicio, deadline de seguridad y tiempo de carga.
4. Cuánto esfuerzo de preparación, QA y revisión de muestras puede asumir el docente sin perder el beneficio de autonomía.
5. Qué recuperación operativa ofrece el producto tras un error, una caída o pérdida de acceso, sin bucles ni pérdida de control.

Preparar medidas y propuestas concretas; no inventar cifras en nombre del usuario. Hay perfiles de 30 segundos/512 tokens y de 50 segundos/768 tokens: ninguno es un requisito universal de experiencia. No alterar protocolos congelados para adaptarlos a una cifra nueva.

## Qué está bloqueado y qué no

| Necesidad | Situación práctica | Dirección |
|---|---|---|
| Explicaciones y ejemplos fieles | Fallos empíricos con fuentes presentes; no incapacidad universal demostrada | Diagnóstico pareado y conversación revisable. Más contexto o VRAM no garantiza resolverlo. |
| Publicación generativa autónoma | Contrato sucesor pendiente y revisión semántica aún sin evidencia suficiente | Preparar contrato y aceptación empírica para revisión humana; no inventar permiso ni exigir garantía lógica universal. |
| Cubrir el temario permitido | Fuentes incorporadas insuficientes y coste de cobertura no inventariado | Incorporación por bloques y cobertura visible, sin reducir silenciosamente el alcance. |
| Diagramas y algunas tablas | Extracción parcial y QA pendiente | Resolver páginas de mayor valor con formatos/extractores disponibles; OCR nuevo solo con justificación y recursos. |
| Latencia, memoria y carga docente | Memoria finita, tolerancias no acordadas y costes no medidos suficientemente | Medir episodio y preparación en un perfil concreto; no recomendar compras o nube por defecto. |
| Identidad, budgets y estado | Defectos corregibles, algunos ya en reparación | Completar pruebas y correcciones en CPU; no llamarlos límites inherentes del tutor. |

## Decisiones materiales pendientes

Mantener preparadas las propuestas de [decisiones del usuario](../audits/2026-10-27-needs-proportionality/decisiones-para-el-usuario.md): hitos separados de producto e investigación, contrato/criterios de publicación generativa, servicio tolerable y esfuerzo docente. Los diez requisitos ambiguos no equivalen a diez preguntas nuevas; agrupar los que dependen de la misma decisión.

Conciliar los contratos históricos de resumen, conservación y purga con las versiones posteriores y el consentimiento efectivo. No volver a preguntar decisiones ya fijadas ni alterar datos heredados antes de resolver una precedencia dudosa.

No activar otra política, retirar una obligación constitucional, rebajar gates ni abrir participante por este anexo. Puede prepararse implementación optativa de laboratorio y pruebas de compatibilidad; cualquier cambio material debe presentarse concreto y revisable. Mientras tanto continúan las correcciones independientes.

## Límite de complejidad

No ampliar ahora voz, web, LAN, memoria longitudinal, GraphRAG, formalización completa del curso, fine-tuning sin evaluador suficiente o más paneles. Preservar las rutas existentes con su seguridad. Ninguna de esas tecnologías queda prohibida para siempre: su necesidad tendrá que derivarse de un problema demostrado del uso.

La simplificación buscada consiste en conservar resultados y garantías con menos prescripciones, no en eliminar privacidad, autorización, revisión o evidencia para anunciar antes una herramienta terminada.

## Aclaración humana posterior: objetivo de piloto real, no explotación

El usuario precisa: «el alcance de estas herramientas no son la explotación, sino probar su eficacia con algunos estudiantes en una situación real». Esta decisión prevalece sobre cualquier interpretación de los hitos anteriores como preparación de un servicio general de producción.

El próximo hito es una actividad piloto acotada, con estudiantes reales, objetivos y fuentes concretos y una configuración estable. No requiere cobertura completa de la asignatura, cinco modos validados, voz, escalabilidad, disponibilidad continua ni automatización de toda la operación. Se conserva el temario permitido; se declara qué parte se evalúa, sin anunciar cobertura del resto.

La preparación mínima incluye fuentes revisadas y autorizadas, ejemplos y casos representativos, controles de errores críticos, referencias y límites comprensibles, consentimiento y conservación elegida, aislamiento de datos y una vía de cierre/parada. La supervisión del piloto no sustituye cada respuesta por aprobación humana ni convierte un preview no autorizado en salida apta para personas.

Los criterios de avance deben dimensionarse al dominio y al riesgo del piloto. Se prepara una propuesta concreta de adaptación de contratos y gates, sin abrirlos automáticamente ni exigir una garantía universal. Las correcciones de identidad, configuración, privacidad y estado siguen siendo necesarias para interpretar los resultados y proteger a los participantes.

La evaluación debe separar fidelidad, utilidad, aplicación o transferencia, experiencia, bloqueos, tiempos y esfuerzo docente del valor investigador de la arquitectura. Un grupo pequeño puede informar viabilidad y problemas, pero no justifica por sí solo una afirmación general de eficacia causal. No se producirán notas académicas ni perfiles de capacidad.

Preparar el protocolo y los materiales está autorizado. Contactar estudiantes, iniciar sesiones con personas o asumir decisiones institucionales no se ejecuta automáticamente: se concreta el piloto con el usuario. No se abre otra revisión completa de requisitos para incorporar esta prioridad.
