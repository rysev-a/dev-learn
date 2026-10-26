//! Загрузка веб-страницы по HTTP/1.1, HTTP/2 и HTTP/3: пораундовая модель. Страница — HTML и N ресурсов;
//! считаем рукопожатия, число «кругов» запросов, передачу по узкому месту и цену потерь:
//! h1 — шесть соединений, h2 — одно TCP (потеря тормозит все потоки), h3 — QUIC (потоки независимы).

use crate::ip::*;
use crate::sim::udp1;
use crate::transfer::{path_info, PathInfo};
use crate::types::*;
use crate::util::{num_str, to_fixed};

/// Условия загрузки: RTT (мкс), канал (Мбит/с), вероятность потери, число ресурсов, их размер (КБ), HTTPS.
#[derive(Clone, Debug)]
pub struct PageEnv {
    pub rtt: f64,
    pub rate: f64,
    pub loss_p: f64,
    pub count: f64,
    pub kb: f64,
    pub https: bool,
}

/// Время загрузки страницы по одной версии HTTP, мкс.
#[derive(Clone, Debug)]
pub struct PageModel {
    pub proto: HttpProto,
    pub total: f64,
    pub setup: f64,
    pub rounds: f64,
    pub xfer: f64,
    pub loss: f64,
    pub l: f64,
}

pub fn page_model(env: &PageEnv, proto: HttpProto) -> PageModel {
    let PageEnv { rtt, rate, loss_p, count, kb, https } = *env;
    let bytes = (count + 1.0) * kb * 1024.0;
    let l = (bytes / 1460.0) * loss_p; // ожидаемое число потерянных пакетов
    let tcp_setup = rtt; // SYN → SYN-ACK
    let tls_setup = if https { rtt } else { 0.0 }; // TLS 1.3: ещё один круг
    let xfer = ((bytes * 8.0) / (rate * 1e6)) * 1e6; // мкс по узкому месту
    let slow = 3.0 * rtt; // разгон окна
    let (setup, rounds, loss) = match proto {
        HttpProto::H1 => (tcp_setup + tls_setup, 1.0 + (count / 6.0).ceil(), (l * rtt) / 6.0), // HTML, затем ресурсы по 6 штук
        HttpProto::H2 => (tcp_setup + tls_setup, 2.0, l * rtt), // HTML и все ресурсы разом; потеря стопорит все потоки
        HttpProto::H3 => (rtt, 2.0, l * rtt * 0.15),            // QUIC: транспорт и шифрование за один круг
    };
    let total = setup + rounds * rtt + xfer + (if proto == HttpProto::H1 { slow * 1.5 } else { slow }) + loss;
    PageModel { proto, total, setup, rounds, xfer, loss, l }
}

/// Итог измерения загрузки.
#[derive(Clone, Debug)]
pub enum PageloadResult {
    Failed(String),
    Ok { want: HttpProto, used: HttpProto, note: String, chosen: PageModel, all: Vec<PageModel>, env: PageEnv, ip: String },
}

/// Измерить загрузку страницы с устройства `dev_id` на сервер `dst`.
pub fn pageload(state: &mut NetState, dev_id: &str, dst: u32, https: bool) -> PageloadResult {
    let info = path_info(state, dev_id, dst);
    let PathInfo::Ok { dst_id, rtt0, rate, loss_p, .. } = info else {
        return PageloadResult::Failed("нет связи с сервером".into());
    };
    let http = dst_id.as_deref().and_then(|id| state.devices.get(id)).and_then(|d| d.http.clone());
    let Some(page) = http.as_ref().and_then(|h| h.page.clone()) else {
        return PageloadResult::Failed("на сервере нет страницы для измерения".into());
    };
    let want = http.as_ref().and_then(|h| h.protocol).unwrap_or(HttpProto::H1);
    let mut used = want;
    let mut note = String::new();
    if want == HttpProto::H3 {
        let u = udp1(state, dev_id, dst, 443, 50001);
        if u.status != ProbeStatus::Reply {
            used = HttpProto::H2;
            note = "UDP/443 до сервера не проходит или не слушается — браузер откатился на HTTP/2".into();
        }
    }
    let env = PageEnv { rtt: rtt0, rate, loss_p, count: page.count, kb: page.kb, https };
    let all: Vec<PageModel> = [HttpProto::H1, HttpProto::H2, HttpProto::H3].iter().map(|p| page_model(&env, *p)).collect();
    let chosen = all.iter().find(|x| x.proto == used).cloned().unwrap_or_else(|| all[0].clone());
    PageloadResult::Ok { want, used, note, chosen, all, env, ip: ip_str(dst) }
}

/// Вывод команды `pageload`.
pub fn fmt_page(r: &PageloadResult) -> String {
    match r {
        PageloadResult::Failed(e) => format!("pageload: {e}"),
        PageloadResult::Ok { want, used, note, chosen, all, env, .. } => {
            let s = |us: f64| to_fixed(us / 1e6, 2);
            let arrow = if note.is_empty() { String::new() } else { format!(" → {}", used.name()) };
            let mut l = vec![
                format!(
                    "страница: {} ресурсов по ~{} КБ · RTT {} мс · канал {} Мбит/с · потери {}%",
                    num_str(env.count + 1.0),
                    num_str(env.kb),
                    to_fixed(env.rtt / 1000.0, 0),
                    num_str(env.rate),
                    to_fixed(env.loss_p * 100.0, 1)
                ),
                format!("сервер предлагает: {}{}", want.name(), arrow),
                format!(
                    "загрузка: {} с (рукопожатия {}, {} кругов запросов, передача {}, потери {})",
                    s(chosen.total),
                    s(chosen.setup),
                    num_str(chosen.rounds),
                    s(chosen.xfer),
                    s(chosen.loss)
                ),
                String::new(),
                "для сравнения:".to_string(),
            ];
            for x in all {
                l.push(format!("  {:<9} {} с{}", x.proto.name(), s(x.total), if x.proto == *used { "   ← сейчас" } else { "" }));
            }
            if !note.is_empty() {
                l.push(String::new());
                l.push(note.clone());
            }
            l.join("\n")
        }
    }
}
