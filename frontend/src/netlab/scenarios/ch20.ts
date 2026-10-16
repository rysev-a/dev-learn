/* Глава 20 «Облако и контейнеры»: Docker-мост и публикация, NAT-шлюз VPC, трёхзвенная группа безопасности, сервис Kubernetes. */
import { device, iface, link, makeState, ports } from "../model.ts";
import type { Scenario, Device, Service } from "../types.ts";
import { gw, route } from "./helpers.ts";

const srv = (id: string, name: string, x: number, y: number, ip: string, via: string, services: Service[] = [], extra: Partial<Device> = {}) =>
  device(id, "server", name, x, y, { ifaces: [iface("eth0", { ip })], routes: via ? gw(via) : [], services, ...extra });

export const CH20: Scenario[] = [
  {
    id: "n20-docker",
    title: "Docker: выход и публикация порта",
    statement:
      "На Docker-узле 192.168.0.5 работают контейнеры c1 (172.17.0.2, веб на порту 80) и c2 на мосту br0 (172.17.0.0/16). Пересылка между интерфейсами на узле выключена, подмены адресов нет. Сделайте так, чтобы контейнеры выходили во внешнюю сеть (подмена источника на eth0), а клиенту из локальной сети был доступен веб c1 по адресу узла на порту 8080 (проброс 8080 → 172.17.0.2:80). Прямой порт 80 узла остаётся закрытым.",
    hint: "Три шага на узле: `sysctl -w net.ipv4.ip_forward=1`; `iptables -t nat -A POSTROUTING -s 172.17.0.0/16 -o eth0 -j MASQUERADE`; `iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 -j DNAT --to-destination 172.17.0.2:80`. Именно это Docker делает сам при запуске контейнера с -p 8080:80.",
    tools: { nat: true },
    build: () =>
      makeState(
        [
          device("host", "router", "Docker-узел", 300, 180, {
            ifaces: [iface("eth0", { ip: "192.168.0.5" }), iface("br0", { ip: "172.17.0.1", prefix: 16 })],
            forward: false,
          }),
          device("sw0", "switch", "br0 (мост)", 440, 180, { ifaces: ports(4) }),
          srv("c1", "c1 (веб)", 580, 90, "172.17.0.2", "172.17.0.1", [{ proto: "tcp", port: 80 }]),
          srv("c2", "c2", 580, 270, "172.17.0.3", "172.17.0.1"),
          device("lan", "switch", "LAN", 170, 180, { ifaces: ports(4) }),
          device("pc", "host", "Клиент", 60, 90, { ifaces: [iface("eth0", { ip: "192.168.0.20" })] }),
          device("ext", "host", "Внешний хост", 60, 270, { ifaces: [iface("eth0", { ip: "192.168.0.30" })] }),
        ],
        [
          link("pc:eth0", "lan:p1"),
          link("ext:eth0", "lan:p2"),
          link("lan:p3", "host:eth0"),
          link("host:br0", "sw0:p1"),
          link("c1:eth0", "sw0:p2"),
          link("c2:eth0", "sw0:p3"),
        ],
      ),
    goals: [
      { id: "g1", text: "Контейнер c2 пингует внешний хост (192.168.0.30)", ping: { from: "c2", to: "@ext" } },
      { id: "g2", text: "Клиент открывает веб c1 через узел: 192.168.0.5:8080", tcp: { from: "pc", to: "@host.eth0", port: 8080 } },
      { id: "g3", text: "Порт 80 узла снаружи закрыт", tcp: { from: "pc", to: "@host.eth0", port: 80, expect: "fail" } },
    ],
    solution: [
      { cmd: ["host", "sysctl -w net.ipv4.ip_forward=1"] },
      { cmd: ["host", "iptables -t nat -A POSTROUTING -s 172.17.0.0/16 -o eth0 -j MASQUERADE"] },
      { cmd: ["host", "iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 -j DNAT --to-destination 172.17.0.2:80"] },
    ],
  },
  {
    id: "n20-natgw",
    title: "Приватная подсеть VPC и NAT-шлюз",
    statement:
      "Сервер приложений 10.0.2.10 в приватной подсети должен выходить за обновлениями к репозиторию 198.51.100.10, но оставаться недоступным снаружи. NAT-шлюз (10.0.1.5 в публичной подсети, внешний адрес 203.0.113.9) уже есть. Настройте: маршрут по умолчанию приватной подсети через NAT-шлюз (на маршрутизаторе VPC), подмену источника на шлюзе и обратный маршрут в приватную подсеть на шлюзе.",
    hint: "На VPC-маршрутизаторе: `ip route add default via 10.0.1.5`. На NAT-шлюзе: `iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE` и `ip route add 10.0.2.0/24 via 10.0.1.1`.",
    tools: { nat: true },
    build: () =>
      makeState(
        [
          srv("app", "Сервер приложений", 60, 180, "10.0.2.10", "10.0.2.1"),
          device("vpc", "router", "Маршрутизатор VPC", 200, 180, {
            ifaces: [iface("eth0", { ip: "10.0.2.1" }), iface("eth1", { ip: "10.0.1.1" })],
          }),
          device("natgw", "router", "NAT-шлюз", 350, 180, {
            ifaces: [iface("eth0", { ip: "10.0.1.5" }), iface("eth1", { ip: "203.0.113.9" })],
            routes: gw("203.0.113.254"),
          }),
          device("isp", "internet", "Интернет", 470, 180, { ifaces: [iface("eth0", { ip: "203.0.113.254" }), iface("eth1", { ip: "198.51.100.254" })], locked: true }),
          srv("repo", "Репозиторий", 590, 180, "198.51.100.10", "198.51.100.254", [{ proto: "tcp", port: 443 }], { locked: true }),
        ],
        [link("app:eth0", "vpc:eth0"), link("vpc:eth1", "natgw:eth0"), link("natgw:eth1", "isp:eth0"), link("isp:eth1", "repo:eth0")],
      ),
    goals: [
      { id: "g1", text: "Сервер приложений пингует репозиторий", ping: { from: "app", to: "@repo" } },
      { id: "g2", text: "Репозиторий видит адрес NAT-шлюза", ping: { from: "app", to: "@repo", seenSrc: "@natgw.eth1" } },
      { id: "g3", text: "Репозиторий не достаёт до приватного сервера напрямую", ping: { from: "repo", to: "@app", expect: "fail" } },
    ],
    solution: [
      { cmd: ["vpc", "ip route add default via 10.0.1.5"] },
      { cmd: ["natgw", "iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE"] },
      { cmd: ["natgw", "ip route add 10.0.2.0/24 via 10.0.1.1"] },
    ],
  },
  {
    id: "n20-sg",
    title: "Трёхзвенное приложение: группы безопасности",
    statement:
      "Веб (10.0.1.10), приложение (10.0.2.10) и база (10.0.3.10) в разных подсетях за маршрутизатором VPC. Политика — DROP. Настройте разрешения по принципу минимума: из интернета только HTTPS на веб; веб → приложение на порт 8080; приложение → база на 3306; ответы разрешены. Всё остальное, включая веб → база и интернет → приложение, закрыто.",
    hint: "Правила FORWARD: 1) ESTABLISHED,RELATED; 2) `-p tcp -d 10.0.1.10 --dport 443`; 3) `-p tcp -s 10.0.1.10 -d 10.0.2.10 --dport 8080`; 4) `-p tcp -s 10.0.2.10 -d 10.0.3.10 --dport 3306`. Политика DROP остановит остальное.",
    tools: { fw: true },
    build: () => {
      const r = device("vpc", "router", "VPC-маршрутизатор", 300, 180, {
        ifaces: [iface("eth0", { ip: "198.51.100.2" }), iface("eth1", { ip: "10.0.1.1" }), iface("eth2", { ip: "10.0.2.1" }), iface("eth3", { ip: "10.0.3.1" })],
      });
      r.fw.policy = "DROP";
      return makeState(
        [
          device("guest", "host", "Клиент из интернета", 60, 180, { ifaces: [iface("eth0", { ip: "198.51.100.50" })], routes: [route("0.0.0.0/0", "198.51.100.2")], locked: true }),
          r,
          srv("web", "Веб", 520, 60, "10.0.1.10", "10.0.1.1", [{ proto: "tcp", port: 443 }]),
          srv("app", "Приложение", 520, 180, "10.0.2.10", "10.0.2.1", [{ proto: "tcp", port: 8080 }]),
          srv("db", "База данных", 520, 300, "10.0.3.10", "10.0.3.1", [{ proto: "tcp", port: 3306 }]),
        ],
        [link("guest:eth0", "vpc:eth0"), link("vpc:eth1", "web:eth0"), link("vpc:eth2", "app:eth0"), link("vpc:eth3", "db:eth0")],
      );
    },
    goals: [
      { id: "g1", text: "Интернет → веб (443)", tcp: { from: "guest", to: "@web", port: 443 } },
      { id: "g2", text: "Веб → приложение (8080)", tcp: { from: "web", to: "@app", port: 8080 } },
      { id: "g3", text: "Приложение → база (3306)", tcp: { from: "app", to: "@db", port: 3306 } },
      { id: "g4", text: "Интернет → приложение закрыто", tcp: { from: "guest", to: "@app", port: 8080, expect: "fail" } },
      { id: "g5", text: "Веб → база закрыто", tcp: { from: "web", to: "@db", port: 3306, expect: "fail" } },
    ],
    solution: [
      { cmd: ["vpc", "iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT"] },
      { cmd: ["vpc", "iptables -A FORWARD -p tcp -d 10.0.1.10 --dport 443 -j ACCEPT"] },
      { cmd: ["vpc", "iptables -A FORWARD -p tcp -s 10.0.1.10 -d 10.0.2.10 --dport 8080 -j ACCEPT"] },
      { cmd: ["vpc", "iptables -A FORWARD -p tcp -s 10.0.2.10 -d 10.0.3.10 --dport 3306 -j ACCEPT"] },
    ],
  },
  {
    id: "n20-k8s",
    title: "Service Kubernetes и готовность подов",
    statement:
      "Сервис web (виртуальный адрес 10.96.0.10:80) должен раскладывать запросы по трём подам 10.244.1.5, 10.244.1.6 и 10.244.1.7, но в списке эндпоинтов пока один. К тому же второй под ещё не готов (порт не слушает). Добавьте эндпоинты и включите проверку готовности, чтобы запросы шли только на готовые поды и распределялись между ними.",
    hint: "На узле (kube-proxy): `lb add 10.244.1.6:80`, `lb add 10.244.1.7:80`, `lb health on` — проба готовности исключит под, который не слушает порт.",
    tools: { lb: true },
    build: () =>
      makeState(
        [
          device("client", "host", "Под-клиент", 60, 180, { ifaces: [iface("eth0", { ip: "10.96.0.9" })] }),
          device("kp", "router", "Узел (kube-proxy)", 240, 180, {
            ifaces: [iface("eth0", { ip: "10.96.0.10", prefix: 24 }), iface("eth1", { ip: "10.244.1.1", prefix: 24 })],
            lb: { vip: "10.96.0.10", port: 80, algo: "rr", health: false, backends: [{ ip: "10.244.1.5", port: 80 }] },
          }),
          device("br", "switch", "Мост подов", 390, 180, { ifaces: ports(5) }),
          srv("p1", "под 1", 540, 70, "10.244.1.5", "10.244.1.1", [{ proto: "tcp", port: 80 }]),
          srv("p2", "под 2 (не готов)", 540, 180, "10.244.1.6", "10.244.1.1", []),
          srv("p3", "под 3", 540, 290, "10.244.1.7", "10.244.1.1", [{ proto: "tcp", port: 80 }]),
        ],
        [link("client:eth0", "kp:eth0"), link("kp:eth1", "br:p1"), link("p1:eth0", "br:p2"), link("p2:eth0", "br:p3"), link("p3:eth0", "br:p4")],
      ),
    goals: [
      { id: "g1", text: "6 соединений делятся между готовыми подами", lbspread: { from: "client", to: "@kp", port: 80, n: 6, distinct: 2, avoid: ["p2"] } },
    ],
    solution: [
      { cmd: ["kp", "lb add 10.244.1.6:80"] },
      { cmd: ["kp", "lb add 10.244.1.7:80"] },
      { cmd: ["kp", "lb health on"] },
    ],
  },
];
