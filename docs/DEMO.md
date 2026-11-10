> Guía de un demostrador anterior. Para el chat actual y el estado del proyecto, consultar [ESTUDIO](ESTUDIO.md) y [CONTINUAR](CONTINUAR.md). No acredita por sí sola el piloto generativo actual.

# Demostración local de ORALIA — unos diez minutos

Estado de la Feature 010: implementación guiada integrada, con aceptación todavía pendiente. Los paquetes ficticios se publicaron y ensayaron solo en un entorno aislado; no se instalaron en la demo personal. El cuarto conjunto reservado cumple el umbral de clasificación: 12/12 conversaciones y 46/48 actos (36/36 críticos); faltan la revisión humana de sistema y el cierre de preservación. G2 no aprobado; utilidad humana y voz real pendientes. Evidencia y límites en [evidencia 010](../specs/010-guided-dialogue/implementation-evidence.md).

## Preparación previa

Desde `D:\Proyecto personal\ORALIA`, Windows/PowerShell, Python3.12, uv y Node18+:

```powershell
uv sync --extra dev
pnpm.cmd --dir apps/web install
.\scripts\demo.ps1 -Action Check
```

Instalar dependencias requiere conexión o cachés preparadas. Check no descarga modelos,
no arranca servicios y no pide credencial. El recorrido con fuentes necesita el modelo
`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` ya disponible localmente.
Si falta, prepararlo explícitamente en una terminal con conexión antes del ensayo:

```powershell
uv run --no-sync python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"
```

Ese comando es una descarga voluntaria, separada del arranque. Si el equipo impone modo
offline, su administrador debe preparar la caché antes; no lo desactiva el lanzador.
Alternativa sin modelo local: `.\scripts\demo.ps1 -TextOnly`, con texto sin fuentes;
no se presenta como demostración de recuperación. Cambiar entre ambos perfiles exige
Reset explícito, porque las actividades ya publicadas son inmutables.

## Un comando de arranque

```powershell
.\scripts\demo.ps1
```

La demo local no pide credencial: Área docente se abre directamente. Usar solo datos
ficticios. Este acceso está limitado al lanzador demo, su base aislada y localhost;
el arranque normal de ORALIA conserva autenticación. Las sesiones participantes siguen
requiriendo su autorización propia. No publicar esta demo en red.
El lanzador busca Node en el PATH y, si falta, en instalaciones locales conocidas,
incluido el runtime de Codex si está presente. Solo añade su carpeta al PATH durante
esta ejecución y lo restaura al terminar; no instala paquetes ni cambia el PATH permanente.
El script usa UTF-8 con BOM para admitir también Windows PowerShell 5.1.
Se genera un secreto interno efímero sin mostrarlo. Para pruebas automatizadas
puede suministrarse `ORALIA_DEMO_ADMIN_SECRET` solo en entorno de proceso; no usar argumentos,
archivos .env ni scripts con una contraseña. No hay contraseña demo predeterminada.

API `http://127.0.0.1:8010`, web `http://127.0.0.1:5180`. El navegador se abre tras verificar
ambos servicios y calentar embeddings en la API. La consola muestra DEMO LISTA. Es normal
que cargar recursos locales tarde algunos segundos. Sin navegador automático: `-NoBrowser`.
Si PowerShell restringe scripts, seguir la política del equipo; alternativa equivalente:
`uv run --offline --no-sync python -X utf8 -m oralia.demo start`. No cambiar políticas globales.

Los datos están en `.oralia-demo` y el lock en `.oralia-demo.lock`; no se usa `oralia.db`
ni `.oralia_data`. Índice/archivos/tmp/config/cache Vite/logs propios. Modelo de embeddings
en caché es un recurso de lectura compartido, no el índice habitual. Las cookies
`oralia_demo_admin`/`oralia_demo_participant` no sustituyen las del entorno habitual.

## Guion listo para presentar

| Minuto | Acción | Qué explicar |
|---|---|---|
| 0–1 | Mostrar portada y abrir Área docente directamente, sin credencial. | Acceso demo local, solo datos ficticios. IA con errores posibles; no califica. Generación determinista, no LLM real. |
| 1–2 | En Versiones de actividad desplegar Materiales disponibles y estado. | Curso ficticio sobre agua, DOCX breve activo y fragmentos reales indexados. Política1día y versiones activas. El archivo está en `.oralia-demo/files/agua-demo.docx`. |
| 2–3 | En Demo: autoestudio del agua, pulsar Abrir actividad de autoestudio. Escribir `demo-007` e iniciar. | ID ya seleccionado. El código es seudónimo, no autenticación. API emite autorización secreta propia; una sola sesión activa. |
| 3–5 | Leer aviso, seleccionar Conservar transcripción de esta sesión y Conservar resumen de esta sesión. Preguntar «¿A qué temperatura hierve el agua?». Desplegar Fuentes con teclado. | Respuesta extractiva, documento/versión/ubicación y fragmento recuperado. No confundir embeddings reales con generación LLM. Conservación voluntaria por ámbitos. |
| 5–6 | Finalizar sesión. Volver al inicio y al área docente. Abrir Revisar sesión. | Solo contenido cerrado, vigente y consentido. Revisar entradas, respuesta, fuentes y decisiones; no hay nota. |
| 6–8 | Seleccionar la sesión, Incluir texto libre autorizado y confirmar revisión de todo el texto. Descargar JSON y Markdown. | Alias por lote y campos permitidos. La revisión humana sigue siendo necesaria: no anonimización perfecta. Archivos solo en descarga del navegador. |
| 8–9 | Confirmar eliminar el contenido de esta sesión y pulsar Eliminar sesión revisada. | Recibo sin contenido. Ya no está disponible para revisión ni exportación. La prueba automatizada comprueba ambas denegaciones. |
| 9–10 | Abrir actividad de defensa. Usar `demo-007`, iniciar por texto y responder «El agua hierve a 100 grados». Dejar conservación desmarcada y finalizar. | Alternativa efímera. La sesión funciona pero no es revisable al cerrar. Voz real y utilidad con personas siguen sin validar. |

Si conservas una defensa, el cierre ofrece revisión textual y confirmación. Si eliges
no conservar, no hay un segundo permiso implícito: se elimina el contenido al cierre.
Los bloques JSON de revisión/resumen siguen disponibles; su rediseño queda para después.
Para repetir el guion sin reset, cerrar la sesión activa anterior. El seed no duplica
curso/material/actividades ni borra sesiones. Las descargas ya guardadas en tu navegador
son externas al entorno demo; el borrado del servidor no elimina archivos descargados.

## Progreso visible del arranque

La consola informa etapas reales en español. `[INICIO]` indica una operación en curso;
`[OK]` aparece al terminarla. El orden es dependencias y puertos, comprobación/carga de
embeddings locales (solo perfil full), esquema existente, preparación de datos e índice,
inicio de API, inicio de interfaz y espera de disponibilidad. En TextOnly se preparan
solo datos y no se anuncia carga de embeddings ni fuentes disponibles.

«Proceso iniciado; disponibilidad pendiente» no significa servicio listo. La API full
calienta su propio modelo en un proceso distinto; se conserva esa comprobación. Solo
tras verificar la respuesta propia de ambos servicios aparece `DEMO LISTA`, su URL y
«Ctrl+C o .\scripts\demo.ps1 -Action Stop»; entonces se abre el navegador salvo NoBrowser.

Si una etapa dura, cada cinco segundos aproximadamente aparece, por ejemplo:

```text
[ESPERA] Espera de disponibilidad: 5s transcurridos. La carga inicial puede tardar; la operación sigue en curso.
```

El tiempo corresponde a esa etapa, sin porcentaje ni estimación de tiempo restante del
lanzador. Las bibliotecas pueden mostrar sus propios contadores medidos de carga de pesos.
Los avisos no prueban avance interno ni sustituyen el timeout: preparación120s,
disponibilidad90s. Al terminar, fallar o cancelar la etapa cesan los avisos.

`[FALLO]` identifica etapa, causa conocida y acción. Si la causa no se determina, lo dice
sin inventarla; el diagnóstico saneado está en `.oralia-demo/logs/startup.log` cuando la
raíz es válida y escribible, además de prepare.log/api.log/web.log. No se crea otra ruta
para diagnosticar un entorno no reconocido. `[CANCELADO]` es diferente de fallo y no
anuncia etapa completada. Credenciales y variables de entorno completas no se imprimen.
Check sigue sin pedir credenciales ni iniciar servicios: mensajes en stderr y JSON final
en stdout; es compatible con `scripts/check-demo.ps1` y redirección de salida UTF-8.

Se ha eliminado la comprobación completa duplicada CLI→supervisor: ahora se ejecuta una
vez dentro del bloqueo y antes de pedir la credencial. Se mantienen preparación/esquema,
validación de Node/Vite antes del lanzamiento y calentamiento propio de API; son controles
con fines o procesos distintos. No se atribuye mejora de rendimiento sin comparación.

Ensayo008 con recursos preparados y NoBrowser: primer arranque observado17,875s hasta
DEMO LISTA; posterior17,688s. No son cargas de caché fría ni tiempo de instalación/modelo.
El primero ya tenía dependencias/caché preparadas; las duraciones dependen del equipo y
carga simultánea. Datos habituales/demo sin cambios y ningún Reset durante el ensayo.
Resultados, eventos temporales y comandos en `specs/008-demo-startup-progress/`.

## Parada y reinicio de datos

Ctrl+C en la terminal de arranque, o desde otra terminal:

```powershell
.\scripts\demo.ps1 -Action Stop
```

Solo detiene API/frontend y preparación propios; no cierra el navegador ni procesos
ajenos. Los datos se conservan. Volver a arrancar no solicita credencial en modo demo:
reinicio de proceso invalida tokens antiguos. Para restaurar fixtures desde cero:

```powershell
.\scripts\demo.ps1 -Action Reset
```

Primero parar. Se muestra la ruta exacta y se exige `BORRAR DEMO`; cualquier otra entrada
cancela. Se comprueba marcador, raíz y ausencia de enlaces/junctions antes de borrar.
Nunca acepta una carpeta habitual como destino. Después del reset volver a arrancar.
El pequeño lock externo se conserva para impedir carreras entre operaciones.

## Solución de problemas

| Situación | Acción |
|---|---|
| Puerto ocupado | No se mata nada ni se cambia puerto. Liberarlo voluntariamente o elegir `-ApiPort 8011 -WebPort 5181` explícitamente; conservar esos parámetros para Check. Stop lee los puertos del lanzamiento propio. |
| Falta uv/Python/Node/Vite | Preparar dependencias con los comandos iniciales. El lanzador no instala silenciosamente. |
| Faltan embeddings | Preparación voluntaria con conexión o `-TextOnly` (sin fuentes), nunca evidencia simulada. |
| Demo activa / segunda operación | Usar Stop o Ctrl+C; después reintentar. Reset durante ejecución se rechaza. |
| 409 al iniciar sesión | Ya existe una sesión activa; finalizarla en su pestaña. Si se perdió acceso, Reset explícito solo de demo tras parar. |
| Credencial / reinicio | En demo no se pide credencial. El acceso normal de ORALIA sigue protegido. |
| Actividad retirada/modificada o cambio de perfil | No se reescribe una versión usada. Revisar en Gobierno o Reset confirmado para volver al guion inicial. |
| Fallo de extracción/índice/esquema | Ver `.oralia-demo/logs/prepare.log`. Se migran solo datos demo; instalación limpia incluye corrección del lock de índice en007. No usar create_all para ocultar fallos. |
| Timeout o hijo terminado | Se limpian hijos propios; revisar logs/api.log y logs/web.log, verificar recursos y reintentar. |
| Recibo no reconocible / PID reciclado | No se mata ningún PID. Revisar la terminal original y usar Ctrl+C; no borrar recibos para forzar operaciones sobre procesos no verificados. |
| Sin apertura automática del navegador | Abrir la URL anunciada, o usar -NoBrowser. Los servicios siguen locales. |

## Validación y límites

Pruebas en `tests/demo`, recorrido real en `tests/e2e/test_demo_journey.spec.ts`. Ensayo
PowerShell y centinelas en `specs/007-local-demonstration/validation-demo.json`; gates y
tabla completa en implementation-evidence.md. No se utiliza base habitual para pruebas.
El ensayo offline prohíbe sockets externos y usa embeddings/Chroma reales; el navegador
rechaza peticiones externas. No equivale a validar voz, LLM o utilidad humana.

Paquete006 original preservado y fuente correspondiente archivada en007. El paquete
reproducido con código007 vive separado en `evidence006-current`; no se modifican hashes
para hacer pasar el original por código nuevo. No se hacen commits ni cambios de T090/T150.


## Diálogo guiado 010: operación y límites actuales

El perfil `guided_controlled` usa unidades docentes publicadas, no un LLM libre.
El proveedor efectivo se muestra como `reviewed-unit-renderer/v1`; avisos fijos usan
`fixed-dialogue-template/v1`. Una respuesta degradada no demuestra que el contenido
sea suficiente. Los cinco modos de estudio requieren habilitación explícita;
la defensa conserva su pregunta y las restricciones de solución.

Los materiales ficticios editables están en `materiales/docente/dialogue/`.
Su publicación exige revisión docente, versiones activas y políticas explícitas.
No se instalan automáticamente sobre las actividades existentes. Conservar el
material breve original permite demostrar límites de cobertura.

En una actividad preparada, usar Repetir, Otra forma, Ayuda y Continuar con teclado.
Cambiar de tema exige confirmación cuando corresponde. Recuperar sesión requiere
la autorización propietaria conservada en ese navegador; el seudónimo no recupera
permisos perdidos. El área docente permite cerrar una sesión activa solo tras
confirmación; no fabrica consentimiento ni conserva contenido por ese cierre.

Si un envío queda sin resultado por un fallo de transporte, consultar su estado con
el control de reconciliación antes de enviar otro. La consulta no vuelve a generar
la respuesta ni promete recuperar contenido ya retirado o borrado. Los recibos
no contienen el texto de la conversación.

Al cerrar, elegir por separado transcripción y resumen. La alternativa efímera deja
ambos sin conservar; al terminar se limpian la transcripción y el contexto del navegador. El resumen devuelto por el cierre se muestra una sola vez, sin persistirlo; la eliminación explícita limpia también esa vista. La
revisión y la exportación requieren ámbitos vigentes. La eliminación y la caducidad
impiden reproducir el contenido desde recibos o contexto.

Ensayo medido en un workspace temporal propio y PowerShell con PATH de máquina y
usuario: 33,687 s en el primer arranque observado y 16,141 s en el siguiente preparado.
No se verificó una carga fría del modelo. Se bloquearon conexiones Python externas
del ensayo y se mantuvieron recursos locales preparados; no se afirma desconexión
física del equipo. Se verificaron ambos servicios, parada de procesos propios y
persistencia idéntica de `oralia.db`, base y fixtures de la demo habitual. No se usó
Reset. Detalle: `specs/010-guided-dialogue/operational-rehearsal/result.json`.

Las nueve llamadas reales al modelo local del estudio de viabilidad no habilitan
su publicación. La comparación determinista de 24 casos por condición no prueba
superioridad educativa ni rendimiento causal. Los primeros fallos reservados se
conservan y sus regresiones posteriores se etiquetan como desarrollo.


### Estado del diálogo guiado 19-10-2026

Correcciones de repetición por objeto, continuidad de comparación y falsos conflictos de coherencia validadas con1139 pruebas y21 recorridos de navegador. Perfil determinista de unidades revisadas, sin validación de utilidad humana ni voz real. El entorno aislado permanece preparado y detenido; no requiere Reset. Ver [guía010](../specs/010-guided-dialogue/quickstart.md), [tabla completa](../specs/010-guided-dialogue/task-evidence.md) y [24 diálogos para revisión humana](../specs/010-guided-dialogue/human-system-review-current.md). La feature permanece abierta por revisión humana y pérdida histórica de evidencia documentada.


En autoestudio guiado, cuando la API ofrece temas, las preguntas amplias muestran junto a la conversación los temas publicados. «Elegir [tema]» propone el cambio y «Confirmar tema [tema]» lo aplica; la pregunta pendiente se mantiene hasta confirmar. Los controles se deshabilitan mientras un envío está en curso o sin reconciliar. Son opciones de navegación basadas en metadatos devueltos por la API, no respuestas generativas. Revisión humana pendiente por [bloques](../specs/010-guided-dialogue/human-review-blocks/README.md).
