# CS.Core — an audio course on programming

A textbook "from zero to your own web service": 12 books, 316 chapters. Every chapter has slides with frame-by-frame animations, voice-over text, a theory quiz and hands-on practice right in the browser:
code is checked in an isolated sandbox, while circuits, networks, virtual machines, system design and HTML/CSS markup are checked by interactive labs.

**Site:** <https://cs-core.tech> — a trial launch on a single small machine. The service is still evolving and cannot yet handle heavy load:
when overloaded, code checking is temporarily unavailable (theory, quizzes and the in-browser labs keep working).
You can run the system yourself from prebuilt images — see ["Running it yourself"](#running-it-yourself).

> Status: MVP. The whole course is written, but there is no voice-over yet (slides advance on a timer, the paragraph text is shown in the "Voice-over" window); the voice will be generated once, when all books are ready.

## Books

| Book | Chapters | What it covers |
|---|---|---|
| Discrete Mathematics | 10 | the language of mathematics, counting and logic, graphs and probability |
| Python as a First Language | 52 | from the basics to the data model, metaprogramming, asynchrony and interpreter internals |
| Algorithms and Data Structures | 19 | complexity, hash tables, trees, heaps, graphs, dynamic programming |
| Computer Architecture | 22 | from the transistor and gates to the processor, RISC-V, cache and pipeline |
| From Assembler to C | 14 | the C language alongside RISC-V assembly |
| Diving into Unix | 17 | processes, the scheduler, memory, VFS, networking, containers, the kernel |
| Computer Networks | 20 | from the cable and Ethernet to TLS, DNS, HTTP/3 and security |
| Virtualization | 16 | VT-x, EPT, virtio, KVM, migration, containers, confidential computing |
| Databases | 32 | SQL and "under the hood": transactions, indexes, replication, sharding |
| Learning Rust | 51 | ownership, traits, Tokio, a server on Axum and Sqlx |
| Modern Frontend | 39 | JavaScript, HTML and CSS (markup, selectors, cascade, flexbox, grid, responsive design, animations), the browser, Node.js, bundling, your own mini-framework |
| System Design | 24 | from requirements and back-of-the-envelope estimates to designing Uber, Instagram, a messenger |

## What is inside a chapter

- **Look and feel:** light and dark color themes (Dracula, One Dark, Nord, Tokyo Night, Solarized, Monokai, GitHub Light, Gruvbox Light and others) for the site, slides and code editor — in the settings.
- **Theory:** animated slides (diagrams are built from data: cells, pointers, gates, regions, code) and the lesson's "Voice-over" text.
- **Questions:** a quiz; only the server knows the correct answers.
- **Practice:** code exercises (Python, JavaScript, SQL, C, Rust, tokio/axum/sqlx) are checked in a sandbox with no network and with limits; exercises with typed answers;
  **labs**: circuits made of gates, assembly and RISC-V, a network simulator, virtualization, a high-load service diagram, HTML and CSS (markup, selectors, cascade).
  Lab solutions are re-checked by the server with the same code that computes them in the browser.

## How it works

```
browser (Leptos, wasm) ──► Traefik ──► frontend (Caddy, static files)
                                   └─► backend (axum) ──► SurrealDB
                                            ▲
         worker (Python) ──► dind ──► sandboxes (python, node, rust, gcc, sqlite)   ← picks up jobs from the backend
```

- `backend/` — axum + SurrealDB: the course API, progress, the code-check queue, login. The course content is data in `backend/data` (texts, slides, SQL for exercises and quizzes, labs).
- `frontend/` — the Leptos interface (CSR, trunk).
- `packages/` — shared Rust crates: the slide and scene model, syntax highlighting, generators, lab engines (`sdlab`, `netlab`, `archlab`, `riscvlab`, `virtlab`, `weblab`).
  They run both in the browser (wasm) and on the server, where they verify submitted solutions.
- `worker/` — the code-check worker: takes jobs from the queue and runs sandboxes in a separate Docker daemon.
- `deploy/` — `docker compose` (Traefik, frontend, backend, SurrealDB, database backups, worker), Dockerfiles and the release script.
- `e2e/` — Playwright browser tests for every book and lab; `voice/` — voice-over (kokoro-ru), run once at the end.

## Running it yourself

Prebuilt images are on Docker Hub: [`alexeirysev/cs-core-api`](https://hub.docker.com/r/alexeirysev/cs-core-api) (backend),
[`alexeirysev/cs-core-proxy`](https://hub.docker.com/r/alexeirysev/cs-core-proxy) (the site), [`alexeirysev/cs-core-worker`](https://hub.docker.com/r/alexeirysev/cs-core-worker) (code checking).
Nothing needs to be built, and the data stays with you.

**Platforms.** These are Linux container images built for two CPU architectures — `linux/amd64` (Intel and AMD) and `linux/arm64` (Apple Silicon, ARM servers); Docker picks the right one itself.
Supported: **Linux**, **macOS** (Intel and Apple Silicon, via Docker Desktop), **Windows** (Docker Desktop with WSL2). You need Docker with Compose v2 and 2–4 GB of free memory
(for code checking — 8 GB and 15 GB of disk).

```bash
git clone https://github.com/rysev-a/dev-learn.git && cd dev-learn
cp deploy/.env.example deploy/.env
```

Open `deploy/.env` and set the following (you can leave the rest alone):

```bash
CS_CORE_URL=http://localhost
CS_CORE_HTTP_PORT=8080                         # the site's port on your machine
CS_CORE_HTTPS_PORT=8443
CS_CORE_WORKER_TOKEN=paste-the-output-of-openssl-rand-hex-32
SURREAL_PASS=choose-a-database-password
ADMIN_EMAIL=you@example.com                # administrator login
ADMIN_PASSWORD=at-least-8-characters
```

Start it:

```bash
export CS_CORE_REGISTRY=alexeirysev/ CS_CORE_TAG=latest        # or a specific version, for example 0.1.0
docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --no-build
```

The site is at <http://localhost:8080>. The first start takes about a minute: the backend seeds the course into the database. Sign up on the site or log in as the administrator. To stop: `docker compose -f deploy/docker-compose.yml --env-file deploy/.env down` (data is kept in the volume).

**Code checking (optional).** Theory, quizzes and the in-browser labs work right away. To have code exercises checked, enable the `checks` profile — the worker and a separate Docker daemon for sandboxes
(it runs in a `privileged` container as its own daemon; your Docker is not affected):

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile checks up -d --no-build
docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile checks --profile setup run --rm images   # once: the sandbox images, 15–40 minutes
```

Sandbox resources are limited by the variables `CS_CORE_SANDBOX_CPUS`, `CS_CORE_SANDBOX_MEM`, `CS_CORE_LIGHT_SLOTS`, `CS_CORE_HEAVY_SLOTS`, and the queue ceiling by `CS_CORE_QUEUE_LIMIT` (see `deploy/.env.example`).
Tested on Linux x86_64 and on macOS with Apple Silicon.

## Local run and development

- **The frontend and shared crates** build from the repository without private dependencies:
  ```bash
  rustup target add wasm32-unknown-unknown && cargo install trunk
  cd frontend/app && trunk serve              # http://127.0.0.1:7054, /api is proxied to 127.0.0.1:8001
  cd packages/weblab && cargo test            # tests of any crate in packages/
  cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/slides   # slide check
  ```
- **The backend** uses the author's shared libraries from a private registry (`auth`, `admin_api`, `mail` and others), so it does not build from someone else's clone. The author runs:
  ```bash
  cd backend && SURREAL_USER=root SURREAL_PASS=devpass BIND=127.0.0.1:8001 CS_CORE_WORKER_TOKEN=dev \
    DEMO_USER_EMAIL=student@mail.com DEMO_USER_PASSWORD=student \
    DEMO_ADMIN_EMAIL=programmer@mail.com DEMO_ADMIN_PASSWORD=programmer cargo run     # without SurrealDB it runs on an in-memory database
  cd worker && CS_CORE_WORKER_TOKEN=dev uv run worker.py --server http://127.0.0.1:8001 --name dev --light 2 --heavy 1   # code checking (needs Docker)
  ```
- **The whole stack in Docker:** `deploy/docker-compose.yml` (Traefik, frontend, backend, SurrealDB, database backups; the `checks` profile — the worker and sandboxes), see [`docs/deploy.md`](docs/deploy.md).
- **Browser tests:** `cd e2e && npm ci && npm test` (the built frontend and backend are required, see `e2e/README.md`).

## Server, domain and release

The deployment scheme, HTTPS via Traefik and Let's Encrypt, backups, updates — [`docs/deploy.md`](docs/deploy.md); a step-by-step guide for whoever deploys the service — [`docs/deploy-agent.md`](docs/deploy-agent.md);
how code checking and the workers work — [`docs/code-runner.md`](docs/code-runner.md). Releases to the site go out automatically when a release is created on GitHub (`.github/workflows/release.yml`).

## How to add or fix content

The course is data: texts in `backend/data/textbook`, slides in `backend/data/slides` (chapters 13–15 of book 11 and a few others are generators in `packages/gen`), quizzes and exercises as SQL in `backend/data/sql`, labs as JSON in `backend/data/labs`.
The rules (paragraph = scene = part, colors, format) are in [`AGENTS.md`](AGENTS.md). After making changes: run the tests of the relevant `packages/` crates and `cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/slides`.

## License

See [LICENSE](LICENSE).
