//! Лаборатория «Системный дизайн» (книга 18): схема высоконагруженного сервиса на поле, расчёт под заданной нагрузкой и
//! цели упражнения. Расчёт, цели и допустимость связей — крейт `sdlab` (общий с сервером, он же перепроверяет решение);
//! здесь только интерфейс.
//!
//! * `lab.rs` — состояние: схема, выбор, отказы, расчёт и действия над схемой;
//! * `logic.rs` — чистая логика (черновик, правки, провода, вписывание, подписи) с тестами;
//! * `board.rs` — поле: палитра, компоненты, связи, порты, автоподстановка, сдвиг и масштаб (`board_view.rs`);
//! * `panels.rs` — карточка параметров, справка, инструменты, цели и метрики;
//! * `icons.rs` — значки компонентов.
//!
//! Черновик (схема) уходит хозяину при каждой правке, а когда выполнены все цели, решение отправляется на сервер один раз.

use std::sync::Arc;

use leptos::{ev, portal::Portal, prelude::*};

mod board;
mod icons;
mod lab;
mod logic;
mod panels;

use board::Board;
use lab::Lab;
use panels::{Chips, Corner, Goals, Metrics, Overlay, Toolbar};

use super::LabProps;
use crate::dom;

/// Что написать в итоге: решено раньше, засчитано только что или решение ещё проверяется на сервере.
fn verdict_text(solved_before: bool, solved: bool) -> &'static str {
    if solved_before {
        "Упражнение уже было решено."
    } else if solved {
        "Упражнение засчитано."
    } else {
        "Проверяю решение на сервере…"
    }
}

/// Лаборатория выбранного упражнения.
#[component]
pub fn SdLab(props: LabProps) -> impl IntoView {
    let scenario = match logic::parse_scenario(&props.task.spec) {
        Ok(s) => s,
        Err(e) => return view! { <p class="error">{e}</p> }.into_any(),
    };
    let initial = logic::restore(&scenario, &props.draft.get_untracked());
    let lab = Lab::new(Arc::new(scenario), initial, props.task.hint.clone(), props.on_draft);

    // решение отправляется один раз, когда выполнены все цели; если сервер отказал, повтор — после новых правок
    let solved_before = props.solved.get_untracked();
    let reported = StoredValue::new(false);
    let (solved, report) = (props.solved, props.report);
    Effect::new(move |_| {
        let ok = lab.solved_now.get();
        if solved.get_untracked() {
            return;
        }
        if !ok {
            reported.set_value(false);
        } else if !reported.get_value() {
            reported.set_value(true);
            report.run(lab.state.with_untracked(logic::draft_json));
        }
    });

    // во весь экран: страница под схемой не прокручивается, Esc закрывает
    let page_overflow = StoredValue::new_local(None::<String>);
    Effect::new(move |_| {
        let Some(body) = web_sys::window().and_then(|w| w.document()).and_then(|d| d.body()) else { return };
        let style = body.style();
        if lab.fs.get() {
            page_overflow.set_value(Some(style.get_property_value("overflow").unwrap_or_default()));
            let _ = style.set_property("overflow", "hidden");
        } else if let Some(old) = page_overflow.try_update_value(Option::take).flatten() {
            let _ = style.set_property("overflow", &old);
        }
    });
    on_cleanup(move || {
        if let (Some(old), Some(body)) = (page_overflow.try_update_value(Option::take).flatten(), web_sys::window().and_then(|w| w.document()).and_then(|d| d.body())) {
            let _ = body.style().set_property("overflow", &old);
        }
    });
    dom::on_window(ev::keydown, move |e| {
        if e.key() == "Escape" && lab.fs.get_untracked() {
            lab.fs.set(false);
        }
    });

    let verdict = Signal::derive(move || verdict_text(solved_before, solved.get()).to_owned());
    let (has_next, on_next) = (props.has_next, props.on_next);
    let side = move || view! { <Goals lab=lab verdict=verdict has_next=has_next on_next=on_next /> <Metrics lab=lab /> };
    view! {
        {move || {
            if lab.fs.get() {
                // на весь экран — поверх страницы, вне её вёрстки
                view! {
                    <Portal>
                        <div class="sd fs">
                            <div class="sd-fs-main">
                                <BoardCard lab=lab fullscreen=true />
                            </div>
                            <div class="sd-side">{side()}</div>
                        </div>
                    </Portal>
                }
                .into_any()
            } else {
                view! {
                    <div class="sd">
                        <div class="sd-work">
                            <BoardCard lab=lab fullscreen=false />
                        </div>
                        <div class="sd-bottom">{side()}</div>
                    </div>
                }
                .into_any()
            }
        }}
    }
    .into_any()
}

/// Карточка поля: нагрузка, инструменты, подсказка, само поле и сообщения под ним.
#[component]
fn BoardCard(lab: Lab, fullscreen: bool) -> impl IntoView {
    let edge_hint = move || {
        let e = lab.sel_edge.get()?;
        let name = |id: &str| lab.state.with(|s| s.node(id).map_or_else(|| id.to_owned(), |n| n.name.clone()));
        Some(format!("Связь «{} → {}» выбрана — «Удалить» уберёт её.", name(&e.from), name(&e.to)))
    };
    view! {
        <div class="sd-boardcard">
            <Chips lab=lab />
            <Toolbar lab=lab />
            {move || lab.hint_open.get().then(|| view! { <p class="sd-hint">{lab.hint.get_value()}</p> })}
            <Board lab=lab fullscreen=fullscreen corner=move || view! { <Corner lab=lab /> } overlay=move || view! { <Overlay lab=lab /> } />
            {move || {
                let n = lab.notice.get();
                (!n.is_empty()).then(|| view! { <p class="sd-notice">{n}</p> })
            }}
            {move || edge_hint().map(|t| view! { <p class="sd-hint">{t}</p> })}
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn verdict_distinguishes_old_new_and_pending_solutions() {
        assert_eq!(verdict_text(true, true), "Упражнение уже было решено.");
        assert_eq!(verdict_text(false, true), "Упражнение засчитано.");
        assert_eq!(verdict_text(false, false), "Проверяю решение на сервере…");
    }
}
