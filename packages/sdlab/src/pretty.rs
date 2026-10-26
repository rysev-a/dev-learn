//! Запись JSON для файлов данных: верхние уровни — по строке на поле, «листья» (узлы, цели, связи, нагрузка) — одной
//! строкой, целые числа без `.0`. Читаемо в диффах и компактно.

use std::io;

use serde::Serialize;
use serde_json::ser::{CompactFormatter, Formatter};

/// Форматировщик: развёрнуты контейнеры до глубины 4 и контейнеры с ключами `start`, `solution`, `nodes`, `goals`.
struct Layout {
    depth: usize,
    /// глубина контейнера, с которого всё пишется в одну строку
    compact_from: Option<usize>,
    frames: Vec<Frame>,
    in_key: bool,
    key: String,
}

struct Frame {
    expanded: bool,
    items: bool,
}

const EXPAND_KEYS: [&str; 4] = ["start", "solution", "nodes", "goals"];
const EXPAND_DEPTH: usize = 4;

impl Layout {
    fn new() -> Layout {
        Layout { depth: 0, compact_from: None, frames: Vec::new(), in_key: false, key: String::new() }
    }

    fn enter<W: ?Sized + io::Write>(&mut self, w: &mut W, open: &[u8]) -> io::Result<()> {
        self.depth += 1;
        let expanded = self.compact_from.is_none() && (self.depth <= EXPAND_DEPTH || EXPAND_KEYS.contains(&self.key.as_str()));
        if !expanded && self.compact_from.is_none() {
            self.compact_from = Some(self.depth);
        }
        self.frames.push(Frame { expanded, items: false });
        w.write_all(open)
    }

    fn leave<W: ?Sized + io::Write>(&mut self, w: &mut W, close: &[u8]) -> io::Result<()> {
        let f = self.frames.pop().unwrap_or(Frame { expanded: false, items: false });
        if f.expanded && f.items {
            self.newline(w, self.depth - 1)?;
        }
        if self.compact_from == Some(self.depth) {
            self.compact_from = None;
        }
        self.depth -= 1;
        w.write_all(close)
    }

    fn newline<W: ?Sized + io::Write>(&self, w: &mut W, depth: usize) -> io::Result<()> {
        w.write_all(b"\n")?;
        for _ in 0..depth {
            w.write_all(b"  ")?;
        }
        Ok(())
    }

    fn item<W: ?Sized + io::Write>(&mut self, w: &mut W, first: bool) -> io::Result<()> {
        if !first {
            w.write_all(b",")?;
        }
        let depth = self.depth;
        if let Some(f) = self.frames.last_mut() {
            f.items = true;
            if f.expanded {
                return self.newline(w, depth);
            }
            if !first {
                w.write_all(b" ")?;
            }
        }
        Ok(())
    }
}

impl Formatter for Layout {
    fn begin_array<W: ?Sized + io::Write>(&mut self, w: &mut W) -> io::Result<()> {
        self.enter(w, b"[")
    }
    fn end_array<W: ?Sized + io::Write>(&mut self, w: &mut W) -> io::Result<()> {
        self.leave(w, b"]")
    }
    fn begin_array_value<W: ?Sized + io::Write>(&mut self, w: &mut W, first: bool) -> io::Result<()> {
        self.key.clear();
        self.item(w, first)
    }
    fn begin_object<W: ?Sized + io::Write>(&mut self, w: &mut W) -> io::Result<()> {
        self.enter(w, b"{")
    }
    fn end_object<W: ?Sized + io::Write>(&mut self, w: &mut W) -> io::Result<()> {
        self.leave(w, b"}")
    }
    fn begin_object_key<W: ?Sized + io::Write>(&mut self, w: &mut W, first: bool) -> io::Result<()> {
        self.in_key = true;
        self.key.clear();
        self.item(w, first)
    }
    fn end_object_key<W: ?Sized + io::Write>(&mut self, _w: &mut W) -> io::Result<()> {
        self.in_key = false;
        Ok(())
    }
    fn begin_object_value<W: ?Sized + io::Write>(&mut self, w: &mut W) -> io::Result<()> {
        w.write_all(b": ")
    }
    fn write_string_fragment<W: ?Sized + io::Write>(&mut self, w: &mut W, fragment: &str) -> io::Result<()> {
        if self.in_key {
            self.key.push_str(fragment);
        }
        w.write_all(fragment.as_bytes())
    }
    fn write_f64<W: ?Sized + io::Write>(&mut self, w: &mut W, value: f64) -> io::Result<()> {
        if value.fract() == 0.0 && value.abs() < 1e15 {
            w.write_all(format!("{}", value as i64).as_bytes())
        } else {
            CompactFormatter.write_f64(w, value)
        }
    }
}

/// Значение в виде текста файла данных (с переводом строки в конце).
pub fn to_string<T: Serialize>(value: &T) -> Result<String, serde_json::Error> {
    let mut buf = Vec::new();
    let mut ser = serde_json::Serializer::with_formatter(&mut buf, Layout::new());
    value.serialize(&mut ser)?;
    let mut s = String::from_utf8(buf).map_err(serde::ser::Error::custom)?;
    s.push('\n');
    Ok(s)
}
