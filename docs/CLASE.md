# Clase con el autoestudio: guion del docente

Objetivo: los alumnos solo abren la web y empiezan. Todo lo demas lo hace `scripts\clase.ps1`.

## Una vez (antes del primer dia)
1. **Cloudflare (lo haces tu en el panel):**
   - En el tunel que ya usas, añade una ruta publica `estudio.<tu-dominio>` -> `http://localhost:8037`.
   - Crea una aplicacion de **Cloudflare Access** sobre ese host con la politica «el correo termina en `@alumnos.upm.es`». Copia su *Application Audience (AUD) tag* y el dominio de tu equipo (`<equipo>.cloudflareaccess.com`).
2. Copia `config\clase.ejemplo.json` a `config\clase.json` y rellena `hosts`, `team` y `aud` (no son secretos; el fichero queda fuera de git). `minutes` es la duracion de la clase y `slots` los alumnos que se procesan a la vez (4 con la GPU libre).
3. Proteccion de datos: el visto bueno del DPD (ver `docs\PROTECCION-DATOS.md`). Sin el, haz la primera clase en modo local.
4. **Consentimiento informado por escrito** (hoja, cuestionario y protocolo en `docs\piloto\`) (compromiso de la solicitud de la ayuda): cada participante lo firma antes de su primera sesion y se le asigna un codigo de participante. Quien no lo firme no participa. La pantalla «Entendido, comenzar» no lo sustituye.

## El dia de la clase (5 minutos antes)
1. **Cierra todo lo que use la GPU**: ComfyUI, otros `llama-server`, juegos... El sistema no cabe junto a ellos.
2. Abre PowerShell en la carpeta del proyecto y ejecuta:
   ```
   .\scripts\clase.ps1
   ```
   (`-SoloLocal` si los alumnos estan delante de este ordenador y no hay tunel; `-Minutes 90` para cambiar la duracion.)
3. Espera al cuadro verde **LISTO**. El script ya habra comprobado: GPU libre, registro de avisos vacio, los dos modelos y el ranking a velocidad normal (reinicia solo hasta 3 veces si uno sale lento), el servicio Cloudflared y que `https://estudio.<dominio>/estudio` pide identificacion.
4. Pasa a los alumnos la direccion que muestra el cuadro. Entran con su correo `@alumnos.upm.es`, leen el aviso de datos, pulsan «Entendido, comenzar» y preguntan.
5. Deja la ventana abierta: cada 30 s escribe `estado=ok alumnos=N turnos_en_curso=M`. Si sale **PROBLEMA** dos veces seguidas suena un aviso.

## Si algo falla
| Sintoma | Que hacer |
|---|---|
| El script dice que la GPU esta ocupada | Cierra ComfyUI y cualquier `llama-server` ajeno; repite |
| «El sistema no esta sano» al arrancar | Mira `%TEMP%\oralia-clase.log`; repite el script (reinicia los servicios) |
| PROBLEMA durante la clase | `Ctrl+C` y volver a lanzar `clase.ps1`: los alumnos tendran que pulsar «Comenzar» de nuevo (pierden el historial) |
| Los alumnos ven respuestas muy lentas (>1 min) | Algo mas usa la GPU; ciérralo. Con 10 a la vez la espera media medida es de ~50 s |
| Cloudflare responde pero la web da 403/404 | Comprueba que `hosts` en `clase.json` es exactamente el nombre del host publico |
| «Acceso denegado» a un alumno | Su correo no termina en `@alumnos.upm.es` o Access no le ha dado entrada |

## Al terminar
- `Ctrl+C` (o espera: la sesion del servidor termina sola al cumplirse los minutos; los servicios se paran).
- Revisa los avisos reales: `python scripts\avisos_docente.py pendientes` o la pagina local de revision (`docs\ESTUDIO.md`). Marca acierto / falsa alarma / dudoso.
- Antes de otra clase de prueba o ensayo, vacia el registro si son datos de prueba: `python scripts\avisos_docente.py purgar todo`. Los reales se conservan hasta fin de curso o 6 meses (ver `docs\PROTECCION-DATOS.md`).

## Lo que el sistema NO hace solo
- No reinicia un servicio caido (un reinicio tira las sesiones en curso).
- No avisa al alumno de que la sesion esta a punto de caducar: pon `minutes` mayor que la clase.
- No protege de procesos ajenos que ocupen la GPU durante la clase.
