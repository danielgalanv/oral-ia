# Resultado de la verificación del paquete docente

18 de octubre de2026. Feature009 corregida y verificada,sin commits ni Reset de demo.

## Corrección comprobada

Recortes largos: perfil canónico material-excerpt/v1 reconstruido desde material DB
vigente y autorizado,con hash/rango/traza y plantilla exacta; T090 no acepta texto libre.
El archivo04 se extrae por líneas: su bloqueo concreto también provenía de mezclar
«No contiene datos de personas» con otras oraciones. Coherencia ahora compara por
oración,sin quitar verificador ni eximir contradicciones explícitas entre fuentes.
Área técnica ya permite activar documentos processed, como admite el backend.

Archivo04 íntegro, SHA256
8d9f065a557f2bd274dbe579f19cad4c1523fc3969e04802986a9e76002eeca9. No fue acortado ni
sustituido para pasar. Además se probó un bloque>400 por HTTP real para aislar recorte.
El informe previo está archivado en009/teacher-result-before.md.

## Evidencia medida

| Prueba | Resultado |
|---|---|
| HTTP3materiales×2modos×4scopes | 24passed,16.12s;04original incluido |
| Matriz/coherencia/HTTP dirigidos | 62passed,17.28s |
| Suite determinista final | 921 passed, 3 deselected, 1 warning in 113.30s (0:01:53) |
| Playwright completo | 12passed(1.3m);04cargado por navegador5.7s |
| check-demo.ps1 | 3checks aprobados,67.4s |
| Build/lint/Black/Ruff | correctos,0nuevas infracciones Ruff |
| Experimento009 | 204celdas reproducidas;originales006–008 intactos |

Scopes [],transcript,summary,ambos;salida válida en ambos modos,segundo turno utilizable
en autoestudio,cierre T150,revisión parcial,JSON/Markdown y eliminación verificable.
Navegador usa login,carga04 real,activación/publicación,consulta100/fuentes,cierre,
revisión/exportaciones/borrado;sin respuestas simuladas.18recursos demo/habituales
sin cambios;demo preparada y detenida.

## Límites e incidencias

Valida estos casos concretos, no todos los documentos ni toda semántica. Archivo03
conflictivo y archivo02/preguntas de extensión no se declaran validados. Generación
determinista;recuperación/embeddings e índice reales en HTTP/browser. Voz real,LLM y
utilidad con personas sin validar. La detección de contradicciones sigue siendo léxica.

Se observaron fallos Chroma en la suite grande y se corrigió el cierre de clientes de
pruebas, limitado a tmp_path propio;33pruebas dirigidas y921globales finales pasan.
También se aisló índice por ejecución E2E. No se cambiaron umbrales/recuperación de
producción ni se garantiza ausencia de fallos nativos. Diagnósticos previos preservados.

[Tabla completa, comandos, archivos y evidencia](../../specs/009-long-extractive-binding/implementation-evidence.md).
[Captura del recorrido largo](../../specs/009-long-extractive-binding/browser-long-material.png).
