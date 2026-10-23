//! График окна перегрузки (cwnd) по времени передачи: «пила», уровни BDP и окна приёма.

use leptos::prelude::*;
use netlab::transfer::TransferChart;
use netlab::util::to_fixed;

const W: f64 = 640.0;
const H: f64 = 150.0;
const L: f64 = 60.0;
const B: f64 = 22.0;
const T: f64 = 10.0;

/// Разметка графика: подготовленные числа и подписи (чистая функция — легко проверить).
#[derive(Clone, Debug, PartialEq)]
pub struct ChartLayout {
    pub points: String,
    pub max_t: f64,
    pub max_y: f64,
    pub bdp_y: f64,
    pub rwnd_y: Option<f64>,
}

impl ChartLayout {
    pub fn new(c: &TransferChart) -> ChartLayout {
        let max_t = c.trace.iter().map(|p| p.t).fold(1.0, f64::max);
        let max_y = c.trace.iter().map(|p| p.cwnd).chain([c.bdp_kb * 1.15, c.rwnd_kb.min(c.bdp_kb * 3.0), 10.0]).fold(f64::MIN, f64::max);
        let x = |t: f64| L + (t / max_t) * (W - L - 8.0);
        let y = |v: f64| H - B - (v.min(max_y) / max_y) * (H - B - T);
        let points = c.trace.iter().map(|p| format!("{},{}", to_fixed(x(p.t), 1), to_fixed(y(p.cwnd), 1))).collect::<Vec<_>>().join(" ");
        ChartLayout { points, max_t, max_y, bdp_y: y(c.bdp_kb), rwnd_y: (c.rwnd_kb < max_y).then(|| y(c.rwnd_kb)) }
    }
}

#[component]
pub fn Chart(chart: TransferChart) -> impl IntoView {
    let lay = ChartLayout::new(&chart);
    let kb = |v: f64| to_fixed(v, 0);
    let rwnd = lay.rwnd_y.map(|ry| {
        view! {
            <line x1=L.to_string() x2=(W - 8.0).to_string() y1=ry.to_string() y2=ry.to_string() class="rw"></line>
            <text x=(W - 10.0).to_string() y=(ry + 11.0).to_string() class="lbl rw" text-anchor="end">{format!("окно приёма {} КБ", kb(chart.rwnd_kb))}</text>
        }
    });
    view! {
        <figure class="nl-chart">
            <svg viewBox=format!("0 0 {W} {H}") role="img" aria-label="График окна перегрузки">
                <line x1=L.to_string() y1=T.to_string() x2=L.to_string() y2=(H - B).to_string() class="ax"></line>
                <line x1=L.to_string() y1=(H - B).to_string() x2=(W - 8.0).to_string() y2=(H - B).to_string() class="ax"></line>
                <line x1=L.to_string() x2=(W - 8.0).to_string() y1=lay.bdp_y.to_string() y2=lay.bdp_y.to_string() class="bdp"></line>
                <text x=(W - 10.0).to_string() y=(lay.bdp_y - 3.0).to_string() class="lbl" text-anchor="end">{format!("ёмкость канала (BDP) {} КБ", kb(chart.bdp_kb))}</text>
                {rwnd}
                <polyline points=lay.points.clone() class="cw"></polyline>
                <text x=(L - 4.0).to_string() y=(T + 8.0).to_string() class="lbl" text-anchor="end">{format!("{} КБ", kb(lay.max_y))}</text>
                <text x=(L - 4.0).to_string() y=(H - B).to_string() class="lbl" text-anchor="end">"0"</text>
                <text x=(W - 8.0).to_string() y=(H - 6.0).to_string() class="lbl" text-anchor="end">{format!("{} мс", kb(lay.max_t))}</text>
                <text x=(L + 4.0).to_string() y=(H - 6.0).to_string() class="lbl">{format!("cwnd, алгоритм {}", chart.cc.as_str())}</text>
            </svg>
            {(chart.qcap_kb > 0.0).then(|| view! { <figcaption>{format!("очередь на узком месте до {} КБ", kb(chart.qcap_kb))}</figcaption> })}
        </figure>
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use netlab::transfer::TracePoint;
    use netlab::types::Cc;

    fn chart(rwnd: f64) -> TransferChart {
        TransferChart {
            trace: vec![TracePoint { t: 0.0, cwnd: 14.0, rtt: 10.0 }, TracePoint { t: 100.0, cwnd: 60.0, rtt: 12.0 }],
            bdp_kb: 50.0,
            rwnd_kb: rwnd,
            qcap_kb: 0.0,
            cc: Cc::Cubic,
            from: "a".into(),
            to: "b".into(),
        }
    }

    #[test]
    fn layout_scales_to_the_largest_value() {
        let l = ChartLayout::new(&chart(1000.0));
        assert_eq!(l.max_t, 100.0);
        assert_eq!(l.max_y, 150.0, "окно приёма урезано до тройного BDP");
        assert_eq!(l.rwnd_y, None, "окно приёма вышло за пределы графика");
        assert!(l.points.starts_with("60.0,"), "{}", l.points);
        assert!(l.points.contains(" 632.0,"), "{}", l.points);
    }

    #[test]
    fn small_receive_window_gets_its_own_line() {
        let l = ChartLayout::new(&chart(32.0));
        assert!(l.rwnd_y.is_some());
        assert!(l.rwnd_y.unwrap_or(0.0) > l.bdp_y, "окно приёма ниже уровня BDP");
    }

    #[test]
    fn empty_trace_does_not_divide_by_zero() {
        let mut c = chart(32.0);
        c.trace.clear();
        let l = ChartLayout::new(&c);
        assert_eq!(l.max_t, 1.0);
        assert!(l.points.is_empty());
    }
}
