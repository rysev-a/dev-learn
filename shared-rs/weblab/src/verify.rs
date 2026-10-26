//! Проверка решения: задание + присланный текст → отчёт.

use crate::css::{self, Stylesheet};
use crate::html::{self, Doc};
use crate::selector::{check_selector, has_id};
use crate::spec::{Check, Item, Kind, Report, Solution, Task};

/// Условия, которые заданы данными, и условия «по умолчанию» для вида упражнения.
pub fn verify(task: &Task, solution: &Solution) -> Report {
    let mut items = Vec::new();
    match task.kind {
        Kind::Html => {
            let doc = Doc::parse(&solution.html);
            items.extend(task.checks.iter().filter_map(|c| html::run(&doc, c)));
        }
        Kind::Css => {
            let doc = Doc::parse(&task.html);
            // правила из `<style>` задания идут раньше правил ученика
            let user = Stylesheet::parse(&solution.css);
            let sheet = Stylesheet::parse(&format!("{}\n{}", doc.style_text(), solution.css));
            items.extend(task.checks.iter().filter_map(|c| css::run(&doc, &sheet, &user, c, task.viewport)));
        }
        Kind::Selector => {
            items.extend(check_selector(task, &solution.css));
            // из условий для текста селектора имеют смысл только «без #id»
            for c in &task.checks {
                if matches!(c, Check::NoIds) {
                    items.push(Item { text: "Без селекторов по `#id`".into(), ok: !has_id(&solution.css), detail: "найден селектор по идентификатору".into() });
                }
            }
        }
    }
    // пустой редактор не решает задачу, даже если все условия — «чего-то нет»
    let empty = match task.kind {
        Kind::Html => solution.html.trim().is_empty(),
        Kind::Css | Kind::Selector => solution.css.trim().is_empty(),
    };
    if empty {
        items.push(Item { text: "Решение написано".into(), ok: false, detail: "редактор пуст".into() });
    }
    Report { items }
}

/// Проверка данных задания (для тестов и сида): условия заданы корректно, эталон проходит, заготовка — нет.
pub fn self_check(task: &Task) -> Result<(), String> {
    let reference = task.reference.as_ref().ok_or("нет эталона")?;
    let good = Solution {
        html: if matches!(task.kind, Kind::Html) { reference.html.clone() } else { String::new() },
        css: if matches!(task.kind, Kind::Selector) { reference.selector.clone() } else { reference.css.clone() },
    };
    let rep = verify(task, &good);
    if !rep.ok() {
        return Err(format!("эталон не проходит: {}", rep.reason().unwrap_or_default()));
    }
    let start = Solution { html: task.starter_html.clone(), css: task.starter_css.clone() };
    if verify(task, &start).ok() {
        return Err("заготовка уже решает задачу".into());
    }
    Ok(())
}
