# Feature 006 — Validación arquitectónica y comparación experimental

Añade instrumentos reproducibles para evaluar si la arquitectura multiagente de ORAL-IA aporta control, trazabilidad, reutilización, detección de errores y degradación frente a un baseline monolítico. La validación evalúa el sistema, no al estudiante.

## Propósito

Producir evidencia técnica y docente suficiente para decidir qué componentes de la arquitectura deben conservarse, simplificarse o ampliarse después del MVP.

## Condiciones comparables

Debe poder ejecutar, sobre un conjunto de escenarios preparados y datos ficticios o consentidos:

1. respuesta directa de un modelo monolítico;
2. agencia completa;
3. agencia sin verificador de fundamentación cuando el protocolo lo autorice;
4. agencia sin verificador de coherencia cuando el protocolo lo autorice;
5. distintas estrategias de recuperación;
6. distintas composiciones de agentes;
7. fallos inyectados de agente, modelo, índice, transcripción y recursos.

Los controles constitucionales y de privacidad no pueden desactivarse en experimentos con usuarios. Las ablaciones de seguridad solo pueden ejecutarse con datos sintéticos, sin mostrar salidas inseguras a participantes.

## Métricas arquitectónicas

Como mínimo:

- agentes activados por sesión y turno;
- composiciones distintas;
- respuestas bloqueadas y reformuladas;
- respuestas sin fuentes;
- cobertura y precisión de recuperación sobre un conjunto etiquetado;
- conflictos y contradicciones detectados;
- fallos de coordinación;
- latencia total y por agente;
- CPU, memoria, GPU y tamaño de contexto;
- timeouts y recuperaciones ante fallo;
- porcentaje de turnos completamente trazables;
- capacidad de reconstrucción de sesiones;
- reutilización de agentes entre agencias;
- correcciones de transcripción y cambios provocados por ellas.

## Indicadores de utilidad docente y experiencia

Como mínimo: sesiones completadas, abandonos, duración, utilidad percibida, facilidad de uso, calidad percibida de preguntas y repreguntas, utilidad para preparar explicaciones, porcentaje de transcripciones revisables y tiempo de revisión docente.

Estos indicadores no deben combinarse en una calificación individual ni utilizarse para inferir capacidad académica.

## Catálogo de escenarios de prueba

Debe incluir:

- consulta con evidencia clara;
- consulta sin evidencia;
- fuentes conflictivas;
- intento de obtener información fuera de alcance;
- respuesta generada con afirmación no respaldada;
- contradicción conversacional;
- repetición y ausencia de progreso;
- timeout de agente;
- modelo no disponible;
- índice no disponible;
- fallo de transcripción y degradación a texto;
- conflicto de actualización del estado;
- límite de turnos o duración;
- solicitud de eliminación;
- intento de salida con nota o decisión académica.

## Reproducción

Cada ejecución experimental debe fijar y registrar versión del código, configuración, modelos, parámetros, versión del índice, documentos, escenario, semilla cuando aplique, agentes, orden, límites y entorno de hardware. Debe poder reconstruirse el flujo y comparar resultados, aun cuando una salida generativa no sea idéntica byte a byte.

## Informes

El sistema debe generar:

- resultados estructurados para análisis;
- resumen por escenario y configuración;
- comparación entre baseline y agencia;
- incidencias y datos faltantes;
- advertencias sobre muestras pequeñas o condiciones no comparables;
- informe final con beneficios observados, costes, limitaciones y propuesta de evolución.

## Escenarios prioritarios

### Escenario A — Baseline frente a agencia

El mismo conjunto de consultas se ejecuta con baseline monolítico y agencia completa. El informe compara fundamentación, bloqueos, trazabilidad, latencia y recursos sin afirmar superioridad si los datos no la sostienen.

### Escenario B — Ablación de verificador

Con datos sintéticos, se compara la agencia con y sin verificación de fundamentación y se cuantifica qué errores detecta y qué coste introduce.

### Escenario C — Recuperación ante fallo

Se inyectan fallos controlados y se mide si el sistema degrada, conserva estado y produce una traza comprensible.

### Escenario D — Reproducción

Un tercero ejecuta de nuevo un escenario utilizando el paquete registrado y obtiene la misma secuencia de componentes y decisiones estructurales dentro de las tolerancias definidas.

### Escenario E — Informe prudente

Los datos son insuficientes o contradictorios. El informe lo declara y evita concluir que la arquitectura es mejor.

## Fuera de alcance

- evaluación psicométrica o académica de estudiantes;
- modelos predictivos de rendimiento;
- experimentos sin consentimiento;
- publicación automática de datos;
- ocultación de resultados negativos;
- optimización autónoma de políticas en producción.

## Criterios de éxito

- Se ejecutan de forma reproducible baseline, agencia completa y al menos una ablación.
- El porcentaje de decisiones trazables puede calcularse automáticamente.
- Los fallos previstos producen métricas y evidencias de recuperación o terminación segura.
- El informe distingue observaciones, métricas, inferencias y limitaciones.
- Los resultados permiten identificar qué verificadores o agentes aportan beneficio y qué coste introducen.
- Ninguna métrica se utiliza para asignar notas o clasificar estudiantes.
