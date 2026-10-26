//! TLS/HTTPS в симуляторе: сертификат сервера (CN, SAN, издатель, срок), цепочка до доверенного корня,
//! версии протокола, проверка клиентом и стоимость рукопожатия в кругах. «Сейчас» — фиксированная дата.

use crate::http::ParsedUrl;
use crate::ip::*;
use crate::sim::{delivered_to, fmt_ms, tcp1};
use crate::types::*;
use crate::util::{js_num, OrdMap};

/// «Сегодня» для проверки срока сертификатов.
pub const NOW: &str = "2026-10-16";

/// Корневые и промежуточные центры сертификации по умолчанию.
pub fn default_pki() -> Pki {
    let mut cas = OrdMap::new();
    cas.insert("PublicRootCA", Ca { issuer: None });
    cas.insert("PublicIntCA", Ca { issuer: Some("PublicRootCA".into()) });
    cas.insert("CorpRootCA", Ca { issuer: None });
    cas.insert("CorpIntCA", Ca { issuer: Some("CorpRootCA".into()) });
    cas.insert("ShadyRootCA", Ca { issuer: None });
    Pki { cas }
}

/// Доверенные корни клиента по умолчанию.
pub fn default_trust() -> Vec<String> {
    vec!["PublicRootCA".to_string()]
}

/// Конфигурация TLS-сервера по умолчанию.
pub fn new_tls() -> TlsConfig {
    TlsConfig {
        cert: TlsCert {
            cn: "www.example.org".into(),
            san: vec!["www.example.org".into()],
            issuer: "PublicIntCA".into(),
            not_after: "2027-01-15".into(),
        },
        chain: vec!["PublicIntCA".into()],
        versions: vec!["1.2".into(), "1.3".into()],
    }
}

/// Дни от 1970-01-01 до гражданской даты (алгоритм Хиннанта).
fn days_from_civil(y: i64, m: i64, d: i64) -> i64 {
    let y = if m <= 2 { y - 1 } else { y };
    let era = if y >= 0 { y } else { y - 399 } / 400;
    let yoe = y - era * 400;
    let doy = (153 * (if m > 2 { m - 3 } else { m + 9 }) + 2) / 5 + d - 1;
    let doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    era * 146097 + doe - 719468
}

fn civil_from_days(z: i64) -> (i64, i64, i64) {
    let z = z + 719468;
    let era = if z >= 0 { z } else { z - 146096 } / 146097;
    let doe = z - era * 146097;
    let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    let y = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = doy - (153 * mp + 2) / 5 + 1;
    let m = if mp < 10 { mp + 3 } else { mp - 9 };
    (if m <= 2 { y + 1 } else { y }, m, d)
}

/// «ГГГГ-ММ-ДД» → число дней от начала эпохи; `None` для чего-то иного.
pub fn parse_date(s: &str) -> Option<i64> {
    let b = s.as_bytes();
    if b.len() != 10 || b[4] != b'-' || b[7] != b'-' {
        return None;
    }
    let y: i64 = s[0..4].parse().ok()?;
    let m: i64 = s[5..7].parse().ok()?;
    let d: i64 = s[8..10].parse().ok()?;
    if !(1..=12).contains(&m) || !(1..=31).contains(&d) {
        return None;
    }
    Some(days_from_civil(y, m, d))
}

/// Дата через `n` дней после «сегодня» в виде «ГГГГ-ММ-ДД».
pub fn add_days(n: f64) -> String {
    let now = parse_date(NOW).unwrap_or(0);
    let n = if n.is_finite() { n.clamp(-3_000_000.0, 3_000_000.0) } else { 0.0 };
    let (y, m, d) = civil_from_days((now as f64 + n).floor() as i64);
    format!("{y:04}-{m:02}-{d:02}")
}

fn name_matches(pattern: &str, host: &str) -> bool {
    let p = pattern.to_lowercase();
    let h = host.to_lowercase();
    if p == h {
        return true;
    }
    if p.starts_with("*.") {
        let rest = &p[1..]; // .example.org
        return h.ends_with(rest) && h.len() > rest.len() && !h[..h.len() - rest.len()].contains('.');
    }
    false
}

/// Итог проверки сертификата клиентом.
#[derive(Clone, Debug, PartialEq)]
pub struct TlsVerdict {
    pub ok: bool,
    pub version: Option<String>,
    pub curl_code: i32,
    pub error: Option<String>,
    pub lines: Vec<String>,
}

/// Проверка клиентом `client`: версии, срок, имя, цепочка до доверенного корня.
pub fn validate(state: &NetState, client: &Device, host: &str, tls: &TlsConfig) -> TlsVerdict {
    let default = default_pki();
    let cas = state.pki.as_ref().map(|p| &p.cas).unwrap_or(&default.cas);
    let trust = client.trust.clone().unwrap_or_else(default_trust);
    let min_v = client.tls_min.clone().unwrap_or_else(|| "1.2".into());
    let mut lines: Vec<String> = Vec::new();
    let usable: Vec<&String> = tls.versions.iter().filter(|v| js_num(v) >= js_num(&min_v)).collect();
    if usable.is_empty() {
        return TlsVerdict {
            ok: false,
            version: None,
            curl_code: 35,
            error: Some(format!(
                "alert protocol version — сервер поддерживает только TLS {}, клиент требует не ниже {}",
                tls.versions.join(", "),
                min_v
            )),
            lines,
        };
    }
    let version = if usable.iter().any(|v| v.as_str() == "1.3") { "1.3".to_string() } else { usable[usable.len() - 1].clone() };
    lines.push(format!("версия протокола: TLS {version}"));
    let c = &tls.cert;
    lines.push(format!("сертификат: CN={}, SAN={}, издатель {}, действует до {}", c.cn, c.san.join(", "), c.issuer, c.not_after));
    let fail = |code: i32, e: String, lines: Vec<String>| TlsVerdict {
        ok: false,
        version: Some(version.clone()),
        curl_code: code,
        error: Some(e),
        lines,
    };
    if let (Some(na), Some(now)) = (parse_date(&c.not_after), parse_date(NOW)) {
        if na < now {
            return fail(60, format!("SSL certificate problem: certificate has expired (до {}, сегодня {NOW})", c.not_after), lines);
        }
    }
    if !c.san.iter().chain(std::iter::once(&c.cn)).any(|n| name_matches(n, host)) {
        return fail(
            60,
            format!("SSL: no alternative certificate subject name matches target host name '{host}' (в сертификате: {})", c.san.join(", ")),
            lines,
        );
    }
    let sent: Vec<&String> = tls.chain.iter().collect();
    let mut cur = c.issuer.clone();
    let mut path = vec![c.cn.clone(), cur.clone()];
    for _ in 0..6 {
        if trust.contains(&cur) {
            lines.push(format!("цепочка: {}  — корень {cur} в хранилище доверия клиента", path.join(" ← ")));
            return TlsVerdict { ok: true, version: Some(version), curl_code: 0, error: None, lines };
        }
        let Some(ca) = cas.get(&cur) else {
            return fail(
                60,
                format!("SSL certificate problem: unable to get local issuer certificate (неизвестный издатель {cur})"),
                lines,
            );
        };
        let Some(issuer) = ca.issuer.clone() else {
            return fail(
                60,
                format!("SSL certificate problem: self-signed certificate in certificate chain (корень {cur} клиенту не доверен)"),
                lines,
            );
        };
        if !sent.iter().any(|s| **s == cur) {
            return fail(
                60,
                format!(
                    "SSL certificate problem: unable to get local issuer certificate (сервер не прислал промежуточный сертификат {cur})"
                ),
                lines,
            );
        }
        cur = issuer;
        path.push(cur.clone());
    }
    fail(60, "слишком длинная цепочка".into(), lines)
}

/// Итог HTTPS-запроса.
#[derive(Clone, Debug, Default)]
pub struct TlsFetchResult {
    pub error: Option<String>,
    pub run: Option<ProbeRun>,
    pub response: Option<HttpResponse>,
    pub via: Option<String>,
}

/// HTTPS-запрос: TCP-проба на порт + проверка TLS + ответ веб-сервера.
pub fn tls_fetch(state: &mut NetState, dev_id: &str, u: &ParsedUrl, ip: u32, method: &str, headers: &OrdMap<String>) -> TlsFetchResult {
    let mut run = tcp1(state, dev_id, ip, u.port, 50000, true);
    if run.status == ProbeStatus::Refused {
        return TlsFetchResult {
            error: Some(format!("curl: (7) Failed to connect to {} port {}: Connection refused", u.host, u.port)),
            run: Some(run),
            ..Default::default()
        };
    }
    if run.status != ProbeStatus::Connected {
        return TlsFetchResult {
            error: Some(format!("curl: (28) Connection timed out — {}:{} не отвечает", u.host, u.port)),
            run: Some(run),
            ..Default::default()
        };
    }
    let dev = delivered_to(state, &run, Some(ip));
    let Some(dev) = dev.filter(|d| d.tls.is_some()) else {
        return TlsFetchResult {
            error: Some("curl: (35) SSL connect error — на порту нет TLS-сервера".into()),
            run: Some(run),
            ..Default::default()
        };
    };
    let Some(client) = state.devices.get(dev_id).cloned() else { return TlsFetchResult::default() };
    let Some(tls) = dev.tls.as_ref() else { return TlsFetchResult::default() };
    let v = validate(state, &client, &u.host, tls);
    let rtts: f64 = if v.version.as_deref() == Some("1.2") { 2.0 } else { 1.0 };
    let rtt = run.rtt_us.unwrap_or(0.0);
    let text = if v.ok {
        format!("TLS {}: рукопожатие за {} кр., сертификат принят", v.version.clone().unwrap_or_default(), rtts)
    } else {
        format!("TLS: отказ — {}", v.error.clone().unwrap_or_default())
    };
    run.events.push(NetEvent { t: rtt + 30.0, dev: dev.id.clone(), kind: EventKind::Tls, text });
    if !v.ok {
        return TlsFetchResult {
            error: Some(format!("curl: ({}) {}", v.curl_code, v.error.unwrap_or_default())),
            run: Some(run),
            ..Default::default()
        };
    }
    let Some(http) = dev.http.as_ref() else {
        return TlsFetchResult { error: Some("curl: (52) Empty reply from server".into()), run: Some(run), ..Default::default() };
    };
    let mut resp = crate::http::respond(
        http,
        &crate::http::HttpRequest {
            method: method.to_string(),
            path: u.path.clone(),
            host: Some(u.host.clone()),
            headers: headers.clone(),
        },
    );
    resp.rtt_us = Some(rtt * (2.0 + rtts));
    let via = format!("TLS {}, рукопожатие {} кр. = {}", v.version.unwrap_or_default(), rtts, fmt_ms(Some(rtt * rtts)));
    TlsFetchResult { response: Some(resp), run: Some(run), via: Some(via), error: None }
}

/// `openssl s_client`: подробный вывод рукопожатия.
pub fn s_client(state: &mut NetState, dev_id: &str, host: &str, ip: u32, port: i64) -> (String, ProbeRun) {
    let run = tcp1(state, dev_id, ip, port, 50000, false);
    if run.status != ProbeStatus::Connected {
        let msg = if run.status == ProbeStatus::Refused { "Connection refused" } else { "Connection timed out" };
        return (format!("connect: {msg}"), run);
    }
    let dev = delivered_to(state, &run, Some(ip));
    let Some(dev) = dev.filter(|d| d.tls.is_some()) else { return ("openssl: на порту нет TLS".into(), run) };
    let Some(client) = state.devices.get(dev_id).cloned() else { return (String::new(), run) };
    let Some(tls) = dev.tls.as_ref() else { return (String::new(), run) };
    let v = validate(state, &client, host, tls);
    let mut out: Vec<String> = vec![format!("CONNECTED({}:{})", ip_str(ip), port)];
    out.extend(v.lines.iter().map(|l| format!("  {l}")));
    out.push(if v.ok { "Verification: OK".to_string() } else { format!("Verification error: {}", v.error.clone().unwrap_or_default()) });
    if let Some(ver) = &v.version {
        out.push(format!("Protocol: TLS {ver} (рукопожатие {} кр.)", if ver == "1.2" { 2 } else { 1 }));
    }
    (out.join("\n"), run)
}
