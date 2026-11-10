# Acceso de alumnos por túnel de Cloudflare

Implementado en `src/oralia/documentary/public_access.py` (desactivado si no hay `ORALIA_PUBLIC_HOSTS`).

## Qué hace
- Solo los hosts de `ORALIA_PUBLIC_HOSTS` se tratan como públicos; cualquier otro host no local da 403.
- `/documentary/enter` por host público exige el JWT de Cloudflare Access (`Cf-Access-Jwt-Assertion`): firma RS256 con las claves de `https://<equipo>.cloudflareaccess.com/cdn-cgi/access/certs`, audiencia, emisor, vigencia y correo terminado en `@alumnos.upm.es`. Sin eso, 401.
- Una concesión por correo (entrar de nuevo revoca la anterior), máximo 10 entradas/min por correo, cookie `Secure`.
- Por host público se cierran `/api/v1/retrieval`, `/tecnica` y `/api/v1/documentary/<id>/{pages,original,preview}`. El acceso local del docente no cambia.
- Límites de turno: uno en curso por alumno (429), 6 por minuto (429) y cola global de 12 (503, "servidor ocupado").
- `/health` informa de generador, revisor y ranking (`status: degraded` si falla alguno), turnos en curso y alumnos conectados.

## Para activarlo (lo haces tú en Cloudflare)
1. Túnel de `cloudflared` hacia `http://127.0.0.1:8037` con un nombre de host (p. ej. `estudio.<dominio>`).
2. Aplicación de Cloudflare Access sobre ese host con política "correo termina en `@alumnos.upm.es`". Copia el *Application Audience (AUD) tag* y el dominio del equipo.
3. Antes de lanzar `scripts/study-chat.ps1`:
   `$env:ORALIA_PUBLIC_HOSTS="estudio.<dominio>"; $env:ORALIA_ACCESS_TEAM="<equipo>.cloudflareaccess.com"; $env:ORALIA_ACCESS_AUD="<AUD>"`

## Pendiente
- Protección de datos (A5): base legal, aviso a los alumnos, plazo de conservación de `registro-avisos/`.
- Probado solo con claves simuladas (tests); falta una prueba real con Access.
- No hay aviso al alumno antes de que la sesión global caduque.
