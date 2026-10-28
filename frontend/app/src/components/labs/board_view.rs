//! A window onto an "infinite" board, shared by all lab boards (system design, architecture, networks): panning (empty
//! space, middle mouse button), zoom (Ctrl/⌘ + wheel, buttons), conversion of screen coordinates to board coordinates,
//! dragging of items and an element-size observer. In React these were `useBoardView.tsx` and `board-pan.ts`.
//!
//! The arithmetic is pure types and functions (with tests); [`BoardView`] only ties them to signals and `<svg>` sizes.
//! The board is a window (`viewBox`) onto a plane: at zoom `z` a piece of size `width/z × height/z` is visible, starting at the
//! `pan` point; `<svg>` fits the window into its own size keeping proportions (`preserveAspectRatio = xMidYMid meet`).
//!
//! What differs between boards (zoom limits, initial pan, rounding, world bounds and click threshold) is collected in
//! [`BoardConfig`]; each lab has its own constant, while the code is shared.

use leptos::{html::ElementType, prelude::*, svg};
use wasm_bindgen::JsCast;

use crate::dom;

/// Step of the zoom buttons.
pub const ZOOM_STEP: f64 = 1.25;

// --- pure arithmetic ----------------------------------------------------------------------------

/// JavaScript's `Math.round`: halves round toward +∞.
pub fn js_round(x: f64) -> f64 {
    (x + 0.5).floor()
}

/// A point (on screen or on the board).
#[derive(Clone, Copy, Debug, PartialEq, Default)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

impl Point {
    pub const fn new(x: f64, y: f64) -> Self {
        Self { x, y }
    }
}

/// Board pan and zoom.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct View {
    /// top-left corner of the window on the board
    pub pan: Point,
    pub zoom: f64,
}

impl View {
    /// Window center on the board; `world` is the window size at zoom 1.
    pub fn center(&self, world: (f64, f64)) -> Point {
        Point::new(self.pan.x + world.0 / self.zoom / 2.0, self.pan.y + world.1 / self.zoom / 2.0)
    }
}

/// A rectangular area on the board: limits per axis `(from, to)`.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Bounds {
    pub x: (f64, f64),
    pub y: (f64, f64),
}

impl Bounds {
    pub const fn new(x: (f64, f64), y: (f64, f64)) -> Self {
        Self { x, y }
    }

    /// An area symmetric about the origin.
    pub const fn symmetric(limit: f64) -> Self {
        Self { x: (-limit, limit), y: (-limit, limit) }
    }

    /// Keeps the top-left corner of an element of size `size` inside the area (the element does not cross its right and bottom edges).
    pub fn clamp(&self, p: Point, size: (f64, f64)) -> Point {
        Point::new(p.x.clamp(self.x.0, self.x.1 - size.0), p.y.clamp(self.y.0, self.y.1 - size.1))
    }

    /// A point inside the area, with integer coordinates (like JavaScript's `Math.round`).
    pub fn snap(&self, p: Point) -> Point {
        let p = self.clamp(p, (0.0, 0.0));
        Point::new(js_round(p.x), js_round(p.y))
    }
}

/// How boards differ: zoom limits, initial pan, pan rounding, where the window and elements may be.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct BoardConfig {
    pub zoom_min: f64,
    pub zoom_max: f64,
    /// top-left corner of the window in the initial view (initial zoom is 100 %)
    pub home: Point,
    /// the pan is always an integer (manual pan and zoom around a point are rounded)
    pub round_pan: bool,
    /// where the window center may be: the board cannot be carried away entirely; `None` means no limits
    pub window_limit: Option<Bounds>,
    /// where board elements may be
    pub items: Bounds,
    /// pointer shift (screen px) below which a press stays a click rather than a drag
    pub click_slop: f64,
}

impl BoardConfig {
    /// Defaults: zoom 30–300 %, integer pan, window and elements almost unbounded, click threshold 6 px.
    pub const DEFAULT: BoardConfig = BoardConfig {
        zoom_min: 0.3,
        zoom_max: 3.0,
        home: Point::new(0.0, 0.0),
        round_pan: true,
        window_limit: None,
        items: Bounds::symmetric(2600.0),
        click_slop: 6.0,
    };

    /// Initial view: initial pan and 100 % zoom.
    pub fn home_view(&self) -> View {
        View { pan: self.home, zoom: 1.0 }
    }

    pub fn clamp_zoom(&self, z: f64) -> f64 {
        z.clamp(self.zoom_min, self.zoom_max)
    }

    fn snap_pan(&self, p: Point) -> Point {
        if self.round_pan {
            Point::new(js_round(p.x), js_round(p.y))
        } else {
            p
        }
    }

    /// Returns the window to the board limits: the window center is no further than `window_limit`. `world` is the window size at zoom 1.
    pub fn constrain(&self, view: View, world: (f64, f64)) -> View {
        let Some(limit) = self.window_limit else { return view };
        let (w, h) = (world.0 / view.zoom, world.1 / view.zoom);
        let c = limit.clamp(Point::new(view.pan.x + w / 2.0, view.pan.y + h / 2.0), (0.0, 0.0));
        View { pan: Point::new(c.x - w / 2.0, c.y - h / 2.0), zoom: view.zoom }
    }

    /// Changes zoom by `factor` times (above 1 zooms in) without moving the board point `at` under the cursor.
    pub fn zoom_at(&self, view: View, factor: f64, at: Point, world: (f64, f64)) -> View {
        let zoom = self.clamp_zoom(view.zoom * factor);
        if !zoom.is_finite() || (zoom - view.zoom).abs() < 1e-9 {
            return view;
        }
        let r = view.zoom / zoom;
        let pan = self.snap_pan(Point::new(at.x - (at.x - view.pan.x) * r, at.y - (at.y - view.pan.y) * r));
        self.constrain(View { pan, zoom }, world)
    }

    /// A window of the required zoom with the same midpoint (the "100 %" button in networks).
    pub fn zoom_to(&self, view: View, zoom: f64, world: (f64, f64)) -> View {
        self.zoom_at(view, zoom / view.zoom, view.center(world), world)
    }

    /// Manual pan: the new window pan and (if the window hit the limit) a "rebased" gesture, so a board that no longer
    /// moves does not force the hand back to where it "overshot".
    pub fn pan_drag(&self, d: PanDrag, now: Point, zoom: f64, world: (f64, f64)) -> (Point, PanDrag) {
        let want = self.snap_pan(d.pan_at(now));
        let pan = self.constrain(View { pan: want, zoom }, world).pan;
        let d = if pan == want { d } else { PanDrag { from: now, offset: pan, ..d } };
        (pan, d)
    }

    /// Press and release at almost the same point is a click.
    pub fn is_click(&self, down: Point, up: Point) -> bool {
        (up.x - down.x).hypot(up.y - down.y) < self.click_slop
    }
}

/// Value of the `viewBox` attribute for a `w × h` window at zoom 1: the larger the zoom, the smaller the piece of the board.
pub fn view_box(view: View, w: f64, h: f64) -> String {
    let r = |n: f64| js_round(n * 100.0) / 100.0;
    format!("{} {} {} {}", r(view.pan.x), r(view.pan.y), r(w / view.zoom), r(h / view.zoom))
}

/// Zoom factor per wheel "tick": smooth and equal in both directions.
pub fn wheel_factor(delta_y: f64) -> f64 {
    (-delta_y * 0.0025).exp()
}

/// Height of the board window (in board units) for a manual `<svg>` height in pixels: the window proportions match `<svg>`,
/// so the board does not "float" with margins (`worldH` from `GateBoard.tsx`).
pub fn world_height_for(px_height: f64, px_width: f64, world_w: f64) -> Option<f64> {
    (px_width > 0.0 && px_height > 0.0).then(|| px_height * world_w / px_width)
}

/// Manual board pan: where the press happened (screen), what the pan was and how many screen pixels per board unit.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct PanDrag {
    pub from: Point,
    pub offset: Point,
    pub scale: f64,
}

impl PanDrag {
    /// Window pan when the pointer is at `now`: the board "follows" the hand (pull right and the content moves right).
    pub fn pan_at(&self, now: Point) -> Point {
        Point::new(self.offset.x - (now.x - self.from.x) / self.scale, self.offset.y - (now.y - self.from.y) / self.scale)
    }
}

/// Dragging a board element: where the element stood and how far the pointer was offset from its corner at press time.
#[derive(Clone, Copy, Debug, PartialEq, Default)]
pub struct ItemDrag {
    pub from: Point,
    pub grip: Point,
}

impl ItemDrag {
    /// Pressed on an element standing at `at`, the pointer (in board coordinates) is at `pointer`.
    pub fn start(pointer: Point, at: Point) -> Self {
        Self { from: at, grip: Point::new(at.x - pointer.x, at.y - pointer.y) }
    }

    /// Where the element is for pointer `pointer` (world bounds are the caller's job: [`Bounds::clamp`] or [`Bounds::snap`]).
    pub fn at(&self, pointer: Point) -> Point {
        Point::new(pointer.x + self.grip.x, pointer.y + self.grip.y)
    }

    /// The element moved further than `slop` from the press point: this is a drag, not a click.
    pub fn moved_far(&self, now: Point, slop: f64) -> bool {
        (now.x - self.from.x).hypot(now.y - self.from.y) > slop
    }
}

/// Where the board is on screen: the `<svg>` rectangle, pixels per board unit at zoom 1 and margins around the fitted board.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Metrics {
    pub left: f64,
    pub top: f64,
    pub width: f64,
    pub height: f64,
    pub base: f64,
    pub off_x: f64,
    pub off_y: f64,
}

/// Metrics for a `view_w × view_h` window fitted into the `<svg>` rectangle. The 1 px border is not counted in sizes.
pub fn metrics(left: f64, top: f64, width: f64, height: f64, view_w: f64, view_h: f64) -> Metrics {
    let base = (width / view_w).min(height / view_h);
    Metrics { left, top, width, height, base, off_x: (width - view_w * base) / 2.0, off_y: (height - view_h * base) / 2.0 }
}

impl Metrics {
    /// A screen point (`clientX`, `clientY`) in board coordinates, taking pan and zoom into account.
    pub fn to_board(&self, client: Point, view: View) -> Point {
        let scale = self.base * view.zoom;
        if scale.is_nan() || scale <= 0.0 {
            return view.pan;
        }
        Point::new(view.pan.x + (client.x - self.left - self.off_x) / scale, view.pan.y + (client.y - self.top - self.off_y) / scale)
    }
}

// --- board state --------------------------------------------------------------------------------

/// Window onto the board: pan, zoom and coordinate conversion. Copied as a set of signals.
#[derive(Clone, Copy)]
pub struct BoardView {
    /// root `<svg>` of the board
    pub svg: NodeRef<svg::Svg>,
    pub pan: RwSignal<Point>,
    pub zoom: RwSignal<f64>,
    /// a manual board pan is in progress
    pub panning: RwSignal<bool>,
    cfg: BoardConfig,
    /// window size onto the board at zoom 1 (width, height)
    world: Signal<(f64, f64)>,
    drag: StoredValue<Option<PanDrag>>,
}

impl BoardView {
    pub fn new(svg: NodeRef<svg::Svg>, cfg: BoardConfig, world: Signal<(f64, f64)>) -> Self {
        Self { svg, pan: RwSignal::new(cfg.home), zoom: RwSignal::new(1.0), panning: RwSignal::new(false), cfg, world, drag: StoredValue::new(None) }
    }

    pub fn config(&self) -> BoardConfig {
        self.cfg
    }

    pub fn view(&self) -> View {
        View { pan: self.pan.get(), zoom: self.zoom.get() }
    }

    fn view_untracked(&self) -> View {
        View { pan: self.pan.get_untracked(), zoom: self.zoom.get_untracked() }
    }

    pub fn set_view(&self, view: View) {
        self.pan.set(view.pan);
        self.zoom.set(view.zoom);
    }

    /// Restore the initial view.
    pub fn reset(&self) {
        self.set_view(self.cfg.home_view());
    }

    /// The board is panned or zoom is not 100 % (in a reactive context, a subscription).
    pub fn changed(&self) -> bool {
        self.view() != self.cfg.home_view()
    }

    /// `viewBox` value (in a reactive context, a subscription to pan, zoom and window size).
    pub fn view_box(&self) -> String {
        let (w, h) = self.world.get();
        view_box(self.view(), w, h)
    }

    /// Where the board is on screen right now; `None` until `<svg>` appears or while it has no size.
    pub fn metrics(&self) -> Option<Metrics> {
        let rect = self.svg.get_untracked()?.get_bounding_client_rect();
        let (w, h) = self.world.get_untracked();
        let m = metrics(rect.left(), rect.top(), rect.width(), rect.height(), w, h);
        (m.base > 0.0 && m.base.is_finite()).then_some(m)
    }

    /// A screen point in board coordinates (no signal subscription: called from event handlers).
    pub fn to_board(&self, client_x: f64, client_y: f64) -> Point {
        match self.metrics() {
            Some(m) => m.to_board(Point::new(client_x, client_y), self.view_untracked()),
            None => Point::default(),
        }
    }

    /// The screen point lies over the board.
    pub fn contains_client(&self, client: Point) -> bool {
        self.svg.get_untracked().is_some_and(|s| {
            let r = s.get_bounding_client_rect();
            client.x >= r.left() && client.x <= r.right() && client.y >= r.top() && client.y <= r.bottom()
        })
    }

    /// Press and release at almost the same point is a click (threshold comes from the board settings).
    pub fn is_click(&self, down: Point, up: Point) -> bool {
        self.cfg.is_click(down, up)
    }

    /// Start of a manual board pan.
    pub fn begin_pan(&self, client_x: f64, client_y: f64) {
        let Some(m) = self.metrics() else { return };
        let view = self.view_untracked();
        self.drag.set_value(Some(PanDrag { from: Point::new(client_x, client_y), offset: view.pan, scale: m.base * view.zoom }));
        self.panning.set(true);
    }

    /// Moves the board with the hand while a pan is in progress; `true` means the event was handled.
    pub fn move_pan(&self, client_x: f64, client_y: f64) -> bool {
        let Some(d) = self.drag.get_value() else { return false };
        let (pan, d) = self.cfg.pan_drag(d, Point::new(client_x, client_y), self.zoom.get_untracked(), self.world.get_untracked());
        self.drag.set_value(Some(d));
        self.pan.set(pan);
        true
    }

    /// End of a pan; `true` if a pan was in progress.
    pub fn end_pan(&self) -> bool {
        if self.drag.get_value().is_none() {
            return false;
        }
        self.drag.set_value(None);
        self.panning.set(false);
        true
    }

    /// Zoom buttons: around the window center.
    pub fn zoom_by(&self, factor: f64) {
        let view = self.view_untracked();
        let world = self.world.get_untracked();
        self.set_view(self.cfg.zoom_at(view, factor, view.center(world), world));
    }

    /// Zoom `zoom` with the same window midpoint.
    pub fn zoom_to(&self, zoom: f64) {
        self.set_view(self.cfg.zoom_to(self.view_untracked(), zoom, self.world.get_untracked()));
    }

    /// Zoom `zoom`, the pan stays as before (the window's top-left corner stays in place).
    pub fn set_zoom(&self, zoom: f64) {
        self.zoom.set(zoom);
    }

    /// Wheel over the board: with Ctrl/⌘ zooms around the cursor (the page does not scroll then). A full-screen
    /// board (`always`) also zooms with a plain wheel.
    pub fn on_wheel(&self, ev: &web_sys::WheelEvent, always: bool) {
        if !(always || ev.ctrl_key() || ev.meta_key()) {
            return;
        }
        ev.prevent_default();
        let Some(m) = self.metrics() else { return };
        let view = self.view_untracked();
        let at = m.to_board(Point::new(f64::from(ev.client_x()), f64::from(ev.client_y())), view);
        self.set_view(self.cfg.zoom_at(view, wheel_factor(ev.delta_y()), at, self.world.get_untracked()));
    }

    /// Press on the board: the middle button, or the left one on an empty spot (`background`), starts a pan. `true` means the press was handled.
    pub fn on_pointer_down(&self, ev: &web_sys::PointerEvent, background: bool) -> bool {
        let middle = ev.button() == 1;
        if !(middle || (background && ev.button() == 0)) {
            return false;
        }
        ev.prevent_default();
        self.begin_pan(f64::from(ev.client_x()), f64::from(ev.client_y()));
        true
    }
}

// --- DOM helpers --------------------------------------------------------------------------------

/// The chapter page is expanded to full screen: boards fill the shell (class `fill`).
pub fn use_fullscreen() -> impl Fn() -> bool + Copy + Send + Sync + 'static {
    let fs = use_context::<crate::components::fullscreen::Fullscreen>();
    move || fs.is_some_and(|f| f.is_on())
}

/// The press landed on the `<svg>` itself or on the dotted background (`bg_class`): a board pan starts here.
pub fn is_background(target: Option<web_sys::EventTarget>, bg_class: &str) -> bool {
    let Some(el) = target.and_then(|t| t.dyn_into::<web_sys::Element>().ok()) else {
        return false;
    };
    el.tag_name().eq_ignore_ascii_case("svg") || el.get_attribute("class").is_some_and(|c| c.split_whitespace().any(|x| x == bg_class))
}

/// The event came from an element lying inside `selector` (or being it itself).
pub fn target_within(target: Option<web_sys::EventTarget>, selector: &str) -> bool {
    target.and_then(|t| t.dyn_into::<web_sys::Element>().ok()).and_then(|el| el.closest(selector).ok().flatten()).is_some()
}

/// Element size `(width, height)` in pixels; updated on every size change (`ResizeObserver`).
/// While there is no element, the size is zero.
pub fn use_element_size<E>(node: NodeRef<E>) -> ReadSignal<(f64, f64)>
where
    E: ElementType + 'static,
    E::Output: JsCast + Clone + 'static,
{
    let (size, set_size) = signal((0.0, 0.0));
    let guard = StoredValue::new_local(None::<dom::ResizeGuard>);
    Effect::new(move |_| {
        let Some(el) = node.get() else { return };
        let el: web_sys::Element = el.unchecked_into();
        let read = {
            let el = el.clone();
            move || {
                let r = el.get_bounding_client_rect();
                let now = (r.width(), r.height());
                if size_differs(size.get_untracked(), now) {
                    set_size.set(now);
                }
            }
        };
        read();
        guard.set_value(dom::observe_resize(&[el], read));
    });
    size
}

fn size_differs(a: (f64, f64), b: (f64, f64)) -> bool {
    (a.0 - b.0).abs() > 0.5 || (a.1 - b.1).abs() > 0.5
}

/// Zoom buttons above the board: −, percent (100 %), +, "reset".
///
/// By default "⌖" is visible when the view differs from the initial one and restores it, while "100 %" changes zoom without touching
/// the pan. `changed`, `on_reset` and `on_actual` override this (for example, fit the whole diagram or return moved blocks).
#[component]
pub fn ZoomControls(
    view: BoardView,
    /// when to show the "reset" button (instead of "view is not initial")
    #[prop(optional, into)]
    changed: Option<Signal<bool>>,
    /// what the "reset" button does (instead of restoring the initial view)
    #[prop(optional)]
    on_reset: Option<Callback<()>>,
    /// what the "100 %" button does (instead of changing zoom without a pan)
    #[prop(optional)]
    on_actual: Option<Callback<()>>,
) -> impl IntoView {
    let shown = move || changed.map_or_else(|| view.changed(), |c| c.get());
    let reset = move |_| match on_reset {
        Some(r) => r.run(()),
        None => view.reset(),
    };
    let actual = move |_| match on_actual {
        Some(a) => a.run(()),
        None => view.set_zoom(1.0),
    };
    view! {
        <div class="lab-zoom" role="group" aria-label=i18n::tr("Board zoom")>
            <button type="button" title=i18n::tr("Zoom out (Ctrl + wheel)") on:click=move |_| view.zoom_by(1.0 / ZOOM_STEP)>"−"</button>
            <button type="button" class="pct" title=i18n::tr("Zoom 100%") on:click=actual>{move || format!("{}%", js_round(view.zoom.get() * 100.0))}</button>
            <button type="button" title=i18n::tr("Zoom in (Ctrl + wheel)") on:click=move |_| view.zoom_by(ZOOM_STEP)>"+"</button>
            {move || shown().then(|| view! { <button type="button" title=i18n::tr("Reset board position and zoom to 100%") on:click=reset>"⌖"</button> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// System design and architecture: a 780×560 window.
    const SD: BoardConfig = BoardConfig::DEFAULT;
    const SD_WORLD: (f64, f64) = (780.0, 560.0);
    /// Networks: a 704×360 window with spare room on the left, zoom 40–400 %, pan is not rounded, window is bounded.
    const NET: BoardConfig = BoardConfig {
        zoom_min: 0.4,
        zoom_max: 4.0,
        home: Point::new(-24.0, 0.0),
        round_pan: false,
        window_limit: Some(Bounds::new((-324.0, 980.0), (-300.0, 660.0))),
        items: Bounds::new((-200.0, 840.0), (-100.0, 460.0)),
        click_slop: 4.0,
    };
    const NET_WORLD: (f64, f64) = (704.0, 360.0);

    #[test]
    fn zoom_stays_within_bounds_and_keeps_the_anchor_point_still() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let v = View { pan: Point::new(100.0, 50.0), zoom: 1.0 };
        // under the anchor is the board point (300, 150); after zooming it stays at the same window spot
        let at = Point::new(300.0, 150.0);
        let z = SD.zoom_at(v, 2.0, at, SD_WORLD);
        assert_eq!(z.zoom, 2.0);
        assert_eq!((at.x - z.pan.x) * z.zoom, (at.x - v.pan.x) * v.zoom);
        assert_eq!((at.y - z.pan.y) * z.zoom, (at.y - v.pan.y) * v.zoom);
        assert_eq!(SD.zoom_at(v, 100.0, Point::default(), SD_WORLD).zoom, SD.zoom_max);
        assert_eq!(SD.zoom_at(v, 0.0001, Point::default(), SD_WORLD).zoom, SD.zoom_min);
        // at the limit nothing changes
        let top = View { pan: Point::new(5.0, 5.0), zoom: SD.zoom_max };
        assert_eq!(SD.zoom_at(top, 2.0, Point::default(), SD_WORLD), top);
        // not a number is not a zoom
        assert_eq!(SD.zoom_at(v, f64::NAN, Point::default(), SD_WORLD), v);
        // the pan is rounded like in JavaScript
        let r = SD.zoom_at(View { pan: Point::new(0.0, 0.0), zoom: 1.0 }, 1.5, Point::new(100.0, 100.0), SD_WORLD);
        assert_eq!(r.pan, Point::new(33.0, 33.0));
    }

    #[test]
    fn zoom_around_a_pixel_anchor_matches_the_board_point_formula() {
        let _ru = locales::guard(i18n::Locale::Ru);
        // the anchor is 200×100 px from the board corner at 1 px per unit: under it is the point (300, 150)
        let v = View { pan: Point::new(100.0, 50.0), zoom: 1.0 };
        let m = metrics(0.0, 0.0, 780.0, 560.0, 780.0, 560.0);
        let at = m.to_board(Point::new(200.0, 100.0), v);
        assert_eq!(at, Point::new(300.0, 150.0));
        let z = SD.zoom_at(v, 2.0, at, SD_WORLD);
        assert_eq!(z.pan.x + 200.0 / 2.0, 300.0);
        assert_eq!(z.pan.y + 100.0 / 2.0, 150.0);
    }

    #[test]
    fn net_zoom_keeps_the_anchor_point_still_and_stays_in_bounds() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let home = NET.home_view();
        let anchor = Point::new(300.0, 100.0);
        let z = NET.zoom_at(home, 2.0, anchor, NET_WORLD);
        assert_eq!(z.zoom, 2.0);
        // the anchor's fractional position in the window did not change
        let (w0, h0, w1, h1) = (NET_WORLD.0, NET_WORLD.1, NET_WORLD.0 / z.zoom, NET_WORLD.1 / z.zoom);
        let before = ((anchor.x - home.pan.x) / w0, (anchor.y - home.pan.y) / h0);
        let after = ((anchor.x - z.pan.x) / w1, (anchor.y - z.pan.y) / h1);
        assert!((before.0 - after.0).abs() < 1e-9 && (before.1 - after.1).abs() < 1e-9);
        assert_eq!(NET.zoom_at(home, 100.0, anchor, NET_WORLD).zoom, NET.zoom_max);
        assert!((NET.zoom_at(home, 0.0001, anchor, NET_WORLD).zoom - NET.zoom_min).abs() < 1e-9);
        // at the limit nothing changes
        let top = NET.zoom_at(home, 100.0, anchor, NET_WORLD);
        assert_eq!(NET.zoom_at(top, 2.0, anchor, NET_WORLD), top);
        // not a number is not a zoom
        assert_eq!(NET.zoom_at(home, f64::NAN, anchor, NET_WORLD), home);
        // the pan is not rounded
        assert!((NET.zoom_at(home, 1.5, Point::new(0.0, 0.0), NET_WORLD).pan.x + 16.0).abs() < 1e-9);
    }

    #[test]
    fn zoom_to_keeps_the_center() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let home = NET.home_view();
        let z = NET.zoom_to(home, 2.0, NET_WORLD);
        assert_eq!(z.zoom, 2.0);
        let (c0, c1) = (home.center(NET_WORLD), z.center(NET_WORLD));
        assert!((c0.x - c1.x).abs() < 1e-9 && (c0.y - c1.y).abs() < 1e-9);
        assert_eq!(NET.zoom_to(z, 1.0, NET_WORLD), home);
    }

    #[test]
    fn window_center_is_the_middle_of_the_visible_board() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(NET.home_view().center(NET_WORLD), Point::new(328.0, 180.0));
        assert_eq!(View { pan: Point::new(10.0, 20.0), zoom: 2.0 }.center(SD_WORLD), Point::new(205.0, 160.0));
    }

    #[test]
    fn view_box_shrinks_with_zoom() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let home = SD.home_view();
        assert_eq!(view_box(home, 780.0, 560.0), "0 0 780 560");
        assert_eq!(view_box(View { pan: Point::new(-10.0, 20.0), zoom: 2.0 }, 780.0, 560.0), "-10 20 390 280");
        assert_eq!(view_box(View { pan: Point::new(0.0, 0.0), zoom: 3.0 }, 780.0, 560.0), "0 0 260 186.67");
        // 880×440 window (architecture)
        assert_eq!(view_box(home, 880.0, 440.0), "0 0 880 440");
        assert_eq!(view_box(View { pan: Point::new(-10.0, 20.0), zoom: 2.0 }, 880.0, 440.0), "-10 20 440 220");
        assert_eq!(view_box(View { pan: Point::new(0.0, 0.0), zoom: 3.0 }, 880.0, 440.0), "0 0 293.33 146.67");
        // networks: initial window with spare room on the left
        assert_eq!(view_box(NET.home_view(), NET_WORLD.0, NET_WORLD.1), "-24 0 704 360");
    }

    #[test]
    fn home_view_starts_at_the_configured_pan() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(SD.home_view(), View { pan: Point::new(0.0, 0.0), zoom: 1.0 });
        assert_eq!(NET.home_view(), View { pan: Point::new(-24.0, 0.0), zoom: 1.0 });
    }

    #[test]
    fn wheel_zooms_symmetrically() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert!((wheel_factor(0.0) - 1.0).abs() < 1e-12);
        assert!((wheel_factor(100.0) * wheel_factor(-100.0) - 1.0).abs() < 1e-12);
        assert!(wheel_factor(-100.0) > 1.0, "wheel away from you zooms in");
    }

    #[test]
    fn panning_follows_the_hand() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let d = PanDrag { from: Point::new(100.0, 100.0), offset: Point::new(10.0, 10.0), scale: 2.0 };
        // pulled right by 40 px: content moved right, so the window on the board shifted left by 20 units
        assert_eq!(d.pan_at(Point::new(140.0, 100.0)), Point::new(-10.0, 10.0));
        assert_eq!(d.pan_at(Point::new(100.0, 80.0)), Point::new(10.0, 20.0));
        assert_eq!(SD.pan_drag(d, Point::new(140.0, 100.0), 1.0, SD_WORLD).0, Point::new(-10.0, 10.0));
        // the pan is rounded if the board is configured that way
        assert_eq!(SD.pan_drag(d, Point::new(101.0, 100.0), 1.0, SD_WORLD).0, Point::new(10.0, 10.0));
        assert_eq!(NET.pan_drag(d, Point::new(101.0, 100.0), 1.0, NET_WORLD).0, Point::new(9.5, 10.0));
        // pulled right by 40 px in the networks window at 2 px per unit zoom: the window shifted by 20 units
        let s = PanDrag { from: Point::new(0.0, 0.0), offset: NET.home, scale: 2.0 };
        assert_eq!(NET.pan_drag(s, Point::new(40.0, -10.0), 1.0, NET_WORLD).0, Point::new(-44.0, 5.0));
    }

    #[test]
    fn panning_cannot_carry_the_board_away() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let d = PanDrag { from: Point::new(0.0, 0.0), offset: NET.home, scale: 1.0 };
        // pulled left and up by a hundred thousand px: the window center hit the limit
        let (pan, rebased) = NET.pan_drag(d, Point::new(-100_000.0, 100_000.0), 1.0, NET_WORLD);
        let c = View { pan, zoom: 1.0 }.center(NET_WORLD);
        assert_eq!((c.x, c.y), (980.0, -300.0));
        // the gesture is rebased: move the hand back a little and the board immediately goes back, instead of "catching up" a hundred thousand px
        let (back, _) = NET.pan_drag(rebased, Point::new(-99_990.0, 100_000.0), 1.0, NET_WORLD);
        assert_eq!(back.x, pan.x - 10.0);
        // without limits the gesture does not change
        let (_, same) = SD.pan_drag(d, Point::new(-100_000.0, 0.0), 1.0, SD_WORLD);
        assert_eq!(same, d);
    }

    #[test]
    fn constrain_keeps_the_window_inside_and_leaves_free_boards_alone() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let far = View { pan: Point::new(100_000.0, -100_000.0), zoom: 1.0 };
        let c = NET.constrain(far, NET_WORLD).center(NET_WORLD);
        assert_eq!((c.x, c.y), (980.0, -300.0));
        assert_eq!(NET.constrain(NET.home_view(), NET_WORLD), NET.home_view());
        assert_eq!(SD.constrain(far, SD_WORLD), far);
    }

    #[test]
    fn click_is_a_small_move() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert!(SD.is_click(Point::new(10.0, 10.0), Point::new(12.0, 13.0)));
        assert!(!SD.is_click(Point::new(10.0, 10.0), Point::new(10.0, 16.0)));
        // networks have a smaller threshold
        assert!(NET.is_click(Point::new(10.0, 10.0), Point::new(12.0, 11.0)));
        assert!(!NET.is_click(Point::new(10.0, 10.0), Point::new(10.0, 14.0)));
    }

    #[test]
    fn dragged_item_keeps_its_grip_and_stays_in_the_world() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let d = ItemDrag::start(Point::new(105.0, 52.0), Point::new(100.0, 50.0));
        // the pointer shifted by (20, 10), so the element did by the same amount
        let to = SD.items.snap(d.at(Point::new(125.0, 62.0)));
        assert_eq!(to, Point::new(120.0, 60.0));
        assert!(d.moved_far(to, 6.0));
        assert!(!d.moved_far(Point::new(103.0, 52.0), 6.0));
        assert_eq!(SD.items.snap(d.at(Point::new(9000.0, -9000.0))), Point::new(2600.0, -2600.0));
        // coordinates are rounded like in JavaScript
        assert_eq!(SD.items.snap(d.at(Point::new(105.4, 52.6))), Point::new(100.0, 51.0));
    }

    #[test]
    fn metrics_fit_the_board_into_the_svg_and_map_points_back() {
        let _ru = locales::guard(i18n::Locale::Ru);
        // a 780×560 board in a 1560×1120 svg: zoom 2, no margins
        let m = metrics(100.0, 50.0, 1560.0, 1120.0, 780.0, 560.0);
        assert_eq!((m.base, m.off_x, m.off_y), (2.0, 0.0, 0.0));
        let home = SD.home_view();
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), home);
        assert_eq!(p, Point::new(200.0, 100.0));
        // at zoom 2 and pan (10, 20) the same pixel is a different board point
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), View { pan: Point::new(10.0, 20.0), zoom: 2.0 });
        assert_eq!(p, Point::new(110.0, 70.0));
        // svg wider than the board: margins left and right, the point is measured from the fitted board
        let wide = metrics(0.0, 0.0, 1000.0, 560.0, 780.0, 560.0);
        assert_eq!((wide.base, wide.off_x, wide.off_y), (1.0, 110.0, 0.0));
        assert_eq!(wide.to_board(Point::new(110.0, 0.0), home), Point::new(0.0, 0.0));
        // zero size gives no infinities
        let none = metrics(0.0, 0.0, 0.0, 0.0, 780.0, 560.0);
        assert_eq!(none.to_board(Point::new(5.0, 5.0), home), Point::new(0.0, 0.0));
    }

    #[test]
    fn net_mouse_maps_into_the_board_with_letterboxing() {
        let _ru = locales::guard(i18n::Locale::Ru);
        // svg twice as large as the networks window: zoom 2, no margins
        let home = NET.home_view();
        let m = metrics(100.0, 50.0, 1408.0, 720.0, NET_WORLD.0, NET_WORLD.1);
        assert_eq!(m.base, 2.0);
        assert_eq!(m.to_board(Point::new(100.0, 50.0), home), Point::new(-24.0, 0.0));
        assert_eq!(m.to_board(Point::new(100.0 + 2.0 * 124.0, 50.0 + 2.0 * 10.0), home), Point::new(100.0, 10.0));
        // svg wider than the window: margins left and right
        let wide = metrics(0.0, 0.0, 904.0, 360.0, NET_WORLD.0, NET_WORLD.1);
        assert_eq!(wide.base, 1.0);
        assert_eq!(wide.to_board(Point::new(100.0, 0.0), home), Point::new(-24.0, 0.0));
        // no size: the window corner
        let none = metrics(0.0, 0.0, 0.0, 0.0, NET_WORLD.0, NET_WORLD.1);
        assert_eq!(none.to_board(Point::new(5.0, 5.0), home), Point::new(-24.0, 0.0));
    }

    #[test]
    fn js_round_rounds_halves_up() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert_eq!(js_round(2.5), 3.0);
        assert_eq!(js_round(-2.5), -2.0);
        assert_eq!(js_round(-2.6), -3.0);
    }

    #[test]
    fn items_are_held_inside_the_world() {
        let _ru = locales::guard(i18n::Locale::Ru);
        // symmetric area: coordinates are no further than the limit
        assert_eq!(SD.items.clamp(Point::new(5000.0, -5000.0), (0.0, 0.0)), Point::new(2600.0, -2600.0));
        assert_eq!(SD.items.clamp(Point::new(10.0, 10.0), (0.0, 0.0)), Point::new(10.0, 10.0));
        // architecture area: the element's top-left corner is such that it fits entirely
        let arch = Bounds::new((-4000.0, 4000.0), (-3000.0, 3000.0));
        assert_eq!(arch.clamp(Point::new(9000.0, 5000.0), (64.0, 48.0)), Point::new(3936.0, 2952.0));
        assert_eq!(arch.clamp(Point::new(-9000.0, -5000.0), (64.0, 48.0)), Point::new(-4000.0, -3000.0));
        assert_eq!(arch.clamp(Point::new(10.0, 20.0), (64.0, 48.0)), Point::new(10.0, 20.0));
        // a device in networks: integer coordinates within the field
        assert_eq!(NET.items.snap(Point::new(90.4, 270.6)), Point::new(90.0, 271.0));
        assert_eq!(NET.items.snap(Point::new(5000.0, -5000.0)), Point::new(840.0, -100.0));
    }

    #[test]
    fn manual_height_keeps_the_aspect_of_the_window() {
        let _ru = locales::guard(i18n::Locale::Ru);
        // svg 880×330 px: a window onto the board of 880×330 units
        assert_eq!(world_height_for(330.0, 880.0, 880.0), Some(330.0));
        assert_eq!(world_height_for(660.0, 440.0, 880.0), Some(1320.0));
        assert_eq!(world_height_for(300.0, 0.0, 880.0), None);
    }

    #[test]
    fn size_change_below_half_a_pixel_is_ignored() {
        let _ru = locales::guard(i18n::Locale::Ru);
        assert!(!size_differs((100.0, 50.0), (100.3, 50.0)));
        assert!(size_differs((100.0, 50.0), (101.0, 50.0)));
    }
}
