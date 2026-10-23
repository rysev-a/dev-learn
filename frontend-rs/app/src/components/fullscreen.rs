//! Полноэкранный режим главы: состояние (флаг в адресе `?fs=1` и нативный полный экран), слоты оболочки, в которые вкладки
//! кладут свои пункты и кнопки, и чистые помощники адреса.
//!
//! Оболочка (дерево, вкладки, «Свернуть») живёт в макете главы; вкладка публикует свои пункты и кнопки через [`FsItems`] и
//! [`FsHead`]: они монтируются прямо в элементы оболочки (в React — порталы `itemsSlot` и `headSlot`). Вне полного экрана
//! слотов нет, и эти компоненты ничего не рисуют — вкладка показывает всё сама.

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

// --- адрес --------------------------------------------------------------------------------------

/// Значение параметра из строки запроса (`?a=1&b=2`). Значения здесь — простые идентификаторы, без экранирования.
pub fn query_param(search: &str, key: &str) -> Option<String> {
    search.trim_start_matches('?').split('&').find_map(|pair| {
        let (k, v) = pair.split_once('=').unwrap_or((pair, ""));
        (k == key).then(|| v.to_string())
    })
}

/// Строка запроса с заданным параметром (`None` — параметр убран); остальные параметры сохраняются.
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

/// В строке запроса стоит `fs=1`.
pub fn fs_in_search(search: &str) -> bool {
    query_param(search, FS_PARAM).as_deref() == Some("1")
}

/// Адрес главы или её вкладки (`sub` — `""`, `questions` или `exercises`); в полном экране к нему добавляется `?fs=1`.
pub fn chapter_href(book: i64, chapter: i64, sub: &str, fs: bool) -> String {
    let sub = if sub.is_empty() { String::new() } else { format!("/{sub}") };
    format!("/book/{book}/chapter/{chapter}{sub}{}", set_query_param("", FS_PARAM, fs.then_some("1")))
}

/// Адрес относится к странице главы: только здесь флаг полного экрана живёт в адресе.
fn in_chapter(path: &str) -> bool {
    path.strip_prefix("/book/").is_some_and(|rest| rest.contains("/chapter/"))
}

// --- нативный полный экран ----------------------------------------------------------------------

mod native {
    /// Браузер сейчас в полном экране.
    pub fn active() -> bool {
        web_sys::window().and_then(|w| w.document()).is_some_and(|d| d.fullscreen_element().is_some())
    }

    /// Входит в полный экран у корня документа или выходит из него. Берём именно корень, а не оверлей главы: оверлей при
    /// смене главы пересоздаётся, и браузер вышел бы из режима, когда его элемент исчезает из DOM. Отказ браузера (например,
    /// без жеста пользователя при открытии по ссылке `?fs=1`) не страшен: оболочка остаётся поверх страницы.
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

// --- состояние ----------------------------------------------------------------------------------

/// Состояние полного экрана главы; общее для всех глав раздела (создаётся в макете главы, который при смене главы не
/// пересоздаётся), поэтому раскрытые разделы дерева переживают переход к другой главе.
#[derive(Clone, Copy)]
pub struct Fullscreen {
    on: RwSignal<bool>,
    /// раскрытые разделы дерева содержания
    pub open_sections: RwSignal<HashSet<i64>>,
}

impl Fullscreen {
    /// Включён ли полный экран (в реактивном контексте — подписка).
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

/// Создаёт состояние и кладёт его в контекст. Состояние — первичное, адрес за ним следует: если вкладка перешла на адрес без
/// `fs=1` (например, выбрала упражнение), флаг возвращается в адрес. Нативный полный экран включается и выключается вместе
/// с состоянием; выход из него клавишей Esc (или кнопкой браузера) закрывает и оболочку.
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

// --- слоты оболочки -----------------------------------------------------------------------------

/// Места в оболочке, куда вкладка кладёт свои пункты (левое дерево) и кнопки (шапка). Создаются вместе с главой.
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

/// Монтирует `children` внутрь элемента, который назвала `target`; пока элемента нет (или он сменился), вид не показывается.
/// Без обёртки (в отличие от `Portal`): раскладка слота (`flex`, `gap`) остаётся такой же, как у соседей.
fn teleport(target: impl Fn() -> Option<web_sys::HtmlElement> + 'static, children: ChildrenFn) {
    Effect::new(move |_| {
        let Some(element) = target() else { return };
        let children = children.clone();
        // хранилище принадлежит текущему запуску эффекта: при следующем запуске или снятии оно освобождается, и вид уходит из DOM
        let mounted = StoredValue::new_local(None);
        mounted.set_value(Some(mount_to(element, move || untrack(|| children()))));
    });
}

/// Пункты вкладки в левом дереве полного экрана (слайды, вопросы, упражнения).
#[component]
pub fn FsItems(children: ChildrenFn) -> impl IntoView {
    let (fs, slots) = (expect_context::<Fullscreen>(), expect_context::<Slots>());
    teleport(move || fs.is_on().then(|| slots.items.get().map(Into::into)).flatten(), children);
}

/// Кнопки вкладки в шапке оболочки полного экрана.
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
        assert_eq!(set_query_param("?fs=1", "fs", None), "", "последний параметр уходит вместе с «?»");
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
