> Operación vigente: [ESTUDIO](ESTUDIO.md). Estado, límites recientes y plan: [CONTINUAR](CONTINUAR.md). La revisión conceptual experimental no está promovida.

# Piloto de autoestudio de requisitos — chat

Desde `D:\Proyecto personal\ORALIA`:

```powershell
.\scripts\study-chat.ps1
```

El lanzador prepara recursos aislados y carga el generador Qwen2.5-14B y el revisor Qwen3-8B. Requiere GPU disponible; el script no detiene aplicaciones ajenas. Abre la interfaz cuando el servicio está listo. Pulsa **Comenzar**. **Ctrl+C** cierra los servicios propios.

Este lanzador corresponde al piloto de **requisitos de ingeniería del software**. Selecciona la política de esa actividad autorizada por el usuario en `config/requirements-study-policy.json`: alcance explícito y fuentes públicas acotadas de NASA/Sommerville. El runtime genérico no habilita Internet para otras actividades. Antes de una consulta externa aparece un aviso; sus URLs se separan de las fuentes docentes.

Para la misma actividad sin Internet:

```powershell
.\scripts\study-chat.ps1 -Offline
```

También puede indicarse una política explícita con `-ActivityPolicy`. Desactivar Internet no elimina el alcance docente. Una política que no declare `activity_scope` no sirve para este recorrido. Las políticas antiguas se conservan para reproducir sus ensayos, sin reinterpretarlas.

## Recorrido

1. Recuperación de pasajes locales comprobados y resolución del referente a partir del historial mostrado.
2. Control separado del alcance de la actividad. Una duda ajena recibe un aviso operativo; una intención incierta pide precisar. No se completa una respuesta ajena usando conocimientos generales.
3. Generación de una explicación a partir de los pasajes y revisión del borrador real. Los ejemplos y sus cifras pueden ser hipotéticos y coherentes.
4. Si la revisión indica insuficiencia, se puede intentar una ampliación web una vez, con permisos, respaldo y contraste docente. Con recuperación vacía se usa la ruta web completa. La incertidumbre no se transforma en aprobación.
5. Solo el texto confirmado como mostrado entra al historial. Las correcciones y los intentos no mostrados se conservan en las trazas de ensayo, no como respuestas del alumno.

El control terminológico añadido detecta una confusión concreta y documentada entre `Completeness` y «Complejidad», con testigo literal en las fuentes. Solicita reparación al modelo y nueva revisión; no reemplaza palabras silenciosamente ni es un verificador semántico general.

## Qué se ha comprobado

Doce preguntas aprobadas en tres conversaciones completas con modelos reales y navegador; la B4 mostró la confusión terminológica y se corrigió después en otro ensayo automático. También se comprobaron dos avisos fuera del tema sin generación académica y dos ampliaciones web completas, de unos 339 segundos cada una. Se mantuvieron 180 s/etapa y 600 s/turno.

El banco es conocido: es una regresión y no demuestra utilidad con estudiantes ni fiabilidad universal. El revisor local ha dejado pasar errores; la inspección docente sigue siendo necesaria para decidir el siguiente ensayo real. No se evalúa al alumno, no hay rúbrica y no se ha validado voz. La entrega a participantes continúa cerrada.

Las respuestas completas, las versiones incorrectas, las correcciones y los límites están en [el informe de la implementación](audits/2026-11-03-study-controls-v3/resume-20261104/report.md).


## Palabras clave (04-11-2026)

Toda respuesta académica del piloto normal termina con Palabras clave. Su presencia se comprueba sin inventar términos; si falta se pide completarla y se revisa otra vez. No se bloquea por comas, repeticiones o una lista más larga de lo sugerido. La lista no acredita la explicación. La revisión conceptual nueva permanece experimental; el piloto conserva su revisor anterior. [Cuatro preguntas, comparación y límites](audits/2026-11-04-concept-keywords/report.md).
