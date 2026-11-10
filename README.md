> **Copia pública del proyecto ORAL-IA.** Contiene el código, las pruebas, las especificaciones y los informes de ensayo en Markdown. No incluye el material docente ni los textos de documentos de terceros usados en el piloto, ni datos personales; consulta `materiales/README.md`. Sin ese material el asistente no tiene qué consultar y algunas pruebas que lo necesitan no pasarán. No hay todavía licencia de uso asignada: todos los derechos reservados hasta que se indique otra cosa.

# ORALIA

Asistente local para estudiar con documentación docente y recoger evidencias de una conversación. **No califica, no aplica rúbricas ni sustituye al profesor.** El objetivo actual es un piloto pequeño de autoestudio por chat sobre requisitos de Ingeniería del Software; el examen oral de preguntas fijadas por el profesor y la voz son fases posteriores.

## Empezar

- **Trabajar con el código:** [CONTRIBUTING.md](CONTRIBUTING.md): instalación, estructura, pruebas, GPU y limpieza.
- **Continuar el desarrollo:** [estado y plan vigente](docs/CONTINUAR.md). Primer punto: compactar la revisión.
- **Usar el piloto actual:** [docs/ESTUDIO.md](docs/ESTUDIO.md).
- **Entender los componentes:** [mapa de arquitectura](docs/ARQUITECTURA.md).

```powershell
uv sync --frozen --extra dev
pnpm.cmd --dir apps/web install --frozen-lockfile
.\scripts\study-chat.ps1 -PrepareOnly -Offline -NoBrowser
```

La preparación usa embeddings locales CPU y necesita sus archivos ya disponibles. No descarga modelos ni arranca el generador. El arranque real requiere un entorno CUDA separado y GPU libre: ver la guía de contribución antes de ejecutarlo.

## Estado que no debe confundirse

- El piloto usa `study-dialogue/v4`, `web-review/v8` y alcance `web-control/v5`. La política de actividad habilita ampliación web restringida; `-Offline` la desactiva. El runtime genérico no da permiso web por defecto.
- Hay ensayos reales y fallos documentados. **No está acreditada la fiabilidad general ni abierta la aceptación del piloto con estudiantes.**
- El catálogo persistente se crea al preparar materiales. Su uso por el revisor conceptual es experimental: el caso largo tardó 396 s frente a 151 s con planificación en turno. No se promovió ese revisor al chat estable.
- Materiales originales, cuarentena, bases de datos y evidencias se conservan. Caché no significa evidencia descartable.

La [constitución](.specify/memory/constitution.md), [Feature012](specs/012-conversational-course-study/spec.md) y su [índice de tareas](specs/012-conversational-course-study/tasks.md) rigen el desarrollo. Las instrucciones de seis features del [MVP anterior](docs/MVP.md) y la [demo anterior](docs/DEMO.md) describen demostradores distintos, no el estado actual de todo el proyecto.
