# Analyze y converge — corrección didáctica D01,20-10-2026

Estado: **no converged**;83/90tareas completadas. Se comprueban41FR,11SC,30escenarios,12decisiones A–L,11principios y52elementos de checklist completos. Analyze no detecta contradicciones críticas entre artefactos de intención. Esa conclusión no elimina la contradicción de preservación ya registrada contra la constitución.

| Hallazgo vigente | Tipo | Severidad | Fuente | Evidencia y trabajo pendiente |
|---|---|---|---|---|
| T061 | contradicts | CRITICAL | FR027/028/032; Constitución VIII/X | Seis archivos históricos siguen distintos del baseline inicial; sin copia recuperable/restauración o excepción aprobada. La propuesta de disposición no equivale a aceptación. |
| T067 | partial | HIGH | plan G1; FR016/030/041; SC011 | D01 anterior tiene revisión humana negativa: requiere corrección. Sucesor completo corregido listo, pero revisión humana pendiente; otros23 no aprobados. |

T053/T054/T055/T056/T065 dependen de esas puertas y permanecen abiertos. La comparación pareada previa se conserva como evidencia de su versión, sin atribuir superioridad al contenido didáctico nuevo. No se detecta una brecha nueva de construcción en la ampliación revisada y no se duplican tareas que ya cubren el trabajo pendiente. No se declara cierre ni converged por acumular tests.

## Trazabilidad de las correcciones

FR038/T085: política sucesora optativa y plantillas aditivas de saludo/orientación. FR039/T086: propósito por cláusula, predicado/objeto/contexto; nombre frente a proceso, causa, condiciones y posibilidad; negaciones/coordinación y foco frente a complemento. FR040/T086–088: variantes publicadas del mismo propósito, alternativa ante duda, ejemplo posterior a contestación directa; literalidad íntegra; límite sin mecanismo autorizado. FR041/SC011/T084/T088–090: oráculos separados de autorización, dos dominios, corpus congelados/fallos conservados y D01 completo con matriz de criterios humanos.

La selección genérica excluye variantes de propósito salvo repetición, que necesita todas las referencias aprobadas. Los subobjetivos conservan cobertura completa y los tipos de unidad existentes; no hay DDL nuevo ni agente nuevo. Publicación valida permisos completos del sucesor. Cada unidad vuelve a validar curso/tema/actividad/fuentes y el renderer/verificadores/T090 deciden publicación; defensa/práctica protegida no revelan mecanismos study_only. La preparación usa API docente de pruebas explícita y datos ficticios; el contenido nuevo es propuesta de IA, no revisión didáctica humana.

La revisión pasada D01 ya no se trata como No evaluado: didactic-human-review-status.json registra requires_correction en el predecessor y pending en el sucesor. Las otras23 conversaciones no reciben aprobación por esta corrección. El plan G1 exige literalmente: «Revisar transcriptos sintéticos de forma humana con rúbrica de sistema». No se inventa una aprobación automática para sustituir ese requisito.

## Evidencia final y preservación

- didactic-validation/report.md/summary.json:1185Python/931omitidas,27Playwright, build/lint, Black123, Ruff10heredadas/0nuevas con multiplicidad frente al baseline durable.
-20recorridos didácticos/68pasos:16expuestos pasan y última reserva4/4 (13pasos) pasa en primera ejecución. Primeras reservas3/4 y3/4 se conservan; tercer ciclo4/4 se conserva con la regresión posterior que motivó la última versión. No se renombran casos expuestos como reserva nueva.
-24diálogos/197pasos originales reproducidos actualmente, auditoría expuesta. D01-corrected-for-human-review.md contiene siete pasos completos y evidencia por seis observaciones humanas. human-review-didactic-blocks organiza24sucesores en seis bloques.
-source-didactic-cycle4-prereserve-20261020.json/zip congela582archivos antes de la última reserva; permanecen idénticos durante la validación final. Las redacciones/códigos/resultados intermedios quedan conservados. Un global intermedio rechazó correctamente un cambio concurrente de manifiesto; el global final pasó con fuente estable.
-evidence-didactic-verified-20261020:204celdas/0errores y replay coincide. didactic-experiment-comparison.json verifica protocolo/resultados estructurales iguales a006–009 y anteriores010; no demuestra suficiencia didáctica ni voz/utilidad.
-didactic-preservation-current.json:229históricos vigilados/0cambios nuevos,223coinciden con baseline inicial y6pérdidas anteriores siguen explícitas. SHA de oralia.db/demo.db/fixtures.json intactos. Puertos propios8026/5196/8005/8015/5175 comprobados libres; demo preparada y detenida, sin Reset ni commits.

## Límites

Reconocimiento/repertorio didáctico finitos; no se afirma comprensión general ni calidad para cualquier formulación. Los tests de pertinencia pueden fallar aunque pase publicación, pero no son revisión humana independiente. G2 generativo no se habilita, G3 utilidad y G4audio real siguen pendientes. La corrección textual no prueba STT/TTS, silencios/interrupciones ni audio efímero. No se integra ningún paquete docente de otra auditoría sin revisar fuentes y publicar una sucesora.

El pase de analyze/converge fue de solo lectura sobre spec/plan/tasks, con hashes comprobados antes/después. Este informe se registra después en la fase de implementación/evidencia; no modifica intención ni crea excepciones constitucionales.
