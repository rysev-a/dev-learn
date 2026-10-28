#!/bin/sh
# One-off: loads the sandbox images into dind (DOCKER_HOST points to dind). The images live in the dind-data volume and survive restarts.
set -e
for img in python:3.13-slim rust:1.97-slim node:22-alpine; do
  echo "== pull $img"
  docker pull "$img"
done
echo "== build cs-core-rust-crates:1 (slow: tokio, axum, sqlx, PostgreSQL)"
docker build -t cs-core-rust-crates:1 /app/docker/rust-crates
docker image ls
