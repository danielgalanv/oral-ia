# Demo launcher contract v1

`.\scripts\demo.ps1` inicia foreground, pregunta credencial oculta y abre navegador
cuando API y frontend están preparados. API8010/web5180 localhost. Opciones explícitas
-ApiPort/-WebPort, -NoBrowser, -TextOnly. Nunca puertos automáticos ni descargas.
`-Action Check`: dependencias/puertos/recursos/esquema, sin contraseña ni procesos.
`-Action Stop`: otra terminal, solicitud validada al supervisor; no kill por PID ajeno.
`-Action Reset`: solo parado, muestra raíz y requiere BORRAR DEMO; rechazo/cancelación no
borra nada. No flags para eludir confirmación de borrado ni autenticación.

Interno `python -m oralia.demo start|check|stop|reset`, opciones equivalentes. Credencial
solo env ORALIA_DEMO_ADMIN_SECRET (entorno de proceso) o getpass. El shell restaura env.
Errores nozero+mensaje accionable; logs locales de hijos sin secretos; timeout de arranque
90s, Stop20s. Readiness propio no autoriza contenido; login/API006 sin bypass.
