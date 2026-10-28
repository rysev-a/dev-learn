# Code checking: the queue and workers

Checking solutions (python, js, c, rust, sql) is the heaviest and the most dangerous part of the service: it runs someone else's code.
That is why the API **does not start containers itself**: a solution goes into a queue (`backend/src/jobs.rs`) and is executed by a worker (`worker/worker.py`, the sandbox is `worker/runner.py`).

```
browser ──POST /api/exercises/run──► API (VPS) ──► exec_jobs table ◄── claim (long polling, outgoing HTTPS) ── worker (VM at home)
   ▲                                                                                                                  │
   └──────── GET /api/exercises/run/{id} (queued → running → done) ◄── POST /internal/worker/jobs/{id}/result ◄───────┘
```

## Workers

There is no built-in worker: jobs are executed only by external `worker/worker.py` workers (Python, only the standard library + the Docker CLI) — for development one
is started next to the backend, in production — as a separate compose service with its own Docker daemon `dind` or on another machine. `CS_CORE_WORKER_TOKEN` is required
(a secret shared by the backend and the workers); without it `/internal/worker/*` responds with 404. If no worker has responded within 30 s, `POST /run` responds with 503
"checking is temporarily unavailable" (theory, quizzes and the in-browser labs keep working). State — `GET /api/exercises/runner/status`.
The queue is managed by a single backend instance (changes are made under a process lock).

## What the queue does

- Lanes: `light` (python, js, sql — seconds) and `heavy` (rust, c — compilation); a worker has its own slots for each.
- A user has at most one check at a time; the queue holds at most 300 jobs (otherwise 503).
- A job lease lasts 45 s, and the worker extends it with a heartbeat every 10 s; if it disappears, the job returns to the queue (two attempts,
  then the error "the checking server did not respond").
- An identical solution to the same version of an exercise is served from the cache (the cache lasts 7 days), no worker is needed.
- The attempt and the "solved" status are recorded by the API from the result; the worker has no access to the database.

## The sandbox (`worker/runner.py`)

`--network none`, memory/CPU/process limits, `--read-only`, tmpfs, `--cap-drop ALL`, `no-new-privileges`, `ulimit`,
the `nobody` user (except for PostgreSQL exercises: they need root and several capabilities), an output ceiling of 1 MB, the container
gets a name and is **stopped by name on timeout** (previously only the docker client was killed while the loop kept running),
at startup the worker removes forgotten `cs-core-run-*` containers.

## A worker on a home server

1. A VM (KVM: Proxmox/libvirt) in a separate network, with limits on cores/memory/disk. VM firewall: outgoing **only** to the VPS on port 443 (plus DNS and
   an update window), no access to the home network, no incoming connections (except SSH from the admin network). Once a day or on suspicion — roll back to a snapshot.
2. In the VM: Docker, the images `python:3.13-slim`, `rust:1.97-slim`, `node:22-alpine`, `cs-core-rust-crates:1`
   (`docker build -t cs-core-rust-crates:1 worker/docker/rust-crates`), the repository and `uv`.
3. Start (a systemd unit with `Restart=always`):

   ```
   cd worker && CS_CORE_WORKER_TOKEN=… uv run worker.py --server https://cs-core.example.com --name home-1 --light 4 --heavy 2
   ```

   On the VPS the backend is started with the same `CS_CORE_WORKER_TOKEN`.
4. Stronger isolation as the next step: gVisor (`--runtime=runsc`) inside the VM; queue and container-count metrics.

## What else is needed before a public launch

Rate limits on sign-up, login and `run` by IP (sign-up is already rate-limited), HTTPS, quotas on drafts. The deployment scheme is in `docs/deploy.md`.
