# Protección de datos del autoestudio (borrador para consultar con el DPD de la UPM)

No es asesoramiento jurídico: es el inventario técnico y una propuesta para llevar a la persona responsable (Delegado de Protección de Datos / servicio jurídico). Estado: sin decidir.

## 1. Qué datos hay y dónde
| Dato | Dónde | Identifica al alumno | Observación |
|---|---|---|---|
| Correo `@alumnos.upm.es` | Cloudflare Access (registros de acceso) y memoria del servidor mientras dura la sesión | Sí | El servidor no lo escribe en disco; Cloudflare lo conserva según su política |
| Preguntas y respuestas | Memoria de la sesión; Cloudflare las ve en tránsito (HTTPS termina en Cloudflare) | Indirectamente (texto libre) | El alumno puede escribir datos personales en una pregunta |
| Avisos y rechazos | `registro-avisos/avisos.jsonl` | No: guarda pregunta, respuesta, fuentes y veredicto, sin correo ni sesión | Sin plazo de conservación; fuera de git; no entra en la copia en la nube |
| Etiquetas del docente | mismo fichero | No | |
| Modelos | Locales (llama.cpp, GPU local) | — | Ningún texto del alumno sale a servicios de IA externos |

## 2. Riesgos
1. Cloudflare actúa como encargado/tercero: ve el tráfico y los correos. Hay que ver si la UPM ya tiene contrato con ellos (se usa para otra aplicación).
2. Texto libre: una pregunta puede contener datos personales o de terceros; se guarda en el registro si genera aviso o rechazo.
3. Sin plazo de conservación del registro.
4. No se avisa al alumno de que sus preguntas pueden revisarse.

## 3. Propuesta
- **Finalidad**: apoyo al aprendizaje y mejora del sistema por el docente; no se usa para evaluar ni calificar al alumno.
- **Base**: a decidir por el DPD (misión de interés público docente o consentimiento informado). Si es consentimiento, debe poder rechazarse sin perjuicio y habría que añadir una casilla previa al acceso.
- **Minimización**: no asociar el correo a las entradas del registro (ya es así). Mantenerlo así: si algún día se quiere ligar, pseudonimizar con un identificador no reversible.
- **Conservación**: borrar `avisos.jsonl` al terminar el curso o 6 meses tras la última clase, lo que ocurra antes; borrar las entradas ya etiquetadas tras extraer las estadísticas. (Pendiente de implementar un comando `--purgar` si se aprueba.)
- **Acceso**: solo el docente, en local (la página de revisión escucha en 127.0.0.1).
- **Aviso al alumno** (texto propuesto, para mostrar antes de entrar o en la página de bienvenida):

> Este asistente de estudio funciona con modelos de lenguaje que se ejecutan en un ordenador de la universidad; tus preguntas no se envían a servicios de IA externos. Para acceder se comprueba tu correo @alumnos.upm.es mediante Cloudflare Access. Cuando una respuesta recibe un aviso de posible error o el asistente rechaza una pregunta, el texto de la pregunta y la respuesta (sin tu nombre ni tu correo) se guarda para que el profesor revise y mejore el sistema, y se borra al terminar el curso. No escribas datos personales tuyos ni de otras personas. Las respuestas pueden contener errores: contrástalas con el material. El uso es voluntario y no afecta a tu calificación.

## 4. Decisiones (07-11-2026, docente)
1. Base legal propuesta: **interés público docente** (sin casilla de consentimiento; el DPD debe confirmarlo).
2. Conservación: **fin de curso o 6 meses**, lo que ocurra antes. Comando: `python scripts/avisos_docente.py purgar <días>|todo` (imprime antes el resumen; borra avisos y etiquetas).
3. Aviso: **pantalla previa con «Entendido, comenzar»** (texto en `DiagnosticStudy.tsx`; web compilada y comprobada (tsc, eslint, vite)).
4. Cloudflare: **no hay contrato/acuerdo UPM–Cloudflare** conocido para este uso. **Bloquea abrir a alumnos** hasta que el DPD confirme que el servicio ya usado para la otra aplicación cubre también esta.

## 5. Cambio de decisión (10-11-2026, docente): consentimiento informado
La solicitud de la ayuda se comprometió a consentimiento informado específico por escrito, seudonimización con código de participante, sin audio, anonimización irreversible al cierre y resultados agregados. Por eso **se sustituye la base «interés público docente» de la decisión 1 por consentimiento informado**: la pantalla «Entendido, comenzar» no basta; cada participante firma antes de su primera sesión, con derecho a retirarse sin efecto sobre la calificación. Sigue pendiente el visto bueno del DPD (también sobre Cloudflare). Pendiente de crear: hoja de información y consentimiento, y lista de códigos de participante (fuera de git). Limitación: Cloudflare Access ve el correo en tránsito, así que la seudonimización en origen no es total con ese acceso.
