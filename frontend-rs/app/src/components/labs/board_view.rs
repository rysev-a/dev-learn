//! Окно на «бесконечную» доску, общее для досок лабораторий (системный дизайн, архитектура, сети): сдвиг (пустое место,
//! средняя кнопка мыши), масштаб (Ctrl/⌘ + колесо, кнопки), перевод экранных координат в координаты доски и наблюдатель
//! за размером элемента. В React это `useBoardView.tsx` и `board-pan.ts`.
//!
//! Арифметика — чистые функции вверху файла (с тестами); [`BoardView`] только связывает их с сигналами и размерами `<svg>`.
//! Доска — окно (`viewBox`) на плоскость: при масштабе `z` видно кусок размером `ширина/z × высота/z`, начиная с точки
//! `pan`; `<svg>` вписывает окно в свои размеры с сохранением пропорций (`preserveAspectRatio = xMidYMid meet`).

use leptos::{
    html::ElementType,
    prelude::*,
    svg,
};
use wasm_bindgen::JsCast;

use crate::dom;

/// Границы и шаг масштаба.
pub const ZOOM_MIN: f64 = 0.3;
pub const ZOOM_MAX: f64 = 3.0;
pub const ZOOM_STEP: f64 = 1.25;
/// Сдвиг указателя (px экрана), меньше которого нажатие на порт считается щелчком, а не перетаскиванием.
pub const CLICK_SLOP: f64 = 6.0;

// --- чистая арифметика --------------------------------------------------------------------------

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
}

/// `Math.round` в JavaScript: половина округляется к +∞.
pub fn js_round(x: f64) -> f64 {
    (x + 0.5).floor()
}

pub fn clamp_zoom(z: f64) -> f64 {
    z.clamp(ZOOM_MIN, ZOOM_MAX)
}

/// Ограничивает координату пределами «мира» (элементы нельзя унести дальше).
pub fn clamp_world(v: f64, limit: f64) -> f64 {
    v.clamp(-limit, limit)
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

/// Перетаскивание элемента доски: где элемент стоял и на сколько указатель был смещён от его центра в момент нажатия.
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

    /// Новое место элемента для указателя `pointer`: целые координаты не дальше `limit` от начала координат.
    pub fn to(&self, pointer: Point, limit: f64) -> Point {
        Point::new(js_round(clamp_world(pointer.x + self.grip.x, limit)), js_round(clamp_world(pointer.y + self.grip.y, limit)))
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

/// Метрики для доски `view_w × view_h`, вписанной в прямоугольник `<svg>`. Рамка (1 px) в размерах не учитывается.
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

    /// Центр видимой доски в пикселях от её угла: вокруг него работают кнопки масштаба.
    pub fn center(&self) -> Point {
        Point::new((self.width - 2.0 * self.off_x) / 2.0, (self.height - 2.0 * self.off_y) / 2.0)
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
    /// размеры окна на доску при масштабе 1 (ширина постоянна, высота зависит от пропорций поля)
    width: f64,
    height: Signal<f64>,
    drag: StoredValue<Option<PanDrag>>,
}

impl BoardView {
    pub fn new(svg: NodeRef<svg::Svg>, width: f64, height: Signal<f64>) -> Self {
        Self { svg, pan: RwSignal::new(Point::default()), zoom: RwSignal::new(1.0), panning: RwSignal::new(false), width, height, drag: StoredValue::new(None) }
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

    /// Значение `viewBox` (в реактивном контексте — подписка на сдвиг, масштаб и высоту окна).
    pub fn view_box(&self) -> String {
        view_box(self.view(), self.width, self.height.get())
    }

    /// Где доска на экране сейчас; `None`, пока `<svg>` не появился или у него нет размера.
    pub fn metrics(&self) -> Option<Metrics> {
        let rect = self.svg.get_untracked()?.get_bounding_client_rect();
        let m = metrics(rect.left(), rect.top(), rect.width(), rect.height(), self.width, self.height.get_untracked());
        (m.base > 0.0 && m.base.is_finite()).then_some(m)
    }

    /// Экранная точка в координатах доски (без подписки на сигналы: вызывается в обработчиках событий).
    pub fn to_board(&self, client_x: f64, client_y: f64) -> Point {
        match self.metrics() {
            Some(m) => m.to_board(Point::new(client_x, client_y), self.view_untracked()),
            None => Point::default(),
        }
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

    /// Колесо над доской: с Ctrl/⌘ — масштаб вокруг курсора (страница при этом не прокручивается).
    pub fn on_wheel(&self, ev: &web_sys::WheelEvent) {
        if !(ev.ctrl_key() || ev.meta_key()) {
            return;
        }
        ev.prevent_default();
        let Some(m) = self.metrics() else { return };
        let anchor = Point::new(f64::from(ev.client_x()) - m.left - m.off_x, f64::from(ev.client_y()) - m.top - m.off_y);
        self.set_view(zoom_around(self.view_untracked(), wheel_factor(ev.delta_y()), anchor, m.base));
    }

    /// Нажатие на пустом месте доски или средней кнопкой: начало сдвига. `true` — нажатие обработано.
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
#[component]
pub fn ZoomControls(
    #[prop(into)] zoom: Signal<f64>,
    /// доска сдвинута или масштаб не исходный (показать кнопку «вернуть»)
    #[prop(into)]
    changed: Signal<bool>,
    on_zoom_by: Callback<f64>,
    on_actual: Callback<()>,
    on_reset: Callback<()>,
) -> impl IntoView {
    view! {
        <div class="lab-zoom" role="group" aria-label="Масштаб доски">
            <button type="button" title="Уменьшить (Ctrl + колесо)" on:click=move |_| on_zoom_by.run(1.0 / ZOOM_STEP)>"−"</button>
            <button type="button" class="pct" title="Масштаб 100 %" on:click=move |_| on_actual.run(())>{move || format!("{}%", js_round(zoom.get() * 100.0))}</button>
            <button type="button" title="Увеличить (Ctrl + колесо)" on:click=move |_| on_zoom_by.run(ZOOM_STEP)>"+"</button>
            {move || changed.get().then(|| view! { <button type="button" title="Вернуть доску на место и масштаб 100 %" on:click=move |_| on_reset.run(())>"⌖"</button> })}
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
        // у предела ничего не меняется
        let top = View { pan: Point::new(5.0, 5.0), zoom: ZOOM_MAX };
        assert_eq!(zoom_around(top, 2.0, Point::default(), 1.0), top);
        // нет размера — нет масштаба
        assert_eq!(zoom_around(v, 2.0, Point::default(), 0.0), v);
        assert_eq!(zoom_around(v, 2.0, Point::default(), f64::NAN), v);
    }

    #[test]
    fn view_box_shrinks_with_zoom() {
        assert_eq!(view_box(View::HOME, 780.0, 560.0), "0 0 780 560");
        assert_eq!(view_box(View { pan: Point::new(-10.0, 20.0), zoom: 2.0 }, 780.0, 560.0), "-10 20 390 280");
        assert_eq!(view_box(View { pan: Point::new(0.0, 0.0), zoom: 3.0 }, 780.0, 560.0), "0 0 260 186.67");
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
        assert_eq!(drag_pan(d, Point::new(140.0, 100.0)), Point::new(-10.0, 10.0));
        assert_eq!(drag_pan(d, Point::new(100.0, 80.0)), Point::new(10.0, 20.0));
    }

    #[test]
    fn dragged_item_keeps_its_grip_and_stays_in_the_world() {
        let d = ItemDrag::start(Point::new(105.0, 52.0), Point::new(100.0, 50.0));
        // указатель сместился на (20, 10) — элемент на столько же
        let to = d.to(Point::new(125.0, 62.0), 2600.0);
        assert_eq!(to, Point::new(120.0, 60.0));
        assert!(d.moved_far(to, 6.0));
        assert!(!d.moved_far(Point::new(103.0, 52.0), 6.0));
        assert_eq!(d.to(Point::new(9000.0, -9000.0), 2600.0), Point::new(2600.0, -2600.0));
        // координаты округляются, как в JavaScript
        assert_eq!(d.to(Point::new(105.4, 52.6), 2600.0), Point::new(100.0, 51.0));
    }

    #[test]
    fn click_is_a_small_move() {
        assert!(is_click(Point::new(10.0, 10.0), Point::new(12.0, 13.0)));
        assert!(!is_click(Point::new(10.0, 10.0), Point::new(10.0, 16.0)));
    }

    #[test]
    fn metrics_fit_the_board_into_the_svg_and_map_points_back() {
        // доска 780×560 в svg 1560×1120: масштаб 2, полей нет
        let m = metrics(100.0, 50.0, 1560.0, 1120.0, 780.0, 560.0);
        assert_eq!((m.base, m.off_x, m.off_y), (2.0, 0.0, 0.0));
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), View::HOME);
        assert_eq!(p, Point::new(200.0, 100.0));
        // при масштабе 2 и сдвиге (10, 20) тот же пиксель — другая точка доски
        let p = m.to_board(Point::new(100.0 + 400.0, 50.0 + 200.0), View { pan: Point::new(10.0, 20.0), zoom: 2.0 });
        assert_eq!(p, Point::new(110.0, 70.0));
        // svg шире доски: слева и справа поля, точка отсчитывается от вписанной доски
        let wide = metrics(0.0, 0.0, 1000.0, 560.0, 780.0, 560.0);
        assert_eq!((wide.base, wide.off_x, wide.off_y), (1.0, 110.0, 0.0));
        assert_eq!(wide.to_board(Point::new(110.0, 0.0), View::HOME), Point::new(0.0, 0.0));
        assert_eq!(wide.center(), Point::new(390.0, 280.0));
        // нулевой размер не даёт бесконечностей
        let none = metrics(0.0, 0.0, 0.0, 0.0, 780.0, 560.0);
        assert_eq!(none.to_board(Point::new(5.0, 5.0), View::HOME), Point::new(0.0, 0.0));
    }

    #[test]
    fn js_round_rounds_halves_up() {
        assert_eq!(js_round(2.5), 3.0);
        assert_eq!(js_round(-2.5), -2.0);
        assert_eq!(js_round(-2.6), -3.0);
    }

    #[test]
    fn world_is_clamped_symmetrically() {
        assert_eq!(clamp_world(5000.0, 2600.0), 2600.0);
        assert_eq!(clamp_world(-5000.0, 2600.0), -2600.0);
        assert_eq!(clamp_world(10.0, 2600.0), 10.0);
    }

    #[test]
    fn size_change_below_half_a_pixel_is_ignored() {
        assert!(!size_differs((100.0, 50.0), (100.3, 50.0)));
        assert!(size_differs((100.0, 50.0), (101.0, 50.0)));
    }
}
