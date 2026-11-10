# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_teacher_long_material.spec.ts >> docente: archivo04 original por UI, actividad, fuentes, cierre, revisión, exportación y borrado
- Location: ..\..\tests\e2e\test_teacher_long_material.spec.ts:6:5

# Error details

```
TimeoutError: page.waitForResponse: Timeout 15000ms exceeded while waiting for event "response"
```

# Page snapshot

```yaml
- generic [ref=f1e2]:
  - banner [ref=f1e3]:
    - navigation "Navegación general" [ref=f1e4]:
      - link "Volver al inicio" [ref=f1e5] [cursor=pointer]:
        - /url: /
  - main [ref=f1e6]:
    - heading "ORAL-IA — Área técnica" [level=1] [ref=f1e7]
    - navigation "Secciones del área técnica" [ref=f1e8]:
      - button "Catálogo" [ref=f1e9] [cursor=pointer]
      - button "Nueva actividad" [ref=f1e10] [cursor=pointer]
      - button "Sesiones" [ref=f1e11] [cursor=pointer]
      - button "Materiales" [ref=f1e12] [cursor=pointer]
    - region [ref=f1e13]:
      - heading "Materiales autorizados (FR-001, FR-011, FR-013)" [level=2] [ref=f1e14]
      - generic [ref=f1e15]:
        - generic [ref=f1e16]: Identificador de asignatura (course_id)
        - textbox "Identificador de asignatura (course_id)" [ref=f1e17]: e6a205c1-c01d-476f-9cce-d3f3ebf035d3
      - generic [ref=f1e18]:
        - generic [ref=f1e19]:
          - generic [ref=f1e20]: Documento (PDF, DOCX, PPTX, TXT o Markdown)
          - button "Documento (PDF, DOCX, PPTX, TXT o Markdown)" [ref=f1e21]
        - button "Cargar documento" [active] [ref=f1e22] [cursor=pointer]
      - heading "Documentos de la asignatura (0)" [level=3] [ref=f1e23]
      - list
      - heading "Conflictos pendientes de revisión (FR-022a)" [level=3] [ref=f1e24]
      - paragraph [ref=f1e25]: No hay conflictos pendientes.
      - list
```

# Test source

```ts
  1   | import { test, expect } from "@playwright/test";
  2   | import { readFile } from "node:fs/promises";
  3   | import { resolve } from "node:path";
  4   | import { randomUUID, createHash } from "node:crypto";
  5   | 
  6   | test("docente: archivo04 original por UI, actividad, fuentes, cierre, revisión, exportación y borrado", async ({
  7   |   page,
  8   | }) => {
  9   |   test.setTimeout(90_000);
  10  |   page.setDefaultTimeout(15_000);
  11  |   const suffix = randomUUID();
  12  |   const name = `Material largo ${suffix}`;
  13  |   const participant = `long-${suffix}`;
  14  |   const material = resolve(
  15  |     process.cwd(),
  16  |     "../../materiales/docente/04-caso-largo-incidencia.txt",
  17  |   );
  18  |   await page.goto("/gobierno");
  19  |   await page
  20  |     .getByLabel("Credencial local")
  21  |     .fill("fictional-e2e-installation-secret-005");
  22  |   await page.getByLabel("Credencial local").press("Enter");
  23  |   async function fillConfiguration(label: string) {
  24  |     await page.getByLabel("Nombre de actividad", { exact: true }).fill(label);
  25  |     await page.getByLabel("Materia", { exact: true }).fill("Agua");
  26  |     await page
  27  |       .getByRole("textbox", { name: "Objetivo", exact: true })
  28  |       .fill("Explicar el agua con material autorizado");
  29  |     await page.getByLabel("Modo y composición").selectOption("self_study");
  30  |     await page
  31  |       .getByLabel("Código seudónimo destinatario de la política")
  32  |       .fill(participant);
  33  |     await page.getByLabel("Permitir elección de conservación").check();
  34  |     await page
  35  |       .getByRole("button", { name: "Preparar política explícita para revisar" })
  36  |       .click();
  37  |     await page
  38  |       .getByLabel("He revisado los permisos de salida de esta versión")
  39  |       .check();
  40  |   }
  41  |   await page
  42  |     .getByLabel("Nombre de asignatura", { exact: true })
  43  |     .fill(`Agua larga ${suffix}`);
  44  |   await fillConfiguration(`Borrador ${suffix}`);
  45  |   const draftResponse = page.waitForResponse(
  46  |     (r) =>
  47  |       r.url().endsWith("/governance/activities") &&
  48  |       r.request().method() === "POST",
  49  |   );
  50  |   await page
  51  |     .getByRole("button", { name: "Guardar borrador", exact: true })
  52  |     .click();
  53  |   const draft = await (await draftResponse).json();
  54  |   await page.goto("/tecnica");
  55  |   await page.getByRole("button", { name: "Materiales", exact: true }).click();
  56  |   await page
  57  |     .getByLabel("Identificador de asignatura (course_id)", { exact: true })
  58  |     .fill(draft.course_id);
  59  |   await page
  60  |     .getByLabel("Documento (PDF, DOCX, PPTX, TXT o Markdown)")
  61  |     .setInputFiles(material);
> 62  |   const upload = page.waitForResponse(
      |                       ^ TimeoutError: page.waitForResponse: Timeout 15000ms exceeded while waiting for event "response"
  63  |     (r) =>
  64  |       r.url().endsWith("/materials/documents") &&
  65  |       r.request().method() === "POST",
  66  |   );
  67  |   await page
  68  |     .getByRole("button", { name: "Cargar documento", exact: true })
  69  |     .click();
  70  |   const uploaded = await (await upload).json();
  71  |   expect(uploaded.status).toBe("processed");
  72  |   expect(uploaded.content_hash).toBe(
  73  |     createHash("sha256")
  74  |       .update(await readFile(material))
  75  |       .digest("hex"),
  76  |   );
  77  |   const item = page
  78  |     .getByRole("listitem")
  79  |     .filter({ hasText: "04-caso-largo-incidencia.txt" });
  80  |   await item.getByRole("button", { name: "Activar", exact: true }).click();
  81  |   await expect(item).toContainText("active");
  82  |   await page.goto("/gobierno");
  83  |   await page
  84  |     .getByRole("combobox", { name: "Asignatura", exact: true })
  85  |     .selectOption(draft.course_id);
  86  |   await fillConfiguration(name);
  87  |   await page.getByLabel(/04-caso-largo-incidencia.txt v1/).check();
  88  |   const configured = page.waitForResponse(
  89  |     (r) =>
  90  |       r.url().endsWith("/governance/activities") &&
  91  |       r.request().method() === "POST",
  92  |   );
  93  |   await page
  94  |     .getByRole("button", { name: "Guardar borrador", exact: true })
  95  |     .click();
  96  |   const activity = await (await configured).json();
  97  |   expect(activity.material_versions).toEqual([
  98  |     { document_id: uploaded.id, version: 1 },
  99  |   ]);
  100 |   const article = page.getByRole("article", {
  101 |     name: `Actividad ${name} versión 1`,
  102 |     exact: true,
  103 |   });
  104 |   await article
  105 |     .getByRole("button", { name: "Activar versión", exact: true })
  106 |     .click();
  107 |   await expect(article).toContainText("active");
  108 |   await article
  109 |     .getByRole("link", { name: "Abrir actividad de autoestudio" })
  110 |     .click();
  111 |   await page
  112 |     .getByLabel("Código de participante (seudónimo)", { exact: true })
  113 |     .fill(participant);
  114 |   const opened = page.waitForResponse(
  115 |     (r) =>
  116 |       r.url().endsWith("/api/v1/sessions") && r.request().method() === "POST",
  117 |   );
  118 |   await page.getByRole("button", { name: "Iniciar", exact: false }).click();
  119 |   const session = await (await opened).json();
  120 |   await page
  121 |     .getByLabel("Conservar transcripción de esta sesión", { exact: true })
  122 |     .check();
  123 |   await page
  124 |     .getByLabel("Conservar resumen de esta sesión", { exact: true })
  125 |     .check();
  126 |   await page
  127 |     .getByLabel("Tu mensaje", { exact: true })
  128 |     .fill("¿A qué temperatura hierve el agua?");
  129 |   await page.getByRole("button", { name: "Enviar", exact: true }).click();
  130 |   await expect(page.locator(".system")).toContainText("100");
  131 |   await expect(page.getByLabel("Tu mensaje", { exact: true })).toBeEnabled();
  132 |   await page.getByText("Fuentes", { exact: true }).click();
  133 |   await expect(page.locator(".sources-panel")).toContainText("100");
  134 |   await page.screenshot({
  135 |     path: resolve(
  136 |       process.cwd(),
  137 |       "../../specs/009-long-extractive-binding/browser-long-material.png",
  138 |     ),
  139 |     fullPage: true,
  140 |   });
  141 |   await page.getByRole("button", { name: "Finalizar", exact: false }).click();
  142 |   await expect(page.getByRole("status").first()).toContainText("closed");
  143 |   await page.goto("/gobierno");
  144 |   await page
  145 |     .getByRole("button", {
  146 |       name: `Revisar sesión ${session.session_id}`,
  147 |       exact: true,
  148 |     })
  149 |     .click();
  150 |   await expect(
  151 |     page.getByRole("region", { name: "Revisión consentida" }),
  152 |   ).toContainText("100");
  153 |   await page
  154 |     .getByLabel(`Sesión ${session.session_id}`, { exact: false })
  155 |     .check();
  156 |   await page.getByLabel("Incluir texto libre autorizado").check();
  157 |   await page
  158 |     .getByLabel(
  159 |       "He revisado el texto libre de todas las sesiones seleccionadas",
  160 |     )
  161 |     .check();
  162 |   for (const format of ["JSON", "Markdown"]) {
```