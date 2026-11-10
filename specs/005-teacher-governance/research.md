# Investigación de integración — Feature 005

## Acceso
Decisión: reemplazar auth_stub y añadir guard global previo a recepción de cuerpos.
Razón: proteger también rutas de material/configuración y sesiones ajenas; una ruta
nueva protegida no cierra las vías antiguas. Tokens aleatorios con hashes en memoria,
expiración y cookies HttpOnly/SameSite; secreto de instalación por entorno. Denegaciones
estructuradas sin URL, query, cabeceras ni contenido. Origin se valida contra host local.
Alternativas: códigos como contraseña (rechazado, identificadores no son secretos),
SSO/JWT/servicio externo (fuera de alcance), bypass sin configuración (rechazado).

## Versiones y materiales
Decisión: reutilizar ActivityConfiguration.family_id/version e inmutabilidad; tabla
ActivityGovernance separada para estado de publicación, selección de modelo y materiales
con versión. Clonar configuración, política y configuración específica de modo.
Alternativas: editar usado en lugar (rompe historia), rehacer núcleo (innecesario).
Activación valida disponibilidad y material; futuras sesiones no usan retiradas.

## Consentimiento, revisión y borrado
Decisión: política finita de la actividad y ConsentRecord existentes; preferencia del
propietario previa al cierre para modos que no transportaban consentimiento. Defensa
conserva su cierre explícito actual. La transición ganadora liquida una sola vez.
Revisión/exportación consultan vigencia a cada petición, sin confiar en visibilidad UI.
La eliminación afecta contenido propio incluso en tablas compartidas; conserva un
recibo sin contenido y evita resurrección por resultados tardíos. No borra materiales.
Alternativas: filtrar solo Transcript (deja copias), borrado diferido sin consentimiento
(incumple principio VII), conservar sesiones por defecto (rechazado).

## Exportación
Decisión: JSON con schema_version y Markdown desde la misma proyección cerrada. Alias
por lote, sin códigos/IDs directos en análisis; confirmación de revisión de texto libre
antes de incluirlo. Rechazo atómico de lote no autorizado; no archivos de servidor.
Alternativas: volcado ORM (filtra secretos), expresión regular como anonimización
garantizada (no defendible), CSV como único formato (pierde estructura de evidencia).

## Evidencia previa e incógnitas
Inspeccionados modelos y routers actuales: auth_stub no hace nada, versiones existen,
defensa tiene consentimiento, autoestudio tiene solo autorización de actividad.
Esta brecha de consentimiento se integra, no se declara resuelta por código existente.
No quedan incógnitas de requisitos bloqueantes; comprobar carreras y rollback en tests.

## Compatibilidad comprobada de privacidad

La regresión detectó expectativas históricas de guardar respuestas tras cierre sin
consentimiento. Se retiró el texto y se preservaron recibos de estructura auditables;
los tests ahora usan tokens explícitos para recursos privados y distinguen contenido
eliminado de metadatos técnicos. No se introdujeron credenciales permanentes como bearer
ni un interruptor de autorización para tests. Los cuerpos de login inválidos se saneaban
para evitar que errores de validación repitieran la credencial.
