# Инструкция для агента: развернуть «say» на сервере с docker compose

Это пошаговая инструкция для агента (или человека), который разворачивает сервис на **одной машине, где есть только Docker с compose-плагином**
(ни Rust, ни Python, ни Node на хосте не нужны). Выбор схемы и порядок работ — в `docs/deploy.md`.

Состав стека (`deploy/docker-compose.yml`, проект `say`):

| Сервис | Что это |
|---|---|
| `proxy` | Caddy: HTTPS, раздаёт собранный Leptos-фронтенд (`frontend/`, trunk собирает wasm внутри образа), `/api` → `api`, `/internal` наружу закрыт |
| `api` | бэкенд на axum (`backend/`): при старте сидит содержимое курса в SurrealDB, ведёт очередь проверок и API воркеров |
| `surrealdb` | база (том `surreal-data`, порт 8000 только внутри сети; для разработки опубликован `127.0.0.1:18000`) |
| `worker` | воркер проверки кода: забирает задания у `api` и запускает песочницы |
| `dind` | **отдельный** Docker-демон (`privileged`) только для песочниц; образы лежат в томе `dind-data` |
| `backup` | раз в сутки экспорт SurrealDB (`surreal export` по HTTP, файлы `say-*.surql`) в том `backups` (хранятся 14 последних) |
| `images` | разовая задача (профиль `setup`): заливает образы песочниц в `dind` |

Проверено локально: сборка всех образов, запуск, регистрация, закрытый `/internal`, воркер подключается, проверка кода проходит через всю цепочку
(`api` → очередь → `worker` → `dind` → результат), e2e-тесты идут против готового стека (`e2e/README.md`, «Против готового стека»). Сборка образа `say-rust-crates:1`
и проверка Rust/C/JS-задач долгие — проверьте на сервере (шаг 6).

---

## 0. Правила (нарушать нельзя)

1. **Не монтируйте `/var/run/docker.sock` хоста ни в один контейнер** и не публикуйте порт `2375` `dind` наружу: код учеников исполняется в `dind`, сокет хоста = root на машине.
2. **Не задавайте `DEMO_USER_*`/`DEMO_ADMIN_*`** (демо-пользователи без политики паролей — только для разработки): на сервере администратор — `ADMIN_EMAIL`/`ADMIN_PASSWORD`.
3. **Секреты не коммитите**: `deploy/.env` в git не попадает (`.dockerignore` и `.gitignore`-правила), токен — только в нём.
4. У `api` нет Docker и встроенного воркера: код проверяет только отдельный `worker`. Не добавляйте `api` доступ к docker.
5. Не удаляйте тома `surreal-data` (база с прогрессом пользователей) и `backups` без явного указания владельца. `docker compose down -v` стирает **все** тома — не использовать на рабочем сервере.
6. Аудио не синтезируем и не генерируем (правило проекта, см. AGENTS.md): в образ `api` аудио не кладётся.
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
для `dind` не подходят. Если `privileged` запрещён политикой сервера — остановитесь и спросите владельца (альтернатива — отдельная машина под воркер, схема B в `docs/deploy.md`).

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

И вручную: `SURREAL_PASS` (пароль root SurrealDB), `ADMIN_EMAIL` и `ADMIN_PASSWORD` (начальный администратор, вход по email, пароль ≥ 8 символов),
при необходимости `SMTP_*`/`MAIL_FROM` (без `SMTP_HOST` письма подтверждения никуда не уходят), `SAY_SITE` (домен), `SAY_SANDBOX_CPUS`, `SAY_SANDBOX_MEM`, `SAY_LIGHT_SLOTS`/`SAY_HEAVY_SLOTS` (слоты не больше `SAY_SANDBOX_CPUS`; обычно `light = ядра`, `heavy = ядра/2`).

**Вариант «порты 80/443 заняты другим прокси»** (например Traefik на этом же сервере): поставьте `SAY_SITE=:80`, `SAY_HTTP_PORT=<свободный локальный порт, например 8088>`,
`SAY_HTTPS_PORT=<свободный порт>` и направьте существующий прокси на `127.0.0.1:<SAY_HTTP_PORT>` (HTTPS и сертификат делает он). Существующий прокси должен передавать `X-Forwarded-Proto`/`Host`. Не удаляйте и не меняйте чужие сервисы.

**Вариант «проверить по HTTP без домена»**: `SAY_SITE=:80`, любые свободные порты (8080 часто занят другим стеком — проверьте, куда на самом деле отвечает `localhost`).

**Токен реестра crates.** Общие библиотеки лежат в приватном реестре `lab` (gitness); без токена бэкенд не соберётся. Токен выдаёт владелец (в `~/.cargo/credentials.toml`
у него — строка `[registries.lab] token = "Bearer …"`), он передаётся **только** в окружении на время сборки (`LAB_TOKEN=<токен без слова Bearer>`), в файлы и git не пишется.

**Нет сети до реестра `lab`** (ошибка `Failed to connect to git.service-lab.dev`): подложите зависимости готовым каталогом. На машине, где реестр доступен (или
есть кэш cargo): `cd backend && cargo vendor --locked /путь/vendor-backend`, затем положите в каталог файл `.cargo-config.toml` (замена источников на `/vendor`:
`[source.crates-io] replace-with`, `[source."sparse+https://git.service-lab.dev/pkg/lab/lab_crates/cargo/index/"] registry = … replace-with = "vendored-sources"`,
`[source.vendored-sources] directory = "/vendor"`) и укажите `SAY_VENDOR_DIR=/путь/vendor-backend` в `deploy/.env`. По умолчанию (`deploy/no-vendor`) работает реестр с токеном.

Проверьте конфигурацию:

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env config -q && echo OK
```

## 4. Первый запуск

```bash
LAB_TOKEN=… docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --build
docker compose -f deploy/docker-compose.yml --env-file deploy/.env ps
```

Первая сборка долгая (10–20 минут: бэкенд с SurrealDB-клиентом и wasm-фронтенд). `api` при первом старте сидит курс в SurrealDB (≈ 5–15 с) — до этого он `starting`, `proxy` и `worker` ждут его.
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

`workers: 1` и `available: true` — воркер подключился. Затем сквозная проверка кода (вход и регистрация — по **email**, дальше заголовок `Authorization: Bearer <token>`):

```bash
J='content-type: application/json'
curl -s -X POST $BASE/api/auth/signup -H "$J" -d '{"email":"check@example.com","password":"check-pass-12345","name":"check"}'
TOKEN=$(curl -s -X POST $BASE/api/auth/login -H "$J" -d '{"email":"check@example.com","password":"check-pass-12345"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
RES=$(curl -s -X POST $BASE/api/exercises/run -H "$J" -H "Authorization: Bearer $TOKEN" -d '{"book":13,"chapter":0,"task":"intro-variable","code":"year = 1991\nprint(year)"}')
ID=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
sleep 5; curl -s -H "Authorization: Bearer $TOKEN" $BASE/api/exercises/run/$ID      # "state":"done" ... "solved":true
```

Регистрации ограничены по частоте (429) — это норма. Затем проверьте по одной задаче каждого режима (после шага 5): JS (книга 11), C (книга 16), Rust (книга 10, глава 1);
эталонные решения лежат в `backend/data/sql/tasks/*.sql` (поле `spec`). Ту же проверку делают e2e-тесты книг (`e2e/README.md`).

Также: откройте сайт в браузере, зарегистрируйтесь, откройте любую главу, слайды и упражнение (если есть доступ к браузеру).

## 7. Обновление

```bash
cd /opt/say && git pull
LAB_TOKEN=… docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --build
```

Нужен `LAB_TOKEN` (или `SAY_VENDOR_DIR`). `api` при старте пересеивает содержимое курса, только если изменился хеш исходников; прогресс пользователей не затрагивается.
Бэкенд должен работать **одним экземпляром** (очередь проверок под замком процесса). Образы песочниц обновлять нужно, только если менялся
`worker/docker/rust-crates` или версии образов в `worker/runner.py` (тогда повторите шаг 5; кэш проверок хранится в базе и протухает за 7 дней сам).
После выкладки повторите шаг 6.

## 8. Бэкапы и восстановление

Раз в сутки сервис `backup` кладёт экспорт SurrealDB в том `backups` (`say-YYYYMMDD-HHMMSS.surql`, последние 14). Этого **недостаточно**: том живёт на той же машине. Договоритесь с владельцем о копии наружу (cron + `rsync`/объектное хранилище).

Достать копию из тома:

```bash
docker run --rm -v say_backups:/b -v "$PWD":/out alpine sh -c 'cp "$(ls -t /b/say-*.surql | head -1)" /out/say-latest.surql'
```

Восстановить: остановить `api`, `surreal import` в чистую базу (пространство `stack`, база `say`), запустить `api`. Данные курса восстанавливать не нужно — сид пересоздаёт их из файлов;
в копии важны пользователи и прогресс.

## 9. Журналы и диагностика

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env logs --tail 100 api worker dind proxy
```

| Симптом | Причина и что делать |
|---|---|
| `dind` не становится `healthy` | Нужен `privileged` и rootful Docker; проверьте `docker compose logs dind` (часто — нет `overlay`/cgroup или мало места). Не заменяйте на монтирование сокета хоста |
| `api` долго `starting` | идёт первый сид (`start_period: 180s`) или нет связи с `surrealdb`; смотрите `logs api surrealdb`. `DB_STRICT=1`: без базы бэкенд не стартует |
| В `status` `workers: 0`, проверка отвечает 503 | воркер не подключился: `logs worker` (неверный `SAY_WORKER_TOKEN`, `api` не `healthy`, нет связи с `dind`); токен в `.env` одинаков для `api` и `worker` — после правки пересоздайте оба (`up -d`) |
| Проверка зависает в «В очереди» | нет свободных слотов (`SAY_LIGHT_SLOTS`/`SAY_HEAVY_SLOTS`) или образа в `dind`: выполните шаг 5 |
| В песочнице «файл не найден» / пустой каталог | не совпал путь каталога песочниц: воркер должен иметь `TMPDIR=/sandboxes`, а том `sandboxes` — смонтирован в `worker` и `dind` по пути `/sandboxes` (так в compose; не меняйте) |
| `proxy` не выдаёт сертификат | DNS домена не указывает на сервер, порты 80/443 закрыты или заняты; для проверки поставьте `SAY_SITE=:80` |
| Сборка `api` падает на `git.service-lab.dev` | нет токена или сети до реестра: `LAB_TOKEN` либо `SAY_VENDOR_DIR` (шаг 3) |
| Нужно остановить всё | `docker compose -f deploy/docker-compose.yml --env-file deploy/.env stop` (тома сохраняются) |

Лимиты ресурсов для всех песочниц сразу задаёт `dind` (`SAY_SANDBOX_CPUS`/`SAY_SANDBOX_MEM`). Если сайт тормозит во время проверок — уменьшите их и слоты, перезапустите `dind` и `worker`.

## 10. Что сообщить владельцу после развёртывания

- адрес сайта и что вы проверили из шага 6 (с результатами команд);
- какие образы песочниц залиты и какие режимы (`python`, `js`, `c`, `rust`, `sql`) реально проверены сквозной проверкой;
- выбранные лимиты и слоты (`.env` без секретов), где лежит код и тома;
- что **не** сделано: внешняя копия бэкапов, мониторинг, лимиты на регистрацию и вход по IP (`docs/deploy.md`, чек-лист — до открытой регистрации они обязательны);
- любые отступления от этой инструкции и их причины.
