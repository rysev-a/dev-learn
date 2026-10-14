// Слайды для «Изучаем Rust», глава 1 — «Введение в Rust».
// Тот же дизайн-код, что и у Linux-книги: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: слайды с примерами кода на Rust и подсветкой синтаксиса.

const RS_KW = new Set([
  "fn", "let", "mut", "pub", "struct", "enum", "impl", "match", "if", "else",
  "for", "while", "loop", "return", "use", "mod", "crate", "self", "Self",
  "move", "ref", "const", "static", "type", "where", "async", "await",
  "unsafe", "trait", "dyn", "in", "as", "break", "continue",
]);
const RS_TY = new Set([
  "i8", "i16", "i32", "i64", "i128", "isize", "u8", "u16", "u32", "u64",
  "u128", "usize", "f32", "f64", "bool", "char", "str", "String", "Vec",
  "Option", "Result", "Box", "Rc", "Arc", "RefCell", "HashMap",
]);

// Крошечный токенизатор Rust: комментарии, строки, времена жизни, ключевые
// слова, типы, макросы, числа, вызовы функций. Достаточно для слайдов.
function rsSpan(src) {
  const out = [];
  const re =
    /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*")|('(\w+)\b)|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*!)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, life, num, mac, word] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (life) out.push(<span key={out.length} className="rs-life">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (mac) out.push(<span key={out.length} className="rs-mac">{tok}</span>);
    else if (word) {
      let cls = "";
      if (RS_KW.has(word)) cls = "rs-kw";
      else if (RS_TY.has(word)) cls = "rs-ty";
      else if (/^[A-Z]/.test(word)) cls = "rs-ty";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>{word}</span>
        ) : (
          <span key={out.length}>{word}</span>
        ),
      );
    } else out.push(<span key={out.length}>{tok}</span>);
  }
  return out;
}

function RustCode({ children }) {
  return <pre className="rs-code">{rsSpan(children)}</pre>;
}

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОСНОВЫ / ГЛАВА 1</span>
      <span>{String(n).padStart(2, "0")} / 17</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

function Node({ mono, title, sub, kind }) {
  return (
    <div className={`s-node ${kind || ""}`}>
      <span className={mono ? "s-node-mono" : "s-node-title"}>{title}</span>
      {sub && <span className="s-node-sub">{sub}</span>}
    </div>
  );
}

const Cmd = ({ children }) => (
  <div className="s-cmd">
    <pre>{children}</pre>
  </div>
);

const Arr = () => <span className="s-arr">→</span>;
const Down = () => <span className="s-arr">↓</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title="What is Rust?"
      sub="Системный язык программирования"
      main="Скорость как в си, безопасность памяти — на этапе компиляции."
    >
      <div className="s-cols">
        <Node kind="green" title="Fast" sub="Производительность уровня C/C++" />
        <Node kind="green" title="Safe" sub="Память проверяет компилятор" />
        <Node kind="green" title="No GC" sub="Без сборщика мусора" />
      </div>
      <div className="s-label">ГДЕ РОДИЛСЯ</div>
      <div className="s-grid2">
        <Node mono title="Mozilla" sub="Исследовательский проект 2006 → 1.0 в 2015" />
        <Node mono title="Stack Overflow" sub="Самый любимый язык разработчиков" />
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Memory bugs"
      sub="Проблема, которую решает Rust"
      main="~70% критичных уязвимостей — ошибки работы с памятью."
    >
      <div className="s-cols">
        <Node mono title="malloc()" sub="Выделить память" />
        <Arr />
        <Node kind="amber" mono title="free()?" sub="Освободить... и не ошибиться" />
      </div>
      <div className="s-label">КЛАССИЧЕСКИЕ ОШИБКИ</div>
      <div className="s-grid2">
        <Node kind="amber" mono title="use after free" sub="Обращение к освобождённой памяти" />
        <Node kind="amber" mono title="double free" sub="Двойное освобождение" />
        <Node kind="amber" mono title="buffer overflow" sub="Выход за границы буфера" />
        <Node kind="amber" mono title="memory leak" sub="Забыли освободить" />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Three paths"
      sub="Как языки решают проблему памяти"
      main="Раст — третий путь: проверки до запуска, без сборщика мусора."
    >
      <div className="s-cols">
        <Node title="Manual" sub="C / C++ · полный контроль · полная ответственность" />
        <Node title="Garbage collector" sub="Java · Python · Go · паузы и runtime" />
        <Node kind="green" title="Compile-time" sub="Rust · проверяет компилятор · без GC" />
      </div>
      <div className="s-label">ЦЕНА ВОПРОСА</div>
      <Cmd>{"manual    → скорость, но уязвимости\ngc        → удобно, но паузы и память\nrust      → скорость + безопасность"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Ownership"
      sub="Центральное понятие Rust"
      main="Один владелец; при передаче владение перемещается."
    >
      <RustCode>{`fn main() {
    let s1 = String::from("data");
    let s2 = s1;      // ownership moves -> s1
    // println!("{}", s1);  // ERROR: s1 is gone
}`}</RustCode>
      <div className="s-cols">
        <Node mono title="s1: String" sub="Владелец до move" />
        <Arr />
        <Node kind="green" mono title="s2: String" sub="Новый владелец" />
        <Node kind="amber" mono title="s1" sub="Использовать нельзя" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Borrowing"
      sub="Доступ без передачи владения"
      main="Правило: много читателей ИЛИ один писатель — проверяет компилятор."
    >
      <RustCode>{`fn len(s: &String) -> usize {
    s.chars().count()
}

let text = String::from("hello");
let n = len(&text);   // borrow, not move`}</RustCode>
      <div className="s-label">ЧТО ИСКЛЮЧАЕТ</div>
      <div className="s-grid2">
        <Node mono title="data races" sub="Гонки данных" />
        <Node mono title="dangling refs" sub="Висячие ссылки" />
        <Node mono title="use after free" sub="Мёртвая память" />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Compiler as mentor"
      sub="Лучшие ошибки в индустрии"
      main="Компилятор объясняет причину и подсказывает исправление."
    >
      <RustCode>{`error[E0382]: borrow of moved value: \`s1\`
  --> src/main.rs:4:20
   |
3  |     let s2 = s1;
   |              -- value moved here
4  |     println!("{}", s1);
   |                    ^^ value borrowed here
help: consider cloning the value`}</RustCode>
      <div className="s-cols">
        <Node kind="amber" mono title="where" sub="Файл и строка ошибки" />
        <Node mono title="why" sub="Что произошло" />
        <Node kind="green" mono title="help" sub="Как починить" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Zero-cost abstractions"
      sub="Удобство без платы за него"
      main="Высокоуровневый код работает со скоростью ручного цикла."
    >
      <div className="s-cols">
        <Node title="Iterators" sub="Цепочки обработок" />
        <Node title="Closures" sub="Функции как значения" />
        <Node title="Generics" sub="Обобщённый код" />
      </div>
      <Down />
      <div className="s-cols">
        <Node kind="green" mono title="machine code" sub="Разворачивается на этапе компиляции" />
        <Node kind="green" mono title="≈ C speed" sub="Без runtime и интерпретации" />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="No garbage collector"
      sub="Предсказуемая память"
      main="Память освобождается в момент выхода владельца — без пауз."
    >
      <div className="s-label">ЖИЗНЬ ЗНАЧЕНИЯ</div>
      <div className="s-blocks">
        <div className="s-block">alloc</div>
        <div className="s-block changed">use</div>
        <div className="s-block changed">drop</div>
      </div>
      <div className="s-grid2">
        <Node title="С GC" sub="Сборщик может остановить программу в любой момент" kind="amber" />
        <Node kind="green" title="Rust" sub="drop — строго в известный момент" />
      </div>
      <p className="s-hint">Поэтому Rust — для игр, realtime, embedded и ОС.</p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Cargo"
      sub="Сборка, пакеты и тесты"
      main="Вся работа с проектом — несколько команд карго."
    >
      <Cmd>{"cargo new demo    — создать проект\ncargo build      — собрать\ncargo run        — запустить\ncargo test       — тесты"}</Cmd>
      <div className="s-cols">
        <Node mono title="Cargo.toml" sub="Манифест проекта" />
        <Arr />
        <Node kind="green" mono title="crates.io" sub="Каталог библиотек-крейтов" />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Hello, world!"
      sub="Первая программа"
      main="Три строки: главная функция и макрос печати."
    >
      <RustCode>{`fn main() {
    println!("Hello, world!");
}`}</RustCode>
      <div className="s-grid2">
        <Node mono title="fn main()" sub="Точка входа программы" />
        <Node kind="amber" mono title="println!" sub="! — макрос, а не функция" />
      </div>
      <p className="s-hint">Точка с запятой — конец высказывания.</p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Variables"
      sub="Неизменяемость по умолчанию"
      main="let — константа по смыслу; mut — явное разрешение менять."
    >
      <RustCode>{`let x = 5;        // immutable by default
// x = 6;         // ERROR: cannot assign twice

let mut y = 10;   // \`mut\` = mutable
y += 1;           // ok`}</RustCode>
      <div className="s-cols">
        <Node kind="green" mono title="let" sub="Значение зафиксировано" />
        <Node kind="amber" mono title="let mut" sub="Разрешено изменять" />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Types"
      sub="Строгие, но не занудные"
      main="Типы-обёртки заменяют нулевые указатели и исключения."
    >
      <div className="s-label">СКАЛЯРНЫЕ</div>
      <div className="s-cols">
        <Node mono title="i32 u64 usize" sub="Целые" />
        <Node mono title="f64" sub="Дробные" />
        <Node mono title="bool char" sub="Логика и символы" />
      </div>
      <div className="s-label">СОСТАВНЫЕ И ОСОБЫЕ</div>
      <div className="s-cols">
        <Node mono title="tuple array" sub="Кортежи и массивы" />
        <Node mono title="&str / String" sub="Два вида строк" />
        <Node kind="amber" mono title="Option / Result" sub="«Нет значения» и «Ошибка»" />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Where Rust runs"
      sub="Область применения"
      main="Везде, где одновременно нужны скорость и надёжность."
    >
      <div className="s-grid2">
        <Node mono title="CLI tools" sub="Утилиты командной строки" />
        <Node mono title="Web servers" sub="Серверы и прокси" />
        <Node mono title="Databases" sub="Хранилища данных" />
        <Node mono title="Embedded" sub="Встраиваемые системы" />
        <Node mono title="WASM" sub="Код в браузере" />
        <Node mono title="OS" sub="Код в ядре Linux" />
      </div>
      <p className="s-hint">Firefox, Dropbox, Cloudflare, Discord — на горячих участках.</p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Community"
      sub="Культура документации"
      main="Много лет — самый любимый язык в опросах разработчиков."
    >
      <div className="s-bar-wrap">
        <div className="s-bar"><div style={{ width: "86%" }} /></div>
        <div className="s-note">«Most loved language», Stack Overflow</div>
      </div>
      <div className="s-grid2">
        <Node kind="green" title="The Book" sub="Официальная бесплатная книга" />
        <Node kind="green" title="docs.rs" sub="Документация на каждый крейт" />
        <Node title="Friendly compiler" sub="Ошибки учат, а не ругают" />
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Learning curve"
      sub="Честно о входе"
      main="Медленный вход — плата за гарантию: скомпилировалось — работает."
    >
      <div className="s-blocks">
        <div className="s-block">week 1 · fight</div>
        <div className="s-block changed">weeks 2–4 · rules</div>
        <div className="s-block changed">month 2+ · flow</div>
      </div>
      <div className="s-grid2">
        <Node kind="amber" title="Борьба" sub="Компилятор заворачивает «рабочий» код" />
        <Node kind="green" title="Прорыв" sub="Правила становятся интуицией" />
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Book map"
      sub="Что будет дальше"
      main="Каждая тема — отдельная глава, которую удобно слушать в дороге."
    >
      <div className="s-grid2">
        <Node mono title="Ownership" sub="Владение и заимствование" />
        <Node mono title="Types + match" sub="Типы и образцы" />
        <Node mono title="Traits" sub="Трейты и дженерики" />
        <Node mono title="Errors" sub="Option / Result без исключений" />
        <Node mono title="Collections" sub="Vec, String, HashMap" />
        <Node mono title="Concurrency" sub="Потоки без страха" />
      </div>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Summary"
      sub="Итог главы"
      main="Следующий шаг — установить тулчейн и написать первую программу."
    >
      <div className="s-cols">
        <Node kind="green" mono title="safe" sub="Память без GC" />
        <Node kind="green" mono title="checked" sub="Проверки до запуска" />
        <Node kind="green" mono title="cargo" sub="Экосистема" />
      </div>
      <div className="s-label">ЧЕК-ЛИСТ ГЛАВЫ</div>
      <Cmd>{"[x] зачем появился Rust\n[x] владение и заимствование — на пальцах\n[x] карго и первая программа\n[ ] установить rustup — следующий шаг"}</Cmd>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R1 = {
  "10:1": [
    S01,
    S02,
    S03,
    S04,
    S05,
    S06,
    S07,
    S08,
    S09,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R1).
export const SLIDE_TITLES_R1 = {
  "10:1": [
    "Что такое Rust",
    "Проблема памяти",
    "Три пути",
    "Владение",
    "Заимствование",
    "Компилятор-наставник",
    "Нулевая стоимость",
    "Без сборщика мусора",
    "Карго",
    "Первая программа",
    "Переменные",
    "Типы данных",
    "Где используется",
    "Сообщество",
    "Как учить",
    "План книги",
    "Итог",
  ],
};
