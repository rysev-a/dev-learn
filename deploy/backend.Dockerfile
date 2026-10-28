# syntax=docker/dockerfile:1
#
# Backend on axum + SurrealDB (the backend directory). Build context is the repository root.
#
# Shared crates (auth, auth_api, admin_api, system_tasks, mail, observability) live in the private `lab` registry: a gitness token is needed
# (build secret `lab_token`; cargo reads the registry index even when everything is already compiled):
#   LAB_TOKEN=… docker build -f deploy/backend.Dockerfile --secret id=lab_token,env=LAB_TOKEN -t cs-core-backend .
# Without access to the lab registry (no network to git.service-lab.dev) the dependencies can be supplied as a ready `cargo vendor` directory:
#   (cd backend && cargo vendor --locked /tmp/vendor-backend) and put `.cargo-config.toml` there (source replacement pointing to /vendor),
#   then `--build-context vendor=/tmp/vendor-backend` (in compose: the CS_CORE_VENDOR_DIR variable). By default the vendor context is empty
#   (deploy/no-vendor) and the registry with the token is used.
# Fast build on the ready lab dependency graph (amd64 host only, and `docker login git.service-lab.dev`):
#   --build-arg BASE=git.service-lab.dev/lab/lab_images/backend.base:rust-1.98.1
#
# The backend reads the course content (textbooks, slides, exercise/quiz SQL) from /app/data at startup.
# The course data (crate content) is shared with the frontend and generators: it lives in packages and is referenced by the path ../packages.
ARG BASE=rust:1.98.1-bookworm
FROM ${BASE} AS build
ENV CARGO_TARGET_DIR=/target
COPY backend/.cargo/config.toml /usr/local/cargo/config.toml
WORKDIR /src/backend
COPY packages/i18n /src/packages/i18n
COPY packages/locales /src/packages/locales
COPY packages/content /src/packages/content
COPY packages/highlight /src/packages/highlight
# lab engines: the server re-checks solutions with the same code that runs in the browser
COPY packages/sdlab /src/packages/sdlab
COPY packages/virtlab /src/packages/virtlab
COPY packages/weblab /src/packages/weblab
COPY packages/riscvlab /src/packages/riscvlab
COPY packages/archlab /src/packages/archlab
COPY packages/netlab /src/packages/netlab
COPY --from=vendor / /vendor
RUN if [ -f /vendor/.cargo-config.toml ]; then cat /vendor/.cargo-config.toml >> /usr/local/cargo/config.toml; fi
# dependency layer: while the manifest and lock are unchanged, only the sources are rebuilt
COPY backend/Cargo.toml backend/Cargo.lock ./
RUN mkdir src && echo 'fn main() {}' > src/main.rs && : > src/lib.rs
RUN --mount=type=secret,id=lab_token,required=false \
    CARGO_REGISTRIES_LAB_TOKEN="Bearer $(cat /run/secrets/lab_token 2>/dev/null)" \
    cargo build --release --locked
COPY backend/src ./src
RUN --mount=type=secret,id=lab_token,required=false \
    touch src/main.rs src/lib.rs \
 && CARGO_REGISTRIES_LAB_TOKEN="Bearer $(cat /run/secrets/lab_token 2>/dev/null)" \
    cargo build --release --locked \
 && strip --strip-debug -o /out-server /target/release/cs-core-backend

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /out-server /app/server
COPY backend/data/textbook /app/data/textbook
COPY backend/data/sql /app/data/sql
COPY backend/data/slides /app/data/slides
COPY backend/data/labs /app/data/labs
COPY backend/data/en /app/data/en
ENV DATA_DIR=/app/data BIND=0.0.0.0:8000 RUST_LOG=info
EXPOSE 8000
ENTRYPOINT ["/app/server"]
