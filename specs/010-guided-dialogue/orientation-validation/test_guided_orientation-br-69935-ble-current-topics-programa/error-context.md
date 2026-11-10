# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_guided_orientation.spec.ts >> broad orientation offers actionable current topics: programa
- Location: ..\..\tests\e2e\test_guided_orientation.spec.ts:9:7

# Error details

```
Test timeout of 120000ms exceeded.
```

```
Error: locator.fill: Test timeout of 120000ms exceeded.
Call log:
  - waiting for getByLabel('Tu mensaje', { exact: true })

```

# Page snapshot

```yaml
- generic [ref=e2]:
  - banner [ref=e3]:
    - navigation "Navegación general" [ref=e4]:
      - link "Volver al inicio" [ref=e5] [cursor=pointer]:
        - /url: /
  - main [ref=e6]:
    - heading "ORAL-IA — Autoestudio" [level=1] [ref=e7]
    - region "Recuperación de sesión" [ref=e8]:
      - button "Buscar mi sesión activa" [ref=e9] [cursor=pointer]
    - region "Capacidades de la actividad" [ref=e10]:
      - paragraph [ref=e11]: "Perfil: diálogo guiado con contenido docente revisado."
      - paragraph [ref=e12]: "Proveedor efectivo observado: compositor de unidades docentes v1."
      - paragraph [ref=e13]: Las respuestas se componen desde unidades docentes publicadas. No es generación libre; la utilidad con personas sigue pendiente de validación.
    - alert [ref=e14]: "No se pudo iniciar la sesión: Ya hay una sesión activa. Si conservas su acceso, retómala; si lo perdiste, solicita un cierre docente confirmado."
    - generic [ref=e15]:
      - generic [ref=e16]:
        - generic [ref=e17]: Código de participante (seudónimo)
        - textbox "Código de participante (seudónimo)" [ref=e18]: synthetic-010
        - paragraph [ref=e19]: No use su nombre real ni datos personales.
      - generic [ref=e20]:
        - generic [ref=e21]: Identificador de actividad
        - textbox "Identificador de actividad" [ref=e22]: 1587caad-30cb-458b-b04f-fa02ab91cb58
      - button "Iniciar sesión" [active] [ref=e23] [cursor=pointer]
```

# Test source

```ts
  1  | import { execFileSync } from "node:child_process";
  2  | import { resolve } from "node:path";
  3  | import { test, expect } from "./local_auth";
  4  | 
  5  | for (const [domain, broad, topic, nextTopic] of [
  6  |   ["agua", "dime que sabes sobre el agua?", "condensacion", "evaporacion"],
  7  |   ["programa", "¿Qué hace el programa?", "entrada", "salida"],
  8  | ]) {
  9  |   test(`broad orientation offers actionable current topics: ${domain}`, async ({ page }) => {
  10 |     test.setTimeout(120_000);
  11 |     const fixture = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", "self_study", "--domain", domain], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
  12 |     await page.goto(`/autoestudio?activity=${fixture.activity_id}`);
  13 |     await page.getByLabel("Código de participante (seudónimo)", { exact: true }).fill("synthetic-010");
  14 |     const started = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
  15 |     await page.getByRole("button", { name: "Iniciar sesión", exact: true }).click();
  16 |     const session = await (await started).json();
  17 |     try {
  18 |       const endpoint = `/sessions/${session.session_id}/study-turns`;
> 19 |       const response = () => page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
     |                                                          ^ Error: locator.fill: Test timeout of 120000ms exceeded.
  20 |       await page.getByLabel("Tu mensaje", { exact: true }).fill(broad);
  21 |       let pending = response();
  22 |       await page.getByRole("button", { name: "Enviar", exact: true }).click();
  23 |       const initial = await (await pending).json();
  24 |       expect(initial.dialogue_status.available_topics).toContain(topic);
  25 |       const guidance = page.getByRole("region", { name: "Elegir tema de estudio" });
  26 |       await expect(guidance).toContainText("Elige un tema publicado");
  27 |       await expect(guidance.getByRole("button")).toHaveCount(initial.dialogue_status.available_topics.length);
  28 |       pending = response();
  29 |       await guidance.getByRole("button", { name: `Elegir ${topic}`, exact: true }).focus();
  30 |       await page.keyboard.press("Enter");
  31 |       const proposed = await (await pending).json();
  32 |       expect(proposed.dialogue_status.pending_topic).toBe(topic);
  33 |       expect(proposed.dialogue_status.rendered_unit_ids).toHaveLength(0);
  34 |       pending = response();
  35 |       await guidance.getByRole("button", { name: `Confirmar tema ${topic}`, exact: true }).focus();
  36 |       await page.keyboard.press("Enter");
  37 |       const confirmed = await (await pending).json();
  38 |       expect(confirmed.dialogue_status.pending_topic).toBeNull();
  39 |       expect(confirmed.dialogue_status.rendered_unit_ids.length).toBeGreaterThan(0);
  40 |       expect(confirmed.dialogue_status.grounding_verdict).toBe("fundamentada");
  41 |       expect(confirmed.dialogue_status.coherence_verdict).toBe("approved");
  42 |       expect(confirmed.output_text.toLowerCase()).toContain(topic === "condensacion" ? "condensación" : topic);
  43 |       // A pending review question must survive selecting a different topic until confirmation.
  44 |       pending = response();
  45 |       await page.getByRole("region", { name: "Controles de diálogo" }).getByLabel("Modo de estudio").selectOption("concept_review");
  46 |       await page.getByRole("button", { name: "Cambiar modo de estudio", exact: true }).click();
  47 |       const question = (await (await pending).json()).dialogue_status.pending_question;
  48 |       expect(question?.text).toBeTruthy();
  49 |       pending = response();
  50 |       await guidance.getByRole("button", { name: `Elegir ${nextTopic}`, exact: true }).click();
  51 |       const waiting = await (await pending).json();
  52 |       expect(waiting.dialogue_status.pending_question).toEqual(question);
  53 |       expect(waiting.dialogue_status.pending_topic).toBe(nextTopic);
  54 |       await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toContainText(question.text);
  55 |       pending = response();
  56 |       await guidance.getByRole("button", { name: `Confirmar tema ${nextTopic}`, exact: true }).click();
  57 |       const changed = await (await pending).json();
  58 |       expect(changed.dialogue_status.pending_question.turn_id).not.toBe(question.turn_id);
  59 |       // Ephemeral closure clears the new surface as well as the conversation.
  60 |       await page.getByRole("button", { name: "Finalizar sesión", exact: true }).click();
  61 |       await expect(page.getByRole("status").filter({ hasText: "Sesión finalizada" })).toBeVisible();
  62 |       await expect(guidance).toHaveCount(0);
  63 |       await expect(page.locator(".system")).toHaveCount(0);
  64 |       expect((await page.request.get(`/api/v1/governance/sessions/${session.session_id}`)).status()).toBe(404);
  65 |     } finally {
  66 |       // Only this test's session, through the real authenticated closure route.
  67 |       await page.request.post(`/api/v1/governance/sessions/${session.session_id}/close`, { data: { confirm: true, reason: "abandoned" } });
  68 |     }
  69 |   });
  70 | }
  71 | 
```