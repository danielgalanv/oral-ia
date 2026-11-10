# Revisión independiente de la entrega web operativa — 30-10-2026

Se leyeron el informe, tareas, implementación de política/adquisición, contratos de revisión,
API e interfaz. Se repitieron `tests/unit/test_web_evidence.py` y
`tests/unit/test_study_lab.py`: **76 pruebas pasan**, con la advertencia preexistente de
Starlette. No se repitieron las otras 123 regresiones ni las 14 UI en esta auditoría; esos
resultados corresponden a la entrega original. Sin GPU, red real nueva o cambios de producción.

Se verificaron todos los hashes `release_sha256` del informe contra los archivos actuales.
La captura RFC2119 conserva 4723 bytes y su SHA256 coincide. Su estado es
`acquired_unreviewed`, sin contenido aprobado ni entregado al modelo.

## Dictamen acotado

La entrega es coherente como **adquisición/inspección**, no como ampliación autónoma del
autoestudio. T114/T115 tienen implementación y pruebas acordes con ese alcance; no se
detectó en lo revisado una declaración falsa de aprobación semántica. Esta revisión no es
una certificación exhaustiva de seguridad ni del parser HTTP.

Tres límites relevantes para la necesidad humana:

1. `CuratedPublicSearch` consulta un catálogo de URLs por concepto configurado. No descubre
   fuentes nuevas en un buscador general; su cobertura depende del catálogo.
2. La inspección depende de una decisión docente explícita de alcance/insuficiencia; no se
   ha implementado esa decisión autónoma a partir de la pregunta.
3. `review_web` devuelve `unknown` sin evaluadores y mantiene siempre vacías las listas de
   contenido aprobado y evidencia entregada al modelo. Recibir todas las páginas docentes
   en un puerto no equivale a entender o comparar su contenido.

El informe declara correctamente esos límites. Por tanto no procede cerrar T116–T118 ni
prometer que el alumno ya recibe respuestas ampliadas y contrastadas desde Internet.
T151–T153 detallan ese trabajo, sin reemplazar los pendientes originales.

## Próximo resultado útil

Una demostración pequeña de decisión de contenido, antes de otra ampliación de transporte:
complemento externo compatible, contradicción con el curso, formulaciones diferentes pero
compatibles e información cuyo respaldo no se puede establecer. Congelar fuentes y criterios
antes de evaluar; medir decisiones correctas, falsas contradicciones, falsos permisos y
abstenciones, sin usar los oráculos como evaluador de ejecución.

Después debe recorrerse la cadena completa: detectar la carencia local, adquirir fuente,
contrastar, generar solo lo permitido y mostrar la atribución. El primer caso debe producir
una explicación aprovechable; conflicto e incertidumbre deben explicar su límite y permitir
continuar. No se exige un verificador universal, pero sí evidencia empírica suficiente del
mecanismo elegido. Un fixture que hace cumplir el contrato no demuestra ese mecanismo.

La comprobación de navegador de la nueva interfaz también sigue pendiente: la entrega
original acredita SSR, no navegación real. Puede completarse en CPU con proveedor simulado
claramente identificado; no sustituye el hito semántico.
