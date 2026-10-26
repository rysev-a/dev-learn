//! Окно на «бесконечную» доску, общее для всех досок лабораторий (системный дизайн, архитектура, сети): сдвиг (пустое
//! место, средняя кнопка мыши), масштаб (Ctrl/⌘ + колесо, кнопки), перевод экранных координат в координаты доски,
//! перетаскивание элементов и наблюдатель за размером элемента. В React это `useBoardView.tsx` и `board-pan.ts`.
//!
//! Арифметика — чистые типы и функции (с тестами); [`BoardView`] только связывает их с сигналами и размерами `<svg>`.
//! Доска — окно (`viewBox`) на плоскость: при масштабе `z` видно кусок размером `ширина/z × высота/z`, начиная с точки
//! `pan`; `<svg>` вписывает окно в свои размеры с сохранением пропорций (`preserveAspectRatio = xMidYMid meet`).
//!
//! Чем доски различаются — пределы масштаба, исходный сдвиг, округление, границы мира и порог щелчка — собрано в
//! [`BoardConfig`]; у каждой лаборатории своя константа, а код один.

use leptos::{html::ElementType, prelude::*, svg};
use wasm_bindgen::JsCast;

use crate::dom;

/// Шаг кнопок масштаба.
pub const ZOOM_STEP: f64 = 1.25;

// --- чистая арифметика --------------------------------------------------------------------------

/// `Math.round` в JavaScript: половина округляется к +∞.
pub fn js_round(x: f64) -> f64 {
    (x + 0.5).floor()
}

/// Точка (на экране или на доске).
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

/// Сдвиг и масштаб доски.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct View {
    /// левый верхний угол окна на доске
    pub pan: Point,
    pub zoom: f64,
}

impl View {
    /// Центр окна на доске; `world` — размеры окна при масштабе 1.
    pub fn center(&self, world: (f64, f64)) -> Point {
        Point::new(self.pan.x + world.0 / self.zoom / 2.0, self.pan.y + world.1 / self.zoom / 2.0)
    }
}

/// Прямоугольная область на доске: пределы по осям `(от, до)`.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Bounds {
    pub x: (f64, f64),
    pub y: (f64, f64),
}

impl Bounds {
    pub const fn new(x: (f64, f64), y: (f64, f64)) -> Self {
        Self { x, y }
    }

    /// Область, симметричная относительно начала координат.
    pub const fn symmetric(limit: f64) -> Self {
        Self { x: (-limit, limit), y: (-limit, limit) }
    }

    /// Удерживает левый верхний угол элемента размера `size` внутри области (элемент не выходит за её правый и нижний край).
    pub fn clamp(&self, p: Point, size: (f64, f64)) -> Point {
        Point::new(p.x.clamp(self.x.0, self.x.1 - size.0), p.y.clamp(self.y.0, self.y.1 - size.1))
    }

    /// Точка в области, с целыми координатами (как `Math.round` в JavaScript).
    pub fn snap(&self, p: Point) -> Point {
        let p = self.clamp(p, (0.0, 0.0));
        Point::new(js_round(p.x), js_round(p.y))
    }
}

/// Чем различаются доски: пределы масштаба, исходный сдвиг, округление сдвига, где может быть окно и элементы.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct BoardConfig {
    pub zoom_min: f64,
    pub zoom_max: f64,
    /// левый верхний угол окна в исходном виде (масштаб исходного вида — 100 %)
    pub home: Point,
    /// сдвиг всегда целый (сдвиг рукой и масштаб вокруг точки округляются)
    pub round_pan: bool,
    /// где может быть центр окна: доску нельзя «унести» совсем; `None` — без пределов
    pub window_limit: Option<Bounds>,
    /// где могут быть элементы доски
    pub items: Bounds,
    /// сдвиг указателя (px экрана), меньше которого нажатие остаётся щелчком, а не перетаскиванием
    pub click_slop: f64,
}

impl BoardConfig {
    /// Значения по умолчанию: масштаб 30–300 %, целый сдвиг, окно и элементы почти без пределов, порог щелчка 6 px.
    pub const DEFAULT: BoardConfig = BoardConfig {
        zoom_min: 0.3,
        zoom_max: 3.0,
        home: Point::new(0.0, 0.0),
        round_pan: true,
        window_limit: None,
        items: Bounds::symmetric(2600.0),
        click_slop: 6.0,
    };

    /// Исходный вид: исходный сдвиг и масштаб 100 %.
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

    /// Возвращает окно в пределы доски: центр окна не дальше `window_limit`. `world` — размеры окна при масштабе 1.
    pub fn constrain(&self, view: View, world: (f64, f64)) -> View {
        let Some(limit) = self.window_limit else { return view };
        let (w, h) = (world.0 / view.zoom, world.1 / view.zoom);
        let c = limit.clamp(Point::new(view.pan.x + w / 2.0, view.pan.y + h / 2.0), (0.0, 0.0));
        View { pan: Point::new(c.x - w / 2.0, c.y - h / 2.0), zoom: view.zoom }
    }

    /// Меняет масштаб в `factor` раз (больше 1 — приближает), не сдвигая точку доски `at` под курсором.
    pub fn zoom_at(&self, view: View, factor: f64, at: Point, world: (f64, f64)) -> View {
        let zoom = self.clamp_zoom(view.zoom * factor);
        if !zoom.is_finite() || (zoom - view.zoom).abs() < 1e-9 {
            return view;
        }
        let r = view.zoom / zoom;
        let pan = self.snap_pan(Point::new(at.x - (at.x - view.pan.x) * r, at.y - (at.y - view.pan.y) * r));
        self.constrain(View { pan, zoom }, world)
    }

    /// Окно нужного масштаба с той же серединой (кнопка «100 %» в сетях).
    pub fn zoom_to(&self, view: View, zoom: f64, world: (f64, f64)) -> View {
        self.zoom_at(view, zoom / view.zoom, view.center(world), world)
    }

    /// Сдвиг рукой: новый сдвиг окна и (если окно упёрлось в предел) «перебазированный» жест — доска, дальше уже не
    /// уезжающая, не заставляет вернуть руку на то место, где она «перетянула».
    pub fn pan_drag(&self, d: PanDrag, now: Point, zoom: f64, world: (f64, f64)) -> (Point, PanDrag) {
        let want = self.snap_pan(d.pan_at(now));
        let pan = self.constrain(View { pan: want, zoom }, world).pan;
        let d = if pan == want { d } else { PanDrag { from: now, offset: pan, ..d } };
        (pan, d)
    }

    /// Нажатие и отпускание почти в одной точке — это щелчок.
    pub fn is_click(&self, down: Point, up: Point) -> bool {
        (up.x - down.x).hypot(up.y - down.y) < self.click_slop
    }
}

/// Значение атрибута `viewBox` для окна `w × h` при масштабе 1: чем крупнее масштаб, тем меньше кусок доски.
pub fn view_box(view: View, w: f64, h: f64) -> String {
    let r = |n: f64| js_round(n * 100.0) / 100.0;
    format!("{} {} {} {}", r(view.pan.x), r(view.pan.y), r(w / view.zoom), r(h / view.zoom))
}

/// Коэффициент масштаба за один «тик» колеса: плавно и в обе стороны одинаково.
pub fn wheel_factor(delta_y: f64) -> f64 {
    (-delta_y * 0.0025).exp()
}

/// Высота окна на доску (в единицах доски) при ручной высоте `<svg>` в пикселях: пропорции окна совпадают с `<svg>`,
/// поэтому доска не «плывёт» полями (`worldH` из `GateBoard.tsx`).
pub fn world_height_for(px_height: f64, px_width: f64, world_w: f64) -> Option<f64> {
    (px_width > 0.0 && px_height > 0.0).then(|| px_height * world_w / px_width)
}

/// Сдвиг доски рукой: где нажали (экран), каким был сдвиг и сколько пикселей экрана в единице доски.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct PanDrag {
    pub from: Point,
    pub offset: Point,
    pub scale: f64,
}

impl PanDrag {
    /// Сдвиг окна, когда указатель в `now`: доска «едет» за рукой (потянули вправо — содержимое сдвинулось вправо).
    pub fn pan_at(&self, now: Point) -> Point {
        Point::new(self.offset.x - (now.x - self.from.x) / self.scale, self.offset.y - (now.y - self.from.y) / self.scale)
    }
}

/// Перетаскивание элемента доски: где элемент стоял и на сколько указатель был смещён от его угла в момент нажатия.
#[derive(Clone, Copy, Debug, PartialEq, Default)]
pub struct ItemDrag {
    pub from: Point,
    pub grip: Point,
}

impl ItemDrag {
    /// Нажали на элемент, стоящий в `at`, указатель (в координатах доски) — в `pointer`.
    pub fn start(pointer: Point, at: Point) -> Self {
        Self { from: at, grip: Point::new(at.x - pointer.x, at.y - pointer.y) }
    }

    /// Где элемент для указателя `pointer` (границы мира — на вызывающем: [`Bounds::clamp`] или [`Bounds::snap`]).
    pub fn at(&self, pointer: Point) -> Point {
        Point::new(pointer.x + self.grip.x, pointer.y + self.grip.y)
    }

    /// Элемент уехал от места нажатия дальше `slop` — это перетаскивание, а не щелчок.
    pub fn moved_far(&self, now: Point, slop: f64) -> bool {
        (now.x - self.from.x).hypot(now.y - self.from.y) > slop
    }
}

/// Где доска на экране: прямоугольник `<svg>`, пикселей на единицу доски при масштабе 1 и поля вокруг вписанной доски.
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

/// Метрики для окна `view_w × view_h`, вписанного в прямоугольник `<svg>`. Рамка (1 px) в размерах не учитывается.
pub fn metrics(left: f64, top: f64, width: f64, height: f64, view_w: f64, view_h: f64) -> Metrics {
    let base = (width / view_w).min(height / view_h);
    Metrics { left, top, width, height, base, off_x: (width - view_w * base) / 2.0, off_y: (height - view_h * base) / 2.0 }
}

impl Metrics {
    /// Экранная точка (`clientX`, `clientY`) в координатах доски с учётом сдвига и масштаба.
    pub fn to_board(&self, client: Point, view: View) -> Point {
        let scale = self.base * view.zoom;
        if scale.is_nan() || scale <= 0.0 {
            return view.pan;
        }
        Point::new(view.pan.x + (client.x - self.left - self.off_x) / scale, view.pan.y + (client.y - self.top - self.off_y) / scale)
    }
}

// --- состояние доски ----------------------------------------------------------------------------

/// Окно на доску: сдвиг, масштаб и перевод координат. Копируется как набор сигналов.
#[derive(Clone, Copy)]
pub struct BoardView {
    /// корневой `<svg>` доски
    pub svg: NodeRef<svg::Svg>,
    pub pan: RwSignal<Point>,
    pub zoom: RwSignal<f64>,
    /// идёт сдвиг доски рукой
    pub panning: RwSignal<bool>,
    cfg: BoardConfig,
    /// размеры окна на доску при масштабе 1 (ширина, высота)
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

    /// Вернуть исходный вид.
    pub fn reset(&self) {
        self.set_view(self.cfg.home_view());
    }

    /// Доска сдвинута или масштаб не 100 % (в реактивном контексте — подписка).
    pub fn changed(&self) -> bool {
        self.view() != self.cfg.home_view()
    }

    /// Значение `viewBox` (в реактивном контексте — подписка на сдвиг, масштаб и размеры окна).
    pub fn view_box(&self) -> String {
        let (w, h) = self.world.get();
        view_box(self.view(), w, h)
    }

    /// Где доска на экране сейчас; `None`, пока `<svg>` не появился или у него нет размера.
    pub fn metrics(&self) -> Option<Metrics> {
        let rect = self.svg.get_untracked()?.get_bounding_client_rect();
        let (w, h) = self.world.get_untracked();
        let m = metrics(rect.left(), rect.top(), rect.width(), rect.height(), w, h);
        (m.base > 0.0 && m.base.is_finite()).then_some(m)
    }

    /// Экранная точка в координатах доски (без подписки на сигналы: вызывается в обработчиках событий).
    pub fn to_board(&self, client_x: f64, client_y: f64) -> Point {
        match self.metrics() {
            Some(m) => m.to_board(Point::new(client_x, client_y), self.view_untracked()),
            None => Point::default(),
        }
    }

    /// Точка экрана лежит над доской.
    pub fn contains_client(&self, client: Point) -> bool {
        self.svg.get_untracked().is_some_and(|s| {
            let r = s.get_bounding_client_rect();
            client.x >= r.left() && client.x <= r.right() && client.y >= r.top() && client.y <= r.bottom()
        })
    }

    /// Нажатие и отпускание почти в одной точке — это щелчок (порог — из настроек доски).
    pub fn is_click(&self, down: Point, up: Point) -> bool {
        self.cfg.is_click(down, up)
    }

    /// Начало сдвига доски рукой.
    pub fn begin_pan(&self, client_x: f64, client_y: f64) {
        let Some(m) = self.metrics() else { return };
        let view = self.view_untracked();
        self.drag.set_value(Some(PanDrag { from: Point::new(client_x, client_y), offset: view.pan, scale: m.base * view.zoom }));
        self.panning.set(true);
    }

    /// Двигает доску за рукой, пока идёт сдвиг; `true` — событие обработано.
    pub fn move_pan(&self, client_x: f64, client_y: f64) -> bool {
        let Some(d) = self.drag.get_value() else { return false };
        let (pan, d) = self.cfg.pan_drag(d, Point::new(client_x, client_y), self.zoom.get_untracked(), self.world.get_untracked());
        self.drag.set_value(Some(d));
        self.pan.set(pan);
        true
    }

    /// Конец сдвига; `true` — сдвиг шёл.
    pub fn end_pan(&self) -> bool {
        if self.drag.get_value().is_none() {
            return false;
        }
        self.drag.set_value(None);
        self.panning.set(false);
        true
    }

    /// Кнопки масштаба: вокруг центра окна.
    pub fn zoom_by(&self, factor: f64) {
        let view = self.view_untracked();
        let world = self.world.get_untracked();
        self.set_view(self.cfg.zoom_at(view, factor, view.center(world), world));
    }

    /// Масштаб `zoom` с той же серединой окна.
    pub fn zoom_to(&self, zoom: f64) {
        self.set_view(self.cfg.zoom_to(self.view_untracked(), zoom, self.world.get_untracked()));
    }

    /// Масштаб `zoom`, сдвиг остаётся прежним (левый верхний угол окна стоит на месте).
    pub fn set_zoom(&self, zoom: f64) {
        self.zoom.set(zoom);
    }

    /// Колесо над доской: с Ctrl/⌘ — масштаб вокруг курсора (страница при этом не прокручивается). Доска во весь
    /// экран (`always`) масштабируется и простым колесом.
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

    /// Нажатие на доске: средняя кнопка или левая на пустом месте (`background`) начинает сдвиг. `true` — нажатие обработано.
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

// --- помощники DOM ------------------------------------------------------------------------------

/// Страница главы развёрнута на весь экран: доски заполняют оболочку (класс `fill`).
pub fn use_fullscreen() -> impl Fn() -> bool + Copy + Send + Sync + 'static {
    let fs = use_context::<crate::components::fullscreen::Fullscreen>();
    move || fs.is_some_and(|f| f.is_on())
}

/// Нажатие пришлось на сам `<svg>` или на точечный фон (`bg_class`): здесь начинается сдвиг доски.
pub fn is_background(target: Option<web_sys::EventTarget>, bg_class: &str) -> bool {
    let Some(el) = target.and_then(|t| t.dyn_into::<web_sys::Element>().ok()) else {
        return false;
    };
    el.tag_name().eq_ignore_ascii_case("svg") || el.get_attribute("class").is_some_and(|c| c.split_whitespace().any(|x| x == bg_class))
}

/// Событие пришло из элемента, который лежит внутри `selector` (или сам им является).
pub fn target_within(target: Option<web_sys::EventTarget>, selector: &str) -> bool {
    target.and_then(|t| t.dyn_into::<web_sys::Element>().ok()).and_then(|el| el.closest(selector).ok().flatten()).is_some()
}

/// Размер элемента `(ширина, высота)` в пикселях; обновляется при каждом изменении размера (`ResizeObserver`).
/// Пока элемента нет, размер нулевой.
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

/// Кнопки масштаба над доской: −, процент (100 %), +, «вернуть на место».
///
/// По умолчанию «⌖» виден, когда вид отличается от исходного, и возвращает его, а «100 %» меняет масштаб, не трогая
/// сдвиг. `changed`, `on_reset` и `on_actual` подменяют это (например, вписать схему целиком или вернуть сдвинутые блоки).
#[component]
pub fn ZoomControls(
    view: BoardView,
    /// когда показывать кнопку «вернуть» (вместо «вид не исходный»)
    #[prop(optional, into)]
    changed: Option<Signal<bool>>,
    /// что делает кнопка «вернуть» (вместо возврата исходного вида)
    #[prop(optional)]
    on_reset: Option<Callback<()>>,
    /// что делает кнопка «100 %» (вместо смены масштаба без сдвига)
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
        <div class="lab-zoom" role="group" aria-label="Масштаб доски">
            <button type="button" title="Уменьшить (Ctrl + колесо)" on:click=move |_| view.zoom_by(1.0 / ZOOM_STEP)>"−"</button>
            <button type="button" class="pct" title="Масштаб 100 %" on:click=actual>{move || format!("{}%", js_round(view.zoom.get() * 100.0))}</button>
            <button type="button" title="Увеличить (Ctrl + колесо)" on:click=move |_| view.zoom_by(ZOOM_STEP)>"+"</button>
            {move || shown().then(|| view! { <button type="button" title="Вернуть доску на место и масштаб 100 %" on:click=reset>"⌖"</button> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Системный дизайн и архитектура: окно 780×560.
    const SD: BoardConfig = BoardConfig::DEFAULT;
    const SD_WORLD: (f64, f64) = (780.0, 560.0);
    /// Сети: окно 704×360 с запасом слева, масштаб 40–400 %, сдвиг не округляется, окно ограничено.
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
        let v = View { pan: Point::new(100.0, 50.0), zoom: 1.0 };
        // под якорем — точка доски (300, 150); после масштаба она на том же месте окна
        let at = Point::new(300.0, 150.0);
        let z = SD.zoom_at(v, 2.0, at, SD_WORLD);
        assert_eq!(z.zoom, 2.0);
        assert_eq!((at.x - z.pan.x) * z.zoom, (at.x - v.pan.x) * v.zoom);
        assert_eq!((at.y - z.pan.y) * z.zoom, (at.y - v.pan.y) * v.zoom);
        assert_eq!(SD.zoom_at(v, 100.0, Point::default(), SD_WORLD).zoom, SD.zoom_max);
        assert_eq!(SD.zoom_at(v, 0.0001, Point::default(), SD_WORLD).zoom, SD.zoom_min);
        // у предела ничего не меняется
        let top = View { pan: Point::new(5.0, 5.0), zoom: SD.zoom_max };
        assert_eq!(SD.zoom_at(top, 2.0, Point::default(), SD_WORLD), top);
        // не число — не масштаб
        assert_eq!(SD.zoom_at(v, f64::NAN, Point::default(), SD_WORLD), v);
        // сдвиг округляется, как в JavaScript
        let r = SD.zoom_at(View { pan: Point::new(0.0, 0.0), zoom: 1.0 }, 1.5, Point::new(100.0, 100.0), SD_WORLD);
        assert_eq!(r.pan, Point::new(33.0, 33.0));
    }

    #[test]
    fn zoom_around_a_pixel_anchor_matches_the_board_point_formula() {
        // якорь в 200×100 px от угла доски при 1 px на единицу: под ним точка (300, 150)
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
        let home = NET.home_view();
        let anchor = Point::new(300.0, 100.0);
        let z = NET.zoom_at(home, 2.0, anchor, NET_WORLD);
        assert_eq!(z.zoom, 2.0);
        // доля положения якоря в окне не изменилась
        let (w0, h0, w1, h1) = (NET_WORLD.0, NET_WORLD.1, NET_WORLD.0 / z.zoom, NET_WORLD.1 / z.zoom);
        let before = ((anchor.x - home.pan.x) / w0, (anchor.y - home.pan.y) / h0);
        let after = ((anchor.x - z.pan.x) / w1, (anchor.y - z.pan.y) / h1);
        assert!((before.0 - after.0).abs() < 1e-9 && (before.1 - after.1).abs() < 1e-9);
        assert_eq!(NET.zoom_at(home, 100.0, anchor, NET_WORLD).zoom, NET.zoom_max);
        assert!((NET.zoom_at(home, 0.0001, anchor, NET_WORLD).zoom - NET.zoom_min).abs() < 1e-9);
        // у предела ничего не меняется
        let top = NET.zoom_at(home, 100.0, anchor, NET_WORLD);
        assert_eq!(NET.zoom_at(top, 2.0, anchor, NET_WORLD), top);
        // не число — не масштаб
        assert_eq!(NET.zoom_at(home, f64::NAN, anchor, NET_WORLD), home);
        // сдвиг не округляется
        assert!((NET.zoom_at(home, 1.5, Point::new(0.0, 0.0), NET_WORLD).pan.x + 16.0).abs() < 1e-9);
    }

    #[test]
    fn zoom_to_keeps_the_center() {
        let home = NET.home_view();
        let z = NET.zoom_to(home, 2.0, NET_WORLD);
        assert_eq!(z.zoom, 2.0);
        let (c0, c1) = (home.center(NET_WORLD), z.center(NET_WORLD));
        assert!((c0.x - c1.x).abs() < 1e-9 && (c0.y - c1.y).abs() < 1e-9);
        assert_eq!(NET.zoom_to(z, 1.0, NET_WORLD), home);
    }

    #[test]
    fn window_center_is_the_middle_of_the_visible_board() {
        assert_eq!(NET.home_view().center(NET_WORLD), Point::new(328.0, 180.0));
        assert_eq!(View { pan: Point::new(10.0, 20.0), zoom: 2.0 }.center(SD_WORLD), Point::new(205.0, 160.0));
    }

    #[test]
    fn view_box_shrinks_with_zoom() {
        let home = SD.home_view();
        assert_eq!(view_box(home, 780.0, 560.0), "0 0 780 560");
        assert_eq!(view_box(View { pan: Point::new(-10.0, 20.0), zoom: 2.0 }, 780.0, 560.0), "-10 20 390 280");
        assert_eq!(view_box(View { pan: Point::new(0.0, 0.0), zoom: 3.0 }, 780.0, 560.0), "0 0 260 186.67");
        // окно 880×440 (архитектура)
        assert_eq!(view_box(home, 880.0, 440.0), "0 0 880 440");
        assert_eq!(view_box(View { pan: Point::new(-10.0, 20.0), zoom: 2.0 }, 880.0, 440.0), "-10 20 440 220");
        assert_eq!(view_box(View { pan: Point::new(0.0, 0.0), zoom: 3.0 }, 880.0, 440.0), "0 0 293.33 146.67");
        // сети: исходное окно с запасом слева
        assert_eq!(view_box(NET.home_view(), NET_WORLD.0, NET_WORLD.1), "-24 0 704 360");
    }

    #[test]
    fn home_view_starts_at_the_configured_pan() {
        assert_eq!(SD.home_view(), View { pan: Point::new(0.0, 0.0), zoom: 1.0 });
        assert_eq!(NET.home_view(), View { pan: Point::new(-24.0, 0.0), zoom: 1.0 });
    }

    #[test]
    fn wheel_zooms_symmetrically() {
        assert!((wheel_factor(0.0) - 1.0).abs() < 1e-12);
        assert!((wheel_factor(100.0) * wheel_factor(-100.0) - 1.0).abs() < 1e-12);
        assert!(wheel_factor(-100.0) > 1.0, "колесо от себя приближает");
    }

    #[test]
    fn panning_follows_the_hand() {
        let d = PanDrag { from: Point::new(100.0, 100.0), offset: Point::new(10.0, 10.0), scale: 2.0 };
        // потянули вправо на 40 px: содержимое уехало вправо — окно на доске сдвинулось влево на 20 единиц
        assert_eq!(d.pan_at(Point::new(140.0, 100.0)), Point::new(-10.0, 10.0));
        assert_eq!(d.pan_at(Point::new(100.0, 80.0)), Point::new(10.0, 20.0));
        assert_eq!(SD.pan_drag(d, Point::new(140.0, 100.0), 1.0, SD_WORLD).0, Point::new(-10.0, 10.0));
        // сдвиг округляется, если так настроено доской
        assert_eq!(SD.pan_drag(d, Point::new(101.0, 100.0), 1.0, SD_WORLD).0, Point::new(10.0, 10.0));
        assert_eq!(NET.pan_drag(d, Point::new(101.0, 100.0), 1.0, NET_WORLD).0, Point::new(9.5, 10.0));
        // потянули вправо на 40 px в окне сетей при масштабе 2 px на единицу: окно сдвинулось на 20 единиц
        let s = PanDrag { from: Point::new(0.0, 0.0), offset: NET.home, scale: 2.0 };
        assert_eq!(NET.pan_drag(s, Point::new(40.0, -10.0), 1.0, NET_WORLD).0, Point::new(-44.0, 5.0));
    }

    #[test]
    fn panning_cannot_carry_the_board_away() {
        let d = PanDrag { from: Point::new(0.0, 0.0), offset: NET.home, scale: 1.0 };
        // потянули влево и вверх на сто тысяч px: центр окна упёрся в предел
        let (pan, rebased) = NET.pan_drag(d, Point::new(-100_000.0, 100_000.0), 1.0, NET_WORLD);
        let c = View { pan, zoom: 1.0 }.center(NET_WORLD);
        assert_eq!((c.x, c.y), (980.0, -300.0));
        // жест перебазирован: чуть вернули руку — доска сразу поехала обратно, а не «догоняет» сто тысяч px
        let (back, _) = NET.pan_drag(rebased, Point::new(-99_990.0, 100_000.0), 1.0, NET_WORLD);
        assert_eq!(back.x, pan.x - 10.0);
        // без пределов жест не меняется
        let (_, same) = SD.pan_drag(d, Point::new(-100_000.0, 0.0), 1.0, SD_WORLD);
        assert_eq!(same, d);
    }

    #[test]
    fn constrain_keeps_the_window_inside_and_leaves_free_boards_alone() {
        let far = View { pan: Point::new(100_000.0, -100_000.0), zoom: 1.0 };
        let c = NET.constrain(far, NET_WORLD).center(NET_WORLD);
        assert_eq!((c.x, c.y), (980.0, -300.0));
        assert_eq!(NET.constrain(NET.home_view(), NET_WORLD), NET.home_view());
        assert_eq!(SD.constrain(far, SD_WORLD), far);
    }

    #[test]
    fn click_is_a_small_move() {
        assert!(SD.is_click(Point::new(10.0, 10.0), Point::new(12.0, 13.0)));
        assert!(!SD.is_click(Point::new(10.0, 10.0), Point::new(10.0, 16.0)));
        // у сетей порог меньше
        assert!(NET.is_click(Point::new(10.0, 10.0), Point::new(12.0, 11.0)));
        assert!(!NET.is_click(Point::new(10.0, 10.0), Point::new(10.0, 14.0)));
    }

    #[test]
    fn dragged_item_keeps_its_grip_and_stays_in_the_world() {
        let d = ItemDrag::start(Point::new(105.0, 52.0), Point::new(100.0, 50.0));
        // указатель сместился на (20, 10) — элемент на столько же
        let to = SD.items.snap(d.at(Point::new(125.0, 62.0)));
        assert_eq!(to, Point::new(120.0, 60.0));
        assert!(d.moved_far(to, 6.0));
        assert!(!d.moved_far(Point::new(103.0, 52.0), 6.0));
        assert_eq!(SD.items.snap(d.at(Point::new(9000.0, -9000.0))), Point::new(2600.0, -2600.0));
        // координаты округляются, как в JavaScript
        assert_eq!(SD.items.snap(d.at(Point::new(105.4, 52.6))), Point::new(100.0, 51.0));
    }

    #[test]
    fn metrics_fit_the_board_into_the_svg_and_map_points_back() {
        // доска 780×560 в svg 1560×1120: масштаб 2, полей нет
        let m = metrics(100.0, 50.0, 1560.0, 1120.0, 780.0, 560.0);
        assert_eq!((m.base, m.off_x, m.off_y), (2.0, 0.0, 0.0));
        let home = SD.home_view();
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), home);
        assert_eq!(p, Point::new(200.0, 100.0));
        // при масштабе 2 и сдвиге (10, 20) тот же пиксель — другая точка доски
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), View { pan: Point::new(10.0, 20.0), zoom: 2.0 });
        assert_eq!(p, Point::new(110.0, 70.0));
        // svg шире доски: слева и справа поля, точка отсчитывается от вписанной доски
        let wide = metrics(0.0, 0.0, 1000.0, 560.0, 780.0, 560.0);
        assert_eq!((wide.base, wide.off_x, wide.off_y), (1.0, 110.0, 0.0));
        assert_eq!(wide.to_board(Point::new(110.0, 0.0), home), Point::new(0.0, 0.0));
        // нулевой размер не даёт бесконечностей
        let none = metrics(0.0, 0.0, 0.0, 0.0, 780.0, 560.0);
        assert_eq!(none.to_board(Point::new(5.0, 5.0), home), Point::new(0.0, 0.0));
    }

    #[test]
    fn net_mouse_maps_into_the_board_with_letterboxing() {
        // svg вдвое крупнее окна сетей: масштаб 2, полей нет
        let home = NET.home_view();
        let m = metrics(100.0, 50.0, 1408.0, 720.0, NET_WORLD.0, NET_WORLD.1);
        assert_eq!(m.base, 2.0);
        assert_eq!(m.to_board(Point::new(100.0, 50.0), home), Point::new(-24.0, 0.0));
        assert_eq!(m.to_board(Point::new(100.0 + 2.0 * 124.0, 50.0 + 2.0 * 10.0), home), Point::new(100.0, 10.0));
        // svg шире окна: слева и справа поля
        let wide = metrics(0.0, 0.0, 904.0, 360.0, NET_WORLD.0, NET_WORLD.1);
        assert_eq!(wide.base, 1.0);
        assert_eq!(wide.to_board(Point::new(100.0, 0.0), home), Point::new(-24.0, 0.0));
        // нет размера — угол окна
        let none = metrics(0.0, 0.0, 0.0, 0.0, NET_WORLD.0, NET_WORLD.1);
        assert_eq!(none.to_board(Point::new(5.0, 5.0), home), Point::new(-24.0, 0.0));
    }

    #[test]
    fn js_round_rounds_halves_up() {
        assert_eq!(js_round(2.5), 3.0);
        assert_eq!(js_round(-2.5), -2.0);
        assert_eq!(js_round(-2.6), -3.0);
    }

    #[test]
    fn items_are_held_inside_the_world() {
        // симметричная область: координаты не дальше предела
        assert_eq!(SD.items.clamp(Point::new(5000.0, -5000.0), (0.0, 0.0)), Point::new(2600.0, -2600.0));
        assert_eq!(SD.items.clamp(Point::new(10.0, 10.0), (0.0, 0.0)), Point::new(10.0, 10.0));
        // область архитектуры: левый верхний угол элемента — так, чтобы он помещался целиком
        let arch = Bounds::new((-4000.0, 4000.0), (-3000.0, 3000.0));
        assert_eq!(arch.clamp(Point::new(9000.0, 5000.0), (64.0, 48.0)), Point::new(3936.0, 2952.0));
        assert_eq!(arch.clamp(Point::new(-9000.0, -5000.0), (64.0, 48.0)), Point::new(-4000.0, -3000.0));
        assert_eq!(arch.clamp(Point::new(10.0, 20.0), (64.0, 48.0)), Point::new(10.0, 20.0));
        // устройство в сетях: целые координаты в пределах поля
        assert_eq!(NET.items.snap(Point::new(90.4, 270.6)), Point::new(90.0, 271.0));
        assert_eq!(NET.items.snap(Point::new(5000.0, -5000.0)), Point::new(840.0, -100.0));
    }

    #[test]
    fn manual_height_keeps_the_aspect_of_the_window() {
        // svg 880×330 px: окно на доску 880×330 единиц
        assert_eq!(world_height_for(330.0, 880.0, 880.0), Some(330.0));
        assert_eq!(world_height_for(660.0, 440.0, 880.0), Some(1320.0));
        assert_eq!(world_height_for(300.0, 0.0, 880.0), None);
    }

    #[test]
    fn size_change_below_half_a_pixel_is_ignored() {
        assert!(!size_differs((100.0, 50.0), (100.3, 50.0)));
        assert!(size_differs((100.0, 50.0), (101.0, 50.0)));
    }
}
