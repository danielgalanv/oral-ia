import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { test, expect } from "./local_auth";

for (const mode of ["self_study", "oral_defense"] as const) {
  for (const retain of [false, true]) {
    test(`guided consent, browser caches, export and deletion: ${mode}, retain=${retain}`, async ({ page }) => {
      test.setTimeout(120_000);
      const fixture = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", mode], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
      await page.goto(`${mode === "self_study" ? "/autoestudio" : "/defensa"}?activity=${fixture.activity_id}`);
      await page.getByLabel(mode === "self_study" ? "Código de participante (seudónimo)" : "Código seudónimo", { exact: true }).fill("synthetic-010");
      const started = page.waitForResponse(response => response.url().endsWith("/api/v1/sessions") && response.request().method() === "POST");
      await page.getByRole("button", { name: mode === "self_study" ? "Iniciar sesión" : "Iniciar defensa", exact: true }).click();
      const session = await (await started).json();
      if (mode === "oral_defense") await expect(page.locator(".system")).toContainText("condiciones");
      if (retain) {
        await page.getByLabel(mode === "self_study" ? "Conservar transcripción de esta sesión" : "Conservar transcripción", { exact: true }).check();
        await page.getByLabel(mode === "self_study" ? "Conservar resumen de esta sesión" : "Conservar resumen", { exact: true }).check();
      }
      const turnPath = mode === "self_study" ? `/sessions/${session.session_id}/study-turns` : `/defense-sessions/${session.session_id}/defense-turns`;
      await page.getByLabel(mode === "self_study" ? "Tu mensaje" : "Tu respuesta", { exact: true }).fill(mode === "self_study" ? "¿A qué temperatura hierve el agua?" : "no sé justificarlo");
      const turn = page.waitForResponse(response => response.url().endsWith(turnPath) && response.request().method() === "POST");
      await page.getByRole("button", { name: "Enviar", exact: true }).click();
      const actual = await (await turn).json();
      expect(actual.dialogue_status.rendered_unit_ids.length).toBeGreaterThan(0);
      if (mode === "oral_defense") expect(actual.output_text).not.toContain("100 grados");
      if (!retain) {
        // A resumed question is also browser state and must disappear on erasure.
        await page.reload();
        await page.getByRole("button", { name: "Buscar mi sesión activa", exact: true }).click();
        await page.getByRole("button", { name: "Retomar mi sesión", exact: true }).click();
        if (mode === "oral_defense") await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toBeVisible();
      }
      const endPath = mode === "self_study" ? `/sessions/${session.session_id}/study-end` : `/defense-sessions/${session.session_id}/defense-end`;
      const final = page.getByRole("button", { name: "Finalizar sesión", exact: true });
      await expect(final).toBeEnabled();
      if (mode === "oral_defense") {
        await final.click();
        await expect(page.getByRole("region", { name: "Transcripción completa de la sesión" })).toBeVisible();
      }
      const closed = page.waitForResponse(response => response.url().endsWith(endPath) && response.request().method() === "POST");
      await page.getByRole("button", { name: mode === "self_study" ? "Finalizar sesión" : "Confirmar cierre de sesión", exact: true }).click();
      expect((await (await closed).json()).status).toBe("closed_voluntary");
      await expect(page.getByRole("status").filter({ hasText: "Sesión finalizada" })).toBeVisible();
      if (!retain) {
        await expect(page.locator(".system")).toHaveCount(0);
        await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toHaveCount(0);
        await expect(page.getByRole("region", { name: "Transcripción completa de la sesión" })).toHaveCount(0);
        expect((await page.request.get(`/api/v1/governance/sessions/${session.session_id}`)).status()).toBe(404);
        expect((await page.request.post("/api/v1/governance/exports", { data: { session_ids: [session.session_id] } })).status()).toBe(409);
        return;
      }
      await page.goto("/gobierno");
      await page.getByRole("button", { name: `Revisar sesión ${session.session_id}`, exact: true }).click();
      const review = page.getByRole("region", { name: "Revisión consentida" });
      await expect(review).toContainText(actual.output_text);
      if (mode === "oral_defense") await expect(review).not.toContainText("100 grados");
      await page.getByLabel(`Sesión ${session.session_id}`, { exact: false }).check();
      await page.getByLabel("Incluir texto libre autorizado").check();
      await page.getByLabel("He revisado el texto libre de todas las sesiones seleccionadas").check();
      for (const format of ["JSON", "Markdown"]) {
        const pending = page.waitForEvent("download");
        await page.getByRole("button", { name: `Exportar ${format}`, exact: true }).click();
        const downloaded = await pending;
        const body = await readFile((await downloaded.path())!, "utf8");
        expect(body).not.toContain("synthetic-010");
        expect(body).not.toContain("dialogue_context");
        expect(body).not.toContain("client_request_id");
        if (mode === "oral_defense") expect(body).not.toContain("100 grados");
      }
      await page.getByLabel("Confirmo eliminar el contenido de esta sesión", { exact: true }).check();
      await page.getByRole("button", { name: "Eliminar sesión revisada", exact: true }).click();
      await expect(page.getByRole("status").filter({ hasText: "Eliminación confirmada" })).toBeVisible();
      expect((await page.request.get(`/api/v1/governance/sessions/${session.session_id}`)).status()).toBe(404);
      expect((await page.request.post("/api/v1/governance/exports", { data: { session_ids: [session.session_id] } })).status()).toBe(409);
    });
  }
}
