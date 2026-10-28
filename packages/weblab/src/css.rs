//! Stylesheet parsing and the cascade: which property value an element gets (no layout: geometry is computed only by a browser).

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
    /// condition of the enclosing `@media`
    pub media: Option<String>,
    /// condition of the enclosing `@container` (applies only if the check set a container width)
    pub container: Option<String>,
}

#[derive(Debug, Default, Clone)]
pub struct Stylesheet {
    pub rules: Vec<Rule>,
    pub errors: Vec<String>,
    pub media: Vec<String>,
    /// `@container` conditions
    pub containers: Vec<String>,
    /// `@keyframes`: name and body
    pub keyframes: Vec<(String, String)>,
}

/// Properties we know exist: a typo like `colr` ends up among the parse errors.
const KNOWN: &str = "align-content align-items align-self all animation animation-delay animation-direction animation-duration animation-fill-mode animation-iteration-count animation-name animation-play-state animation-timing-function appearance aspect-ratio backdrop-filter backface-visibility background background-attachment background-clip background-color background-image background-origin background-position background-repeat background-size border border-bottom border-bottom-color border-bottom-left-radius border-bottom-right-radius border-bottom-style border-bottom-width border-collapse border-color border-image border-left border-left-color border-left-style border-left-width border-radius border-right border-right-color border-right-style border-right-width border-spacing border-style border-top border-top-color border-top-left-radius border-top-right-radius border-top-style border-top-width border-width bottom box-shadow box-sizing caption-side caret-color clear clip clip-path color column-count column-gap column-rule column-width columns content counter-increment counter-reset cursor direction display empty-cells fill filter flex flex-basis flex-direction flex-flow flex-grow flex-shrink flex-wrap float font font-family font-feature-settings font-kerning font-size font-size-adjust font-stretch font-style font-variant font-weight gap grid grid-area grid-auto-columns grid-auto-flow grid-auto-rows grid-column grid-column-end grid-column-gap grid-column-start grid-gap grid-row grid-row-end grid-row-gap grid-row-start grid-template grid-template-areas grid-template-columns grid-template-rows height hyphens image-rendering inline-size inset inset-block inset-inline isolation justify-content justify-items justify-self left letter-spacing line-height list-style list-style-image list-style-position list-style-type margin margin-block margin-bottom margin-inline margin-left margin-right margin-top mask max-height max-width max-inline-size min-height min-width min-inline-size mix-blend-mode object-fit object-position opacity order orphans outline outline-color outline-offset outline-style outline-width overflow overflow-wrap overflow-x overflow-y overscroll-behavior padding padding-block padding-bottom padding-inline padding-left padding-right padding-top page-break-after page-break-before page-break-inside perspective place-content place-items place-self pointer-events position quotes resize right rotate row-gap scale scroll-behavior scroll-margin scroll-padding scroll-snap-align scroll-snap-type shape-outside stroke stroke-width tab-size table-layout text-align text-align-last text-decoration text-decoration-color text-decoration-line text-decoration-style text-decoration-thickness text-indent text-overflow text-shadow text-transform text-underline-offset top touch-action transform transform-origin transform-style transition transition-delay transition-duration transition-property transition-timing-function translate unicode-bidi user-select container container-name container-type accent-color color-scheme text-wrap text-underline-position block-size min-block-size max-block-size margin-inline-start margin-inline-end margin-block-start margin-block-end padding-inline-start padding-inline-end padding-block-start padding-block-end inset-inline-start inset-inline-end inset-block-start inset-block-end border-start-start-radius border-start-end-radius border-end-start-radius border-end-end-radius transition-behavior animation-composition animation-timeline view-transition-name scroll-snap-stop overflow-clip-margin vertical-align visibility white-space widows width will-change word-break word-spacing word-wrap writing-mode z-index zoom";

/// States that depend on user actions: a rule with such a pseudo-class applies only if the check requested the state (`state`).
const DYNAMIC: &[&str] = &[
    "hover", "focus", "focus-visible", "focus-within", "active", "visited", "target", "placeholder-shown", "invalid", "valid", "user-invalid", "user-valid",
    "indeterminate", "in-range", "out-of-range", "default",
];
/// Pseudo-classes determined by the markup are replaced with attribute selectors.
const STATIC: &[(&str, &str)] = &[
    ("checked", "[checked]"), ("disabled", "[disabled]"), ("enabled", ":not([disabled])"), ("required", "[required]"), ("optional", ":not([required])"),
    ("link", "[href]"), ("any-link", "[href]"),
];
const PSEUDO_ELEMENTS: &[&str] = &["before", "after", "first-line", "first-letter", "marker", "placeholder", "selection", "backdrop", "file-selector-button", "cue"];

/// A rule selector split into parts: what element matching understands, the states and the pseudo-element.
pub struct SelectorParts {
    pub selector: scraper::Selector,
    pub states: Vec<String>,
    pub pseudo: Option<String>,
}

/// Parses a CSS selector: states (`:hover`, `:focus`…) and pseudo-elements (`::before`…) are extracted separately, the rest is parsed by the engine.
pub fn parse_selector(raw: &str) -> Result<SelectorParts, String> {
    let chars: Vec<char> = raw.trim().chars().collect();
    let (mut out, mut states, mut pseudo) = (String::new(), Vec::new(), None::<String>);
    let (mut i, mut brackets, mut parens, mut quote) = (0usize, 0i32, 0i32, None::<char>);
    while i < chars.len() {
        let c = chars[i];
        if let Some(q) = quote {
            out.push(c);
            if c == q {
                quote = None;
            }
            i += 1;
            continue;
        }
        match c {
            '"' | '\'' => {
                quote = Some(c);
                out.push(c);
                i += 1;
            }
            '[' => {
                brackets += 1;
                out.push(c);
                i += 1;
            }
            ']' => {
                brackets -= 1;
                out.push(c);
                i += 1;
            }
            '(' => {
                parens += 1;
                out.push(c);
                i += 1;
            }
            ')' => {
                parens -= 1;
                out.push(c);
                i += 1;
            }
            ':' if brackets == 0 && parens == 0 => {
                let double = chars.get(i + 1) == Some(&':');
                let start = i + if double { 2 } else { 1 };
                let mut end = start;
                while end < chars.len() && (chars[end].is_alphanumeric() || chars[end] == '-' || chars[end] == '_') {
                    end += 1;
                }
                let name: String = chars[start..end].iter().collect::<String>().to_lowercase();
                let functional = chars.get(end) == Some(&'(');
                if !functional && (double || matches!(name.as_str(), "before" | "after" | "first-line" | "first-letter")) {
                    if !PSEUDO_ELEMENTS.contains(&name.as_str()) {
                        return Err(i18n::trf!("pseudo-element ::{0} is not supported", name));
                    }
                    pseudo = Some(name);
                } else if !functional && DYNAMIC.contains(&name.as_str()) {
                    states.push(name);
                } else if let (false, Some((_, rep))) = (functional, STATIC.iter().find(|(n, _)| *n == name)) {
                    out.push_str(rep);
                } else {
                    out.extend(&chars[i..end]);
                }
                i = end;
            }
            _ => {
                out.push(c);
                i += 1;
            }
        }
    }
    let t = out.trim_end();
    if t.is_empty() || t.ends_with(['>', '+', '~', ',']) || out.ends_with(char::is_whitespace) {
        out = format!("{}{}*", out.trim_end(), if t.is_empty() { "" } else { " " });
    }
    let selector = selector(&out).map_err(|_| i18n::trf!("selector “{0}” could not be parsed", raw))?;
    Ok(SelectorParts { selector, states, pseudo })
}

/// Which states count as active when the check asks for `state`.
fn active_states(state: Option<&str>) -> Vec<String> {
    match state {
        None => vec![],
        Some("active") => vec!["hover".into(), "active".into()],
        Some("focus") | Some("focus-visible") => vec!["focus".into(), "focus-visible".into(), "focus-within".into()],
        Some(other) => vec![other.to_string()],
    }
}

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

/// Splits on a character outside brackets and quotes.
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

/// A `{ … }` block from the position after `{`: returns the contents and the position after the closing brace.
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
            errors.push(i18n::trf!("declaration “{0}” has no colon", part));
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
            errors.push(i18n::trf!("declaration “{0}” has no {1}", part, if prop.is_empty() { i18n::tr("property") } else { i18n::tr("a value") }));
            continue;
        }
        if !prop.starts_with("--") && !prop.starts_with('-') && !KNOWN.split(' ').any(|k| k == prop) {
            errors.push(i18n::trf!("unknown property `{0}`", prop));
        }
        out.push(Decl { prop, value, important });
    }
    out
}

impl Stylesheet {
    pub fn parse(src: &str) -> Stylesheet {
        let src: Vec<char> = strip_comments(src).chars().collect();
        let mut sheet = Stylesheet::default();
        sheet.parse_into(&src, None, None);
        sheet
    }

    fn parse_into(&mut self, chars: &[char], media: Option<&str>, container: Option<&str>) {
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
                    // `@import …;` and the like: ignored
                    if !head.starts_with('@') {
                        self.errors.push(i18n::trf!("“{0}” outside a rule", head));
                    }
                    i += 1;
                }
                Some('}') => {
                    self.errors.push(i18n::tr("extra closing `}`").into());
                    i += 1;
                }
                Some('{') => {
                    let Some((body, next)) = block(chars, i + 1) else {
                        self.errors.push(i18n::trf!("`{{` after “{0}” is not closed", head));
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
                                self.parse_into(&inner, Some(&cond), container);
                            }
                            "container" => {
                                let cond = at["container".len()..].trim().to_string();
                                self.containers.push(cond.clone());
                                let inner: Vec<char> = body.chars().collect();
                                self.parse_into(&inner, media, Some(&cond));
                            }
                            "supports" | "layer" => {
                                let inner: Vec<char> = body.chars().collect();
                                self.parse_into(&inner, media, container);
                            }
                            "keyframes" | "-webkit-keyframes" => {
                                let kf_name = at[name.len()..].trim().trim_matches(|c| c == '"' || c == '\'').to_string();
                                self.keyframes.push((kf_name, body.clone()));
                            }
                            _ => {} // font-face, …
                        }
                    } else {
                        if head.is_empty() {
                            self.errors.push(i18n::tr("rule without a selector").into());
                            continue;
                        }
                        let selectors: Vec<String> = split_outside(&head, ',').into_iter().map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect();
                        for s in &selectors {
                            if let Err(e) = parse_selector(s) {
                                self.errors.push(e);
                            }
                        }
                        let decls = parse_decls(&body, &mut self.errors);
                        self.rules.push(Rule { selectors, decls, media: media.map(String::from), container: container.map(String::from) });
                    }
                }
                _ => {
                    if !head.is_empty() {
                        self.errors.push(i18n::trf!("“{0}” is unfinished: no `{{`", head));
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

/// Whether the `@media` condition holds at viewport width `width`.
pub fn media_matches(cond: &str, width: f64) -> bool {
    media_matches_env(cond, width, &BTreeMap::new())
}

/// Default environment feature values (light scheme, normal motion, mouse, landscape orientation).
fn env_value<'a>(env: &'a BTreeMap<String, String>, key: &str) -> &'a str {
    env.get(key).map(String::as_str).unwrap_or(match key {
        "prefers-color-scheme" => "light",
        "prefers-reduced-motion" => "no-preference",
        "hover" => "hover",
        "pointer" => "fine",
        "orientation" => "landscape",
        _ => "",
    })
}

/// The same with a given environment (`prefers-color-scheme: dark`, `prefers-reduced-motion: reduce`, `hover: none`, `pointer: coarse`, `orientation: portrait`).
pub fn media_matches_env(cond: &str, width: f64, env: &BTreeMap<String, String>) -> bool {
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
                (f @ ("prefers-color-scheme" | "prefers-reduced-motion" | "hover" | "pointer" | "orientation"), _) => ok &= val.trim() == env_value(env, f),
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

// ---------- values ----------

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

/// Color as `rgb(r, g, b)` / `rgba(…)`, if it is a color.
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
    if let Some(args) = t.strip_prefix("hsla(").or_else(|| t.strip_prefix("hsl(")).and_then(|x| x.strip_suffix(')')) {
        let nums: Vec<f64> = args
            .split(|c: char| c == ',' || c == '/' || c.is_whitespace())
            .filter(|x| !x.is_empty())
            .map(|x| x.trim_end_matches("deg").trim_end_matches('%').parse::<f64>().unwrap_or(f64::NAN))
            .collect();
        if nums.len() < 3 || nums.iter().any(|n| n.is_nan()) {
            return None;
        }
        let (h, sat, light) = (nums[0].rem_euclid(360.0), (nums[1] / 100.0).clamp(0.0, 1.0), (nums[2] / 100.0).clamp(0.0, 1.0));
        let c = (1.0 - (2.0 * light - 1.0).abs()) * sat;
        let x = c * (1.0 - ((h / 60.0) % 2.0 - 1.0).abs());
        let m = light - c / 2.0;
        let (r, g, b) = match (h / 60.0) as u32 {
            0 => (c, x, 0.0),
            1 => (x, c, 0.0),
            2 => (0.0, c, x),
            3 => (0.0, x, c),
            4 => (x, 0.0, c),
            _ => (c, 0.0, x),
        };
        let a = nums.get(3).copied().map(|a| if args.trim_end().ends_with('%') { a / 100.0 } else { a }).unwrap_or(1.0);
        return Some(rgb_string(((r + m) * 255.0).round() as u8, ((g + m) * 255.0).round() as u8, ((b + m) * 255.0).round() as u8, a));
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

#[derive(Clone, Copy)]
struct Ctx {
    /// the element's font size in px (for `em`)
    font: f64,
    viewport: f64,
    /// unitless property (`order`, `flex-grow`, `z-index`…): `0` stays `0`
    unitless: bool,
}

/// Properties where a unitless number is a plain number, not a length.
fn is_unitless(prop: &str) -> bool {
    matches!(
        prop,
        "flex-grow" | "flex-shrink" | "order" | "z-index" | "opacity" | "line-height" | "font-weight" | "animation-iteration-count" | "column-count" | "zoom" | "aspect-ratio" | "tab-size"
            | "orphans" | "widows" | "scale"
    )
}

/// Number with a unit → px if the unit is known; otherwise the original token.
fn length(token: &str, ctx: &Ctx) -> String {
    let t = token.trim().to_lowercase();
    if t == "0" {
        return if ctx.unitless { "0".into() } else { "0px".into() };
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

// ---------- calc(), clamp(), min(), max() ----------

#[derive(Clone, Copy, Debug, PartialEq)]
enum Val {
    Len(f64),
    Num(f64),
}

struct Math<'a> {
    s: &'a [u8],
    i: usize,
    ctx: &'a Ctx,
}

impl Math<'_> {
    fn ws(&mut self) {
        while self.s.get(self.i).is_some_and(|c| c.is_ascii_whitespace()) {
            self.i += 1;
        }
    }

    fn eat(&mut self, c: u8) -> bool {
        self.ws();
        if self.s.get(self.i) == Some(&c) {
            self.i += 1;
            true
        } else {
            false
        }
    }

    fn sum(&mut self) -> Option<Val> {
        let mut acc = self.term()?;
        loop {
            self.ws();
            let op = match self.s.get(self.i) {
                Some(b'+') => b'+',
                Some(b'-') => b'-',
                _ => return Some(acc),
            };
            self.i += 1;
            let rhs = self.term()?;
            acc = match (acc, rhs) {
                (Val::Len(a), Val::Len(b)) => Val::Len(if op == b'+' { a + b } else { a - b }),
                (Val::Num(a), Val::Num(b)) => Val::Num(if op == b'+' { a + b } else { a - b }),
                _ => return None,
            };
        }
    }

    fn term(&mut self) -> Option<Val> {
        let mut acc = self.primary()?;
        loop {
            self.ws();
            let op = match self.s.get(self.i) {
                Some(b'*') => b'*',
                Some(b'/') => b'/',
                _ => return Some(acc),
            };
            self.i += 1;
            let rhs = self.primary()?;
            acc = match (op, acc, rhs) {
                (b'*', Val::Len(a), Val::Num(b)) | (b'*', Val::Num(b), Val::Len(a)) => Val::Len(a * b),
                (b'*', Val::Num(a), Val::Num(b)) => Val::Num(a * b),
                (b'/', Val::Len(a), Val::Num(b)) if b != 0.0 => Val::Len(a / b),
                (b'/', Val::Num(a), Val::Num(b)) if b != 0.0 => Val::Num(a / b),
                _ => return None,
            };
        }
    }

    fn args(&mut self, n: Option<usize>) -> Option<Vec<Val>> {
        if !self.eat(b'(') {
            return None;
        }
        let mut out = vec![self.sum()?];
        while self.eat(b',') {
            out.push(self.sum()?);
        }
        if !self.eat(b')') || n.is_some_and(|n| n != out.len()) {
            return None;
        }
        Some(out)
    }

    fn primary(&mut self) -> Option<Val> {
        self.ws();
        let rest = std::str::from_utf8(&self.s[self.i..]).ok()?;
        for name in ["calc", "clamp", "min", "max"] {
            if rest.starts_with(name) && rest[name.len()..].trim_start().starts_with('(') {
                self.i += name.len();
                let a = self.args(match name {
                    "calc" => Some(1),
                    "clamp" => Some(3),
                    _ => None,
                })?;
                let nums: Vec<f64> = a.iter().map(|v| match v { Val::Len(x) | Val::Num(x) => *x }).collect();
                let all_len = a.iter().all(|v| matches!(v, Val::Len(_)));
                let all_num = a.iter().all(|v| matches!(v, Val::Num(_)));
                if name != "calc" && !(all_len || all_num) {
                    return None;
                }
                let r = match name {
                    "calc" => return a.into_iter().next(),
                    "clamp" => nums[1].max(nums[0]).min(nums[2]),
                    "min" => nums.iter().cloned().fold(f64::INFINITY, f64::min),
                    _ => nums.iter().cloned().fold(f64::NEG_INFINITY, f64::max),
                };
                return Some(if all_len { Val::Len(r) } else { Val::Num(r) });
            }
        }
        if self.eat(b'(') {
            let v = self.sum()?;
            return if self.eat(b')') { Some(v) } else { None };
        }
        // number with an optional unit
        let start = self.i;
        if matches!(self.s.get(self.i), Some(b'+') | Some(b'-')) {
            self.i += 1;
        }
        while self.s.get(self.i).is_some_and(|c| c.is_ascii_digit() || *c == b'.') {
            self.i += 1;
        }
        let n: f64 = std::str::from_utf8(&self.s[start..self.i]).ok()?.parse().ok()?;
        let u = self.i;
        while self.s.get(self.i).is_some_and(|c| c.is_ascii_alphabetic() || *c == b'%') {
            self.i += 1;
        }
        let unit = std::str::from_utf8(&self.s[u..self.i]).ok()?;
        Some(match unit {
            "" => Val::Num(n),
            "px" => Val::Len(n),
            "rem" => Val::Len(n * 16.0),
            "em" => Val::Len(n * self.ctx.font),
            "vw" => Val::Len(n * self.ctx.viewport / 100.0),
            "pt" => Val::Len(n * 96.0 / 72.0),
            _ => return None, // %, vh, ch… cannot be computed without layout
        })
    }
}

/// Value of `calc()`/`clamp()`/`min()`/`max()` in px (or a number) if all terms are known without layout.
fn math_value(v: &str, ctx: &Ctx) -> Option<String> {
    let t = v.trim().to_lowercase();
    if !["calc(", "clamp(", "min(", "max("].iter().any(|f| t.starts_with(f)) {
        return None;
    }
    let mut m = Math { s: t.as_bytes(), i: 0, ctx };
    let r = m.sum()?;
    m.ws();
    if m.i != t.len() {
        return None;
    }
    Some(match r {
        Val::Len(x) => format!("{}px", fmt_num(x)),
        Val::Num(x) => fmt_num(x),
    })
}

/// Value in canonical form: colors as `rgb(…)`, lengths in px, case and whitespace normalized.
fn norm(value: &str, ctx: &Ctx) -> String {
    let v = value.trim();
    if let Some(m) = math_value(v, ctx) {
        return m;
    }
    if v.contains('(') && !v.to_lowercase().starts_with("rgb") && !v.to_lowercase().starts_with("hsl") && split_outside(v, ' ').len() == 1 {
        // functions (calc, var, url, repeat…): only whitespace is normalized
        return v.split_whitespace().collect::<Vec<_>>().join(" ").to_lowercase();
    }
    let tokens: Vec<String> = split_outside(v, ' ').into_iter().filter(|t| !t.trim().is_empty()).collect();
    let out: Vec<String> = tokens
        .iter()
        .map(|t| {
            if let Some(m) = math_value(t, ctx) {
                m
            } else if let Some(c) = color(t) {
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

// ---------- cascade ----------

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

fn is_time(t: &str) -> bool {
    let t = t.to_lowercase();
    (t.ends_with("ms") && t[..t.len() - 2].parse::<f64>().is_ok()) || (t.ends_with('s') && t[..t.len() - 1].parse::<f64>().is_ok())
}

fn is_timing(t: &str) -> bool {
    let t = t.to_lowercase();
    matches!(t.as_str(), "ease" | "linear" | "ease-in" | "ease-out" | "ease-in-out" | "step-start" | "step-end") || t.starts_with("cubic-bezier(") || t.starts_with("steps(")
}

fn is_style(t: &str) -> bool {
    matches!(t, "none" | "solid" | "dashed" | "dotted" | "double" | "groove" | "ridge" | "inset" | "outset" | "hidden")
}

/// Expands a shorthand property into its longhands.
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
        "background" => split_outside(v, ' ')
            .iter()
            .filter_map(|t| {
                let l = t.to_lowercase();
                if color(t).is_some() {
                    Some(("background-color".to_string(), t.clone()))
                } else if l.starts_with("url(") || l.contains("-gradient(") {
                    Some(("background-image".to_string(), t.clone()))
                } else {
                    None
                }
            })
            .collect(),
        "border-radius" => {
            let h = v.split('/').next().unwrap_or("").trim();
            let p: Vec<&str> = h.split_whitespace().collect();
            let (tl, tr, br, bl) = match p.len() {
                1 => (p[0], p[0], p[0], p[0]),
                2 => (p[0], p[1], p[0], p[1]),
                3 => (p[0], p[1], p[2], p[1]),
                4 => (p[0], p[1], p[2], p[3]),
                _ => return vec![],
            };
            vec![
                ("border-top-left-radius".into(), tl.into()),
                ("border-top-right-radius".into(), tr.into()),
                ("border-bottom-right-radius".into(), br.into()),
                ("border-bottom-left-radius".into(), bl.into()),
            ]
        }
        "place-items" | "place-content" | "place-self" => {
            let base = &prop["place-".len()..];
            let p: Vec<&str> = v.split_whitespace().collect();
            let (a, j) = match p.len() {
                1 => (p[0], p[0]),
                2 => (p[0], p[1]),
                _ => return vec![],
            };
            vec![(format!("align-{base}"), a.into()), (format!("justify-{base}"), j.into())]
        }
        "margin-inline" | "padding-inline" | "margin-block" | "padding-block" | "inset-inline" | "inset-block" => {
            let (kind, axis) = prop.rsplit_once('-').unwrap_or((prop, ""));
            let (a, b) = if axis == "inline" { ("left", "right") } else { ("top", "bottom") };
            let p: Vec<&str> = v.split_whitespace().collect();
            let (x, y) = match p.len() {
                1 => (p[0], p[0]),
                2 => (p[0], p[1]),
                _ => return vec![],
            };
            let name = |side: &str| if kind == "inset" { side.to_string() } else { format!("{kind}-{side}") };
            vec![(name(a), x.into()), (name(b), y.into())]
        }
        "margin-inline-start" | "margin-inline-end" | "padding-inline-start" | "padding-inline-end" | "margin-block-start" | "margin-block-end" | "padding-block-start" | "padding-block-end" => {
            let parts: Vec<&str> = prop.split('-').collect(); // margin, inline, start
            let side = match (parts[1], parts[2]) {
                ("inline", "start") => "left",
                ("inline", _) => "right",
                (_, "start") => "top",
                _ => "bottom",
            };
            vec![(format!("{}-{side}", parts[0]), v.into())]
        }
        "text-decoration" => {
            let (mut line, mut style, mut col) = (Vec::new(), "solid".to_string(), "currentcolor".to_string());
            for t in split_outside(v, ' ').iter().filter(|t| !t.is_empty()) {
                match t.to_lowercase().as_str() {
                    "underline" | "overline" | "line-through" | "none" => line.push(t.clone()),
                    "solid" | "double" | "dotted" | "dashed" | "wavy" => style = t.clone(),
                    _ => col = t.clone(),
                }
            }
            vec![("text-decoration-line".into(), if line.is_empty() { "none".into() } else { line.join(" ") }), ("text-decoration-style".into(), style), ("text-decoration-color".into(), col)]
        }
        "outline" => {
            let (mut w, mut st, mut c) = ("medium".to_string(), "none".to_string(), "currentcolor".to_string());
            for t in split_outside(v, ' ').iter().filter(|t| !t.is_empty()) {
                if is_style(&t.to_lowercase()) {
                    st = t.clone();
                } else if color(t).is_some() || t.eq_ignore_ascii_case("currentcolor") {
                    c = t.clone();
                } else {
                    w = t.clone();
                }
            }
            vec![("outline-width".into(), w), ("outline-style".into(), st), ("outline-color".into(), c)]
        }
        "font" => {
            let (mut style, mut weight, mut size, mut lh) = ("normal".to_string(), "normal".to_string(), String::new(), "normal".to_string());
            let toks: Vec<String> = split_outside(v, ' ').into_iter().filter(|t| !t.is_empty()).collect();
            let mut i = 0;
            while i < toks.len() {
                let t = toks[i].to_lowercase();
                let is_size = t.split('/').next().is_some_and(|h| h.starts_with(|c: char| c.is_ascii_digit() || c == '.') && h.trim_start_matches(|c: char| c.is_ascii_digit() || c == '.').len() > 0)
                    || matches!(t.as_str(), "small" | "medium" | "large" | "x-large" | "xx-large" | "x-small" | "xx-small" | "smaller" | "larger");
                if is_size {
                    let mut parts = toks[i].splitn(2, '/');
                    size = parts.next().unwrap_or("").to_string();
                    if let Some(l) = parts.next() {
                        lh = l.to_string();
                    }
                    i += 1;
                    break;
                }
                match t.as_str() {
                    "italic" | "oblique" => style = t,
                    "bold" | "bolder" | "lighter" => weight = t,
                    "normal" | "small-caps" => {}
                    n if n.parse::<u32>().is_ok() => weight = n.to_string(),
                    _ => {}
                }
                i += 1;
            }
            let family = toks[i.min(toks.len())..].join(" ");
            if size.is_empty() {
                return vec![];
            }
            let mut out = vec![("font-style".to_string(), style), ("font-weight".to_string(), weight), ("font-size".to_string(), size), ("line-height".to_string(), lh)];
            if !family.is_empty() {
                out.push(("font-family".to_string(), family));
            }
            out
        }
        "transition" => {
            let (mut props, mut durs, mut timings, mut delays) = (Vec::new(), Vec::new(), Vec::new(), Vec::new());
            for part in split_outside(v, ',') {
                let (mut prop_name, mut dur, mut delay, mut timing) = ("all".to_string(), None, None, "ease".to_string());
                for t in split_outside(&part, ' ').iter().map(|t| t.trim()).filter(|t| !t.is_empty()) {
                    if is_time(t) {
                        if dur.is_none() {
                            dur = Some(t.to_string());
                        } else {
                            delay = Some(t.to_string());
                        }
                    } else if is_timing(t) {
                        timing = t.to_string();
                    } else {
                        prop_name = t.to_string();
                    }
                }
                props.push(prop_name);
                durs.push(dur.unwrap_or_else(|| "0s".into()));
                timings.push(timing);
                delays.push(delay.unwrap_or_else(|| "0s".into()));
            }
            vec![
                ("transition-property".into(), props.join(", ")),
                ("transition-duration".into(), durs.join(", ")),
                ("transition-timing-function".into(), timings.join(", ")),
                ("transition-delay".into(), delays.join(", ")),
            ]
        }
        "animation" => {
            let mut cols: [Vec<String>; 8] = Default::default();
            for part in split_outside(v, ',') {
                let (mut name, mut dur, mut delay, mut timing, mut count, mut dir, mut fill, mut play) =
                    ("none".to_string(), None, None, "ease".to_string(), "1".to_string(), "normal".to_string(), "none".to_string(), "running".to_string());
                for t in split_outside(&part, ' ').iter().map(|t| t.trim()).filter(|t| !t.is_empty()) {
                    let l = t.to_lowercase();
                    if is_time(t) {
                        if dur.is_none() {
                            dur = Some(t.to_string());
                        } else {
                            delay = Some(t.to_string());
                        }
                    } else if is_timing(t) {
                        timing = t.to_string();
                    } else if l == "infinite" || l.parse::<f64>().is_ok() {
                        count = l;
                    } else if matches!(l.as_str(), "normal" | "reverse" | "alternate" | "alternate-reverse") {
                        dir = l;
                    } else if matches!(l.as_str(), "forwards" | "backwards" | "both") {
                        fill = l;
                    } else if matches!(l.as_str(), "running" | "paused") {
                        play = l;
                    } else {
                        name = t.to_string();
                    }
                }
                for (c, x) in cols.iter_mut().zip([name, dur.unwrap_or_else(|| "0s".into()), timing, delay.unwrap_or_else(|| "0s".into()), count, dir, fill, play]) {
                    c.push(x);
                }
            }
            ["animation-name", "animation-duration", "animation-timing-function", "animation-delay", "animation-iteration-count", "animation-direction", "animation-fill-mode", "animation-play-state"]
                .iter()
                .zip(cols.iter())
                .map(|(n, c)| (n.to_string(), c.join(", ")))
                .collect()
        }
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

/// Which longhands make up a shorthand (to check `margin` on all four sides).
fn parts_of(prop: &str) -> Option<Vec<String>> {
    let four = |p: &str, s: &str| ["top", "right", "bottom", "left"].iter().map(|x| format!("{p}-{x}{s}")).collect();
    Some(match prop {
        "margin" | "padding" => four(prop, ""),
        "border-width" => four("border", "-width"),
        "border-style" => four("border", "-style"),
        "border-color" => four("border", "-color"),
        "inset" => ["top", "right", "bottom", "left"].iter().map(|s| s.to_string()).collect(),
        "border-radius" => ["top-left", "top-right", "bottom-right", "bottom-left"].iter().map(|c| format!("border-{c}-radius")).collect(),
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
        "border-top-left-radius" | "border-top-right-radius" | "border-bottom-right-radius" | "border-bottom-left-radius" => "0px",
        "transition-property" => "all",
        "transition-duration" | "transition-delay" | "animation-duration" | "animation-delay" => "0s",
        "transition-timing-function" | "animation-timing-function" => "ease",
        "animation-name" => "none",
        "animation-iteration-count" => "1",
        "animation-direction" => "normal",
        "animation-fill-mode" => "none",
        "animation-play-state" => "running",
        "outline-style" => "none",
        "text-decoration-style" => "solid",
        _ => return None,
    })
}

/// User-agent styles for the tags that occur in the exercises.
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

/// Declaration priority: (important, origin, specificity, order). Origin: 0 — browser, 1 — author, 2 — the `style` attribute.
type Weight = (bool, u8, [u32; 3], usize);

pub struct Cascade<'a> {
    pub doc: &'a Doc,
    pub sheet: &'a Stylesheet,
    pub viewport: f64,
    /// the state in which styles are computed: `hover`, `focus`, `active`… (`None` — normal)
    pub state: Option<&'a str>,
    /// container width for `@container` rules (`None` — such rules do not apply)
    pub container: Option<f64>,
    /// environment features for `@media`: `prefers-color-scheme: dark`, `prefers-reduced-motion: reduce`… (empty — default values)
    pub env: &'a BTreeMap<String, String>,
}

impl Cascade<'_> {
    /// The element's declared values after the cascade, before inheritance and unit resolution, plus its custom properties.
    /// Whether the rule selector matches the element in the requested state and for the requested pseudo-element.
    fn applies(&self, raw: &str, el: &ElementRef, pseudo: Option<&str>) -> bool {
        let Ok(parts) = parse_selector(raw) else { return false };
        if parts.pseudo.as_deref() != pseudo {
            return false;
        }
        let active = active_states(self.state);
        parts.states.iter().all(|st| active.contains(st)) && parts.selector.matches(el)
    }

    fn declared(&self, el: &ElementRef, pseudo: Option<&str>, parent_customs: &BTreeMap<String, String>) -> (BTreeMap<String, (Weight, String)>, BTreeMap<String, String>) {
        let mut raw: Vec<(String, String, Weight)> = Vec::new();
        let mut order = 0usize;
        if pseudo.is_none() {
            for (p, v) in ua_style(el.value().name()) {
                order += 1;
                raw.push((p.into(), v.into(), (false, 0, [0; 3], order)));
            }
        }
        for rule in &self.sheet.rules {
            if let Some(m) = &rule.media {
                if !media_matches_env(m, self.viewport, self.env) {
                    continue;
                }
            }
            if let Some(c) = &rule.container {
                if !self.container.is_some_and(|w| media_matches_env(c, w, self.env)) {
                    continue;
                }
            }
            // for a rule with a selector list, the most specific matching selector counts
            let sp = rule.selectors.iter().filter(|s| self.applies(s, el, pseudo)).map(|s| specificity(s)).max();
            let Some(sp) = sp else { continue };
            for d in &rule.decls {
                order += 1;
                raw.push((d.prop.clone(), d.value.clone(), (d.important, 1u8, sp, order)));
            }
        }
        if let Some(style) = el.value().attr("style").filter(|_| pseudo.is_none()) {
            let mut ignore = Vec::new();
            for d in parse_decls(style, &mut ignore) {
                order += 1;
                raw.push((d.prop.clone(), d.value.clone(), (d.important, 2u8, [0; 3], order)));
            }
        }
        // custom properties: own ones win by priority, the rest are inherited
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

    /// Computed values of all known properties of the element (with inheritance, `var()` and units in px).
    pub fn computed(&self, el: &ElementRef) -> BTreeMap<String, String> {
        self.computed_for(el, None)
    }

    /// The same for a pseudo-element (`before`, `after`…): inherits from the element itself.
    pub fn computed_for(&self, el: &ElementRef, pseudo: Option<&str>) -> BTreeMap<String, String> {
        let parent = if pseudo.is_some() { Some(self.computed_for(el, None)) } else { el.parent().and_then(ElementRef::wrap).map(|p| self.computed_for(&p, None)) };
        let parent_customs: BTreeMap<String, String> = parent.as_ref().map(|p| p.iter().filter(|(k, _)| k.starts_with("--")).map(|(k, v)| (k.clone(), v.clone())).collect()).unwrap_or_default();
        let (declared, customs) = self.declared(el, pseudo, &parent_customs);
        let parent_font = parent.as_ref().and_then(|p| p.get("font-size")).and_then(|v| parse_px(v)).unwrap_or(16.0);
        let mut out: BTreeMap<String, String> = BTreeMap::new();
        let font_ctx = Ctx { font: parent_font, viewport: self.viewport, unitless: false };
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
                        // percentages are relative to the parent's font size
                        match n.strip_suffix('%').and_then(|x| x.parse::<f64>().ok()) {
                            Some(p) => parent_font * p / 100.0,
                            None => parse_px(&n).unwrap_or(parent_font),
                        }
                    }
                }
            }
            None => parent_font,
        };
        let ctx = Ctx { font: own_font, viewport: self.viewport, unitless: false };
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
                _ => Some(if prop == "font-size" { format!("{}px", fmt_num(own_font)) } else { norm(&raw, &Ctx { unitless: is_unitless(prop), ..ctx }) }),
            };
            if let Some(v) = value {
                out.insert(prop.clone(), v);
            }
        }
        // inherited properties the element lacks
        if let Some(p) = &parent {
            for (k, v) in p {
                if inherited(k) && !out.contains_key(k) {
                    out.insert(k.clone(), v.clone());
                }
            }
        }
        // `currentcolor` for the border and background color is the text color
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

/// Substitutes `var(--x, fallback)`.
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

/// Property value on an element; shorthands (`margin`, `gap`) are assembled from their longhands.
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

/// A CSS condition. `None` means the condition belongs to HTML.
/// `sheet` is all rules (from the task's `<style>` and the student's) for the cascade, `user` is only the student's rules for static conditions.
pub fn run(doc: &Doc, sheet: &Stylesheet, user: &Stylesheet, check: &Check, viewport: f64) -> Option<Item> {
    Some(match check {
        Check::CssValid => Item { text: i18n::tr("CSS without errors").into(), ok: user.errors.is_empty(), detail: user.errors.first().cloned().unwrap_or_default() },
        Check::NoImportant => Item { text: i18n::tr("No `!important`").into(), ok: !user.uses_important(), detail: i18n::tr("`!important` found").into() },
        Check::NoIds => Item { text: i18n::tr("No selectors by `#id`").into(), ok: !user.uses_ids(), detail: i18n::tr("an id selector was found").into() },
        Check::Uses { prop, value, msg } => {
            let p = prop.to_lowercase();
            let text = msg.clone().unwrap_or_else(|| match value {
                Some(v) => i18n::trf!("Uses `{0}: {1}`", p, v),
                None => i18n::trf!("Uses `{0}`", p),
            });
            let ctx0 = Ctx { font: 16.0, viewport: 1024.0, unitless: false };
            let same = |a: &str, b: &str| a.trim().eq_ignore_ascii_case(b.trim()) || norm(a, &ctx0) == norm(b, &ctx0);
            let ok = user.rules.iter().flat_map(|r| &r.decls).any(|d| d.prop == p && value.as_ref().is_none_or(|v| same(&d.value, v)));
            Item { text, ok, detail: i18n::tr("no such declaration in your CSS").into() }
        }
        Check::Keyframes { name, contains, msg } => {
            let text = msg.clone().unwrap_or_else(|| match contains {
                Some(c) => i18n::trf!("There is `@keyframes {0}` with `{1}`", name, c),
                None => i18n::trf!("There is `@keyframes {0}`", name),
            });
            let found = user.keyframes.iter().find(|(n, _)| n == name);
            let ok = found.is_some_and(|(_, body)| contains.as_ref().is_none_or(|c| body.to_lowercase().contains(&c.to_lowercase())));
            Item { text, ok, detail: if found.is_some() { i18n::tr("the required property is missing from the keyframes").into() } else { i18n::tr("no such animation (@keyframes) in your CSS").into() } }
        }
        Check::Container { contains, msg } => {
            let text = msg.clone().unwrap_or_else(|| i18n::trf!("There is `@container` with `{0}`", contains));
            let ok = user.containers.iter().any(|m| m.to_lowercase().contains(&contains.to_lowercase()));
            Item { text, ok, detail: i18n::tr("no `@container` rule with this condition").into() }
        }
        Check::Media { contains, msg } => {
            let text = msg.clone().unwrap_or_else(|| i18n::trf!("There is `@media` with `{0}`", contains));
            let ok = user.media.iter().any(|m| m.to_lowercase().contains(&contains.to_lowercase()));
            Item { text, ok, detail: i18n::tr("no `@media` rule with this condition").into() }
        }
        Check::Style { sel, prop, equals, one_of, min, max, any, viewport: vp, state, pseudo, container_width, env, contains, msg } => {
            let prop = prop.to_lowercase();
            let width = vp.unwrap_or(viewport);
            let want = equals.clone().or_else(|| (!one_of.is_empty()).then(|| one_of.join(" | "))).or_else(|| contains.as_ref().map(|c| i18n::trf!("contains “{0}”", c))).unwrap_or_else(|| match (min, max) {
                (Some(a), Some(b)) => i18n::trf!("from {0} to {1} px", fmt_num(*a), fmt_num(*b)),
                (Some(a), None) => i18n::trf!("at least {0} px", fmt_num(*a)),
                (None, Some(b)) => i18n::trf!("at most {0} px", fmt_num(*b)),
                _ => i18n::tr("set").into(),
            });
            let at = [
                vp.map(|_| i18n::trf!("at width {0}px", fmt_num(width))),
                state.as_ref().map(|st| i18n::trf!("in state :{0}", st)),
                container_width.map(|w| i18n::trf!("in container {0}px", fmt_num(w))),
                (!env.is_empty()).then(|| env.iter().map(|(k, v)| format!("{k}: {v}")).collect::<Vec<_>>().join(", ")),
            ]
            .into_iter()
            .flatten()
            .collect::<Vec<_>>()
            .join(", ");
            let at = if at.is_empty() { at } else { format!(" ({at})") };
            let target = pseudo.as_ref().map(|p| format!("{sel}::{p}")).unwrap_or_else(|| sel.clone());
            let text = msg.clone().unwrap_or_else(|| i18n::trf!("For `{0}` {1}: {2}{3}", target, prop, want, at));
            let els = match doc.select(sel) {
                Err(e) => return Some(Item { text, ok: false, detail: e }),
                Ok(v) if v.is_empty() => return Some(Item { text, ok: false, detail: i18n::tr("no such element in the markup").into() }),
                Ok(v) => v,
            };
            let cascade = Cascade { doc, sheet, viewport: width, state: state.as_deref(), container: *container_width, env };
            let mut first_bad = None;
            let mut good = 0;
            for el in &els {
                let map = cascade.computed_for(el, pseudo.as_deref());
                let got = value_of(&map, &prop);
                let font = map.get("font-size").and_then(|v| parse_px(v)).unwrap_or(16.0);
                let ctx = Ctx { font, viewport: width, unitless: is_unitless(&prop) };
                let ok = match &got {
                    None => false,
                    Some(g) => {
                        let eq = |w: &str| norm(w, &ctx) == *g;
                        let num = parse_px(g).or_else(|| g.trim().parse::<f64>().ok());
                        equals.as_deref().is_none_or(eq)
                            && contains.as_ref().is_none_or(|c| g.to_lowercase().contains(&c.to_lowercase()))
                            && (one_of.is_empty() || one_of.iter().any(|w| eq(w)))
                            && min.is_none_or(|m| num.is_some_and(|n| n + 1e-6 >= m))
                            && max.is_none_or(|m| num.is_some_and(|n| n <= m + 1e-6))
                    }
                };
                if ok {
                    good += 1;
                } else if first_bad.is_none() {
                    first_bad = Some(i18n::trf!("{0} currently has {1}", describe(el), got.map(|g| format!("`{}`", plain(&prop, &g))).unwrap_or_else(|| i18n::tr("not set").into())));
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
        let c = Cascade { doc: &doc, sheet: &sheet, viewport: 1024.0, state: None, container: None, env: &Default::default() };
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
        let narrow = Cascade { doc: &doc, sheet: &sheet, viewport: 400.0, state: None, container: None, env: &Default::default() }.computed(&el);
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

    fn style_in(html: &str, css: &str, sel: &str, prop: &str, state: Option<&str>, pseudo: Option<&str>, container: Option<f64>, viewport: f64) -> Option<String> {
        let doc = Doc::parse(html);
        let sheet = Stylesheet::parse(css);
        let c = Cascade { doc: &doc, sheet: &sheet, viewport, state, container, env: &Default::default() };
        let el = doc.select(sel).unwrap().into_iter().next().unwrap();
        value_of(&c.computed_for(&el, pseudo), prop)
    }

    #[test]
    fn state_pseudo_classes_apply_only_in_that_state() {
        let css = "a { color: blue } a:hover { color: red } a:focus-visible { outline: 2px solid green }";
        assert!(Stylesheet::parse(css).errors.is_empty(), "{:?}", Stylesheet::parse(css).errors);
        let html = "<a href=x>t</a>";
        assert_eq!(style_in(html, css, "a", "color", None, None, None, 1024.0).as_deref(), Some("rgb(0, 0, 255)"));
        assert_eq!(style_in(html, css, "a", "color", Some("hover"), None, None, 1024.0).as_deref(), Some("rgb(255, 0, 0)"));
        assert_eq!(style_in(html, css, "a", "outline-width", Some("focus"), None, None, 1024.0).as_deref(), Some("2px"));
        assert_eq!(style_in(html, css, "a", "outline-width", None, None, None, 1024.0), None, "rule does not apply without focus");
    }

    #[test]
    fn attribute_based_pseudo_classes_and_pseudo_elements() {
        let css = "input:checked + label { color: red } .card::before { content: \"→\"; color: blue } a:link { color: green }";
        assert!(Stylesheet::parse(css).errors.is_empty(), "{:?}", Stylesheet::parse(css).errors);
        let html = "<input type=checkbox checked><label>x</label><div class=card>c</div><a href=y>l</a>";
        assert_eq!(style_in(html, css, "label", "color", None, None, None, 1024.0).as_deref(), Some("rgb(255, 0, 0)"));
        assert_eq!(style_in(html, css, ".card", "content", None, None, None, 1024.0), None, "pseudo-element does not style the element itself");
        assert_eq!(style_in(html, css, ".card", "content", None, Some("before"), None, 1024.0).as_deref(), Some("\"→\""));
        assert_eq!(style_in(html, css, ".card", "color", None, Some("before"), None, 1024.0).as_deref(), Some("rgb(0, 0, 255)"));
        assert_eq!(style_in(html, css, "a", "color", None, None, None, 1024.0).as_deref(), Some("rgb(0, 128, 0)"));
        assert!(Stylesheet::parse("a::nonsense { color: red }").errors.len() == 1);
    }

    #[test]
    fn container_queries_follow_the_container_width() {
        let css = ".card { display: block } @container (min-width: 400px) { .card { display: flex } }";
        let html = "<div class=card></div>";
        assert_eq!(style_in(html, css, ".card", "display", None, None, None, 1024.0).as_deref(), Some("block"));
        assert_eq!(style_in(html, css, ".card", "display", None, None, Some(300.0), 1024.0).as_deref(), Some("block"));
        assert_eq!(style_in(html, css, ".card", "display", None, None, Some(500.0), 1024.0).as_deref(), Some("flex"));
        assert_eq!(Stylesheet::parse(css).containers, vec!["(min-width: 400px)".to_string()]);
    }

    #[test]
    fn transition_animation_font_and_other_shorthands() {
        let html = "<p class=a>x</p>";
        let g = |css: &str, prop: &str| style_in(html, css, ".a", prop, None, None, None, 1024.0);
        assert_eq!(g(".a { transition: color .3s ease-in, opacity 1s linear 0.5s }", "transition-property").as_deref(), Some("color, opacity"));
        assert_eq!(g(".a { transition: color .3s ease-in, opacity 1s linear 0.5s }", "transition-delay").as_deref(), Some("0s, 0.5s"));
        assert_eq!(g(".a { animation: spin 2s linear infinite }", "animation-name").as_deref(), Some("spin"));
        assert_eq!(g(".a { animation: spin 2s linear infinite }", "animation-iteration-count").as_deref(), Some("infinite"));
        assert_eq!(g(".a { place-items: center }", "align-items").as_deref(), Some("center"));
        assert_eq!(g(".a { place-items: center start }", "justify-items").as_deref(), Some("start"));
        assert_eq!(g(".a { font: italic bold 20px/1.5 Georgia, serif }", "font-size").as_deref(), Some("20px"));
        assert_eq!(g(".a { font: italic bold 20px/1.5 Georgia, serif }", "font-weight").as_deref(), Some("bold"));
        assert_eq!(g(".a { font: italic bold 20px/1.5 Georgia, serif }", "line-height").as_deref(), Some("1.5"));
        assert_eq!(g(".a { border-radius: 8px 4px }", "border-radius").as_deref(), Some("8px 4px"));
        assert_eq!(g(".a { border-radius: 50% }", "border-top-left-radius").as_deref(), Some("50%"));
        assert_eq!(g(".a { margin-inline: auto }", "margin-right").as_deref(), Some("auto"));
        assert_eq!(g(".a { padding-block: 8px 12px }", "padding-bottom").as_deref(), Some("12px"));
        assert_eq!(g(".a { text-decoration: underline wavy red }", "text-decoration-style").as_deref(), Some("wavy"));
        assert_eq!(g(".a { outline: 2px dashed blue }", "outline-style").as_deref(), Some("dashed"));
        assert_eq!(g(".a { background: url(a.png) #fff }", "background-image").as_deref(), Some("url(a.png)"));
    }

    #[test]
    fn calc_clamp_min_max_are_resolved_to_pixels() {
        let html = "<div class=a><p class=b>x</p></div>";
        let at = |css: &str, vp: f64| style_in(html, css, ".b", "font-size", None, None, None, vp);
        assert_eq!(at(".b { font-size: calc(1rem + 4px) }", 1024.0).as_deref(), Some("20px"));
        assert_eq!(at(".b { font-size: clamp(16px, 2vw, 32px) }", 1000.0).as_deref(), Some("20px"));
        assert_eq!(at(".b { font-size: clamp(16px, 2vw, 32px) }", 400.0).as_deref(), Some("16px"));
        assert_eq!(at(".b { font-size: clamp(16px, 2vw, 32px) }", 2000.0).as_deref(), Some("32px"));
        assert_eq!(at(".b { font-size: min(3rem, 40px) }", 1024.0).as_deref(), Some("40px"));
        assert_eq!(at(".b { font-size: max(1rem, calc(10px * 2)) }", 1024.0).as_deref(), Some("20px"));
        // percentages cannot be computed without layout — the value stays as written
        assert_eq!(style_in(html, ".b { width: calc(100% - 20px) }", ".b", "width", None, None, None, 800.0).as_deref(), Some("calc(100% - 20px)"));
    }

    #[test]
    fn keyframes_are_collected() {
        let sheet = Stylesheet::parse("@keyframes spin { from { transform: rotate(0) } to { transform: rotate(360deg) } } .a { animation: spin 1s }");
        assert!(sheet.errors.is_empty(), "{:?}", sheet.errors);
        assert_eq!(sheet.keyframes.len(), 1);
        assert_eq!(sheet.keyframes[0].0, "spin");
        assert!(sheet.keyframes[0].1.contains("rotate(360deg)"));
    }

    #[test]
    fn hsl_colors_and_unitless_zero() {
        assert_eq!(color("hsl(0, 100%, 50%)").as_deref(), Some("rgb(255, 0, 0)"));
        assert_eq!(color("hsl(120deg 100% 25%)").as_deref(), Some("rgb(0, 128, 0)"));
        assert_eq!(color("hsla(240, 100%, 50%, 0.5)").as_deref(), Some("rgba(0, 0, 255, 0.5)"));
        assert_eq!(color("hsl(200, 20%, 40%)").as_deref(), Some("rgb(82, 109, 122)"));
        let html = "<div class=a></div>";
        let g = |css: &str, prop: &str| style_in(html, css, ".a", prop, None, None, None, 1024.0);
        assert_eq!(g(".a { order: 0; margin-top: 0 }", "order").as_deref(), Some("0"));
        assert_eq!(g(".a { order: 0; margin-top: 0 }", "margin-top").as_deref(), Some("0px"));
        assert_eq!(g(".a { flex-grow: 0 }", "flex-grow").as_deref(), Some("0"));
    }

    #[test]
    fn media_environment_features() {
        let css = "p { color: black } @media (prefers-color-scheme: dark) { p { color: white } } @media (prefers-reduced-motion: reduce) { p { transition: none } }";
        let doc = Doc::parse("<p>x</p>");
        let sheet = Stylesheet::parse(css);
        let el = doc.select("p").unwrap().into_iter().next().unwrap();
        let light = Default::default();
        let dark: BTreeMap<String, String> = [("prefers-color-scheme".to_string(), "dark".to_string())].into();
        let reduce: BTreeMap<String, String> = [("prefers-reduced-motion".to_string(), "reduce".to_string())].into();
        let at = |env: &BTreeMap<String, String>, prop: &str| value_of(&Cascade { doc: &doc, sheet: &sheet, viewport: 1024.0, state: None, container: None, env }.computed(&el), prop);
        assert_eq!(at(&light, "color").as_deref(), Some("rgb(0, 0, 0)"));
        assert_eq!(at(&dark, "color").as_deref(), Some("rgb(255, 255, 255)"));
        assert_eq!(at(&reduce, "transition-property").as_deref(), Some("none"));
        assert!(media_matches_env("(hover: none)", 800.0, &[("hover".to_string(), "none".to_string())].into()));
        assert!(!media_matches_env("(hover: none)", 800.0, &Default::default()));
    }
}
