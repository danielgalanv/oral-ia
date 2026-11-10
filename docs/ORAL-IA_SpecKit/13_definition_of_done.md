# Definition of Done

## Para cada feature

Una feature solo puede considerarse completada cuando:

1. La especificación no contiene ambigüedades críticas y todos los escenarios prioritarios tienen criterios observables.
2. El plan ha superado la comprobación constitucional.
3. Todas las tareas obligatorias están completadas o existe una desviación aprobada y documentada.
4. El código mantiene contratos y esquemas versionados.
5. Las migraciones pueden aplicarse desde una instalación limpia.
6. Existen pruebas unitarias, de contrato e integración para sus componentes.
7. Existe al menos un flujo extremo a extremo del escenario principal.
8. Existen pruebas de los fallos y degradaciones relevantes.
9. No hay salidas que asignen notas, suplanten al profesor o tomen decisiones académicas.
10. La trazabilidad permite reconstruir cada turno afectado por la feature.
11. Los datos, logs y exportaciones cumplen minimización y privacidad.
12. La interfaz esencial es utilizable por texto y teclado.
13. Se documentan instalación, configuración, ejecución, pruebas y limitaciones.
14. Se incluye un conjunto pequeño de datos o materiales ficticios para demostrarla.
15. `/speckit-analyze` no presenta errores críticos y `/speckit-converge` no detecta trabajo funcional obligatorio pendiente.

## Para el MVP completo

Además:

1. Autoestudio y defensa oral usan la misma base arquitectónica.
2. Los agentes se reutilizan y combinan sin modificar sus implementaciones.
3. El estado cognitivo está fuera del contexto del LLM y es versionado.
4. Las respuestas distinguen evidencia recuperada, conocimiento general permitido e información no verificable.
5. La salida visible pasa por verificadores independientes.
6. Las sesiones pueden reconstruirse desde configuración, eventos y artefactos versionados.
7. Los fallos de LLM, RAG y voz degradan o terminan de forma controlada.
8. Se puede añadir un agente de prueba mediante su contrato sin modificar el orquestador.
9. Existe un baseline monolítico y al menos una comparación reproducible.
10. El informe final identifica beneficios, costes, limitaciones y problemas no resueltos sin exagerar conclusiones.
11. La instalación funciona en un ordenador local con un perfil de hardware documentado.
12. No depende de robot, Internet, Moodle, expedientes ni servicios personales.
