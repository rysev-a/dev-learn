/* Глава 11 «HTTP/1.1»: коды, редирект, кэш-заголовки, cookie, ETag. */
import { newHttp } from "../http.js";
import { device, iface, link, makeState, ports } from "../model.js";

function site(routes) {
  return makeState(
    [
      device("pc", "host", "Браузер (ПК)", 80, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.10" })],
        hosts: { "www.example.org": "192.168.0.20" },
      }),
      device("sw", "switch", "Коммутатор", 250, 180, { ifaces: ports(4) }),
      device("web", "server", "Веб-сервер", 520, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.20" })],
        services: [{ proto: "tcp", port: 80 }],
        http: newHttp({ routes }),
      }),
    ],
    [link("pc:eth0", "sw:p1"), link("web:eth0", "sw:p2")],
  );
}

const TOOLS = { http: true };
const HOME = { path: "/", status: 200, body: "<h1>Главная</h1>" };

export const CH11 = [
  {
    id: "n11-404",
    title: "Страница не найдена",
    statement:
      "Ссылка «О нас» ведёт на /about, но сервер отвечает 404 Not Found. Откройте терминал браузера (ПК) и выполните `curl -v http://www.example.org/about`: в стартовой строке ответа виден код. Добавьте на веб-сервере маршрут /about с кодом 200 и текстом, содержащим слово «About».",
    hint: "На сервере: `web route /about 200 About us page` или форма «+ маршрут» (путь /about, код 200, текст). Затем снова curl.",
    tools: TOOLS,
    build: () => site([HOME]),
    goals: [
      { id: "g1", text: "GET /about возвращает 200", http: { from: "pc", url: "http://www.example.org/about", status: 200, bodyIncludes: "About" } },
      { id: "g2", text: "Главная по-прежнему доступна", http: { from: "pc", url: "http://www.example.org/", status: 200 } },
    ],
    solution: [{ cmd: ["web", "web route /about 200 About us page"] }],
  },
  {
    id: "n11-redirect",
    title: "Постоянный редирект",
    statement:
      "Страница /old-page переехала на /new-page, но по старому адресу сейчас 404, и поисковики теряют ссылки. Настройте на сервере постоянное перенаправление 301 со старого адреса на новый. Проверьте двумя способами: `curl -I` показывает 301 и заголовок Location, а `curl -L` доходит до итоговой страницы.",
    hint: "`web redirect /old-page 301 /new-page` или форма с кодом 301 и адресом назначения в последнем поле.",
    tools: TOOLS,
    build: () => site([HOME, { path: "/new-page", status: 200, body: "<h1>Новая страница</h1>" }]),
    goals: [
      { id: "g1", text: "Старый адрес даёт 301 с Location: /new-page", http: { from: "pc", url: "http://www.example.org/old-page", status: 301, header: { location: "/new-page" } } },
      { id: "g2", text: "curl -L доходит до /new-page с кодом 200 за два запроса", http: { from: "pc", url: "http://www.example.org/old-page", follow: true, status: 200, hops: 2, finalUrl: "/new-page" } },
    ],
    solution: [{ cmd: ["web", "web redirect /old-page 301 /new-page"] }],
  },
  {
    id: "n11-cache",
    title: "Кэш: статика надолго, личное — никогда",
    statement:
      "Сайт отдаёт логотип /logo.png и страницу личного кабинета /account без заголовков кэширования. Логотип браузер каждый раз скачивает заново, а страницу кабинета может сохранить общий кэш. Добавьте заголовки: логотипу — Cache-Control: max-age=31536000 (год), личной странице — Cache-Control: no-store.",
    hint: "`web header /logo.png Cache-Control max-age=31536000` и `web header /account Cache-Control no-store`. Проверка: `curl -I http://www.example.org/logo.png`.",
    tools: TOOLS,
    build: () =>
      site([HOME, { path: "/logo.png", status: 200, type: "image/png", body: "PNG…" }, { path: "/account", status: 200, body: "<h1>Личный кабинет</h1>" }]),
    goals: [
      { id: "g1", text: "/logo.png: Cache-Control с max-age=31536000", http: { from: "pc", url: "http://www.example.org/logo.png", status: 200, header: { "cache-control": "max-age=31536000" } } },
      { id: "g2", text: "/account: Cache-Control: no-store", http: { from: "pc", url: "http://www.example.org/account", status: 200, header: { "cache-control": "no-store" } } },
    ],
    solution: [
      { cmd: ["web", "web header /logo.png Cache-Control max-age=31536000"] },
      { cmd: ["web", "web header /account Cache-Control no-store"] },
    ],
  },
  {
    id: "n11-cookie",
    title: "Безопасная cookie сессии",
    statement:
      "После входа на /login сервер выдаёт cookie сессии заголовком Set-Cookie: sid=9f3a без флагов, и любой скрипт на странице её прочитает, а по обычному HTTP она уйдёт открытым текстом. Исправьте заголовок так, чтобы в нём были HttpOnly, Secure и SameSite=Lax.",
    hint: "`web header /login Set-Cookie sid=9f3a; HttpOnly; Secure; SameSite=Lax` — тот же заголовок заменит прежний.",
    tools: TOOLS,
    build: () => site([HOME, { path: "/login", status: 200, body: "<h1>Вход выполнен</h1>", headers: { "set-cookie": "sid=9f3a" } }]),
    goals: [
      { id: "g1", text: "Set-Cookie содержит HttpOnly", http: { from: "pc", url: "http://www.example.org/login", status: 200, header: { "set-cookie": "HttpOnly" } } },
      { id: "g2", text: "Set-Cookie содержит Secure", http: { from: "pc", url: "http://www.example.org/login", status: 200, header: { "set-cookie": "Secure" } } },
      { id: "g3", text: "Set-Cookie содержит SameSite=Lax", http: { from: "pc", url: "http://www.example.org/login", status: 200, header: { "set-cookie": "SameSite=Lax" } } },
    ],
    solution: [{ cmd: ["web", "web header /login Set-Cookie sid=9f3a; HttpOnly; Secure; SameSite=Lax"] }],
  },
  {
    id: "n11-etag",
    title: "Условный запрос и 304",
    statement:
      "Большой справочник /data меняется редко. Клиент, у которого уже есть копия, должен получать короткий ответ 304 Not Modified вместо повторной загрузки. Задайте ресурсу ETag \"v42\" и проверьте: `curl -H \"If-None-Match: \\\"v42\\\"\" -v http://www.example.org/data`.",
    hint: "`web etag /data \"v42\"` (кавычки — часть значения). Запрос с If-None-Match, равным ETag, получит 304 без тела.",
    tools: TOOLS,
    build: () => site([HOME, { path: "/data", status: 200, body: "{...большой справочник...}", type: "application/json" }]),
    goals: [
      { id: "g1", text: "Ответ содержит заголовок ETag", http: { from: "pc", url: "http://www.example.org/data", status: 200, header: { etag: "v42" } } },
      { id: "g2", text: "Повторный запрос с If-None-Match получает 304", http: { from: "pc", url: "http://www.example.org/data", headers: { "if-none-match": '"v42"' }, status: 304 } },
    ],
    solution: [{ cmd: ["web", 'web etag /data "v42"'] }],
  },
];
