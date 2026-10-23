# Инструкция для агента: развернуть «say» на сервере с docker compose

Это пошаговая инструкция для агента (или человека), который разворачивает сервис на **одной машине, где есть только Docker с compose-плагином**
(ни Python, ни Node, ни `sqlite3` на хосте не нужны). Рассуждения, почему схема такая, — в `deploy.md` (раздел 7, «Этап 1»).

Состав стека (`deploy/docker-compose.yml`, проект `say`):

| Сервис | Что это |
|---|---|
| `proxy` | Caddy: HTTPS, раздаёт собранный фронтенд, `/api` → `api`, `/internal` наружу закрыт |
| `api` | FastAPI + SQLite (том `data`, файл `/data/say.db`); при старте сидит содержимое курса и запускает uvicorn |
| `worker` | воркер проверки кода: забирает задания у `api` и запускает песочницы |
| `dind` | **отдельный** Docker-демон (`privileged`) только для песочниц; образы лежат в томе `dind-data` |
| `backup` | раз в сутки онлайн-копия SQLite в том `backups` (хранятся 14 последних) |
| `images` | разовая задача (профиль `setup`): заливает образы песочниц в `dind` |

Проверено локально (2026-10-22): сборка всех образов, запуск, регистрация, закрытый `/internal`, воркер подключается, **проверка Python-задачи проходит
через всю цепочку** (`api` → очередь → `worker` → `dind` → результат), данные переживают перезапуск `api`, копия SQLite создаётся, после проверок в `dind`
не остаётся контейнеров. **Не проверено**: сборка образа `say-rust-crates:1` и проверка Rust/C/JS-задач (долго; проверьте на сервере, шаг 6).

---

## 0. Правила (нарушать нельзя)

1. **Не монтируйте `/var/run/docker.sock` хоста ни в один контейнер** и не публикуйте порт `2375` `dind` наружу: код учеников исполняется в `dind`, сокет хоста = root на машине.
2. **Не включайте временных пользователей**: в compose задано `SAY_DEFAULT_USERS=0` (иначе создаются `student/student` и `programmer/programmer`). Не убирайте.
3. **Секреты не коммитите**: `deploy/.env` в git не попадает (`.dockerignore` и `.gitignore`-правила), токен — только в нём.
4. Не меняйте `SAY_RUNNER=remote` на `local` (в `local` Docker запускается из процесса API).
5. Не удаляйте тома `data` (база с прогрессом пользователей) и `backups` без явного указания владельца. `docker compose down -v` стирает **все** тома — не использовать на рабочем сервере.
6. Аудио не синтезируем и не генерируем (правило проекта, см. AGENTS.md): сид всегда `--no-audio` (в контейнере это уже так).
7. Что-то непонятное, ломающее или необратимое (удаление данных, открытие портов, смена домена с уже выданным сертификатом) — остановитесь и спросите владельца.

---

## 1. Что нужно узнать у владельца до начала

- **Домен** сайта (например `say.example.com`) и что его DNS `A`/`AAAA` указывает на сервер. Без домена можно проверить по HTTP: `SAY_SITE=:80`.
- **Свободны ли порты 80 и 443** на сервере. Если их уже держит другой прокси (Traefik/nginx) — см. шаг 3, вариант «за существующим прокси».
- **Сколько ядер и памяти** отдать песочницам (`SAY_SANDBOX_CPUS`, `SAY_SANDBOX_MEM`): это потолок всех проверок кода сразу. Рекомендация: 50–70% ядер и памяти, остальное остаётся сайту.
- Как получить код: репозиторий `git@github.com:rysev-a/dev-learn.git` (ветка `main`); нужен доступ (deploy key или токен). Уточните, где хранить код (например `/opt/say`).

## 2. Проверка сервера

```bash
docker version && docker compose version     # compose v2+
nproc; free -h; df -h /var/lib/docker       # ядра, память, место (образы песочниц ≈ 5–8 ГБ, rust-образ с крейтами — больше всего)
docker info | grep -iE "storage driver|cgroup"   # overlay2, cgroup v2 желательно
```

Нужно: Docker 25+, compose v2, свободно ≥ 20 ГБ на диске Docker, `privileged`-контейнеры разрешены (rootful Docker). Rootless Docker и «песочницы без привилегий»
для `dind` не подходят. Если `privileged` запрещён политикой сервера — остановитесь и спросите владельца (альтернатива — отдельная VM под воркер, `deploy.md` этап 2).

## 3. Подготовка

```bash
git clone git@github.com:rysev-a/dev-learn.git /opt/say && cd /opt/say     # путь уточните у владельца
cp deploy/.env.example deploy/.env
```

Заполните `deploy/.env`:

```bash
# токен (общий секрет API и воркера)
sed -i "s/^SAY_WORKER_TOKEN=.*/SAY_WORKER_TOKEN=$(openssl rand -hex 32)/" deploy/.env
```

И вручную: `SAY_SITE` (домен), `SAY_SANDBOX_CPUS`, `SAY_SANDBOX_MEM`, `SAY_LIGHT_SLOTS`/`SAY_HEAVY_SLOTS` (слоты не больше `SAY_SANDBOX_CPUS`; обычно `light = ядра`, `heavy = ядра/2`).

**Вариант «порты 80/443 заняты другим прокси»** (например Traefik на этом же сервере): поставьте `SAY_SITE=:80`, `SAY_HTTP_PORT=<свободный локальный порт, например 8088>`,
`SAY_HTTPS_PORT=<свободный порт>` и направьте существующий прокси на `127.0.0.1:<SAY_HTTP_PORT>` (HTTPS и сертификат делает он). `SAY_SECURE_COOKIE` оставьте `1`, если пользователи заходят по HTTPS.
Существующий прокси должен передавать `X-Forwarded-Proto`/`Host`. Не удаляйте и не меняйте чужие сервисы.

**Вариант «проверить по HTTP без домена»**: `SAY_SITE=:80`, `SAY_SECURE_COOKIE=0`, любые свободные порты. Для рабочего режима вернуть `1`.

Проверьте конфигурацию:

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env config -q && echo OK
```

## 4. Первый запуск

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --build
docker compose -f deploy/docker-compose.yml --env-file deploy/.env ps
```

Сборка фронтенда и API занимает несколько минут. `api` при первом старте сидит курс (≈ 30–60 с) — до этого он `unhealthy`/`starting`, `proxy` и `worker` ждут его.
Ожидаемо: все сервисы `Up`, `api`, `dind` — `healthy`.

## 5. Образы песочниц (один раз)

Проверка кода не работает, пока в `dind` нет образов. Они хранятся в томе `dind-data` и переживают перезапуск.

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile setup run --rm images
```

Скачиваются `python:3.13-slim`, `rust:1.97-slim`, `node:22-alpine` и **собирается `say-rust-crates:1`** (tokio, axum, sqlx, PostgreSQL — долго, 15–40 минут и несколько ГБ; нужен выход в интернет у `dind`).
Если сборка упала — прочитайте вывод (обычно сеть/DNS или нехватка места) и повторите; уже скачанные слои сохранены.

Проверьте: `docker compose -f deploy/docker-compose.yml --env-file deploy/.env exec dind docker image ls`.

## 6. Проверка работы (обязательно, после каждой выкладки)

Подставьте свой адрес (`https://<домен>` или `http://localhost:<SAY_HTTP_PORT>`):

```bash
BASE=https://say.example.com
curl -s -o /dev/null -w "главная %{http_code}\n" $BASE/                    # 200
curl -s -o /dev/null -w "api     %{http_code}\n" $BASE/api/books           # 200
curl -s -o /dev/null -w "internal %{http_code}\n" $BASE/internal/worker/jobs   # 404 — API воркеров наружу закрыт
curl -s $BASE/api/exercises/runner/status                                  # {"queued":0,"running":0,"workers":1,"available":true}
```

`workers: 1` и `available: true` — воркер подключился. Затем сквозная проверка кода (временный пользователь, потом можно удалить из БД):

```bash
J='content-type: application/json'
curl -s -c /tmp/cj -X POST $BASE/api/auth/register -H "$J" -d '{"email":"check@example.com","login":"check","password":"check-pass-12345"}'
RES=$(curl -s -b /tmp/cj -X POST $BASE/api/exercises/run -H "$J" -d '{"book":13,"chapter":0,"task":"intro-variable","code":"year = 1991\nprint(year)"}')
ID=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
sleep 5; curl -s -b /tmp/cj $BASE/api/exercises/run/$ID      # "state":"done" ... "solved":true
```

Затем проверьте по одной задаче каждого режима (после шага 5): JS (книга 11), C (книга 16), Rust (книга 10, глава 1) — найдите id так:
`docker compose ... exec api python -c "import sqlite3; print(sqlite3.connect('/data/say.db').execute(\"select book_id,chapter,id from tasks where mode='rust' limit 1\").fetchall())"`
(`mode`: `rust`, `c`, `js`). Для каждой отправьте эталонное решение (см. модули `backend/app/exercises/*_tasks`) и убедитесь, что `solved: true`.

Также: откройте сайт в браузере, зарегистрируйтесь, откройте любую главу, слайды и упражнение (если есть доступ к браузеру).

## 7. Обновление

```bash
cd /opt/say && git pull
docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --build
```

`api` при каждом старте повторно сидит содержимое курса (книги, главы, задачи, квизы) — прогресс пользователей не затрагивается. Образы песочниц обновлять нужно, только если менялся
`backend/docker/rust-crates` или версии образов в `backend/app/exercises/runner.py` (тогда повторите шаг 5 и сбросьте кэш проверок: он хранится в базе `exec_cache` и протухает за 7 дней сам).
После выкладки повторите шаг 6.

## 7а. Вариант: бэкенд на axum + SurrealDB (вместо Python-API)

Тот же сайт, прокси и воркер, но `api` — Rust-бэкенд (`backend-rs/`), данные — в SurrealDB (том `surreal-data`), а не в SQLite. Использовать, **только если владелец
просит именно этот вариант**. Отличия от шагов 3–7:

1. **Токен реестра crates.** Общие библиотеки лежат в приватном реестре `lab` (gitness); без токена бэкенд не соберётся. Токен выдаёт владелец (в `~/.cargo/credentials.toml`
   у него — строка `[registries.lab] token = "Bearer …"`), он передаётся **только** в окружении на время сборки (`LAB_TOKEN=<токен без слова Bearer>`), в файлы и git не пишется.
2. В `deploy/.env` дополнительно: `SURREAL_PASS` (пароль root SurrealDB), `ADMIN_EMAIL` и `ADMIN_PASSWORD` (начальный администратор, вход по email, пароль ≥ 8 символов),
   при необходимости `SMTP_*`/`MAIL_FROM` (без `SMTP_HOST` письма подтверждения никуда не уходят, а входу подтверждение не мешает). Остальное — как в шаге 3.
3. Запуск (обе compose-файла подряд, `LAB_TOKEN` задан в окружении только для этой команды):

```bash
LAB_TOKEN=… docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.rust.yml --env-file deploy/.env up -d --build
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.rust.yml --env-file deploy/.env --profile setup run --rm images   # образы песочниц, как в шаге 5
```

   Первая сборка Rust-бэкенда долгая (10–20 минут: компилируется SurrealDB и зависимости). На старте бэкенд сидит курс в SurrealDB (≈ 5–15 с), `api` до этого `starting`.
4. Проверка (шаг 6) та же, но вход и регистрация — по **email**: `POST /api/auth/signup` `{email, password, name}` затем `POST /api/auth/login` `{email, password}` → `{token, user, …}`;
   дальше заголовок `Authorization: Bearer <token>` вместо cookie. Админка и пользователи — `/api/admin/*` (вход администратора `POST /api/admin/login`).
5. Бэкапы: сервис `backup` делает `surreal export` раз в сутки в том `backups` (файлы `say-*.surql`); восстановление — `surreal import` в чистую базу.
6. Обновление — как в шаге 7, но с `LAB_TOKEN` и обоими файлами. Бэкенд должен работать **одним экземпляром** (очередь проверок под замком процесса).
7. Данные Python-варианта (SQLite) сюда не переносятся: пользователи и прогресс начинаются с нуля.
8. **Сайт в этом варианте — Leptos-фронтенд** (`frontend-rs`): `deploy/docker-compose.rust.yml` подменяет сборку прокси на `deploy/proxy-rs.Dockerfile` (trunk собирает wasm
   внутри образа, около 3 минут; по сети отдаётся со сжатием ≈ 3 МБ). Регистрации в этом варианте ограничены по частоте (429) — это норма.
9. **Нет сети до реестра `lab`** (ошибка `Failed to connect to git.service-lab.dev`): подложите зависимости готовым каталогом. На машине, где реестр доступен (или
   есть кэш cargo): `cd backend-rs && cargo vendor --locked /путь/vendor-backend`, затем положите в каталог файл `.cargo-config.toml` (замена источников на `/vendor`:
   `[source.crates-io] replace-with`, `[source."sparse+https://git.service-lab.dev/pkg/lab/lab_crates/cargo/index/"] registry = … replace-with = "vendored-sources"`,
   `[source.vendored-sources] directory = "/vendor"`) и укажите `SAY_VENDOR_DIR=/путь/vendor-backend` в `deploy/.env`. По умолчанию (`deploy/no-vendor`) работает реестр с токеном.
10. Локальная проверка стека: `SAY_SITE=:80`, `SAY_SECURE_COOKIE=0`, порты `SAY_HTTP_PORT`/`SAY_HTTPS_PORT` — свободные (8080 часто занят другим стеком — проверьте, куда
    на самом деле отвечает `localhost`). Песочницы: образы заливаются в `dind` (шаг 5) или по одному: `docker exec say-dind-1 docker pull python:3.13-slim`. Тесты на готовый стек —
    `e2e/README.md` («Против готового стека»).

## 8. Бэкапы и восстановление

Раз в сутки сервис `backup` кладёт копию в том `backups` (`say-YYYYMMDD-HHMMSS.db`, последние 14). Этого **недостаточно**: том живёт на той же машине. Договоритесь с владельцем о копии наружу (cron + `rsync`/объектное хранилище).

Достать копию из тома:

```bash
docker run --rm -v say_backups:/b -v "$PWD":/out alpine sh -c 'cp "$(ls -t /b/say-*.db | head -1)" /out/say-latest.db'
```

Восстановить (сервис остановить, текущий файл сохранить):

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env stop api backup
docker run --rm -v say_data:/d -v "$PWD":/in alpine sh -c 'cp /d/say.db /d/say.db.before-restore && cp /in/say-latest.db /d/say.db && rm -f /d/say.db-wal /d/say.db-shm'
docker compose -f deploy/docker-compose.yml --env-file deploy/.env start api backup
```

## 9. Журналы и диагностика

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env logs --tail 100 api worker dind proxy
```

| Симптом | Причина и что делать |
|---|---|
| `dind` не становится `healthy` | Нужен `privileged` и rootful Docker; проверьте `docker compose logs dind` (часто — нет `overlay`/cgroup или мало места). Не заменяйте на монтирование сокета хоста |
| `api` долго `starting` | идёт первый сид (до 2 минут, `start_period: 120s`); смотрите `logs api`. Если падает с ошибкой Python — прочтите трейс, не обходите |
| В `status` `workers: 0`, проверка отвечает 503 | воркер не подключился: `logs worker` (неверный `SAY_WORKER_TOKEN`, `api` не `healthy`, нет связи с `dind`); токен в `.env` одинаков для `api` и `worker` — после правки пересоздайте оба (`up -d`) |
| Проверка зависает в «В очереди» | нет свободных слотов (`SAY_LIGHT_SLOTS`/`SAY_HEAVY_SLOTS`) или образа в `dind`: выполните шаг 5 |
| В песочнице «файл не найден» / пустой каталог | не совпал путь каталога песочниц: воркер должен иметь `TMPDIR=/sandboxes`, а том `sandboxes` — смонтирован в `worker` и `dind` по пути `/sandboxes` (так в compose; не меняйте) |
| `proxy` не выдаёт сертификат | DNS домена не указывает на сервер, порты 80/443 закрыты или заняты; для проверки поставьте `SAY_SITE=:80`, `SAY_SECURE_COOKIE=0` |
| После входа сессия не держится | `SAY_SECURE_COOKIE=1` при заходе по обычному HTTP — используйте HTTPS или `0` только для проверки |
| `database is locked` в логах `api` | сообщите владельцу: SQLite перегружен, нужен WAL/переезд (`deploy.md`, раздел 3) |
| Нужно остановить всё | `docker compose -f deploy/docker-compose.yml --env-file deploy/.env stop` (тома сохраняются) |

Лимиты ресурсов для всех песочниц сразу задаёт `dind` (`SAY_SANDBOX_CPUS`/`SAY_SANDBOX_MEM`). Если сайт тормозит во время проверок — уменьшите их и слоты, перезапустите `dind` и `worker`.

## 10. Что сообщить владельцу после развёртывания

- адрес сайта и что вы проверили из шага 6 (с результатами команд);
- какие образы песочниц залиты и какие режимы (`python`, `js`, `c`, `rust`, `sql`) реально проверены сквозной проверкой;
- выбранные лимиты и слоты (`.env` без секретов), где лежит код и тома;
- что **не** сделано: внешняя копия бэкапов, мониторинг, лимиты на регистрацию и вход по IP (`deploy.md`, раздел 6 — до открытой регистрации они обязательны);
- любые отступления от этой инструкции и их причины.
