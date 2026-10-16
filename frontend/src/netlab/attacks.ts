/* Атаки на фоне: подмена ARP (MITM), SYN-флуд, сканирование портов. Атакующий — обычное устройство
   с полем attack; перед каждой пробой атаки «проверяются на достижимость» настоящими пакетами, поэтому
   файрвол и коммутация влияют на результат так же, как в жизни. */
import { ipStr, parseIp, inNet, networkOf } from "./ip.ts";
import { lookup, rtOf, tcp1 } from "./sim.ts";
import type { Device, Iface, NetState } from "./types.ts";

const firstIp = (d: Device): Iface | undefined => d.ifaces.find((i) => i.ip !== null);

/** подготовить побочные эффекты атак перед пробой */
export function attacksBefore(state: NetState): void {
  if (state.__busy) return;
  state.__busy = true;
  try {
    const rt = rtOf(state);
    const synflood: Record<string, boolean> = {};
    rt.fx = { synflood };
    for (const dev of Object.values(state.devices)) {
      const a = dev.attack;
      if (!a) continue;
      if (a.type === "arpspoof" && a.victim && a.gatewayIp) {
        const victim = state.devices[a.victim];
        const gwIp = parseIp(a.gatewayIp);
        if (!victim || gwIp === null || victim.arpStatic?.[a.gatewayIp]) continue;
        const own = firstIp(dev);
        const vif = firstIp(victim);
        if (!own || !vif || !inNet(parseIp(vif.ip), networkOf(parseIp(own.ip), own.prefix), own.prefix)) continue;
        (rt.arp[victim.id] ??= {})[gwIp] = { mac: own.mac, at: 0, sim: -1 };
      } else if (a.type === "synflood" && a.target && a.port !== undefined) {
        const tgt = state.devices[a.target];
        const tip = parseIp(firstIp(tgt)?.ip);
        if (tip === null || !lookup(dev, tip)) continue;
        const r = tcp1(state, dev.id, tip, a.port, { sport: 60000 });
        if (r.status === "connected" || r.status === "refused") synflood[`${a.target}:${a.port}`] = true;
      }
    }
  } finally {
    delete state.__busy;
  }
}

/** фоновый трафик для перехвата: сканер обходит порты цели */
export function backgroundTraffic(state: NetState): void {
  if (state.__busy) return;
  state.__busy = true;
  try {
    for (const dev of Object.values(state.devices)) {
      const a = dev.attack;
      if (a?.type !== "scan" || !a.target) continue;
      const tgt = state.devices[a.target];
      const tip = parseIp(firstIp(tgt)?.ip);
      if (tip === null || !lookup(dev, tip)) continue;
      for (const p of a.ports ?? []) tcp1(state, dev.id, tip, p, { sport: 61000 + p });
    }
  } finally {
    delete state.__busy;
  }
}

export { ipStr };
