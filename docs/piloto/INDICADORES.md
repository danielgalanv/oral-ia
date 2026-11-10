# Indicadores y protocolo de la clase piloto (24-11-2026)

Indicadores que la solicitud de la ayuda se comprometió a recoger, y cómo se obtiene cada uno. Todos se presentan agregados en la memoria final, incluidos los negativos. Los datos de participantes viven en `piloto-privado/` (fuera de git, ver `.gitignore`).

| Indicador de la solicitud | Cómo se obtiene | Dónde |
|---|---|---|
| Sesiones completadas y tasa de abandono a mitad de sesión | El profesor anota por participante si terminó (`completada` = `si` o `no`) | `sesiones.csv` |
| Tiempo medio de interacción | Hora de inicio y fin que anota el profesor, o `duracion_minutos` | `sesiones.csv` |
| Preguntas por sesión, aclaraciones, consultas a fuentes, cancelaciones | Copia de sesión que descarga el participante (Finalizar y Descargar JSON) importada con el script; si no la descarga, se deja en blanco | `sesiones.csv` |
| Porcentaje de transcripciones utilizables sin corrección | **No aplica al chat de texto.** Se medirá solo si se integra la voz | — |
| Utilidad percibida por el estudiantado | Cuestionario de utilidad al cierre | `cuestionarios.csv` |
| Tiempo de revisión docente por sesión frente a la revisión manual | El profesor cronometra la revisión de los avisos y registros de cada sesión (`minutos_revision_docente`) y estima el tiempo manual equivalente | `sesiones.csv` |
| Comparación cualitativa de la calidad de la explicación oral con el grupo de referencia | La hace el profesor con sus propios métodos; ORAL-IA no puntúa ni infiere aprendizaje | Fuera de la herramienta |

## Antes de la clase

1. Preparar los códigos: `python scripts/piloto_registro.py codigos 18`. Crea `piloto-privado/codigos.csv` con un código aleatorio por participante. Rellena a mano el nombre junto a cada código al recoger el consentimiento.
2. Imprimir las hojas de consentimiento (`CONSENTIMIENTO.docx`) y los cuestionarios (`CUESTIONARIO.docx`). Sin consentimiento firmado no se participa.
3. Inicializar los registros: `python scripts/piloto_registro.py iniciar`.
4. Medir dos turnos de 10 con la GPU libre y hacer una prueba general (`docs/CLASE.md`).
5. Vaciar el registro de avisos de pruebas: `python scripts/avisos_docente.py purgar todo`.

## Durante la clase

1. Dividir a los 18 participantes en dos turnos de 9. Dar a cada uno su código en un papel; no se usa el nombre en pantalla ni en los registros.
2. Anotar en `piloto-privado/sesiones.csv`, por participante: código, fecha, turno, hora de inicio y fin, y si terminó.
3. Pedir que, al terminar, pulsen Finalizar y descarguen la sesión en JSON (opcional) y rellenen el cuestionario en papel.

## Después de la clase

1. Importar las copias de sesión descargadas: `python scripts/piloto_registro.py importar P-XXX informe.json`.
2. Pasar los cuestionarios a `piloto-privado/cuestionarios.csv`, uno por fila.
3. Revisar los avisos reales del chat con el profesor y cronometrar la revisión: `python scripts/avisos_docente.py pendientes`.
4. Obtener los indicadores agregados: `python scripts/piloto_registro.py resumen`. El resumen oculta los desgloses con menos de 5 participantes.
5. Al cerrar el piloto: `python scripts/piloto_registro.py anonimizar --confirmar` borra la tabla de códigos y nombres. Después los datos quedan anonimizados de forma irreversible.

## Pendiente de completar por el equipo

- Persona o contacto de protección de datos de la UPM que debe constar en la hoja de consentimiento, si procede. Hoy la hoja incluye el contacto del responsable y la Agencia Española de Protección de Datos.
- Fecha de cierre del piloto y del curso, para fijar el plazo de purga del registro de avisos.
