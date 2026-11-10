# Incidentes CPU conservados; cero inferencias adicionales

1. El primer prepare.py no podía importar el fixture tests por la ruta de
   importación de un script independiente. Se conservó prepare-first.py y se
   añadió la raíz del workspace al sys.path local. prepare-cpu.log conserva la
   reproducción correcta. Ocurrió antes de cargar el worker.
2. Tras cerrar la GPU, el primer intento de crear una página de lectura mediante
   Python -c falló por comillas del shell: SyntaxError de cadena sin cerrar y
   PowerShell no reconoció el texto estático style-src. No se creó la página,
   no se ejecutó contenido académico ni hubo llamada/carga/calentamiento. Se
   sustituyó por un archivo Python literal build_answer_page.py, ejecutado en
   CPU. No se cambió el texto canónico de la respuesta ni el reloj/cupo.

Ambos incidentes están separados de la comparación académica y no se atribuyen
a un modelo o estrategia. Los intentos anteriores y relojes históricos no se
reescriben. El reloj del primerpreflight de esta continuación sigue siendo el
único plazo de30min, incluida la construcción de la entrega.
