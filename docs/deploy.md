# How to deploy "cs-core"

The operational guide for whoever sets the service up is `docs/deploy-agent.md`; this document covers choosing a setup and the order of work.

## What runs

| Part | Image | Requirements | State |
|---|---|---|---|
| entry point | `traefik:v3.3` (routes: `deploy/traefik/http.yml` for development and `tls.yml` for the server; the Docker socket is not mounted) | ports 80/443 | stateless |
| site | `cs-core-proxy` (frontend: Caddy serving the wasm static files, ≈120 MB, not published externally) | — | stateless |
| backend | `cs-core-api` (axum, ≈400 MB) | ≈1 GB of memory; **exactly one instance** (the check queue is guarded by a process-level lock) | stateless, everything is in the database |
| database | `surrealdb/surrealdb:v3` | disk for `surrealkv`, ≈1 GB of memory | **the only storage**: users, progress, queue |
| worker | `cs-core-worker` (Python, ≈260 MB) | outbound HTTPS access to the backend | stateless |
| sandboxes | `dind` (a separate Docker daemon, `privileged`) + the `python`, `rust`, `node`, `cs-core-rust-crates` images (≈5–8 GB) | cores and memory for checks (`CS_CORE_SANDBOX_CPUS`, `CS_CORE_SANDBOX_MEM`) | images in the `dind-data` volume |
| backups | `backup` (`surreal export` once a day) | the `backups` volume | the last 14 `.surql` files |

The course content (texts, slides, exercise and quiz SQL, labs) is **baked into the `cs-core-api` image** and re-seeded into the database at startup if the hash of the sources has changed. So editing a text means a new build of `cs-core-api`; user data is not touched.

The load on the site is small: static files and short JSON requests. The expensive part is code checking: each check occupies a core for seconds (Python, JS, SQL) or tens of seconds (Rust, C). The queue and slots (`CS_CORE_LIGHT_SLOTS`, `CS_CORE_HEAVY_SLOTS`) protect the site from overload; the result cache keyed by the solution hash removes repeats.

## The main risk: other people's code

The sandbox isolates students' code (`--network none`, limits, `--cap-drop ALL`, `nobody`, `--read-only`), but it lives inside the `privileged` `dind` container. A sandbox escape + `privileged` = root on the host, and the host holds the database with users. This is what drives the order of the setups.

## Setups

**A. Everything on one machine (compose) — the start.** Suitable for a closed launch and the first users. A VPS with 4 vCPU / 8 GB / 80 GB of disk, rootful Docker 25+. Pro: one command, nothing else needed. Con: higher risk — other people's code next to the database. Mitigation: registration is closed or invitation-only, small slots, the sandbox image is not updated "on the fly", database backups are kept off the machine.

**B. Site and database on a VPS, worker on a separate machine (a VM at home or a second VPS) — the target setup.** The worker connects to the backend over HTTPS on its own, has no databases or user secrets, and can be rolled back to a snapshot. The code is already in place (`worker/worker.py --server https://…`, `docs/code-runner.md`). One configuration change is needed: Caddy currently blocks `/internal/*` for everyone outside. Options: (1) a separate address/port for workers with an IP allowlist and a token; (2) a private network between the machines (WireGuard/Tailscale) — then the worker goes straight to `api:8000` through the tunnel and Caddy stays as is (recommended).

**C. Kubernetes, managed services** — overkill for now: the backend must run as a single instance, and the sandboxes need a privileged Docker. Come back to this as the service grows.

Recommendation: **start with A on closed registration and prepare B right away**, because the move is just transferring the `worker`+`dind` services to another machine and changing `--server`; the data and the `cs-core-api`/`cs-core-proxy` images do not change.

## Order of work

1. **Preparation.** A domain (A/AAAA records pointing to the server), a VPS, SMTP for confirmation emails (without `SMTP_HOST`, emails are visible only in the admin tasks), secrets: `openssl rand -hex 32` for `CS_CORE_WORKER_TOKEN`, passwords `SURREAL_PASS`, `ADMIN_PASSWORD`.
2. **Building the images.** The backend takes a long time to build (10–20 minutes) and requires private libraries (the author's registry: the `LAB_TOKEN` token or a ready-made `cargo vendor` directory — `CS_CORE_VENDOR_DIR`). Currently the images are built
   on the server itself by the `deploy/server/release.sh` script (see "Release deployment" below); by hand the same is done with `docker build` for the three Dockerfiles, tagged `cs-core-api|proxy|worker:<tag>`,
   and `docker compose … up -d --no-build`. The image tag (`CS_CORE_TAG` in `.env`) is both the version and the rollback point. If an external registry is needed, the names are set with `CS_CORE_REGISTRY` (with a trailing slash) and `CS_CORE_TAG`.
3. **First launch** following `docs/deploy-agent.md`: `.env`, `up -d`, run `--profile checks --profile setup run --rm images` once (the sandbox images, 15–40 minutes), an end-to-end code check for each mode.
4. **External verification:** the e2e tests can run against a ready-made stack (`e2e/README.md`, "Against a ready-made stack"): logging in as a test user, walking through the chapters, the labs.
5. **Operations:** monitor the availability of `/api/exercises/runner/status` (`workers` ≥ 1, `available: true`) and of the home page; logs via `docker compose logs`; database backups must be **moved off the machine** (`rsync`/object storage): the `backups` volume on the same machine does not count as a backup; once a quarter, test the restore (`surreal import` into a clean database).
6. **Updates:** new build → `pull` → `up -d`. There is a single backend, so an update is an interruption of tens of seconds while it starts and checks the seed hash; the worker reconnects on its own. The sandbox images are updated separately (when `worker/docker/rust-crates` or the versions in `worker/runner.py` change → repeat the `images` step).
7. **Setup B:** bring up `worker`+`dind` on a second machine (`docker-compose` with these two services, `--server` pointing to the backend address through the tunnel), and remove them from the main stack.

## HTTPS

By default Traefik serves the site over HTTP only (`traefik/http.yml`: development and access by the machine's address). The production mode is enabled with three lines in `deploy/.env`:

```
CS_CORE_DOMAIN=cs-core.example.com
CS_CORE_TRAEFIK_CONFIG=./traefik/tls.yml
CS_CORE_URL=https://cs-core.example.com
```

Requirements: the domain's A record (and `www`) points to the server, and ports 80 and 443 are open to the outside. Traefik obtains a Let's Encrypt certificate itself (TLS-ALPN, the `traefik-acme` volume) and renews it;
HTTP is redirected to HTTPS, `www` to the domain without `www`, and the HSTS header is added. In this mode the site does not open by the machine's address without a domain. `ACME_EMAIL` (optional) is
the address for Let's Encrypt notifications.

## Release deployment (GitHub Actions)

Create a release on GitHub (not a draft and not a pre-release) — and a few minutes later the site is updated. The workflow is `.github/workflows/release.yml`; tests of the crates and the frontend on every push and PR are in `ci.yml`.

How it works:

1. Actions takes the sources by the release tag (`git archive`) and sends them to the server over SSH. The Actions key is dedicated, and in `~/.ssh/authorized_keys` it is allowed to run **only** `~/cs-core/release.sh`
   (`restrict,command="…"`): no shell and no port forwarding. The script is in the repository — `deploy/server/release.sh`; its copy on the server is updated manually (when the script changes).
2. The images are built **on the server**: the backend depends on private libraries (the author's registry) that the GitHub runner does not have; their sources are on the server in `~/cs-core-vendor`.
3. The script starts the stack with the new tag (`CS_CORE_TAG` in `~/cs-core/shared/.env`) and waits until the site responds at `https://domain/` and `/api/books`; if it does not, it **restores the previous tag** and exits with an error (the workflow turns red).
4. The three latest versions are kept (the `~/cs-core/releases/<tag>` directories and the `cs-core-*:<tag>` images). Manual rollback: set `CS_CORE_TAG=<previous tag>` in `shared/.env` and run `docker compose … up -d --no-build`
   (or create/re-publish a release with the old tag, or run the workflow manually: Actions → "Release deployment" → Run workflow → tag).

Configured once: the `DEPLOY_SSH_KEY` secret (the private key) and the `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_HOST_KEY` (the host fingerprint: a line from `known_hosts`), `SITE_URL` variables in Settings → Secrets and variables → Actions.
To make a deployment wait for approval, add required reviewers in Settings → Environments → `production`. Changing the server means new variable values and a new key (`ssh-keygen -t ed25519`, the public part in `authorized_keys` with the same restrictions).

Limitations: deployments do not overlap (`concurrency`); backend tests do not run in Actions (private libraries) — before a release, run `cd backend && cargo test` and the e2e tests locally; user data and settings
(`shared/.env`, the SurrealDB volume) are not touched by a deployment.

## Publishing images to Docker Hub

The images for running it yourself (README, "Running it yourself") are hosted on Docker Hub under the `alexeirysev` namespace: `cs-core-api`, `cs-core-proxy`, `cs-core-worker`, with the tags `<version>` and `latest`, for the `linux/amd64` and `linux/arm64` architectures.
They are published by `deploy/publish.sh <version> <image tag on the server>` **from an Apple Silicon computer**: `arm64` is built there (the backend needs private libraries — the `vendor` directory, which CI does not have),
`amd64` is pulled from the server where the release was built, and then a single multi-arch tag is created. You need `docker login` to Docker Hub and ssh access to the server. After deploying a release to the site, run the script with the same tag so the images match the site.
The first publication creates the repositories as public; the backend image contains the compiled code of the private libraries (no sources in it).

## Checklist before opening registration

- the administrator password and the worker token are generated, `DEMO_*` are not set;
- HTTPS works, the security headers are in place (the `secure` middleware in `deploy/traefik/tls.yml`), `/internal/*` returns 404 from outside;
- confirmation emails arrive (SMTP verified with a real mailbox);
- registration rate limiting is on (429 on a burst); consider limiting code checks per IP;
- the sandboxes are checked for escapes: `--network none` and the limits (`docs/code-runner.md`), `dind` is not published externally, the host socket is not mounted anywhere;
- database backups leave the machine, and restoring has been tested;
- disk headroom for images (`dind-data` grows when the sandbox images are updated).

## What has not been verified

A real server and domain; publishing images to the registry; setup B (the worker through a tunnel); load testing; restoring the database from a backup on a clean machine.
