//! Нижние карточки лаборатории: «Собрать у себя на компьютере» (профиль «настоящая программа») и справочник команд.

use leptos::prelude::*;
use riscvlab::{
    isa::{Ext, OPS, PSEUDO},
    project::{make_zip, project_files, project_zip},
};

use super::{
    download::{save_bytes, save_text},
    session::Session,
};

/// Имя архива проекта.
const ZIP_NAME: &str = "riscv-program.zip";

/// Проект для сборки на своём компьютере: файлы, просмотр содержимого и скачивание (отдельным файлом и архивом).
#[component]
pub fn ProjectCard(session: Session) -> impl IntoView {
    let files = Memo::new(move |_| project_files(&session.source.get()));
    let open = RwSignal::new("program.s".to_string());
    let shown = Memo::new(move |_| files.with(|f| f.iter().find(|x| x.name == open.get()).or_else(|| f.first()).cloned()));
    let download_zip = move |_| {
        let bytes = make_zip(&project_zip(&files.get_untracked()));
        let _ = save_bytes(&bytes, "application/zip", ZIP_NAME);
    };
    let tabs = move || {
        files
            .get()
            .into_iter()
            .map(|f| {
                let name = f.name.clone();
                let on = f.name.clone();
                view! { <button type="button" class:on=move || shown.get().is_some_and(|s| s.name == on) on:click=move |_| open.set(name.clone())>{f.name}</button> }
            })
            .collect_view()
    };
    let file = move || {
        let f = shown.get()?;
        let (name, content) = (f.name.clone(), f.content.clone());
        Some(view! {
            <p class="lab-muted">
                {f.note.clone()}" "
                <button type="button" class="quiz-btn ghost" on:click=move |_| { let _ = save_text(&content, &name); }>{format!("Скачать {}", f.name)}</button>
            </p>
            <pre class="lab-data mono lab-file">{f.content}</pre>
        })
    };
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>"Собрать у себя на компьютере"</h3>
                    <p>
                        "Эта программа — обычный файл на ассемблере RISC-V. Скачайте проект, установите инструменты (команды — в README) \
                         и выполните "<span class="mono">"make run"</span>": настоящий компилятор превратит текст в те же 32-битные слова, \
                         что в листинге выше, а qemu выполнит их."
                    </p>
                </div>
                <button type="button" class="quiz-btn" on:click=download_zip>"Скачать проект (.zip)"</button>
            </div>
            <div class="lab-seg" role="group" aria-label="Файлы проекта">{tabs}</div>
            {file}
        </div>
    }
}

/// Справочник: команды RV32IM и псевдокоманды.
#[component]
pub fn ReferenceCard() -> impl IntoView {
    let ops = OPS
        .iter()
        .map(|o| {
            let fmt = format!("{:?}{}", o.fmt, if o.ext == Ext::M { " · M" } else { "" });
            view! {
                <tr>
                    <td class="left mono"><strong>{o.mnemonic}</strong></td>
                    <td class="left mono">{o.example}</td>
                    <td class="left">{o.meaning}</td>
                    <td class="mono">{fmt}</td>
                </tr>
            }
        })
        .collect_view();
    let pseudo = PSEUDO
        .iter()
        .map(|p| view! { <tr><td class="left mono"><strong>{p.example}</strong></td><td class="left mono">{format!("= {}", p.becomes)}</td></tr> })
        .collect_view();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>"Справочник: команды RISC-V (RV32IM)"</h3>
                    <p>
                        "32 регистра по 32 бита; x0 (zero) всегда равен нулю. У регистров есть «ABI-имена»: a0…a7 — аргументы и результат, \
                         t0…t6 — временные, s0…s11 — «неприкосновенные» (функция обязана вернуть их как были), ra — адрес возврата, sp — стек. \
                         Комментарии — после «#». Метки — «имя:»."
                    </p>
                </div>
            </div>
            <div class="lab-scroll">
                <table class="lab-table ref">
                    <thead>
                        <tr>
                            <th class="left">"команда"</th>
                            <th class="left">"пример"</th>
                            <th class="left">"что делает"</th>
                            <th>"формат"</th>
                        </tr>
                    </thead>
                    <tbody>{ops}</tbody>
                </table>
                <h4 class="lab-ref-sub">"Псевдокоманды — сокращения, которые ассемблер разворачивает сам"</h4>
                <table class="lab-table ref"><tbody>{pseudo}</tbody></table>
            </div>
        </div>
    }
}
