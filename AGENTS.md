# Trabajo con consumo contenido

- Completar el objetivo solicitado con cambios acotados; evitar mejoras y refactorizaciones ajenas al encargo.
- Consultar primero el código vigente y la especificación pertinente. Leer fragmentos concretos antes que archivos completos.
- Acotar búsquedas por directorio y tipo de archivo. No recorrer por defecto entornos, dependencias, índices, bases de datos, carpetas temporales, copias históricas ni evidencias archivadas; consultarlos si el objetivo lo requiere.
- Limitar la salida de herramientas a errores, resúmenes y fragmentos relevantes; conservar logs extensos en archivos cuando sean necesarios.
- Ejecutar las comprobaciones necesarias para el cambio. Ampliarlas según el alcance y el riesgo; no repetir pruebas satisfactorias sin cambios o dudas que lo justifiquen.
- Usar Spec Kit cuando el trabajo requiera su flujo o el usuario lo pida; resolver directamente correcciones pequeñas que no lo necesiten.
- No usar subagentes salvo petición explícita del usuario o instrucciones aplicables que los requieran.
- Dar actualizaciones y respuestas finales breves, con cambios, validación y limitaciones materiales. Evitar informes adicionales salvo necesidad o petición.
- Al cerrar un objetivo sustancial, actualizar el documento de estado pertinente con decisiones y pendientes para facilitar la continuidad; evitar duplicar documentación.
- Estas pautas no sustituyen los requisitos de calidad, privacidad, evidencia ni validación del proyecto. Señalar los bloqueos y la incertidumbre sin iniciar ciclos indefinidos de reintentos.

## Puntos de entrada

- Estado y siguiente trabajo: `docs/CONTINUAR.md`; primer punto pendiente, compactar revisión.
- Trabajo individual: `CONTRIBUTING.md`; mapa: `docs/ARQUITECTURA.md`.
- Limpieza: `scripts/clean_workspace.py` (vista previa por defecto). Datos, originales y evidencias no son cachés descartables.
