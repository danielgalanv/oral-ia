import { execFileSync } from "node:child_process";
import { resolve } from "node:path";
import { test, expect } from "./local_auth";

for (const mode of ["self_study", "oral_defense"] as const) {
  test(`guided actual provider, owner resume and confirmed close: ${mode}`, async ({ page }) => {
    test.setTimeout(120_000);
    const prepared = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", mode], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
    await page.goto(`${mode === "self_study" ? "/autoestudio" : "/defensa"}?activity=${prepared.activity_id}`);
    await expect(page.getByRole("region", { name: "Capacidades de la actividad" })).toContainText("contenido docente revisado");
    await page.getByLabel(mode === "self_study" ? "Código de participante (seudónimo)" : "Código seudónimo", { exact: true }).fill("synthetic-010");
    const started = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
    await page.getByRole("button", { name: mode === "self_study" ? "Iniciar sesión" : "Iniciar defensa", exact: true }).click();
    const session = await (await started).json();
    try {
      if (mode === "oral_defense") await expect(page.locator(".system")).toContainText("condiciones");
      const initialQuestion = mode === "oral_defense" ? await page.locator(".system p").first().innerText() : null;
      const endpoint = mode === "self_study" ? `/sessions/${session.session_id}/study-turns` : `/defense-sessions/${session.session_id}/defense-turns`;
      for (const text of mode === "self_study" ? ["¿A qué temperatura hierve el agua?", "el agua puede pasar a ser vapor en algun momento?", "dimelo"] : ["a los 99 grados", "no sé justificarlo", "puedes repetir?", "no entiendo, dilo de otra forma"]) {
        await page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true }).fill(text);
        const response = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
        await page.getByRole("button", { name: "Enviar", exact: true }).click();
        const actual = await (await response).json();
        expect(actual.output_text).toBeTruthy();
        expect(actual.dialogue_status.provider).toBe("reviewed-unit-renderer/v1");
        expect(actual.dialogue_status.rendered_unit_ids.length).toBeGreaterThan(0);
        if (mode === "oral_defense") {
          expect(actual.output_text).not.toContain("100");
          expect(actual.sources.every((source: { fragment_text: string }) => !source.fragment_text)).toBe(true);
        }
      }
      const controls = page.getByRole("region", { name: "Controles de diálogo" });
      const repeatedByButton = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
      await controls.getByRole("button", { name: "Repetir", exact: true }).focus();
      await page.keyboard.press("Enter");
      const buttonResult = await (await repeatedByButton).json();
      expect(buttonResult.dialogue_status.primary_act).toBe("repeat");
      if (initialQuestion) {
        expect(buttonResult.output_text).toBe(initialQuestion);
        await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toContainText(initialQuestion);
      } else {
        const sourcePanel = page.locator(".sources-panel").first();
        await sourcePanel.locator("summary").focus();
        await page.keyboard.press("Enter");
        await expect(sourcePanel).toHaveAttribute("open", "");
        await controls.getByLabel("Modo de estudio", { exact: true }).selectOption("guided_explanation");
        const modeChanged = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
        await controls.getByRole("button", { name: "Cambiar modo de estudio", exact: true }).focus();
        await page.keyboard.press("Enter");
        expect((await (await modeChanged).json()).mode).toBe("guided_explanation");
      }
      // Synthetic loss of transport AFTER the actual API commits. No favorable
      // response is substituted: reconciliation must find that exact real turn.
      const before = await (await page.request.get("/api/v1/governance/active-session")).json();
      let committedTurnId: string | undefined;
      let onInjectedLoss: (() => void) | null = null;
      const injectedLoss = new Promise<void>(complete => { onInjectedLoss = complete; });
      await page.route(`**/api/v1${endpoint}`, async route => {
        const actual = await route.fetch();
        expect(actual.status()).toBe(200);
        committedTurnId = (await actual.json()).turn_id;
        await route.abort("failed");
        onInjectedLoss?.();
      }, { times: 1 });
      await page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true }).fill("puedes repetir?");
      await page.getByRole("button", { name: "Enviar", exact: true }).click();
      // Wait for the real commit and injected transport failure before checking UI.
      // This does not replace the API response or extend the application's deadline.
      await injectedLoss;
      await expect(page.getByRole("region", { name: "Envío sin confirmar" })).toBeVisible();
      await expect(page.getByRole("button", { name: "Enviar", exact: true })).toBeDisabled();
      const reconciled = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
      await page.getByRole("button", { name: "Consultar resultado del envío", exact: true }).click();
      const projected = await (await reconciled).json();
      expect(projected.turn_id).toBe(committedTurnId);
      expect(projected.request_replayed).toBe(true);
      await expect(page.getByRole("region", { name: "Envío sin confirmar" })).toHaveCount(0);
      const after = await (await page.request.get("/api/v1/governance/active-session")).json();
      expect(after.session.turn_count).toBe(before.session.turn_count + 1);
      await page.reload();
      await page.getByRole("button", { name: "Buscar mi sesión activa", exact: true }).click();
      await page.getByRole("button", { name: "Retomar mi sesión", exact: true }).click();
      await expect(page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true })).toBeVisible();
      await page.goto("/gobierno");
      await page.getByRole("button", { name: "Comprobar sesión activa", exact: true }).click();
      const close = page.getByRole("button", { name: "Cerrar sesión activa con confirmación", exact: true });
      await expect(close).toBeDisabled();
      await page.getByLabel("He revisado la sesión y confirmo el cierre docente", { exact: true }).check();
      await close.click();
      await expect(page.getByRole("region", { name: "Gestión de sesión activa" })).toContainText("Cierre docente confirmado");
      const state = await page.request.get(`/api/v1/governance/active-session`);
      expect((await state.json()).session).toBeNull();
    } finally {
      if (session.session_id) {
        await page.request.post(`/api/v1/governance/sessions/${session.session_id}/close`, {
          data: { confirm: true, reason: "abandoned" },
        }).catch(() => {});
      }
    }
  });
}
