//! Модель передачи файла по TCP: окно приёма, окно перегрузки, медленный старт, потери и очередь.
//! Это не пакетная симуляция, а пораундовая модель (один шаг — один круговой обход): достаточно, чтобы видеть
//! «пилу», влияние окна и алгоритма, потерь и размера буфера. Детерминирована.

use crate::ip::*;
use crate::sim::{ping1, PingOpts};
use crate::types::*;
use crate::util::to_fixed;
use serde::{Deserialize, Serialize};

const MSS: f64 = 1460.0;
const INIT: f64 = 10.0 * MSS;

/// Участок пути «туда»: кабель и откуда он идёт.
#[derive(Clone, Debug)]
pub struct PathHop {
    pub link: Link,
    pub from: String,
    pub from_port: String,
    pub to: String,
}

fn forward_path(state: &NetState, run: &ProbeRun) -> Vec<PathHop> {
    let mut hops: Vec<&Hop> = run
        .hops
        .iter()
        .filter(|h| matches!(&h.frame.body, Payload::Ip(p) if p.proto == Proto::Icmp && p.icmp.as_ref().map(|i| i.typ) == Some(IcmpType::EchoReq)))
        .collect();
    hops.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap_or(std::cmp::Ordering::Equal));
    hops.into_iter()
        .filter_map(|h| {
            let p = state.peer_of(&h.from, &h.from_port)?;
            Some(PathHop { link: state.links[p.link].clone(), from: h.from.clone(), from_port: h.from_port.clone(), to: h.to.clone() })
        })
        .collect()
}

fn mbps_of(l: &Link) -> f64 {
    if l.mbps == 0.0 {
        1000.0
    } else {
        l.mbps
    }
}

/// Свойства пути до адреса.
#[derive(Clone, Debug)]
pub enum PathInfo {
    /// Связи нет: статус пробы.
    NoReply(ProbeStatus),
    Ok {
        probe: ProbeRun,
        dst_id: Option<String>,
        path: Vec<PathHop>,
        /// RTT без нагрузки, мкс.
        rtt0: f64,
        /// Скорость узкого места, Мбит/с.
        rate: f64,
        /// Вероятность потери пакета на пути.
        loss_p: f64,
        /// Индекс участка-узкого места.
        bott: Option<usize>,
    },
}

/// Свойства пути: RTT, узкое место, вероятность потери, получатель.
pub fn path_info(state: &mut NetState, src_id: &str, dst: u32) -> PathInfo {
    ping1(state, src_id, dst, &PingOpts { id: 900, ..Default::default() }); // прогрев ARP и таблиц
    let probe = ping1(state, src_id, dst, &PingOpts { id: 901, ..Default::default() });
    if probe.status != ProbeStatus::Reply {
        return PathInfo::NoReply(probe.status);
    }
    let dst_id = probe.delivered.iter().find(|x| x.dst == Some(dst)).map(|x| x.dev.clone());
    let path = forward_path(state, &probe);
    let rate = path.iter().map(|h| mbps_of(&h.link)).fold(f64::INFINITY, f64::min);
    let loss_p = 1.0 - path.iter().fold(1.0, |a, h| a * (1.0 - h.link.loss.filter(|l| *l != 0.0).unwrap_or(0.0) / 100.0));
    let bott = path.iter().position(|h| mbps_of(&h.link) == rate);
    PathInfo::Ok { rtt0: probe.rtt_us.unwrap_or(0.0), probe, dst_id, path, rate, loss_p, bott }
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct TracePoint {
    pub t: f64,
    pub cwnd: f64,
    pub rtt: f64,
}

/// График передачи: окно перегрузки и RTT по кругам.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct TransferChart {
    pub trace: Vec<TracePoint>,
    pub bdp_kb: f64,
    pub rwnd_kb: f64,
    pub qcap_kb: f64,
    pub cc: Cc,
    pub from: String,
    pub to: String,
}

/// Итог передачи файла.
#[derive(Clone, Debug)]
pub struct TransferResult {
    pub ok: bool,
    /// «done» или статус пробы / «nopath».
    pub status: String,
    pub mbps: f64,
    pub seconds: f64,
    pub loaded_rtt_ms: f64,
    pub losses: u32,
    pub limit: String,
    pub bdp_kb: f64,
    pub rwnd_kb: f64,
    pub chart: Option<TransferChart>,
    pub text: String,
}

fn failed(status: &str) -> TransferResult {
    TransferResult {
        ok: false,
        status: status.into(),
        mbps: 0.0,
        seconds: 0.0,
        loaded_rtt_ms: 0.0,
        losses: 0,
        limit: String::new(),
        bdp_kb: 0.0,
        rwnd_kb: 0.0,
        chart: None,
        text: "нет связи: передавать некуда".into(),
    }
}

/// Передача `bytes` байт от устройства `src_id` к адресу `dst`.
pub fn transfer(state: &mut NetState, src_id: &str, dst: u32, bytes: f64) -> TransferResult {
    let info = path_info(state, src_id, dst);
    let PathInfo::Ok { dst_id, path, rtt0, rate, loss_p, bott, .. } = info else {
        return match info {
            PathInfo::NoReply(s) => failed(s.as_str()),
            _ => failed("nopath"),
        };
    };
    let (Some(bott), Some(dst_id)) = (bott, dst_id) else { return failed("nopath") };
    let bott = &path[bott];
    let qlen = state.devices.get(&bott.from).and_then(|d| d.iface(&bott.from_port)).and_then(|i| i.txqueuelen).unwrap_or(1000) as f64; // пакетов
    let Some(srcd) = state.devices.get(src_id) else { return failed("nopath") };
    let Some(dstd) = state.devices.get(&dst_id) else { return failed("nopath") };
    let rwnd = dstd.rwnd.unwrap_or(64) as f64 * 1024.0; // байт
    let cc = srcd.cc.unwrap_or(Cc::Cubic);

    let rate_bps = (rate * 1e6) / 8.0; // байт/с
    let bdp = (rate_bps * rtt0) / 1e6;
    let qcap = qlen * 1500.0;

    let mut cwnd = INIT;
    let mut ssthresh = f64::INFINITY;
    let mut sent = 0.0;
    let mut t = 0.0;
    let mut loss_acc = 0.0;
    let mut losses = 0u32;
    let mut max_rtt = rtt0;
    let mut trace = vec![TracePoint { t: 0.0, cwnd: cwnd / 1024.0, rtt: rtt0 / 1000.0 }];
    let mut rounds = 0;

    while sent < bytes && rounds < 4000 {
        rounds += 1;
        let win;
        let rtt;
        let delivered;
        if cc == Cc::Bbr {
            // BBR держит скорость у канала и почти игнорирует потери
            win = rwnd.min(if rounds < 4 { cwnd } else { bdp * 1.25 + 4.0 * MSS });
            rtt = rtt0 + ((win - bdp).max(0.0) * 8.0) / (rate * 1e6) * 1e6;
            delivered = win.min((rate_bps * rtt) / 1e6) * (1.0 - loss_p * 0.6);
            cwnd = if rounds < 4 { cwnd * 2.0 } else { win };
        } else {
            win = cwnd.min(rwnd);
            let queued = (win - bdp).min(qcap).max(0.0);
            rtt = rtt0 + ((queued * 8.0) / (rate * 1e6)) * 1e6;
            delivered = win.min((rate_bps * rtt) / 1e6);
            let mut loss = false;
            if win > bdp + qcap {
                loss = true; // очередь переполнена
            }
            loss_acc += (delivered / MSS) * loss_p;
            if loss_acc >= 1.0 {
                loss_acc -= 1.0;
                loss = true;
            }
            if loss {
                losses += 1;
                let beta = if cc == Cc::Cubic { 0.7 } else { 0.5 };
                ssthresh = (2.0 * MSS).max(win * beta);
                cwnd = ssthresh;
            } else if cwnd < ssthresh {
                cwnd = (cwnd * 2.0).min(if ssthresh == f64::INFINITY { f64::INFINITY } else { ssthresh });
            } else {
                cwnd += (if cc == Cc::Cubic { 3.0 } else { 1.0 }) * MSS;
            }
        }
        sent += delivered;
        t += rtt;
        max_rtt = max_rtt.max(rtt);
        trace.push(TracePoint { t: t / 1000.0, cwnd: (if cc == Cc::Bbr { win } else { cwnd }) / 1024.0, rtt: rtt / 1000.0 });
    }

    let seconds = t / 1e6;
    let mbps = (sent.min(bytes) * 8.0) / 1e6 / seconds;
    let limit = if cc == Cc::Bbr {
        "канал"
    } else if rwnd < bdp * 0.9 {
        "окно приёма"
    } else if loss_p > 0.001 {
        "потери (алгоритм сбрасывает окно)"
    } else {
        "канал"
    };
    let text = [
        format!("передано {} МБ за {} с — {} Мбит/с", to_fixed(bytes / 1e6, 0), to_fixed(seconds, 2), to_fixed(mbps, 1)),
        format!(
            "канал {} Мбит/с · RTT {} мс · BDP {} КБ",
            crate::util::num_str(rate),
            to_fixed(rtt0 / 1000.0, 1),
            to_fixed(bdp / 1024.0, 0)
        ),
        format!("окно приёма {} КБ · алгоритм {} · потерь: {}", to_fixed(rwnd / 1024.0, 0), cc.as_str(), losses),
        format!("RTT под нагрузкой до {} мс (очередь {} пакетов)", to_fixed(max_rtt / 1000.0, 0), crate::util::num_str(qlen)),
        format!("ограничивает: {limit}"),
    ]
    .join("\n");
    TransferResult {
        ok: true,
        status: "done".into(),
        mbps,
        seconds,
        loaded_rtt_ms: max_rtt / 1000.0,
        losses,
        limit: limit.into(),
        bdp_kb: bdp / 1024.0,
        rwnd_kb: rwnd / 1024.0,
        chart: Some(TransferChart {
            trace,
            bdp_kb: bdp / 1024.0,
            rwnd_kb: rwnd / 1024.0,
            qcap_kb: qcap / 1024.0,
            cc,
            from: src_id.to_string(),
            to: ip_str(dst),
        }),
        text,
    }
}
