# Validación conversacional sin pantalla — 20-10-2026

Se implementan FR034–037 y SC010 mediante política optativa `guided-screenless/v1`, con el mismo perfil `guided_controlled`. Opciones verbales, fuentes, ayuda/modos, conservación confirmada, cierre, revisión propia y eliminación funcionan por texto/transcripción. El código anterior y las actividades usadas conservan su comportamiento. No se habilita un modelo generativo ni audio real.

| Comprobación | Resultado medido |
|---|---|
| Global Python (incluye diez Python e2e) | 1166 aprobadas, 911 omitidas, un aviso de deprecación; 307,24 s |
| Playwright completo, navegador y API reales | 25/25; 3,1 minutos informados por Playwright |
| 24 diálogos originales con política optativa | 24/24, 197 pasos originales; 55,44 s; no son reserva nueva |
| Cuatro recorridos reservados nuevos | 4/4 en primera ejecución, 14 pasos cada uno; pytest21/4 omitidos incluye17 pruebas de núcleo; 40,04 s |
| Cuatro recorridos de desarrollo actuales | 4/4, 14 pasos cada uno; pytest21/4 omitidos; 50,27 s |
| Black | 121 archivos afectados comprobados |
| Ruff estructural | 10 incidencias heredadas, cero nuevas; Counter por ruta/código/mensaje con multiplicidad |
| Frontend | build y lint pasan; fase Vite575 ms (no tiempo total de compilación) |
| Experimento comparable | 204 celdas, cero errores; replay coincide; protocolo y resultados estructurales iguales a006–009 y anterior010 |
| Preservación | 229 archivos vigilados, cero cambios nuevos; las seis pérdidas anteriores siguen explícitas |

## Comandos

Desde la raíz: `uv run --offline --no-sync pytest -q`; `pnpm.cmd --dir apps/web run test:e2e`; `pnpm.cmd --dir apps/web run build`; `pnpm.cmd --dir apps/web run lint`. XML/logs de cada pase en esta carpeta. Black usa la lista de121 rutas afectadas, incluida en python-files.json. Ruff: `uv run --offline --no-sync ruff check src tests scripts --output-format json`, comparado estructuralmente con specs/001-core-cognitive-runtime/t090-ruff-baseline.json.

Para evaluaciones explícitas, definir ORALIA_SCREENLESS_RUN con carpeta **nueva** y ORALIA_SCREENLESS_PARTITION=development o reserved; ejecutar tests/integration/test_screenless_dialogue.py. Los casos reservados ya expuestos no vuelven a ser una reserva nueva. ORALIA_SCREENLESS_AUDIT activa la auditoría de24 casos existentes en carpeta nueva. Las ejecuciones por defecto omiten estos corpus explícitos; omitido no significa aprobado.

Experimento: `uv run --offline --no-sync python -m oralia.validation run --output specs/010-guided-dialogue/evidence-screenless-comparable-20261020 --repetitions 2 --authorize-synthetic-ablations`; `uv run --offline --no-sync python -m oralia.validation replay --package specs/010-guided-dialogue/evidence-screenless-comparable-20261020`. La salida debe ser nueva. También se conservan el paquete intermedio68 y el de306 celdas (tres repeticiones); no se presentan como comparación204.

## Fallos conservados y alcance de la evidencia

Se conservaron el caso rojo inicial, el fallo de catálogo en desarrollo, el cierre prematuro, el payload de recibo inestable y la primera navegación de desarrollo que confirmaba el tema antes de la orden explícita. La auditoría semántica detectó una sustitución real de tema al recibir «confirmo: salida»; se corrigió y probó antes de la primera reserva. Después de esa reserva solo cambió el oráculo de auditoría24: permitía erróneamente exigir una pregunta protegida ya usada. Ahora acepta un límite explícito seguro y rechaza unidades de otro tema. Producción y corpus reservado no cambiaron; screenless-reserve-integrity.json y ambas fuentes archivadas lo verifican. La primera auditoría con ese oráculo defectuoso queda conservada (23/24), seguida de24/24.

El primer global completo reveló nueve fixtures T090/T150 con destinatarios ficticios no declarados (1154 pasan/9 fallan). Se declararon antes del primer uso, manteniendo pruebas negativas de salida bloqueada e inmutabilidad; no se modificaron los controles de producción. El global1139 anterior excluía los diez Python e2e; no era equivalente a la colección completa actual. Los fallos, reintentos y resultados anteriores se mantienen.

No se midió una mejora de rendimiento. Los tiempos dependen de concurrencia de verificaciones; no son evidencia de carga fría ni de desconexión física. Los paquetes experimentales son sintéticos y no aprueban calidad conversacional, voz ni utilidad humana.

## Entrega y límites

Tabla completa en ../task-evidence.md:76/83 completadas. Matriz actual en ../screenless-matrix-current.md y24 transcripciones en ../human-system-review-screenless-current.md, organizadas en seis bloques nuevos. Revisión humana **No evaluado** en todos los casos. G4-audio-gate.md documenta STT/TTS, interrupciones/silencios y audio efímero todavía pendientes; no se descargaron modelos.

Las bases habituales y fixtures conservan sus SHA; demo preparada y detenida, sin Reset ni commits. G0/G1 no se cierran: T061 conserva pérdida histórica no restaurada y T067 exige revisión humana explícita. No se atribuye esa aprobación a una orden de continuar. Véase ../analysis-convergence-screenless-current.md.
