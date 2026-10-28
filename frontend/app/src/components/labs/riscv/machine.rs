//! Правая колонка лаборатории: процессор, итог проверки, периферия или вывод программы, окно памяти.

use leptos::prelude::*;
use riscvlab::machine::MMIO_MAP;

use super::{
    format::{exit_code_text, hex_addr, led_cells, mem_rows, reg_rows, switches_of, Status, MemRow, RunResult, WINDOWS, WINDOW_BYTES},
    session::Session,
};

/// Карточка «Процессор RV32IM»: кнопки, 32 регистра и строка состояния.
#[component]
pub fn CpuCard(session: Session) -> impl IntoView {
    let can_step = Memo::new(move |_| session.status.with(|s| s.as_ref().is_some_and(Status::can_step)));
    let body = move || match session.status.get() {
        None => view! { <p class="lab-muted">{i18n::tr("Fix the errors in the program — then you can run it.")}</p> }.into_any(),
        Some(st) => {
            let regs = reg_rows(&st.regs, st.last_reg)
                .into_iter()
                .map(|r| {
                    let title = format!("x{} = 0x{}", r.num, r.hex);
                    view! {
                        <div class="lab-reg" class:changed=r.changed title=title>
                            <span class="lab-reg-name">{r.name}" "<small>{format!("x{}", r.num)}</small></span>
                            <span class="lab-reg-val mono">{r.signed}</span>
                            <span class="lab-reg-hex mono">{r.hex}</span>
                        </div>
                    }
                })
                .collect_view();
            view! {
                <div class="lab-regs rv32">{regs}</div>
                <div class="lab-status">
                    <span class="lab-badge">{format!("pc = 0x{}", hex_addr(st.pc))}</span>
                    <span class="lab-badge">{i18n::trf!("instructions executed: {0}", st.steps)}</span>
                    {(!st.last_insn.is_empty()).then(|| view! { <span class="lab-badge mono">{st.last_insn.clone()}</span> })}
                    {st.halted.then(|| view! { <span class="lab-badge ok">{i18n::tr("halted")}</span> })}
                </div>
            }
            .into_any()
        }
    };
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <h3>{i18n::tr("RV32IM processor")}</h3>
                <div class="lab-actions">
                    <button type="button" class="quiz-btn" prop:disabled=move || !can_step.get() on:click=move |_| session.step()>{i18n::tr("Step ▸")}</button>
                    <button type="button" class="quiz-btn ghost" prop:disabled=move || !can_step.get() on:click=move |_| session.run()>{i18n::tr("Run")}</button>
                    <button type="button" class="quiz-btn ghost" on:click=move |_| session.reset()>{i18n::tr("Reset")}</button>
                </div>
            </div>
            {body}
        </div>
    }
}

/// Итог проверки: плашка видна, только когда программа остановилась.
#[component]
pub fn ResultAlert(#[prop(into)] result: Signal<Option<RunResult>>, on_next: Callback<()>, #[prop(into)] has_next: Signal<bool>) -> impl IntoView {
    move || {
        let r = result.get()?;
        let ok = r.ok;
        let icon = if ok { "M20 6 9 17l-5-5" } else { "M18 6 6 18M6 6l12 12" };
        Some(view! {
            <div class="lab-alert" class:ok=ok class:bad=!ok role="status">
                <span class="lab-alert-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d=icon /></svg></span>
                <div class="lab-alert-body">
                    <p class="lab-alert-title">{if ok { i18n::tr("Exercise complete!") } else { i18n::tr("Not there yet") }}</p>
                    {(!r.message.is_empty()).then(|| view! { <p class="lab-alert-text">{r.message.clone()}</p> })}
                </div>
                {(ok && has_next.get()).then(|| view! {
                    <button type="button" class="lab-alert-next" on:click=move |_| on_next.run(())>
                        {i18n::tr("Next")}
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7" /></svg>
                    </button>
                })}
            </div>
        })
    }
}

/// Консоль: всё, что программа вывела, и мигающий курсор.
#[component]
fn Console(session: Session) -> impl IntoView {
    view! {
        <pre class="lab-console mono">
            {move || session.status.with(|s| s.as_ref().map(|s| s.uart.clone()).unwrap_or_default())}
            <span class="lab-caret">"▮"</span>
        </pre>
    }
}

/// Ряд из восьми «лампочек» (светодиоды или переключатели): номер и горит ли.
#[component]
fn Lamps(label: &'static str, prefix: &'static str, #[prop(into)] bits: Signal<u8>, switch: bool) -> impl IntoView {
    view! {
        <span class="lab-leds" aria-label=label>
            {move || {
                led_cells(bits.get())
                    .into_iter()
                    .map(|(i, on)| view! { <span class="lab-led" class:sw=switch class:on=on title=format!("{prefix}{i}")>{i}</span> })
                    .collect_view()
            }}
        </span>
    }
}

/// Карточка «Периферия» (профиль «плата»): светодиоды, переключатели, таймер, консоль UART и карта адресов.
#[component]
pub fn PeripheralsCard(session: Session) -> impl IntoView {
    let leds = Memo::new(move |_| session.status.with(|s| s.as_ref().map_or(0, |s| s.leds)));
    let steps = move || session.status.with(|s| s.as_ref().map_or(0, |s| s.steps));
    let switches = session.spec.with_value(switches_of);
    let map = MMIO_MAP
        .iter()
        .map(|m| {
            view! {
                <tr>
                    <td class="left mono">{format!("0x{:x}", m.addr)}</td>
                    <td class="left"><strong>{i18n::tr(m.name)}</strong>{format!(" — {}", i18n::tr(m.note))}</td>
                </tr>
            }
        })
        .collect_view();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>{i18n::tr("Peripherals")}</h3>
                    <p>
                        {i18n::tr("Devices are connected to the same buses as memory and appear to the program as ordinary addresses. Writing or reading such an address is a conversation with the device.")}
                    </p>
                </div>
            </div>
            <div class="lab-dev">
                <span class="lab-dev-name">{i18n::tr("LEDs")}</span>
                <Lamps label=i18n::tr("LEDs") prefix="LED" bits=leds switch=false />
            </div>
            <div class="lab-dev">
                <span class="lab-dev-name">{i18n::tr("Switches")}</span>
                <Lamps label=i18n::tr("Switches") prefix="SW" bits=Signal::stored(switches) switch=true />
            </div>
            <div class="lab-dev">
                <span class="lab-dev-name">{i18n::tr("Timer")}</span>
                <span class="mono">{steps}</span>
            </div>
            <p class="lab-data-title">{i18n::tr("Console (UART):")}</p>
            <Console session=session />
            <table class="lab-table ref"><tbody>{map}</tbody></table>
        </div>
    }
}

/// Карточка «Вывод программы» (профиль «настоящая программа»): стандартный вывод и код возврата.
#[component]
pub fn OutputCard(session: Session) -> impl IntoView {
    let exit = move || session.status.with(|s| s.as_ref().and_then(|s| s.exit_code));
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <div>
                    <h3>{i18n::tr("Program output")}</h3>
                    <p>
                        {i18n::tr("Everything the program sent to standard output with the write system call. When it calls exit, the exit code is shown here too.")}
                    </p>
                </div>
            </div>
            <Console session=session />
            {move || exit().map(|code| view! { <p class="lab-exit mono">{exit_code_text(code)}</p> })}
        </div>
    }
}

/// Карточка «Память»: три окна по 256 байт; зелёным — последний записанный байт, синим — прочитанный.
#[component]
pub fn MemoryCard(session: Session) -> impl IntoView {
    let rows = Memo::new(move |_| {
        let base = WINDOWS.get(session.window.get()).unwrap_or(&WINDOWS[0]).from;
        session.memory(|mem, read, write| mem_rows(mem, base, (WINDOW_BYTES / 16) as usize, read, write))
    });
    let tabs = WINDOWS
        .iter()
        .enumerate()
        .map(|(i, w)| view! { <button type="button" class:on=move || session.window.get() == i on:click=move |_| session.window.set(i)>{i18n::tr(w.title)}</button> })
        .collect_view();
    view! {
        <div class="lab-card">
            <div class="lab-card-head">
                <h3>{i18n::tr("Memory")}</h3>
                <div class="lab-seg" role="group" aria-label=i18n::tr("Memory window")>{tabs}</div>
            </div>
            <p class="lab-muted">
                {i18n::tr("A 256-byte window. Green is the last byte written, blue is the byte read. Words are stored “low byte first” (little-endian).")}
            </p>
            <MemoryGrid rows=rows />
        </div>
    }
}

/// Сетка памяти: адрес строки, шестнадцатеричные байты и текстовое представление.
#[component]
fn MemoryGrid(rows: Memo<Vec<MemRow>>) -> impl IntoView {
    let heads = (0..16).map(|i| view! { <span>{format!("{i:X}")}</span> }).collect_view();
    let body = move || {
        rows.get()
            .into_iter()
            .map(|row| {
                let cells = row
                    .cells
                    .iter()
                    .map(|c| view! { <span class=c.class() title=i18n::trf!("address 0x{0}", hex_addr(c.addr))>{c.hex.clone()}</span> })
                    .collect_view();
                let ascii = row
                    .cells
                    .iter()
                    .map(|c| view! { <span class:dot=c.ch == '·'>{c.ch.to_string()}</span> })
                    .collect_view();
                view! {
                    <div class="lab-disk-row">
                        <span class="lab-addr">{hex_addr(row.addr)}</span>
                        {cells}
                        <span class="lab-ascii">{ascii}</span>
                    </div>
                }
            })
            .collect_view()
    };
    view! {
        <div class="lab-disk lab-mem mono">
            <div class="lab-disk-head"><span></span>{heads}<span class="lab-ascii-head">{i18n::tr("text")}</span></div>
            {body}
        </div>
    }
}
