/* Глава 6 «UDP и сокеты»: слушающие порты, два сервиса, файрвол для UDP, молчание и отказ. */
import { device, iface, link, makeState } from "../model.js";

const gw = (via) => [{ dst: "0.0.0.0/0", via, dev: null }];
const host = (id, name, x, y, ip, prefix = 24, via = null, extra = {}) =>
  device(id, "host", name, x, y, { ifaces: [iface("eth0", { ip, prefix })], routes: via ? gw(via) : [], ...extra });
const server = (id, name, x, y, ip, via, services = [], extra = {}) =>
  device(id, "server", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], services, ...extra });

export const CH06 = [
  {
    id: "n6-listen",
    title: "Сервер не слушает UDP-порт",
    statement:
      "Клиент отправляет датаграммы на порт 5000 сервера, но ничего не получает. В терминале клиента выполните `nc -u 192.168.0.20 5000` и посмотрите на ответ: приходит ICMP «порт недоступен». Запустите на сервере прослушивание UDP-порта 5000 и повторите.",
    hint: "На сервере в терминале: `nc -u -l 5000`. Или в карточке сервера «Слушающие порты»: протокол udp, порт 5000. TCP-порт с тем же номером — это другой сокет, он не поможет.",
    tools: {},
    build: () =>
      makeState(
        [host("pc1", "Клиент", 110, 180, "192.168.0.10"), server("srv", "Сервер", 530, 180, "192.168.0.20", null, [{ proto: "tcp", port: 5000 }])],
        [link("pc1:eth0", "srv:eth0")],
      ),
    goals: [
      { id: "g1", text: "Клиент получает ответ на UDP-порту 5000", udp: { from: "pc1", to: "@srv", port: 5000 } },
      { id: "g2", text: "Порт 5000 по TCP остаётся открытым", tcp: { from: "pc1", to: "@srv", port: 5000 } },
    ],
    solution: [{ cmd: ["srv", "nc -u -l 5000"] }],
  },
  {
    id: "n6-two",
    title: "TCP и UDP на одном сервере",
    statement:
      "Сервер должен отвечать на веб-запросы (TCP, порт 80) и на запросы имён (UDP, порт 53). Сейчас он ничего не слушает. Откройте оба порта и проверьте каждый: TCP-порт 53 при этом должен остаться закрытым — разные протоколы дают разные сокеты.",
    hint: "В карточке сервера секция «Слушающие порты»: выберите протокол tcp, порт 80; затем udp, порт 53. Терминал: `nc -l 80` и `nc -u -l 53`.",
    tools: {},
    build: () =>
      makeState(
        [host("pc1", "Клиент", 110, 180, "192.168.0.10"), server("srv", "Сервер", 530, 180, "192.168.0.20", null)],
        [link("pc1:eth0", "srv:eth0")],
      ),
    goals: [
      { id: "g1", text: "Веб (tcp/80) отвечает", tcp: { from: "pc1", to: "@srv", port: 80 } },
      { id: "g2", text: "DNS (udp/53) отвечает", udp: { from: "pc1", to: "@srv", port: 53 } },
      { id: "g3", text: "TCP-порт 53 закрыт", tcp: { from: "pc1", to: "@srv", port: 53, expect: "fail" } },
    ],
    solution: [{ cmd: ["srv", "nc -l 80"] }, { cmd: ["srv", "nc -u -l 53"] }],
  },
  {
    id: "n6-fw",
    title: "Файрвол: только DNS и веб",
    statement:
      "Домашний шлюз по умолчанию запрещает всё (политика DROP на FORWARD). NAT уже настроен. Откройте для клиентов сети то, что нужно: запросы DNS (udp/53) и веб (tcp/80), а также разрешите ответы на уже установленные соединения. SSH (tcp/22) должен остаться закрытым.",
    hint: "Правила FORWARD по порядку: 1) `-m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT` (ответы), 2) `-p udp --dport 53 -j ACCEPT`, 3) `-p tcp --dport 80 -j ACCEPT`. В форме файрвола выберите состояние «уже установлено» для первого правила.",
    tools: { fw: true },
    build: () => {
      const g = device("gw", "router", "Шлюз", 250, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "203.0.113.2" })],
        routes: gw("203.0.113.1"),
      });
      g.nat.push({ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" });
      g.fw.policy = "DROP";
      return makeState(
        [
          host("pc1", "Клиент", 80, 180, "192.168.0.10", 24, "192.168.0.1"),
          g,
          device("isp", "internet", "Провайдер", 420, 180, {
            ifaces: [iface("eth0", { ip: "203.0.113.1" }), iface("eth1", { ip: "198.51.100.1" })],
            locked: true,
          }),
          server("srv", "Сервер", 575, 180, "198.51.100.10", "198.51.100.1", [
            { proto: "udp", port: 53 },
            { proto: "tcp", port: 80 },
            { proto: "tcp", port: 22 },
          ]),
        ],
        [link("pc1:eth0", "gw:eth0"), link("gw:eth1", "isp:eth0"), link("isp:eth1", "srv:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "DNS-запрос (udp/53) получает ответ", udp: { from: "pc1", to: "@srv", port: 53 } },
      { id: "g2", text: "Веб (tcp/80) открывается", tcp: { from: "pc1", to: "@srv", port: 80 } },
      { id: "g3", text: "SSH (tcp/22) закрыт", tcp: { from: "pc1", to: "@srv", port: 22, expect: "fail" } },
    ],
    solution: [
      { cmd: ["gw", "iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -p udp --dport 53 -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -p tcp --dport 80 -j ACCEPT"] },
    ],
  },
  {
    id: "n6-diagnose",
    title: "Отказ или молчание",
    statement:
      "Два сервера должны отвечать по UDP на порту 5000. Клиент пробует оба. С первым ответ приходит сразу в виде ICMP «порт недоступен» (отказ), со вторым — тишина (пакеты пропадают). Это две разные причины: у первого порт просто не слушает, а у второго что-то режет пакеты по дороге. Исправьте обе.",
    hint: "Первый: на сервере 1 откройте UDP-порт 5000 (`nc -u -l 5000`). Второй: на маршрутизаторе в журнале «файрвол: DROP» — удалите правило, режущее UDP на порт 5000.",
    tools: { fw: true },
    build: () => {
      const r = device("r1", "router", "Маршрутизатор", 250, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "10.0.1.1" }), iface("eth2", { ip: "10.0.2.1" })],
      });
      r.fw.rules.push({ action: "DROP", proto: "udp", dport: 5000, dst: "10.0.2.10" });
      return makeState(
        [
          host("pc1", "Клиент", 70, 180, "192.168.0.10", 24, "192.168.0.1"),
          r,
          server("s1", "Сервер 1", 480, 70, "10.0.1.10", "10.0.1.1"),
          server("s2", "Сервер 2", 480, 290, "10.0.2.10", "10.0.2.1", [{ proto: "udp", port: 5000 }]),
        ],
        [link("pc1:eth0", "r1:eth0"), link("r1:eth1", "s1:eth0"), link("r1:eth2", "s2:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Сервер 1 отвечает по UDP/5000", udp: { from: "pc1", to: "@s1", port: 5000 } },
      { id: "g2", text: "Сервер 2 отвечает по UDP/5000", udp: { from: "pc1", to: "@s2", port: 5000 } },
    ],
    solution: [
      { cmd: ["s1", "nc -u -l 5000"] },
      { cmd: ["r1", "iptables -D FORWARD -p udp --dport 5000 -d 10.0.2.10 -j DROP"] },
    ],
  },
];
