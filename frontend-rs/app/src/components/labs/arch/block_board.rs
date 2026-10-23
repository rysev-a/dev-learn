//! Доска с блоками: прямоугольники с типизированными портами, соединяемые шинами (`BlockBoard.tsx`). Порт можно
//! раскрыть (▸) и тянуть шину от отдельного поля. Типы совместимы только по имени. В режиме `readonly` (внутренность
//! блока) блоки можно двигать на экране — схема не меняется.

use std::{
    collections::{HashMap, HashSet},
    sync::Arc,
};

use archlab::{
    blocks::{add_bus_wire, port_values, BlockInstance, BlockInterface, BusEnd, BusWire},
    interfaces::bus_text,
    layout::BoxKind,
    model::{wire_path, NodeValue},
};
use leptos::{ev, prelude::*, svg};

use super::{
    block_logic::{
        board_size, join_error, kind_of, layout_boxes, next_bus_id, orient, pin_for, pin_map, ports_of, toggle_expanded, wire_class, BoxInfo, PinHit, RowInfo, BLOCKS_BOARD_H,
    },
    common::{Exp, Lib, Scope},
    view::{clamp_world, is_background, is_click, use_fullscreen, ArchView, Point, ZoomControls},
};
use crate::dom;

fn bp(p: Point) -> archlab::model::Point {
    archlab::model::Point { x: p.x, y: p.y }
}

fn client(e: &web_sys::PointerEvent) -> Point {
    Point::new(f64::from(e.client_x()), f64::from(e.client_y()))
}

/// Перетаскиваемый блок: смещение указателя внутри него, высота (для границ мира) и точка нажатия на порт.
#[derive(Clone, Copy, Default)]
struct DragInfo {
    off: Point,
    h: f64,
    pin_down: Option<Point>,
}

/// Подпись и вид шины на доске.
#[derive(Clone, Debug, PartialEq)]
struct WireView {
    id: String,
    d: String,
    mx: f64,
    my: f64,
    text: String,
    width: usize,
    class: &'static str,
}

/// Всё, что нужно обработчикам доски: сигналы состояния и данные схемы.
#[derive(Clone, Copy)]
struct Ix {
    iface: StoredValue<Arc<BlockInterface>>,
    library: Signal<Lib>,
    instances: RwSignal<Vec<BlockInstance>>,
    bus_wires: RwSignal<Vec<BusWire>>,
    view: ArchView,
    readonly: bool,
    expanded: RwSignal<HashSet<String>>,
    moved: RwSignal<HashMap<String, Point>>,
    pending: RwSignal<Option<BusEnd>>,
    sticky: RwSignal<bool>,
    cursor: RwSignal<Option<Point>>,
    hover: RwSignal<Option<String>>,
    moving: RwSignal<Option<String>>,
    drag: StoredValue<DragInfo>,
    pins: Memo<HashMap<String, PinHit>>,
    on_edited: Option<Callback<()>>,
    on_message: Option<Callback<String>>,
}

impl Ix {
    /// Выполнить `f` с функцией «порты узла» (читает схему без подписки на сигналы).
    fn with_ports<R>(&self, f: impl FnOnce(&archlab::blocks::PortsOf) -> R) -> R {
        let iface = self.iface.get_value();
        let lib = self.library.get_untracked();
        self.instances.with_untracked(|ins| f(&ports_of(&iface, &lib.0, ins)))
    }

    fn cancel_wire(&self) {
        self.pending.set(None);
        self.sticky.set(false);
        self.hover.set(None);
        self.cursor.set(None);
    }

    fn connect(&self, a: BusEnd, b: BusEnd) {
        let outcome = self.with_ports(|ports| {
            let (from, to) = orient(&a, &b, ports);
            match join_error(&from, &to, ports) {
                Some(e) => Err(e),
                None => Ok(self.bus_wires.with_untracked(|w| {
                    let wire = BusWire { id: next_bus_id(w), from, to };
                    add_bus_wire(w, wire, ports)
                })),
            }
        });
        match outcome {
            Err(e) => {
                if let Some(m) = self.on_message {
                    m.run(e);
                }
            }
            Ok(next) => {
                self.bus_wires.set(next);
                if let Some(c) = self.on_edited {
                    c.run(());
                }
            }
        }
    }

    fn on_move(&self, e: &web_sys::PointerEvent) {
        let c = client(e);
        if self.view.move_pan(c.x, c.y) {
            return;
        }
        if let Some(id) = self.moving.get_untracked() {
            let p = self.view.to_board(c.x, c.y);
            let d = self.drag.get_value();
            let o = clamp_world(Point::new(p.x - d.off.x, p.y - d.off.y), archlab::layout::BLOCK_W, if d.h > 0.0 { d.h } else { 80.0 });
            if self.readonly {
                self.moved.update(|m| {
                    m.insert(id, o);
                });
            } else {
                self.instances.update(|l| {
                    if let Some(i) = l.iter_mut().find(|i| i.id == id) {
                        i.x = o.x;
                        i.y = o.y;
                    }
                });
            }
            return;
        }
        if self.pending.get_untracked().is_some() {
            self.cursor.set(Some(self.view.to_board(c.x, c.y)));
        }
    }

    fn on_up(&self, e: &web_sys::PointerEvent) {
        if self.view.end_pan() {
            return;
        }
        if self.moving.get_untracked().is_some() {
            self.moving.set(None);
            if !self.readonly {
                if let Some(c) = self.on_edited {
                    c.run(());
                }
            }
            return;
        }
        let Some(pending) = self.pending.get_untracked() else { return };
        if self.sticky.get_untracked() {
            return;
        }
        let target = self.hover.get_untracked().and_then(|k| self.pins.with_untracked(|p| p.get(&k).map(|h| h.row.end.clone())));
        match target {
            Some(t) if t != pending => {
                self.connect(pending, t);
                self.cancel_wire();
            }
            _ if self.drag.get_value().pin_down.is_some_and(|d| is_click(d, client(e))) => self.sticky.set(true),
            _ => self.cancel_wire(),
        }
    }

    fn board_down(&self, e: &web_sys::PointerEvent) {
        if self.sticky.get_untracked() && e.button() == 0 {
            self.cancel_wire();
            return;
        }
        let free = self.pending.get_untracked().is_none();
        self.view.on_pointer_down(e, free && is_background(e.target(), "bb-bg"));
    }

    fn pin_down(&self, e: &web_sys::PointerEvent, row: &RowInfo) {
        if self.readonly || e.button() != 0 {
            return;
        }
        e.prevent_default();
        e.stop_propagation();
        if let Some(from) = self.pending.get_untracked().filter(|_| self.sticky.get_untracked()) {
            self.cancel_wire();
            if from != row.end {
                self.connect(from, row.end.clone());
            }
            return;
        }
        let c = client(e);
        self.pending.set(Some(row.end.clone()));
        self.sticky.set(false);
        self.drag.update_value(|d| d.pin_down = Some(c));
        self.hover.set(None);
        self.cursor.set(Some(self.view.to_board(c.x, c.y)));
    }

    fn box_down(&self, e: &web_sys::PointerEvent, node: &str, kind: BoxKind, at: Point, h: f64) {
        if kind != BoxKind::Block || e.button() != 0 {
            return;
        }
        if self.sticky.get_untracked() {
            self.cancel_wire();
            return;
        }
        e.prevent_default();
        let c = client(e);
        let p = self.view.to_board(c.x, c.y);
        self.drag.update_value(|d| {
            d.off = Point::new(p.x - at.x, p.y - at.y);
            d.h = h;
        });
        self.moving.set(Some(node.to_string()));
    }

    fn remove_instance(&self, id: &str) {
        self.instances.update(|l| l.retain(|i| i.id != id));
        self.bus_wires.update(|l| l.retain(|w| w.from.node != id && w.to.node != id));
        if let Some(c) = self.on_edited {
            c.run(());
        }
    }
}

/// Доска блоков: в режиме `readonly` — только просмотр (внутренность блока или процессор).
#[component]
pub fn BlockBoard(
    iface: Arc<BlockInterface>,
    #[prop(into)] library: Signal<Lib>,
    instances: RwSignal<Vec<BlockInstance>>,
    bus_wires: RwSignal<Vec<BusWire>>,
    #[prop(into)] expansion: Signal<Option<Exp>>,
    scope: Scope,
    #[prop(default = false)] readonly: bool,
    #[prop(default = None)] clock_node: Option<String>,
    #[prop(default = BLOCKS_BOARD_H)] height: f64,
    #[prop(default = 1.0)] spread: f64,
    #[prop(optional)] on_toggle: Option<Callback<String>>,
    #[prop(optional)] on_inspect: Option<Callback<String>>,
    #[prop(optional)] on_edited: Option<Callback<()>>,
    #[prop(optional)] on_message: Option<Callback<String>>,
) -> impl IntoView {
    let fullscreen = use_fullscreen();
    let svg_ref = NodeRef::<svg::Svg>::new();
    let (board_w, board_h) = instances.with_untracked(|i| board_size(i, spread, height));
    let view = ArchView::new(svg_ref, Signal::stored((board_w, board_h)));
    let expanded = RwSignal::new(HashSet::<String>::new());
    let moved = RwSignal::new(HashMap::<String, Point>::new());
    let iface_v = StoredValue::new(iface);

    let boxes = Memo::new(move |_| {
        let iface = iface_v.get_value();
        let lib = library.get();
        instances.with(|ins| expanded.with(|ex| moved.with(|mv| layout_boxes(&iface, &lib.0, ins, ex, mv, board_w, spread))))
    });
    let pins = Memo::new(move |_| boxes.with(|b| pin_map(b)));
    let ix = Ix {
        iface: iface_v,
        library,
        instances,
        bus_wires,
        view,
        readonly,
        expanded,
        moved,
        pending: RwSignal::new(None),
        sticky: RwSignal::new(false),
        cursor: RwSignal::new(None),
        hover: RwSignal::new(None),
        moving: RwSignal::new(None),
        drag: StoredValue::new(DragInfo::default()),
        pins,
        on_edited,
        on_message,
    };

    // шины с подписями: значения порта берутся из развёрнутой схемы
    let scope_for_wires = scope.clone();
    let wires_view = Memo::new(move |_| {
        let iface = iface_v.get_value();
        let lib = library.get();
        let exp = expansion.get();
        pins.with(|pins| {
            instances.with(|ins| {
                bus_wires.with(|ws| {
                    let ports = ports_of(&iface, &lib.0, ins);
                    ws.iter()
                        .filter_map(|w| {
                            let (a, b) = (pin_for(pins, &w.from)?, pin_for(pins, &w.to)?);
                            let info = archlab::blocks::end_info(&w.from, &ports);
                            let values: Vec<NodeValue> = match (&exp, &info) {
                                (Some(e), Some(_)) => port_values(&*scope_for_wires, &e.0, &w.from, &ports),
                                _ => Vec::new(),
                            };
                            let width = info.map_or(1, |i| i.length);
                            Some(WireView {
                                id: w.id.clone(),
                                d: wire_path(bp(a.pos), bp(b.pos)),
                                mx: (a.pos.x + b.pos.x) / 2.0,
                                my: (a.pos.y + b.pos.y) / 2.0,
                                text: bus_text(&values),
                                width,
                                class: wire_class(&values, width),
                            })
                        })
                        .collect::<Vec<_>>()
                })
            })
        })
    });
    let wire_ids = Memo::new(move |_| wires_view.with(|w| w.iter().map(|x| x.id.clone()).collect::<Vec<_>>()));

    // контакты, к которым можно присоединить тянущуюся шину (остальные гаснут)
    let compatible = Memo::new(move |_| {
        let Some(pending) = ix.pending.get() else { return HashSet::new() };
        let iface = iface_v.get_value();
        let lib = library.get();
        pins.with(|pins| {
            instances.with(|ins| {
                let ports = ports_of(&iface, &lib.0, ins);
                pins.iter().filter(|(_, p)| join_error(&pending, &p.row.end, &ports).is_none()).map(|(k, _)| k.clone()).collect::<HashSet<_>>()
            })
        })
    });
    let preview = Memo::new(move |_| {
        let pending = ix.pending.get()?;
        let (a, target) = pins.with(|p| (pin_for(p, &pending).cloned(), ix.hover.get().and_then(|k| p.get(&k).cloned())));
        let a = a?;
        let end = target.as_ref().map(|t| t.pos).or(ix.cursor.get())?;
        let d = if a.row.side_in { wire_path(bp(end), bp(a.pos)) } else { wire_path(bp(a.pos), bp(end)) };
        let ok = match &target {
            Some(t) => {
                let iface = iface_v.get_value();
                let lib = library.get();
                instances.with(|ins| join_error(&pending, &t.row.end, &ports_of(&iface, &lib.0, ins)).is_none())
            }
            None => false,
        };
        Some((d, ok))
    });

    dom::on_window(ev::pointermove, move |e| ix.on_move(&e));
    dom::on_window(ev::pointerup, move |e| ix.on_up(&e));
    dom::on_window(ev::keydown, move |e| {
        if e.key() == "Escape" && ix.pending.get_untracked().is_some() {
            ix.cancel_wire();
        }
    });
    // пока шина тянется за мышью, нажатие мимо порта и мимо кнопок масштаба её отменяет
    dom::on_window(ev::pointerdown, move |e| {
        if !ix.sticky.get_untracked() || e.button() == 1 {
            return;
        }
        if !super::view::target_within(e.target(), ".bpin-hit") && !super::view::target_within(e.target(), ".lab-zoom") {
            ix.cancel_wire();
        }
    });

    let box_keys = Memo::new(move |_| boxes.with(|b| b.iter().map(BoxInfo::key).collect::<Vec<_>>()));
    let changed = Signal::derive(move || moved.with(|m| !m.is_empty()));
    let reset_moved = Callback::new(move |()| moved.set(HashMap::new()));

    view! {
        <div class="lab-board" class:fill=fullscreen>
            <ZoomControls view=view extra_changed=changed on_reset=reset_moved />
            <svg
                node_ref=svg_ref
                class="lab-board-svg bb"
                class:readonly=readonly
                class:panning=move || view.panning.get()
                viewBox=move || view.view_box()
                role="img"
                aria-label="Доска с блоками и шинами"
                on:pointerdown=move |e| ix.board_down(&e)
                on:wheel=move |e| view.on_wheel(&e, fullscreen())
                on:mousedown=|e| {
                    if e.button() == 1 {
                        e.prevent_default();
                    }
                }
                on:auxclick=|e| {
                    if e.button() == 1 {
                        e.prevent_default();
                    }
                }
            >
                <defs>
                    <pattern id="bb-dots" width="22" height="22" patternUnits="userSpaceOnUse">
                        <circle cx="1.5" cy="1.5" r="1.5" class="grid-dot"></circle>
                    </pattern>
                </defs>
                <rect
                    class="bb-bg"
                    x=move || view.pan.get().x.to_string()
                    y=move || view.pan.get().y.to_string()
                    width=move || (board_w / view.zoom.get()).to_string()
                    height=move || (board_h / view.zoom.get()).to_string()
                    fill="url(#bb-dots)"
                ></rect>
                <For each=move || wire_ids.get() key=|id| id.clone() children=move |id| wire_view(ix, wires_view, id) />
                <For
                    each=move || box_keys.get()
                    key=|k| k.clone()
                    children={
                        let scope = scope.clone();
                        let clock = clock_node.clone();
                        move |(node, tag)| box_view(ix, boxes, compatible, scope.clone(), clock.clone(), node, kind_of(tag), on_toggle, on_inspect)
                    }
                />
                {move || preview.get().map(|(d, ok)| view! { <path class="bwire-preview" class:ok=ok d=d></path> })}
            </svg>
        </div>
    }
}

/// Шина: линия по значению сигнала, подпись с битами посередине, широкая полоса для щелчка (клик — удалить).
fn wire_view(ix: Ix, wires: Memo<Vec<WireView>>, id: String) -> impl IntoView {
    let me = Memo::new({
        let id = id.clone();
        move |_| wires.with(|l| l.iter().find(|w| w.id == id).cloned())
    });
    let readonly = ix.readonly;
    let wide = me.with_untracked(|w| w.as_ref().is_some_and(|w| w.width > 1));
    let remove_id = id.clone();
    view! {
        <g
            class="bwire"
            class:bus=wide
            on:pointerdown=move |e| {
                if !readonly && e.button() == 0 {
                    ix.bus_wires.update(|l| l.retain(|w| w.id != remove_id));
                    if let Some(c) = ix.on_edited {
                        c.run(());
                    }
                }
            }
        >
            {(!readonly).then(|| view! { <title>"Клик — удалить шину"</title> })}
            <path class="bwire-hit" d=move || me.with(|w| w.as_ref().map(|w| w.d.clone()).unwrap_or_default())></path>
            <path class=move || format!("bwire-line {}", me.with(|w| w.as_ref().map_or("vx", |w| w.class))) d=move || me.with(|w| w.as_ref().map(|w| w.d.clone()).unwrap_or_default())></path>
            <g class="bwire-tag" transform=move || me.with(|w| w.as_ref().map(|w| format!("translate({} {})", w.mx, w.my)).unwrap_or_default())>
                <rect
                    x=move || me.with(|w| w.as_ref().map_or(0.0, |w| -(w.text.chars().count() as f64 * 3.6 + 5.0)))
                    y="-8"
                    width=move || me.with(|w| w.as_ref().map_or(0.0, |w| w.text.chars().count() as f64 * 7.2 + 10.0))
                    height="16"
                    rx="8"
                ></rect>
                <text y="3.5" text-anchor="middle">{move || me.with(|w| w.as_ref().map(|w| w.text.clone()).unwrap_or_default())}</text>
            </g>
        </g>
    }
}

/// Прямоугольник: блок (с заголовком, «лупой» и крестиком) или колонка портов упражнения.
#[allow(clippy::too_many_arguments)]
fn box_view(
    ix: Ix,
    boxes: Memo<Vec<BoxInfo>>,
    compatible: Memo<HashSet<String>>,
    scope: Scope,
    clock: Option<String>,
    node: String,
    kind: BoxKind,
    on_toggle: Option<Callback<String>>,
    on_inspect: Option<Callback<String>>,
) -> impl IntoView {
    let me = Memo::new({
        let node = node.clone();
        move |_| boxes.with(|b| b.iter().find(|x| x.node == node && x.kind == kind).cloned())
    });
    let snapshot = me.get_untracked();
    let (title, w) = snapshot.as_ref().map(|b| (b.title.clone(), b.w)).unwrap_or_default();
    let readonly = ix.readonly;
    let at = move || me.with(|b| b.as_ref().map_or(Point::default(), |b| Point::new(b.x, b.y)));
    let height = move || me.with(|b| b.as_ref().map_or(0.0, |b| b.h));
    let at_now = move || me.with_untracked(|b| b.as_ref().map_or(Point::default(), |b| Point::new(b.x, b.y)));
    let height_now = move || me.with_untracked(|b| b.as_ref().map_or(0.0, |b| b.h));
    let row_keys = Memo::new(move |_| me.with(|b| b.as_ref().map(|b| b.rows.iter().map(|r| r.key.clone()).collect::<Vec<_>>()).unwrap_or_default()));
    let rows = view! {
        <For
            each=move || row_keys.get()
            key=|k| k.clone()
            children={
                let (node, scope) = (node.clone(), scope.clone());
                move |key| row_view(ix, me, compatible, scope.clone(), clock.clone(), node.clone(), kind, w, key, on_toggle)
            }
        />
    };
    let (n_head, n_title, n_inspect, n_del) = (node.clone(), node.clone(), node.clone(), node);
    let head = (kind == BoxKind::Block).then(|| {
        let down = move |e: web_sys::PointerEvent, node: &str| ix.box_down(&e, node, kind, at_now(), height_now());
        let inspect_x = w - if readonly { 14.0 } else { 36.0 };
        let (down2, n_title2) = (down, n_title.clone());
        view! {
            <rect class="bbox-head" width=w height="28" rx="10" on:pointerdown=move |e| down(e, &n_head)></rect>
            <text class="bbox-title" x="10" y="18" on:pointerdown=move |e| down2(e, &n_title2)>{title.clone()}</text>
            <g
                class="bbtn inspect"
                transform=format!("translate({inspect_x} 14)")
                on:pointerdown=|e| e.stop_propagation()
                on:click=move |_| {
                    if let Some(c) = on_inspect {
                        c.run(n_inspect.clone());
                    }
                }
            >
                <title>"Заглянуть внутрь"</title>
                <circle r="9"></circle>
                <circle class="lens" r="3.2" cx="-0.8" cy="-0.8"></circle>
                <path class="lens" d="M1.6 1.6 L4.6 4.6"></path>
            </g>
            {(!readonly).then(|| view! {
                <g
                    class="bbtn del"
                    transform=format!("translate({} 14)", w - 14.0)
                    on:pointerdown=|e| e.stop_propagation()
                    on:click=move |_| ix.remove_instance(&n_del)
                >
                    <title>"Убрать блок с доски"</title>
                    <circle r="9"></circle>
                    <path d="M-3 -3 L3 3 M3 -3 L-3 3"></path>
                </g>
            })}
        }
    });
    let top_title = (kind != BoxKind::Block).then(|| view! { <text class="bbox-title top" x="10" y="18">{me.with_untracked(|b| b.as_ref().map(|b| b.title.clone()).unwrap_or_default())}</text> });
    view! {
        <g class="bbox" class:top=kind != BoxKind::Block transform=move || format!("translate({} {})", at().x, at().y)>
            <rect class="bbox-rect" width=w height=height rx="10"></rect>
            {head}
            {top_title}
            {rows}
        </g>
    }
}

/// Строка порта: подпись, значения (у колонок упражнения) и контакт.
#[allow(clippy::too_many_arguments)]
fn row_view(
    ix: Ix,
    owner: Memo<Option<BoxInfo>>,
    compatible: Memo<HashSet<String>>,
    scope: Scope,
    clock: Option<String>,
    node: String,
    kind: BoxKind,
    w: f64,
    key: String,
    on_toggle: Option<Callback<String>>,
) -> impl IntoView {
    let _ = node;
    let row = owner.with_untracked(|b| b.as_ref().and_then(|b| b.rows.iter().find(|r| r.key == key).cloned()));
    let Some(row) = row else { return ().into_any() };
    let readonly = ix.readonly;
    let y = Memo::new({
        let key = key.clone();
        move |_| owner.with(|b| b.as_ref().and_then(|b| b.rows.iter().find(|r| r.key == key).map(|r| r.y)).unwrap_or(0.0))
    });
    let expanded = Memo::new({
        let key = key.clone();
        move |_| owner.with(|b| b.as_ref().and_then(|b| b.rows.iter().find(|r| r.key == key).map(|r| r.expanded)).unwrap_or(false))
    });
    let dim = {
        let key = key.clone();
        move || ix.pending.with(Option::is_some) && !compatible.with(|c| c.contains(&key))
    };
    let hovered = {
        let key = key.clone();
        move || ix.hover.with(|h| h.as_deref() == Some(key.as_str()))
    };
    let depth = row.depth as f64;
    let ty = row.ty.name();
    let toggle_key = key.clone();
    let toggle = move |e: web_sys::PointerEvent| {
        e.stop_propagation();
        e.prevent_default();
        ix.expanded.update(|set| toggle_expanded(set, &toggle_key));
    };
    // стрелка раскрытия поля: слева у входов, справа у выходов
    let caret = row.expandable.then(|| {
        let (cx, tx) = if row.side_in { (8.0 + depth * 10.0, 15.0 + depth * 10.0) } else { (w - 22.0 - depth * 10.0, w - 15.0 - depth * 10.0) };
        view! {
            <g class="caret" on:pointerdown=toggle>
                <title>{move || if expanded.get() { "Свернуть поля" } else { "Показать поля" }}</title>
                <rect x=cx y="-9" width="14" height="18" rx="4"></rect>
                <text x=tx y="4" text-anchor="middle">{move || if expanded.get() { "▾" } else { "▸" }}</text>
            </g>
        }
    });
    let label = if row.side_in {
        let x = (if row.expandable { 26.0 } else { 12.0 }) + depth * 10.0;
        view! { <text class="blabel" x=x y="4">{row.name.clone()}<tspan class="btype">{format!(": {ty}")}</tspan></text> }.into_any()
    } else if kind != BoxKind::TopIn {
        let x = w - (if row.expandable { 26.0 } else { 12.0 }) - depth * 10.0;
        view! { <text class="blabel out" x=x y="4" text-anchor="end">{row.name.clone()}<tspan class="btype">{format!(": {ty}")}</tspan></text> }.into_any()
    } else {
        view! { <text class="blabel" x=10.0 + depth * 8.0 y="4">{row.name.clone()}</text> }.into_any()
    };
    let chips = match kind {
        BoxKind::TopIn => {
            let n = row.nodes.len();
            row.nodes
                .iter()
                .enumerate()
                .map(|(i, nd)| {
                    let x = w - 16.0 - (n - i) as f64 * 21.0 - if row.expandable { 18.0 } else { 0.0 };
                    let (v1, v2, nd2) = (nd.clone(), nd.clone(), nd.clone());
                    let (s1, s2) = (scope.clone(), scope.clone());
                    let is_clock = clock.as_deref() == Some(nd.as_str());
                    view! {
                        <g
                            class="bchip"
                            class:v1=move || s1(&v1) == Some(1)
                            class:clk=is_clock
                            class=("static", readonly)
                            transform=format!("translate({x} 0)")
                            on:pointerdown=|e| e.stop_propagation()
                            on:click=move |_| {
                                if !readonly {
                                    if let Some(c) = on_toggle {
                                        c.run(nd2.clone());
                                    }
                                }
                            }
                        >
                            {(!readonly).then(|| view! { <title>"Клик — переключить"</title> })}
                            <rect x="0" y="-9" width="18" height="18" rx="5"></rect>
                            <text x="9" y="4" text-anchor="middle">{move || s2(&v2).map_or_else(|| "?".to_string(), |b| b.to_string())}</text>
                        </g>
                    }
                })
                .collect_view()
                .into_any()
        }
        BoxKind::TopOut => {
            let chip_w = f64::max(18.0, row.nodes.len() as f64 * 8.0 + 8.0);
            let (nodes, s) = (row.nodes.clone(), scope.clone());
            let text = move || bus_text(&nodes.iter().map(|n| s(n)).collect::<Vec<_>>());
            view! {
                <g class="bchip out" transform=format!("translate({} 0)", w - 8.0 - chip_w)>
                    <rect x="0" y="-9" width=chip_w height="18" rx="5"></rect>
                    <text x=chip_w / 2.0 y="4" text-anchor="middle">{text}</text>
                </g>
            }
            .into_any()
        }
        BoxKind::Block => ().into_any(),
    };
    let cx = if row.side_in { 0.0 } else { w };
    let r = if row.nodes.len() > 1 { 6.5 } else { 5.0 };
    let (k_enter, k_leave) = (key.clone(), key);
    let row_for_down = row.clone();
    let tip = format!("{}: {}", row.name, ty);
    view! {
        <g class="brow" class:dim=dim class:hover=hovered transform=move || format!("translate(0 {})", y.get())>
            {caret}
            {label}
            {chips}
            <g
                class="bpin"
                on:pointerenter=move |_| {
                    if ix.pending.with_untracked(Option::is_some) {
                        ix.hover.set(Some(k_enter.clone()));
                    }
                }
                on:pointerleave=move |_| {
                    if ix.hover.with_untracked(|h| h.as_deref() == Some(k_leave.as_str())) {
                        ix.hover.set(None);
                    }
                }
            >
                <title>{tip}</title>
                <circle class="bpin-hit" cx=cx cy="0" r="12" on:pointerdown=move |e| ix.pin_down(&e, &row_for_down)></circle>
                <circle class="bpin-dot" cx=cx cy="0" r=r></circle>
            </g>
        </g>
    }
    .into_any()
}
