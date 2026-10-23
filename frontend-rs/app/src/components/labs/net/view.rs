//! Геометрия поля сети: окно на поле (сдвиг и масштаб), перевод координат мыши в координаты схемы, положение подписей
//! кабелей и поиск устройства под курсором. Чистая арифметика с тестами; DOM и сигналы — в `board.rs`.
//!
//! Поле — плоскость, на которой устройства стоят в координатах упражнения (обычно 0…640 × 0…360). `<svg>` показывает
//! окно `Rect` на эту плоскость (`viewBox`): чем крупнее масштаб, тем меньше окно.

/// Размеры карточки устройства на поле.
pub const DEV_W: f64 = 104.0;
pub const DEV_H: f64 = 58.0;

/// Границы и шаг масштаба.
pub const ZOOM_MIN: f64 = 0.4;
pub const ZOOM_MAX: f64 = 4.0;
pub const ZOOM_STEP: f64 = 1.25;

/// Сдвиг указателя (px экрана), меньше которого нажатие считается щелчком, а не перетаскиванием.
pub const CLICK_SLOP: f64 = 4.0;

/// Точка на экране или на поле.
#[derive(Clone, Copy, Debug, PartialEq, Default)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

impl Point {
    pub const fn new(x: f64, y: f64) -> Point {
        Point { x, y }
    }
}

/// Прямоугольник на поле (окно просмотра).
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Rect {
    pub x: f64,
    pub y: f64,
    pub w: f64,
    pub h: f64,
}

/// Исходное окно: поле 640×360 с запасом слева, чтобы влезали подписи.
pub const HOME: Rect = Rect { x: -24.0, y: 0.0, w: 704.0, h: 360.0 };

/// В пределах каких координат может лежать центр окна: поле нельзя «унести» совсем.
const CENTER_X: (f64, f64) = (-324.0, 980.0);
const CENTER_Y: (f64, f64) = (-300.0, 660.0);

/// Предел координат устройства при перетаскивании.
const DEVICE_X: (f64, f64) = (-200.0, 840.0);
const DEVICE_Y: (f64, f64) = (-100.0, 460.0);

/// `Math.round` в JavaScript: половина округляется к +∞.
pub fn js_round(x: f64) -> f64 {
    (x + 0.5).floor()
}

impl Rect {
    /// Масштаб окна: 1 — исходное, 2 — вдвое крупнее.
    pub fn zoom(&self) -> f64 {
        HOME.w / self.w
    }

    /// Значение атрибута `viewBox`.
    pub fn attr(&self) -> String {
        let r = |n: f64| js_round(n * 100.0) / 100.0;
        format!("{} {} {} {}", r(self.x), r(self.y), r(self.w), r(self.h))
    }

    fn clamped(mut self) -> Rect {
        let cx = (self.x + self.w / 2.0).clamp(CENTER_X.0, CENTER_X.1);
        let cy = (self.y + self.h / 2.0).clamp(CENTER_Y.0, CENTER_Y.1);
        self.x = cx - self.w / 2.0;
        self.y = cy - self.h / 2.0;
        self
    }

    /// Окно нужного масштаба с той же серединой.
    pub fn with_zoom(self, zoom: f64) -> Rect {
        let anchor = Point::new(self.x + self.w / 2.0, self.y + self.h / 2.0);
        let z = zoom.clamp(ZOOM_MIN, ZOOM_MAX);
        self.zoomed(z / self.zoom(), anchor)
    }

    /// Меняет масштаб в `factor` раз (больше 1 — приближает), не сдвигая точку поля под `anchor`.
    pub fn zoomed(self, factor: f64, anchor: Point) -> Rect {
        let zoom = (self.zoom() * factor).clamp(ZOOM_MIN, ZOOM_MAX);
        if (zoom - self.zoom()).abs() < 1e-9 || !zoom.is_finite() {
            return self;
        }
        let w = HOME.w / zoom;
        let h = HOME.h / zoom;
        let r = w / self.w;
        Rect { x: anchor.x - (anchor.x - self.x) * r, y: anchor.y - (anchor.y - self.y) * r, w, h }.clamped()
    }

    /// Сдвигает окно на `dx`, `dy` единиц поля.
    pub fn panned(self, dx: f64, dy: f64) -> Rect {
        Rect { x: self.x + dx, y: self.y + dy, ..self }.clamped()
    }
}

/// Где `<svg>` на экране.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Screen {
    pub left: f64,
    pub top: f64,
    pub width: f64,
    pub height: f64,
}

impl Screen {
    /// Пикселей экрана на единицу поля: окно вписано в `<svg>` с сохранением пропорций (`xMidYMid meet`).
    pub fn scale(&self, vb: &Rect) -> f64 {
        (self.width / vb.w).min(self.height / vb.h)
    }

    /// Экранная точка (`clientX`, `clientY`) в координатах поля.
    pub fn to_board(self, vb: &Rect, client: Point) -> Point {
        let s = self.scale(vb);
        if !(s.is_finite() && s > 0.0) {
            return Point::new(vb.x, vb.y);
        }
        let ox = (self.width - vb.w * s) / 2.0;
        let oy = (self.height - vb.h * s) / 2.0;
        Point::new(vb.x + (client.x - self.left - ox) / s, vb.y + (client.y - self.top - oy) / s)
    }

    /// Сдвиг в единицах поля, соответствующий сдвигу указателя на `dx`, `dy` пикселей (доска «едет» за рукой).
    pub fn pan_delta(&self, vb: &Rect, dx: f64, dy: f64) -> (f64, f64) {
        let s = self.scale(vb);
        if !(s.is_finite() && s > 0.0) {
            return (0.0, 0.0);
        }
        (-dx / s, -dy / s)
    }
}

/// Нажатие и отпускание почти в одной точке — это щелчок.
pub fn is_click(down: Point, up: Point) -> bool {
    (up.x - down.x).hypot(up.y - down.y) < CLICK_SLOP
}

/// Координаты устройства после перетаскивания: целые, в пределах поля.
pub fn clamp_device(p: Point) -> Point {
    Point::new(js_round(p.x.clamp(DEVICE_X.0, DEVICE_X.1)), js_round(p.y.clamp(DEVICE_Y.0, DEVICE_Y.1)))
}

/// Кабель на поле: концы у центров устройств, подписи портов вблизи концов.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct LinkGeom {
    pub a: Point,
    pub b: Point,
    pub label_a: Point,
    pub label_b: Point,
    pub mid: Point,
}

/// Положение кабеля между центрами устройств `a` и `b`: подписи портов отступают от центра на 74 единицы
/// (не дальше 0,42 длины).
pub fn link_geom(a: Point, b: Point) -> LinkGeom {
    let len = (b.x - a.x).hypot(b.y - a.y);
    let len = if len == 0.0 { 1.0 } else { len };
    let t = (74.0 / len).min(0.42);
    LinkGeom {
        a,
        b,
        label_a: Point::new(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t),
        label_b: Point::new(b.x + (a.x - b.x) * t, b.y + (a.y - b.y) * t),
        mid: Point::new((a.x + b.x) / 2.0, (a.y + b.y) / 2.0),
    }
}

/// Точка на отрезке `a`–`b` на доле пути `p`.
pub fn lerp(a: Point, b: Point, p: f64) -> Point {
    Point::new(a.x + (b.x - a.x) * p, a.y + (b.y - a.y) * p)
}

/// Устройство под точкой поля: карточка `DEV_W × DEV_H` вокруг центра; при наложении — верхнее (нарисованное позже).
pub fn device_at<'a>(devices: impl DoubleEndedIterator<Item = (&'a str, Point)>, p: Point) -> Option<&'a str> {
    devices.rev().find(|(_, c)| (p.x - c.x).abs() <= DEV_W / 2.0 && (p.y - c.y).abs() <= DEV_H / 2.0).map(|(id, _)| id)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn home_is_zoom_one() {
        assert_eq!(HOME.zoom(), 1.0);
        assert_eq!(HOME.attr(), "-24 0 704 360");
    }

    #[test]
    fn zoom_keeps_the_anchor_point_still_and_stays_in_bounds() {
        let anchor = Point::new(300.0, 100.0);
        let z = HOME.zoomed(2.0, anchor);
        assert_eq!(z.zoom(), 2.0);
        // доля положения якоря в окне не изменилась
        let before = ((anchor.x - HOME.x) / HOME.w, (anchor.y - HOME.y) / HOME.h);
        let after = ((anchor.x - z.x) / z.w, (anchor.y - z.y) / z.h);
        assert!((before.0 - after.0).abs() < 1e-9 && (before.1 - after.1).abs() < 1e-9);
        assert_eq!(HOME.zoomed(100.0, anchor).zoom(), ZOOM_MAX);
        assert!((HOME.zoomed(0.0001, anchor).zoom() - ZOOM_MIN).abs() < 1e-9);
        // у предела ничего не меняется
        let top = HOME.zoomed(100.0, anchor);
        assert_eq!(top.zoomed(2.0, anchor), top);
        // не число — не масштаб
        assert_eq!(HOME.zoomed(f64::NAN, anchor), HOME);
    }

    #[test]
    fn with_zoom_keeps_the_center() {
        let z = HOME.with_zoom(2.0);
        assert_eq!(z.zoom(), 2.0);
        assert!((z.x + z.w / 2.0 - (HOME.x + HOME.w / 2.0)).abs() < 1e-9);
        assert!((z.y + z.h / 2.0 - (HOME.y + HOME.h / 2.0)).abs() < 1e-9);
        assert_eq!(z.with_zoom(1.0), HOME);
    }

    #[test]
    fn panning_cannot_carry_the_board_away() {
        let far = HOME.panned(100_000.0, -100_000.0);
        assert!(far.x + far.w / 2.0 <= CENTER_X.1 + 1e-9);
        assert!(far.y + far.h / 2.0 >= CENTER_Y.0 - 1e-9);
        assert_eq!(HOME.panned(10.0, 5.0), Rect { x: -14.0, y: 5.0, ..HOME });
    }

    #[test]
    fn mouse_maps_into_the_board_with_letterboxing() {
        // svg вдвое крупнее окна: масштаб 2, полей нет
        let s = Screen { left: 100.0, top: 50.0, width: 1408.0, height: 720.0 };
        assert_eq!(s.scale(&HOME), 2.0);
        assert_eq!(s.to_board(&HOME, Point::new(100.0, 50.0)), Point::new(-24.0, 0.0));
        assert_eq!(s.to_board(&HOME, Point::new(100.0 + 2.0 * 124.0, 50.0 + 2.0 * 10.0)), Point::new(100.0, 10.0));
        // svg шире окна: слева и справа поля
        let wide = Screen { left: 0.0, top: 0.0, width: 904.0, height: 360.0 };
        assert_eq!(wide.scale(&HOME), 1.0);
        assert_eq!(wide.to_board(&HOME, Point::new(100.0, 0.0)), Point::new(-24.0, 0.0));
        // нет размера — нет бесконечностей
        let none = Screen { left: 0.0, top: 0.0, width: 0.0, height: 0.0 };
        assert_eq!(none.to_board(&HOME, Point::new(5.0, 5.0)), Point::new(-24.0, 0.0));
        assert_eq!(none.pan_delta(&HOME, 5.0, 5.0), (0.0, 0.0));
    }

    #[test]
    fn panning_follows_the_hand() {
        let s = Screen { left: 0.0, top: 0.0, width: 1408.0, height: 720.0 };
        // потянули вправо на 40 px: содержимое уехало вправо, окно сдвинулось влево на 20 единиц
        assert_eq!(s.pan_delta(&HOME, 40.0, -10.0), (-20.0, 5.0));
    }

    #[test]
    fn click_is_a_small_move() {
        assert!(is_click(Point::new(10.0, 10.0), Point::new(12.0, 11.0)));
        assert!(!is_click(Point::new(10.0, 10.0), Point::new(10.0, 16.0)));
    }

    #[test]
    fn device_position_is_rounded_and_limited() {
        assert_eq!(clamp_device(Point::new(90.4, 270.6)), Point::new(90.0, 271.0));
        assert_eq!(clamp_device(Point::new(5000.0, -5000.0)), Point::new(840.0, -100.0));
    }

    #[test]
    fn port_labels_sit_near_the_ends() {
        let g = link_geom(Point::new(0.0, 0.0), Point::new(200.0, 0.0));
        assert_eq!(g.label_a, Point::new(74.0, 0.0));
        assert_eq!(g.label_b, Point::new(126.0, 0.0));
        assert_eq!(g.mid, Point::new(100.0, 0.0));
        // у короткого кабеля подписи не заходят дальше 0,42 длины
        let short = link_geom(Point::new(0.0, 0.0), Point::new(100.0, 0.0));
        assert!((short.label_a.x - 42.0).abs() < 1e-9);
        // кабель нулевой длины не даёт NaN
        let zero = link_geom(Point::new(5.0, 5.0), Point::new(5.0, 5.0));
        assert!(zero.label_a.x.is_finite());
        assert_eq!(lerp(Point::new(0.0, 0.0), Point::new(10.0, 20.0), 0.5), Point::new(5.0, 10.0));
    }

    #[test]
    fn topmost_device_wins_under_the_cursor() {
        let devs = [("a", Point::new(100.0, 100.0)), ("b", Point::new(130.0, 110.0)), ("c", Point::new(400.0, 100.0))];
        assert_eq!(device_at(devs.iter().copied(), Point::new(120.0, 105.0)), Some("b"));
        assert_eq!(device_at(devs.iter().copied(), Point::new(60.0, 100.0)), Some("a"));
        assert_eq!(device_at(devs.iter().copied(), Point::new(250.0, 100.0)), None);
        assert_eq!(device_at(devs.iter().copied(), Point::new(400.0 + DEV_W / 2.0, 100.0 + DEV_H / 2.0)), Some("c"));
    }
}
