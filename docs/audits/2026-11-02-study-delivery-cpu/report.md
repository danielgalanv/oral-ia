# Entrega por HTTP y navegador — validación CPU

La entrega corregida de T186 se ha comprobado por HTTP y en un navegador real. **Tres pruebas HTTP pasan y el recorrido de navegador termina completo. No se cargaron modelos ni se usó GPU para inferencia o aceleración del navegador.** No se modificó producción en este incremento.

- [Resultado completo del navegador](browser-1793616983700/result.json).
- [Captura de la conversación visible](browser-1793616983700/visible-conversation.png).
- [Pruebas HTTP](http.log).
- [Preservación, Ruff y limpieza](final-checks.json).

## Qué se comprobó

Las pruebas HTTP ejercitan las rutas reales de consulta documental e inspección, consentimiento y entrega. Usan bytes del paquete docente real, recuperación determinista de prueba y un proveedor fixture explícito. Verifican texto visible frente a bruto, confirmación única, rechazo del envío duplicado, historial del siguiente turno con exactamente lo mostrado, cierre/reentrada con cuota conservada y sin historial anterior. Una envoltura ambigua o una generación truncada queda fuera del historial; sus recibos conservan el bruto y una pregunta posterior puede continuar.

La prueba de navegador utilizó el frontend compilado en un directorio nuevo del dossier, el servidor HTTP real en 127.0.0.1:8047 y Chromium headless con --disable-gpu y --disable-software-rasterizer. No se interceptaron ni inventaron respuestas HTTP. El proveedor, etiquetado FIXTURE_CPU_REPLAY_NOT_NEW_GENERATION, reprodujo el B3 conservado y respuestas de control deliberadamente identificadas como fixtures.

Se verificó que el cuerpo completo de B3 aparece como texto normal, sin su envoltura JSON, mientras que el detalle técnico conserva el bruto exacto. La siguiente petición recibe el cuerpo realmente mostrado. Una envoltura con campos adicionales no se muestra ni se confirma; la conversación continúa sin incorporarla. La cancelación interrumpe la petición pendiente y permite cerrar y reabrir, manteniendo cinco llamadas de prueba consumidas y descartando el historial. La siguiente pregunta funciona con historial vacío. El navegador no registró errores JavaScript ni peticiones externas. Cerró su contexto y proceso propios.

Las fuentes y su contenido usan también elementos article dentro de las respuestas. Los contadores finales del test se limitan a las respuestas directas de la región diagnóstica; no confunden esos pasajes con turnos nuevos.

## Intentos conservados

El primer arranque del servidor se detuvo antes de abrir el puerto porque faltaba la raíz de tests en PYTHONPATH. Se corrigió la invocación, no la aplicación.

Se conservan tres intentos fallidos del arnés de navegador. El primero seleccionaba dos bloques pre al buscar el bruto: fuente y recibo técnico. El segundo contaba artículos globales. El tercero confirmó que, incluso dentro de la región de inspección, las fuentes contienen artículos anidados; fue necesario seleccionar hijos directos. Mi primera atribución a paneles externos era incorrecta y quedó rectificada en browser-third-failure.json. Los scripts ejecutados, capturas y resultados de cada intento están preservados; no se cuentan como fallos académicos o de la aplicación.

El cuarto intento, browser-1793616983700, completó todos los controles sobre un servidor con cuota e historial nuevos. No se borró ni reinició ningún dato de demo o habitual. Cada servidor de ensayo tuvo salida separada y parada propia.

## Alcance y preservación

Esto valida transporte, presentación y ciclo de sesión. No aporta nuevas respuestas de un LLM ni una medida de calidad semántica o aprendizaje. La recuperación de este ensayo es un doble determinista sobre documentos reales: no acredita el ranking RAG. La generación GPU anterior de T186 permanece separada e intacta.

Los 258 archivos de producción congelados al finalizar T186 conservan sus hashes. Los grupos históricos de 308, 140 y 22 archivos siguen iguales. La compilación Vite termina correctamente en web-dist de este dossier; no se reemplazó el build habitual. Black y Ruff focales pasan. Ruff global mantiene diez diagnósticos anteriores y cero nuevos comparados con multiplicidad.

Los cuatro servidores de prueba cerraron de forma normal y el puerto 8047 quedó libre. No se detuvieron servicios ajenos. No hubo modelos, CUDA, búsqueda web, migraciones, Reset ni commits.

T187 queda completada como validación CPU. Feature 012 y las revisiones sustantivas previas continúan con sus estados existentes.

## Reproducción

Las pruebas HTTP se ejecutan con pytest sobre tests/integration/test_study_presentation_delivery.py, usando una basetemp nueva dentro de .claude-scratch.

Para el navegador: compilar Vite a una carpeta aislada web-dist de este dossier; iniciar serve.py con PYTHONPATH=src;. y CUDA_VISIBLE_DEVICES vacío, puerto 8047 libre y un --output nuevo. Ejecutar browser.cjs con SERVER_RECORDS_DIR igual al nombre de esa salida. El proveedor no carga modelos. Detener solo ese servidor creando stop-request dentro de su salida; también tiene un límite automático de 240 segundos. Cada invocación del navegador crea una carpeta nueva y conserva su script ejecutado.
