import process from "node:process";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Local-only dev server (FR-022): never bind beyond 127.0.0.1.
export default defineConfig({
  plugins: [react()],
  cacheDir: process.env.ORALIA_DEMO_CACHE_DIR,
  envDir: process.env.ORALIA_DEMO_CONFIG_DIR,
  publicDir: process.env.ORALIA_DEMO_PUBLIC_DIR,
  server: {
    host: "127.0.0.1",
    port: Number(process.env.ORALIA_E2E_WEB_PORT ?? 5173),
    strictPort: true,
    proxy: {
      "/api": process.env.ORALIA_E2E_API_URL ?? "http://127.0.0.1:8000",
    },
  },
});
