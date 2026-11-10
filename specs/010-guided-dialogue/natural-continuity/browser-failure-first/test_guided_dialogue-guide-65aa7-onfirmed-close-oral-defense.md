# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_guided_dialogue.spec.ts >> guided actual provider, owner resume and confirmed close: oral_defense
- Location: ..\..\tests\e2e\test_guided_dialogue.spec.ts:6:7

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('.system')
Expected substring: "condiciones"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toContainText" locator('.system') with timeout 5000ms
  - waiting for locator('.system')

```

```yaml
- banner:
  - navigation "Navegación general":
    - link "Volver al inicio":
      - /url: /
- main:
  - heading "ORAL-IA — Defensa oral" [level=1]
  - region "Recuperación de sesión":
    - button "Buscar mi sesión activa"
  - region "Capacidades de la actividad":
    - paragraph: "Perfil: diálogo guiado con contenido docente revisado."
    - paragraph: "Proveedor efectivo observado: compositor de unidades docentes v1."
    - paragraph: Las respuestas se componen desde unidades docentes publicadas. No es generación libre; la utilidad con personas sigue pendiente de validación.
  - alert: Ya hay una sesión activa. Si conservas su acceso, retómala; si lo perdiste, solicita un cierre docente confirmado.
  - paragraph: La voz es opcional y el audio se descarta.
  - text: Código seudónimo
  - textbox "Código seudónimo": synthetic-010
  - text: Actividad
  - textbox "Actividad": a1d35701-db48-43e7-9e0c-932ae98e1200
  - button "Iniciar defensa"
```

# Test source

```ts
  1  | import { execFileSync } from "node:child_process";
  2  | import { resolve } from "node:path";
  3  | import { test, expect } from "./local_auth";
  4  | 
  5  | for (const mode of ["self_study", "oral_defense"] as const) {
  6  |   test(`guided actual provider, owner resume and confirmed close: ${mode}`, async ({ page }) => {
  7  |     test.setTimeout(120_000);
  8  |     const prepared = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", mode], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
  9  |     await page.goto(`${mode === "self_study" ? "/autoestudio" : "/defensa"}?activity=${prepared.activity_id}`);
  10 |     await expect(page.getByRole("region", { name: "Capacidades de la actividad" })).toContainText("contenido docente revisado");
  11 |     await page.getByLabel(mode === "self_study" ? "Código de participante (seudónimo)" : "Código seudónimo", { exact: true }).fill("synthetic-010");
  12 |     const started = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
  13 |     await page.getByRole("button", { name: mode === "self_study" ? "Iniciar sesión" : "Iniciar defensa", exact: true }).click();
  14 |     const session = await (await started).json();
> 15 |     if (mode === "oral_defense") await expect(page.locator(".system")).toContainText("condiciones");
     |                                                                        ^ Error: expect(locator).toContainText(expected) failed
  16 |     const initialQuestion = mode === "oral_defense" ? await page.locator(".system p").first().innerText() : null;
  17 |     const endpoint = mode === "self_study" ? `/sessions/${session.session_id}/study-turns` : `/defense-sessions/${session.session_id}/defense-turns`;
  18 |     for (const text of mode === "self_study" ? ["¿A qué temperatura hierve el agua?", "el agua puede pasar a ser vapor en algun momento?", "dimelo"] : ["a los 99 grados", "no sé justificarlo", "puedes repetir?", "no entiendo, dilo de otra forma"]) {
  19 |       await page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true }).fill(text);
  20 |       const response = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
  21 |       await page.getByRole("button", { name: "Enviar", exact: true }).click();
  22 |       const actual = await (await response).json();
  23 |       expect(actual.output_text).toBeTruthy();
  24 |       expect(actual.dialogue_status.provider).toBe("reviewed-unit-renderer/v1");
  25 |       expect(actual.dialogue_status.rendered_unit_ids.length).toBeGreaterThan(0);
  26 |       if (mode === "oral_defense") {
  27 |         expect(actual.output_text).not.toContain("100");
  28 |         expect(actual.sources.every((source: { fragment_text: string }) => !source.fragment_text)).toBe(true);
  29 |       }
  30 |     }
  31 |     const controls = page.getByRole("region", { name: "Controles de diálogo" });
  32 |     const repeatedByButton = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
  33 |     await controls.getByRole("button", { name: "Repetir", exact: true }).focus();
  34 |     await page.keyboard.press("Enter");
  35 |     const buttonResult = await (await repeatedByButton).json();
  36 |     expect(buttonResult.dialogue_status.primary_act).toBe("repeat");
  37 |     if (initialQuestion) {
  38 |       expect(buttonResult.output_text).toBe(initialQuestion);
  39 |       await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toContainText(initialQuestion);
  40 |     } else {
  41 |       const sourcePanel = page.locator(".sources-panel").first();
  42 |       await sourcePanel.locator("summary").focus();
  43 |       await page.keyboard.press("Enter");
  44 |       await expect(sourcePanel).toHaveAttribute("open", "");
  45 |       await controls.getByLabel("Modo de estudio", { exact: true }).selectOption("guided_explanation");
  46 |       const modeChanged = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
  47 |       await controls.getByRole("button", { name: "Cambiar modo de estudio", exact: true }).focus();
  48 |       await page.keyboard.press("Enter");
  49 |       expect((await (await modeChanged).json()).mode).toBe("guided_explanation");
  50 |     }
  51 |     // Synthetic loss of transport AFTER the actual API commits. No favorable
  52 |     // response is substituted: reconciliation must find that exact real turn.
  53 |     const before = await (await page.request.get("/api/v1/governance/active-session")).json();
  54 |     let committedTurnId: string | undefined;
  55 |     await page.route(`**/api/v1${endpoint}`, async route => {
  56 |       const actual = await route.fetch();
  57 |       expect(actual.status()).toBe(200);
  58 |       committedTurnId = (await actual.json()).turn_id;
  59 |       await route.abort("failed");
  60 |     }, { times: 1 });
  61 |     await page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true }).fill("puedes repetir?");
  62 |     await page.getByRole("button", { name: "Enviar", exact: true }).click();
  63 |     await expect(page.getByRole("region", { name: "Envío sin confirmar" })).toBeVisible();
  64 |     await expect(page.getByRole("button", { name: "Enviar", exact: true })).toBeDisabled();
  65 |     const reconciled = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
  66 |     await page.getByRole("button", { name: "Consultar resultado del envío", exact: true }).click();
  67 |     const projected = await (await reconciled).json();
  68 |     expect(projected.turn_id).toBe(committedTurnId);
  69 |     expect(projected.request_replayed).toBe(true);
  70 |     await expect(page.getByRole("region", { name: "Envío sin confirmar" })).toHaveCount(0);
  71 |     const after = await (await page.request.get("/api/v1/governance/active-session")).json();
  72 |     expect(after.session.turn_count).toBe(before.session.turn_count + 1);
  73 |     await page.reload();
  74 |     await page.getByRole("button", { name: "Buscar mi sesión activa", exact: true }).click();
  75 |     await page.getByRole("button", { name: "Retomar mi sesión", exact: true }).click();
  76 |     await expect(page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true })).toBeVisible();
  77 |     await page.goto("/gobierno");
  78 |     await page.getByRole("button", { name: "Comprobar sesión activa", exact: true }).click();
  79 |     const close = page.getByRole("button", { name: "Cerrar sesión activa con confirmación", exact: true });
  80 |     await expect(close).toBeDisabled();
  81 |     await page.getByLabel("He revisado la sesión y confirmo el cierre docente", { exact: true }).check();
  82 |     await close.click();
  83 |     await expect(page.getByRole("region", { name: "Gestión de sesión activa" })).toContainText("Cierre docente confirmado");
  84 |     const state = await page.request.get(`/api/v1/governance/active-session`);
  85 |     expect((await state.json()).session).toBeNull();
  86 |   });
  87 | }
  88 | 
```