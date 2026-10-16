/* Глава 16 «Файрволы, прокси и NAT»: проброс портов, зоны и DMZ, hairpin NAT, прокси. */
import { newHttp } from "../http.js";
import { device, iface, link, makeState, ports } from "../model.js";

const gw = (via) => [{ dst: "0.0.0.0/0", via, dev: null }];
const route = (dst, via) => ({ dst, via, dev: null });
const server = (id, name, x, y, ip, via, services = [], extra = {}) =>
  device(id, "server", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], services, ...extra });

export const CH16 = [
  {
    id: "n16-portfwd",
    title: "Два сервиса за одним адресом",
    statement:
      "Снаружи виден один адрес шлюза 203.0.113.2. За ним два сервера: веб (192.168.0.10, порт 80) и SSH (192.168.0.20, порт 22). Нужно пробросить 8080 → 192.168.0.10:80 и 2222 → 192.168.0.20:22. Политика FORWARD — DROP: помните, что фильтр видит уже внутренние адреса и порты, так что разрешить нужно именно их. Остальное снаружи должно оставаться закрытым.",
    hint: "DNAT: `iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 8080 -j DNAT --to-destination 192.168.0.10:80` (и 2222 → 192.168.0.20:22). Разрешения: `iptables -A FORWARD -p tcp -d 192.168.0.10 --dport 80 -j ACCEPT` и `iptables -A FORWARD -p tcp -d 192.168.0.20 --dport 22 -j ACCEPT`.",
    tools: { nat: true, fw: true },
    build: () => {
      const g = device("gw", "router", "Шлюз", 280, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "203.0.113.2" })],
        routes: gw("203.0.113.1"),
      });
      g.nat.push({ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" });
      g.fw.policy = "DROP";
      g.fw.rules.push({ action: "ACCEPT", state: "established" }, { action: "ACCEPT", src: "192.168.0.0/24" });
      return makeState(
        [
          server("web", "Веб (LAN)", 80, 90, "192.168.0.10", "192.168.0.1", [{ proto: "tcp", port: 80 }]),
          server("ssh", "SSH (LAN)", 80, 270, "192.168.0.20", "192.168.0.1", [{ proto: "tcp", port: 22 }]),
          device("sw", "switch", "SW", 180, 180, { ifaces: ports(4) }),
          g,
          device("isp", "internet", "Провайдер", 440, 180, { ifaces: [iface("eth0", { ip: "203.0.113.1" }), iface("eth1", { ip: "198.51.100.1" })], locked: true }),
          device("guest", "host", "Гость", 590, 180, { ifaces: [iface("eth0", { ip: "198.51.100.50" })], routes: gw("198.51.100.1"), locked: true }),
        ],
        [link("web:eth0", "sw:p1"), link("ssh:eth0", "sw:p2"), link("sw:p3", "gw:eth0"), link("gw:eth1", "isp:eth0"), link("isp:eth1", "guest:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Гость открывает 203.0.113.2:8080 (веб)", tcp: { from: "guest", to: "@gw.eth1", port: 8080 } },
      { id: "g2", text: "Гость открывает 203.0.113.2:2222 (SSH)", tcp: { from: "guest", to: "@gw.eth1", port: 2222 } },
      { id: "g3", text: "Прямой порт 80 шлюза снаружи закрыт", tcp: { from: "guest", to: "@gw.eth1", port: 80, expect: "fail" } },
      { id: "g4", text: "Веб-сервер LAN сам выходит в интернет", ping: { from: "web", to: "@guest" } },
    ],
    solution: [
      { cmd: ["gw", "iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 8080 -j DNAT --to-destination 192.168.0.10:80"] },
      { cmd: ["gw", "iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 2222 -j DNAT --to-destination 192.168.0.20:22"] },
      { cmd: ["gw", "iptables -A FORWARD -p tcp -d 192.168.0.10 --dport 80 -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -p tcp -d 192.168.0.20 --dport 22 -j ACCEPT"] },
    ],
  },
  {
    id: "n16-dmz",
    title: "Зоны: LAN, DMZ и интернет",
    statement:
      "Трёхногий файрвол: eth0 — внутренняя сеть LAN, eth1 — демилитаризованная зона с веб-сервером, eth2 — интернет. Политика FORWARD — DROP. Настройте правила: из LAN можно куда угодно; из интернета — только HTTPS (tcp/443) на веб-сервер в DMZ; из DMZ во внутреннюю сеть — ничего; ответы на разрешённые соединения пропускаются.",
    hint: "1) `iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`; 2) `iptables -A FORWARD -i eth0 -j ACCEPT` (всё, что идёт из LAN); 3) `iptables -A FORWARD -p tcp -d 203.0.113.2 --dport 443 -j ACCEPT`. Всё остальное, включая DMZ → LAN, остановит политика DROP.",
    tools: { fw: true },
    build: () => {
      const g = device("gw", "router", "Файрвол", 300, 180, {
        ifaces: [iface("eth0", { ip: "192.0.2.1" }), iface("eth1", { ip: "203.0.113.1", prefix: 29 }), iface("eth2", { ip: "198.51.100.2" })],
        routes: [],
      });
      g.fw.policy = "DROP";
      return makeState(
        [
          device("lan", "host", "ПК (LAN)", 60, 70, { ifaces: [iface("eth0", { ip: "192.0.2.10" })], routes: gw("192.0.2.1") }),
          server("lansrv", "Сервер (LAN)", 60, 290, "192.0.2.20", "192.0.2.1", [{ proto: "tcp", port: 22 }]),
          device("sw", "switch", "SW", 170, 180, { ifaces: ports(4) }),
          g,
          server("dmz", "Веб (DMZ)", 440, 60, "203.0.113.2", "203.0.113.1", [{ proto: "tcp", port: 443 }, { proto: "tcp", port: 22 }]),
          device("guest", "host", "Гость", 590, 290, { ifaces: [iface("eth0", { ip: "198.51.100.50" })], routes: [route("0.0.0.0/0", "198.51.100.2")], locked: true }),
        ],
        [link("lan:eth0", "sw:p1"), link("lansrv:eth0", "sw:p2"), link("sw:p3", "gw:eth0"), link("dmz:eth0", "gw:eth1"), link("gw:eth2", "guest:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "LAN → интернет (ping гостя)", ping: { from: "lan", to: "@guest" } },
      { id: "g2", text: "LAN → веб в DMZ (tcp/443)", tcp: { from: "lan", to: "@dmz", port: 443 } },
      { id: "g3", text: "Гость → веб в DMZ (tcp/443)", tcp: { from: "guest", to: "@dmz", port: 443 } },
      { id: "g4", text: "Гость → DMZ по SSH закрыто", tcp: { from: "guest", to: "@dmz", port: 22, expect: "fail" } },
      { id: "g5", text: "Гость → LAN закрыто", tcp: { from: "guest", to: "@lansrv", port: 22, expect: "fail" } },
      { id: "g6", text: "DMZ → LAN закрыто", tcp: { from: "dmz", to: "@lansrv", port: 22, expect: "fail" } },
    ],
    solution: [
      { cmd: ["gw", "iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -i eth0 -j ACCEPT"] },
      { cmd: ["gw", "iptables -A FORWARD -p tcp -d 203.0.113.2 --dport 443 -j ACCEPT"] },
    ],
  },
  {
    id: "n16-hairpin",
    title: "Петля через шлюз (hairpin NAT)",
    statement:
      "Проброс 203.0.113.2:8080 → 192.168.0.20:80 работает для гостей из интернета, но внутренний клиент, открывая тот же публичный адрес, получает тишину: сервер отвечает ему напрямую, а клиент ждал ответ от 203.0.113.2 и отбрасывает чужой. Добавьте на шлюзе подмену источника для трафика LAN к серверу через интерфейс eth0.",
    hint: "`iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -d 192.168.0.20 -o eth0 -j MASQUERADE` — тогда сервер увидит источником шлюз и вернёт ответ ему, а шлюз развернёт обратно.",
    tools: { nat: true },
    build: () => {
      const g = device("gw", "router", "Шлюз", 280, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "203.0.113.2" })],
        routes: gw("203.0.113.1"),
      });
      g.nat.push({ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" });
      g.nat.push({ chain: "PREROUTING", action: "DNAT", dst: "203.0.113.2", proto: "tcp", dport: 8080, to: "192.168.0.20:80" });
      return makeState(
        [
          device("pc", "host", "Клиент (LAN)", 70, 80, { ifaces: [iface("eth0", { ip: "192.168.0.10" })], routes: gw("192.168.0.1") }),
          server("srv", "Сервер (LAN)", 70, 280, "192.168.0.20", "192.168.0.1", [{ proto: "tcp", port: 80 }]),
          device("sw", "switch", "SW", 170, 180, { ifaces: ports(4) }),
          g,
          device("isp", "internet", "Провайдер", 440, 180, { ifaces: [iface("eth0", { ip: "203.0.113.1" }), iface("eth1", { ip: "198.51.100.1" })], locked: true }),
          device("guest", "host", "Гость", 590, 180, { ifaces: [iface("eth0", { ip: "198.51.100.50" })], routes: gw("198.51.100.1"), locked: true }),
        ],
        [link("pc:eth0", "sw:p1"), link("srv:eth0", "sw:p2"), link("sw:p3", "gw:eth0"), link("gw:eth1", "isp:eth0"), link("isp:eth1", "guest:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Гость открывает 203.0.113.2:8080", tcp: { from: "guest", to: "@gw.eth1", port: 8080 } },
      { id: "g2", text: "Внутренний клиент открывает 203.0.113.2:8080", tcp: { from: "pc", to: "@gw.eth1", port: 8080 } },
    ],
    solution: [{ cmd: ["gw", "iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -d 192.168.0.20 -o eth0 -j MASQUERADE"] }],
  },
  {
    id: "n16-proxy",
    title: "Выход в интернет только через прокси",
    statement:
      "Рабочие станции не должны выходить в интернет напрямую: файрвол пропускает только прокси-сервер 192.168.0.5. Сейчас прокси не может связаться с сайтами (его трафик тоже режется), а политика прокси ничего не запрещает. Разрешите на шлюзе выход прокси-серверу и запретите на прокси сайт social.example. Проверка: `curl -x 192.168.0.5:3128 http://news.example/` должен вернуть 200, а social.example — 403 от прокси.",
    hint: "На шлюзе: `iptables -A FORWARD -s 192.168.0.5 -j ACCEPT`. На прокси: `proxy deny social.example` или форма «запретить». Прямые запросы с рабочей станции остаются закрытыми.",
    tools: { fw: true, proxy: true },
    build: () => {
      const g = device("gw", "router", "Шлюз", 280, 180, {
        ifaces: [iface("eth0", { ip: "192.168.0.1" }), iface("eth1", { ip: "198.51.100.2" })],
        routes: [],
      });
      g.nat.push({ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" });
      g.fw.policy = "DROP";
      g.fw.rules.push({ action: "ACCEPT", state: "established" });
      const site = (id, name, y, ip, body) =>
        device(id, "server", name, 560, y, {
          ifaces: [iface("eth0", { ip })],
          routes: gw("198.51.100.2"),
          services: [{ proto: "tcp", port: 80 }],
          http: newHttp({ routes: [{ path: "/", status: 200, body }] }),
          locked: true,
        });
      return makeState(
        [
          device("pc", "host", "Рабочая станция", 60, 60, { ifaces: [iface("eth0", { ip: "192.168.0.10" })], routes: gw("192.168.0.1") }),
          device("px", "server", "Прокси", 60, 300, {
            ifaces: [iface("eth0", { ip: "192.168.0.5" })],
            routes: gw("192.168.0.1"),
            proxy: { port: 3128, deny: [] },
            services: [{ proto: "tcp", port: 3128 }],
            hosts: { "news.example": "198.51.100.10", "social.example": "198.51.100.20" },
          }),
          device("sw", "switch", "SW", 170, 180, { ifaces: ports(4) }),
          g,
          device("ix", "switch", "Интернет", 430, 180, { ifaces: ports(4), locked: true }),
          site("news", "news.example", 90, "198.51.100.10", "<h1>Новости</h1>"),
          site("social", "social.example", 270, "198.51.100.20", "<h1>Соцсеть</h1>"),
        ],
        [link("pc:eth0", "sw:p1"), link("px:eth0", "sw:p2"), link("sw:p3", "gw:eth0"), link("gw:eth1", "ix:p1"), link("ix:p2", "news:eth0"), link("ix:p3", "social:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Через прокси: news.example → 200", http: { from: "pc", url: "http://news.example/", proxy: "192.168.0.5:3128", status: 200, bodyIncludes: "Новости" } },
      { id: "g2", text: "Через прокси: social.example → 403", http: { from: "pc", url: "http://social.example/", proxy: "192.168.0.5:3128", status: 403 } },
      { id: "g3", text: "Минуя прокси станция в интернет не выходит", ping: { from: "pc", to: "198.51.100.10", expect: "fail" } },
    ],
    solution: [
      { cmd: ["gw", "iptables -A FORWARD -s 192.168.0.5 -j ACCEPT"] },
      { cmd: ["px", "proxy deny social.example"] },
    ],
  },
];
