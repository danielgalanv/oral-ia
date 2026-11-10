import type { FullConfig } from "@playwright/test";
import { createHash, randomUUID } from "node:crypto";
import { readdir, readFile, mkdir, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const historicalFeatures = [
  "006-architecture-validation",
  "007-local-demonstration",
  "008-demo-startup-progress",
  "009-long-extractive-binding",
  "010-guided-dialogue",
  "011-real-course-self-study",
];

async function snapshot(root: string): Promise<Record<string, string>> {
  const values: Record<string, string> = {};
  async function walk(directory: string, prefix: string) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = join(directory, entry.name);
      const key = `${prefix}/${entry.name}`;
      if (entry.isDirectory() && entry.name === "__pycache__") continue;
      if (entry.isDirectory()) await walk(path, key);
      else if (entry.isFile()) {
        values[key] = createHash("sha256").update(await readFile(path)).digest("hex");
      }
    }
  }
  for (const feature of historicalFeatures) await walk(join(root, feature), feature);
  return values;
}

export default async function preservationGuard(config: FullConfig) {
  const workspace = resolve(dirname(config.configFile), "../..");
  const specs = join(workspace, "specs");
  const before = await snapshot(specs);
  const output = join(workspace, ".claude-scratch", `e2e-preservation-${randomUUID()}.json`);
  return async () => {
    const after = await snapshot(specs);
    const changed = [...new Set([...Object.keys(before), ...Object.keys(after)])]
      .filter(key => before[key] !== after[key]).sort();
    await mkdir(dirname(output), { recursive: true });
    await writeFile(output, JSON.stringify({ checked_files: Object.keys(before).length, changed, before, after }, null, 2));
    if (changed.length) throw new Error(`La regresión modificó evidencia histórica: ${changed.join(", ")}. Informe: ${output}`);
  };
}
