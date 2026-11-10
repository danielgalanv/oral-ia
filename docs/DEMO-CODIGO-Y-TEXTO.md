# Código de demo y defensa por texto

18 de octubre de 2026. Diagnóstico de las dos sesiones comunicadas por el usuario:
ambas usaban un código distinto de demo-007, mientras las políticas inmutables de
las dos actividades preparadas solo permiten el destinatario demo-007. Por ello T090
bloqueó la salida; la defensa no mostró pregunta y sus controles quedaron deshabilitados
tras el cierre seguro. No se modificaron políticas ni sesiones para eludir ese bloqueo.

Corrección de interfaz: preseleccionar demo-007 solo bajo VITE_ORALIA_DEMO_PROFILE,
explicar que el nombre real no sirve como código en estas actividades y mostrar que
la defensa preparada es textual, sin audio habilitado. El campo sigue siendo editable
para actividades nuevas con otro destinatario explícitamente autorizado.

Para probar: recargar la página, abrir la actividad desde Área docente e iniciar con
demo-007. La defensa presenta pregunta escrita y el campo «Tu respuesta». Autoestudio
admite «Hola» antes de una consulta de contenido. No hay sesiones activas bloqueando
el arranque en el momento de este diagnóstico.

Verificación HTTP real, autenticación y material: 24 passed, 1 warning, 19,27 s en
tests/integration/test_teacher_material_pack.py; ahora los casos de autoestudio envían
Hola y exigen que la sesión siga abierta antes de consultar agua y cerrar/exportar.
Build/lint y Ruff del archivo de pruebas correctos. Voz real no configurada ni validada.
