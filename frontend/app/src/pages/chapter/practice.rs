//! Вкладка «Практика»: сами упражнения (`code::Exercises`) и их пункты в левом дереве полноэкранного режима.

use api::dto::{progress_key, Task};
use leptos::prelude::*;
use leptos_router::{
    hooks::{use_location, use_navigate},
    NavigateOptions,
};

use super::{code, ChapterCtx};
use crate::{
    components::{
        fs_tree::{FsItem, ItemState},
        fullscreen::{query_param, set_query_param, FsItems},
    },
    progress::ProgressStore,
};

/// Адрес с выбранным упражнением: остальные параметры (в том числе `fs`) сохраняются.
pub fn task_href(path: &str, search: &str, task: &str) -> String {
    format!("{path}{}", set_query_param(search, "task", Some(task)))
}

#[component]
pub fn Practice() -> impl IntoView {
    view! {
        <TaskItems />
        <code::Exercises />
    }
}

/// Упражнения главы со статусами в дереве полного экрана; выбранное — в адресе (`?task=`), как и у самой вкладки.
#[component]
fn TaskItems() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    let progress = expect_context::<ProgressStore>();
    let location = use_location();
    let navigate = use_navigate();
    let tasks = Memo::new(move |_| ctx.tasks.get().ready().map(|t| t.tasks.clone()).unwrap_or_default());
    let statuses = Memo::new(move |_| {
        let num = ctx.chapter.get().ready()?.num;
        progress.data.with(|d| d.code.get(&progress_key(ctx.book, num)).cloned())
    });
    let current = Memo::new(move |_| {
        let search = location.search.get();
        tasks.with(|t| code::selected(t, query_param(&search, "task").as_deref()))
    });
    let pick = Callback::new(move |id: String| {
        let href = task_href(&location.pathname.get_untracked(), &location.search.get_untracked(), &id);
        navigate(&href, NavigateOptions { replace: true, scroll: false, ..Default::default() });
    });
    let state_of = move |task: &Task| {
        let id = task.id.clone();
        Signal::derive(move || statuses.with(|s| ItemState::from_status(s.as_ref().and_then(|m| m.get(&id)).map_or("", String::as_str))))
    };
    view! {
        <FsItems>
            {move || {
                tasks
                    .get()
                    .into_iter()
                    .enumerate()
                    .map(|(i, task)| {
                        let (id, state) = (task.id.clone(), state_of(&task));
                        view! {
                            <FsItem num=i + 1 on=Signal::derive(move || current.get() == i) state=state on_click=Callback::new(move |()| pick.run(id.clone()))>
                                {task.title}
                            </FsItem>
                        }
                    })
                    .collect_view()
            }}
        </FsItems>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn picking_a_task_keeps_the_fullscreen_flag() {
        assert_eq!(task_href("/book/9/chapter/5/exercises", "?fs=1", "s05-03"), "/book/9/chapter/5/exercises?fs=1&task=s05-03");
        assert_eq!(task_href("/book/9/chapter/5/exercises", "?task=s05-01&fs=1", "s05-03"), "/book/9/chapter/5/exercises?fs=1&task=s05-03");
        assert_eq!(task_href("/book/9/chapter/5/exercises", "", "a"), "/book/9/chapter/5/exercises?task=a");
    }
}
