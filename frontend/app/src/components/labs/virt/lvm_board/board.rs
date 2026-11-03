//! Board of the LVM lab (modeled on the oVirt topology board and on the boards of the "Computer architecture" and "System design" labs):
//! — an object has pins: an input on the left and an output on the right (if the kind takes part in a relation); a link is dragged from a pin
//!   to another object (or made by clicking two pins); the direction is fixed by the model, so it does not matter which end is pressed;
//! — objects can be dragged, and also dragged from the palette straight onto the board;
//! — the board can be panned (empty space, middle button) and zoomed (Ctrl + wheel, buttons).
//!
//! Pointer state is signals in [`Ix`]; global mouse handlers hang on the window, and the pure decisions ("what is under the cursor",
//! "can it be connected", "how to fit the board") are functions from `logic.rs`.

use leptos::{ev, prelude::*, svg};
use virtlab::lvm_board::{Edge, Kind, Node};
use wasm_bindgen::JsCast;

use super::{
    icons,
    lab::Lab,
    logic::{self, NodeInfo, Pending, Pin, BOARD, BOARD_W, MOVE_SLOP, NODE_H, NODE_W},
};
use crate::{
    components::labs::board_view::{is_background, use_element_size, BoardView, ItemDrag, Point, View, ZoomControls},
    dom,
};

fn client(e: &web_sys::PointerEvent) -> Point {
    Point::new(f64::from(e.client_x()), f64::from(e.client_y()))
}

/// Focus in an input field: Delete and Backspace work there as usual.
fn typing_in_field(target: Option<web_sys::EventTarget>) -> bool {
    target
        .and_then(|t| t.dyn_into::<web_sys::Element>().ok())
        .is_some_and(|el| ["INPUT", "SELECT", "TEXTAREA"].contains(&el.tag_name().to_ascii_uppercase().as_str()))
}

/// The object being dragged and the press point on a pin (screen).
#[derive(Clone, Copy, Default)]
struct DragInfo {
    item: ItemDrag,
    pin_down: Option<Point>,
}

/// Pointer state on the board: what is dragged and what is aimed at.
#[derive(Clone, Copy)]
struct Ix {
    lab: Lab,
    view: BoardView,
    /// kind of the object dragged from the palette
    placing: RwSignal<Option<Kind>>,
    /// cursor position on screen while dragging from the palette
    cursor: RwSignal<Option<Point>>,
    /// object being moved
    moving: RwSignal<Option<String>>,
    moved_far: RwSignal<bool>,
    /// wire dragged from a pin
    pending: RwSignal<Option<Pending>>,
    /// wire "stuck" to the cursor after clicking a pin
    sticky: RwSignal<bool>,
    cursor_board: RwSignal<Option<Point>>,
    /// object under the end of the wire
    hover: RwSignal<Option<String>>,
    drag: StoredValue<DragInfo>,
    /// ghost of a palette object under the cursor
    ghost: Memo<Option<Node>>,
}

impl Ix {
    fn new(lab: Lab, view: BoardView) -> Self {
        let placing = RwSignal::new(None::<Kind>);
        let cursor = RwSignal::new(None::<Point>);
        let ghost = Memo::new(move |_| {
            let (kind, at) = (placing.get()?, cursor.get()?);
            if !view.contains_client(at) {
                return None;
            }
            Some(logic::ghost_node(kind, view.to_board(at.x, at.y)))
        });
        Self {
            lab,
            view,
            placing,
            cursor,
            moving: RwSignal::new(None),
            moved_far: RwSignal::new(false),
            pending: RwSignal::new(None),
            sticky: RwSignal::new(false),
            cursor_board: RwSignal::new(None),
            hover: RwSignal::new(None),
            drag: StoredValue::new(DragInfo::default()),
            ghost,
        }
    }

    fn cancel_wire(&self) {
        self.pending.set(None);
        self.sticky.set(false);
        self.hover.set(None);
        self.cursor_board.set(None);
    }

    /// Press on an object: either finishes a "stuck" wire or starts a drag.
    fn node_down(&self, e: &web_sys::PointerEvent, id: &str) {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        if let Some(p) = self.pending.get_untracked().filter(|_| self.sticky.get_untracked()) {
            self.cancel_wire();
            if p.id != id {
                self.lab.connect(&p.id, id);
            }
            return;
        }
        let at = self.view.to_board(f64::from(e.client_x()), f64::from(e.client_y()));
        let Some((x, y)) = self.lab.board.with_untracked(|t| t.node(id).map(|n| (n.x, n.y))) else { return };
        self.drag.set_value(DragInfo { item: ItemDrag::start(at, Point::new(x, y)), pin_down: None });
        self.moved_far.set(false);
        self.moving.set(Some(id.to_owned()));
    }

    /// Press on a pin: start of a wire or connection with a "stuck" wire.
    fn pin_down(&self, e: &web_sys::PointerEvent, id: &str, pin: Pin) {
        if e.button() != 0 {
            return;
        }
        e.prevent_default();
        e.stop_propagation();
        if let Some(p) = self.pending.get_untracked().filter(|_| self.sticky.get_untracked()) {
            self.cancel_wire();
            if p.id != id {
                self.lab.connect(&p.id, id);
            }
            return;
        }
        self.pending.set(Some(Pending { id: id.to_owned(), pin }));
        self.sticky.set(false);
        self.drag.update_value(|d| d.pin_down = Some(client(e)));
        self.hover.set(None);
        self.cursor_board.set(Some(self.view.to_board(f64::from(e.client_x()), f64::from(e.client_y()))));
    }

    /// Press on the board background: cancels the wire, clears the selection and starts panning; the middle button pans anywhere.
    fn board_down(&self, e: &web_sys::PointerEvent) {
        if e.button() == 1 {
            self.view.on_pointer_down(e, false);
            return;
        }
        if e.button() != 0 || self.placing.get_untracked().is_some() {
            return;
        }
        if !is_background(e.target(), "vl-lvm-bg") {
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
            self.hover.set(self.lab.board.with_untracked(|t| logic::node_at(t, &p.id, b)));
        }
    }

    fn on_up(&self, e: &web_sys::PointerEvent) {
        let at = client(e);
        if self.view.end_pan() {
            return;
        }
        if let Some(kind) = self.placing.get_untracked() {
            self.placing.set(None);
            self.cursor.set(None);
            if self.view.contains_client(at) {
                let p = self.view.to_board(at.x, at.y);
                self.lab.add(kind, Some(BOARD.items.snap(p)));
            }
            return;
        }
        if let Some(id) = self.moving.get_untracked() {
            let far = self.moved_far.get_untracked();
            self.moving.set(None);
            self.moved_far.set(false);
            if far {
                if let Some((x, y)) = self.lab.board.with_untracked(|t| t.node(&id).map(|n| (n.x, n.y))) {
                    self.lab.move_node(&id, x, y, true);
                }
            } else {
                self.lab.select_node(Some(id));
            }
            return;
        }
        if let Some(p) = self.pending.get_untracked().filter(|_| !self.sticky.get_untracked()) {
            let b = self.view.to_board(at.x, at.y);
            let target = self.lab.board.with_untracked(|t| logic::node_at(t, &p.id, b));
            match target {
                Some(t) => {
                    self.lab.connect(&p.id, &t);
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

/// Palette, delete and start-over buttons, and the board.
#[component]
pub fn Board(lab: Lab) -> impl IntoView {
    let svg_ref = NodeRef::<svg::Svg>::new();
    let size = use_element_size(svg_ref);
    let world_h = Memo::new(move |_| {
        let (w, h) = size.get();
        logic::world_height(w, h)
    });
    let view = BoardView::new(svg_ref, BOARD, Signal::derive(move || (BOARD_W, world_h.get())));
    let ix = Ix::new(lab, view);

    // fit the whole board into the viewport
    let fitted = RwSignal::new(None::<View>);
    let fit = Callback::new(move |()| {
        let points: Vec<Point> = lab.board.with_untracked(|t| t.nodes.iter().map(|n| Point::new(n.x, n.y)).collect());
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

    dom::on_window(ev::pointermove, move |e| ix.on_move(&e));
    dom::on_window(ev::pointerup, move |e| ix.on_up(&e));
    dom::on_window(ev::keydown, move |e| ix.on_key(&e));

    let node_ids = Memo::new(move |_| lab.board.with(|t| t.nodes.iter().map(|n| n.id.clone()).collect::<Vec<_>>()));
    let edges = Memo::new(move |_| lab.board.with(|t| t.edges.clone()));
    let wire = Memo::new(move |_| {
        ix.pending.get().and_then(|p| lab.board.with(|t| logic::pending_wire(t, &p, ix.hover.get().as_deref(), ix.cursor_board.get())))
    });
    let wire_shown = Memo::new(move |_| wire.with(Option::is_some));
    let ghost_shown = Memo::new(move |_| ix.ghost.with(Option::is_some));

    let buttons = lab
        .scenario()
        .palette
        .iter()
        .copied()
        .map(|kind| {
            view! {
                <button
                    type="button"
                    class="vl-lvm-add"
                    data-kind=kind.as_str()
                    title=i18n::tr("Drag it onto the board, or click to put it in the next free place.")
                    on:pointerdown=move |e| {
                        if e.button() != 0 {
                            return;
                        }
                        e.prevent_default();
                        ix.placing.set(Some(kind));
                        ix.cursor.set(Some(client(&e)));
                    }
                    on:click=move |_| {
                        // after a click the board is fitted again: a new object must not end up beyond the edge
                        if lab.add(kind, None) {
                            fit.run(());
                        }
                    }
                >
                    <svg class="vl-lvm-addico" viewBox="0 0 24 24" aria-hidden="true" inner_html=icons::markup(kind)></svg>
                    {format!("+ {}", kind.label())}
                </button>
            }
        })
        .collect_view();

    view! {
        <div class="vl-lvm-boardwrap">
            <div class="vl-lvm-toolbar" role="toolbar" aria-label=i18n::tr("Objects: drag onto the board or click")>
                {buttons}
                <span class="vl-lvm-spacer"></span>
                <button type="button" class="quiz-btn ghost vl-lvm-delete" disabled=move || !lab.can_delete() on:click=move |_| lab.remove_selected()>
                    {i18n::tr("Delete")}
                </button>
                <button type="button" class="quiz-btn ghost vl-lvm-reset" on:click=move |_| lab.reset()>
                    {i18n::tr("Start over")}
                </button>
            </div>
            <div class="vl-lvm-viewport">
                <ZoomControls view=view changed=changed on_reset=fit />
                <svg
                    node_ref=svg_ref
                    class="vl-lvm-board"
                    class:panning=move || view.panning.get()
                    class:placing=move || ix.placing.get().is_some()
                    viewBox=move || view.view_box()
                    role="img"
                    aria-label=i18n::tr("LVM storage")
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
                        <pattern id="vl-lvm-dots" width="22" height="22" patternUnits="userSpaceOnUse">
                            <circle cx="1.5" cy="1.5" r="1.3" class="vl-lvm-dot"></circle>
                        </pattern>
                    </defs>
                    <rect
                        class="vl-lvm-bg"
                        x=move || view.pan.get().x.to_string()
                        y=move || view.pan.get().y.to_string()
                        width=move || (BOARD_W / view.zoom.get()).to_string()
                        height=move || (world_h.get() / view.zoom.get()).to_string()
                        fill="url(#vl-lvm-dots)"
                    ></rect>
                    <For each=move || edges.get() key=|e| (e.from.clone(), e.to.clone()) children=move |edge| view! { <EdgeView ix=ix edge=edge /> } />
                    {move || wire_shown.get().then(|| view! {
                        <path
                            class=move || format!("vl-lvm-pending {}", wire.get().map(|w| w.1).unwrap_or_default())
                            d=move || wire.get().map(|w| w.0).unwrap_or_default()
                        ></path>
                    })}
                    <For each=move || node_ids.get() key=|id| id.clone() children=move |id| real_node_view(ix, id) />
                    {move || ghost_shown.get().then(|| view! { <NodeView ix=ix node=ix.ghost.into() ghost=true /> })}
                </svg>
            </div>
            <p class="vl-lvm-tip">
                {i18n::tr("Pins: input on the left, output on the right. Drag from a pin to another object (or click two pins); the direction is fixed by LVM. Ctrl + wheel to zoom, empty space to pan, ⌖ to fit the board.")}
            </p>
        </div>
    }
}

/// Object with identifier `id`: follows its own node on the board.
fn real_node_view(ix: Ix, id: String) -> impl IntoView {
    let lab = ix.lab;
    let node = Memo::new(move |_| lab.board.with(|t| t.node(&id).cloned()));
    view! { <NodeView ix=ix node=node.into() ghost=false /> }
}

/// Link between two objects: a line, a wide invisible strip for clicking and a label of the relation.
#[component]
fn EdgeView(ix: Ix, edge: Edge) -> impl IntoView {
    let lab = ix.lab;
    let geom = {
        let edge = edge.clone();
        Memo::new(move |_| lab.board.with(|t| logic::edge_geom(t, &edge)))
    };
    let label = {
        let edge = edge.clone();
        Memo::new(move |_| lab.board.with(|t| logic::edge_rel(t, &edge)).map(|r| r.label()).unwrap_or_default())
    };
    let selected = {
        let edge = edge.clone();
        Memo::new(move |_| lab.sel_edge.with(|e| e.as_ref() == Some(&edge)))
    };
    let (data_from, data_to) = (edge.from.clone(), edge.to.clone());
    let d = move || geom.get().map(|g| g.0).unwrap_or_default();
    view! {
        <g
            class="vl-lvm-edge"
            data-from=data_from
            data-to=data_to
            class:on=move || selected.get()
        >
            <path class="line" d=d></path>
            <path
                class="hit"
                d=d
                on:pointerdown=|e| {
                    if e.button() == 0 {
                        e.stop_propagation();
                    }
                }
                on:click=move |_| lab.select_edge(Some(edge.clone()))
            ></path>
            <text class="lbl" x=move || geom.get().map(|g| g.1.x).unwrap_or_default() y=move || geom.get().map(|g| g.1.y - 6.0).unwrap_or_default() text-anchor="middle">
                {move || label.get()}
            </text>
        </g>
    }
}

/// Object on the board: frame, icon, name, status chip, badges and pins. `ghost` — a ghost from the palette.
#[component]
fn NodeView(ix: Ix, node: Signal<Option<Node>>, ghost: bool) -> impl IntoView {
    let Some(first) = node.get_untracked() else { return ().into_any() };
    let (id, kind) = (first.id, first.kind);
    let lab = ix.lab;

    let info = {
        let id = id.clone();
        Memo::new(move |_| if ghost { NodeInfo::default() } else { lab.board.with(|t| lab.eval.with(|ev| logic::node_info(t, ev, &id))) })
    };
    let class = {
        let id = id.clone();
        move || {
            let mut c = format!("vl-lvm-node {} {}", kind.as_str(), info.with(logic::status_class));
            if lab.sel.with(|s| s.as_deref() == Some(id.as_str())) {
                c.push_str(" on");
            }
            if ix.moving.with(|m| m.as_deref() == Some(id.as_str())) {
                c.push_str(" moving");
            }
            if ghost {
                c.push_str(" ghost");
            }
            if lab.lost.with(|l| l.contains(&id)) {
                c.push_str(" path-bad");
            }
            if ix.hover.with(|h| h.as_deref() == Some(id.as_str())) {
                c.push(' ');
                c.push_str(lab.board.with(|t| logic::hover_class(t, ix.pending.read().as_ref(), &id)));
            }
            c
        }
    };
    let name = Memo::new(move |_| node.get().map(|n| logic::short_name(&n.name)).unwrap_or_default());
    let title = Memo::new(move |_| node.get().map(|n| logic::describe_node(&n, &info.get())).unwrap_or_default());
    let transform = move || node.get().map(|n| format!("translate({},{})", n.x, n.y)).unwrap_or_default();
    let pin_class = {
        let id = id.clone();
        move |pin: Pin| {
            let id = id.clone();
            move || {
                let state = lab.board.with(|t| logic::port_state(t, ix.pending.read().as_ref(), &id));
                format!("vl-lvm-pin {} {}", if pin == Pin::In { "in" } else { "out" }, state.class())
            }
        }
    };
    let (half_w, half_h) = (NODE_W / 2.0, NODE_H / 2.0);
    let badge = move || info.with(|i| i.badge.clone());
    let chip = move || {
        info.get().chip.map(|c| view! { <span class=format!("vl-chip {}", c.class)>{c.text}</span> })
    };
    let own = id.clone();
    let in_id = id.clone();
    let out_id = id.clone();
    let data_id = id.clone();

    view! {
        <g
            class=class
            data-id=data_id
            data-kind=kind.as_str()
            transform=transform
            on:pointerdown=move |e| {
                if !ghost {
                    ix.node_down(&e, &own)
                }
            }
        >
            <title>{move || title.get()}</title>
            <rect x={-half_w} y={-half_h} width=NODE_W height=NODE_H rx="9"></rect>
            <g class="vl-lvm-ico" transform=format!("translate({},{}) scale(0.5)", -half_w + 6.0, -half_h + 5.0) inner_html=icons::markup(kind)></g>
            <text class="vl-lvm-badge" class:over=move || info.with(|i| i.warn) x={half_w - 6.0} y={-half_h + 15.0} text-anchor="end">
                {badge}
            </text>
            <text class="vl-lvm-name" x="0" y="-2" text-anchor="middle">
                {move || name.get()}
            </text>
            <foreignObject class="vl-lvm-chipbox" x={-half_w + 3.0} y="6" width={NODE_W - 6.0} height="20">
                <div class="vl-lvm-status">{chip}</div>
            </foreignObject>
            {(!ghost && logic::has_in(kind)).then(|| view! {
                <circle class=pin_class(Pin::In) data-node=in_id.clone() data-pin="in" cx={-half_w} cy="0" r="5.5" on:pointerdown=move |e| ix.pin_down(&e, &in_id, Pin::In)>
                    <title>{i18n::tr("Input: other objects link here")}</title>
                </circle>
            })}
            {(!ghost && logic::has_out(kind)).then(|| view! {
                <circle class=pin_class(Pin::Out) data-node=out_id.clone() data-pin="out" cx=half_w cy="0" r="5.5" on:pointerdown=move |e| ix.pin_down(&e, &out_id, Pin::Out)>
                    <title>{i18n::tr("Output: drag to another object")}</title>
                </circle>
            })}
        </g>
    }
    .into_any()
}
