//! Окно «За кадром»: текст абзаца текущего слайда. Закреплено у нижнего края, стоит по центру области, где показано; слова
//! подсвечиваются по мере «чтения». «Лапка» наверху меняет высоту (не выше полного текста); высота запоминается.

use leptos::{html, prelude::*};

use crate::{dom, settings};

const MIN_H: f64 = 60.0;
/// «Показывать весь текст» (до 70% экрана): запоминается вместо высоты конкретного абзаца.
const FULL: f64 = 2000.0;

/// Номер слова, которое читается сейчас: `t` и `d` — время и длительность абзаца (без чтения слов не подсвечены).
pub fn current_word(words: usize, t: Option<f64>, d: f64) -> Option<usize> {
    let t = t?;
    (words > 0 && d > 0.0).then(|| (((t / d) * words as f64).floor() as usize).min(words - 1))
}

#[component]
pub fn VoicePopup(text: String, #[prop(into)] t: Signal<Option<f64>>, d: f64) -> impl IntoView {
    let words: Vec<String> = text.split_whitespace().map(String::from).collect();
    let cur = {
        let n = words.len();
        Memo::new(move |_| current_word(n, t.get(), d))
    };
    let pop = NodeRef::<html::Div>::new();
    let body = NodeRef::<html::P>::new();
    let height = RwSignal::new(settings::read(settings::VOICE_H).and_then(|v| v.parse::<f64>().ok()).filter(|v| (MIN_H..=FULL).contains(v)));

    // полная высота окна нужна плееру и полям страницы; центр и ширина — по области, где окно показано
    let guard = StoredValue::new_local(None::<dom::ResizeGuard>);
    Effect::new(move |_| {
        let Some(el) = pop.get() else { return };
        let area: Option<web_sys::Element> = el.parent_element().and_then(|p| p.closest(".slide-fs-main, .content").ok().flatten());
        let place = {
            let el = el.clone();
            let area = area.clone();
            move || {
                dom::set_root_var("--voice-h", &format!("{}px", el.offset_height()));
                if let Some(area) = &area {
                    let r = area.get_bounding_client_rect();
                    let html: &web_sys::HtmlElement = el.as_ref();
                    let style = html.style();
                    let _ = style.set_property("--vp-x", &format!("{}px", (r.left() + r.width() / 2.0).round()));
                    let _ = style.set_property("--vp-w", &format!("{}px", (r.width() - 32.0).round()));
                }
            }
        };
        place();
        let mut watched: Vec<web_sys::Element> = vec![el.clone().into()];
        watched.extend(area);
        guard.set_value(dom::observe_resize(&watched, place));
    });
    on_cleanup(move || {
        guard.set_value(None);
        dom::remove_root_var("--voice-h");
    });

    // текущее слово остаётся в видимой части текста
    Effect::new(move |_| {
        let _ = cur.get();
        let Some(p) = body.get() else { return };
        let Some(now) = p.query_selector(".now").ok().flatten().and_then(|e| wasm_bindgen::JsCast::dyn_into::<web_sys::HtmlElement>(e).ok()) else { return };
        let top = f64::from(now.offset_top()) - f64::from(p.offset_top());
        let (scroll, view) = (f64::from(p.scroll_top()), f64::from(p.client_height()));
        if top < scroll || top + f64::from(now.offset_height()) > scroll + view {
            p.set_scroll_top((top - view / 3.0).max(0.0) as i32);
        }
    });

    let clamp = move |v: f64| {
        let content = body.get_untracked().map_or(v, |p| f64::from(p.scroll_height()));
        let screen = web_sys::window().and_then(|w| w.inner_height().ok()).and_then(|h| h.as_f64()).unwrap_or(900.0) * 0.7;
        v.min(content).min(screen).max(MIN_H).round()
    };
    let start_resize = move |ev: web_sys::PointerEvent| {
        if ev.button() != 0 {
            return;
        }
        ev.prevent_default();
        let (y0, h0) = (f64::from(ev.client_y()), body.get_untracked().map_or(MIN_H, |p| f64::from(p.client_height())));
        let handles = StoredValue::new_local(Vec::<WindowListenerHandle>::new());
        let mv = window_event_listener(leptos::ev::pointermove, move |e| height.set(Some(clamp(h0 + y0 - f64::from(e.client_y())))));
        let up = window_event_listener(leptos::ev::pointerup, move |e| {
            handles.update_value(|hs| hs.drain(..).for_each(|h| h.remove()));
            let want = h0 + y0 - f64::from(e.client_y());
            let full = body.get_untracked().is_some_and(|p| clamp(want) >= f64::from(p.scroll_height()));
            let value = if full { FULL } else { clamp(want) };
            settings::write(settings::VOICE_H, Some(&value.to_string()));
            if full {
                height.set(Some(FULL));
            }
        });
        handles.set_value(vec![mv, up]);
    };

    let word_views = words
        .into_iter()
        .enumerate()
        .map(|(i, w)| {
            let class = move || match cur.get() {
                None => "",
                Some(c) if i < c => "past",
                Some(c) if i == c => "now",
                Some(_) => "next",
            };
            view! { <span class=class>{w}" "</span> }
        })
        .collect_view();

    view! {
        <div class="voice-pop" role="region" aria-label="Текст озвучки" node_ref=pop>
            <div
                class="voice-pop-grip"
                role="separator"
                aria-orientation="horizontal"
                aria-label="Высота окна"
                title="Потяните вверх или вниз, чтобы изменить высоту (двойной клик — по умолчанию)"
                on:pointerdown=start_resize
                on:dblclick=move |_| {
                    height.set(None);
                    settings::write(settings::VOICE_H, None);
                }
            >
                <i></i>
            </div>
            <div class="voice-pop-tag">"За кадром"</div>
            <p class="voice-pop-text" node_ref=body style=move || height.get().map(|h| format!("max-height: min({h}px, 70vh)"))>
                {word_views}
            </p>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::current_word;

    #[test]
    fn highlighted_word_follows_the_clock() {
        assert_eq!(current_word(10, None, 5.0), None, "без чтения слова не подсвечены");
        assert_eq!(current_word(10, Some(0.0), 5.0), Some(0));
        assert_eq!(current_word(10, Some(2.6), 5.0), Some(5));
        assert_eq!(current_word(10, Some(99.0), 5.0), Some(9), "не дальше последнего слова");
        assert_eq!(current_word(0, Some(1.0), 5.0), None);
    }
}
