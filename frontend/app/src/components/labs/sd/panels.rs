//! Панели лаборатории «Системный дизайн» вокруг поля: плавающая карточка параметров компонента, справка, кнопки в углу
//! поля, панель инструментов (удалить, отказ, подсказка, сбросить), цели и метрики. Все читают общее состояние [`Lab`].

use leptos::prelude::*;
use sdlab::{
    jsfmt,
    kinds::{self, ParamSpec, ParamType},
    FailKind, Kind, NodeLoad, ParamValue,
};

use super::{lab::Lab, logic};
use crate::components::labs::board_view::js_round;

// --- карточка параметров ------------------------------------------------------------------------

/// Плавающая карточка выбранного компонента: параметры, отключение для проверки отказа и его нагрузка.
#[component]
pub fn ParamsCard(lab: Lab, id: String) -> impl IntoView {
    let Some(first) = lab.state.with_untracked(|s| s.node(&id).cloned()) else { return ().into_any() };
    let spec = kinds::spec(first.kind);
    let kind = first.kind;
    let sc = lab.scenario();
    let node = {
        let id = id.clone();
        Memo::new(move |_| lab.state.with(|s| s.node(&id).cloned()))
    };
    let fields = spec
        .params
        .iter()
        .filter(|p| sc.param_visible(kind, p))
        .map(|p| view! { <Field lab=lab id=id.clone() spec=p /> })
        .collect_view();
    let can_fail = !matches!(kind, Kind::Clients | Kind::Monitor);
    let load = {
        let id = id.clone();
        Memo::new(move |_| lab.result.with(|r| r.loads.get(&id).cloned()))
    };
    let is_down = {
        let id = id.clone();
        Memo::new(move |_| lab.down.with(|d| d.contains(&id)))
    };
    let down_id = id.clone();

    view! {
        <div class="sd-float">
            <button type="button" class="sd-float-x" title="Закрыть" aria-label="Закрыть" on:click=move |_| lab.select_node(None)>
                "×"
            </button>
            <h4>{move || node.get().map(|n| n.name).unwrap_or_default()}</h4>
            <p class="sd-about">{spec.about}</p>
            {fields}
            {can_fail.then(|| view! {
                <label class="sd-field row">
                    <span>"Отключить (проверить отказ)"</span>
                    <input type="checkbox" prop:checked=move || is_down.get() on:change=move |e| lab.set_down(&down_id, event_target_checked(&e)) />
                </label>
                {move || load.get().map(|l| view! { <p class=format!("sd-load {}", load_status(&l))>{load_text(&l)}</p> })}
            })}
        </div>
    }
    .into_any()
}

/// Состояние узла для класса `sd-load`.
fn load_status(l: &NodeLoad) -> &'static str {
    use sdlab::NodeStatus::*;
    match l.status {
        Idle => "idle",
        Ok => "ok",
        Warm => "warm",
        Hot => "hot",
        Over => "over",
        Down => "down",
    }
}

/// «Нагрузка: 40 · ёмкость: 300 · загрузка 13% · заметка».
fn load_text(l: &NodeLoad) -> String {
    let n = |x: f64| jsfmt::num(js_round(x));
    let note = l.note.as_deref().filter(|s| !s.is_empty()).map(|s| format!(" · {s}")).unwrap_or_default();
    format!("Нагрузка: {} · ёмкость: {} · загрузка {}%{note}", n(l.load), n(l.cap), n(l.util * 100.0))
}

/// Поле одного параметра: число, список или флаг.
#[component]
fn Field(lab: Lab, id: String, spec: &'static ParamSpec) -> impl IntoView {
    let value = {
        let id = id.clone();
        Memo::new(move |_| lab.state.with(|s| s.node(&id).map(|n| n.param(spec.key).clone())).unwrap_or(ParamValue::Num(0.0)))
    };
    let control = match spec.ty {
        // число: правка уходит в схему сразу (в пределах), текст поля выравнивается по пределам, когда его покидают
        ParamType::Int => {
            let (id_input, id_change) = (id.clone(), id.clone());
            let commit = move |id: &str, text: &str| {
                let x = logic::clamp_int(text, spec.min, spec.max)?;
                lab.set_param(id, spec.key, ParamValue::Num(x));
                Some(x)
            };
            view! {
                <input
                    type="number"
                    min=spec.min.map(jsfmt::num)
                    max=spec.max.map(jsfmt::num)
                    value=value.get_untracked().as_text().into_owned()
                    on:input=move |e| {
                        commit(&id_input, &event_target_value(&e));
                    }
                    on:change=move |e| {
                        if let Some(x) = commit(&id_change, &event_target_value(&e)) {
                            event_target::<web_sys::HtmlInputElement>(&e).set_value(&jsfmt::num(x));
                        }
                    }
                />
            }
            .into_any()
        }
        ParamType::Bool => {
            let id = id.clone();
            view! {
                <input
                    type="checkbox"
                    prop:checked=move || value.with(ParamValue::is_true)
                    on:change=move |e| lab.set_param(&id, spec.key, ParamValue::Bool(event_target_checked(&e)))
                />
            }
            .into_any()
        }
        ParamType::Select => {
            let id = id.clone();
            let options = spec
                .options
                .iter()
                .map(|o| {
                    let text = o.value.as_text().into_owned();
                    let mine = text.clone();
                    view! { <option value=text prop:selected=move || value.with(|v| v.as_text() == mine.as_str())>{o.label}</option> }
                })
                .collect_view();
            view! {
                <select on:change=move |e| {
                    if let Some(v) = logic::option_value(spec, &event_target_value(&e)) {
                        lab.set_param(&id, spec.key, v);
                    }
                }>{options}</select>
            }
            .into_any()
        }
    };
    view! {
        <label class="sd-field">
            <span>{spec.label}</span>
            {control}
            {spec.help.map(|h| view! { <small>{h}</small> })}
        </label>
    }
}

// --- справка и кнопки в углу -----------------------------------------------------------------------

/// Всплывающая справка: как пользоваться полем и справочник чисел модели.
#[component]
pub fn HelpPopup() -> impl IntoView {
    view! {
        <div class="sd-help" role="dialog" aria-label="Справка по схеме">
            <p class="sd-about">
                "Выберите компонент на схеме, чтобы изменить его параметры. Новые компоненты перетащите на поле из палитры над ним (или кликните по кнопке), связи тяните от выходного порта к входному — подходящие соседи подключаются сами."
            </p>
            <h5>"Справочник чисел"</h5>
            <ul>{logic::reference_lines().into_iter().map(|l| view! { <li>{l}</li> }).collect_view()}</ul>
        </div>
    }
}

/// Кнопки в левом верхнем углу поля: справка и «во весь экран»; справка раскрывается под ними.
#[component]
pub fn Corner(lab: Lab) -> impl IntoView {
    let (help, fs) = (lab.help_open, lab.fs);
    view! {
        <div class="sd-corner">
            <div class="sd-corner-btns">
                <button type="button" class="sd-iconbtn" class:on=move || help.get() title="Справка" aria-label="Справка" aria-pressed=move || help.get().to_string() on:click=move |_| help.update(|v| *v = !*v)>
                    "?"
                </button>
                <button
                    type="button"
                    class="sd-iconbtn"
                    title=move || if fs.get() { "Свернуть (Esc)" } else { "Схема на весь экран" }
                    aria-label=move || if fs.get() { "Свернуть" } else { "На весь экран" }
                    on:click=move |_| fs.update(|v| *v = !*v)
                >
                    {move || {
                        let path = if fs.get() { "M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" } else { "M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" };
                        view! {
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d=path></path>
                            </svg>
                        }
                    }}
                </button>
            </div>
            {move || help.get().then(|| view! { <HelpPopup /> })}
        </div>
    }
}

/// Карточка параметров выбранного компонента поверх поля.
#[component]
pub fn Overlay(lab: Lab) -> impl IntoView {
    move || lab.selected.get().map(|id| view! { <ParamsCard lab=lab id=id /> })
}

// --- панель инструментов ---------------------------------------------------------------------------

/// «Удалить», выбор отказа, «Подсказка» и «Сбросить».
#[component]
pub fn Toolbar(lab: Lab) -> impl IntoView {
    let current = move || lab.fail.get().map(|f| f.as_str()).unwrap_or_default();
    let option = move |f: FailKind| {
        let value = f.as_str();
        view! { <option value=value prop:selected=move || current() == value>{logic::fail_text(f).unwrap_or_default()}</option> }
    };
    view! {
        <div class="sd-toolbar">
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.remove_selected() disabled=move || !lab.can_delete()>
                "Удалить"
            </button>
            <span class="sd-spacer"></span>
            <label class="sd-fail">
                <span>"Отказ:"</span>
                <select on:change=move |e| lab.fail.set(event_target_value(&e).parse::<FailKind>().ok())>
                    <option value="" prop:selected=move || current().is_empty()>"нет"</option>
                    {option(FailKind::Zone)}
                    {option(FailKind::Region)}
                    {option(FailKind::Deploy)}
                    {move || lab.fail_kinds.get().into_iter().map(option).collect_view()}
                </select>
            </label>
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.hint_open.update(|v| *v = !*v)>
                "Подсказка"
            </button>
            <button type="button" class="quiz-btn ghost" on:click=move |_| lab.reset()>
                "Сбросить"
            </button>
        </div>
    }
}

/// Плашки с нагрузкой упражнения над полем.
#[component]
pub fn Chips(lab: Lab) -> impl IntoView {
    let chips = logic::workload_chips(&lab.scenario().workload);
    view! { <div class="sd-chips">{chips.into_iter().map(|c| view! { <span>{c}</span> }).collect_view()}</div> }
}

// --- цели и метрики ---------------------------------------------------------------------------------

/// Итог в стиле приложения: значок, заголовок, пояснение и кнопка «дальше».
#[component]
fn ResultAlert(#[prop(into)] title: String, #[prop(into)] text: Signal<String>, #[prop(into)] has_next: Signal<bool>, on_next: Callback<()>) -> impl IntoView {
    view! {
        <div class="lab-alert ok" role="status">
            <span class="lab-alert-ico" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                    <path d="M20 6 9 17l-5-5"></path>
                </svg>
            </span>
            <div class="lab-alert-body">
                <p class="lab-alert-title">{title}</p>
                <p class="lab-alert-text">{move || text.get()}</p>
            </div>
            {move || has_next.get().then(|| view! {
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

/// Цели упражнения с отметками; когда все выполнены — итог и кнопка перехода дальше.
#[component]
pub fn Goals(
    lab: Lab,
    /// что написать в итоге: упражнение уже было решено, засчитано сейчас или решение ещё проверяется
    #[prop(into)]
    verdict: Signal<String>,
    /// есть ли следующее упражнение и как к нему перейти
    #[prop(into)]
    has_next: Signal<bool>,
    on_next: Callback<()>,
) -> impl IntoView {
    view! {
        <div class="sd-goals">
            <h4>"Цели"</h4>
            <ul>
                {move || {
                    lab.goals
                        .get()
                        .into_iter()
                        .map(|g| {
                            view! {
                                <li class=if g.ok { "ok" } else { "bad" }>
                                    <span class="sd-gmark">{if g.ok { "✓" } else { "✗" }}</span>
                                    <span class="sd-gtext">{g.text} <small>{g.detail}</small></span>
                                </li>
                            }
                        })
                        .collect_view()
                }}
            </ul>
            {move || lab.solved_now.get().then(|| view! { <ResultAlert title="Все цели выполнены" text=verdict has_next=has_next on_next=on_next /> })}
        </div>
    }
}

/// Одна строка метрик: название и значение (`bad` подсвечивает значение).
fn metric(name: &'static str, value: String, bad: bool) -> impl IntoView {
    view! {
        <div>
            <dt>{name}</dt>
            <dd class=if bad { "bad" } else { "" }>{value}</dd>
        </div>
    }
}

/// Метрики расчёта: задержки, успешные ответы, доступность, стоимость и показатели компонентов, которые есть на схеме.
#[component]
pub fn Metrics(lab: Lab) -> impl IntoView {
    let num = jsfmt::num;
    let pct0 = move |x: f64| format!("{}%", num(js_round(x * 100.0)));
    view! {
        <div class="sd-metrics">
            <h4>
                "Метрики "
                {move || lab.fail.get().and_then(logic::fail_text).map(|t| view! { <small>{format!("· {t}")}</small> })}
            </h4>
            {move || {
                let r = lab.result.get();
                let latency = if r.entry { format!("{} / {} мс", num(r.p50), num(r.p99)) } else { "—".to_owned() };
                view! {
                    <dl>
                        {metric("p50 / p99", latency, false)}
                        {metric("Успешных ответов", logic::fmt_pct(r.success), r.success < 0.99)}
                        {metric("Доступность", logic::fmt_pct(r.availability), false)}
                        {metric("Стоимость", format!("${} в мес.", num(r.cost)), false)}
                        {r.hit.map(|h| metric("Попаданий в кэш", pct0(h), false))}
                        {r.cdn_hit.map(|h| metric("Попаданий в CDN", pct0(h), false))}
                        {r.lag_sec.map(|l| metric("Отставание очереди", if l >= 999.0 { "не разбирается".to_owned() } else { format!("{} с", num(l)) }, l >= 999.0))}
                        {r.replica_lag_ms.map(|l| metric("Отставание реплик", format!("{} мс", num(l)), false))}
                    </dl>
                    {r.warnings.iter().map(|w| view! { <p class="sd-warn">{w.clone()}</p> }).collect_view()}
                }
            }}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use sdlab::NodeStatus;

    fn load(status: NodeStatus, note: Option<&str>) -> NodeLoad {
        NodeLoad { load: 40.4, cap: 300.0, util: 0.1347, units: 1.0, status, note: note.map(String::from) }
    }

    #[test]
    fn load_line_rounds_numbers_and_appends_the_note() {
        assert_eq!(load_text(&load(NodeStatus::Ok, None)), "Нагрузка: 40 · ёмкость: 300 · загрузка 13%");
        assert_eq!(load_text(&load(NodeStatus::Hot, Some("упор в базу"))), "Нагрузка: 40 · ёмкость: 300 · загрузка 13% · упор в базу");
        assert_eq!(load_text(&load(NodeStatus::Hot, Some(""))), "Нагрузка: 40 · ёмкость: 300 · загрузка 13%");
    }

    #[test]
    fn load_status_matches_css_classes() {
        assert_eq!(load_status(&load(NodeStatus::Over, None)), "over");
        assert_eq!(load_status(&load(NodeStatus::Down, None)), "down");
        assert_eq!(load_status(&load(NodeStatus::Idle, None)), "idle");
    }
}
