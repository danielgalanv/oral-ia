# Respuesta íntegra para revisión docente de este caso

¿Para qué sirve mantener trazabilidad entre necesidades, requisitos y pruebas? Explica cómo la usarías, con un ejemplo hipotético sencillo, para analizar qué revisar si cambia una necesidad del cliente, y qué no permite concluir por sí sola.

Mantener trazabilidad entre necesidades, requisitos y pruebas es crucial para asegurar que todos los elementos del desarrollo de un sistema estén alineados y coherentes. Esta trazabilidad permite rastrear cómo una necesidad del cliente se traduce en requisitos específicos y luego en pruebas que validan que esos requisitos se cumplen correctamente.

### ¿Cómo usaría la trazabilidad?

Supongamos un caso hipotético donde un cliente necesita que su sistema de gestión de pacientes permita buscar a un paciente en todas las clínicas. Este requerimiento sería una necesidad del cliente. La trazabilidad nos permitiría identificar:

1. **Necesidad del Cliente**: "El sistema debe permitir buscar a un paciente en todas las clínicas."
2. **Requisito Funcional**: "El sistema debe proporcionar una funcionalidad de búsqueda que permita encontrar a un paciente en cualquier clínica."
3. **Pruebas de Validación**: "Se debe realizar una prueba que demuestre que la búsqueda de un paciente funciona correctamente en todas las clínicas."

Si la necesidad del cliente cambia, por ejemplo, a "El sistema debe permitir buscar a un paciente en todas las clínicas y en sus citas médicas pasadas", la trazabilidad nos ayudaría a identificar qué requisitos y pruebas deben ser revisados y actualizados:

- **Revisar el Requisito Funcional**: El requisito funcional original podría necesitar ser modificado para incluir la búsqueda en citas médicas pasadas.
- **Revisar las Pruebas de Validación**: Se necesitarían nuevas pruebas para validar la nueva funcionalidad de búsqueda en citas médicas pasadas.

Además, la trazabilidad permite también el recorrido inverso, desde los requisitos hasta las necesidades del cliente, asegurando que cada requisito tenga un origen claro. Sin embargo, no garantiza que no haya requisitos redundantes o inconsistentes; es necesario evaluar la traza para asegurar que está correcta y que abarca completamente el requisito padre, pero no necesariamente se evalúa la calidad individual de cada requisito.

### ¿Qué no permite concluir por sí sola la trazabilidad?

La trazabilidad no permite determinar automáticamente si el cambio en la necesidad del cliente tiene implicaciones en otros aspectos del sistema que no sean directamente relacionados con la búsqueda de pacientes. Por ejemplo, si el cambio en la necesidad del cliente implica una mayor carga de datos, esto podría tener implicaciones en el rendimiento del sistema, en la capacidad de almacenamiento, en la seguridad de los datos, etc. Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas.

En resumen, la trazabilidad es una herramienta valiosa para asegurar que los cambios en las necesidades del cliente se reflejan adecuadamente en los requisitos y pruebas correspondientes, pero no reemplaza la necesidad de una evaluación integral de los impactos de estos cambios en el sistema completo.

## Fuentes consultadas — procedencia del host

- 6 - Procedimiento requisitos.pdf, página 11. Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, página 13. Requirements imprecision
- 6 - Procedimiento requisitos.pdf, página 10. Verificar la calidad de los requisitos del sistema
- nasa-handbook.pdf, página 142. NASA §6.2 Requirements Management
- 5 - Requisitos.pdf, página 20. Goals and requirements

Revisión asistida de este caso; no publicación para participantes. Permanece una ambigüedad de redacción sobre impactos indirectos, interpretada con su condición de ausencia de deducción automática. No garantía universal de ausencia de errores.
