# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_scenario_a.spec.ts >> Escenario A — sesión completa de participante
- Location: ..\..\tests\e2e\test_scenario_a.spec.ts:8:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.turn-log .system')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" locator('.turn-log .system') with timeout 5000ms
  - waiting for locator('.turn-log .system')

```

```yaml
- banner:
  - navigation "Navegación general":
    - link "Volver al inicio":
      - /url: /
- main:
  - heading "ORAL-IA — Participante" [level=1]
  - status: Estás interactuando con ORAL-IA, un sistema automático de apoyo docente. Puede cometer errores y no sustituye el criterio del profesorado.
  - log: Hola, esto es una prueba
  - text: Tu mensaje
  - textbox "Tu mensaje" [disabled]
  - button "Enviar" [disabled]
  - region "Privacidad de tu sesión":
    - heading "Privacidad de tu sesión" [level=2]
    - paragraph: Uso local seudónimo. La negativa no impide participar. Sin consentimiento se elimina contenido al cerrar; audio nunca se conserva.
    - paragraph: "Plazo: 30 días. Acceso docente solo a lo consentido."
    - button "Revisar registro completo"
  - button "Finalizar sesión" [disabled]
```

# Test source

```ts
  1  | import { test, expect } from "./local_auth";
  2  | 
  3  | // Escenario A (quickstart.md): sesión válida de extremo a extremo — inicio, un turno,
  4  | // finalización voluntaria, y verificación en el área técnica de que todo quedó
  5  | // registrado. Requires `npm install` in apps/web and the API running on :8000; this
  6  | // environment has no Node.js available so this spec is written but not run here.
  7  | 
  8  | test("Escenario A — sesión completa de participante", async ({
  9  |   page,
  10 |   request,
  11 | }) => {
  12 |   const seedResponse = await request.post(
  13 |     "http://127.0.0.1:8005/api/v1/activities",
  14 |     {
  15 |       data: {
  16 |         course_id: "30000000-0000-0000-0000-000000000001",
  17 |         name: "Actividad E2E",
  18 |         subject: "Demo",
  19 |         objective: "Probar el flujo end-to-end",
  20 |         mode: "texto",
  21 |         language: "es",
  22 |         max_turns: 10,
  23 |         max_duration_seconds: 900,
  24 |         retention_policy_id: "30000000-0000-0000-0000-000000000002",
  25 |         output_authorization_policy: {
  26 |           schema_version: 1,
  27 |           policy_id: "e2e-core",
  28 |           policy_version: 1,
  29 |           allowed_recipients: ["part-e2e001"],
  30 |           allowed_disclosures: [
  31 |             {
  32 |               category: "public_activity",
  33 |               provenance: "trusted_template",
  34 |               recipient: "part-e2e001",
  35 |             },
  36 |           ],
  37 |           allowed_scopes: {
  38 |             topics: ["activity"],
  39 |             purposes: ["acknowledge_turn"],
  40 |             actions: ["continue"],
  41 |           },
  42 |           general_knowledge_allowed: false,
  43 |           allowed_templates: [["sc007-acknowledgement", 1]],
  44 |           allowed_operational_messages: [],
  45 |         },
  46 |       },
  47 |     },
  48 |   );
  49 |   expect(seedResponse.ok(), await seedResponse.text()).toBeTruthy();
  50 |   const activity = await seedResponse.json();
  51 | 
  52 |   await page.goto("/participante");
  53 |   await page
  54 |     .getByLabel("Código de participante (seudónimo)")
  55 |     .fill("part-e2e001");
  56 |   await page.getByLabel("Identificador de actividad").fill(activity.id);
  57 |   const started = page.waitForResponse(
  58 |     (response) =>
  59 |       response.url().endsWith("/api/v1/sessions") &&
  60 |       response.request().method() === "POST",
  61 |   );
  62 |   await page.getByRole("button", { name: "Iniciar sesión" }).click();
  63 |   const session = await (await started).json();
  64 | 
  65 |   await expect(page.getByRole("status")).toContainText("sistema automático");
  66 | 
  67 |   await page.getByLabel("Tu mensaje").fill("Hola, esto es una prueba");
  68 |   await page.getByRole("button", { name: "Enviar" }).click();
> 69 |   await expect(page.locator(".turn-log .system")).toBeVisible();
     |                                                   ^ Error: expect(locator).toBeVisible() failed
  70 | 
  71 |   await page.getByRole("button", { name: "Finalizar sesión" }).click();
  72 |   await expect(page.getByRole("status")).toContainText("finalizado");
  73 | 
  74 |   await page.goto("/tecnica");
  75 |   await page.getByRole("button", { name: "Sesiones" }).click();
  76 |   await expect(
  77 |     page.getByRole("button", {
  78 |       name: `${session.session_id.slice(0, 8)} — closed_voluntary — 1 turnos`,
  79 |       exact: true,
  80 |     }),
  81 |   ).toBeVisible();
  82 | });
  83 | 
```