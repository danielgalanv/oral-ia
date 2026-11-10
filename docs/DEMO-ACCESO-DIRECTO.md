# Acceso docente directo en la demo local

Cambio solicitado expresamente por el usuario el 18 de octubre de 2026.
`scripts/demo.ps1` ya no solicita credencial: el lanzador genera un secreto interno
aleatorio y la API demo permite acceso docente local directo. Abrir Área docente.

La activación requiere el entrypoint demo, marcador de directorio válido, coincidencia
exacta de la base aislada, namespace de cookies demo y LAN desactivada. La aplicación
normal no activa este permiso por variables de entorno: create_app sigue protegida.
El filtro de origen/localhost y la propiedad de sesiones participantes permanecen.
La demo permite operaciones docentes sobre sus datos ficticios a cualquier usuario
local que la abra; no utilizar datos personales ni exponerla en red. Reiniciar tras
24 horas renueva el permiso temporal. No sustituye autenticación normal.

Verificación: 45 pruebas demo/acceso aprobadas; tras retirar import getpass y adaptar
su prueba, 29 pruebas dirigidas de acceso/progreso aprobadas. Recorrido Playwright demo
sin login docente: 1 passed (45,2 s), incluye fuentes, consentimiento, exportación,
borrado y defensa efímera. Build/lint correctos; Black/Ruff afectados correctos.
Demo preparada y detenida. Sin Reset ni cambios de datos habituales.

El comportamiento de autenticación demo difiere deliberadamente de los informes
históricos 007–009. Sus paquetes experimentales se conservan; no se afirma replay de
esos manifiestos contra estas fuentes nuevas. No se ha repetido la suite global.
