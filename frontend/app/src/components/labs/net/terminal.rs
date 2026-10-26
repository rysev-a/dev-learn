//! Мини-терминал устройства: вывод по строкам, строка ввода с историей команд (стрелки вверх и вниз), курсор сразу в строке.

use leptos::{html, prelude::*};
use wasm_bindgen::JsCast;

use super::lab::Lab;
use super::logic;

/// Выделен ли сейчас текст на странице (чтобы клик по терминалу не сбивал выделение вывода).
fn has_selection() -> bool {
    web_sys::window().and_then(|w| selection_text(&w)).is_some_and(|t| !t.is_empty())
}

fn selection_text(w: &web_sys::Window) -> Option<String> {
    let f = js_sys::Reflect::get(w, &"getSelection".into()).ok()?;
    let sel = f.dyn_ref::<js_sys::Function>()?.call0(w).ok()?;
    let to_string = js_sys::Reflect::get(&sel, &"toString".into()).ok()?;
    let text = to_string.dyn_ref::<js_sys::Function>()?.call0(&sel).ok()?;
    text.as_string()
}

/// Поставить курсор в поле, не прокручивая страницу (`focus({preventScroll: true})`).
fn focus_quietly(el: &web_sys::HtmlInputElement) {
    let opts = js_sys::Object::new();
    let _ = js_sys::Reflect::set(&opts, &"preventScroll".into(), &true.into());
    match js_sys::Reflect::get(el, &"focus".into()).ok().and_then(|f| f.dyn_into::<js_sys::Function>().ok()) {
        Some(f) => {
            let _ = f.call1(el, &opts);
        }
        None => {
            let _ = el.focus();
        }
    }
}

#[component]
pub fn Terminal(lab: Lab, id: String) -> impl IntoView {
    let name = lab.name_of(&id);
    let prompt = logic::prompt(&name);
    let value = RwSignal::new(String::new());
    // история команд от новых к старым и позиция в ней (−1 — строка набирается заново)
    let hist = RwSignal::new(Vec::<String>::new());
    let pos = RwSignal::new(-1isize);
    let out_ref = NodeRef::<html::Div>::new();
    let input_ref = NodeRef::<html::Input>::new();

    let lines = {
        let id = id.clone();
        Signal::derive(move || lab.terms.with(|t| t.get(&id).cloned().unwrap_or_default()))
    };

    // курсор сразу в строке ввода: терминал открывают, чтобы печатать
    Effect::new(move |_| {
        if let Some(i) = input_ref.get() {
            focus_quietly(&i);
        }
    });
    // новый вывод — прокрутка вниз
    let count = Memo::new(move |_| lines.with(Vec::len));
    Effect::new(move |_| {
        count.track();
        if let Some(b) = out_ref.get() {
            leptos::leptos_dom::helpers::request_animation_frame(move || b.set_scroll_top(b.scroll_height()));
        }
    });

    let submit = {
        let id = id.clone();
        move |e: web_sys::SubmitEvent| {
            e.prevent_default();
            let line = value.get_untracked().trim().to_string();
            if line.is_empty() {
                return;
            }
            hist.update(|h| h.insert(0, line.clone()));
            pos.set(-1);
            value.set(String::new());
            lab.terminal_run(&id, &line);
        }
    };
    let on_key = move |e: web_sys::KeyboardEvent| {
        let step = hist.with_untracked(|h| logic::history_step(h, pos.get_untracked(), &e.key()));
        if let Some((n, text)) = step {
            e.prevent_default();
            pos.set(n);
            value.set(text);
        }
    };

    let shown_prompt = prompt.clone();
    view! {
        <div
            class="nl-term"
            on:click=move |_| {
                // клик в любое место терминала ставит курсор в строку ввода (если не выделяют текст вывода)
                if !has_selection() {
                    if let Some(i) = input_ref.get_untracked() {
                        focus_quietly(&i);
                    }
                }
            }
        >
            <div class="nl-term-out" node_ref=out_ref>
                {move || lines.with(Vec::is_empty).then(|| view! { <div class="nl-term-hint">"Введите «help», чтобы увидеть команды."</div> })}
                {move || {
                    let p = shown_prompt.clone();
                    lines
                        .get()
                        .into_iter()
                        .map(|l| {
                            let text = if l.cmd { format!("{p}{}", l.text) } else { l.text };
                            view! { <div class=if l.cmd { "cmd" } else { "res" }>{text}</div> }
                        })
                        .collect::<Vec<_>>()
                }}
            </div>
            <form class="nl-term-in" on:submit=submit>
                <span>{prompt}</span>
                <input
                    node_ref=input_ref
                    prop:value=move || value.get()
                    on:input=move |e| value.set(event_target_value(&e))
                    on:keydown=on_key
                    spellcheck="false"
                    autocapitalize="off"
                    autocomplete="off"
                    aria-label="Командная строка"
                />
            </form>
        </div>
    }
}
