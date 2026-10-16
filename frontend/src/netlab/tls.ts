/* TLS/HTTPS в симуляторе: сертификат сервера (CN, SAN, издатель, срок), цепочка до доверенного корня,
   версии протокола, проверка клиентом и стоимость рукопожатия в кругах. «Сейчас» — фиксированная дата. */
import { ipStr } from "./ip.ts";
import { deliveredTo, fmtMs, tcp1 } from "./sim.ts";
import type { Device, HttpConfig, HttpRequest, HttpResponse, NetState, ParsedUrl, Pki, ProbeRun, TlsConfig } from "./types.ts";

export const NOW = "2026-10-16";
const DAY = 86400000;

export const DEFAULT_PKI: Pki = {
  cas: {
    PublicRootCA: { issuer: null },
    PublicIntCA: { issuer: "PublicRootCA" },
    CorpRootCA: { issuer: null },
    CorpIntCA: { issuer: "CorpRootCA" },
    ShadyRootCA: { issuer: null },
  },
};
export const DEFAULT_TRUST = ["PublicRootCA"];

export function newTls(extra: Partial<TlsConfig> = {}): TlsConfig {
  return {
    cert: { cn: "www.example.org", san: ["www.example.org"], issuer: "PublicIntCA", notAfter: "2027-01-15" },
    chain: ["PublicIntCA"],
    versions: ["1.2", "1.3"],
    ...extra,
  };
}

export const addDays = (n: number): string => new Date(Date.parse(NOW) + n * DAY).toISOString().slice(0, 10);

function nameMatches(pattern: string, host: string) {
  const p = pattern.toLowerCase();
  const h = host.toLowerCase();
  if (p === h) return true;
  if (p.startsWith("*.")) {
    const rest = p.slice(1); // .example.org
    return h.endsWith(rest) && !h.slice(0, -rest.length).includes(".") && h.length > rest.length;
  }
  return false;
}

/** проверка клиентом: {ok, error, curlCode, lines} */
export interface TlsVerdict {
  ok: boolean;
  version?: string | undefined;
  curlCode: number;
  error: string | null;
  lines: string[];
}

export function validate(state: NetState, client: Device, host: string, tls: TlsConfig): TlsVerdict {
  const cas = state.pki?.cas ?? DEFAULT_PKI.cas;
  const trust = client.trust ?? DEFAULT_TRUST;
  const minV = client.tlsMin ?? "1.2";
  const lines: string[] = [];
  const usable = (tls.versions ?? []).filter((v) => Number(v) >= Number(minV));
  if (!usable.length) {
    return { ok: false, curlCode: 35, error: `alert protocol version — сервер поддерживает только TLS ${tls.versions.join(", ")}, клиент требует не ниже ${minV}`, lines };
  }
  const version = usable.includes("1.3") ? "1.3" : usable[usable.length - 1];
  lines.push(`версия протокола: TLS ${version}`);
  const c = tls.cert;
  lines.push(`сертификат: CN=${c.cn}, SAN=${c.san.join(", ")}, издатель ${c.issuer}, действует до ${c.notAfter}`);
  if (Date.parse(c.notAfter) < Date.parse(NOW))
    return { ok: false, version, curlCode: 60, error: `SSL certificate problem: certificate has expired (до ${c.notAfter}, сегодня ${NOW})`, lines };
  if (!c.san.concat(c.cn).some((n: string) => nameMatches(n, host)))
    return { ok: false, version, curlCode: 60, error: `SSL: no alternative certificate subject name matches target host name '${host}' (в сертификате: ${c.san.join(", ")})`, lines };
  const sent = new Set(tls.chain ?? []);
  let cur = c.issuer;
  const path = [c.cn, cur];
  for (let i = 0; i < 6; i++) {
    if (trust.includes(cur)) {
      lines.push(`цепочка: ${path.join(" ← ")}  — корень ${cur} в хранилище доверия клиента`);
      return { ok: true, version, curlCode: 0, error: null, lines };
    }
    if (!cas[cur]) return { ok: false, version, curlCode: 60, error: `SSL certificate problem: unable to get local issuer certificate (неизвестный издатель ${cur})`, lines };
    const issuer = cas[cur]!.issuer;
    if (issuer === null)
      return { ok: false, version, curlCode: 60, error: `SSL certificate problem: self-signed certificate in certificate chain (корень ${cur} клиенту не доверен)`, lines };
    if (!sent.has(cur))
      return { ok: false, version, curlCode: 60, error: `SSL certificate problem: unable to get local issuer certificate (сервер не прислал промежуточный сертификат ${cur})`, lines };
    cur = issuer;
    path.push(cur);
  }
  return { ok: false, version, curlCode: 60, error: "слишком длинная цепочка", lines };
}

/** HTTPS-запрос: TCP-проба на 443 + проверка TLS + ответ веб-сервера (respond передаётся из http.js) */
export interface TlsFetchResult {
  error?: string;
  run?: ProbeRun;
  response?: HttpResponse;
  via?: string;
}

export function tlsFetch(
  state: NetState,
  d: Device,
  u: ParsedUrl,
  ip: number,
  { method, headers }: { method: string; headers: Record<string, string> },
  respond: (http: HttpConfig, req: HttpRequest) => HttpResponse,
): TlsFetchResult {
  const run = tcp1(state, d.id, ip, u.port, { session: true });
  if (run.status === "refused") return { error: `curl: (7) Failed to connect to ${u.host} port ${u.port}: Connection refused`, run };
  if (run.status !== "connected") return { error: `curl: (28) Connection timed out — ${u.host}:${u.port} не отвечает`, run };
  const dev = deliveredTo(state, run, ip);
  if (!dev?.tls) return { error: "curl: (35) SSL connect error — на порту нет TLS-сервера", run };
  const v = validate(state, d, u.host, dev.tls);
  const rtts = v.version === "1.2" ? 2 : 1;
  run.events.push({
    t: (run.rttUs ?? 0) + 30,
    dev: dev.id,
    kind: "tls",
    text: v.ok ? `TLS ${v.version}: рукопожатие за ${rtts} кр., сертификат принят` : `TLS: отказ — ${v.error}`,
  });
  if (!v.ok) return { error: `curl: (${v.curlCode}) ${v.error}`, run };
  if (!dev.http) return { error: "curl: (52) Empty reply from server", run };
  const resp = respond(dev.http, { method, path: u.path, host: u.host, headers });
  return {
    response: { ...resp, rttUs: (run.rttUs ?? 0) * (2 + rtts) },
    run,
    via: `TLS ${v.version}, рукопожатие ${rtts} кр. = ${fmtMs((run.rttUs ?? 0) * rtts)}`,
  };
}

/** openssl s_client: подробный вывод рукопожатия */
export function sClient(state: NetState, d: Device, host: string, ip: number, port = 443): { out: string; run: ProbeRun } {
  const run = tcp1(state, d.id, ip, port, { session: false });
  if (run.status !== "connected") return { out: `connect: ${run.status === "refused" ? "Connection refused" : "Connection timed out"}`, run };
  const dev = deliveredTo(state, run, ip);
  if (!dev?.tls) return { out: "openssl: на порту нет TLS", run };
  const v = validate(state, d, host, dev.tls);
  const out = [
    `CONNECTED(${ipStr(ip)}:${port})`,
    ...v.lines.map((l) => "  " + l),
    v.ok ? `Verification: OK` : `Verification error: ${v.error}`,
    v.version ? `Protocol: TLS ${v.version} (рукопожатие ${v.version === "1.2" ? 2 : 1} кр.)` : "",
  ].filter(Boolean);
  return { out: out.join("\n"), run };
}
