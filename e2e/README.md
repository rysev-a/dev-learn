# E2E tests (Playwright, TypeScript)

They test the Leptos frontend (`frontend`) together with the `backend` (in-memory database, the course is seeded from `backend/data`). Order: build → run.

```bash
cd e2e && npm install && npx playwright install chromium   # once
npm run build                                              # trunk build → e2e/.dist and cargo build of the backend
npm test                                                   # everything; one chapter of one book at a time (workers = 1)
npx playwright test tests/books/dm.spec.ts                 # one book
E2E_PORT=8102 npx playwright test tests/labs                # your own port: several runs do not interfere with each other
```

- Tests do not share progress: each one takes a new user (`loginFresh`) and seeds the state it needs through the API.
- The browser console is guarded (`guard.assertClean()`): a Rust panic or `console.error` is a failure.
- Tests read the course content (books, chapters, exercises, lab references) from `backend/data` rather than duplicating it.

## Contents

| Directory | What it tests |
|---|---|
| `tests/shell` | login and sign-up, the dashboard (three bars and chapter squares), the menu, the book page, settings, full screen, the player and the "Voice-over" window |
| `tests/learning` | questions, exercises with typed answers (DM), code practice (a fake worker; `E2E_WORKER=1` — a real sandbox in Docker), the practice shell |
| `tests/labs` | the five labs: system design, networks, virtualization, circuits and Mini-8 assembly, RISC-V — the reference through a draft (the "data → engine → server" pipeline), by hand, and a server rejection. `E2E_ARCH_ALL=1` — all 95 circuit exercises |
| `tests/books` | **one file per book, one test per chapter**: all slides and diagram steps, tabs, progress, the console (302+ chapters, about 30 minutes) |

Running one book: `E2E_PORT=8101 npx playwright test tests/books/09-db.spec.ts --reporter=list --output=/tmp/pw-books`.
For parallel runs, each has its own `E2E_PORT` and its own `--output` (a shared `test-results` folder gets corrupted).

## Against a ready-made stack

`E2E_BASE_URL=http://127.0.0.1:18080 E2E_USER=admin@example.com E2E_PASSWORD=… npx playwright test tests/shell` — the tests run against an already running stack (for example, `docker compose` with the Rust backend,
see `docs/deploy-agent.md`), and no server of their own is started. Only the tests that need public routes and sign-up are included (shell, books, labs);
the `FakeWorker` code-practice tests are designed for a server of their own.
A ready-made stack limits sign-ups (429), so instead of a new user for every test, the tests log in as the given one (`E2E_USER`, `E2E_PASSWORD`) and erase its progress.

## Building the backend without access to the private registry

The backend depends on private libraries from the lab registry. If the registry is unavailable, build against a ready `cargo vendor` directory (on the server — `~/cs-core-vendor`, the author's copy — `~/.cache/cs-core/vendor-backend`):
in a copy of `.cargo-config.toml` from that directory, replace `directory = "/vendor"` with the path to the directory and pass the file: `CARGO_FLAGS="--config /path/vendor-local.toml" npm run build`.
