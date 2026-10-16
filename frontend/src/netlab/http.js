/* HTTP/1.1 в симуляторе: веб-сервер — набор маршрутов (путь → статус, тело, заголовки, редирект),
   клиент — curl. Сетевая часть (DNS, TCP-сессия с рукопожатием) идёт через настоящую симуляцию,
   а разбор запроса и ответа считается здесь. */
import { ipStr, parseIp } from "./ip.js";
import { fmtMs, tcp1 } from "./sim.js";
import { tlsFetch as realTls } from "./tls.js";

export const newHttp = (extra = {}) => ({ routes: [], ...extra });

export const REASONS = {
  200: "OK",
  201: "Created",
  204: "No Content",
  301: "Moved Permanently",
  302: "Found",
  304: "Not Modified",
  307: "Temporary Redirect",
  308: "Permanent Redirect",
  400: "Bad Request",
  401: "Unauthorized",
  403: "Forbidden",
  404: "Not Found",
  405: "Method Not Allowed",
  429: "Too Many Requests",
  500: "Internal Server Error",
  502: "Bad Gateway",
  503: "Service Unavailable",
};

/** ответ веб-сервера (конфиг http) на запрос {method, path, host, headers} */
export function respond(http, req) {
  const path = req.path.split("?")[0];
  const r = http.routes.find((x) => x.path === path);
  if (!r) {
    const body = "<h1>404 Not Found</h1>";
    return { status: 404, reason: REASONS[404], headers: { server: "nginx", "content-type": "text/html", "content-length": String(body.length) }, body };
  }
  let status = r.status ?? 200;
  let body = r.body ?? (status >= 300 && status < 400 ? "" : `<h1>${path}</h1>`);
  const headers = { server: "nginx", "content-type": r.type ?? "text/html", ...Object.fromEntries(Object.entries(r.headers ?? {}).map(([k, v]) => [k.toLowerCase(), v])) };
  if (r.location) headers.location = r.location;
  if (r.etag) {
    headers.etag = r.etag;
    if (req.headers?.["if-none-match"] === r.etag) {
      status = 304;
      body = "";
    }
  }
  if (req.method === "HEAD") body = "";
  headers["content-length"] = String(body.length);
  return { status, reason: REASONS[status] ?? "", headers, body };
}

const URL_RE = /^(https?):\/\/([^/:?#]+)(?::(\d+))?(\/[^?#]*)?(\?[^#]*)?$/i;

export function parseUrl(u) {
  const m = URL_RE.exec(u);
  if (!m) return null;
  const scheme = m[1].toLowerCase();
  return { scheme, host: m[2].toLowerCase(), port: Number(m[3] ?? (scheme === "https" ? 443 : 80)), path: (m[4] ?? "/") + (m[5] ?? "") };
}

/** запрос с редиректами: возвращает {responses, error, run} (run — последняя сетевая проба) */
export function httpFetch(state, d, { url, method = "GET", follow = false, headers = {}, toIp, proxy = null }) {
  const responses = [];
  let cur = url;
  let run = null;
  for (let hop = 0; hop < 6; hop++) {
    const u = parseUrl(cur);
    if (!u) return { responses, error: `curl: (3) неверный адрес «${cur}»`, run };
    if (proxy) {
      const px = viaProxy(state, d, u, proxy, { method, headers, toIp });
      run = px.run ?? run;
      if (px.error) return { responses, error: px.error, run };
      responses.push({ url: cur, ...px.response, ip: px.ip });
      break;
    }
    const res = toIp(state, d, u.host);
    if (res.err) return { responses, error: `curl: (6) Could not resolve host: ${u.host} — ${res.err}`, run: res.run ?? run };
    if (u.scheme === "https") {
      const t = realTls(state, d, u, res.ip, { method, headers }, respond);
      run = t.run ?? run;
      if (t.error) return { responses, error: t.error, run };
      responses.push({ url: cur, ...t.response, ip: res.ip, via: t.via });
    } else {
      run = tcp1(state, d.id, res.ip, u.port, { session: true });
      if (run.status === "refused") return { responses, error: `curl: (7) Failed to connect to ${u.host} port ${u.port}: Connection refused`, run };
      if (run.status !== "connected") return { responses, error: `curl: (28) Connection timed out — ${u.host}:${u.port} не отвечает`, run };
      const dev = state.devices[run.delivered.find((x) => x.dst === res.ip)?.dev];
      if (dev?.rproxy) {
        const rp = rproxyHandle(state, dev, u, { method, headers }, run);
        run.events.push({ t: (run.rttUs ?? 0) + 40, dev: dev.id, kind: "http", text: `${method} ${u.path} → ${rp.status} ${rp.reason}${rp.headers["x-cache"] ? " (кэш: " + rp.headers["x-cache"] + ")" : ""}` });
        responses.push({ url: cur, ...rp, ip: res.ip });
      } else {
        if (!dev?.http) return { responses, error: "curl: (52) Empty reply from server — на порту нет веб-сервера", run };
        const resp = respond(dev.http, { method, path: u.path, host: u.host, headers });
        run.events.push({ t: (run.rttUs ?? 0) + 40, dev: dev.id, kind: "http", text: `${method} ${u.path} → ${resp.status} ${resp.reason}` });
        responses.push({ url: cur, ...resp, ip: res.ip, rttUs: (run.rttUs ?? 0) * 2 });
      }
    }
    const last = responses[responses.length - 1];
    if (follow && [301, 302, 307, 308].includes(last.status) && last.headers.location) {
      const loc = last.headers.location;
      cur = /^https?:\/\//i.test(loc) ? loc : `${u.scheme}://${u.host}${u.port !== (u.scheme === "https" ? 443 : 80) ? ":" + u.port : ""}${loc.startsWith("/") ? loc : "/" + loc}`;
      continue;
    }
    break;
  }
  return { responses, error: null, run };
}

/** обратный прокси / CDN-узел: маршрутизация по хосту и пути, кэш */
function rproxyHandle(state, dev, u, { method, headers }, run) {
  const rules = [...dev.rproxy.rules].sort((a, b) => (b.path ?? "/").length - (a.path ?? "/").length);
  const rule = rules.find((r) => (!r.host || r.host === "*" || r.host === u.host) && u.path.startsWith(r.path ?? "/"));
  const base = (run.rttUs ?? 0) * 2;
  const bad = (status, body) => ({ status, reason: REASONS[status], headers: { server: "nginx", "content-length": String(body.length) }, body, rttUs: base });
  if (!rule) return bad(404, "no route");
  const key = `${u.host}${u.path}`;
  const cache = ((state.rt ??= { arp: {}, mac: {}, ct: {}, dnsCache: {} }).rpcache ??= {});
  const mine = (cache[dev.id] ??= {});
  if (rule.cache && mine[key]) return { ...mine[key], headers: { ...mine[key].headers, "x-cache": "HIT", age: "5" }, rttUs: base };
  const [bip, bport] = rule.backend.split(":");
  const up = tcp1(state, dev.id, parseIp(bip), Number(bport ?? 80), { session: true });
  if (up.status !== "connected") return bad(502, `прокси: сервер ${rule.backend} недоступен (${up.status === "refused" ? "порт закрыт" : "нет ответа"})`);
  const site = state.devices[up.delivered.find((x) => x.dst === parseIp(bip))?.dev];
  if (!site?.http) return bad(502, "пустой ответ сервера");
  const resp = respond(site.http, { method, path: u.path, host: u.host, headers });
  const out = { ...resp, headers: { ...resp.headers, via: "1.1 reverse-proxy", ...(rule.cache ? { "x-cache": "MISS" } : {}) }, rttUs: base + (up.rttUs ?? 0) * 2 };
  if (rule.cache && resp.status === 200) mine[key] = out;
  return out;
}

/** запрос через HTTP-прокси ip:port: клиент → прокси (ACL) → сайт от имени прокси */
function viaProxy(state, d, u, proxy, { method, headers, toIp }) {
  const [pip, pport] = proxy.split(":");
  const pr = toIp(state, d, pip);
  if (pr.err) return { error: `curl: (5) Could not resolve proxy: ${pip}` };
  const run = tcp1(state, d.id, pr.ip, Number(pport ?? 3128), { session: true });
  if (run.status === "refused") return { error: `curl: (7) Failed to connect to proxy ${proxy}: Connection refused`, run };
  if (run.status !== "connected") return { error: `curl: (28) Connection timed out — прокси ${proxy} не отвечает`, run };
  const pd = state.devices[run.delivered.find((x) => x.dst === pr.ip)?.dev];
  if (!pd?.proxy) return { error: "curl: (56) на порту нет HTTP-прокси", run };
  const off = (run.rttUs ?? 0) / 2;
  const note = (t, text) => run.events.push({ t: off + t, dev: pd.id, kind: "http", text });
  if (pd.proxy.deny.includes(u.host)) {
    note(20, `прокси: ${u.host} запрещён политикой — 403`);
    const body = "Access denied by proxy policy";
    return { response: { status: 403, reason: "Forbidden", headers: { server: "squid", "content-length": String(body.length) }, body, rttUs: (run.rttUs ?? 0) * 2 }, run, ip: pr.ip };
  }
  const up = toIp(state, pd, u.host);
  if (up.err) {
    note(20, `прокси: не разрешил имя ${u.host} — 502`);
    return { response: { status: 502, reason: "Bad Gateway", headers: { server: "squid" }, body: "proxy: cannot resolve", rttUs: (run.rttUs ?? 0) * 2 }, run, ip: pr.ip };
  }
  const upRun = tcp1(state, pd.id, up.ip, u.port, { session: true });
  for (const x of upRun.hops) run.hops.push({ ...x, t0: x.t0 + off, t1: x.t1 + off });
  for (const x of upRun.events) run.events.push({ ...x, t: x.t + off });
  if (upRun.status !== "connected") {
    note(30, `прокси: сайт ${u.host} недоступен (${upRun.status}) — 502`);
    return { response: { status: 502, reason: "Bad Gateway", headers: { server: "squid" }, body: "proxy: upstream failure", rttUs: (run.rttUs ?? 0) * 2 }, run, ip: pr.ip };
  }
  const site = state.devices[upRun.delivered.find((x) => x.dst === up.ip)?.dev];
  if (!site?.http) return { response: { status: 502, reason: "Bad Gateway", headers: { server: "squid" }, body: "proxy: empty reply", rttUs: (run.rttUs ?? 0) * 2 }, run, ip: pr.ip };
  const resp = respond(site.http, { method, path: u.path, host: u.host, headers });
  note((upRun.rttUs ?? 0) + 60, `прокси: ${method} ${u.host}${u.path} → ${resp.status}`);
  return { response: { ...resp, headers: { ...resp.headers, via: "1.1 proxy" }, rttUs: (run.rttUs ?? 0) * 2 + (upRun.rttUs ?? 0) * 2 }, run, ip: pr.ip };
}

export function fmtCurl(r, { verbose, head, method }) {
  if (r.error) return r.error;
  const out = [];
  for (const x of r.responses) {
    const u = parseUrl(x.url);
    if (verbose) {
      out.push(`* подключено к ${u.host} (${ipStr(x.ip)}) порт ${u.port}${x.via ? " — " + x.via : ""}`);
      out.push(`> ${method} ${u.path} HTTP/1.1`, `> Host: ${u.host}`, "> Accept: */*", ">");
    }
    if (verbose || head) {
      out.push(`< HTTP/1.1 ${x.status} ${x.reason}`);
      for (const [k, v] of Object.entries(x.headers)) out.push(`< ${k}: ${v}`);
      out.push("<");
    }
    if (!head && x.body) out.push(x.body);
    if (verbose && x.rttUs) out.push(`* ответ получен за ${fmtMs(x.rttUs)}`);
  }
  return out.join("\n");
}
