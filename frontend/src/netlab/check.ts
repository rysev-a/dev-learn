/* Проверка упражнения: цели сценария прогоняются на чистой копии сети (без кэшей ARP и MAC),
   чтобы результат не зависел от того, что ученик успел «нащупать» пингами. */
import { clone, connect } from "./model.ts";
import { ipStr, parseIp } from "./ip.ts";
import { fmtMs, ping1, tcp1, udp1 } from "./sim.ts";
import { transfer } from "./transfer.ts";
import { exec, toIp } from "./term.ts";
import { httpFetch } from "./http.ts";
import type { FetchResult } from "./http.ts";
import { pageload } from "./pageload.ts";
import { sshConnect } from "./ssh.ts";
import type { Goal, GoalResult, GoalRun, NetState, Op, ProbeGoal, ProbeRun } from "./types.ts";

const emptyRun = (): GoalRun => ({ hops: [], events: [], delivered: [] });

/** «10.0.0.5» | «@srv» | «@r1.eth1» → число */
export function resolveTarget(state: NetState, spec: string): number | null {
  if (spec.startsWith("@")) {
    const [id, ifn] = spec.slice(1).split(".");
    const d = state.devices[id];
    const i = ifn ? d.ifaces.find((x) => x.name === ifn) : d.ifaces.find((x) => x.ip);
    return i && i.ip ? parseIp(i.ip) : null;
  }
  return parseIp(spec);
}

type Resolved = { ip: number; run?: ProbeRun | undefined; err?: undefined } | { err: string; ip?: undefined; run?: ProbeRun | undefined };

/** цель пробы: IP, «@устройство» или имя (через hosts и DNS-резолвер устройства-источника) */
export function resolveFrom(state: NetState, spec: string, fromId: string): Resolved {
  if (spec.startsWith("@")) {
    const ip = resolveTarget(state, spec);
    return ip === null ? { err: "у цели нет адреса" } : { ip };
  }
  const direct = parseIp(spec);
  if (direct !== null) return { ip: direct };
  return toIp(state, state.devices[fromId], spec);
}

/** итог пробы цели: статус и то, что нужно панели результата */
type ProbeOutcome = GoalRun & Partial<Omit<ProbeRun, keyof GoalRun>> & { status: string };

export function runProbe(state: NetState, g: Goal): ProbeOutcome {
  const p = (g.ping ?? g.tcp ?? g.udp) as ProbeGoal;
  const res = resolveFrom(state, p.to, p.from);
  if (res.err !== undefined) return { status: "noaddr", err: res.err, events: res.run?.events ?? [], hops: res.run?.hops ?? [], delivered: [] };
  const dst = res.ip;
  const popts: { size?: number; df?: boolean } = {};
  if (g.ping && p.sizeFromMtu) {
    const i = state.devices[p.from].ifaces.find((x) => x.ip) ?? state.devices[p.from].ifaces[0];
    popts.size = (i.mtu ?? 1500) - 28;
    popts.df = true;
  } else if (g.ping && p.size !== undefined) {
    popts.size = p.size;
    popts.df = !!p.df;
  }
  const port = p.port ?? 0;
  const once = (): ProbeRun =>
    g.ping ? ping1(state, p.from, dst, popts) : g.udp ? udp1(state, p.from, dst, port) : tcp1(state, p.from, dst, port);
  if (p.warm) once(); // «прогрев»: ARP и таблицы коммутаторов уже выучены
  return once();
}

const STATUS_TEXT: Record<string, string> = {
  reply: "ответ получен",
  connected: "соединение установлено",
  refused: "порт закрыт (RST)",
  timeout: "ответа нет",
  ttl: "TTL истёк по дороге",
  unreach: "получено «недоступно»",
  noaddr: "имя или адрес цели не определились",
  toolong: "пакет больше MTU интерфейса",
  frag: "нужна фрагментация, а DF запрещает",
  unreach_port: "порт недоступен (ICMP)",
};

const PROTO_NAMES: Record<string, string> = { h1: "HTTP/1.1", h2: "HTTP/2", h3: "HTTP/3" };

/** пакет действительно прошёл через устройство: оно его отправляло или он был адресован его интерфейсу */
const touches = (run: GoalRun, state: NetState, id: string): boolean =>
  run.hops.some((h) => {
    if (h.frame.type !== "ip") return false;
    if (h.from === id) return true;
    if (h.to !== id) return false;
    const d = state.devices[id];
    return d.kind === "switch" || d.kind === "hub" ? true : d.ifaces.some((i) => i.name === h.toPort && i.mac === h.frame.dst);
  });

/** чистая копия сети без кэшей ARP и MAC */
const fresh = (state: NetState): NetState => {
  const s = clone(state);
  delete s.rt;
  return s;
};

const fail = (g: Goal, detail: string, run: GoalRun = emptyRun()): GoalResult => ({ id: g.id, text: g.text, ok: false, detail, run });

export function checkGoals(state: NetState, goals: Goal[]): GoalResult[] {
  return goals.map((g): GoalResult => {
    if (g.dns) {
      const s = fresh(state);
      const x = g.dns;
      const r = toIp(s, s.devices[x.from], x.name);
      const got = r.err !== undefined ? (r.err.includes("NXDOMAIN") ? "NXDOMAIN" : "ошибка") : ipStr(r.ip);
      const ok = got === x.expect;
      return {
        id: g.id,
        text: g.text,
        ok,
        detail: ok ? `${x.name} → ${got}` : r.err !== undefined ? `${x.name}: ${r.err}` : `${x.name} → ${got}, а ожидалось ${x.expect}`,
        run: r.run ?? emptyRun(),
      };
    }
    if (g.mtu) {
      const x = g.mtu;
      const dev = state.devices[x.dev];
      const i = dev.ifaces.find((k) => k.name === (x.iface ?? "eth0"));
      const m = i?.mtu ?? 1500;
      const ok = (x.min === undefined || m >= x.min) && (x.max === undefined || m <= x.max);
      return { id: g.id, text: g.text, ok, detail: ok ? `MTU ${i?.name} = ${m}` : `MTU ${i?.name ?? "?"} = ${m}, нужно ${x.min !== undefined ? "не меньше " + x.min : ""}${x.max !== undefined ? " не больше " + x.max : ""}`, run: emptyRun() };
    }
    if (g.lbspread) {
      const s = fresh(state);
      const x = g.lbspread;
      const res = resolveFrom(s, x.to, x.from);
      if (res.err !== undefined) return fail(g, res.err);
      const hits: Record<string, number> = {};
      let okN = 0;
      let last: ProbeRun | null = null;
      for (let i = 0; i < x.n; i++) {
        last = tcp1(s, x.from, res.ip, x.port, { sport: 50000 + i });
        if (last.status === "connected") {
          okN++;
          const dev = [...last.delivered].reverse().find((e) => e.dev !== x.from)?.dev;
          if (dev !== undefined) hits[dev] = (hits[dev] ?? 0) + 1;
        }
      }
      const bad: string[] = [];
      if (okN < x.n) bad.push(`успешных соединений ${okN} из ${x.n}`);
      const used = Object.keys(hits);
      if (x.distinct && used.length < x.distinct) bad.push(`задействовано серверов ${used.length}, а нужно ${x.distinct}`);
      for (const a of x.avoid ?? []) if (hits[a]) bad.push(`запросы попали на неисправный «${s.devices[a].name}»`);
      if (x.sticky && used.length > 1) bad.push("один клиент попадает на разные серверы");
      const spread = used.map((k) => `${s.devices[k].name}: ${hits[k]}`).join(", ");
      return { id: g.id, text: g.text, ok: bad.length === 0, detail: bad.length ? bad.join("; ") : spread, run: last ?? emptyRun() };
    }
    if (g.ssh) {
      const s = fresh(state);
      const x = g.ssh;
      const dst = resolveFrom(s, x.to, x.from);
      if (dst.err !== undefined) return fail(g, dst.err);
      let jump: { ip: number } | null = null;
      if (x.via) {
        const j = resolveFrom(s, x.via, x.from);
        if (j.err !== undefined) return fail(g, j.err);
        jump = { ip: j.ip };
      }
      const r = sshConnect(s, s.devices[x.from], x.user, dst.ip, { jump, pass: x.pass ?? null, noKey: x.auth === "password" });
      const wantFail = x.expect === "fail";
      const ok = wantFail ? !r.ok : r.ok && (!x.auth || r.auth === x.auth);
      const detail = r.ok ? `вход выполнен (${r.auth === "key" ? "по ключу" : "по паролю"})${wantFail ? " — а должен быть закрыт" : ""}` : `${(r.error ?? "").split("\n").pop()}${wantFail ? " — так и задумано" : ""}`;
      return { id: g.id, text: g.text, ok, detail, run: r.run ?? emptyRun() };
    }
    if (g.page) {
      const s = fresh(state);
      const x = g.page;
      const res = resolveFrom(s, x.to, x.from);
      if (res.err !== undefined) return fail(g, res.err);
      const r = pageload(s, s.devices[x.from], { dstIp: res.ip, https: x.https ?? true });
      if (!r.ok) return fail(g, r.error);
      const sec = r.chosen.total / 1e6;
      const ok = sec <= x.maxS;
      return {
        id: g.id,
        text: g.text,
        ok,
        detail: `${sec.toFixed(2)} с по ${PROTO_NAMES[r.used]}${r.note ? " (откат с HTTP/3)" : ""}${ok ? "" : `, нужно не больше ${x.maxS} с`}`,
        run: emptyRun(),
      };
    }
    if (g.http) {
      const s = fresh(state);
      const x = g.http;
      let r: FetchResult = { responses: [], error: null, run: null };
      for (let i = 0; i < (x.repeat ?? 1); i++) r = httpFetch(s, s.devices[x.from], { url: x.url, method: x.method ?? "GET", follow: !!x.follow, headers: x.headers ?? {}, toIp, proxy: x.proxy ?? null });
      const run: GoalRun = r.run ?? emptyRun();
      if (x.fail) return { id: g.id, text: g.text, ok: !!r.error, detail: r.error ? `${r.error} — так и задумано` : "запрос прошёл, а должен быть запрещён", run };
      if (r.error) return fail(g, r.error, run);
      const resp = x.nth !== undefined ? r.responses[x.nth] : r.responses[r.responses.length - 1];
      const bad: string[] = [];
      if (!resp) bad.push("ответа нет");
      else {
        const rtt = (resp.rttUs ?? 0) / 1000;
        if (x.status !== undefined && resp.status !== x.status) bad.push(`код ${resp.status} ${resp.reason}, а нужен ${x.status}`);
        for (const [k, v] of Object.entries(x.header ?? {})) {
          const got = resp.headers[k.toLowerCase()];
          if (got === undefined) bad.push(`нет заголовка ${k}`);
          else if (v !== true && !String(got).toLowerCase().includes(String(v).toLowerCase())) bad.push(`${k}: «${got}», нужно содержащее «${v}»`);
        }
        for (const k of x.noHeader ?? []) if (resp.headers[k.toLowerCase()] !== undefined) bad.push(`заголовок ${k} не нужен`);
        if (x.bodyIncludes && !resp.body.includes(x.bodyIncludes)) bad.push(`в теле нет «${x.bodyIncludes}»`);
        if (x.maxRttMs !== undefined && rtt > x.maxRttMs) bad.push(`ответ за ${rtt.toFixed(0)} мс, нужно быстрее ${x.maxRttMs}`);
        if (x.hops !== undefined && r.responses.length !== x.hops) bad.push(`запросов ${r.responses.length}, а нужно ${x.hops}`);
        if (x.finalUrl && !(resp.url ?? "").endsWith(x.finalUrl)) bad.push(`итоговый адрес ${resp.url}`);
      }
      return { id: g.id, text: g.text, ok: bad.length === 0, detail: bad.length ? bad.join("; ") : resp ? `${resp.status} ${resp.reason}${r.responses.length > 1 ? `, запросов: ${r.responses.length}` : ""}` : "", run };
    }
    if (g.xfer) {
      const s = fresh(state);
      const x = g.xfer;
      const dst = resolveTarget(s, x.to);
      if (dst === null) return fail(g, "у цели нет адреса");
      const r = transfer(s, x.from, dst, { bytes: (x.mb ?? 50) * 1e6 });
      if (!r.ok) return fail(g, r.text);
      const mbps = r.mbps;
      const loaded = r.loadedRttMs;
      const bad: string[] = [];
      if (x.minMbps !== undefined && mbps < x.minMbps) bad.push(`скорость ${mbps.toFixed(1)} Мбит/с — нужно не меньше ${x.minMbps}`);
      if (x.maxLoadedRttMs !== undefined && loaded > x.maxLoadedRttMs) bad.push(`RTT под нагрузкой ${loaded.toFixed(0)} мс — нужно не больше ${x.maxLoadedRttMs}`);
      return {
        id: g.id,
        text: g.text,
        ok: bad.length === 0,
        detail: bad.length ? bad.join("; ") : `${mbps.toFixed(1)} Мбит/с, RTT под нагрузкой до ${loaded.toFixed(0)} мс`,
        run: { hops: [], events: [], delivered: [], chart: r.chart },
      };
    }
    const s = fresh(state);
    const run = runProbe(s, g);
    const p = (g.ping ?? g.tcp ?? g.udp) as ProbeGoal;
    const wantOk = (p.expect ?? "ok") === "ok";
    const gotOk = run.status === "reply" || run.status === "connected";
    let ok = wantOk === gotOk;
    let detail = (run.status === "unreach" && run.code === "port" ? STATUS_TEXT["unreach_port"] : run.status === "unreach" && run.code === "frag" ? `${STATUS_TEXT["frag"]} (MTU ${run.mtu})` : run.status === "toolong" ? `${STATUS_TEXT["toolong"]} (MTU ${run.mtu})` : STATUS_TEXT[run.status]) ?? run.status;
    const clash = run.events.find((e) => e.kind === "conflict");
    if (clash && wantOk) return fail(g, clash.text, run);
    if (p.noLoop && run.events.some((e) => e.kind === "loop")) return fail(g, "в сети петля: кадры ходят по кругу", run);
    if (p.notSeenBy && run.hops.some((h) => h.to === p.notSeenBy && h.frame.type === "ip")) {
      return fail(g, `чужой кадр дошёл до «${s.devices[p.notSeenBy].name}» — его можно подслушать`, run);
    }
    const rttUs = run.rttUs ?? null;
    if (ok && wantOk) {
      if (p.maxRttMs !== undefined && rttUs !== null && rttUs / 1000 > p.maxRttMs) {
        ok = false;
        detail = `ответ пришёл за ${fmtMs(rttUs)}, а нужно быстрее ${p.maxRttMs} мс`;
      } else if (p.via && !touches(run, s, p.via)) {
        ok = false;
        detail = `пакет дошёл, но не через «${s.devices[p.via].name}»`;
      } else if (p.avoid && touches(run, s, p.avoid)) {
        ok = false;
        detail = `пакет дошёл, но прошёл через «${s.devices[p.avoid].name}»`;
      } else if (p.seenSrc) {
        const want = resolveTarget(s, p.seenSrc);
        const hit = run.delivered.find((x) => x.dev === p.to.replace(/^@/, "").split(".")[0]);
        if (!hit || hit.src !== want) {
          ok = false;
          detail = hit
            ? `получатель видит отправителя ${ipStr(hit.src)}, а должен видеть ${ipStr(want)}`
            : "получатель не видит запрос";
        } else detail = `получатель видит отправителя ${ipStr(hit.src)}`;
      } else if (rttUs !== null) detail += ` за ${fmtMs(rttUs)}`;
    } else if (!ok && wantOk) {
      detail = `${detail} — должно получиться`;
    } else if (!ok && !wantOk) {
      detail = `${detail} — а должно быть запрещено`;
    } else if (ok && !wantOk) detail = `${detail} — так и задумано`;
    return { id: g.id, text: g.text, ok, detail, run };
  });
}

/** применить шаги эталонного решения: {cable:[a,b]} | {cmd:[dev, "строка"]} */
export function applyOps(state: NetState, ops: Op[]): NetState {
  for (const op of ops) {
    if ("unlink" in op) {
      const [a, b] = op.unlink;
      const i = state.links.findIndex((l) => {
        const x = l.a.split(":")[0];
        const y = l.b.split(":")[0];
        return (x === a && y === b) || (x === b && y === a);
      });
      if (i < 0) throw new Error(`нет кабеля ${a}–${b}`);
      state.links.splice(i, 1);
    } else if ("drop" in op) {
      state.links = state.links.filter((l) => l.a.split(":")[0] !== op.drop && l.b.split(":")[0] !== op.drop);
    } else if ("cable" in op) {
      const r = connect(state, op.cable[0], op.cable[1], op.extra);
      if (!r.ok) throw new Error(r.error);
    } else {
      const r = exec(state, op.cmd[0], op.cmd[1]);
      if (r.changed === false && /Error|Permission|RTNETLINK|не /.test(r.out))
        throw new Error(`${op.cmd[0]}: ${op.cmd[1]} → ${r.out}`);
    }
  }
  return state;
}
