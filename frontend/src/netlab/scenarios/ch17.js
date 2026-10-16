/* Глава 17 «Балансировка, CDN и обратный прокси»: пул, здоровье, привязка, маршрутизация L7, кэш. */
import { newHttp } from "../http.js";
import { device, iface, link, makeState, ports } from "../model.js";

const gw = (via) => [{ dst: "0.0.0.0/0", via, dev: null }];
const back = (id, name, y, ip, services) =>
  device(id, "server", name, 560, y, { ifaces: [iface("eth0", { ip })], routes: gw("10.0.1.1"), services });

function farm({ backends, svc = {}, algo = "rr", health = false }) {
  return makeState(
    [
      device("pc", "host", "Клиент", 50, 180, { ifaces: [iface("eth0", { ip: "10.0.0.10" })] }),
      device("lb", "router", "Балансировщик", 240, 180, {
        ifaces: [iface("eth0", { ip: "10.0.0.100" }), iface("eth1", { ip: "10.0.1.1" })],
        lb: { vip: "10.0.0.100", port: 80, algo, health, backends },
      }),
      device("sw", "switch", "SW", 390, 180, { ifaces: ports(5) }),
      back("s1", "Сервер 1", 70, "10.0.1.11", svc.s1 ?? [{ proto: "tcp", port: 80 }]),
      back("s2", "Сервер 2", 180, "10.0.1.12", svc.s2 ?? [{ proto: "tcp", port: 80 }]),
      back("s3", "Сервер 3", 290, "10.0.1.13", svc.s3 ?? [{ proto: "tcp", port: 80 }]),
    ],
    [link("pc:eth0", "lb:eth0"), link("lb:eth1", "sw:p1"), link("s1:eth0", "sw:p2"), link("s2:eth0", "sw:p3"), link("s3:eth0", "sw:p4")],
  );
}
const ALL = [
  { ip: "10.0.1.11", port: 80 },
  { ip: "10.0.1.12", port: 80 },
  { ip: "10.0.1.13", port: 80 },
];

export const CH17 = [
  {
    id: "n17-pool",
    title: "Добавьте серверы в пул",
    statement:
      "Сервис вырос, поставили ещё два сервера (10.0.1.12 и 10.0.1.13), но балансировщик по-прежнему шлёт всё на первый. Добавьте оба в пул и убедитесь, что девять запросов раскладываются по трём серверам.",
    hint: "На балансировщике: `lb add 10.0.1.12:80` и `lb add 10.0.1.13:80` либо поле «+ в пул» в карточке. Проверьте командой `lb show`.",
    tools: { lb: true },
    build: () => farm({ backends: [ALL[0]] }),
    goals: [{ id: "g1", text: "9 соединений делятся между тремя серверами", lbspread: { from: "pc", to: "@lb", port: 80, n: 9, distinct: 3 } }],
    solution: [{ cmd: ["lb", "lb add 10.0.1.12:80"] }, { cmd: ["lb", "lb add 10.0.1.13:80"] }],
  },
  {
    id: "n17-health",
    title: "Проверка здоровья",
    statement:
      "В пуле три сервера, но второй не слушает порт 80 — каждый третий запрос получает отказ. Включите проверку здоровья на балансировщике: он перестанет отправлять запросы мёртвому серверу, и все соединения будут успешными.",
    hint: "`lb health on` или флажок «проверка здоровья» в карточке балансировщика. Потом запустите ▶ у цели и посмотрите, на какие серверы попали запросы.",
    tools: { lb: true },
    build: () => farm({ backends: ALL, svc: { s2: [] } }),
    goals: [{ id: "g1", text: "6 соединений: все успешны, второй сервер не задействован", lbspread: { from: "pc", to: "@lb", port: 80, n: 6, avoid: ["s2"] } }],
    solution: [{ cmd: ["lb", "lb health on"] }],
  },
  {
    id: "n17-sticky",
    title: "Привязка клиента к серверу",
    statement:
      "Приложение хранит сессию в памяти сервера: после входа каждый следующий запрос должен попадать на тот же сервер, а сейчас запросы клиента разбросаны по кругу. Переключите алгоритм на привязку по адресу клиента.",
    hint: "`lb algo hash` или выбор «привязка по адресу клиента» в карточке. Помните: это временное решение — лучше выносить сессии во внешнее хранилище.",
    tools: { lb: true },
    build: () => farm({ backends: ALL, algo: "rr", health: true }),
    goals: [{ id: "g1", text: "Все 6 запросов клиента попадают на один сервер", lbspread: { from: "pc", to: "@lb", port: 80, n: 6, distinct: 1, sticky: true } }],
    solution: [{ cmd: ["lb", "lb algo hash"] }],
  },
  {
    id: "n17-rproxy",
    title: "Обратный прокси: маршрутизация по пути",
    statement:
      "Единая точка входа 10.0.0.80 должна разбирать запросы: всё, кроме /api, — на веб-сервер 10.0.2.20:80, а /api — на сервер API 10.0.2.10:8080. Сейчас правил нет, и прокси отвечает «no route». Добавьте два правила, более длинный путь побеждает.",
    hint: "`rproxy add * / 10.0.2.20:80` и `rproxy add * /api 10.0.2.10:8080`. Проверка: `curl http://10.0.0.80/` и `curl http://10.0.0.80/api/items`.",
    tools: { rproxy: true },
    build: () =>
      makeState(
        [
          device("pc", "host", "Клиент", 60, 180, { ifaces: [iface("eth0", { ip: "10.0.0.10" })] }),
          device("rp", "server", "Обратный прокси", 260, 180, {
            ifaces: [iface("eth0", { ip: "10.0.0.80" }), iface("eth1", { ip: "10.0.2.1" })],
            services: [{ proto: "tcp", port: 80 }],
            rproxy: { rules: [] },
          }),
          device("web", "server", "Веб", 520, 80, {
            ifaces: [iface("eth0", { ip: "10.0.2.20" })],
            routes: gw("10.0.2.1"),
            services: [{ proto: "tcp", port: 80 }],
            http: newHttp({ routes: [{ path: "/", status: 200, body: "<h1>Витрина</h1>" }] }),
          }),
          device("api", "server", "API", 520, 280, {
            ifaces: [iface("eth0", { ip: "10.0.2.10" })],
            routes: gw("10.0.2.1"),
            services: [{ proto: "tcp", port: 8080 }],
            http: newHttp({ routes: [{ path: "/api/items", status: 200, type: "application/json", body: '{"items": []}' }] }),
          }),
          device("sw", "switch", "SW", 400, 180, { ifaces: ports(4) }),
        ],
        [link("pc:eth0", "rp:eth0"), link("rp:eth1", "sw:p1"), link("web:eth0", "sw:p2"), link("api:eth0", "sw:p3")],
      ),
    goals: [
      { id: "g1", text: "GET / возвращает витрину", http: { from: "pc", url: "http://10.0.0.80/", status: 200, bodyIncludes: "Витрина" } },
      { id: "g2", text: "GET /api/items возвращает JSON от API", http: { from: "pc", url: "http://10.0.0.80/api/items", status: 200, bodyIncludes: "items" } },
    ],
    solution: [{ cmd: ["rp", "rproxy add * / 10.0.2.20:80"] }, { cmd: ["rp", "rproxy add * /api 10.0.2.10:8080"] }],
  },
  {
    id: "n17-cdn",
    title: "Кэш на узле CDN",
    statement:
      "Узел CDN стоит рядом с клиентом (RTT меньше миллисекунды), а исходный сервер — на другом континенте (около 120 мс). Узел уже передаёт запросы дальше, но ничего не кэширует: каждый ответ приходит издалека. Включите кэш для всех путей и убедитесь: второй запрос отдаётся из кэша заголовком X-Cache: HIT и укладывается в 20 мс.",
    hint: "`rproxy cache / on` на узле или флажок «кэш» у правила. Выполните `curl -I http://cdn.example/logo.png` дважды: первый ответ MISS, второй HIT.",
    tools: { rproxy: true },
    build: () =>
      makeState(
        [
          device("pc", "host", "Клиент", 70, 180, { ifaces: [iface("eth0", { ip: "10.0.0.10" })], hosts: { "cdn.example": "10.0.0.80" } }),
          device("edge", "server", "Узел CDN", 300, 180, {
            ifaces: [iface("eth0", { ip: "10.0.0.80" }), iface("eth1", { ip: "172.16.0.1", prefix: 30 })],
            services: [{ proto: "tcp", port: 80 }],
            rproxy: { rules: [{ path: "/", backend: "172.16.0.2:80" }] },
            routes: [],
          }),
          device("origin", "server", "Исходный сервер", 540, 180, {
            ifaces: [iface("eth0", { ip: "172.16.0.2", prefix: 30 })],
            routes: gw("172.16.0.1"),
            services: [{ proto: "tcp", port: 80 }],
            http: newHttp({ routes: [{ path: "/logo.png", status: 200, type: "image/png", body: "PNG…" }] }),
          }),
        ],
        [link("pc:eth0", "edge:eth0", { km: 20 }), link("edge:eth1", "origin:eth0", { km: 12000 })],
      ),
    goals: [
      { id: "g1", text: "Второй запрос отдаётся из кэша (X-Cache: HIT)", http: { from: "pc", url: "http://cdn.example/logo.png", repeat: 2, status: 200, header: { "x-cache": "HIT" } } },
      { id: "g2", text: "Второй запрос быстрее 20 мс", http: { from: "pc", url: "http://cdn.example/logo.png", repeat: 2, status: 200, maxRttMs: 20 } },
    ],
    solution: [{ cmd: ["edge", "rproxy cache / on"] }],
  },
];
