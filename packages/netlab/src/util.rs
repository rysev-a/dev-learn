//! Small helpers reproducing JavaScript behaviour where the student can see it:
//! rounding, `toFixed`, `Number(...)`, string length in UTF-16 and an insertion-ordered map.

use serde::de::{MapAccess, Visitor};
use serde::ser::SerializeMap;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use std::fmt;
use std::marker::PhantomData;

/// `Math.round`: halves round up.
pub fn js_round(x: f64) -> f64 {
    let r = x.floor();
    if x - r >= 0.5 {
        r + 1.0
    } else {
        r
    }
}

/// `Number.prototype.toFixed`: exact decimal expansion and "half up" rounding.
pub fn to_fixed(x: f64, digits: usize) -> String {
    if x.is_nan() {
        return "NaN".into();
    }
    if x.is_infinite() {
        return if x < 0.0 { "-Infinity".into() } else { "Infinity".into() };
    }
    let neg = x < 0.0;
    let v = x.abs();
    let full = format!("{:.110}", v);
    let (int_part, frac_part) = match full.split_once('.') {
        Some((i, f)) => (i.to_string(), f.to_string()),
        None => (full.clone(), String::new()),
    };
    let mut digs: Vec<u8> = int_part.bytes().chain(frac_part.bytes().take(digits)).collect();
    let next = frac_part.as_bytes().get(digits).copied().unwrap_or(b'0');
    if next >= b'5' {
        let mut i = digs.len();
        loop {
            if i == 0 {
                digs.insert(0, b'1');
                break;
            }
            i -= 1;
            if digs[i] == b'9' {
                digs[i] = b'0';
            } else {
                digs[i] += 1;
                break;
            }
        }
    }
    let int_len = digs.len() - digits;
    let mut s = String::from_utf8_lossy(&digs[..int_len]).into_owned();
    if digits > 0 {
        s.push('.');
        s.push_str(&String::from_utf8_lossy(&digs[int_len..]));
    }
    if neg {
        s.insert(0, '-');
    }
    s
}

/// `Number(string)`: empty is 0, non-numeric is NaN.
pub fn js_num(s: &str) -> f64 {
    let t = s.trim();
    if t.is_empty() {
        return 0.0;
    }
    match t {
        "Infinity" | "+Infinity" => return f64::INFINITY,
        "-Infinity" => return f64::NEG_INFINITY,
        _ => {}
    }
    let radix = |p: &str, r: u32| -> Option<f64> {
        let body = t.strip_prefix(p)?;
        if body.is_empty() {
            return Some(f64::NAN);
        }
        let mut n = 0f64;
        for c in body.chars() {
            n = n * r as f64 + c.to_digit(r)? as f64;
        }
        Some(n)
    };
    for (p, r) in [("0x", 16), ("0X", 16), ("0b", 2), ("0B", 2), ("0o", 8), ("0O", 8)] {
        if t.starts_with(p) {
            return radix(p, r).unwrap_or(f64::NAN);
        }
    }
    if t.chars().any(|c| c.is_alphabetic() && c != 'e' && c != 'E') {
        return f64::NAN;
    }
    t.parse::<f64>().unwrap_or(f64::NAN)
}

/// `Number(x) || fallback`: NaN and 0 are replaced by the fallback value.
pub fn num_or(s: Option<&str>, default: f64) -> f64 {
    let n = s.map(js_num).unwrap_or(f64::NAN);
    if n.is_nan() || n == 0.0 {
        default
    } else {
        n
    }
}

/// Number from a command as a port or counter: NaN and negatives become 0, the fractional part is dropped.
pub fn to_int(f: f64) -> i64 {
    if f.is_nan() {
        0
    } else {
        f.trunc() as i64
    }
}

/// String length in UTF-16 units (`String.prototype.length`).
pub fn utf16_len(s: &str) -> usize {
    s.encode_utf16().count()
}

/// Number as JavaScript prints it in a template string (integers without ".0").
pub fn num_str(x: f64) -> String {
    if x.is_nan() {
        "NaN".into()
    } else if x == x.trunc() && x.abs() < 1e21 {
        format!("{}", x as i64)
    } else {
        format!("{}", x)
    }
}

/// String from an optional value as a JavaScript template would render it for `undefined`.
pub fn und(o: Option<&str>) -> &str {
    o.unwrap_or("undefined")
}

/// Insertion-ordered map (like a JavaScript object with non-numeric keys). Inserting an existing key
/// does not change its position. In JSON a plain object.
#[derive(Clone, Debug)]
pub struct OrdMap<V> {
    entries: Vec<(String, V)>,
}

/// Equality does not depend on key order: two maps with the same key-value pairs are equal.
impl<V: PartialEq> PartialEq for OrdMap<V> {
    fn eq(&self, other: &Self) -> bool {
        self.entries.len() == other.entries.len() && self.entries.iter().all(|(k, v)| other.get(k) == Some(v))
    }
}

impl<V> Default for OrdMap<V> {
    fn default() -> Self {
        OrdMap { entries: Vec::new() }
    }
}

impl<V> OrdMap<V> {
    pub fn new() -> Self {
        Self::default()
    }
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }
    pub fn len(&self) -> usize {
        self.entries.len()
    }
    pub fn get(&self, k: &str) -> Option<&V> {
        self.entries.iter().find(|(x, _)| x == k).map(|(_, v)| v)
    }
    pub fn get_mut(&mut self, k: &str) -> Option<&mut V> {
        self.entries.iter_mut().find(|(x, _)| x == k).map(|(_, v)| v)
    }
    pub fn contains_key(&self, k: &str) -> bool {
        self.get(k).is_some()
    }
    pub fn insert(&mut self, k: impl Into<String>, v: V) {
        let k = k.into();
        if let Some(slot) = self.get_mut(&k) {
            *slot = v;
        } else {
            self.entries.push((k, v));
        }
    }
    pub fn remove(&mut self, k: &str) -> Option<V> {
        let i = self.entries.iter().position(|(x, _)| x == k)?;
        Some(self.entries.remove(i).1)
    }
    pub fn iter(&self) -> impl Iterator<Item = (&String, &V)> {
        self.entries.iter().map(|(k, v)| (k, v))
    }
    pub fn iter_mut(&mut self) -> impl Iterator<Item = (&String, &mut V)> {
        self.entries.iter_mut().map(|(k, v)| (&*k, v))
    }
    pub fn keys(&self) -> impl Iterator<Item = &String> {
        self.entries.iter().map(|(k, _)| k)
    }
    pub fn values(&self) -> impl Iterator<Item = &V> {
        self.entries.iter().map(|(_, v)| v)
    }
    pub fn clear(&mut self) {
        self.entries.clear();
    }
    /// Value by key; if absent, insert `make()`.
    pub fn get_or_insert_with(&mut self, k: &str, make: impl FnOnce() -> V) -> &mut V {
        let i = match self.entries.iter().position(|(x, _)| x == k) {
            Some(i) => i,
            None => {
                self.entries.push((k.to_string(), make()));
                self.entries.len() - 1
            }
        };
        &mut self.entries[i].1
    }
}

impl<V: Serialize> Serialize for OrdMap<V> {
    fn serialize<S: Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        let mut m = s.serialize_map(Some(self.entries.len()))?;
        for (k, v) in &self.entries {
            m.serialize_entry(k, v)?;
        }
        m.end()
    }
}

impl<'de, V: Deserialize<'de>> Deserialize<'de> for OrdMap<V> {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct Vis<V>(PhantomData<V>);
        impl<'de, V: Deserialize<'de>> Visitor<'de> for Vis<V> {
            type Value = OrdMap<V>;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
                f.write_str(i18n::tr("an object"))
            }
            fn visit_map<A: MapAccess<'de>>(self, mut a: A) -> Result<Self::Value, A::Error> {
                let mut out = OrdMap::new();
                while let Some((k, v)) = a.next_entry::<String, V>()? {
                    out.insert(k, v);
                }
                Ok(out)
            }
        }
        d.deserialize_map(Vis(PhantomData))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn to_fixed_like_js() {
        assert_eq!(to_fixed(2.5, 0), "3");
        assert_eq!(to_fixed(0.0625, 3), "0.063");
        assert_eq!(to_fixed(1.005, 2), "1.00");
        assert_eq!(to_fixed(0.1 + 0.2, 3), "0.300");
        assert_eq!(to_fixed(99.96, 1), "100.0");
        assert_eq!(to_fixed(-0.0001, 3), "-0.000");
        assert_eq!(to_fixed(12.0, 0), "12");
    }

    #[test]
    fn js_num_parsing() {
        assert_eq!(js_num(" 12 "), 12.0);
        assert_eq!(js_num(""), 0.0);
        assert!(js_num("abc").is_nan());
        assert_eq!(js_num("0x10"), 16.0);
        assert!(js_num("inf").is_nan());
        assert_eq!(js_num("1e3"), 1000.0);
        assert_eq!(js_num(".5"), 0.5);
    }

    #[test]
    fn js_round_halves_up() {
        assert_eq!(js_round(2.5), 3.0);
        assert_eq!(js_round(-2.5), -2.0);
        assert_eq!(js_round(2.4), 2.0);
    }

    #[test]
    fn ordmap_order() {
        let mut m = OrdMap::new();
        m.insert("b", 1);
        m.insert("a", 2);
        m.insert("b", 3);
        assert_eq!(m.keys().cloned().collect::<Vec<_>>(), vec!["b", "a"]);
        let j = serde_json::to_string(&m).unwrap();
        assert_eq!(j, r#"{"b":3,"a":2}"#);
        let back: OrdMap<i32> = serde_json::from_str(&j).unwrap();
        assert_eq!(back, m);
        let other: OrdMap<i32> = serde_json::from_str(r#"{"a":2,"b":3}"#).unwrap();
        assert_eq!(other, m, "equality ignores order");
    }
}
