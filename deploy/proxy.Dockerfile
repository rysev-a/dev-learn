# Build of the Leptos frontend (frontend) and Caddy: HTTPS, static files, /api -> api. /internal (the worker API) is not exposed outside.
FROM rust:1.98.1-bookworm AS web
RUN rustup target add wasm32-unknown-unknown
# trunk: a prebuilt binary (cargo install would build it for about ten minutes); trunk downloads wasm-bindgen itself
ARG TRUNK=0.21.14
RUN curl -fsSL "https://github.com/trunk-rs/trunk/releases/download/v${TRUNK}/trunk-$(uname -m)-unknown-linux-gnu.tar.gz" | tar -xz -C /usr/local/bin
WORKDIR /src
# shared data and lab engine crates (referenced by the ../packages paths)
COPY packages/i18n packages/i18n
COPY packages/locales packages/locales
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
