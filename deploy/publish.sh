#!/bin/bash
# Publishing images to Docker Hub: one tag for two architectures (linux/amd64 and linux/arm64).
#   amd64 is taken from the server where the release was built (it is x86_64);
#   arm64 is built here (an Apple Silicon Mac or any ARM machine), because the backend needs private libraries (the vendor directory) that CI does not have.
#
# Usage: deploy/publish.sh <version> <image tag on the server>      for example: deploy/publish.sh 0.1.0 manual-2
# Required: `docker login` to Docker Hub, ssh access to the server, the vendor directory ($VENDOR, by default ~/.cache/cs-core/vendor-backend: `cd backend && cargo vendor --locked <directory>`
# plus `.cargo-config.toml` from docs/deploy.md). Variables: DOCKERHUB_NAMESPACE (alexeirysev), DEPLOY_SSH (rysev-a@212.57.126.97), VENDOR.
set -euo pipefail

VERSION="${1:?version, for example 0.1.0}"
SERVER_TAG="${2:?image tag on the server, for example manual-2}"
NS="${DOCKERHUB_NAMESPACE:-alexeirysev}"
HOST="${DEPLOY_SSH:-rysev-a@212.57.126.97}"
VENDOR="${VENDOR:-$HOME/.cache/cs-core/vendor-backend}"
IMAGES="cs-core-api cs-core-proxy cs-core-worker"

cd "$(dirname "$0")/.."
[ -d "$VENDOR" ] || { echo "no dependencies directory $VENDOR" >&2; exit 1; }

echo "== arm64: build"
docker build --platform linux/arm64 -f deploy/backend.Dockerfile --build-context "vendor=$VENDOR" -t "$NS/cs-core-api:$VERSION-arm64" .
docker build --platform linux/arm64 -f deploy/proxy.Dockerfile -t "$NS/cs-core-proxy:$VERSION-arm64" .
docker build --platform linux/arm64 -f deploy/worker.Dockerfile -t "$NS/cs-core-worker:$VERSION-arm64" .

echo "== amd64: images $SERVER_TAG from the server"
# shellcheck disable=SC2086
ssh "$HOST" "docker save $(for i in $IMAGES; do printf '%s ' "$i:$SERVER_TAG"; done) | gzip" | gunzip | docker load
for i in $IMAGES; do docker tag "$i:$SERVER_TAG" "$NS/$i:$VERSION-amd64"; done

echo "== publishing"
for i in $IMAGES; do
  docker push "$NS/$i:$VERSION-amd64"
  docker push "$NS/$i:$VERSION-arm64"
  docker buildx imagetools create -t "$NS/$i:$VERSION" -t "$NS/$i:latest" "$NS/$i:$VERSION-amd64" "$NS/$i:$VERSION-arm64"
done

echo "== done:"
for i in $IMAGES; do docker buildx imagetools inspect "$NS/$i:$VERSION" | sed -n '1,/^Manifests/p;/Platform/p' | grep -E "Name|Platform"; done
