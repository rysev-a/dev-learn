//! Доска со схемой из вентилей: элементы, провода, входы-тумблеры и выходы упражнения (`GateBoard.tsx`).
//!
//! Всё, что касается мыши и холста: перенос элементов, провода (клик по контакту, затем по другому, или протянуть),
//! автоподстановка связей, сдвиг и масштаб. Схему (`gates`, `wires`) хозяйничает упражнение; доска меняет её через
//! сигналы и сообщает `on_edited`. Глобальные обработчики мыши висят на окне (как `document` в React), а чистые
//! решения — функции из `gate_logic.rs`.

use std::sync::Arc;

use archlab::{
    exercise::CircuitSpec,
    layout::{gate_pin_y, suggest_wires, AutoWire, AutoWireInput, AUTO_WIRE_RADIUS_DEFAULT, AUTO_WIRE_RADIUS_FACTOR},
    model::{
        input_ys, out_pin_x, output_ys, pin_pos, wire_path, GateInstance, GateType, InputId, InputState, NodeValue, PinKind, PinRef, UidGen, Values, Wire, YMap, BOARD_H, BOARD_W,
        INPUT_X, OUT_X,
    },
};
use leptos::{ev, prelude::*, svg};

use super::{
    check::value_in,
    common::{node_class, node_text, GateShape},
    gate_logic::{can_drop, connect, gate_origin, palette_drop_spot, remap_drop, remove_gate, Connect, DROP_ID},
    view::{clamp_world, is_background, is_click, js_round, target_within, use_element_width, use_fullscreen, world_height_for, ArchView, Point, ZoomControls},
};
use crate::{dom, settings};

/// Ключ настройки: высота доски (px), выбранная «лапкой».
const HEIGHT_KEY: &str = "say-lab-board-height";
const HEIGHT_MIN: f64 = 220.0;
const HEIGHT_MAX: f64 = 1400.0;
/// Сдвиг (единицы доски), с которого перенос элемента считается настоящим (включает автопроводку).
const MOVE_SLOP: f64 = 6.0;

fn clamp_height(h: f64) -> f64 {
    js_round(h.clamp(HEIGHT_MIN, HEIGHT_MAX))
}

fn saved_height() -> Option<f64> {
    settings::read(HEIGHT_KEY).and_then(|v| v.parse::<f64>().ok()).filter(|h| *h > 0.0).map(clamp_height)
}

fn bp(p: archlab::model::Point) -> Point {
    Point::new(p.x, p.y)
}

fn client(e: &web_sys::PointerEvent) -> Point {
    Point::new(f64::from(e.client_x()), f64::from(e.client_y()))
}

/// Элемент палитры: тип вентиля, закрыт ли он ещё (составные открываются сборкой вручную), подписи.
#[derive(Clone, Debug, PartialEq)]
pub struct PaletteItem {
    pub ty: GateType,
    pub locked: bool,
    pub title: String,
    pub label: String,
}

/// Перетаскиваемый элемент: смещение указателя внутри него, откуда начали, и точка нажатия на контакт.
#[derive(Clone, Copy, Default)]
struct DragInfo {
    off: Point,
    from: Point,
    pin_down: Option<Point>,
}

/// Значения сигналов на доске: по узлу и по входному контакту (значение провода, который в него идёт).
#[derive(Clone, Copy)]
struct Vals {
    values: Memo<Values>,
    wires: RwSignal<Vec<Wire>>,
}

impl Vals {
    fn node(&self, node: &str) -> NodeValue {
        self.values.with(|v| value_in(v, node))
    }

    fn pin(&self, node: &str, pin: PinKind) -> NodeValue {
        if pin == PinKind::Out {
            return self.node(node);
        }
        let source = self.wires.with(|ws| ws.iter().find(|w| w.to.node == node && w.to.pin == pin).map(|w| w.from.node.clone()));
        source.and_then(|s| self.node(&s))
    }
}

/// Состояние указателя на доске: что несут, что двигают, откуда тянут провод и какие связи предлагает автопроводка.
#[derive(Clone, Copy)]
struct Ix {
    gates: RwSignal<Vec<GateInstance>>,
    wires: RwSignal<Vec<Wire>>,
    view: ArchView,
    steps_mode: bool,
    auto_on: bool,
    palette: Signal<Vec<PaletteItem>>,
    uid: StoredValue<UidGen>,
    in_y: StoredValue<YMap>,
    out_y: StoredValue<YMap>,
    /// тип элемента, который несут из палитры
    placing: RwSignal<Option<GateType>>,
    /// положение курсора на экране, пока несут
    cursor: RwSignal<Option<Point>>,
    moving: RwSignal<Option<String>>,
    moved_far: RwSignal<bool>,
    /// откуда тянется провод
    pending: RwSignal<Option<PinRef>>,
    /// провод «прилип» к курсору после щелчка по контакту
    sticky: RwSignal<bool>,
    hover: RwSignal<Option<PinRef>>,
    cursor_board: RwSignal<Option<Point>>,
    drag: StoredValue<DragInfo>,
    auto_wires: Memo<Vec<AutoWire>>,
    on_edited: Callback<()>,
    on_message: Callback<String>,
    on_locked_pick: Callback<GateType>,
}

/// Связи автопроводки для элемента на его месте.
fn suggest(gate: &GateInstance, gates: &[GateInstance], wires: &[Wire], in_y: &YMap, out_y: &YMap, steps_mode: bool, keep: &[AutoWire]) -> Vec<AutoWire> {
    suggest_wires(&AutoWireInput {
        gate,
        gates,
        wires,
        input_y: in_y,
        output_y: out_y,
        steps_mode,
        radius: Some(AUTO_WIRE_RADIUS_DEFAULT * AUTO_WIRE_RADIUS_FACTOR),
        keep,
    })
}

impl Ix {
    fn pos(&self, r: &PinRef) -> Point {
        self.gates.with(|g| self.in_y.with_value(|iy| self.out_y.with_value(|oy| bp(pin_pos(r, g, oy, iy)))))
    }

    fn suggest_untracked(&self, gate: &GateInstance, keep: &[AutoWire]) -> Vec<AutoWire> {
        self.gates.with_untracked(|g| {
            self.wires.with_untracked(|w| self.in_y.with_value(|iy| self.out_y.with_value(|oy| suggest(gate, g, w, iy, oy, self.steps_mode, keep))))
        })
    }

    fn add_wires(&self, list: &[AutoWire]) {
        self.wires.update(|all| {
            for w in list {
                let id = self.uid.try_update_value(|u| u.next("w")).unwrap_or_default();
                all.push(Wire { id, from: w.from.clone(), to: w.to.clone() });
            }
        });
        self.on_edited.run(());
    }

    /// Ставит элемент `ty` с центром в `at`; `held` — связи, которые автопроводка предлагала для «призрака».
    fn place(&self, ty: GateType, at: Point, held: Option<Vec<AutoWire>>) {
        let o = gate_origin(at);
        let id = self.uid.try_update_value(|u| u.next("g")).unwrap_or_default();
        let gate = GateInstance { id: id.clone(), ty, x: o.x, y: o.y };
        let auto = match held {
            Some(h) if self.auto_on => self.suggest_untracked(&gate, &remap_drop(&h, &id)),
            _ => Vec::new(),
        };
        self.gates.update(|l| l.push(gate));
        if auto.is_empty() {
            self.on_edited.run(());
        } else {
            self.add_wires(&auto);
        }
    }

    fn try_connect(&self, a: PinRef, b: PinRef) {
        let wires = self.wires.get_untracked();
        let uid = self.uid;
        match connect(&wires, &a, &b, self.steps_mode, || uid.try_update_value(|u| u.next("w")).unwrap_or_default()) {
            Connect::Rejected(msg) => self.on_message.run(msg.to_string()),
            Connect::Cycle(rest) => {
                self.on_message.run("Так схема замкнётся в цикл — сигнал будет бежать по кругу".to_string());
                self.wires.set(rest);
                self.on_edited.run(());
            }
            Connect::Added(next) => {
                self.wires.set(next);
                self.on_edited.run(());
            }
        }
    }

    fn cancel_wire(&self) {
        self.pending.set(None);
        self.sticky.set(false);
        self.hover.set(None);
        self.cursor_board.set(None);
    }

    fn remove_wire(&self, id: &str) {
        self.wires.update(|l| l.retain(|w| w.id != id));
        self.on_edited.run(());
    }

    fn remove_gate(&self, id: &str) {
        let mut gates = self.gates.get_untracked();
        let mut wires = self.wires.get_untracked();
        remove_gate(&mut gates, &mut wires, id);
        self.gates.set(gates);
        self.wires.set(wires);
        self.on_edited.run(());
    }

    fn on_move(&self, e: &web_sys::PointerEvent) {
        let c = client(e);
        if self.view.move_pan(c.x, c.y) {
            return;
        }
        if self.placing.get_untracked().is_some() {
            self.cursor.set(Some(c));
            return;
        }
        if let Some(id) = self.moving.get_untracked() {
            let p = self.view.to_board(c.x, c.y);
            let d = self.drag.get_value();
            let o = clamp_world(Point::new(p.x - d.off.x, p.y - d.off.y), archlab::model::GATE_W, archlab::model::GATE_H);
            self.gates.update(|l| {
                if let Some(g) = l.iter_mut().find(|g| g.id == id) {
                    g.x = o.x;
                    g.y = o.y;
                }
            });
            if !self.moved_far.get_untracked() && (o.x - d.from.x).hypot(o.y - d.from.y) > MOVE_SLOP {
                self.moved_far.set(true);
            }
            return;
        }
        if self.pending.get_untracked().is_some() {
            self.cursor_board.set(Some(self.view.to_board(c.x, c.y)));
        }
    }

    fn on_up(&self, e: &web_sys::PointerEvent) {
        if self.view.end_pan() {
            return;
        }
        let c = client(e);
        if let Some(ty) = self.placing.get_untracked() {
            let held = self.auto_wires.get_untracked();
            self.placing.set(None);
            self.cursor.set(None);
            if target_within(e.target(), ".lab-board-svg") {
                self.place(ty, self.view.to_board(c.x, c.y), Some(held));
            } else if target_within(e.target(), ".lab-palette") {
                self.place(ty, palette_drop_spot(self.gates.with_untracked(Vec::len)), None);
            }
            return;
        }
        if self.moving.get_untracked().is_some() {
            let auto = self.auto_wires.get_untracked();
            self.moving.set(None);
            self.moved_far.set(false);
            if auto.is_empty() {
                self.on_edited.run(());
            } else {
                self.add_wires(&auto);
            }
            return;
        }
        let Some(pending) = self.pending.get_untracked() else { return };
        if self.sticky.get_untracked() {
            return;
        }
        match self.hover.get_untracked() {
            Some(target) if target != pending => {
                self.try_connect(pending, target);
                self.cancel_wire();
            }
            _ if self.drag.get_value().pin_down.is_some_and(|down| is_click(down, c)) => self.sticky.set(true),
            _ => self.cancel_wire(),
        }
    }

    fn board_down(&self, e: &web_sys::PointerEvent) {
        if self.sticky.get_untracked() && e.button() == 0 {
            self.cancel_wire();
            return;
        }
        let free = self.placing.get_untracked().is_none() && self.pending.get_untracked().is_none();
        self.view.on_pointer_down(e, free && is_background(e.target(), "lab-board-bg"));
    }

    fn gate_down(&self, e: &web_sys::PointerEvent, g: &GateInstance) {
        if e.button() != 0 {
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
            d.off = Point::new(p.x - g.x, p.y - g.y);
            d.from = Point::new(g.x, g.y);
        });
        self.moved_far.set(false);
        self.moving.set(Some(g.id.clone()));
    }

    fn pin_down(&self, e: &web_sys::PointerEvent, node: &str, pin: PinKind) {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        e.stop_propagation();
        let me = PinRef { node: node.to_string(), pin };
        if let Some(from) = self.pending.get_untracked().filter(|_| self.sticky.get_untracked()) {
            self.cancel_wire();
            if from != me {
                self.try_connect(from, me);
            }
            return;
        }
        let c = client(e);
        self.pending.set(Some(me));
        self.sticky.set(false);
        self.drag.update_value(|d| d.pin_down = Some(c));
        self.hover.set(None);
        self.cursor_board.set(Some(self.view.to_board(c.x, c.y)));
    }

    fn pin_enter(&self, node: &str, pin: PinKind) {
        if self.pending.get_untracked().is_some() {
            self.hover.set(Some(PinRef { node: node.to_string(), pin }));
        }
    }

    fn pin_leave(&self, node: &str, pin: PinKind) {
        if self.hover.with_untracked(|h| h.as_ref().is_some_and(|h| h.node == node && h.pin == pin)) {
            self.hover.set(None);
        }
    }

    fn start_place(&self, e: &web_sys::PointerEvent, ty: GateType) {
        if e.button() != 0 {
            return;
        }
        if self.palette.with_untracked(|p| p.iter().any(|i| i.ty == ty && i.locked)) {
            self.on_locked_pick.run(ty);
            return;
        }
        e.prevent_default();
        self.placing.set(Some(ty));
        self.cursor.set(Some(client(e)));
    }
}

/// Доска вентилей упражнения.
#[component]
pub fn GateBoard(
    gates: RwSignal<Vec<GateInstance>>,
    wires: RwSignal<Vec<Wire>>,
    spec: Arc<CircuitSpec>,
    input_state: RwSignal<InputState>,
    steps_mode: bool,
    values: Memo<Values>,
    #[prop(into)] palette: Signal<Vec<PaletteItem>>,
    uid: StoredValue<UidGen>,
    on_toggle_input: Callback<InputId>,
    on_edited: Callback<()>,
    on_message: Callback<String>,
    on_locked_pick: Callback<GateType>,
) -> impl IntoView {
    let svg_ref = NodeRef::<svg::Svg>::new();
    let width = use_element_width(svg_ref);
    let board_h = RwSignal::new(saved_height());
    let resize = RwSignal::new(None::<(f64, f64)>);
    // высота меняется без смены масштаба: видимое окно мира растёт вместе с высотой
    let fullscreen = use_fullscreen();
    let manual = Memo::new(move |_| board_h.get().filter(|_| !fullscreen()).and_then(|h| world_height_for(h, width.get(), BOARD_W)));
    let world = Signal::derive(move || (BOARD_W, manual.get().unwrap_or(BOARD_H)));
    let view = ArchView::new(svg_ref, world);

    let in_y = StoredValue::new(input_ys(&spec.inputs));
    let out_y = StoredValue::new(output_ys(&spec.outputs));
    let placing = RwSignal::new(None::<GateType>);
    let cursor = RwSignal::new(None::<Point>);
    let moving = RwSignal::new(None::<String>);
    let moved_far = RwSignal::new(false);
    let keep = StoredValue::new(Vec::<AutoWire>::new());
    let auto_on = settings::AUTOWIRE_LAB_FLAG.read();

    let drop_gate = Memo::new(move |_| {
        let (ty, at) = (placing.get()?, cursor.get()?);
        if !view.contains_client(at) {
            return None;
        }
        let o = gate_origin(view.to_board(at.x, at.y));
        Some(GateInstance { id: DROP_ID.to_string(), ty, x: o.x, y: o.y })
    });
    let auto_wires = Memo::new(move |_| {
        if !auto_on {
            return Vec::new();
        }
        let gate = match moving.get() {
            Some(id) => moved_far.get().then(|| gates.with(|l| l.iter().find(|g| g.id == id).cloned())).flatten(),
            None => drop_gate.get(),
        };
        let list = gate
            .map(|g| {
                let held = keep.get_value();
                gates.with(|gs| wires.with(|ws| in_y.with_value(|iy| out_y.with_value(|oy| suggest(&g, gs, ws, iy, oy, steps_mode, &held)))))
            })
            .unwrap_or_default();
        keep.set_value(list.clone());
        list
    });

    let ix = Ix {
        gates,
        wires,
        view,
        steps_mode,
        auto_on,
        palette,
        uid,
        in_y,
        out_y,
        placing,
        cursor,
        moving,
        moved_far,
        pending: RwSignal::new(None),
        sticky: RwSignal::new(false),
        hover: RwSignal::new(None),
        cursor_board: RwSignal::new(None),
        drag: StoredValue::new(DragInfo::default()),
        auto_wires,
        on_edited,
        on_message,
        on_locked_pick,
    };
    let vals = Vals { values, wires };

    dom::on_window(ev::pointermove, move |e| {
        if let Some((y0, h0)) = resize.get_untracked() {
            board_h.set(Some(clamp_height(h0 + f64::from(e.client_y()) - y0)));
            return;
        }
        ix.on_move(&e);
    });
    dom::on_window(ev::pointerup, move |e| {
        if resize.get_untracked().is_some() {
            resize.set(None);
            settings::write(HEIGHT_KEY, board_h.get_untracked().map(|h| h.to_string()).as_deref());
            return;
        }
        ix.on_up(&e);
    });
    dom::on_window(ev::keydown, move |e| {
        if e.key() == "Escape" {
            ix.cancel_wire();
        }
    });

    // «лапка» под полем: потянуть вверх или вниз — доска меняет высоту
    let start_resize = move |e: web_sys::PointerEvent| {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        let h = board_h.get_untracked().or_else(|| svg_ref.get_untracked().map(|s| s.get_bounding_client_rect().height())).unwrap_or(330.0);
        resize.set(Some((f64::from(e.client_y()), h)));
    };
    let resize_key = move |e: web_sys::KeyboardEvent| {
        let step = match e.key().as_str() {
            "ArrowDown" => 24.0,
            "ArrowUp" => -24.0,
            _ => return,
        };
        e.prevent_default();
        if let Some(svg) = svg_ref.get_untracked() {
            let h = clamp_height(svg.get_bounding_client_rect().height() + step);
            board_h.set(Some(h));
            settings::write(HEIGHT_KEY, Some(&h.to_string()));
        }
    };

    let gate_keys = Memo::new(move |_| gates.with(|g| g.iter().map(|x| (x.id.clone(), x.ty)).collect::<Vec<_>>()));
    let wire_ids = Memo::new(move |_| wires.with(|w| w.iter().map(|x| x.id.clone()).collect::<Vec<_>>()));

    let preview = Memo::new(move |_| {
        let pending = ix.pending.get()?;
        let end = match ix.hover.get() {
            Some(h) => ix.pos(&h),
            None => ix.cursor_board.get()?,
        };
        let ok = ix.hover.with(|h| h.as_ref().is_some_and(|h| can_drop(&pending, h)));
        let to = archlab::model::Point { x: end.x, y: end.y };
        let from = archlab::model::Point { x: ix.pos(&pending).x, y: ix.pos(&pending).y };
        Some((wire_path(from, to), ok))
    });

    let palette_buttons = move || {
        palette
            .get()
            .into_iter()
            .map(|item| {
                let ty = item.ty;
                view! {
                    <button
                        type="button"
                        class="lab-pal-sq"
                        class:locked=item.locked
                        title=item.title.clone()
                        aria-label=item.label.clone()
                        on:pointerdown=move |e| ix.start_place(&e, ty)
                    >
                        <svg viewBox="-12 0 96 48" aria-hidden="true" style="overflow: visible"><GateShape ty=ty label=false /></svg>
                        {item.locked.then(|| view! { <span class="lab-pal-lock">"🔒"</span> })}
                    </button>
                }
            })
            .collect_view()
    };

    let inputs = spec.inputs.clone();
    let input_nodes = inputs.into_iter().map(|id| input_node(ix, vals, input_state, &spec, id, on_toggle_input)).collect_view();
    let output_nodes = spec.outputs.iter().map(|o| output_node(ix, vals, o.clone())).collect_view();

    view! {
        <div class="lab-board" class:fill=fullscreen>
            {move || (!palette.with(Vec::is_empty)).then(|| view! {
                <div class="lab-palette" role="toolbar" aria-label="Элементы: перетащите на доску или кликните">{palette_buttons()}</div>
            })}
            <ZoomControls view=view />
            <svg
                node_ref=svg_ref
                class="lab-board-svg"
                class:panning=move || view.panning.get()
                viewBox=move || view.view_box()
                style=move || manual.get().and(board_h.get()).map(|h| format!("height: {h}px")).unwrap_or_default()
                role="img"
                aria-label="Интерактивная доска с логическими элементами"
                on:pointerdown=move |e| ix.board_down(&e)
                on:wheel=move |e| view.on_wheel(&e, false)
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
                    <pattern id="lab-dots" width="22" height="22" patternUnits="userSpaceOnUse">
                        <circle cx="1.5" cy="1.5" r="1.5" class="grid-dot"></circle>
                    </pattern>
                </defs>
                <rect
                    class="lab-board-bg"
                    x=move || view.pan.get().x.to_string()
                    y=move || view.pan.get().y.to_string()
                    width=move || (BOARD_W / view.zoom.get()).to_string()
                    height=move || (world.get().1 / view.zoom.get()).to_string()
                    fill="url(#lab-dots)"
                ></rect>
                <For each=move || wire_ids.get() key=|id| id.clone() children=move |id| wire_view(ix, vals, id) />
                {input_nodes}
                {output_nodes}
                <For each=move || gate_keys.get() key=|k| k.clone() children=move |(id, ty)| gate_view(ix, vals, id, ty) />
                {move || auto_wires.get().into_iter().map(|w| view! { <path class="wire-auto" d=wire_path(w.a, w.b)></path> }).collect_view()}
                {move || preview.get().map(|(d, ok)| view! { <path class="wire-preview" class:ok=ok d=d></path> })}
            </svg>
            {move || (!fullscreen()).then(|| view! {
                <button
                    type="button"
                    class="lab-resize-grip"
                    role="separator"
                    aria-orientation="horizontal"
                    aria-label="Высота доски: потяните вверх или вниз, либо стрелками"
                    title="Потяните, чтобы изменить высоту доски (двойной щелчок — по умолчанию)"
                    on:pointerdown=start_resize
                    on:dblclick=move |_| {
                        board_h.set(None);
                        settings::write(HEIGHT_KEY, None);
                    }
                    on:keydown=resize_key
                >
                    <svg viewBox="0 0 28 8" aria-hidden="true"><path d="M2 2h24M2 6h24"></path></svg>
                </button>
            })}
            {move || placing.get().map(|ty| view! {
                <div class="lab-ghost" style=move || cursor.get().map(|at| format!("left: {}px; top: {}px", at.x, at.y)).unwrap_or_default() aria-hidden="true">
                    <svg viewBox="0 0 84 48" width="56" height="32"><GateShape ty=ty label=false /></svg>
                </div>
            })}
        </div>
    }
}

/// Провод: линия, цвет которой зависит от сигнала, и широкая полоса для щелчка (клик — удалить).
fn wire_view(ix: Ix, vals: Vals, id: String) -> impl IntoView {
    let wire = Memo::new({
        let id = id.clone();
        move |_| ix.wires.with(|ws| ws.iter().find(|w| w.id == id).cloned())
    });
    let d = move || {
        wire.get()
            .map(|w| {
                let (a, b) = (ix.pos(&w.from), ix.pos(&w.to));
                wire_path(archlab::model::Point { x: a.x, y: a.y }, archlab::model::Point { x: b.x, y: b.y })
            })
            .unwrap_or_default()
    };
    let class = move || format!("wire-line {}", node_class(wire.get().and_then(|w| vals.node(&w.from.node))));
    view! {
        <g
            class="wire"
            on:pointerdown=move |e| {
                if e.button() == 0 {
                    ix.remove_wire(&id);
                }
            }
        >
            <title>"Клик — удалить провод"</title>
            <path class="wire-hit" d=d></path>
            <path class=class d=d></path>
        </g>
    }
}

/// Контакт: невидимый круг для мыши и цветная точка сигнала.
fn pin_view(ix: Ix, node: String, pin: PinKind, value: impl Fn() -> NodeValue + Send + Sync + 'static, cx: f64, cy: f64) -> impl IntoView {
    let (n1, n2, n3) = (node.clone(), node.clone(), node);
    view! {
        <g class="pin" on:pointerenter=move |_| ix.pin_enter(&n1, pin) on:pointerleave=move |_| ix.pin_leave(&n2, pin)>
            <circle class="pin-hit" cx=cx cy=cy r="13" on:pointerdown=move |e| ix.pin_down(&e, &n3, pin)></circle>
            <circle class=move || format!("pin-dot {}", node_class(value())) cx=cx cy=cy r="5.5"></circle>
        </g>
    }
}

/// Вход-тумблер на левом краю: клик переключает, от точки справа тянут провод.
fn input_node(ix: Ix, vals: Vals, input_state: RwSignal<InputState>, spec: &CircuitSpec, id: InputId, toggle: Callback<InputId>) -> impl IntoView {
    let y = ix.in_y.with_value(|m| m.get(id.as_str())).unwrap_or(200.0);
    let label = spec.label_of(id);
    let is_clock = spec.clock == Some(id);
    let level = move || input_state.with(|s| s.get(id));
    let name = id.as_str().to_string();
    let title_label = label.clone();
    view! {
        <g class="input-node" class:is-clock=is_clock>
            <g
                class="node-click"
                on:pointerdown=move |e| {
                    if e.button() == 0 {
                        toggle.run(id);
                    }
                }
            >
                <title>{move || format!("Клик — переключить {title_label} ({} → {})", level(), 1 - level())}</title>
                <rect class="node-box" x="10" y=y - 22.0 width="86" height="44" rx="10"></rect>
                <text class="node-label" x="30" y=y + 5.0>{label}</text>
                <rect class=move || format!("node-chip {}", node_class(Some(level()))) x="56" y=y - 12.0 width="26" height="24" rx="7"></rect>
                <text class="node-chip-text" x="69" y=y + 5.0>{move || level().to_string()}</text>
            </g>
            {pin_view(ix, name.clone(), PinKind::Out, move || vals.node(&name), INPUT_X, y)}
        </g>
    }
}

/// Выход упражнения на правом краю: значение и контакт, к которому подводят провод.
fn output_node(ix: Ix, vals: Vals, name: String) -> impl IntoView {
    let y = ix.out_y.with_value(|m| m.get(&name)).unwrap_or(200.0);
    let (n_chip, n_text, n_pin) = (name.clone(), name.clone(), name.clone());
    view! {
        <g class="out-node">
            <rect class="node-box out-box" x="788" y=y - 22.0 width="86" height="44" rx="10"></rect>
            <text class="node-label" x="812" y=y + 5.0>{name.clone()}</text>
            <rect class=move || format!("node-chip {}", node_class(vals.node(&n_chip))) x="834" y=y - 12.0 width="26" height="24" rx="7"></rect>
            <text class="node-chip-text" x="847" y=y + 5.0>{move || node_text(vals.node(&n_text))}</text>
            {pin_view(ix, name, PinKind::In0, move || vals.pin(&n_pin, PinKind::In0), OUT_X, y)}
        </g>
    }
}

/// Вентиль: контур, контакты, кнопка удаления и «щуп» со значением выхода.
fn gate_view(ix: Ix, vals: Vals, id: String, ty: GateType) -> impl IntoView {
    let at = Memo::new({
        let id = id.clone();
        move |_| ix.gates.with(|l| l.iter().find(|g| g.id == id).map(|g| (g.x, g.y)).unwrap_or((0.0, 0.0)))
    });
    let me = {
        let id = id.clone();
        move || GateInstance { id: id.clone(), ty, x: at.get_untracked().0, y: at.get_untracked().1 }
    };
    let out_x = out_pin_x(ty);
    let in_pins = ty
        .pins()
        .iter()
        .map(|pin| {
            let (pin, node) = (*pin, id.clone());
            let py = gate_pin_y(ty, pin);
            let n_val = node.clone();
            view! {
                <g transform=format!("translate(-8 {py})")>{pin_view(ix, node, pin, move || vals.pin(&n_val, pin), 0.0, 0.0)}</g>
            }
        })
        .collect_view();
    let (del_id, out_id, probe_id, cls_id) = (id.clone(), id.clone(), id.clone(), id.clone());
    let out_probe = probe_id.clone();
    view! {
        <g
            class="gate"
            class:dragging=move || ix.moving.with(|m| m.as_deref() == Some(cls_id.as_str()))
            transform=move || format!("translate({} {})", at.get().0, at.get().1)
            on:pointerdown=move |e| ix.gate_down(&e, &me())
        >
            <GateShape ty=ty />
            <g
                class="gate-del"
                on:pointerdown=|e| e.stop_propagation()
                on:click=move |_| ix.remove_gate(&del_id)
            >
                <title>"Удалить элемент"</title>
                <circle cx="76" cy="0" r="8"></circle>
                <path d="M73 -3 L79 3 M79 -3 L73 3"></path>
            </g>
            {in_pins}
            {pin_view(ix, out_id, PinKind::Out, move || vals.node(&out_probe), out_x, 24.0)}
            <g class="probe" transform=format!("translate({} 24)", out_x + 20.0)>
                <circle r="9"></circle>
                <text y="3.5" text-anchor="middle">{move || node_text(vals.node(&probe_id))}</text>
            </g>
        </g>
    }
}
