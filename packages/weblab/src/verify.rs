//! Solution check: task + submitted text → report.

use crate::css::{self, Stylesheet};
use crate::html::{self, Doc};
use crate::selector::{check_selector, has_id};
use crate::spec::{Check, Item, Kind, Report, Solution, Task};

/// Conditions given by the data plus the "default" conditions for the exercise kind.
pub fn verify(task: &Task, solution: &Solution) -> Report {
    let mut items = Vec::new();
    match task.kind {
        Kind::Html => {
            let doc = Doc::parse(&solution.html);
            items.extend(task.checks.iter().filter_map(|c| html::run(&doc, c)));
        }
        Kind::Css => {
            let doc = Doc::parse(&task.html);
            // rules from the task's `<style>` come before the student's rules
            let user = Stylesheet::parse(&solution.css);
            let sheet = Stylesheet::parse(&format!("{}\n{}", doc.style_text(), solution.css));
            items.extend(task.checks.iter().filter_map(|c| css::run(&doc, &sheet, &user, c, task.viewport)));
        }
        Kind::Selector => {
            items.extend(check_selector(task, &solution.css));
            // of the conditions, only "no #id" makes sense for selector text
            for c in &task.checks {
                if matches!(c, Check::NoIds) {
                    items.push(Item { text: i18n::tr("No selectors by `#id`").into(), ok: !has_id(&solution.css), detail: i18n::tr("an id selector was found").into() });
                }
            }
        }
    }
    // an empty editor does not solve the task, even if every condition is "something is absent"
    let empty = match task.kind {
        Kind::Html => solution.html.trim().is_empty(),
        Kind::Css | Kind::Selector => solution.css.trim().is_empty(),
    };
    if empty {
        items.push(Item { text: i18n::tr("Solution written").into(), ok: false, detail: i18n::tr("the editor is empty").into() });
    }
    Report { items }
}

/// Task data check (for tests and the seed): conditions are well-formed, the reference solution passes, the starter does not.
pub fn self_check(task: &Task) -> Result<(), String> {
    let reference = task.reference.as_ref().ok_or(i18n::tr("no reference solution"))?;
    let good = Solution {
        html: if matches!(task.kind, Kind::Html) { reference.html.clone() } else { String::new() },
        css: if matches!(task.kind, Kind::Selector) { reference.selector.clone() } else { reference.css.clone() },
    };
    let rep = verify(task, &good);
    if !rep.ok() {
        return Err(i18n::trf!("the reference solution fails: {0}", rep.reason().unwrap_or_default()));
    }
    let start = Solution { html: task.starter_html.clone(), css: task.starter_css.clone() };
    if verify(task, &start).ok() {
        return Err(i18n::tr("the starter already solves the task").into());
    }
    Ok(())
}
