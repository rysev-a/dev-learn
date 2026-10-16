/* Глава 1 «Как устроена сеть»: кабели, порты, задержка пути, простая диагностика, сеть сетей. */
import { device, eth, iface, link, makeState, ports } from "../model.ts";
import type { Scenario, Device } from "../types.ts";

const host = (id: string, name: string, x: number, y: number, ip: string, prefix = 24, extra: Partial<Device> = {}) =>
  device(id, "host", name, x, y, { ifaces: [iface("eth0", { ip, prefix })], ...extra });

export const CH01: Scenario[] = [
  {
    id: "n1-cable",
    title: "Соедините два компьютера",
    statement:
      "Два компьютера уже настроены: адреса 192.168.0.1 и 192.168.0.2 в одной подсети. Но между ними нет канала. Нажмите «Кабель», выберите первый узел, затем второй, и проверьте связь командой ping.",
    hint: "Канал — это ребро графа. Без кабеля узлы не могут обменяться даже одним пакетом.",
    tools: { cable: true },
    build: () =>
      makeState(
        [
          host("pc1", "ПК 1", 160, 180, "192.168.0.1"),
          host("pc2", "ПК 2", 480, 180, "192.168.0.2"),
        ],
        [],
      ),
    goals: [{ id: "g1", text: "ПК 1 пингует ПК 2", ping: { from: "pc1", to: "@pc2" } }],
    solution: [{ cable: ["pc1", "pc2"] }],
  },
  {
    id: "n1-switch",
    title: "Коммутатор в центре",
    statement:
      "Четыре компьютера, все в одной подсети 192.168.0.0/24, и один коммутатор. Проложите кабели от каждого компьютера к коммутатору. Напрямую у компьютера всего один порт, а коммутатор соединяет сразу многих. Проверьте, что любой достаёт до любого.",
    hint: "У коммутатора восемь портов. Каждый компьютер подключается своим кабелем к своему порту.",
    tools: { cable: true },
    build: () =>
      makeState(
        [
          host("pc1", "ПК 1", 100, 80, "192.168.0.1"),
          host("pc2", "ПК 2", 100, 280, "192.168.0.2"),
          host("pc3", "ПК 3", 540, 80, "192.168.0.3"),
          host("pc4", "ПК 4", 540, 280, "192.168.0.4"),
          device("sw1", "switch", "Коммутатор", 320, 180, { ifaces: ports(8) }),
        ],
        [],
      ),
    goals: [
      { id: "g1", text: "ПК 1 достаёт до ПК 2", ping: { from: "pc1", to: "@pc2" } },
      { id: "g2", text: "ПК 3 достаёт до ПК 4", ping: { from: "pc3", to: "@pc4" } },
      { id: "g3", text: "ПК 1 достаёт до ПК 4", ping: { from: "pc1", to: "@pc4" } },
    ],
    solution: [
      { cable: ["pc1", "sw1"] },
      { cable: ["pc2", "sw1"] },
      { cable: ["pc3", "sw1"] },
      { cable: ["pc4", "sw1"] },
    ],
  },
  {
    id: "n1-fast-path",
    title: "Короткий путь против длинного",
    statement:
      "К серверу ведут два пути: через маршрутизатор «Быстрый» (кабели по 20 км) и через «Медленный» (по 1500 км). Сейчас ПК использует длинный путь — отсюда большая задержка распространения (около 5 мкс на километр). Откройте терминал ПК, посмотрите ping и traceroute, затем переключите шлюз по умолчанию на быстрый маршрутизатор.",
    hint: "Сначала `ip route` — там строка default. Удалите её: `ip route del default`, затем `ip route add default via 10.0.1.1`. Адрес 10.0.1.1 — это «Быстрый» на стороне ПК.",
    tools: {},
    build: () =>
      makeState(
        [
          device("pc1", "host", "ПК", 90, 180, {
            ifaces: [
              iface("eth0", { ip: "10.0.1.2" }),
              iface("eth1", { ip: "10.0.2.2" }),
            ],
            routes: [{ dst: "0.0.0.0/0", via: "10.0.2.1", dev: null }],
          }),
          device("r_fast", "router", "Быстрый", 320, 80, {
            ifaces: [
              iface("eth0", { ip: "10.0.1.1" }),
              iface("eth1", { ip: "10.0.3.1" }),
            ],
            routes: [],
          }),
          device("r_slow", "router", "Медленный", 320, 290, {
            ifaces: [
              iface("eth0", { ip: "10.0.2.1" }),
              iface("eth1", { ip: "10.0.4.1" }),
            ],
            routes: [{ dst: "10.0.3.0/24", via: "10.0.4.2", dev: null }],
          }),
          device("srv", "server", "Сервер", 550, 180, {
            ifaces: [
              iface("eth0", { ip: "10.0.3.2" }),
              iface("eth1", { ip: "10.0.4.2" }),
            ],
            routes: [
              { dst: "10.0.1.0/24", via: "10.0.3.1", dev: null },
              { dst: "10.0.2.0/24", via: "10.0.4.1", dev: null },
            ],
          }),
        ],
        [
          link("pc1:eth0", "r_fast:eth0", { km: 20 }),
          link("pc1:eth1", "r_slow:eth0", { km: 1500 }),
          link("r_fast:eth1", "srv:eth0", { km: 20 }),
          link("r_slow:eth1", "srv:eth1", { km: 1500 }),
        ],
      ),
    goals: [
      {
        id: "g1",
        text: "Сервер отвечает быстрее 5 мс",
        ping: { from: "pc1", to: "@srv", maxRttMs: 5 },
      },
      {
        id: "g2",
        text: "Пакет идёт через «Быстрый»",
        ping: { from: "pc1", to: "@srv", via: "r_fast" },
      },
    ],
    solution: [
      { cmd: ["pc1", "ip route del default"] },
      { cmd: ["pc1", "ip route add default via 10.0.1.1"] },
    ],
  },
  {
    id: "n1-diagnose",
    title: "Почему не пингуется",
    statement:
      "ПК 1 не достаёт ни до ПК 2, ни до сервера. Адреса настроены верно, ошибок в адресах нет. Найдите две неисправности на нижних уровнях — физическом и канальном — и устраните их. Подсказка: смотрите, что в терминале показывает `ip link` и все ли кабели на месте.",
    hint: "Один порт выключен программно (`ip link set eth0 up` на нужном компьютере), а у сервера нет кабеля — добавьте его через «Кабель».",
    tools: { cable: true },
    build: () =>
      makeState(
        [
          host("pc1", "ПК 1", 100, 90, "192.168.0.1"),
          host("pc2", "ПК 2", 100, 270, "192.168.0.2", 24, {}),
          device("sw1", "switch", "Коммутатор", 320, 180, { ifaces: ports(8) }),
          device("srv", "server", "Сервер", 540, 180, {
            ifaces: [iface("eth0", { ip: "192.168.0.10" })],
            services: [{ proto: "tcp", port: 80 }],
          }),
        ].map((d) => {
          if (d.id === "pc2") d.ifaces[0]!.up = false;
          return d;
        }),
        [link("pc1:eth0", "sw1:p1"), link("pc2:eth0", "sw1:p2")],
      ),
    goals: [
      { id: "g1", text: "ПК 1 пингует ПК 2", ping: { from: "pc1", to: "@pc2" } },
      { id: "g2", text: "ПК 1 пингует сервер", ping: { from: "pc1", to: "@srv" } },
      { id: "g3", text: "ПК 2 открывает порт 80 сервера", tcp: { from: "pc2", to: "@srv", port: 80 } },
    ],
    solution: [
      { cmd: ["pc2", "ip link set eth0 up"] },
      { cable: ["srv", "sw1"] },
    ],
  },
  {
    id: "n1-two-nets",
    title: "Две сети и маршрутизатор",
    statement:
      "ПК А живёт в сети 192.168.1.0/24, ПК Б — в 192.168.2.0/24. Их соединяет маршрутизатор, и он уже настроен. Но компьютеры не знают, куда слать пакеты для чужой сети. Так устроен интернет: сеть сетей. Укажите каждому компьютеру шлюз по умолчанию — адрес маршрутизатора в его сети.",
    hint: "Команда `ip route add default via <адрес маршрутизатора>`. Для ПК А шлюз 192.168.1.1, для ПК Б — 192.168.2.1.",
    tools: {},
    build: () =>
      makeState(
        [
          host("pa", "ПК А", 100, 180, "192.168.1.10"),
          device("r1", "router", "Маршрутизатор", 320, 180, {
            ifaces: [iface("eth0", { ip: "192.168.1.1" }), iface("eth1", { ip: "192.168.2.1" })],
          }),
          host("pb", "ПК Б", 540, 180, "192.168.2.10"),
        ],
        [link("pa:eth0", "r1:eth0"), link("pb:eth0", "r1:eth1")],
      ),
    goals: [
      { id: "g1", text: "ПК А достаёт до ПК Б", ping: { from: "pa", to: "@pb" } },
      { id: "g2", text: "ПК Б достаёт до ПК А", ping: { from: "pb", to: "@pa" } },
    ],
    solution: [
      { cmd: ["pa", "ip route add default via 192.168.1.1"] },
      { cmd: ["pb", "ip route add default via 192.168.2.1"] },
    ],
  },
];

export { eth };
