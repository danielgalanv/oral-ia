import { execFileSync } from "node:child_process";
import { resolve } from "node:path";
import { test, expect } from "./local_auth";

for (const [domain, broad, topic, nextTopic] of [
  ["agua", "dime que sabes sobre el agua?", "condensacion", "evaporacion"],
  ["programa", "¿Qué hace el programa?", "entrada", "salida"],
]) {
  test(`broad orientation offers actionable current topics: ${domain}`, async ({ page }) => {
    test.setTimeout(120_000);
    const fixture = JSON.parse(execFileSync("uv", ["run", "--offline", "--no-sync", "python", "-X", "utf8", "tests/dialogue/prepare_api.py", "--mode", "self_study", "--domain", domain], { cwd: resolve(process.cwd(), "../.."), encoding: "utf8" }));
    await page.goto(`/autoestudio?activity=${fixture.activity_id}`);
    await page.getByLabel("Código de participante (seudónimo)", { exact: true }).fill("synthetic-010");
    const started = page.waitForResponse(r => r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST");
    await page.getByRole("button", { name: "Iniciar sesión", exact: true }).click();
    const session = await (await started).json();
    try {
      const endpoint = `/sessions/${session.session_id}/study-turns`;
      const response = () => page.waitForResponse(r => r.url().endsWith(endpoint) && r.request().method() === "POST");
      await page.getByLabel("Tu mensaje", { exact: true }).fill(broad);
      let pending = response();
      await page.getByRole("button", { name: "Enviar", exact: true }).click();
      const initial = await (await pending).json();
      expect(initial.dialogue_status.available_topics).toContain(topic);
      const guidance = page.getByRole("region", { name: "Elegir tema de estudio" });
      await expect(guidance).toContainText("Elige un tema publicado");
      await expect(guidance.getByRole("button")).toHaveCount(initial.dialogue_status.available_topics.length);
      pending = response();
      await guidance.getByRole("button", { name: `Elegir ${topic}`, exact: true }).focus();
      await page.keyboard.press("Enter");
      const proposed = await (await pending).json();
      expect(proposed.dialogue_status.pending_topic).toBe(topic);
      expect(proposed.dialogue_status.rendered_unit_ids).toHaveLength(0);
      pending = response();
      await guidance.getByRole("button", { name: `Confirmar tema ${topic}`, exact: true }).focus();
      await page.keyboard.press("Enter");
      const confirmed = await (await pending).json();
      expect(confirmed.dialogue_status.pending_topic).toBeNull();
      expect(confirmed.dialogue_status.rendered_unit_ids.length).toBeGreaterThan(0);
      expect(confirmed.dialogue_status.grounding_verdict).toBe("fundamentada");
      expect(confirmed.dialogue_status.coherence_verdict).toBe("approved");
      expect(confirmed.output_text.toLowerCase()).toContain(topic === "condensacion" ? "condensación" : topic);
      // A pending review question must survive selecting a different topic until confirmation.
      pending = response();
      await page.getByRole("region", { name: "Controles de diálogo" }).getByLabel("Modo de estudio").selectOption("concept_review");
      await page.getByRole("button", { name: "Cambiar modo de estudio", exact: true }).click();
      const question = (await (await pending).json()).dialogue_status.pending_question;
      expect(question?.text).toBeTruthy();
      pending = response();
      await guidance.getByRole("button", { name: `Elegir ${nextTopic}`, exact: true }).click();
      const waiting = await (await pending).json();
      expect(waiting.dialogue_status.pending_question).toEqual(question);
      expect(waiting.dialogue_status.pending_topic).toBe(nextTopic);
      await expect(page.getByRole("region", { name: "Pregunta pendiente" })).toContainText(question.text);
      pending = response();
      await guidance.getByRole("button", { name: `Confirmar tema ${nextTopic}`, exact: true }).click();
      const changed = await (await pending).json();
      expect(changed.dialogue_status.pending_question.turn_id).not.toBe(question.turn_id);
      // Ephemeral closure clears the new surface as well as the conversation.
      await page.getByRole("button", { name: "Finalizar sesión", exact: true }).click();
      await expect(page.getByRole("status").filter({ hasText: "Sesión finalizada" })).toBeVisible();
      await expect(guidance).toHaveCount(0);
      await expect(page.locator(".system")).toHaveCount(0);
      expect((await page.request.get(`/api/v1/governance/sessions/${session.session_id}`)).status()).toBe(404);
    } finally {
      // Only this test's session, through the real authenticated closure route.
      await page.request.post(`/api/v1/governance/sessions/${session.session_id}/close`, { data: { confirm: true, reason: "abandoned" } });
    }
  });
}
