/* Глава 19 «Атаки и защита»: ARP-спуфинг, SYN-флуд, сканирование, открытая база данных. */
import { device, iface, link, makeState, ports } from "../model.ts";
import type { NetState, Scenario, Device, Service } from "../types.ts";
import { gw } from "./helpers.ts";

const srv = (id: string, name: string, x: number, y: number, ip: string, via: string, services: Service[] = [], extra: Partial<Device> = {}) =>
  device(id, "server", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], services, ...extra });
const host = (id: string, name: string, x: number, y: number, ip: string, via: string, extra: Partial<Device> = {}) =>
  device(id, "host", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], ...extra });

export const CH19: Scenario[] = [
  {
    id: "n19-arp",
    title: "Подмена ARP: трафик идёт через чужой ПК",
    statement:
      "В локальной сети появился ПК злоумышленника 192.168.0.66: он рассылает ложные ARP-ответы, и трафик ПК к шлюзу 192.168.0.1 идёт через него. Посмотрите на ПК `arp -n`: у шлюза не его MAC. Узнайте настоящий MAC шлюза (`ip addr` на шлюзе) и закрепите его на ПК статической записью, чтобы ложные ответы перестали действовать.",
    hint: "На шлюзе: `ip addr` → MAC интерфейса eth0 (28:28:00:00:…). На ПК: `arp -s 192.168.0.1 <этот MAC>`. Проверка: `arp -n` и ▶ у цели — пакеты больше не заходят на ПК злоумышленника.",
    tools: {},
    build: () =>
      makeState(
        [
          host("pc", "ПК жертвы", 70, 80, "192.168.0.10", "192.168.0.1"),
          host("evil", "ПК злоумышленника", 70, 290, "192.168.0.66", "192.168.0.1", {
            forward: true,
            attack: { type: "arpspoof", victim: "pc", gatewayIp: "192.168.0.1" },
          }),
          device("sw", "switch", "SW", 190, 180, { ifaces: ports(4) }),
          device("gw", "router", "Шлюз", 320, 180, { ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "198.51.100.2" })], routes: gw("198.51.100.1"), nat: [{ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" }] }),
          device("isp", "internet", "Интернет", 450, 180, { ifaces: [iface("eth0", { ip: "198.51.100.1" }), iface("eth1", { ip: "203.0.113.1" })], locked: true }),
          srv("web", "Сайт", 580, 180, "203.0.113.10", "203.0.113.1", [{ proto: "tcp", port: 80 }], { locked: true }),
        ],
        [link("pc:eth0", "sw:p1"), link("evil:eth0", "sw:p2"), link("sw:p3", "gw:eth0"), link("gw:eth1", "isp:eth0"), link("isp:eth1", "web:eth0")],
      ),
    goals: [
      { id: "g1", text: "ПК пингует сайт", ping: { from: "pc", to: "@web" } },
      { id: "g2", text: "Трафик ПК не проходит через ПК злоумышленника", ping: { from: "pc", to: "@web", avoid: "evil" } },
    ],
    solution: (st: NetState) => [{ cmd: ["pc", `arp -s 192.168.0.1 ${st.devices.gw.ifaces[0].mac}`] }],
  },
  {
    id: "n19-synflood",
    title: "SYN-флуд на веб-сервер",
    statement:
      "Злоумышленник заваливает сервер SYN-пакетами, и настоящие клиенты не могут подключиться (запрос клиента молчит; в журнале ▶ — «очередь переполнена»). Включите на сервере SYN-куки: тогда состояние до подтверждения не хранится и очередь не переполняется. Можно ещё закрыть источник файрволом, но куки защищают от любых источников.",
    hint: "На сервере: `sysctl -w net.ipv4.tcp_syncookies=1`. Альтернатива на файрволе: `iptables -A FORWARD -s 198.51.100.66 -j DROP`.",
    tools: { fw: true, tcp: true },
    build: () =>
      makeState(
        [
          host("client", "Клиент", 60, 80, "198.51.100.10", "198.51.100.1"),
          host("bot", "Атакующий", 60, 290, "198.51.100.66", "198.51.100.1", { attack: { type: "synflood", target: "web", port: 80 } }),
          device("ix", "switch", "Интернет", 190, 180, { ifaces: ports(4), locked: true }),
          device("fw", "router", "Файрвол", 330, 180, { ifaces: [iface("eth0", { ip: "198.51.100.1" }), iface("eth1", { ip: "203.0.113.1" })] }),
          srv("web", "Веб-сервер", 500, 180, "203.0.113.20", "203.0.113.1", [{ proto: "tcp", port: 80 }]),
        ],
        [link("client:eth0", "ix:p1"), link("bot:eth0", "ix:p2"), link("ix:p3", "fw:eth0"), link("fw:eth1", "web:eth0")],
      ),
    goals: [{ id: "g1", text: "Клиент подключается к порту 80 во время атаки", tcp: { from: "client", to: "@web", port: 80 } }],
    solution: [{ cmd: ["web", "sysctl -w net.ipv4.tcp_syncookies=1"] }],
  },
  {
    id: "n19-scan",
    title: "Найдите сканер и закройте лишнее",
    statement:
      "Кто-то обходит порты сервера. Запустите на шлюзе `tcpdump -i any tcp` и найдите источник: десятки SYN на разные порты с одного адреса. Заблокируйте его на файрволе, закройте на сервере ненужный Telnet (порт 23) и убедитесь, что легитимный пользователь по-прежнему работает с SSH и сайтом.",
    hint: "Источник — 198.51.100.66. На шлюзе: `iptables -A FORWARD -s 198.51.100.66 -j DROP`. На сервере: `close tcp 23`. Порт 3306 (база) должен быть закрыт для всех внешних, он и так не нужен снаружи: закройте его так же `close tcp 3306`.",
    tools: { fw: true },
    build: () =>
      makeState(
        [
          host("user", "Пользователь", 60, 80, "198.51.100.10", "198.51.100.1"),
          host("scanner", "Сканер", 60, 290, "198.51.100.66", "198.51.100.1", { attack: { type: "scan", target: "srv", ports: [21, 22, 23, 80, 443, 3306, 8080] } }),
          device("ix", "switch", "Интернет", 190, 180, { ifaces: ports(4), locked: true }),
          device("gw", "router", "Шлюз", 330, 180, { ifaces: [iface("eth0", { ip: "198.51.100.1" }), iface("eth1", { ip: "203.0.113.1" })] }),
          srv("srv", "Сервер", 500, 180, "203.0.113.20", "203.0.113.1", [
            { proto: "tcp", port: 22 },
            { proto: "tcp", port: 23 },
            { proto: "tcp", port: 80 },
            { proto: "tcp", port: 3306 },
          ]),
        ],
        [link("user:eth0", "ix:p1"), link("scanner:eth0", "ix:p2"), link("ix:p3", "gw:eth0"), link("gw:eth1", "srv:eth0")],
      ),
    goals: [
      { id: "g1", text: "Сканер не достаёт до SSH (порт 22)", tcp: { from: "scanner", to: "@srv", port: 22, expect: "fail" } },
      { id: "g2", text: "Telnet (23) закрыт для пользователя", tcp: { from: "user", to: "@srv", port: 23, expect: "fail" } },
      { id: "g3", text: "База (3306) закрыта снаружи", tcp: { from: "user", to: "@srv", port: 3306, expect: "fail" } },
      { id: "g4", text: "Пользователь по-прежнему работает по SSH", tcp: { from: "user", to: "@srv", port: 22 } },
      { id: "g5", text: "…и открывает сайт (80)", tcp: { from: "user", to: "@srv", port: 80 } },
    ],
    solution: [
      { cmd: ["gw", "iptables -A FORWARD -s 198.51.100.66 -j DROP"] },
      { cmd: ["srv", "close tcp 23"] },
      { cmd: ["srv", "close tcp 3306"] },
    ],
  },
  {
    id: "n19-exposure",
    title: "База данных видна из интернета",
    statement:
      "Во «внутренней» зоне стоят веб (443), сервер приложений и база данных (3306). Политика FORWARD сейчас ACCEPT, поэтому базу видно из интернета. Разрешите порт базы только серверу приложений 203.0.113.20, а всем остальным запретите. Порядок правил важен: сначала разрешение, потом запрет.",
    hint: "`iptables -A FORWARD -p tcp --dport 3306 -s 203.0.113.20 -j ACCEPT`, затем `iptables -A FORWARD -p tcp --dport 3306 -j DROP`. Веб (443) остаётся открытым, так как для него запрета нет.",
    tools: { fw: true },
    build: () =>
      makeState(
        [
          host("guest", "Гость из интернета", 60, 180, "198.51.100.50", "198.51.100.2", { locked: true }),
          device("gw", "router", "Файрвол", 230, 180, { ifaces: [iface("eth0", { ip: "198.51.100.2" }), iface("eth1", { ip: "203.0.113.1" })] }),
          device("sw", "switch", "SW", 350, 180, { ifaces: ports(5) }),
          srv("web", "Веб", 520, 60, "203.0.113.10", "203.0.113.1", [{ proto: "tcp", port: 443 }]),
          srv("app", "Приложение", 520, 180, "203.0.113.20", "203.0.113.1", [{ proto: "tcp", port: 8080 }]),
          srv("db", "База данных", 520, 300, "203.0.113.30", "203.0.113.1", [{ proto: "tcp", port: 3306 }]),
        ],
        [link("guest:eth0", "gw:eth0"), link("gw:eth1", "sw:p1"), link("web:eth0", "sw:p2"), link("app:eth0", "sw:p3"), link("db:eth0", "sw:p4")],
      ),
    goals: [
      { id: "g1", text: "Гость открывает веб (443)", tcp: { from: "guest", to: "@web", port: 443 } },
      { id: "g2", text: "Гость не достаёт до базы (3306)", tcp: { from: "guest", to: "@db", port: 3306, expect: "fail" } },
      { id: "g3", text: "Сервер приложений достаёт до базы", tcp: { from: "app", to: "@db", port: 3306 } },
    ],
    solution: [
      { cmd: ["gw", "iptables -A FORWARD -p tcp --dport 3306 -s 203.0.113.20 -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -p tcp --dport 3306 -j DROP"] },
    ],
  },
];
