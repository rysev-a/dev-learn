//! HTTP/1.1 в симуляторе: веб-сервер — набор маршрутов (путь → статус, тело, заголовки, редирект), клиент — curl.
//! Сетевая часть (DNS, TCP-сессия с рукопожатием) идёт через настоящую симуляцию, а разбор запроса и ответа
//! считается здесь.

use crate::ip::*;
use crate::sim::{delivered_to, fmt_ms, tcp1};
use crate::term::to_ip;
use crate::tls::tls_fetch;
use crate::types::*;
use crate::util::{js_num, to_int, utf16_len, OrdMap};

/// Пустая конфигурация веб-сервера.
pub fn new_http() -> HttpConfig {
    HttpConfig::default()
}

/// Пояснение к коду ответа.
pub fn reason(status: u32) -> &'static str {
    match status {
        200 => "OK",
        201 => "Created",
        204 => "No Content",
        301 => "Moved Permanently",
        302 => "Found",
        304 => "Not Modified",
        307 => "Temporary Redirect",
        308 => "Permanent Redirect",
        400 => "Bad Request",
        401 => "Unauthorized",
        403 => "Forbidden",
        404 => "Not Found",
        405 => "Method Not Allowed",
        429 => "Too Many Requests",
        500 => "Internal Server Error",
        502 => "Bad Gateway",
        503 => "Service Unavailable",
        _ => "",
    }
}

/// Запрос к веб-серверу.
#[derive(Clone, Debug, Default)]
pub struct HttpRequest {
    pub method: String,
    pub path: String,
    pub host: Option<String>,
    pub headers: OrdMap<String>,
}

/// Разобранный адрес.
#[derive(Clone, Debug, PartialEq)]
pub struct ParsedUrl {
    pub scheme: String,
    pub host: String,
    pub port: i64,
    pub path: String,
}

fn response(status: u32, headers: OrdMap<String>, body: String) -> HttpResponse {
    HttpResponse { status, reason: reason(status).to_string(), headers, body, rtt_us: None, ip: None, via: None, url: None }
}

/// Ответ веб-сервера на запрос.
pub fn respond(http: &HttpConfig, req: &HttpRequest) -> HttpResponse {
    let path = req.path.split('?').next().unwrap_or("");
    let Some(r) = http.routes.iter().find(|x| x.path == path) else {
        let body = "<h1>404 Not Found</h1>".to_string();
        let mut h = OrdMap::new();
        h.insert("server", "nginx".to_string());
        h.insert("content-type", "text/html".to_string());
        h.insert("content-length", utf16_len(&body).to_string());
        return response(404, h, body);
    };
    let mut status = r.status.unwrap_or(200);
    let mut body = match &r.body {
        Some(b) => b.clone(),
        None => {
            if (300..400).contains(&status) {
                String::new()
            } else {
                format!("<h1>{path}</h1>")
            }
        }
    };
    let mut headers = OrdMap::new();
    headers.insert("server", "nginx".to_string());
    headers.insert("content-type", r.typ.clone().unwrap_or_else(|| "text/html".into()));
    for (k, v) in r.headers.iter() {
        headers.insert(k.to_lowercase(), v.clone());
    }
    if let Some(l) = r.location.as_ref().filter(|l| !l.is_empty()) {
        headers.insert("location", l.clone());
    }
    if let Some(e) = r.etag.as_ref().filter(|e| !e.is_empty()) {
        headers.insert("etag", e.clone());
        if req.headers.get("if-none-match") == Some(e) {
            status = 304;
            body = String::new();
        }
    }
    if req.method == "HEAD" {
        body = String::new();
    }
    headers.insert("content-length", utf16_len(&body).to_string());
    response(status, headers, body)
}

/// Разбор адреса `http(s)://хост[:порт][/путь][?запрос]`.
pub fn parse_url(u: &str) -> Option<ParsedUrl> {
    let lower = u.to_lowercase();
    let (scheme, rest) = if lower.starts_with("https://") {
        ("https", u.get(8..).unwrap_or(""))
    } else if lower.starts_with("http://") {
        ("http", u.get(7..).unwrap_or(""))
    } else {
        return None;
    };
    // хост: всё до первого «/», «:», «?», «#»
    let host_end = rest.find(['/', ':', '?', '#']).unwrap_or(rest.len());
    let host = &rest[..host_end];
    if host.is_empty() {
        return None;
    }
    let mut tail = &rest[host_end..];
    let mut port: Option<i64> = None;
    if let Some(after) = tail.strip_prefix(':') {
        let digits: String = after.chars().take_while(|c| c.is_ascii_digit()).collect();
        if digits.is_empty() {
            return None;
        }
        port = digits.parse().ok();
        tail = &after[digits.len()..];
    }
    // путь [^?#]*, затем запрос [^#]*, затем конец
    let path_end = tail.find(['?', '#']).unwrap_or(tail.len());
    let path = &tail[..path_end];
    if !path.is_empty() && !path.starts_with('/') {
        return None;
    }
    let mut after = &tail[path_end..];
    let mut query = "";
    if after.starts_with('?') {
        let q_end = after.find('#').unwrap_or(after.len());
        query = &after[..q_end];
        after = &after[q_end..];
    }
    if !after.is_empty() {
        return None;
    }
    let path = if path.is_empty() { "/" } else { path };
    Some(ParsedUrl {
        scheme: scheme.into(),
        host: host.to_lowercase(),
        port: port.unwrap_or(if scheme == "https" { 443 } else { 80 }),
        path: format!("{path}{query}"),
    })
}

/// Параметры запроса с редиректами.
#[derive(Clone, Debug, Default)]
pub struct FetchOptions {
    pub url: String,
    pub method: String,
    pub follow: bool,
    pub headers: OrdMap<String>,
    pub proxy: Option<String>,
}

/// Итог: цепочка ответов, ошибка и последняя сетевая проба.
#[derive(Clone, Debug, Default)]
pub struct FetchResult {
    pub responses: Vec<HttpResponse>,
    pub error: Option<String>,
    pub run: Option<ProbeRun>,
}

/// Запрос с редиректами (до шести переходов).
pub fn http_fetch(state: &mut NetState, dev_id: &str, o: &FetchOptions) -> FetchResult {
    let mut responses: Vec<HttpResponse> = Vec::new();
    let mut cur = o.url.clone();
    let mut run: Option<ProbeRun> = None;
    for _hop in 0..6 {
        let Some(u) = parse_url(&cur) else {
            return FetchResult { responses, error: Some(format!("curl: (3) неверный адрес «{cur}»")), run };
        };
        if let Some(proxy) = &o.proxy {
            let px = via_proxy(state, dev_id, &u, proxy, &o.method, &o.headers);
            if px.run.is_some() {
                run = px.run.clone();
            }
            match (&px.error, &px.response) {
                (None, Some(resp)) => {
                    let mut r = resp.clone();
                    r.url = Some(cur.clone());
                    r.ip = px.ip;
                    responses.push(r);
                }
                _ => return FetchResult { responses, error: Some(px.error.unwrap_or_else(|| "proxy: нет ответа".into())), run },
            }
            break;
        }
        let res = match to_ip(state, dev_id, &u.host) {
            Ok(r) => r,
            Err(e) => {
                return FetchResult {
                    responses,
                    error: Some(format!("curl: (6) Could not resolve host: {} — {}", u.host, e.err)),
                    run: e.run.or(run),
                };
            }
        };
        if u.scheme == "https" {
            let t = tls_fetch(state, dev_id, &u, res.ip, &o.method, &o.headers);
            if t.run.is_some() {
                run = t.run.clone();
            }
            match (&t.error, &t.response) {
                (None, Some(resp)) => {
                    let mut r = resp.clone();
                    r.url = Some(cur.clone());
                    r.ip = Some(res.ip);
                    r.via = t.via.clone();
                    responses.push(r);
                }
                _ => return FetchResult { responses, error: Some(t.error.unwrap_or_else(|| "curl: (35) SSL connect error".into())), run },
            }
        } else {
            let mut r = tcp1(state, dev_id, res.ip, u.port, 50000, true);
            if r.status == ProbeStatus::Refused {
                return FetchResult {
                    responses,
                    error: Some(format!("curl: (7) Failed to connect to {} port {}: Connection refused", u.host, u.port)),
                    run: Some(r),
                };
            }
            if r.status != ProbeStatus::Connected {
                return FetchResult {
                    responses,
                    error: Some(format!("curl: (28) Connection timed out — {}:{} не отвечает", u.host, u.port)),
                    run: Some(r),
                };
            }
            let dev = delivered_to(state, &r, Some(res.ip));
            let rtt = r.rtt_us.unwrap_or(0.0);
            if let Some(dev) = dev.as_ref().filter(|d| d.rproxy.is_some()) {
                let rp = rproxy_handle(state, dev, &u, &o.method, &o.headers, &r);
                let cache = rp.headers.get("x-cache").filter(|c| !c.is_empty()).map(|c| format!(" (кэш: {c})")).unwrap_or_default();
                r.events.push(NetEvent {
                    t: rtt + 40.0,
                    dev: dev.id.clone(),
                    kind: EventKind::Http,
                    text: format!("{} {} → {} {}{}", o.method, u.path, rp.status, rp.reason, cache),
                });
                let mut out = rp;
                out.url = Some(cur.clone());
                out.ip = Some(res.ip);
                run = Some(r);
                responses.push(out);
            } else {
                let Some(http) = dev.as_ref().and_then(|d| d.http.as_ref()) else {
                    return FetchResult {
                        responses,
                        error: Some("curl: (52) Empty reply from server — на порту нет веб-сервера".into()),
                        run: Some(r),
                    };
                };
                let resp = respond(
                    http,
                    &HttpRequest { method: o.method.clone(), path: u.path.clone(), host: Some(u.host.clone()), headers: o.headers.clone() },
                );
                let dev_id_out = dev.as_ref().map(|d| d.id.clone()).unwrap_or_default();
                r.events.push(NetEvent {
                    t: rtt + 40.0,
                    dev: dev_id_out,
                    kind: EventKind::Http,
                    text: format!("{} {} → {} {}", o.method, u.path, resp.status, resp.reason),
                });
                let mut out = resp;
                out.url = Some(cur.clone());
                out.ip = Some(res.ip);
                out.rtt_us = Some(rtt * 2.0);
                run = Some(r);
                responses.push(out);
            }
        }
        let Some(last) = responses.last() else { break };
        let loc = last.headers.get("location").cloned().filter(|l| !l.is_empty());
        if o.follow && [301, 302, 307, 308].contains(&last.status) {
            if let Some(loc) = loc {
                let lower = loc.to_lowercase();
                cur = if lower.starts_with("http://") || lower.starts_with("https://") {
                    loc
                } else {
                    let default_port = if u.scheme == "https" { 443 } else { 80 };
                    let port = if u.port != default_port { format!(":{}", u.port) } else { String::new() };
                    let slash = if loc.starts_with('/') { loc.clone() } else { format!("/{loc}") };
                    format!("{}://{}{}{}", u.scheme, u.host, port, slash)
                };
                continue;
            }
        }
        break;
    }
    FetchResult { responses, error: None, run }
}

/// Обратный прокси / CDN-узел: маршрутизация по хосту и пути, кэш.
fn rproxy_handle(
    state: &mut NetState,
    dev: &Device,
    u: &ParsedUrl,
    method: &str,
    headers: &OrdMap<String>,
    run: &ProbeRun,
) -> HttpResponse {
    let Some(rp) = dev.rproxy.as_ref() else { return response(502, OrdMap::new(), String::new()) };
    let path_of = |r: &RProxyRule| r.path.clone().unwrap_or_else(|| "/".into());
    let mut rules: Vec<&RProxyRule> = rp.rules.iter().collect();
    rules.sort_by_key(|r| std::cmp::Reverse(utf16_len(&path_of(r))));
    let rule = rules.into_iter().find(|r| {
        let host_ok = r.host.as_deref().map(|h| h.is_empty() || h == "*" || h == u.host).unwrap_or(true);
        host_ok && u.path.starts_with(&path_of(r))
    });
    let base = run.rtt_us.unwrap_or(0.0) * 2.0;
    let bad = |status: u32, body: &str| {
        let mut h = OrdMap::new();
        h.insert("server", "nginx".to_string());
        h.insert("content-length", utf16_len(body).to_string());
        let mut r = response(status, h, body.to_string());
        r.rtt_us = Some(base);
        r
    };
    let Some(rule) = rule.cloned() else { return bad(404, "no route") };
    let key = format!("{}{}", u.host, u.path);
    if rule.cache {
        if let Some(hit) = state.rt.rpcache.get(&dev.id).and_then(|m| m.get(&key)).cloned() {
            let mut h = hit.headers.clone();
            h.insert("x-cache", "HIT".to_string());
            h.insert("age", "5".to_string());
            return HttpResponse { headers: h, rtt_us: Some(base), ..hit };
        }
    }
    let mut parts = rule.backend.split(':');
    let bip = parts.next().unwrap_or("");
    let bport = parts.next();
    let bip_n = parse_ip(bip).unwrap_or(0);
    let port = match bport {
        Some(p) => to_int(js_num(p)),
        None => 80,
    };
    let up = tcp1(state, &dev.id, bip_n, port, 50000, true);
    if up.status != ProbeStatus::Connected {
        let why = if up.status == ProbeStatus::Refused { "порт закрыт" } else { "нет ответа" };
        return bad(502, &format!("прокси: сервер {} недоступен ({why})", rule.backend));
    }
    let site = delivered_to(state, &up, Some(bip_n));
    let Some(http) = site.as_ref().and_then(|s| s.http.as_ref()) else { return bad(502, "пустой ответ сервера") };
    let resp = respond(
        http,
        &HttpRequest { method: method.to_string(), path: u.path.clone(), host: Some(u.host.clone()), headers: headers.clone() },
    );
    let mut h = resp.headers.clone();
    h.insert("via", "1.1 reverse-proxy".to_string());
    if rule.cache {
        h.insert("x-cache", "MISS".to_string());
    }
    let out = HttpResponse { headers: h, rtt_us: Some(base + up.rtt_us.unwrap_or(0.0) * 2.0), ..resp.clone() };
    if rule.cache && resp.status == 200 {
        state.rt.rpcache.entry(dev.id.clone()).or_default().insert(key, out.clone());
    }
    out
}

#[derive(Default)]
struct ProxyResult {
    error: Option<String>,
    run: Option<ProbeRun>,
    response: Option<HttpResponse>,
    ip: Option<u32>,
}

/// Запрос через HTTP-прокси ip:порт: клиент → прокси (ACL) → сайт от имени прокси.
fn via_proxy(state: &mut NetState, dev_id: &str, u: &ParsedUrl, proxy: &str, method: &str, headers: &OrdMap<String>) -> ProxyResult {
    let mut parts = proxy.split(':');
    let pip = parts.next().unwrap_or("");
    let pport = parts.next();
    let pr = match to_ip(state, dev_id, pip) {
        Ok(r) => r,
        Err(_) => return ProxyResult { error: Some(format!("curl: (5) Could not resolve proxy: {pip}")), ..Default::default() },
    };
    let pport_n = match pport {
        Some(p) => to_int(js_num(p)),
        None => 3128,
    };
    let mut run = tcp1(state, dev_id, pr.ip, pport_n, 50000, true);
    if run.status == ProbeStatus::Refused {
        return ProxyResult {
            error: Some(format!("curl: (7) Failed to connect to proxy {proxy}: Connection refused")),
            run: Some(run),
            ..Default::default()
        };
    }
    if run.status != ProbeStatus::Connected {
        return ProxyResult {
            error: Some(format!("curl: (28) Connection timed out — прокси {proxy} не отвечает")),
            run: Some(run),
            ..Default::default()
        };
    }
    let pd = delivered_to(state, &run, Some(pr.ip));
    let Some(pd) = pd.filter(|d| d.proxy.is_some()) else {
        return ProxyResult {
            error: Some("curl: (56) на порту нет HTTP-прокси".into()), run: Some(run), ..Default::default()
        };
    };
    let Some(pcfg) = pd.proxy.clone() else { return ProxyResult::default() };
    let rtt = run.rtt_us.unwrap_or(0.0);
    let off = rtt / 2.0;
    let note = |run: &mut ProbeRun, t: f64, text: String| {
        run.events.push(NetEvent { t: off + t, dev: pd.id.clone(), kind: EventKind::Http, text })
    };
    let mk = |status: u32, server_body: (&str, &str), rtt_us: f64| {
        let mut h = OrdMap::new();
        h.insert("server", "squid".to_string());
        if status == 403 {
            h.insert("content-length", utf16_len(server_body.1).to_string());
        }
        let mut r = response(status, h, server_body.1.to_string());
        r.reason = server_body.0.to_string();
        r.rtt_us = Some(rtt_us);
        r
    };
    if pcfg.deny.iter().any(|x| *x == u.host) {
        note(&mut run, 20.0, format!("прокси: {} запрещён политикой — 403", u.host));
        let r = mk(403, ("Forbidden", "Access denied by proxy policy"), rtt * 2.0);
        return ProxyResult { response: Some(r), run: Some(run), ip: Some(pr.ip), error: None };
    }
    let up = match to_ip(state, &pd.id, &u.host) {
        Ok(r) => r,
        Err(_) => {
            note(&mut run, 20.0, format!("прокси: не разрешил имя {} — 502", u.host));
            let r = mk(502, ("Bad Gateway", "proxy: cannot resolve"), rtt * 2.0);
            return ProxyResult { response: Some(r), run: Some(run), ip: Some(pr.ip), error: None };
        }
    };
    let up_run = tcp1(state, &pd.id, up.ip, u.port, 50000, true);
    for x in &up_run.hops {
        let mut h = x.clone();
        h.t0 += off;
        h.t1 += off;
        run.hops.push(h);
    }
    for x in &up_run.events {
        let mut e = x.clone();
        e.t += off;
        run.events.push(e);
    }
    if up_run.status != ProbeStatus::Connected {
        note(&mut run, 30.0, format!("прокси: сайт {} недоступен ({}) — 502", u.host, up_run.status.as_str()));
        let r = mk(502, ("Bad Gateway", "proxy: upstream failure"), rtt * 2.0);
        return ProxyResult { response: Some(r), run: Some(run), ip: Some(pr.ip), error: None };
    }
    let site = delivered_to(state, &up_run, Some(up.ip));
    let Some(http) = site.as_ref().and_then(|s| s.http.as_ref()) else {
        let r = mk(502, ("Bad Gateway", "proxy: empty reply"), rtt * 2.0);
        return ProxyResult { response: Some(r), run: Some(run), ip: Some(pr.ip), error: None };
    };
    let resp = respond(
        http,
        &HttpRequest { method: method.to_string(), path: u.path.clone(), host: Some(u.host.clone()), headers: headers.clone() },
    );
    note(&mut run, up_run.rtt_us.unwrap_or(0.0) + 60.0, format!("прокси: {} {}{} → {}", method, u.host, u.path, resp.status));
    let mut h = resp.headers.clone();
    h.insert("via", "1.1 proxy".to_string());
    let out = HttpResponse { headers: h, rtt_us: Some(rtt * 2.0 + up_run.rtt_us.unwrap_or(0.0) * 2.0), ..resp };
    ProxyResult { response: Some(out), run: Some(run), ip: Some(pr.ip), error: None }
}

/// Вывод curl: обычный, с заголовками (-I) или подробный (-v).
pub fn fmt_curl(r: &FetchResult, verbose: bool, head: bool, method: &str) -> String {
    if let Some(e) = &r.error {
        return e.clone();
    }
    let mut out: Vec<String> = Vec::new();
    for x in &r.responses {
        let Some(u) = parse_url(x.url.as_deref().unwrap_or("")) else { continue };
        if verbose {
            let via = x.via.as_ref().map(|v| format!(" — {v}")).unwrap_or_default();
            out.push(format!("* подключено к {} ({}) порт {}{}", u.host, ip_str_opt(x.ip), u.port, via));
            out.push(format!("> {} {} HTTP/1.1", method, u.path));
            out.push(format!("> Host: {}", u.host));
            out.push("> Accept: */*".into());
            out.push(">".into());
        }
        if verbose || head {
            out.push(format!("< HTTP/1.1 {} {}", x.status, x.reason));
            for (k, v) in x.headers.iter() {
                out.push(format!("< {k}: {v}"));
            }
            out.push("<".into());
        }
        if !head && !x.body.is_empty() {
            out.push(x.body.clone());
        }
        if verbose {
            if let Some(rtt) = x.rtt_us.filter(|r| *r != 0.0) {
                out.push(format!("* ответ получен за {}", fmt_ms(Some(rtt))));
            }
        }
    }
    out.join("\n")
}
