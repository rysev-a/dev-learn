//! Слайды главы: рамка слайда и панель просмотра (шапка с плеером, сцена, точки).

use leptos::prelude::*;

use super::{
    fs_tree::FsItem,
    fullscreen::{FsHead, FsItems, Fullscreen},
};
use crate::{dom, player::fmt_time};

fn play_icon() -> impl IntoView {
    view! {
        <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
            <path d="M2.5 1.2v9.6L10.5 6z" />
        </svg>
    }
}

fn pause_icon() -> impl IntoView {
    view! {
        <svg width="11" height="11" viewBox="0 0 12 12" fill="currentColor">
            <rect x="2" y="1.5" width="3" height="9" rx="0.8" />
            <rect x="7" y="1.5" width="3" height="9" rx="0.8" />
        </svg>
    }
}

/// Номер слайда после нажатия стрелки: вправо и вниз — вперёд, влево и вверх — назад; остальные клавиши — `None`.
pub fn arrow_target(key: &str, idx: usize, count: usize) -> Option<usize> {
    match key {
        "ArrowRight" | "ArrowDown" => Some((idx + 1).min(count.saturating_sub(1))),
        "ArrowLeft" | "ArrowUp" => Some(idx.saturating_sub(1)),
        _ => None,
    }
}

/// Панель просмотра: номер слайда, время главы, «Играть/Пауза», сам слайд и точки переключения. В полном экране шапка
/// уходит в шапку оболочки, названия слайдов — в левое дерево, а сцена занимает всё поле; стрелки листают слайды.
#[component]
pub fn SlidePanel(
    /// показанный слайд
    #[prop(into)]
    idx: Signal<usize>,
    count: usize,
    /// названия слайдов для списка полного экрана
    titles: Vec<String>,
    /// позиция и длина главы, секунды
    #[prop(into)]
    time: Signal<(f64, f64)>,
    #[prop(into)] playing: Signal<bool>,
    on_play: Callback<()>,
    on_pause: Callback<()>,
    on_pick: Callback<usize>,
    /// слайд `i` на экране (пересоздаётся при смене слайда, как `key` в React)
    stage: Callback<usize, AnyView>,
) -> impl IntoView {
    let controls = move || {
        view! {
            <span class="slide-panel-num">{move || format!("{:02} / {count:02}", idx.get() + 1)}</span>
            <span class="s-time-mono">{move || { let (t, d) = time.get(); format!("{} / {}", fmt_time(t), fmt_time(d)) }}</span>
            <button class="slide-btn" on:click=move |_| if playing.get() { on_pause.run(()) } else { on_play.run(()) } title=move || if playing.get() { "Пауза" } else { "Играть" }>
                {move || if playing.get() { pause_icon().into_any() } else { play_icon().into_any() }}
                <span>{move || if playing.get() { "Пауза" } else { "Играть" }}</span>
            </button>
        }
    };
    // режим выбирается при создании: при смене полного экрана вкладка создаётся заново
    if expect_context::<Fullscreen>().is_on_untracked() {
        dom::on_window(leptos::ev::keydown, move |ev| {
            let typing = ev.target().and_then(|t| wasm_bindgen::JsCast::dyn_into::<web_sys::HtmlElement>(t).ok()).is_some_and(|el| matches!(el.tag_name().as_str(), "INPUT" | "TEXTAREA") || el.is_content_editable());
            if let (false, Some(i)) = (typing, arrow_target(&ev.key(), idx.get_untracked(), count)) {
                ev.prevent_default();
                on_pick.run(i);
            }
        });
        return view! {
            <FsHead>{controls()}</FsHead>
            <FsItems>
                {titles
                    .iter()
                    .enumerate()
                    .map(|(i, title)| {
                        let title = title.clone();
                        view! { <FsItem num=i + 1 on=Signal::derive(move || idx.get() == i) on_click=Callback::new(move |()| on_pick.run(i))>{title}</FsItem> }
                    })
                    .collect_view()}
            </FsItems>
            <div class="slide-fs-stage">{move || stage.run(idx.get())}</div>
        }
        .into_any();
    }
    let dots = (0..count)
        .map(|i| view! { <button class="slide-dot" class:on=move || idx.get() == i on:click=move |_| on_pick.run(i) title=format!("Слайд {}", i + 1)></button> })
        .collect_view();
    view! {
        <aside class="slide-panel">
            <div class="slide-panel-head">{controls()}</div>
            <div class="slide-stage">{move || stage.run(idx.get())}</div>
            <div class="slide-dots">{dots}</div>
        </aside>
    }
    .into_any()
}

#[cfg(test)]
mod tests {
    use super::arrow_target;

    #[test]
    fn arrows_move_one_slide_and_stop_at_the_ends() {
        assert_eq!(arrow_target("ArrowRight", 2, 5), Some(3));
        assert_eq!(arrow_target("ArrowDown", 4, 5), Some(4), "дальше последнего не идём");
        assert_eq!(arrow_target("ArrowLeft", 2, 5), Some(1));
        assert_eq!(arrow_target("ArrowUp", 0, 5), Some(0), "раньше первого не идём");
        assert_eq!(arrow_target("Enter", 2, 5), None);
        assert_eq!(arrow_target("ArrowRight", 0, 0), Some(0));
    }
}
