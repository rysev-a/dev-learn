/* Симулятор сети: кадры, ARP, коммутаторы, маршрутизация, TTL, ICMP, TCP-рукопожатие, NAT и
   фильтр FORWARD. Всё синхронное и детерминированное: одна «проба» (ping, TCP-подключение)
   даёт список хопов для анимации, журнал событий и итог. Время — в микросекундах. */
import {
  BCAST_MAC,
  inNet,
  inNetStr,
  ipStr,
  isPrivate,
  maskOf,
  networkOf,
  parseCidr,
  parseIp,
  parseNet,
} from "./ip.js";
import { attacksBefore } from "./attacks.js";
import { recordCapture } from "./capture.js";
import { dnsIn } from "./dns.js";
import { getIface, peerOf } from "./model.js";

const PROC = { host: 20, server: 20, router: 50, internet: 50, switch: 5, hub: 1 };
const SIZE = { arp: 60, icmp: 98, tcp: 74, udp: 74 };

export const rtOf = (state) => (state.rt ??= { arp: {}, mac: {}, ct: {}, dnsCache: {} });

/* ---- маршруты ------------------------------------------------------------------- */

export function routeTable(d, { noTun = false } = {}) {
  const out = [];
  for (const i of d.ifaces) {
    if (i.ip === null || !i.up) continue;
    if (noTun && i.tun) continue;
    const ip = parseIp(i.ip);
    out.push({
      net: networkOf(ip, i.prefix),
      prefix: i.prefix,
      via: null,
      dev: i.name,
      connected: true,
    });
  }
  for (const r of d.routes) {
    const n = parseNet(r.dst);
    if (!n) continue;
    const via = r.via ? parseIp(r.via) : null;
    let dev = r.dev ?? null;
    if (via !== null && !dev)
      dev = out.find((c) => c.connected && inNet(via, c.net, c.prefix))?.dev ?? null;
    if (!dev) continue;
    const ifc = getIface(d, dev);
    if (!ifc || !ifc.up || ifc.ip === null || (noTun && ifc.tun)) continue;
    out.push({ net: n.net, prefix: n.prefix, via, dev, connected: false });
  }
  return out;
}

export function lookup(d, dst, opts) {
  let best = null;
  for (const r of routeTable(d, opts)) {
    if (!inNet(dst, r.net, r.prefix)) continue;
    if (!best || r.prefix > best.prefix || (r.prefix === best.prefix && r.connected && !best.connected))
      best = r;
  }
  return best;
}

export const ownIps = (d) =>
  d.ifaces.filter((i) => i.ip !== null).map((i) => parseIp(i.ip));

/* ---- кортежи соединений (conntrack) ----------------------------------------------- */

function tupleOf(p) {
  return {
    proto: p.proto,
    src: p.src,
    dst: p.dst,
    sport: p.proto === "icmp" ? p.icmp.id : p.sport,
    dport: p.proto === "icmp" ? p.icmp.id : p.dport,
  };
}
const same = (a, b) =>
  a.proto === b.proto &&
  a.src === b.src &&
  a.dst === b.dst &&
  a.sport === b.sport &&
  a.dport === b.dport;
const reverse = (t) => ({
  proto: t.proto,
  src: t.dst,
  dst: t.src,
  sport: t.dport,
  dport: t.sport,
});
function applyTuple(p, t) {
  p.src = t.src;
  p.dst = t.dst;
  if (p.proto === "icmp") return;
  p.sport = t.sport;
  p.dport = t.dport;
}

/* ---- описание кадров для подписей и журнала ------------------------------------- */

function describe(f) {
  if (f.type === "arp") {
    const a = f.arp;
    return a.op === "req"
      ? `ARP: у кого ${ipStr(a.tip)}?`
      : `ARP: ${ipStr(a.sip)} — это ${a.smac}`;
  }
  const p = f.ip;
  const addr = `${ipStr(p.src)}→${ipStr(p.dst)}`;
  if (p.proto === "icmp") {
    const t = p.icmp.type;
    const nm =
      t === "echo-req"
        ? "ICMP echo"
        : t === "echo-rep"
          ? "ICMP ответ"
          : t === "ttl"
            ? "ICMP TTL истёк"
            : "ICMP недоступно";
    return `${nm} ${addr}`;
  }
  if (p.tunnel) return `VPN-туннель ${ipStr(p.src)}→${ipStr(p.dst)} (внутри: ${ipStr(p.tunnel.inner.src)}→${ipStr(p.tunnel.inner.dst)} ${p.tunnel.inner.proto})`;
  if (p.proto === "udp" && p.dns) {
    const q = p.dns.q;
    return p.dns.response
      ? `DNS ответ ${p.dns.rcode}${p.dns.referral ? " (реферал " + p.dns.referral.zone + ")" : ""} ${ipStr(p.src)}→${ipStr(p.dst)}`
      : `DNS ${q.name} ${q.type}? ${ipStr(p.src)}→${ipStr(p.dst)}`;
  }
  if (p.proto === "udp") return `UDP ${ipStr(p.src)}:${p.sport}→${ipStr(p.dst)}:${p.dport}`;
  const sq = p.seq !== undefined ? ` seq=${p.seq}${p.flags.includes("ACK") ? ` ack=${p.ack}` : ""}${p.len ? ` len=${p.len}` : ""}` : "";
  return `TCP ${p.flags}${sq} ${ipStr(p.src)}:${p.sport}→${ipStr(p.dst)}:${p.dport}`;
}
const kindOf = (f) => (f.type === "arp" ? "arp" : f.ip.proto);

/* ---- симулятор -------------------------------------------------------------------- */

const bindOk = (svc, dst) => !svc.bind || svc.bind === "0.0.0.0" || parseIp(svc.bind) === dst || (svc.bind === "127.0.0.1" && (dst >>> 24) === 127);
let seq = 1;
let uidSeq = 0;

export class Sim {
  constructor(state) {
    this.s = state;
    this.id = seq++;
    this.rt = rtOf(state);
    this.events = [];
    this.hops = [];
    this.delivered = [];
    this.probe = null;
    this.resolving = new Set();
    this.seen = new Set();
    this.dnsPend = new Map();
    this.dnsSeq = 0;
  }

  dev(id) {
    return this.s.devices[id];
  }

  log(t, dev, kind, text) {
    this.events.push({ t, dev, kind, text });
  }

  /* --- уровень 2 --- */

  xmit(devId, port, frame, at) {
    const d = this.dev(devId);
    const ifc = getIface(d, port);
    const peer = peerOf(this.s, devId, port);
    if (!peer) {
      this.log(at, devId, "drop", `порт ${port}: кабель не подключён`);
      return;
    }
    if (!ifc.up) {
      this.log(at, devId, "drop", `порт ${port} выключен`);
      return;
    }
    if (frame.type === "ip" && frame.ip.size) {
      const mtu = Math.min(ifc.mtu ?? 1500, peer.link.mtu ?? 1500);
      if (frame.ip.size > mtu) {
        const origin = this.probe?.origin === devId && !frame.ip.fwd;
        if (origin) {
          this.log(at, devId, "drop", `пакет ${frame.ip.size} Б больше MTU ${mtu} интерфейса ${port}: message too long`);
          if (this.probe && !this.probe.result) this.probe.result = { status: "toolong", from: null, at, mtu };
          return;
        }
        if (frame.ip.df) {
          this.log(at, devId, "drop", `пакет ${frame.ip.size} Б не лезет в MTU ${mtu}, а запрещена фрагментация (DF)${d.icmpBlock ? " — ICMP «frag needed» тоже заблокирован: отправитель ничего не узнает" : " — шлю ICMP «frag needed»"}`);
          if (!d.icmpBlock) this.icmpError(d, ifc, { ...frame.ip, src: frame.ip.src }, "unreach", at, "frag", mtu);
          return;
        }
        this.log(at, devId, "info", `пакет ${frame.ip.size} Б больше MTU ${mtu}: фрагментирую`);
      }
    }
    const mbps = peer.link.mbps || 1000;
    const dt = Math.round(((frame.size * 8) / mbps) * 1) + Math.round(peer.link.km * 5);
    const t1 = at + Math.max(1, dt);
    this.hops.push({
      from: devId,
      fromPort: port,
      to: peer.dev,
      toPort: peer.port,
      t0: at,
      t1,
      kind: kindOf(frame),
      label: describe(frame),
      frame,
    });
    this.recv(peer.dev, peer.port, frame, t1);
  }

  recv(devId, port, frame, at) {
    const d = this.dev(devId);
    if (d.kind === "switch") return this.switchIn(d, port, frame, at);
    if (d.kind === "hub") return this.hubIn(d, port, frame, at);
    const ifc = getIface(d, port);
    if (!ifc.up) return this.log(at, devId, "drop", `порт ${port} выключен`);
    if (frame.dst !== ifc.mac && frame.dst !== BCAST_MAC) return; // чужой кадр
    const t = at + (PROC[d.kind] ?? 20);
    if (frame.type === "arp") return this.arpIn(d, ifc, frame, t);
    this.ipIn(d, ifc, { ...frame.ip, icmp: frame.ip.icmp && { ...frame.ip.icmp } }, t);
  }

  /** кадр уже проходил через это устройство — значит, в сети петля */
  loopSeen(d, frame, at) {
    frame.uid ??= ++uidSeq;
    const key = `${d.id}|${frame.uid}`;
    if (this.seen.has(key)) {
      this.log(at, d.id, "loop", "этот кадр уже проходил здесь — в сети петля, кадры будут ходить по кругу");
      return true;
    }
    this.seen.add(key);
    return false;
  }

  hubIn(d, port, frame, at) {
    if (this.loopSeen(d, frame, at)) return;
    const t = at + PROC.hub;
    this.log(t, d.id, "learn", "хаб повторяет кадр на все остальные порты");
    for (const i of d.ifaces) if (i.name !== port) this.xmit(d.id, i.name, frame, t);
  }

  switchIn(d, port, frame, at) {
    if (this.loopSeen(d, frame, at)) return;
    const pin = getIface(d, port);
    if (!pin.up) return this.log(at, d.id, "drop", `порт ${port} выключен`);
    const vlan = pin.trunk ? (frame.vlan ?? 1) : (pin.vlan ?? 1);
    const key = (m) => (vlan === 1 ? m : `${m}@vlan${vlan}`);
    const mt = (this.rt.mac[d.id] ??= {});
    if (frame.src !== BCAST_MAC && mt[key(frame.src)] !== port) {
      mt[key(frame.src)] = port;
      this.log(at, d.id, "learn", `запомнил: ${frame.src} за портом ${port}${vlan === 1 ? "" : ` (VLAN ${vlan})`}`);
    }
    const t = at + PROC.switch;
    const out = (name) => {
      const e = getIface(d, name);
      if (e.trunk) return this.xmit(d.id, name, { ...frame, vlan }, t);
      if ((e.vlan ?? 1) !== vlan) return;
      this.xmit(d.id, name, { ...frame, vlan: undefined }, t);
    };
    const known = frame.dst !== BCAST_MAC ? mt[key(frame.dst)] : null;
    if (known) {
      if (known === port) return;
      return out(known);
    }
    this.log(
      t,
      d.id,
      "learn",
      frame.dst === BCAST_MAC
        ? "широковещательный кадр — рассылаю во все порты этого VLAN"
        : `адрес ${frame.dst} неизвестен — рассылаю во все порты этого VLAN`,
    );
    for (const i of d.ifaces) if (i.name !== port) out(i.name);
  }

  /* --- ARP --- */

  arpIn(d, ifc, frame, at) {
    const a = frame.arp;
    if (ifc.ip === null || a.tip !== parseIp(ifc.ip)) return;
    const cache = (this.rt.arp[d.id] ??= {});
    const prev = cache[a.sip];
    if (prev && prev.sim === this.id && prev.mac !== a.smac)
      this.log(at, d.id, "conflict", `конфликт адресов: ${ipStr(a.sip)} отвечают сразу два устройства (${prev.mac} и ${a.smac})`);
    cache[a.sip] = { mac: a.smac, at, sim: this.id };
    if (a.op === "req") {
      this.log(at, d.id, "arp", `${ifc.ip} — это я, отвечаю ${ifc.mac}`);
      const rep = {
        type: "arp",
        size: SIZE.arp,
        src: ifc.mac,
        dst: a.smac,
        arp: { op: "rep", sip: a.tip, smac: ifc.mac, tip: a.sip, tmac: a.smac },
      };
      this.xmit(d.id, ifc.name, rep, at);
    }
  }

  resolve(d, ifc, nextHop, at) {
    const st = d.arpStatic?.[ipStr(nextHop)];
    if (st) return { mac: st, at };
    const cache = (this.rt.arp[d.id] ??= {});
    const known = (e) => ({ mac: e.mac, at: e.sim === this.id ? Math.max(at, e.at) : at });
    if (cache[nextHop]) return known(cache[nextHop]);
    const key = `${d.id}:${nextHop}`;
    if (this.resolving.has(key)) return null;
    this.resolving.add(key);
    this.log(at, d.id, "arp", `нужен MAC для ${ipStr(nextHop)} — спрашиваю ARP-запросом`);
    const req = {
      type: "arp",
      size: SIZE.arp,
      src: ifc.mac,
      dst: BCAST_MAC,
      arp: { op: "req", sip: parseIp(ifc.ip), smac: ifc.mac, tip: nextHop, tmac: null },
    };
    this.xmit(d.id, ifc.name, req, at);
    this.resolving.delete(key);
    const got = cache[nextHop];
    return got ? known(got) : null;
  }

  /* --- уровень 3: отправка --- */

  ipOut(d, pkt, at) {
    const local = ownIps(d);
    if (local.includes(pkt.dst)) {
      if (pkt.src === null) pkt.src = pkt.dst;
      return this.ipIn(d, null, pkt, at); // сам себе
    }
    const r = lookup(d, pkt.dst, pkt.noTun ? { noTun: true } : undefined);
    if (!r) {
      this.log(at, d.id, "drop", `нет маршрута до ${ipStr(pkt.dst)} (Network is unreachable)`);
      return false;
    }
    const ifc = getIface(d, r.dev);
    if (pkt.src === null) pkt.src = parseIp(ifc.ip);
    if (ifc.tun) return this.tunSend(d, ifc, pkt, at);
    const hop = r.via ?? pkt.dst;
    const m = this.resolve(d, ifc, hop, at);
    if (!m) {
      this.log(at + 1000, d.id, "drop", `${ipStr(hop)} не ответил на ARP (Host unreachable)`);
      return false;
    }
    this.xmit(
      d.id,
      ifc.name,
      { type: "ip", size: SIZE[pkt.proto], src: ifc.mac, dst: m.mac, ip: pkt },
      m.at,
    );
    return true;
  }

  /* --- туннель (VPN): внутренний пакет упаковывается в UDP до пира --- */
  tunSend(d, ifc, pkt, at) {
    const peer = parseIp(ifc.tun.peer);
    this.log(at, d.id, "tun", `туннель ${ifc.name}: ${ipStr(pkt.src)}→${ipStr(pkt.dst)} упакован в UDP до ${ifc.tun.peer}`);
    const outer = {
      src: null,
      dst: peer,
      ttl: 64,
      proto: "udp",
      sport: ifc.tun.port,
      dport: ((this.rt.tunPeer ??= {})[`${d.id}:${ifc.name}`]?.port) ?? ifc.tun.port,
      size: (pkt.size ?? 84) + 60,
      noTun: true,
      tunnel: { inner: { ...pkt, icmp: pkt.icmp && { ...pkt.icmp } }, key: ifc.tun.key, name: ifc.name },
    };
    return this.ipOut(d, outer, at + 15);
  }

  tunIn(d, pkt, at) {
    const tif = d.ifaces.find((i) => i.tun && i.tun.port === pkt.dport && parseIp(i.tun.peer) === pkt.src);
    if (!tif) {
      this.log(at, d.id, "drop", `UDP/${pkt.dport} от ${ipStr(pkt.src)}: туннеля с таким пиром нет — пакет отброшен`);
      return true;
    }
    if (tif.tun.key !== pkt.tunnel.key) {
      this.log(at, d.id, "drop", `туннель ${tif.name}: ключ не совпал — пакет от ${ipStr(pkt.src)} отброшен (тишина, как у WireGuard)`);
      return true;
    }
    (this.rt.tunPeer ??= {})[`${d.id}:${tif.name}`] = { ip: pkt.src, port: pkt.sport };
    const inner = { ...pkt.tunnel.inner, icmp: pkt.tunnel.inner.icmp && { ...pkt.tunnel.inner.icmp } };
    this.log(at, d.id, "tun", `туннель ${tif.name}: распаковал ${ipStr(inner.src)}→${ipStr(inner.dst)}`);
    this.ipIn(d, tif, inner, at + 15);
    return true;
  }

  icmpError(d, ifc, pkt, type, at, code = null, mtu = null) {
    if (d.icmpBlock) return;
    if (pkt.proto === "icmp" && pkt.icmp.type !== "echo-req" && pkt.icmp.type !== "echo-rep") return;
    const orig = { ...tupleOf(pkt) };
    const err = {
      src: ifc && ifc.ip ? parseIp(ifc.ip) : null,
      dst: pkt.src,
      ttl: 64,
      proto: "icmp",
      icmp: { type, id: 0, orig, code, mtu },
    };
    this.ipOut(d, err, at);
  }

  /* --- уровень 3: приём и пересылка --- */

  ipIn(d, ifc, pkt, at) {
    const ct = (this.rt.ct[d.id] ??= []);
    const tup = tupleOf(pkt);
    let est = false;
    // ответ на уже проходивший поток: обратная трансляция
    const rep = ct.find((e) => same(reverse(e.tr), tup));
    const fwd = rep ? null : ct.find((e) => same(e.orig, tup));
    if (rep) {
      est = true;
      rep.replied = true;
      if (!same(rep.tr, rep.orig))
        this.log(at, d.id, "nat", `NAT: ответ ${ipStr(pkt.src)}→${ipStr(pkt.dst)} возвращаю клиенту ${ipStr(rep.orig.src)}`);
      applyTuple(pkt, reverse(rep.orig));
    } else if (fwd) {
      est = !!fwd.replied;
      applyTuple(pkt, fwd.tr);
    } else if (pkt.proto === "icmp" && pkt.icmp.orig) {
      // ошибка ICMP про уже трансформированный пакет
      const e = ct.find((x) => same(x.tr, pkt.icmp.orig));
      if (e) {
        pkt.dst = e.orig.src;
        pkt.icmp = { ...pkt.icmp, orig: e.orig };
      }
    } else if (ifc) {
      const rule = d.nat.find(
        (n) =>
          n.chain === "PREROUTING" &&
          n.action === "DNAT" &&
          (!n.in || n.in === ifc.name) &&
          (!n.dst || inNetStr(pkt.dst, n.dst)) &&
          (!n.proto || n.proto === pkt.proto) &&
          (!n.dport || n.dport === pkt.dport),
      );
      if (rule) {
        const [h, p] = rule.to.split(":");
        const nd = parseIp(h);
        if (nd !== null) {
          this.log(
            at,
            d.id,
            "nat",
            `DNAT: ${ipStr(pkt.dst)}:${pkt.dport} → ${h}${p ? ":" + p : ""}`,
          );
          pkt.dst = nd;
          if (p) pkt.dport = Number(p);
        }
      }
    }

    if (!rep && !fwd && d.lb && pkt.proto === "tcp" && pkt.dport === d.lb.port && parseIp(d.lb.vip) === pkt.dst) {
      return this.lbIn(d, pkt, at, tup);
    }
    if (ownIps(d).includes(pkt.dst)) return this.localIn(d, pkt, at);
    if (!d.forward) {
      return this.log(
        at,
        d.id,
        "drop",
        `пакет для ${ipStr(pkt.dst)} — не мне, а пересылка выключена (ip_forward=0)`,
      );
    }
    this.forward(d, ifc, pkt, at, est, tup);
  }

  /* --- балансировщик (L4): виртуальный адрес → один из бэкендов; источник подменяется на адрес балансировщика --- */
  backendDev(ip) {
    const n = parseIp(ip);
    return Object.values(this.s.devices).find((x) => x.ifaces.some((i) => i.ip !== null && parseIp(i.ip) === n));
  }

  backendUp(b) {
    const dev = this.backendDev(b.ip);
    if (!dev) return false;
    const n = parseIp(b.ip);
    const ifc = dev.ifaces.find((i) => i.ip !== null && parseIp(i.ip) === n);
    return ifc.up && dev.services.some((s) => s.proto === "tcp" && s.port === b.port && bindOk(s, n));
  }

  lbIn(d, pkt, at, tup) {
    const lb = d.lb;
    const live = lb.health ? lb.backends.filter((b) => this.backendUp(b)) : lb.backends;
    if (!live.length) return this.log(at, d.id, "drop", "балансировщик: нет живых серверов в пуле — 503");
    const st = ((this.rt.lb ??= {})[d.id] ??= { n: 0 });
    const b = lb.algo === "hash" ? live[pkt.src % live.length] : live[st.n++ % live.length];
    const r = lookup(d, parseIp(b.ip));
    if (!r) return this.log(at, d.id, "drop", `балансировщик: нет маршрута до ${b.ip}`);
    const out = getIface(d, r.dev);
    this.log(at, d.id, "nat", `балансировщик (${lb.algo === "hash" ? "хеш по адресу клиента" : "по кругу"}): ${ipStr(pkt.src)} → сервер ${b.ip}:${b.port}`);
    const ct = (this.rt.ct[d.id] ??= []);
    pkt.dst = parseIp(b.ip);
    pkt.dport = b.port;
    pkt.src = parseIp(out.ip);
    const used = new Set(ct.map((e) => e.tr.sport));
    let sp = 41000;
    while (used.has(sp)) sp++;
    pkt.sport = sp;
    pkt.ttl = Math.max(1, pkt.ttl - 1);
    ct.push({ orig: tup, tr: tupleOf(pkt), replied: false });
    pkt.fwd = true;
    this.ipOut(d, pkt, at + 5);
  }

  forward(d, ifc, pkt, at, est, origTuple) {
    if (d.dropPrivate && (isPrivate(pkt.src) || isPrivate(pkt.dst))) {
      return this.log(
        at,
        d.id,
        "drop",
        `интернет не маршрутизирует частные адреса: ${ipStr(isPrivate(pkt.src) ? pkt.src : pkt.dst)}`,
      );
    }
    if (pkt.ttl <= 1) {
      this.log(at, d.id, "drop", `TTL истёк — отправителю уходит ICMP «time exceeded»`);
      return this.icmpError(d, ifc, pkt, "ttl", at);
    }
    pkt.ttl -= 1;
    const r = lookup(d, pkt.dst);
    if (!r) {
      this.log(at, d.id, "drop", `нет маршрута до ${ipStr(pkt.dst)} — шлю ICMP «unreachable»`);
      return this.icmpError(d, ifc, pkt, "unreach", at);
    }
    const out = getIface(d, r.dev);
    const verdict = this.filter(d, pkt, ifc?.name, out.name, est ? "established" : "new");
    if (verdict !== "ACCEPT") {
      this.log(at, d.id, "fw", `файрвол: ${verdict} ${ipStr(pkt.src)}→${ipStr(pkt.dst)}`);
      if (verdict === "REJECT") this.icmpError(d, ifc, pkt, "unreach", at);
      return;
    }
    if (!est) {
      const ct = this.rt.ct[d.id];
      const origT = origTuple;
      const exists = ct.find((e) => same(e.orig, origT));
      if (!exists) {
        const rule = d.nat.find(
          (n) =>
            n.chain === "POSTROUTING" &&
            n.action === "MASQUERADE" &&
            (!n.out || n.out === out.name) &&
            (!n.src || inNetStr(pkt.src, n.src)) &&
            (!n.dst || inNetStr(pkt.dst, n.dst)),
        );
        if (rule && out.ip !== null) {
          const before = ipStr(pkt.src);
          pkt.src = parseIp(out.ip);
          if (pkt.proto !== "icmp") {
            const used = new Set(ct.map((e) => e.tr.sport));
            let sp = 40000;
            while (used.has(sp)) sp++;
            pkt.sport = sp;
          }
          this.log(
            at,
            d.id,
            "nat",
            `MASQUERADE: ${before} → ${out.ip}${pkt.proto === "icmp" ? "" : ":" + pkt.sport}`,
          );
        }
        ct.push({ orig: origT, tr: tupleOf(pkt), replied: false });
        if (ct.length > 200) ct.shift();
      }
    }
    pkt.fwd = true;
    this.ipOut(d, pkt, at + 5);
  }

  filter(d, pkt, inName, outName, state) {
    for (const r of d.fw.rules) {
      if (r.src && !inNetStr(pkt.src, r.src)) continue;
      if (r.dst && !inNetStr(pkt.dst, r.dst)) continue;
      if (r.proto && r.proto !== pkt.proto) continue;
      if (r.dport && r.dport !== pkt.dport) continue;
      if (r.sport && r.sport !== pkt.sport) continue;
      if (r.in && r.in !== inName) continue;
      if (r.out && r.out !== outName) continue;
      if (r.state && r.state !== state) continue;
      return r.action;
    }
    return d.fw.policy;
  }

  /* --- уровень 4: локальная доставка --- */

  localIn(d, pkt, at) {
    this.delivered.push({
      dev: d.id,
      src: pkt.src,
      dst: pkt.dst,
      proto: pkt.proto,
      dport: pkt.dport ?? null,
      sport: pkt.sport ?? null,
    });
    const reply = (extra) =>
      this.ipOut(d, { src: pkt.dst, dst: pkt.src, ttl: 64, ...extra }, at + 5);
    if (pkt.proto === "icmp") {
      const t = pkt.icmp.type;
      if (t === "echo-req") {
        this.log(at, d.id, "icmp", `echo-запрос от ${ipStr(pkt.src)}, отвечаю`);
        return reply({ proto: "icmp", icmp: { type: "echo-rep", id: pkt.icmp.id } });
      }
      return this.probeReply(d, pkt, at);
    }
    if (pkt.proto === "udp") {
      if (pkt.tunnel && this.tunIn(d, pkt, at)) return;
      if (pkt.dns && dnsIn(this, d, pkt, at, reply)) return;
      const svc = d.services.find((x) => x.proto === "udp" && x.port === pkt.dport && bindOk(x, pkt.dst));
      if (svc) {
        this.log(at, d.id, "udp", `порт ${pkt.dport}/udp слушает — отвечаю датаграммой`);
        return reply({ proto: "udp", sport: pkt.dport, dport: pkt.sport });
      }
      if (this.probe && d.id === this.probe.origin) return this.probeReply(d, pkt, at);
      this.log(at, d.id, "udp", `порт ${pkt.dport}/udp никто не слушает — шлю ICMP «порт недоступен»`);
      return this.icmpError(d, null, pkt, "unreach", at, "port");
    }
    if (pkt.proto === "tcp") {
      const sess = this.probe?.session;
      const mk = (flags, seq, ack, len = 0) => ({ proto: "tcp", sport: pkt.dport, dport: pkt.sport, flags, seq, ack, len });
      if (pkt.flags === "SYN" && this.rt.fx?.synflood?.[`${d.id}:${pkt.dport}`] && !d.syncookies) {
        return this.log(at, d.id, "drop", "очередь полуоткрытых соединений переполнена (SYN-флуд) — новый SYN отброшен");
      }
      if (pkt.flags === "SYN") {
        const svc = d.services.find((s) => s.proto === "tcp" && s.port === pkt.dport && bindOk(s, pkt.dst));
        if (svc) {
          this.log(at, d.id, "tcp", `порт ${pkt.dport} слушает — отвечаю SYN-ACK`);
          return reply(mk("SYN-ACK", 5000, (pkt.seq ?? 0) + 1));
        }
        this.log(at, d.id, "tcp", `порт ${pkt.dport} никто не слушает — отвечаю RST`);
        return reply(mk("RST", 0, (pkt.seq ?? 0) + 1));
      }
      if (sess && d.id !== this.probe.origin) {
        // сервер: данные, закрытие
        if (pkt.flags === "PSH-ACK") {
          this.log(at, d.id, "tcp", `получен запрос (${pkt.len} Б) — отправляю ответ 1000 Б и закрываю соединение`);
          const ack = pkt.seq + pkt.len;
          reply(mk("PSH-ACK", pkt.ack, ack, 1000));
          return reply(mk("FIN-ACK", pkt.ack + 1000, ack));
        }
        if (pkt.flags === "FIN-ACK") {
          this.log(at, d.id, "tcp", "клиент тоже закрыл — подтверждаю последним ACK, соединение закрыто");
          return reply(mk("ACK", pkt.ack, pkt.seq + 1));
        }
        return;
      }
      return this.probeReply(d, pkt, at);
    }
  }

  probeReply(d, pkt, at) {
    const p = this.probe;
    if (!p || d.id !== p.origin) return;
    if (p.result && !(p.session && pkt.proto === "tcp")) return;
    const who = ipStr(pkt.src);
    const reply = (pkt.proto === "icmp" && pkt.icmp.type === "echo-rep") || pkt.proto === "tcp" || pkt.proto === "udp";
    if (reply && p.dst !== undefined && pkt.src !== p.dst) {
      this.log(at, d.id, "drop", `ответ пришёл с адреса ${who}, а запрос уходил на ${ipStr(p.dst)} — отбрасываю (так делает любой узел без NAT-обратного преобразования)`);
      return;
    }
    if (pkt.proto === "icmp") {
      const t = pkt.icmp.type;
      if (t === "echo-rep" && pkt.icmp.id === p.id) {
        p.result = { status: "reply", from: pkt.src, ttl: pkt.ttl, at };
        this.log(at, d.id, "icmp", `получен ответ от ${who}`);
      } else if (t === "ttl" || t === "unreach") {
        const o = pkt.icmp.orig;
        if (o && o.sport === (p.sport ?? p.id)) {
          p.result = { status: t, from: pkt.src, at, code: pkt.icmp.code, mtu: pkt.icmp.mtu };
          this.log(
            at,
            d.id,
            "icmp",
            t === "ttl"
              ? `${who}: TTL истёк по дороге`
              : pkt.icmp.code === "frag"
                ? `${who}: нужна фрагментация, а DF запрещает (MTU ${pkt.icmp.mtu})`
                : pkt.icmp.code === "port"
                ? `${who}: порт недоступен (ICMP port unreachable)`
                : `${who}: сеть или узел недоступны`,
          );
        }
      }
    } else if (pkt.proto === "udp" && pkt.dport === p.sport) {
      p.result = { status: "reply", from: pkt.src, at, dns: pkt.dns };
      this.log(at, d.id, "udp", `получена датаграмма-ответ от ${who}`);
    } else if (pkt.proto === "tcp" && pkt.dport === p.sport) {
      const rst = pkt.flags === "RST";
      const mk = (flags, seq, ack, len = 0) => ({ proto: "tcp", sport: p.sport, dport: pkt.sport, flags, seq, ack, len });
      const send = (extra, t) => this.ipOut(d, { src: pkt.dst, dst: pkt.src, ttl: 64, ...extra }, t);
      if (pkt.flags === "SYN-ACK" || rst) {
        p.result = { status: rst ? "refused" : "connected", from: pkt.src, at };
        this.log(at, d.id, "tcp", rst ? `получен RST — порт закрыт` : `получен SYN-ACK — соединение установлено`);
        if (p.session && !rst) {
          send(mk("ACK", pkt.ack, pkt.seq + 1), at + 5);
          send(mk("PSH-ACK", pkt.ack, pkt.seq + 1, 100), at + 10);
        }
      } else if (p.session) {
        if (pkt.flags === "PSH-ACK") {
          this.log(at, d.id, "tcp", `получен ответ (${pkt.len} Б), подтверждаю`);
          send(mk("ACK", pkt.ack, pkt.seq + pkt.len), at + 5);
        } else if (pkt.flags === "FIN-ACK") {
          this.log(at, d.id, "tcp", "сервер закрыл соединение (FIN) — закрываю свою сторону");
          send(mk("FIN-ACK", pkt.ack, pkt.seq + 1), at + 5);
        } else if (pkt.flags === "ACK") this.log(at, d.id, "tcp", "последний ACK получен — соединение закрыто");
      }
    }
  }
}

/* ---- пробы ---------------------------------------------------------------------- */

function finish(sim, p, t0) {
  recordCapture(sim);
  sim.events.sort((a, b) => a.t - b.t);
  sim.hops.sort((a, b) => a.t0 - b.t0);
  const r = p.result;
  return {
    status: r ? r.status : "timeout",
    from: r ? r.from : null,
    code: r ? (r.code ?? null) : null,
    mtu: r ? (r.mtu ?? null) : null,
    dns: r ? (r.dns ?? null) : null,
    rttUs: r ? r.at - t0 : null,
    events: sim.events,
    hops: sim.hops,
    delivered: sim.delivered,
  };
}

/** одна ICMP-проба: ttl можно задать (для traceroute) */
export function ping1(state, devId, dstIp, { ttl = 64, id = 1, size = null, df = false } = {}) {
  attacksBefore(state);
  const sim = new Sim(state);
  const d = state.devices[devId];
  const p = { origin: devId, id, result: null, dst: dstIp };
  sim.probe = p;
  const t0 = 0;
  sim.log(t0, devId, "icmp", `ping ${ipStr(dstIp)}`);
  sim.ipOut(
    d,
    { src: null, dst: dstIp, ttl, proto: "icmp", icmp: { type: "echo-req", id }, ...(size !== null ? { size: size + 28, df } : {}) },
    t0 + (PROC[d.kind] ?? 20),
  );
  return finish(sim, p, t0);
}

/** TCP-подключение к порту: SYN → SYN-ACK / RST / тишина */
export function tcp1(state, devId, dstIp, port, { sport = 50000, session = false } = {}) {
  attacksBefore(state);
  const sim = new Sim(state);
  const d = state.devices[devId];
  const p = { origin: devId, id: 0, sport, result: null, session, dst: dstIp };
  sim.probe = p;
  const t0 = 0;
  sim.log(t0, devId, "tcp", `подключаюсь к ${ipStr(dstIp)}:${port}`);
  sim.ipOut(
    d,
    { src: null, dst: dstIp, ttl: 64, proto: "tcp", sport, dport: port, flags: "SYN", seq: 1000, ack: 0, len: 0 },
    t0 + (PROC[d.kind] ?? 20),
  );
  return finish(sim, p, t0);
}

/** одна UDP-датаграмма на порт: ответ, ICMP «порт недоступен» или тишина */
export function udp1(state, devId, dstIp, port, { sport = 50001 } = {}) {
  const sim = new Sim(state);
  const d = state.devices[devId];
  const p = { origin: devId, id: 0, sport, result: null, dst: dstIp };
  sim.probe = p;
  const t0 = 0;
  sim.log(t0, devId, "udp", `отправляю датаграмму на ${ipStr(dstIp)}:${port}/udp`);
  sim.ipOut(
    d,
    { src: null, dst: dstIp, ttl: 64, proto: "udp", sport, dport: port },
    t0 + (PROC[d.kind] ?? 20),
  );
  return finish(sim, p, t0);
}

/** DNS-запрос с устройства: вопрос q к серверу server (число) */
export function dns1(state, devId, server, q, { rd = true } = {}) {
  const sim = new Sim(state);
  const d = state.devices[devId];
  const sport = 50002;
  const p = { origin: devId, id: 0, sport, result: null, dst: server };
  sim.probe = p;
  const t0 = 0;
  sim.log(t0, devId, "dns", `спрашиваю ${ipStr(server)}: «${q.name} ${q.type}»`);
  sim.ipOut(
    d,
    { src: null, dst: server, ttl: 64, proto: "udp", sport, dport: 53, dns: { id: 1, q, response: false, rd } },
    t0 + (PROC[d.kind] ?? 20),
  );
  return finish(sim, p, t0);
}

export function traceroute(state, devId, dstIp, maxHops = 12) {
  const hops = [];
  let misses = 0;
  for (let ttl = 1; ttl <= maxHops; ttl++) {
    const r = ping1(state, devId, dstIp, { ttl, id: 100 + ttl });
    hops.push({ ttl, ...r });
    if (r.status === "reply" || r.status === "unreach") break;
    if (r.status === "timeout" && ++misses >= 3) break;
  }
  return hops;
}

export const fmtMs = (us) => (us === null ? "—" : `${(us / 1000).toFixed(us < 10000 ? 3 : 1)} мс`);
export { maskOf, parseCidr };
