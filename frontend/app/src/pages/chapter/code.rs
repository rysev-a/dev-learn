//! Вкладка «Практика»: упражнения с кодом (проверка в песочнице через очередь) и, если кода нет, задачи с вводом ответа.

use std::collections::HashMap;

use api::dto::{Attempt, ChapterState, RunResult, RunState, SqlDataset, Task};
use gloo_timers::{callback::Timeout, future::TimeoutFuture};
use highlight::Lang;
use leptos::{prelude::*, task::spawn_local};
use leptos_router::{
    hooks::{use_location, use_navigate},
    NavigateOptions,
};

use super::{Answers, ChapterCtx};
use crate::{
    components::{
        code_editor::CodeEditor,
        fullscreen::{chapter_href, Fullscreen},
        labs::LabHost,
        overload::{Overload, OverloadNotice, OverloadState},
        results::{History, Results},
        sql_schema::SqlSchema,
    },
    hooks::{client, use_load, Load},
    progress::ProgressStore,
    settings,
};

/// Очередь длиннее этого места или ожидание дольше этого (мс) — показываем окно о перегрузке.
const BUSY_QUEUE_PLACE: i64 = 8;
const BUSY_WAIT_MS: u32 = 25_000;
const DRAFT_DELAY_MS: u32 = 700;
const POLL_MS: u32 = 700;
/// Дольше этого проверку не ждём (6 минут при опросе раз в 0,7 с).
const MAX_POLLS: u32 = 6 * 60 * 1000 / POLL_MS;

/// Язык подсветки редактора по режиму задачи (песочница определяет язык решения).
pub fn lang_of(mode: &str) -> Lang {
    match mode {
        "rust" => Lang::Rust,
        "c" => Lang::C,
        "sql" => Lang::Sql,
        "func" | "stdout" => Lang::Python,
        _ => Lang::Plain,
    }
}

/// Номер выбранной задачи по `?task=`: неизвестный id — первая.
pub fn selected(tasks: &[Task], param: Option<&str>) -> usize {
    param.and_then(|p| tasks.iter().position(|t| t.id == p)).unwrap_or(0)
}

/// Учебная база SQL-задачи (режим `sql`) из наборов главы по ключу `dataset`.
fn sql_dataset(task: &Task, datasets: &StoredValue<HashMap<String, SqlDataset>>) -> Option<SqlDataset> {
    let key = task.dataset.as_deref().filter(|_| task.mode == "sql")?;
    datasets.with_value(|d| d.get(key).cloned())
}

/// Подпись справа от полосы прогресса: где выполняются упражнения главы.
fn run_label(tasks: &[Task]) -> &'static str {
    if tasks.iter().all(|t| t.mode == "lab") {
        return "интерактивно · в браузере";
    }
    match tasks.iter().find(|t| t.mode != "lab").map(|t| t.mode.as_str()) {
        Some("sql") => "sql · docker",
        Some("rust") => "rust · docker",
        Some("c") => "c · docker",
        Some("js") => "javascript · docker",
        _ => "python · docker",
    }
}

/// Первая глава книги после `num`, у которой есть код-задачи (id для адреса): по порядку номеров глав.
fn next_chapter(course: &[api::dto::Section], counts: &api::dto::Counts, book: i64, num: i64) -> Option<i64> {
    let with_tasks = counts.get(&book.to_string())?;
    let mut chapters: Vec<_> = course.iter().flat_map(|s| s.chapters.iter()).filter(|c| c.num > num).collect();
    chapters.sort_by_key(|c| c.num);
    chapters.into_iter().find(|c| with_tasks.get(&c.num.to_string()).is_some_and(|n| *n > 0)).map(|c| c.id)
}

/// Сообщение об ожидании: место в очереди.
pub fn queue_text(position: Option<i64>) -> String {
    match position {
        Some(p) if p > 1 => format!("В очереди (перед вами {})…", p - 1),
        _ => "В очереди…".to_string(),
    }
}

#[component]
pub fn Exercises() -> impl IntoView {
    let ctx = expect_context::<ChapterCtx>();
    move || match (ctx.chapter.get(), ctx.tasks.get()) {
        (Load::Ready(ch), Load::Ready(t)) if !t.tasks.is_empty() => view! { <CodePractice book=ctx.book num=ch.num tasks=t.tasks datasets=t.datasets /> }.into_any(),
        (Load::Ready(_), Load::Loading) | (Load::Loading, _) => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
        (Load::Ready(_), _) if ctx.answer_count.get() > 0 => view! { <Answers /> }.into_any(),
        (Load::Failed(e), _) => view! { <p class="error">{e}</p> }.into_any(),
        _ => view! { <p class="empty">"Для этой главы нет упражнений"</p> }.into_any(),
    }
}

#[component]
fn CodePractice(book: i64, num: i64, tasks: Vec<Task>, datasets: HashMap<String, SqlDataset>) -> impl IntoView {
    let state = use_load(move || Some(()), move |c, _| async move { c.chapter_state(book, num).await });
    // первая следующая глава книги, где есть код-задачи: после последнего упражнения «Дальше →» ведёт туда
    let course = use_load(move || Some(()), move |c, _| async move { c.course(book).await });
    let counts = use_load(move || Some(()), |c, _| async move { c.code_counts().await });
    let next = Signal::derive(move || {
        let (course, counts) = (course.get(), counts.get());
        next_chapter(course.ready()?, counts.ready()?, book, num)
    });
    let tasks = StoredValue::new(tasks);
    let datasets = StoredValue::new(datasets);
    move || match state.get() {
        Load::Ready(s) => view! { <CodeBody book=book num=num tasks=tasks.get_value() datasets=datasets.get_value() state=s next=next /> }.into_any(),
        Load::Failed(e) => view! { <p class="error">{e}</p> }.into_any(),
        Load::Loading => view! { <p class="empty">"Загрузка…"</p> }.into_any(),
    }
}

#[component]
fn CodeBody(book: i64, num: i64, tasks: Vec<Task>, datasets: HashMap<String, SqlDataset>, state: ChapterState, next: Signal<Option<i64>>) -> impl IntoView {
    let progress = expect_context::<ProgressStore>();
    let navigate = use_navigate();
    let navigate_next = navigate.clone();
    let fullscreen = expect_context::<Fullscreen>();
    let location = use_location();
    let total = tasks.len();
    let tasks = StoredValue::new(tasks);
    let datasets = StoredValue::new(datasets);
    let status = RwSignal::new(state.status);
    let drafts = RwSignal::new(state.drafts);
    let results = RwSignal::new(HashMap::<String, RunResult>::new());
    let history = RwSignal::new(Vec::<Attempt>::new());
    let busy = RwSignal::new(None::<String>);
    let phase = RwSignal::new(String::new());
    let hints = RwSignal::new(HashMap::<String, bool>::new());

    let idx = Memo::new(move |_| {
        let search = location.search.get();
        let param = search.trim_start_matches('?').split('&').find_map(|kv| kv.strip_prefix("task=")).map(String::from);
        tasks.with_value(|t| selected(t, param.as_deref()))
    });
    let task = move || tasks.with_value(|t| t[idx.get()].clone());
    let select = Callback::new(move |i: usize| {
        let id = tasks.with_value(|t| t[i].id.clone());
        navigate(&format!("{}?task={id}", location.pathname.get_untracked()), NavigateOptions { replace: true, ..Default::default() });
    });
    let code_of = move |t: &Task| drafts.with(|d| d.get(&t.id).cloned()).unwrap_or_else(|| t.starter.clone());
    let done = move || status.with(|s| s.values().filter(|v| *v == "ok").count());

    // черновик уходит на сервер через паузу и при уходе со страницы
    let pending = StoredValue::new(HashMap::<String, String>::new());
    let timer: StoredValue<Option<Timeout>, LocalStorage> = StoredValue::new_local(None);
    let flush = move || {
        timer.set_value(None);
        for (id, code) in pending.try_update_value(std::mem::take).unwrap_or_default() {
            spawn_local(async move {
                let _ = client().save_draft(book, num, &id, &code).await;
            });
        }
    };
    on_cleanup(flush);
    let edit = move |id: String, code: String| {
        drafts.update(|d| {
            d.insert(id.clone(), code.clone());
        });
        pending.update_value(|p| {
            p.insert(id, code);
        });
        timer.set_value(Some(Timeout::new(DRAFT_DELAY_MS, flush)));
    };

    // история попыток выбранной задачи
    Effect::new(move |_| {
        let id = task().id;
        history.set(Vec::new());
        spawn_local(async move {
            if let Ok(list) = client().attempts(book, num, &id).await {
                if task().id == id {
                    history.set(list);
                }
            }
        });
    });

    // после последнего упражнения — к первому упражнению следующей главы с задачами
    let has_next = move || idx.get() + 1 < total || next.get().is_some();
    let go_next = Callback::new(move |()| {
        let i = idx.get_untracked();
        if i + 1 < total {
            select.run(i + 1);
        } else if let Some(id) = next.get_untracked() {
            navigate_next(&chapter_href(book, id, "exercises", fullscreen.is_on_untracked()), Default::default());
        }
    });
    let accepted = Memo::new(move |_| {
        let t = task();
        let code = code_of(&t);
        status.with(|s| s.get(&t.id).map(String::as_str) == Some("ok")) && history.with(|h| h.iter().any(|a| a.status == "ok" && a.code == code))
    });
    let go_mode = move || accepted.get() && has_next();

    let overload = OverloadState::new();
    let run = Callback::new(move |()| {
        if busy.get_untracked().is_some() {
            return;
        }
        let t = task();
        let (id, code) = (t.id.clone(), code_of(&t));
        flush();
        busy.set(Some(id.clone()));
        phase.set(String::new());
        spawn_local(async move {
            let c = client();
            let outcome = async {
                let (job, mut st) = c.run(book, num, &id, &code).await?;
                let mut polls = 0;
                let mut warned = false;
                loop {
                    match st {
                        RunState::Done(res) => return Ok(res),
                        RunState::Queued { position } => {
                            phase.set(queue_text(position));
                            // длинная очередь или долгое ожидание — предложить запустить систему у себя (один раз за проверку)
                            if !warned && (position.unwrap_or(0) >= BUSY_QUEUE_PLACE || polls * POLL_MS >= BUSY_WAIT_MS) {
                                warned = true;
                                overload.raise(Overload::Busy);
                            }
                        }
                        RunState::Running => phase.set("Выполняется в песочнице…".to_string()),
                    }
                    polls += 1;
                    if polls > MAX_POLLS {
                        return Err(api::ApiError { status: 0, message: "Проверка слишком долго ждёт в очереди — попробуйте позже.".into() });
                    }
                    TimeoutFuture::new(POLL_MS).await;
                    st = c.run_state(&job).await?;
                }
            }
            .await;
            match outcome {
                Ok(res) => {
                    let st = if res.solved { "ok" } else { "bad" };
                    status.update(|s| {
                        if s.get(&id).map(String::as_str) != Some("ok") {
                            s.insert(id.clone(), st.to_string());
                        }
                    });
                    progress.set_code_status(book, num, &id, st);
                    if let Some(a) = &res.attempt {
                        history.update(|h| h.insert(0, Attempt { id: a.id, code: code.clone(), status: a.status.clone(), passed: res.passed, total: res.total, created_at: a.created_at.clone() }));
                    }
                    results.update(|r| {
                        r.insert(id.clone(), res.clone());
                    });
                    // автопереход (настройка выключена по умолчанию): через секунду, если ученик остался на этой задаче
                    if res.solved && settings::read(settings::AUTO_NEXT).as_deref() == Some("1") {
                        let id = id.clone();
                        Timeout::new(1000, move || {
                            if task().id == id {
                                go_next.run(());
                            }
                        })
                        .forget();
                    }
                }
                Err(e) => {
                    // 503: проверка недоступна или очередь переполнена
                    if e.status == 503 {
                        overload.raise(Overload::Unavailable);
                    }
                    results.update(|r| {
                        r.insert(id.clone(), RunResult { status: "error".into(), results: Vec::new(), stdout: String::new(), stderr: e.message, passed: 0, total: 0, solved: false, attempt: None });
                    });
                }
            }
            busy.set(None);
            phase.set(String::new());
        });
    });
    // Ctrl/Cmd+Enter: проверить; если принятое решение не менялось — перейти дальше
    let primary = Callback::new(move |()| if go_mode() { go_next.run(()) } else { run.run(()) });

    let list = move || {
        tasks.with_value(|ts| {
            ts.iter()
                .enumerate()
                .map(|(i, t)| {
                    let id = t.id.clone();
                    let st = Memo::new(move |_| status.with(|s| s.get(&id).cloned()).unwrap_or_default());
                    view! {
                        <button class="pr-item" class:on=move || idx.get() == i class:ok=move || st.get() == "ok" class:bad=move || st.get() == "bad" title=t.title.clone() on:click=move |_| select.run(i)>
                            <span class="pr-mark">{move || match st.get().as_str() { "ok" => "✓".to_string(), "bad" => "✗".to_string(), _ => (i + 1).to_string() }}</span>
                            <span class="pr-name">{t.title.clone()}</span>
                        </button>
                    }
                })
                .collect_view()
        })
    };

    let main = move || {
        let t = task();
        let i = idx.get();
        let st = Memo::new({
            let id = t.id.clone();
            move |_| status.with(|s| s.get(&id).cloned()).unwrap_or_default()
        });
        let editor = if t.mode == "lab" {
            let id = t.id.clone();
            let draft = {
                let t = t.clone();
                Signal::derive(move || drafts.with(|d| d.get(&t.id).cloned()).unwrap_or_default())
            };
            let on_solved = Callback::new({
                let id = id.clone();
                move |()| {
                    status.update(|s| {
                        s.insert(id.clone(), "ok".to_string());
                    });
                    progress.set_code_status(book, num, &id, "ok");
                }
            });
            let solved = {
                let id = id.clone();
                Signal::derive(move || status.with(|s| s.get(&id).map(String::as_str) == Some("ok")))
            };
            view! {
                <LabHost
                    book=book
                    num=num
                    task_id=id.clone()
                    draft=draft
                    on_draft=Callback::new(move |code| edit(id.clone(), code))
                    solved=solved
                    on_solved=on_solved
                    on_next=go_next
                    has_next=Signal::derive(has_next)
                />
            }
            .into_any()
        } else {
            let id = t.id.clone();
            let value = {
                let t = t.clone();
                Signal::derive(move || code_of(&t))
            };
            let running = Signal::derive(move || busy.get().is_some());
            let hint = t.hint.clone();
            let starter = t.starter.clone();
            let res = {
                let id = id.clone();
                Signal::derive(move || results.with(|r| r.get(&id).cloned()))
            };
            let hint_id = id.clone();
            let id_for_edit = id.clone();
            view! {
                <CodeEditor value=value on_input=Callback::new(move |code| edit(id_for_edit.clone(), code)) on_run=primary lang=lang_of(&t.mode) accepted=Signal::derive(move || accepted.get()) />
                <div class="ex-row">
                    {move || if go_mode() {
                        view! { <button class="quiz-btn" on:click=move |_| go_next.run(()) title="Дальше (Ctrl+Enter)">"Дальше →"</button> }.into_any()
                    } else {
                        view! { <button class="quiz-btn" on:click=move |_| run.run(()) disabled=move || running.get() title="Проверить (Ctrl+Enter)">{move || if running.get() { if phase.get().starts_with("В очереди") { "В очереди…" } else { "Проверяю…" } } else { "Проверить" }}</button> }.into_any()
                    }}
                    {move || go_mode().then(|| view! { <button class="quiz-btn ghost" on:click=move |_| run.run(()) disabled=move || running.get() title="Запустить проверку ещё раз">"Проверить ещё раз"</button> })}
                    {(!hint.is_empty()).then(|| {
                        let hint_id = hint_id.clone();
                        let hint_id2 = hint_id.clone();
                        view! { <button class="quiz-btn ghost" on:click=move |_| hints.update(|h| { let e = h.entry(hint_id.clone()).or_insert(false); *e = !*e })>{move || if hints.with(|h| h.get(&hint_id2).copied().unwrap_or(false)) { "Скрыть подсказку" } else { "Подсказка" }}</button> }
                    })}
                    <button class="quiz-btn ghost" title="Вернуть исходный шаблон" on:click={
                        let id = id.clone();
                        move |_| edit(id.clone(), starter.clone())
                    }>"Сбросить"</button>
                </div>
                {move || {
                    let t = task();
                    (!t.hint.is_empty() && hints.with(|h| h.get(&t.id).copied().unwrap_or(false))).then(|| view! { <p class="ex-hint">{t.hint}</p> })
                }}
                <Results res=res running=running phase=Signal::from(phase) />
                <History items=history current=Signal::derive(move || code_of(&task())) on_pick=Callback::new({
                    let id = id.clone();
                    move |code| edit(id.clone(), code)
                }) />
            }
            .into_any()
        };
        // учебная база SQL-задачи: ERD и данные таблиц
        let schema = sql_dataset(&t, &datasets).map(|schema| view! { <SqlSchema schema=schema /> });
        view! {
            <div class="pr-main">
                <div class="pr-head">
                    <h3>{format!("{}. {}", i + 1, t.title)}</h3>
                    <span class="pr-badge" class:ok=move || st.get() == "ok" class:bad=move || st.get() == "bad">
                        {move || match st.get().as_str() { "ok" => "выполнено", "bad" => "не пройдено", _ => "не решено" }}
                    </span>
                </div>
                <p class="pr-statement">{t.statement.clone()}</p>
                {schema}
                {editor}
            </div>
        }
    };

    // упражнения-лаборатории занимают всю ширину: список упражнений — полосой сверху (как `lab-pr` в React)
    let labs = tasks.with_value(|t| t.iter().all(|x| x.mode == "lab"));
    view! {
        <section class="pr" class:lab-pr=labs>
            <OverloadNotice state=overload />
            <div class="pr-top">
                <span class="pr-top-label">{move || format!("Решено {} из {total}", done())}</span>
                <div class="pr-bar" role="progressbar" aria-valuemin="0" aria-valuemax=total>
                    <i style=move || format!("width: {}%", done() * 100 / total.max(1))></i>
                </div>
                <span class="pr-top-label">{run_label(&tasks.with_value(|t| t.clone()))}</span>
            </div>
            <div class="pr-body">
                <aside class="pr-list" aria-label="Упражнения">{list}</aside>
                {main}
            </div>
        </section>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn task(id: &str) -> Task {
        Task { id: id.into(), mode: "func".into(), title: String::new(), statement: String::new(), starter: String::new(), hint: String::new(), dataset: None }
    }

    #[test]
    fn selected_task_comes_from_the_address_and_defaults_to_the_first() {
        let tasks = [task("a"), task("b")];
        assert_eq!(selected(&tasks, Some("b")), 1);
        assert_eq!(selected(&tasks, Some("zzz")), 0);
        assert_eq!(selected(&tasks, None), 0);
    }

    #[test]
    fn queue_message_counts_those_ahead() {
        assert_eq!(queue_text(Some(1)), "В очереди…");
        assert_eq!(queue_text(Some(4)), "В очереди (перед вами 3)…");
        assert_eq!(queue_text(None), "В очереди…");
    }

    #[test]
    fn next_chapter_is_the_first_later_one_with_code_tasks() {
        use api::dto::{ChapterRef, Counts, Section};
        let chapter = |id: i64, num: i64| ChapterRef { id, num, title: String::new(), parts_count: 1 };
        let course = vec![Section { id: 1, title: String::new(), chapters: vec![chapter(11, 1), chapter(12, 2), chapter(13, 3), chapter(14, 4)] }];
        let counts: Counts = [("13".to_string(), [("1".to_string(), 5), ("3".to_string(), 7)].into_iter().collect())].into_iter().collect();
        assert_eq!(next_chapter(&course, &counts, 13, 1), Some(13), "глава 2 без задач пропускается");
        assert_eq!(next_chapter(&course, &counts, 13, 3), None, "после последней главы с задачами идти некуда");
        assert_eq!(next_chapter(&course, &counts, 99, 1), None, "у книги без задач — нет");
    }

    #[test]
    fn label_names_the_runtime_of_the_chapter() {
        let t = |mode: &str| Task { id: "x".into(), mode: mode.into(), title: String::new(), statement: String::new(), starter: String::new(), hint: String::new(), dataset: None };
        assert_eq!(run_label(&[t("sql")]), "sql · docker");
        assert_eq!(run_label(&[t("func"), t("stdout")]), "python · docker");
        assert_eq!(run_label(&[t("lab")]), "интерактивно · в браузере");
        assert_eq!(run_label(&[t("lab"), t("rust")]), "rust · docker");
    }

    #[test]
    fn editor_language_follows_the_task_mode() {
        assert_eq!(lang_of("func"), Lang::Python);
        assert_eq!(lang_of("rust"), Lang::Rust);
        assert_eq!(lang_of("sql"), Lang::Sql);
        assert_eq!(lang_of("lab"), Lang::Plain);
    }
}
