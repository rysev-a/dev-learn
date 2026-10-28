//! Network board geometry: device card sizes, window settings on the board, cable label positions and finding the
//! device under the cursor. Pure arithmetic with tests; pan and zoom are the shared `board_view.rs`, the DOM is in `board.rs`.
//!
//! The board is a plane on which devices stand at exercise coordinates (usually 0…640 × 0…360). `<svg>` shows
//! a window onto this plane (`viewBox`): the larger the zoom, the smaller the window.

use crate::components::labs::board_view::{BoardConfig, Bounds, Point};

/// Device card size on the board.
pub const DEV_W: f64 = 104.0;
pub const DEV_H: f64 = 58.0;

/// Window onto the board at 100 % zoom: a 640×360 board with spare room on the left so labels fit.
pub const WORLD: (f64, f64) = (704.0, 360.0);

/// Board pan and zoom: 40–400 %, pan is not rounded, the window's top-left corner in the initial view is (−24, 0); the window center
/// cannot be carried past the limits (the board is never lost entirely), nor a device out of the board. Click threshold is 4 px.
pub const BOARD: BoardConfig = BoardConfig {
    zoom_min: 0.4,
    zoom_max: 4.0,
    home: Point::new(-24.0, 0.0),
    round_pan: false,
    window_limit: Some(Bounds::new((-324.0, 980.0), (-300.0, 660.0))),
    items: Bounds::new((-200.0, 840.0), (-100.0, 460.0)),
    click_slop: 4.0,
};

/// A cable on the board: ends at device centers, port labels near the ends.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct LinkGeom {
    pub a: Point,
    pub b: Point,
    pub label_a: Point,
    pub label_b: Point,
    pub mid: Point,
}

/// Position of a cable between device centers `a` and `b`: port labels step back from the center by 74 units
/// (no further than 0.42 of the length).
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

/// A point on segment `a`–`b` at path fraction `p`.
pub fn lerp(a: Point, b: Point, p: f64) -> Point {
    Point::new(a.x + (b.x - a.x) * p, a.y + (b.y - a.y) * p)
}

/// Device under a board point: a `DEV_W × DEV_H` card around the center; when overlapping, the top one (drawn later).
pub fn device_at<'a>(devices: impl DoubleEndedIterator<Item = (&'a str, Point)>, p: Point) -> Option<&'a str> {
    devices.rev().find(|(_, c)| (p.x - c.x).abs() <= DEV_W / 2.0 && (p.y - c.y).abs() <= DEV_H / 2.0).map(|(id, _)| id)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn port_labels_sit_near_the_ends() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let g = link_geom(Point::new(0.0, 0.0), Point::new(200.0, 0.0));
        assert_eq!(g.label_a, Point::new(74.0, 0.0));
        assert_eq!(g.label_b, Point::new(126.0, 0.0));
        assert_eq!(g.mid, Point::new(100.0, 0.0));
        // on a short cable labels do not go past 0.42 of the length
        let short = link_geom(Point::new(0.0, 0.0), Point::new(100.0, 0.0));
        assert!((short.label_a.x - 42.0).abs() < 1e-9);
        // a zero-length cable gives no NaN
        let zero = link_geom(Point::new(5.0, 5.0), Point::new(5.0, 5.0));
        assert!(zero.label_a.x.is_finite());
        assert_eq!(lerp(Point::new(0.0, 0.0), Point::new(10.0, 20.0), 0.5), Point::new(5.0, 10.0));
    }

    #[test]
    fn topmost_device_wins_under_the_cursor() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let devs = [("a", Point::new(100.0, 100.0)), ("b", Point::new(130.0, 110.0)), ("c", Point::new(400.0, 100.0))];
        assert_eq!(device_at(devs.iter().copied(), Point::new(120.0, 105.0)), Some("b"));
        assert_eq!(device_at(devs.iter().copied(), Point::new(60.0, 100.0)), Some("a"));
        assert_eq!(device_at(devs.iter().copied(), Point::new(250.0, 100.0)), None);
        assert_eq!(device_at(devs.iter().copied(), Point::new(400.0 + DEV_W / 2.0, 100.0 + DEV_H / 2.0)), Some("c"));
    }

    #[test]
    fn the_home_window_shows_the_whole_field_with_room_for_labels() {
        let _ru = locales::guard(i18n::Locale::Ru);
        use crate::components::labs::board_view::view_box;
        assert_eq!(view_box(BOARD.home_view(), WORLD.0, WORLD.1), "-24 0 704 360");
    }
}
