/* Глава 12 «HTTP/2 и HTTP/3»: выбор протокола под задержку и потери, открытый UDP/443. */
import { newHttp } from "../http.ts";
import { device, iface, link, makeState } from "../model.ts";
import type { Scenario, Device } from "../types.ts";
import { gw } from "./helpers.ts";

const router = (id: string, x: number, y: number, a: string, b: string) => device(id, "router", "Маршрутизатор", x, y, { ifaces: [iface("eth0", { ip: a }), iface("eth1", { ip: b })] });
const web = (id: string, name: string, x: number, y: number, ip: string, via: string, protocol: "h1" | "h2" | "h3", extra: Partial<Device> = {}) =>
  device(id, "server", name, x, y, {
    ifaces: [iface("eth0", { ip })],
    routes: gw(via),
    services: [{ proto: "tcp", port: 443 }],
    http: newHttp({ routes: [{ path: "/", status: 200, body: "<h1>Главная</h1>" }], page: { count: 40, kb: 50 }, protocol }),
    ...extra,
  });
const TOOLS = { http: true, fw: true };

export const CH12: Scenario[] = [
  {
    id: "n12-h2",
    title: "Много файлов и большая задержка",
    statement:
      "Страница из 41 файла загружается с далёкого сервера (RTT около 120 мс) по HTTP/1.1: браузер получает ресурсы по шесть штук, и каждая «волна» стоит целого круга. Выполните на ПК `pageload https://www.example.org/` — в таблице видно, сколько заняла бы загрузка по каждой версии. Включите на сервере протокол, который отдаёт все ресурсы одним соединением параллельно, и уложите загрузку в 1,3 секунды.",
    hint: "На сервере: переключатель «протокол» в карточке — HTTP/2, или `web protocol h2`. HTTP/3 здесь не нужен: потерь на канале нет.",
    tools: TOOLS,
    build: () =>
      makeState(
        [
          device("pc", "host", "Браузер (ПК)", 70, 180, { ifaces: [iface("eth0", { ip: "10.0.0.10" })], routes: gw("10.0.0.1"), hosts: { "www.example.org": "10.0.1.10" } }),
          router("r1", 310, 180, "10.0.0.1", "10.0.1.1"),
          web("web", "Сайт", 560, 180, "10.0.1.10", "10.0.1.1", "h1"),
        ],
        [link("pc:eth0", "r1:eth0", { km: 20 }), link("r1:eth1", "web:eth0", { km: 11960, mbps: 100 })],
      ),
    goals: [{ id: "g1", text: "Страница загружается за 1,3 с или быстрее", page: { from: "pc", to: "www.example.org", maxS: 1.3 } }],
    solution: [{ cmd: ["web", "web protocol h2"] }],
  },
  {
    id: "n12-h3",
    title: "Мобильная сеть с потерями: нужен HTTP/3",
    statement:
      "Клиенты ходят по мобильной сети: RTT около 120 мс и потери 2%. На потерях HTTP/2 страдает от блокировки на TCP, и загрузка занимает несколько секунд. Переведите сайт на HTTP/3, но помните: он живёт на UDP/443. Нажмите «Проверить» и посмотрите на причину: сервер должен слушать udp/443, а файрвол маршрутизатора не должен резать этот порт. Цель — загрузка не дольше 2 с.",
    hint: "Три шага: 1) `web protocol h3`; 2) на сервере слушать UDP: `nc -u -l 443` или форма «Слушающие порты» (udp, 443); 3) на маршрутизаторе удалить правило, режущее UDP/443. Проверка: `pageload https://www.example.org/` (там же видно откат на HTTP/2).",
    tools: TOOLS,
    build: () => {
      const r = router("r1", 310, 180, "10.0.0.1", "10.0.1.1");
      r.fw.rules.push({ action: "DROP", proto: "udp", dport: 443 });
      return makeState(
        [
          device("pc", "host", "Браузер (ПК)", 70, 180, { ifaces: [iface("eth0", { ip: "10.0.0.10" })], routes: gw("10.0.0.1"), hosts: { "www.example.org": "10.0.1.10" } }),
          r,
          web("web", "Сайт", 560, 180, "10.0.1.10", "10.0.1.1", "h2"),
        ],
        [link("pc:eth0", "r1:eth0", { km: 20 }), link("r1:eth1", "web:eth0", { km: 11960, mbps: 100, loss: 2 })],
      );
    },
    goals: [
      { id: "g1", text: "Страница загружается за 2 с или быстрее", page: { from: "pc", to: "www.example.org", maxS: 2 } },
      { id: "g2", text: "UDP/443 доходит до сервера", udp: { from: "pc", to: "@web", port: 443 } },
    ],
    solution: [
      { cmd: ["web", "web protocol h3"] },
      { cmd: ["web", "nc -u -l 443"] },
      { cmd: ["r1", "iptables -D FORWARD -p udp --dport 443 -j DROP"] },
    ],
  },
  {
    id: "n12-choose",
    title: "Новее — не значит лучше",
    statement:
      "Два сайта в разных условиях. Первый (`www.example.org`) далеко, потерь нет. Второй (`app.example.org`) — по ненадёжному каналу с потерями 2%, а корпоративная политика полностью запрещает UDP, так что HTTP/3 недоступен. Выберите на каждом сервере тот протокол, при котором страница грузится быстрее: первый должен укладываться в 1,6 с, второй — в 2,5 с.",
    hint: "Первый: HTTP/2 — потерь нет, мультиплексирование выигрывает. Второй: из доступных HTTP/1.1 и HTTP/2 при потерях лучше HTTP/1.1: шесть соединений не блокируют друг друга. Сравните таблицы `pageload`.",
    tools: TOOLS,
    build: () => {
      const r1 = device("r1", "router", "Маршрутизатор (политика: UDP запрещён)", 270, 180, {
        ifaces: [iface("eth0", { ip: "10.0.0.1" }), iface("eth1", { ip: "10.0.1.1" }), iface("eth2", { ip: "10.0.2.1" })],
        locked: true,
      });
      r1.fw.rules.push({ action: "DROP", proto: "udp" });
      return makeState(
        [
          device("pc", "host", "Браузер (ПК)", 60, 180, {
            ifaces: [iface("eth0", { ip: "10.0.0.10" })],
            routes: gw("10.0.0.1"),
            hosts: { "www.example.org": "10.0.1.10", "app.example.org": "10.0.2.10" },
          }),
          r1,
          web("w1", "www.example.org", 560, 80, "10.0.1.10", "10.0.1.1", "h1"),
          web("w2", "app.example.org", 560, 290, "10.0.2.10", "10.0.2.1", "h1"),
        ],
        [
          link("pc:eth0", "r1:eth0", { km: 20 }),
          link("r1:eth1", "w1:eth0", { km: 15980, mbps: 100 }),
          link("r1:eth2", "w2:eth0", { km: 9980, mbps: 100, loss: 2 }),
        ],
      );
    },
    goals: [
      { id: "g1", text: "www.example.org загружается за 1,6 с или быстрее", page: { from: "pc", to: "www.example.org", maxS: 1.6 } },
      { id: "g2", text: "app.example.org загружается за 2,5 с или быстрее", page: { from: "pc", to: "app.example.org", maxS: 2.5 } },
    ],
    solution: [{ cmd: ["w1", "web protocol h2"] }],
  },
];
