//! Перенос слайдов из выгрузки прежнего TypeScript-кода (`frontend/scripts/slides-export.mjs`): JSON-дерево слайда → типизированные
//! данные. Разовый инструмент: после переноса источником остаются данные и генераторы на Rust.

use anyhow::{anyhow, bail, Context, Result};
use content::{
    dsl,
    item::{Anchor, Channel, Dir, GateKind},
    slide::{Card, Cell as RowCell, Topic},
    Block, Chapter, Frame, Item, Lang, SceneSpec, Slide, Tone,
};
use serde_json::Value;

fn num(v: &Value, k: &str) -> Option<f64> {
    v.get(k).and_then(Value::as_f64)
}
fn req(v: &Value, k: &str) -> Result<f64> {
    num(v, k).ok_or_else(|| anyhow!("нет числа «{k}»"))
}
fn string(v: &Value, k: &str) -> Option<String> {
    match v.get(k)? {
        Value::String(s) => Some(s.clone()),
        Value::Number(n) => Some(n.to_string()),
        _ => None,
    }
}
fn flag(v: &Value, k: &str) -> bool {
    v.get(k).and_then(Value::as_bool).unwrap_or(false)
}

fn tone(v: &Value, key: &str) -> Result<Option<Tone>> {
    let Some(c) = v.get(key).and_then(Value::as_str) else { return Ok(None) };
    Ok(Some(match c {
        "m" => Tone::Muted,
        "g" => Tone::Green,
        "y" => Tone::Yellow,
        "r" => Tone::Red,
        "b" => Tone::Blue,
        "v" => Tone::Violet,
        "K" => Tone::Ink,
        "R" => Tone::SolidRed,
        "W" => Tone::Light,
        "n" => Tone::Outline,
        other => bail!("неизвестный цвет «{other}»"),
    }))
}

fn lang(v: &Value) -> Result<Lang> {
    Ok(match v.get("lang").and_then(Value::as_str) {
        None => Lang::Plain,
        Some("rs") => Lang::Rust,
        Some("c") => Lang::C,
        Some("asm") => Lang::Asm,
        Some("py") => Lang::Python,
        Some("sql") => Lang::Sql,
        Some("js") => Lang::Js,
        Some("css") => Lang::Css,
        Some(other) => bail!("неизвестный язык «{other}»"),
    })
}

/// `dash`: `true` — пунктир по умолчанию, строка или число — свой штрих.
fn dash(v: &Value) -> Option<String> {
    match v.get("dash")? {
        Value::Bool(true) => Some("3 3".into()),
        Value::String(s) => Some(s.clone()),
        Value::Number(n) => Some(n.to_string()),
        _ => None,
    }
}

fn indices(v: &Value, k: &str) -> Vec<usize> {
    match v.get(k) {
        Some(Value::Number(n)) => n.as_u64().map(|n| vec![n as usize]).unwrap_or_default(),
        Some(Value::Array(a)) => a.iter().filter_map(|x| x.as_u64().map(|n| n as usize)).collect(),
        _ => Vec::new(),
    }
}

/// Элемент кадра.
pub fn item(v: &Value) -> Result<Item> {
    let t = v.get("t").and_then(Value::as_str).ok_or_else(|| anyhow!("нет вида элемента"))?;
    let id = string(v, "id").ok_or_else(|| anyhow!("нет id"))?;
    let o = num(v, "o").unwrap_or(1.0);
    let s = num(v, "s").unwrap_or(1.0);
    let tn = tone(v, "c")?;
    let text = string(v, "text").unwrap_or_default();
    let sub = string(v, "sub");
    Ok(match t {
        "cell" => {
            let mut c = dsl::cell(id, req(v, "x")?, req(v, "y")?, text);
            c.w = num(v, "w").unwrap_or(30.0);
            c.h = num(v, "h").unwrap_or(26.0);
            c.size = num(v, "size").unwrap_or(11.0);
            c.sub_size = num(v, "subSize").unwrap_or(8.5);
            c.tone = tn.unwrap_or_default();
            c.sub = sub;
            c.dash = flag(v, "dash");
            c.text_color = string(v, "tc");
            c.o = o;
            c.s = s;
            c.into()
        }
        "dot" => {
            let mut d = dsl::dot(id, req(v, "x")?, req(v, "y")?, text);
            d.r = num(v, "r").unwrap_or(12.0);
            d.size = num(v, "size").unwrap_or(10.5);
            d.tone = tn.unwrap_or_default();
            d.sub = sub;
            d.dash = flag(v, "dash");
            d.text_color = string(v, "tc");
            d.o = o;
            d.s = s;
            d.into()
        }
        "lnode" => {
            let mut n = dsl::lnode(id, req(v, "x")?, req(v, "y")?, text);
            n.w = num(v, "w").unwrap_or(46.0);
            n.h = num(v, "h").unwrap_or(24.0);
            n.size = num(v, "size").unwrap_or(11.0);
            n.tone = tn.unwrap_or_default();
            n.nil = flag(v, "nil");
            n.sub = sub;
            n.o = o;
            n.s = s;
            n.into()
        }
        "text" => {
            let mut x = dsl::text(id, req(v, "x")?, req(v, "y")?, text);
            x.size = num(v, "size").unwrap_or(10.0);
            x.tone = tn;
            x.mono = flag(v, "mono");
            x.bold = flag(v, "bold");
            x.anchor = match v.get("anchor").and_then(Value::as_str) {
                Some("start") => Anchor::Start,
                Some("end") => Anchor::End,
                _ => Anchor::Middle,
            };
            x.o = o;
            x.s = s;
            x.into()
        }
        "ptr" => {
            let mut p = dsl::ptr(id, req(v, "x")?, req(v, "y")?, text);
            p.tone = tn.unwrap_or(Tone::Green);
            p.dir = if v.get("dir").and_then(Value::as_str) == Some("up") { Dir::Up } else { Dir::Down };
            p.size = num(v, "size").unwrap_or(9.5);
            p.o = o;
            p.s = s;
            p.into()
        }
        "line" => {
            let mut l = dsl::line(id, req(v, "x1")?, req(v, "y1")?, req(v, "x2")?, req(v, "y2")?);
            l.tone = tn.unwrap_or_default();
            l.arrow = flag(v, "arrow");
            l.dash = dash(v);
            l.bend = num(v, "bend").unwrap_or(0.0);
            l.width = num(v, "w").unwrap_or(1.6);
            l.o = o;
            l.s = s;
            l.into()
        }
        "box" => {
            let mut z = dsl::zone(id, req(v, "x")?, req(v, "y")?, num(v, "w").unwrap_or(100.0), num(v, "h").unwrap_or(40.0));
            z.tone = tn.unwrap_or(Tone::Outline);
            z.dash = flag(v, "dash");
            z.label = string(v, "lbl");
            z.o = o;
            z.s = s;
            z.into()
        }
        "path" => {
            let mut p = dsl::path(id, string(v, "d").ok_or_else(|| anyhow!("нет d"))?);
            p.tone = tn.unwrap_or(Tone::Green);
            p.width = num(v, "w").unwrap_or(2.0);
            p.dash = dash(v);
            p.fill = string(v, "fill");
            p.fill_opacity = num(v, "fillOpacity");
            p.draw = num(v, "draw");
            p.o = o;
            p.into()
        }
        "bar" => {
            let mut b = dsl::bar(id, req(v, "x")?, req(v, "y")?, num(v, "hh").unwrap_or(0.0));
            b.w = num(v, "w").unwrap_or(16.0);
            b.max = num(v, "max").unwrap_or(100.0);
            b.tone = tn.unwrap_or_default();
            b.text = string(v, "text");
            b.o = o;
            b.into()
        }
        "code" => {
            let lines: Vec<String> = v.get("lines").and_then(Value::as_array).ok_or_else(|| anyhow!("нет lines"))?.iter().map(|l| l.as_str().unwrap_or("").to_string()).collect();
            let mut c = dsl::code(lang(v)?, id, req(v, "x")?, req(v, "y")?, &[]);
            c.lines = lines;
            c.hl = indices(v, "hl");
            c.bad = indices(v, "bad");
            c.size = num(v, "size").unwrap_or(9.5);
            c.lh = num(v, "lh").unwrap_or(13.0);
            c.w = num(v, "w").unwrap_or(150.0);
            c.o = o;
            c.into()
        }
        "gate" => content::item::Gate {
            id,
            x: req(v, "x")?,
            y: req(v, "y")?,
            gate: match v.get("g").and_then(Value::as_str).unwrap_or("and") {
                "and" => GateKind::And,
                "nand" => GateKind::Nand,
                "or" => GateKind::Or,
                "nor" => GateKind::Nor,
                "xor" => GateKind::Xor,
                "xnor" => GateKind::Xnor,
                "not" => GateKind::Not,
                "buf" => GateKind::Buf,
                other => bail!("неизвестный вентиль «{other}»"),
            },
            tone: tn.unwrap_or_default(),
            text: string(v, "text"),
            size: num(v, "size").unwrap_or(8.5),
            sub,
            o,
            s,
            delay: 0.0,
        }
        .into(),
        "tr" => content::item::Transistor {
            id,
            x: req(v, "x")?,
            y: req(v, "y")?,
            channel: if v.get("kind").and_then(Value::as_str) == Some("p") { Channel::P } else { Channel::N },
            on: flag(v, "on"),
            tone: tn.unwrap_or_default(),
            sub,
            o,
            s,
            delay: 0.0,
        }
        .into(),
        "sw" => content::item::Switch { id, x: req(v, "x")?, y: req(v, "y")?, on: flag(v, "on"), tone: tn.unwrap_or_default(), sub, o, s, delay: 0.0 }.into(),
        "lamp" => content::item::Lamp { id, x: req(v, "x")?, y: req(v, "y")?, r: num(v, "r").unwrap_or(9.0), on: flag(v, "on"), tone: tn.unwrap_or_default(), sub, o, s, delay: 0.0 }.into(),
        other => bail!("неизвестный вид элемента «{other}»"),
    })
}

fn frame(v: &Value) -> Result<Frame> {
    let items = v.as_array().ok_or_else(|| anyhow!("кадр — не список"))?;
    items.iter().map(|i| item(i).with_context(|| format!("элемент {}", i.get("id").and_then(Value::as_str).unwrap_or("?")))).collect::<Result<Vec<_>>>().map(|v| Frame(v))
}

fn strings(v: &Value) -> Result<Vec<String>> {
    v.as_array().ok_or_else(|| anyhow!("не список строк"))?.iter().map(|s| s.as_str().map(String::from).ok_or_else(|| anyhow!("не строка"))).collect()
}

/// Сцена слайда; `given` — метки шагов из слайда (перекрывают метки сцены).
pub fn scene(v: &Value, given: Option<&Value>) -> Result<SceneSpec> {
    let mut spec = SceneSpec::new(&[], &[], vec![]);
    spec.labels = strings(&v["labels"])?;
    spec.captions = strings(&v["caption"])?;
    spec.frames = v["frames"].as_array().ok_or_else(|| anyhow!("нет frames"))?.iter().map(frame).collect::<Result<_>>()?;
    spec.base = v.get("base").filter(|b| !b.is_null()).map(frame).transpose()?.unwrap_or_default();
    let cues = given.filter(|g| !g.is_null()).or_else(|| v.get("cues").filter(|c| !c.is_null()));
    spec.cues = cues.map(|c| c.as_array().map(|a| a.iter().filter_map(Value::as_f64).collect()).ok_or_else(|| anyhow!("метки не списком"))).transpose()?;
    // ошибка авторов прежнего кода (2 сцены из 3199): меток не хватает или лишние — достраиваем шагом 8 с и обрезаем
    if let Some(c) = &mut spec.cues {
        let steps = spec.frames.len().saturating_sub(1);
        while c.len() < steps {
            let next = c.last().map_or(5.0, |l| l + 8.0);
            c.push(next);
        }
        c.truncate(steps);
    }
    // в прежнем коде под одним id мог меняться вид элемента (текст → указатель): там это просто смена рисунка, без плавного
    // перехода; в данных у каждого вида свой id (`id~вид`), иначе нельзя проверить сцену
    let mut first_kind: std::collections::HashMap<String, &'static str> = std::collections::HashMap::new();
    for it in spec.base.0.iter_mut().chain(spec.frames.iter_mut().flat_map(|f| f.0.iter_mut())) {
        let k = it.kind();
        let first = *first_kind.entry(it.id().to_string()).or_insert(k);
        if first != k {
            let renamed = format!("{}~{k}", it.id());
            it.set_id(renamed);
        }
    }
    spec.step_ms = num(v, "ms").map_or(2800, |m| m as u32);
    spec.height = num(v, "h").unwrap_or(170.0);
    Ok(spec)
}

/// Текст узла дерева: строка или цепочка строк и вставок кода (`s-path` → `` `код` ``).
fn text_of(n: &Value) -> Result<String> {
    match n {
        Value::Null => Ok(String::new()),
        Value::String(s) => Ok(s.clone()),
        Value::Array(a) => a.iter().map(text_of).collect::<Result<Vec<_>>>().map(|v| v.concat()),
        Value::Object(o) if o.get("tag").and_then(Value::as_str) == Some("span") && o.get("cls").and_then(Value::as_str).is_some_and(|c| c.starts_with("s-path")) => {
            Ok(format!("`{}`", text_of(o.get("children").unwrap_or(&Value::Null))?))
        }
        other => bail!("в тексте неожиданный узел: {other}"),
    }
}

fn children(n: &Value) -> &[Value] {
    n.get("children").and_then(Value::as_array).map_or(&[], Vec::as_slice)
}
fn cls(n: &Value) -> &str {
    n.get("cls").and_then(Value::as_str).unwrap_or("")
}

fn card(n: &Value) -> Result<Card> {
    Ok(Card {
        title: text_of(&n["title"])?,
        sub: n.get("sub").filter(|s| !s.is_null()).map(text_of).transpose()?,
        kind: n.get("kind").and_then(Value::as_str).unwrap_or("").trim().to_string(),
        mono: flag(n, "mono"),
    })
}

/// Сцена, написанная генератором на Rust вместо ручной отрисовки React: по имени прежнего компонента (`ShapesIntro`) отдаёт её описание.
pub type Resolver<'a> = &'a dyn Fn(&str) -> Option<SceneSpec>;

fn block(n: &Value, resolve: Resolver) -> Result<Block> {
    if n.get("scene").is_some() {
        return Ok(Block::Scene(scene(&n["scene"], n.get("cues"))?));
    }
    if let Some(name) = n.get("comp").and_then(Value::as_str) {
        let mut spec = resolve(name).ok_or_else(|| anyhow!("сцена ручной отрисовки «{name}» ещё не переписана в генератор"))?;
        if let Some(c) = n.get("cues").filter(|c| !c.is_null()).and_then(Value::as_array) {
            spec.cues = Some(c.iter().filter_map(Value::as_f64).collect());
        }
        return Ok(Block::Scene(spec));
    }
    if let Some(w) = n.get("widget").and_then(Value::as_str) {
        return Ok(match w {
            "pycode" => Block::Code { lang: Lang::Python, text: text_of(&n["text"])? },
            "rscode" => Block::Code { lang: Lang::Rust, text: text_of(&n["text"])? },
            "cmd" => Block::Cmd { text: text_of(&n["text"])? },
            other => bail!("виджет «{other}» вне ряда карточек"),
        });
    }
    let text = || text_of(n.get("children").unwrap_or(&Value::Null));
    Ok(match (n.get("tag").and_then(Value::as_str), cls(n)) {
        (Some("div"), "s-note") => Block::Note { text: text()? },
        (Some("div"), "s-label") => Block::Label { text: text()? },
        (Some("p"), "s-hint") => Block::Hint { text: text()? },
        (Some("div"), "s-grid2") if children(n).iter().all(|c| c.get("widget").and_then(Value::as_str) == Some("node")) => Block::Grid { cards: children(n).iter().map(card).collect::<Result<_>>()? },
        (Some("div"), "s-grid2") => Block::Topics {
            items: children(n)
                .iter()
                .map(|t| {
                    let spans: Vec<&Value> = children(t).iter().filter(|c| cls(c) != "s-divider").collect();
                    let [big, title, sub] = spans[..] else { bail!("тема: ждали 3 надписи, есть {}", spans.len()) };
                    Ok(Topic { big: text_of(&big["children"])?, title: text_of(&title["children"])?, sub: text_of(&sub["children"])? })
                })
                .collect::<Result<_>>()?,
        },
        (Some("div"), "s-cols") => Block::Cols {
            cells: children(n)
                .iter()
                .map(|c| match c.get("widget").and_then(Value::as_str) {
                    Some("node") => Ok(RowCell::Card(card(c)?)),
                    Some("arr") => Ok(RowCell::Arrow),
                    _ => bail!("в ряду карточек неожиданный узел: {c}"),
                })
                .collect::<Result<_>>()?,
        },
        (Some("div"), "s-table") => Block::Table {
            rows: children(n)
                .iter()
                .map(|r| {
                    let [l, rt] = children(r) else { bail!("строка таблицы: ждали 2 ячейки") };
                    Ok((text_of(&l["children"])?, text_of(&rt["children"])?))
                })
                .collect::<Result<_>>()?,
        },
        (tag, c) => bail!("неизвестный блок <{tag:?} class=\"{c}\">"),
    })
}

/// Глава из выгрузки; `Err` — перечень причин (по слайдам).
pub fn chapter(key: &str, doc: &Value, resolve: Resolver) -> Result<Chapter> {
    let (book, num) = key.split_once(':').ok_or_else(|| anyhow!("ключ «{key}»"))?;
    let slides = doc["slides"].as_array().ok_or_else(|| anyhow!("нет slides"))?;
    let rubric = slides.first().and_then(|s| s["rubric"].as_str()).ok_or_else(|| anyhow!("нет рубрики"))?.to_string();
    let mut out = Vec::new();
    let mut problems = Vec::new();
    for (i, s) in slides.iter().enumerate() {
        let body = match &s["body"] {
            Value::Array(a) => a.clone(),
            Value::Null => Vec::new(),
            other => vec![other.clone()],
        };
        let blocks: Result<Vec<Block>> = body.iter().map(|b| block(b, resolve)).collect();
        match blocks {
            Ok(body) => out.push(Slide {
                title: text_of(&s["title"]).unwrap_or_default(),
                sub: s.get("sub").filter(|x| !x.is_null()).and_then(|x| text_of(x).ok()),
                short: s.get("short").and_then(Value::as_str).map(String::from),
                main: text_of(&s["main"]).unwrap_or_default(),
                body,
            }),
            Err(e) => problems.push(format!("слайд {}: {e:#}", i + 1)),
        }
    }
    if !problems.is_empty() {
        bail!("{}", problems.join("; "));
    }
    Ok(Chapter { book: book.parse()?, chapter: num.parse()?, rubric, slides: out })
}
