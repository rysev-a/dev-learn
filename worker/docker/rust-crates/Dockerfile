# Sandbox image for Rust exercises with crates: rust:1.97-slim + prebuilt tokio, axum, sqlx (PostgreSQL),
# serde, tower, tungstenite, argon2, etc., plus a PostgreSQL server with a ready cluster at /opt/pgdata
# (the runner starts it before a check: see PG_START in worker/runner.py). Build (network needed once):
#   docker build -t cs-core-rust-crates:1 backend/docker/rust-crates
# During a check the network is off: student code is built directly with rustc, and --extern for all prebuilt rlibs
# is in /opt/ext/externs (one `--extern name=path` line each).
FROM rust:1.97-slim

RUN cargo new --lib /opt/deps \
 && cd /opt/deps \
 && cargo add tokio --features full \
 && cargo add tokio-stream tokio-util futures bytes serde_json tracing rand \
 && cargo add tokio-util --features full \
 && cargo add serde --features derive \
 && cargo add axum --features ws,macros \
 && cargo add tower --features util,limit,timeout \
 && cargo add tower-http --features cors,trace,timeout,limit \
 && cargo add sqlx --no-default-features --features runtime-tokio,postgres,migrate,derive,chrono,uuid,json \
 && cargo add tokio-tungstenite \
 && cargo add argon2 \
 && cargo add http-body-util \
 && cargo add chrono --features serde \
 && cargo add sha2 hmac base64 subtle hex \
 && cargo add uuid --features v4,serde \
 && cargo build --release --message-format=json > /tmp/build.json

COPY mkext.sh /tmp/mkext.sh
RUN sh /tmp/mkext.sh

# PostgreSQL: the cluster is initialised once at build time (trust access from 127.0.0.1, database chat);
# during a check (read-only root FS) the runner copies it to /tmp and starts it as the postgres user.
RUN apt-get update \
 && apt-get install -y --no-install-recommends postgresql \
 && rm -rf /var/lib/apt/lists/* \
 && PGBIN=$(ls -d /usr/lib/postgresql/*/bin | head -1) \
 && ln -s "$PGBIN" /opt/pgbin \
 && mkdir -p /opt/pgdata && chown postgres /opt/pgdata \
 && runuser -u postgres -- /opt/pgbin/initdb -D /opt/pgdata --auth=trust --encoding=UTF8 --locale=C.UTF-8 >/dev/null \
 && runuser -u postgres -- /opt/pgbin/pg_ctl -D /opt/pgdata -o "-c listen_addresses=127.0.0.1 -c unix_socket_directories=/tmp" -w start >/dev/null \
 && runuser -u postgres -- /opt/pgbin/createdb -h 127.0.0.1 chat \
 && runuser -u postgres -- /opt/pgbin/pg_ctl -D /opt/pgdata -m fast -w stop >/dev/null \
 && du -sh /opt/pgdata
