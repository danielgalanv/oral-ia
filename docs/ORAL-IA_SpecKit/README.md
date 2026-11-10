# ORAL-IA — paquete de trabajo para GitHub Spec Kit y Claude Code

Este paquete transforma el documento conceptual de ORAL-IA en entradas separadas para las skills de Spec Kit. La separación evita mezclar reglas permanentes, requisitos funcionales, decisiones técnicas, tareas y criterios de validación.

## Estrategia recomendada

No implemente todo el sistema como una única feature. Use una constitución común y seis features acumulativas:

1. **001 — Núcleo cognitivo y ejecución local**
2. **002 — Materiales autorizados y RAG trazable**
3. **003 — Agencia de autoestudio**
4. **004 — Agencia de defensa oral y voz opcional**
5. **005 — Configuración docente, revisión, privacidad y exportación**
6. **006 — Validación arquitectónica y comparación con baseline monolítico**

Cada feature debe quedar integrada, probada y revisada antes de iniciar la siguiente. Las features posteriores pueden depender de las anteriores, pero no deben reescribir sus contratos sin una decisión arquitectónica explícita.

## Preparación

Desde la raíz del repositorio:

```powershell
claude
```

Compruebe que aparecen las skills `/speckit-*` y que el repositorio está limpio antes de iniciar cada feature:

```text
/git status
```

En una terminal externa también puede usar:

```powershell
git status
git add .
git commit -m "Checkpoint before Spec Kit feature"
```

## Primera ejecución: constitución

Ejecute una sola vez:

```text
/speckit-constitution
```

Pegue el contenido de `00_constitution_prompt.md`. Revise el documento generado y confirme que las reglas no se han convertido en decisiones de implementación demasiado concretas.

## Ciclo de trabajo por feature

Para cada archivo de `features/`, en orden:

### 1. Crear la especificación

```text
/speckit-specify
```

Pegue el contenido completo del archivo de la feature.

### 2. Resolver ambigüedades

```text
/speckit-clarify
```

Use `10_clarification_decisions.md` como criterio de respuesta. No responda de forma distinta entre features salvo que quiera modificar deliberadamente el alcance.

### 3. Crear el plan técnico

```text
/speckit-plan
```

Pegue `11_plan_prompt.md`. Añada al final el nombre y número de la feature actual para que el plan se limite a ella.

### 4. Comprobar la calidad de requisitos

```text
/speckit-checklist
```

Pegue el bloque apropiado de `12_checklist_prompts.md`.

### 5. Generar tareas

```text
/speckit-tasks
```

No añada instrucciones salvo que necesite exigir que las tareas se organicen por historia de usuario y puedan validarse de forma independiente.

### 6. Analizar consistencia

```text
/speckit-analyze
```

No implemente mientras existan errores críticos, requisitos sin cobertura o contradicciones entre la constitución, la especificación, el plan y las tareas.

### 7. Implementar

```text
/speckit-implement
```

Puede añadir:

```text
Implementa únicamente la feature actual. Respeta el orden de dependencias de tasks.md. Ejecuta las pruebas tras cada bloque funcional. No amplíes el alcance ni sustituyas contratos ya aprobados sin documentar la desviación.
```

### 8. Cerrar brechas

```text
/speckit-converge
```

Revise las tareas añadidas, vuelva a implementar lo pendiente y repita hasta satisfacer `13_definition_of_done.md`.

## Regla de control de alcance

La implementación mínima debe demostrar la arquitectura, no intentar resolver desde el principio todos los problemas de una arquitectura cognitiva general. Quedan fuera del MVP:

- robots y dispositivos físicos;
- Moodle y sistemas institucionales;
- expedientes y calificaciones oficiales;
- evaluación automática, notas o aplicación autónoma de rúbricas;
- acceso abierto a Internet durante sesiones; la constitución 2.0.0 permite únicamente
  ampliación documental restringida de autoestudio con permiso por actividad, procedencia
  externa visible y contraste con el material docente. Sigue pendiente de implementación;
- creación autónoma de código o agentes;
- memoria académica o psicológica longitudinal;
- herramientas personales como correo o calendario;
- microservicios distribuidos salvo necesidad demostrada.

## Alternativa de una sola especificación

`15_one_shot_specify_prompt.md` permite crear una única feature para todo el MVP. Es útil para una exploración rápida, pero no es la opción recomendada: produce planes y listas de tareas muy extensos, dificulta las pruebas incrementales y aumenta el riesgo de que Claude mezcle investigación arquitectónica con funcionalidades de interfaz.

## Archivos de referencia

- `10_clarification_decisions.md`: decisiones que deben mantenerse estables.
- `11_plan_prompt.md`: arquitectura y pila técnica propuestas.
- `12_checklist_prompts.md`: controles de calidad de requisitos, privacidad y arquitectura.
- `13_definition_of_done.md`: criterio de finalización por feature y para el MVP.
- `14_domain_model.md`: vocabulario y entidades que deben mantenerse consistentes.
- `SOURCE_MAPPING.md`: relación entre el documento original y las features.
