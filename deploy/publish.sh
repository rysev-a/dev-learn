#!/bin/bash
# Публикация образов в Docker Hub: один тег на две архитектуры (linux/amd64 и linux/arm64).
#   amd64 — забирается с сервера, где собран релиз (там x86_64);
#   arm64 — собирается здесь (Mac на Apple Silicon или любая ARM-машина), потому что бэкенду нужны закрытые библиотеки (каталог vendor), которых нет в CI.
#
# Использование: deploy/publish.sh <версия> <тег образов на сервере>      например: deploy/publish.sh 0.1.0 manual-2
# Нужно: `docker login` в Docker Hub, ssh-доступ к серверу, каталог vendor ($VENDOR, по умолчанию /tmp/vendor-backend: `cd backend && cargo vendor --locked <каталог>`
# плюс `.cargo-config.toml` из docs/deploy.md). Переменные: DOCKERHUB_NAMESPACE (alexeirysev), DEPLOY_SSH (rysev-a@212.57.126.97), VENDOR.
set -euo pipefail

VERSION="${1:?версия, например 0.1.0}"
SERVER_TAG="${2:?тег образов на сервере, например manual-2}"
NS="${DOCKERHUB_NAMESPACE:-alexeirysev}"
HOST="${DEPLOY_SSH:-rysev-a@212.57.126.97}"
VENDOR="${VENDOR:-/tmp/vendor-backend}"
IMAGES="cs-core-api cs-core-proxy cs-core-worker"

cd "$(dirname "$0")/.."
[ -d "$VENDOR" ] || { echo "нет каталога зависимостей $VENDOR" >&2; exit 1; }

echo "== arm64: сборка"
docker build --platform linux/arm64 -f deploy/backend.Dockerfile --build-context "vendor=$VENDOR" -t "$NS/cs-core-api:$VERSION-arm64" .
docker build --platform linux/arm64 -f deploy/proxy.Dockerfile -t "$NS/cs-core-proxy:$VERSION-arm64" .
docker build --platform linux/arm64 -f deploy/worker.Dockerfile -t "$NS/cs-core-worker:$VERSION-arm64" .

echo "== amd64: образы $SERVER_TAG с сервера"
# shellcheck disable=SC2086
ssh "$HOST" "docker save $(for i in $IMAGES; do printf '%s ' "$i:$SERVER_TAG"; done) | gzip" | gunzip | docker load
for i in $IMAGES; do docker tag "$i:$SERVER_TAG" "$NS/$i:$VERSION-amd64"; done

echo "== публикация"
for i in $IMAGES; do
  docker push "$NS/$i:$VERSION-amd64"
  docker push "$NS/$i:$VERSION-arm64"
  docker buildx imagetools create -t "$NS/$i:$VERSION" -t "$NS/$i:latest" "$NS/$i:$VERSION-amd64" "$NS/$i:$VERSION-arm64"
done

echo "== готово:"
for i in $IMAGES; do docker buildx imagetools inspect "$NS/$i:$VERSION" | sed -n '1,/^Manifests/p;/Platform/p' | grep -E "Name|Platform"; done
