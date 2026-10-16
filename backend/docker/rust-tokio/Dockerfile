# Образ песочницы для упражнений с асинхронностью: rust:1.97-slim + заранее собранные tokio и родственные крейты.
# Сборка (нужна сеть один раз): docker build -t say-rust-tokio:1 backend/docker/rust-tokio
# Во время проверки сеть отключена: код ученика собирается напрямую rustc с --extern на готовые rlib.
FROM rust:1.97-slim

RUN cargo new --lib /opt/deps \
 && cd /opt/deps \
 && cargo add tokio --features full \
 && cargo add tokio-stream tokio-util futures bytes \
 && cargo add tokio-util --features full \
 && cargo build --release \
 && mkdir -p /opt/ext \
 && for name in tokio tokio_stream tokio_util futures futures_util futures_core futures_channel futures_task futures_sink futures_io bytes; do \
      f=$(ls target/release/deps/lib${name}-*.rlib 2>/dev/null | head -1); \
      [ -n "$f" ] && ln -sf "/opt/deps/$f" "/opt/ext/lib${name}.rlib"; \
    done \
 && ls /opt/ext
