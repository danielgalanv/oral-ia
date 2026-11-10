# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_governance_flow.spec.ts >> local governance: real login, immutable successor, consented review, two exports, deletion and logout
- Location: ..\..\tests\e2e\test_governance_flow.spec.ts:7:5

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.waitForResponse: Test timeout of 30000ms exceeded.
```

# Page snapshot

```yaml
- generic [ref=f2e2]:
  - banner [ref=f2e3]:
    - navigation "Navegación general" [ref=f2e4]:
      - link "Volver al inicio" [ref=f2e5] [cursor=pointer]:
        - /url: /
  - main [ref=f2e6]:
    - heading "ORAL-IA — Gobierno docente" [level=1] [ref=f2e7]
    - region "Gestión de sesión activa" [ref=f2e8]:
      - heading "Sesión activa" [level=2] [ref=f2e9]
      - button "Comprobar sesión activa" [ref=f2e10] [cursor=pointer]
    - paragraph [ref=f2e11]: Configuración y evidencia del sistema; sin notas ni perfiles de estudiantes.
    - button "Cerrar acceso docente" [ref=f2e12] [cursor=pointer]
    - status [ref=f2e13]: "Eliminación confirmada: contenido no disponible para revisión ni exportación."
    - generic [ref=f2e14]:
      - heading "Nueva configuración" [level=2] [ref=f2e15]
      - group [ref=f2e17]:
        - generic [ref=f2e18]:
          - text: Asignatura
          - combobox "Asignatura" [ref=f2e19]:
            - option "Crear asignatura local"
            - option "Curso E2E autoestudio"
            - option "Dominio sintético"
            - option "Dominio sintético"
            - option "Curso ficticio local" [selected]
        - generic [ref=f2e20]:
          - text: Nombre de actividad
          - textbox "Nombre de actividad" [ref=f2e21]: Gobierno 78d9e697-2465-46ba-87d8-d6a1437bef28
        - generic [ref=f2e22]:
          - text: Materia
          - textbox "Materia" [ref=f2e23]: Explicación de decisiones
        - generic [ref=f2e24]:
          - text: Objetivo
          - textbox "Objetivo" [ref=f2e25]: Preparar una explicación de las decisiones del proyecto
        - generic [ref=f2e26]:
          - text: Modo y composición
          - combobox "Modo y composición" [ref=f2e27]:
            - option "Defensa oral" [selected]
            - option "Autoestudio"
        - paragraph [ref=f2e28]: "Agentes de la composición disponible: material-retriever, followup-question-agent, practice-question-agent, grounding-verifier, coherence-verifier, constitutional-control, safe-fallback. Sus contratos y controles obligatorios se mantienen."
        - generic [ref=f2e29]:
          - text: Modelo local
          - combobox "Modelo local" [ref=f2e30]:
            - option "deterministic" [selected]
            - option "guided_controlled"
        - generic [ref=f2e31]:
          - text: Idioma
          - textbox "Idioma" [ref=f2e32]: es
        - generic [ref=f2e33]:
          - text: Límite de turnos
          - spinbutton "Límite de turnos" [ref=f2e34]: "3"
        - generic [ref=f2e35]:
          - text: Límite de segundos
          - spinbutton "Límite de segundos" [ref=f2e36]: "600"
        - generic [ref=f2e37]:
          - text: Plazo finito de conservación en días
          - spinbutton "Plazo finito de conservación en días" [ref=f2e38]: "7"
        - generic [ref=f2e39]:
          - text: Contenido permitido por la política de conservación
          - combobox "Contenido permitido por la política de conservación" [ref=f2e40]:
            - option "Transcripción y resumen, elegibles por separado" [selected]
            - option "Solo transcripción"
            - option "Solo resumen"
        - generic [ref=f2e41]:
          - text: Acceso al contenido conservado
          - combobox "Acceso al contenido conservado" [ref=f2e42]:
            - option "Participante y revisión docente autorizada" [selected]
            - option "Solo participante"
        - generic [ref=f2e43]:
          - checkbox "Permitir conocimiento general etiquetado" [ref=f2e44]
          - text: Permitir conocimiento general etiquetado
        - generic [ref=f2e45]:
          - checkbox "Permitir elección de conservación" [checked] [ref=f2e46]
          - text: Permitir elección de conservación
        - generic [ref=f2e47]:
          - checkbox "Autorizar resumen descriptivo" [checked] [ref=f2e48]
          - text: Autorizar resumen descriptivo
        - generic [ref=f2e49]:
          - text: Preguntas iniciales, una por línea
          - textbox "Preguntas iniciales, una por línea" [ref=f2e50]: Explica la decisión principal de tu proyecto.
        - generic [ref=f2e51]:
          - text: Temas autorizados separados por comas
          - textbox "Temas autorizados separados por comas" [ref=f2e52]: arquitectura
        - generic [ref=f2e53]:
          - text: Dificultad orientativa de preguntas
          - combobox "Dificultad orientativa de preguntas" [ref=f2e54]:
            - option "Baja"
            - option "Media" [selected]
            - option "Alta"
        - generic [ref=f2e55]:
          - checkbox "Entrada de voz local configurada" [ref=f2e56]
          - text: Entrada de voz local configurada
        - generic [ref=f2e57]:
          - checkbox "Salida de voz local configurada" [ref=f2e58]
          - text: Salida de voz local configurada
        - group "Versiones de material autorizadas" [ref=f2e59]
        - generic [ref=f2e61]:
          - text: Código seudónimo destinatario de la política
          - textbox "Código seudónimo destinatario de la política" [ref=f2e62]
        - button "Preparar política explícita para revisar" [ref=f2e63] [cursor=pointer]
        - generic [ref=f2e64]:
          - text: Política de salida autorizada
          - textbox "Política de salida autorizada" [ref=f2e65]: "{ \"allowed_disclosures\": [ { \"category\": \"defense_summary\", \"provenance\": \"persisted_session_facts\", \"recipient\": \"pilot-f871b82d-a47f-4d5f-a3e3-f9863043087a\" }, { \"category\": \"generated_defense\", \"provenance\": \"defense-agency\", \"recipient\": \"pilot-f871b82d-a47f-4d5f-a3e3-f9863043087a\" } ], \"allowed_operational_messages\": [], \"allowed_recipients\": [ \"pilot-f871b82d-a47f-4d5f-a3e3-f9863043087a\" ], \"allowed_scopes\": { \"actions\": [ \"acknowledge_missing_info\", \"ask\", \"clarify\", \"finish\", \"respond\" ], \"purposes\": [ \"clarify_response\", \"missing_information\", \"oral_defense\", \"oral_defense_close\", \"oral_defense_summary\" ], \"topics\": [ \"activity\" ] }, \"allowed_templates\": [ [ \"defense-clarification\", 1 ], [ \"defense-dynamic-output\", 1 ], [ \"defense-initial-question\", 1 ], [ \"defense-limit-close\", 1 ], [ \"defense-missing-information\", 1 ], [ \"defense-summary\", 1 ], [ \"defense-voluntary-close\", 1 ] ], \"general_knowledge_allowed\": false, \"policy_id\": \"7f46f502-fdff-4652-afd8-b411b4f80ce9\", \"policy_version\": 1, \"schema_version\": 1 }"
        - generic [ref=f2e66]:
          - checkbox "He revisado los permisos de salida de esta versión" [checked] [ref=f2e67]
          - text: He revisado los permisos de salida de esta versión
        - button "Guardar borrador" [ref=f2e68] [cursor=pointer]
    - generic [ref=f2e69]:
      - heading "Versiones de actividad" [level=2] [ref=f2e70]
      - group [ref=f2e71]:
        - generic "Materiales disponibles y estado" [ref=f2e72]
      - article "Actividad Gobierno 78d9e697-2465-46ba-87d8-d6a1437bef28 versión 2" [ref=f2e73]:
        - heading "Gobierno 78d9e697-2465-46ba-87d8-d6a1437bef28 v2" [level=3] [ref=f2e74]
        - paragraph [ref=f2e75]: c4d0f625-3812-46f7-9474-4c3f50016b06 — active — 3 turnos
        - paragraph [ref=f2e76]:
          - link "Abrir actividad de defensa" [ref=f2e77] [cursor=pointer]:
            - /url: /defensa?activity=c4d0f625-3812-46f7-9474-4c3f50016b06
        - button "Editar como nueva versión" [ref=f2e78] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e79] [cursor=pointer]
        - button "Activar versión" [disabled] [ref=f2e80]
        - button "Retirar versión" [ref=f2e81] [cursor=pointer]
      - article "Actividad Gobierno 78d9e697-2465-46ba-87d8-d6a1437bef28 versión 1" [ref=f2e82]:
        - heading "Gobierno 78d9e697-2465-46ba-87d8-d6a1437bef28 v1" [level=3] [ref=f2e83]
        - paragraph [ref=f2e84]: 3444142a-94a1-4810-ad16-4ee5d43c39dc — retired — 2 turnos
        - button "Editar como nueva versión" [ref=f2e85] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e86] [cursor=pointer]
        - button "Activar versión" [ref=f2e87] [cursor=pointer]
        - button "Retirar versión" [disabled] [ref=f2e88]
      - article "Actividad Diálogo sintético versión 1" [ref=f2e89]:
        - heading "Diálogo sintético v1" [level=3] [ref=f2e90]
        - paragraph [ref=f2e91]: 2f58eeaf-1268-464b-a3cc-fa83218d6352 — active — 16 turnos
        - paragraph [ref=f2e92]:
          - link "Abrir actividad de autoestudio" [ref=f2e93] [cursor=pointer]:
            - /url: /autoestudio?activity=2f58eeaf-1268-464b-a3cc-fa83218d6352
        - button "Editar como nueva versión" [ref=f2e94] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e95] [cursor=pointer]
        - button "Activar versión" [disabled] [ref=f2e96]
        - button "Retirar versión" [ref=f2e97] [cursor=pointer]
      - article "Actividad Diálogo sintético versión 1" [ref=f2e98]:
        - heading "Diálogo sintético v1" [level=3] [ref=f2e99]
        - paragraph [ref=f2e100]: 4fad9358-c6a2-442f-be61-7775a9803751 — active — 16 turnos
        - paragraph [ref=f2e101]:
          - link "Abrir actividad de autoestudio" [ref=f2e102] [cursor=pointer]:
            - /url: /autoestudio?activity=4fad9358-c6a2-442f-be61-7775a9803751
        - button "Editar como nueva versión" [ref=f2e103] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e104] [cursor=pointer]
        - button "Activar versión" [disabled] [ref=f2e105]
        - button "Retirar versión" [ref=f2e106] [cursor=pointer]
      - article "Actividad Defensa HTTP versión 1" [ref=f2e107]:
        - heading "Defensa HTTP v1" [level=3] [ref=f2e108]
        - paragraph [ref=f2e109]: 9d4c856a-cc8c-4007-868a-aeb3837e27a2 — active — 10 turnos
        - paragraph [ref=f2e110]:
          - link "Abrir actividad de defensa" [ref=f2e111] [cursor=pointer]:
            - /url: /defensa?activity=9d4c856a-cc8c-4007-868a-aeb3837e27a2
        - button "Editar como nueva versión" [ref=f2e112] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e113] [cursor=pointer]
        - button "Activar versión" [disabled] [ref=f2e114]
        - button "Retirar versión" [ref=f2e115] [cursor=pointer]
      - article "Actividad Defensa HTTP versión 1" [ref=f2e116]:
        - heading "Defensa HTTP v1" [level=3] [ref=f2e117]
        - paragraph [ref=f2e118]: 91db6cbe-d629-40c2-b39e-7e452847be48 — active — 2 turnos
        - paragraph [ref=f2e119]:
          - link "Abrir actividad de defensa" [ref=f2e120] [cursor=pointer]:
            - /url: /defensa?activity=91db6cbe-d629-40c2-b39e-7e452847be48
        - button "Editar como nueva versión" [ref=f2e121] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e122] [cursor=pointer]
        - button "Activar versión" [disabled] [ref=f2e123]
        - button "Retirar versión" [ref=f2e124] [cursor=pointer]
      - article "Actividad Defensa HTTP versión 1" [ref=f2e125]:
        - heading "Defensa HTTP v1" [level=3] [ref=f2e126]
        - paragraph [ref=f2e127]: c85dd592-c111-47f9-a79c-a9e157ccacdf — active — 10 turnos
        - paragraph [ref=f2e128]:
          - link "Abrir actividad de defensa" [ref=f2e129] [cursor=pointer]:
            - /url: /defensa?activity=c85dd592-c111-47f9-a79c-a9e157ccacdf
        - button "Editar como nueva versión" [ref=f2e130] [cursor=pointer]
        - button "Duplicar como nueva actividad" [ref=f2e131] [cursor=pointer]
        - button "Activar versión" [disabled] [ref=f2e132]
        - button "Retirar versión" [ref=f2e133] [cursor=pointer]
    - generic [ref=f2e134]:
      - heading "Sesiones consentidas vigentes" [level=2] [ref=f2e135]
      - button "Actualizar revisión" [ref=f2e136] [cursor=pointer]
      - paragraph [ref=f2e137]: No hay sesiones revisables.
      - paragraph [ref=f2e138]: Los alias no garantizan anonimización del texto libre. Revisa su posible información personal antes de incluirlo.
      - generic [ref=f2e139]:
        - checkbox "Incluir texto libre autorizado" [checked] [ref=f2e140]
        - text: Incluir texto libre autorizado
      - generic [ref=f2e141]:
        - checkbox "He revisado el texto libre de todas las sesiones seleccionadas" [checked] [ref=f2e142]
        - text: He revisado el texto libre de todas las sesiones seleccionadas
      - button "Exportar JSON" [disabled] [ref=f2e143]
      - button "Exportar Markdown" [disabled] [ref=f2e144]
      - button "Purgar expirados" [ref=f2e145] [cursor=pointer]
    - generic [ref=f2e146]:
      - heading "Estado técnico del índice" [level=2] [ref=f2e147]
      - generic [ref=f2e148]: "{ \"status\": \"metadata_available\", \"version\": \"1\", \"integrity_verified\": false }"
      - paragraph [ref=f2e149]: Estos metadatos muestran la versión local; no acreditan integridad ni calidad de recuperación.
      - button "Reconstruir índice autorizado" [ref=f2e150] [cursor=pointer]
    - generic [ref=f2e151]:
      - heading "Métricas agregadas del sistema" [level=2] [ref=f2e152]
      - generic [ref=f2e153]: "{ \"scope\": \"system_aggregate\", \"sessions\": 6, \"turns\": 17, \"completed_sessions\": 6, \"blocked_turns\": 0, \"incidents\": 0, \"latency_ms_mean\": 48.411764705882355, \"latency_observations\": 17, \"missing\": { \"turn_latency\": 0, \"perceived_usefulness\": \"not_collected\", \"academic_metrics\": \"out_of_scope\" } }"
    - link "Participar en defensa" [ref=f2e154] [cursor=pointer]:
      - /url: /defensa
    - link "Participar en autoestudio" [ref=f2e155] [cursor=pointer]:
      - /url: /autoestudio
```

# Test source

```ts
  51  |     exact: true,
  52  |   });
  53  |   await firstArticle.getByRole("button", { name: "Activar versión" }).press("Enter");
  54  |   await expect(firstArticle).toContainText("active");
  55  |   await page.goto("/defensa");
  56  |   await page.getByLabel("Código seudónimo", { exact: true }).fill(participant);
  57  |   await page.getByLabel("Actividad", { exact: true }).fill(activity.id);
  58  |   const opened = page.waitForResponse(
  59  |     (r) =>
  60  |       r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST",
  61  |   );
  62  |   await page.getByRole("button", { name: "Iniciar defensa" }).press("Enter");
  63  |   const session = await (await opened).json();
  64  |   await expect(page.locator(".system")).toHaveCount(1);
  65  |   await page.getByLabel("Conservar transcripción", { exact: true }).press("Space");
  66  |   await page.getByLabel("Conservar resumen", { exact: true }).press("Space");
  67  |   await page
  68  |     .getByLabel("Tu respuesta", { exact: true })
  69  |     .fill("Una explicación ficticia de la decisión principal.");
  70  |   await page.getByRole("button", { name: "Enviar", exact: true }).press("Enter");
  71  |   await expect(page.getByRole("status")).toContainText("closed_limit_reached");
  72  |   await page.goto("/gobierno");
  73  |   await page
  74  |     .getByRole("button", {
  75  |       name: `Revisar sesión ${session.session_id}`,
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
> 151 |   const deleted = page.waitForResponse(
      |                        ^ Error: page.waitForResponse: Test timeout of 30000ms exceeded.
  152 |     r => r.url().endsWith(`/governance/sessions/${session.session_id}/content`)
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
  176 |   await expect(page.getByLabel("Credencial local")).toBeVisible();
  177 |   expect(
  178 |     (
  179 |       await page.request.get("http://127.0.0.1:8005/api/v1/governance/sessions")
  180 |     ).status(),
  181 |   ).toBe(401);
  182 | });
  183 | 
```