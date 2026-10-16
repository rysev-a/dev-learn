/* Перехват пакетов (tcpdump): каждый кадр, прошедший через интерфейс при пробах, попадает в кольцо
   устройства; команда tcpdump показывает кольцо с фильтром. Время в кольце — монотонное «московское». */
import { ipStr } from "./ip.ts";
import type { Frame, NetState } from "./types.ts";
import type { Sim } from "./sim.ts";

const LIMIT = 300;
const FLAG: Record<string, string> = { SYN: "S", "SYN-ACK": "S.", ACK: ".", "PSH-ACK": "P.", "FIN-ACK": "F.", RST: "R." };

export function recordCapture(sim: Sim): void {
  const rt = sim.rt;
  const cap = (rt.cap ??= {});
  const base = rt.clock ?? 0;
  let last = 0;
  const put = (dev: string, iface: string, row: { t: number; dir: string; frame: Frame }) => {
    const k = `${dev}:${iface}`;
    (cap[k] ??= []).push(row);
    if (cap[k].length > LIMIT) cap[k].shift();
  };
  for (const h of sim.hops) {
    put(h.from, h.fromPort, { t: base + h.t0, dir: "Out", frame: h.frame });
    put(h.to, h.toPort, { t: base + h.t1, dir: "In", frame: h.frame });
    last = Math.max(last, h.t1);
  }
  rt.clock = base + last + 500_000;
}

const clock = (us: number) => {
  const sec = Math.floor(us / 1e6);
  const f = String(Math.round(us % 1e6)).padStart(6, "0");
  const hh = 12 + Math.floor(sec / 3600);
  return `${String(hh).padStart(2, "0")}:${String(Math.floor(sec / 60) % 60).padStart(2, "0")}:${String(sec % 60).padStart(2, "0")}.${f}`;
};

export function lineOf(row: { frame: Frame }): string {
  const f = row.frame;
  if (f.type === "arp") {
    const a = f.arp;
    return a.op === "req"
      ? `ARP, Request who-has ${ipStr(a.tip)} tell ${ipStr(a.sip)}, length 28`
      : `ARP, Reply ${ipStr(a.sip)} is-at ${a.smac}, length 28`;
  }
  const p = f.ip;
  const len = (p.size ?? 84) - 20;
  if (p.proto === "icmp") {
    const ic = p.icmp ?? { type: "", id: 0 };
    const t = ic.type;
    const what =
      t === "echo-req" ? `echo request, id ${ic.id}, length ${len}` : t === "echo-rep" ? `echo reply, id ${ic.id}, length ${len}` : t === "ttl" ? "time exceeded in-transit, length 56" : ic.code === "port" ? "destination unreachable (port), length 56" : ic.code === "frag" ? `destination unreachable (need to frag, mtu ${ic.mtu}), length 56` : "destination unreachable (net), length 56";
    return `IP ${ipStr(p.src)} > ${ipStr(p.dst)}: ICMP ${what}${p.ttl !== undefined ? ` [ttl ${p.ttl}]` : ""}`;
  }
  if (p.proto === "udp") {
    if (p.dns) return `IP ${ipStr(p.src)}.${p.sport} > ${ipStr(p.dst)}.${p.dport}: UDP, DNS ${p.dns.response ? "ответ " + p.dns.rcode : p.dns.q.name + " " + p.dns.q.type + "?"}`;
    return `IP ${ipStr(p.src)}.${p.sport} > ${ipStr(p.dst)}.${p.dport}: UDP, length ${p.len ?? 56}`;
  }
  const fl = p.flags ?? "";
  return `IP ${ipStr(p.src)}.${p.sport} > ${ipStr(p.dst)}.${p.dport}: Flags [${FLAG[fl] ?? fl}], seq ${p.seq ?? 0}${fl.includes("ACK") ? `, ack ${p.ack}` : ""}, length ${p.len ?? 0}`;
}

function matches(row: { frame: Frame }, filters: string[]): boolean {
  const f = row.frame;
  const proto = f.type === "arp" ? "arp" : f.ip.proto;
  for (let i = 0; i < filters.length; i++) {
    const w = filters[i];
    if (["icmp", "tcp", "udp", "arp"].includes(w)) {
      if (proto !== w) return false;
    } else if (w === "host") {
      const h = filters[++i];
      if (f.type === "arp") {
        if (!(ipStr(f.arp.sip) === h || ipStr(f.arp.tip) === h)) return false;
      } else if (ipStr(f.ip.src) !== h && ipStr(f.ip.dst) !== h) return false;
    } else if (w === "port") {
      const n = Number(filters[++i]);
      if (f.type === "arp" || (f.ip.sport !== n && f.ip.dport !== n)) return false;
    }
  }
  return true;
}

/** строки перехвата для устройства: iface или «any» */
export function captureLines(state: NetState, dev: string, iface: string, filters: string[], count: number): string[] {
  const cap = state.rt?.cap ?? {};
  const keys = iface === "any" ? state.devices[dev].ifaces.map((i) => `${dev}:${i.name}`) : [`${dev}:${iface}`];
  const rows = keys.flatMap((k) => (cap[k] ?? []).map((r) => ({ ...r, k })));
  rows.sort((a, b) => a.t - b.t);
  const out = rows.filter((r) => matches(r, filters)).slice(-count);
  return out.map((r) => `${clock(r.t)} ${iface === "any" ? r.k.split(":")[1] + " " : ""}${r.dir.padEnd(3)} ${lineOf(r)}`);
}
