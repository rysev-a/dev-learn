//! Chapter fullscreen mode: state (the `?fs=1` flag in the address and native fullscreen), the shell slots into which tabs
//! put their items and buttons, and pure address helpers.
//!
//! The shell (tree, tabs, "Collapse") lives in the chapter layout; a tab publishes its items and buttons via [`FsItems`] and
//! [`FsHead`]: they are mounted straight into shell elements (in React, the `itemsSlot` and `headSlot` portals). Outside fullscreen
//! there are no slots and these components render nothing: the tab shows everything itself.

use std::collections::HashSet;

use leptos::{
    html,
    mount::mount_to,
    prelude::*,
};
use leptos_router::{
    hooks::{use_location, use_navigate},
    NavigateOptions,
};

use crate::dom;

const FS_PARAM: &str = "fs";

// --- address ------------------------------------------------------------------------------------

/// Value of a query-string parameter (`?a=1&b=2`). Values here are plain identifiers, with no escaping.
pub fn query_param(search: &str, key: &str) -> Option<String> {
    search.trim_start_matches('?').split('&').find_map(|pair| {
        let (k, v) = pair.split_once('=').unwrap_or((pair, ""));
        (k == key).then(|| v.to_string())
    })
}

/// Query string with the given parameter set (`None` removes the parameter); other parameters are preserved.
pub fn set_query_param(search: &str, key: &str, value: Option<&str>) -> String {
    let mut pairs: Vec<String> = search
        .trim_start_matches('?')
        .split('&')
        .filter(|pair| !pair.is_empty() && pair.split('=').next() != Some(key))
        .map(String::from)
        .collect();
    if let Some(v) = value {
        pairs.push(format!("{key}={v}"));
    }
    if pairs.is_empty() {
        String::new()
    } else {
        format!("?{}", pairs.join("&"))
    }
}

/// The query string contains `fs=1`.
pub fn fs_in_search(search: &str) -> bool {
    query_param(search, FS_PARAM).as_deref() == Some("1")
}

/// Address of a chapter or its tab (`sub` is `""`, `questions` or `exercises`); in fullscreen `?fs=1` is appended.
pub fn chapter_href(book: i64, chapter: i64, sub: &str, fs: bool) -> String {
    let sub = if sub.is_empty() { String::new() } else { format!("/{sub}") };
    format!("/book/{book}/chapter/{chapter}{sub}{}", set_query_param("", FS_PARAM, fs.then_some("1")))
}

/// The address belongs to a chapter page: only here does the fullscreen flag live in the address.
fn in_chapter(path: &str) -> bool {
    path.strip_prefix("/book/").is_some_and(|rest| rest.contains("/chapter/"))
}

// --- native fullscreen --------------------------------------------------------------------------

mod native {
    /// The browser is currently in fullscreen.
    pub fn active() -> bool {
        web_sys::window().and_then(|w| w.document()).is_some_and(|d| d.fullscreen_element().is_some())
    }

    /// Enters or leaves fullscreen at the document root. The root is used, not the chapter overlay: the overlay is recreated
    /// when the chapter changes, and the browser would leave the mode when its element disappears from the DOM. A browser refusal (for example,
    /// without a user gesture when opened via a `?fs=1` link) is harmless: the shell stays on top of the page.
    pub fn set(on: bool) {
        let Some(doc) = web_sys::window().and_then(|w| w.document()) else { return };
        if on && doc.fullscreen_element().is_none() {
            if let Some(root) = doc.document_element() {
                let _ = root.request_fullscreen();
            }
        } else if !on && doc.fullscreen_element().is_some() {
            doc.exit_fullscreen();
        }
    }
}

// --- state --------------------------------------------------------------------------------------

/// Chapter fullscreen state; shared by all chapters of a section (created in the chapter layout, which is not recreated when the
/// chapter changes), so expanded tree sections survive navigation to another chapter.
#[derive(Clone, Copy)]
pub struct Fullscreen {
    on: RwSignal<bool>,
    /// expanded sections of the table-of-contents tree
    pub open_sections: RwSignal<HashSet<i64>>,
}

impl Fullscreen {
    /// Whether fullscreen is on (in a reactive context, a subscription).
    pub fn is_on(&self) -> bool {
        self.on.get()
    }

    pub fn is_on_untracked(&self) -> bool {
        self.on.get_untracked()
    }

    pub fn set(&self, on: bool) {
        self.on.set(on);
    }
}

/// Creates the state and puts it into the context. The state is primary, the address follows it: if a tab navigated to an address without
/// `fs=1` (for example, selected an exercise), the flag is put back into the address. Native fullscreen is turned on and off together
/// with the state; leaving it with Esc (or the browser button) also closes the shell.
pub fn provide_fullscreen() -> Fullscreen {
    let location = use_location();
    let navigate = use_navigate();
    let fs = Fullscreen { on: RwSignal::new(fs_in_search(&location.search.get_untracked())), open_sections: RwSignal::new(HashSet::new()) };
    let on = fs.on;

    Effect::new(move |_| {
        let (path, search, want) = (location.pathname.get(), location.search.get(), on.get());
        if in_chapter(&path) && fs_in_search(&search) != want {
            navigate(&format!("{path}{}", set_query_param(&search, FS_PARAM, want.then_some("1"))), NavigateOptions { replace: true, scroll: false, ..Default::default() });
        }
    });
    Effect::new(move |_| native::set(on.get()));
    dom::on_window_untyped("fullscreenchange", move || {
        if on.get_untracked() && !native::active() {
            on.set(false);
        }
    });
    dom::on_window(leptos::ev::keydown, move |ev| {
        if ev.key() == "Escape" && on.get_untracked() {
            on.set(false);
        }
    });
    on_cleanup(|| native::set(false));
    provide_context(fs);
    fs
}

// --- shell slots --------------------------------------------------------------------------------

/// Places in the shell where a tab puts its items (left tree) and buttons (header). Created together with the chapter.
#[derive(Clone, Copy)]
pub struct Slots {
    pub items: NodeRef<html::Div>,
    pub head: NodeRef<html::Span>,
}

impl Slots {
    pub fn provide() -> Self {
        let slots = Self { items: NodeRef::new(), head: NodeRef::new() };
        provide_context(slots);
        slots
    }
}

/// Mounts `children` inside the element named by `target`; while the element is missing (or has changed), the view is not shown.
/// No wrapper (unlike `Portal`): the slot layout (`flex`, `gap`) stays the same as its neighbors'.
fn teleport(target: impl Fn() -> Option<web_sys::HtmlElement> + 'static, children: ChildrenFn) {
    Effect::new(move |_| {
        let Some(element) = target() else { return };
        let children = children.clone();
        // the storage belongs to the current effect run: on the next run or disposal it is released, and the view leaves the DOM
        let mounted = StoredValue::new_local(None);
        mounted.set_value(Some(mount_to(element, move || untrack(|| children()))));
    });
}

/// Tab items in the left fullscreen tree (slides, questions, exercises).
#[component]
pub fn FsItems(children: ChildrenFn) -> impl IntoView {
    let (fs, slots) = (expect_context::<Fullscreen>(), expect_context::<Slots>());
    teleport(move || fs.is_on().then(|| slots.items.get().map(Into::into)).flatten(), children);
}

/// Tab buttons in the fullscreen shell header.
#[component]
pub fn FsHead(children: ChildrenFn) -> impl IntoView {
    let (fs, slots) = (expect_context::<Fullscreen>(), expect_context::<Slots>());
    teleport(move || fs.is_on().then(|| slots.head.get().map(Into::into)).flatten(), children);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn query_params_are_read_and_replaced_without_touching_the_others() {
        assert_eq!(query_param("?task=a1&fs=1", "task").as_deref(), Some("a1"));
        assert_eq!(query_param("?task=a1", "fs"), None);
        assert_eq!(query_param("", "fs"), None);
        assert_eq!(set_query_param("?task=a1", "fs", Some("1")), "?task=a1&fs=1");
        assert_eq!(set_query_param("?fs=1&task=a1", "fs", None), "?task=a1");
        assert_eq!(set_query_param("?fs=1", "fs", None), "", "the last parameter goes away together with the '?'");
        assert_eq!(set_query_param("?task=a1", "task", Some("b2")), "?task=b2");
    }

    #[test]
    fn fullscreen_flag_is_exactly_fs_equals_one() {
        assert!(fs_in_search("?fs=1"));
        assert!(fs_in_search("?slide=3&fs=1"));
        assert!(!fs_in_search("?fs=0"));
        assert!(!fs_in_search("?fsx=1"));
        assert!(!fs_in_search(""));
    }

    #[test]
    fn chapter_links_carry_the_fullscreen_flag() {
        assert_eq!(chapter_href(13, 161, "", false), "/book/13/chapter/161");
        assert_eq!(chapter_href(13, 161, "", true), "/book/13/chapter/161?fs=1");
        assert_eq!(chapter_href(13, 161, "questions", true), "/book/13/chapter/161/questions?fs=1");
        assert_eq!(chapter_href(9, 5, "exercises", false), "/book/9/chapter/5/exercises");
    }

    #[test]
    fn the_flag_lives_in_the_address_only_on_chapter_pages() {
        assert!(in_chapter("/book/13/chapter/161"));
        assert!(in_chapter("/book/13/chapter/161/exercises"));
        assert!(!in_chapter("/book/13"));
        assert!(!in_chapter("/settings"));
        assert!(!in_chapter("/"));
    }
}
