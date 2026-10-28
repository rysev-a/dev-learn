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
                <button type="button" class="quiz-btn ghost" on:click=move |_| { let _ = save_text(&content, &name); }>{i18n::trf!("Download {0}", f.name)}</button>
            </p>
            <pre class="lab-data mono lab-file">{f.content}</pre>
        })
    };
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>{i18n::tr("Build on your own computer")}</h3>
                    <p>
                        {i18n::tr("This program is a plain RISC-V assembly file. Download the project, install the tools (commands are in the README) and run ")}<span class="mono">"make run"</span>{i18n::tr(": a real compiler will turn the text into the same 32-bit words as in the listing above, and qemu will run them.")}
                    </p>
                </div>
                <button type="button" class="quiz-btn" on:click=download_zip>{i18n::tr("Download project (.zip)")}</button>
            </div>
            <div class="lab-seg" role="group" aria-label=i18n::tr("Project files")>{tabs}</div>
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
                    <td class="left mono">{i18n::tr(o.example)}</td>
                    <td class="left">{i18n::tr(o.meaning)}</td>
                    <td class="mono">{fmt}</td>
                </tr>
            }
        })
        .collect_view();
    let pseudo = PSEUDO
        .iter()
        .map(|p| view! { <tr><td class="left mono"><strong>{i18n::tr(p.example)}</strong></td><td class="left mono">{format!("= {}", i18n::tr(p.becomes))}</td></tr> })
        .collect_view();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>{i18n::tr("Reference: RISC-V instructions (RV32IM)")}</h3>
                    <p>
                        {i18n::tr("32 registers of 32 bits each; x0 (zero) is always zero. Registers have “ABI names”: a0…a7 — arguments and result, t0…t6 — temporaries, s0…s11 — “saved” (a function must return them unchanged), ra — return address, sp — stack. Comments start with “#”. Labels are “name:”.")}
                    </p>
                </div>
            </div>
            <div class="lab-scroll">
                <table class="lab-table ref">
                    <thead>
                        <tr>
                            <th class="left">{i18n::tr("instruction")}</th>
                            <th class="left">{i18n::tr("example")}</th>
                            <th class="left">{i18n::tr("what it does")}</th>
                            <th>{i18n::tr("format")}</th>
                        </tr>
                    </thead>
                    <tbody>{ops}</tbody>
                </table>
                <h4 class="lab-ref-sub">{i18n::tr("Pseudo-instructions — shortcuts the assembler expands by itself")}</h4>
                <table class="lab-table ref"><tbody>{pseudo}</tbody></table>
            </div>
        </div>
    }
}
