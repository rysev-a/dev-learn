#!/bin/bash
# Release deployment on the server. This is the only command the GitHub Actions SSH key is allowed to run
# (in ~/.ssh/authorized_keys: restrict,command="…/release.sh" ssh-ed25519 …); what the key asks for arrives in SSH_ORIGINAL_COMMAND.
#
#   deploy <tag>   reads the release source tar.gz from stdin, builds the cs-core-*:<tag> images and starts the stack; on failure restores the previous version
#
# Layout on the server ($BASE, ~/cs-core by default): releases/<tag>/ holds the sources, shared/.env the settings (not in git), shared/current_tag the deployed tag.
# The backend dependencies directory (private crate registry) is $VENDOR (~/cs-core-vendor by default).
set -euo pipefail

BASE="${BASE:-$HOME/cs-core}"
VENDOR="${VENDOR:-$HOME/cs-core-vendor}"
KEEP=3

cmd="${SSH_ORIGINAL_COMMAND:-}"
action="${cmd%% *}"
tag="${cmd#* }"
[ "$action" != "$cmd" ] || { echo "expected: deploy <tag>" >&2; exit 2; }
case "$tag" in
  "" | *[!A-Za-z0-9._-]*) echo "invalid tag: '$tag'" >&2; exit 2 ;;
esac

compose() {
  docker compose -f "$BASE/releases/$1/deploy/docker-compose.yml" --env-file "$BASE/shared/.env" --profile checks "${@:2}"
}

set_tag() {
  sed -i '/^CS_CORE_TAG=/d' "$BASE/shared/.env"
  echo "CS_CORE_TAG=$1" >> "$BASE/shared/.env"
}

smoke() {
  domain="$(sed -n 's/^CS_CORE_DOMAIN=//p' "$BASE/shared/.env" | head -1)"
  i=0
  while [ "$i" -lt 40 ]; do
    if curl -fsS -o /dev/null --resolve "$domain:443:127.0.0.1" "https://$domain/api/books" 2>/dev/null \
      && curl -fsS -o /dev/null --resolve "$domain:443:127.0.0.1" "https://$domain/" 2>/dev/null; then
      return 0
    fi
    i=$((i + 1)); sleep 5
  done
  return 1
}

case "$action" in
  deploy)
    exec 9>"$BASE/.deploy.lock"
    flock -n 9 || { echo "a deployment is already running" >&2; exit 3; }
    rel="$BASE/releases/$tag"
    rm -rf "$rel"; mkdir -p "$rel"
    echo "== unpacking $tag"
    tar -xz -C "$rel"
    [ -f "$BASE/shared/.env" ] || { echo "missing $BASE/shared/.env" >&2; exit 4; }
    cd "$rel"
    echo "== building images"
    docker build -f deploy/backend.Dockerfile --build-context "vendor=$VENDOR" -t "cs-core-api:$tag" .
    docker build -f deploy/proxy.Dockerfile -t "cs-core-proxy:$tag" .
    docker build -f deploy/worker.Dockerfile -t "cs-core-worker:$tag" .
    prev="$(cat "$BASE/shared/current_tag" 2>/dev/null || true)"
    echo "== starting (was: ${prev:-nothing})"
    set_tag "$tag"
    compose "$tag" up -d --no-build --remove-orphans
    if smoke; then
      echo "$tag" > "$BASE/shared/current_tag"
      echo "== deployed: $tag"
    else
      echo "== check failed, restoring ${prev:-—}" >&2
      compose "$tag" logs --tail 40 api >&2 || true
      if [ -n "$prev" ] && [ -d "$BASE/releases/$prev" ]; then
        set_tag "$prev"
        compose "$prev" up -d --no-build --remove-orphans
      fi
      exit 1
    fi
    # keep the three latest versions: directories and images
    ls -1dt "$BASE"/releases/*/ | tail -n +$((KEEP + 1)) | xargs -r rm -rf
    for repo in cs-core-api cs-core-proxy cs-core-worker; do
      docker images "$repo" --format '{{.CreatedAt}}\t{{.Tag}}' | sort -r | tail -n +$((KEEP + 1)) | cut -f2 | xargs -r -I{} docker rmi "$repo:{}" >/dev/null 2>&1 || true
    done
    docker image prune -f >/dev/null 2>&1 || true
    docker builder prune -f --filter until=168h >/dev/null 2>&1 || true
    ;;
  *)
    echo "unknown command: '$action'" >&2; exit 2
    ;;
esac
