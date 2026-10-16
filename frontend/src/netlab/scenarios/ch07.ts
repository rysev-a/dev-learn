/* Глава 7 «TCP»: отказ и молчание, файрвол с состоянием, режущие ответы правила. */
import { device, iface, link, makeState } from "../model.ts";
import type { Scenario, Device, Service } from "../types.ts";
import { gw } from "./helpers.ts";

const host = (id: string, name: string, x: number, y: number, ip: string, prefix = 24, via: string | null = null, extra: Partial<Device> = {}) =>
  device(id, "host", name, x, y, { ifaces: [iface("eth0", { ip, prefix })], routes: via ? gw(via) : [], ...extra });
const server = (id: string, name: string, x: number, y: number, ip: string, via: string, services: Service[] = [], extra: Partial<Device> = {}) =>
  device(id, "server", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], services, ...extra });

export const CH07: Scenario[] = [
  {
    id: "n7-triage",
    title: "Три сервера: отказ, молчание, успех",
    statement:
      "Клиент пробует подключиться к порту 80 трёх серверов. Сервер 1 отвечает RST (отказ), сервер 2 молчит, сервер 3 работает. Нажмите ▶ у каждой цели и сравните журналы: RST — узел жив, порт закрыт; тишина — пакет пропал по дороге. Исправьте оба сервера: на первом запустите сервис, а второй освободите от правила файрвола.",
    hint: "Сервер 1: `nc -l 80` в его терминале. Сервер 2: на маршрутизаторе найдите правило DROP для tcp порт 80 к 10.0.2.10 в секции «Файрвол» и удалите его.",
    tools: { fw: true },
    build: () => {
      const r = device("r1", "router", "Маршрутизатор", 250, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "10.0.1.1" }), iface("eth2", { ip: "10.0.2.1" }), iface("eth3", { ip: "10.0.3.1" })],
      });
      r.fw.rules.push({ action: "DROP", proto: "tcp", dport: 80, dst: "10.0.2.10" });
      return makeState(
        [
          host("pc1", "Клиент", 70, 180, "192.168.0.10", 24, "192.168.0.1"),
          r,
          server("s1", "Сервер 1", 480, 60, "10.0.1.10", "10.0.1.1"),
          server("s2", "Сервер 2", 480, 180, "10.0.2.10", "10.0.2.1", [{ proto: "tcp", port: 80 }]),
          server("s3", "Сервер 3", 480, 300, "10.0.3.10", "10.0.3.1", [{ proto: "tcp", port: 80 }]),
        ],
        [link("pc1:eth0", "r1:eth0"), link("r1:eth1", "s1:eth0"), link("r1:eth2", "s2:eth0"), link("r1:eth3", "s3:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Сервер 1: порт 80 открыт", tcp: { from: "pc1", to: "@s1", port: 80 } },
      { id: "g2", text: "Сервер 2: порт 80 открыт", tcp: { from: "pc1", to: "@s2", port: 80 } },
      { id: "g3", text: "Сервер 3: порт 80 открыт", tcp: { from: "pc1", to: "@s3", port: 80 } },
    ],
    solution: [
      { cmd: ["s1", "nc -l 80"] },
      { cmd: ["r1", "iptables -D FORWARD -p tcp --dport 80 -d 10.0.2.10 -j DROP"] },
    ],
  },
  {
    id: "n7-sport",
    title: "Рукопожатие обрывается на втором шаге",
    statement:
      "Клиент не может подключиться к веб-серверу: ни отказа, ни ответа. Нажмите ▶ у цели и посмотрите журнал: SYN доходит до сервера, сервер отвечает SYN-ACK, но ответ пропадает в маршрутизаторе — кто-то запретил пересылку пакетов с порта 80. Найдите и удалите это правило.",
    hint: "На маршрутизаторе в секции «Файрвол» есть правило DROP tcp, в логе оно выглядит как «файрвол: DROP». Нужно удалить правило, режущее порт отправителя 80.",
    tools: { fw: true },
    build: () => {
      const r = device("r1", "router", "Маршрутизатор", 320, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "10.0.0.1" })],
      });
      r.fw.rules.push({ action: "DROP", proto: "tcp", sport: 80 });
      return makeState(
        [
          host("pc1", "Клиент", 80, 180, "192.168.0.10", 24, "192.168.0.1"),
          r,
          server("web", "Веб-сервер", 560, 180, "10.0.0.10", "10.0.0.1", [{ proto: "tcp", port: 80 }]),
        ],
        [link("pc1:eth0", "r1:eth0"), link("r1:eth1", "web:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "ping проходит", ping: { from: "pc1", to: "@web" } },
      { id: "g2", text: "Клиент завершает рукопожатие с портом 80", tcp: { from: "pc1", to: "@web", port: 80 } },
    ],
    solution: [{ cmd: ["r1", "iptables -D FORWARD -p tcp --sport 80 -j DROP"] }],
  },
  {
    id: "n7-stateful",
    title: "Файрвол с отслеживанием соединений",
    statement:
      "В локальной сети 192.0.2.0/24 живут клиент и свой веб-сервер (порт 80). Снаружи ходят гости. Нужно: клиент ходит в интернет свободно, гость снаружи свободно открывает только то, что нужно, — но к веб-серверу в локальной сети подключаться не должен, хотя ответы на соединения клиента принимаются. Выставьте политику FORWARD DROP, разрешите «уже установленные» соединения и новые соединения из своей сети.",
    hint: "Правила по порядку: `iptables -P FORWARD DROP`, `iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`, `iptables -A FORWARD -s 192.0.2.0/24 -j ACCEPT`. Новое соединение извне (SYN гостя) не попадёт ни под одно разрешение — политика DROP его отбросит.",
    tools: { fw: true },
    build: () =>
      makeState(
        [
          host("pc1", "Клиент", 70, 70, "192.0.2.10", 24, "192.0.2.1"),
          server("lan", "Веб-сервер LAN", 70, 290, "192.0.2.20", "192.0.2.1", [{ proto: "tcp", port: 80 }]),
          device("sw", "switch", "Коммутатор", 175, 180, { ifaces: [iface("p1"), iface("p2"), iface("p3")] }),
          device("gw", "router", "Шлюз", 300, 180, {
            ifaces: [iface("eth0", { ip: "192.0.2.1" }), iface("eth1", { ip: "203.0.113.2", prefix: 30 })],
            routes: gw("203.0.113.1"),
          }),
          device("isp", "internet", "Провайдер", 440, 180, {
            ifaces: [iface("eth0", { ip: "203.0.113.1", prefix: 30 }), iface("eth1", { ip: "198.51.100.1" }), iface("eth2", { ip: "198.51.101.1" })],
            routes: [{ dst: "192.0.2.0/24", via: "203.0.113.2", dev: null }],
            locked: true,
          }),
          server("web", "Сайт", 580, 90, "198.51.100.10", "198.51.100.1", [{ proto: "tcp", port: 80 }], { locked: true }),
          host("guest", "Гость", 580, 280, "198.51.101.50", 24, "198.51.101.1", { locked: true }),
        ],
        [
          link("pc1:eth0", "sw:p1"),
          link("lan:eth0", "sw:p2"),
          link("sw:p3", "gw:eth0"),
          link("gw:eth1", "isp:eth0"),
          link("isp:eth1", "web:eth0"),
          link("isp:eth2", "guest:eth0"),
        ],
      ),
    goals: [
      { id: "g1", text: "Клиент открывает внешний сайт (tcp/80)", tcp: { from: "pc1", to: "@web", port: 80 } },
      { id: "g2", text: "Гость не открывает веб-сервер локальной сети", tcp: { from: "guest", to: "@lan", port: 80, expect: "fail" } },
      { id: "g3", text: "Клиент по-прежнему видит свой веб-сервер", tcp: { from: "pc1", to: "@lan", port: 80 } },
    ],
    solution: [
      { cmd: ["gw", "iptables -P FORWARD DROP"] },
      { cmd: ["gw", "iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -s 192.0.2.0/24 -j ACCEPT"] },
    ],
  },
];
