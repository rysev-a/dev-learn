# Сборка Leptos-фронтенда (frontend-rs) и Caddy: HTTPS, статика, /api → api. /internal (API воркеров) наружу не отдаётся.
# Вариант прокси для стека на Rust (deploy/docker-compose.rust.yml); для Python-стека — proxy.Dockerfile (React).
FROM rust:1.98.1-bookworm AS web
RUN rustup target add wasm32-unknown-unknown
# trunk: готовый бинарь (cargo install собирал бы его минут десять); wasm-bindgen trunk скачает сам
ARG TRUNK=0.21.14
RUN curl -fsSL "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK}/trunk-$(uname -m)-unknown-linux-gnu.tar.gz" | tar -xz -C /usr/local/bin
WORKDIR /src
# общие крейты данных и движков лабораторий (подключаются путями ../shared-rs)
COPY shared-rs/content shared-rs/content
COPY shared-rs/highlight shared-rs/highlight
COPY shared-rs/sdlab shared-rs/sdlab
COPY shared-rs/virtlab shared-rs/virtlab
COPY shared-rs/riscvlab shared-rs/riscvlab
COPY shared-rs/archlab shared-rs/archlab
COPY shared-rs/netlab shared-rs/netlab
# стили общие с React-фронтендом: index.html подключает их из frontend/src
COPY frontend/src/App.css frontend/src/App.css
COPY frontend/src/lab/lab.css frontend/src/lab/lab.css
COPY frontend/src/netlab/netlab.css frontend/src/netlab/netlab.css
COPY frontend/src/sdlab/sdlab.css frontend/src/sdlab/sdlab.css
COPY frontend/src/virtlab/virtlab.css frontend/src/virtlab/virtlab.css
COPY frontend-rs frontend-rs
WORKDIR /src/frontend-rs/app
RUN CARGO_TARGET_DIR=/target trunk build --release --dist /dist

FROM caddy:2
COPY --from=web /dist /srv
COPY deploy/Caddyfile /etc/caddy/Caddyfile
