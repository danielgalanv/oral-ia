# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_guided_dialogue.spec.ts >> guided actual provider, owner resume and confirmed close: self_study
- Location: ..\..\tests\e2e\test_guided_dialogue.spec.ts:6:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('region', { name: 'Envío sin confirmar' })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByRole('region', { name: 'Envío sin confirmar' }) with timeout 5000ms
  - waiting for getByRole('region', { name: 'Envío sin confirmar' })

```

```yaml
- banner:
  - navigation "Navegación general":
    - link "Volver al inicio":
      - /url: /
- main:
  - heading "ORAL-IA — Autoestudio" [level=1]
  - region "Capacidades de la actividad":
    - paragraph: "Perfil: diálogo guiado con contenido docente revisado."
    - paragraph: "Proveedor efectivo observado: compositor de unidades docentes v1."
    - paragraph: Las respuestas se componen desde unidades docentes publicadas. No es generación libre; la utilidad con personas sigue pendiente de validación.
    - paragraph: "Temas disponibles: condensacion, congelacion, ebullicion, evaporacion, presion. Para cambiar, escribe «cambiar de tema» y confirma el tema propuesto."
  - region "Controles de diálogo":
    - button "Repetir" [disabled]
    - button "Otra forma" [disabled]
    - button "Ayuda" [disabled]
    - button "Continuar" [disabled]
    - button "Otro tema" [disabled]
    - text: Modo de estudio
    - combobox "Modo de estudio" [disabled]:
      - option "Elige un modo habilitado"
      - option "Resolver una duda"
      - option "Explicación guiada" [selected]
      - option "Preguntas de práctica"
      - option "Preparar una exposición"
      - option "Revisar conceptos"
    - button "Cambiar modo de estudio" [disabled]
  - status: Estás interactuando con ORAL-IA, un sistema automático de apoyo docente. Puede cometer errores y no sustituye el criterio del profesorado.
  - log:
    - paragraph: ¿A qué temperatura hierve el agua?
    - paragraph: A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius. La temperatura de ebullición depende de la presión; mencionar la condición evita presentar el número como universal.
    - group:
      - text: Fuentes
      - list:
        - listitem: "bc4076f8-2895-49a9-b81a-0ac06a30d81a (v1) — ebullicion: Objetivo: Distinguir la ebullición bajo condiciones declaradas. A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius. La temperatura de ebullición depende de la presión; mencionar la condición evita presentar el número como universal. Ejemplo: Al calentar agua en una olla abierta se forman burbujas en el líquido cuando alcanza la ebullición en esas condiciones. Contraste: La ebullición forma vapor en el volumen del líquido; la evaporación sucede en su superficie."
    - paragraph: el agua puede pasar a ser vapor en algun momento?
    - paragraph: La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición.
    - group: Fuentes
    - paragraph: dimelo
    - paragraph: La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición.
    - group: Fuentes
    - paragraph: Repetir
    - paragraph: La evaporación es el paso de agua líquida a vapor desde la superficie. Puede producirse sin que todo el líquido alcance la ebullición.
    - group: Fuentes
    - paragraph: Explicación guiada
    - paragraph: Un paño húmedo puede secarse por evaporación sin hervir el agua que contiene.
    - group: Fuentes
    - paragraph: puedes repetir?
  - region "Elegir tema de estudio":
    - heading "¿Qué quieres estudiar?" [level=2]
    - paragraph: Elige un tema publicado para consultar su explicación o practicar. Primero se propone el tema; debes confirmar el cambio.
    - list:
      - listitem:
        - button "Elegir condensacion" [disabled]
      - listitem:
        - button "Elegir congelacion" [disabled]
      - listitem:
        - button "Elegir ebullicion" [disabled]
      - listitem:
        - button "Elegir evaporacion" [disabled]
      - listitem:
        - button "Elegir presion" [disabled]
  - text: Tu mensaje
  - textbox "Tu mensaje" [disabled]
  - button "Enviar" [disabled]
  - region "Privacidad de tu sesión":
    - heading "Privacidad de tu sesión" [level=2]
    - paragraph: Uso local seudónimo. La negativa no impide participar. Sin consentimiento se elimina contenido al cerrar; audio nunca se conserva.
    - paragraph: "Plazo: 1 días. Acceso docente solo a lo consentido."
    - group "Tu elección se enviará al responder o finalizar":
      - text: Tu elección se enviará al responder o finalizar
      - checkbox "Conservar transcripción de esta sesión"
      - text: Conservar transcripción de esta sesión
      - checkbox "Conservar resumen de esta sesión"
      - text: Conservar resumen de esta sesión
      - paragraph: Sin seleccionar, se elimina el contenido al cerrar. No es necesario conservar para participar.
    - button "Revisar registro completo"
  - button "Finalizar sesión" [disabled]
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
  15 |     if (mode === "oral_defense") await expect(page.locator(".system")).toContainText("condiciones");
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
> 63 |     await expect(page.getByRole("region", { name: "Envío sin confirmar" })).toBeVisible();
     |                                                                             ^ Error: expect(locator).toBeVisible() failed
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