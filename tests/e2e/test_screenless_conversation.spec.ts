import { execFileSync } from "node:child_process";
import { resolve } from "node:path";
import { test, expect } from "./local_auth";

for (const mode of ["self_study", "oral_defense"] as const) {
  test(`screen-hidden transcript navigation, consent, review and erasure: ${mode}`, async ({ page }, testInfo) => {
    test.setTimeout(120_000);
    const fixture = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", mode, "--screenless"], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
    await page.goto(`${mode === "self_study" ? "/autoestudio" : "/defensa"}?activity=${fixture.activity_id}`);
    await page.getByLabel(mode === "self_study" ? "Código de participante (seudónimo)" : "Código seudónimo", { exact: true }).fill("synthetic-010");
    const started = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
    await page.getByRole("button", { name: mode === "self_study" ? "Iniciar sesión" : "Iniciar defensa", exact: true }).click();
    const session = await (await started).json();
    try {
      if (mode === "oral_defense") await expect(page.locator(".system")).toContainText("condiciones");
      // Hide every panel that previously supplied meaning absent from the dialogue.
      await page.addStyleTag({ content: '[aria-label="Capacidades de la actividad"], [aria-label="Controles de diálogo"], [aria-label="Elegir tema de estudio"], [aria-label="Privacidad de tu sesión"], .sources-panel, fieldset { display: none !important; }' });
      const endpoint = mode === "self_study" ? `/sessions/${session.session_id}/study-turns` : `/defense-sessions/${session.session_id}/defense-turns`;
      for (const text of ["hola", "qué temas hay", "elijo condensacion", "confirmo", "de dónde sale eso", "conservar resumen y transcripción", "confirmo conservar resumen y transcripción", "terminar la sesión", "confirmo cerrar"]) {
        await page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true }).fill(text);
        const response = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
        await page.getByRole("button", { name: "Enviar", exact: true }).click();
        const actual = await (await response).json();
        expect(actual.output_text).toBeTruthy();
        if (text === "hola") {
          expect(actual.output_text).toContain("condensacion");
          expect(actual.output_text).toContain("elijo");
          await page.screenshot({ path: testInfo.outputPath("spoken-options-text-proof.png"), fullPage: true });
        }
        if (text === "elijo condensacion") expect(actual.output_text).toContain("Se propone");
        if (text === "de dónde sale eso") expect(actual.output_text).toContain("sección");
        if (text === "conservar resumen y transcripción") expect(actual.output_text).toContain("confirmo conservar resumen y transcripción");
        if (text === "terminar la sesión") expect(actual.output_text).toContain("confirmo cerrar");
      }
      const closed = page.getByRole("region", { name: "Conversación del registro cerrado" });
      await expect(closed).toBeVisible();
      for (const text of ["revisar intervención uno", "eliminar mi contenido", "confirmo eliminar el contenido de esta sesión", "revisar intervención uno"]) {
        await closed.getByLabel("Mensaje conversacional de revisión", { exact: true }).fill(text);
        const response = page.waitForResponse(r => r.url().endsWith(`/sessions/${session.session_id}/conversation-controls`) && r.request().method() === "POST");
        await closed.getByRole("button", { name: "Enviar al registro", exact: true }).click();
        const actual = await (await response).json();
        if (text === "eliminar mi contenido") expect(actual.output_text).toContain("no se puede deshacer");
        if (actual.deleted) {
          await expect(page.locator(".system")).toHaveCount(0);
          await expect(closed).toContainText("Contenido eliminado");
        }
      }
      await expect(closed).toContainText("No hay una transcripción");
      expect((await page.request.get(`/api/v1/governance/sessions/${session.session_id}`)).status()).toBe(404);
    } finally {
      await page.request.post(`/api/v1/governance/sessions/${session.session_id}/close`, { data: { confirm: true, reason: "abandoned" } });
    }
  });
}
