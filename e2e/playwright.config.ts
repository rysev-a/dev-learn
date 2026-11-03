import { defineConfig } from "@playwright/test";
import path from "node:path";
import { fileURLToPath } from "node:url";

/* E2E tests: the Leptos frontend (built into e2e/.dist) is served by the backend on an in-memory database; course content is seeded from backend/data.
   Build: `npm run build` (trunk + cargo). A single worker process: book tests run one chapter at a time, labs do not compete for CPU. */
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const port = Number(process.env.E2E_PORT ?? 8099);
/** A ready-made stack (e.g. `docker compose … up`): tests run against it, no own server is started. */
const external = process.env.E2E_BASE_URL;

export default defineConfig({
  testDir: "tests",
  timeout: 90_000,
  expect: { timeout: 10_000 },
  workers: 1,
  fullyParallel: false,
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: external ?? `http://127.0.0.1:${port}`,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    viewport: { width: 1400, height: 1000 },
    locale: "ru-RU",
  },
  projects: [{ name: "chromium", use: { browserName: "chromium" } }],
  webServer: external
    ? undefined
    : {
    command: "./target/debug/cs-core-backend",
    cwd: path.join(root, "backend"),
    url: `http://127.0.0.1:${port}/api/books`,
    timeout: 180_000,
    reuseExistingServer: !process.env.CI,
    env: {
      BIND: `127.0.0.1:${port}`,
      SURREALDB_URL: "memory",
      STATIC_DIR: path.join(root, "e2e", ".dist"),
      CS_CORE_WORKER_TOKEN: "e2e",
      DEMO_USER_EMAIL: "student@mail.com",
      DEMO_USER_PASSWORD: "student",
      DEMO_ADMIN_EMAIL: "programmer@mail.com",
      DEMO_ADMIN_PASSWORD: "programmer",
      RECORDS_DIR: path.join(root, "e2e", ".records"),
      RUST_LOG: "warn",
    },
  },
});
