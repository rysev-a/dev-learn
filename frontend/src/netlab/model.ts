/* Состояние сети: устройства, интерфейсы, кабели. Всё — простые JSON-объекты, чтобы
   решение ученика можно было сохранить строкой, а проверку — повторить на чистой копии. */
import { macStr } from "./ip.ts";
import type { Device, DeviceKind, Iface, Link, NetState } from "./types.ts";

let macSeq = 1;

export function iface(name: string, extra: Partial<Iface> = {}): Iface {
  return { name, mac: macStr(macSeq++), ip: null, prefix: 24, up: true, ...extra };
}

/** устройство: kind — host | server | router | switch | internet (маршрутизатор провайдера) */
export function device(
  id: string,
  kind: DeviceKind,
  name: string,
  x: number,
  y: number,
  extra: Partial<Device> = {},
): Device {
  const ifaces = extra.ifaces ?? [];
  const d: Device = {
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

export const eth = (n: number, extra?: Partial<Iface>): Iface[] =>
  Array.from({ length: n }, (_, i) => iface(`eth${i}`, i === 0 ? extra : {}));
export const ports = (n: number): Iface[] => Array.from({ length: n }, (_, i) => iface(`p${i + 1}`));

export function link(a: string, b: string, extra: Partial<Link> = {}): Link {
  return { a, b, km: 0.01, mbps: 1000, ...extra };
}

export function makeState(devices: Device[], links: Link[], meta: Record<string, unknown> = {}): NetState {
  return { devices: Object.fromEntries(devices.map((d) => [d.id, d])), links, ...meta };
}

export const clone = <T>(s: T): T => JSON.parse(JSON.stringify(s));

/** «pc1:eth0» → {dev, port} */
export function ref(s: string): { dev: string; port: string } {
  const [dev, port] = s.split(":");
  return { dev, port };
}

export function linkOf(state: NetState, dev: string, port: string): Link | null {
  const key = `${dev}:${port}`;
  return state.links.find((l) => l.a === key || l.b === key) ?? null;
}

/** по другую сторону кабеля от (dev, port) */
export function peerOf(state: NetState, dev: string, port: string) {
  const l = linkOf(state, dev, port);
  if (!l) return null;
  const key = `${dev}:${port}`;
  return { ...ref(l.a === key ? l.b : l.a), link: l };
}

export const getIface = (d: Device, name: string): Iface | null =>
  d.ifaces.find((i) => i.name === name) ?? null;

/** интерфейс, который обязан существовать (иначе — ошибка в сценарии или команде) */
export function ifaceOf(d: Device, name: string): Iface {
  const i = getIface(d, name);
  if (!i) throw new Error(`${d.id}: нет интерфейса ${name}`);
  return i;
}

export function freePort(state: NetState, devId: string): Iface | null {
  const d = state.devices[devId];
  return d.ifaces.find((i) => !linkOf(state, devId, i.name)) ?? null;
}

/** добавить кабель между первыми свободными портами; вернёт {ok, error} */
export function connect(
  state: NetState,
  a: string,
  b: string,
  extra: Partial<Link> = {},
): { ok: boolean; error?: string } {
  if (a === b) return { ok: false, error: "Нельзя соединить устройство с самим собой" };
  const pa = freePort(state, a);
  const pb = freePort(state, b);
  if (!pa) return { ok: false, error: `У «${state.devices[a].name}» нет свободных портов` };
  if (!pb) return { ok: false, error: `У «${state.devices[b].name}» нет свободных портов` };
  state.links.push(link(`${a}:${pa.name}`, `${b}:${pb.name}`, extra));
  return { ok: true };
}

export function disconnect(state: NetState, idx: number): void {
  state.links.splice(idx, 1);
}

/** состояние без служебных кэшей — для сохранения в кабинете */
export function strip(state: NetState): NetState {
  const s = clone(state);
  delete s.rt;
  return s;
}
