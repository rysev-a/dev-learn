//! Поле схемы (по мотивам досок лаборатории «Архитектура компьютера»):
//! — у компонента порты: вход слева, выход справа; связь тянут от выхода ко входу (или кликают по двум портам);
//! — компоненты перетаскиваются, из палитры их можно перетащить прямо на поле;
//! — подходящие соседи соединяются сами (пунктир-подсказка, пока компонент двигают);
//! — поле можно сдвигать (пустое место, средняя кнопка) и масштабировать (Ctrl + колесо, кнопки).
//!
//! Состояние указателя — сигналы в [`Ix`]; глобальные обработчики мыши висят на окне (как `document` в React), а чистые
//! решения («что под курсором», «можно ли соединить», «как вписать схему») — функции из `logic.rs`.

use leptos::{ev, prelude::*, svg};
use sdlab::{
    kinds,
    layout::BOARD_W,
    ports::{has_in, has_out, suggest_edges, AUTO_RADIUS, NODE_H, NODE_W},
    Kind, NodeLoad, NodeStatus, SdEdge, SdNode,
};
use wasm_bindgen::JsCast;

use super::{
    icons,
    lab::Lab,
    logic::{self, Pending, Pin, BOARD, MAX_H, MIN_H, MOVE_SLOP},
};
use crate::{
    components::labs::board_view::{is_background, js_round, target_within, use_element_size, BoardView, ItemDrag, Point, View, ZoomControls},
    dom, settings,
};

/// Ключ настройки: высота поля (px), выбранная «лапкой».
const BOARD_H_KEY: &str = "say-sd-board-h";

/// Высота поля из настроек; вне допустимых пределов — не задана.
fn saved_height() -> Option<f64> {
    settings::read(BOARD_H_KEY).and_then(|v| v.parse::<f64>().ok()).filter(|h| (MIN_H..=MAX_H).contains(h))
}

fn clamp_height(h: f64) -> f64 {
    js_round(h.clamp(MIN_H, MAX_H))
}

fn client(e: &web_sys::PointerEvent) -> Point {
    Point::new(f64::from(e.client_x()), f64::from(e.client_y()))
}

/// Класс узла по состоянию нагрузки.
fn status_class(s: NodeStatus) -> &'static str {
    match s {
        NodeStatus::Idle => "idle",
        NodeStatus::Ok => "ok",
        NodeStatus::Warm => "warm",
        NodeStatus::Hot => "hot",
        NodeStatus::Over => "over",
        NodeStatus::Down => "down",
    }
}

/// Ширина полоски загрузки узла (px внутри рамки): не уже 2.
fn bar_width(util: f64) -> f64 {
    (util.min(1.0) * (NODE_W - 16.0)).max(2.0)
}

fn target_element(target: Option<web_sys::EventTarget>) -> Option<web_sys::Element> {
    target.and_then(|t| t.dyn_into::<web_sys::Element>().ok())
}

/// Фокус в поле ввода: клавиши Delete и Backspace там работают как обычно.
fn typing_in_field(target: Option<web_sys::EventTarget>) -> bool {
    target_element(target).is_some_and(|el| ["INPUT", "SELECT", "TEXTAREA"].contains(&el.tag_name().to_ascii_uppercase().as_str()))
}

/// Перетаскиваемый компонент и точка нажатия на порт (экранная).
#[derive(Clone, Copy, Default)]
struct DragInfo {
    item: ItemDrag,
    pin_down: Option<Point>,
}

/// Состояние указателя на поле: что тянут, куда целятся и какие связи предлагают.
#[derive(Clone, Copy)]
struct Ix {
    lab: Lab,
    view: BoardView,
    /// вид компонента, который тащат из палитры
    placing: RwSignal<Option<Kind>>,
    /// положение курсора на экране, пока тащат из палитры
    cursor: RwSignal<Option<Point>>,
    /// компонент, который двигают
    moving: RwSignal<Option<String>>,
    moved_far: RwSignal<bool>,
    /// провод, который тянут от порта
    pending: RwSignal<Option<Pending>>,
    /// провод «приклеился» к курсору после щелчка по порту
    sticky: RwSignal<bool>,
    cursor_board: RwSignal<Option<Point>>,
    /// компонент под концом провода
    hover: RwSignal<Option<String>>,
    drag: StoredValue<DragInfo>,
    /// призрак компонента из палитры под курсором
    ghost: Memo<Option<SdNode>>,
    /// связи, которые предлагает автоподстановка
    auto_edges: Memo<Vec<SdEdge>>,
}

impl Ix {
    fn new(lab: Lab, view: BoardView) -> Self {
        let placing = RwSignal::new(None::<Kind>);
        let cursor = RwSignal::new(None::<Point>);
        let moving = RwSignal::new(None::<String>);
        let moved_far = RwSignal::new(false);

        let ghost = Memo::new(move |_| {
            let (kind, at) = (placing.get()?, cursor.get()?);
            if !view.contains_client(at) {
                return None;
            }
            Some(logic::ghost_node(kind, view.to_board(at.x, at.y)))
        });
        // автоподстановка: включена по настройке (читается при открытии доски); прежний результат нужен, чтобы пунктир не дрожал
        let auto_on = settings::AUTOWIRE_SD_FLAG.read();
        let auto_edges = Memo::new(move |keep: Option<&Vec<SdEdge>>| {
            if !auto_on {
                return Vec::new();
            }
            let node = match moving.get() {
                Some(id) => moved_far.get().then(|| lab.state.with(|s| s.node(&id).cloned())).flatten(),
                None => ghost.get(),
            };
            let keep = keep.map(Vec::as_slice).unwrap_or_default();
            node.map(|n| lab.state.with(|s| suggest_edges(s, &n, keep, AUTO_RADIUS))).unwrap_or_default()
        });

        Self {
            lab,
            view,
            placing,
            cursor,
            moving,
            moved_far,
            pending: RwSignal::new(None),
            sticky: RwSignal::new(false),
            cursor_board: RwSignal::new(None),
            hover: RwSignal::new(None),
            drag: StoredValue::new(DragInfo::default()),
            ghost,
            auto_edges,
        }
    }

    fn cancel_wire(&self) {
        self.pending.set(None);
        self.sticky.set(false);
        self.hover.set(None);
        self.cursor_board.set(None);
    }

    fn connect_pending(&self, p: &Pending, other: &str) {
        let (from, to) = logic::pin_edge(p, other);
        self.lab.connect(&from, &to);
    }

    /// Нажатие на компонент: либо завершает «приклеенный» провод, либо начинает перетаскивание.
    fn node_down(&self, e: &web_sys::PointerEvent, id: &str) {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        if let Some(p) = self.pending.get_untracked().filter(|_| self.sticky.get_untracked()) {
            self.cancel_wire();
            if p.id != id {
                self.connect_pending(&p, id);
            }
            return;
        }
        let at = self.view.to_board(f64::from(e.client_x()), f64::from(e.client_y()));
        let Some((x, y)) = self.lab.state.with_untracked(|s| s.node(id).map(|n| (n.x, n.y))) else { return };
        self.drag.set_value(DragInfo { item: ItemDrag::start(at, Point::new(x, y)), pin_down: None });
        self.moved_far.set(false);
        self.moving.set(Some(id.to_owned()));
    }

    /// Нажатие на порт: начало провода или соединение с «приклеенным» проводом.
    fn pin_down(&self, e: &web_sys::PointerEvent, id: &str, pin: Pin) {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        e.stop_propagation();
        if let Some(p) = self.pending.get_untracked().filter(|_| self.sticky.get_untracked()) {
            self.cancel_wire();
            if p.id != id && p.pin != pin {
                self.connect_pending(&p, id);
            }
            return;
        }
        self.pending.set(Some(Pending { id: id.to_owned(), pin }));
        self.sticky.set(false);
        self.drag.update_value(|d| d.pin_down = Some(client(e)));
        self.hover.set(None);
        self.cursor_board.set(Some(self.view.to_board(f64::from(e.client_x()), f64::from(e.client_y()))));
    }

    /// Нажатие на фон поля: отменяет провод, снимает выбор и начинает сдвиг; средняя кнопка двигает поле везде.
    fn board_down(&self, e: &web_sys::PointerEvent) {
        if e.button() == 1 {
            self.view.on_pointer_down(e, false);
            return;
        }
        if e.button() != 0 || self.placing.get_untracked().is_some() {
            return;
        }
        if !is_background(e.target(), "sd-bg") {
            return;
        }
        if self.pending.get_untracked().is_some() {
            self.cancel_wire();
            return;
        }
        self.lab.select_node(None);
        self.lab.select_edge(None);
        self.view.on_pointer_down(e, true);
    }

    fn on_move(&self, e: &web_sys::PointerEvent) {
        let at = client(e);
        if self.view.move_pan(at.x, at.y) {
            return;
        }
        if self.placing.get_untracked().is_some() {
            self.cursor.set(Some(at));
            return;
        }
        if let Some(id) = self.moving.get_untracked() {
            let item = self.drag.get_value().item;
            let to = BOARD.items.snap(item.at(self.view.to_board(at.x, at.y)));
            self.lab.move_node(&id, to.x, to.y, false);
            if !self.moved_far.get_untracked() && item.moved_far(to, MOVE_SLOP) {
                self.moved_far.set(true);
            }
            return;
        }
        if let Some(p) = self.pending.get_untracked() {
            let b = self.view.to_board(at.x, at.y);
            self.cursor_board.set(Some(b));
            self.hover.set(self.lab.state.with_untracked(|s| logic::node_at(s, &p.id, b)));
        }
    }

    fn on_up(&self, e: &web_sys::PointerEvent) {
        let at = client(e);
        if self.view.end_pan() {
            return;
        }
        if let Some(kind) = self.placing.get_untracked() {
            let held = self.auto_edges.get_untracked();
            self.placing.set(None);
            self.cursor.set(None);
            if target_within(e.target(), ".sd-board") {
                let p = self.view.to_board(at.x, at.y);
                self.lab.add(kind, Some(BOARD.items.snap(p)), &held);
            }
            return;
        }
        if let Some(id) = self.moving.get_untracked() {
            let auto = self.auto_edges.get_untracked();
            let far = self.moved_far.get_untracked();
            self.moving.set(None);
            self.moved_far.set(false);
            if far {
                if let Some((x, y)) = self.lab.state.with_untracked(|s| s.node(&id).map(|n| (n.x, n.y))) {
                    self.lab.move_node(&id, x, y, true);
                }
                if !auto.is_empty() {
                    self.lab.apply_edges(&auto);
                }
            } else {
                self.lab.select_node(Some(id));
            }
            return;
        }
        if let Some(p) = self.pending.get_untracked().filter(|_| !self.sticky.get_untracked()) {
            let b = self.view.to_board(at.x, at.y);
            let target = self.lab.state.with_untracked(|s| logic::node_at(s, &p.id, b));
            match target {
                Some(t) => {
                    self.connect_pending(&p, &t);
                    self.cancel_wire();
                }
                None if self.drag.get_value().pin_down.is_some_and(|d| self.view.is_click(d, at)) => self.sticky.set(true),
                None => self.cancel_wire(),
            }
        }
    }

    fn on_key(&self, e: &web_sys::KeyboardEvent) {
        match e.key().as_str() {
            "Escape" => self.cancel_wire(),
            "Delete" | "Backspace" if !typing_in_field(e.target()) => self.lab.remove_selected(),
            _ => {}
        }
    }
}

/// Палитра, поле и подсказка под ним.
#[component]
pub fn Board(
    lab: Lab,
    /// поле занимает весь экран: высота окна берётся из размеров на экране
    fullscreen: bool,
    /// кнопки в левом верхнем углу поля (справка, во весь экран)
    #[prop(into)]
    corner: ViewFn,
    /// плавающая карточка поверх поля (параметры выбранного компонента)
    #[prop(into)]
    overlay: ViewFn,
) -> impl IntoView {
    let svg_ref = NodeRef::<svg::Svg>::new();
    let size = use_element_size(svg_ref);
    // высота поля, выбранная «лапкой» (px); пока не трогали — поле держит пропорции окна просмотра
    let board_h = RwSignal::new(saved_height());
    let resize = RwSignal::new(None::<(f64, f64)>);
    let sized = move || fullscreen || board_h.get().is_some();
    let world_h = Memo::new(move |_| {
        let (w, h) = size.get();
        logic::world_height(sized(), w, h)
    });
    let view = BoardView::new(svg_ref, BOARD, Signal::derive(move || (BOARD_W, world_h.get())));
    let ix = Ix::new(lab, view);

    // вписать всю схему в окно просмотра
    let fitted = RwSignal::new(None::<View>);
    let fit = Callback::new(move |()| {
        let points: Vec<Point> = lab.state.with_untracked(|s| s.nodes.iter().map(|n| Point::new(n.x, n.y)).collect());
        let v = logic::fit_view(&points, world_h.get_untracked());
        view.set_view(v);
        fitted.set(Some(v));
    });
    let did_fit = StoredValue::new(false);
    Effect::new(move |_| {
        if size.get().0 > 0.0 && !did_fit.get_value() {
            did_fit.set_value(true);
            fit.run(());
        }
    });
    let changed = Memo::new(move |_| fitted.get().is_none_or(|f| f != view.view()));

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
            settings::write(BOARD_H_KEY, board_h.get_untracked().map(|h| h.to_string()).as_deref());
            return;
        }
        ix.on_up(&e);
    });
    dom::on_window(ev::keydown, move |e| ix.on_key(&e));

    // «лапка» под полем: потянуть вверх или вниз — поле меняет высоту
    let start_resize = move |e: web_sys::PointerEvent| {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        let h = board_h.get_untracked().or_else(|| svg_ref.get_untracked().map(|s| s.get_bounding_client_rect().height())).unwrap_or(420.0);
        resize.set(Some((f64::from(e.client_y()), h)));
    };

    let node_keys = Memo::new(move |_| lab.state.with(|s| s.nodes.iter().map(|n| (n.id.clone(), n.kind)).collect::<Vec<_>>()));
    let edges = Memo::new(move |_| lab.state.with(|s| s.edges.clone()));
    let wire = Memo::new(move |_| ix.pending.get().and_then(|p| lab.state.with(|s| logic::pending_wire(s, &p, ix.hover.get().as_deref(), ix.cursor_board.get()))));
    let wire_shown = Memo::new(move |_| wire.with(Option::is_some));
    let ghost_shown = Memo::new(move |_| ix.ghost.with(Option::is_some));

    let palette = lab.scenario().palette.clone();
    let buttons = palette
        .into_iter()
        .map(|kind| {
            let spec = kinds::spec(kind);
            view! {
                <button
                    type="button"
                    class="sd-add"
                    title=format!("{}. Перетащите на поле — связи подставятся сами.", spec.about)
                    on:pointerdown=move |e| {
                        if e.button() != 0 {
                            return;
                        }
                        e.prevent_default();
                        ix.placing.set(Some(kind));
                        ix.cursor.set(Some(client(&e)));
                    }
                    on:click=move |_| {
                        // после клика схема вписывается заново: новый компонент не должен оказаться за краем
                        if lab.add(kind, None, &[]) {
                            fit.run(());
                        }
                    }
                >
                    {format!("+ {}", spec.label)}
                </button>
            }
        })
        .collect_view();

    view! {
        <div class="sd-boardwrap" class:fill=fullscreen>
            <div class="sd-toolbar" role="toolbar" aria-label="Компоненты: перетащите на поле или кликните">{buttons}</div>
            <div
                class="sd-viewport"
                class:sized=move || board_h.get().is_some() && !fullscreen
                style=move || match board_h.get() {
                    Some(h) if !fullscreen => format!("height: {h}px"),
                    _ => String::new(),
                }
            >
                {corner.run()}
                {overlay.run()}
                <ZoomControls view=view changed=changed on_reset=fit />
                {(!fullscreen).then(|| view! {
                    <div
                        class="sd-resize"
                        role="separator"
                        aria-orientation="horizontal"
                        aria-label="Высота схемы"
                        title="Потяните, чтобы изменить высоту схемы (двойной клик — по умолчанию)"
                        on:pointerdown=start_resize
                        on:dblclick=move |_| {
                            board_h.set(None);
                            settings::write(BOARD_H_KEY, None);
                        }
                    >
                        <i></i>
                    </div>
                })}
                <svg
                    node_ref=svg_ref
                    class="sd-board"
                    class:panning=move || view.panning.get()
                    class:placing=move || ix.placing.get().is_some()
                    viewBox=move || view.view_box()
                    role="img"
                    aria-label="Схема сервиса"
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
                        <pattern id="sd-dots" width="22" height="22" patternUnits="userSpaceOnUse">
                            <circle cx="1.5" cy="1.5" r="1.3" class="sd-dot"></circle>
                        </pattern>
                    </defs>
                    <rect
                        class="sd-bg"
                        x=move || view.pan.get().x.to_string()
                        y=move || view.pan.get().y.to_string()
                        width=move || (BOARD_W / view.zoom.get()).to_string()
                        height=move || (world_h.get() / view.zoom.get()).to_string()
                        fill="url(#sd-dots)"
                    ></rect>
                    <For each=move || edges.get() key=|e| (e.from.clone(), e.to.clone()) children=move |edge| view! { <EdgeView ix=ix edge=edge /> } />
                    <For each=move || ix.auto_edges.get() key=|e| (e.from.clone(), e.to.clone()) children=move |edge| auto_edge_view(ix, edge) />
                    {move || wire_shown.get().then(|| view! {
                        <path
                            class=move || format!("sd-pending {}", wire.get().map(|w| w.1).unwrap_or_default())
                            d=move || wire.get().map(|w| w.0).unwrap_or_default()
                        ></path>
                    })}
                    <For each=move || node_keys.get() key=|k| k.clone() children=move |(id, _)| real_node_view(ix, id) />
                    {move || ghost_shown.get().then(|| view! { <NodeView ix=ix node=ix.ghost.into() ghost=true /> })}
                </svg>
            </div>
            <p class="sd-tip">
                "Порты: вход слева, выход справа. Тяните от выхода ко входу (или кликните по двум портам). Компонент, поставленный рядом с подходящими, подключится сам. Ctrl + колесо — масштаб, пустое место — сдвиг, ⌖ — вписать схему."
            </p>
        </div>
    }
}

/// Пунктир автоподставленной связи.
fn auto_edge_view(ix: Ix, edge: SdEdge) -> impl IntoView {
    let lab = ix.lab;
    let d = move || lab.state.with(|s| ix.ghost.with(|g| logic::auto_edge_path(s, g.as_ref(), &edge))).unwrap_or_default();
    view! { <path class="sd-auto" d=d></path> }
}

/// Компонент схемы с идентификатором `id`: следит за своим узлом в состоянии.
fn real_node_view(ix: Ix, id: String) -> impl IntoView {
    let lab = ix.lab;
    let node = Memo::new(move |_| lab.state.with(|s| s.node(&id).cloned()));
    view! { <NodeView ix=ix node=node.into() ghost=false /> }
}

/// Связь между двумя компонентами: линия и широкая невидимая полоса для клика.
#[component]
fn EdgeView(ix: Ix, edge: SdEdge) -> impl IntoView {
    let lab = ix.lab;
    let d = {
        let edge = edge.clone();
        Memo::new(move |_| lab.state.with(|s| logic::edge_path(s, &edge)).unwrap_or_default())
    };
    let selected = {
        let edge = edge.clone();
        Memo::new(move |_| lab.sel_edge.with(|e| e.as_ref() == Some(&edge)))
    };
    let dead = {
        let edge = edge.clone();
        Memo::new(move |_| lab.down.with(|down| down.contains(&edge.from) || down.contains(&edge.to)))
    };
    view! {
        <g class="sd-edge" class:on=move || selected.get() class:dead=move || dead.get()>
            <path class="line" d=move || d.get()></path>
            <path
                class="hit"
                d=move || d.get()
                on:pointerdown=|e| {
                    if e.button() == 0 {
                        e.stop_propagation();
                    }
                }
                on:click=move |_| lab.select_edge(Some(edge.clone()))
            ></path>
        </g>
    }
}

/// Компонент на поле: рамка, значок, название, краткие параметры, полоска загрузки и порты. `ghost` — призрак из палитры.
#[component]
fn NodeView(ix: Ix, node: Signal<Option<SdNode>>, ghost: bool) -> impl IntoView {
    let Some(first) = node.get_untracked() else { return ().into_any() };
    let (id, kind) = (first.id, first.kind);
    let lab = ix.lab;

    let load = {
        let id = id.clone();
        Memo::new(move |_| lab.result.with(|r| r.loads.get(&id).cloned()))
    };
    let status = {
        let id = id.clone();
        Memo::new(move |_| {
            if lab.down.with(|d| d.contains(&id)) {
                "down"
            } else {
                load.get().map_or("idle", |l: NodeLoad| status_class(l.status))
            }
        })
    };
    let class = {
        let id = id.clone();
        move || {
            let mut c = format!("sd-node {} {}", kind.as_str(), status.get());
            if lab.sel.with(|s| s.as_deref() == Some(id.as_str())) {
                c.push_str(" on");
            }
            if ix.moving.with(|m| m.as_deref() == Some(id.as_str())) {
                c.push_str(" moving");
            }
            if ghost {
                c.push_str(" ghost");
            }
            if ix.hover.with(|h| h.as_deref() == Some(id.as_str())) {
                let class = lab.state.with(|s| logic::hover_class(s, ix.pending.read().as_ref(), &id));
                c.push(' ');
                c.push_str(class);
            }
            c
        }
    };
    let lines = Memo::new(move |_| node.get().map(|n| logic::name_lines(&n.name)).unwrap_or_default());
    let title = Memo::new(move |_| node.get().map(|n| logic::describe_node(&n)).unwrap_or_default());
    let summary = Memo::new(move |_| node.get().map(|n| logic::summary(&n)).unwrap_or_default());
    let transform = move || node.get().map(|n| format!("translate({},{})", n.x, n.y)).unwrap_or_default();
    let pin_class = {
        let id = id.clone();
        move |pin: Pin| {
            let id = id.clone();
            move || {
                let Some(p) = ix.pending.get() else { return String::new() };
                let state = lab.state.with(|s| logic::port_state(s, Some(&p), &id, pin));
                format!("sd-pin {} {}", if pin == Pin::In { "in" } else { "out" }, state.class())
            }
        }
    };
    let (half_w, half_h) = (NODE_W / 2.0, NODE_H / 2.0);
    let bar = move || {
        let l = load.get().filter(|l| l.status != NodeStatus::Idle && kind != Kind::Monitor && !ghost)?;
        Some(view! {
            <g class="sd-bar" transform=format!("translate({},{})", -half_w + 8.0, half_h - 8.0)>
                <rect width=NODE_W - 16.0 height="4" rx="2" class="bg"></rect>
                <rect width=bar_width(l.util) height="4" rx="2" class="fg"></rect>
            </g>
        })
    };
    let own = id.clone();
    let down_id = id.clone();
    let out_id = id.clone();

    view! {
        <g class=class transform=transform on:pointerdown=move |e| if !ghost { ix.node_down(&e, &own) }>
            <title>{move || title.get()}</title>
            <rect x={-half_w} y={-half_h} width=NODE_W height=NODE_H rx="9"></rect>
            {move || {
                let lines = lines.get();
                let n = lines.len();
                lines
                    .into_iter()
                    .enumerate()
                    .map(|(i, line)| {
                        let y = if n == 1 { -5 } else { -14 + 12 * i as i32 };
                        view! { <text class="sd-name" x="0" y=y text-anchor="middle">{line}</text> }
                    })
                    .collect_view()
            }}
            <g class="sd-ico" transform=format!("translate({},5) scale(0.55)", -half_w + 9.0) inner_html=icons::markup(kind)></g>
            <text class="sd-sub" x={-half_w + 28.0} y="15">
                {move || if status.get() == "down" { "отключён".to_owned() } else if ghost { String::new() } else { summary.get() }}
            </text>
            {bar}
            {(!ghost && has_in(kind)).then(|| view! {
                <circle class=pin_class(Pin::In) cx={-half_w} cy="0" r="5.5" on:pointerdown=move |e| ix.pin_down(&e, &down_id, Pin::In)>
                    <title>"Вход: сюда приходят запросы"</title>
                </circle>
            })}
            {(!ghost && has_out(kind)).then(|| view! {
                <circle class=pin_class(Pin::Out) cx=half_w cy="0" r="5.5" on:pointerdown=move |e| ix.pin_down(&e, &out_id, Pin::Out)>
                    <title>"Выход: потяните к входу другого компонента"</title>
                </circle>
            })}
        </g>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn height_from_settings_must_be_within_limits() {
        assert_eq!(clamp_height(100.0), MIN_H);
        assert_eq!(clamp_height(5000.0), MAX_H);
        assert_eq!(clamp_height(400.4), 400.0);
    }

    #[test]
    fn load_bar_is_never_thinner_than_two_and_never_overflows() {
        assert_eq!(bar_width(0.0), 2.0);
        assert_eq!(bar_width(0.5), (NODE_W - 16.0) / 2.0);
        assert_eq!(bar_width(3.0), NODE_W - 16.0);
    }

    #[test]
    fn node_status_has_a_css_class_for_every_state() {
        for (s, c) in [(NodeStatus::Idle, "idle"), (NodeStatus::Ok, "ok"), (NodeStatus::Warm, "warm"), (NodeStatus::Hot, "hot"), (NodeStatus::Over, "over"), (NodeStatus::Down, "down")] {
            assert_eq!(status_class(s), c);
        }
    }
}
