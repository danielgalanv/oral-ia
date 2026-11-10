# Verificación final de presentación

La primera comprobación de texto visible HTML comparaba espacios añadidos por
el parser al separar nodos strong de signos de puntuación. Falló esa aserción
de presentación, no una comparación de texto canónico: JSON y Markdown ya
conservaban exactamente las diez salidas. Se conserva seal-first.py.

Se corrigió el check para ignorar únicamente whitespace de layout al comparar
el contenido de cada bloque renderizado; no elimina letras, palabras, signos
o condiciones. Los checks canónicos siguen exigiendo las salidas completas
exactas en Markdown y sus finish_reason=stop. Sin inferencia, carga o cupo
adicional; mismo reloj original.
