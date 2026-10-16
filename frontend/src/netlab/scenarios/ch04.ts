/* Глава 4 «IP-адресация»: раздача адресов, конфликт, три ошибки, NAT, проброс порта. */
import { device, iface, link, makeState, ports } from "../model.ts";
import type { Scenario, Device } from "../types.ts";
import { gw } from "./helpers.ts";

const host = (id: string, name: string, x: number, y: number, ip: string, prefix = 24, extra: Partial<Device> = {}) =>
  device(id, "host", name, x, y, { ifaces: [iface("eth0", { ip, prefix })], ...extra });
const bare = (id: string, name: string, x: number, y: number) => device(id, "host", name, x, y, { ifaces: [iface("eth0")] });

export const CH04: Scenario[] = [
  {
    id: "n4-plan",
    title: "Раздайте адреса по плану",
    statement:
      "Маршрутизатор настроен, а у четырёх компьютеров адресов нет. Сеть 192.168.10.0/24 разделена на две. Отдел А: 192.168.10.0/26 (шлюз .1, у ПК А1 адрес .2, у ПК А2 — .3). Отдел Б: 192.168.10.64/27 (шлюз .65, ПК Б1 — .66, ПК Б2 — .67). Задайте каждому ПК адрес, маску и шлюз в его карточке и проверьте связь между отделами.",
    hint: "Маска /26 — это 255.255.255.192, /27 — 255.255.255.224. В карточке ПК: IP в первом поле, длина маски после «/», шлюз по умолчанию — внизу. Или в терминале: `ip addr add 192.168.10.2/26 dev eth0`, `ip route add default via 192.168.10.1`.",
    tools: {},
    build: () =>
      makeState(
        [
          bare("pa1", "ПК А1", 90, 80),
          bare("pa2", "ПК А2", 90, 160),
          device("r1", "router", "Маршрутизатор", 320, 120, {
            ifaces: [iface("eth0", { ip: "192.168.10.1", prefix: 26 }), iface("eth1", { ip: "192.168.10.65", prefix: 27 })],
          }),
          bare("pb1", "ПК Б1", 540, 80),
          bare("pb2", "ПК Б2", 540, 160),
          device("sw_a", "switch", "SW А", 200, 120, { ifaces: ports(4) }),
          device("sw_b", "switch", "SW Б", 440, 120, { ifaces: ports(4) }),
        ],
        [
          link("pa1:eth0", "sw_a:p1"),
          link("pa2:eth0", "sw_a:p2"),
          link("sw_a:p3", "r1:eth0"),
          link("pb1:eth0", "sw_b:p1"),
          link("pb2:eth0", "sw_b:p2"),
          link("sw_b:p3", "r1:eth1"),
        ],
      ),
    goals: [
      { id: "g1", text: "ПК А1 пингует ПК А2 (внутри отдела)", ping: { from: "pa1", to: "192.168.10.3" } },
      { id: "g2", text: "ПК А1 пингует ПК Б1 (через маршрутизатор)", ping: { from: "pa1", to: "192.168.10.66" } },
      { id: "g3", text: "ПК Б2 пингует ПК А2", ping: { from: "pb2", to: "192.168.10.3" } },
      { id: "g4", text: "ПК Б1 пингует ПК Б2", ping: { from: "pb1", to: "192.168.10.67" } },
    ],
    solution: [
      { cmd: ["pa1", "ip addr add 192.168.10.2/26 dev eth0"] },
      { cmd: ["pa1", "ip route add default via 192.168.10.1"] },
      { cmd: ["pa2", "ip addr add 192.168.10.3/26 dev eth0"] },
      { cmd: ["pa2", "ip route add default via 192.168.10.1"] },
      { cmd: ["pb1", "ip addr add 192.168.10.66/27 dev eth0"] },
      { cmd: ["pb1", "ip route add default via 192.168.10.65"] },
      { cmd: ["pb2", "ip addr add 192.168.10.67/27 dev eth0"] },
      { cmd: ["pb2", "ip route add default via 192.168.10.65"] },
    ],
  },
  {
    id: "n4-conflict",
    title: "Конфликт адресов",
    statement:
      "ПК 2 и ПК 3 получили один и тот же адрес 192.168.0.20. Пока ПК 1 пингует «двойника», ответы приходят то от одного, то от другого. Запустите ping, посмотрите журнал: ARP-ответы пришли от двух устройств. Смените адрес у одного из компьютеров на свободный (например .30), чтобы у каждого был свой.",
    hint: "Адрес меняется в карточке ПК (поле IP) или командами `ip addr flush dev eth0` и `ip addr add 192.168.0.30/24 dev eth0`.",
    tools: {},
    build: () =>
      makeState(
        [
          host("pc1", "ПК 1", 100, 180, "192.168.0.10"),
          host("pc2", "ПК 2", 540, 80, "192.168.0.20"),
          host("pc3", "ПК 3", 540, 280, "192.168.0.20"),
          device("sw1", "switch", "Коммутатор", 320, 180, { ifaces: ports(4) }),
        ],
        [link("pc1:eth0", "sw1:p1"), link("pc2:eth0", "sw1:p2"), link("pc3:eth0", "sw1:p3")],
      ),
    goals: [
      { id: "g1", text: "ПК 1 пингует 192.168.0.20 без конфликта", ping: { from: "pc1", to: "192.168.0.20" } },
      { id: "g2", text: "ПК 1 пингует 192.168.0.30", ping: { from: "pc1", to: "192.168.0.30" } },
    ],
    solution: [
      { cmd: ["pc3", "ip addr flush dev eth0"] },
      { cmd: ["pc3", "ip addr add 192.168.0.30/24 dev eth0"] },
    ],
  },
  {
    id: "n4-three-errors",
    title: "Три ошибки в настройках",
    statement:
      "Три компьютера подключены к одной сети через коммутатор, и ни один не достаёт до сервера за маршрутизатором. У каждого своя ошибка: у кого-то опечатка в шлюзе, у кого-то неверная маска, у кого-то адрес из чужой подсети. Адрес маршрутизатора в этой сети — 192.168.1.1, маска сети /24. Исправьте настройки так, чтобы все три пинговали сервер.",
    hint: "ПК А: шлюз должен быть адресом маршрутизатора. ПК Б: маска /26 не включает шлюз .1 — нужна /24. ПК В: адрес 192.168.2.x не из этой сети, его нужно поменять на 192.168.1.x.",
    tools: {},
    build: () =>
      makeState(
        [
          host("pa", "ПК А", 90, 60, "192.168.1.10", 24, { routes: gw("192.168.1.254") }),
          host("pb", "ПК Б", 90, 180, "192.168.1.70", 26),
          host("pc", "ПК В", 90, 300, "192.168.2.30", 24),
          device("sw1", "switch", "Коммутатор", 260, 180, { ifaces: ports(6) }),
          device("r1", "router", "Маршрутизатор", 420, 180, {
            ifaces: [iface("eth0", { ip: "192.168.1.1" }), iface("eth1", { ip: "10.0.0.1" })],
          }),
          device("srv", "server", "Сервер", 570, 180, {
            ifaces: [iface("eth0", { ip: "10.0.0.10" })],
            routes: gw("10.0.0.1"),
          }),
        ],
        [
          link("pa:eth0", "sw1:p1"),
          link("pb:eth0", "sw1:p2"),
          link("pc:eth0", "sw1:p3"),
          link("sw1:p4", "r1:eth0"),
          link("r1:eth1", "srv:eth0"),
        ],
      ),
    goals: [
      { id: "g1", text: "ПК А пингует сервер", ping: { from: "pa", to: "@srv" } },
      { id: "g2", text: "ПК Б пингует сервер", ping: { from: "pb", to: "@srv" } },
      { id: "g3", text: "ПК В пингует сервер", ping: { from: "pc", to: "@srv" } },
    ],
    solution: [
      { cmd: ["pa", "ip route del default"] },
      { cmd: ["pa", "ip route add default via 192.168.1.1"] },
      { cmd: ["pb", "ip addr flush dev eth0"] },
      { cmd: ["pb", "ip addr add 192.168.1.70/24 dev eth0"] },
      { cmd: ["pb", "ip route add default via 192.168.1.1"] },
      { cmd: ["pc", "ip addr flush dev eth0"] },
      { cmd: ["pc", "ip addr add 192.168.1.30/24 dev eth0"] },
      { cmd: ["pc", "ip route add default via 192.168.1.1"] },
    ],
  },
  {
    id: "n4-nat",
    title: "Выход в интернет через NAT",
    statement:
      "Домашняя сеть 192.168.0.0/24 с частными адресами и шлюзом, у которого со стороны провайдера публичный адрес 203.0.113.2. Провайдер (его настроить нельзя) не пропускает частные адреса, поэтому запросы ПК до сайта 198.51.100.10 пропадают. Включите на шлюзе подмену адреса (MASQUERADE на интерфейсе, смотрящем в интернет) и убедитесь, что сайт видит адрес шлюза.",
    hint: "Выберите шлюз, в секции «NAT» укажите интерфейс eth1 и нажмите «включить». Или в терминале: `iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE`. Затем нажмите ▶ у цели и посмотрите, как меняется адрес отправителя в журнале.",
    tools: { nat: true },
    build: () =>
      makeState(
        [
          host("pc1", "ПК", 70, 180, "192.168.0.10", 24, { routes: gw("192.168.0.1") }),
          device("gw", "router", "Домашний шлюз", 230, 180, {
            ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "203.0.113.2" })],
            routes: gw("203.0.113.1"),
          }),
          device("isp", "internet", "Провайдер", 400, 180, {
            ifaces: [iface("eth0", { ip: "203.0.113.1" }), iface("eth1", { ip: "198.51.100.1" })],
            locked: true,
          }),
          device("web", "server", "Сайт", 570, 180, {
            ifaces: [iface("eth0", { ip: "198.51.100.10" })],
            routes: gw("198.51.100.1"),
            services: [{ proto: "tcp", port: 80 }],
          }),
        ],
        [link("pc1:eth0", "gw:eth0"), link("gw:eth1", "isp:eth0", { km: 5 }), link("isp:eth1", "web:eth0", { km: 300 })],
      ),
    goals: [
      { id: "g1", text: "ПК пингует сайт", ping: { from: "pc1", to: "@web" } },
      { id: "g2", text: "Сайт видит адрес шлюза 203.0.113.2, а не частный", ping: { from: "pc1", to: "@web", seenSrc: "@gw.eth1" } },
      { id: "g3", text: "ПК открывает порт 80 сайта", tcp: { from: "pc1", to: "@web", port: 80 } },
    ],
    solution: [{ cmd: ["gw", "iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE"] }],
  },
  {
    id: "n4-dnat",
    title: "Проброс порта внутрь сети",
    statement:
      "Во внутренней сети работает веб-сервер 192.168.0.10, порт 80. MASQUERADE уже включён, поэтому изнутри всё работает. Но гость из интернета (198.51.100.50) не может открыть сайт: снаружи виден только публичный адрес шлюза 203.0.113.2. Пробросьте порт 8080 шлюза на 192.168.0.10:80, чтобы гость мог открыть http://203.0.113.2:8080.",
    hint: "На шлюзе в секции «NAT» заполните «Проброс порта»: вход eth1, порт 8080, на 192.168.0.10:80. Или в терминале: `iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 8080 -j DNAT --to-destination 192.168.0.10:80`.",
    tools: { nat: true },
    build: () => {
      const g = device("gw", "router", "Шлюз", 280, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "203.0.113.2" })],
        routes: gw("203.0.113.1"),
      });
      g.nat.push({ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" });
      return makeState(
        [
          device("srv", "server", "Веб-сервер", 90, 180, {
            ifaces: [iface("eth0", { ip: "192.168.0.10" })],
            routes: gw("192.168.0.1"),
            services: [{ proto: "tcp", port: 80 }],
          }),
          g,
          device("isp", "internet", "Провайдер", 440, 180, {
            ifaces: [iface("eth0", { ip: "203.0.113.1" }), iface("eth1", { ip: "198.51.100.1" })],
            locked: true,
          }),
          host("guest", "Гость", 590, 180, "198.51.100.50", 24, { routes: gw("198.51.100.1"), locked: true }),
        ],
        [link("srv:eth0", "gw:eth0"), link("gw:eth1", "isp:eth0"), link("isp:eth1", "guest:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Веб-сервер выходит в интернет (ping гостя)", ping: { from: "srv", to: "@guest" } },
      { id: "g2", text: "Гость открывает 203.0.113.2:8080", tcp: { from: "guest", to: "@gw.eth1", port: 8080 } },
      { id: "g3", text: "Порт 80 шлюза остаётся закрытым", tcp: { from: "guest", to: "@gw.eth1", port: 80, expect: "fail" } },
    ],
    solution: [
      { cmd: ["gw", "iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 8080 -j DNAT --to-destination 192.168.0.10:80"] },
    ],
  },
];
