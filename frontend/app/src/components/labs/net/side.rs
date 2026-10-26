//! Цели упражнения с отметками, итоговая плашка и журнал последнего пакета.

use leptos::prelude::*;
use netlab::sim::fmt_ms;

use super::lab::Lab;
use super::logic;

/// Плашка итога: значок, заголовок, пояснение и (если есть куда) кнопка «Дальше».
#[component]
fn Alert(ok: bool, title: &'static str, #[prop(into)] text: Signal<String>, #[prop(into)] has_next: Signal<bool>, on_next: Callback<()>) -> impl IntoView {
    view! {
        <div class=if ok { "lab-alert ok" } else { "lab-alert bad" } role="status">
            <span class="lab-alert-ico" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                    <path d=if ok { "M20 6 9 17l-5-5" } else { "M18 6 6 18M6 6l12 12" }></path>
                </svg>
            </span>
            <div class="lab-alert-body">
                <p class="lab-alert-title">{title}</p>
                <p class="lab-alert-text">{move || text.get()}</p>
            </div>
            {move || (ok && has_next.get()).then(|| view! {
                <button type="button" class="lab-alert-next" on:click=move |_| on_next.run(())>
                    "Дальше"
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M5 12h14M12 5l7 7-7 7"></path>
                    </svg>
                </button>
            })}
        </div>
    }
}

/// Цели: номер до первой правки, потом ✓ или ✗ и пояснение; ▶ показывает путь пакета по цели.
#[component]
pub fn Goals(
    lab: Lab,
    /// число целей упражнения
    count: usize,
    solved_before: bool,
    #[prop(into)] solved: Signal<bool>,
    #[prop(into)] has_next: Signal<bool>,
    on_next: Callback<()>,
) -> impl IntoView {
    let items = (0..count)
        .map(|i| {
            let goal = move || lab.goals.with(|g| g.get(i).cloned());
            let shown = move || lab.touched.get() || solved.get();
            let class = move || match (shown(), goal()) {
                (true, Some(g)) if g.ok => "ok",
                (true, Some(_)) => "bad",
                _ => "",
            };
            let mark = move || match (shown(), goal()) {
                (true, Some(g)) => (if g.ok { "✓" } else { "✗" }).to_string(),
                _ => (i + 1).to_string(),
            };
            view! {
                <li class=class>
                    <span class="nl-gmark">{mark}</span>
                    <span class="nl-gtext">
                        {move || goal().map(|g| g.text).unwrap_or_default()}
                        {move || {
                            let d = goal().filter(|_| shown()).map(|g| g.detail).unwrap_or_default();
                            (!d.is_empty()).then(|| view! { <small>{d}</small> })
                        }}
                    </span>
                    <button type="button" class="nl-play" title="Показать путь пакета" on:click=move |_| lab.play_goal(i)>"▶"</button>
                </li>
            }
        })
        .collect_view();
    let verdict = Signal::derive(move || logic::verdict_text(solved_before, solved.get()).to_string());
    let hint = Signal::derive(|| "Нажмите ▶ у цели — увидите, где пакет теряется, и поправьте настройки.".to_string());
    view! {
        <div class="nl-goals">
            <h4>"Цели"</h4>
            <ul>{items}</ul>
            <div class="nl-actions">
                <button
                    type="button"
                    class="quiz-btn"
                    on:click=move |_| {
                        lab.touched.set(true);
                        lab.checked.set(true);
                    }
                >
                    "Проверить"
                </button>
            </div>
            {move || {
                if lab.solved_now.get() {
                    view! { <Alert ok=true title="Все цели выполнены" text=verdict has_next=has_next on_next=on_next /> }.into_any()
                } else if lab.checked.get() {
                    view! { <Alert ok=false title="Пока не всё работает" text=hint has_next=has_next on_next=on_next /> }.into_any()
                } else {
                    ().into_any()
                }
            }}
        </div>
    }
}

/// Журнал событий последней пробы: время, устройство, что произошло.
#[component]
pub fn Log(lab: Lab) -> impl IntoView {
    let title = move || lab.run.with(|r| r.as_ref().map(|r| r.title.clone()).filter(|t| !t.is_empty()));
    // номера событий пересчитываются на каждый кадр анимации, а список перерисовывается, только когда они изменились
    let visible = Memo::new(move |_| lab.run.with(|r| r.as_ref().map(|run| logic::log_indices(run, lab.slot.get())).unwrap_or_default()));
    let lines = move || {
        let idx = visible.get();
        lab.run.with(|r| {
            r.as_ref()
                .map(|run| idx.into_iter().filter_map(|i| run.events.get(i)).map(|e| (logic::event_class(e.kind), fmt_ms(Some(e.t)), e.dev.clone(), e.text.clone())).collect::<Vec<_>>())
                .unwrap_or_default()
        })
    };
    view! {
        <div class="nl-log">
            <h4>"Журнал " {move || title().map(|t| view! { <small>{format!("· {t}")}</small> })}</h4>
            {move || {
                let l = lines();
                if l.is_empty() {
                    view! { <p class="nl-none">"Запустите ping в терминале или нажмите ▶ у цели — здесь появится путь пакета: ARP, пересылка, NAT, потери."</p> }.into_any()
                } else {
                    view! {
                        <ol>
                            {l.into_iter().map(|(class, time, dev, text)| view! {
                                <li class=class><time>{time}</time><b>{lab.name_of(&dev)}</b><span>{text}</span></li>
                            }).collect_view()}
                        </ol>
                    }
                    .into_any()
                }
            }}
        </div>
    }
}
