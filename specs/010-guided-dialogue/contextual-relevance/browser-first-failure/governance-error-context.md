# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_governance_flow.spec.ts >> local governance: real login, immutable successor, consented review, two exports, deletion and logout
- Location: ..\..\tests\e2e\test_governance_flow.spec.ts:7:5

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: getByRole('status')
Expected substring: "Eliminación confirmada"
Received string:    "Borrador creado: c97c8532-82d6-4ba7-a857-7051aa37c8af — versión 2. Revisa y activa para nuevos usos."
Timeout: 5000ms

Call log:
  - Expect "toContainText" getByRole('status') with timeout 5000ms
  - waiting for getByRole('status')
    14 × locator resolved to <p role="status">Borrador creado: c97c8532-82d6-4ba7-a857-7051aa37…</p>
       - unexpected value "Borrador creado: c97c8532-82d6-4ba7-a857-7051aa37c8af — versión 2. Revisa y activa para nuevos usos."

```

```yaml
- status: "Borrador creado: c97c8532-82d6-4ba7-a857-7051aa37c8af — versión 2. Revisa y activa para nuevos usos."
```

# Test source

```ts
  50  |     name: `Actividad ${name} versión 1`,
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
  149 |   await page.getByRole("button", { name: "Eliminar sesión revisada" }).press("Enter");
> 150 |   await expect(page.getByRole("status")).toContainText(
      |                                          ^ Error: expect(locator).toContainText(expected) failed
  151 |     "Eliminación confirmada",
  152 |   );
  153 |   expect(
  154 |     (
  155 |       await page.request.get(
  156 |         `http://127.0.0.1:8005/api/v1/governance/sessions/${session.session_id}`,
  157 |       )
  158 |     ).status(),
  159 |   ).toBe(404);
  160 |   expect(
  161 |     (
  162 |       await page.request.post(
  163 |         "http://127.0.0.1:8005/api/v1/governance/exports",
  164 |         { data: { session_ids: [session.session_id] } },
  165 |       )
  166 |     ).status(),
  167 |   ).toBe(409);
  168 |   await page.getByRole("button", { name: "Cerrar acceso docente" }).press("Enter");
  169 |   await expect(page.getByLabel("Credencial local")).toBeVisible();
  170 |   expect(
  171 |     (
  172 |       await page.request.get("http://127.0.0.1:8005/api/v1/governance/sessions")
  173 |     ).status(),
  174 |   ).toBe(401);
  175 | });
  176 | 
```