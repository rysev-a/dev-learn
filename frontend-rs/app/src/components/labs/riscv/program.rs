//! Левая колонка лаборатории: карточка «Программа» (редактор, подсказка, ошибки ассемблера) и листинг «Машинный код».

use highlight::Lang;
use leptos::prelude::*;

use super::{
    format::{listing_rows, ListingRow},
    session::Session,
};
use crate::components::code_editor::CodeEditor;

/// Данные задания (секция `.data`): доступны по меткам, менять нельзя.
#[component]
pub fn TaskData(data: String) -> impl IntoView {
    (!data.trim().is_empty()).then(|| {
        view! {
            <div class="lab-card">
                <p class="lab-data-title">"Данные задания (доступны по меткам, менять нельзя):"</p>
                <pre class="lab-data mono">{data}</pre>
            </div>
        }
    })
}

/// Карточка «Программа»: кнопки, подсказка, редактор с подсветкой и ошибки по строкам.
#[component]
pub fn ProgramCard(session: Session, hint: String, #[prop(into)] solved: Signal<bool>) -> impl IntoView {
    let has_hint = !hint.is_empty();
    let errors = move || {
        let errors = session.asm.with(|a| a.errors.clone());
        (!errors.is_empty()).then(|| {
            view! {
                <ul class="lab-errors" role="alert">
                    {errors
                        .into_iter()
                        .map(|e| view! { <li><strong>{format!("Строка {}:", e.line)}</strong>" "{e.message}</li> })
                        .collect_view()}
                </ul>
            }
        })
    };
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <h3>"Программа"</h3>
                <div class="lab-actions">
                    {has_hint.then(|| view! {
                        <button type="button" class="quiz-btn ghost" on:click=move |_| session.hint_open.update(|o| *o = !*o)>
                            {move || if session.hint_open.get() { "Скрыть подсказку" } else { "Подсказка" }}
                        </button>
                    })}
                    <button type="button" class="quiz-btn ghost" on:click=move |_| session.restart()>"Начать заново"</button>
                </div>
            </div>
            {move || (has_hint && session.hint_open.get()).then(|| view! { <p class="ex-hint">{hint.clone()}</p> })}
            <CodeEditor
                value=session.source
                on_input=Callback::new(move |text| session.edit(text))
                on_run=Callback::new(move |()| session.run())
                lang=Lang::Asm
                accepted=solved
                autofocus=false
            />
            {errors}
        </div>
    }
}

/// Листинг: что ассемблер сделал из программы — по настоящему 32-битному слову на команду, поля раскрашены.
#[component]
pub fn ListingCard(session: Session) -> impl IntoView {
    let rows = Memo::new(move |_| session.asm.with(|a| listing_rows(&a.lines)));
    let pc = Memo::new(move |_| session.status.with(|s| s.as_ref().map(|s| s.pc)));
    let body = move || {
        let rows = rows.get();
        if rows.is_empty() {
            return view! { <p class="lab-muted">"Команд пока нет."</p> }.into_any();
        }
        view! {
            <div class="lab-scroll">
                <table class="lab-table">
                    <thead>
                        <tr>
                            <th>"адрес"</th>
                            <th>"hex"</th>
                            <th class="left">"поля (старшие биты слева)"</th>
                            <th class="left">"команда"</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.into_iter().map(|row| view! { <ListingLine row=row session=session pc=pc /> }).collect_view()}
                    </tbody>
                </table>
            </div>
        }
        .into_any()
    };
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>"Машинный код"</h3>
                    <p>
                        "Что ассемблер сделал из вашей программы: каждая команда — одно настоящее 32-битное слово RISC-V. \
                         Цветом выделены поля; нажмите на строку, чтобы увидеть формат команды."
                    </p>
                </div>
            </div>
            {body}
        </div>
    }
}

/// Строка листинга; по клику под ней раскрывается легенда полей.
#[component]
fn ListingLine(row: ListingRow, session: Session, pc: Memo<Option<u32>>) -> impl IntoView {
    let addr = row.addr;
    let fields = |row: &ListingRow| {
        row.fields
            .iter()
            .map(|f| view! { <span class=format!("fld {}", f.cls) title=f.name.clone()>{f.bits.clone()}</span> })
            .collect_view()
    };
    let bits = fields(&row);
    let legend = {
        let (fmt, row) = (row.fmt, row.clone());
        move || {
            let items = row
                .fields
                .iter()
                .map(|f| view! { <span class="lab-legend-item"><span class=format!("fld {}", f.cls)>{f.bits.clone()}</span>{format!(" {}", f.name)}</span> })
                .collect_view();
            view! {
                <tr class="explain-row">
                    <td colspan="4">
                        <div class="lab-legend"><strong>{format!("Формат {fmt}.")}</strong>{items}</div>
                    </td>
                </tr>
            }
        }
    };
    view! {
        <tr
            class:current=move || pc.get() == Some(addr)
            class:selected=move || session.selected.get() == Some(addr)
            class:pseudo=row.pseudo
            on:click=move |_| session.selected.update(|s| *s = if *s == Some(addr) { None } else { Some(addr) })
        >
            <td class="mono">{row.addr_hex}</td>
            <td class="mono">{row.word_hex}</td>
            <td class="left mono lab-fields">{bits}</td>
            <td class="left mono">{row.text}</td>
        </tr>
        {move || (session.selected.get() == Some(addr)).then(&legend)}
    }
}
