/* Глава 13 «TLS и HTTPS»: просрочка, имя, цепочка, недоверенный CA, версия протокола. */
import { newHttp } from "../http.ts";
import { device, iface, link, makeState, ports } from "../model.ts";
import { DEFAULT_PKI, newTls } from "../tls.ts";
import type { Scenario } from "../types.ts";

function site({ tls = {}, pcExtra = {}, host = "www.example.org", hostIp = "192.168.0.20" } = {}) {
  return makeState(
    [
      device("pc", "host", "Браузер (ПК)", 80, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.10" })],
        hosts: { [host]: hostIp },
        ...pcExtra,
      }),
      device("sw", "switch", "Коммутатор", 260, 180, { ifaces: ports(4) }),
      device("web", "server", "Веб-сервер", 520, 180, {
        ifaces: [iface("eth0", { ip: hostIp })],
        services: [{ proto: "tcp", port: 443 }],
        http: newHttp({ routes: [{ path: "/", status: 200, body: "<h1>Защищённая главная</h1>" }] }),
        tls: newTls(tls),
      }),
    ],
    [link("pc:eth0", "sw:p1"), link("web:eth0", "sw:p2")],
    { pki: DEFAULT_PKI },
  );
}

const TOOLS = { tls: true };
const OK = { from: "pc", url: "https://www.example.org/", status: 200, bodyIncludes: "Защищённая" };

export const CH13: Scenario[] = [
  {
    id: "n13-expired",
    title: "Сертификат просрочен",
    statement:
      "Сайт перестал открываться по HTTPS: `curl https://www.example.org/` выдаёт «certificate has expired». Проверьте срок на сервере (`tls show`; сегодня 2026-10-16) и выпустите новый сертификат на 90 дней у промежуточного центра PublicIntCA на то же имя.",
    hint: "На сервере: `tls cert new www.example.org --issuer PublicIntCA --days 90`. Цепочка и версии остаются. Проверка: `openssl s_client -connect www.example.org:443`.",
    tools: TOOLS,
    build: () => site({ tls: { cert: { cn: "www.example.org", san: ["www.example.org"], issuer: "PublicIntCA", notAfter: "2026-09-01" } } }),
    goals: [{ id: "g1", text: "HTTPS-запрос возвращает 200", http: OK }],
    solution: [{ cmd: ["web", "tls cert new www.example.org --issuer PublicIntCA --days 90"] }],
  },
  {
    id: "n13-name",
    title: "Имя не совпадает с сертификатом",
    statement:
      "Сертификат выпущен только на example.org, а пользователи открывают www.example.org. Браузер отказывает: имя не найдено среди SAN. Выпустите сертификат, в котором есть оба имени: example.org и www.example.org.",
    hint: "`tls cert new example.org www.example.org --issuer PublicIntCA --days 90` — первое имя становится CN, все перечисленные попадают в SAN.",
    tools: TOOLS,
    build: () => site({ tls: { cert: { cn: "example.org", san: ["example.org"], issuer: "PublicIntCA", notAfter: "2027-01-15" } } }),
    goals: [{ id: "g1", text: "https://www.example.org/ открывается", http: OK }],
    solution: [{ cmd: ["web", "tls cert new example.org www.example.org --issuer PublicIntCA --days 90"] }],
  },
  {
    id: "n13-chain",
    title: "Забытый промежуточный сертификат",
    statement:
      "У вас сайт открывается, у клиентов — «unable to get local issuer certificate». Сервер присылает только листовой сертификат, а выдавший его PublicIntCA клиент не знает: в хранилище доверия только корневой PublicRootCA. Добавьте промежуточный сертификат в цепочку, которую присылает сервер.",
    hint: "`tls chain add PublicIntCA`. Сервер должен присылать листовой и все промежуточные сертификаты; корневой клиент уже знает.",
    tools: TOOLS,
    build: () => site({ tls: { chain: [] } }),
    goals: [{ id: "g1", text: "HTTPS-запрос возвращает 200", http: OK }],
    solution: [{ cmd: ["web", "tls chain add PublicIntCA"] }],
  },
  {
    id: "n13-trust",
    title: "Внутренний центр сертификации",
    statement:
      "Внутренний сервис intranet.corp использует сертификат от корпоративного центра CorpIntCA (его корень — CorpRootCA). Он правильно настроен на сервере: срок, имя и цепочка в порядке. Но корень CorpRootCA нет в хранилище доверия ПК, поэтому браузер ругается на «self-signed certificate in chain». Добавьте CorpRootCA в доверенные на ПК — так делают на корпоративных устройствах. Осторожно: лишний корень в хранилище — дыра в безопасности.",
    hint: "На ПК: `trust show`, затем `trust add CorpRootCA`. Проверка: `curl https://intranet.corp/`.",
    tools: TOOLS,
    build: () =>
      site({
        host: "intranet.corp",
        tls: { cert: { cn: "intranet.corp", san: ["intranet.corp"], issuer: "CorpIntCA", notAfter: "2027-06-01" }, chain: ["CorpIntCA"] },
      }),
    goals: [{ id: "g1", text: "https://intranet.corp/ открывается", http: { from: "pc", url: "https://intranet.corp/", status: 200, bodyIncludes: "Защищённая" } }],
    solution: [{ cmd: ["pc", "trust add CorpRootCA"] }],
  },
  {
    id: "n13-version",
    title: "Старая версия TLS",
    statement:
      "Сервер настроен давно и поддерживает только TLS 1.0 и 1.1: современные клиенты их отключили и получают alert protocol version. Включите на сервере TLS 1.2 и 1.3. Затем выполните `openssl s_client -connect www.example.org:443` и посмотрите, сколько кругов занимает рукопожатие.",
    hint: "`tls versions 1.2,1.3` — клиент выберет самую новую из общих: 1.3, рукопожатие за один круг.",
    tools: TOOLS,
    build: () => site({ tls: { versions: ["1.0", "1.1"] } }),
    goals: [{ id: "g1", text: "HTTPS-запрос возвращает 200", http: OK }],
    solution: [{ cmd: ["web", "tls versions 1.2,1.3"] }],
  },
];
