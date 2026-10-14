// Слайды для «Изучаем Rust», глава 5 — «Обработка ошибок».
// Тот же дизайн-код, что и в главе 1: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

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
      <span>ДАННЫЕ И АБСТРАКЦИИ / ГЛАВА 5</span>
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
      title="Error handling"
      sub="Глава 5 · Паника и Result"
      main="Два сорта ошибок — два механизма; исключений нет вовсе."
    >
      <div className="s-cols">
        <Node kind="amber" mono title="panic!" sub="Непоправимые: продолжать нельзя" />
        <Node kind="green" mono title="Result" sub="Ожидаемые: может не удаться" />
      </div>
      <div className="s-label">ПОЧЕМУ БЕЗ ИСКЛЮЧЕНИЙ ЛУЧШЕ</div>
      <div className="s-cols">
        <Node title="Ни один вызов не выстрелит мимо" sub="Система типов не даст забыть про неудачу — обработать заставит компилятор" />
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Panic"
      sub="Непоправимая ошибка"
      main="Паника — пожарная сигнализация: не тушим, а эвакуируемся."
    >
      <div className="s-cols">
        <Node kind="amber" mono title="v[99]" sub="Индекс за границей" />
        <Node kind="amber" mono title="n / 0" sub="Деление на ноль" />
      </div>
      <div className="s-label">ЧТО ПРОИСХОДИТ</div>
      <div className="s-blocks">
        <div className="s-block">печатает сообщение с местом ошибки</div>
        <div className="s-block changed">разматывает стек: drop у всех владельцев</div>
        <div className="s-block changed">завершает программу</div>
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="panic!"
      sub="Своими руками"
      main="Паникуй сам — лишь когда дальше работать нельзя."
    >
      <RustCode>{`let home = config.get("home");
if home.is_none() {
    panic!("нет домашней папки в конфиге");
}`}</RustCode>
      <div className="s-grid2">
        <Node kind="green" title="Примеры и тесты" sub="Нарушено предположение — громко падаем, не тащим мусор" />
        <Node kind="amber" title="Библиотеки" sub="Только для ошибок программиста, не пользователя" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Result"
      sub="Ожидаемые ошибки"
      main="Result в сигнатуре — уже документация: операция может не удаться."
    >
      <RustCode>{`enum Result<T, E> {
    Ok(T),    // успех: значение внутри
    Err(E),   // неудача: описание ошибки
}

fn read_config() -> Result<Config, IoError> { /* ... */ }`}</RustCode>
      <div className="s-cols">
        <Node kind="green" mono title="Ok(T)" sub="Получилось" />
        <Node kind="amber" mono title="Err(E)" sub="Причина внутри" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Result vs Option"
      sub="Разные вопросы — разные типы"
      main="Причина, спрятанная в Option, обижает пользователя: «что-то не получилось», без деталей."
    >
      <div className="s-table">
        <div>
          <span className="s-path accent">Option</span>
          <span>есть ли значение: config.get("token")</span>
        </div>
        <div>
          <span className="s-path accent">Result</span>
          <span>что пошло не так: File::open(path)</span>
        </div>
      </div>
      <div className="s-cols">
        <Node mono title="поле конфига" sub="Его просто может не быть" />
        <Node kind="green" mono title="открытие файла" sub="Десять причин отказать — причина внутри" />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="match"
      sub="Полный контроль над исходом"
      main="Пока ветка ошибки не обработана, программа не соберётся."
    >
      <RustCode>{`match File::open("app.toml") {
    Ok(file) => load(file),
    Err(e) => {
        eprintln!("не открылось: {e}");
        Config::default()   // запасной вариант
    }
}`}</RustCode>
      <p className="s-hint">Компилятор не даст рассмотреть только удачный исход.</p>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="unwrap"
      sub="Ленивый путь"
      main="unwrap — короткий путь с паникой внутри; в продакшене это мина."
    >
      <RustCode>{`let n = "42".parse::<i32>().unwrap();     // тест: ок
let f = File::open("app.toml").unwrap();  // прод: мина`}</RustCode>
      <div className="s-grid2">
        <Node kind="green" mono title="unwrap()" sub="Примеры, тесты, доказуемая невозможность ошибки" />
        <Node kind="amber" mono title="unwrap()" sub="Продакшен: сухое сообщение, случайное место падения" />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="expect"
      sub="Паника с объяснением"
      main="В прототипах и тестах expect — разумный минимум вежливости."
    >
      <RustCode>{`let f = File::open("app.toml")
    .expect("ожидал конфиг в домашней папке");`}</RustCode>
      <div className="s-cols">
        <Node mono title="unwrap" sub="Сухое сообщение без подробностей" />
        <Node kind="green" mono title="expect(msg)" sub="Хотя бы объяснит нарушенное предположение" />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Propagate by hand"
      sub="Ошибка решает не средний слой"
      main="Логировать, показывать окно или повторить попытку — дело верхних этажей."
    >
      <RustCode>{`fn read(path: &str) -> Result<String, io::Error> {
    match File::open(path) {
        Ok(f) => read_all(f),   // успех — работаем
        Err(e) => Err(e),       // неудача — немедленно наверх
    }
}`}</RustCode>
      <p className="s-hint">Работает, но многословно — и повторяется в каждой функции.</p>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="The ? operator"
      sub="Один символ вместо матча"
      main="Сделай это, а не выйдет — пусть разбирается вызывающий."
    >
      <RustCode>{`fn read(path: &str) -> Result<String, io::Error> {
    let mut f = File::open(path)?;    // не вышло? верни ошибку выше
    let mut s = String::new();
    f.read_to_string(&mut s)?;        // и здесь тоже
    Ok(s)
}`}</RustCode>
      <div className="s-cols">
        <Node mono title="expr?" sub="Успех: значение распаковано" />
        <Node kind="green" mono title="Err" sub="Ошибка: немедленный возврат из функции" />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="? and the call stack"
      sub="Куда уходит ошибка"
      main="? работает только в функциях, которые сами возвращают Result или Option."
    >
      <div className="s-tree">
        <Node kind="green" mono title="main()" sub="Наконец разбирается с Err" />
        <Down />
        <Node mono title="load_config()" sub="Передаёт дальше через ?" />
        <Down />
        <Node kind="amber" mono title="File::open(path)?" sub="Ошибка родилась здесь" />
      </div>
      <div className="s-cols">
        <Node kind="amber" mono title="fn -> Result | Option" sub="Иначе ? просто не соберётся; по знакам видно места риска" />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="One error type"
      sub="? преобразует сам"
      main="У каждой функции один понятный тип ошибки; различия сглаживаются на входе."
    >
      <RustCode>{`fn load() -> Result<Config, AppError> {
    let text = fs::read_to_string("app.toml")?;  // io::Error -> AppError
    let cfg = parse_config(&text)?;              // ParseError -> AppError
    Ok(cfg)
}`}</RustCode>
      <div className="s-cols">
        <Node mono title="io::Error" sub="Файловая" />
        <Node mono title="ParseError" sub="Разбор текста" />
        <Arr />
        <Node kind="green" mono title="AppError" sub="Один тип на выходе" />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Custom errors"
      sub="Enum с вариантом на каждую неудачу"
      main="Библиотека сообщает об ошибке, приложение принимает решение."
    >
      <RustCode>{`enum AppError {
    Io(io::Error),          // файловая
    Parse(ParseError),      // текст не разобрался
    MissingField(String),   // в конфиге нет поля
}`}</RustCode>
      <div className="s-grid2">
        <Node kind="green" mono title="thiserror" sub="Библиотекам: чёткие типы ошибок" />
        <Node kind="green" mono title="anyhow" sub="Приложениям: общий ящик с контекстом" />
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Messages for humans"
      sub="Контекст к всплывающей ошибке"
      main="Хорошие сообщения об ошибках — половина репутации программы."
    >
      <Cmd>{"плохо:   нет такого файла\nхорошо:  не удалось прочитать настройки —\n         нет app.toml в домашней папке"}</Cmd>
      <div className="s-cols">
        <Node kind="amber" title="Загадка" sub="Сбой пользователь простит, а загадку — нет" />
        <Node kind="green" title="Причина и контекст" sub="Не просто «нет файла», а где искали и зачем" />
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Rules"
      sub="Сведём в одну таблицу"
      main="Баг — паникуй; капризы внешнего мира — возвращай Result."
    >
      <div className="s-table">
        <div>
          <span className="s-path accent">паника</span>
          <span>баги и невозможные состояния</span>
        </div>
        <div>
          <span className="s-path accent">Result</span>
          <span>всё, что может не получиться по вине внешнего мира</span>
        </div>
        <div>
          <span className="s-path accent">unwrap / expect</span>
          <span>тесты, примеры, доказуемая невозможность ошибки</span>
        </div>
        <div>
          <span className="s-path accent">?</span>
          <span>обычный код; библиотеки почти никогда не паникуют</span>
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="What's next"
      sub="Мост к абстракциям"
      main="Следующая глава — трейты и обобщённые типы: код для многих типов без потери скорости."
    >
      <div className="s-cols">
        <Node kind="green" title="Умеем" sub="Описывать данные, собирать в коллекции, встречать неудачи" />
        <Node mono title="Traits + Generics" sub="Глава 6 · главное оружие абстракций в Расте" />
      </div>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Summary"
      sub="Итог"
      main="Выбирай по смыслу: баг — паникуй, внешний мир — Result."
    >
      <div className="s-cols">
        <Node kind="amber" mono title="panic!" sub="Громкое падение с размоткой стека" />
        <Node kind="green" mono title="Result" sub="Ok и Err; неудачу не забыть заставит компилятор" />
        <Node mono title="?" sub="Передаст наверх и преобразует тип" />
      </div>
      <div className="s-label">ЧЕК-ЛИСТ ГЛАВЫ</div>
      <Cmd>{"[x] паника — для багов, Result — для внешнего мира\n[x] матч: полный контроль над исходом\n[x] unwrap и expect — короткие пути с паникой\n[x] ? — передать наверх, попутно преобразовав тип"}</Cmd>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R5 = {
  "10:5": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R5).
export const SLIDE_TITLES_R5 = {
  "10:5": [
    "Обработка ошибок",
    "Паника",
    "panic! своими руками",
    "Result",
    "Result и Option",
    "Матч",
    "unwrap",
    "expect",
    "Передача наверх",
    "Оператор ?",
    "? и стек вызовов",
    "Один тип ошибки",
    "Свои типы ошибок",
    "Сообщения для людей",
    "Практические правила",
    "Что дальше",
    "Итог",
  ],
};
