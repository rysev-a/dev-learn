// Слайды для «Изучаем Rust», глава 3 — «Структуры и перечисления».
// Тот же дизайн-код, что и у предыдущих глав: рубрика + номер, «ГЛАВНОЕ» внизу.
// Один абзац урока = один слайд. Примеры кода — с подсветкой синтаксиса.

const RS_KW = new Set([
  "fn",
  "let",
  "mut",
  "pub",
  "struct",
  "enum",
  "impl",
  "match",
  "if",
  "else",
  "for",
  "while",
  "loop",
  "return",
  "use",
  "mod",
  "crate",
  "self",
  "Self",
  "move",
  "ref",
  "const",
  "static",
  "type",
  "where",
  "async",
  "await",
  "unsafe",
  "trait",
  "dyn",
  "in",
  "as",
  "break",
  "continue",
]);
const RS_TY = new Set([
  "i8",
  "i16",
  "i32",
  "i64",
  "i128",
  "isize",
  "u8",
  "u16",
  "u32",
  "u64",
  "u128",
  "usize",
  "f32",
  "f64",
  "bool",
  "char",
  "str",
  "String",
  "Vec",
  "Option",
  "Result",
  "Box",
  "Rc",
  "Arc",
  "RefCell",
  "HashMap",
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
    if (com)
      out.push(
        <span key={out.length} className="rs-com">
          {tok}
        </span>,
      );
    else if (str)
      out.push(
        <span key={out.length} className="rs-str">
          {tok}
        </span>,
      );
    else if (life)
      out.push(
        <span key={out.length} className="rs-life">
          {tok}
        </span>,
      );
    else if (num)
      out.push(
        <span key={out.length} className="rs-num">
          {tok}
        </span>,
      );
    else if (mac)
      out.push(
        <span key={out.length} className="rs-mac">
          {tok}
        </span>,
      );
    else if (word) {
      let cls = "";
      if (RS_KW.has(word)) cls = "rs-kw";
      else if (RS_TY.has(word)) cls = "rs-ty";
      else if (/^[A-Z]/.test(word)) cls = "rs-ty";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>
            {word}
          </span>
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
      <span>ДАННЫЕ И АБСТРАКЦИИ / ГЛАВА 3</span>
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

// --- сцены ----------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title="Структуры и перечисления"
      sub="Глава 3 · Собственные типы данных"
      main="Структуры собирают данные в целое, перечисления описывают «одно из»."
    >
      <RustCode>{`struct User {
    name: String,
    active: bool,
}

enum Shape {
    Circle(f64),
    Rect { w: f64, h: f64 },
}`}</RustCode>
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="struct"
          sub="Связанные данные — один целый"
        />
        <Node
          kind="green"
          mono
          title="enum"
          sub="Значение — одно из списка вариантов"
        />
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Именованные поля"
      sub="Структура — анкета с подписанными графами"
      main="После объявления тип становится равноправным со встроенными."
    >
      <RustCode>{`struct User {
    name: String,
    email: String,
    active: bool,
}`}</RustCode>
      <div className="s-cols">
        <Node mono title="struct User" sub="Имя + тип у каждого поля" />
        <Arr />
        <Node
          kind="green"
          title="Новый тип"
          sub="User — полноценный тип языка"
        />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Экземпляры"
      sub="Заполняем анкету"
      main="Пропустить поле нельзя; владение относится к структуре целиком — вместе с полями."
    >
      <RustCode>{`let mut u = User {
    name: String::from("Анна"),
    email: String::from("anna@mail.ru"),
    active: true,
};
u.email = String::from("new@mail.ru");   // доступ через точку`}</RustCode>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Пропустил поле"
          sub="Программа не соберётся"
        />
        <Node title="Жизнь экземпляра" sub="Умирает — умирают и все его поля" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Кортежные структуры"
      sub="Поля без имён — только по порядку"
      main="Типы разные, поэтому перепутать цвет и точку нельзя."
    >
      <RustCode>{`struct Color(i32, i32, i32);
struct Point(i32, i32);

let red = Color(255, 0, 0);
let origin = Point(0, 0);

fn draw(p: Point) {}
// draw(red);   // ОШИБКА: ожидалась точка, а не цвет`}</RustCode>
      <div className="s-cols">
        <Node mono title="Color(255, 0, 0)" sub="Числа, но цвет" />
        <Node mono title="Point(0, 0)" sub="Числа, но точка" />
        <Node
          kind="green"
          title="Новый тип"
          sub="Дешёвый способ из готовых частей"
        />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Юнит-структуры"
      sub="Тип вовсе без данных"
      main="Тип-маркер различает ситуации самим фактом своего существования."
    >
      <RustCode>{`struct Marker;   // никаких полей — только имя типа`}</RustCode>
      <div className="s-cols">
        <Node mono title="struct Marker;" sub="Маркер и носитель поведения" />
        <Node kind="green" title="Зачем" sub="Различать ситуации без данных" />
      </div>
      <p className="s-hint">
        В полную силу раскроется, когда дойдём до трейтов.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Методы"
      sub="Блок имплементации"
      main="Первый параметр метода — сам экземпляр; вызов через точку."
    >
      <RustCode>{`struct Rect { w: f64, h: f64 }

impl Rect {
    fn area(&self) -> f64 {
        self.w * self.h
    }
}

let a = Rect { w: 3.0, h: 4.0 };
println!("{}", a.area());   // 12 — вызов через точку`}</RustCode>
      <div className="s-cols">
        <Node mono title="impl Rect" sub="Поведение рядом с данными" />
        <Arr />
        <Node
          kind="green"
          mono
          title="a.area()"
          sub="Один читает, другой меняет"
        />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Конструкторы"
      sub="Ассоциированные функции без экземпляра"
      main="Традиция: у каждого типа есть ::new, который возвращает заполненный экземпляр."
    >
      <RustCode>{`impl Rect {
    fn new(w: f64, h: f64) -> Self {
        Rect { w, h }
    }
}

let a = Rect::new(3.0, 4.0);   // через двойное двоеточие`}</RustCode>
      <div className="s-cols">
        <Node mono title="Rect::new" sub="Без self — не метод" />
        <Arr />
        <Node
          kind="green"
          mono
          title="Self"
          sub="Правильно заполненный экземпляр"
        />
      </div>
      <p className="s-hint">Похожи на статические методы в других языках.</p>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Поведение и ссылки"
      sub="Интерфейс виден в одном месте"
      main="Компилятор применяет к методам правила заимствования из прошлой главы."
    >
      <RustCode>{`impl Rect {
    fn area(&self) -> f64 { self.w * self.h }
    fn grow(&mut self, k: f64) {
        self.w *= k;
        self.h *= k;
    }
}`}</RustCode>
      <Down />
      <div className="s-cols">
        <Node mono title="&self" sub="Только читает" />
        <Node mono title="&mut self" sub="Меняет данные" />
        <Node mono title="self" sub="Забирает во владение" />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Перечисления"
      sub="Варианты несут данные"
      main="Один тип описывает четыре разных события, и каждое несёт свой груз."
    >
      <RustCode>{`enum Message {
    Quit,                        // без данных
    Move { x: i32, y: i32 },     // координаты
    Write(String),               // строка текста
    ChangeColor(i32, i32, i32),  // три числа
}`}</RustCode>
      <div className="s-cols">
        <Node mono title="Message" sub="Один тип — четыре варианта" />
        <Node
          kind="green"
          title="Каждый вариант"
          sub="Со своими данными внутри"
        />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Безопасное объединение"
      sub="Enum против union из си"
      main="Перечисление хранит метку активного варианта — обмануть её невозможно."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="union в C"
          sub="Не помнит, какой вариант активен"
        />
        <Node
          kind="green"
          mono
          title="enum в Rust"
          sub="Метка активного варианта внутри"
        />
      </div>
      <div className="s-label">ВНУТРИ ВАРИАНТА МОЖЕТ ЛЕЖАТЬ</div>
      <div className="s-cols">
        <Node mono title="числа" />
        <Node mono title="строки" />
        <Node mono title="структуры" />
        <Node mono title="перечисления" />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Option"
      sub="Замена нулевого указателя"
      main="Отсутствие значения — полноценное значение: типизированное и проверяемое."
    >
      <RustCode>{`let maybe: Option<i32> = Some(5);
let empty: Option<i32> = None;

// Some(value) — значение есть и лежит внутри
// None         — значения нет`}</RustCode>
      <div className="s-cols">
        <Node kind="green" mono title="Some(v)" sub="Значение внутри" />
        <Node mono title="None" sub="Пусто — но тип известно" />
      </div>
      <div className="s-note amber">
        Изобретатель нулевых ссылок Тони Хоар называл их своей «ошибкой на
        миллиард долларов».
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Null не пройдёт"
      sub="Проверка присутствия при сборке"
      main="Использовать значение из Option, не проверив, нельзя — аварий не будет вовсе."
    >
      <RustCode>{`let user: Option<String> = find(7);

// let n = user.len();   // ОШИБКА: а вдруг None?

match user {
    Some(name) => println!("{}", name),
    None => println!("пользователя нет"),
}`}</RustCode>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Без проверки"
          sub="Не соберётся — и это спасает"
        />
        <Node
          kind="green"
          title="С проверкой"
          sub="Разыменование нуля исключено"
        />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Сопоставление"
      sub="Матч обязан быть исчерпывающим"
      main="Пять вариантов — рассмотри все пять; забытые случаи ловит компилятор."
    >
      <RustCode>{`let msg = Message::Write(String::from("привет"));

match msg {
    Message::Quit => println!("выход"),
    Message::Move { x, y } => println!("{} {}", x, y),
    Message::Write(t) => println!("{}", t),
    Message::ChangeColor(r, g, b) => println!("{} {} {}", r, g, b),
}
// убери любую ветку — программа не соберётся`}</RustCode>
      <div className="s-cols">
        <Node
          kind="green"
          title="Исчерпывающе"
          sub="Каждый вариант рассмотрен"
        />
        <Node
          title="Рефакторинг"
          sub="Новый вариант — покажет все места, где о нём забыли"
        />
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Match-выражение"
      sub="Не инструкция, а выражение"
      main="Каждая ветка выдаёт значение, результат можно сразу присвоить."
    >
      <RustCode>{`let code = 1;
let label = match code {
    0 => "ок",
    1 => "предупреждение",
    _ => "всё остальное",
};
// label == "предупреждение"`}</RustCode>
      <div className="s-grid2">
        <Node kind="green" title="Выражение" sub="Ветки возвращают значение" />
        <Node mono title="_" sub="Универсальный образец: всё остальное" />
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="If let"
      sub="Когда интересен один вариант"
      main="Если значение подходит под образец — делаем одно, иначе — запасное действие."
    >
      <RustCode>{`let maybe = Some(String::from("порт 8080"));

if let Some(v) = maybe {
    println!("есть: {}", v);
} else {
    println!("пусто — идём дальше");
}`}</RustCode>
      <div className="s-grid2">
        <Node mono title="if let" sub="Компактнее полного match" />
        <Node
          kind="green"
          title="Частый гость"
          sub="Рядом с Option: есть — работаем, нет — дальше"
        />
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Что дальше"
      sub="Когда значений становится много"
      main="Дальше — коллекции: вектор, строка и хеш-таблица."
    >
      <div className="s-grid2">
        <Node mono title="Vec<T>" sub="Список значений" />
        <Node mono title="String" sub="Текст, владеющий байтами" />
        <Node mono title="HashMap" sub="Пары ключ — значение" />
      </div>
      <p className="s-hint">
        ГЛАВА 4 — коллекции, где наши типы живут десятками и миллионами.
      </p>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Итог"
      sub="Итог главы"
      main="Следующая глава — коллекции: вектор, строка и хеш-таблица."
    >
      <div className="s-cols">
        <Node kind="green" mono title="struct" sub="Данные в одном типе" />
        <Node kind="green" mono title="impl" sub="Методы и конструкторы" />
        <Node kind="green" mono title="enum" sub="Варианты с данными" />
      </div>
      <div className="s-label">ЧЕК-ЛИСТ ГЛАВЫ</div>
      <Cmd>
        {
          "[x] структуры: именованные, кортежные, юнит\n[x] методы в impl и конструкторы ::new\n[x] enum — варианты несут данные\n[x] Option — типизированная замена null\n[x] match покрывает все варианты, if let — коротко"
        }
      </Cmd>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R3 = {
  "10:3": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R3).
export const SLIDE_TITLES_R3 = {
  "10:3": [
    "Собственные типы",
    "Именованные поля",
    "Экземпляры",
    "Кортежные структуры",
    "Юнит-структуры",
    "Методы",
    "Конструкторы",
    "Поведение и ссылки",
    "Перечисления",
    "Безопасное объединение",
    "Option",
    "Null не пройдёт",
    "Сопоставление",
    "Match-выражение",
    "If let",
    "Что дальше",
    "Итог",
  ],
};
