# Сборка Leptos-фронтенда (frontend) и Caddy: HTTPS, статика, /api → api. /internal (API воркеров) наружу не отдаётся.
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
COPY shared-rs/weblab shared-rs/weblab
COPY shared-rs/riscvlab shared-rs/riscvlab
COPY shared-rs/archlab shared-rs/archlab
COPY shared-rs/netlab shared-rs/netlab
COPY frontend frontend
WORKDIR /src/frontend/app
RUN CARGO_TARGET_DIR=/target trunk build --release --dist /dist

FROM caddy:2
COPY --from=web /dist /srv
COPY deploy/Caddyfile /etc/caddy/Caddyfile
