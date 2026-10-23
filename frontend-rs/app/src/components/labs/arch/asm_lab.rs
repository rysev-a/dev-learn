//! Ассемблер процессора «Мини-8»: пишем программу, смотрим машинный код и запускаем её на виртуальном диске в
//! эмуляторе или на процессоре, собранном из вентилей (`AsmLab.tsx`, `AsmShared.tsx`).

use std::sync::Arc;

use archlab::{
    asm::{
        assemble,
        isa::{fields, OPS, PSEUDO, REG_COUNT},
        machine::RUN_LIMIT,
        tasks::{compare, hex},
        AsmResult, Machine, MachineView,
    },
    cpu8::GateMachine,
    exercise::{AsmSpec, DiskRegion},
};
use leptos::prelude::*;

use super::{common::ResultAlert, cpu::CpuInspector};
use crate::components::labs::LabProps;

/// Ячеек памяти в строке сетки.
const ROW_LEN: usize = 16;

/// Чем выполняется программа.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Engine {
    /// быстрая программа-эмулятор
    Emu,
    /// тот же процессор, собранный из вентилей
    Gates,
}

/// Машина выбранного вида.
pub enum Sim {
    Emu(Box<Machine>),
    Gates(Box<GateMachine>),
}

impl Sim {
    /// Новая машина с программой и диском; процессор на вентилях может не собраться — тогда причина.
    pub fn build(engine: Engine, asm: &AsmResult, disk: &[u8]) -> Result<Option<Sim>, String> {
        if !asm.errors.is_empty() {
            return Ok(None);
        }
        Ok(Some(match engine {
            Engine::Emu => Sim::Emu(Box::new(Machine::new(&asm.words, disk))),
            Engine::Gates => Sim::Gates(Box::new(GateMachine::new(&asm.words, disk)?)),
        }))
    }

    pub fn step(&mut self) {
        match self {
            Sim::Emu(m) => m.step(),
            Sim::Gates(m) => m.step(),
        }
    }

    pub fn run(&mut self, limit: u64) {
        match self {
            Sim::Emu(m) => m.run(limit),
            Sim::Gates(m) => m.run(limit),
        }
    }

    pub fn view(&self) -> MachineView {
        match self {
            Sim::Emu(m) => m.view(),
            Sim::Gates(m) => m.view(),
        }
    }
}

/// Итог задания по состоянию машины: ошибка, «ещё работает» (`None`) или сверка диска с ожидаемым.
pub fn task_result(view: &MachineView, expected: &[u8]) -> Option<(bool, String)> {
    if let Some(err) = &view.error {
        return Some((false, err.clone()));
    }
    view.halted.then(|| {
        let r = compare(&view.mem, expected);
        (r.ok, r.message)
    })
}

/// Ячейка сетки памяти.
#[derive(Clone, Debug, PartialEq)]
pub struct MemCell {
    pub addr: usize,
    pub hex: String,
    pub ch: char,
    /// байт отличается от исходного содержимого диска
    pub changed: bool,
    pub read: bool,
    pub written: bool,
    /// номер области диска; `None` — вне областей
    pub region: Option<usize>,
}

/// Номер области диска, в которую попал адрес.
pub fn region_of(regions: &[DiskRegion], addr: usize) -> Option<usize> {
    regions.iter().position(|r| addr >= r.from && addr < r.from + r.length)
}

/// Сетка памяти из строк по 16 байт: что изменила программа, что прочла и что записала последним.
pub fn memory_rows(mem: &[u8], disk: &[u8], view: Option<&MachineView>, regions: &[DiskRegion], rows: usize) -> Vec<(usize, Vec<MemCell>)> {
    (0..rows)
        .map(|row| {
            let cells = (0..ROW_LEN)
                .map(|col| {
                    let addr = row * ROW_LEN + col;
                    let b = mem.get(addr).copied().unwrap_or(0);
                    MemCell {
                        addr,
                        hex: format!("{b:02X}"),
                        ch: if (32..127).contains(&b) { char::from(b) } else { '·' },
                        changed: Some(&b) != disk.get(addr),
                        read: view.is_some_and(|v| v.last_read == Some(addr)),
                        written: view.is_some_and(|v| v.last_write == Some(addr)),
                        region: region_of(regions, addr),
                    }
                })
                .collect();
            (row * ROW_LEN, cells)
        })
        .collect()
}

/// Класс ячейки сетки.
pub fn cell_class(c: &MemCell) -> String {
    let mut out = String::from("lab-cell");
    if let Some(r) = c.region {
        out.push_str(&format!(" rg{r}"));
    }
    for (on, name) in [(c.changed, "changed"), (c.read, "read"), (c.written, "written")] {
        if on {
            out.push(' ');
            out.push_str(name);
        }
    }
    out
}

/// Сетка памяти: адрес строки, шестнадцатеричные байты и текстовое представление.
#[component]
pub fn MemoryGrid(#[prop(into)] rows: Signal<Vec<(usize, Vec<MemCell>)>>) -> impl IntoView {
    view! {
        <div class="lab-disk mono">
            <div class="lab-disk-head">
                <span></span>
                {(0..ROW_LEN).map(|i| view! { <span>{format!("{i:X}")}</span> }).collect_view()}
                <span class="lab-ascii-head">"текст"</span>
            </div>
            {move || rows.get().into_iter().map(|(addr, cells)| view! {
                <div class="lab-disk-row">
                    <span class="lab-addr">{format!("{addr:02X}")}</span>
                    {cells.iter().map(|c| view! { <span class=cell_class(c) title=format!("адрес 0x{:02X}", c.addr)>{c.hex.clone()}</span> }).collect_view()}
                    <span class="lab-ascii">{cells.iter().map(|c| view! { <span class=if c.ch == '·' { "dot" } else { "" }>{c.ch.to_string()}</span> }).collect_view()}</span>
                </div>
            }).collect_view()}
        </div>
    }
}

/// Ассемблер Мини-8: упражнение главы 15.
#[component]
pub fn AsmLab(props: LabProps, spec: Arc<AsmSpec>) -> impl IntoView {
    let LabProps { task, draft, on_draft, solved, report, on_next, has_next } = props;
    let initial = draft.get_untracked();
    let source = RwSignal::new(if initial.trim().is_empty() { spec.starter.clone() } else { initial });
    let engine = RwSignal::new(Engine::Emu);
    let reset_key = RwSignal::new(0u32);
    let hint_open = RwSignal::new(false);
    let selected = RwSignal::new(None::<usize>);
    let asm = Memo::new(move |_| source.with(|s| assemble(s)));

    // машина создаётся заново при изменении программы, смене процессора и «Сбросить»
    let disk_bytes = spec.disk.0.clone();
    let build = {
        let disk = disk_bytes.clone();
        move || match asm.with_untracked(|a| Sim::build(engine.get_untracked(), a, &disk)) {
            Ok(s) => (s, None),
            Err(e) => (None, Some(e)),
        }
    };
    let (first_sim, first_error) = build();
    let sim: RwSignal<Option<Sim>> = RwSignal::new(first_sim);
    let sim_error = RwSignal::new(first_error);
    Effect::new(move |prev: Option<()>| {
        reset_key.track();
        asm.track();
        engine.track();
        if prev.is_some() {
            let (built, error) = build();
            sim.set(built);
            sim_error.set(error);
        }
    });

    let view = Memo::new(move |_| sim.with(|s| s.as_ref().map(Sim::view)));
    let expected = spec.expected.0.clone();
    let result = {
        let expected = expected.clone();
        Memo::new(move |_| view.with(|v| v.as_ref().and_then(|v| task_result(v, &expected))))
    };
    let can_step = move || view.with(|v| v.as_ref().is_some_and(|v| !v.halted && v.error.is_none()));
    let reported = StoredValue::new(solved.get_untracked());
    Effect::new(move |_| {
        if result.with(|r| r.as_ref().is_some_and(|r| r.0)) && !reported.get_value() {
            reported.set_value(true);
            report.run(source.get_untracked());
        }
    });

    let edit = move |text: String| {
        selected.set(None);
        source.set(text.clone());
        on_draft.run(text);
    };
    let restart = {
        let starter = spec.starter.clone();
        move |_| edit(starter.clone())
    };
    // Tab в редакторе — два пробела, а не уход фокуса
    let on_key = move |e: web_sys::KeyboardEvent| {
        if e.key() != "Tab" {
            return;
        }
        e.prevent_default();
        let el = event_target::<web_sys::HtmlTextAreaElement>(&e);
        let (start, end) = (el.selection_start().ok().flatten().unwrap_or(0) as usize, el.selection_end().ok().flatten().unwrap_or(0) as usize);
        let text = el.value();
        let (head, tail): (String, String) = (text.chars().take(start).collect(), text.chars().skip(end).collect());
        let next = format!("{head}  {tail}");
        el.set_value(&next);
        let _ = el.set_selection_start(Some((start + 2) as u32));
        let _ = el.set_selection_end(Some((start + 2) as u32));
        edit(next);
    };

    let step = move |_| {
        sim.update(|s| {
            if let Some(s) = s {
                s.step();
            }
        })
    };
    let run = move |_| {
        sim.update(|s| {
            if let Some(s) = s {
                s.run(RUN_LIMIT);
            }
        })
    };

    // листинг машинного кода
    let listing = move || {
        let pc = view.with(|v| v.as_ref().map(|v| v.pc));
        asm.with(|a| {
            a.lines
                .iter()
                .map(|l| {
                    let (op, ra, rb, rc) = fields(l.word);
                    let (addr, text) = (l.addr, l.text.clone());
                    let current = pc == Some(addr as i32);
                    view! {
                        <tr class:current=current class:selected=move || selected.get() == Some(addr) on:click=move |_| selected.update(|s| *s = if *s == Some(addr) { None } else { Some(addr) })>
                            <td>{addr}</td>
                            <td class="mono">{format!("{:04x}", l.word)}</td>
                            <td class="mono f-op">{op}</td>
                            <td class="mono f-a">{ra}</td>
                            <td class="mono f-b">{rb}</td>
                            <td class="mono f-c">{rc}</td>
                            <td class="left mono">{text}</td>
                        </tr>
                    }
                })
                .collect_view()
        })
    };

    let regions = spec.regions.clone();
    let disk = spec.disk.0.clone();
    let grid = {
        let (regions, disk) = (regions.clone(), disk.clone());
        Signal::derive(move || {
            let v = view.get();
            let mem = v.as_ref().map_or_else(|| disk.clone(), |v| v.mem.clone());
            memory_rows(&mem, &disk, v.as_ref(), &regions, 16)
        })
    };
    let regs = move || {
        let v = view.get();
        (0..REG_COUNT)
            .map(|i| {
                let val = v.as_ref().and_then(|v| v.regs.get(i).copied()).unwrap_or(0);
                let changed = v.as_ref().is_some_and(|v| v.last_reg == Some(i));
                view! {
                    <div class="lab-reg" class:changed=changed>
                        <span class="lab-reg-name">{format!("r{i}")}</span>
                        <span class="lab-reg-val mono">{val}</span>
                        <span class="lab-reg-hex mono">{format!("0x{val:02X}")}</span>
                    </div>
                }
            })
            .collect_view()
    };

    let hint = task.hint.clone();
    let region_chips = regions.iter().enumerate().map(|(i, r)| view! { <span class=format!("lab-region rg{i}")>{format!("{} · {}", r.name, hex(r.from as u8))}</span> }).collect_view();
    let ops = OPS
        .iter()
        .map(|o| {
            view! {
                <tr>
                    <td class="left mono"><strong>{o.mnemonic}</strong></td>
                    <td class="left mono">{o.example}</td>
                    <td class="left">{o.meaning}</td>
                    <td class="mono">{format!("{:04b}", o.opcode)}</td>
                </tr>
            }
        })
        .collect_view();
    let pseudo = PSEUDO.iter().map(|p| view! { <tr><td class="left mono"><strong>{p.example}</strong></td><td class="left mono">{format!("= {}", p.becomes)}</td></tr> }).collect_view();

    view! {
        <div class="lab lab-asm">
            <div class="lab-asm-grid">
                <section class="lab-col">
                    <div class="lab-card">
                        <div class="lab-card-head">
                            <h3>"Программа"</h3>
                            <div class="lab-actions">
                                <button type="button" class="quiz-btn ghost" on:click=move |_| hint_open.update(|v| *v = !*v)>{move || if hint_open.get() { "Скрыть подсказку" } else { "Подсказка" }}</button>
                                <button type="button" class="quiz-btn ghost" on:click=restart>"Начать заново"</button>
                            </div>
                        </div>
                        {move || hint_open.get().then(|| view! { <p class="ex-hint">{hint.clone()}</p> })}
                        <textarea
                            class="lab-editor"
                            spellcheck="false"
                            rows="16"
                            aria-label="Текст программы на ассемблере"
                            prop:value=move || source.get()
                            on:input=move |e| edit(event_target_value(&e))
                            on:keydown=on_key
                        ></textarea>
                        {move || {
                            let errors = asm.with(|a| a.errors.clone());
                            (!errors.is_empty()).then(|| view! {
                                <ul class="lab-errors" role="alert">
                                    {errors.into_iter().map(|e| view! { <li><strong>{format!("Строка {}:", e.line)}</strong>{format!(" {}", e.message)}</li> }).collect_view()}
                                </ul>
                            })
                        }}
                    </div>

                    <div class="lab-card">
                        <div class="lab-card-head">
                            <div>
                                <h3>"Машинный код"</h3>
                                <p>"Что ассемблер сделал из вашей программы: каждая команда — одно 16-битное слово из полей «код · A · B · C». Нажмите на строку, чтобы разобрать её по битам."</p>
                            </div>
                        </div>
                        {move || if asm.with(|a| a.lines.is_empty()) {
                            view! { <p class="lab-muted">"Команд пока нет."</p> }.into_any()
                        } else {
                            view! {
                                <div class="lab-scroll">
                                    <table class="lab-table">
                                        <thead>
                                            <tr><th>"адрес"</th><th>"hex"</th><th>"код"</th><th>"A"</th><th>"B"</th><th>"C"</th><th class="left">"команда"</th></tr>
                                        </thead>
                                        <tbody>{listing}</tbody>
                                    </table>
                                </div>
                            }.into_any()
                        }}
                        {move || selected.get().is_some().then(|| view! {
                            <p class="lab-explain">
                                "Первые четыре бита — " <strong>"код операции"</strong>
                                ": по ним процессор понимает, что делать. Дальше поля A, B и C: в зависимости от команды это номера регистров, число или смещение перехода. Подробности — в справочнике ниже."
                            </p>
                        })}
                    </div>
                </section>

                <section class="lab-col">
                    <div class="lab-card">
                        <div class="lab-card-head">
                            <h3>"Процессор"</h3>
                            <div class="lab-seg" role="group" aria-label="Чем выполнять программу">
                                <button type="button" class:on=move || engine.get() == Engine::Emu on:click=move |_| engine.set(Engine::Emu) title="Быстрая программа-эмулятор">"Эмулятор"</button>
                                <button type="button" class:on=move || engine.get() == Engine::Gates on:click=move |_| engine.set(Engine::Gates) title="Тот же процессор, собранный из вентилей: каждая команда считается схемой">"Схема из вентилей"</button>
                            </div>
                            <div class="lab-actions">
                                <button type="button" class="quiz-btn" on:click=step disabled=move || !can_step()>"Шаг ▸"</button>
                                <button type="button" class="quiz-btn ghost" on:click=run disabled=move || !can_step()>"Выполнить"</button>
                                <button type="button" class="quiz-btn ghost" on:click=move |_| reset_key.update(|n| *n += 1)>"Сбросить"</button>
                            </div>
                        </div>
                        {move || match view.get() {
                            Some(v) => view! {
                                <div class="lab-regs">{regs()}</div>
                                <div class="lab-status">
                                    <span class="lab-badge">{format!("следующая команда: {}", v.pc)}</span>
                                    <span class="lab-badge">{format!("выполнено шагов: {}", v.steps)}</span>
                                    {v.halted.then(|| view! { <span class="lab-badge ok">"остановлен (hlt)"</span> })}
                                </div>
                            }.into_any(),
                            None => match sim_error.get() {
                                Some(e) => view! { <p class="lab-muted">{format!("Процессор на вентилях не собрался: {e}")}</p> }.into_any(),
                                None => view! { <p class="lab-muted">"Исправьте ошибки в программе — тогда её можно запустить."</p> }.into_any(),
                            },
                        }}
                    </div>

                    {move || result.get().map(|(ok, message)| view! {
                        <ResultAlert
                            ok=ok
                            title=move || if ok { "Задание выполнено!" } else { "Пока не то" }
                            text=message
                            on_next=(ok && has_next.get()).then_some(on_next)
                        />
                    })}

                    <div class="lab-card">
                        <div class="lab-card-head">
                            <div>
                                <h3>"Виртуальный диск"</h3>
                                <p>"256 байт памяти. Жёлтым подсвечены байты, которые ваша программа изменила; зелёным — записанный последним, синим — прочитанный."</p>
                            </div>
                        </div>
                        <div class="lab-regions">{region_chips}</div>
                        <MemoryGrid rows=grid />
                    </div>
                </section>
            </div>

            {move || (engine.get() == Engine::Gates && sim.with(|s| matches!(s, Some(Sim::Gates(_))))).then(|| view! {
                <div class="lab-card">
                    <div class="lab-card-head">
                        <div>
                            <h3>"Устройство процессора"</h3>
                            <p>
                                "Сейчас программу выполняет не эмулятор, а схема из вентилей: каждый такт в ней — целая команда. Кнопка с лупой на блоке показывает, из чего он собран, "
                                "вплоть до отдельных вентилей; значения на проводах — живые, по текущему шагу."
                            </p>
                        </div>
                    </div>
                    <CpuInspector sim=sim />
                </div>
            })}

            <div class="lab-card">
                <div class="lab-card-head">
                    <div>
                        <h3>"Справочник: команды процессора Мини-8"</h3>
                        <p>
                            "8 регистров r0…r7 (r0 всегда равен нулю), числа — байты 0…255. Команда занимает 16 бит: "
                            <span class="mono">"код(4) · A(3) · B(3) · C(6)"</span>
                            ". Комментарии — после «;». Метки — «имя:» в начале строки; константы — «.equ ИМЯ, число»."
                        </p>
                    </div>
                </div>
                <div class="lab-scroll">
                    <table class="lab-table ref">
                        <thead>
                            <tr><th class="left">"команда"</th><th class="left">"пример"</th><th class="left">"что делает"</th><th>"код"</th></tr>
                        </thead>
                        <tbody>{ops}</tbody>
                    </table>
                    <h4 class="lab-ref-sub">"Псевдокоманды — сокращения, которые ассемблер разворачивает сам"</h4>
                    <table class="lab-table ref"><tbody>{pseudo}</tbody></table>
                </div>
            </div>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use archlab::asm::assemble;

    fn region(name: &str, from: usize, length: usize) -> DiskRegion {
        DiskRegion { name: name.into(), from, length }
    }

    /// Машина после `n` шагов (подсветка чтения и записи относится к последней выполненной команде).
    fn after_steps(source: &str, disk: &[u8], n: usize) -> MachineView {
        let asm = assemble(source);
        let mut sim = Sim::build(Engine::Emu, &asm, disk).expect("эмулятор собирается").expect("программа без ошибок");
        for _ in 0..n {
            sim.step();
        }
        sim.view()
    }

    fn run_to_end(source: &str, disk: &[u8]) -> MachineView {
        let asm = assemble(source);
        let mut sim = Sim::build(Engine::Emu, &asm, disk).expect("эмулятор собирается").expect("программа без ошибок");
        sim.run(RUN_LIMIT);
        sim.view()
    }

    #[test]
    fn broken_program_has_no_machine() {
        let asm = assemble("zzz r1");
        assert!(!asm.errors.is_empty());
        assert!(matches!(Sim::build(Engine::Emu, &asm, &[0; 256]), Ok(None)));
    }

    #[test]
    fn result_is_known_only_after_halt_or_error() {
        let mut expected = vec![0u8; 256];
        expected[0] = 7;
        let running = MachineView { regs: vec![0; 8], pc: 0, mem: vec![0; 256], halted: false, error: None, steps: 0, last_read: None, last_write: None, last_reg: None };
        assert_eq!(task_result(&running, &expected), None);
        let err = MachineView { error: Some("сломалось".into()), ..running.clone() };
        assert_eq!(task_result(&err, &expected), Some((false, "сломалось".to_string())));
        let done = run_to_end("li r1, 7\nsb r1, 0(r0)\nhlt", &[0; 256]);
        assert_eq!(task_result(&done, &expected).map(|r| r.0), Some(true));
        let wrong = run_to_end("li r1, 8\nsb r1, 0(r0)\nhlt", &[0; 256]);
        let r = task_result(&wrong, &expected).expect("остановилась");
        assert!(!r.0 && r.1.contains("0x00"), "{}", r.1);
    }

    #[test]
    fn memory_grid_marks_changes_reads_writes_and_regions() {
        let disk = vec![0u8; 256];
        // li, sb — записали 65 по адресу 3
        let wrote = after_steps("li r1, 65\nsb r1, 3(r0)\nlb r2, 4(r0)\nhlt", &disk, 2);
        let regions = [region("вход", 0, 4), region("выход", 4, 4)];
        let rows = memory_rows(&wrote.mem, &disk, Some(&wrote), &regions, 16);
        assert_eq!(rows.len(), 16);
        let cells = &rows[0].1;
        assert_eq!(cells.len(), 16);
        assert_eq!((cells[3].hex.as_str(), cells[3].ch), ("41", 'A'));
        assert!(cells[3].changed && cells[3].written && cells[3].region == Some(0));
        assert_eq!(cells[9].region, None);
        assert_eq!(cells[0].ch, '·');
        assert_eq!(rows[1].0, 16);
        assert_eq!(cell_class(&cells[3]), "lab-cell rg0 changed written");
        // lb — прочли адрес 4
        let read = after_steps("li r1, 65\nsb r1, 3(r0)\nlb r2, 4(r0)\nhlt", &disk, 3);
        let cell = &memory_rows(&read.mem, &disk, Some(&read), &regions, 1)[0].1[4];
        assert!(!cell.changed && cell.read && !cell.written);
        assert_eq!(cell_class(cell), "lab-cell rg1 read");
    }

    #[test]
    fn region_lookup_is_half_open() {
        let regions = [region("a", 0, 4), region("b", 4, 4)];
        assert_eq!((region_of(&regions, 3), region_of(&regions, 4), region_of(&regions, 8)), (Some(0), Some(1), None));
    }

    #[test]
    fn gate_machine_runs_the_same_program_as_the_emulator() {
        let asm = assemble("li r1, 5\nli r2, 3\nadd r3, r1, r2\nsb r3, 0(r0)\nhlt");
        let mut gates = Sim::build(Engine::Gates, &asm, &[0; 256]).expect("процессор собирается").expect("без ошибок");
        gates.run(RUN_LIMIT);
        let emu = run_to_end("li r1, 5\nli r2, 3\nadd r3, r1, r2\nsb r3, 0(r0)\nhlt", &[0; 256]);
        assert_eq!(gates.view().mem, emu.mem);
        assert_eq!(gates.view().regs, emu.regs);
    }
}
