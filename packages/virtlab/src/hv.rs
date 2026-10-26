//! Модель мини-гипервизора (глава 2): ученик играет монитор виртуальных машин.
//!
//! Гость исполняет программу без привилегий. Обычные команды идут напрямую, а на привилегированных процессор вызывает
//! ловушку, и монитор должен правильно сымитировать действие над виртуальным состоянием гостя. Команда POPF в кольце 1
//! не вызывает ловушки (дыра x86), пока не включена двоичная трансляция.
//!
//! Цель упражнения — по одной на программу: пройти программу, на каждой ловушке выбрав верную имитацию (идентификатор цели
//! совпадает с [`Program::id`]). Историю действий ученика ведёт [`Session`] (то же, что обработчики `HvLab.tsx`);
//! для серверной перепроверки история записывается как [`Run`] и воспроизводится [`replay`].

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;

/// Программа гостя: команды в текстовом виде («ADD 3», «CLI», «POPF 1»…).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Program {
    /// Идентификатор программы (он же идентификатор цели).
    pub id: String,
    /// Название вкладки.
    pub title: String,
    /// Команды программы.
    pub code: Vec<String>,
    /// Текст цели.
    pub goal: String,
}

impl Program {
    /// Цель упражнения по этой программе.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }

    /// Проверка: программа не пуста и все команды разбираются.
    pub fn validate(&self) -> Result<(), SpecError> {
        for c in &self.code {
            Instr::parse(c).map_err(|e| SpecError::new(format!("программа {}: {e}", self.id)))?;
        }
        if self.code.is_empty() {
            return Err(SpecError::new(format!("программа {}: пустая", self.id)));
        }
        Ok(())
    }
}

/// Команда гостя.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Instr {
    /// `ADD n` — обычная команда, идёт напрямую.
    Add(i64),
    /// `CLI` — запретить прерывания.
    Cli,
    /// `STI` — разрешить прерывания.
    Sti,
    /// `WRCR3 n` — записать в CR3.
    Wrcr3(i64),
    /// `RDCR3` — прочитать CR3 в аккумулятор.
    Rdcr3,
    /// `HLT` — остановить процессор.
    Hlt,
    /// `IRQ n` — внешнее прерывание для гостя.
    Irq(i64),
    /// `POPF n` — загрузить флаги.
    Popf(i64),
    /// Любая другая команда: исполняется напрямую и ничего не меняет (как `default` в TypeScript).
    Other,
}

impl Instr {
    /// Разобрать команду вида «ИМЯ» или «ИМЯ число».
    pub fn parse(text: &str) -> Result<Instr, SpecError> {
        let mut it = text.split(' ');
        let op = it.next().unwrap_or("");
        let arg = it.next();
        let num = |name: &str| -> Result<i64, SpecError> {
            arg.and_then(|a| a.parse::<i64>().ok())
                .ok_or_else(|| SpecError::new(format!("команда «{text}»: {name} требует целое число")))
        };
        Ok(match op {
            "ADD" => Instr::Add(num("ADD")?),
            "CLI" => Instr::Cli,
            "STI" => Instr::Sti,
            "WRCR3" => Instr::Wrcr3(num("WRCR3")?),
            "RDCR3" => Instr::Rdcr3,
            "HLT" => Instr::Hlt,
            "IRQ" => Instr::Irq(num("IRQ")?),
            "POPF" => Instr::Popf(num("POPF")?),
            _ => Instr::Other,
        })
    }
}

/// Виртуальное состояние гостя и счётчики прогона.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GuestState {
    /// Номер текущей команды.
    pub pc: usize,
    /// Аккумулятор.
    pub acc: i64,
    /// Виртуальный флаг прерываний IF.
    pub vif: i64,
    /// Виртуальный CR3.
    pub vcr3: i64,
    /// Очередь прерываний, ждущих разрешения.
    pub queue: Vec<i64>,
    /// Доставленные гостю прерывания.
    pub delivered: Vec<i64>,
    /// Журнал шагов (для показа).
    pub log: Vec<String>,
    /// Число неверных выборов монитора.
    pub mistakes: u32,
    /// Была команда, которую монитор не заметил (POPF без трансляции).
    pub silent: bool,
    /// Гость остановлен (HLT).
    pub halted: bool,
}

impl Default for GuestState {
    fn default() -> Self {
        initial()
    }
}

/// Начальное состояние гостя.
pub fn initial() -> GuestState {
    GuestState {
        pc: 0,
        acc: 0,
        vif: 1,
        vcr3: 0,
        queue: vec![],
        delivered: vec![],
        log: vec![],
        mistakes: 0,
        silent: false,
        halted: false,
    }
}

/// Вариант имитации на ловушке.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TrapOption {
    /// Текст варианта.
    pub label: String,
    /// Верный ли вариант.
    pub ok: bool,
    /// Пояснение (для неверного — почему нельзя).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub why: Option<String>,
}

/// Что происходит на команде.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Inspection {
    /// Команда идёт напрямую на процессоре.
    Direct,
    /// Команда «молча» не сработала, ловушки не было.
    Silent {
        /// Объяснение.
        why: String,
    },
    /// Ловушка: монитор выбирает имитацию.
    Trap {
        /// Заголовок ловушки.
        title: String,
        /// Варианты (в порядке модели; интерфейс может перемешать).
        options: Vec<TrapOption>,
    },
}

fn opt(label: impl Into<String>, ok: bool, why: Option<&str>) -> TrapOption {
    TrapOption { label: label.into(), ok, why: why.map(str::to_string) }
}

/// Что происходит на команде `ins` в состоянии `s` (`translate` — включена ли двоичная трансляция).
pub fn inspect(ins: &Instr, s: &GuestState, translate: bool) -> Inspection {
    let trap = |title: String, options: Vec<TrapOption>| Inspection::Trap { title, options };
    match ins {
        Instr::Add(_) | Instr::Other => Inspection::Direct,
        Instr::Cli => trap(
            "CLI — запретить прерывания".into(),
            vec![
                opt("виртуальный флаг vif ← 0", true, None),
                opt(
                    "выполнить CLI на настоящем процессоре",
                    false,
                    Some("монитор перестал бы получать прерывания таймера и потерял управление"),
                ),
                opt("vif ← 1", false, Some("это противоположное действие")),
            ],
        ),
        Instr::Sti => trap(
            "STI — разрешить прерывания".into(),
            vec![
                opt("vif ← 1 и доставить очередь", true, None),
                opt("vif ← 1, очередь оставить", false, Some("прерывания, пришедшие раньше, так и не дойдут до гостя")),
                opt(
                    "выполнить STI на настоящем процессоре",
                    false,
                    Some("настоящий флаг и так включён: гость не получил бы своё состояние"),
                ),
            ],
        ),
        Instr::Wrcr3(n) => trap(
            format!("MOV CR3, {n} — сменить таблицы страниц"),
            vec![
                opt(format!("виртуальный vcr3 ← {n}"), true, None),
                opt(
                    format!("записать {n} в настоящий CR3"),
                    false,
                    Some("гость получил бы доступ к чужой памяти: настоящим CR3 владеет монитор"),
                ),
                opt(format!("acc ← {n}"), false, Some("команда пишет в CR3, а не в аккумулятор")),
            ],
        ),
        Instr::Rdcr3 => trap(
            "MOV acc, CR3 — прочитать таблицы страниц".into(),
            vec![
                opt("acc ← виртуальный vcr3", true, None),
                opt("acc ← настоящий CR3", false, Some("гость увидел бы настоящее состояние хозяина, а не своё")),
                opt("vcr3 ← 0", false, Some("чтение ничего не должно менять")),
            ],
        ),
        Instr::Hlt => trap(
            "HLT — остановить процессор".into(),
            vec![
                opt("остановить виртуальный процессор гостя", true, None),
                opt("остановить настоящий процессор", false, Some("остановились бы все остальные гости и сам монитор")),
                opt("ничего не делать", false, Some("гость ждёт прерывания, а процессор хозяина молотил бы впустую")),
            ],
        ),
        Instr::Irq(n) => trap(
            format!("внешнее прерывание {n} для гостя"),
            vec![
                opt("доставить гостю сейчас", s.vif == 1, Some("гость запретил прерывания: доставлять нельзя")),
                opt("поставить в очередь", s.vif == 0, Some("гость прерывания разрешил: ждать незачем")),
            ],
        ),
        Instr::Popf(n) => {
            if !translate {
                return Inspection::Silent {
                    why: "В кольце 1 команда POPF не может изменить флаг IF, но и не вызывает ловушку: ничего не произошло, монитор не узнал."
                        .into(),
                };
            }
            trap(
                format!("POPF {n} — загрузить флаги (после трансляции — вызов монитора)"),
                vec![
                    opt(format!("vif ← {n}"), true, None),
                    opt("игнорировать, как делает процессор", false, Some("ради этого и включили трансляцию")),
                    opt(
                        "выполнить POPF на настоящем процессоре",
                        false,
                        Some("настоящий IF не должен зависеть от гостя"),
                    ),
                ],
            )
        }
    }
}

/// Применить верную имитацию (или прямое исполнение) команды к состоянию.
pub fn apply(ins: &Instr, s: &GuestState) -> GuestState {
    let mut t = s.clone();
    t.pc += 1;
    match ins {
        Instr::Add(n) => t.acc += n,
        Instr::Cli => t.vif = 0,
        Instr::Sti => {
            t.vif = 1;
            let q = std::mem::take(&mut t.queue);
            t.delivered.extend(q);
        }
        Instr::Wrcr3(n) => t.vcr3 = *n,
        Instr::Rdcr3 => t.acc = t.vcr3,
        Instr::Hlt => t.halted = true,
        Instr::Irq(n) => {
            if t.vif != 0 {
                t.delivered.push(*n);
            } else {
                t.queue.push(*n);
            }
        }
        Instr::Popf(n) => t.vif = *n,
        Instr::Other => {}
    }
    t
}

/// Ожидаемое виртуальное состояние при верной имитации всей программы.
pub fn expected(code: &[Instr]) -> GuestState {
    code.iter().fold(initial(), |s, i| apply(i, &s))
}

/// Итог прогона программы (остановка гостя).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Finish {
    /// Состояние верное: монитор не пропустил команду, а acc, vif, vcr3 и доставленные прерывания совпали с ожидаемыми.
    pub ok: bool,
    /// Число неверных выборов за прогон.
    pub mistakes: u32,
    /// Итоговое состояние.
    pub state: GuestState,
    /// Ожидаемое состояние при верной имитации.
    pub want: GuestState,
}

/// Результат кнопки «Шаг».
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Stepped {
    /// Шагать нечем: программа остановлена или кончилась, либо на команде ловушка (нужен выбор).
    Blocked,
    /// Команда исполнена напрямую.
    Direct,
    /// Команда не сработала молча (POPF без трансляции).
    Silent {
        /// Объяснение для ученика.
        why: String,
    },
}

/// Результат выбора варианта на ловушке.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Choice {
    /// Сейчас нет ловушки или такого варианта нет.
    Invalid,
    /// Неверный вариант: ошибка записана, состояние не изменилось.
    Wrong {
        /// Почему нельзя.
        why: String,
    },
    /// Верный вариант, программа продолжается.
    Applied,
    /// Верный вариант, гость остановлен: прогон окончен.
    Finished(Box<Finish>),
}

/// Прогон программы учеником: те же действия, что в `HvLab.tsx` (шаг, выбор на ловушке, начать сначала).
#[derive(Clone, Debug)]
pub struct Session {
    raw: Vec<String>,
    code: Vec<Instr>,
    translate: bool,
    state: GuestState,
    want: GuestState,
    finish: Option<Finish>,
}

impl Session {
    /// Новый прогон программы `code`.
    pub fn new(code: &[String], translate: bool) -> Result<Session, SpecError> {
        let parsed = code.iter().map(|c| Instr::parse(c)).collect::<Result<Vec<_>, _>>()?;
        let want = expected(&parsed);
        Ok(Session { raw: code.to_vec(), code: parsed, translate, state: initial(), want, finish: None })
    }

    /// Текущее состояние гостя.
    pub fn state(&self) -> &GuestState {
        &self.state
    }

    /// Итог, если прогон окончен остановкой гостя.
    pub fn finish(&self) -> Option<&Finish> {
        self.finish.as_ref()
    }

    /// Включена ли двоичная трансляция.
    pub fn translate(&self) -> bool {
        self.translate
    }

    /// Прогон уже начат (трансляцию менять нельзя).
    pub fn started(&self) -> bool {
        self.state.pc > 0 || !self.state.log.is_empty()
    }

    /// Включить/выключить трансляцию; до запуска. `false` — прогон начат, ничего не изменилось.
    pub fn set_translate(&mut self, on: bool) -> bool {
        if self.started() {
            return false;
        }
        self.translate = on;
        true
    }

    /// Начать сначала (трансляция сохраняется).
    pub fn reset(&mut self) {
        self.state = initial();
        self.finish = None;
    }

    /// Текущая команда (текстом), если гость не остановлен и программа не кончилась.
    pub fn current(&self) -> Option<&str> {
        if self.state.halted {
            return None;
        }
        self.raw.get(self.state.pc).map(String::as_str)
    }

    /// Что происходит на текущей команде.
    pub fn inspect(&self) -> Option<Inspection> {
        if self.state.halted {
            return None;
        }
        self.code.get(self.state.pc).map(|i| inspect(i, &self.state, self.translate))
    }

    /// Кнопка «Шаг»: прямая команда исполняется, «тихая» тоже (ничего не меняя), на ловушке шаг заблокирован.
    pub fn step(&mut self) -> Stepped {
        let (Some(ins), Some(info)) = (self.code.get(self.state.pc).cloned(), self.inspect()) else {
            return Stepped::Blocked;
        };
        let text = self.raw[self.state.pc].clone();
        match info {
            Inspection::Trap { .. } => Stepped::Blocked,
            Inspection::Direct => {
                let mut t = apply(&ins, &self.state);
                t.log.push(format!("{text} — напрямую на процессоре"));
                self.state = t;
                Stepped::Direct
            }
            Inspection::Silent { why } => {
                let mut t = self.state.clone();
                t.pc += 1;
                t.silent = true;
                t.log.push(format!("{text} — без ловушки, ничего не изменилось"));
                self.state = t;
                Stepped::Silent { why }
            }
        }
    }

    /// Выбрать вариант на ловушке по тексту.
    pub fn choose(&mut self, label: &str) -> Choice {
        let (Some(ins), Some(Inspection::Trap { options, .. })) =
            (self.code.get(self.state.pc).cloned(), self.inspect())
        else {
            return Choice::Invalid;
        };
        let Some(o) = options.iter().find(|o| o.label == label) else {
            return Choice::Invalid;
        };
        if !o.ok {
            self.state.mistakes += 1;
            return Choice::Wrong { why: o.why.clone().unwrap_or_default() };
        }
        let text = self.raw[self.state.pc].clone();
        let mut t = apply(&ins, &self.state);
        t.log.push(format!("{text} — ловушка: {}", o.label));
        self.state = t;
        if self.state.halted {
            let f = self.make_finish();
            self.finish = Some(f.clone());
            return Choice::Finished(Box::new(f));
        }
        Choice::Applied
    }

    fn make_finish(&self) -> Finish {
        let (s, w) = (&self.state, &self.want);
        let ok = !s.silent && s.acc == w.acc && s.vif == w.vif && s.vcr3 == w.vcr3 && s.delivered == w.delivered;
        Finish { ok, mistakes: s.mistakes, state: s.clone(), want: w.clone() }
    }
}

/// Одно действие ученика в записи прогона.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "step", rename_all = "snake_case")]
pub enum Step {
    /// «Шаг» на прямой команде.
    Direct,
    /// «Шаг» на команде, не вызвавшей ловушку (POPF без трансляции).
    Silent,
    /// Выбор варианта на ловушке (текст варианта; неверный выбор тоже записывается — он считается ошибкой).
    Trap {
        /// Текст выбранного варианта.
        label: String,
    },
}

/// Запись прогона: настройка и действия. Клиент может приложить её к решению, сервер — воспроизвести.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Run {
    /// Была ли включена двоичная трансляция.
    pub translate: bool,
    /// Действия по порядку.
    pub steps: Vec<Step>,
}

/// Воспроизвести запись прогона на программе. Ошибка — запись не соответствует модели (действие невозможно на этой
/// команде, лишние действия после остановки гостя, программа не доведена до остановки).
pub fn replay(program: &Program, run: &Run) -> Result<Finish, SpecError> {
    let mut s = Session::new(&program.code, run.translate)?;
    for (i, st) in run.steps.iter().enumerate() {
        if s.finish().is_some() {
            return Err(SpecError::new(format!("действие {}: после остановки гостя", i + 1)));
        }
        let bad = |what: &str| SpecError::new(format!("действие {}: {what}", i + 1));
        match st {
            Step::Direct => match s.inspect() {
                Some(Inspection::Direct) => {
                    s.step();
                }
                _ => return Err(bad("команда не прямая")),
            },
            Step::Silent => match s.inspect() {
                Some(Inspection::Silent { .. }) => {
                    s.step();
                }
                _ => return Err(bad("команда не «тихая»")),
            },
            Step::Trap { label } => {
                if s.choose(label) == Choice::Invalid {
                    return Err(bad("такой ловушки или варианта нет"));
                }
            }
        }
    }
    s.finish().cloned().ok_or_else(|| SpecError::new("программа не доведена до остановки гостя"))
}

/// Идеальный прогон программы: на каждой ловушке верный вариант. Если без трансляции встретилась «тихая» команда,
/// прогон продолжается и закончится неверным итогом ([`Finish::ok`] = `false`).
pub fn ideal_run(program: &Program, translate: bool) -> Result<Run, SpecError> {
    let mut s = Session::new(&program.code, translate)?;
    let mut steps = vec![];
    for _ in 0..(program.code.len() * 2 + 4) {
        match s.inspect() {
            None => break,
            Some(Inspection::Direct) => {
                s.step();
                steps.push(Step::Direct);
            }
            Some(Inspection::Silent { .. }) => {
                s.step();
                steps.push(Step::Silent);
            }
            Some(Inspection::Trap { options, .. }) => {
                let Some(o) = options.iter().find(|o| o.ok) else {
                    return Err(SpecError::new("на ловушке нет верного варианта"));
                };
                s.choose(&o.label);
                steps.push(Step::Trap { label: o.label.clone() });
            }
        }
    }
    Ok(Run { translate, steps })
}

/// Нужна ли программе двоичная трансляция: без неё встречается команда, не вызывающая ловушку.
pub fn needs_translation(program: &Program) -> Result<bool, SpecError> {
    Ok(ideal_run(program, false)?.steps.contains(&Step::Silent))
}

/// Программы по умолчанию (упражнение главы 2).
pub fn default_programs() -> Vec<Program> {
    let p = |id: &str, title: &str, code: &[&str], goal: &str| Program {
        id: id.into(),
        title: title.into(),
        code: code.iter().map(|c| c.to_string()).collect(),
        goal: goal.into(),
    };
    vec![
        p(
            "base",
            "Привилегированные команды",
            &["ADD 3", "CLI", "WRCR3 4096", "ADD 2", "RDCR3", "STI", "HLT"],
            "Пройдите программу: на каждой ловушке выберите верную имитацию",
        ),
        p(
            "irq",
            "Прерывания",
            &["CLI", "IRQ 1", "IRQ 2", "STI", "HLT"],
            "Не потеряйте прерывания: они ждут в очереди, пока гость не разрешит",
        ),
        p(
            "popf",
            "Проблема POPF",
            &["CLI", "POPF 1", "ADD 2", "HLT"],
            "Выполните программу так, чтобы POPF изменила виртуальный флаг IF",
        ),
    ]
}
