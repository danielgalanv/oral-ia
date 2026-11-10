# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_guided_orientation.spec.ts >> broad orientation offers actionable current topics: agua
- Location: ..\..\tests\e2e\test_guided_orientation.spec.ts:9:7

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: getByRole('region', { name: 'Elegir tema de estudio' })
Expected substring: "Elige un tema publicado"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toContainText" getByRole('region', { name: 'Elegir tema de estudio' }) with timeout 5000ms
  - waiting for getByRole('region', { name: 'Elegir tema de estudio' })

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
    - paragraph: "Proveedor efectivo observado: plantilla determinista autorizada."
    - paragraph: Las respuestas se componen desde unidades docentes publicadas. No es generación libre; la utilidad con personas sigue pendiente de validación.
    - paragraph: "Temas disponibles: condensacion, congelacion, ebullicion, evaporacion, presion. Para cambiar, escribe «cambiar de tema» y confirma el tema propuesto."
  - region "Controles de diálogo":
    - button "Repetir"
    - button "Otra forma"
    - button "Ayuda"
    - button "Continuar"
    - button "Otro tema"
    - text: Modo de estudio
    - combobox "Modo de estudio":
      - option "Elige un modo habilitado" [selected]
      - option "Resolver una duda"
      - option "Explicación guiada"
      - option "Preguntas de práctica"
      - option "Preparar una exposición"
      - option "Revisar conceptos"
    - button "Cambiar modo de estudio" [disabled]
  - status: Estás interactuando con ORAL-IA, un sistema automático de apoyo docente. Puede cometer errores y no sustituye el criterio del profesorado.
  - log:
    - paragraph: dime que sabes sobre el agua?
    - paragraph: Podemos trabajar los objetivos publicados de esta actividad. Elige un tema disponible o pide una pregunta de práctica.
  - text: Tu mensaje
  - textbox "Tu mensaje"
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
  - button "Finalizar sesión"
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
  17 |     const endpoint = `/sessions/${session.session_id}/study-turns`;
  18 |     const response = () => page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
  19 |     await page.getByLabel("Tu mensaje", { exact: true }).fill(broad);
  20 |     let pending = response();
  21 |     await page.getByRole("button", { name: "Enviar", exact: true }).click();
  22 |     const initial = await (await pending).json();
  23 |     expect(initial.dialogue_status.available_topics).toContain(topic);
  24 |     const guidance = page.getByRole("region", { name: "Elegir tema de estudio" });
> 25 |     await expect(guidance).toContainText("Elige un tema publicado");
     |                            ^ Error: expect(locator).toContainText(expected) failed
  26 |     await expect(guidance.getByRole("button")).toHaveCount(initial.dialogue_status.available_topics.length);
  27 |     pending = response();
  28 |     await guidance.getByRole("button", { name: `Elegir ${topic}`, exact: true }).focus();
  29 |     await page.keyboard.press("Enter");
  30 |     const proposed = await (await pending).json();
  31 |     expect(proposed.dialogue_status.pending_topic).toBe(topic);
  32 |     expect(proposed.dialogue_status.rendered_unit_ids).toHaveLength(0);
  33 |     pending = response();
  34 |     await guidance.getByRole("button", { name: `Confirmar tema ${topic}`, exact: true }).focus();
  35 |     await page.keyboard.press("Enter");
  36 |     const confirmed = await (await pending).json();
  37 |     expect(confirmed.dialogue_status.pending_topic).toBeNull();
  38 |     expect(confirmed.dialogue_status.rendered_unit_ids.length).toBeGreaterThan(0);
  39 |     expect(confirmed.dialogue_status.grounding_verdict).toBe("fundamentada");
  40 |     expect(confirmed.dialogue_status.coherence_verdict).toBe("approved");
  41 |     expect(confirmed.output_text.toLowerCase()).toContain(topic === "condensacion" ? "condensación" : topic);
  42 |     // A pending review question must survive selecting a different topic until confirmation.
  43 |     pending = response();
  44 |     await page.getByRole("region", { name: "Controles de diálogo" }).getByLabel("Modo de estudio").selectOption("concept_review");
  45 |     await page.getByRole("button", { name: "Cambiar modo de estudio", exact: true }).click();
  46 |     const question = (await (await pending).json()).dialogue_status.pending_question;
  47 |     expect(question?.text).toBeTruthy();
  48 |     pending = response();
  49 |     await guidance.getByRole("button", { name: `Elegir ${nextTopic}`, exact: true }).click();
  50 |     const waiting = await (await pending).json();
  51 |     expect(waiting.dialogue_status.pending_question).toEqual(question);
  52 |     expect(waiting.dialogue_status.pending_topic).toBe(nextTopic);
  53 |     await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toContainText(question.text);
  54 |     pending = response();
  55 |     await guidance.getByRole("button", { name: `Confirmar tema ${nextTopic}`, exact: true }).click();
  56 |     const changed = await (await pending).json();
  57 |     expect(changed.dialogue_status.pending_question.turn_id).not.toBe(question.turn_id);
  58 |     // Ephemeral closure clears the new surface as well as the conversation.
  59 |     await page.getByRole("button", { name: "Finalizar sesión", exact: true }).click();
  60 |     await expect(page.getByRole("status").filter({ hasText: "Sesión finalizada" })).toBeVisible();
  61 |     await expect(guidance).toHaveCount(0);
  62 |     await expect(page.locator(".system")).toHaveCount(0);
  63 |     expect((await page.request.get(`/api/v1/governance/sessions/${session.session_id}`)).status()).toBe(404);
  64 |   });
  65 | }
  66 | 
```