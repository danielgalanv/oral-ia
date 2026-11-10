# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_governance_flow.spec.ts >> local governance: real login, immutable successor, consented review, two exports, deletion and logout
- Location: ..\..\tests\e2e\test_governance_flow.spec.ts:7:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByLabel('Credencial local')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByLabel('Credencial local') with timeout 5000ms
  - waiting for getByLabel('Credencial local')

```

```yaml
- banner:
  - navigation "Navegación general":
    - link "Volver al inicio":
      - /url: /
- main:
  - heading "ORAL-IA — Gobierno docente" [level=1]
  - region "Gestión de sesión activa":
    - heading "Sesión activa" [level=2]
    - button "Comprobar sesión activa"
  - paragraph: Configuración y evidencia del sistema; sin notas ni perfiles de estudiantes.
  - button "Cerrar acceso docente"
  - status: "Eliminación confirmada: contenido no disponible para revisión ni exportación."
  - heading "Nueva configuración" [level=2]
  - group:
    - text: Asignatura
    - combobox "Asignatura":
      - option "Crear asignatura local"
      - option "Curso E2E autoestudio"
      - option "Dominio sintético"
      - option "Dominio sintético"
      - option "Curso ficticio local" [selected]
    - text: Nombre de actividad
    - textbox "Nombre de actividad": Gobierno b9a37c2d-e58c-4f35-90d8-21f8d189418b
    - text: Materia
    - textbox "Materia": Explicación de decisiones
    - text: Objetivo
    - textbox "Objetivo": Preparar una explicación de las decisiones del proyecto
    - text: Modo y composición
    - combobox "Modo y composición":
      - option "Defensa oral" [selected]
      - option "Autoestudio"
    - paragraph: "Agentes de la composición disponible: material-retriever, followup-question-agent, practice-question-agent, grounding-verifier, coherence-verifier, constitutional-control, safe-fallback. Sus contratos y controles obligatorios se mantienen."
    - text: Modelo local
    - combobox "Modelo local":
      - option "deterministic" [selected]
      - option "guided_controlled"
    - text: Idioma
    - textbox "Idioma": es
    - text: Límite de turnos
    - spinbutton "Límite de turnos": "3"
    - text: Límite de segundos
    - spinbutton "Límite de segundos": "600"
    - text: Plazo finito de conservación en días
    - spinbutton "Plazo finito de conservación en días": "7"
    - text: Contenido permitido por la política de conservación
    - combobox "Contenido permitido por la política de conservación":
      - option "Transcripción y resumen, elegibles por separado" [selected]
      - option "Solo transcripción"
      - option "Solo resumen"
    - text: Acceso al contenido conservado
    - combobox "Acceso al contenido conservado":
      - option "Participante y revisión docente autorizada" [selected]
      - option "Solo participante"
    - checkbox "Permitir conocimiento general etiquetado"
    - text: Permitir conocimiento general etiquetado
    - checkbox "Permitir elección de conservación" [checked]
    - text: Permitir elección de conservación
    - checkbox "Autorizar resumen descriptivo" [checked]
    - text: Autorizar resumen descriptivo Preguntas iniciales, una por línea
    - textbox "Preguntas iniciales, una por línea": Explica la decisión principal de tu proyecto.
    - text: Temas autorizados separados por comas
    - textbox "Temas autorizados separados por comas": arquitectura
    - text: Dificultad orientativa de preguntas
    - combobox "Dificultad orientativa de preguntas":
      - option "Baja"
      - option "Media" [selected]
      - option "Alta"
    - checkbox "Entrada de voz local configurada"
    - text: Entrada de voz local configurada
    - checkbox "Salida de voz local configurada"
    - text: Salida de voz local configurada
    - group "Versiones de material autorizadas"
    - text: Código seudónimo destinatario de la política
    - textbox "Código seudónimo destinatario de la política"
    - button "Preparar política explícita para revisar"
    - text: Política de salida autorizada
    - textbox "Política de salida autorizada": "{ \"allowed_disclosures\": [ { \"category\": \"defense_summary\", \"provenance\": \"persisted_session_facts\", \"recipient\": \"pilot-3e5b8a06-113b-4374-98a2-e3b573c39488\" }, { \"category\": \"generated_defense\", \"provenance\": \"defense-agency\", \"recipient\": \"pilot-3e5b8a06-113b-4374-98a2-e3b573c39488\" } ], \"allowed_operational_messages\": [], \"allowed_recipients\": [ \"pilot-3e5b8a06-113b-4374-98a2-e3b573c39488\" ], \"allowed_scopes\": { \"actions\": [ \"acknowledge_missing_info\", \"ask\", \"clarify\", \"finish\", \"respond\" ], \"purposes\": [ \"clarify_response\", \"missing_information\", \"oral_defense\", \"oral_defense_close\", \"oral_defense_summary\" ], \"topics\": [ \"activity\" ] }, \"allowed_templates\": [ [ \"defense-clarification\", 1 ], [ \"defense-dynamic-output\", 1 ], [ \"defense-initial-question\", 1 ], [ \"defense-limit-close\", 1 ], [ \"defense-missing-information\", 1 ], [ \"defense-summary\", 1 ], [ \"defense-voluntary-close\", 1 ] ], \"general_knowledge_allowed\": false, \"policy_id\": \"57106d89-5fe1-4132-a5da-f94dd185f9e1\", \"policy_version\": 1, \"schema_version\": 1 }"
    - checkbox "He revisado los permisos de salida de esta versión" [checked]
    - text: He revisado los permisos de salida de esta versión
    - button "Guardar borrador"
  - heading "Versiones de actividad" [level=2]
  - group: Materiales disponibles y estado
  - article "Actividad Gobierno b9a37c2d-e58c-4f35-90d8-21f8d189418b versión 2":
    - heading "Gobierno b9a37c2d-e58c-4f35-90d8-21f8d189418b v2" [level=3]
    - paragraph: d7cc7907-6dd6-4e35-8422-2e9522c46bb4 — active — 3 turnos
    - paragraph:
      - link "Abrir actividad de defensa":
        - /url: /defensa?activity=d7cc7907-6dd6-4e35-8422-2e9522c46bb4
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión" [disabled]
    - button "Retirar versión"
  - article "Actividad Gobierno b9a37c2d-e58c-4f35-90d8-21f8d189418b versión 1":
    - heading "Gobierno b9a37c2d-e58c-4f35-90d8-21f8d189418b v1" [level=3]
    - paragraph: bd0e9e3a-fbd0-4401-9306-44055b12ffa6 — retired — 2 turnos
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión"
    - button "Retirar versión" [disabled]
  - article "Actividad Diálogo sintético versión 1":
    - heading "Diálogo sintético v1" [level=3]
    - paragraph: 99dc010f-402d-4235-9e8e-4f3eaa2d6a72 — active — 16 turnos
    - paragraph:
      - link "Abrir actividad de autoestudio":
        - /url: /autoestudio?activity=99dc010f-402d-4235-9e8e-4f3eaa2d6a72
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión" [disabled]
    - button "Retirar versión"
  - article "Actividad Diálogo sintético versión 1":
    - heading "Diálogo sintético v1" [level=3]
    - paragraph: 96aa9b90-c8ab-4dc2-b0ee-036ff93d02d3 — active — 16 turnos
    - paragraph:
      - link "Abrir actividad de autoestudio":
        - /url: /autoestudio?activity=96aa9b90-c8ab-4dc2-b0ee-036ff93d02d3
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión" [disabled]
    - button "Retirar versión"
  - article "Actividad Defensa HTTP versión 1":
    - heading "Defensa HTTP v1" [level=3]
    - paragraph: 174e80ff-ec0c-42d2-9ee8-751dd9151b6b — active — 10 turnos
    - paragraph:
      - link "Abrir actividad de defensa":
        - /url: /defensa?activity=174e80ff-ec0c-42d2-9ee8-751dd9151b6b
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión" [disabled]
    - button "Retirar versión"
  - article "Actividad Defensa HTTP versión 1":
    - heading "Defensa HTTP v1" [level=3]
    - paragraph: 98e95004-9fc3-41a7-9e74-1362ebcd3dbd — active — 2 turnos
    - paragraph:
      - link "Abrir actividad de defensa":
        - /url: /defensa?activity=98e95004-9fc3-41a7-9e74-1362ebcd3dbd
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión" [disabled]
    - button "Retirar versión"
  - article "Actividad Defensa HTTP versión 1":
    - heading "Defensa HTTP v1" [level=3]
    - paragraph: f70fd291-c521-4d42-87eb-3d63a5395376 — active — 10 turnos
    - paragraph:
      - link "Abrir actividad de defensa":
        - /url: /defensa?activity=f70fd291-c521-4d42-87eb-3d63a5395376
    - button "Editar como nueva versión"
    - button "Duplicar como nueva actividad"
    - button "Activar versión" [disabled]
    - button "Retirar versión"
  - heading "Sesiones consentidas vigentes" [level=2]
  - button "Actualizar revisión"
  - paragraph: No hay sesiones revisables.
  - paragraph: Los alias no garantizan anonimización del texto libre. Revisa su posible información personal antes de incluirlo.
  - checkbox "Incluir texto libre autorizado" [checked]
  - text: Incluir texto libre autorizado
  - checkbox "He revisado el texto libre de todas las sesiones seleccionadas" [checked]
  - text: He revisado el texto libre de todas las sesiones seleccionadas
  - button "Exportar JSON" [disabled]
  - button "Exportar Markdown" [disabled]
  - button "Purgar expirados"
  - heading "Estado técnico del índice" [level=2]
  - text: "{ \"status\": \"metadata_available\", \"version\": \"1\", \"integrity_verified\": false }"
  - paragraph: Estos metadatos muestran la versión local; no acreditan integridad ni calidad de recuperación.
  - button "Reconstruir índice autorizado"
  - heading "Métricas agregadas del sistema" [level=2]
  - text: "{ \"scope\": \"system_aggregate\", \"sessions\": 6, \"turns\": 17, \"completed_sessions\": 6, \"blocked_turns\": 0, \"incidents\": 0, \"latency_ms_mean\": 47.35294117647059, \"latency_observations\": 17, \"missing\": { \"turn_latency\": 0, \"perceived_usefulness\": \"not_collected\", \"academic_metrics\": \"out_of_scope\" } }"
  - link "Participar en defensa":
    - /url: /defensa
  - link "Participar en autoestudio":
    - /url: /autoestudio
```

# Test source

```ts
  76  |       exact: true,
  77  |     })
  78  |     .press("Enter");
  79  |   await expect(
  80  |     page.getByRole("region", { name: "Revisión consentida" }),
  81  |   ).toContainText("Una explicación ficticia");
  82  |   await page
  83  |     .getByLabel(`Sesión ${session.session_id}`, { exact: false })
  84  |     .press("Space");
  85  |   await page.getByLabel("Incluir texto libre autorizado").press("Space");
  86  |   await expect(
  87  |     page.getByRole("button", { name: "Exportar JSON", exact: true }),
  88  |   ).toBeDisabled();
  89  |   await page
  90  |     .getByLabel(
  91  |       "He revisado el texto libre de todas las sesiones seleccionadas",
  92  |     )
  93  |     .press("Space");
  94  |   for (const format of ["JSON", "Markdown"]) {
  95  |     const pending = page.waitForEvent("download");
  96  |     await page
  97  |       .getByRole("button", { name: `Exportar ${format}`, exact: true })
  98  |       .press("Enter");
  99  |     const file = await (await pending).path();
  100 |     const text = await readFile(file!, "utf8");
  101 |     expect(text).toContain("Una explicación ficticia");
  102 |     expect(text).not.toContain(participant);
  103 |     expect(text).not.toContain(session.session_id);
  104 |     expect(text).not.toContain(session.access_token);
  105 |     expect(text).not.toContain("fictional-e2e-installation-secret-005");
  106 |   }
  107 |   await firstArticle
  108 |     .getByRole("button", { name: "Editar como nueva versión" })
  109 |     .press("Enter");
  110 |   await page.getByLabel("Límite de turnos", { exact: true }).fill("3");
  111 |   await page
  112 |     .getByLabel("He revisado los permisos de salida de esta versión")
  113 |     .press("Space");
  114 |   const duplicated = page.waitForResponse(
  115 |     (r) =>
  116 |       r.url().endsWith(`/governance/activities/${activity.id}/duplicate`) &&
  117 |       r.request().method() === "POST",
  118 |   );
  119 |   await page
  120 |     .getByRole("button", { name: "Crear versión sucesora", exact: true })
  121 |     .press("Enter");
  122 |   expect((await duplicated).status()).toBe(201);
  123 |   const successor = page.getByRole("article", {
  124 |     name: `Actividad ${name} versión 2`,
  125 |     exact: true,
  126 |   });
  127 |   await successor.getByRole("button", { name: "Activar versión" }).press("Enter");
  128 |   await expect(successor).toContainText("active");
  129 |   await expect(firstArticle).toContainText("retired");
  130 |   const previous = await page.request.get(
  131 |     `http://127.0.0.1:8005/api/v1/governance/sessions/${session.session_id}`,
  132 |   );
  133 |   expect((await previous.json()).configuration.version).toBe(1);
  134 |   const retiredStart = await request.post(
  135 |     "http://127.0.0.1:8005/api/v1/sessions",
  136 |     {
  137 |       data: {
  138 |         participant_code: "another-pilot",
  139 |         activity_configuration_id: activity.id,
  140 |       },
  141 |     },
  142 |   );
  143 |   expect(retiredStart.status()).toBe(409);
  144 |   await page
  145 |     .getByLabel("Confirmo eliminar el contenido de esta sesión", {
  146 |       exact: true,
  147 |     })
  148 |     .press("Space");
  149 |   const deleteReviewed = page.getByRole("button", { name: "Eliminar sesión revisada" });
  150 |   await expect(deleteReviewed).toBeEnabled();
  151 |   const deleted = page.waitForResponse(
  152 |     r => r.url().endsWith(`/api/v1/sessions/${session.session_id}/content`)
  153 |       && r.request().method() === "DELETE",
  154 |   );
  155 |   await deleteReviewed.press("Enter");
  156 |   expect((await deleted).status()).toBe(200);
  157 |   await expect(page.getByRole("status")).toContainText(
  158 |     "Eliminación confirmada",
  159 |   );
  160 |   expect(
  161 |     (
  162 |       await page.request.get(
  163 |         `http://127.0.0.1:8005/api/v1/governance/sessions/${session.session_id}`,
  164 |       )
  165 |     ).status(),
  166 |   ).toBe(404);
  167 |   expect(
  168 |     (
  169 |       await page.request.post(
  170 |         "http://127.0.0.1:8005/api/v1/governance/exports",
  171 |         { data: { session_ids: [session.session_id] } },
  172 |       )
  173 |     ).status(),
  174 |   ).toBe(409);
  175 |   await page.getByRole("button", { name: "Cerrar acceso docente" }).press("Enter");
> 176 |   await expect(page.getByLabel("Credencial local")).toBeVisible();
      |                                                     ^ Error: expect(locator).toBeVisible() failed
  177 |   expect(
  178 |     (
  179 |       await page.request.get("http://127.0.0.1:8005/api/v1/governance/sessions")
  180 |     ).status(),
  181 |   ).toBe(401);
  182 | });
  183 | 
```