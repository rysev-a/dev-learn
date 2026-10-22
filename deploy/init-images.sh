#!/bin/sh
# Разово заливает в dind образы песочниц (DOCKER_HOST указывает на dind). Образы лежат в томе dind-data и переживают перезапуск.
set -e
for img in python:3.13-slim rust:1.97-slim node:22-alpine; do
  echo "== pull $img"
  docker pull "$img"
done
echo "== build say-rust-crates:1 (долго: tokio, axum, sqlx, PostgreSQL)"
docker build -t say-rust-crates:1 /app/docker/rust-crates
docker image ls
