# AGENTS.md — rules for the "cs-core" project

"CS.Core" audio course: backend on axum + SurrealDB (`backend/`), frontend on Leptos (`frontend/`), shared Rust crates (`packages/`),
a code-checking worker in Python (`worker/`), kokoro-ru voice-over (`voice/`). The course content is data in `backend/data/`
(texts `textbook/<id>-<slug>/*.md`, slides `slides/`, labs `labs/`, exercise and quiz SQL `sql/`, audio `audio/`).

**The previous implementation was removed on 26.10.2026** (FastAPI + SQLite, React + Vite, hand-written Python task modules, quizzes and slides in TypeScript)
and is preserved in the git tag `legacy-react-python`: `git show legacy-react-python:<path>` or `git worktree add /tmp/legacy legacy-react-python`.
Paths such as `frontend/src/slides/…`, `exercises/*_tasks`, `content/quizzes/*.ts`, `npm run …:export`, `seed_textbook.py`, `app/…` in the per-book sections
below refer to that old code; **the source of truth is now the data files** (see "Content storage"). The sections about the interface
(header, fullscreen mode, dashboard, chapter tabs) describe behavior that is also implemented in the Leptos version (`frontend/app/src/{pages,components}/*.rs`).

## MANDATORY RULE: we are writing the book now, there is no voice-over

The course is written in full, and **the audio will be generated much later, once all chapters of all books are ready**. Therefore for now
**we absolutely abstract away from audio** — in all books and sections we work in the format "slides + text that
will later be spoken off-screen":

- **all existing sound has been deleted** (`backend/data/audio/` is empty, 16.10.2026) so the project stays light; generating it
  later is a single command, run once, which takes a while to finish, so **100% of the attention goes to the content**;
- we do not synthesize wav; we do not run voice-over (`voice/`, synthesis scripts); the backend does not generate audio;
- we do not compute `cues` from pauses in wav and do not check voice-over durations — `cues` are computed by character share
  (≈ 14 characters per second), which is enough until the final voice-over;
- we do not maintain `docs/audio-status.md` as we go and do not write "voice-over is outdated" in tasks and reports: when
  a paragraph is rewritten, the old wav is simply considered stale, and everything will be voiced again at the end;
- sound does not slow decisions down: text can be edited, chapters rewritten and added, numbering changed (if the content
  calls for it, taking into account only user progress and the slide/quiz/exercise keys);
- the lesson text is nevertheless written as an off-screen narration: conversational Russian, Latin names and terms spelled out in Russian
  ("yu-ti-ef-eight", "system-dee"), no "see the figure" and no code inside a paragraph — code lives on the slides;
- the remaining "one paragraph = one scene = one part" rules stay: the structure must be ready for voice-over.

## Repository structure

- `backend/` — backend (section "Backend"); `backend/data/` — course data; `frontend/` — Leptos frontend; `packages/` — shared crates;
  `worker/` — code-checking worker (`worker.py`, sandbox `runner.py`, `docker/rust-crates` — image for tasks with tokio/axum/sqlx);
  `voice/` — voice-over (`engine.py`, `download_model.py`; the model is in `voice/models`, not tracked by git); `e2e/`, `deploy/`, `docs/`; `packages/i18n` — translation functions (a shared crate without texts), `packages/locales` — cs-core JSON dictionaries.
- Python remains in the worker and the voice-over: `cd worker && uv run worker.py …`; the worker has no dependencies (standard library + Docker CLI).
- Paths are resolved from the files of the package/crate, not from the CWD (except for the explicit `DATA_DIR`, `STATIC_DIR`).

## Code checking: queue and workers

The backend does not start containers: `POST /api/exercises/run` puts the solution into a queue (`backend/src/jobs.rs`) and answers `202`; the client polls
`GET /api/exercises/run/{id}` (`queued` with a queue position → `running` → `done` with a result, `pages/chapter/code.rs`). It is executed by the external worker
`worker/worker.py` (on the same machine or another one, `CS_CORE_WORKER_TOKEN`): it fetches jobs itself over HTTPS at `/internal/worker/*` and has no access
to the database. Lanes: `light` (python/js/sql) and `heavy` (rust/c), leases with heartbeats, a result cache keyed by the solution hash, a queue ceiling, two attempts;
queue changes happen under a single process lock, **the backend runs as a single instance**. The sandbox lives only in `worker/runner.py` (`_run_container`:
container name, stop on timeout, output ceiling, `--cap-drop ALL`, `nobody`). There is no built-in worker. Details and deploying the worker
on a home server are in `docs/code-runner.md`; queue tests are in `backend/tests/api.rs`.

## Deployment

A single machine that has only docker compose: `deploy/docker-compose.yml` (traefik as the entry point, proxy on Caddy with the Leptos static files — frontend, api on axum, surrealdb, backup;
profile `checks` — worker, dind and a one-off images service), `traefik/http.yml` and `traefik/tls.yml` (routes), Dockerfiles (`backend.Dockerfile`, `proxy.Dockerfile`, `worker.Dockerfile`) and the `Caddyfile` next to them. The instructions for the agent on the server are in
`docs/deploy-agent.md`, the choice of scheme and the order of work in `docs/deploy.md`. The worker starts sandboxes in a **separate dind daemon** (the host socket is not
mounted into containers); the sandbox directory `/sandboxes` is a volume shared by the worker and dind. The backend is built with the secret `lab_token` (`LAB_TOKEN=… docker compose …
up -d --build`) or with a ready `cargo vendor` (`CS_CORE_VENDOR_DIR`). Voice-over is not part of the images (`voice/` is separate).
**Release deployment:** `.github/workflows/release.yml` (a GitHub release → `deploy/server/release.sh` on the server builds the `cs-core-*:<tag>` images, starts the stack and rolls back if the check fails); `ci.yml` — tests of `packages/` and the frontend (the backend is not built in Actions: the closed libraries of the lab registry live on the server in `~/cs-core-vendor`). Public images on Docker Hub (`alexeirysev/cs-core-*`, amd64 + arm64) — `deploy/publish.sh`. Details — `docs/deploy.md`, "Release deployment" and "Publishing images to Docker Hub".

## Backend: axum + SurrealDB (`backend/`)

Routes: `/api/books`, `/api/chapters`, `/api/progress`, `/api/quizzes`, `/api/answers`, `/api/exercises`, `/api/slides`, `/api/labs`, `/internal/worker`; login,
registration and the admin panel are the shared lab crates (`auth`, `auth_api`, `admin_api`, `system_tasks`, `mail`, `observability`) from the private `lab` registry
(`/Users/rysev-a/Projects/lab/.worktrees/main/packages`; the structure standard is `web-services/standard.md` there). Versions and features are in `[workspace.dependencies]`
of `backend/Cargo.toml`: the list is **1 to 1 as in lab** (`web-services/Cargo.toml`), `Cargo.lock` is taken from there too (so that the dependency graph and the prebuilt base images
match); beyond the list there are only `rusqlite` (reading the seed SQL files) and `sha2`. When you update versions in lab, update them here too; do not diverge.

- Layout: `lib.rs` (router, `build()` — schema, seed, auth, background tasks), `config.rs` (environment), `db.rs` (SurrealDB connection and table schema),
  `seed.rs` (seeding content from `backend/data`: `textbook/**/*.md`, `slides`, `labs` and `sql/{books.sql,tasks,quizzes,answers}` — the SQL
  is executed in in-memory SQLite and transferred to SurrealDB; re-seeding only if the source hash changed, mode `SEED=auto|always|off`), route modules
  `courses`, `progress`, `quizzes`, `answers`, `exercises`, `worker_api`, the check queue `jobs.rs` (the same model as the Python one: lease, heartbeat, cache,
  two attempts; queue changes happen under a single process lock, **the backend runs as a single instance**), `practice.rs`, `schema_view.rs` (ERD data for SQL tasks).
  Chapter ids are assigned in the order of books and chapters; audio ids are `uuid5` of `<book audio_prefix><chapter>-l<paragraph index>`.
- The session is a token (`Authorization: Bearer`, issued by `POST /api/auth/login`), login is by **email** (the `auth` crate has no logins, the name is `profile.name`);
  the password is at least 8 characters (demo users `DEMO_USER_*`, `DEMO_ADMIN_*` — no policy, for development only). The frontend works with this API
  (`frontend/app/src/session.rs`, client — `frontend/crates/api`).
 
- **Code is checked by an external worker** `worker/worker.py` (Docker orchestration is Python, `worker/runner.py`); the backend only keeps the queue and hands out
  jobs at `/internal/worker/*` with the token `CS_CORE_WORKER_TOKEN`; there is no built-in local worker.
- Running for development (SurrealDB from the lab dev stack: `ws://127.0.0.1:8123`, root/devpass):
  `cd backend && SURREAL_USER=root SURREAL_PASS=devpass BIND=127.0.0.1:8001 CS_CORE_WORKER_TOKEN=dev DEMO_USER_EMAIL=student@mail.com DEMO_USER_PASSWORD=student DEMO_ADMIN_EMAIL=programmer@mail.com DEMO_ADMIN_PASSWORD=programmer cargo run`;
  worker: `cd worker && CS_CORE_WORKER_TOKEN=dev uv run worker.py --server http://127.0.0.1:8001 --name dev --light 2 --heavy 1`;
  frontend: `cd frontend/app && trunk serve`. Without an available SurrealDB (and without `DB_STRICT`) the backend runs on an in-memory database.
  Variables: `BIND`, `SURREALDB_URL`, `SURREAL_USER`/`SURREAL_PASS`/`SURREAL_NS`/`SURREAL_DB`, `DB_STRICT`, `DATA_DIR`, `AUDIO_DIR`, `STATIC_DIR` (serves `frontend/dist`),
  `CS_CORE_WORKER_TOKEN`, `SEED`, `ADMIN_EMAIL`/`ADMIN_PASSWORD`, `APP_URL`, `SITE_NAME`, `SMTP_*` (without `SMTP_HOST` emails appear only in the admin panel tasks).
- Tests: `cd backend && cargo test` (in-memory SurrealDB, seed from the real sources, login, progress, quizzes, answers, the queue and the worker API).
- Docker: `deploy/backend.Dockerfile` (context — the repository root; build secret `lab_token` = the gitness token, `LAB_TOKEN=… docker build --secret id=lab_token,env=LAB_TOKEN`)
  and `deploy/docker-compose.yml` (api, surrealdb, `surreal export` backups, worker, dind); see `docs/deploy-agent.md`.

## Leptos frontend and shared crates (`frontend/`, `packages/`)

The frontend is Leptos 0.8 CSR + trunk (library versions as in lab, `/Users/rysev-a/Projects/lab/.worktrees/main`). **The course content is data on the backend**
(SurrealDB), the client only renders. The lab frontend crates (`auth_client`, `ui_kit`, `admin_ui`) are not installed from the registry — login and the shell are written here.
Styles: `frontend/app/styles/{app,lab,netlab,sdlab,virtlab}.css` (shared, included in `app/index.html`) and `app/style.css` (the textarea-based code editor);
we do not introduce new CSS classes for slides (the same `a-*`, `s-*`).

**Shared crates in `packages/`** (each is a separate package without a common workspace; the backend and frontend include them by path):
- `highlight` — highlighting for py/c/asm/rust/sql/js/css, `Lang` with serde;
- `content` — the course data model (serde): `Tone`, scheme elements (`Cell`, `Dot`, `Lnode`, `Text`, `Ptr`, `Line`, `Zone`, `Path`, `Bar`, `Code`,
  `Gate`, `Transistor`, `Switch`, `Lamp`, `Circle`, `Region` — the regions ∪ ∩ \ and complement), `SceneSpec`/`Scene::compile` (validation: number of captions,
  element kind for an `id`, finite numbers, step marks) and `Scene::lint` (text fits in cells, nothing outside the canvas), `Slide`/`Block`/`Chapter`
  (blocks: scheme, code, "ON SCREEN", caption, callout, hint, themes, cards, table), `content::dsl` constructors;
- `gen` — **content generators in Rust**: `generated()` (chapters whose source is code: `py_ch00`, `dm/ch01…10`), `bin generate <dir>` writes the
  data files, `bin lint_slides <dir>` checks them. New chapters are written with generators: scene = `SceneSpec` of frames, chapter = `Chapter`; errors are caught by
  `Scene::compile`, `Chapter::check`, `lint`.
- labs `sdlab`, `netlab`, `archlab`, `riscvlab`, `virtlab` — section "Labs".

**Content storage:** slides are files `backend/data/slides/<book>-<chapter>.json` (canonical JSON of `content::Chapter`). For chapters from `gen::generated()`
the source is the generator (the file is overwritten by `generate`, do not edit by hand); the other chapters were ported once from the old TypeScript, and now the JSON is
the only source (edit by script or by hand, then `lint_slides` and re-seed). The backend seed puts them into the tables `slide_chapters` (rubric, slide count)
and `slides` (a slide is a document, the body is an array of blocks; a scene is nested JSON) → `GET /api/slides` and `GET /api/slides/{book}/{chapter}`. The seed validates each chapter
(`Chapter::check`) and it is part of the re-seed hash. The client (`frontend/crates/api` → `Client::slides`) receives `content::Chapter` and renders `components/blocks.rs`
(`DataSlide`/`BlockView`) and `scene::SceneView`. Quizzes, code tasks and answer-entry exercises are SQL files `backend/data/sql/{quizzes,tasks,answers}`,
edited directly (see "Exercises in the DB" and "Quizzes in the DB"); labs are JSON in `backend/data/labs`.

- Contents of `frontend` (workspace): `crates/scene` (scheme rendering: `Stage`, `SceneView`, views of all elements, `Paint`, `use_steps`, `use_reveal`), `crates/api`
  (client and DTOs), `app` (shell, login, progress, the player on virtual clocks at 14 chars/s, the "Off-screen" window, slides, quiz, answers, code practice).
- Running: the backend on 8001 (see above), then `cd frontend/app && trunk serve` (port 7054, `/api` is proxied to 8001).
  Tests: `cd frontend && cargo test --workspace`, `cd packages/<crate> && cargo test`.
  Data check: `cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/slides`.
- Rules: number of paragraphs = number of scenes = number of parts, colors only `--s-*` (both themes), no voice-over; motion goes through CSS transitions and state,
  `prefers-reduced-motion` turns it off; a scene has `labels`/`caption` of equal length, number of frames = number of captions; `cues` marks are by character share.

## Labs: data, engines in Rust, server-side checking

Lab exercises (book 14 "schemes, Mini-8, RISC-V", 15 "networks", 17 "virtualization", 18 "system design") are **data on the backend**, and the computation is done by
the shared Rust crates `packages/{archlab,riscvlab,netlab,sdlab,virtlab}` (serde, no browser; built natively and to wasm). They also run in the Leptos interface
(computation in the browser) and on the server (**verifying the submitted solution**: we do not trust the client).

- **Data:** `backend/data/labs/<kind>/<book>-<chapter:02>.json` (`arch`, `riscv` — both in `labs/arch`, `net`, `virt`, `sd`): `LabChapter { book, chapter, lab,
  tasks: [{ id, title, statement, hint, spec }] }`; `spec` holds the scenario (initial scheme, goals, constraints) and the reference (`solution` / `reference`). The data files are canonical, they are edited
  directly (or written by a generator script) together with a crate test; the "golden" results of the old TypeScript engine are kept as fixtures of differential tests
  (`packages/*/tests/golden*.json`) — the tests stay, and they cannot be recreated without the `legacy-react-python` tag. New exercises are added to the data, and the reference
  must pass the engine's check while the initial scheme must not.
- **Seed and API (`backend/src/labs.rs`):** the files go into the table `lab_tasks` (they are part of the re-seed hash); `GET /api/labs/{book}/{chapter}` returns exercises **without the reference**
  (`spec.solution` and `spec.reference` are stripped). `PUT /api/exercises/{book}/{chapter}/{id}/solved` for exercises with lab data re-checks the solution with the engine
  (`sd::verify_raw`, `net::verify_json`, `riscv::task::verify`, `virt::verify`, `arch.verify` — composite blocks are assembled from the student's own solutions, `code_drafts`) and on
  rejection answers 422 with the reason. Exercises without lab data are accepted as before (with a warning in the log).
- **Backend tests (`backend/tests/api.rs`):** the references of all exercises are accepted, the initial schemes are not (system design, networks: all 79, architecture: all 103
  in course order, RISC-V, virtualization by `trace`).
- **Leptos interface:** `frontend/app/src/components/labs/` — `LabHost` (loading the chapter scenarios, submitting the solution and showing the rejection reason) and one module per lab
  kind (`sd`, `virt`, `net`, `arch`, `riscv`); the shared board code is `board_view.rs`. The "Practice" tab of a chapter made only of lab exercises gets the class
  `lab-pr` (an exercise strip at the top).
- Differences from the previous behavior: the `instances` limit of `app`/`ws` in system design was raised from 30 to 40 (the references of final exercises 22–24 needed 33–35);
  the server is stricter than the client (parameters per the reference table, hidden parameters are not changed, components outside the palette and closed blocks are rejected).

## E2E tests (Playwright, TypeScript)

`e2e/` — browser tests against the Leptos frontend and the backend (in-memory database, the course is seeded from `backend/data`). Build and run — `e2e/README.md`
(`npm run build` → `npm test`; one book — `npx playwright test tests/books/<file>`). Each test takes a new user (`loginFresh`), the console guard
turns a Rust panic and `console.error` into a failure. The book tests go one chapter at a time (`workers = 1`), labs are checked in three ways: the reference
through a draft, by hand in the interface, and a server rejection. If a test reveals an application defect, we fix the application and the test stays strict (`test.fixme` — only
temporarily). Before committing interface changes: rebuild `e2e/.dist` and run the affected modules.

## Content: new books and chapters

**New books are added only with slides.** A book must have:

1. A textbook `backend/data/textbook/<id>-<slug>/<slug>-NN.md` (format: `#BOOK`, `#SECTION`, `#CHAPTER N | Title`, the lesson text on one line, paragraphs separated by
   literal `\n\n`).
2. Slides for EVERY chapter: a generator in `packages/gen` (scene = `SceneSpec` of frames, chapter = `Chapter`, number of scenes = number of paragraphs; samples —
   `gen/src/dm/ch01.rs…ch10.rs`, `gen/src/py_ch00.rs`), registration in `generated()`, then
   `cd packages/gen && cargo run --release --bin generate ../../backend/data/slides` and `lint_slides`.
3. A theory quiz for each chapter — `backend/data/sql/quizzes/NN-<slug>.sql` (5 questions, `kind = 'theory'`, the fields `answer` and `expl` are required; format — as in the neighboring
   files).
4. Registering the book — one line in `backend/data/sql/books.sql` (id, short name `slug`, title, order `ord`, `audio_prefix`; the fields `icon` and
   `slides_dir` are not used by the Leptos frontend). The test `backend/tests/api.rs` and e2e check consistency.
5. Tasks — `backend/data/sql/tasks/NN-<book>.sql` (see "Exercises in the DB"); labs — `backend/data/labs/<kind>/<book>-<chapter>.json`.

Re-seeding happens at backend start if the source hash changed (`SEED=always` — forced).

## Book order and book 13 "Python as a first language"

- The order of books in the left menu is the `ord` field in `backend/data/sql/books.sql`, according to the plan in `course.MD`; the seed does not touch user progress.
- Python (book 13): 52 chapters **0–51** in 14 sections: "Basics" (0 introduction, 1–4), "Data and loops" (5–8), "Dictionaries and tuples" (9–11), "Classes" (12–14),
  "Exceptions and files" (15–17), "Data model" (18–21), "Iterators and generators" (22–24), "Functional programming" (25–28),
  "Metaprogramming" (29–32), "Standard library" (33–39), "Class design" (40–42), "Asynchrony" (43–46), "Python internals" (47–49),
  "Projects and tools" (50–51). Chapters are written in the animated format: 13 paragraphs = 13 scenes, 9 code tasks, a quiz of 5 questions. The mode of all new tasks is
  `stdout` with a hidden `driver` (the student writes a class/function, the driver prints the result; banned techniques — via ast over `/sandbox/solution.py`).
- **Inserting a chapter in the middle is allowed**, but requires a shift: the number is part of the slide file name (`13-NN.json`), `py-NN.md` and the first phrase of the text ("Chapter N."),
  of the quiz, task and exercise keys (SQL), of the user progress tables in SurrealDB (column `chapter` with `book_id = 13`) and of the audio ids. Do the shift
  with a script from larger numbers to smaller ones, and save a copy of the database beforehand.
- Code task modes (field `mode` in `tasks`; everything else — tests, reference output, driver, `setup`, `flags` — lives in `spec`): `func` (calling a function with
  JSON arguments; tuples are real tuples), `stdout` (output comparison; with a hidden `driver` — code that prints the result after the student's solution:
  classes, files, generators, mocks), `sql` (the student's query runs in SQLite on the ready `setup` database; the result of the last SELECT or of the check query `check` is compared — as a set of rows or in order with `ordered`; for plans — `contains`/`forbid`), `rust` (the student's code + a hidden `driver`
  are assembled into one file and compiled with `rustc` in the image `rust:1.97-slim`: no network, std only; the driver is wrapped in `mod __cs_core_driver`), `c`
  (gcc 14), `js` (node 22), `lab` (lab exercises, checked by the engine). The registry of modes and images is `worker/runner.py`.
- Efficiency in algorithm tasks is checked not by words: the driver counts accesses to data (a list subclass with a `__getitem__` counter) or feeds an input
  on which O(n²) does not finish within the sandbox limit (25 s); to verify, also run the naive solution — it must fail.
- Check every task reference in the sandbox: the solution passes, the empty starter does not.

## Exercises in the DB: SQL files

At runtime the application reads tasks **only from the `tasks` table** (`book_id, chapter, id, ord, mode, title, statement, starter, hint, spec`; everything else —
tests, reference output, driver, `setup`, `flags` — goes into `spec` as JSON, Python tuples are stored as `{"__tuple__": [...]}` and returned as tuples).
The source of truth is the SQL files in `backend/data/sql/tasks`: `00-schema.sql` creates the table, `NN-<book>.sql` has one `INSERT` per task. They are **edited
directly** (the hand-written Python modules are gone: the old ones are in the tag `legacy-react-python`); the backend seeds them at start if the source hash changed.
Check new tasks in the sandbox (`worker/runner.py`): the solution passes, the empty starter does not.

## Quizzes in the DB: answers only on the server

The source is the SQL files in `backend/data/sql/quizzes` (`00-schema.sql` — the tables `quizzes` and `quiz_questions`, `NN-<book>.sql` — one `INSERT` per quiz and
question), they are edited directly; the seed loads them into SurrealDB at start if the source hash changed.

API (`backend/src/quizzes.rs`): `GET /api/quizzes` — the number of questions per chapter; `GET /api/quizzes/{book}/{chapter}` — questions and options **without answers** and
`reveal` with the answer and explanation for the questions the user has already answered; `POST /api/quizzes/{book}/{chapter}/answer` `{question, pick}` — records the
choice (a question is answered once) and returns the correct answer, the explanation and the number of correct ones; `DELETE /api/progress/quiz?book=&chapter=` — retake.
`GET /api/progress` returns `quizRight` (the number of correct answers per chapter), the client does not know the answers. Chosen options cannot be recorded retroactively.

## Book 9 "Databases": layout

32 chapters. **1–16 — "SQL basics"** (text `textbook/9-bazy-dannyh/13-db-NN.md`, 13 paragraphs = 13 scenes `slides/anim/DbNN.tsx`, slides `slides/db/chNN.tsx`,
a quiz of 5 questions in `content/quizzes/db-sql.ts`, 30–50 exercises): basics and syntax, filtering, sorting and LIMIT, text and NULL, aggregates, JOIN, subqueries, DML, DDL, CASE,
functions, GROUP BY/HAVING, indexes and EXPLAIN, CTE, windows, views. The teaching databases are a shop (customers, products, orders, order_items), HR (departments,
employees), a school and movies; tasks are written in `exercises/db_tasks/ch01.py … ch16.py`, id — `sNN-KK`. **17–32 — "under the hood"** (slides, quizzes, tasks; they used to be
chapters 1–16: their numbers were shifted by +16, slide keys — `"9:17"` … `"9:32"`, scenes — `slides/anim/Db17.tsx … Db32.tsx`).

- `sql` mode tasks: executed in the sandbox SQLite on the `setup` database; values (not column names) are compared — as a set of rows or in order (`ordered`);
  for DML/DDL — `check` (a query after the solution); for plans — `check` with `EXPLAIN QUERY PLAN` and `contains`/`forbid`. Tasks have `expected_cols` (the reference column names).
  The `func` mode is Python simulations (caches, replicas, the optimizer, security, etc.).
- Each SQL exercise shows the "Database" widget (`components/SqlSchema.tsx`): an ERD diagram (tables can be dragged, relations are highlighted) and
  a view of the table data. The schema and rows are built on the backend from `setup` (`exercises/schema_view.py`) and arrive together with the chapter tasks (`datasets`).
- A wrong result of a SQL task is shown as two tables side by side (yours and the correct one, `components/SqlDiff.tsx`): differing values, extra and missing
  rows and columns are highlighted. The sandbox returns `got_rows`, `got_cols`, `exp_rows`, `exp_cols`; the result in the logs is aligned by columns.
- Task references are computed on the host (`sqlite3`) and re-checked in Docker: the solution passes, the empty starter does not; query plans differ between SQLite versions,
  the source of truth is Docker.

## Book 14 "Computer Architecture": the lab

The book was rebuilt from scratch and **does not use Python** (neither in the text nor in practice). 22 chapters:
1–3 "Computer and transistor" (levels of abstraction, transistor physics and CMOS, standards and open
architectures — after Harris and Harris), 4–5 "Basics" (numbers, text and data protection), 6–9 "Digital logic",
10–12 "Processor building blocks" (registers and clock, ALU, memory), 13–14 "Processor" (decoder, a processor built from blocks),
15–17 "Programming" (Mini-8, RISC-V, real programs), 18–22 — cache, pipeline, virtual memory,
input/output, parallelism. **Do not insert a chapter in the middle** (the number is part of the slide, quiz and task keys
and of the audio id `arch-ch<N>-l<i>`).

- Exercises are a React port of the trainer `/Users/rysev-a/Projects/learn/processor` (Angular). The framework-free engine
  was copied as is into `frontend/src/lab/**` (schemes: `exercises/logic-gates`, blocks `blocks.ts`,
  assembler `asm/`, the Mini-8 processor on gates `cpu8/`, RISC-V `riscv/`); the interface was rewritten in React:
  `lab/react/` (`GateBoard`, `BlockBoard`, `CircuitView`, `CircuitLab`, `CheckPanel`, `WaveDiagram`,
  `AsmLab`, `RvLab`, `CpuInspector`), styles — `lab/lab.css` (application tokens, both themes). Engine changes made while
  copying: exercises store solutions in `localStorage` with a user prefix (`setLabNamespace`),
  hints about closed blocks say "practice «…»". Not ported: "Auto mode" (step-by-step walkthroughs),
  the `?edit=1` mode for editing a block's solution from the view.
- Chapter practice is `components/LabPractice.tsx` (lazy-loaded): a strip of exercises at the top,
  one exercise on the right. Checking happens **in the browser**; a solved exercise is sent to
  `PUT /api/exercises/14/<chapter>/<id>/solved` (the server accepts only `lab` mode tasks, writes an attempt,
  the "solved" status and the solution as a draft). For schemes the solution is JSON (`{gates,wires}` or
  `{instances,busWires}`), for the assembler and RISC-V it is the program text (the draft is written automatically, like for code).
  On login `lab/hydrate.ts` rewrites what is solved on the server into `localStorage`: blocks are assembled from the solutions
  of other chapters, the palette unlocks composite elements. "Reset exercises" in settings also erases the snapshot.
- Contents: chapters 6–14 are schemes (`lab/registry.ts`, sections from `lab/sections/sections.ts`), 15 — Mini-8,
  16 — RISC-V, 17 — real programs (built locally: Makefile + zip). The registry of chapters → lab type is
  `LAB_CHAPTERS` in `lab/registry.ts`. After editing lab data **rebuild the manifest**:
  `cd frontend && npm run lab:manifest` (writes `backend/app/exercises/arch_tasks/lab_manifest.json`;
  the dashboard counters and the task list depend on it), and the engine integrity is checked by
  `npm run lab:check` (the reference solutions of schemes, Mini-8 and RISC-V pass the checks).
- Slides are frame-by-frame animations in the DSL `slides/anim/alg.tsx` (the book 7 elements are extended with `gate`, `tr`,
  `sw`, `lamp`; helpers in `anim/hw.tsx`: `GT`, `pl`, `wr`, `bit`, `mux`, `wave`), one file per chapter
  `anim/ArcNN.tsx` (scenes `V01…`, one per paragraph; chapters 1–3 and 6–17 have 10 paragraphs each, 4, 5, 18–22 have 13).
  The rules are the same as for the other animated books: number of paragraphs = number of scenes, colors only `--s-*`.
- Chapters without a lab (1–5 and 18–22, theory and calculations) got answer-entry tasks — the same system as in "Discrete Mathematics"
  (`frontend/content/exercises/arch.ts`, 10–12 tasks per chapter: bits and units, CMOS and power, two's complement, Hamming codes and CRC,
  average cache access time, pipeline CPI, address translation and page faults, input/output, Amdahl's law). The server checks the answers;
  after editing — `cd frontend && npm run answers:export`, then `uv run seed_textbook.py --no-audio`.
- Audio for this book has not been synthesized yet; the `cues` in the slides are computed by character
  share and after voice-over they must be recomputed from the pauses in wav.

## Audio: one slide — one file (no exceptions)

Each lesson paragraph is voiced as a **separate wav file** and shown as a
separate "part" of the chapter: switching a slide starts playing its paragraph from the
beginning, without the tail of the previous phrase. The seeder does this by itself for all chapters of all
books (the split into paragraphs is in `backend/src/seed.rs`), the frontend turns on the parts mode
when a chapter has more than one part. Therefore:

- number of lesson paragraphs = number of scenes in the slides = number of parts (verify it);
- do not bring back chapter voice-over as a single file and binding slides to sentences
  by time (karaoke mode);
- part ids are `uuid5` of `<book audio_prefix><chapter>-l<paragraph index>`: if
  you edit a paragraph's text, regenerate its wav (the seed skips existing
  files), and if the number of paragraphs changes, the whole chapter.

## Recording a voice for a slide: "Play + record"

An authoring tool in the slide header (`components/slides.rs`, `RecordCtl`; the button is visible **to administrators only**): next to "Play" there is
"Record": the slide plays from the current position, the microphone is recorded through `MediaRecorder` (`frontend/app/src/recorder.rs`, webm/opus, or mp4 in Safari);
recording ends with the "Stop" button or when the player leaves this slide (the player stops, the slide stays). The file goes to
`POST /api/records/{book}/{chapter}/{slide}` (`backend/src/records.rs`, the body is the file as is, the type is `Content-Type`, 403 for a non-administrator) and is stored in
`RECORDS_DIR` (by default `media/records` in the repository root, not tracked by git) as `<book>/<chapter>/<slide 0-based>.<webm|m4a|ogg|wav>`;
a slide has one file — a previous one with another extension is deleted. Promises in `recorder.rs` are handled with callbacks: `wasm-bindgen-futures`
is not in the dependency set. The test is `slide_recordings_are_saved_by_administrators_only` (`backend/tests/api.rs`).

## Header and settings

On the right of the header there are two square icons (36 px, `.btn-icon`, as in the neighboring trainer):
a gear — the `/settings` page (`pages/settings/index.tsx`) and the theme switch
(sun/moon). Appearance settings live in the browser `localStorage`, the keys and helpers are in `lib/settings.ts`:
theme, collapsed sections menu, autoplay of animations (`cs-core-anim-auto`; when off,
scenes immediately show the final state, as with `prefers-reduced-motion`) and resetting exercise
progress. A new setting = a toggle row on the settings page + a key in
`KEYS`.

## Internationalization: Russian and English

Two languages of the interface and content. **The translation key is the English text**, the Russian version is in the dictionary (`ui_kit`/`auth_client` in lab work the same way).

- **Interface and lab engines**. Two crates: `packages/i18n` — **logic without texts** (shared, usable in any project: language, `tr`/`trf!`/`plural`,
  loading dictionaries from JSON with `i18n::load_json(Locale::Ru, json)`), `packages/locales` — **the cs-core dictionaries**: JSON files `locales/ru/<area>.json`
  (`ui`, `labs_ui`, `server`, `archlab`, `riscvlab`, `netlab`, `sdlab`, `virtlab`, `weblab`; a flat object "English key → translation", entries sorted by key)
  and `locales::install()`, which embeds them with `include_str!` and loads them into `i18n` once (called by `settings::init_locale` on the frontend and by `build()` on the backend).
  In code: `i18n::tr("Sign in")` (returns `&'static str`, so it fits everywhere a literal used to be),
  `i18n::trf!("Solved {0} of {1}", a, b)` (substitutions `{}` in order or `{0}`, `{1}` by number; `{{`/`}}` are literal braces; values with a format like `{:.2}` are formatted beforehand with `format!`),
  `i18n::plural(n, "row", "rows")` (the three Russian forms are in the dictionary under the key `"row|rows"`), `i18n::t!("Dark")` (marks a key where a function cannot be called: `const` and static tables;
  display through `tr(...)`; a plain English literal in the table is also acceptable if `tr` is applied where it is shown), `i18n::tr_dyn(&str)` (server messages).
  A new area = a file in `locales/ru/` and a line in `locales::RU`; the test `packages/locales/tests/dictionary.rs` scans the sources of the frontend, backend and lab crates:
  every key from the code is in the dictionary, and the dictionary has no extra entries, duplicates (including across areas) or mismatches in substitutions and plural forms.
  The language is chosen at start (`settings::init_locale`: `cs-core-lang` in `localStorage`, otherwise the browser language, otherwise English) and changes **by reloading the page** (`settings::switch_locale`, the EN/RU switch
  in the header and on the login screen). The API client sends `Accept-Language`. **The server checks lab solutions in the request language:** `i18n::with_locale(locale, || …)` in `labs::check` (the language is per-thread, the global `set_locale`
  is one per process); in tests that compare Russian texts, enable the language with `locales::guard(Locale::Ru)` (frontend) or `locales::set_locale(Ru)` (crate tests: `locales` is a dev-dependency, it also loads the dictionaries). Unit tests without the guard run in English;
  e2e runs in a `ru-RU` browser, English is checked by `e2e/tests/shell/language.spec.ts`. **New interface text and engine messages go only through `tr`/`trf!`, with an entry in the dictionary.** Data that an engine
  compares or parses (command names, keys, the contents of the HTML pages of exercises) is not translated.
- **Server messages** (`ApiError`, code-check errors) are English text, which is also the dictionary key; the client shows `tr_dyn(detail)`. We do not write Russian text in `ApiError`.
- **Course content**: the base is Russian (`backend/data/…`), the translation lies next to it in `backend/data/<lang>/` with the same layout: `textbook/<id>-<slug>/…`, `slides/<book>-<chapter>.json`,
  `sql/books.sql` (only translated books: title and order), `sql/quizzes/…`, `sql/answers/…` (the seed takes the Russian `00-schema.sql`). The seed puts the translation into the tables `<table>_i18n`
  with a `lang` field; **chapter and section ids are shared with the Russian ones**, so addresses, progress, drafts and "solved" do not depend on the language. A book is translated **in full**; the structure must match
  the Russian one (numbers and count of chapters, paragraphs, slides, questions, options, the index of the correct answer, the number of tasks) — `seed::check_translation` fails the seed otherwise, so that progress does not break.
  The request language is the `Accept-Language` header or `?lang=` (`backend/src/lang.rs`); for a book without a translation into that language the answer is Russian, and `GET /api/books` returns `langs` (the client draws an "RU" label and
  a note). Counts (progress, per-chapter numbers) always go by the Russian rows. Lesson parts in another language have their own ids (`uuid5` of `<lang>:<prefix><chapter>-l<paragraph>`), and the audio for them is separate.
- **Code tasks and labs**: the texts of code tasks (`title`, `statement`, `hint`, `starter`) live in `data/<lang>/tasks/<book>-<chapter>.json`; tests, driver and reference stay shared (Russian) in the `tasks` table,
  so everything the student must print (strings in guillemets and quotes) stays verbatim in Russian in the English statement; in `starter` only comments are translated (`seed::check_starters`; `code_skeleton` strips `/* */`, `#`, `//` and `--`).
  The lab texts are `data/<lang>/labs/<kind>/<book>-<chapter>.json`: `title`, `statement`, `hint` and `spec_text` — translated captions inside the scenario by JSON paths (`/goals/0/text`, device and node names);
  the scenario, goals, references and HTML pages are shared. The tables are `tasks_i18n` and `lab_tasks_i18n`, the substitution is `lang::overlay` and `labs::apply_spec_text` (both in the API response and when checking a solution).
  For lab tasks (`mode = 'lab'`) `data/<lang>/tasks/<book>-<chapter>.json` holds the same `title`/`statement`/`hint` as `labs/` (the structure is checked by `seed::check_translation`).
- **RULE: in exercises, text and strings are English only.** In all new and rewritten exercises (code tasks, answer-entry tasks, labs) everything that is in the task data is written in English:
  strings in drivers and tests, expected output, input examples, names of people and things in examples, messages the student must print, captions in scenarios. Then the same statement holds for both languages,
  and the English translation needs no Russian guillemets. Only the explanations in `statement`/`hint` remain Russian (and only in the Russian version of the book). The exception is tasks that are by nature about Cyrillic and Unicode
  (encodings, `str.upper()` for Russian letters, etc.): there the strings are Russian, and the statement says so. Old exercises with Russian strings (Python of book 13, JavaScript of book 11, part of books 15–17) are converted to English strings
  as work on the book proceeds; until they are converted, the English statement quotes the Russian output verbatim (`seed::check_starters` checks only `starter`).
- **Translated: all books of the course** (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18; there is currently no fallback to Russian). Books 7–10 and 16: textbook, slides, quizzes and code task texts (Russian output strings in statements are quoted verbatim in guillemets/backticks). In detail: book 11 "Modern Frontend" (39 chapters, 900 JS tasks and 171 HTML/CSS exercises), 14 "Computer Architecture" (22 chapters, answer-entry tasks, labs), 15 "Computer Networks", 17 "Virtualization", 18 "System Design" (textbook, slides, quizzes, code tasks and labs), 13 "Python as a first language" in full (52 chapters: textbook, slides, quizzes, 418 code tasks) and book 12 "Discrete Mathematics" (textbook, 130 slides, 10 quizzes, 75 answer-entry tasks; yes/no answers are accepted as `yes`/`true` and `no`/`false`). In the English Python slides the code and program output are in English (quoted strings are translated), in tasks with output checking the output stays Russian.
  The English off-screen text was written anew, not translated line by line (Latin terms are written normally, not spelled out in Russian). Slides: the scene strings are translated by a script over the JSON, then
  `cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/<lang>/slides` — English is longer than Russian in narrow cells, shorten captions if needed.
- **A new translated book**: translation files per the list above, the book row in `data/<lang>/sql/books.sql`, then `cargo test` (the seed checks the structure) and the test `translated_books_are_served_in_english_and_the_rest_in_russian`.

## Color themes (like VS Code)

The mode (light or dark) is `data-theme` on `<html>` (`cs-core-theme`), the color theme on top of it is `data-palette` (`cs-core-palette-dark`, `cs-core-palette-light`; the default theme is not stored and sets no attribute). All colors of the site, slides, labs and the code editor are
CSS variables: the base values are in `frontend/app/styles/app.css`, the themes in `frontend/app/styles/themes.css` (included after it; blocks `:root[data-palette="<id>"]` and the same `.palette-card[data-palette="<id>"]` for preview cards).
Code highlighting takes the colors `--syn-keyword|builtin|string|number|call|comment` with a fallback from `--s-*` (`highlight::Kind::css`), so a theme colors both the editor and the code on slides.

- The theme list for settings is `frontend/app/src/themes.rs` (`PALETTES`: id, name, mode); choosing is `settings::choose_palette` (it switches the mode too), applying is `settings::apply_theme`; early application without a "flash" is a script in `index.html`.
  The "Settings" → "Color theme" page: cards with a code sample, each drawn in its own theme regardless of the current one. The test `themes::tests` ensures every theme has a block in `themes.css`.
- **`themes.css` is generated**: the main colors of each theme (background, panels, borders, text, accent, code and scheme colors) are set by hand, the derived ones (hover, transparencies, selection shades) are computed, and the contrast of text, code and buttons is verified
  (text/background ≥ 6, muted ≥ 4.5, code on a panel ≥ 3.5, background on accent ≥ 3.5). To add a theme: a block with all variables (sample — any existing one), a line in `PALETTES`, a contrast check; the main interface color is `--s-accent` (equal to the theme accent).
- Tests: `e2e/tests/shell/settings.spec.ts` ("color themes").

## Chapter fullscreen mode

Fullscreen expands the **whole chapter page**, not only the slides: the shell lives in
the chapter layout (`pages/chapters/detail.tsx`, the `.slide-fs` overlay, address `?fs=1`). Header: lesson title,
the tabs "Theory / Questions / Practice" (the same routes, `?fs=1` is preserved), the buttons of the active
tab and "Collapse"; on the left a tree (`components/FsTree.tsx`): sections → chapters, under the current
chapter the items of the active tab (slides / questions with ✓✗ / exercises with statuses). A tab puts
its items and buttons into the shell slots through portals (`itemsSlot`, `headSlot` from the route context), and
in normal mode renders them itself — so new tab content in fullscreen is added
by a portal into `itemsSlot`, without separate logic. A click on another chapter in the tree opens it on
"Theory". The player (`.np-card`) is visible over the overlay, arrows flip slides, Esc closes.
Native fullscreen is taken from `document.documentElement`: when the chapter changes the overlay may
be recreated, and the browser would exit fullscreen when its element disappears from the DOM.

## Users and the personal account

Without login the application is closed: a login and registration form (`frontend/app/src/pages/auth.rs`), the session is a token (`Authorization: Bearer`, issued by
`POST /api/auth/login`), login by **email**; the password is at least 8 characters. Login, registration and the admin panel are the shared lab crates. For development the backend creates demo
users from `DEMO_USER_*` and `DEMO_ADMIN_*` (`student@mail.com / student`, `programmer@mail.com / programmer`); on the server they are not set.
All progress lives in the user's tables (SurrealDB), the chapter key is always "book + chapter number", not the chapter id: viewed slides, answers to questions,
solved answer-entry tasks, code task statuses, code drafts, attempt history (up to 50 per task). Client: `session.rs` (who is logged in), `progress.rs`
(a copy of the progress and mutators). Code checking (`POST /api/exercises/run`) requires login and writes an attempt; a user can have only one check running at a time.
The course seed does not touch the user tables.

## Home: progress dashboard

The left sections menu (`AsideMenu`) is shown on all pages. The home page (`pages/books/index.tsx`) is a
dashboard: overall progress on slides, questions and exercises, and a card for each section with three
bars and chapter squares (the color is the share done, a click opens the chapter). Progress lives in the user's
account on the server (see "Users and the personal account"); the client takes it from `useProgress()`
(`lib/progress.tsx`): viewed slides (written by the "Theory" tab), answers to questions (`Quiz`),
solved answer-entry tasks and code task statuses. The number of code exercises per chapter is returned by
`GET /api/exercises`.
The top section of the interface is called "Sections", the logo is "CS.Core".

## Sections menu

The left menu (`components/AsideMenu.tsx`) collapses with a button in the header:
instead of titles — a column of square icons in the shadcn/lucide style (24×24,
stroke 1.8; `components/BookIcon.tsx`, the icon is chosen by the name from the book's `icon` field, to add a new icon —
add an entry to `ICONS`). The state is stored in `localStorage` (`cs-core-aside-collapsed`).

## Chapter page: three tabs

Each chapter opens with tabs, each with its own address (React Router,
`App.tsx`; the shared layout and chapter data are in `pages/chapters/detail.tsx`):

- `/book/:bookId/chapter/:chapterId` — "Theory": slides and voice-over
  (`pages/chapter/theory.rs`);
- `.../questions` — "Questions": the theory quiz (`questions.tsx`);
- `.../exercises` — "Practice" (`exercises.tsx`): code exercises in Docker.

A tab is shown only if the chapter has content for it. Practice:
at the top the progress "solved N of M", on the left a list of exercises with statuses
(not solved / failed / done), on the right one exercise — the statement,
editor, hint, tests and execution logs (`stdout`/`stderr` of the sandbox).
The selected exercise is in the address (`?task=<id>`), the logs of the last run are in memory, while the statuses
(solved stays solved), the code draft (saved automatically) and the attempt history are in the account;
a click on an attempt in the history returns its code to the editor. Ctrl+Enter (and Cmd+Enter) checks the solution; if the exercise is already solved, it leads to the next one, and after the last — to the first exercise of the next chapter of the book that has code tasks (the "Next →" button does the same). When a task is opened or changed, focus goes straight to the editor (`CodeEditor`, prop `focusKey`), with the cursor at the end of the text. The "Auto-advance" setting (`cs-core-auto-next`, off by default): after a successful check the next exercise opens in a second, if the student stayed on this task. For books without code (discrete mathematics) the "Practice" tab
shows the old `Exercises.tsx` with answer entry.

## Exercises: what exists

- Quizzes (`frontend/content/quizzes/`) are theory only, `kind: "theory"`; they live in the DB (section "Quizzes in the DB").
- Answer-entry exercises — "Discrete Mathematics"
  (sources `frontend/content/exercises/dm.ts`, key `"<bookId>:<N>"`, component `Exercises.tsx`). They live in the DB
  (tables `answer_sets`, `answer_tasks`, SQL — `backend/data/sql/answers`, export `npm run answers:export`,
  freshness check `npm run answers:check`); the client receives statements and hints without answers, what is entered
  is checked by the server (`POST /api/answers/{book}/{chapter}/check`, comparison ignoring case and spaces, numbers by
  value), the correct answer is not revealed. Solved tasks are `answer_solved`; `DELETE /api/answers?book=&chapter=` —
  start over (`PUT /api/progress/answers` was removed: what is solved cannot be "recorded" without checking). Recovery and the order of
  work are the same as for quizzes (section "Quizzes in the DB"): the server fills empty tables itself, `seed_textbook.py --no-audio`
  reloads them.
- Code exercises — all books with tasks except book 14 (it has a lab, see above) (component `components/CodePractice.tsx`):
  the editor `CodeEditor.tsx` on CodeMirror 6 (Python highlighting in the colors
  `--s-*`, both themes; Tab — indent, Ctrl/Cmd+Enter — check), checking
  **only on the server** in a Docker sandbox (`backend/app/exercises/`);
  solutions, drafts and attempt history are stored in the user's account.
  A running Docker and the image `python:3.13-slim` are required.
  Function tasks (`mode: "func"`) can return and accept tuples:
  in the task module write them as Python tuples (`"expected": (1, 9)`) — the runner
  passes tuples to the sandbox with a tag, so `[1, 9]` and `(1, 9)` are distinguished
  in tests. Dictionary keys in JSON tests are strings only.

## Book 7 "Algorithms and Data Structures": layout

19 chapters in five sections: "Foundation" (1 complexity, 2 arrays and strings, 3 linked
lists, 4 search and sorting), "Structures and patterns" (5 hash tables, 6 two pointers,
7 window and divide and conquer), "Strings and numbers" (8 string algorithms: prefix and
Z functions, hashes, trie, Levenshtein; 9 numeric algorithms and bits: Euclid, remainders, fast
exponentiation, sieve, masks), "Trees and heaps" (10 trees and traversals, 11 search trees, 12 heap and
heapq, 13 red-black trees, 14 segment trees and Fenwick), "Graphs and strategies"
(15 graph traversals, 16 shortest paths and spanning trees, 17 disjoint sets and backtracking,
18 dynamic programming, 19 greedy algorithms). The order of chapters was rebuilt by content (16.10.2026): the old
chapters 8–15 became 10, 11, 12, 13, 15, 16, 18, 19 — the slide, quiz and task keys, the text,
scene and slide files were renamed along with them; **user progress under the old numbers 8–15
was not carried over** (the transfer is SQL over the tables `slide_views`, `quiz_picks`, `answer_solved`,
`code_status`, `code_attempts`, `code_drafts` for `book_id = 7`).

- Animations are the frame-by-frame DSL `frontend/src/slides/anim/alg.tsx`: a scene =
  `scene({labels, caption, frames, base, cues, h})`, a frame is a list of elements with an `id`
  (`cell`, `dot`, `lnode`, `text`, `ptr`, `line`, `box`, `path`, `bar`, `code`); the same
  `id` in adjacent frames smoothly moves/recolors, an absent one fades out.
  Helpers: `row`, `edge`, `tree`, `chain`, `curveD`; shared by chapters 8, 9, 14 and 17 —
  `slides/anim/ad.tsx` (`Tx`, `LIST`, `span`). All scenes of chapter N live in one
  file `slides/anim/AlgNN.tsx` (`export const V01 … VNN`, one per paragraph).
  `labels` are written as literals on one line (the generator counts frames from them).
- A slide file `slides/algo/chNN.tsx` is an ordinary file: `<VNN cues={[…]} />` inside `Slide`; the
  `cues` marks are the start seconds of steps 1, 2, …, computed from the voice-over durations (wav pauses ≥0.2 s;
  without sound — by character share). The rule is the same: number of paragraphs = number of scenes = number of parts.
  When you edit a paragraph's text, change both the caption and `cues`.
- Tasks: `exercises/algo_tasks/chNN.py` per chapter (`TASKS = {N: [...]}`), the module
  `_kept.py` keeps the old tasks that moved between chapters (`KEPT`). Efficiency is
  checked by large inputs (sandbox limit 25 s) and access counters; in tasks on a
  "custom" hash table instances are checked by the probe counter `probes`, in pattern tasks
  dictionaries and sets are forbidden by code analysis (ast in the driver reads `/sandbox/solution.py`).
  References are checked in Docker: the solution passes, the starter and the naive variant do not.
  Chapters 8, 9, 14 and 17 have 20 exercises each: functions (`func`) and classes with a hidden driver; banning
  techniques (find/in/slices, dictionaries and sets, bisect) is ast analysis of `/sandbox/solution.py`;
  the data for large inputs is built by the driver itself (xorshift), the expected output is computed by the reference.
  Write new chapters of the book with the same pipeline: text → scenes `AlgNN.tsx` (13 paragraphs = 13
  scenes of 3–4 frames) → slides (`cues` marks by character share) → quiz `content/quizzes/algo.ts` → tasks.
- If a chapter paragraph is rewritten, delete its wav and rerun the voice-over; if the number of
  paragraphs changes — delete all the wav files of the chapter (the seeder skips existing files).

## Book 8 "Diving into Unix": layout

17 chapters (0–16) in eight sections. The goal of the book is for the reader to understand how an operating system works as a whole and how
Unix works: from the philosophy and processor modes (chapter 0) to the terminal and the event loop (chapter 16). Sections: "Introduction"
(0 what an operating system is, where Unix came from, kernel and user space, monolith and microkernel,
BSD/POSIX/GNU/Linux, philosophy), "Shell and files" (1 file system, 2 shell and pipelines, 3 permissions and privileges),
"Processes and scheduling" (4 processes and signals, 5 scheduler: EEVDF, sched_ext), "Kernel internals" (6 system
calls, 7 interrupts and time, 8 synchronization), "Memory and disks" (9 memory, 10 VFS, page cache, disks),
"Network and services" (11 network and eBPF, 12 boot, systemd, packages), "Isolation and the kernel" (13 containers, 14 modules,
Rust, observability), "Programs together" (15 interprocess communication: pipes, FIFO, Unix sockets and descriptor passing,
shared memory, futex, queues, signals; 16 non-blocking I/O, select/poll/epoll, io_uring,
terminals, pty, groups and sessions). Chapters 0, 15 and 16 were added with these numbers so as not to shift the rest (slide,
quiz and task keys, audio ids). The skeleton is "Linux Kernel Development" by Love (processes, scheduling, calls, interrupts,
synchronization, memory, VFS, block layer, modules), but the facts are up to kernel 6.x/7.x everywhere: EEVDF instead of CFS (6.6),
sched_ext and PREEMPT_RT (6.12), lazy preemption (6.13), BH workqueue instead of tasklet (6.9), folios, MGLRU and
maple tree (6.1), SLUB only, cgroup v2, io_uring, eBPF/XDP, Rust officially since 7.0. When editing, verify new
facts against kernel.org/LWN, do not "remember" them.

- Format is the same as in book 14: one paragraph = one slide = one scene of 3–4 frames. Texts `textbook/8-linux/linux-NN.md`
  (10 paragraphs of 70–100 words; Latin names in the voiced text are spelled out in Russian: "system-dee", "et-see", "ee-bee-pee-ef").
  Scenes of chapter N are `slides/anim/OsNN.tsx` (`export const V01 … V10`), helpers are `slides/anim/lx.tsx`
  (`Tx`, `Bx`, `Ar`, `Zn`, `Cd`, `If`, …; all on top of `alg.tsx`, canvas 360×170, colors only `--s-*`);
  the slide files `slides/linux/chNN.tsx` export `SLIDES_LX<N>` and `SLIDE_TITLES_LX<N>` with the key `"8:N"`.
  `labels` and `caption` are literal arrays of equal length, number of frames = number of captions.
- Chapter numbers are part of the audio id (`lin-ch<N>-l<i>`): the old 10 chapters of ~20 paragraphs are completely outdated, their wav
  files must be deleted before voice-over; the seeder skips existing files.
- Quizzes — `content/quizzes/linux.ts` (8 questions per chapter, 136 in total, `kind: "theory"`, correct answers in different positions).
- Tasks are **in C only** (ideologically required: the Unix and Linux kernel is written in C; there are
  no Python exercises in this book and none may be added). `exercises/linux_tasks/c_tasks.py` has 185 exercises (8–12 per chapter, mode `c`, keys `u<chapter>-…`; chapters 1–14 have
  8 "main" and 3–4 added, chapters 0, 15, 16 have 8, 11 and 8):
  real fork, pipe, mmap, sockets, POSIX threads, chroot, rlimit inside the sandbox and models of kernel structures (schedulers,
  buddy, page tables, journals, device operation tables). The rules of mode `c` are in the section "Book 16". Every reference
  is checked in Docker: the solution passes, the empty starter does not; for race and ordering tasks there are also "naive" solutions
  that must fail (shared memory without atomic operations, a mutex without PTHREAD_PROCESS_SHARED, a pipe reader without
  closing the write end, a sequential "echo server", a seqlock without retrying the read). Mind the sandbox peculiarities:
  uid 0 without CAP_SYS_NICE (nice downward does not work), ports below 1024 are not privileged (`ip_unprivileged_port_start=0`),
  io_uring is closed by seccomp (so chapter 16 has only its model — the ring), `unshare`/`sethostname` are forbidden, the architecture may
  be x86_64 or aarch64 (for seccomp choose `AUDIT_ARCH_*` by macros), the number of minor page faults
  depends on the kernel (it may serve several pages at once). Add new exercises to `c_tasks.py` (or next to it, but in
  mode `c`); the identifiers of the former Python tasks (`fs-…`, `sh-…`, `proc-…`, `k-…`, etc.) have been removed.

## Book 10 "Learning Rust": chapters 1–5 (for those coming from Python), 34–37 (Tokio) and 44–51 (chat)

Sections: "Basics" (1 values, types, stack), "Core of the language" (2 ownership and Box, 3 borrowing), "Data and
abstractions" (4 structs/enum/match, 5 collections and errors); chapters 6–16 are the former ones. The numbering of chapters 6+ did not change.
Each of chapters 1–5 has: 13 paragraphs = 13 animated scenes, a quiz of 5 questions (`content/quizzes/rust.ts`) and **exactly 30
exercises** (`exercises/rust_tasks/ch01_05.py`, id `r<chapter>-…`). Each chapter draws parallels with the book
"Computer Architecture" (stack frames and sp, alignment, malloc, niches, stack unwinding, MESI).

- Scenes are the frame-by-frame DSL `slides/anim/alg.tsx` with support for `lang: "rs"` (Rust highlighting) and `bad` (red
  lines with compiler errors); shared helpers are `slides/anim/rs.tsx` (`Box`, `arrow`, `rs`, `slot`); scenes of
  chapter N are `slides/anim/RsNN.tsx`, slides are `slides/learn-rust/chNN.tsx` (`SLIDES_R<N>`, key `"10:<N>"`).
- Code tasks of mode `rust` are checked like this: the reference runs in the sandbox, `expected` is taken from its output, the starter
  must fail (a compilation error or wrong output). Banning a technique (for example `.clone()`, `for`, `match`)
  is done through `include_str!("main.rs")` in the driver and counting a substring split into two parts
  (`concat!("ab", "cd")`), so that the driver itself does not contain it. "Fix…" tasks — the starter does not compile (E0382,
  E0499, E0502, E0505, E0597, E0106, etc.); mind two-phase borrows: `v.push(*first)` with `first = &v[0]`
  compiles, while `push(100); push(*first)` does not.
- Chapters 33–37 (Tokio: 34 time, timers and `select!`, 35 channels and synchronization, 36 network and asynchronous I/O, 37 cancellation, load and shutdown) and
  **44–51 "Chat: Axum, Sqlx, Tokio"** (44 routes, handlers, extractors; 45 state and tower layers; 46 JSON, serde and a unified error type;
  47 PostgreSQL and sqlx; 48 users: passwords, sessions, permissions; 49 rooms and messages: the chat REST API; 50 WebSocket; 51 a finished service: configuration,
  logs, shutdown, tests, packaging) — the same format: 13 scenes (`Rs34–Rs37.tsx`, `Rs44–Rs51.tsx`), quizzes `content/quizzes/rust-tokio.ts` and `rust-chat.ts`,
  30 tasks each (`rust_tasks/ch34–37.py`, `ch44–51.py`, mode `rust` with `standalone: True` and `crates: ['tokio']`). This is **one chat project growing through the chapters**: in chapters 49–51
  the tasks share a skeleton (table schema, users, `AppError`, the `CurrentUser` extractor), and the student writes the handlers.
  The sandbox image is `cs-core-rust-crates:1` (`backend/docker/rust-crates/Dockerfile`, built once: `docker build -t cs-core-rust-crates:1 backend/docker/rust-crates`):
  tokio full, tokio-stream/util, futures, bytes, axum (ws, macros), tower, tower-http, serde, serde_json, sqlx (PostgreSQL, chrono, uuid, json), tokio-tungstenite,
  argon2, sha2, hmac, base64, subtle, hex, rand, tracing, chrono, uuid. The runner supplies `--extern` from `/opt/ext/externs` (built by `mkext.sh` from the rlibs
  with which cargo built the root crate — dependencies sometimes have two builds). Tasks with the field **`postgres: True`** get a running PostgreSQL 17: the runner copies
  the ready cluster `/opt/pgdata` into tmpfs and starts it as the postgres user (`PG_START` in `runner.py`), the connection string is
  `postgres://postgres@127.0.0.1/chat`, every check gets a clean database. Version peculiarities: axum 0.8 (`/{id}`, `/{*rest}`, native async fn in `FromRequest`),
  sqlx 0.9 (dynamic SQL only through `sqlx::AssertSqlSafe(String)`), argon2 0.6 (`phc::PasswordHash`, `hash_password(pw)` takes the salt itself),
  tokio-tungstenite/axum ws (`Message::Text(Utf8Bytes)`). Without `test-util` time in Tokio cannot be "fast-forwarded" — use short real pauses
  and timeouts on every wait; for stability do not rely on the order of events between different connections.
- Voice-over is not done: all `cues` are computed by characters.

## Book 16 "From assembler to the C language": all 14 chapters written

The C language only, **no OS at all** (no fork, no sockets, no system calls: they are in the book "Diving into Unix").
Every construct is shown next to the RISC-V assembler from book 14. Sections: "Language basics" (1 first program, types,
compilation; 2 branching, loops, functions), "Memory and data" (3 pointers and arrays; 4 strings, structs, union;
5 dynamic memory and data structures), "Abstractions in C" (6 function pointers, qsort and callbacks;
7 preprocessor, macros and headers), "I/O and data" (8 stdio and buffering; 9 byte order, IEEE 754,
bit tricks), "Projects and tools" (10 multi-file projects, make, libraries; 11 UB, debugging, sanitizers),
"Going deeper" (12 hash tables, trees and heaps; 13 testing and style; 14 modern C: C11 and C23; the last paragraph is
a summary of the whole book). The table of contents `c-toc.md` was removed: the texts of all chapters live in `textbook/16-c/c-NN.md`.
Do not insert a chapter in the middle (the number is part of the slide, quiz and task keys and of the audio id `c-ch<N>-l<i>`).

- Scenes are `slides/anim/ClNN.tsx` (helpers `slides/anim/cl.tsx`: `cc` — C code, `asm` — RISC-V assembler, plus
  `Box`/`arrow`/`slot`); the DSL `alg.tsx` supports `lang: "c"` and `lang: "asm"`. Slides are `slides/learn-c/chNN.tsx`
  (`SLIDES_C<N>`, key `"16:<N>"`), quizzes are `content/quizzes/c.ts`. 13 paragraphs = 13 scenes in each chapter.
- Code tasks are mode `c` (`backend/app/exercises/c_tasks/`: `ch01_05.py` and `ch06.py … ch14.py`, 30 per chapter — 420 tasks; registry — `c_tasks/__init__.py`): the student writes functions, the hidden
  `driver` is `int main` (the student's code and the driver are glued into one file and built with `gcc 14` in the image
  `rust:1.97-slim`, no network; default flags `-std=gnu11 -O1 -Wall`, custom ones in the task field `flags`: for memory
  tasks — `-fsanitize=address,undefined -fno-sanitize-recover=all`, including LeakSanitizer). The driver **must not
  redefine the student's structs**; it prints results, `expected` is taken from the reference output. Banning a technique is
  done by reading `/sandbox/main.c` in the driver (`src_count`, the part before the marker `/*__DRIVER__*/`).
- Reference control: the solution passes, the starter does not (for infinite loops — by the 10 s timeout); efficiency is
  checked by large inputs. A reference whose output you have not checked by eye is not a reference: `expected` is computed from it.

## Book 15 "Computer Networks": fully written (20 chapters)

It comes right after "Linux" (field `ord` = 6, `audio_prefix` = `net-ch`). Four sections: "Network basics" (1–5), "Transport
layer" (6–9), "Application layer" (10–14), "Operations and security" (15–20). There is no table-of-contents file any more: each
chapter is a separate `textbook/15-networks/networks-NN.md` with its own `#SECTION`.

- A chapter = text (10 paragraphs of 65–90 words, Latin names and terms spelled out in Russian: "em-ti-yu", "eych-ti-ti-pi", "ti-el-es"),
  scenes `slides/anim/NtNN.tsx` (`V01…V10`, 4 frames each, helpers `anim/lx.tsx`; chapters 9, 14, 15, 18 have `Cd` code inserts),
  slides `slides/networks/chNN.tsx` (`SLIDES_NT<N>`/`SLIDE_TITLES_NT<N>`, key `"15:N"`), a quiz `content/quizzes/networks.ts`
  (5 questions) and practice. **Do not insert a chapter in the middle** (the number is part of the slide, quiz, task keys and of the audio id
  `net-ch<N>-l<i>`). No voice-over: `cues` are computed by character share.
- **Practice is a network simulator in the browser** (`frontend/src/netlab/`, mode `lab`; the package `exercises/net_tasks/` holds
  `lab_manifest.json` and the code tasks). The student connects devices with cables, configures addresses, routes, VLAN, NAT, firewall,
  DNS, HTTP, TLS, SSH, VPN, load balancers and runs Linux commands in a mini terminal; packets run along the scheme, with a log next to it.
  Exceptions — **chapters 9 and 14 are code in Python** (`net_tasks/ch09.py`, `ch14.py`: sockets over loopback, `http.server`, WebSocket,
  SSE, protobuf varint, gRPC frames; mode `stdout` with a driver, references checked in Docker, built by a script from `tkNN.py`).
- Devices: `host`, `server`, `router`, `switch`, `hub`, `internet` (the provider, does not route private addresses);
  `locked: true` — configuration is closed. The engine has no React:
  - `ip.ts`, `model.ts` (state, cables with `km`, `mbps`, `loss`, `mtu`), `sim.ts` (frames, ARP, a switch with VLAN and
    trunk, loops, hub, routing, TTL, ICMP, TCP session seq/ack/FIN, UDP, conntrack, MASQUERADE and DNAT, the FORWARD chain,
    MTU and DF, UDP tunnels, the L4 balancer `lb`, time in microseconds), `term.ts` (commands: `ip`, `ping -s -M`, `traceroute`,
    `curl -v -L -x`, `dig`, `nc`, `ss`, `sysctl`, `iptables`, `tcpdump`, `openssl s_client`, `ssh -J`, `ssh-keygen`,
    `iperf3`, `pageload` and the "admin" ones `dns`, `web`, `tls`, `trust`, `sshd`, `vpn`, `lb`, `rproxy`, `proxy`, `listen`, `close`);
  - `dns.ts` (authoritative servers, delegation, recursive resolver, cache), `http.ts` (routes, redirects, ETag, proxy,
    reverse proxy with cache), `tls.ts` (certificates, chain, versions, trust), `ssh.ts` (host keys, known_hosts, bastion),
    `transfer.ts` (download: receive window, cwnd, reno/cubic/bbr algorithms, queue), `pageload.ts` (HTTP/1.1, /2, /3),
    `capture.ts` (tcpdump), `attacks.ts` (ARP spoofing, SYN flood, scanner), `check.ts` (goals).
  - Goals (`check.ts`): `ping`, `tcp`, `udp` (options `expect`, `via`, `avoid`, `maxRttMs`, `seenSrc`, `warm`, `notSeenBy`, `noLoop`,
    `sizeFromMtu`), `http` (`status`, `header`, `bodyIncludes`, `follow`, `repeat`, `proxy`, `maxRttMs`, `fail`), `dns`, `xfer`,
    `page`, `lbspread`, `ssh`, `mtu`.
  - Interface: `components/NetPractice.tsx`, `netlab/react/NetLab.tsx` (board, goals, log, the `Chart.tsx` graph), `Board.tsx`,
    `DevicePanel.tsx` (forms by the `tools` flags: `cable`, `nat`, `fw`, `dns`, `http`, `tls`, `tcp`, `queue`, `proxy`, `lb`,
    `rproxy`, `ssh`, `vpn`, + terminal), styles `netlab.css`. The network state is a draft in the account, what is solved goes to
    `PUT /api/exercises/15/<chapter>/<id>/solved`.
  - Scenario: `netlab/scenarios/chNN.ts` → `{id, title, statement, hint, tools, build(), goals, solution}`; `solution` is the reference steps
    (`{cable}`, `{unlink}`, `{drop}`, `{cmd: [device, "string"]}`) or a function of the state. After edits:
    `cd frontend && npm run net:check` (the starter does not pass the goals, the reference does) and `npm run net:manifest`
    (writes `net_tasks/lab_manifest.json`), then `npm run tasks:export` (SQL for the DB) and reload the tasks:
    `cd backend && uv run seed_textbook.py --no-audio`.
  - Check the scene layout with the heuristic "text fits in cells, nothing is outside the canvas or overlapping" (the linter lives outside the
    repository); colors only `--s-*`.

## Book 17 "Virtualization": fully written (16 chapters)

It comes right after "Computer Networks" (field `ord` = 7, `audio_prefix` = `virt-ch`, the icon is in
`BookIcon.tsx`): it needs both Linux (KVM, cgroups, namespaces) and networks (virtio-net, bridges, veth).
16 chapters in five sections: "Virtualization basics" (1 why, and the Popek–Goldberg conditions, 2 trap-and-emulate,
the x86 problem, binary translation, paravirtualization, 3 VT-x/AMD-V, VM exit, ARM EL2, RISC-V H), "Memory and
I/O" (4 EPT/NPT, 5 ballooning/KSM, 6 virtio, 7 IOMMU/VFIO/SR-IOV), "Hypervisors and operations"
(8 KVM and QEMU, 9 qcow2, 10 live migration, 11 vCPU/NUMA/steal time), "Containers, cloud and security"
(12 containers versus VMs, 13 microVM and cloud, 14 security and confidential computing), "Practice and
extras" (15 nested virtualization, 16 practice with QEMU/KVM and observability).

- Chapters 1–16 are fully ready: texts `textbook/17-virtualization/virtualization-0N.md` (10 paragraphs of 70–85 words,
  Latin names spelled out in Russian: "vee-tee-iks", "kay-vee-em"), slides `slides/virtualization/chNN.tsx`
  (`SLIDES_VM<N>` / `SLIDE_TITLES_VM<N>`, key `"17:N"`), scenes `slides/anim/VmNN.tsx` (4 frames per paragraph, helpers
  `slides/anim/lx.tsx`, as in "Linux"), quizzes `content/quizzes/virtualization.ts` (5 questions per chapter) and 8 code tasks each
  in `exercises/virt_tasks/ch0N.py` (mode `func`: models of the monitor, traps, translation, VMCS, ARM and RISC-V, page
  tables, EPT and TLB, ballooning and KSM, virtio queues, IOMMU, VFIO and SR-IOV, KVM calls, qcow2 images and layers, live migration, NUMA,
  vCPU scheduling, containers and cgroups, microVM, side channels, RMP and attestation, nested
  virtualization and parsing the output of kvm_stat/perf/qemu-img/virsh).
  The reference of every task is checked in Docker: the solution passes, the empty starter does not.
- Interactive exercises (mode `lab`, simulators in the browser): `frontend/src/virtlab/` (`VirtLab.tsx` — the registry
  id → component, `goals.ts` — the goals hook `useGoals`, `virtlab.css`); the definitions are `exercises/virt_tasks/labs.py`
  (`LAB_TASKS`, placed first in the chapter list). They live among the code tasks: `CodePractice` on a task with
  `mode == "lab"` renders `VirtLab` instead of the editor, and `onSolved` sends `PUT /api/exercises/17/<chapter>/<id>/solved`.
  Six simulators, each with a model (pure js, tested on node) and an interface with goals:
  `virt-sim-hv` (chapter 2, `hv.ts` + `HvLab.tsx`: the student is the monitor, chooses emulation on traps, POPF and translation),
  `virt-sim-ept` (chapter 4, `ept.ts` + `EptLab.tsx`: shadow tables versus EPT, page sizes, TLB, four workloads),
  `virt-sim-virtqueue` (chapter 6, `virtq.ts` + `VirtqLab.tsx`: virtio rings, batches and notification suppression),
  `virt-sim-numa` (chapter 11, `numa.ts` + `NumaLab.tsx`: placing machines on nodes, vNUMA),
  `virt-sim-qcow2` (chapter 9, `qcow2.ts` + `Qcow2Lab.tsx`: snapshots, layers, merging, rollback),
  `virt-sim-migration` (chapter 10, `migration.ts` + `MigrationLab.tsx`: pre-copy, auto-converge, post-copy, three scenarios).
  A new simulator = model + component + an entry in `LABS` + a definition in `labs.py`; the goals must be reachable.
- Chapter numbers are part of the slide, quiz, task keys and audio ids (`virt-ch<N>-l<i>`): **do not insert a chapter in the middle**.
- No voice-over (see the mandatory rule at the beginning of the file): `cues` are computed by character share.

## Book 18 "System Design": fully written (24 chapters, 149 interactive exercises)

It comes after "Modern Frontend" (field `ord` = 11, `audio_prefix` = `sd-ch`, icon `layers`, slides directory
`system-design`). A classic course: from requirements and estimates to the final exam. Five sections: "Load basics"
(1 requirements, load and estimates; 2 scaling and balancing; 3 caching and CDN), "Data" (4 replication;
5 sharding; 6 consistency, CAP, idempotency; 7 search and file storage), "Asynchrony and resilience"
(8 queues and workers; 9 resilience patterns; 10 microservices and API gateway), "Typical systems" (11 real time:
WebSocket and chat; 12 news feed; 13 typical tasks: URL shortener, counters, identifiers, rate limiter),
"Operations" (14 observability and SLO; 15 zones and regions; 16 CI/CD and zero-downtime deployment; 17 cloud and cost),
"Final projects" (18 short-video service, 19 Google Drive, 20 Instagram, 21 taxi (Uber), 22 social network (VKontakte), 23 food delivery, 24 messenger:
each has 5–8 stages — the scheme of a stage is the starting point for the next — and an "from scratch" exam). **Do not insert a chapter in the middle** (the number
is part of the slide, quiz, task keys and of the audio id `sd-ch<N>-l<i>`).

- A chapter = text (13 paragraphs of 65–80 words, conversational Russian, Latin terms and abbreviations spelled out in Russian: "es-el-ou",
  "eych-ti-ti-pi"), scenes `slides/anim/SdNN.tsx` (`V01…V13`, 4 frames each; helpers `slides/anim/sd.tsx`: `X` — a node,
  `flow` — a row of nodes with arrows, `Bar` — a bar; on top of `dsl.ts` and `lx.tsx`), slides `slides/system-design/chNN.tsx`
  (`SLIDES_SD<N>`/`SLIDE_TITLES_SD<N>`, key `"18:N"`), a quiz `content/quizzes/system-design.ts` (5 questions per chapter).
  No voice-over: `cues` by character share. Scene lint is "text fits in cells, nothing overlaps or is outside the canvas".
- **Practice is the lab "scheme of a high-load service"** (`frontend/src/sdlab/`, mode `lab`; the package
  `exercises/sd_tasks/` holds `lab_manifest.json`). The student drags components onto the board, connects them, configures
  parameters (size, number of instances, TTL, replicas, shards, zones, tariff…), turns on failures ("Failure: zone, region,
  deployment, component") and sees the load of each node, p50/p99, availability and cost. A solution is accepted when
  all goals are met; the scheme is a draft in the account, what is solved goes to `PUT /api/exercises/18/<chapter>/<id>/solved`.
  The component is `components/SdPractice.tsx` (modeled on `NetPractice`), in `pages/chapters/exercises.tsx` — for book `18`.
  - The model (`engine.ts`, pure, deterministic, tested on node): requests of three classes — static, read, write
    — pass through the scheme as "decision trees" (CDN: hit/miss; cache: `cacheHit` = 0.95·√(size/working set)·TTL·
    (1 − 0.4·write share); queue: a write goes into a buffer, workers drain it at the rate `drain`; the limiter
    drops the excess). The node capacity is the table `REF` (server S/M/L = 300/700/1500 req/s, database — 1000/3000/8000
    reads and 200/600/1500 writes, cache — 60 000, worker S/M — 150/400, search — 1200 req/s and ≤ 40 GB per shard, WebSocket
    — 15 000 connections per gateway); latency grows as 1/(1 − load), p99 = 1.8·p50 + tail penalty; availability is the product
    over nodes (redundancy: 1 − (1 − a)ⁿ). Failures: `fail` = component kind, `zone` (minus a third with "three zones"),
    `region` (minus a half with "two regions"), `deploy` (all = everything, rolling = minus one, blue/green = nothing).
    Prices are in `REF` (server S/M/L — $60/120/240 per month, database — $100/250/600), reserved ×0.6, spot ×0.3, blue/green ×2, cache — $12 per GB. Additional parameters
    (`basic: false` in `kinds.ts`: retries, circuit breaker, idempotency keys, feed pull/push/hybrid, deployment, tariff,
    cache policy, synchronicity, shard key, DLQ) are shown only in exercises where they are listed in `show`.
  - The scheme board (`sdlab/react/Board.tsx`, ports and auto-links — `sdlab/ports.ts`) is modeled on the boards of book 14: a component has an input on the left
    and an output on the right, a link is dragged from an output to an input (or by clicking two ports; validity is `engine.canLink`, cycles and duplicates are forbidden);
    components can be dragged, they can be dragged from the palette onto the board, and **auto-completion** (`suggestEdges`) shows with a dashed line
    and creates links with the nearest suitable neighbors; pan and zoom is the shared hook `lab/react/useBoardView.tsx` (Ctrl + wheel, buttons).
    Auto-linking can be turned off in settings — separately for books 14 and 18 (`cs-core-autowire-lab`, `cs-core-autowire-sd`, `autoWireOn` in `lib/settings.ts`; read when the board opens).
    The "Link" mode no longer exists; exercise text must not refer to such a button.
  - Goals (`checks.ts`): `capacity` (the most loaded component), `util` (the load of a component of the given kind), `p99`, `p50`,
    `success`, `availability`, `cost`, `has`, `lacks`, `link`, `hit`, `cdnHit`, `survive` (after a failure successful ≥ 99%),
    `param`, `lag`, `replicaLag`, `shardShare`, `noSpof`. A new goal = a variant in `types.ts` + `describe` and `checkGoals`.
  - Scenario: `sdlab/scenarios/chNN.ts` → `SdScenario` (`id`, `title`, `statement`, `hint`, `workload`, `palette`, `start`,
    `goals`, `solution`, `show`); schemes are written with the helpers `N` (a node), `S(nodes, ["users>lb>app>db", …])` (layout and
    chains), `WL` (workload). The order of exercises in a chapter is the order in the array. After edits:
    `cd frontend && npm run sd:check` (**in the initial scheme at least one goal is not met, in the reference all are met**, the reference
    components are in the palette) and `npm run sd:manifest` (writes `sd_tasks/lab_manifest.json`), then `npm run tasks:export` and
    `cd backend && uv run seed_textbook.py --no-audio`. The numbers are chosen by calculation (a node script calls `evaluate`), not
    "by eye": the exercise statement and hint must match what the engine computes.
  - Chapters 18–24 ("projects") are built in stages: the scheme of each stage is the starting point for the next, the final exam
    starts from an MVP and requires assembling everything. In 19–24 the scheme is a builder function with `Opts` (`drive`, `insta`, `taxi`, `vk`, `food`, `chat`), the stages are
    constants `S1…S5`/`W1…W5`, the palettes `P1…P6` grow with the topic.
  - Component kinds added for projects: dependency services `auth`, `geo`, `ml`, `pay` (the share of requests that call
    them is `Workload.calls`; a needed service without a link ⇒ those requests fail; `geoUpdates` is the load on `geo`),
    `stream` as a side event log with consumers `worker`/`notify`/`analytics`, `notify` (push), `analytics`, the storage
    class `blob.tier` (hot/mix/cold) with `Workload.mediaTB`. `survive` requires N+1 headroom: losing a zone removes ⌈n/3⌉ instances, a region — ⌈n/2⌉.
    The project workload is `Workload` with `hotKey`, `monotonic`, `fanout`, `spikeSec`, `connections`/`msgPerConn`, `calls`.
  - At the bottom center of the board there is a "grip" for height (`.sd-resize`: drag with the mouse, double click — restore the default proportions; the height is stored in `cs-core-sd-board-h`, there is no grip in fullscreen).
  - Above the board, icons in the top-left corner: "?" (help and the number reference as a popup) and "fullscreen" (a portal into `body`, Esc closes);
    the parameters of the selected component are a floating card over the board (× closes), there is no separate panel; text inside nodes wraps to two lines.
- The pipeline for a new chapter: the text and quiz are a specification (a `chat/…`-like Python file → JSON), the generator creates
  `textbook/18-system-design/sd-NN.md`, `slides/system-design/chNN.tsx` and the quiz; scenes and lab scenarios are written by hand.

## Book 11 "Modern Frontend": history, language, HTML and CSS, browser, Node.js, build

Not about algorithms (they are in book 7) and not about frameworks: at the end we write our own mini-framework. **39 chapters** in eight sections (on 26–27.10.2026 the sections "HTML and markup" and "CSS and layout" were inserted, the chapter "CSS for programmers"
was removed, the rest were shifted by script across texts, slides, quizzes and tasks; the "chapter N" references inside texts and slides were fixed):
"History" (1 the birth of JavaScript, 2 Node.js and io.js, 3 ES5 → ES6, Babel, bundlers, preprocessors), "The JavaScript language" (4 first program
and values, 5 operators and type coercion, 6 functions and closures, 7 objects, arrays, Map/Set, JSON, 8 classes, prototypes, iterators;
9–10 modules, errors, promises and async/await; 11–12 functional programming), **"HTML and markup" (13 document, semantics and accessibility, 14 images,
media and tables, 15 forms and accessibility)**, **"CSS and layout" (16 selectors, states and specificity, 17 cascade, inheritance, units and variables, 18 box model, styling and positioning,
19 Flexbox, 20 Grid, 21 responsiveness, states and animations)**, "JavaScript in the browser" (22–28: 22 engine and event loop, 23 DOM, 24 events, 25 forms and
storage, 26 network, 27 Service Worker, 28 performance), "JavaScript in Node.js" (29 Node internals, 30 HTTP server, 31 runtimes: Deno, Bun),
"Build and packages" (32 package managers, 33 npm and JSR registries, 34 bundlers, 35 TypeScript and linters), "Your own mini-framework" (36 reactivity,
37 templates and virtual DOM, 38 components and router, 39 project build: Vite, tests, deploy). The texts are in `backend/data/textbook/11-js/js-NN.md`.
**Inserting and removing a chapter — only with a shift script** (the number is part of the text and slide file names, quiz and task keys, "chapter N" references in texts).

- Format is the same as in the other animated books: 13 paragraphs = 13 slides = 13 scenes (3 frames). The slides of chapters 1–12 and 16–34 are ready data
  `backend/data/slides/11-NN.json` (ported from the old TypeScript, edited directly), the slides of chapters 13–21 are the generators `packages/gen/src/web_ch13…21.rs`.
  Texts (conversational Russian: English words are spelled out in Russian — "nout", "jason", "ai-o-jey-es"); quizzes — `backend/data/sql/quizzes/11-js*.sql` (5 questions each).
- JS tasks are mode `js` (`backend/data/sql/tasks/11-js.sql`, 30 per chapter). The student's code and the hidden driver are glued into one ES module `main.mjs` and
  run by `node` in the image `node:22-alpine` (no network, `--max-old-space-size=256`, 10 s); the line-by-line `console.log` output is compared. The driver starts
  with the marker `/*__DRIVER__*/`; to forbid a technique, the driver reads `/sandbox/main.mjs` and counts substrings in the part before the marker. Because of ESM the order
  of `process.nextTick` and microtasks at the top level is the reverse of the familiar CommonJS one — do not rely on it in tests. There are no DOM tests: browser APIs
  are checked on mini-models (a node tree, an event bus) and pure functions. The reference of every task is checked: the solution passes, the empty starter does not.
- **The web lab (HTML and CSS)** — the section below: chapters 13–21 consist entirely of lab exercises (HTML markup, selectors, cascade, flexbox, grid, responsiveness, animations).
- Voice-over is not done (`cues` by characters), we do not touch it in this book until the end of work on the course.

## Web lab: HTML and CSS without a browser

The crate `packages/weblab` (shared between the wasm interface and the server): the student writes **markup**, **styles** or a **selector**, and checking does not start a browser.
The data is `backend/data/labs/web/<book>-<chapter:02>.json` (`LabChapter` with `lab: "web"`, tasks `{id, title, statement, hint, spec}`; the same exercises are
in the `tasks` table as rows with `mode = 'lab'` — SQL in `backend/data/sql/tasks`, files `11-js-html-NN.sql` and `11-js-css-NN.sql`; quizzes of chapters 13–21 — `quizzes/11-js-html-NN.sql`, `11-js-css-NN.sql`). `spec` is `weblab::Task`:
- `kind: "html"` — conditions on the student's markup: `exists`, `count`, `text`, `attr`, `child`, `order`, `forbid`, `headings` (one `h1`, levels without gaps), `labels`
  (captions on fields), `img_alt`, `doctype`, `clean_parse` (parsing by `html5ever` without errors; without a doctype the fragment is parsed as if it were present); `starter_html` is the starter;
- `kind: "css"` — the HTML is given (`html`, may contain `<style>` — these are the task styles, they come before the student's styles), the student writes CSS (`starter_css`); conditions:
  `style` (the computed value of a property on elements by selector: cascade with specificity, order, `!important`, the `style` attribute; inheritance, `var()`, `inherit/initial/unset`,
  shorthands `margin`/`padding`/`border`/`border-radius`/`flex`/`gap`/`font`/`background`/`transition`/`animation`/`place-*`/`outline`/`text-decoration` and logical `*-inline|block`,
  units `em`/`rem`/`vw`/`pt` → px, `calc()`/`clamp()`/`min()`/`max()` (without percentages) → px, colors (names, hex, `rgb()`, `hsl()`) → `rgb()`, `@media` by window width; condition fields: `equals`, `one_of`, `contains`, `min`/`max`,
  `any`, `viewport` (window width), `state` (`hover`/`focus`/`active`: rules with these pseudo-classes apply only in it), `pseudo` (`before`/`after`/…: pseudo-element styles), `container_width` (container width for `@container`),
  `env` (environment features for `@media`: `prefers-color-scheme: dark`, `prefers-reduced-motion: reduce`, `hover: none`, `pointer`, `orientation`)),
  `uses` (the student's CSS has a property and/or value; colors are compared after normalization), `media`, `container`, `keyframes` (`name`, `contains`), `no_important`, `no_ids`, `css_valid`;
  not counted: geometry and layout (column widths, box positions), `@layer`, `:not(:hover)`; so for flex and grid the property values are checked, and the student sees the result in the preview;
- `kind: "selector"` — the HTML is given, the student writes one selector: it must select exactly the elements whose `id` is in `want`; `max_specificity` limits its weight;
- `reference` — the reference, not given to the client (`public_spec` strips it); `weblab::verify::self_check` and the test `packages/weblab/tests/data.rs` require the reference to pass
  all conditions and the starter not to. Geometry, layout and pixels are not counted (a real engine is needed: a possible extension is Chromium in the worker sandbox).
- Server: `PUT /api/exercises/{book}/{chapter}/{id}/solved` with the body `{solution: "{\"html\": …, \"css\": …}"}` (for `selector` the selector is in `css`) re-checks with `weblab::verify`;
  the test `web_lab_accepts_references_and_rejects_starters` (`backend/tests/api.rs`). The interface is `frontend/app/src/components/labs/web.rs`: an editor (`highlight::Lang::Html`/`Css`),
  a preview in an `iframe` with an empty `sandbox` (widths 360/768/1100), the list of conditions is recomputed on every edit; for a selector the selected elements are outlined.
- New exercises are edits to the JSON and the `tasks` rows (the generator script is not kept in the repository: the files are canonical); first run `cd packages/weblab && cargo test`.

## What was removed and must not be brought back

- The lesson text as a reading page — no. The text is shown only by the "Off-screen" popup window at the bottom of the screen
  (`VoiceText` in `pages/chapter/theory.rs`): the paragraph of the current slide, words are highlighted as it is "read". The window is pinned to the bottom edge and centered on the area where it is shown (the chapter column `.content` or `.slide-fs-main` in fullscreen; `--vp-x`/`--vp-w`), the "Off-screen" caption is on top, tall by default (up to 12em of text); at the top there is a "grip" for height (drag up — taller, but not taller than the full text — only while there is scrolling; double click — default; `cs-core-voice-h`), the full window height is written to `--voice-h`, so the player and page margins do not hide under the window. While there is no
  wav, the player runs virtual clocks (`lib/voice.ts`, ~14 characters per second) — slides and `cues` follow them; when a
  part gets a file (the backend returns `dur` > 0), it plays, and the window stays.
- Code checking in the browser: checkers, Pyodide, web-tree-sitter were removed from
  the dependencies and from `frontend/public/`. Code is checked only through the
  Docker sandbox (`app/exercises/`). CodeMirror is only an editor
  (highlighting and input), without running or parsing code on the client. The only
  exception is the book 14 lab: the simulators of gates, Mini-8 and RISC-V are part of
  the exercise itself and run in the browser (this is not checking the user's Python).
- Code quizzes: quizzes are theory only.

## Miscellaneous

- Logs and wav probes are not committed; we do not keep code "just in case" — unused code is deleted (history is in git, the previous implementation is the tag `legacy-react-python`).
- `course.MD` is the course plan (the order of books in the left menu).
- Build and checks before a commit: `cd backend && cargo test`, `cd frontend && cargo test --workspace`, tests of the affected `packages` crates,
  `cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/slides`, when editing the interface — rebuild `e2e/.dist` and run the affected e2e modules.

