/* Глава 10 «DNS»: резолвер у клиента, записи, псевдонимы, делегирование, hosts, корневой сервер резолвера. */
import { newDns } from "../dns.js";
import { device, iface, link, makeState, ports } from "../model.js";

const gw = (via) => [{ dst: "0.0.0.0/0", via, dev: null }];
const IP = { root: "198.51.100.10", tld: "198.51.100.20", auth: "198.51.100.30", web: "198.51.100.40" };

/** общий мир: ПК и резолвер в локальной сети за NAT, интернет с корнем, TLD, авторитативным сервером и сайтом */
function world({ pcResolver = "192.168.0.53", lock = {}, authRecords, tldDeleg = true, resolverRoot = IP.root, pcExtra = {} } = {}) {
  const gwDev = device("gw", "router", "Шлюз", 250, 180, {
    ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "198.51.100.2" })],
    nat: [{ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" }],
  });
  const devices = [
    device("pc", "host", "ПК", 60, 80, { ifaces: [iface("eth0", { ip: "192.168.0.10" })], routes: gw("192.168.0.1"), resolver: pcResolver || undefined, ...pcExtra }),
    device("res", "server", "Резолвер", 60, 280, {
      ifaces: [iface("eth0", { ip: "192.168.0.53" })],
      routes: gw("192.168.0.1"),
      resolver: "192.168.0.53",
      dns: newDns({ recursive: true, roots: [resolverRoot] }),
    }),
    device("sw", "switch", "SW", 150, 180, { ifaces: ports(4) }),
    gwDev,
    device("ix", "switch", "Интернет", 400, 180, { ifaces: ports(6), locked: true }),
    device("root", "server", "Корень (.)", 560, 50, {
      ifaces: [iface("eth0", { ip: IP.root })],
      dns: newDns({ zones: [""], delegations: [{ zone: "org", ns: IP.tld }] }),
      locked: lock.root ?? true,
    }),
    device("tld", "server", "Сервер .org", 590, 130, {
      ifaces: [iface("eth0", { ip: IP.tld })],
      dns: newDns({ zones: ["org"], delegations: tldDeleg ? [{ zone: "example.org", ns: IP.auth }] : [] }),
      locked: lock.tld ?? true,
    }),
    device("auth", "server", "Авторит. example.org", 590, 230, {
      ifaces: [iface("eth0", { ip: IP.auth })],
      dns: newDns({ zones: ["example.org"], records: authRecords ?? [{ name: "www.example.org", type: "A", value: IP.web, ttl: 300 }] }),
      locked: lock.auth ?? true,
    }),
    device("web", "server", "Сайт", 560, 310, { ifaces: [iface("eth0", { ip: IP.web })], routes: gw(IP.root.replace(/\.\d+$/, ".2")), services: [{ proto: "tcp", port: 80 }], locked: true }),
  ];
  // серверы в интернете отвечают назад через шлюз
  for (const id of ["root", "tld", "auth", "web"]) devices.find((d) => d.id === id).routes = [{ dst: "0.0.0.0/0", via: "198.51.100.2", dev: null }];
  return makeState(devices, [
    link("pc:eth0", "sw:p1"),
    link("res:eth0", "sw:p2"),
    link("sw:p3", "gw:eth0"),
    link("gw:eth1", "ix:p1"),
    link("ix:p2", "root:eth0", { km: 3000 }),
    link("ix:p3", "tld:eth0", { km: 2000 }),
    link("ix:p4", "auth:eth0", { km: 500 }),
    link("ix:p5", "web:eth0", { km: 500 }),
  ]);
}

const TOOLS = { dns: true };

export const CH10 = [
  {
    id: "n10-resolver",
    title: "У клиента нет DNS-сервера",
    statement:
      "ПК открывает сайт по адресу, но не по имени: ping www.example.org отвечает «Temporary failure in name resolution». В локальной сети есть рекурсивный резолвер 192.168.0.53. Укажите его на ПК и убедитесь, что имя разрешается и сайт открывается по имени. Нажмите ▶ у цели и посмотрите путь запроса: резолвер идёт к корню, затем к серверу .org, затем к авторитативному серверу.",
    hint: "На ПК: в карточке поле «DNS-сервер», или `echo \"nameserver 192.168.0.53\" > /etc/resolv.conf`. Проверка: `dig www.example.org` и `cat /etc/resolv.conf`.",
    tools: TOOLS,
    build: () => world({ pcResolver: "" }),
    goals: [
      { id: "g1", text: "www.example.org разрешается в 198.51.100.40", dns: { from: "pc", name: "www.example.org", expect: IP.web } },
      { id: "g2", text: "ПК пингует сайт по имени", ping: { from: "pc", to: "www.example.org" } },
      { id: "g3", text: "ПК открывает порт 80 по имени", tcp: { from: "pc", to: "www.example.org", port: 80 } },
    ],
    solution: [{ cmd: ["pc", 'echo "nameserver 192.168.0.53" > /etc/resolv.conf'] }],
  },
  {
    id: "n10-record",
    title: "Запись указывает на старый сервер",
    statement:
      "Сайт переехал на сервер 198.51.100.40, а в зоне example.org запись www всё ещё ведёт на старый адрес 198.51.100.99, где ничего нет. Вы администратор зоны: зайдите на авторитативный сервер, удалите старую запись и добавьте верную. Проверьте, что имя разрешается и порт 80 по имени открывается.",
    hint: "На авторитативном сервере: в секции DNS-записей удалите запись крестиком и добавьте новую, либо `dns del www.example.org A`, затем `dns add www.example.org A 198.51.100.40`.",
    tools: TOOLS,
    build: () => world({ lock: { auth: false }, authRecords: [{ name: "www.example.org", type: "A", value: "198.51.100.99", ttl: 300 }] }),
    goals: [
      { id: "g1", text: "www.example.org → 198.51.100.40", dns: { from: "pc", name: "www.example.org", expect: IP.web } },
      { id: "g2", text: "Сайт открывается по имени (tcp/80)", tcp: { from: "pc", to: "www.example.org", port: 80 } },
    ],
    solution: [
      { cmd: ["auth", "dns del www.example.org A"] },
      { cmd: ["auth", `dns add www.example.org A ${IP.web}`] },
    ],
  },
  {
    id: "n10-cname",
    title: "Псевдоним CNAME",
    statement:
      "У сайта должно быть второе имя shop.example.org, которое ведёт туда же, куда www. Добавьте на авторитативном сервере запись CNAME, а не второй A: тогда при смене адреса менять придётся одну запись. Проверьте, что резолвер возвращает адрес сайта и порт 80 по новому имени открывается.",
    hint: "`dns add shop.example.org CNAME www.example.org` или форма «+ запись»: имя shop.example.org, тип CNAME, значение www.example.org. Резолвер сам доберётся до A.",
    tools: TOOLS,
    build: () => world({ lock: { auth: false } }),
    goals: [
      { id: "g1", text: "shop.example.org → 198.51.100.40", dns: { from: "pc", name: "shop.example.org", expect: IP.web } },
      { id: "g2", text: "Сайт открывается по имени shop.example.org", tcp: { from: "pc", to: "shop.example.org", port: 80 } },
    ],
    solution: [{ cmd: ["auth", "dns add shop.example.org CNAME www.example.org"] }],
  },
  {
    id: "n10-delegation",
    title: "Разорвано делегирование",
    statement:
      "Сервер верхнего домена .org «забыл», что зона example.org делегирована авторитативному серверу 198.51.100.30, поэтому на запрос www.example.org отвечает NXDOMAIN. Нажмите ▶ у цели и найдите шаг, где цепочка обрывается. Вы управляете сервером .org: восстановите делегирование.",
    hint: "На сервере .org: `dns delegate example.org 198.51.100.30` или форма «+ делегирование» (зона example.org, сервер 198.51.100.30).",
    tools: TOOLS,
    build: () => world({ lock: { tld: false }, tldDeleg: false }),
    goals: [
      { id: "g1", text: "www.example.org разрешается", dns: { from: "pc", name: "www.example.org", expect: IP.web } },
      { id: "g2", text: "Сайт открывается по имени", tcp: { from: "pc", to: "www.example.org", port: 80 } },
    ],
    solution: [{ cmd: ["tld", "dns delegate example.org 198.51.100.30"] }],
  },
  {
    id: "n10-roothint",
    title: "Резолвер не знает корня",
    statement:
      "ПК настроен верно, но на любой запрос резолвер возвращает SERVFAIL: в его настройках стоит неверный адрес корневого сервера 198.51.100.99. Найдите причину по журналу ▶ (резолвер не получает ответа), а затем задайте правильный корневой сервер 198.51.100.10.",
    hint: "На резолвере: `dns root 198.51.100.10` или поле «корневой сервер» в секции DNS. Проверьте `dig www.example.org` на ПК.",
    tools: TOOLS,
    build: () => world({ lock: { }, resolverRoot: "198.51.100.99" }),
    goals: [
      { id: "g1", text: "Имя разрешается через резолвер", dns: { from: "pc", name: "www.example.org", expect: IP.web } },
      { id: "g2", text: "Сайт открывается по имени", tcp: { from: "pc", to: "www.example.org", port: 80 } },
    ],
    solution: [{ cmd: ["res", "dns root 198.51.100.10"] }],
  },
  {
    id: "n10-hosts",
    title: "Файл hosts для проверки",
    statement:
      "Перед запуском нового сайта нужно проверить его по имени staging.example.org на тестовом сервере 198.51.100.40, но в DNS такой записи ещё нет (запрос даёт NXDOMAIN). Не трогая DNS, добавьте локальную подсказку в файл hosts на ПК и убедитесь, что пинг и подключение по имени работают.",
    hint: "На ПК: `echo \"198.51.100.40 staging.example.org\" >> /etc/hosts`; `cat /etc/hosts` покажет файл. Запись hosts побеждает ответ DNS — так бывает и в жизни, когда «сайт не обновляется» у одного человека.",
    tools: TOOLS,
    build: () => world(),
    goals: [
      { id: "g1", text: "В DNS имени по-прежнему нет", dns: { from: "res", name: "staging.example.org", expect: "NXDOMAIN" } },
      { id: "g2", text: "ПК пингует staging.example.org", ping: { from: "pc", to: "staging.example.org" } },
      { id: "g3", text: "ПК открывает порт 80 по этому имени", tcp: { from: "pc", to: "staging.example.org", port: 80 } },
    ],
    solution: [{ cmd: ["pc", 'echo "198.51.100.40 staging.example.org" >> /etc/hosts'] }],
  },
];
