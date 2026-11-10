# Incidencia de preservación: estado y decisión pendiente

Se sobrescribieron seis salidas de navegador de Feature009 durante una regresión con
rutas fijas. No se conservó una copia recuperable de los originales. La corrección del
test usa salidas por ejecución y las regresiones posteriores verifican cero cambios nuevos.
Eso evita repetir la incidencia; no recupera los bytes perdidos.

La búsqueda independiente examinó 41.595 archivos, 2.112 candidatos PNG/JSON por
contenido, 37 comprimidos y 2.990 miembros, sin coincidencias SHA256. Informe completo
y límites en workspace-originals-search-2026-10-19.json. Las búsquedas anteriores de
ZIP/tar y rollouts tampoco hallaron originales. No hay una fuente de restauración
identificada y no se solicita al usuario que aporte una ruta de backup que desconoce.

Alcance exacto y hashes: incident.json. Las nuevas versiones sobrescritas se conservaron
en current-overwritten-outputs. Los cuatro paquetes experimentales 006–009 y sus 16
archivos siguen intactos; el archivo04 también. El código actual reproduce 204 celdas
en un paquete nuevo. Las bases habitual y demo no se alteraron.

No debe declararse T061 restaurada ni editar hashes para fingir coincidencia. La
validación técnica y el resto del trabajo independiente se han realizado y documentado.
El estado restante es una pérdida de evidencia histórica sin recuperación acreditada,
no un simple retraso esperando un archivo desconocido.

Para resolver el cierre, el propietario debe decidir explícitamente el tratamiento
de esta pérdida y, si corresponde, la excepción de alcance documental que admite.
Esa decisión no recupera los archivos ni autoriza afirmar que fueron preservados.
La ausencia de backup y una instrucción genérica de continuar no equivalen a aceptar
la pérdida. Mientras no exista esa decisión, la brecha de preservación sigue abierta.
La revisión humana de los 24 diálogos (T067) es una obligación independiente.


Revalidación actual, separada de la restauración: preservation-incident/revalidation-20261019-162715/report.md,
**3/3 Playwright aprobados (1,4 min)** para carga normal/lenta/error del archivo04.
Normal201/processed en10.584 ms; lento201/processed en19.155 ms (16.000 ms artificiales,
endpoint3.094 ms); error422 en49 ms. Una petición por caso. Guard229 archivos/0 cambios.
Se verificó el manifiesto SHA nuevo sin discrepancias. Evidencias nuevas agrupadas en evidence/;
no sobrescriben el histórico ni recuperan sus bytes. No prueban G1, voz o utilidad humana.
T061 no se marca restaurada y la revisión humana de sistema sigue independiente.


## Propuesta concreta para decisión del propietario (no aprobada)

Registrar los seis archivos como pérdida histórica no recuperada, conservar sus SHA originales y todos los informes de búsqueda, mantener las salidas nuevas identificadas como revalidación y conservar los cuatro paquetes experimentales originales. Mantener T061 **no restaurada**; no cambiar el criterio ni los hashes para convertir revalidación en preservación.

Decisión propuesta a contestar expresamente: «Acepto registrar esta incidencia como pérdida histórica no recuperada y conservar la revalidación nueva como evidencia sustituta identificada. Solicito evaluar el cierre documental con esta no conformidad explícita; no autorizo afirmar restauración ni preservación de los seis originales». También puede rechazarse y mantenerse el cierre bloqueado. Aún no existe respuesta a esta propuesta.

La aceptación registra el tratamiento de la incidencia; no elimina automáticamente una obligación constitucional. Cualquier excepción normativa necesaria para el cierre debe proponerse y ratificarse por el procedimiento de gobernanza correspondiente; ni esta propuesta ni una instrucción genérica de continuar enmiendan la constitución. La revisión T067 permanece independiente.
