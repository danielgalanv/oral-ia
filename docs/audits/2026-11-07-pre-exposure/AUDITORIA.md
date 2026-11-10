# Auditoría previa a abrir el autoestudio a alumnos por túnel (07-11-2026)

Alcance: código del chat de alumnos (`documentary/*`, `course_dialogue/*`, scripts), pruebas de carga ya hechas y estado del repositorio. No se ha probado con alumnos reales ni con el túnel. Cada hallazgo indica su evidencia.

## A. Antes de exponer (bloqueantes)
1. **Acceso: cualquiera que llegue recibe permisos de inspección.** `POST /documentary/enter` (`documentary/__main__.py:167`) emite sin credencial una concesión de rol `teacher`; la API la exige para todo `/api/`. Detrás de un túnel sin identificación, es acceso abierto. Además `_local_transport` (`interfaces/api/deps/local_access.py:89`) rechaza cualquier host que no sea local, así que con el dominio público el chat responde 403; el interruptor `ORALIA_ALLOW_LAN=1` desactiva también las comprobaciones de host y origen, no sirve. Hace falta: lista de hosts públicos permitidos, validación del JWT de Cloudflare Access (emisor, audiencia y correo `@alumnos.upm.es`) y emitir la concesión solo desde esa identidad.
2. **Superficie de más.** El servidor del chat también sirve `/api/v1/documentary/{id}/pages` (texto completo de las páginas), `/original` (PDF íntegros), `/preview/{página}`, `/api/v1/retrieval` (búsqueda libre sin tope, usa la GPU) y la ruta `/tecnica`. `CONTRIBUTING.md` avisa de que los PDF y sus derechos no forman parte de una promesa de distribución pública. Decidir qué ve el alumno: lo razonable es solo las páginas citadas en sus respuestas y cerrar `/retrieval`, `/pages` completo y `/tecnica` en el modo alumno.
3. **Sin límites por alumno.** No hay límite de ritmo ni de cola (`grep` de limitadores: ninguno; el único tope es de intentos de login). Un alumno que programe peticiones monopoliza el semáforo de 4 turnos y la GPU; además `/documentary/enter` puede llenar el tope de 4096 concesiones (503 para todos durante una hora). Hace falta: un turno en curso por alumno, N turnos por minuto, cola máxima con mensaje de "servidor ocupado" y límite de concesiones por identidad.
4. **Cookie sin `Secure`** (solo `httponly` y `samesite=strict`), válida solo para HTTP local; con HTTPS del túnel debe llevarlo.
5. **Datos personales.** Cloudflare ve todo el tráfico (preguntas y respuestas) y registra los correos de Access; `registro-avisos/` guarda preguntas de alumnos sin política de conservación. Hay que decidir con quien corresponda (protección de datos de la UPM): base legal, aviso a los alumnos, plazo de conservación y pseudonimizar el correo si se asocia a avisos.

## B. Operación (importantes)
1. **GPU dedicada.** Medido: con la GPU libre, 10 alumnos a la vez dan ~10 respuestas/min (media 49 s en ráfaga, un alumno solo 10 s); con otro proceso en la GPU, el prompt del 14B bajó de miles a 77 tok/s y hubo respuestas de más de 2 min. Definir que durante la clase la GPU no se comparte y comprobarlo en el arranque.
2. **Sin supervisor.** El lanzador es manual: si cae un servidor llama.cpp o el servidor del chat nadie lo reinicia; `/health` solo responde "ok" sin comprobar los modelos. Hace falta un `/health` real (modelos, ranking, cola) y un script de reinicio.
3. **Sesión.** La conexión caduca a los 15 s sin actividad (pierde el historial en conexiones móviles inestables); la sesión global termina a los N minutos y el servidor se cierra sin aviso previo al alumno.
4. **Sin métricas.** No hay latencia, errores ni cola visibles; el docente no sabe si la clase va bien. Un panel mínimo (solo docente) basta.
5. **Espera de 30–90 s en ráfagas** con solo "Preparando la respuesta… N s". Sin posición en la cola ni respuesta parcial.

## C. Calidad
1. Revisor validado solo con errores inyectados y 24 respuestas reales; cobertura sobre errores reales desconocida. El registro de avisos y la página docente cubren la mejora con datos reales, pero no registran respuestas sin aviso.
2. Fallo conocido de contenido: el generador atribuyó a IEEE 830 la estructura de unas diapositivas; solo se detecta si la norma tiene sigla y número.
3. Controles web (apoyo/compatibilidad) medidos solo en prueba sintética; ampliación web real ejercitada una vez.
4. Recuperación evaluada con preguntas sintéticas; los seguimientos ("y eso?") no se han probado en el chat real con el recuperador nuevo.

## D. Mantenimiento
1. **No hay control de versiones** (el directorio no es un repositorio git) ni copia de seguridad: todo el trabajo de estos días, la documentación y los datos docentes dependen de un solo disco.
2. El servicio de ranking usa el Python de otro proyecto (`D:\ai-toolkit\venv`); si cambia, el chat sin ranking no arranca.
3. 11 tests antiguos fallan (parados por decisión del docente) y los e2e no se ejecutan (falta `pnpm`); la verificación descansa en 1342 tests unitarios y pruebas manuales.
4. `.claude-scratch` tiene 829 ejecuciones (121 MB); rutas absolutas `D:\` en scripts; `CONTINUAR.md` ya es largo.

## E. Replanteamientos a considerar
1. **Mostrar la respuesta antes de la revisión**: pasarla por streaming y añadir el aviso cuando termine el revisor. La espera percibida pasaría de 10–60 s a ~1 s hasta el primer texto; coste: el alumno puede ver unos segundos una respuesta que luego lleva aviso. Decisión docente.
2. **Mantener la arquitectura** (GPU local + túnel + turnos programados) para un piloto de ≤20 alumnos; si crece, un servidor con GPU propia. Un único modelo para generar y revisar quitaría los turnos de GPU, pero el 24B juzgó mal el alcance y como generador no está medido: no ahora.

## Orden propuesto
1) Acceso (A1, A4) y superficie (A2) · 2) límites por alumno (A3) · 3) git y copia de seguridad (D1) · 4) `/health` real, reinicio y GPU dedicada (B1–B2) · 5) respuesta en streaming (E1) · 6) decisión de protección de datos (A5, en paralelo desde ya).
