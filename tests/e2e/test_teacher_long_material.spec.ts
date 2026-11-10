import { test, expect } from "@playwright/test";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { randomUUID, createHash } from "node:crypto";

for (const scenario of ["normal", "slow", "error"] as const) {
  test(`docente: archivo04 original por UI, actividad, fuentes, cierre, revisión, exportación y borrado [${scenario}]`, async ({ page }, testInfo) => {
    test.setTimeout(120_000);
    page.setDefaultTimeout(15_000);
    const suffix = randomUUID();
    const name = `Material largo ${suffix}`;
    const participant = `long-${suffix}`;
    const material = resolve(
      process.cwd(),
      "../../materiales/docente/04-caso-largo-incidencia.txt",
    );
    await page.goto("/gobierno");
    await page
      .getByLabel("Credencial local")
      .fill("fictional-e2e-installation-secret-005");
    await page.getByLabel("Credencial local").press("Enter");
    async function fillConfiguration(label: string) {
      await page.getByLabel("Nombre de actividad", { exact: true }).fill(label);
      await page.getByLabel("Materia", { exact: true }).fill("Agua");
      await page
        .getByRole("textbox", { name: "Objetivo", exact: true })
        .fill("Explicar el agua con material autorizado");
      await page.getByLabel("Modo y composición").selectOption("self_study");
      await page
        .getByLabel("Código seudónimo destinatario de la política")
        .fill(participant);
      await page.getByLabel("Permitir elección de conservación").check();
      await page
        .getByRole("button", {
          name: "Preparar política explícita para revisar",
        })
        .click();
      await page
        .getByLabel("He revisado los permisos de salida de esta versión")
        .check();
    }
    await page
      .getByLabel("Nombre de asignatura", { exact: true })
      .fill(`Agua larga ${suffix}`);
    await fillConfiguration(`Borrador ${suffix}`);
    const draftResponse = page.waitForResponse(
      (r) =>
        r.url().endsWith("/governance/activities") &&
        r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "Guardar borrador", exact: true })
      .click();
    const draft = await (await draftResponse).json();
    await page.goto("/tecnica");
    await page.getByRole("button", { name: "Materiales", exact: true }).click();
    await page
      .getByLabel("Identificador de asignatura (course_id)", { exact: true })
      .fill(draft.course_id);
    await page
      .getByLabel("Documento (PDF, DOCX, PPTX, TXT o Markdown)")
      .setInputFiles(
        scenario === "error"
          ? {
              name: "invalid.exe",
              mimeType: "application/octet-stream",
              buffer: Buffer.from("fictitious unsupported file"),
            }
          : material,
      );
    const uploadStarted = Date.now();
    const controlledDelayMs = scenario === "slow" ? 16_000 : 0;
    if (scenario === "slow") {
      await page.setExtraHTTPHeaders({ "x-oralia-e2e-delivery": "slow" });
    }
    let uploadRequests = 0;
    let uploadRequestAt: number | null = null;
    page.on("request", (request) => {
      if (
        request.url().endsWith("/materials/documents") &&
        request.method() === "POST"
      ) {
        uploadRequestAt = Date.now();
        uploadRequests += 1;
      }
    });
    const upload = page.waitForResponse(
      (r) =>
        r.url().endsWith("/materials/documents") &&
        r.request().method() === "POST",
      { timeout: 60_000 },
    );
    await page
      .getByRole("button", { name: "Cargar documento", exact: true })
      .click();
    if (scenario === "slow") {
      const form = page.getByRole("form", { name: "Carga de documento" });
      await expect(form).toHaveAttribute("aria-busy", "true");
      await expect(page.getByRole("status")).toContainText("Carga en curso");
      await expect(
        page.getByRole("button", { name: "Cargar documento", exact: true }),
      ).toBeDisabled();
      await expect(
        page.getByLabel("Identificador de asignatura (course_id)", {
          exact: true,
        }),
      ).toBeDisabled();
      await expect(
        page.getByLabel("Documento (PDF, DOCX, PPTX, TXT o Markdown)"),
      ).toBeDisabled();
      await form.evaluate((element) => {
        const form = element as HTMLFormElement;
        form.requestSubmit();
        form.requestSubmit();
      });
      await page.screenshot({
        path: testInfo.outputPath("busy-real-response.png"),
        fullPage: true,
      });
    }
    const response = await upload;
    const headersAt = Date.now();
    const uploaded = await response.json();
    await writeFile(
      testInfo.outputPath(`upload-${scenario}.json`),
      JSON.stringify(
        {
          scenario,
          uploadRequests,
          controlled_delivery_delay_ms: controlledDelayMs,
          actual_ingestion_ms:
            response.headers()["x-oralia-e2e-ingest-ms"] ?? null,
          harness_delivery_delay_ms:
            response.headers()["x-oralia-e2e-delay-ms"] ?? null,
          response_status: response.status(),
          status: uploaded.status,
          content_hash: uploaded.content_hash,
          request_after_ms:
            uploadRequestAt === null ? null : uploadRequestAt - uploadStarted,
          headers_after_ms: headersAt - uploadStarted,
          body_after_ms: Date.now() - uploadStarted,
          timing_basis:
            "real HTTP in isolated API process; model cache prepared; cold/warm not inferred",
        },
        null,
        2,
      ),
    );
    expect(uploadRequests).toBe(1);
    if (scenario === "slow") {
      expect(response.headers()["x-oralia-e2e-delay-ms"]).toBe("16000");
      expect(headersAt - uploadStarted).toBeGreaterThanOrEqual(16_000);
    }
    if (scenario === "error") {
      expect(response.status()).toBe(422);
      await expect(page.getByRole("alert")).toContainText(
        "No se pudo cargar el documento",
      );
      await expect(
        page.getByRole("form", { name: "Carga de documento" }),
      ).toHaveAttribute("aria-busy", "false");
      await expect(
        page.getByRole("button", { name: "Cargar documento", exact: true }),
      ).toBeEnabled();
      await expect(page.getByRole("status")).toHaveCount(0);
      return;
    }
    expect(response.status()).toBe(201);
    expect(uploaded.status).toBe("processed");
    expect(uploaded.content_hash).toBe(
      createHash("sha256")
        .update(await readFile(material))
        .digest("hex"),
    );
    const item = page
      .getByRole("listitem")
      .filter({ hasText: "04-caso-largo-incidencia.txt" });
    await item.getByRole("button", { name: "Activar", exact: true }).click();
    await expect(item).toContainText("active");
    await page.goto("/gobierno");
    await page
      .getByRole("combobox", { name: "Asignatura", exact: true })
      .selectOption(draft.course_id);
    await fillConfiguration(name);
    await page.getByLabel(/04-caso-largo-incidencia.txt v1/).check();
    const configured = page.waitForResponse(
      (r) =>
        r.url().endsWith("/governance/activities") &&
        r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "Guardar borrador", exact: true })
      .click();
    const activity = await (await configured).json();
    expect(activity.material_versions).toEqual([
      { document_id: uploaded.id, version: 1 },
    ]);
    const article = page.getByRole("article", {
      name: `Actividad ${name} versión 1`,
      exact: true,
    });
    await article
      .getByRole("button", { name: "Activar versión", exact: true })
      .click();
    await expect(article).toContainText("active");
    await article
      .getByRole("link", { name: "Abrir actividad de autoestudio" })
      .click();
    await page
      .getByLabel("Código de participante (seudónimo)", { exact: true })
      .fill(participant);
    const opened = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "Iniciar", exact: false }).click();
    const session = await (await opened).json();
    await page
      .getByLabel("Conservar transcripción de esta sesión", { exact: true })
      .check();
    await page
      .getByLabel("Conservar resumen de esta sesión", { exact: true })
      .check();
    await page
      .getByLabel("Tu mensaje", { exact: true })
      .fill("¿A qué temperatura hierve el agua?");
    await page.getByRole("button", { name: "Enviar", exact: true }).click();
    await expect(page.locator(".system")).toContainText("100");
    await expect(page.getByLabel("Tu mensaje", { exact: true })).toBeEnabled();
    await page.getByText("Fuentes", { exact: true }).click();
    await expect(page.locator(".sources-panel")).toContainText("100");
    await page.screenshot({
      path: testInfo.outputPath(scenario === "slow" ? "browser-long-slow.png" : "browser-long-material.png"),
      fullPage: true,
    });
    await page.getByRole("button", { name: "Finalizar", exact: false }).click();
    await expect(page.getByRole("status").first()).toContainText("closed");
    await page.goto("/gobierno");
    await page
      .getByRole("button", {
        name: `Revisar sesión ${session.session_id}`,
        exact: true,
      })
      .click();
    await expect(
      page.getByRole("region", { name: "Revisión consentida" }),
    ).toContainText("100");
    await page
      .getByLabel(`Sesión ${session.session_id}`, { exact: false })
      .check();
    await page.getByLabel("Incluir texto libre autorizado").check();
    await page
      .getByLabel(
        "He revisado el texto libre de todas las sesiones seleccionadas",
      )
      .check();
    for (const format of ["JSON", "Markdown"]) {
      const pending = page.waitForEvent("download");
      await page
        .getByRole("button", { name: `Exportar ${format}`, exact: true })
        .click();
      const text = await readFile((await (await pending).path())!, "utf8");
      expect(text).toContain("100");
      expect(text).not.toContain(participant);
    }
    await page
      .getByLabel("Confirmo eliminar el contenido de esta sesión", {
        exact: true,
      })
      .check();
    await page
      .getByRole("button", { name: "Eliminar sesión revisada" })
      .click();
    await expect(page.getByRole("status")).toContainText(
      "Eliminación confirmada",
    );
    expect(
      (
        await page.request.get(
          `/api/v1/governance/sessions/${session.session_id}`,
        )
      ).status(),
    ).toBe(404);
    expect(
      (
        await page.request.post("/api/v1/governance/exports", {
          data: { session_ids: [session.session_id] },
        })
      ).status(),
    ).toBe(409);
  });
}
