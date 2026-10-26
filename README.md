# CS.Core — аудиокурс по программированию

Учебник «от нуля до своего веб-сервиса»: 12 книг, 311 глав. В каждой главе — слайды с покадровыми анимациями, закадровый текст, квиз на теорию и практика прямо в браузере:
код проверяется в изолированной песочнице, а схемы, сети, виртуальные машины, системный дизайн и разметка HTML/CSS проверяются интерактивными лабораториями.

**Сайт:** <https://cs-core.tech> — тестовый запуск на одной небольшой машине. Сервис в стадии развития и пока не выдерживает большую нагрузку:
при перегрузке проверка кода временно недоступна (теория, вопросы и лаборатории в браузере продолжают работать).
Систему можно запустить у себя из готовых образов — см. [«Запуск у себя»](#запуск-у-себя).

> Статус: MVP. Курс написан целиком, озвучки пока нет (слайды идут по таймеру, текст абзаца показывается в окне «За кадром»); голос будет сгенерирован один раз, когда все книги готовы.

## Книги

| Книга | Глав | О чём |
|---|---|---|
| Дискретная математика | 10 | язык математики, счёт и логика, графы и вероятность |
| Python как первый язык | 52 | от основ до модели данных, метапрограммирования, асинхронности и внутренностей интерпретатора |
| Алгоритмы и структуры данных | 19 | сложность, хеш-таблицы, деревья, кучи, графы, динамика |
| Архитектура компьютера | 22 | от транзистора и вентилей до процессора, RISC-V, кэша и конвейера |
| От assembler к языку C | 14 | язык C рядом с ассемблером RISC-V |
| Погружаемся в Unix | 17 | процессы, планировщик, память, VFS, сеть, контейнеры, ядро |
| Компьютерные сети | 20 | от кабеля и Ethernet до TLS, DNS, HTTP/3 и безопасности |
| Виртуализация | 16 | VT-x, EPT, virtio, KVM, миграция, контейнеры, confidential computing |
| Базы данных | 32 | SQL и «под капотом»: транзакции, индексы, репликация, шардирование |
| Изучаем Rust | 51 | владение, трейты, Tokio, сервер на Axum и Sqlx |
| Современный Frontend | 34 | JavaScript, HTML и CSS, браузер, Node.js, сборка, свой мини-фреймворк |
| Системный дизайн | 24 | от требований и прикидок до проектирования Uber, Instagram, мессенджера |

## Что внутри главы

- **Оформление:** светлые и тёмные цветовые темы (Dracula, One Dark, Nord, Tokyo Night, Solarized, Monokai, GitHub Light, Gruvbox Light и другие) для сайта, слайдов и редактора кода — в настройках.
- **Теория:** слайды-анимации (схемы строятся из данных: ячейки, указатели, вентили, области, код) и текст урока «За кадром».
- **Вопросы:** квиз; верные ответы знает только сервер.
- **Практика:** код-упражнения (Python, JavaScript, SQL, C, Rust, tokio/axum/sqlx) проверяются в песочнице без сети и с лимитами; упражнения с вводом ответа;
  **лаборатории**: схемы из вентилей, ассемблер и RISC-V, симулятор сети, виртуализация, схема высоконагруженного сервиса, HTML и CSS (разметка, селекторы, каскад).
  Решения лабораторий перепроверяет сервер тем же кодом, что считает в браузере.

## Как устроено

```
браузер (Leptos, wasm) ──► Traefik ──► frontend (Caddy, статика)
                                   └─► backend (axum) ──► SurrealDB
                                            ▲
         воркер (Python) ──► dind ──► песочницы (python, node, rust, gcc, sqlite)   ← забирает задания у backend
```

- `backend/` — axum + SurrealDB: API курса, прогресс, очередь проверок кода, вход. Содержимое курса — данные в `backend/data` (тексты, слайды, SQL задач и квизов, лаборатории).
- `frontend/` — интерфейс на Leptos (CSR, trunk).
- `packages/` — общие крейты Rust: модель слайдов и сцен, подсветка, генераторы, движки лабораторий (`sdlab`, `netlab`, `archlab`, `riscvlab`, `virtlab`, `weblab`).
  Они работают и в браузере (wasm), и на сервере, где проверяют присланные решения.
- `worker/` — воркер проверки кода: берёт задания из очереди и запускает песочницы в отдельном Docker-демоне.
- `deploy/` — `docker compose` (Traefik, frontend, backend, SurrealDB, копии базы, воркер), Dockerfile'ы и скрипт выкладки.
- `e2e/` — браузерные тесты Playwright на каждую книгу и лабораторию; `voice/` — озвучка (kokoro-ru), запускается один раз в конце.

## Запуск у себя

Готовые образы лежат на Docker Hub: [`alexeirysev/cs-core-api`](https://hub.docker.com/r/alexeirysev/cs-core-api) (бэкенд),
[`alexeirysev/cs-core-proxy`](https://hub.docker.com/r/alexeirysev/cs-core-proxy) (сайт), [`alexeirysev/cs-core-worker`](https://hub.docker.com/r/alexeirysev/cs-core-worker) (проверка кода).
Собирать ничего не нужно, данные остаются у вас.

**Платформы.** Образы Linux-контейнеров, собраны для двух архитектур процессора — `linux/amd64` (Intel и AMD) и `linux/arm64` (Apple Silicon, ARM-серверы); Docker сам выберет нужную.
Подходят: **Linux**, **macOS** (Intel и Apple Silicon, через Docker Desktop), **Windows** (Docker Desktop с WSL2). Нужен Docker с Compose v2 и 2–4 ГБ свободной памяти
(для проверки кода — 8 ГБ и 15 ГБ диска).

```bash
git clone https://github.com/rysev-a/dev-learn.git && cd dev-learn
cp deploy/.env.example deploy/.env
```

Откройте `deploy/.env` и задайте (остальное можно не трогать):

```bash
SAY_URL=http://localhost
SAY_HTTP_PORT=8080                         # порт сайта на вашей машине
SAY_HTTPS_PORT=8443
SAY_WORKER_TOKEN=вставьте-вывод-openssl-rand-hex-32
SURREAL_PASS=придумайте-пароль-базы
ADMIN_EMAIL=you@example.com                # вход администратора
ADMIN_PASSWORD=не-короче-8-символов
```

Запуск:

```bash
export SAY_REGISTRY=alexeirysev/ SAY_TAG=latest        # или конкретная версия, например 0.1.0
docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d --no-build
```

Сайт — <http://localhost:8080>. Первый старт занимает около минуты: бэкенд засевает курс в базу. Зарегистрируйтесь на сайте или войдите администратором. Остановить: `docker compose -f deploy/docker-compose.yml --env-file deploy/.env down` (данные сохранятся в томе).

**Проверка кода (по желанию).** Теория, вопросы и лаборатории в браузере работают сразу. Чтобы проверялись код-упражнения, включите профиль `checks` — воркер и отдельный Docker-демон для песочниц
(он запускается в `privileged`-контейнере, как отдельный демон, ваш Docker не затрагивается):

```bash
docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile checks up -d --no-build
docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile checks run --rm images   # один раз: образы песочниц, 15–40 минут
```

Ресурсы песочниц ограничиваются переменными `SAY_SANDBOX_CPUS`, `SAY_SANDBOX_MEM`, `SAY_LIGHT_SLOTS`, `SAY_HEAVY_SLOTS`, потолок очереди — `SAY_QUEUE_LIMIT` (см. `deploy/.env.example`).
Проверено на Linux x86_64 и на macOS с Apple Silicon.

## Локальный запуск и разработка

- **Фронтенд и общие крейты** собираются из репозитория без закрытых зависимостей:
  ```bash
  rustup target add wasm32-unknown-unknown && cargo install trunk
  cd frontend/app && trunk serve              # http://127.0.0.1:7054, /api проксируется на 127.0.0.1:8001
  cd packages/weblab && cargo test            # тесты любого крейта из packages/
  cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/slides   # проверка слайдов
  ```
- **Бэкенд** использует общие библиотеки автора из закрытого реестра (`auth`, `admin_api`, `mail` и другие), поэтому из чужого клона не собирается. У автора:
  ```bash
  cd backend && SURREAL_USER=root SURREAL_PASS=devpass BIND=127.0.0.1:8001 SAY_WORKER_TOKEN=dev \
    DEMO_USER_EMAIL=student@mail.com DEMO_USER_PASSWORD=student \
    DEMO_ADMIN_EMAIL=programmer@mail.com DEMO_ADMIN_PASSWORD=programmer cargo run     # без SurrealDB работает на базе в памяти
  cd worker && SAY_WORKER_TOKEN=dev uv run worker.py --server http://127.0.0.1:8001 --name dev --light 2 --heavy 1   # проверка кода (нужен Docker)
  ```
- **Весь стек в Docker:** `deploy/docker-compose.yml` (Traefik, frontend, backend, SurrealDB, копии базы; профиль `checks` — воркер и песочницы), см. [`docs/deploy.md`](docs/deploy.md).
- **Тесты в браузере:** `cd e2e && npm ci && npm test` (нужны собранные фронтенд и бэкенд, см. `e2e/README.md`).

## Сервер, домен и выкладка

Схема развёртывания, HTTPS через Traefik и Let's Encrypt, бэкапы, обновления — [`docs/deploy.md`](docs/deploy.md); пошаговая инструкция для того, кто разворачивает сервис, — [`docs/deploy-agent.md`](docs/deploy-agent.md);
как устроена проверка кода и воркеры — [`docs/code-runner.md`](docs/code-runner.md). Выкладка на сайт идёт автоматически при создании релиза на GitHub (`.github/workflows/release.yml`).

## Как добавить или исправить содержимое

Курс — данные: тексты `backend/data/textbook`, слайды `backend/data/slides` (главы 13–15 книги 11 и несколько других — генераторы в `packages/gen`), квизы и задачи — SQL в `backend/data/sql`, лаборатории — JSON в `backend/data/labs`.
Правила (абзац = сцена = часть, цвета, формат) — в [`AGENTS.md`](AGENTS.md). После правок: тесты соответствующих крейтов `packages/` и `cd packages/gen && cargo run --release --bin lint_slides ../../backend/data/slides`.

## Лицензия

См. [LICENSE](LICENSE).
