import { execFileSync } from "node:child_process";
import { resolve } from "node:path";
import { test, expect } from "./local_auth";

for (const domain of ["agua", "programa"] as const) {
  test(`successor didactic explanations without visual controls: ${domain}`, async ({ page }, testInfo) => {
    test.setTimeout(120_000);
    const fixture = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", "self_study", "--domain", domain, "--screenless", "--pedagogy"], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
    await page.goto(`/autoestudio?activity=${fixture.activity_id}`);
    await page.getByLabel("Código de participante (seudónimo)", { exact: true }).fill("synthetic-010");
    const started = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
    await page.getByRole("button", { name: "Iniciar sesión", exact: true }).click();
    const session = await (await started).json();
    try {
      await page.addStyleTag({ content: '[aria-label="Capacidades de la actividad"], [aria-label="Controles de diálogo"], [aria-label="Elegir tema de estudio"], .sources-panel { display: none !important; }' });
      const endpoint = `/sessions/${session.session_id}/study-turns`;
      const messages = domain === "agua"
        ? ["hola", "dime que sabes sobre el agua?", "¿A qué temperatura hierve el agua?", "el agua puede pasar a ser vapor en algun momento?", "dimelo", "el agua puede pasar a ser vapor en algun momento?", "¿Cómo pasa el agua líquida a vapor?"]
        : ["hola", "¿Cómo valida el programa un registro?"];
      for (const text of messages) {
        await page.getByLabel("Tu mensaje", { exact: true }).fill(text);
        const pending = page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
        await page.getByRole("button", { name: "Enviar", exact: true }).click();
        const actual = await (await pending).json();
        if (text === "hola") expect(actual.output_text).toMatch(/^Hola\./);
        if (text.startsWith("¿Cómo")) {
          expect(actual.output_text).toContain("Primero");
          expect(actual.output_text).toContain("Después");
          expect(actual.output_text).toContain("Por último");
        }
      }
      await page.screenshot({ path: testInfo.outputPath("didactic-text-proof.png"), fullPage: true });
    } finally {
      await page.request.post(`/api/v1/governance/sessions/${session.session_id}/close`, { data: { confirm: true, reason: "abandoned" } });
    }
  });
}
