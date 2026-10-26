//! Редактор кода для упражнений: `<textarea>` с подсветкой, нарисованной под ним (общий лексер crate `highlight`).
//! Tab вставляет отступ, Ctrl/Cmd+Enter — проверить. Высота растёт по числу строк.

use highlight::{highlight, Lang};
use leptos::{html, prelude::*};
use wasm_bindgen::JsCast;

const INDENT: &str = "    ";

/// Вставка отступа вместо смены фокуса: новое значение и позиция курсора (в символах).
pub fn insert_indent(value: &str, start: usize, end: usize) -> (String, usize) {
    let chars: Vec<char> = value.chars().collect();
    let (start, end) = (start.min(chars.len()), end.min(chars.len()));
    let mut out: String = chars[..start].iter().collect();
    out.push_str(INDENT);
    out.extend(&chars[end..]);
    (out, start + INDENT.chars().count())
}

#[component]
pub fn CodeEditor(
    #[prop(into)] value: Signal<String>,
    on_input: Callback<String>,
    on_run: Callback<()>,
    #[prop(default = Lang::Python)] lang: Lang,
    /// решение принято: зелёная рамка
    #[prop(into, default = false.into())]
    accepted: Signal<bool>,
    /// фокус при создании
    #[prop(default = true)]
    autofocus: bool,
) -> impl IntoView {
    let area = NodeRef::<html::Textarea>::new();
    let shade = NodeRef::<html::Pre>::new();
    if autofocus {
        Effect::new(move |_| {
            if let Some(el) = area.get() {
                let _ = el.focus();
                let end = el.value().chars().count() as u32;
                let _ = el.set_selection_range(end, end);
            }
        });
    }
    let rows = move || value.with(|v| v.lines().count().max(1) + usize::from(v.ends_with('\n'))).max(6);
    let highlighted = move || {
        value
            .get()
            .split('\n')
            .map(|line| {
                let tokens = highlight(lang, line)
                    .into_iter()
                    .map(|t| match t.kind.css() {
                        Some(color) => view! { <span style=format!("color: {color}")>{t.text}</span> }.into_any(),
                        None => t.text.into_any(),
                    })
                    .collect_view();
                view! { <div class="rs-line">{tokens}" "</div> }
            })
            .collect_view()
    };
    let on_keydown = move |ev: web_sys::KeyboardEvent| {
        let key = ev.key();
        if key == "Enter" && (ev.ctrl_key() || ev.meta_key()) {
            ev.prevent_default();
            on_run.run(());
        } else if key == "Tab" && !ev.shift_key() {
            ev.prevent_default();
            let Some(el) = area.get() else { return };
            let (start, end) = (el.selection_start().ok().flatten().unwrap_or(0) as usize, el.selection_end().ok().flatten().unwrap_or(0) as usize);
            let (text, caret) = insert_indent(&el.value(), start, end);
            on_input.run(text.clone());
            el.set_value(&text);
            let _ = el.set_selection_range(caret as u32, caret as u32);
        }
    };
    // подсветка под текстом двигается вместе с горизонтальной прокруткой поля
    let on_scroll = move |_| {
        if let (Some(a), Some(s)) = (area.get(), shade.get()) {
            if let Ok(s) = s.clone().dyn_into::<web_sys::HtmlElement>() {
                s.set_scroll_left(a.scroll_left());
            }
        }
    };
    view! {
        <div class="rs-editor" class:right=move || accepted.get()>
            <pre class="rs-shade" aria-hidden="true" node_ref=shade>{highlighted}</pre>
            <textarea
                class="rs-input"
                node_ref=area
                rows=rows
                spellcheck="false"
                wrap="off"
                autocapitalize="off"
                prop:value=move || value.get()
                on:input=move |ev| on_input.run(event_target_value(&ev))
                on:keydown=on_keydown
                on:scroll=on_scroll
            ></textarea>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::insert_indent;

    #[test]
    fn indent_replaces_the_selection_and_moves_the_caret() {
        assert_eq!(insert_indent("ab", 1, 1), ("a    b".to_string(), 5));
        assert_eq!(insert_indent("abcd", 1, 3), ("a    d".to_string(), 5));
        assert_eq!(insert_indent("я", 1, 1), ("я    ".to_string(), 5), "позиции — в символах, не в байтах");
        assert_eq!(insert_indent("x", 9, 9).0, "x    ", "позиция за концом не ломает строку");
    }
}
