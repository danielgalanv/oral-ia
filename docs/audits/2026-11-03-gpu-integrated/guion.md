# Revisión docente después del ensayo GPU

El ensayo ha terminado y sus servicios están detenidos. No hace falta cargar modelos para leer las respuestas.

1. Abrir la [segunda ejecución](transcript-run002-mobile.html): definición, tipos, aclaración, ejemplos funcionales y tiempo ficticio de 0,3 s. Es la ejecución que más respuestas generadas mostró (10/12); no significa que estén todas aprobadas.
2. Leer C4 y el comentario separado: cifrado y autenticación no son por sí solos requisitos incompatibles. Se conserva el texto original.
3. Comparar la [tercera ejecución](transcript-mobile.html). El perfil experimental no resolvió el ejemplo ni todos los bloqueos y no se ha promovido.
4. Consultar el [informe](report.md): el último intento web llegó al contraste documental, pero terminó a los 600 s sin explicación mostrada. No se presenta como una prueba web positiva.

## Para una nueva revisión interactiva

T queda pausado por la última indicación del usuario y no se reanudará automáticamente; comprobar la disponibilidad GPU antes de otra inferencia. La entrada normal mantiene los perfiles v1/v7, con las correcciones operativas, y no activa automáticamente los perfiles experimentales del arnés.

Desde la raíz del proyecto, cuando se vaya a hacer esa revisión:

```powershell
.\scripts\study-chat.ps1 -WebPolicy .\docs\audits\2026-11-03-cpu-completion\policy-requirements-lab-v2.json
```

Esto prepara una copia nueva compatible con el código actual. No reutilizar a ciegas rutas preparadas antes de los cambios: sus recibos detectan el cambio y deben rechazarlo.

Usar las mismas doce preguntas aprobadas; los fallos se conservan y no se reenvían automáticamente. Si una respuesta se bloquea, anotar pregunta y mensaje, sin interpretarlo como error académico del alumno. Finalizar permite descargar JSON/Markdown antes de descartar. No hay cupo educativo de preguntas; sí límites técnicos de contexto y vida del runtime. La siguiente campaña debe resolver T213/T214 y fijar controles antes de ejecutarlos.
