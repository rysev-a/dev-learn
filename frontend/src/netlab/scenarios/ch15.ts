/* Глава 15 «Диагностика»: потерянный пакет, MTU, привязка сервиса, три уровня сразу. */
import { newDns } from "../dns.ts";
import { newHttp } from "../http.ts";
import { device, iface, link, makeState, ports } from "../model.ts";
import { DEFAULT_PKI, newTls } from "../tls.ts";
import type { Scenario, Device, Route } from "../types.ts";
import { gw, route } from "./helpers.ts";

const router = (id: string, name: string, x: number, y: number, ifs: [string, string, number?][], routes: Route[] = [], extra: Partial<Device> = {}) =>
  device(id, "router", name, x, y, { ifaces: ifs.map(([n, ip, p = 24]) => iface(n, { ip, prefix: p })), routes, ...extra });

export const CH15: Scenario[] = [
  {
    id: "n15-where",
    title: "Где пропал пакет",
    statement:
      "Клиент пингует сервер без проблем, но подключение к порту 8080 молчит — ни отказа, ни ответа. По пути три маршрутизатора. Выполните `traceroute 10.0.4.10` на клиенте, затем `curl 10.0.4.10:8080`, а потом откройте терминалы маршрутизаторов и выполните `tcpdump -i any tcp`. Найдите маршрутизатор, на который SYN приходит, но дальше не уходит, и снимите правило, которое его останавливает.",
    hint: "На том маршрутизаторе, где SYN входит и не выходит, в секции «Файрвол» удалите правило DROP для tcp/8080. Подсказка: журнал ▶ показывает «файрвол: DROP» и устройство.",
    tools: { fw: true },
    build: () => {
      const r2 = router("r2", "R2", 300, 180, [["eth0", "10.0.2.1", 30], ["eth1", "10.0.3.1", 30]], [route("10.0.4.0/24", "10.0.3.2"), route("10.0.1.0/24", "10.0.2.2")]);
      r2.fw.rules.push({ action: "DROP", proto: "tcp", dport: 8080 });
      return makeState(
        [
          device("pc", "host", "Клиент", 40, 180, { ifaces: [iface("eth0", { ip: "10.0.1.10" })], routes: gw("10.0.1.1") }),
          router("r1", "R1", 170, 180, [["eth0", "10.0.1.1"], ["eth1", "10.0.2.2", 30]], [route("10.0.4.0/24", "10.0.2.1")]),
          r2,
          router("r3", "R3", 430, 180, [["eth0", "10.0.3.2", 30], ["eth1", "10.0.4.1"]], gw("10.0.3.1")),
          device("srv", "server", "Сервер", 570, 180, { ifaces: [iface("eth0", { ip: "10.0.4.10" })], routes: gw("10.0.4.1"), services: [{ proto: "tcp", port: 8080 }] }),
        ],
        [link("pc:eth0", "r1:eth0"), link("r1:eth1", "r2:eth0"), link("r2:eth1", "r3:eth0"), link("r3:eth1", "srv:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "ping до сервера проходит", ping: { from: "pc", to: "@srv" } },
      { id: "g2", text: "Порт 8080 сервера открывается", tcp: { from: "pc", to: "@srv", port: 8080 } },
    ],
    solution: [{ cmd: ["r2", "iptables -D FORWARD -p tcp --dport 8080 -j DROP"] }],
  },
  {
    id: "n15-mtu",
    title: "Маленькое проходит, большое — нет",
    statement:
      "Между офисами проложен туннель с MTU 1400, а маршрутизатор R1 блокирует ICMP «frag needed». Клиент шлёт пакеты по 1500 байт с запретом фрагментации, они пропадают, и никто не сообщает об этом отправителю. Определите порог: `ping -c 1 -s 1472 -M do 10.0.2.10` не проходит, `-s 1372` проходит. Выставьте MTU интерфейса клиента, чтобы большие пакеты помещались в туннель (не меньше 1300, чтобы не терять эффективность).",
    hint: "`ip link set eth0 mtu 1400` на клиенте. Размер данных пинга = MTU − 28 байт заголовков: 1400 − 28 = 1372.",
    tools: {},
    build: () =>
      makeState(
        [
          device("pc", "host", "Клиент", 60, 180, { ifaces: [iface("eth0", { ip: "10.0.1.10" })], routes: gw("10.0.1.1") }),
          router("r1", "R1 (ICMP заблокирован)", 230, 180, [["eth0", "10.0.1.1"], ["eth1", "172.16.0.1", 30]], [route("10.0.2.0/24", "172.16.0.2")], { icmpBlock: true }),
          router("r2", "R2", 400, 180, [["eth0", "172.16.0.2", 30], ["eth1", "10.0.2.1"]], gw("172.16.0.1")),
          device("srv", "server", "Сервер", 560, 180, { ifaces: [iface("eth0", { ip: "10.0.2.10" })], routes: gw("10.0.2.1") }),
        ],
        [link("pc:eth0", "r1:eth0"), link("r1:eth1", "r2:eth0", { km: 300, mtu: 1400 }), link("r2:eth1", "srv:eth0")],
      ),
    goals: [
      { id: "g1", text: "Пакет размера MTU клиента с запретом фрагментации проходит", ping: { from: "pc", to: "@srv", sizeFromMtu: true } },
      { id: "g2", text: "MTU клиента не меньше 1300 и не больше 1400", mtu: { dev: "pc", iface: "eth0", min: 1300, max: 1400 } },
    ],
    solution: [{ cmd: ["pc", "ip link set eth0 mtu 1400"] }],
  },
  {
    id: "n15-bind",
    title: "Сервис слушает только localhost",
    statement:
      "Веб-сервис на сервере работает: `curl 127.0.0.1` изнутри отвечает. Но клиенты получают отказ на порту 80. Откройте терминал сервера и выполните `ss -ltn`: сервис слушает 127.0.0.1:80, то есть только локальные подключения. Перепривяжите его, чтобы он слушал все адреса.",
    hint: "На сервере: `listen tcp 80 0.0.0.0` или кнопка «слушать везде» в секции слушающих портов.",
    tools: {},
    build: () =>
      makeState(
        [
          device("pc", "host", "Клиент", 100, 180, { ifaces: [iface("eth0", { ip: "192.168.0.10" })] }),
          device("sw", "switch", "SW", 310, 180, { ifaces: ports(4) }),
          device("srv", "server", "Сервер", 520, 180, { ifaces: [iface("eth0", { ip: "192.168.0.20" })], services: [{ proto: "tcp", port: 80, bind: "127.0.0.1" }] }),
        ],
        [link("pc:eth0", "sw:p1"), link("srv:eth0", "sw:p2")],
      ),
    goals: [
      { id: "g1", text: "Клиент открывает порт 80 сервера", tcp: { from: "pc", to: "@srv", port: 80 } },
      { id: "g2", text: "Сервер по-прежнему слушает порт 80", ping: { from: "pc", to: "@srv" } },
    ],
    solution: [{ cmd: ["srv", "listen tcp 80 0.0.0.0"] }],
  },
  {
    id: "n15-triage",
    title: "Три уровня сразу",
    statement:
      "Пользователь пишет: «https://www.example.org не открывается». На пути три независимые поломки: клиент неверно указал DNS-сервер, сервис на 443-м порту слушает не там, где нужно, а сертификат просрочен. Идите по уровням: `dig www.example.org`, потом `curl -v https://www.example.org/`, `ss -ltn` на сервере, `tls show`. Найдите и исправьте все три причины.",
    hint: "1) на клиенте: `echo \"nameserver 192.168.0.53\" > /etc/resolv.conf`; 2) на сервере: `listen tcp 443 0.0.0.0`; 3) на сервере: `tls cert new www.example.org --issuer PublicIntCA --days 90`.",
    tools: { dns: true, tls: true },
    build: () =>
      makeState(
        [
          device("pc", "host", "Клиент", 60, 180, { ifaces: [iface("eth0", { ip: "192.168.0.10" })], resolver: "192.168.0.35" }),
          device("sw", "switch", "SW", 250, 180, { ifaces: ports(6) }),
          device("res", "server", "DNS-резолвер", 430, 70, {
            ifaces: [iface("eth0", { ip: "192.168.0.53" })],
            dns: newDns({ recursive: true, zones: ["example.org"], records: [{ name: "www.example.org", type: "A", value: "192.168.0.20", ttl: 300 }] }),
          }),
          device("web", "server", "Веб-сервер", 520, 290, {
            ifaces: [iface("eth0", { ip: "192.168.0.20" })],
            services: [{ proto: "tcp", port: 443, bind: "127.0.0.1" }],
            http: newHttp({ routes: [{ path: "/", status: 200, body: "<h1>Защищённая главная</h1>" }] }),
            tls: newTls({ cert: { cn: "www.example.org", san: ["www.example.org"], issuer: "PublicIntCA", notAfter: "2026-08-20" } }),
          }),
        ],
        [link("pc:eth0", "sw:p1"), link("res:eth0", "sw:p2"), link("web:eth0", "sw:p3")],
        { pki: DEFAULT_PKI },
      ),
    goals: [
      { id: "g1", text: "Имя www.example.org разрешается", dns: { from: "pc", name: "www.example.org", expect: "192.168.0.20" } },
      { id: "g2", text: "https://www.example.org/ возвращает 200", http: { from: "pc", url: "https://www.example.org/", status: 200, bodyIncludes: "Защищённая" } },
    ],
    solution: [
      { cmd: ["pc", 'echo "nameserver 192.168.0.53" > /etc/resolv.conf'] },
      { cmd: ["web", "listen tcp 443 0.0.0.0"] },
      { cmd: ["web", "tls cert new www.example.org --issuer PublicIntCA --days 90"] },
    ],
  },
];
