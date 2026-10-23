//! Состояние лаборатории RISC-V: текст программы, ассемблирование, машина и итог запуска.
//!
//! Машина лежит в сигнале и меняется на месте (`update`), а всё, что рисует интерфейс, — производные `Memo`
//! (`status`, `result`), которые пересчитываются после каждого шага. Правка текста или «Сбросить» собирает машину заново.

use leptos::prelude::*;
use riscvlab::{asm::AsmResult, assemble, machine::Machine, task::TaskSpec};

use super::format::{build_machine, evaluate, run_limit, window_for, RunResult, Status};

/// Все сигналы одного упражнения; копируется по значению в обработчики.
#[derive(Clone, Copy)]
pub struct Session {
    pub spec: StoredValue<TaskSpec>,
    /// текст программы ученика (без данных задания)
    pub source: RwSignal<String>,
    /// результат ассемблирования полного текста (программа + данные задания)
    pub asm: Memo<AsmResult>,
    machine: RwSignal<Option<Machine>>,
    /// снимок машины; `None`, пока в программе есть ошибки
    pub status: Memo<Option<Status>>,
    /// итог, когда машина остановилась
    pub result: Memo<Option<RunResult>>,
    /// номер окна памяти
    pub window: RwSignal<usize>,
    /// выбранная строка листинга (адрес)
    pub selected: RwSignal<Option<u32>>,
    pub hint_open: RwSignal<bool>,
    reset: RwSignal<u32>,
    on_draft: Callback<String>,
}

impl Session {
    /// `initial` — текст программы при открытии; `report` вызывается с текстом программы, когда запуск выполнил задание
    /// (и сервер его ещё не засчитал).
    pub fn new(spec: TaskSpec, initial: String, solved: Signal<bool>, report: Callback<String>, on_draft: Callback<String>) -> Self {
        let spec = StoredValue::new(spec);
        let source = RwSignal::new(initial);
        let asm = Memo::new(move |_| spec.with_value(|s| assemble(&s.full_source(&source.get()))));
        let machine = RwSignal::new(asm.with_untracked(|a| spec.with_value(|s| build_machine(s, a))));
        let reset = RwSignal::new(0u32);
        // новая программа или «Сбросить» — машина с нуля (первый прогон не нужен: машина уже собрана)
        Effect::new(move |prev: Option<()>| {
            asm.track();
            reset.track();
            if prev.is_some() {
                machine.set(asm.with_untracked(|a| spec.with_value(|s| build_machine(s, a))));
            }
        });
        let status = Memo::new(move |_| machine.with(|m| m.as_ref().map(Status::of)));
        let result = Memo::new(move |_| {
            machine.with(|m| {
                let m = m.as_ref()?;
                asm.with(|a| spec.with_value(|s| evaluate(s, a, m, &source.get_untracked())))
            })
        });
        // задание выполнено — сообщаем решение (сервер перепроверит его тем же движком)
        Effect::new(move |_| {
            if result.get().is_some_and(|r| r.ok) && !solved.get_untracked() {
                report.run(source.get_untracked());
            }
        });
        Self { spec, source, asm, machine, status, result, window: RwSignal::new(0), selected: RwSignal::new(None), hint_open: RwSignal::new(false), reset, on_draft }
    }

    /// Ученик правит текст программы.
    pub fn edit(&self, text: String) {
        self.selected.set(None);
        self.source.set(text.clone());
        self.on_draft.run(text);
    }

    /// «Начать заново»: вернуть заготовку.
    pub fn restart(&self) {
        let starter = self.spec.with_value(|s| s.starter.clone());
        self.edit(starter);
    }

    /// Одна команда.
    pub fn step(&self) {
        self.machine.update(|m| {
            if let Some(m) = m {
                m.step();
            }
        });
        self.follow();
    }

    /// До остановки (но не дольше лимита шагов задачи).
    pub fn run(&self) {
        let limit = self.spec.with_value(run_limit);
        let can = self.status.with_untracked(|s| s.as_ref().is_some_and(Status::can_step));
        if !can {
            return;
        }
        self.machine.update(|m| {
            if let Some(m) = m {
                m.run(limit);
            }
        });
        self.follow();
    }

    /// «Сбросить»: машина в начальное состояние, программа та же.
    pub fn reset(&self) {
        self.reset.update(|n| *n += 1);
    }

    /// Окно памяти перескакивает туда, где команда только что писала или читала.
    fn follow(&self) {
        let addr = self.machine.with_untracked(|m| m.as_ref().and_then(|m| m.last_write.or(m.last_read)));
        if let Some(i) = addr.and_then(window_for) {
            self.window.set(i);
        }
    }

    /// Окно памяти: байты машины, а пока её нет — образ из ассемблера.
    pub fn memory<R>(&self, f: impl FnOnce(&[u8], Option<u32>, Option<u32>) -> R) -> R {
        self.machine.with(|m| match m {
            Some(m) => f(&m.mem, m.last_read, m.last_write),
            None => self.asm.with(|a| f(&a.image, None, None)),
        })
    }
}
