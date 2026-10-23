//! Числа так, как их печатает JavaScript: тексты целей и подписи должны совпадать с прежней версией до символа.

/// `Math.round`: половина округляется к +∞ (у `f64::round` — от нуля, для отрицательных иначе).
pub fn round(x: f64) -> f64 {
    if !x.is_finite() {
        return x;
    }
    let f = x.floor();
    if x - f >= 0.5 {
        f + 1.0
    } else {
        f
    }
}

/// `String(x)` для числа: целые без дробной части, `NaN` и `Infinity` словами.
pub fn num(x: f64) -> String {
    if x.is_nan() {
        "NaN".into()
    } else if x.is_infinite() {
        if x > 0.0 { "Infinity".into() } else { "-Infinity".into() }
    } else if x == 0.0 {
        "0".into()
    } else {
        format!("{x}")
    }
}

/// `x.toFixed(digits)`: точное десятичное разложение числа, при равенстве двух ближайших вариантов — больший по модулю
/// (у `format!("{:.1}")` «половинки» округляются к чётному: 98.25 → 98.2, а в JavaScript — 98.3).
pub fn fixed(x: f64, digits: usize) -> String {
    if !x.is_finite() {
        return num(x);
    }
    let neg = x < 0.0;
    // 60 знаков хватает, чтобы разложение двойного числа такого масштаба было точным
    let exact = format!("{:.60}", x.abs());
    let (int, frac) = exact.split_once('.').unwrap_or((&exact, ""));
    let mut digs: Vec<u8> = int.bytes().chain(frac.bytes().take(digits)).map(|b| b - b'0').collect();
    let round_up = frac.as_bytes().get(digits).is_some_and(|&b| b >= b'5');
    if round_up {
        let mut i = digs.len();
        loop {
            if i == 0 {
                digs.insert(0, 1);
                break;
            }
            i -= 1;
            if digs[i] == 9 {
                digs[i] = 0;
            } else {
                digs[i] += 1;
                break;
            }
        }
    }
    let text: String = digs.iter().map(|d| char::from(b'0' + d)).collect();
    let split = text.len() - digits;
    let mut out = String::new();
    if neg {
        out.push('-');
    }
    out.push_str(&text[..split]);
    if digits > 0 {
        out.push('.');
        out.push_str(&text[split..]);
    }
    out
}

/// Доля в процентах, как в подписях целей: `99.9%` и `99.950%` для долей от 0,999.
pub fn pct(x: f64) -> String {
    format!("{}%", fixed(x * 100.0, if x >= 0.999 { 3 } else { 1 }))
}

/// Целое число процентов: `Math.round(x * 100)`.
pub fn pct0(x: f64) -> String {
    num(round(x * 100.0))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn to_fixed_matches_javascript() {
        // значения, проверенные в Node: (98.25).toFixed(1) === "98.3", (0.5).toFixed(0) === "1", (2.5).toFixed(0) === "3"
        assert_eq!(fixed(98.25, 1), "98.3");
        assert_eq!(fixed(0.5, 0), "1");
        assert_eq!(fixed(2.5, 0), "3");
        assert_eq!(fixed(99.9, 1), "99.9");
        assert_eq!(fixed(99.95, 1), "100.0"); // 99.95 в двоичной записи чуть больше половинки
        assert_eq!(fixed(99.99999, 3), "100.000");
        assert_eq!(fixed(0.0, 1), "0.0");
        assert_eq!(fixed(-0.0, 1), "0.0");
        assert_eq!(fixed(-1.25, 1), "-1.3");
        assert_eq!(fixed(1234.5678, 2), "1234.57");
    }

    #[test]
    fn math_round_halves_go_up() {
        assert_eq!(round(0.5), 1.0);
        assert_eq!(round(1.5), 2.0);
        assert_eq!(round(2.5), 3.0);
        assert_eq!(round(-0.5), 0.0);
        assert_eq!(round(-1.5), -1.0);
        assert_eq!(round(0.49999999999999994), 0.0);
    }

    #[test]
    fn numbers_print_like_javascript() {
        assert_eq!(num(300.0), "300");
        assert_eq!(num(0.5), "0.5");
        assert_eq!(num(0.1 + 0.2), "0.30000000000000004");
        assert_eq!(num(f64::INFINITY), "Infinity");
        assert_eq!(pct(0.9995), "99.950%");
        assert_eq!(pct(0.98), "98.0%");
    }
}
