# syntax=docker/dockerfile:1
#
# Бэкенд на axum + SurrealDB (backend-rs). Контекст сборки — корень репозитория.
#
# Общие crates (auth, auth_api, admin_api, system_tasks, mail, observability) лежат в приватном реестре `lab`: нужен токен gitness
# (секрет сборки `lab_token`; cargo читает индекс реестра, даже когда всё уже скомпилировано):
#   LAB_TOKEN=… docker build -f deploy/backend-rs.Dockerfile --secret id=lab_token,env=LAB_TOKEN -t say-backend-rs .
# Быстрая сборка на готовом графе зависимостей lab (только amd64-хост и `docker login git.service-lab.dev`):
#   --build-arg BASE=git.service-lab.dev/lab/lab_images/backend.base:rust-1.98.1
#
# Содержимое курса (учебники, слайды, SQL упражнений/квизов) бэкенд читает при запуске из /app/data — оно общее с Python-бэкендом.
# Данные курса (crate content) общие с фронтендом и генераторами: лежат в shared-rs и подключаются путём ../shared-rs.
ARG BASE=rust:1.98.1-bookworm
FROM ${BASE} AS build
ENV CARGO_TARGET_DIR=/target
COPY backend-rs/.cargo/config.toml /usr/local/cargo/config.toml
WORKDIR /src/backend-rs
COPY shared-rs/content /src/shared-rs/content
COPY shared-rs/highlight /src/shared-rs/highlight
# движки лабораторий: сервер перепроверяет решения тем же кодом, что работает в браузере
COPY shared-rs/sdlab /src/shared-rs/sdlab
COPY shared-rs/virtlab /src/shared-rs/virtlab
COPY shared-rs/riscvlab /src/shared-rs/riscvlab
COPY shared-rs/archlab /src/shared-rs/archlab
COPY shared-rs/netlab /src/shared-rs/netlab
# слой зависимостей: пока не менялись манифест и lock, пересобираются только исходники
COPY backend-rs/Cargo.toml backend-rs/Cargo.lock ./
RUN mkdir src && echo 'fn main() {}' > src/main.rs && : > src/lib.rs
RUN --mount=type=secret,id=lab_token,required=true \
    CARGO_REGISTRIES_LAB_TOKEN="Bearer $(cat /run/secrets/lab_token)" \
    cargo build --release --locked
COPY backend-rs/src ./src
RUN --mount=type=secret,id=lab_token,required=true \
    touch src/main.rs src/lib.rs \
 && CARGO_REGISTRIES_LAB_TOKEN="Bearer $(cat /run/secrets/lab_token)" \
    cargo build --release --locked \
 && strip --strip-debug -o /out-server /target/release/say-backend

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /out-server /app/server
COPY backend/app/data/textbook /app/data/textbook
COPY backend/app/data/sql /app/data/sql
COPY backend/app/data/slides /app/data/slides
COPY backend/app/data/labs /app/data/labs
ENV DATA_DIR=/app/data BIND=0.0.0.0:8000 RUST_LOG=info
EXPOSE 8000
ENTRYPOINT ["/app/server"]
