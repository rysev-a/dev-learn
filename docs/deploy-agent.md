# Agent instructions: deploy "cs-core" on a server with docker compose

This is a step-by-step guide for an agent (or a human) deploying the service on **a single machine that has only Docker with the compose plugin**
(no Rust, Python or Node is needed on the host). Choosing a scheme and the order of work are covered in `docs/deploy.md`.

Stack composition (`deploy/docker-compose.yml`, project `cs-core`):

| Service | What it is |
|---|---|
| `traefik` | entry point: ports 80/443, routes in `deploy/traefik/http.yml` (development) or `tls.yml` (domain and HTTPS) (`/api` → `api`, everything else → `proxy`); the Docker socket is not mounted |
| `proxy` | frontend: Caddy serving the Leptos static files (`frontend/`, trunk builds the wasm inside the image); not published externally, `/internal` returns 404 |
| `api` | axum backend (`backend/`): on startup it seeds the course content into SurrealDB, runs the check queue and the worker API |
| `surrealdb` | database (volume `surreal-data`, port 8000 only inside the network; `127.0.0.1:18000` is published for development) |
| `worker` | (profile `checks`) code-check worker: takes jobs from `api` and runs sandboxes |
| `dind` | (profile `checks`) a **separate** Docker daemon (`privileged`) used only for sandboxes; images live in the `dind-data` volume |
| `backup` | once a day exports SurrealDB (`surreal export` over HTTP, files `cs-core-*.surql`) to the `backups` volume (the 14 latest are kept) |
| `images` | one-off task (profile `setup`): loads the sandbox images into `dind` |

Verified locally: building all images, startup, registration, closed `/internal`, the worker connects, code checking works through the whole chain
(`api` → queue → `worker` → `dind` → result), and the e2e tests run against a ready stack (`e2e/README.md`, "Against a ready stack"). Building the `cs-core-rust-crates:1` image
and checking Rust/C/JS tasks take a long time — verify them on the server (step 6).

---

## 0. Rules (must not be violated)

1. **Do not mount the host's `/var/run/docker.sock` into any container** and do not publish `dind` port `2375` externally: student code runs in `dind`, and the host socket means root on the machine.
2. **Do not set `DEMO_USER_*`/`DEMO_ADMIN_*`** (demo users without a password policy — for development only): on the server the administrator is set via `ADMIN_EMAIL`/`ADMIN_PASSWORD`.
3. **Do not commit secrets**: `deploy/.env` stays out of git (`.dockerignore` and `.gitignore` rules); the token lives only there.
4. `api` has no Docker and no built-in worker: code is checked only by the separate `worker`. Do not give `api` access to docker.
5. Do not delete the `surreal-data` volume (the database with user progress) or `backups` without an explicit instruction from the owner. `docker compose down -v` wipes **all** volumes — do not use it on a production server.
6. We do not synthesize or generate audio (project rule, see AGENTS.md): no audio goes into the `api` image.
7. If anything is unclear, breaking or irreversible (deleting data, opening ports, changing the domain after a certificate has already been issued) — stop and ask the owner.

---

## 1. What to find out from the owner before starting

- The site's **domain** (for example `cs-core.example.com`) and whether its DNS `A`/`AAAA` records point to the server. Without a domain you can verify over HTTP: `CS_CORE_SITE=:80`.
- **Whether ports 80 and 443 are free** on the server. If another proxy (Traefik/nginx) already holds them — see step 3, the "behind an existing proxy" option.
- **How many cores and how much memory** to give the sandboxes (`CS_CORE_SANDBOX_CPUS`, `CS_CORE_SANDBOX_MEM`): this is the ceiling for all code checks combined. Recommendation: 50–70% of cores and memory, the rest stays for the site.
- How to get the code: repository `git@github.com:rysev-a/dev-learn.git` (branch `main`); access is required (a deploy key or a token). Ask where to keep the code (for example `/opt/cs-core`).

## 2. Check the server

```bash
docker version && docker compose version     # compose v2+
nproc; free -h; df -h /var/lib/docker       # cores, memory, disk space (sandbox images ≈ 5–8 GB, the rust image with crates is the largest)
docker info | grep -iE "storage driver|cgroup"   # overlay2, cgroup v2 preferred
```

Required: Docker 25+, compose v2, ≥ 20 GB free on the Docker disk, `privileged` containers allowed (rootful Docker). Rootless Docker and "unprivileged sandboxes"
do not work for `dind`. If server policy forbids `privileged` — stop and ask the owner (the alternative is a separate machine for the worker, scheme B in `docs/deploy.md`).

## 3. Preparation

```bash
git clone git@github.com:rysev-a/dev-learn.git /opt/cs-core && cd /opt/cs-core     # confirm the path with the owner
cp deploy/.env.example deploy/.env
```

Fill in `deploy/.env`:

```bash
# token (shared secret between the API and the worker)
sed -i "s/^CS_CORE_WORKER_TOKEN=.*/CS_CORE_WORKER_TOKEN=$(openssl rand -hex 32)/" deploy/.env
```

And by hand: `SURREAL_PASS` (the SurrealDB root password), `ADMIN_EMAIL` and `ADMIN_PASSWORD` (the initial administrator, login by email, password ≥ 8 characters),
if needed `SMTP_*`/`MAIL_FROM` (without `SMTP_HOST` confirmation emails go nowhere), `CS_CORE_SITE` (domain), `CS_CORE_SANDBOX_CPUS`, `CS_CORE_SANDBOX_MEM`, `CS_CORE_LIGHT_SLOTS`/`CS_CORE_HEAVY_SLOTS` (slots must not exceed `CS_CORE_SANDBOX_CPUS`; usually `light = cores`, `heavy = cores/2`).

**Ports and HTTPS.** The entry point is the Traefik from this same compose: it listens on `CS_CORE_HTTP_PORT` (80 by default) and `CS_CORE_HTTPS_PORT` (443). If those ports on the machine are already taken by someone else's proxy,
set different ones and point that proxy at `127.0.0.1:<CS_CORE_HTTP_PORT>` (it then handles HTTPS and the certificate). While there is no domain, the site works over HTTP at the machine's address; with a domain — `CS_CORE_DOMAIN`, `CS_CORE_TRAEFIK_CONFIG=./traefik/tls.yml`
(the Let's Encrypt certificate is obtained automatically) — `docs/deploy.md`, section "HTTPS". The `proxy` service (frontend) is not published externally.

**Crates registry token.** Shared libraries live in the private `lab` registry (gitness); without a token the backend will not build. The owner provides the token (in `~/.cargo/credentials.toml`
on their machine there is a line `[registries.lab] token = "Bearer …"`); it is passed **only** through the environment during the build (`LAB_TOKEN=<token without the word Bearer>`) and is never written to files or git.

**No network access to the `lab` registry** (error `Failed to connect to git.service-lab.dev`): supply the dependencies as a ready-made directory. On a machine where the registry is reachable (or
the cargo cache exists): `cd backend && cargo vendor --locked /path/vendor-backend`, then put a `.cargo-config.toml` file into that directory (source replacement with `/vendor`:
`[source.crates-io] replace-with`, `[source."sparse+https://git.service-lab.dev/pkg/lab/lab_crates/cargo/index/"] registry = … replace-with = "vendored-sources"`,
`[source.vendored-sources] directory = "/vendor"`) and set `CS_CORE_VENDOR_DIR=/path/vendor-backend` in `deploy/.env`. By default (`deploy/no-vendor`) the registry with a token is used.

Check the configuration:

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env config -q && echo OK
```

## 4. First launch

```bash
LAB_TOKEN=… docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --build
docker compose -f deploy/docker-compose.yml --env-file deploy/.env ps
```

The first build is long (10–20 minutes: the backend with the SurrealDB client and the wasm frontend). On first start `api` seeds the course into SurrealDB (≈ 5–15 s) — until then it is `starting`, and `proxy` and `worker` wait for it.
Expected: all services `Up`, `api` and `dind` are `healthy`.

## 5. Sandbox images (once)

Code checking does not work until `dind` has the images. They are stored in the `dind-data` volume and survive restarts.

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile checks --profile setup run --rm images
```

This pulls `python:3.13-slim`, `rust:1.97-slim`, `node:22-alpine` and **builds `cs-core-rust-crates:1`** (tokio, axum, sqlx, PostgreSQL — long, 15–40 minutes and several GB; `dind` needs internet access).
If the build failed — read the output (usually network/DNS or lack of space) and repeat; already downloaded layers are kept.

Verify: `docker compose -f deploy/docker-compose.yml --env-file deploy/.env exec dind docker image ls`.

## 6. Verify operation (mandatory, after every release)

Substitute your own address (`https://<domain>` or `http://<machine address>:<CS_CORE_HTTP_PORT>`):

```bash
BASE=https://cs-core.example.com
curl -s -o /dev/null -w "home %{http_code}\n" $BASE/                    # 200
curl -s -o /dev/null -w "api     %{http_code}\n" $BASE/api/books           # 200
curl -s -o /dev/null -w "internal %{http_code}\n" $BASE/internal/worker/jobs   # 404 — the worker API is closed to the outside
curl -s $BASE/api/exercises/runner/status                                  # {"queued":0,"running":0,"workers":1,"available":true}
```

`workers: 1` and `available: true` mean the worker has connected. Then an end-to-end code check (login and registration are by **email**, afterwards use the `Authorization: Bearer <token>` header):

```bash
J='content-type: application/json'
curl -s -X POST $BASE/api/auth/signup -H "$J" -d '{"email":"check@example.com","password":"check-pass-12345","name":"check"}'
TOKEN=$(curl -s -X POST $BASE/api/auth/login -H "$J" -d '{"email":"check@example.com","password":"check-pass-12345"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
RES=$(curl -s -X POST $BASE/api/exercises/run -H "$J" -H "Authorization: Bearer $TOKEN" -d '{"book":13,"chapter":0,"task":"intro-variable","code":"year = 1991\nprint(year)"}')
ID=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
sleep 5; curl -s -H "Authorization: Bearer $TOKEN" $BASE/api/exercises/run/$ID      # "state":"done" ... "solved":true
```

Registrations are rate-limited (429) — this is normal. Then check one task of each mode (after step 5): JS (book 11), C (book 16), Rust (book 10, chapter 1);
the reference solutions are in `backend/data/sql/tasks/*.sql` (the `spec` field). The e2e book tests perform the same check (`e2e/README.md`).

Also: open the site in a browser, register, open any chapter, the slides and an exercise (if you have browser access).

## 7. Updating

```bash
cd /opt/cs-core && git pull
LAB_TOKEN=… docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --build
```

`LAB_TOKEN` (or `CS_CORE_VENDOR_DIR`) is required. On startup `api` re-seeds the course content only if the source hash has changed; user progress is not affected.
The backend must run as a **single instance** (the check queue is guarded by a process lock). Sandbox images need updating only if
`worker/docker/rust-crates` or the image versions in `worker/runner.py` changed (then repeat step 5; the check cache is stored in the database and expires on its own after 7 days).
After the release, repeat step 6.

## 8. Backups and restore

Once a day the `backup` service puts a SurrealDB export into the `backups` volume (`cs-core-YYYYMMDD-HHMMSS.surql`, the latest 14). This is **not enough**: the volume lives on the same machine. Agree with the owner on an off-site copy (cron + `rsync`/object storage).

Get a copy out of the volume:

```bash
docker run --rm -v cs-core_backups:/b -v "$PWD":/out alpine sh -c 'cp "$(ls -t /b/cs-core-*.surql | head -1)" /out/cs-core-latest.surql'
```

Restore: stop `api`, run `surreal import` into a clean database (namespace `stack`, database `cs-core`), start `api`. Course data does not need to be restored — the seed recreates it from files;
what matters in the copy is users and progress.

## 9. Logs and diagnostics

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env logs --tail 100 api worker dind proxy
```

| Symptom | Cause and what to do |
|---|---|
| `dind` does not become `healthy` | `privileged` and rootful Docker are required; check `docker compose logs dind` (often no `overlay`/cgroup or low disk space). Do not replace it with mounting the host socket |
| `api` stays `starting` for a long time | the first seed is running (`start_period: 180s`) or there is no connection to `surrealdb`; look at `logs api surrealdb`. With `DB_STRICT=1` the backend does not start without a database |
| `status` shows `workers: 0`, checks return 503 | the worker has not connected: `logs worker` (wrong `CS_CORE_WORKER_TOKEN`, `api` not `healthy`, no connection to `dind`); the token in `.env` is the same for `api` and `worker` — after editing, recreate both (`up -d`) |
| A check hangs in "Queued" | no free slots (`CS_CORE_LIGHT_SLOTS`/`CS_CORE_HEAVY_SLOTS`) or no image in `dind`: run step 5 |
| In the sandbox "file not found" / empty directory | the sandbox directory path does not match: the worker must have `TMPDIR=/sandboxes`, and the `sandboxes` volume must be mounted in both `worker` and `dind` at `/sandboxes` (as in compose; do not change it) |
| the site does not open from outside | `docker compose ps`: `traefik` must be `healthy`; ports `CS_CORE_HTTP_PORT`/`CS_CORE_HTTPS_PORT` must be free and open in the firewall; routes are in `deploy/traefik/http.yml` or `tls.yml` |
| The `api` build fails on `git.service-lab.dev` | no token or no network to the registry: `LAB_TOKEN` or `CS_CORE_VENDOR_DIR` (step 3) |
| Need to stop everything | `docker compose -f deploy/docker-compose.yml --env-file deploy/.env stop` (volumes are kept) |

Resource limits for all sandboxes at once are set by `dind` (`CS_CORE_SANDBOX_CPUS`/`CS_CORE_SANDBOX_MEM`). If the site slows down during checks — reduce them and the slots, then restart `dind` and `worker`.

## 10. What to report to the owner after deployment

- the site address and which checks from step 6 you ran (with the command results);
- which sandbox images are loaded and which modes (`python`, `js`, `c`, `rust`, `sql`) were actually verified by an end-to-end check;
- the chosen limits and slots (`.env` without secrets), where the code and the volumes are;
- what is **not** done: off-site backup copy, monitoring, rate limits on registration and login by IP (`docs/deploy.md`, the checklist — they are mandatory before registration is opened to the public);
- any deviations from this guide and the reasons for them.
