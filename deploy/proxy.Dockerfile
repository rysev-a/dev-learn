# Сборка Leptos-фронтенда (frontend) и Caddy: HTTPS, статика, /api → api. /internal (API воркеров) наружу не отдаётся.
FROM rust:1.98.1-bookworm AS web
RUN rustup target add wasm32-unknown-unknown
# trunk: готовый бинарь (cargo install собирал бы его минут десять); wasm-bindgen trunk скачает сам
ARG TRUNK=0.21.14
RUN curl -fsSL "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK}/trunk-$(uname -m)-unknown-linux-gnu.tar.gz" | tar -xz -C /usr/local/bin
WORKDIR /src
# общие крейты данных и движков лабораторий (подключаются путями ../packages)
COPY packages/content packages/content
COPY packages/highlight packages/highlight
COPY packages/sdlab packages/sdlab
COPY packages/virtlab packages/virtlab
COPY packages/weblab packages/weblab
COPY packages/riscvlab packages/riscvlab
COPY packages/archlab packages/archlab
COPY packages/netlab packages/netlab
COPY frontend frontend
WORKDIR /src/frontend/app
RUN CARGO_TARGET_DIR=/target trunk build --release --dist /dist

FROM caddy:2
COPY --from=web /dist /srv
COPY deploy/Caddyfile /etc/caddy/Caddyfile
