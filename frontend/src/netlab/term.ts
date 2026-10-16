/* Мини-терминал Linux для устройств сети: ip, ping, traceroute, curl, iptables, sysctl и т. д.
   Команды меняют состояние — так же, как формы в карточке устройства (они зовут те же функции),
   поэтому эталонное решение упражнения — просто список команд. */
import {
  cidrStr,
  ipStr,
  netStr,
  parseCidr,
  parseIp,
  parseNet,
  inNet,
  networkOf,
} from "./ip.ts";
import { getIface, ifaceOf } from "./model.ts";
import { transfer } from "./transfer.ts";
import type { TransferChart, TransferResult } from "./transfer.ts";
import { fmtCurl, httpFetch, newHttp } from "./http.ts";
import type { FetchResult } from "./http.ts";
import { fmtPage, pageload } from "./pageload.ts";
import { DEFAULT_PKI, DEFAULT_TRUST, NOW, addDays, newTls, sClient } from "./tls.ts";
import { answerIp, fmtDns, fqdn, localLookup, newDns } from "./dns.ts";
import { captureLines } from "./capture.ts";
import { makeKey, newSsh, sshConnect } from "./ssh.ts";
import { backgroundTraffic } from "./attacks.ts";
import { fmtMs, lookup, ping1, routeTable, tcp1, traceroute, rtOf, udp1, dns1 } from "./sim.ts";
import type { RouteEntry } from "./sim.ts";
import type { Device, FwRule, NatRule, NetState, ProbeRun, ToIp } from "./types.ts";

/** результат команды терминала: вывод, изменилось ли состояние сети, проба для анимации */
export interface CmdResult {
  out: string;
  changed?: boolean;
  probe?: ProbeRun | null | undefined;
  http?: FetchResult;
  clear?: boolean;
  chart?: TransferChart | null;
  xfer?: TransferResult;
}

const NO = (d: Device) =>
  d.locked ? `Permission denied: «${d.name}» принадлежит провайдеру — настраивать его нельзя` : null;

/* ---- изменение настроек (общие для форм и терминала) ------------------------------- */

export function setAddr(d: Device, ifName: string, cidr: string): string | null {
  const i = getIface(d, ifName);
  if (!i) return `Cannot find device "${ifName}"`;
  const c = parseCidr(cidr);
  if (!c) return `Error: inet prefix is expected rather than "${cidr}".`;
  if (i.ip !== null) return "RTNETLINK answers: File exists (сначала ip addr flush dev " + ifName + ")";
  i.ip = ipStr(c.ip);
  i.prefix = c.prefix;
  return null;
}

export function clearAddr(d: Device, ifName: string): string | null {
  const i = getIface(d, ifName);
  if (!i) return `Cannot find device "${ifName}"`;
  i.ip = null;
  // маршруты через пропавший интерфейс исчезают вместе с адресом
  d.routes = d.routes.filter((r) => {
    if (!r.via) return true;
    const v = parseIp(r.via);
    return d.ifaces.some(
      (x) => x.ip !== null && inNet(v, networkOf(parseIp(x.ip), x.prefix), x.prefix),
    );
  });
  return null;
}

export function setUp(d: Device, ifName: string, up: boolean): string | null {
  const i = getIface(d, ifName);
  if (!i) return `Cannot find device "${ifName}"`;
  i.up = up;
  return null;
}

export function addRoute(d: Device, dst: string | null, via: string | null, dev: string | null): string | null {
  const isDefault = dst === "default" || dst === "0.0.0.0/0";
  const n = isDefault ? { net: 0, prefix: 0 } : parseNet(dst);
  if (!n || (!isDefault && parseCidr(dst) === null && parseIp(dst) === null))
    return `Error: inet prefix is expected rather than "${dst}".`;
  const key = netStr(n.net, n.prefix);
  if (via) {
    const v = parseIp(via);
    if (v === null) return `Error: inet address is expected rather than "${via}".`;
    const ok = d.ifaces.some(
      (x) => x.ip !== null && x.up && inNet(v, networkOf(parseIp(x.ip), x.prefix), x.prefix),
    );
    if (!ok) return "Error: Nexthop has invalid gateway. (шлюз должен лежать в одной из подключённых подсетей)";
  } else if (!dev || !getIface(d, dev)) {
    return "Error: нужно указать via <шлюз> или dev <интерфейс>";
  }
  const dup = d.routes.find((r) => r.dst === key);
  if (dup || (n.prefix !== 0 && routeTable(d).some((r) => r.connected && r.net === n.net && r.prefix === n.prefix)))
    return "RTNETLINK answers: File exists";
  d.routes.push({ dst: key, via: via ?? null, dev: dev ?? null });
  return null;
}

export function delRoute(d: Device, dst: string | null): string | null {
  const isDefault = dst === "default" || dst === "0.0.0.0/0";
  const n = isDefault ? { net: 0, prefix: 0 } : parseNet(dst);
  if (!n) return `Error: inet prefix is expected rather than "${dst}".`;
  const key = netStr(n.net, n.prefix);
  const i = d.routes.findIndex((r) => r.dst === key);
  if (i < 0) return "RTNETLINK answers: No such process";
  d.routes.splice(i, 1);
  return null;
}

/** шлюз по умолчанию: пустая строка — убрать */
export function setGateway(d: Device, gw: string | null): string | null {
  const old = d.routes.filter((r) => r.dst === "0.0.0.0/0");
  d.routes = d.routes.filter((r) => r.dst !== "0.0.0.0/0");
  if (!gw) return null;
  const e = addRoute(d, "default", gw, null);
  if (e) d.routes.push(...old);
  return e;
}

export const getGateway = (d: Device) => d.routes.find((r) => r.dst === "0.0.0.0/0")?.via ?? "";

/* ---- вывод ------------------------------------------------------------------------ */

const routeLine = (r: RouteEntry, d: Device): string => {
  const dst = r.prefix === 0 ? "default" : netStr(r.net, r.prefix);
  if (r.connected) {
    const i = ifaceOf(d, r.dev);
    return `${dst} dev ${r.dev} proto kernel scope link src ${i.ip}`;
  }
  return r.via ? `${dst} via ${ipStr(r.via)} dev ${r.dev}` : `${dst} dev ${r.dev} scope link`;
};

function showAddr(d: Device) {
  return d.ifaces
    .map((i, n) => {
      const st = i.up ? "UP" : "DOWN";
      return (
        `${n + 1}: ${i.name}: <${st}> mtu ${i.mtu ?? 1500}\n    link/ether ${i.mac}` +
        (i.ip ? `\n    inet ${i.ip}/${i.prefix}` : "")
      );
    })
    .join("\n");
}

const HELP = `Доступные команды:
  ip addr [add|del|flush ...]    ip link [set <if> up|down]
  ip route [add|del|get ...]     ip neigh   (или arp -n)
  ping [-c N] [-t TTL] <ip>      traceroute <ip>
  curl <ip>[:порт]               nc -zv <ip> <порт>    nc -l <порт>
  ss -ltn                        sysctl net.ipv4.ip_forward|tcp_rmem|tcp_congestion_control
  iperf3 <ip> [-n МБ]            ip link set <if> txqueuelen N
  iptables [-t nat] -L|-A|-I|-D|-F|-P ...   hostname   clear`;

/* ---- iptables --------------------------------------------------------------------- */

const STATE_MAP: Record<string, string> = { ESTABLISHED: "established", NEW: "new" };

/** правило iptables из параметров командной строки (фильтр FORWARD и таблица nat) */
type RuleSpec = Partial<Omit<FwRule, "action">> & { action?: string; to?: string };

function parseRuleSpec(tokens: string[]): RuleSpec & { error?: string } {
  const r: RuleSpec = {};
  for (let i = 0; i < tokens.length; i++) {
    const t = tokens[i];
    const v = tokens[i + 1];
    if (t === "-s") (r.src = v), i++;
    else if (t === "-d") (r.dst = v), i++;
    else if (t === "-i") (r.in = v), i++;
    else if (t === "-o") (r.out = v), i++;
    else if (t === "-p") (r.proto = v), i++;
    else if (t === "--dport") (r.dport = Number(v)), i++;
    else if (t === "--sport") (r.sport = Number(v)), i++;
    else if (t === "-j") (r.action = v), i++;
    else if (t === "--to-destination") (r.to = v), i++;
    else if (t === "-m") i++;
    else if (t === "--ctstate" || t === "--state") {
      const parts = v.split(",");
      r.state = parts.every((p) => p === "ESTABLISHED" || p === "RELATED")
        ? "established"
        : parts.length === 1
          ? STATE_MAP[parts[0]]
          : undefined;
      i++;
    } else return { error: `iptables: неизвестный параметр «${t}»` };
  }
  return r;
}

const canon = (r: object): string => JSON.stringify(Object.fromEntries(Object.entries(r).filter(([, v]) => v !== undefined).sort(([a], [b]) => (a < b ? -1 : 1))));

function ruleText(r: RuleSpec): string {
  const parts: string[] = [];
  if (r.in) parts.push(`-i ${r.in}`);
  if (r.out) parts.push(`-o ${r.out}`);
  if (r.proto) parts.push(`-p ${r.proto}`);
  if (r.src) parts.push(`-s ${r.src}`);
  if (r.dst) parts.push(`-d ${r.dst}`);
  if (r.sport) parts.push(`--sport ${r.sport}`);
  if (r.dport) parts.push(`--dport ${r.dport}`);
  if (r.state) parts.push(`state ${r.state === "established" ? "ESTABLISHED,RELATED" : "NEW"}`);
  if (r.to) parts.push(`to:${r.to}`);
  return parts.join(" ") || "anywhere";
}

function iptables(d: Device, tokens: string[]): CmdResult {
  let table = "filter";
  let i = 0;
  if (tokens[0] === "-t") {
    table = tokens[1];
    i = 2;
  }
  if (table !== "nat" && table !== "filter") return { out: `iptables: таблица «${table}» не поддерживается` };
  const op = tokens[i];
  const chain = tokens[i + 1];
  const rest = tokens.slice(i + 2);
  const nat = table === "nat";

  if (op === "-L" || op === "-S") {
    const chains = nat ? ["PREROUTING", "POSTROUTING"] : ["FORWARD"];
    const want = chain && !chain.startsWith("-") ? [chain] : chains;
    const out: string[] = [];
    for (const c of want) {
      if (!chains.includes(c)) return { out: `iptables: нет цепочки «${c}» в таблице ${table}` };
      if (nat) {
        out.push(`Chain ${c} (policy ACCEPT)`);
        d.nat
          .filter((n) => n.chain === c)
          .forEach((n, k) => out.push(`${k + 1}  ${n.action}  ${ruleText(n)}`));
      } else {
        out.push(`Chain ${c} (policy ${d.fw.policy})`);
        d.fw.rules
          .forEach((n, k) => out.push(`${k + 1}  ${n.action}  ${ruleText(n)}`));
      }
    }
    return { out: out.join("\n") };
  }
  const bad = NO(d);
  if (bad) return { out: bad };

  if (op === "-F") {
    if (nat) d.nat = [];
    else d.fw.rules = [];
    return { out: "", changed: true };
  }
  if (op === "-P") {
    if (nat || chain !== "FORWARD")
      return { out: "iptables: политику можно задать только для FORWARD" };
    if (!["ACCEPT", "DROP"].includes(rest[0])) return { out: "iptables: политика — ACCEPT или DROP" };
    d.fw.policy = rest[0];
    return { out: "", changed: true };
  }
  if (op === "-A" || op === "-I" || op === "-D") {
    let spec = rest;
    let pos = 0;
    if (op === "-I" && /^\d+$/.test(rest[0] ?? "")) {
      pos = Number(rest[0]) - 1;
      spec = rest.slice(1);
    }
    const r = parseRuleSpec(spec);
    if (r.error) return { out: r.error };
    const action = r.action;
    if (!action) return { out: "iptables: не указана цель (-j)" };
    if (nat) {
      if (!["PREROUTING", "POSTROUTING"].includes(chain))
        return { out: `iptables: в таблице nat моделируются цепочки PREROUTING и POSTROUTING` };
      if (chain === "POSTROUTING" && r.action !== "MASQUERADE")
        return { out: "iptables: в POSTROUTING поддерживается цель MASQUERADE" };
      if (chain === "PREROUTING" && (r.action !== "DNAT" || !r.to))
        return { out: "iptables: в PREROUTING нужна цель DNAT --to-destination адрес[:порт]" };
      if (r.to && parseIp(r.to.split(":")[0]) === null)
        return { out: `iptables: неверный адрес «${r.to}»` };
      const rule: NatRule = { chain, ...r, action };
      if (op === "-D") {
        const k = d.nat.findIndex((n) => canon(n) === canon(rule));
        if (k < 0) return { out: "iptables: такого правила нет" };
        d.nat.splice(k, 1);
      } else if (op === "-I") {
        const first = d.nat.findIndex((n) => n.chain === chain);
        d.nat.splice(first < 0 ? d.nat.length : first + pos, 0, rule);
      } else d.nat.push(rule);
      return { out: "", changed: true };
    }
    if (chain !== "FORWARD")
      return { out: "iptables: в этом симуляторе фильтруется только цепочка FORWARD" };
    if (!["ACCEPT", "DROP", "REJECT"].includes(action))
      return { out: "iptables: цель — ACCEPT, DROP или REJECT" };
    const fw: FwRule = { ...r, action };
    if (op === "-D") {
      const k = d.fw.rules.findIndex((n) => canon(n) === canon(fw));
      if (k < 0) return { out: "iptables: такого правила нет" };
      d.fw.rules.splice(k, 1);
    } else if (op === "-I") d.fw.rules.splice(pos, 0, fw);
    else d.fw.rules.push(fw);
    return { out: "", changed: true };
  }
  return { out: "iptables: неизвестная операция. Пример: iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE" };
}

/* ---- имена: hosts → DNS-запрос к резолверу ------------------------------------------ */

/** имя или адрес → {ip, run} | {err}; run — проба DNS для анимации/журнала */
export function toIp(state: NetState, d: Device, arg: string): ReturnType<ToIp> {
  const l = localLookup(d, arg);
  if (l.ip !== undefined && l.ip !== null) return { ip: l.ip, from: l.from };
  if (l.error) return { err: `Temporary failure in name resolution (${l.error})` };
  if (l.ask === undefined || l.ask === null) return { err: "Temporary failure in name resolution (в /etc/resolv.conf нет DNS-сервера)" };
  const run = dns1(state, d.id, l.ask, { name: fqdn(arg), type: "A" });
  if (run.status !== "reply" || !run.dns) return { err: "Temporary failure in name resolution (DNS-сервер не отвечает)", run };
  const ip = answerIp(run.dns);
  if (ip === null) return { err: run.dns.rcode === "NXDOMAIN" ? "Name or service not known (NXDOMAIN)" : `имя не разрешилось (${run.dns.rcode})`, run };
  return { ip, run };
}

function doDig(state: NetState, d: Device, a: string[], mode: string): CmdResult {
  const at = a.find((x) => x.startsWith("@"));
  const rest = a.filter((x) => !x.startsWith("@"));
  let name = rest[0];
  let type = (rest[1] ?? "A").toUpperCase();
  let server = at ? parseIp(at.slice(1)) : d.resolver ? parseIp(d.resolver) : null;
  if (mode === "nslookup" && rest[1] && parseIp(rest[1]) !== null) {
    server = parseIp(rest[1]);
    type = "A";
  }
  if (!name) return { out: "dig: укажите имя: dig www.example.org [A|CNAME|NS] [@сервер]" };
  if (server === null) return { out: "dig: нет DNS-сервера: добавьте «nameserver …» в /etc/resolv.conf или укажите @сервер" };
  const run = dns1(state, d.id, server, { name: fqdn(name), type });
  if (run.status !== "reply" || !run.dns)
    return { out: ";; соединение не удалось: DNS-сервер " + ipStr(server) + " не отвечает (timed out)", probe: run };
  const out = [
    `;; опрос ${ipStr(server)}, вопрос «${fqdn(name)} ${type}», время ${fmtMs(run.rttUs)}`,
    fmtDns(run.dns),
  ].join("\n");
  return { out, probe: run };
}

function dnsAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (sub === "show" || !sub) {
    if (!d.dns) return { out: "DNS-сервер на этом устройстве не включён (dns enable)" };
    const L = [`режим: ${d.dns.recursive ? "рекурсивный резолвер" : "авторитативный сервер"}`];
    if (d.dns.zones.length) L.push(`зоны: ${d.dns.zones.join(", ")}`);
    if (d.dns.roots.length) L.push(`корневые серверы: ${d.dns.roots.join(", ")}`);
    for (const r of d.dns.records) L.push(`${r.name}.  ${r.ttl ?? 300}  IN  ${r.type}  ${r.value}`);
    for (const x of d.dns.delegations) L.push(`делегирование: ${x.zone} → NS ${x.ns}`);
    return { out: L.join("\n") };
  }
  if (bad) return { out: bad };
  if (sub === "enable") {
    d.dns ??= newDns();
    return { out: "DNS-сервер включён (слушает udp/53)", changed: true };
  }
  if (!d.dns) return { out: "сначала включите DNS-сервер: dns enable" };
  if (sub === "recursive") {
    d.dns.recursive = a[1] !== "off";
    return { out: `рекурсия: ${d.dns.recursive ? "включена" : "выключена"}`, changed: true };
  }
  if (sub === "root") {
    if (parseIp(a[1] ?? "") === null) return { out: "dns root <ip корневого сервера>" };
    d.dns.roots = [a[1]];
    return { out: "корневой сервер задан", changed: true };
  }
  if (sub === "zone") {
    const z = fqdn(a[1] ?? "");
    if (!z) return { out: "dns zone <зона>" };
    if (!d.dns.zones.includes(z)) d.dns.zones.push(z);
    return { out: `зона ${z} обслуживается этим сервером`, changed: true };
  }
  if (sub === "add") {
    const [, name, type, ...v] = a;
    const value = v[0];
    const T = (type ?? "").toUpperCase();
    if (!name || !["A", "CNAME", "NS", "MX", "TXT"].includes(T) || !value) return { out: "dns add <имя> <A|CNAME|MX|TXT> <значение> [ttl]" };
    if (T === "A" && parseIp(value) === null) return { out: `неверный IPv4-адрес «${value}»` };
    const ttl = Number(v[1]) || 300;
    d.dns.records.push({ name: fqdn(name), type: T, value: T === "CNAME" ? fqdn(value) : value, ttl });
    return { out: "запись добавлена", changed: true };
  }
  if (sub === "del") {
    const name = fqdn(a[1] ?? "");
    const T = a[2] ? a[2].toUpperCase() : null;
    const n = d.dns.records.length;
    d.dns.records = d.dns.records.filter((r) => !(fqdn(r.name) === name && (!T || r.type === T)));
    return d.dns.records.length < n ? { out: "запись удалена", changed: true } : { out: "такой записи нет" };
  }
  if (sub === "delegate") {
    if (!a[1] || parseIp(a[2] ?? "") === null) return { out: "dns delegate <зона> <ip сервера имён>" };
    d.dns.delegations = d.dns.delegations.filter((x) => fqdn(x.zone) !== fqdn(a[1]));
    d.dns.delegations.push({ zone: fqdn(a[1]), ns: a[2] });
    return { out: `зона ${fqdn(a[1])} делегирована ${a[2]}`, changed: true };
  }
  if (sub === "undelegate") {
    d.dns.delegations = d.dns.delegations.filter((x) => fqdn(x.zone) !== fqdn(a[1] ?? ""));
    return { out: "делегирование убрано", changed: true };
  }
  return { out: "dns show | enable | recursive on|off | root <ip> | zone <z> | add … | del … | delegate <зона> <ip> | undelegate <зона>" };
}

function fileWrite(d: Device, line: string): CmdResult | null {
  const m = /^echo\s+(.*?)\s*(>>?)\s*(\/etc\/(?:resolv\.conf|hosts))\s*$/.exec(line);
  if (!m) return null;
  const bad = NO(d);
  if (bad) return { out: bad };
  const body = m[1].replace(/^["']|["']$/g, "").trim();
  if (m[3].endsWith("resolv.conf")) {
    const ip = /^nameserver\s+(\S+)$/.exec(body)?.[1];
    if (!ip || parseIp(ip) === null) return { out: "в resolv.conf нужна строка вида: nameserver 10.0.0.53" };
    d.resolver = ip;
    return { out: "", changed: true };
  }
  const h = /^(\S+)\s+(\S+)$/.exec(body);
  if (!h || parseIp(h[1]) === null) return { out: "в hosts нужна строка вида: 10.0.0.5 имя" };
  d.hosts = m[2] === ">" ? {} : { ...(d.hosts ?? {}) };
  d.hosts[fqdn(h[2])] = h[1];
  return { out: "", changed: true };
}

function doCurl(state: NetState, d: Device, a: string[]): CmdResult {
  let method = "GET";
  let proxy: string | null = null;
  const headers: Record<string, string> = {};
  const flags = new Set<string>();
  let url: string | null = null;
  for (let i = 0; i < a.length; i++) {
    const x = a[i];
    if (x === "-x") proxy = a[++i];
    else if (x === "-X") method = (a[++i] ?? "GET").toUpperCase();
    else if (x === "-H") {
      const [k, ...v] = (a[++i] ?? "").replace(/^["']|["']$/g, "").split(":");
      headers[k.trim().toLowerCase()] = v.join(":").trim();
    } else if (x.startsWith("-")) {
      for (const ch of x.slice(1)) flags.add(ch);
    } else url = x.replace(/^["']|["']$/g, "");
  }
  if (!url) return { out: "curl: укажите адрес, например curl -v http://www.example.org/" };
  if (!/^https?:\/\//i.test(url)) url = "http://" + url;
  const head = flags.has("I");
  if (head) method = "HEAD";
  const r = httpFetch(state, d, { url, method, follow: flags.has("L"), headers, toIp, proxy });
  return { out: fmtCurl(r, { verbose: flags.has("v"), head, method }), probe: r.run, http: r };
}

function webAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") {
    if (!d.http) return { out: "веб-сервер не включён (web enable)" };
    return { out: d.http.routes.map((r) => `${r.path}  ${r.status ?? 200}${r.location ? " → " + r.location : ""}${r.headers ? "  " + Object.entries(r.headers).map(([k, v]) => `${k}: ${v}`).join("; ") : ""}`).join("\n") || "(маршрутов нет)" };
  }
  if (bad) return { out: bad };
  if (sub === "enable") {
    d.http ??= newHttp();
    if (!d.services.some((s) => s.proto === "tcp" && s.port === 80)) d.services.push({ proto: "tcp", port: 80 });
    return { out: "веб-сервер включён на tcp/80", changed: true };
  }
  if (!d.http) return { out: "сначала: web enable" };
  const path = a[1];
  if (sub === "route") {
    const status = Number(a[2] ?? 200);
    if (!path || !path.startsWith("/") || !(status >= 100 && status < 600)) return { out: "web route /путь <код> [текст ответа]" };
    d.http.routes = d.http.routes.filter((r) => r.path !== path);
    d.http.routes.push({ path, status, body: a.slice(3).join(" ") || undefined });
    return { out: `маршрут ${path} → ${status}`, changed: true };
  }
  if (sub === "redirect") {
    const status = Number(a[2] ?? 301);
    if (!path || !a[3] || ![301, 302, 307, 308].includes(status)) return { out: "web redirect /старый <301|302|307|308> /новый" };
    d.http.routes = d.http.routes.filter((r) => r.path !== path);
    d.http.routes.push({ path, status, location: a[3] });
    return { out: `${path} → ${status} → ${a[3]}`, changed: true };
  }
  if (sub === "header") {
    const r = d.http.routes.find((x) => x.path === path);
    if (!r) return { out: `нет маршрута ${path}` };
    if (!a[2]) return { out: "web header /путь Имя значение" };
    (r.headers ??= {})[a[2].toLowerCase()] = a.slice(3).join(" ");
    return { out: "заголовок добавлен", changed: true };
  }
  if (sub === "protocol") {
    const proto = a[1];
    if (proto !== "h1" && proto !== "h2" && proto !== "h3") return { out: "web protocol h1|h2|h3" };
    d.http.protocol = proto;
    return { out: `сервер предлагает ${{ h1: "HTTP/1.1", h2: "HTTP/2", h3: "HTTP/3" }[a[1]]}${a[1] === "h3" ? " (нужен открытый UDP/443)" : ""}`, changed: true };
  }
  if (sub === "etag") {
    const r = d.http.routes.find((x) => x.path === path);
    if (!r || !a[2]) return { out: "web etag /путь значение" };
    r.etag = a[2];
    return { out: "ETag задан", changed: true };
  }
  if (sub === "del") {
    d.http.routes = d.http.routes.filter((r) => r.path !== path);
    return { out: "маршрут удалён", changed: true };
  }
  return { out: "web show | enable | protocol h1|h2|h3 | route /p код [текст] | redirect /p код /куда | header /p Имя знач | etag /p знач | del /p" };
}

function tlsAdmin(state: NetState, d: Device, a: string[]) {
  const cas = (state.pki ?? DEFAULT_PKI).cas;
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") {
    if (!d.tls) return { out: "TLS на этом устройстве не включён (tls enable)" };
    const c = d.tls.cert;
    return { out: [`сертификат: CN=${c.cn}`, `  SAN: ${c.san.join(", ")}`, `  издатель: ${c.issuer}`, `  действует до: ${c.notAfter} (сегодня ${NOW})`, `цепочка, которую сервер присылает: ${d.tls.chain.length ? d.tls.chain.join(" → ") : "(только свой сертификат)"}`, `версии TLS: ${d.tls.versions.join(", ")}`].join("\n") };
  }
  if (bad) return { out: bad };
  if (sub === "enable") {
    d.tls ??= newTls();
    if (!d.services.some((s) => s.proto === "tcp" && s.port === 443)) d.services.push({ proto: "tcp", port: 443 });
    return { out: "TLS включён на tcp/443", changed: true };
  }
  if (!d.tls) return { out: "сначала: tls enable" };
  if (sub === "cert" && a[1] === "new") {
    const rest = a.slice(2);
    const iss = rest.indexOf("--issuer");
    const days = rest.indexOf("--days");
    const issuer = iss >= 0 ? rest[iss + 1] : null;
    const n = days >= 0 ? Number(rest[days + 1]) : 90;
    const names = rest.filter((x, i) => !x.startsWith("--") && (iss < 0 || (i !== iss + 1)) && (days < 0 || i !== days + 1));
    if (!names.length || !issuer || !(n >= 1)) return { out: "tls cert new <имя> [доп. имена…] --issuer <CA> --days <N>" };
    if (!cas[issuer] || cas[issuer].issuer === null && false) return { out: `неизвестный издатель «${issuer}» (доступны: ${Object.keys(cas).join(", ")})` };
    d.tls.cert = { cn: names[0], san: names, issuer, notAfter: addDays(n) };
    return { out: `выпущен сертификат CN=${names[0]} SAN=${names.join(",")} издатель ${issuer} до ${d.tls.cert.notAfter}`, changed: true };
  }
  if (sub === "chain") {
    if (a[1] === "clear") {
      d.tls.chain = [];
      return { out: "цепочка очищена: сервер присылает только свой сертификат", changed: true };
    }
    if (a[1] === "add") {
      if (!cas[a[2]]) return { out: `неизвестный CA «${a[2] ?? ""}»` };
      if (!d.tls.chain.includes(a[2])) d.tls.chain.push(a[2]);
      return { out: `в цепочку добавлен ${a[2]}`, changed: true };
    }
  }
  if (sub === "versions") {
    const v = (a[1] ?? "").split(",").filter(Boolean);
    if (!v.length || v.some((x: string) => !["1.0", "1.1", "1.2", "1.3"].includes(x))) return { out: "tls versions 1.2,1.3" };
    d.tls.versions = v;
    return { out: `версии: ${v.join(", ")}`, changed: true };
  }
  return { out: "tls show | enable | cert new <имя> [имена…] --issuer <CA> --days N | chain add <CA> | chain clear | versions 1.2,1.3" };
}

function trustAdmin(state: NetState, d: Device, a: string[]) {
  const cas = (state.pki ?? DEFAULT_PKI).cas;
  const sub = a[0];
  if (!sub || sub === "show") return { out: `доверенные корневые CA: ${(d.trust ?? DEFAULT_TRUST).join(", ")}` };
  const bad = NO(d);
  if (bad) return { out: bad };
  if (sub === "add") {
    if (!cas[a[1]]) return { out: `неизвестный CA «${a[1] ?? ""}» (доступны: ${Object.keys(cas).join(", ")})` };
    d.trust = [...new Set([...(d.trust ?? DEFAULT_TRUST), a[1]])];
    return { out: `корневой CA ${a[1]} добавлен в хранилище доверия`, changed: true };
  }
  if (sub === "del") {
    d.trust = (d.trust ?? DEFAULT_TRUST).filter((x) => x !== a[1]);
    return { out: "удалён из хранилища", changed: true };
  }
  return { out: "trust show | add <CA> | del <CA>" };
}

function proxyAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") return { out: d.proxy ? `прокси на tcp/${d.proxy.port ?? 3128}; запрещены: ${d.proxy.deny.join(", ") || "(нет)"}` : "прокси не включён (proxy enable)" };
  if (bad) return { out: bad };
  if (sub === "enable") {
    d.proxy ??= { port: 3128, deny: [] };
    const port = d.proxy.port ?? 3128;
    if (!d.services.some((s) => s.proto === "tcp" && s.port === port)) d.services.push({ proto: "tcp", port });
    return { out: `HTTP-прокси включён на tcp/${port}`, changed: true };
  }
  if (!d.proxy) return { out: "сначала: proxy enable" };
  if (sub === "deny" && a[1]) {
    if (!d.proxy.deny.includes(a[1])) d.proxy.deny.push(a[1]);
    return { out: `${a[1]} запрещён`, changed: true };
  }
  if (sub === "allow" && a[1]) {
    d.proxy.deny = d.proxy.deny.filter((x) => x !== a[1]);
    return { out: `${a[1]} разрешён`, changed: true };
  }
  return { out: "proxy show | enable | deny <хост> | allow <хост>" };
}

function lbAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") {
    if (!d.lb) return { out: "на этом узле нет балансировщика" };
    return { out: [`виртуальный адрес ${d.lb.vip}:${d.lb.port}`, `алгоритм: ${d.lb.algo === "hash" ? "хеш по адресу клиента (привязка)" : "по кругу"}`, `проверка здоровья: ${d.lb.health ? "включена" : "выключена"}`, ...d.lb.backends.map((b) => `  сервер ${b.ip}:${b.port}`)].join("\n") };
  }
  if (bad) return { out: bad };
  const lb = d.lb;
  if (!lb) return { out: "на этом узле нет балансировщика" };
  if (sub === "add") {
    const [ip, port] = (a[1] ?? "").split(":");
    if (parseIp(ip ?? "") === null) return { out: "lb add <ip>:<порт>" };
    if (lb.backends.some((b) => b.ip === ip && b.port === Number(port ?? lb.port))) return { out: "такой сервер уже в пуле" };
    lb.backends.push({ ip, port: Number(port ?? lb.port) });
    return { out: `сервер ${ip}:${port ?? lb.port} добавлен в пул`, changed: true };
  }
  if (sub === "del") {
    const n = lb.backends.length;
    lb.backends = lb.backends.filter((b) => b.ip !== (a[1] ?? "").split(":")[0]);
    return lb.backends.length < n ? { out: "удалён из пула", changed: true } : { out: "такого сервера нет" };
  }
  if (sub === "algo") {
    if (!["rr", "hash"].includes(a[1])) return { out: "lb algo rr (по кругу) | hash (привязка по адресу клиента)" };
    lb.algo = a[1];
    return { out: `алгоритм: ${a[1]}`, changed: true };
  }
  if (sub === "health") {
    lb.health = a[1] !== "off";
    return { out: `проверка здоровья ${lb.health ? "включена" : "выключена"}`, changed: true };
  }
  return { out: "lb show | add ip:порт | del ip | algo rr|hash | health on|off" };
}

function rproxyAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") return { out: d.rproxy ? d.rproxy.rules.map((r) => `${r.host ?? "*"}${r.path ?? "/"} → ${r.backend}${r.cache ? "  [кэш]" : ""}`).join("\n") || "(правил нет)" : "обратный прокси не включён (rproxy enable)" };
  if (bad) return { out: bad };
  if (sub === "enable") {
    d.rproxy ??= { rules: [] };
    if (!d.services.some((s) => s.proto === "tcp" && s.port === 80)) d.services.push({ proto: "tcp", port: 80 });
    return { out: "обратный прокси включён на tcp/80", changed: true };
  }
  if (!d.rproxy) return { out: "сначала: rproxy enable" };
  if (sub === "add") {
    const [, host, path, backend] = a;
    if (!path?.startsWith("/") || !backend || parseIp(backend.split(":")[0]) === null) return { out: "rproxy add <хост|*> </путь> <ip:порт>" };
    d.rproxy.rules = d.rproxy.rules.filter((r) => !((r.host ?? "*") === host && r.path === path));
    d.rproxy.rules.push({ host: host === "*" ? undefined : host, path, backend });
    return { out: `правило: ${host}${path} → ${backend}`, changed: true };
  }
  if (sub === "del") {
    d.rproxy.rules = d.rproxy.rules.filter((r) => r.path !== a[1]);
    return { out: "правило удалено", changed: true };
  }
  if (sub === "cache") {
    const r = d.rproxy.rules.find((x) => x.path === a[1]);
    if (!r) return { out: `нет правила для ${a[1] ?? ""}` };
    r.cache = a[2] !== "off";
    return { out: `кэш для ${a[1]}: ${r.cache ? "включён" : "выключен"}`, changed: true };
  }
  return { out: "rproxy show | enable | add <хост|*> /путь ip:порт | del /путь | cache /путь on|off" };
}

function sshClient(state: NetState, d: Device, cmd: string, a: string[]): CmdResult {
  if (cmd === "ssh-keygen") {
    if (a[0] === "-R") {
      if (d.knownHosts) delete d.knownHosts[a[1]];
      return { out: `адрес ${a[1] ?? ""} удалён из known_hosts`, changed: true };
    }
    if (a[0] === "-l") return { out: d.sshKey ? `256 ${d.sshKey} (ED25519)` : "ключа нет: ssh-keygen" };
    const bad = NO(d);
    if (bad) return { out: bad };
    d.sshKey = makeKey(d);
    return { out: `Создана пара ключей ED25519. Отпечаток: ${d.sshKey}`, changed: true };
  }
  const flags: { pass: string | null; jump: string | null; noKey: boolean } = { pass: null, jump: null, noKey: false };
  const rest: string[] = [];
  for (let i = 0; i < a.length; i++) {
    if (a[i] === "-P" || a[i] === "-p") flags.pass = a[++i];
    else if (a[i] === "-J") flags.jump = a[++i];
    else if (a[i] === "-o" && a[i + 1] === "PubkeyAuthentication=no") (flags.noKey = true), i++;
    else rest.push(a[i]);
  }
  const target = rest[rest.length - 1] ?? "";
  const [user, host] = target.includes("@") ? target.split("@") : [null, target];
  if (!user || !host) return { out: `${cmd}: укажите пользователя и узел: ${cmd} alice@10.0.0.5` };
  const res = toIp(state, d, host);
  if (res.err !== undefined) return { out: `ssh: ${host}: ${res.err}` };
  let jump: { ip: number } | null = null;
  if (flags.jump) {
    const [, jh] = flags.jump.includes("@") ? flags.jump.split("@") : [null, flags.jump];
    const jr = toIp(state, d, jh);
    if (jr.err !== undefined) return { out: `ssh: бастион ${jh}: ${jr.err}` };
    jump = { ip: jr.ip };
  }
  if (cmd === "ssh-copy-id") {
    if (!d.sshKey) return { out: "ssh-copy-id: у вас нет ключа — выполните ssh-keygen" };
    const r = sshConnect(state, d, user, res.ip, { pass: flags.pass, noKey: true, jump });
    if (!r.ok || !r.srv) return { out: r.error ?? "", probe: r.run };
    const u = r.srv.ssh?.users[user];
    if (u && !u.keys.includes(d.sshKey)) u.keys.push(d.sshKey);
    return { out: `Ключ ${d.sshKey} добавлен на ${r.srv.name} для пользователя ${user}`, changed: true, probe: r.run };
  }
  const r = sshConnect(state, d, user, res.ip, { pass: flags.pass, noKey: flags.noKey, jump });
  if (!r.ok || !r.srv) return { out: r.error ?? "", probe: r.run };
  return { out: [...(r.lines ?? []), `${user}@${r.srv.name}:~$ (сеанс установлен; exit — выйти)`].join("\n"), probe: r.run };
}

function sshdAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") {
    if (!d.ssh) return { out: "SSH-сервер не включён (sshd enable)" };
    return { out: [`ключ хоста: ${d.ssh.hostKey}`, `вход по паролю: ${d.ssh.passwordAuth ? "разрешён" : "выключен"}`, ...Object.entries(d.ssh.users).map(([u, v]) => `пользователь ${u}: ключей ${v.keys.length}${v.keys.length ? " (" + v.keys.join(", ") + ")" : ""}`)].join("\n") };
  }
  if (bad) return { out: bad };
  if (sub === "enable") {
    d.ssh ??= newSsh();
    if (!d.services.some((s) => s.proto === "tcp" && s.port === 22)) d.services.push({ proto: "tcp", port: 22 });
    return { out: "SSH-сервер включён на tcp/22", changed: true };
  }
  if (!d.ssh) return { out: "сначала: sshd enable" };
  if (sub === "user") {
    if (!a[1]) return { out: "sshd user <имя> [пароль]" };
    d.ssh.users[a[1]] = { keys: d.ssh.users[a[1]]?.keys ?? [], password: a[2] ?? d.ssh.users[a[1]]?.password };
    return { out: `пользователь ${a[1]} создан`, changed: true };
  }
  if (sub === "authorize") {
    const u = d.ssh.users[a[1]];
    if (!u || !a[2]) return { out: "sshd authorize <пользователь> <отпечаток ключа>" };
    if (!u.keys.includes(a[2])) u.keys.push(a[2]);
    return { out: `ключ ${a[2]} разрешён для ${a[1]}`, changed: true };
  }
  if (sub === "password") {
    if (!["on", "off"].includes(a[1])) return { out: "sshd password on|off" };
    d.ssh.passwordAuth = a[1] === "on";
    return { out: `вход по паролю ${d.ssh.passwordAuth ? "разрешён" : "выключен"}`, changed: true };
  }
  if (sub === "hostkey") {
    d.ssh.hostKey = `SHA256:hostKey${Math.abs([...d.id].reduce((s, c) => s + c.charCodeAt(0), 0) * 31 + (d.ssh.rot = (d.ssh.rot ?? 0) + 1))}`;
    return { out: `ключ хоста заменён: ${d.ssh.hostKey}`, changed: true };
  }
  return { out: "sshd show | enable | user <имя> [пароль] | authorize <пользователь> <отпечаток> | password on|off | hostkey" };
}

function vpnAdmin(d: Device, a: string[]): CmdResult {
  const bad = NO(d);
  const sub = a[0];
  if (!sub || sub === "show") {
    const t = d.ifaces.filter((i) => i.tun);
    return { out: t.length ? t.map((i) => `${i.name}: ${i.ip}/${i.prefix} ↔ ${i.tun?.peer}:${i.tun?.port}  ключ ${i.tun?.key ? "задан" : "нет"}  ${i.up ? "up" : "down"}`).join("\n") : "туннелей нет" };
  }
  if (bad) return { out: bad };
  if (sub === "add") {
    const name = a[1];
    const g = (flag: string) => a[a.indexOf(flag) + 1];
    const peer = g("--peer");
    const addr = g("--address");
    const key = g("--key");
    const c = parseCidr(addr ?? "");
    if (!name || parseIp(peer ?? "") === null || !c || !key) return { out: "vpn add wg0 --peer <внешний IP пира> --address 10.9.0.1/30 --key <общий секрет>" };
    if (getIface(d, name)) return { out: `интерфейс ${name} уже есть` };
    d.ifaces.push({ name, mac: "00:00:00:00:00:00", ip: ipStr(c.ip), prefix: c.prefix, up: true, tun: { peer, port: 51820, key } });
    return { out: `туннель ${name} создан: пир ${peer}, UDP/51820. Теперь добавьте маршруты в чужие сети: ip route add <сеть> dev ${name}`, changed: true };
  }
  if (sub === "del") {
    d.ifaces = d.ifaces.filter((i) => !(i.tun && i.name === a[1]));
    d.routes = d.routes.filter((r) => r.dev !== a[1]);
    return { out: "туннель удалён", changed: true };
  }
  return { out: "vpn show | add <имя> --peer <ip> --address <ip/маска> --key <секрет> | del <имя>" };
}

/* ---- ping / traceroute / curl ------------------------------------------------------ */

function doPing(state: NetState, d: Device, args: string[]): CmdResult {
  let count = 3;
  let ttl = 64;
  let size: number | null = null;
  let df = false;
  const rest: string[] = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "-c") count = Math.min(10, Number(args[++i]) || 3);
    else if (args[i] === "-t") ttl = Number(args[++i]) || 64;
    else if (args[i] === "-s") size = Math.max(0, Number(args[++i]) || 56);
    else if (args[i] === "-M") df = args[++i] === "do";
    else rest.push(args[i]);
  }
  if (!rest[0]) return { out: "ping: укажите адрес или имя" };
  const name = rest[0];
  const res = toIp(state, d, name);
  if (res.err !== undefined) return { out: `ping: ${name}: ${res.err}`, probe: res.run };
  const dst = res.ip;
  if (!lookup(d, dst) && !d.ifaces.some((i) => i.ip === ipStr(dst)))
    return { out: "ping: connect: Network is unreachable" };
  rest[0] = ipStr(dst);
  const lines = [`PING ${name}${name !== rest[0] ? ` (${rest[0]})` : ""}: ${size ?? 56} data bytes${df ? ", DF" : ""}`];
  let got = 0;
  let last: ProbeRun | null = null;
  for (let s = 1; s <= count; s++) {
    const r = ping1(state, d.id, dst, { ttl, id: s, size, df });
    last = r;
    if (r.status === "toolong") lines.push(`ping: local error: message too long, mtu=${r.mtu}`);
    else if (r.status === "unreach" && r.code === "frag") lines.push(`From ${ipStr(r.from)} icmp_seq=${s} Frag needed and DF set (mtu = ${r.mtu})`);
    else if (r.status === "reply") {
      got++;
      lines.push(`${(size ?? 56) + 8} bytes from ${ipStr(r.from)}: icmp_seq=${s} time=${fmtMs(r.rttUs)}`);
    } else if (r.status === "ttl") lines.push(`From ${ipStr(r.from)} icmp_seq=${s} Time to live exceeded`);
    else if (r.status === "unreach") lines.push(`From ${ipStr(r.from)} icmp_seq=${s} Destination Host Unreachable`);
    else lines.push(`Request timeout for icmp_seq=${s}`);
  }
  lines.push(`--- ${rest[0]} ping statistics ---`);
  lines.push(`${count} packets transmitted, ${got} received, ${Math.round(((count - got) / count) * 100)}% packet loss`);
  return { out: lines.join("\n"), probe: last };
}

function doTraceroute(state: NetState, d: Device, args: string[]): CmdResult {
  const res = toIp(state, d, args[0] ?? "");
  if (res.err !== undefined) return { out: `traceroute: ${args[0] ?? ""}: ${res.err}` };
  const dst = res.ip;
  if (!lookup(d, dst)) return { out: "traceroute: connect: Network is unreachable" };
  const hops = traceroute(state, d.id, dst);
  const lines = [`traceroute to ${args[0]}, 12 hops max`];
  for (const h of hops)
    lines.push(
      h.status === "timeout"
        ? ` ${h.ttl}  * * *`
        : ` ${h.ttl}  ${ipStr(h.from)}  ${fmtMs(h.rttUs)}`,
    );
  return { out: lines.join("\n"), probe: hops[hops.length - 1] };
}

function doConnect(state: NetState, d: Device, host: string, port: number, mode: string, session = false): CmdResult {
  const res = toIp(state, d, host);
  if (res.err !== undefined) return { out: `${mode}: ${host}: ${res.err}`, probe: res.run };
  const dst = res.ip;
  if (!lookup(d, dst)) return { out: `${mode}: Network is unreachable` };
  const r = tcp1(state, d.id, dst, port, { session });
  const msgs: Record<string, string> = {
    connected: `соединение с ${host}:${port} установлено (SYN → SYN-ACK → ACK) за ${fmtMs(r.rttUs)}${session ? "; запрос 100 Б, ответ 1000 Б, закрыто (FIN). Подробности — в журнале ниже" : ""}`,
    refused: `${mode}: Connection refused — порт ${port} никто не слушает`,
    timeout: `${mode}: Connection timed out — ответа нет (пакет потерян или отфильтрован)`,
    unreach: `${mode}: Destination unreachable от ${r.from ? ipStr(r.from) : "?"}`,
    ttl: `${mode}: TTL истёк`,
  };
  return { out: msgs[r.status] ?? r.status, probe: r };
}

function doUdp(state: NetState, d: Device, host: string, port: number): CmdResult {
  const dst = parseIp(host);
  if (dst === null || !port) return { out: "nc -u: нужно nc -u <ip> <порт>" };
  if (!lookup(d, dst)) return { out: "nc: Network is unreachable" };
  const r = udp1(state, d.id, dst, port);
  const msg =
    r.status === "reply"
      ? `ответная датаграмма от ${host}:${port} за ${fmtMs(r.rttUs)}`
      : r.status === "unreach"
        ? `ICMP: ${r.code === "port" ? "порт недоступен" : "узел недоступен"} (от ${r.from ? ipStr(r.from) : "?"}) — «Connection refused»`
        : "тишина: ответа нет (датаграмма потеряна, отфильтрована или сервер молчит) — UDP не сообщит об этом сам";
  return { out: msg, probe: r };
}

/* ---- разбор строки ------------------------------------------------------------------- */

export function exec(state: NetState, devId: string, line: string): CmdResult {
  const d = state.devices[devId];
  const tokens = line.trim().split(/\s+/).filter(Boolean);
  if (!tokens.length) return { out: "" };
  rtOf(state);
  const fw = line.trim().startsWith("echo") ? fileWrite(d, line.trim()) : null;
  if (fw) return fw;
  const [cmd, ...a] = tokens;
  const done = (err: string | null, extra: Partial<CmdResult> = {}): CmdResult => ({ out: err ?? "", changed: !err, ...extra });

  if (cmd === "clear") return { out: "", clear: true };
  if (cmd === "help" || cmd === "?") return { out: HELP };
  if (cmd === "hostname") return { out: d.name };

  if (d.kind === "hub")
    return { out: "Хаб — повторитель: у него нет ни настроек, ни таблицы адресов. Всё, что пришло на порт, он повторяет на все остальные." };

  if (d.kind === "switch") {
    if (cmd === "show" && (a[0] === "mac" || a[0] === "mac-table")) {
      const mt = rtOf(state).mac[d.id] ?? {};
      const rows = Object.entries(mt).map(([m, p]) => `${m}  ${p}`);
      return { out: rows.length ? `MAC-адрес          порт\n${rows.join("\n")}` : "Таблица MAC пуста — коммутатор ещё ничего не видел" };
    }
    if (cmd === "show" && a[0] === "ports")
      return {
        out: d.ifaces
          .map((i) => `${i.name}  ${i.up ? "up" : "down"}  ${i.trunk ? "trunk" : "access vlan " + (i.vlan ?? 1)}`)
          .join("\n"),
      };
    if (cmd === "port" && (a[1] === "vlan" || a[1] === "trunk" || a[1] === "access")) {
      const bad = NO(d);
      if (bad) return { out: bad };
      const i = getIface(d, a[0]);
      if (!i) return { out: `нет порта «${a[0]}»` };
      if (a[1] === "trunk") i.trunk = true;
      else {
        const v = a[1] === "vlan" ? Number(a[2]) : 1;
        if (!(v >= 1 && v <= 4094)) return { out: "VLAN — число от 1 до 4094" };
        i.trunk = false;
        i.vlan = v;
      }
      return { out: "", changed: true };
    }
    if (cmd === "port" && a.length === 2 && (a[1] === "up" || a[1] === "down")) {
      const bad = NO(d);
      if (bad) return { out: bad };
      return done(setUp(d, a[0], a[1] === "up"));
    }
    return {
      out: "Коммутатор: show mac — таблица MAC-адресов, show ports — состояние портов, port <порт> up|down, port <порт> vlan <номер>, port <порт> trunk. IP-адресов у него нет.",
    };
  }

  if (cmd === "ip") {
    const [obj, verb, ...r] = a;
    if (obj === "addr" || obj === "address" || obj === "a") {
      if (!verb || verb === "show") return { out: showAddr(d) };
      const bad = NO(d);
      if (bad) return { out: bad };
      const dev = r[r.indexOf("dev") + 1];
      if (verb === "add") return done(setAddr(d, dev, r[0]));
      if (verb === "flush") return done(clearAddr(d, r[r.indexOf("dev") + 1] ?? r[0]));
      if (verb === "del") return done(clearAddr(d, dev));
    }
    if (obj === "link" || obj === "l") {
      if (!verb || verb === "show") return { out: showAddr(d) };
      const bad = NO(d);
      if (bad) return { out: bad };
      if (verb === "set") {
        const mt = r.indexOf("mtu");
        if (mt >= 0) {
          const bad = NO(d);
          if (bad) return { out: bad };
          const i = getIface(d, r[0]);
          const v = Number(r[mt + 1]);
          if (!i || !(v >= 68 && v <= 9000)) return { out: "Error: ip link set <if> mtu <68..9000>" };
          i.mtu = v;
          return { out: "", changed: true };
        }
        const k = r.indexOf("txqueuelen");
        if (k >= 0) {
          const i = getIface(d, r[0]);
          const v = Number(r[k + 1]);
          if (!i || !(v >= 1 && v <= 10000)) return { out: "Error: ip link set <if> txqueuelen <1..10000>" };
          i.txqueuelen = v;
          return { out: "", changed: true };
        }
        return done(setUp(d, r[0], r[1] === "up"));
      }
    }
    if (obj === "route" || obj === "r") {
      if (!verb || verb === "show")
        return { out: routeTable(d).map((x) => routeLine(x, d)).join("\n") || "(таблица маршрутов пуста)" };
      if (verb === "get") {
        const dst = parseIp(r[0] ?? "");
        if (dst === null) return { out: `Error: неверный адрес` };
        const rt = lookup(d, dst);
        if (!rt) return { out: "RTNETLINK answers: Network is unreachable" };
        const src = ifaceOf(d, rt.dev).ip;
        return { out: `${r[0]} ${rt.via ? "via " + ipStr(rt.via) + " " : ""}dev ${rt.dev} src ${src}` };
      }
      const bad = NO(d);
      if (bad) return { out: bad };
      if (verb === "add") {
        const dst = r[0];
        const via = r[r.indexOf("via") + 1];
        const dev = r[r.indexOf("dev") + 1];
        return done(addRoute(d, dst, r.includes("via") ? via : null, r.includes("dev") ? dev : null));
      }
      if (verb === "del") return done(delRoute(d, r[0]));
    }
    if (obj === "neigh" || obj === "n") return arp(state, d);
    return { out: "ip: неизвестная команда. Введите «help»." };
  }
  if (cmd === "dig") return doDig(state, d, a, "dig");
  if (cmd === "nslookup" || cmd === "host") return doDig(state, d, cmd === "host" ? a : a, "nslookup");
  if (cmd === "dns") return dnsAdmin(d, a);
  if (cmd === "web") return webAdmin(d, a);
  if (cmd === "ssh" || cmd === "ssh-keygen" || cmd === "ssh-copy-id") return sshClient(state, d, cmd, a);
  if (cmd === "sshd") return sshdAdmin(d, a);
  if (cmd === "vpn") return vpnAdmin(d, a);
  if (cmd === "lb") return lbAdmin(d, a);
  if (cmd === "rproxy") return rproxyAdmin(d, a);
  if (cmd === "proxy") return proxyAdmin(d, a);
  if (cmd === "close") {
    const bad = NO(d);
    if (bad) return { out: bad };
    const n = d.services.length;
    d.services = d.services.filter((x) => !(x.proto === a[0] && x.port === Number(a[1])));
    return d.services.length < n ? { out: `${a[0]}/${a[1]} закрыт`, changed: true } : { out: "close <tcp|udp> <порт>: такого слушающего порта нет" };
  }
  if (cmd === "tcpdump") {
    backgroundTraffic(state);
    const i = a.indexOf("-i");
    const iface = i >= 0 ? a[i + 1] : (d.ifaces[0]?.name ?? "");
    if (iface !== "any" && !getIface(d, iface)) return { out: `tcpdump: нет интерфейса «${iface}» (есть: ${d.ifaces.map((x) => x.name).join(", ")}, any)` };
    const c = a.indexOf("-c");
    const count = c >= 0 ? Number(a[c + 1]) || 20 : 20;
    const filters = a.filter((x, k) => x !== "-i" && x !== "-c" && k !== i + 1 && k !== c + 1 && !x.startsWith("-") && x !== "and");
    const lines = captureLines(state, d.id, iface, filters, count);
    return { out: lines.length ? `tcpdump: listening on ${iface}\n${lines.join("\n")}\n${lines.length} packets captured` : `tcpdump: listening on ${iface}\n(перехваченных пакетов нет — сначала пустите трафик: ping, curl)` };
  }
  if (cmd === "listen") {
    const bad = NO(d);
    if (bad) return { out: bad };
    const [proto, port, addr] = a;
    const s = d.services.find((x) => x.proto === proto && x.port === Number(port));
    if (!s) return { out: `listen <tcp|udp> <порт> <адрес>: на ${proto}/${port} ничего не слушает` };
    if (addr !== "0.0.0.0" && addr !== "127.0.0.1" && parseIp(addr ?? "") === null) return { out: "адрес: 0.0.0.0 (везде), 127.0.0.1 (только локально) или адрес интерфейса" };
    s.bind = addr;
    return { out: `${proto}/${port} теперь слушает ${addr}`, changed: true };
  }
  if (cmd === "tls") return tlsAdmin(state, d, a);
  if (cmd === "trust") return trustAdmin(state, d, a);
  if (cmd === "openssl") {
    const k = a.indexOf("-connect");
    const target = a[k + 1] ?? "";
    const [host, port] = target.split(":");
    if (a[0] !== "s_client" || k < 0 || !host) return { out: "openssl s_client -connect www.example.org:443 [-servername имя]" };
    const sn = a.indexOf("-servername");
    const res = toIp(state, d, host);
    if (res.err !== undefined) return { out: `openssl: ${host}: ${res.err}` };
    const r = sClient(state, d, sn >= 0 ? a[sn + 1] : host, res.ip, Number(port ?? 443));
    return { out: r.out, probe: r.run };
  }
  if (cmd === "pageload") {
    const m = /^(https?):\/\/([\w.-]+)/i.exec(a[0] ?? "");
    if (!m) return { out: "pageload https://www.example.org/ — измерить загрузку страницы" };
    const res = toIp(state, d, m[2]);
    if (res.err !== undefined) return { out: `pageload: ${m[2]}: ${res.err}` };
    return { out: fmtPage(pageload(state, d, { dstIp: res.ip, https: m[1].toLowerCase() === "https" })) };
  }
  if (cmd === "cat") {
    if (a[0] === "/etc/resolv.conf") return { out: d.resolver ? `nameserver ${d.resolver}` : "(файл пуст — DNS-сервер не задан)" };
    if (a[0] === "/etc/hosts") return { out: ["127.0.0.1 localhost", ...Object.entries(d.hosts ?? {}).map(([n, ip]) => `${ip} ${n}`)].join("\n") };
    return { out: `cat: ${a[0] ?? ""}: нет такого файла (доступны /etc/resolv.conf и /etc/hosts)` };
  }
  if (cmd === "arp") {
    if (a[0] === "-s") {
      const bad = NO(d);
      if (bad) return { out: bad };
      if (parseIp(a[1] ?? "") === null || !/^([0-9a-f]{2}:){5}[0-9a-f]{2}$/i.test(a[2] ?? "")) return { out: "arp -s <ip> <mac в виде 28:28:00:00:00:01>" };
      (d.arpStatic ??= {})[a[1]] = a[2].toLowerCase();
      const arpKey = parseIp(a[1]);
      if (arpKey !== null && state.rt?.arp?.[d.id]) delete state.rt.arp[d.id][arpKey];
      return { out: `статическая запись ARP: ${a[1]} = ${a[2]}`, changed: true };
    }
    if (a[0] === "-d") {
      if (d.arpStatic) delete d.arpStatic[a[1]];
      return { out: "статическая запись удалена", changed: true };
    }
    return arp(state, d);
  }
  if (cmd === "ping") return doPing(state, d, a);
  if (cmd === "traceroute" || cmd === "tracepath") return doTraceroute(state, d, a);
  if (cmd === "curl") return doCurl(state, d, a);
  if (cmd === "nc") {
    const udp = a.includes("-u");
    const flags = a.filter((x) => x.startsWith("-"));
    const rest = a.filter((x) => !x.startsWith("-"));
    if (flags.some((f) => /^-.*l/.test(f) && f !== "-u")) {
      const bad = NO(d);
      if (bad) return { out: bad };
      const port = Number(rest[0]);
      if (!port) return { out: "nc: укажите порт: nc -l 8080 (или nc -u -l 5000 для UDP)" };
      const proto = udp ? "udp" : "tcp";
      if (!d.services.some((s) => s.port === port && s.proto === proto)) d.services.push({ proto, port });
      return { out: `слушаю ${proto}-порт ${port}`, changed: true };
    }
    if (udp) return doUdp(state, d, rest[0] ?? "", Number(rest[1]));
    return doConnect(state, d, rest[0] ?? "", Number(rest[1]), "nc");
  }
  if (cmd === "iperf3" || cmd === "iperf") {
    const ip = a.find((x) => parseIp(x) !== null);
    if (!ip) return { out: "iperf3: укажите адрес сервера: iperf3 10.0.0.5 [-n МБ]" };
    const k = a.indexOf("-n");
    const mb = k >= 0 ? Number(a[k + 1]) || 50 : 50;
    const dst = parseIp(ip);
    if (dst === null || !lookup(d, dst)) return { out: "iperf3: Network is unreachable" };
    const r = transfer(state, d.id, dst, { bytes: mb * 1e6 });
    return { out: r.ok ? r.text : `iperf3: ${r.text}`, chart: r.chart, xfer: r };
  }
  if (cmd === "ss" || cmd === "netstat")
    return {
      out: d.services.length
        ? d.services.map((s) => `${s.proto}  LISTEN  ${s.bind ?? "0.0.0.0"}:${s.port}`).join("\n")
        : "(слушающих портов нет)",
    };
  if (cmd === "sysctl" || cmd === "echo") {
    const text = a.join(" ");
    const mem = /tcp_rmem\s*=?\s*"?([\d\s,]+)"?/.exec(text);
    if (mem) {
      const nums = mem[1].split(/[\s,]+/).filter(Boolean).map(Number);
      if (!/=/.test(text)) return { out: `net.ipv4.tcp_rmem = 4096 ${(d.rwnd ?? 64) * 1024} ${(d.rwnd ?? 64) * 1024}` };
      const bad = NO(d);
      if (bad) return { out: bad };
      const maxB = nums[nums.length - 1];
      if (!(maxB >= 4096)) return { out: "sysctl: максимальный размер буфера должен быть не меньше 4096 байт" };
      d.rwnd = Math.round(maxB / 1024);
      return { out: `net.ipv4.tcp_rmem = 4096 ${nums.length > 2 ? nums[1] : maxB} ${maxB}  (окно приёма до ${d.rwnd} КБ)`, changed: true };
    }
    if (/tcp_syncookies/.test(text)) {
      const m = /=\s*([01])/.exec(text);
      if (!m) return { out: `net.ipv4.tcp_syncookies = ${d.syncookies ? 1 : 0}` };
      const bad = NO(d);
      if (bad) return { out: bad };
      d.syncookies = m[1] === "1";
      return { out: `net.ipv4.tcp_syncookies = ${m[1]}`, changed: true };
    }
    if (/tcp_congestion_control/.test(text)) {
      const m = /=\s*(\w+)/.exec(text);
      if (!m) return { out: `net.ipv4.tcp_congestion_control = ${d.cc ?? "cubic"}` };
      const bad = NO(d);
      if (bad) return { out: bad };
      if (!["reno", "cubic", "bbr"].includes(m[1])) return { out: "sysctl: доступны reno, cubic, bbr" };
      d.cc = m[1];
      return { out: `net.ipv4.tcp_congestion_control = ${m[1]}`, changed: true };
    }
    if (!/ip_forward/.test(text)) {
      if (cmd === "echo") return { out: text };
      return { out: "sysctl: поддерживаются net.ipv4.ip_forward, net.ipv4.tcp_rmem, net.ipv4.tcp_congestion_control" };
    }
    const val = /=\s*([01])/.exec(text)?.[1] ?? /^([01])\s*>/.exec(text)?.[1];
    if (val === undefined) return { out: `net.ipv4.ip_forward = ${d.forward ? 1 : 0}` };
    const bad = NO(d);
    if (bad) return { out: bad };
    d.forward = val === "1";
    return { out: `net.ipv4.ip_forward = ${val}`, changed: true };
  }
  if (cmd === "iptables" || cmd === "sudo") {
    const t = cmd === "sudo" ? a.slice(1) : a;
    if (cmd === "sudo" && a[0] !== "iptables") return exec(state, devId, a.join(" "));
    return iptables(d, t);
  }
  return { out: `${cmd}: команда не найдена. Введите «help».` };
}

function arp(state: NetState, d: Device): CmdResult {
  const c = rtOf(state).arp[d.id] ?? {};
  const rows = [
    ...Object.entries(d.arpStatic ?? {}).map(([ip, mac]) => `${ip}  ${mac}  (статическая)`),
    ...Object.entries(c).filter(([ip]) => !d.arpStatic?.[ipStr(Number(ip))]).map(([ip, e]) => `${ipStr(Number(ip))}  ${e.mac}`),
  ];
  return { out: rows.length ? rows.join("\n") : "(кэш ARP пуст — пока ни с кем не говорили)" };
}

export { cidrStr };
