# Comprobación independiente de la demo abierta

Observación directa por navegador, 2026-10-18 20:34 UTC. Instancia existente en http://127.0.0.1:5180; no se reinició, migró ni cerró ninguna sesión.

- Inicio accesible; indica generación determinista, embeddings locales y voz real sin validar.
- Gobierno docente accesible sin credencial en la demo. Dos actividades activas: autoestudio y defensa del agua. No se modificaron configuraciones ni materiales.
- Desde la actividad de autoestudio, campos precargados con actividad válida y demo-007. Pulsar Iniciar sesión devuelve: `No se pudo iniciar la sesión: another interactive session is already active on this instance`.
- El formulario no ofrece recuperación ni cierre autorizado. La pantalla general de defensa tampoco ofrece retomar sesión: muestra únicamente código, actividad e Iniciar defensa.
- No se envió ninguna intervención de contenido, ni se cerró o borró la sesión existente. No se comprobó la identidad de su propietario y no se reutilizó por código.

Conclusión corregida: acceso web y actividades visibles comprobados. La negativa a abrir una segunda sesión era el funcionamiento esperado del límite de una sesión interactiva, no un defecto de inicio ni prueba de una regresión de Feature 010. La sesión anterior pertenecía a las pruebas del usuario. Separadamente, la demo servida no mostraba recuperación autorizada ni traducción completa del aviso; esa mejora de interfaz sigue relacionada con FR-022/023 y T037–T039/T063, sin justificar cierres automáticos ni ampliar concurrencia. Esta observación no prueba el estado de una build distinta ni acredita G1 ni los corpus sintéticos.

## Resolución del bloqueo de la comprobación

El usuario autorizó expresamente cerrar sus sesiones de prueba. Se encontró una única defensa demo activa, sin preferencia ni consentimiento de conservación. Se cerró mediante end_defense_session de la versión previa a 010 archivada y verificada por SHA256 contra evidence-baseline.json, compatible con el esquema de la demo existente. El endpoint de participante había rechazado previamente el acceso docente con 403; no se modificó autorización para eludirlo. Se utilizó el comando de aplicación local para el cierre expresamente autorizado, sin editar SQL manual, migrar la demo ni reiniciar procesos.

Resultado verificado: closed_voluntary, bloqueo liberado y cero sesiones activas; se aplicó conservación efímera según la elección existente. No se creó otra sesión para dejar el acceso libre. El bloqueo operativo de esta comprobación queda resuelto; iniciar un diálogo nuevo y validar sus respuestas sigue pendiente. No registrar este caso como fallo de exclusión mutua ni como aceptación conversacional aprobada.
