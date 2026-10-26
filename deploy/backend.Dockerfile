# syntax=docker/dockerfile:1
#
# Бэкенд на axum + SurrealDB (каталог backend). Контекст сборки — корень репозитория.
#
# Общие crates (auth, auth_api, admin_api, system_tasks, mail, observability) лежат в приватном реестре `lab`: нужен токен gitness
# (секрет сборки `lab_token`; cargo читает индекс реестра, даже когда всё уже скомпилировано):
#   LAB_TOKEN=… docker build -f deploy/backend.Dockerfile --secret id=lab_token,env=LAB_TOKEN -t say-backend .
# Без доступа к реестру lab (нет сети до git.service-lab.dev) зависимости можно подложить готовым каталогом `cargo vendor`:
#   (cd backend && cargo vendor --locked /tmp/vendor-backend) и положить туда `.cargo-config.toml` (замена источников на /vendor),
#   затем `--build-context vendor=/tmp/vendor-backend` (в compose — переменная SAY_VENDOR_DIR). По умолчанию контекст vendor пуст
#   (deploy/no-vendor) и работает реестр с токеном.
# Быстрая сборка на готовом графе зависимостей lab (только amd64-хост и `docker login git.service-lab.dev`):
#   --build-arg BASE=git.service-lab.dev/lab/lab_images/backend.base:rust-1.98.1
#
# Содержимое курса (учебники, слайды, SQL упражнений/квизов) бэкенд читает при запуске из /app/data.
# Данные курса (crate content) общие с фронтендом и генераторами: лежат в packages и подключаются путём ../packages.
ARG BASE=rust:1.98.1-bookworm
FROM ${BASE} AS build
ENV CARGO_TARGET_DIR=/target
COPY backend/.cargo/config.toml /usr/local/cargo/config.toml
WORKDIR /src/backend
COPY packages/content /src/packages/content
COPY packages/highlight /src/packages/highlight
# движки лабораторий: сервер перепроверяет решения тем же кодом, что работает в браузере
COPY packages/sdlab /src/packages/sdlab
COPY packages/virtlab /src/packages/virtlab
COPY packages/weblab /src/packages/weblab
COPY packages/riscvlab /src/packages/riscvlab
COPY packages/archlab /src/packages/archlab
COPY packages/netlab /src/packages/netlab
COPY --from=vendor / /vendor
RUN if [ -f /vendor/.cargo-config.toml ]; then cat /vendor/.cargo-config.toml >> /usr/local/cargo/config.toml; fi
# слой зависимостей: пока не менялись манифест и lock, пересобираются только исходники
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
 && strip --strip-debug -o /out-server /target/release/say-backend

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /out-server /app/server
COPY backend/data/textbook /app/data/textbook
COPY backend/data/sql /app/data/sql
COPY backend/data/slides /app/data/slides
COPY backend/data/labs /app/data/labs
ENV DATA_DIR=/app/data BIND=0.0.0.0:8000 RUST_LOG=info
EXPOSE 8000
ENTRYPOINT ["/app/server"]
