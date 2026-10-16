/* DNS в симуляторе: авторитативные серверы (записи, делегирования), рекурсивный резолвер (итеративный
   обход от корня, CNAME, кэш) и клиентские настройки (resolv.conf, hosts). Запросы и ответы — настоящие
   UDP-датаграммы на порт 53, поэтому видны в журнале и в анимации. */
import { ipStr, parseIp } from "./ip.js";

export const fqdn = (s) => String(s).trim().toLowerCase().replace(/\.$/, "");
const inZone = (name, zone) => zone === "" || name === zone || name.endsWith("." + zone);

export function newDns(extra = {}) {
  return { records: [], delegations: [], zones: [], recursive: false, roots: [], ...extra };
}

/** ответ авторитативного сервера на вопрос q → {rcode, answers, referral} */
export function authAnswer(dns, q) {
  const name = fqdn(q.name);
  const here = dns.records.filter((r) => fqdn(r.name) === name);
  const exact = here.filter((r) => r.type === q.type);
  if (exact.length) return { rcode: "NOERROR", answers: exact.map(rr), referral: null };
  const cn = here.find((r) => r.type === "CNAME");
  if (cn && q.type !== "CNAME") return { rcode: "NOERROR", answers: [rr(cn)], referral: null };
  // делегирование: самая длинная подходящая зона (но своя зона важнее более короткой чужой)
  const del = dns.delegations
    .filter((d) => inZone(name, fqdn(d.zone)))
    .sort((a, b) => fqdn(b.zone).length - fqdn(a.zone).length)[0];
  const own = dns.zones.filter((z) => inZone(name, fqdn(z))).sort((a, b) => fqdn(b).length - fqdn(a).length)[0];
  if (del && (!own || fqdn(del.zone).length > fqdn(own).length))
    return { rcode: "NOERROR", answers: [], referral: { zone: fqdn(del.zone), ns: del.ns } };
  if (own) return { rcode: here.length ? "NOERROR" : "NXDOMAIN", answers: [], referral: null };
  return { rcode: "REFUSED", answers: [], referral: null };
}

const rr = (r) => ({ name: fqdn(r.name), type: r.type, value: r.value, ttl: r.ttl ?? 300 });

/** обработка DNS-пакета на устройстве d; true — пакет обработан */
export function dnsIn(sim, d, pkt, at, reply) {
  const m = pkt.dns;
  const pend = sim.dnsPend;
  if (m.response) {
    const st = pend.get(`${d.id}:${m.id}`);
    if (!st) return false; // ответ клиенту-источнику пробы
    pend.delete(`${d.id}:${m.id}`);
    return resolverStep(sim, d, st, m, at), true;
  }
  if (!d.dns) return false;
  const q = m.q;
  const name = fqdn(q.name);
  sim.log(at, d.id, "dns", `${d.dns.recursive && m.rd ? "резолвер" : "сервер"}: вопрос «${name} ${q.type}»`);
  if (d.dns.recursive && m.rd) {
    const cache = ((sim.rt.dnsCache ??= {})[d.id] ??= {});
    const hit = cache[`${name}|${q.type}`];
    if (hit) {
      sim.log(at, d.id, "dns", `ответ из кэша: ${hit.map((a) => a.value).join(", ")}`);
      reply({ proto: "udp", sport: 53, dport: pkt.sport, dns: { id: m.id, q, response: true, rcode: "NOERROR", answers: hit, ra: true } });
      return true;
    }
    const own = authAnswer(d.dns, q);
    if (own.answers.length) {
      sim.log(at, d.id, "dns", `отвечаю из своей зоны: ${own.answers.map((a) => a.value).join(", ")}`);
      reply({ proto: "udp", sport: 53, dport: pkt.sport, dns: { id: m.id, q, response: true, rcode: "NOERROR", answers: own.answers, ra: true } });
      return true;
    }
    const st = {
      client: { id: m.id, dport: pkt.sport, srcIp: pkt.dst, dstIp: pkt.src },
      q,
      cur: { name, type: q.type },
      chain: [],
      hops: 0,
    };
    if (!d.dns.roots.length) {
      finish(sim, d, st, "SERVFAIL", at, "корневые серверы не заданы");
      return true;
    }
    send(sim, d, st, d.dns.roots[0], at);
    return true;
  }
  const a = authAnswer(d.dns, q);
  sim.log(
    at,
    d.id,
    "dns",
    a.referral
      ? `не знаю, но зона ${a.referral.zone} у ${a.referral.ns} — отправляю реферал`
      : a.answers.length
        ? `отвечаю: ${a.answers.map((x) => `${x.type} ${x.value}`).join(", ")}`
        : `ответ: ${a.rcode}`,
  );
  reply({
    proto: "udp",
    sport: 53,
    dport: pkt.sport,
    dns: { id: m.id, q, response: true, rcode: a.rcode, answers: a.answers, referral: a.referral },
  });
  return true;
}

function send(sim, d, st, server, at) {
  if (++st.hops > 12) return finish(sim, d, st, "SERVFAIL", at, "слишком много шагов");
  const id = ++sim.dnsSeq;
  sim.dnsPend.set(`${d.id}:${id}`, st);
  const ip = parseIp(server);
  sim.log(at, d.id, "dns", `спрашиваю ${server}: «${st.cur.name} ${st.cur.type}»`);
  sim.ipOut(
    d,
    { src: null, dst: ip, ttl: 64, proto: "udp", sport: 33000 + (id % 1000), dport: 53, dns: { id, q: st.cur, response: false, rd: false } },
    at + 5,
  );
  if (sim.dnsPend.get(`${d.id}:${id}`) === st) {
    // ответа не будет: резолвер ждёт таймаут и отвечает SERVFAIL
    sim.dnsPend.delete(`${d.id}:${id}`);
    sim.log(at + 1_000_000, d.id, "dns", `${server} не отвечает — SERVFAIL клиенту`);
    finish(sim, d, st, "SERVFAIL", at + 1_000_000);
  }
}

function resolverStep(sim, d, st, m, at) {
  if (m.answers.length) {
    st.chain.push(...m.answers);
    const want = st.cur.type;
    const final = m.answers.find((a) => a.type === want);
    if (final || st.cur.type === "CNAME") return finish(sim, d, st, "NOERROR", at);
    const cname = m.answers.find((a) => a.type === "CNAME");
    if (cname) {
      sim.log(at, d.id, "dns", `${cname.name} — псевдоним для ${cname.value}, ищу дальше`);
      st.cur = { name: fqdn(cname.value), type: want };
      return send(sim, d, st, d.dns.roots[0], at);
    }
    return finish(sim, d, st, "NOERROR", at);
  }
  if (m.referral) {
    sim.log(at, d.id, "dns", `реферал: зона ${m.referral.zone} → ${m.referral.ns}`);
    return send(sim, d, st, m.referral.ns, at);
  }
  return finish(sim, d, st, m.rcode, at);
}

function finish(sim, d, st, rcode, at, why) {
  if (why) sim.log(at, d.id, "dns", why);
  const answers = st.chain;
  if (rcode === "NOERROR" && answers.length) {
    const c = ((sim.rt.dnsCache ??= {})[d.id] ??= {});
    c[`${fqdn(st.q.name)}|${st.q.type}`] = answers;
  }
  sim.ipOut(
    d,
    {
      src: st.client.srcIp,
      dst: st.client.dstIp,
      ttl: 64,
      proto: "udp",
      sport: 53,
      dport: st.client.dport,
      dns: { id: st.client.id, q: st.q, response: true, rcode, answers, ra: true },
    },
    at + 5,
  );
}

/** резолв на клиенте: hosts → нужно спрашивать сервер (вернёт {ip}|{ask: ip}|{error}) */
export function localLookup(d, name) {
  const n = fqdn(name);
  if (parseIp(n) !== null) return { ip: parseIp(n) };
  const h = d.hosts?.[n];
  if (h) return { ip: parseIp(h), from: "hosts" };
  if (!d.resolver) return { error: "в /etc/resolv.conf нет DNS-сервера" };
  return { ask: parseIp(d.resolver) };
}

export const answerIp = (dns) => {
  const a = (dns?.answers ?? []).find((x) => x.type === "A");
  return a ? parseIp(a.value) : null;
};

export const fmtDns = (dns) =>
  [
    `;; status: ${dns.rcode}`,
    ...(dns.answers ?? []).map((a) => `${a.name}.\t${a.ttl}\tIN\t${a.type}\t${a.value}`),
  ].join("\n");

export { ipStr };
