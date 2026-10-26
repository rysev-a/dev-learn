//! Геометрия поля сети: размеры карточки устройства, настройки окна на поле, положение подписей кабелей и поиск
//! устройства под курсором. Чистая арифметика с тестами; сдвиг и масштаб — общий `board_view.rs`, DOM — в `board.rs`.
//!
//! Поле — плоскость, на которой устройства стоят в координатах упражнения (обычно 0…640 × 0…360). `<svg>` показывает
//! окно на эту плоскость (`viewBox`): чем крупнее масштаб, тем меньше окно.

use crate::components::labs::board_view::{BoardConfig, Bounds, Point};

/// Размеры карточки устройства на поле.
pub const DEV_W: f64 = 104.0;
pub const DEV_H: f64 = 58.0;

/// Окно на поле при масштабе 100 %: поле 640×360 с запасом слева, чтобы влезали подписи.
pub const WORLD: (f64, f64) = (704.0, 360.0);

/// Сдвиг и масштаб поля: 40–400 %, сдвиг не округляется, левый верхний угол окна в исходном виде — (−24, 0); центр окна
/// нельзя унести дальше пределов (поле не теряется совсем), а устройство — за пределы поля. Порог щелчка — 4 px.
pub const BOARD: BoardConfig = BoardConfig {
    zoom_min: 0.4,
    zoom_max: 4.0,
    home: Point::new(-24.0, 0.0),
    round_pan: false,
    window_limit: Some(Bounds::new((-324.0, 980.0), (-300.0, 660.0))),
    items: Bounds::new((-200.0, 840.0), (-100.0, 460.0)),
    click_slop: 4.0,
};

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

    #[test]
    fn the_home_window_shows_the_whole_field_with_room_for_labels() {
        use crate::components::labs::board_view::view_box;
        assert_eq!(view_box(BOARD.home_view(), WORLD.0, WORLD.1), "-24 0 704 360");
    }
}
