# Prompts auxiliares de ejecución

## Antes de `/speckit-implement`

```text
Implementa exclusivamente la feature activa. Lee constitution.md, spec.md, plan.md, data-model.md, contracts/ y tasks.md. Muestra primero un resumen breve de cobertura y riesgos. Sigue el orden de dependencias, marca tareas al completarlas y ejecuta pruebas tras cada historia de usuario. No amplíes alcance, no sustituyas tecnologías o contratos sin documentarlo, no desactives verificadores obligatorios y no uses datos reales no proporcionados.
```

## Después de la primera implementación

```text
Revisa la implementación contra todos los escenarios de aceptación. Busca especialmente estados ocultos dentro de prompts, intercambio de texto libre entre agentes, permisos excesivos, falta de versionado, trazas incompletas, evaluación académica encubierta, audio persistente, materiales no autorizados, errores sin degradación y pruebas que solo validen mocks. Corrige los incumplimientos que estén dentro del alcance de la feature.
```

## Para `/speckit-analyze`

```text
Prioriza contradicciones con la constitución, requisitos sin tarea, tareas sin requisito, escenarios sin prueba, decisiones técnicas no justificadas, duplicación de agentes, acoplamiento entre dominio e infraestructura, falta de privacidad, trazabilidad incompleta y trabajo de features posteriores introducido prematuramente.
```

## Para `/speckit-converge`

```text
Compara código, pruebas, documentación y migraciones con la especificación y la Definition of Done. Añade solo tareas necesarias para cerrar brechas reales de la feature. No propongas mejoras opcionales, refactors estéticos ni features futuras como trabajo obligatorio.
```
