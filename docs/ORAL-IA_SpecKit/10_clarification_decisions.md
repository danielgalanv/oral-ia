# Decisiones de aclaración recomendadas

Use estas respuestas durante `/speckit-clarify` para mantener un alcance coherente. Si Claude formula una pregunta no cubierta, elija la alternativa más simple que preserve la constitución y permita medir la arquitectura.

## Alcance operativo

- **Despliegue inicial:** un único ordenador y una única instalación local.
- **Acceso de red:** solo `localhost` por defecto. La red local queda desactivada en el MVP ordinario.
- **Concurrencia:** una sesión interactiva activa por instancia en la primera versión; pueden conservarse múltiples sesiones históricas. El diseño no debe impedir ampliar la concurrencia después.
- **Robot:** completamente fuera del MVP.
- **Internet:** no disponible durante sesiones ni para recuperación.
- **Sistemas externos:** no Moodle, SSO, correo, calendario, expedientes ni calificaciones.

## Roles

- **Profesor/administrador local:** configura actividades, materiales y revisa datos autorizados.
- **Participante:** usa actividades y controla su transcripción y conservación.
- **Mantenedor/investigador:** accede a registros técnicos y herramientas de validación.
- En modo estrictamente local puede usarse una credencial administrativa configurada durante la instalación y códigos seudónimos para participantes. No inventar una integración institucional.

## Datos y privacidad

- El audio se procesa en memoria o almacenamiento temporal y se elimina tras transcribir.
- Se conservan transcripciones solo con consentimiento y conforme a una política versionada.
- La transcripción original y la corregida se guardan como versiones diferenciadas cuando la sesión se conserva.
- La relación entre identidad real y código, si existe en el piloto, queda fuera del almacén principal de ORAL-IA.
- La negativa a conservar debe permitir una sesión efímera.
- Los registros no incluyen razonamiento privado del modelo, secretos ni prompts del sistema completos cuando contengan información sensible; sí resultados y decisiones estructuradas necesarias para auditoría.

## Conocimiento y fundamentación

- El conocimiento general del modelo está desactivado por defecto.
- Puede habilitarse por actividad y debe quedar etiquetado.
- Una consulta sin evidencia suficiente no se responde como hecho de la asignatura.
- Los conflictos entre materiales se muestran como conflicto, no se resuelven inventando una autoridad.
- Las fuentes deben identificar documento, versión y ubicación.

## Arquitectura de agentes

- Los agentes son componentes invocables dentro de una aplicación, no procesos autónomos obligatorios.
- La composición dinámica selecciona agentes existentes, orden, parámetros y estrategia; no genera código.
- Las salidas entre agentes usan esquemas estructurados y versionados.
- Los controles constitucionales son obligatorios en toda salida visible.
- El generador no puede aprobar su propia salida.
- Las K-lines son configuraciones reutilizables propuestas o registradas; su activación permanente requiere revisión humana.

## Estado y reproducción

- El estado cognitivo vive fuera del contexto del LLM y utiliza versionado optimista o mecanismo equivalente para detectar conflictos.
- Una sesión reproducible significa reconstruir entradas, configuración, agentes, versiones, evidencias, decisiones y cambios de estado.
- No se garantiza identidad textual de modelos generativos salvo ejecución determinista explícita.
- Los cambios de configuración crean versiones nuevas; no alteran retrospectivamente sesiones antiguas.

## Voz

- Texto es la modalidad completa y obligatoria.
- Voz es opcional.
- Baja confianza en términos relevantes exige corrección o aclaración.
- Fallo de STT o TTS degrada a texto.
- No se realizan análisis de emoción, prosodia, identidad de voz ni biometría.

## Evaluación

- No se asignan notas ni se aplica una rúbrica automáticamente.
- El resumen es descriptivo: temas, preguntas, dudas, fuentes e incidencias.
- Dificultad orientativa sirve para seleccionar preguntas, no para clasificar al estudiante.
- Las métricas evalúan el sistema y la arquitectura.

## Errores y recursos

- Un timeout no debe corromper estado ni bloquear indefinidamente la sesión.
- Si falla un componente opcional, se degrada; si falla un control obligatorio, no se muestra la salida.
- Las prioridades son: privacidad y seguridad, interacción activa, transcripción, verificación, generación, registro esencial y análisis secundarios.
- Los límites exactos de tiempo y recursos son configurables y se fijarán en el plan o en perfiles de hardware, no como constantes universales del requisito.
