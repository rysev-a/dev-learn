//! Разбор таблицы стилей и каскад: какое значение свойства получит элемент (без раскладки: геометрию считает только браузер).

use std::collections::BTreeMap;

use scraper::ElementRef;

use crate::html::{selector, Doc};
use crate::selector::{has_id, specificity};
use crate::spec::{Check, Item};

#[derive(Debug, Clone)]
pub struct Decl {
    pub prop: String,
    pub value: String,
    pub important: bool,
}

#[derive(Debug, Clone)]
pub struct Rule {
    pub selectors: Vec<String>,
    pub decls: Vec<Decl>,
    /// условие внешнего `@media`
    pub media: Option<String>,
}

#[derive(Debug, Default, Clone)]
pub struct Stylesheet {
    pub rules: Vec<Rule>,
    pub errors: Vec<String>,
    pub media: Vec<String>,
}

/// Свойства, о существовании которых мы знаем: опечатка вроде `colr` попадает в ошибки разбора.
const KNOWN: &str = "align-content align-items align-self all animation animation-delay animation-direction animation-duration animation-fill-mode animation-iteration-count animation-name animation-play-state animation-timing-function appearance aspect-ratio backdrop-filter backface-visibility background background-attachment background-clip background-color background-image background-origin background-position background-repeat background-size border border-bottom border-bottom-color border-bottom-left-radius border-bottom-right-radius border-bottom-style border-bottom-width border-collapse border-color border-image border-left border-left-color border-left-style border-left-width border-radius border-right border-right-color border-right-style border-right-width border-spacing border-style border-top border-top-color border-top-left-radius border-top-right-radius border-top-style border-top-width border-width bottom box-shadow box-sizing caption-side caret-color clear clip clip-path color column-count column-gap column-rule column-width columns content counter-increment counter-reset cursor direction display empty-cells fill filter flex flex-basis flex-direction flex-flow flex-grow flex-shrink flex-wrap float font font-family font-feature-settings font-kerning font-size font-size-adjust font-stretch font-style font-variant font-weight gap grid grid-area grid-auto-columns grid-auto-flow grid-auto-rows grid-column grid-column-end grid-column-gap grid-column-start grid-gap grid-row grid-row-end grid-row-gap grid-row-start grid-template grid-template-areas grid-template-columns grid-template-rows height hyphens image-rendering inline-size inset inset-block inset-inline isolation justify-content justify-items justify-self left letter-spacing line-height list-style list-style-image list-style-position list-style-type margin margin-block margin-bottom margin-inline margin-left margin-right margin-top mask max-height max-width max-inline-size min-height min-width min-inline-size mix-blend-mode object-fit object-position opacity order orphans outline outline-color outline-offset outline-style outline-width overflow overflow-wrap overflow-x overflow-y overscroll-behavior padding padding-block padding-bottom padding-inline padding-left padding-right padding-top page-break-after page-break-before page-break-inside perspective place-content place-items place-self pointer-events position quotes resize right rotate row-gap scale scroll-behavior scroll-margin scroll-padding scroll-snap-align scroll-snap-type shape-outside stroke stroke-width tab-size table-layout text-align text-align-last text-decoration text-decoration-color text-decoration-line text-decoration-style text-decoration-thickness text-indent text-overflow text-shadow text-transform text-underline-offset top touch-action transform transform-origin transform-style transition transition-delay transition-duration transition-property transition-timing-function translate unicode-bidi user-select vertical-align visibility white-space widows width will-change word-break word-spacing word-wrap writing-mode z-index zoom";

fn strip_comments(src: &str) -> String {
    let mut out = String::with_capacity(src.len());
    let mut it = src.chars().peekable();
    while let Some(c) = it.next() {
        if c == '/' && it.peek() == Some(&'*') {
            it.next();
            while let Some(c) = it.next() {
                if c == '*' && it.peek() == Some(&'/') {
                    it.next();
                    break;
                }
            }
            out.push(' ');
        } else {
            out.push(c);
        }
    }
    out
}

/// Делит по символу вне скобок и кавычек.
fn split_outside(s: &str, sep: char) -> Vec<String> {
    let (mut out, mut cur, mut depth, mut quote) = (Vec::new(), String::new(), 0i32, None::<char>);
    for c in s.chars() {
        match quote {
            Some(q) => {
                cur.push(c);
                if c == q {
                    quote = None;
                }
            }
            None => match c {
                '"' | '\'' => {
                    quote = Some(c);
                    cur.push(c);
                }
                '(' => {
                    depth += 1;
                    cur.push(c);
                }
                ')' => {
                    depth -= 1;
                    cur.push(c);
                }
                c if c == sep && depth <= 0 => out.push(std::mem::take(&mut cur)),
                _ => cur.push(c),
            },
        }
    }
    out.push(cur);
    out
}

/// Блок `{ … }` с позиции после `{`: возвращает содержимое и позицию после закрывающей скобки.
fn block(chars: &[char], mut i: usize) -> Option<(String, usize)> {
    let (start, mut depth, mut quote) = (i, 1, None::<char>);
    while i < chars.len() {
        let c = chars[i];
        match quote {
            Some(q) => {
                if c == q {
                    quote = None;
                }
            }
            None => match c {
                '"' | '\'' => quote = Some(c),
                '{' => depth += 1,
                '}' => {
                    depth -= 1;
                    if depth == 0 {
                        return Some((chars[start..i].iter().collect(), i + 1));
                    }
                }
                _ => {}
            },
        }
        i += 1;
    }
    None
}

pub fn parse_decls(body: &str, errors: &mut Vec<String>) -> Vec<Decl> {
    let mut out = Vec::new();
    for part in split_outside(body, ';') {
        let part = part.trim();
        if part.is_empty() {
            continue;
        }
        let Some((p, v)) = part.split_once(':') else {
            errors.push(format!("в объявлении «{part}» нет двоеточия"));
            continue;
        };
        let prop = p.trim().to_lowercase();
        let mut value = v.trim().to_string();
        let mut important = false;
        let low = value.to_lowercase();
        if let Some(pos) = low.rfind("!important") {
            important = true;
            value = value[..pos].trim().to_string();
        }
        if prop.is_empty() || value.is_empty() {
            errors.push(format!("в объявлении «{part}» нет {}", if prop.is_empty() { "свойства" } else { "значения" }));
            continue;
        }
        if !prop.starts_with("--") && !prop.starts_with('-') && !KNOWN.split(' ').any(|k| k == prop) {
            errors.push(format!("неизвестное свойство `{prop}`"));
        }
        out.push(Decl { prop, value, important });
    }
    out
}

impl Stylesheet {
    pub fn parse(src: &str) -> Stylesheet {
        let src: Vec<char> = strip_comments(src).chars().collect();
        let mut sheet = Stylesheet::default();
        sheet.parse_into(&src, None);
        sheet
    }

    fn parse_into(&mut self, chars: &[char], media: Option<&str>) {
        let mut i = 0;
        while i < chars.len() {
            while i < chars.len() && chars[i].is_whitespace() {
                i += 1;
            }
            if i >= chars.len() {
                break;
            }
            let start = i;
            let (mut quote, mut paren) = (None::<char>, 0);
            while i < chars.len() {
                let c = chars[i];
                match quote {
                    Some(q) => {
                        if c == q {
                            quote = None;
                        }
                    }
                    None => match c {
                        '"' | '\'' => quote = Some(c),
                        '(' => paren += 1,
                        ')' => paren -= 1,
                        '{' | ';' if paren <= 0 => break,
                        '}' if paren <= 0 => break,
                        _ => {}
                    },
                }
                i += 1;
            }
            let head: String = chars[start..i.min(chars.len())].iter().collect();
            let head = head.trim().to_string();
            match chars.get(i) {
                Some(';') => {
                    // `@import …;` и подобное: игнорируем
                    if !head.starts_with('@') {
                        self.errors.push(format!("«{head}» вне правила"));
                    }
                    i += 1;
                }
                Some('}') => {
                    self.errors.push("лишняя закрывающая `}`".into());
                    i += 1;
                }
                Some('{') => {
                    let Some((body, next)) = block(chars, i + 1) else {
                        self.errors.push(format!("не закрыта `{{` после «{head}»"));
                        break;
                    };
                    i = next;
                    if let Some(at) = head.strip_prefix('@') {
                        let name = at.split(|c: char| c.is_whitespace() || c == '(').next().unwrap_or("").to_lowercase();
                        match name.as_str() {
                            "media" => {
                                let cond = at["media".len()..].trim().to_string();
                                self.media.push(cond.clone());
                                let inner: Vec<char> = body.chars().collect();
                                self.parse_into(&inner, Some(&cond));
                            }
                            "supports" | "layer" | "container" => {
                                let inner: Vec<char> = body.chars().collect();
                                self.parse_into(&inner, media);
                            }
                            _ => {} // keyframes, font-face, …
                        }
                    } else {
                        if head.is_empty() {
                            self.errors.push("правило без селектора".into());
                            continue;
                        }
                        let selectors: Vec<String> = split_outside(&head, ',').into_iter().map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect();
                        for s in &selectors {
                            if selector(s).is_err() {
                                self.errors.push(format!("селектор «{s}» не разобран"));
                            }
                        }
                        let decls = parse_decls(&body, &mut self.errors);
                        self.rules.push(Rule { selectors, decls, media: media.map(String::from) });
                    }
                }
                _ => {
                    if !head.is_empty() {
                        self.errors.push(format!("«{head}» не закончено: нет `{{`"));
                    }
                    break;
                }
            }
        }
    }

    pub fn uses_important(&self) -> bool {
        self.rules.iter().flat_map(|r| &r.decls).any(|d| d.important)
    }

    pub fn uses_ids(&self) -> bool {
        self.rules.iter().flat_map(|r| &r.selectors).any(|s| has_id(s))
    }
}

/// Выполняется ли условие `@media` при ширине окна `width`.
pub fn media_matches(cond: &str, width: f64) -> bool {
    split_outside(cond, ',').iter().any(|q| {
        let q = q.trim().to_lowercase();
        if q.starts_with("not ") {
            return false;
        }
        if q.split_whitespace().next() == Some("print") {
            return false;
        }
        let mut ok = true;
        let mut rest = q.as_str();
        while let Some(a) = rest.find('(') {
            let Some(b) = rest[a..].find(')') else { break };
            let feat = &rest[a + 1..a + b];
            rest = &rest[a + b + 1..];
            let Some((name, val)) = feat.split_once(':') else { continue };
            let px = parse_px(val.trim());
            match (name.trim(), px) {
                ("min-width", Some(v)) => ok &= width >= v,
                ("max-width", Some(v)) => ok &= width <= v,
                ("width", Some(v)) => ok &= (width - v).abs() < 0.5,
                ("prefers-color-scheme", _) => ok &= val.trim() == "light",
                ("prefers-reduced-motion", _) => ok &= val.trim() == "no-preference",
                _ => {}
            }
        }
        ok
    })
}

fn parse_px(v: &str) -> Option<f64> {
    let v = v.trim();
    if let Some(n) = v.strip_suffix("px") {
        n.trim().parse().ok()
    } else if let Some(n) = v.strip_suffix("rem").or_else(|| v.strip_suffix("em")) {
        n.trim().parse::<f64>().ok().map(|x| x * 16.0)
    } else {
        None
    }
}

// ---------- значения ----------

const NAMED: &[(&str, (u8, u8, u8))] = &[
    ("black", (0, 0, 0)), ("white", (255, 255, 255)), ("red", (255, 0, 0)), ("green", (0, 128, 0)), ("blue", (0, 0, 255)),
    ("yellow", (255, 255, 0)), ("orange", (255, 165, 0)), ("purple", (128, 0, 128)), ("gray", (128, 128, 128)), ("grey", (128, 128, 128)),
    ("silver", (192, 192, 192)), ("lime", (0, 255, 0)), ("aqua", (0, 255, 255)), ("cyan", (0, 255, 255)), ("fuchsia", (255, 0, 255)),
    ("magenta", (255, 0, 255)), ("maroon", (128, 0, 0)), ("navy", (0, 0, 128)), ("olive", (128, 128, 0)), ("teal", (0, 128, 128)),
    ("pink", (255, 192, 203)), ("brown", (165, 42, 42)), ("gold", (255, 215, 0)), ("tomato", (255, 99, 71)), ("coral", (255, 127, 80)),
    ("crimson", (220, 20, 60)), ("indigo", (75, 0, 130)), ("violet", (238, 130, 238)), ("salmon", (250, 128, 114)), ("khaki", (240, 230, 140)),
    ("lightgray", (211, 211, 211)), ("lightgrey", (211, 211, 211)), ("darkgray", (169, 169, 169)), ("darkgrey", (169, 169, 169)),
    ("lightblue", (173, 216, 230)), ("darkblue", (0, 0, 139)), ("lightgreen", (144, 238, 144)), ("darkgreen", (0, 100, 0)),
    ("darkred", (139, 0, 0)), ("skyblue", (135, 206, 235)), ("steelblue", (70, 130, 180)), ("whitesmoke", (245, 245, 245)),
    ("rebeccapurple", (102, 51, 153)), ("dodgerblue", (30, 144, 255)), ("slategray", (112, 128, 144)), ("midnightblue", (25, 25, 112)),
];

fn hex(s: &str) -> Option<(u8, u8, u8, f64)> {
    let h = s.strip_prefix('#')?;
    let d = |i: usize, n: usize| u8::from_str_radix(&h[i..i + n], 16).ok();
    match h.len() {
        3 => Some((d(0, 1)? * 17, d(1, 1)? * 17, d(2, 1)? * 17, 1.0)),
        4 => Some((d(0, 1)? * 17, d(1, 1)? * 17, d(2, 1)? * 17, d(3, 1)? as f64 * 17.0 / 255.0)),
        6 => Some((d(0, 2)?, d(2, 2)?, d(4, 2)?, 1.0)),
        8 => Some((d(0, 2)?, d(2, 2)?, d(4, 2)?, d(6, 2)? as f64 / 255.0)),
        _ => None,
    }
}

fn fmt_num(x: f64) -> String {
    let r = (x * 1000.0).round() / 1000.0;
    if r.fract() == 0.0 {
        format!("{}", r as i64)
    } else {
        format!("{r}")
    }
}

fn rgb_string(r: u8, g: u8, b: u8, a: f64) -> String {
    if (a - 1.0).abs() < 1e-3 {
        format!("rgb({r}, {g}, {b})")
    } else {
        format!("rgba({r}, {g}, {b}, {})", fmt_num(a))
    }
}

/// Цвет в виде `rgb(r, g, b)` / `rgba(…)`, если это цвет.
pub fn color(token: &str) -> Option<String> {
    let t = token.trim().to_lowercase();
    if let Some((r, g, b, a)) = hex(&t) {
        return Some(rgb_string(r, g, b, a));
    }
    if t == "transparent" {
        return Some("rgba(0, 0, 0, 0)".into());
    }
    if let Some((_, (r, g, b))) = NAMED.iter().find(|(n, _)| *n == t) {
        return Some(rgb_string(*r, *g, *b, 1.0));
    }
    let args = t.strip_prefix("rgba(").or_else(|| t.strip_prefix("rgb(")).and_then(|x| x.strip_suffix(')'))?;
    let nums: Vec<f64> = args.split(|c: char| c == ',' || c == '/' || c.is_whitespace()).filter(|s| !s.is_empty()).map(|s| match s.strip_suffix('%') {
        Some(p) => p.parse::<f64>().map(|x| x * 2.55),
        None => s.parse::<f64>(),
    }.unwrap_or(f64::NAN)).collect();
    if nums.len() < 3 || nums.iter().any(|n| n.is_nan()) {
        return None;
    }
    let a = nums.get(3).copied().unwrap_or(1.0);
    let a = if args.contains('%') && nums.len() == 4 && args.trim_end().ends_with('%') { a / 2.55 / 100.0 } else { a };
    Some(rgb_string(nums[0].round().clamp(0.0, 255.0) as u8, nums[1].round().clamp(0.0, 255.0) as u8, nums[2].round().clamp(0.0, 255.0) as u8, a))
}

struct Ctx {
    /// размер шрифта элемента в px (для `em`)
    font: f64,
    viewport: f64,
}

/// Число с единицей → px, если единица известна; иначе исходный токен.
fn length(token: &str, ctx: &Ctx) -> String {
    let t = token.trim().to_lowercase();
    if t == "0" {
        return "0px".into();
    }
    let split = t.find(|c: char| c.is_alphabetic() || c == '%').unwrap_or(t.len());
    let (num, unit) = t.split_at(split);
    let Ok(n) = num.parse::<f64>() else { return t };
    match unit {
        "px" => format!("{}px", fmt_num(n)),
        "rem" => format!("{}px", fmt_num(n * 16.0)),
        "em" => format!("{}px", fmt_num(n * ctx.font)),
        "vw" => format!("{}px", fmt_num(n * ctx.viewport / 100.0)),
        "pt" => format!("{}px", fmt_num(n * 96.0 / 72.0)),
        "%" | "fr" | "deg" | "s" | "ms" | "vh" | "ch" => format!("{}{unit}", fmt_num(n)),
        "" => fmt_num(n),
        _ => t,
    }
}

/// Значение в канонической записи: цвета — `rgb(…)`, длины — px, регистр и пробелы выровнены.
fn norm(value: &str, ctx: &Ctx) -> String {
    let v = value.trim();
    if v.contains('(') && !v.to_lowercase().starts_with("rgb") && !v.to_lowercase().starts_with("hsl") && split_outside(v, ' ').len() == 1 {
        // функции (calc, var, url, repeat…) — только пробелы выровнены
        return v.split_whitespace().collect::<Vec<_>>().join(" ").to_lowercase();
    }
    let tokens: Vec<String> = split_outside(v, ' ').into_iter().filter(|t| !t.trim().is_empty()).collect();
    let out: Vec<String> = tokens
        .iter()
        .map(|t| {
            if let Some(c) = color(t) {
                c
            } else if t.starts_with(|c: char| c.is_ascii_digit() || c == '.' || c == '-' || c == '+') && !t.contains('(') {
                length(t, ctx)
            } else if t.contains('(') || t.starts_with('"') || t.starts_with('\'') {
                t.to_string()
            } else {
                t.to_lowercase()
            }
        })
        .collect();
    out.join(" ")
}

// ---------- каскад ----------

fn sides(prefix: &str, suffix: &str, value: &str) -> Vec<(String, String)> {
    let v: Vec<&str> = value.split_whitespace().collect();
    let (t, r, b, l) = match v.len() {
        1 => (v[0], v[0], v[0], v[0]),
        2 => (v[0], v[1], v[0], v[1]),
        3 => (v[0], v[1], v[2], v[1]),
        4 => (v[0], v[1], v[2], v[3]),
        _ => return vec![],
    };
    [("top", t), ("right", r), ("bottom", b), ("left", l)].iter().map(|(s, x)| (format!("{prefix}-{s}{suffix}"), x.to_string())).collect()
}

fn is_style(t: &str) -> bool {
    matches!(t, "none" | "solid" | "dashed" | "dotted" | "double" | "groove" | "ridge" | "inset" | "outset" | "hidden")
}

/// Раскрывает сокращённое свойство в составляющие.
fn expand(prop: &str, value: &str) -> Vec<(String, String)> {
    let v = value.trim();
    match prop {
        "margin" | "padding" => sides(prop, "", v),
        "inset" => sides("", "", v).into_iter().map(|(p, x)| (p.trim_start_matches('-').to_string(), x)).collect(),
        "border-width" => sides("border", "-width", v),
        "border-style" => sides("border", "-style", v),
        "border-color" => sides("border", "-color", v),
        "border" | "border-top" | "border-right" | "border-bottom" | "border-left" => {
            let (mut w, mut s, mut c) = ("medium".to_string(), "none".to_string(), "currentcolor".to_string());
            for t in split_outside(v, ' ').iter().filter(|t| !t.is_empty()) {
                if is_style(&t.to_lowercase()) {
                    s = t.clone();
                } else if color(t).is_some() || t.eq_ignore_ascii_case("currentcolor") {
                    c = t.clone();
                } else {
                    w = t.clone();
                }
            }
            let which: Vec<&str> = if prop == "border" { vec!["top", "right", "bottom", "left"] } else { vec![&prop["border-".len()..]] };
            which.iter().flat_map(|side| [(format!("border-{side}-width"), w.clone()), (format!("border-{side}-style"), s.clone()), (format!("border-{side}-color"), c.clone())]).collect()
        }
        "gap" | "grid-gap" => {
            let p: Vec<&str> = v.split_whitespace().collect();
            match p.len() {
                1 => vec![("row-gap".into(), p[0].into()), ("column-gap".into(), p[0].into())],
                2 => vec![("row-gap".into(), p[0].into()), ("column-gap".into(), p[1].into())],
                _ => vec![],
            }
        }
        "flex" => {
            let p: Vec<&str> = v.split_whitespace().collect();
            let (g, s, b) = match p.as_slice() {
                ["none"] => ("0", "0", "auto"),
                ["auto"] => ("1", "1", "auto"),
                [x] if x.parse::<f64>().is_ok() => (*x, "1", "0%"),
                [x, y] if x.parse::<f64>().is_ok() && y.parse::<f64>().is_ok() => (*x, *y, "0%"),
                [x, y] if x.parse::<f64>().is_ok() => (*x, "1", *y),
                [x, y, z] => (*x, *y, *z),
                _ => return vec![],
            };
            vec![("flex-grow".into(), g.into()), ("flex-shrink".into(), s.into()), ("flex-basis".into(), b.into())]
        }
        "flex-flow" => {
            let mut out = Vec::new();
            for t in v.split_whitespace() {
                if t.contains("wrap") {
                    out.push(("flex-wrap".to_string(), t.to_string()));
                } else {
                    out.push(("flex-direction".to_string(), t.to_string()));
                }
            }
            out
        }
        "background" => split_outside(v, ' ').iter().filter(|t| color(t).is_some()).map(|t| ("background-color".to_string(), t.clone())).collect(),
        "overflow" => {
            let p: Vec<&str> = v.split_whitespace().collect();
            match p.len() {
                1 => vec![("overflow-x".into(), p[0].into()), ("overflow-y".into(), p[0].into())],
                2 => vec![("overflow-x".into(), p[0].into()), ("overflow-y".into(), p[1].into())],
                _ => vec![],
            }
        }
        "list-style" => v.split_whitespace().next().map(|t| vec![("list-style-type".to_string(), t.to_string())]).unwrap_or_default(),
        _ => vec![(prop.to_string(), v.to_string())],
    }
}

/// Какие составляющие входят в сокращение (чтобы проверять `margin` по четырём сторонам).
fn parts_of(prop: &str) -> Option<Vec<String>> {
    let four = |p: &str, s: &str| ["top", "right", "bottom", "left"].iter().map(|x| format!("{p}-{x}{s}")).collect();
    Some(match prop {
        "margin" | "padding" => four(prop, ""),
        "border-width" => four("border", "-width"),
        "border-style" => four("border", "-style"),
        "border-color" => four("border", "-color"),
        "inset" => ["top", "right", "bottom", "left"].iter().map(|s| s.to_string()).collect(),
        "gap" => vec!["row-gap".into(), "column-gap".into()],
        _ => return None,
    })
}

fn inherited(prop: &str) -> bool {
    prop.starts_with("--")
        || matches!(
            prop,
            "color" | "font-family" | "font-size" | "font-style" | "font-weight" | "font-variant" | "line-height" | "letter-spacing" | "word-spacing" | "text-align" | "text-indent"
                | "text-transform" | "white-space" | "visibility" | "cursor" | "list-style-type" | "list-style-position" | "direction" | "quotes" | "tab-size" | "word-break" | "overflow-wrap"
                | "pointer-events" | "caret-color" | "border-collapse" | "border-spacing"
        )
}

fn initial(prop: &str) -> Option<&'static str> {
    Some(match prop {
        "color" => "rgb(0, 0, 0)",
        "font-size" => "16px",
        "font-weight" => "400",
        "font-style" => "normal",
        "line-height" => "normal",
        "text-align" => "start",
        "background-color" => "rgba(0, 0, 0, 0)",
        "position" => "static",
        "opacity" => "1",
        "visibility" => "visible",
        "flex-direction" => "row",
        "flex-wrap" => "nowrap",
        "flex-grow" => "0",
        "flex-shrink" => "1",
        "flex-basis" => "auto",
        "justify-content" | "align-items" | "align-content" | "align-self" | "row-gap" | "column-gap" => "normal",
        "order" => "0",
        "box-sizing" => "content-box",
        "float" => "none",
        "overflow-x" | "overflow-y" => "visible",
        "z-index" => "auto",
        "text-decoration-line" => "none",
        "text-transform" => "none",
        "cursor" => "auto",
        "width" | "height" | "top" | "right" | "bottom" | "left" => "auto",
        "margin-top" | "margin-right" | "margin-bottom" | "margin-left" | "padding-top" | "padding-right" | "padding-bottom" | "padding-left" => "0px",
        "border-top-width" | "border-right-width" | "border-bottom-width" | "border-left-width" => "0px",
        "border-top-style" | "border-right-style" | "border-bottom-style" | "border-left-style" => "none",
        "border-radius" => "0px",
        _ => return None,
    })
}

/// Стили пользовательского агента для тегов, которые встречаются в упражнениях.
fn ua_style(tag: &str) -> Vec<(&'static str, &'static str)> {
    let mut v: Vec<(&str, &str)> = Vec::new();
    let display = match tag {
        "html" | "body" | "div" | "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "ul" | "ol" | "section" | "article" | "header" | "footer" | "nav" | "main" | "aside" | "form"
        | "pre" | "blockquote" | "figure" | "figcaption" | "fieldset" | "hr" | "address" | "details" | "dl" | "dt" | "dd" | "menu" | "legend" => "block",
        "li" | "summary" => "list-item",
        "table" => "table",
        "tr" => "table-row",
        "td" | "th" => "table-cell",
        "thead" => "table-header-group",
        "tbody" => "table-row-group",
        "tfoot" => "table-footer-group",
        "caption" => "table-caption",
        "input" | "button" | "select" | "textarea" | "img" | "video" | "canvas" | "svg" => "inline-block",
        "head" | "script" | "style" | "title" | "meta" | "link" | "template" | "datalist" => "none",
        _ => "inline",
    };
    v.push(("display", display));
    match tag {
        "h1" => v.extend([("font-size", "2em"), ("font-weight", "700"), ("margin-top", "0.67em"), ("margin-bottom", "0.67em")]),
        "h2" => v.extend([("font-size", "1.5em"), ("font-weight", "700"), ("margin-top", "0.83em"), ("margin-bottom", "0.83em")]),
        "h3" => v.extend([("font-size", "1.17em"), ("font-weight", "700"), ("margin-top", "1em"), ("margin-bottom", "1em")]),
        "h4" => v.extend([("font-size", "1em"), ("font-weight", "700"), ("margin-top", "1.33em"), ("margin-bottom", "1.33em")]),
        "h5" => v.extend([("font-size", "0.83em"), ("font-weight", "700"), ("margin-top", "1.67em"), ("margin-bottom", "1.67em")]),
        "h6" => v.extend([("font-size", "0.67em"), ("font-weight", "700"), ("margin-top", "2.33em"), ("margin-bottom", "2.33em")]),
        "p" | "dl" | "blockquote" | "figure" | "pre" => v.extend([("margin-top", "1em"), ("margin-bottom", "1em")]),
        "ul" | "ol" => v.extend([("margin-top", "1em"), ("margin-bottom", "1em"), ("padding-left", "40px")]),
        "body" => v.extend([("margin-top", "8px"), ("margin-right", "8px"), ("margin-bottom", "8px"), ("margin-left", "8px")]),
        "b" | "strong" | "th" => v.push(("font-weight", "700")),
        "em" | "i" | "cite" | "dfn" => v.push(("font-style", "italic")),
        "a" => v.extend([("color", "rgb(0, 0, 238)"), ("text-decoration-line", "underline"), ("cursor", "pointer")]),
        "button" => v.push(("cursor", "default")),
        _ => {}
    }
    v
}

/// Приоритет объявления: (важное, источник, специфичность, порядок). Источник: 0 — браузер, 1 — автор, 2 — атрибут `style`.
type Weight = (bool, u8, [u32; 3], usize);

pub struct Cascade<'a> {
    pub doc: &'a Doc,
    pub sheet: &'a Stylesheet,
    pub viewport: f64,
}

impl Cascade<'_> {
    /// Объявленные значения элемента после каскада, до наследования и разрешения единиц, и его пользовательские свойства.
    fn declared(&self, el: &ElementRef, parent_customs: &BTreeMap<String, String>) -> (BTreeMap<String, (Weight, String)>, BTreeMap<String, String>) {
        let mut raw: Vec<(String, String, Weight)> = Vec::new();
        let mut order = 0usize;
        for (p, v) in ua_style(el.value().name()) {
            order += 1;
            raw.push((p.into(), v.into(), (false, 0, [0; 3], order)));
        }
        for rule in &self.sheet.rules {
            if let Some(m) = &rule.media {
                if !media_matches(m, self.viewport) {
                    continue;
                }
            }
            // у правила со списком селекторов работает самый специфичный из совпавших
            let sp = rule.selectors.iter().filter(|s| selector(s).is_ok_and(|sel| sel.matches(el))).map(|s| specificity(s)).max();
            let Some(sp) = sp else { continue };
            for d in &rule.decls {
                order += 1;
                raw.push((d.prop.clone(), d.value.clone(), (d.important, 1u8, sp, order)));
            }
        }
        if let Some(style) = el.value().attr("style") {
            let mut ignore = Vec::new();
            for d in parse_decls(style, &mut ignore) {
                order += 1;
                raw.push((d.prop.clone(), d.value.clone(), (d.important, 2u8, [0; 3], order)));
            }
        }
        // пользовательские свойства: свои побеждают по приоритету, остальные наследуются
        let mut customs = parent_customs.clone();
        let mut won: BTreeMap<String, Weight> = BTreeMap::new();
        for (p, v, w) in raw.iter().filter(|(p, _, _)| p.starts_with("--")) {
            if won.get(p).is_none_or(|old| w >= old) {
                won.insert(p.clone(), *w);
                customs.insert(p.clone(), v.clone());
            }
        }
        let mut best: BTreeMap<String, (Weight, String)> = BTreeMap::new();
        for (p, v, w) in raw.into_iter().filter(|(p, _, _)| !p.starts_with("--")) {
            let v = substitute(&v, &customs, 0);
            for (p, v) in expand(&p, &v) {
                if best.get(&p).is_none_or(|(old, _)| w >= *old) {
                    best.insert(p, (w, v));
                }
            }
        }
        (best, customs)
    }

    /// Вычисленные значения всех известных свойств элемента (с наследованием, `var()` и единицами в px).
    pub fn computed(&self, el: &ElementRef) -> BTreeMap<String, String> {
        let parent = el.parent().and_then(ElementRef::wrap).map(|p| self.computed(&p));
        let parent_customs: BTreeMap<String, String> = parent.as_ref().map(|p| p.iter().filter(|(k, _)| k.starts_with("--")).map(|(k, v)| (k.clone(), v.clone())).collect()).unwrap_or_default();
        let (declared, customs) = self.declared(el, &parent_customs);
        let parent_font = parent.as_ref().and_then(|p| p.get("font-size")).and_then(|v| parse_px(v)).unwrap_or(16.0);
        let mut out: BTreeMap<String, String> = BTreeMap::new();
        let font_ctx = Ctx { font: parent_font, viewport: self.viewport };
        let own_font = match declared.get("font-size") {
            Some((_, v)) => {
                match v.trim() {
                    "inherit" => parent_font,
                    "larger" => parent_font * 1.2,
                    "smaller" => parent_font / 1.2,
                    "small" => 13.0,
                    "medium" => 16.0,
                    "large" => 18.0,
                    t => {
                        let n = norm(t, &font_ctx);
                        // проценты считаются от шрифта родителя
                        match n.strip_suffix('%').and_then(|x| x.parse::<f64>().ok()) {
                            Some(p) => parent_font * p / 100.0,
                            None => parse_px(&n).unwrap_or(parent_font),
                        }
                    }
                }
            }
            None => parent_font,
        };
        let ctx = Ctx { font: own_font, viewport: self.viewport };
        for (k, v) in &customs {
            out.insert(k.clone(), v.clone());
        }
        for (prop, (_, raw)) in declared.iter().filter(|(k, _)| !k.starts_with("--")) {
            let value = match raw.trim().to_lowercase().as_str() {
                "inherit" => parent.as_ref().and_then(|p| p.get(prop)).cloned().or_else(|| initial(prop).map(String::from)),
                "initial" => initial(prop).map(String::from),
                "unset" => {
                    if inherited(prop) { parent.as_ref().and_then(|p| p.get(prop)).cloned() } else { initial(prop).map(String::from) }
                }
                _ => Some(if prop == "font-size" { format!("{}px", fmt_num(own_font)) } else { norm(&raw, &ctx) }),
            };
            if let Some(v) = value {
                out.insert(prop.clone(), v);
            }
        }
        // наследуемые свойства, которых нет у элемента
        if let Some(p) = &parent {
            for (k, v) in p {
                if inherited(k) && !out.contains_key(k) {
                    out.insert(k.clone(), v.clone());
                }
            }
        }
        // `currentcolor` у цвета рамки и фона — цвет текста
        let text = out.get("color").cloned().or_else(|| initial("color").map(String::from)).unwrap_or_default();
        for v in out.values_mut() {
            if v.contains("currentcolor") {
                *v = v.replace("currentcolor", &text);
            }
        }
        for k in ["color", "font-size", "font-weight", "font-style", "line-height", "text-align", "background-color", "position", "visibility", "opacity"] {
            if !out.contains_key(k) {
                if let Some(v) = initial(k) {
                    out.insert(k.into(), v.into());
                }
            }
        }
        out
    }
}

/// Подставляет `var(--x, запасное)`.
fn substitute(v: &str, vars: &BTreeMap<String, String>, depth: u8) -> String {
    if depth > 8 || !v.contains("var(") {
        return v.to_string();
    }
    let mut out = String::new();
    let mut rest = v;
    while let Some(a) = rest.find("var(") {
        out.push_str(&rest[..a]);
        let after = &rest[a + 4..];
        let (mut d, mut end) = (1, after.len());
        for (i, c) in after.char_indices() {
            match c {
                '(' => d += 1,
                ')' => {
                    d -= 1;
                    if d == 0 {
                        end = i;
                        break;
                    }
                }
                _ => {}
            }
        }
        let inner = &after[..end];
        let (name, fallback) = match inner.split_once(',') {
            Some((n, f)) => (n.trim(), Some(f.trim())),
            None => (inner.trim(), None),
        };
        let val = vars.get(name).cloned().or_else(|| fallback.map(String::from)).unwrap_or_default();
        out.push_str(&substitute(&val, vars, depth + 1));
        rest = after.get(end + 1..).unwrap_or("");
    }
    out.push_str(rest);
    out
}

/// Значение свойства у элемента; сокращения (`margin`, `gap`) собираются из составляющих.
fn value_of(map: &BTreeMap<String, String>, prop: &str) -> Option<String> {
    if let Some(parts) = parts_of(prop) {
        let vals: Vec<String> = parts.iter().filter_map(|p| map.get(p).cloned().or_else(|| initial(p).map(String::from))).collect();
        if vals.len() != parts.len() {
            return None;
        }
        let uniq = vals.iter().all(|v| *v == vals[0]);
        return Some(if uniq { vals[0].clone() } else if vals.len() == 4 && vals[0] == vals[2] && vals[1] == vals[3] { format!("{} {}", vals[0], vals[1]) } else { vals.join(" ") });
    }
    map.get(prop).cloned().or_else(|| initial(prop).map(String::from))
}

fn plain(prop: &str, v: &str) -> String {
    let _ = prop;
    v.to_string()
}

/// CSS-условие. `None` — условие относится к HTML.
/// `sheet` — все правила (из `<style>` задания и ученика) для каскада, `user` — только правила ученика для статических условий.
pub fn run(doc: &Doc, sheet: &Stylesheet, user: &Stylesheet, check: &Check, viewport: f64) -> Option<Item> {
    Some(match check {
        Check::CssValid => Item { text: "CSS без ошибок".into(), ok: user.errors.is_empty(), detail: user.errors.first().cloned().unwrap_or_default() },
        Check::NoImportant => Item { text: "Без `!important`".into(), ok: !user.uses_important(), detail: "найден `!important`".into() },
        Check::NoIds => Item { text: "Без селекторов по `#id`".into(), ok: !user.uses_ids(), detail: "найден селектор по идентификатору".into() },
        Check::Uses { prop, value, msg } => {
            let p = prop.to_lowercase();
            let text = msg.clone().unwrap_or_else(|| match value {
                Some(v) => format!("Используется `{p}: {v}`"),
                None => format!("Используется `{p}`"),
            });
            let ok = user.rules.iter().flat_map(|r| &r.decls).any(|d| d.prop == p && value.as_ref().is_none_or(|v| d.value.trim().eq_ignore_ascii_case(v.trim())));
            Item { text, ok, detail: "такого объявления нет в вашем CSS".into() }
        }
        Check::Media { contains, msg } => {
            let text = msg.clone().unwrap_or_else(|| format!("Есть `@media` с `{contains}`"));
            let ok = user.media.iter().any(|m| m.to_lowercase().contains(&contains.to_lowercase()));
            Item { text, ok, detail: "правила `@media` с таким условием нет".into() }
        }
        Check::Style { sel, prop, equals, one_of, min, max, any, viewport: vp, msg } => {
            let prop = prop.to_lowercase();
            let width = vp.unwrap_or(viewport);
            let want = equals.clone().or_else(|| (!one_of.is_empty()).then(|| one_of.join(" | "))).unwrap_or_else(|| match (min, max) {
                (Some(a), Some(b)) => format!("от {} до {} px", fmt_num(*a), fmt_num(*b)),
                (Some(a), None) => format!("не меньше {} px", fmt_num(*a)),
                (None, Some(b)) => format!("не больше {} px", fmt_num(*b)),
                _ => "задано".into(),
            });
            let at = if vp.is_some() { format!(" при ширине {}px", fmt_num(width)) } else { String::new() };
            let text = msg.clone().unwrap_or_else(|| format!("У `{sel}` {prop}: {want}{at}"));
            let els = match doc.select(sel) {
                Err(e) => return Some(Item { text, ok: false, detail: e }),
                Ok(v) if v.is_empty() => return Some(Item { text, ok: false, detail: "в разметке нет такого элемента".into() }),
                Ok(v) => v,
            };
            let cascade = Cascade { doc, sheet, viewport: width };
            let mut first_bad = None;
            let mut good = 0;
            for el in &els {
                let map = cascade.computed(el);
                let got = value_of(&map, &prop);
                let font = map.get("font-size").and_then(|v| parse_px(v)).unwrap_or(16.0);
                let ctx = Ctx { font, viewport: width };
                let ok = match &got {
                    None => false,
                    Some(g) => {
                        let eq = |w: &str| norm(w, &ctx) == *g;
                        let num = parse_px(g);
                        equals.as_deref().is_none_or(eq)
                            && (one_of.is_empty() || one_of.iter().any(|w| eq(w)))
                            && min.is_none_or(|m| num.is_some_and(|n| n + 1e-6 >= m))
                            && max.is_none_or(|m| num.is_some_and(|n| n <= m + 1e-6))
                    }
                };
                if ok {
                    good += 1;
                } else if first_bad.is_none() {
                    first_bad = Some(format!("у {} сейчас {}", describe(el), got.map(|g| format!("`{}`", plain(&prop, &g))).unwrap_or_else(|| "не задано".into())));
                }
            }
            let ok = if *any { good > 0 } else { good == els.len() };
            Item { text, ok, detail: first_bad.unwrap_or_default() }
        }
        _ => return None,
    })
}

fn describe(el: &ElementRef) -> String {
    let v = el.value();
    let mut s = v.name().to_string();
    if let Some(id) = v.attr("id") {
        s = format!("{s}#{id}");
    }
    if let Some(c) = v.classes().next() {
        s = format!("{s}.{c}");
    }
    format!("`{s}`")
}

#[cfg(test)]
mod tests {
    use super::*;

    fn style(html: &str, css: &str, sel: &str, prop: &str) -> Option<String> {
        let doc = Doc::parse(html);
        let sheet = Stylesheet::parse(css);
        let c = Cascade { doc: &doc, sheet: &sheet, viewport: 1024.0 };
        let el = doc.select(sel).unwrap().into_iter().next().unwrap();
        value_of(&c.computed(&el), prop)
    }

    #[test]
    fn specificity_beats_order() {
        let css = "#a { color: red } .b { color: blue } p { color: green }";
        assert_eq!(style("<p id=a class=b>x</p>", css, "p", "color").as_deref(), Some("rgb(255, 0, 0)"));
        assert_eq!(style("<p class=b>x</p>", css, "p", "color").as_deref(), Some("rgb(0, 0, 255)"));
    }

    #[test]
    fn important_and_inline() {
        assert_eq!(style("<p style='color: blue'>x</p>", "p { color: red }", "p", "color").as_deref(), Some("rgb(0, 0, 255)"));
        assert_eq!(style("<p style='color: blue'>x</p>", "p { color: red !important }", "p", "color").as_deref(), Some("rgb(255, 0, 0)"));
    }

    #[test]
    fn inheritance_and_units() {
        let html = "<div><p>x</p></div>";
        assert_eq!(style(html, "div { color: #333; font-size: 20px } p { margin: 0.5em }", "p", "color").as_deref(), Some("rgb(51, 51, 51)"));
        assert_eq!(style(html, "div { font-size: 20px } p { margin: 0.5em }", "p", "margin").as_deref(), Some("10px"));
        assert_eq!(style(html, "p { padding: 1rem 2rem }", "p", "padding").as_deref(), Some("16px 32px"));
    }

    #[test]
    fn variables_and_shorthands() {
        let css = ":root { --gap: 12px; --c: #fff } .row { display: flex; gap: var(--gap); background: var(--c) }";
        let html = "<div class=row></div>";
        assert_eq!(style(html, css, ".row", "gap").as_deref(), Some("12px"));
        assert_eq!(style(html, css, ".row", "background-color").as_deref(), Some("rgb(255, 255, 255)"));
        assert_eq!(style(html, "div { flex: 1 }", "div", "flex-basis").as_deref(), Some("0%"));
        assert_eq!(style(html, "div { border: 2px solid red }", "div", "border-left-width").as_deref(), Some("2px"));
    }

    #[test]
    fn media_queries_follow_the_viewport() {
        assert!(media_matches("(min-width: 600px)", 800.0));
        assert!(!media_matches("(max-width: 500px)", 800.0));
        assert!(media_matches("screen and (min-width: 600px) and (max-width: 900px)", 800.0));
        let css = "p { color: red } @media (max-width: 500px) { p { color: blue } }";
        let doc = Doc::parse("<p>x</p>");
        let sheet = Stylesheet::parse(css);
        let el = doc.select("p").unwrap().into_iter().next().unwrap();
        let narrow = Cascade { doc: &doc, sheet: &sheet, viewport: 400.0 }.computed(&el);
        assert_eq!(narrow.get("color").map(String::as_str), Some("rgb(0, 0, 255)"));
    }

    #[test]
    fn syntax_problems_are_reported() {
        assert!(Stylesheet::parse("p { color: red }").errors.is_empty());
        assert!(!Stylesheet::parse("p { colr: red }").errors.is_empty());
        assert!(!Stylesheet::parse("p { color red }").errors.is_empty());
        assert!(!Stylesheet::parse("p { color: red ").errors.is_empty());
        assert!(!Stylesheet::parse("p color: red }").errors.is_empty());
    }
}
