/* Состояние сети: устройства, интерфейсы, кабели. Всё — простые JSON-объекты, чтобы
   решение ученика можно было сохранить строкой, а проверку — повторить на чистой копии. */
import { macStr } from "./ip.js";

let macSeq = 1;

export function iface(name, extra = {}) {
  return { name, mac: macStr(macSeq++), ip: null, prefix: 24, up: true, ...extra };
}

/** устройство: kind — host | server | router | switch | internet (маршрутизатор провайдера) */
export function device(id, kind, name, x, y, extra = {}) {
  const ifaces = extra.ifaces ?? [];
  const d = {
    id,
    kind,
    name,
    x,
    y,
    ifaces,
    routes: [], // [{dst: "10.0.0.0/24", via: "192.168.1.1" | null, dev: "eth0"}]
    forward: kind === "router" || kind === "internet",
    nat: [], // [{chain, action, in, out, src, proto, dport, to}]
    fw: { policy: "ACCEPT", rules: [] }, // цепочка FORWARD
    services: [], // [{proto: "tcp", port: 80}]
    locked: false,
    dropPrivate: kind === "internet",
    ...extra,
  };
  d.ifaces = ifaces;
  return d;
}

export const eth = (n, extra) =>
  Array.from({ length: n }, (_, i) => iface(`eth${i}`, i === 0 ? extra : {}));
export const ports = (n) => Array.from({ length: n }, (_, i) => iface(`p${i + 1}`));

export function link(a, b, extra = {}) {
  return { a, b, km: 0.01, mbps: 1000, ...extra };
}

export function makeState(devices, links, meta = {}) {
  return { devices: Object.fromEntries(devices.map((d) => [d.id, d])), links, ...meta };
}

export const clone = (s) => JSON.parse(JSON.stringify(s));

/** «pc1:eth0» → {dev, port} */
export function ref(s) {
  const [dev, port] = s.split(":");
  return { dev, port };
}

export function linkOf(state, dev, port) {
  const key = `${dev}:${port}`;
  return state.links.find((l) => l.a === key || l.b === key) ?? null;
}

/** по другую сторону кабеля от (dev, port) */
export function peerOf(state, dev, port) {
  const l = linkOf(state, dev, port);
  if (!l) return null;
  const key = `${dev}:${port}`;
  return { ...ref(l.a === key ? l.b : l.a), link: l };
}

export const getIface = (d, name) => d.ifaces.find((i) => i.name === name) ?? null;

export function freePort(state, devId) {
  const d = state.devices[devId];
  return d.ifaces.find((i) => !linkOf(state, devId, i.name)) ?? null;
}

/** добавить кабель между первыми свободными портами; вернёт {ok, error} */
export function connect(state, a, b, extra = {}) {
  if (a === b) return { ok: false, error: "Нельзя соединить устройство с самим собой" };
  const pa = freePort(state, a);
  const pb = freePort(state, b);
  if (!pa) return { ok: false, error: `У «${state.devices[a].name}» нет свободных портов` };
  if (!pb) return { ok: false, error: `У «${state.devices[b].name}» нет свободных портов` };
  state.links.push(link(`${a}:${pa.name}`, `${b}:${pb.name}`, extra));
  return { ok: true };
}

export function disconnect(state, idx) {
  state.links.splice(idx, 1);
}

/** состояние без служебных кэшей — для сохранения в кабинете */
export function strip(state) {
  const s = clone(state);
  delete s.rt;
  return s;
}
