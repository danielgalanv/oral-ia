# Ampliación web restringida: entrega operativa parcial, 30-10-2026

Se implementaron y probaron T114/T115. Existe una ruta de adquisición pública original, finita y revocable, y una inspección atribuida en la interfaz existente. **No existe todavía una ruta autónoma validada que use Internet para producir una explicación académica.** T116/T117/T118 siguen abiertos. La falta de evaluador acreditado impide incorporar las afirmaciones externas como contenido establecido; no impidió completar política, transporte, extracción, recibos, UI y negativos independientes de ese evaluador.

El autoestudio sigue siendo inspección docente identificada. Feature012, FR-014, T090/T150, G2/G3/G4, SC-001, aceptación docente y participante permanecen sin aprobación nueva. No se calificó, aplicó rúbrica ni infirió capacidad de alumnos. Sin voz, GPU, CUDA, modelos nuevos, migraciones, SQL de sesiones, commits, Reset, cambios de corpus o índices.

## SpecKit: análisis previo y revisión final

Se aplicaron las skills locales `speckit-analyze`, `speckit-implement` y `speckit-converge`, con alcance autorizado T114–T118. Prerrequisitos resolvieron Feature012. Checklists: capacity-decision 8/8, final-local-candidate 9/9, requirements 12/12. No existe `.specify/extensions.yml`; no hay hooks que ejecutar. Proyecto sin Git; ignores existentes comprobados. No se regeneraron ni compactaron los artefactos.

Análisis previo acotado, comunicado antes de implementar:

| Hallazgo | Severidad | Evidencia | Decisión |
|---|---|---|---|
| Capacidad semántica aún no acreditada | Alta, pendiente planificado | plan, FR-014/022/023, T116, verificadores existentes | No confundir implementación del puerto con aprobación; bloquear incorporación externa |
| Búsqueda del chat no es servicio de ORALIA | Media, elección de diseño | Dependencias y servicios inventariados | Puerto propio y catálogo público local; comprobar alternativa sin credenciales |

Cobertura: FR-014/016/017/019/021/022/023/024 y SC-008/009 tienen tareas en el incremento o gates históricos explícitos; 5/5 tareas del incremento trazadas, sin requisitos del incremento sin tarea, duplicidades ni contradicciones constitucionales bloqueantes. Esto no es una afirmación de cumplimiento global de la feature. La autorización documental no acreditaba ya una capacidad semántica.

Convergencia final: tres hallazgos parciales altos, correspondientes a evaluadores separados, integración autónoma y medición independiente; desglosados sin borrar los pendientes originales en T151–T153. No se ejecuta otra campaña por el mero hecho de añadir tareas. Spec/plan/contrato conservan su texto previo y añaden el estado operativo. Solo se marcaron T114/T115.

## Implementación

`web_evidence.py` contiene política inmutable tipada por actividad y versión, default offline, alcance exacto de conceptos y hosts, máximo de búsquedas/páginas/bytes/tiempo/reintentos/redirecciones y recibos. El permiso solo vale en `self_study`; `exam` lo rechaza aunque tenga enabled. La carga de un archivo requiere arranque explícito con `--web-policy`. Cambiar cualquier byte del archivo revoca la vinculación original: editarlo no concede permisos nuevos en el proceso ya abierto. No se modificaron políticas de sesiones existentes.

Los presupuestos viven en el runtime de la actividad, compartidos entre reentradas; no se renuevan al abrir/cerrar inspección. El reloj web comienza al primer intento autorizado y mide tiempo transcurrido desde él. IDs repetidos no repiten tráfico ni consumo; se limita también el número de recibos. Un proceso nuevo es una nueva autorización operativa, no una recuperación transparente de cuota persistida.

Se auditaron HTTPX ya instalado, adaptadores locales de generación, extracción documental y recuperación. No había un buscador público de ORALIA reutilizable. Se eligió `CuratedPublicSearch`: catálogo pequeño de fuentes originales públicas por concepto académico, consultado localmente. No es un buscador general ni descubre sitios arbitrarios. Si no hay entrada, devuelve ausencia de evidencia. Es una alternativa pública viable sin credenciales comprobada con RFC Editor; los puertos permiten reemplazar búsqueda y transporte. No se añadió dependencia. El transporte usa biblioteca estándar para conectar a una IP pública fijada y verificar TLS contra el nombre original; una comprobación DNS anterior seguida de una conexión que resuelva otra vez no habría bastado.

Solo salen GET HTTPS a rutas del catálogo configurado por el host. No se envían preguntas, historial, recibos/IDs de sesión, PDFs privados, alumnos, audio ni credenciales. Se rechazan URL con usuario/contraseña, query, fragmento, puertos alternativos, protocolos ajenos y destinos no autorizados. Cada salto revalida URL, permiso y DNS. Una resolución privada o mixta se rechaza antes de conectar. No se usan cookies, proxies del entorno ni APIs de generación remota. 403 y otras restricciones no se sortean. El adaptador maneja HTTP/1.1, longitud/chunks, encabezados y límites; cierra su stream propio en error/cancelación. No soporta JavaScript, PDF remoto, imágenes, compresión ni autenticación: se declara extracción no disponible.

La captura conserva bytes en hexadecimal, SHA256, texto y hash, título remoto y título de catálogo, entidad atribuida por catálogo, URL pedida/final, instante, edición configurada y Last-Modified cuando llega. La entidad/edición de catálogo es procedencia declarada, no verificación independiente de autoría. Se registran descubrimiento/omisiones, documentos descargados, evidencia entregada al modelo y contenido aprobado por separado; las dos últimas listas quedan vacías. Hash igual señala una copia; hash diferente tampoco demuestra independencia. La caché no sirve de autoridad y se purga al revocar, junto con documentos de los recibos previos.

La extracción HTML elimina script/style y conserva texto inerte. Una detección limitada de instrucciones sospechosas marca cuarentena; su ausencia **no** acredita seguridad. Todo contenido externo, detectado o no, queda fuera de herramientas, instrucciones y generador. La defensa actual no depende de que una expresión regular entienda todas las inyecciones.

`web_review.py` separa respaldo externo y compatibilidad docente. Conserva testigos, identidad/simulación del revisor, todas las páginas disponibles del catálogo vinculado (no solo top-k) y los huecos conocidos. No hace clasificación semántica por palabras clave. Sin evaluadores reales ambos resultados son `unknown`; incluso los veredictos fixture no abren contenido aprobado/publicación.

`study_lab_api.py` añade un endpoint docente autenticado: exige recibo local de la misma inspección, decisión explícita de concepto dentro de alcance e insuficiencia, aviso previo y política de esa actividad. El ranking y cero pasajes no crean esa decisión. La interfaz en Materiales muestra el aviso antes del botón; solo ofrece los conceptos configurados y atribuye lo descargado bajo «Información de Internet», con enlaces separados de los PDF docentes. Muestra que es inspección, con semántica pendiente. Fallos, cancelación o revocación de web no añaden una respuesta al historial ni consumen cuota del generador. Los perfiles normales no reciben red por defecto.

**La decisión docente de esta inspección es un instrumento diagnóstico, no el sustituto de un asesor autónomo ni una obligación propuesta para cada turno futuro.** No se conectó una falsa decisión semántica automática a la generación. Tampoco se inventaron respuestas académicas prefabricadas para sortear ese pendiente.

## Pruebas y adquisición real

- **76 pruebas Python** del bloque (`python-delivery.log`): política, puertos, API, procedencia, offline/examen, decisión explícita y alcance incierto/excluido, consulta sensible, aviso, DNS privado/mixto, redirección privada y límites, reintentos, bytes, extracción insuficiente/formato no soportado, acceso denegado, inyección inerte, copias, revocación durante descarga, cancelación, timeout, red caída, duplicados y continuación. Los tests del parser real usan streams simulados: comprueban IP fijada, hostname TLS, HTTP, headers, cierre y ausencia de cookies/credenciales.
- **123 regresiones Python** (`regressions-final.log`): recuperación/cuota/capacidad, proveedores con dobles CPU, perfiles documentales, RAG, conversación y revisión estructural existentes. No se cargó un modelo generativo. Total entre ambos conjuntos: **199 pruebas Python**.
- **14 pruebas UI CPU** (`ui-final.log`): política y SSR de componentes reales, aviso offline/previo, controles, enlaces, origen separado, duplicados e inercia de HTML. No es un recorrido de navegador ni un ensayo semántico.
- TypeScript, Vite y ESLint aprobados (`tsc.log`, `build.log`, `lint.log`). Build aislado en `web-dist/`; no se sustituyeron builds anteriores.
- Black y Ruff de archivos modificados correctos. Ruff global conserva **10 diagnósticos existentes, cero nuevos**, comparados por Counter de ruta relativa/código/mensaje con multiplicidad. No se afirma que Ruff global esté limpio. La comparación de hashes verifica los **308 archivos históricos** del manifiesto previo sin cambios. Véase `final-checks.json`.

La integración HTTP verifica que un turno local mostrado conserva sus dos mensajes de contexto después de la adquisición; la descarga no llama al generador, no añade texto externo y la siguiente pregunta local pasa de cuota 1 a 2. El mismo ID no vuelve a descargar. Revocar web limpia los documentos y permite continuar localmente. Las pruebas fixture de compatible/conflicto/incierto comprueban que el contrato recibe una página fuera del top-k y declara huecos; **no prueban que un evaluador descubra el significado de esa página**.

Comprobación real separada: `public-probe-001.json`/`.log`. Propósito congelado en el runner: adquirir únicamente terminología normativa de niveles de requisitos desde la fuente original RFC Editor, sin sesión de alumno ni afirmación de insuficiencia del curso. Presupuesto: 1 búsqueda local, 1 página, 32.768 bytes, 20 s globales/10 s por solicitud, 0 reintentos, hasta 1 redirect permitido. Resultado: **1 GET, 4.723 bytes, sin errores, sin reintentos**, estado `acquired_unreviewed`, captura y texto completos. Fuente: [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt), marzo de 1997; no se adquirió aquí su actualización RFC 8174. No se oculta ese límite de edición.

La prueba real demuestra transporte/extracción. No prueba validez de las afirmaciones, vigencia suficiente para una explicación, compatibilidad con material docente, elección autónoma de fuente ni respuesta generativa. No hubo nuevas respuestas de LLM: no existe una transcripción generativa que presentar como si se hubiera producido. Los fragmentos íntegros capturados están en el recibo y en `public-source.txt`.

Fallos de herramientas conservados: un primer comando de regresión señaló una ruta de test inexistente (no ejecutó pruebas); se corrigió a `test_lab_conversation.py`. `npm` no estaba en PATH; se ejecutaron directamente las herramientas instaladas con Node. Black con workers múltiples quedó esperando; solo se detuvieron sus dos procesos propios identificados y se completó con `--workers 1`. No se detuvo ningún proceso ajeno ni se inició servidor nuevo en esta comprobación. Las advertencias de pytest son la deprecación preexistente de Starlette/httpx; no se cambió dependencia para silenciarla.

## Límite semántico preciso

Se revisaron `course_dialogue/verification.py`, `claim_review.py`, `review_repair.py`, `conversation_lab.py` y la evidencia previa de revisión. Los primeros validan estructura/citas/testigos; declaran expresamente que no juzgan entailment o verdad. La autocrítica ya medida en la campaña anterior no se promovió; no se reabrió ni se reinterpretó. Un puerto inyectable no aporta un evaluador acreditado. Tampoco basta un HTTP 200 o la entidad RFC Editor.

Por tanto **no se acredita comparación semántica con casos inéditos no usados para ajustar**, ni compatibilidad por terminología distinta, ni detección automática de una contradicción real fuera del top-k, ni falsedad/independencia de una fuente. No hay candidato validado disponible en esta entrega CPU para medir honestamente esa capacidad. Los positivos con dobles verifican flujo y mantienen bloqueada la incorporación; no se presentan como evidencia positiva de cobertura académica. No se afirma que dos textos distintos sean contradictorios ni que el profesor sea infalible. Sigue pendiente separar y medir falsos permisos, falsos conflictos y cobertura en casos nuevos antes de integrar explicaciones.

## Archivos y uso

Código modificado: `src/oralia/documentary/__main__.py`, `study_lab_api.py`, `apps/web/src/components/DiagnosticStudy.tsx`. Nuevos: `src/oralia/documentary/web_evidence.py`, `web_review.py`, `apps/web/src/components/WebInspection.tsx`, `scripts/check_web_acquisition.py`. Pruebas: `tests/unit/test_web_evidence.py`, `test_study_lab.py`, `test_study_runtime_ui.mjs`. Documentación: spec/plan/tasks y adenda de contrato web; dossier nuevo con recibos, muestra offline, build y verificaciones. `study_lab.py`, recuperación, prompts y límites generativos no se modificaron. El fingerprint del recuperador no cambia; no se creó ni reescribió un índice.

Repetición de adquisición real, con **otra ruta de salida nueva**:

```powershell
.venv/Scripts/python.exe scripts/check_web_acquisition.py <recibo-nuevo.json>
```

Para inspección en la interfaz existente, usar un proceso nuevo y una copia de `policy-example-offline.json`: autorizar manualmente esa nueva copia con enabled=true y versión nueva, sin editar políticas de sesiones existentes. El ejemplo se entrega offline y no se habilita por leerlo. El nuevo argumento `--retrieval-root` permite señalar un índice CPU ya construido de identidad vigente, en vez de reconstruir silenciosamente el histórico.

```powershell
.venv/Scripts/python.exe -m oralia.documentary --package v2 --retrieval --retrieval-root <indice-cpu-vigente> --study-lab --test-provider --web-policy <copia-politica-nueva.json> --web-root docs/audits/2026-10-30-web-fallback-runtime/web-dist --port 8041 --no-browser
```

El CLI habitual sirve `apps/web/dist`; `--web-root` permite visualizar el build aislado de esta entrega sin sustituirlo. No se ha iniciado ese servidor ni se acredita navegador real en esta entrega. `--test-provider` es FIXTURE CPU sin contenido académico; no elegir `--real-provider` bajo la instrucción CPU vigente.

Guion en Materiales: entrar como docente → abrir inspección temporal → realizar un turno local fixture y confirmar su visualización → seleccionar concepto configurado → dejar constancia explícita de alcance/insuficiencia → leer aviso de Internet → consultar fuentes públicas para inspección → abrir enlace/texto inerte → continuar localmente o cancelar/cerrar. Un fallo no reenvía automáticamente la solicitud. Editar/retirar el archivo de política revoca el binding, bloquea nuevas peticiones y la siguiente comprobación de estado oculta el contenido externo en UI. El reloj/presupuesto web no se renueva por reentrada.

Para pruebas sin red: `.venv/Scripts/python.exe -m pytest tests/unit/test_web_evidence.py tests/unit/test_study_lab.py -q` y `node --test tests/unit/test_study_runtime_ui.mjs`. Los comandos de build usan `node node_modules/typescript/bin/tsc -b`, `node node_modules/vite/bin/vite.js build --outDir <carpeta-nueva>` y `node node_modules/eslint/bin/eslint.js .` desde `apps/web`.

| Tarea | Estado real |
|---|---|
| T114 | Completa: política, minimización, presupuesto, recibos y offline por defecto |
| T115 | Completa: adquisición pública acotada, revocable/cancelable, extracción y prueba real |
| T116 | Parcial: contratos y catálogo ampliado; sin evaluadores semánticos acreditados |
| T117 | Parcial: inspección atribuida integrada; sin explicación externa automática validada |
| T118 | Parcial: negativos CPU/adquisición real completos en su alcance; falta medición semántica independiente y conversación real con esa capacidad |

No se cierra Feature012 ni se atribuye aprobación docente o eficacia con estudiantes.
