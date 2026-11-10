# Feature 005 — Configuración docente, revisión, privacidad y exportación

Completa las funciones de gobierno humano de ORAL-IA: gestión de configuraciones y materiales, revisión de sesiones consentidas, corrección de transcripciones, exportación, eliminación, retención, seudonimización y controles de acceso local.

## Propósito

El profesorado debe conservar el control operativo y documental del sistema sin acceder a más datos personales de los necesarios. Los participantes deben conocer y controlar la conservación de sus sesiones.

## Área del profesorado

Debe permitir:

- crear, duplicar, versionar, activar y retirar configuraciones de actividad;
- seleccionar materiales y versiones autorizadas;
- definir modos, preguntas iniciales, temas, límites, idioma, modalidades, conocimiento general y política de conservación;
- seleccionar modelos y agentes disponibles sin alterar sus contratos;
- revisar el estado técnico de materiales e índices;
- consultar sesiones cuya conservación esté autorizada;
- visualizar transcripción original y corregida, fuentes, agentes, verificaciones, incidencias y resumen;
- exportar una sesión o un conjunto autorizado en formatos abiertos;
- eliminar sesiones y verificar que dejan de estar disponibles;
- consultar métricas agregadas que evalúan el sistema, no al estudiante.

## Área del participante

Debe permitir:

- conocer qué datos se procesan y con qué finalidad;
- aceptar o rechazar la conservación cuando corresponda;
- usar un código seudónimo;
- revisar y corregir su transcripción;
- solicitar o ejecutar la eliminación dentro del flujo previsto;
- finalizar voluntariamente;
- consultar fuentes utilizadas y resumen descriptivo.

## Consentimiento y retención

El sistema debe distinguir entre datos necesarios durante la sesión, registros técnicos mínimos y datos opcionales conservados para el piloto. La ausencia de consentimiento no debe impedir usar el sistema cuando sea posible operar de manera efímera.

La política de retención debe estar versionada por actividad e indicar qué se conserva, durante cuánto tiempo y quién puede acceder. Las tareas de purga deben ser comprobables. El audio no se conserva en el flujo ordinario.

## Seudonimización

Las sesiones utilizan códigos sin identidad real. Si existe una tabla externa que relacione código e identidad para el piloto, queda fuera de la aplicación principal o en un almacén separado con acceso restringido. Las exportaciones para análisis agregado deben eliminar identificadores directos y revisar texto libre susceptible de contenerlos.

## Exportación

Debe existir al menos una exportación legible por personas y otra estructurada. Deben incluir configuración y versiones, transcripción autorizada, resumen, fuentes, incidencias y trazabilidad necesaria, excluyendo secretos, credenciales, razonamiento privado del modelo y datos no consentidos.

## Escenarios prioritarios

### Escenario A — Configuración versionada

El profesor modifica una actividad ya utilizada. El sistema crea una nueva versión; las sesiones anteriores mantienen referencia a la versión original y las nuevas usan la activa.

### Escenario B — Sesión efímera

Un participante rechaza conservar la transcripción. La sesión funciona, al finalizar se eliminan los datos no necesarios y queda únicamente el registro técnico mínimo definido y justificado.

### Escenario C — Revisión consentida

El profesor abre una sesión autorizada y puede distinguir entrada, transcripción original, correcciones, respuestas, fuentes, bloqueos, incidencias y resumen.

### Escenario D — Eliminación

Se solicita eliminar una sesión conservada. El sistema elimina los datos alcanzados por la solicitud, registra el resultado sin retener el contenido eliminado y confirma que ya no aparece en consultas o exportaciones.

### Escenario E — Exportación seudonimizada

El profesor exporta sesiones para analizar el piloto. El sistema excluye datos no autorizados, separa identificadores y advierte sobre posible información personal escrita en texto libre.

### Escenario F — Acceso no autorizado

Un participante intenta abrir el área docente o una sesión ajena. El sistema deniega el acceso y registra el intento sin revelar contenido.

## Acceso local

Por defecto la aplicación solo es accesible desde el ordenador anfitrión. Cualquier exposición a red local debe estar desactivada y quedar como configuración administrativa consciente; no debe habilitarse automáticamente.

## Fuera de alcance

- inicio de sesión institucional, SSO o Moodle;
- expedientes y calificaciones;
- cuadro de mando individual de rendimiento académico;
- almacenamiento en nube;
- notificaciones por correo;
- retención indefinida;
- análisis psicológico o biométrico.

## Criterios de éxito

- Toda sesión referencia una configuración inmutable y versionada.
- La negativa a conservar no impide el uso efímero y produce la purga esperada.
- Las exportaciones no contienen audio, secretos ni razonamiento privado.
- La eliminación es verificable.
- La revisión docente muestra evidencia y trazabilidad sin convertirlas en una nota.
- El acceso a datos se limita al rol y a la autorización correspondiente.
