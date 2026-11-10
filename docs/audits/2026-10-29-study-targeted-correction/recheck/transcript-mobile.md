# Revisión de tres casos afectados

Regresiones expuestas; no reserva nueva. Historial reconstruido de respuestas reales anteriores.

## 7. ¿En qué se diferencian verificar y validar una especificación?

La verificación y la validación de una especificación de requisitos son procesos distintos pero complementarios en el desarrollo de sistemas de software. Veamos cómo se diferencian:

### Verificación

**Objetivo**: Verificar que la Especificación de Requisitos del Sistema cumple con el modelo de calidad de requisitos propuesto.

**Actividades principales**:
- **Correcta**: La especificación sigue una estructura y contenido adecuados.
- **Completa**: Incluye todos los aspectos conocidos que el sistema software debe realizar.
- **Consistente internamente**: No contiene contradicciones ni redundancias innecesarias.
- **Consistente externamente**: No tiene requisitos que sean inconsistentes con otros documentos del proyecto.

**Ejemplo hipotético**:
Supongamos que estamos desarrollando un sistema de gestión de inventario. Durante la verificación, nos aseguramos de que cada requerimiento esté bien redactado, sea claro y no tenga ambigüedad. Por ejemplo, si uno de los requisitos es "El sistema debe poder registrar entradas y salidas de productos", verificamos que este requisito no esté duplicado en otro lugar, que no contradiga otros requisitos y que esté correctamente redactado.

### Validación

**Objetivo**: Comprobar que el sistema software descrito por la Especificación de Requisitos del Sistema se corresponde con las necesidades de negocio de clientes y usuarios, obteniendo su aprobación.

**Actividades principales**:
- **Reuniones**: Se realizan sesiones con los stakeholders para discutir y confirmar los requisitos.
- **Prototipado de la interfaz de usuario**: Se crean prototipos para demostrar cómo funcionará el sistema y obtener retroalimentación.
- **Aprobación**: Los stakeholders deben aprobar que los requisitos cumplen con sus necesidades.

**Ejemplo hipotético**:
Continuando con el sistema de gestión de inventario, durante la validación, organizamos reuniones con los gerentes de almacenamiento y los empleados que usarán el sistema. Presentamos los requisitos y solicitamos su aprobación. Por ejemplo, si uno de los requisitos es "El sistema debe generar informes mensuales sobre el inventario", validamos esto presentando un prototipo del informe y asegurándonos de que los gerentes de almacenamiento estén de acuerdo con su formato y contenido.

### Diferencias clave

- **Verificación** se centra en asegurar que los requisitos cumplen con ciertos criterios de calidad internos y externos, mientras que **validación** se enfoca en garantizar que los requisitos satisfacen las necesidades de los usuarios y stakeholders.
- **Verificación** implica revisar la especificación desde una perspectiva técnica, mientras que **validación** implica obtener la aprobación de los usuarios finales y stakeholders.

Ambos procesos son fundamentales para garantizar que el sistema final cumpla con los estándares de calidad y las necesidades de los usuarios.

Fuentes:
- 6 - Procedimiento requisitos.pdf, p. 10: Verificar la calidad de los requisitos del sistema
- 6 - Procedimiento requisitos.pdf, p. 12: Validar los requisitos del sistema
- nasa-handbook.pdf, p. 208: Appendix C: How to Write a Good Requirement— Checklist
- 5 - Requisitos.pdf, p. 89: Key points
- 6 - Procedimiento requisitos.pdf, p. 11: Verificar la calidad de los requisitos del sistema
## 3. No entiendo la diferencia en ese ejemplo. Explícamela con otras palabras.

Claro, permíteme explicar la diferencia entre verificar y validar los requisitos de una aplicación para pedir citas médicas de una manera más sencilla.

### Verificar los requisitos

Cuando verificamos los requisitos, nos aseguramos de que estén bien escritos y cumplan con ciertos criterios de calidad. Esto implica:

- **Claridad**: Los requisitos deben estar bien redactados y ser comprensibles.
- **Complejidad**: Deben cubrir todas las funcionalidades necesarias, como permitir a los pacientes buscar y reservar citas.
- **Consistencia**: No deben haber contradicciones entre los requisitos. Por ejemplo, si uno dice que el paciente puede buscar citas en cualquier clínica, otro no debe decir que solo puede buscar en una clínica específica.
- **Realizabilidad**: Los requisitos deben ser implementables con la tecnología disponible y dentro de un presupuesto razonable.
- **Comprobabilidad**: Se deben poder probar los requisitos de manera práctica. Por ejemplo, se debe poder verificar que el sistema permite a los pacientes buscar y reservar citas correctamente.

### Validar los requisitos

Cuando validamos los requisitos, nos aseguramos de que realmente satisfagan las necesidades de los usuarios y sean aprobados por ellos. Esto implica:

- **Reuniones**: Organizar reuniones con pacientes, médicos y administradores para discutir y obtener feedback sobre los requisitos. Por ejemplo, se podría preguntar si el sistema cubre todas las necesidades de los pacientes y si es fácil de usar.
- **Prototipos**: Crear prototipos de la interfaz de usuario para mostrar cómo funcionaría el sistema y recibir comentarios. Por ejemplo, se podría mostrar un prototipo de la pantalla de búsqueda de citas y pedir a los usuarios que den su opinión sobre su facilidad de uso.
- **Aprobación**: Obtener el visto bueno de los pacientes, médicos y administradores sobre los requisitos. Esto asegura que el sistema final satisfará las necesidades de los usuarios.

### Ejemplo hipotético

Imagina que estamos desarrollando una aplicación para pedir citas médicas. 

#### Verificación:
Nos aseguramos de que los requisitos estén bien redactados y cumplan con ciertos criterios de calidad. Por ejemplo, si un requisito dice "el paciente debe poder buscar citas en todas las clínicas", nos aseguramos de que este requisito esté bien redactado y no tenga ambigüedades. También nos aseguramos de que el requisito sea implementable técnicamente y que podamos probarlo de manera práctica.

#### Validación:
Organizamos reuniones con pacientes y médicos para discutir los requisitos y obtener su feedback. También creamos prototipos de la interfaz de usuario para mostrar cómo funcionaría el sistema y recibir comentarios. Finalmente, obtenemos la aprobación de los pacientes y médicos sobre los requisitos, asegurándonos de que el sistema final satisfará sus necesidades.

En resumen, verificar los requisitos implica asegurarse de que estén bien formados y cumplen con ciertos criterios de calidad, mientras que validar los requisitos implica asegurarse de que realmente satisfacen las necesidades de los usuarios y son aprobados por ellos.

Fuentes:
- 6 - Procedimiento requisitos.pdf, p. 10: Verificar la calidad de los requisitos del sistema
- 6 - Procedimiento requisitos.pdf, p. 12: Validar los requisitos del sistema
- 5 - Requisitos.pdf, p. 13: Requirements imprecision
- 6 - Procedimiento requisitos.pdf, p. 11: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, p. 89: Key points
## 4. ¿Cómo podría comprobar que una cita se reserva correctamente?

Para comprobar que una cita se reserva correctamente en una aplicación para pedir citas médicas, debes seguir estos pasos:

1. **Definir los criterios de comprobación**:
   - **Precisión**: Asegúrate de que el requisito esté bien redactado y no tenga ambigüedades. Por ejemplo, si el requisito es "El paciente debe poder reservar una cita", debe estar claro si esto significa que el paciente puede reservar en cualquier clínica o solo en una específica.
   - **Verificabilidad**: Debes poder definir una prueba que demuestre que el requisito se cumple. Por ejemplo, puedes probar que el sistema permite a los pacientes reservar citas en línea.

2. **Especificar la prueba**:
   - **Prueba de reserva de cita**: Diseña una prueba donde un usuario simulado intente reservar una cita siguiendo los pasos descritos en el requisito. Por ejemplo, el usuario debe poder seleccionar una fecha y hora disponibles, proporcionar información personal y confirmar la cita.

3. **Realizar la prueba**:
   - **Proceso de reserva**: Simula la reserva de una cita siguiendo los pasos de la prueba. Observa si el sistema permite al usuario seleccionar una fecha y hora disponibles, proporcionar información personal y confirmar la cita correctamente.

4. **Verificar el resultado**:
   - **Confirmación de reserva**: Después de realizar la prueba, verifica que la cita haya sido reservada correctamente. Esto implica que la cita debe aparecer en el calendario del paciente y en el sistema de la clínica.

5. **Medir el éxito**:
   - **Criterios de éxito**: Define los criterios de éxito para la prueba. Por ejemplo, la cita debe aparecer en el calendario del paciente y en el sistema de la clínica sin errores.

### Ejemplo Hipotético

Supongamos que tienes un requisito que dice: "El paciente debe poder reservar una cita en línea".

#### Paso 1: Definir los criterios de comprobación
- **Precisión**: El requisito debe ser claro y no ambiguo. Por ejemplo, "El paciente debe poder reservar una cita en línea en cualquier clínica".
- **Verificabilidad**: Debe ser posible probar que el sistema permite a los pacientes reservar citas en línea.

#### Paso 2: Especificar la prueba
- **Prueba de reserva de cita**: Un usuario simulado intenta reservar una cita en línea siguiendo los pasos descritos en el requisito.

#### Paso 3: Realizar la prueba
- **Proceso de reserva**: El usuario simulado selecciona una fecha y hora disponibles, proporciona información personal y confirma la cita.

#### Paso 4: Verificar el resultado
- **Confirmación de reserva**: Verifica que la cita haya sido reservada correctamente. La cita debe aparecer en el calendario del paciente y en el sistema de la clínica.

#### Paso 5: Medir el éxito
- **Criterios de éxito**: La cita debe aparecer en el calendario del paciente y en el sistema de la clínica sin errores.

Siguiendo estos pasos, puedes asegurarte de que la aplicación para pedir citas médicas cumple con el requisito de reservar una cita correctamente.

Fuentes:
- 5 - Requisitos.pdf, p. 13: Requirements imprecision
- nasa-handbook.pdf, p. 210: Appendix C: How to Write a Good Requirement— Checklist
- 6 - Procedimiento requisitos.pdf, p. 11: Verificar la calidad de los requisitos del sistema
- 5 - Requisitos.pdf, p. 61: Interviews in practice
- 7 - Modelos.pdf, p. 38: Tabular description of the ‘Transfer data’ use-case
