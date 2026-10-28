//! Left tree of fullscreen mode: book sections → chapters; under the current chapter is a slot for the items of the active tab
//! (see [`FsItems`](super::fullscreen::FsItems)). A slot item is an [`FsItem`].

use api::dto::Section;
use leptos::{html, prelude::*};

use super::fullscreen::Fullscreen;
use crate::{
    hooks::Load,
    pages::book::BookCtx,
};

/// The section containing chapter `chapter` (by id).
pub fn section_of(sections: &[Section], chapter: i64) -> Option<i64> {
    sections.iter().find(|s| s.chapters.iter().any(|c| c.id == chapter)).map(|s| s.id)
}

/// State of an item under the chapter: slide, question or exercise.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub enum ItemState {
    #[default]
    Open,
    Ok,
    Bad,
}

impl ItemState {
    /// Code task status on the server: `ok` is solved, `bad` is failed, anything else is unsolved.
    pub fn from_status(status: &str) -> Self {
        match status {
            "ok" => ItemState::Ok,
            "bad" => ItemState::Bad,
            _ => ItemState::Open,
        }
    }

    fn class(self) -> &'static str {
        match self {
            ItemState::Open => "",
            ItemState::Ok => "ok",
            ItemState::Bad => "bad",
        }
    }

    /// Icon instead of a number; an unsolved item shows its number.
    fn mark(self, num: usize) -> String {
        match self {
            ItemState::Open => format!("{num:02}"),
            ItemState::Ok => "✓".to_string(),
            ItemState::Bad => "✗".to_string(),
        }
    }
}

/// Item button class.
fn item_class(on: bool, state: ItemState) -> String {
    format!("fst-slide {} {}", if on { "on" } else { "" }, state.class())
}

/// Tree item under the current chapter.
#[component]
pub fn FsItem(
    num: usize,
    /// current item
    #[prop(optional, into)]
    on: Signal<bool>,
    #[prop(optional, into)] state: Signal<ItemState>,
    on_click: Callback<()>,
    children: Children,
) -> impl IntoView {
    view! {
        <button class=move || item_class(on.get(), state.get()) on:click=move |_| on_click.run(())>
            <span class="fst-slide-num">{move || state.get().mark(num)}</span>
            <span class="fst-slide-name">{children()}</span>
        </button>
    }
}

/// Tree: book sections, the open section shows its chapters, the current chapter holds the `items` slot.
#[component]
pub fn FsTree(chapter: i64, items: NodeRef<html::Div>, on_open: Callback<i64>) -> impl IntoView {
    let ctx = expect_context::<BookCtx>();
    let fs = expect_context::<Fullscreen>();
    view! {
        <aside class="slide-fs-toc" aria-label=i18n::tr("Contents")>
            {move || match ctx.course.get() {
                Load::Ready(sections) if !sections.is_empty() => {
                    // the section with the current chapter is expanded until collapsed manually
                    if let Some(sec) = section_of(&sections, chapter) {
                        fs.open_sections.update(|open| {
                            open.insert(sec);
                        });
                    }
                    sections.into_iter().map(|sec| view! { <Sec sec=sec current=chapter on_open=on_open items=items /> }).collect_view().into_any()
                }
                _ => view! { <ItemsSlot items=items /> }.into_any(),
            }}
        </aside>
    }
}

/// The place under the current chapter where the tab puts its items.
#[component]
fn ItemsSlot(items: NodeRef<html::Div>) -> impl IntoView {
    view! { <div class="fst-slides" node_ref=items></div> }
}

/// Section: toggle header and chapters. Chapters are always in the DOM (a collapsed section is hidden by style): the current chapter's slot is
/// not recreated when the section is collapsed.
#[component]
fn Sec(sec: Section, current: i64, on_open: Callback<i64>, items: NodeRef<html::Div>) -> impl IntoView {
    let fs = expect_context::<Fullscreen>();
    let id = sec.id;
    let open = move || fs.open_sections.with(|o| o.contains(&id));
    let toggle = move |_| {
        fs.open_sections.update(|o| {
            if !o.remove(&id) {
                o.insert(id);
            }
        })
    };
    let chapters = sec
        .chapters
        .into_iter()
        .map(|ch| {
            let cur = ch.id == current;
            let open_it = move |_| if !cur { on_open.run(ch.id) };
            view! {
                <div>
                    <button class="slide-fs-toc-item" class:on=cur on:click=open_it>
                        <span class="slide-fs-toc-num">{format!("{:02}", ch.num)}</span>
                        <span class="slide-fs-toc-name">{ch.title}</span>
                    </button>
                    {cur.then(|| view! { <ItemsSlot items=items /> })}
                </div>
            }
        })
        .collect_view();
    view! {
        <div class="fst-sec">
            <button class="fst-sec-head" aria-expanded=move || open().to_string() on:click=toggle>
                <span class="fst-chev" class:open=open>"›"</span>
                {sec.title}
            </button>
            <div style:display=move || if open() { "contents" } else { "none" }>{chapters}</div>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use api::dto::ChapterRef;

    use super::*;

    fn section(id: i64, chapters: &[i64]) -> Section {
        Section { id, title: format!("Section {id}"), chapters: chapters.iter().map(|&c| ChapterRef { id: c, num: c, title: String::new(), parts_count: 1 }).collect() }
    }

    #[test]
    fn the_section_of_a_chapter_is_found_by_chapter_id() {
        let sections = [section(1, &[10, 11]), section(2, &[20])];
        assert_eq!(section_of(&sections, 11), Some(1));
        assert_eq!(section_of(&sections, 20), Some(2));
        assert_eq!(section_of(&sections, 99), None);
    }

    #[test]
    fn item_state_comes_from_the_status_and_picks_the_mark_and_class() {
        assert_eq!(ItemState::from_status("ok"), ItemState::Ok);
        assert_eq!(ItemState::from_status("bad"), ItemState::Bad);
        assert_eq!(ItemState::from_status(""), ItemState::Open);
        assert_eq!(ItemState::Open.mark(3), "03");
        assert_eq!(ItemState::Ok.mark(3), "✓");
        assert_eq!(ItemState::Bad.mark(3), "✗");
        assert_eq!(item_class(true, ItemState::Ok), "fst-slide on ok");
        assert_eq!(item_class(false, ItemState::Open).trim(), "fst-slide");
    }
}
