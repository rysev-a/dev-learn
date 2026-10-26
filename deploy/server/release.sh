#!/bin/bash
# Выкладка релиза на сервере. Это единственная команда, которую разрешено выполнять SSH-ключу GitHub Actions
# (в ~/.ssh/authorized_keys: restrict,command="…/release.sh" ssh-ed25519 …); что просит ключ, приходит в SSH_ORIGINAL_COMMAND.
#
#   deploy <тег>   — читает tar.gz исходников релиза из stdin, собирает образы cs-core-*:<тег> и запускает стек; при неудаче возвращает прежнюю версию
#   export <тег>   — отдаёт в stdout `docker save | gzip` образов этого тега (для публикации в GHCR из Actions)
#
# Раскладка на сервере ($BASE, по умолчанию ~/cs-core): releases/<тег>/ — исходники, shared/.env — настройки (не в git), shared/current_tag — выложенный тег.
# Каталог зависимостей бэкенда (закрытый реестр crates) — $VENDOR (по умолчанию ~/say-vendor).
set -euo pipefail

BASE="${BASE:-$HOME/cs-core}"
VENDOR="${VENDOR:-$HOME/say-vendor}"
KEEP=3

cmd="${SSH_ORIGINAL_COMMAND:-}"
action="${cmd%% *}"
tag="${cmd#* }"
[ "$action" != "$cmd" ] || { echo "ожидается: deploy|export <тег>" >&2; exit 2; }
case "$tag" in
  "" | *[!A-Za-z0-9._-]*) echo "недопустимый тег: '$tag'" >&2; exit 2 ;;
esac

compose() {
  docker compose -f "$BASE/releases/$1/deploy/docker-compose.yml" --env-file "$BASE/shared/.env" --profile checks "${@:2}"
}

set_tag() {
  sed -i '/^SAY_TAG=/d' "$BASE/shared/.env"
  echo "SAY_TAG=$1" >> "$BASE/shared/.env"
}

smoke() {
  domain="$(sed -n 's/^SAY_DOMAIN=//p' "$BASE/shared/.env" | head -1)"
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
  export)
    docker save "cs-core-api:$tag" "cs-core-proxy:$tag" "cs-core-worker:$tag" | gzip
    ;;
  deploy)
    exec 9>"$BASE/.deploy.lock"
    flock -n 9 || { echo "выкладка уже идёт" >&2; exit 3; }
    rel="$BASE/releases/$tag"
    rm -rf "$rel"; mkdir -p "$rel"
    echo "== распаковка $tag"
    tar -xz -C "$rel"
    [ -f "$BASE/shared/.env" ] || { echo "нет $BASE/shared/.env" >&2; exit 4; }
    cd "$rel"
    echo "== сборка образов"
    docker build -f deploy/backend.Dockerfile --build-context "vendor=$VENDOR" -t "cs-core-api:$tag" .
    docker build -f deploy/proxy.Dockerfile -t "cs-core-proxy:$tag" .
    docker build -f deploy/worker.Dockerfile -t "cs-core-worker:$tag" .
    prev="$(cat "$BASE/shared/current_tag" 2>/dev/null || true)"
    echo "== запуск (было: ${prev:-ничего})"
    set_tag "$tag"
    compose "$tag" up -d --no-build --remove-orphans
    if smoke; then
      echo "$tag" > "$BASE/shared/current_tag"
      echo "== выложено: $tag"
    else
      echo "== проверка не прошла, возвращаю ${prev:-—}" >&2
      compose "$tag" logs --tail 40 api >&2 || true
      if [ -n "$prev" ] && [ -d "$BASE/releases/$prev" ]; then
        set_tag "$prev"
        compose "$prev" up -d --no-build --remove-orphans
      fi
      exit 1
    fi
    # хранить три последние версии: каталоги и образы
    ls -1dt "$BASE"/releases/*/ | tail -n +$((KEEP + 1)) | xargs -r rm -rf
    for repo in cs-core-api cs-core-proxy cs-core-worker; do
      docker images "$repo" --format '{{.CreatedAt}}\t{{.Tag}}' | sort -r | tail -n +$((KEEP + 1)) | cut -f2 | xargs -r -I{} docker rmi "$repo:{}" >/dev/null 2>&1 || true
    done
    docker image prune -f >/dev/null 2>&1 || true
    docker builder prune -f --filter until=168h >/dev/null 2>&1 || true
    ;;
  *)
    echo "неизвестная команда: '$action'" >&2; exit 2
    ;;
esac
