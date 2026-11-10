# Correcciones didácticas de D01 — validación20-10-2026

La revisión humana anterior de D01 **requiere corrección**. Se conserva ese resultado; el sucesor espera revisión humana, y los otros23 casos no se consideran aprobados. Se implementan FR038–041/SC011 con política optativa `guided-screenless/v2`, materiales ficticios sucesores y el mismo perfil `guided_controlled`. No se cambia arquitectura, agentes, autenticación, T090/T150, consentimiento o recursos personales.

D01 ahora saluda; reconoce la consulta amplia; contesta Sí y explica evaporación/ebullición antes de los ejemplos; resuelve dímelo con el contexto; cambia estrategia al reiterarse la duda; explica cómo pasa a vapor en pasos. D02 explica condensación paso a paso y cambia explicación ante la duda. El programa ficticio permite contrastar proceso, causa, definición y aceptación sin generalizar sus reglas a todos los programas.

[**D01 completo, siete pasos, listo para revisión humana**](../D01-corrected-for-human-review.md). [Matriz24](../didactic-matrix-current.md), [transcripciones sucesoras24](../human-system-review-didactic-current.md) y [seis bloques](../human-review-didactic-blocks/README.md).

| Comprobación | Resultado medido |
|---|---|
| Global Python completo |1185 aprobadas,931 omitidas,1 aviso de deprecación;265,43s |
| Playwright completo |27/27;3,3min informados por Playwright. Incluye D01 íntegro y proceso de programa sin paneles visuales |
| Diálogos originales actuales |24/24,197 pasos originales;58,87s. Auditoría expuesta, no reserva nueva ni aprobación didáctica global |
| Núcleo y regresiones expuestas |19 pruebas de núcleo y16 recorridos expuestos pasan:35 aprobadas/4 omitidas;44,70s |
| Última reserva nueva |4/4 en primera ejecución,13 pasos;pytest23aprobadas incluye19núcleo,16omitidas;25,69s |
| Corpus didáctico vigente total |20 recorridos,68 pasos:16 expuestos+4reservados nuevos. No confundir con24 diálogos originales |
| Reservas anteriores en su primera ejecución |ciclo1:3/4; ciclo2:3/4; ciclo3:4/4. Se conservan fallos y versiones; no se sustituyen por pases posteriores |
| Black y Ruff |123 archivos Python comprobados;10 incidencias Ruff heredadas,0 nuevas frente a baseline durable de49, por Counter(ruta,código,mensaje) con multiplicidad |
| Frontend |build/lint pasan;506ms fase Vite, no tiempo total ni medida de mejora |
| Experimento comparable |204 celdas,0 errores y replay coincide; protocolo/resultados estructurales iguales a006–009 y anteriores010 |
| Preservación |582 archivos de fuente congelada sin cambios durante la validación final;229históricos vigilados sin cambios nuevos; bases habituales/fixtures SHA intactos |

## Comandos y fuentes

Desde la raíz: `uv run --offline --no-sync pytest -q`; `pnpm.cmd --dir apps/web run test:e2e`; `pnpm.cmd --dir apps/web run build`; `pnpm.cmd --dir apps/web run lint`. Resultados finales: feature010-didactic-verified-global.xml/log y feature010-didactic-verified-browser.log. Black usa python-files.json (123rutas); Ruff JSON/comparación también en esta carpeta, contra specs/001-core-cognitive-runtime/t090-ruff-baseline.json.

Corpus explícitos: ORALIA_DIDACTIC_RUN debe ser una carpeta nueva, ORALIA_DIDACTIC_PARTITION selecciona development, reserved, reserved_cycle_2, reserved_cycle_3 o reserved_cycle_4. `exposed` ejecuta únicamente desarrollo y los tres ciclos ya expuestos, excluyendo el cuarto reservado. Ejecutar `uv run --offline --no-sync pytest tests/integration/test_didactic_quality.py -q`. No dejar flags explícitos activos al ejecutar la suite global; los omitidos no se cuentan como aprobados. Los casos ya ejecutados no vuelven a ser una reserva nueva.

Auditoría actual: ORALIA_SCREENLESS_AUDIT=specs/010-guided-dialogue/didactic-runs/original-24-verified y ORALIA_DIDACTIC_AUDIT=1; ejecutar tests/integration/test_screenless_original_audit.py con pytest. Las carpetas usadas deben conservarse; para repetir, elegir una carpeta nueva. El resultado publicado usó API, renderer y verificadores reales sobre datos ficticios, sin sustituir salidas.

Experimento final: `uv run --offline --no-sync python -m oralia.validation run --output specs/010-guided-dialogue/evidence-didactic-verified-20261020 --repetitions 2 --authorize-synthetic-ablations`; después `uv run --offline --no-sync python -m oralia.validation replay --package specs/010-guided-dialogue/evidence-didactic-verified-20261020`. La salida tiene que ser nueva. Los paquetes anteriores/intermedios permanecen; sus manifiestos no se alteran para aparentar coincidencia.

Fuente de entrega: source-didactic-cycle4-prereserve-20261020.json/zip. didactic-preservation-current.json verifica integridad; didactic-modified-files.json contiene19rutas de código/materiales/tests nuevas o modificadas frente al pase anterior sin pantalla. Spec/plan/tasks/checklists, contratos y guías se actualizan dentro de010; no se crea una feature duplicada.

## Fallos preservados y correcciones

El primer oráculo usaba indebidamente blocked en el esquema de autoestudio; se corrigió el test y se conservaron sus fallos. Las pruebas posteriores separan requisitos de pertinencia/pasos/tema/literalidad de la autorización. El control de compatibilidadv1 demuestra que el material anterior publicado sigue limitado y no satisface un proceso paso a paso.

Ciclo1 PH04 confundía comprobación con el complemento almacenamiento: se corrige el foco de cláusula/predicado y se conservan negaciones/preguntas compuestas. Ciclo2 PJ03 revela una definición compatible bloqueada por el verificador léxico. Se redactan cláusulas docentes afirmativas equivalentes y se comprueba por pares la compatibilidad de variantes del mismo tema; no se relaja el agente. Ciclo3 pasa4/4, pero la regresión expuesta detecta una definición reiterada sin alternativa publicada; se añade una variante. También se separan variantes de propósito de la selección genérica por UUID; el primer filtro rompió repeticiones y produjo9fallos, conservados. El filtro corregido mantiene íntegra la salida al repetir y la selección genérica usa la lección base. Después pasan16regresiones expuestas y el cuarto ciclo nuevo4/4 sin cambios posteriores de fuente.

Se conservan dos globales intermedios:1179/919omitidas sobre una versión anterior y1183aprobadas/1fallo/927omitidas. El fallo del segundo es code/protocol integrity mismatch porque una edición coincidió con creación/replay del paquete en el test CLI. No se suprime esa protección. El global final se ejecutó sin editar código/tests/materiales y aprobó1185/931omitidas. Los tiempos entre pases no demuestran rendimiento superior ni carga fría.

## Límites y estado

Reconocimiento y repertorio didáctico acotados a propósitos, relaciones y materiales publicados; no se demuestra comprensión general del lenguaje natural ni suficiencia para cualquier formulación/asignatura. Las nuevas unidades son propuestas docentes sintéticas de IA publicadas explícitamente en el entorno de pruebas; requieren revisión humana de contenido y didáctica. Los oráculos son independientes de publicación, pero no equivalen a validación humana independiente. La comparación pareada previa corresponde a una versión anterior: no se afirma superioridad del nuevo contenido.

Perfil guiado controlado, no generativo G2 aprobado. Audio real STT/TTS, silencios/interrupciones y utilidad G3 siguen pendientes; ver G4-audio-gate.md. No hay descargas de modelos, compromisos de rendimiento, Reset ni commits. La demo preparada y los datos habituales se conservan; se entrega detenida. Persisten seis pérdidas históricas anteriores, sin restauración o excepción otorgada. T061/T067 y sus dependencias impiden el cierre de la feature:83/90tareas completadas.
