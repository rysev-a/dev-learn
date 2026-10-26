//! Чистая логика лаборатории «Компьютерные сети»: разбор сценария и черновика, раскладка кадров пробы по «моментам»
//! анимации, подписи, правки интерфейса и история терминала. Без сигналов и DOM — всё проверяется обычными тестами.

use netlab::types::{Device, DeviceKind, EventKind, FrameKind, Hop, NetEvent};
use netlab::{state_from_json, GoalResult, NetSpec, NetState};
use serde_json::Value;

/// Длительность одного «момента» анимации, мс.
#[cfg_attr(not(target_arch = "wasm32"), allow(dead_code))]
pub const SLOT_MS: f64 = 320.0;
/// Сколько «моментов» после последнего события пометки ещё висят над устройством.
const MARK_TTL: f64 = 5.0;

/// Сценарий упражнения из `spec` задачи (эталонного решения в нём нет — его сервер не отдаёт).
pub fn parse_spec(raw: &Value) -> Result<NetSpec, String> {
    serde_json::from_value(raw.clone()).map_err(|e| format!("Неверное описание упражнения: {e}"))
}

/// Состояние сети из JSON: каноническая запись или прежняя запись клиента.
pub fn draft_json(state: &NetState) -> String {
    serde_json::to_string(state).unwrap_or_default()
}

fn device_ids(s: &NetState) -> Vec<String> {
    let mut ids: Vec<String> = s.devices.iter().map(|d| d.id.clone()).collect();
    ids.sort();
    ids
}

/// Сохранённое состояние ученика; пустой, испорченный или чужой черновик (другой набор устройств) — исходная сеть.
pub fn restore(spec: &NetSpec, draft: &str) -> NetState {
    let fresh = spec.start_state();
    if draft.trim().is_empty() {
        return fresh;
    }
    match state_from_json(draft) {
        Ok(s) if device_ids(&s) == device_ids(&fresh) => s,
        _ => fresh,
    }
}

/// Отличается ли состояние от исходного (по настройкам и кабелям; кэши симулятора не в счёт).
pub fn differs_from_start(spec: &NetSpec, state: &NetState) -> bool {
    draft_json(state) != draft_json(&spec.start_state())
}

/* ---- проба: «моменты» анимации ---- */

/// Кадры и события последней пробы, разложенные по «моментам» анимации.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct RunView {
    pub hops: Vec<Hop>,
    pub events: Vec<NetEvent>,
    /// отсортированные уникальные времена переходов и событий, мкс
    pub tl: Vec<f64>,
    pub title: String,
}

impl RunView {
    /// `None`, если показывать нечего.
    pub fn new(hops: Vec<Hop>, events: Vec<NetEvent>, title: &str) -> Option<RunView> {
        if hops.is_empty() && events.is_empty() {
            return None;
        }
        let tl = timeline(&hops, &events);
        Some(RunView { hops, events, tl, title: title.to_string() })
    }

    /// Сколько «моментов» длится показ: все точки линии времени и ещё три на «послевкусие».
    pub fn total_slots(&self) -> f64 {
        (self.tl.len() + 3) as f64
    }
}

/// Линия времени: все моменты `t0`/`t1` переходов и `t` событий по возрастанию без повторов.
pub fn timeline(hops: &[Hop], events: &[NetEvent]) -> Vec<f64> {
    let mut ts: Vec<f64> = hops.iter().flat_map(|h| [h.t0, h.t1]).chain(events.iter().map(|e| e.t)).filter(|t| t.is_finite()).collect();
    ts.sort_by(|a, b| a.total_cmp(b));
    ts.dedup();
    ts
}

/// Номер момента по времени.
pub fn slot_of(tl: &[f64], t: f64) -> Option<usize> {
    tl.iter().position(|x| *x == t)
}

/// Пакет, бегущий по кабелю: между устройствами `from` и `to`, доля пути `p` от 0 до 1.
#[derive(Clone, Debug, PartialEq)]
pub struct Dot {
    pub from: String,
    pub to: String,
    pub p: f64,
    pub kind: &'static str,
    pub label: String,
}

/// Пакеты, которые в момент `slot` находятся на кабелях.
pub fn dots(run: &RunView, slot: f64) -> Vec<Dot> {
    run.hops
        .iter()
        .filter_map(|h| {
            let a = slot_of(&run.tl, h.t0)? as f64;
            let end = slot_of(&run.tl, h.t1)? as f64;
            let b = end.max(a + 0.6);
            let p = (slot - a) / (b - a);
            (0.0..=1.0).contains(&p).then(|| Dot { from: h.from.clone(), to: h.to.clone(), p, kind: frame_class(h.kind), label: h.label.clone() })
        })
        .collect()
}

/// Номера событий, которые уже «произошли» к моменту `slot`.
pub fn shown_indices(run: &RunView, slot: f64) -> Vec<usize> {
    run.events.iter().enumerate().filter(|(_, e)| slot_of(&run.tl, e.t).is_some_and(|i| i as f64 <= slot)).map(|(i, _)| i).collect()
}

/// События, которые уже «произошли» к моменту `slot`.
pub fn shown_events(run: &RunView, slot: f64) -> Vec<&NetEvent> {
    shown_indices(run, slot).into_iter().map(|i| &run.events[i]).collect()
}

/// Пометка над устройством: отброшено, NAT, файрвол …
#[derive(Clone, Debug, PartialEq)]
pub struct Mark {
    pub dev: String,
    pub kind: &'static str,
    pub text: String,
    /// номер строки над устройством (пометки одного устройства идут стопкой)
    pub row: usize,
}

/// Текст не длиннее 38 знаков: длинный обрезается до 36 и «…».
pub fn short_text(s: &str) -> String {
    if s.chars().count() > 38 {
        let head: String = s.chars().take(36).collect();
        format!("{head}…")
    } else {
        s.to_string()
    }
}

/// Пометки, которые видны в момент `slot`: отбрасывание, файрвол и NAT, не старше пяти «моментов».
pub fn marks(run: &RunView, slot: f64) -> Vec<Mark> {
    let mut out: Vec<Mark> = Vec::new();
    for e in shown_events(run, slot) {
        if !matches!(e.kind, EventKind::Drop | EventKind::Fw | EventKind::Nat) {
            continue;
        }
        let Some(at) = slot_of(&run.tl, e.t) else { continue };
        if slot - at as f64 > MARK_TTL {
            continue;
        }
        let row = out.iter().filter(|m| m.dev == e.dev).count();
        out.push(Mark { dev: e.dev.clone(), kind: event_class(e.kind), text: short_text(&e.text), row });
    }
    out
}

/// Подпись под полем: что сейчас на кабеле, «…» пока ничего нет, «готово» в конце.
pub fn caption(run: &RunView, slot: f64) -> String {
    match dots(run, slot).into_iter().next() {
        Some(d) => d.label,
        None if slot >= run.tl.len() as f64 => "готово".to_string(),
        None => "…".to_string(),
    }
}

/// Номера событий для журнала: уже случившиеся, а если их ещё нет — все.
pub fn log_indices(run: &RunView, slot: f64) -> Vec<usize> {
    let shown = shown_indices(run, slot);
    if shown.is_empty() {
        (0..run.events.len()).collect()
    } else {
        shown
    }
}

/// Какие события показывать в журнале: уже случившиеся, а если их ещё нет — все.
#[cfg(test)]
pub fn log_lines(run: &RunView, slot: f64) -> Vec<&NetEvent> {
    log_indices(run, slot).into_iter().map(|i| &run.events[i]).collect()
}

/// Класс события в журнале (совпадает с CSS `.nl-log li.<класс>`).
pub fn event_class(k: EventKind) -> &'static str {
    match k {
        EventKind::Icmp => "icmp",
        EventKind::Tcp => "tcp",
        EventKind::Udp => "udp",
        EventKind::Arp => "arp",
        EventKind::Learn => "learn",
        EventKind::Drop => "drop",
        EventKind::Loop => "loop",
        EventKind::Conflict => "conflict",
        EventKind::Nat => "nat",
        EventKind::Fw => "fw",
        EventKind::Tun => "tun",
        EventKind::Dns => "dns",
        EventKind::Http => "http",
        EventKind::Tls => "tls",
        EventKind::Info => "info",
    }
}

/// Класс пакета на кабеле (`.nl-dot.arp`, `.nl-dot.tcp`; остальные — цвет по умолчанию).
pub fn frame_class(k: FrameKind) -> &'static str {
    match k {
        FrameKind::Arp => "arp",
        FrameKind::Tcp => "tcp",
        FrameKind::Udp => "udp",
        FrameKind::Icmp => "icmp",
    }
}

/* ---- подписи ---- */

/// Вид устройства для шапки карточки.
pub fn kind_title(k: DeviceKind) -> &'static str {
    match k {
        DeviceKind::Host => "компьютер",
        DeviceKind::Server => "сервер",
        DeviceKind::Router => "маршрутизатор",
        DeviceKind::Switch => "коммутатор",
        DeviceKind::Hub => "хаб (повторитель)",
        DeviceKind::Internet => "интернет (провайдер)",
    }
}

/// Класс устройства на поле (`.nl-dev.router` …).
pub fn kind_class(k: DeviceKind) -> &'static str {
    match k {
        DeviceKind::Host => "host",
        DeviceKind::Server => "server",
        DeviceKind::Router => "router",
        DeviceKind::Switch => "switch",
        DeviceKind::Hub => "hub",
        DeviceKind::Internet => "internet",
    }
}

/// Приглашение терминала: имя устройства без пробелов и «# ».
pub fn prompt(name: &str) -> String {
    format!("{}# ", name.split_whitespace().collect::<Vec<_>>().join("-"))
}

/// Адреса интерфейсов для подписи под устройством: не более трёх, «ip/префикс».
pub fn ip_labels(d: &Device) -> Vec<String> {
    d.ifaces.iter().filter_map(|i| i.ip.as_deref().filter(|s| !s.is_empty()).map(|ip| format!("{ip}/{}", i.prefix))).take(3).collect()
}

/// Итог по цели для списка: что рисовать в отметке.
#[derive(Clone, Debug, PartialEq)]
pub struct GoalView {
    pub text: String,
    pub ok: bool,
    pub detail: String,
}

impl From<GoalResult> for GoalView {
    fn from(r: GoalResult) -> GoalView {
        GoalView { text: r.text, ok: r.ok, detail: r.detail }
    }
}

/// Все ли цели выполнены (пустой список целей — не решение).
pub fn all_ok(goals: &[GoalView]) -> bool {
    !goals.is_empty() && goals.iter().all(|g| g.ok)
}

/// Итог под списком целей: решено раньше, засчитано сейчас или решение ещё проверяется на сервере.
pub fn verdict_text(solved_before: bool, solved: bool) -> &'static str {
    if solved_before {
        "Упражнение уже было решено."
    } else if solved {
        "Упражнение засчитано."
    } else {
        "Проверяю решение на сервере…"
    }
}

/* ---- правки интерфейса ---- */

/// Оставить только цифры и не больше `max` знаков (поля порта, префикса, кода ответа).
pub fn digits(s: &str, max: usize) -> String {
    s.chars().filter(char::is_ascii_digit).take(max).collect()
}

/// Применить адрес из формы интерфейса: пустое поле снимает адрес; неудачная замена возвращает прежний адрес.
/// `Some(текст)` — ошибка для ученика, `None` — успех (или нечего менять).
pub fn commit_iface_addr(d: &mut Device, name: &str, ip: &str, prefix: &str) -> Option<String> {
    let ip = ip.trim();
    let Some(cur) = d.iface(name) else { return Some(format!("нет интерфейса {name}")) };
    let (old_ip, old_prefix) = (cur.ip.clone().filter(|s| !s.is_empty()), cur.prefix);
    if ip.is_empty() {
        return if old_ip.is_some() { netlab::term::clear_addr(d, name) } else { None };
    }
    if old_ip.as_deref() == Some(ip) && old_prefix.to_string() == prefix {
        return None;
    }
    netlab::term::clear_addr(d, name);
    let err = netlab::term::set_addr(d, name, &format!("{ip}/{prefix}"));
    if err.is_some() {
        if let Some(old) = old_ip {
            netlab::term::set_addr(d, name, &format!("{old}/{old_prefix}"));
        }
    }
    err
}

/// Адрес DNS-сервера из формы: пусто — убрать; не IPv4 — ошибка.
pub fn commit_resolver(d: &mut Device, value: &str) -> Option<String> {
    let v = value.trim();
    if !v.is_empty() && netlab::ip::parse_ip(v).is_none() {
        return Some("нужен IPv4-адрес DNS-сервера".into());
    }
    d.resolver = (!v.is_empty()).then(|| v.to_string());
    None
}

/// Строка таблицы маршрутов для формы.
#[derive(Clone, Debug, PartialEq)]
pub struct RouteRow {
    pub dst: String,
    pub via: String,
    pub dev: String,
    /// подключённая сеть: удалить нельзя
    pub connected: bool,
}

pub fn route_rows(d: &Device) -> Vec<RouteRow> {
    netlab::sim::route_table(d, false)
        .into_iter()
        .map(|r| RouteRow {
            dst: if r.prefix == 0 { "default".into() } else { netlab::ip::net_str(Some(r.net), r.prefix) },
            via: r.via.map(|v| format!("via {}", netlab::ip::ip_str(v))).unwrap_or_else(|| "напрямую".into()),
            dev: r.dev,
            connected: r.connected,
        })
        .collect()
}

/// Версии TLS в порядке от старой к новой: отметка `on` у `version`, остальные как были.
pub fn toggle_tls_version(current: &[String], version: &str, on: bool) -> Vec<String> {
    ["1.0", "1.1", "1.2", "1.3"]
        .iter()
        .filter(|x| if **x == version { on } else { current.iter().any(|c| c == **x) })
        .map(|x| x.to_string())
        .collect()
}

/// Команда веб-сервера для нового маршрута: для 30x — перенаправление.
pub fn web_route_command(path: &str, status: u32, extra: &str) -> String {
    if [301, 302, 307, 308].contains(&status) {
        format!("web redirect {path} {status} {extra}")
    } else {
        format!("web route {path} {status} {extra}")
    }
}

/// Команда правила файрвола `iptables -A FORWARD …` из значений формы (пустые поля пропускаются).
pub fn fw_rule_command(action: &str, proto: &str, src: &str, dst: &str, port: &str, state: &str) -> String {
    let mut p: Vec<String> = Vec::new();
    if !proto.is_empty() {
        p.push(format!("-p {proto}"));
    }
    if !src.is_empty() {
        p.push(format!("-s {src}"));
    }
    if !dst.is_empty() {
        p.push(format!("-d {dst}"));
    }
    if !port.is_empty() {
        p.push(format!("--dport {port}"));
    }
    if !state.is_empty() {
        p.push(format!("-m conntrack --ctstate {state}"));
    }
    format!("iptables -A FORWARD {} -j {action}", p.join(" "))
}

/* ---- история терминала ---- */

/// Шаг по истории стрелками. `hist` — команды от новых к старым, `h` — текущая позиция (−1 — строка набирается заново).
/// Возвращает новую позицию и текст строки; `None` — клавиша ничего не меняет.
pub fn history_step(hist: &[String], h: isize, key: &str) -> Option<(isize, String)> {
    match key {
        "ArrowUp" if !hist.is_empty() => {
            let n = (h + 1).min(hist.len() as isize - 1);
            Some((n, hist[n as usize].clone()))
        }
        "ArrowDown" => {
            let n = h - 1;
            let text = if n >= 0 { hist.get(n as usize).cloned().unwrap_or_default() } else { String::new() };
            Some((n, text))
        }
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use netlab::types::{Frame, Payload};

    fn frame() -> Frame {
        Frame { size: 64, src: "a".into(), dst: "b".into(), vlan: None, uid: None, body: Payload::Arp(netlab::types::ArpInfo { op: netlab::types::ArpOp::Req, sip: 1, smac: "a".into(), tip: 2, tmac: None }) }
    }

    fn hop(t0: f64, t1: f64, label: &str) -> Hop {
        Hop { from: "pc1".into(), from_port: "eth0".into(), to: "sw".into(), to_port: "p1".into(), t0, t1, kind: FrameKind::Arp, label: label.into(), frame: frame() }
    }

    fn event(t: f64, dev: &str, kind: EventKind, text: &str) -> NetEvent {
        NetEvent { t, dev: dev.into(), kind, text: text.into() }
    }

    fn run() -> RunView {
        RunView::new(vec![hop(0.0, 100.0, "ARP"), hop(100.0, 250.0, "ICMP")], vec![event(100.0, "sw", EventKind::Drop, "сброшено"), event(250.0, "pc2", EventKind::Icmp, "ответ")], "ping").expect("проба")
    }

    #[test]
    fn timeline_is_sorted_and_unique() {
        let r = run();
        assert_eq!(r.tl, vec![0.0, 100.0, 250.0]);
        assert_eq!(r.total_slots(), 6.0);
        assert_eq!(slot_of(&r.tl, 250.0), Some(2));
        assert_eq!(slot_of(&r.tl, 7.0), None);
        assert!(RunView::new(vec![], vec![], "x").is_none());
    }

    #[test]
    fn dots_run_along_the_cable_between_two_slots() {
        let r = run();
        assert_eq!(dots(&r, 0.5)[0].p, 0.5);
        // в момент 1 первый переход закончился, второй только начинается
        let d = dots(&r, 1.0);
        assert!(d.iter().any(|x| x.label == "ARP" && (x.p - 1.0).abs() < 1e-9));
        assert!(d.iter().any(|x| x.label == "ICMP" && x.p == 0.0));
        assert!(dots(&r, 5.0).is_empty());
        assert_eq!(caption(&r, 5.0), "готово");
        assert_eq!(caption(&r, 2.5), "…");
        assert_eq!(caption(&r, 1.5), "ICMP");
    }

    #[test]
    fn a_hop_never_runs_faster_than_zero_point_six_of_a_slot() {
        // оба конца в одном моменте: переход растягивается на 0,6 момента
        let r = RunView::new(vec![hop(10.0, 10.0, "мгновенно")], vec![], "x").expect("проба");
        assert!(dots(&r, 0.3)[0].p > 0.4);
        assert!(dots(&r, 0.7).is_empty());
    }

    #[test]
    fn events_appear_when_their_moment_comes_and_marks_expire() {
        let r = run();
        assert_eq!(shown_events(&r, 0.5).len(), 0);
        assert_eq!(shown_events(&r, 1.0).len(), 1);
        assert_eq!(log_lines(&r, 0.0).len(), 2, "пока ничего не случилось, журнал показывает всё");
        let m = marks(&r, 1.0);
        assert_eq!(m, vec![Mark { dev: "sw".into(), kind: "drop", text: "сброшено".into(), row: 0 }]);
        assert!(marks(&r, 7.0).is_empty(), "через пять моментов пометка гаснет");
    }

    #[test]
    fn marks_of_one_device_stack_in_rows() {
        let r = RunView::new(vec![], vec![event(1.0, "r1", EventKind::Nat, "a"), event(2.0, "r1", EventKind::Fw, "b"), event(3.0, "r2", EventKind::Drop, "c"), event(4.0, "r1", EventKind::Info, "d")], "x").expect("проба");
        let m = marks(&r, 3.0);
        assert_eq!(m.iter().map(|x| (x.dev.as_str(), x.row)).collect::<Vec<_>>(), vec![("r1", 0), ("r1", 1), ("r2", 0)]);
    }

    #[test]
    fn long_mark_text_is_cut() {
        let long = "я".repeat(50);
        let s = short_text(&long);
        assert_eq!(s.chars().count(), 37);
        assert!(s.ends_with('…'));
        assert_eq!(short_text("коротко"), "коротко");
    }

    #[test]
    fn prompt_has_no_spaces() {
        assert_eq!(prompt("ПК 1"), "ПК-1# ");
        assert_eq!(prompt("r1"), "r1# ");
    }

    #[test]
    fn history_walks_back_and_forth() {
        let hist = vec!["ping b".to_string(), "ip a".to_string()];
        assert_eq!(history_step(&hist, -1, "ArrowUp"), Some((0, "ping b".into())));
        assert_eq!(history_step(&hist, 0, "ArrowUp"), Some((1, "ip a".into())));
        assert_eq!(history_step(&hist, 1, "ArrowUp"), Some((1, "ip a".into())), "дальше самой старой не уйти");
        assert_eq!(history_step(&hist, 1, "ArrowDown"), Some((0, "ping b".into())));
        assert_eq!(history_step(&hist, 0, "ArrowDown"), Some((-1, String::new())));
        assert_eq!(history_step(&hist, -1, "ArrowDown"), Some((-2, String::new())));
        assert_eq!(history_step(&[], -1, "ArrowUp"), None);
        assert_eq!(history_step(&hist, -1, "a"), None);
    }

    #[test]
    fn digits_are_filtered_and_capped() {
        assert_eq!(digits("8a0b80", 6), "8080");
        assert_eq!(digits("12345", 3), "123");
    }

    #[test]
    fn firewall_command_skips_empty_fields() {
        assert_eq!(fw_rule_command("DROP", "", "", "", "", ""), "iptables -A FORWARD  -j DROP");
        assert_eq!(
            fw_rule_command("ACCEPT", "tcp", "10.0.0.0/24", "", "80", "NEW"),
            "iptables -A FORWARD -p tcp -s 10.0.0.0/24 --dport 80 -m conntrack --ctstate NEW -j ACCEPT"
        );
    }

    #[test]
    fn web_redirect_is_chosen_for_30x() {
        assert_eq!(web_route_command("/a", 301, "/b"), "web redirect /a 301 /b");
        assert_eq!(web_route_command("/a", 404, "нет"), "web route /a 404 нет");
    }

    #[test]
    fn tls_versions_keep_their_order() {
        let cur = vec!["1.2".to_string()];
        assert_eq!(toggle_tls_version(&cur, "1.3", true), vec!["1.2", "1.3"]);
        assert_eq!(toggle_tls_version(&cur, "1.0", true), vec!["1.0", "1.2"]);
        assert_eq!(toggle_tls_version(&cur, "1.2", false), Vec::<String>::new());
    }

    fn host() -> Device {
        let mut d = Device::new("pc", DeviceKind::Host, "ПК", 0.0, 0.0);
        d.ifaces.push(netlab::types::Iface::new("eth0", "28:28:00:00:00:01"));
        d
    }

    #[test]
    fn address_form_sets_replaces_and_clears() {
        let mut d = host();
        assert_eq!(commit_iface_addr(&mut d, "eth0", "10.0.0.5", "24"), None);
        assert_eq!(d.iface("eth0").and_then(|i| i.ip.clone()).as_deref(), Some("10.0.0.5"));
        // смена адреса
        assert_eq!(commit_iface_addr(&mut d, "eth0", "10.0.0.6", "16"), None);
        let i = d.iface("eth0").expect("интерфейс");
        assert_eq!((i.ip.as_deref(), i.prefix), (Some("10.0.0.6"), 16));
        // неверный адрес возвращает прежний
        assert!(commit_iface_addr(&mut d, "eth0", "не адрес", "24").is_some());
        let i = d.iface("eth0").expect("интерфейс");
        assert_eq!((i.ip.as_deref(), i.prefix), (Some("10.0.0.6"), 16));
        // без изменений — тишина
        assert_eq!(commit_iface_addr(&mut d, "eth0", "10.0.0.6", "16"), None);
        // пустое поле снимает адрес
        assert_eq!(commit_iface_addr(&mut d, "eth0", "  ", "24"), None);
        assert_eq!(d.iface("eth0").and_then(|i| i.ip.clone()), None);
        assert!(commit_iface_addr(&mut d, "eth9", "1.1.1.1", "24").is_some());
    }

    #[test]
    fn resolver_must_be_an_ipv4_address() {
        let mut d = host();
        assert!(commit_resolver(&mut d, "dns.local").is_some());
        assert_eq!(commit_resolver(&mut d, " 192.168.0.53 "), None);
        assert_eq!(d.resolver.as_deref(), Some("192.168.0.53"));
        assert_eq!(commit_resolver(&mut d, ""), None);
        assert_eq!(d.resolver, None);
    }

    #[test]
    fn route_rows_show_connected_networks_first() {
        let mut d = host();
        netlab::term::set_addr(&mut d, "eth0", "192.168.0.2/24");
        netlab::term::set_gateway(&mut d, Some("192.168.0.1"));
        let rows = route_rows(&d);
        assert_eq!(rows[0].dst, "192.168.0.0/24");
        assert!(rows[0].connected);
        assert_eq!(rows[1], RouteRow { dst: "default".into(), via: "via 192.168.0.1".into(), dev: "eth0".into(), connected: false });
    }

    #[test]
    fn goal_views_and_verdicts() {
        let g = |ok| GoalView { text: "t".into(), ok, detail: String::new() };
        assert!(!all_ok(&[]));
        assert!(!all_ok(&[g(true), g(false)]));
        assert!(all_ok(&[g(true), g(true)]));
        assert_eq!(verdict_text(true, true), "Упражнение уже было решено.");
        assert_eq!(verdict_text(false, true), "Упражнение засчитано.");
        assert_eq!(verdict_text(false, false), "Проверяю решение на сервере…");
    }

    /// Файлы данных (без эталонного решения, как их отдаёт сервер) разбираются в `NetSpec`, исходная сеть восстанавливается,
    /// а испорченный или чужой черновик заменяется исходной сетью.
    #[test]
    fn every_exercise_spec_parses_without_solution() {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/net");
        let Ok(entries) = std::fs::read_dir(&dir) else { return };
        let mut n = 0;
        for e in entries.filter_map(Result::ok) {
            let text = std::fs::read_to_string(e.path()).expect("файл данных");
            let v: Value = serde_json::from_str(&text).expect("JSON");
            for t in v["tasks"].as_array().expect("упражнения") {
                let mut spec = t["spec"].clone();
                spec.as_object_mut().expect("spec").remove("solution");
                let parsed = parse_spec(&spec).unwrap_or_else(|e| panic!("{}: {e}", t["id"]));
                let start = restore(&parsed, "");
                assert!(!start.devices.is_empty());
                assert!(!differs_from_start(&parsed, &start));
                assert_eq!(restore(&parsed, "{ испорчено").devices.len(), start.devices.len());
                assert_eq!(restore(&parsed, "{\"devices\":[],\"links\":[]}").devices.len(), start.devices.len());
                // сохранённое состояние возвращается как есть
                let mut changed = start.clone();
                changed.links.clear();
                assert!(differs_from_start(&parsed, &changed) || start.links.is_empty());
                assert_eq!(restore(&parsed, &draft_json(&changed)).links.len(), changed.links.len());
                n += 1;
            }
        }
        assert!(n == 0 || n >= 70, "ожидалось ≈79 упражнений, разобрано {n}");
    }
}
