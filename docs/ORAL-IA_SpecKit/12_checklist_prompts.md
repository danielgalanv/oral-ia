# Prompts para `/speckit-checklist`

## Checklist general de requisitos

```text
Genera una checklist de calidad de requisitos para la feature actual. Comprueba que cada requisito sea observable, no ambiguo, verificable y coherente con la constitución. Revisa historias prioritarias, escenarios normales, errores, timeouts, cancelación, concurrencia, degradación, límites de alcance, accesibilidad, privacidad, trazabilidad y criterios de éxito. Señala cualquier decisión técnica introducida indebidamente en la especificación y cualquier comportamiento sin criterio de aceptación.
```

## Checklist de arquitectura cognitiva

```text
Genera una checklist específica para verificar que la feature preserva la arquitectura cognitiva: responsabilidad única de agentes, contratos explícitos, mensajes estructurados, estado externo al LLM, control de acceso al estado, composición de agencias, separación entre recuperación, generación, decisión y verificación, controles constitucionales no omitibles, memoria diferenciada, trazabilidad, cancelación, degradación y posibilidad de sustituir agentes sin modificar el orquestador.
```

## Checklist de RAG y materiales

```text
Genera una checklist de requisitos para materiales autorizados y RAG: formatos, errores de extracción, metadatos, versiones, autorización, vigencia, duplicados, chunking reproducible, reconstrucción del índice, filtros, citas, evidencia insuficiente, conflicto entre fuentes, retirada de versiones, prompt injection documental, aislamiento entre asignaturas y trazabilidad de documento a respuesta.
```

## Checklist de privacidad y datos

```text
Genera una checklist de privacidad por diseño para la feature actual: minimización, seudonimización, consentimiento, sesión efímera, audio temporal, transcripción original y corregida, retención, purga, exportación, control de acceso, exposición de red, secretos y logs, texto libre con datos personales, reproducción sin identidad y ausencia de perfiles académicos o psicológicos.
```

## Checklist de no evaluación académica

```text
Genera una checklist para detectar evaluación académica explícita o encubierta. Revisa notas, puntuaciones, rúbricas autónomas, clasificación de nivel, aprobación/suspenso, juicios de capacidad, perfiles longitudinales, recomendaciones decisorias, lenguaje que suplante al profesor y métricas que puedan reutilizarse para evaluar al estudiante. Verifica que resúmenes y paneles sean descriptivos y evalúen el sistema.
```

## Checklist de voz y accesibilidad

```text
Genera una checklist para voz y accesibilidad: equivalencia funcional por texto, navegación por teclado, pausa y repetición, estados de captura, confianza y segmentos dudosos, corrección antes de análisis, descarte de audio, fallo de STT/TTS, fallback a texto, mensajes comprensibles, etiquetas, contraste, control de ritmo y ausencia de biometría o análisis emocional.
```

## Checklist de validación experimental

```text
Genera una checklist para asegurar que la comparación experimental sea reproducible y prudente: condiciones comparables, versiones, hardware, configuraciones, datasets, semillas cuando apliquen, baseline, ablations, métricas definidas antes del análisis, fallos inyectados, datos sintéticos para pruebas inseguras, muestras insuficientes, resultados negativos, intervalos o variabilidad, separación entre observación e inferencia y prohibición de evaluar estudiantes.
```
