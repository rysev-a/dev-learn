//! Поле сети: устройства (перетаскиваются), кабели с портами и характеристиками, бегущие по ним пакеты, пометки о потерях,
//! прокладка кабеля мышью от устройства к устройству, сдвиг и масштаб окна. Арифметика — в `view.rs`, состояние — в `lab.rs`.

use leptos::{ev, prelude::*, svg};
use netlab::model::split_ref;
use wasm_bindgen::JsCast;
use netlab::types::{DeviceKind, NetState};

use super::lab::Lab;
use super::logic;
use super::view::{self, Point, Screen, DEV_H, DEV_W, HOME, ZOOM_STEP};
use crate::dom;

/// Что делает указатель, пока кнопка нажата.
#[derive(Clone, Debug, PartialEq)]
enum Drag {
    /// тянут устройство: `grab` — где схватили относительно его центра (в координатах поля)
    Device { id: String, grab: Point, down: Point, moved: bool },
    /// тянут кабель от устройства
    Cable { from: String, down: Point, moved: bool },
    /// двигают окно
    Pan { last: Point },
}

/// Всё, что нужно нарисовать про кабель.
#[derive(Clone, Debug, PartialEq)]
pub struct LinkInfo {
    pub geom: view::LinkGeom,
    pub port_a: String,
    pub port_b: String,
    /// один из концов выключен
    pub down: bool,
    pub km: f64,
}

/// Описание кабеля номер `idx`; `None`, если такого кабеля или одного из его устройств нет.
pub fn link_info(state: &NetState, idx: usize) -> Option<LinkInfo> {
    let l = state.links.get(idx)?;
    let (da, pa) = split_ref(&l.a);
    let (db, pb) = split_ref(&l.b);
    let a = state.devices.get(da)?;
    let b = state.devices.get(db)?;
    let up = |d: &netlab::types::Device, port: &str| d.iface(port).map(|i| i.up).unwrap_or(true);
    Some(LinkInfo {
        geom: view::link_geom(Point::new(a.x, a.y), Point::new(b.x, b.y)),
        port_a: pa.to_string(),
        port_b: pb.to_string(),
        down: !up(a, pa) || !up(b, pb),
        km: l.km,
    })
}

/// Центры устройств по порядку добавления (для поиска под курсором).
fn centers(state: &NetState) -> Vec<(String, Point)> {
    state.devices.iter().map(|d| (d.id.clone(), Point::new(d.x, d.y))).collect()
}

fn screen_of(svg: &web_sys::Element) -> Screen {
    let r = svg.get_bounding_client_rect();
    Screen { left: r.left(), top: r.top(), width: r.width(), height: r.height() }
}

fn client(e: &web_sys::PointerEvent) -> Point {
    Point::new(f64::from(e.client_x()), f64::from(e.client_y()))
}

/// Значок устройства (24×24, контур).
fn icon(kind: DeviceKind) -> AnyView {
    match kind {
        DeviceKind::Host => view! { <rect x="2" y="3" width="20" height="14" rx="2"></rect><path d="M8 21h8M12 17v4"></path> }.into_any(),
        DeviceKind::Server => view! {
            <rect x="2" y="2" width="20" height="8" rx="2"></rect>
            <rect x="2" y="14" width="20" height="8" rx="2"></rect>
            <path d="M6 6h.01M6 18h.01"></path>
        }
        .into_any(),
        DeviceKind::Router => view! {
            <rect x="2" y="14" width="20" height="8" rx="2"></rect>
            <path d="M6 18h.01M10 18h.01M15 10v4M17.8 7.2a4 4 0 0 0-5.6 0M20.7 4.3a8 8 0 0 0-11.4 0"></path>
        }
        .into_any(),
        DeviceKind::Hub => view! {
            <rect x="2" y="9" width="20" height="6" rx="2"></rect>
            <path d="M6 12h.01M10 12h.01M14 12h.01M18 12h.01M12 3v6M12 15v6"></path>
        }
        .into_any(),
        DeviceKind::Switch => view! {
            <rect x="2" y="7" width="20" height="10" rx="2"></rect>
            <path d="M6 12h.01M10 12h.01M14 12h.01M18 12h.01"></path>
        }
        .into_any(),
        DeviceKind::Internet => view! { <path d="M17.5 19H9a7 7 0 1 1 6.7-9h1.8a4.5 4.5 0 1 1 0 9Z"></path> }.into_any(),
    }
}

/// Поле сети с кнопками масштаба.
#[component]
pub fn Board(lab: Lab) -> impl IntoView {
    let svg_ref = NodeRef::<svg::Svg>::new();
    let vb = RwSignal::new(HOME);
    let drag = StoredValue::new(None::<Drag>);
    let panning = RwSignal::new(false);
    // свободный конец тянущегося кабеля (в координатах поля)
    let rubber = RwSignal::new(None::<Point>);
    let cable_tool = lab.tools().cable;

    let screen = move || svg_ref.get_untracked().map(|s| screen_of(s.unchecked_ref()));
    let to_board = move |c: Point| screen().map(|s| s.to_board(&vb.get_untracked(), c)).unwrap_or_default();

    let ids = Memo::new(move |_| lab.net.with(|n| n.devices.iter().map(|d| d.id.clone()).collect::<Vec<_>>()));
    let links = Memo::new(move |_| lab.net.with(|n| n.links.iter().enumerate().map(|(i, l)| (i, l.a.clone(), l.b.clone())).collect::<Vec<_>>()));

    // нажатие на устройство: выбрать и начать перетаскивание, а в режиме кабеля — начать (или закончить) кабель
    let device_down = move |e: web_sys::PointerEvent, id: String| {
        if e.button() != 0 {
            return;
        }
        e.stop_propagation();
        let c = client(&e);
        if lab.cable.get_untracked() {
            match lab.cable_from.get_untracked() {
                Some(from) if from != id => {
                    lab.connect(&from, &id);
                    lab.cable_from.set(None);
                }
                _ => {
                    lab.cable_from.set(Some(id.clone()));
                    rubber.set(Some(to_board(c)));
                    drag.set_value(Some(Drag::Cable { from: id, down: c, moved: false }));
                }
            }
            return;
        }
        lab.select(&id);
        let p = to_board(c);
        let center = lab.net.with_untracked(|n| n.devices.get(&id).map(|d| Point::new(d.x, d.y))).unwrap_or(p);
        drag.set_value(Some(Drag::Device { id, grab: Point::new(p.x - center.x, p.y - center.y), down: c, moved: false }));
    };

    let background_down = move |e: web_sys::PointerEvent| {
        let middle = e.button() == 1;
        if !(middle || e.button() == 0) {
            return;
        }
        e.prevent_default();
        drag.set_value(Some(Drag::Pan { last: client(&e) }));
        panning.set(true);
    };

    dom::on_window(ev::pointermove, move |e| {
        let Some(d) = drag.get_value() else { return };
        let c = client(&e);
        match d {
            Drag::Device { id, grab, down, moved } => {
                let moved = moved || !view::is_click(down, c);
                if moved {
                    let p = to_board(c);
                    let pos = view::clamp_device(Point::new(p.x - grab.x, p.y - grab.y));
                    lab.move_device(&id, pos.x, pos.y);
                }
                drag.set_value(Some(Drag::Device { id, grab, down, moved }));
            }
            Drag::Cable { from, down, moved } => {
                let moved = moved || !view::is_click(down, c);
                rubber.set(Some(to_board(c)));
                drag.set_value(Some(Drag::Cable { from, down, moved }));
            }
            Drag::Pan { last } => {
                if let Some(s) = screen() {
                    let (dx, dy) = s.pan_delta(&vb.get_untracked(), c.x - last.x, c.y - last.y);
                    vb.update(|v| *v = v.panned(dx, dy));
                }
                drag.set_value(Some(Drag::Pan { last: c }));
            }
        }
    });
    dom::on_window(ev::pointerup, move |e| {
        let Some(d) = drag.get_value() else { return };
        drag.set_value(None);
        match d {
            Drag::Device { moved, .. } => {
                if moved {
                    lab.moved();
                }
            }
            Drag::Cable { from, moved, .. } => {
                rubber.set(None);
                let p = to_board(client(&e));
                let target = lab.net.with_untracked(|n| {
                    let cs = centers(n);
                    view::device_at(cs.iter().map(|(id, c)| (id.as_str(), *c)), p).map(str::to_string)
                });
                match target {
                    Some(t) if t != from => {
                        lab.connect(&from, &t);
                        lab.cable_from.set(None);
                    }
                    // отпустили над своим устройством без движения — щелчок: ждём второго устройства
                    Some(_) if !moved => {}
                    _ => lab.cable_from.set(None),
                }
            }
            Drag::Pan { .. } => panning.set(false),
        }
    });

    let on_wheel = move |e: web_sys::WheelEvent| {
        if !(e.ctrl_key() || e.meta_key()) {
            return;
        }
        e.prevent_default();
        let Some(s) = screen() else { return };
        let anchor = s.to_board(&vb.get_untracked(), Point::new(f64::from(e.client_x()), f64::from(e.client_y())));
        vb.update(|v| *v = v.zoomed((-e.delta_y() * 0.0025).exp(), anchor));
    };
    let zoom_by = move |f: f64| {
        let v = vb.get_untracked();
        vb.set(v.zoomed(f, Point::new(v.x + v.w / 2.0, v.y + v.h / 2.0)));
    };

    view! {
        <div class="lab-board-wrap">
            <div class="lab-zoom" role="group" aria-label="Масштаб поля">
                <button type="button" title="Уменьшить (Ctrl + колесо)" on:click=move |_| zoom_by(1.0 / ZOOM_STEP)>"−"</button>
                <button type="button" class="pct" title="Масштаб 100 %" on:click=move |_| vb.update(|v| *v = v.with_zoom(1.0))>
                    {move || format!("{}%", view::js_round(vb.get().zoom() * 100.0))}
                </button>
                <button type="button" title="Увеличить (Ctrl + колесо)" on:click=move |_| zoom_by(ZOOM_STEP)>"+"</button>
                {move || (vb.get() != HOME).then(|| view! {
                    <button type="button" title="Вернуть поле на место и масштаб 100 %" on:click=move |_| vb.set(HOME)>"⌖"</button>
                })}
            </div>
            <svg
                node_ref=svg_ref
                class="nl-board"
                viewBox=move || vb.get().attr()
                role="img"
                aria-label="Схема сети"
                style=move || if panning.get() { "touch-action: none; cursor: grabbing" } else { "touch-action: none" }
                on:pointerdown=background_down
                on:wheel=on_wheel
                on:auxclick=|e| {
                    if e.button() == 1 {
                        e.prevent_default();
                    }
                }
            >
                <For each=move || links.get() key=|k| k.clone() children=move |(idx, _, _)| view! { <LinkView lab=lab idx=idx cable_tool=cable_tool /> } />
                {move || {
                    let from = lab.cable_from.get()?;
                    let to = rubber.get()?;
                    let a = lab.net.with(|n| n.devices.get(&from).map(|d| Point::new(d.x, d.y)))?;
                    Some(view! {
                        <g class="nl-link on">
                            <line x1=a.x.to_string() y1=a.y.to_string() x2=to.x.to_string() y2=to.y.to_string() stroke-dasharray="5 4"></line>
                        </g>
                    })
                }}
                <For each=move || ids.get() key=|id| id.clone() children=move |id| view! { <DeviceView lab=lab id=id on_down=Callback::new(move |(e, id)| device_down(e, id)) /> } />
                {move || {
                    let slot = lab.slot.get();
                    let dots = lab.run.with(|r| r.as_ref().map(|run| logic::dots(run, slot))).unwrap_or_default();
                    dots.into_iter()
                        .filter_map(|dot| {
                            let (a, b) = lab.net.with(|n| Some((n.devices.get(&dot.from)?.clone(), n.devices.get(&dot.to)?.clone())))?;
                            let p = view::lerp(Point::new(a.x, a.y), Point::new(b.x, b.y), dot.p);
                            Some(view! {
                                <g class=format!("nl-dot {}", dot.kind) transform=format!("translate({},{})", p.x, p.y)>
                                    <circle r="6"></circle>
                                </g>
                            })
                        })
                        .collect::<Vec<_>>()
                }}
                {move || {
                    let slot = lab.slot.get();
                    let marks = lab.run.with(|r| r.as_ref().map(|run| logic::marks(run, slot))).unwrap_or_default();
                    marks.into_iter()
                        .filter_map(|m| {
                            let d = lab.device(&m.dev)?;
                            let y = d.y - DEV_H / 2.0 - 8.0 - m.row as f64 * 12.0;
                            let glyph = match m.kind {
                                "drop" | "fw" => "✕ ",
                                "nat" => "⇄ ",
                                _ => "",
                            };
                            Some(view! {
                                <g class=format!("nl-mark {}", m.kind) transform=format!("translate({},{})", d.x, y)>
                                    <text>{format!("{glyph}{}", m.text)}</text>
                                </g>
                            })
                        })
                        .collect::<Vec<_>>()
                }}
            </svg>
        </div>
    }
}

/// Кабель: линия, подписи портов и длина.
#[component]
fn LinkView(lab: Lab, idx: usize, cable_tool: bool) -> impl IntoView {
    let info = move || lab.net.with(|n| link_info(n, idx));
    let class = move || {
        let down = info().is_some_and(|i| i.down);
        format!("nl-link {} {}", if lab.sel_link.get() == Some(idx) { "on" } else { "" }, if down { "down" } else { "" })
    };
    let coord = move |f: fn(&LinkInfo) -> f64| move || info().map(|i| f(&i).to_string()).unwrap_or_default();
    view! {
        <g class=class>
            <line x1=coord(|i| i.geom.a.x) y1=coord(|i| i.geom.a.y) x2=coord(|i| i.geom.b.x) y2=coord(|i| i.geom.b.y)></line>
            <line
                class="hit"
                x1=coord(|i| i.geom.a.x)
                y1=coord(|i| i.geom.a.y)
                x2=coord(|i| i.geom.b.x)
                y2=coord(|i| i.geom.b.y)
                on:pointerdown=|e| e.stop_propagation()
                on:click=move |_| {
                    if cable_tool {
                        lab.sel_link.set(Some(idx));
                    }
                }
            ></line>
            <text class="nl-port" x=coord(|i| i.geom.label_a.x) y=move || info().map(|i| (i.geom.label_a.y - 4.0).to_string()).unwrap_or_default()>
                {move || info().map(|i| i.port_a).unwrap_or_default()}
            </text>
            <text class="nl-port" x=coord(|i| i.geom.label_b.x) y=move || info().map(|i| (i.geom.label_b.y - 4.0).to_string()).unwrap_or_default()>
                {move || info().map(|i| i.port_b).unwrap_or_default()}
            </text>
            {move || info().filter(|i| i.km >= 1.0).map(|i| view! {
                <text class="nl-km" x=i.geom.mid.x.to_string() y=(i.geom.mid.y + 12.0).to_string()>{format!("{} км", netlab::util::num_str(i.km))}</text>
            })}
        </g>
    }
}

/// Устройство на поле: рамка, значок, имя и до трёх адресов.
#[component]
fn DeviceView(lab: Lab, id: String, on_down: Callback<(web_sys::PointerEvent, String)>) -> impl IntoView {
    let Some(dev) = lab.device(&id) else { return ().into_any() };
    let kind = dev.kind;
    let locked = dev.locked;
    let name = {
        let id = id.clone();
        move || lab.name_of(&id)
    };
    let pos = {
        let id = id.clone();
        move || lab.net.with(|n| n.devices.get(&id).map(|d| (d.x, d.y))).unwrap_or_default()
    };
    let ips = {
        let id = id.clone();
        move || lab.net.with(|n| n.devices.get(&id).map(logic::ip_labels)).unwrap_or_default()
    };
    let class = {
        let id = id.clone();
        move || {
            let on = lab.sel.get() == id;
            let from = lab.cable_from.get().as_deref() == Some(id.as_str());
            format!("nl-dev {} {} {} {}", logic::kind_class(kind), if on { "on" } else { "" }, if from { "from" } else { "" }, if locked { "locked" } else { "" })
        }
    };
    view! {
        <g class=class transform=move || { let (x, y) = pos(); format!("translate({x},{y})") } on:pointerdown=move |e| on_down.run((e, id.clone()))>
            <rect x=(-DEV_W / 2.0).to_string() y=(-DEV_H / 2.0).to_string() width=DEV_W.to_string() height=DEV_H.to_string() rx="9"></rect>
            <g class="nl-ico" transform="translate(-16,-26) scale(1.35)">{icon(kind)}</g>
            <text class="nl-name" y=(DEV_H / 2.0 - 7.0).to_string()>{name}</text>
            {move || ips().into_iter().enumerate().map(|(i, ip)| view! { <text class="nl-ip" y=(DEV_H / 2.0 + 14.0 + i as f64 * 12.0).to_string()>{ip}</text> }).collect::<Vec<_>>()}
        </g>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::*;
    use netlab::types::{Device, Iface, Link};

    fn state() -> NetState {
        let mut s = NetState::default();
        let mut a = Device::new("a", DeviceKind::Host, "А", 0.0, 0.0);
        a.ifaces.push(Iface::new("eth0", "28:28:00:00:00:01"));
        let mut b = Device::new("b", DeviceKind::Host, "Б", 200.0, 0.0);
        b.ifaces.push(Iface::new("eth0", "28:28:00:00:00:02"));
        s.devices.insert(a);
        s.devices.insert(b);
        let mut l = Link::new("a:eth0", "b:eth0");
        l.km = 5.0;
        s.links.push(l);
        s
    }

    #[test]
    fn link_info_has_geometry_ports_and_length() {
        let s = state();
        let i = link_info(&s, 0).expect("кабель");
        assert_eq!((i.port_a.as_str(), i.port_b.as_str()), ("eth0", "eth0"));
        assert_eq!(i.geom.a, Point::new(0.0, 0.0));
        assert_eq!(i.geom.b, Point::new(200.0, 0.0));
        assert_eq!(i.km, 5.0);
        assert!(!i.down);
        assert!(link_info(&s, 3).is_none());
    }

    #[test]
    fn a_disabled_port_marks_the_cable_down() {
        let mut s = state();
        s.devices.get_mut("b").and_then(|d| d.iface_mut("eth0")).expect("порт").up = false;
        assert!(link_info(&s, 0).expect("кабель").down);
    }

    #[test]
    fn cable_to_a_missing_device_is_skipped() {
        let mut s = state();
        s.links.push(Link::new("a:eth0", "ghost:eth0"));
        assert!(link_info(&s, 1).is_none());
    }

    #[test]
    fn centers_follow_the_order_of_devices() {
        let c = centers(&state());
        assert_eq!(c.iter().map(|(id, _)| id.as_str()).collect::<Vec<_>>(), vec!["a", "b"]);
        assert_eq!(c[1].1, Point::new(200.0, 0.0));
    }
}
