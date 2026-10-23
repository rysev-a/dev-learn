//! Окно на «бесконечную» доску лаборатории: сдвиг (пустое место, средняя кнопка мыши), масштаб (Ctrl/⌘ + колесо,
//! кнопки), перевод экранных координат в координаты доски и наблюдатель за шириной `<svg>`. В React это
//! `useBoardView.tsx` и `board-pan.ts`.
//!
//! Арифметика — чистые функции вверху файла (с тестами); [`ArchView`] только связывает их с сигналами и размерами
//! `<svg>`. Доска — окно (`viewBox`) на плоскость: при масштабе `z` видно кусок размером `ширина/z × высота/z`, начиная
//! с точки `pan`; `<svg>` вписывает окно в свои размеры с сохранением пропорций (`preserveAspectRatio = xMidYMid meet`).

use leptos::{prelude::*, svg};
use wasm_bindgen::JsCast;

use crate::dom;

/// Границы и шаг масштаба.
pub const ZOOM_MIN: f64 = 0.3;
pub const ZOOM_MAX: f64 = 3.0;
pub const ZOOM_STEP: f64 = 1.25;
/// Сдвиг указателя (px экрана), меньше которого нажатие на контакт считается щелчком, а не перетаскиванием.
pub const CLICK_SLOP: f64 = 6.0;
/// Насколько далеко можно уносить элементы от начала координат.
const WORLD_MIN_X: f64 = -4000.0;
const WORLD_MAX_X: f64 = 4000.0;
const WORLD_MIN_Y: f64 = -3000.0;
const WORLD_MAX_Y: f64 = 3000.0;

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
    /// Исходный вид: начало координат и масштаб 100 %.
    pub const HOME: View = View { pan: Point::new(0.0, 0.0), zoom: 1.0 };

    /// Доска сдвинута или масштаб не 100 %.
    pub fn is_changed(&self) -> bool {
        *self != View::HOME
    }
}

/// `Math.round` в JavaScript: половина округляется к +∞.
pub fn js_round(x: f64) -> f64 {
    (x + 0.5).floor()
}

pub fn clamp_zoom(z: f64) -> f64 {
    z.clamp(ZOOM_MIN, ZOOM_MAX)
}

/// Удерживает левый верхний угол элемента размера `w × h` в пределах «мира» (`clampWorld` из `board-pan.ts`).
pub fn clamp_world(p: Point, w: f64, h: f64) -> Point {
    Point::new(p.x.clamp(WORLD_MIN_X, WORLD_MAX_X - w), p.y.clamp(WORLD_MIN_Y, WORLD_MAX_Y - h))
}

/// Меняет масштаб, не сдвигая точку под курсором. `anchor` — точка в пикселях от угла самой доски (без полей),
/// `base` — пикселей экрана на единицу доски при масштабе 1.
pub fn zoom_around(view: View, factor: f64, anchor: Point, base: f64) -> View {
    let zoom = clamp_zoom(view.zoom * factor);
    if zoom == view.zoom || base.is_nan() || base <= 0.0 {
        return view;
    }
    let (wx, wy) = (anchor.x / (base * view.zoom) + view.pan.x, anchor.y / (base * view.zoom) + view.pan.y);
    View { zoom, pan: Point::new(js_round(wx - anchor.x / (base * zoom)), js_round(wy - anchor.y / (base * zoom))) }
}

/// Значение атрибута `viewBox`: чем крупнее масштаб, тем меньше кусок доски.
pub fn view_box(view: View, w: f64, h: f64) -> String {
    let r = |n: f64| js_round(n * 100.0) / 100.0;
    format!("{} {} {} {}", r(view.pan.x), r(view.pan.y), r(w / view.zoom), r(h / view.zoom))
}

/// Коэффициент масштаба за один «тик» колеса: плавно и в обе стороны одинаково.
pub fn wheel_factor(delta_y: f64) -> f64 {
    (-delta_y * 0.0025).exp()
}

/// Сдвиг доски рукой: где нажали (экран), каким был сдвиг и сколько пикселей экрана в единице доски.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct PanDrag {
    pub from: Point,
    pub offset: Point,
    pub scale: f64,
}

/// Доска «едет» за рукой: потянули вправо — содержимое сдвинулось вправо.
pub fn drag_pan(d: PanDrag, now: Point) -> Point {
    Point::new(js_round(d.offset.x - (now.x - d.from.x) / d.scale), js_round(d.offset.y - (now.y - d.from.y) / d.scale))
}

/// Нажатие и отпускание почти в одной точке — это щелчок.
pub fn is_click(down: Point, up: Point) -> bool {
    (up.x - down.x).hypot(up.y - down.y) < CLICK_SLOP
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

/// Метрики для доски `world_w × world_h`, вписанной в прямоугольник `<svg>`.
pub fn metrics(left: f64, top: f64, width: f64, height: f64, world_w: f64, world_h: f64) -> Metrics {
    let base = (width / world_w).min(height / world_h);
    Metrics { left, top, width, height, base, off_x: (width - world_w * base) / 2.0, off_y: (height - world_h * base) / 2.0 }
}

impl Metrics {
    /// Экранная точка (`clientX`, `clientY`) в координатах доски с учётом сдвига и масштаба.
    pub fn to_board(self, client: Point, view: View) -> Point {
        let scale = self.base * view.zoom;
        if scale.is_nan() || scale <= 0.0 {
            return view.pan;
        }
        Point::new(view.pan.x + (client.x - self.left - self.off_x) / scale, view.pan.y + (client.y - self.top - self.off_y) / scale)
    }

    /// Центр видимой доски в пикселях от её угла: вокруг него работают кнопки масштаба.
    pub fn center(&self) -> Point {
        Point::new((self.width - 2.0 * self.off_x) / 2.0, (self.height - 2.0 * self.off_y) / 2.0)
    }
}

/// Высота окна на доску (в единицах доски) при ручной высоте `<svg>` в пикселях: пропорции окна совпадают с `<svg>`,
/// поэтому доска не «плывёт» полями (`worldH` из `GateBoard.tsx`).
pub fn world_height_for(px_height: f64, px_width: f64, world_w: f64) -> Option<f64> {
    (px_width > 0.0 && px_height > 0.0).then(|| px_height * world_w / px_width)
}

// --- состояние доски ----------------------------------------------------------------------------

/// Окно на доску: сдвиг, масштаб и перевод координат. Копируется как набор сигналов.
#[derive(Clone, Copy)]
pub struct ArchView {
    /// корневой `<svg>` доски
    pub svg: NodeRef<svg::Svg>,
    pub pan: RwSignal<Point>,
    pub zoom: RwSignal<f64>,
    /// идёт сдвиг доски рукой
    pub panning: RwSignal<bool>,
    /// размеры окна на доску при масштабе 1 (ширина, высота)
    world: Signal<(f64, f64)>,
    drag: StoredValue<Option<PanDrag>>,
}

impl ArchView {
    pub fn new(svg: NodeRef<svg::Svg>, world: Signal<(f64, f64)>) -> Self {
        Self { svg, pan: RwSignal::new(Point::default()), zoom: RwSignal::new(1.0), panning: RwSignal::new(false), world, drag: StoredValue::new(None) }
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

    pub fn reset(&self) {
        self.set_view(View::HOME);
    }

    pub fn changed(&self) -> bool {
        self.view().is_changed()
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
    pub fn to_board(self, client_x: f64, client_y: f64) -> Point {
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

    /// Начало сдвига доски рукой.
    pub fn begin_pan(&self, client_x: f64, client_y: f64) {
        let Some(m) = self.metrics() else { return };
        let view = self.view_untracked();
        self.drag.set_value(Some(PanDrag { from: Point::new(client_x, client_y), offset: view.pan, scale: m.base * view.zoom }));
        self.panning.set(true);
    }

    /// Двигает доску за рукой, пока идёт сдвиг; `true` — событие обработано.
    pub fn move_pan(&self, client_x: f64, client_y: f64) -> bool {
        match self.drag.get_value() {
            Some(d) => {
                self.pan.set(drag_pan(d, Point::new(client_x, client_y)));
                true
            }
            None => false,
        }
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

    /// Кнопки масштаба: вокруг центра доски.
    pub fn zoom_by(&self, factor: f64) {
        let Some(m) = self.metrics() else { return };
        self.set_view(zoom_around(self.view_untracked(), factor, m.center(), m.base));
    }

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
        let anchor = Point::new(f64::from(ev.client_x()) - m.left - m.off_x, f64::from(ev.client_y()) - m.top - m.off_y);
        self.set_view(zoom_around(self.view_untracked(), wheel_factor(ev.delta_y()), anchor, m.base));
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

/// Ширина элемента в пикселях; обновляется при каждом изменении размера (`ResizeObserver`), пока элемента нет — 0.
pub fn use_element_width<E>(node: NodeRef<E>) -> ReadSignal<f64>
where
    E: leptos::html::ElementType + 'static,
    E::Output: JsCast + Clone + 'static,
{
    let (width, set_width) = signal(0.0);
    let guard = StoredValue::new_local(None::<dom::ResizeGuard>);
    Effect::new(move |_| {
        let Some(el) = node.get() else { return };
        let el: web_sys::Element = el.unchecked_into();
        let read = {
            let el = el.clone();
            move || {
                let w = el.get_bounding_client_rect().width();
                if (width.get_untracked() - w).abs() > 0.5 {
                    set_width.set(w);
                }
            }
        };
        read();
        guard.set_value(dom::observe_resize(&[el], read));
    });
    width
}

/// Кнопки масштаба над доской: −, процент (100 %), +, «вернуть на место». `extra_changed` — доска изменена чем-то ещё
/// (например, сдвинутыми блоками), `on_reset` — что ещё вернуть кнопкой «⌖».
#[component]
pub fn ZoomControls(view: ArchView, #[prop(optional, into)] extra_changed: Option<Signal<bool>>, #[prop(optional)] on_reset: Option<Callback<()>>) -> impl IntoView {
    let changed = move || view.changed() || extra_changed.is_some_and(|c| c.get());
    let reset = move |_| {
        view.reset();
        if let Some(r) = on_reset {
            r.run(());
        }
    };
    view! {
        <div class="lab-zoom" role="group" aria-label="Масштаб доски">
            <button type="button" title="Уменьшить (Ctrl + колесо)" on:click=move |_| view.zoom_by(1.0 / ZOOM_STEP)>"−"</button>
            <button type="button" class="pct" title="Масштаб 100 %" on:click=move |_| view.set_zoom(1.0)>{move || format!("{}%", js_round(view.zoom.get() * 100.0))}</button>
            <button type="button" title="Увеличить (Ctrl + колесо)" on:click=move |_| view.zoom_by(ZOOM_STEP)>"+"</button>
            {move || changed().then(|| view! { <button type="button" title="Вернуть доску на место и масштаб 100 %" on:click=reset>"⌖"</button> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zoom_stays_within_bounds_and_keeps_the_anchor_point_still() {
        let v = View { pan: Point::new(100.0, 50.0), zoom: 1.0 };
        let z = zoom_around(v, 2.0, Point::new(200.0, 100.0), 1.0);
        assert_eq!(z.zoom, 2.0);
        // точка доски под якорем: до — (300, 150), после — те же координаты
        assert_eq!(z.pan.x + 200.0 / 2.0, 300.0);
        assert_eq!(z.pan.y + 100.0 / 2.0, 150.0);
        assert_eq!(zoom_around(v, 100.0, Point::default(), 1.0).zoom, ZOOM_MAX);
        assert_eq!(zoom_around(v, 0.0001, Point::default(), 1.0).zoom, ZOOM_MIN);
        let top = View { pan: Point::new(5.0, 5.0), zoom: ZOOM_MAX };
        assert_eq!(zoom_around(top, 2.0, Point::default(), 1.0), top);
        assert_eq!(zoom_around(v, 2.0, Point::default(), 0.0), v);
        assert_eq!(zoom_around(v, 2.0, Point::default(), f64::NAN), v);
    }

    #[test]
    fn view_box_shrinks_with_zoom() {
        assert_eq!(view_box(View::HOME, 880.0, 440.0), "0 0 880 440");
        assert_eq!(view_box(View { pan: Point::new(-10.0, 20.0), zoom: 2.0 }, 880.0, 440.0), "-10 20 440 220");
        assert_eq!(view_box(View { pan: Point::new(0.0, 0.0), zoom: 3.0 }, 880.0, 440.0), "0 0 293.33 146.67");
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
        assert_eq!(drag_pan(d, Point::new(140.0, 100.0)), Point::new(-10.0, 10.0));
        assert_eq!(drag_pan(d, Point::new(100.0, 80.0)), Point::new(10.0, 20.0));
    }

    #[test]
    fn click_is_a_small_move() {
        assert!(is_click(Point::new(10.0, 10.0), Point::new(12.0, 13.0)));
        assert!(!is_click(Point::new(10.0, 10.0), Point::new(10.0, 16.0)));
    }

    #[test]
    fn metrics_fit_the_board_into_the_svg_and_map_points_back() {
        // доска 880×440 в svg 1760×880: масштаб 2, полей нет
        let m = metrics(100.0, 50.0, 1760.0, 880.0, 880.0, 440.0);
        assert_eq!((m.base, m.off_x, m.off_y), (2.0, 0.0, 0.0));
        assert_eq!(m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), View::HOME), Point::new(200.0, 100.0));
        // при масштабе 2 и сдвиге (10, 20) тот же пиксель — другая точка доски
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), View { pan: Point::new(10.0, 20.0), zoom: 2.0 });
        assert_eq!(p, Point::new(110.0, 70.0));
        // svg шире доски: слева и справа поля, точка отсчитывается от вписанной доски
        let wide = metrics(0.0, 0.0, 1100.0, 440.0, 880.0, 440.0);
        assert_eq!((wide.base, wide.off_x, wide.off_y), (1.0, 110.0, 0.0));
        assert_eq!(wide.to_board(Point::new(110.0, 0.0), View::HOME), Point::new(0.0, 0.0));
        assert_eq!(wide.center(), Point::new(440.0, 220.0));
        // нулевой размер не даёт бесконечностей
        let none = metrics(0.0, 0.0, 0.0, 0.0, 880.0, 440.0);
        assert_eq!(none.to_board(Point::new(5.0, 5.0), View::HOME), Point::new(0.0, 0.0));
    }

    #[test]
    fn js_round_rounds_halves_up() {
        assert_eq!(js_round(2.5), 3.0);
        assert_eq!(js_round(-2.5), -2.0);
        assert_eq!(js_round(-2.6), -3.0);
    }

    #[test]
    fn elements_cannot_leave_the_world() {
        assert_eq!(clamp_world(Point::new(9000.0, 5000.0), 64.0, 48.0), Point::new(3936.0, 2952.0));
        assert_eq!(clamp_world(Point::new(-9000.0, -5000.0), 64.0, 48.0), Point::new(-4000.0, -3000.0));
        assert_eq!(clamp_world(Point::new(10.0, 20.0), 64.0, 48.0), Point::new(10.0, 20.0));
    }

    #[test]
    fn manual_height_keeps_the_aspect_of_the_window() {
        // svg 880×330 px: окно на доску 880×330 единиц
        assert_eq!(world_height_for(330.0, 880.0, 880.0), Some(330.0));
        assert_eq!(world_height_for(660.0, 440.0, 880.0), Some(1320.0));
        assert_eq!(world_height_for(300.0, 0.0, 880.0), None);
    }
}
