/* Глава 18 «SSH, VPN и туннели»: ключи входа, смена ключа хоста, бастион, VPN между офисами, раздельный туннель. */
import { device, iface, link, makeState, ports } from "../model.js";
import { newSsh } from "../ssh.js";

const gw = (via) => [{ dst: "0.0.0.0/0", via, dev: null }];
const route = (dst, via, dev = null) => ({ dst, via, dev });
const tun = (name, ip, prefix, peer, key) => ({ name, mac: "00:00:00:00:00:00", ip, prefix, up: true, tun: { peer, port: 51820, key } });
const box = (id, name, x, y, ip, via, extra = {}) =>
  device(id, "server", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], services: [{ proto: "tcp", port: 22 }], ...extra });

export const CH18 = [
  {
    id: "n18-keys",
    title: "Вход по ключу вместо пароля",
    statement:
      "Сервер пускает пользователя alice по паролю alice123, и ботам этого достаточно. Нужно перейти на ключи. На ПК создайте ключ (`ssh-keygen`), скопируйте его на сервер (`ssh-copy-id -P alice123 alice@192.168.0.20`; пароль нужен один раз), проверьте вход по ключу, а затем выключите парольный вход на сервере (`sshd password off`).",
    hint: "Порядок важен: сначала ключ и копирование, потом отключение паролей — иначе вы отрежете себе вход. Проверка: `ssh alice@192.168.0.20` входит по ключу, `ssh -o PubkeyAuthentication=no -P alice123 alice@192.168.0.20` — отказ.",
    tools: { ssh: true },
    build: () =>
      makeState(
        [
          device("pc", "host", "ПК админа", 100, 180, { ifaces: [iface("eth0", { ip: "192.168.0.10" })] }),
          device("sw", "switch", "SW", 310, 180, { ifaces: ports(4) }),
          box("srv", "Сервер", 520, 180, "192.168.0.20", null, { ssh: newSsh({ users: { alice: { keys: [], password: "alice123" } } }) }),
        ],
        [link("pc:eth0", "sw:p1"), link("srv:eth0", "sw:p2")],
      ),
    goals: [
      { id: "g1", text: "Вход alice по ключу работает", ssh: { from: "pc", to: "@srv", user: "alice", auth: "key" } },
      { id: "g2", text: "Вход по паролю закрыт", ssh: { from: "pc", to: "@srv", user: "alice", auth: "password", pass: "alice123", expect: "fail" } },
    ],
    solution: [
      { cmd: ["pc", "ssh-keygen"] },
      { cmd: ["pc", "ssh-copy-id -P alice123 alice@192.168.0.20"] },
      { cmd: ["srv", "sshd password off"] },
    ],
  },
  {
    id: "n18-hostkey",
    title: "Ключ хоста изменился",
    statement:
      "После переустановки сервера (администратор подтвердил: смена ключа плановая) вход выдаёт «REMOTE HOST IDENTIFICATION HAS CHANGED». В known_hosts клиента остался старый ключ. Удалите устаревшую запись для 192.168.0.20 (`ssh-keygen -R 192.168.0.20`) и войдите снова — клиент запомнит новый ключ.",
    hint: "`ssh-keygen -R 192.168.0.20`, затем `ssh alice@192.168.0.20`. Не выключайте проверку ключа хоста навсегда: она защищает от подмены сервера.",
    tools: { ssh: true },
    build: () => {
      const pc = device("pc", "host", "ПК админа", 100, 180, { ifaces: [iface("eth0", { ip: "192.168.0.10" })], sshKey: "SHA256:pcKeyOK", knownHosts: { "192.168.0.20": "SHA256:hostKeyOLD" } });
      return makeState(
        [
          pc,
          device("sw", "switch", "SW", 310, 180, { ifaces: ports(4) }),
          box("srv", "Сервер (новый)", 520, 180, "192.168.0.20", null, { ssh: newSsh({ hostKey: "SHA256:hostKeyNEW", passwordAuth: false, users: { alice: { keys: ["SHA256:pcKeyOK"] } } }) }),
        ],
        [link("pc:eth0", "sw:p1"), link("srv:eth0", "sw:p2")],
      );
    },
    goals: [
      { id: "g1", text: "Вход alice по ключу выполняется", ssh: { from: "pc", to: "@srv", user: "alice", auth: "key" } },
    ],
    solution: [{ cmd: ["pc", "ssh-keygen -R 192.168.0.20"] }],
  },
  {
    id: "n18-jump",
    title: "Бастион: вход во внутреннюю сеть",
    statement:
      "Сервер 10.0.2.20 во внутренней сети доступен по SSH только с бастиона 10.0.1.5 — так настроен файрвол. Напрямую с ПК он недоступен. Настройте вход `ssh -J alice@10.0.1.5 alice@10.0.2.20` (ключ клиента уже создан): разрешите ключ ПК (`ssh-keygen -l` покажет отпечаток) и на бастионе, и на внутреннем сервере для пользователя alice. Парольный вход там выключен.",
    hint: "`ssh-keygen -l` на ПК → отпечаток. На бастионе и на внутреннем сервере: `sshd authorize alice <отпечаток>`. Затем `ssh -J alice@10.0.1.5 alice@10.0.2.20`.",
    tools: { ssh: true, fw: true },
    build: () => {
      const r = device("r", "router", "Маршрутизатор", 280, 180, {
        ifaces: [iface("eth0", { ip: "10.0.0.1" }), iface("eth1", { ip: "10.0.1.1" }), iface("eth2", { ip: "10.0.2.1" })],
      });
      r.fw.rules.push({ action: "ACCEPT", proto: "tcp", dport: 22, src: "10.0.1.5", dst: "10.0.2.20" }, { action: "DROP", proto: "tcp", dport: 22, dst: "10.0.2.20" });
      return makeState(
        [
          device("pc", "host", "ПК админа", 60, 180, { ifaces: [iface("eth0", { ip: "10.0.0.10" })], routes: gw("10.0.0.1"), sshKey: "SHA256:pcKeyOK" }),
          r,
          box("bast", "Бастион", 520, 60, "10.0.1.5", "10.0.1.1", { ssh: newSsh({ hostKey: "SHA256:bastKey", passwordAuth: false, users: { alice: { keys: [] } } }) }),
          box("int", "Внутренний сервер", 520, 300, "10.0.2.20", "10.0.2.1", { ssh: newSsh({ hostKey: "SHA256:intKey", passwordAuth: false, users: { alice: { keys: [] } } }) }),
        ],
        [link("pc:eth0", "r:eth0"), link("r:eth1", "bast:eth0"), link("r:eth2", "int:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Вход на внутренний сервер через бастион", ssh: { from: "pc", to: "@int", via: "@bast", user: "alice", auth: "key" } },
      { id: "g2", text: "Напрямую с ПК внутренний сервер закрыт", ssh: { from: "pc", to: "@int", user: "alice", expect: "fail" } },
    ],
    solution: [
      { cmd: ["bast", "sshd authorize alice SHA256:pcKeyOK"] },
      { cmd: ["int", "sshd authorize alice SHA256:pcKeyOK"] },
    ],
  },
  {
    id: "n18-vpn",
    title: "VPN между двумя офисами",
    statement:
      "Офисы А (192.168.1.0/24) и Б (192.168.2.0/24) связаны только через интернет, а интернет не маршрутизирует частные адреса. Постройте туннель между шлюзами: на шлюзе А пир 198.51.100.1, адрес туннеля 10.9.0.1/30; на шлюзе Б пир 203.0.113.1, адрес 10.9.0.2/30; общий секрет у обоих одинаковый. Затем добавьте маршруты в чужие сети через туннель.",
    hint: "`vpn add wg0 --peer 198.51.100.1 --address 10.9.0.1/30 --key s3cr3t` на А и `vpn add wg0 --peer 203.0.113.1 --address 10.9.0.2/30 --key s3cr3t` на Б. Маршруты: на А `ip route add 192.168.2.0/24 dev wg0`, на Б `ip route add 192.168.1.0/24 dev wg0`. Выполните ▶ и найдите в журнале упаковку «туннель wg0».",
    tools: { vpn: true },
    build: () =>
      makeState(
        [
          device("pa", "host", "ПК офиса А", 60, 80, { ifaces: [iface("eth0", { ip: "192.168.1.10" })], routes: gw("192.168.1.1") }),
          device("ga", "router", "Шлюз А", 190, 180, { ifaces: [iface("eth0", { ip: "192.168.1.1" }), iface("eth1", { ip: "203.0.113.1" })], routes: gw("203.0.113.254") }),
          device("isp", "internet", "Интернет", 320, 180, { ifaces: [iface("eth0", { ip: "203.0.113.254" }), iface("eth1", { ip: "198.51.100.254" })], locked: true }),
          device("gb", "router", "Шлюз Б", 450, 180, { ifaces: [iface("eth0", { ip: "192.168.2.1" }), iface("eth1", { ip: "198.51.100.1" })], routes: gw("198.51.100.254") }),
          device("pb", "host", "ПК офиса Б", 580, 80, { ifaces: [iface("eth0", { ip: "192.168.2.10" })], routes: gw("192.168.2.1") }),
        ],
        [link("pa:eth0", "ga:eth0"), link("ga:eth1", "isp:eth0", { km: 400 }), link("isp:eth1", "gb:eth1", { km: 400 }), link("gb:eth0", "pb:eth0")],
      ),
    goals: [
      { id: "g1", text: "ПК А достаёт до ПК Б (частные адреса через интернет)", ping: { from: "pa", to: "@pb" } },
      { id: "g2", text: "ПК Б достаёт до ПК А", ping: { from: "pb", to: "@pa" } },
      { id: "g3", text: "Трафик между офисами идёт через шлюзы по туннелю", ping: { from: "pa", to: "@pb", via: "gb" } },
    ],
    solution: [
      { cmd: ["ga", "vpn add wg0 --peer 198.51.100.1 --address 10.9.0.1/30 --key s3cr3t"] },
      { cmd: ["gb", "vpn add wg0 --peer 203.0.113.1 --address 10.9.0.2/30 --key s3cr3t"] },
      { cmd: ["ga", "ip route add 192.168.2.0/24 dev wg0"] },
      { cmd: ["gb", "ip route add 192.168.1.0/24 dev wg0"] },
    ],
  },
  {
    id: "n18-split",
    title: "Раздельный туннель",
    statement:
      "Ноутбук сотрудника дома: туннель к корпоративному шлюзу уже поднят, но маршрут по умолчанию ведёт в туннель — весь интернет идёт через офис, да и сам туннель потерял путь к пиру (ping в корпоративную сеть не проходит). Сделайте раздельный туннель: корпоративные сети 10.0.0.0/8 — в туннель (wg0), всё остальное — напрямую через домашний роутер 192.168.100.1.",
    hint: "`ip route del default`, затем `ip route add default via 192.168.100.1` и `ip route add 10.0.0.0/8 dev wg0`. Проверьте: ping 10.0.0.5 идёт через корпоративный шлюз, ping 198.51.100.10 — нет.",
    tools: { vpn: true },
    build: () =>
      makeState(
        [
          device("lap", "host", "Ноутбук дома", 50, 180, {
            ifaces: [iface("eth0", { ip: "192.168.100.10" }), tun("wg0", "10.9.0.2", 30, "203.0.113.1", "s3cr3t")],
            routes: [route("0.0.0.0/0", null, "wg0")],
          }),
          device("hgw", "router", "Домашний роутер", 190, 180, {
            ifaces: [iface("eth0", { ip: "192.168.100.1" }), iface("eth1", { ip: "203.0.113.50" })],
            routes: gw("203.0.113.254"),
            nat: [{ chain: "POSTROUTING", action: "MASQUERADE", out: "eth1" }],
          }),
          device("ix", "switch", "Интернет", 320, 180, { ifaces: ports(5), locked: true }),
          device("cgw", "router", "Корп. шлюз", 440, 80, {
            ifaces: [iface("eth0", { ip: "10.0.0.1" }), iface("eth1", { ip: "203.0.113.1" }), tun("wg0", "10.9.0.1", 30, "203.0.113.50", "s3cr3t")],
            routes: gw("203.0.113.254"),
          }),
          device("corp", "server", "Корп. сервер", 580, 80, { ifaces: [iface("eth0", { ip: "10.0.0.5" })], routes: [route("0.0.0.0/0", "10.0.0.1")] }),
          device("isp", "internet", "Провайдер", 440, 250, { ifaces: [iface("eth0", { ip: "203.0.113.254" }), iface("eth1", { ip: "198.51.100.254" })], locked: true }),
          device("web", "server", "Публичный сайт", 580, 250, { ifaces: [iface("eth0", { ip: "198.51.100.10" })], routes: gw("198.51.100.254"), locked: true }),
        ],
        [link("lap:eth0", "hgw:eth0"), link("hgw:eth1", "ix:p1"), link("cgw:eth1", "ix:p2"), link("isp:eth0", "ix:p3"), link("cgw:eth0", "corp:eth0"), link("isp:eth1", "web:eth0")],
      ),
    goals: [
      { id: "g1", text: "Корпоративный сервер 10.0.0.5 доступен через туннель", ping: { from: "lap", to: "@corp", via: "cgw" } },
      { id: "g2", text: "Публичный сайт идёт напрямую, мимо корпоративного шлюза", ping: { from: "lap", to: "@web", avoid: "cgw" } },
    ],
    solution: [
      { cmd: ["lap", "ip route del default"] },
      { cmd: ["lap", "ip route add default via 192.168.100.1"] },
      { cmd: ["lap", "ip route add 10.0.0.0/8 dev wg0"] },
    ],
  },
];
