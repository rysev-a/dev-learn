//! Упражнения лаборатории RISC-V как данные и проверка решений.
//!
//! * [`LabChapter`] — файл данных главы (`backend/app/data/labs/arch/<книга>-<глава>.json`);
//! * [`TaskSpec`] — всё, что нужно для проверки: заготовка, эталон, данные задания, тесты;
//! * [`verify`] — ассемблирует присланный текст программы, прогоняет все тесты задачи и выносит вердикт.
//!   Это то, что сервер делает на `PUT /api/exercises/14/<глава>/<id>/solved`.

use serde::{Deserialize, Serialize};

use crate::asm::{assemble, AsmError, AsmResult, RAM_SIZE};
use crate::isa::reg_name;
use crate::js::json_quote;
use crate::machine::{Machine, Options, View, DEFAULT_MAX_STEPS};

/// Самый длинный текст программы, который проверяет сервер (байт).
pub const MAX_PROGRAM_BYTES: usize = 256 * 1024;

/// Лимит шагов на один тест по умолчанию (как в интерфейсе).
pub const DEFAULT_TASK_STEPS: u64 = 200_000;

/// Какая лаборатория.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Lab {
    /// RISC-V: главы 16 и 17 книги 14
    Riscv,
}

/// Окружение, в котором работает программа.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Profile {
    /// учебная плата: остановка `ebreak`, консоль UART, светодиоды, переключатели, таймер (глава 16)
    Board,
    /// настоящая программа: `write` и `exit` как в Linux, точка входа `_start` (глава 17)
    Linux,
}

/// Файл данных главы.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LabChapter {
    /// номер книги
    pub book: u32,
    /// номер главы
    pub chapter: u32,
    /// какая лаборатория
    pub lab: Lab,
    /// задачи
    pub tasks: Vec<Task>,
}

/// Упражнение.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Task {
    /// идентификатор задачи
    pub id: String,
    /// название
    pub title: String,
    /// условие
    pub statement: String,
    /// подсказка
    pub hint: String,
    /// спецификация упражнения
    pub spec: TaskSpec,
}

/// Спецификация упражнения.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TaskSpec {
    /// окружение, в котором работают программы
    pub profile: Profile,
    /// заготовка программы
    pub starter: String,
    /// эталонное решение (клиенту не отдаётся, см. [`TaskSpec::without_reference`]; в ответе сервера поля нет)
    #[serde(default)]
    pub reference: String,
    /// данные задания: ассемблерный текст секции `.data`; дописывается к программе и не редактируется
    pub data: String,
    /// что считается «зависанием»: сколько команд выполнять на тест
    #[serde(default = "default_steps")]
    pub max_steps: u64,
    /// тесты
    pub tests: Vec<Test>,
}

fn default_steps() -> u64 {
    DEFAULT_TASK_STEPS
}

/// Один тест: входы и ожидание.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Test {
    /// положение переключателей (8 бит)
    #[serde(default)]
    pub switches: u8,
    /// регистры, заданные до запуска (кроме sp, который ставит загрузчик, если не указан)
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub regs: Vec<RegInit>,
    /// что должно получиться
    pub check: Check,
}

/// Начальное значение регистра.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RegInit {
    /// номер регистра x0…x31
    pub reg: u8,
    /// значение
    pub value: i32,
}

/// Проверка итогового состояния машины после остановки. Тексты — как в прежней версии на TypeScript.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Check {
    /// в консоли ровно этот текст
    Uart {
        /// ожидаемый вывод
        expected: String,
        /// сообщение при успехе
        ok: String,
    },
    /// светодиоды горят по узору
    Leds {
        /// ожидаемые восемь бит
        expected: u8,
        /// сообщение при успехе
        ok: String,
        /// дописывается к сообщению об ошибке
        #[serde(default, skip_serializing_if = "String::is_empty")]
        bad_suffix: String,
    },
    /// в регистре число
    Reg {
        /// номер регистра x0…x31
        reg: u8,
        /// ожидаемое значение (со знаком)
        expected: i32,
        /// сообщение при успехе
        ok: String,
    },
    /// по метке лежит строка (читается до нулевого байта)
    MemCstr {
        /// имя метки
        symbol: String,
        /// ожидаемая строка
        expected: String,
        /// сообщение при успехе
        ok: String,
    },
    /// по метке лежит массив 32-битных слов
    MemWords {
        /// имя метки
        symbol: String,
        /// ожидаемые слова со знаком
        expected: Vec<i32>,
        /// сообщение при успехе
        ok: String,
    },
    /// sp вернулся на вершину памяти
    StackReturned,
    /// все проверки по порядку; сообщение — первой неудавшейся, иначе `ok`
    All {
        /// вложенные проверки
        checks: Vec<Check>,
        /// сообщение при успехе
        ok: String,
    },
    /// светодиод переключился `toggles` раз по схеме 1, 0, 1, 0…, каждое состояние держалось не меньше `min_gap` тактов
    Blink {
        /// сколько переключений нужно
        toggles: u32,
        /// минимальная выдержка между переключениями, в тактах
        min_gap: u64,
        /// сообщение при успехе
        ok: String,
    },
    /// программа завершилась вызовом exit: вывод и код возврата
    Run {
        /// ожидаемый вывод
        stdout: String,
        /// ожидаемый код возврата
        code: i32,
        /// сообщение при успехе
        ok: String,
    },
}

/// Итог проверки одного условия.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CheckResult {
    /// всё прошло
    pub ok: bool,
    /// текст сообщения
    pub message: String,
}

fn ok(message: &str) -> CheckResult {
    CheckResult { ok: true, message: message.to_string() }
}
fn bad(message: String) -> CheckResult {
    CheckResult { ok: false, message }
}

/// `0b` и восемь двоичных цифр.
fn bin8(n: u32) -> String {
    format!("0b{:08b}", n & 0xff)
}

fn word_at(mem: &[u8], a: usize) -> i32 {
    let b = |k: usize| i32::from(mem.get(a + k).copied().unwrap_or(0));
    b(0) | (b(1) << 8) | (b(2) << 16) | (b(3) << 24)
}

/// Строка до нулевого байта; байты — как коды символов Latin-1 (так её читала прежняя проверка).
fn cstr_at(mem: &[u8], a: Option<u32>) -> String {
    let Some(a) = a else { return String::new() };
    let mut s = String::new();
    let mut i = a as usize;
    while i < mem.len() && mem[i] != 0 {
        s.push(char::from(mem[i]));
        i += 1;
    }
    s
}

impl Check {
    /// Проверить состояние машины после остановки. `symbols` — адреса меток программы.
    pub fn evaluate(&self, v: &View, symbols: &std::collections::BTreeMap<String, u32>) -> CheckResult {
        match self {
            Check::Uart { expected, ok: okm } => {
                if &v.uart == expected {
                    ok(okm)
                } else {
                    bad(format!("В консоли {}, а ожидалось {}", json_quote(&v.uart), json_quote(expected)))
                }
            }
            Check::Leds { expected, ok: okm, bad_suffix } => {
                if v.leds == *expected {
                    ok(okm)
                } else {
                    bad(format!(
                        "Светодиоды {}, а ожидалось {}{}",
                        bin8(u32::from(v.leds)),
                        bin8(u32::from(*expected)),
                        bad_suffix
                    ))
                }
            }
            Check::Reg { reg, expected, ok: okm } => {
                let got = v.regs.get(usize::from(*reg)).copied().unwrap_or(0);
                if got == *expected as u32 {
                    ok(okm)
                } else {
                    bad(format!("В {} лежит {}, а ожидалось {}", reg_name(*reg), got as i32, expected))
                }
            }
            Check::MemCstr { symbol, expected, ok: okm } => {
                let got = cstr_at(&v.mem, symbols.get(symbol).copied());
                if &got == expected {
                    ok(okm)
                } else {
                    bad(format!("В памяти «{got}», а ожидалось «{expected}»"))
                }
            }
            Check::MemWords { symbol, expected, ok: okm } => {
                let base = symbols.get(symbol).copied().unwrap_or(0) as usize;
                let got: Vec<i32> = (0..expected.len()).map(|i| word_at(&v.mem, base + 4 * i)).collect();
                if &got == expected {
                    ok(okm)
                } else {
                    let join = |w: &[i32]| w.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(", ");
                    bad(format!("В памяти {}, а ожидалось {}", join(&got), join(expected)))
                }
            }
            Check::StackReturned => {
                let sp = v.regs.get(2).copied().unwrap_or(0);
                if sp == RAM_SIZE as u32 {
                    ok("")
                } else {
                    bad(format!("Стек не вернулся на место: sp = 0x{sp:x}, а должен быть 0x{RAM_SIZE:x}"))
                }
            }
            Check::All { checks, ok: okm } => {
                for c in checks {
                    let r = c.evaluate(v, symbols);
                    if !r.ok {
                        return r;
                    }
                }
                ok(okm)
            }
            Check::Blink { toggles, min_gap, ok: okm } => {
                // оставляем только настоящие переключения: запись того же значения — не событие
                let mut changes: Vec<(u64, u8)> = Vec::new();
                let mut prev = 0u8;
                for e in &v.led_log {
                    if e.value != prev {
                        changes.push((e.cycle, e.value));
                    }
                    prev = e.value;
                }
                if (changes.len() as u64) < u64::from(*toggles) {
                    return bad(format!("LED переключился {} раз(а), а нужно {}", changes.len(), toggles));
                }
                for (i, (cycle, value)) in changes.iter().enumerate() {
                    let want = u8::from(i % 2 == 0);
                    if *value != want {
                        return bad(format!(
                            "Переключение {}: LED = {}, а должно чередоваться 1, 0, 1, 0…",
                            i + 1,
                            value
                        ));
                    }
                    if i > 0 {
                        let gap = cycle - changes[i - 1].0;
                        if gap < *min_gap {
                            return bad(format!(
                                "Между переключениями {} и {} прошло {} тактов, а нужно хотя бы {}",
                                i,
                                i + 1,
                                gap,
                                min_gap
                            ));
                        }
                    }
                }
                ok(okm)
            }
            Check::Run { stdout, code, ok: okm } => {
                let Some(exit) = v.exit_code else {
                    return bad(
                        "Программа не завершилась вызовом exit: нужно li a7, 93 и ecall (код возврата — в a0)."
                            .to_string(),
                    );
                };
                if &v.uart != stdout {
                    return bad(format!("Вывод {}, а ожидалось {}", json_quote(&v.uart), json_quote(stdout)));
                }
                if exit != *code {
                    return bad(format!("Код возврата {exit}, а ожидался {code}"));
                }
                ok(okm)
            }
        }
    }
}

impl TaskSpec {
    /// Копия без эталонного решения — то, что бэкенд отдаёт клиенту.
    pub fn without_reference(&self) -> TaskSpec {
        TaskSpec { reference: String::new(), ..self.clone() }
    }

    /// Полный текст программы: то, что написал ученик, плюс данные задания.
    pub fn full_source(&self, user: &str) -> String {
        full_source(user, &self.data)
    }
}

/// Полный текст программы: то, что написал ученик, плюс данные задания.
pub fn full_source(user: &str, data: &str) -> String {
    format!("{user}\n.data\n{data}\n")
}

/// Чем закончилась проверка.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    /// все тесты пройдены
    Passed,
    /// программа остановилась, но результат не тот
    Wrong,
    /// машина сломалась: неверная команда, выход из памяти, лимит шагов
    Fault,
    /// программа не собралась (или слишком длинная)
    AsmErrors,
}

/// Итог одного теста.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TestVerdict {
    /// всё прошло
    pub ok: bool,
    /// текст сообщения
    pub message: String,
    /// сколько команд выполнено
    pub steps: u64,
}

/// Вердикт по решению.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Verdict {
    /// всё прошло
    pub ok: bool,
    /// чем закончилась проверка
    pub outcome: Outcome,
    /// сообщение ученику: первое из неудавшихся, иначе — последнего теста
    pub message: String,
    /// ошибки ассемблера (номера строк — по полному тексту: программа и данные задания)
    pub errors: Vec<AsmError>,
    /// тесты
    pub tests: Vec<TestVerdict>,
}

fn failed(outcome: Outcome, message: String, errors: Vec<AsmError>) -> Verdict {
    Verdict { ok: false, outcome, message, errors, tests: Vec::new() }
}

/// Запустить собранную программу в условиях теста и проверить результат.
pub fn run_test(spec: &TaskSpec, asm: &AsmResult, test: &Test) -> (CheckResult, Outcome, u64) {
    let mut m = Machine::new(&asm.image, Options { switches: test.switches, entry: asm.entry });
    for r in &test.regs {
        m.set_reg(r.reg, r.value);
    }
    m.run(if spec.max_steps == 0 { DEFAULT_MAX_STEPS } else { spec.max_steps });
    let steps = m.steps;
    if let Some(e) = &m.error {
        return (CheckResult { ok: false, message: e.clone() }, Outcome::Fault, steps);
    }
    let r = test.check.evaluate(&m.view(), &asm.symbols);
    let outcome = if r.ok { Outcome::Passed } else { Outcome::Wrong };
    (r, outcome, steps)
}

/// Проверка решения: собрать присланный текст программы и прогнать все тесты задачи.
pub fn verify(spec: &TaskSpec, program: &str) -> Verdict {
    if program.len() > MAX_PROGRAM_BYTES {
        let msg =
            format!("Программа слишком длинная: {} байт, а проверяется не больше {}", program.len(), MAX_PROGRAM_BYTES);
        return failed(Outcome::AsmErrors, msg.clone(), vec![AsmError { line: 1, message: msg }]);
    }
    let asm = assemble(&spec.full_source(program));
    if let Some(first) = asm.errors.first() {
        let msg = format!("Строка {}: {}", first.line, first.message);
        return failed(Outcome::AsmErrors, msg, asm.errors.clone());
    }
    if spec.tests.is_empty() {
        return failed(Outcome::Wrong, "У задачи нет тестов".to_string(), Vec::new());
    }
    let mut tests = Vec::new();
    // итог — по первому неудавшемуся тесту, а если все прошли — по последнему
    let mut summary: Option<(Outcome, String)> = None;
    for t in &spec.tests {
        let (r, o, steps) = run_test(spec, &asm, t);
        if summary.as_ref().is_none_or(|(prev, _)| *prev == Outcome::Passed) {
            summary = Some((o, r.message.clone()));
        }
        tests.push(TestVerdict { ok: r.ok, message: r.message, steps });
    }
    let (outcome, message) = summary.unwrap_or((Outcome::Wrong, String::new()));
    Verdict { ok: outcome == Outcome::Passed, outcome, message, errors: Vec::new(), tests }
}

impl LabChapter {
    /// Разобрать файл данных главы.
    pub fn from_json(text: &str) -> Result<LabChapter, serde_json::Error> {
        serde_json::from_str(text)
    }

    /// Канонический JSON файла (с отступами и переводом строки в конце).
    pub fn to_canonical_json(&self) -> Result<String, serde_json::Error> {
        let mut s = serde_json::to_string_pretty(self)?;
        s.push('\n');
        Ok(s)
    }

    /// Задача по id.
    pub fn task(&self, id: &str) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }

    /// Копия главы без эталонных решений — для клиента.
    pub fn without_references(&self) -> LabChapter {
        LabChapter {
            tasks: self.tasks.iter().map(|t| Task { spec: t.spec.without_reference(), ..t.clone() }).collect(),
            ..self.clone()
        }
    }
}

/// Имя файла данных главы: `<книга>-<глава:02>.json`.
pub fn chapter_file_name(book: u32, chapter: u32) -> String {
    format!("{book}-{chapter:02}.json")
}
