//! Структурные проверки разметки.

use std::collections::HashMap;

use ego_tree::NodeId;
use scraper::{ElementRef, Html, Selector};

use crate::spec::{Check, Item};

/// Разобранный документ с порядком узлов.
pub struct Doc {
    pub html: Html,
    source: String,
    order: HashMap<NodeId, usize>,
}

impl Doc {
    pub fn parse(source: &str) -> Doc {
        let html = Html::parse_document(source);
        let order = html.tree.root().descendants().enumerate().map(|(i, n)| (n.id(), i)).collect();
        Doc { html, source: source.to_string(), order }
    }

    /// Фрагмент разбирается как документ: `html`, `head`, `body` добавляет сам разбор.
    pub fn parse_errors(&self) -> Vec<String> {
        // без doctype разбор всегда жалуется («Unexpected token»): для проверки на ошибки добавляем его сами
        if !self.has_doctype() {
            return Html::parse_document(&format!("<!doctype html>{}", self.source)).errors.iter().map(|e| e.to_string()).collect();
        }
        self.html.errors.iter().map(|e| e.to_string()).collect()
    }

    /// Документ начинается с `<!doctype html>` (регистр не важен).
    pub fn has_doctype(&self) -> bool {
        let t = self.source.trim_start().to_lowercase();
        t.starts_with("<!doctype html")
    }

    pub fn select<'a>(&'a self, sel: &str) -> Result<Vec<ElementRef<'a>>, String> {
        let s = selector(sel)?;
        Ok(self.html.select(&s).collect())
    }

    /// Стили, которые уже есть в документе (`<style>`): исходные правила задания, поверх которых работает ученик.
    pub fn style_text(&self) -> String {
        self.select("style").unwrap_or_default().iter().map(|e| e.text().collect::<String>()).collect::<Vec<_>>().join("\n")
    }

    pub fn position(&self, el: &ElementRef) -> usize {
        self.order.get(&el.id()).copied().unwrap_or(usize::MAX)
    }
}

pub fn selector(sel: &str) -> Result<Selector, String> {
    Selector::parse(sel).map_err(|_| format!("селектор «{sel}» не разобран"))
}

/// Текст элемента: пробельные символы схлопнуты, края обрезаны.
pub fn text_of(el: &ElementRef) -> String {
    el.text().collect::<Vec<_>>().join(" ").split_whitespace().collect::<Vec<_>>().join(" ")
}

fn lower(s: &str) -> String {
    s.to_lowercase()
}

fn item(text: String, ok: bool, detail: impl Into<String>) -> Item {
    Item { text, ok, detail: if ok { String::new() } else { detail.into() } }
}

fn named(msg: &Option<String>, auto: String) -> String {
    msg.clone().unwrap_or(auto)
}

fn plural(n: usize) -> &'static str {
    match (n % 10, n % 100) {
        (_, 11..=14) => "элементов",
        (1, _) => "элемент",
        (2..=4, _) => "элемента",
        _ => "элементов",
    }
}

/// Проверка HTML-условия. `None` — условие относится к CSS.
pub fn run(doc: &Doc, check: &Check) -> Option<Item> {
    Some(match check {
        Check::Exists { sel, min, max, msg } => {
            let text = named(msg, match max {
                Some(m) if m == min => format!("Ровно {min} {} `{sel}`", plural(*min)),
                Some(m) => format!("От {min} до {m} {} `{sel}`", plural(*m)),
                None => format!("Есть `{sel}`{}", if *min > 1 { format!(" (не меньше {min})") } else { String::new() }),
            });
            match doc.select(sel) {
                Err(e) => item(text, false, e),
                Ok(v) => {
                    let n = v.len();
                    let ok = n >= *min && max.is_none_or(|m| n <= m);
                    item(text, ok, format!("найдено {n} {}", plural(n)))
                }
            }
        }
        Check::Count { sel, n, msg } => {
            let text = named(msg, format!("{n} {} `{sel}`", plural(*n)));
            match doc.select(sel) {
                Err(e) => item(text, false, e),
                Ok(v) => item(text, v.len() == *n, format!("найдено {}", v.len())),
            }
        }
        Check::Text { sel, equals, contains, msg } => {
            let want = equals.as_ref().or(contains.as_ref()).cloned().unwrap_or_default();
            let text = named(msg, if equals.is_some() { format!("`{sel}` с текстом «{want}»") } else { format!("`{sel}` с текстом, содержащим «{want}»") });
            match doc.select(sel) {
                Err(e) => item(text, false, e),
                Ok(v) if v.is_empty() => item(text, false, "такого элемента нет"),
                Ok(v) => {
                    let ok = v.iter().any(|el| {
                        let t = lower(&text_of(el));
                        match (equals, contains) {
                            (Some(e), _) => t == lower(e.trim()),
                            (None, Some(c)) => t.contains(&lower(c.trim())),
                            _ => true,
                        }
                    });
                    let got = v.first().map(text_of).unwrap_or_default();
                    item(text, ok, format!("сейчас: «{got}»"))
                }
            }
        }
        Check::Attr { sel, name, present, equals, contains, all, msg } => {
            let what = match (present, equals, contains) {
                (Some(false), _, _) => format!("без атрибута `{name}`"),
                (_, Some(e), _) => format!("с `{name}=\"{e}\"`"),
                (_, _, Some(c)) => format!("с `{name}`, содержащим «{c}»"),
                _ => format!("с атрибутом `{name}`"),
            };
            let text = named(msg, format!("{} `{sel}` {what}", if *all { "Каждый" } else { "Есть" }));
            match doc.select(sel) {
                Err(e) => item(text, false, e),
                Ok(v) if v.is_empty() => item(text, false, "такого элемента нет"),
                Ok(v) => {
                    let good = |el: &ElementRef| -> bool {
                        let val = el.value().attr(name);
                        match (present, equals, contains) {
                            (Some(false), _, _) => val.is_none(),
                            (_, Some(e), _) => val.is_some_and(|x| lower(x.trim()) == lower(e.trim())),
                            (_, _, Some(c)) => val.is_some_and(|x| lower(x).contains(&lower(c))),
                            _ => val.is_some_and(|x| !x.trim().is_empty() || present == &Some(true)),
                        }
                    };
                    let hits = v.iter().filter(|e| good(e)).count();
                    let ok = if *all { hits == v.len() } else { hits > 0 };
                    item(text, ok, format!("подходит {hits} из {}", v.len()))
                }
            }
        }
        Check::Child { parent, child, direct, msg } => {
            let sel = if *direct { format!("{parent} > {child}") } else { format!("{parent} {child}") };
            let text = named(msg, format!("`{child}` {} `{parent}`", if *direct { "прямо внутри" } else { "внутри" }));
            match doc.select(&sel) {
                Err(e) => item(text, false, e),
                Ok(v) => item(text, !v.is_empty(), "такой вложенности нет"),
            }
        }
        Check::Order { before, after, msg } => {
            let text = named(msg, format!("`{before}` идёт раньше `{after}`"));
            match (doc.select(before), doc.select(after)) {
                (Err(e), _) | (_, Err(e)) => item(text, false, e),
                (Ok(a), Ok(b)) => match (a.first(), b.first()) {
                    (Some(a), Some(b)) => item(text, doc.position(a) < doc.position(b), "порядок обратный"),
                    _ => item(text, false, "одного из элементов нет"),
                },
            }
        }
        Check::Forbid { sel, msg } => {
            let text = named(msg, format!("Нет `{sel}`"));
            match doc.select(sel) {
                Err(e) => item(text, false, e),
                Ok(v) => item(text, v.is_empty(), format!("найдено {}", v.len())),
            }
        }
        Check::Doctype => item("Документ начинается с `<!doctype html>`".into(), doc.has_doctype(), "объявления типа документа нет — браузер включит режим совместимости"),
        Check::Headings => headings(doc),
        Check::Labels => labels(doc),
        Check::ImgAlt => {
            let text = "У каждой картинки есть `alt`".to_string();
            let v = doc.select("img").unwrap_or_default();
            let bad = v.iter().filter(|e| e.value().attr("alt").is_none()).count();
            item(text, bad == 0, format!("без `alt`: {bad}"))
        }
        Check::CleanParse => {
            let errs = doc.parse_errors();
            // эти замечания есть у любого фрагмента без doctype и не говорят об ошибке ученика
            let real: Vec<&String> = errs.iter().filter(|e| !e.contains("doctype") && !e.contains("DOCTYPE")).collect();
            item("Разметка без ошибок разбора".into(), real.is_empty(), real.first().map(|s| s.to_string()).unwrap_or_default())
        }
        _ => return None,
    })
}

fn headings(doc: &Doc) -> Item {
    let text = "Один `h1`, заголовки идут по уровням без пропусков".to_string();
    let mut levels: Vec<(usize, u8)> = Vec::new();
    for el in doc.html.tree.root().descendants().filter_map(ElementRef::wrap) {
        let n = el.value().name();
        if let [b'h', d @ b'1'..=b'6'] = n.as_bytes() {
            levels.push((doc.position(&el), d - b'0'));
        }
    }
    levels.sort();
    let h1 = levels.iter().filter(|(_, l)| *l == 1).count();
    if h1 != 1 {
        return item(text, false, format!("`h1` должен быть один, сейчас {h1}"));
    }
    let mut prev = 0u8;
    for (_, l) in &levels {
        if *l > prev + 1 {
            return item(text, false, format!("после `h{prev}` сразу `h{l}`"));
        }
        prev = *l;
    }
    item(text, true, "")
}

fn labels(doc: &Doc) -> Item {
    let text = "У каждого поля есть подпись".to_string();
    let fields = doc.select("input, select, textarea").unwrap_or_default();
    let mut bad = Vec::new();
    for f in fields {
        let v = f.value();
        if v.name() == "input" && matches!(v.attr("type").map(str::to_lowercase).as_deref(), Some("hidden" | "submit" | "button" | "reset" | "image")) {
            continue;
        }
        let aria = v.attr("aria-label").is_some_and(|s| !s.trim().is_empty()) || v.attr("aria-labelledby").is_some_and(|s| !s.trim().is_empty());
        let wrapped = f.ancestors().filter_map(ElementRef::wrap).any(|a| a.value().name() == "label");
        let by_for = v.attr("id").is_some_and(|id| {
            !id.is_empty() && doc.select("label[for]").unwrap_or_default().iter().any(|l| l.value().attr("for") == Some(id))
        });
        if !(aria || wrapped || by_for) {
            bad.push(v.attr("name").or(v.attr("id")).unwrap_or(v.name()).to_string());
        }
    }
    item(text, bad.is_empty(), format!("без подписи: {}", bad.join(", ")))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::spec::{Check, Kind, Solution, Task};
    use crate::verify::verify;

    fn html_task(checks: Vec<Check>) -> Task {
        Task { kind: Kind::Html, html: String::new(), starter_html: String::new(), starter_css: String::new(), viewport: 1024.0, checks, want: vec![], max_specificity: None, reference: None }
    }

    fn run_all(html: &str, checks: Vec<Check>) -> Vec<(String, bool)> {
        verify(&html_task(checks), &Solution { html: html.into(), css: String::new() }).items.into_iter().map(|i| (i.text, i.ok)).collect()
    }

    fn all_ok(html: &str, check: Check) -> bool {
        run_all(html, vec![check]).iter().all(|(_, ok)| *ok)
    }

    #[test]
    fn structure_checks() {
        let page = "<!doctype html><html><body><header><h1>Сайт</h1></header><main><h2>Раздел</h2><ul><li>а</li><li>б</li></ul><a href='/x' class='go'>Дальше</a></main></body></html>";
        assert!(all_ok(page, Check::Exists { sel: "main > h2".into(), min: 1, max: None, msg: None }));
        assert!(all_ok(page, Check::Exists { sel: "li".into(), min: 2, max: Some(2), msg: None }));
        assert!(!all_ok(page, Check::Exists { sel: "li".into(), min: 3, max: None, msg: None }));
        assert!(all_ok(page, Check::Text { sel: "h1".into(), equals: Some("сайт".into()), contains: None, msg: None }));
        assert!(all_ok(page, Check::Attr { sel: "a".into(), name: "href".into(), present: None, equals: Some("/x".into()), contains: None, all: true, msg: None }));
        assert!(all_ok(page, Check::Child { parent: "main".into(), child: "li".into(), direct: false, msg: None }));
        assert!(!all_ok(page, Check::Child { parent: "main".into(), child: "li".into(), direct: true, msg: None }));
        assert!(all_ok(page, Check::Order { before: "header".into(), after: "main".into(), msg: None }));
        assert!(!all_ok(page, Check::Order { before: "main".into(), after: "header".into(), msg: None }));
        assert!(all_ok(page, Check::Forbid { sel: "table".into(), msg: None }));
        assert!(all_ok(page, Check::Headings));
        assert!(all_ok(page, Check::CleanParse));
    }

    #[test]
    fn headings_need_one_h1_and_no_gaps() {
        assert!(!all_ok("<h1>a</h1><h3>b</h3>", Check::Headings));
        assert!(!all_ok("<h1>a</h1><h1>b</h1>", Check::Headings));
        assert!(!all_ok("<h2>a</h2>", Check::Headings));
        assert!(all_ok("<h1>a</h1><h2>b</h2><h3>c</h3><h2>d</h2>", Check::Headings));
    }

    #[test]
    fn fields_need_labels() {
        assert!(all_ok("<label for=a>Имя</label><input id=a>", Check::Labels));
        assert!(all_ok("<label>Имя <input></label>", Check::Labels));
        assert!(all_ok("<input aria-label='Поиск'>", Check::Labels));
        assert!(all_ok("<input type=hidden name=t><input type=submit>", Check::Labels));
        assert!(!all_ok("<input name=a>", Check::Labels));
        assert!(!all_ok("<label for=x>Имя</label><input id=a>", Check::Labels));
    }

    #[test]
    fn doctype_and_clean_parse() {
        assert!(all_ok("<!DOCTYPE html><title>t</title><p>x</p>", Check::Doctype));
        assert!(!all_ok("<p>x</p>", Check::Doctype));
        // у фрагмента без doctype ошибок разбора нет, пока теги вложены верно
        assert!(all_ok("<title>t</title><p>x</p>", Check::CleanParse));
        assert!(!all_ok("<div><span></div>", Check::CleanParse));
    }

    #[test]
    fn images_need_alt() {
        assert!(all_ok("<img src=a.png alt=''>", Check::ImgAlt));
        assert!(!all_ok("<img src=a.png>", Check::ImgAlt));
    }

    #[test]
    fn bad_selectors_are_reported_not_panicked() {
        let r = run_all("<p>x</p>", vec![Check::Exists { sel: "p[".into(), min: 1, max: None, msg: None }]);
        assert!(!r[0].1);
    }
}
