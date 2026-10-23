import { defineConfig } from "@playwright/test";
import path from "node:path";
import { fileURLToPath } from "node:url";

/* E2E-тесты: Leptos-фронт (собранный в e2e/.dist) отдаёт backend-rs на базе в памяти, содержимое курса сидится из backend/app/data.
   Сборка: `npm run build` (trunk + cargo). Один рабочий процесс: тесты книг идут по одной главе за раз, лаборатории не конкурируют за CPU. */
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const port = Number(process.env.E2E_PORT ?? 8099);

export default defineConfig({
  testDir: "tests",
  timeout: 90_000,
  expect: { timeout: 10_000 },
  workers: 1,
  fullyParallel: false,
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    viewport: { width: 1400, height: 1000 },
    locale: "ru-RU",
  },
  projects: [{ name: "chromium", use: { browserName: "chromium" } }],
  webServer: {
    command: "./target/debug/say-backend",
    cwd: path.join(root, "backend-rs"),
    url: `http://127.0.0.1:${port}/api/books`,
    timeout: 180_000,
    reuseExistingServer: !process.env.CI,
    env: {
      BIND: `127.0.0.1:${port}`,
      SURREALDB_URL: "memory",
      STATIC_DIR: path.join(root, "e2e", ".dist"),
      SAY_WORKER_TOKEN: "e2e",
      DEMO_USER_EMAIL: "student@mail.com",
      DEMO_USER_PASSWORD: "student",
      DEMO_ADMIN_EMAIL: "programmer@mail.com",
      DEMO_ADMIN_PASSWORD: "programmer",
      RUST_LOG: "warn",
    },
  },
});
