// Слайды для «Изучаем Rust», глава 2 — «Владение и заимствование».
// Тот же дизайн-код, что и у главы 1: рубрика + номер, «ГЛАВНОЕ» внизу.
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
      <span>ЯДРО ЯЗЫКА / ГЛАВА 2</span>
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
      title="Владение и заимствование"
      sub="Глава 2 · Как компилятор управляет памятью"
      main="Память не освободится дважды, а к удалённым данным никто не обратится."
    >
      <RustCode>{`let s = String::from("курс");
// у s ровно один владелец
// когда владелец умрёт — память освободится сама`}</RustCode>
      <div className="s-cols">
        <Node kind="green" title="Без GC" sub="Никакого сборщика мусора" />
        <Node
          kind="green"
          title="Без runtime"
          sub="Нет среды выполнения для памяти"
        />
        <Node
          kind="green"
          title="До запуска"
          sub="Все проверки делает компилятор"
        />
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Один владелец"
      sub="Главный закон владения"
      main="У каждого значения ровно один владелец; вышел из области видимости — память свободна."
    >
      <RustCode>{`fn main() {
    let s = String::from("курс");
    // ... работаем со s
}   // s умирает здесь — память освобождена`}</RustCode>
      <div className="s-blocks">
        <div className="s-block">let s = ... — владелец появился</div>
        <div className="s-block changed">
          конец блока — drop в известный момент
        </div>
      </div>
      <p className="s-hint">
        Момент смерти значения предсказуем, как бой часов.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Перемещение"
      sub="Присваивание для данных в куче"
      main="Новым владельцем становится вторая переменная, старая теряет права на данные."
    >
      <RustCode>{`let s1 = String::from("данные");
let s2 = s1;            // владение переехало: s1 -> s2
// println!("{}", s1);  // ОШИБКА: s1 больше не владеет`}</RustCode>
      <div className="s-cols">
        <Node mono title="s1: String" sub="Старый владелец" />
        <Arr />
        <Node kind="green" mono title="s2: String" sub="Новый владелец" />
        <Node kind="amber" mono title="s1" sub="Использовать нельзя" />
      </div>
      <p className="s-hint">
        Простые числа при этом просто копируются — об этом дальше.
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Зачем move"
      sub="Страховка от двойного освобождения"
      main="Два владельца одной памяти — это double free; перемещение исключает его при компиляции."
    >
      <RustCode>{`let a = String::from("x");
let b = a;   // move: второго владельца не появилось`}</RustCode>
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="free() №1"
          sub="Первый «владелец» прощается с байтами"
        />
        <Node
          kind="amber"
          mono
          title="free() №2"
          sub="Второе освобождение тех же байтов портит память"
        />
      </div>
      <div className="s-cols">
        <Node kind="amber" title="C / C++" sub="Ошибка всплывает при запуске" />
        <Node kind="green" title="Rust" sub="Программа просто не соберётся" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Владение и функции"
      sub="Аргумент — это передача владения"
      main="Отдав значение функции насовсем, дальше им пользоваться нельзя."
    >
      <RustCode>{`fn take(s: String) {
    println!("{}", s);
}   // s умирает вместе с областью видимости функции

let name = String::from("Мария");
take(name);               // владение переехало в функцию
// println!("{}", name);  // ОШИБКА: name уже не наш`}</RustCode>
      <div className="s-cols">
        <Node mono title="name" sub="Владелец" />
        <Arr />
        <Node mono title="take(s)" sub="Функция — новый владелец" />
        <Arr />
        <Node kind="amber" mono title="drop" sub="Конец fn — значение умерло" />
      </div>
      <p className="s-hint">
        Отдать данные и остаться при своих — это заимствование.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Стек и куча"
      sub="Что копируется, а что перемещается"
      main="Всё, что живёт на стеке, копируется автоматически; куча — перемещается."
    >
      <RustCode>{`let x = 5;
let y = x;   // i32 на стеке: копия, обе переменные живы
println!("{} {}", x, y);

let s1 = String::from("текст");
let s2 = s1; // данные в куче: перемещение
// println!("{}", s1);`}</RustCode>
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="i32 f64 bool char"
          sub="Стек — копируется незаметно"
        />
        <Node mono title="String Vec" sub="Куча — перемещается по умолчанию" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Клонирование"
      sub="Явная независимая копия"
      main="clone копирует и данные в куче — увидел clone, значит, здесь настоящее выделение памяти."
    >
      <RustCode>{`let s1 = String::from("оригинал");
let s2 = s1.clone();   // копия: и стек, и куча
println!("{} и {}", s1, s2);   // обе живы`}</RustCode>
      <div className="s-cols">
        <Node mono title="s1" sub="Владелец оригинала" />
        <Arr />
        <Node kind="green" mono title=".clone()" sub="Явное выделение памяти" />
        <Arr />
        <Node kind="green" mono title="s2" sub="Независимая копия" />
      </div>
      <p className="s-hint">
        Дорогое копирование сделано заметным — решение принимается осознанно.
      </p>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Заимствование"
      sub="Доступ без передачи владения"
      main="Ссылка указывает на данные, но владельцем не становится: библиотека — читатели."
    >
      <RustCode>{`fn len(s: &String) -> usize {
    s.chars().count()
}

let text = String::from("владение");
let n = len(&text);            // ссудили ссылку, не владельца
println!("{} {}", text, n);    // text всё ещё наш`}</RustCode>
      <div className="s-cols">
        <Node mono title="text" sub="Владелец — библиотека" />
        <Arr />
        <Node kind="green" mono title="&text" sub="Читатель — не собственник" />
      </div>
      <div className="s-grid2">
        <Node mono title="&T" sub="Неизменяемая: только чтение" />
        <Node mono title="&mut T" sub="Изменяемая: право писать" />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Читатели"
      sub="Неизменяемых ссылок — сколько угодно"
      main="Пока все только читают, испортить данные нельзя — сто читателей одной строки."
    >
      <RustCode>{`let s = String::from("книга");
let r1 = &s;
let r2 = &s;   // читателей — сколько угодно
println!("{} {} {}", r1, r2, s);`}</RustCode>
      <div className="s-tree">
        <Node mono title="s: String" sub="Один владелец" />
        <Down />
        <div className="s-cols">
          <Node kind="green" mono title="r1 = &s" sub="Читатель" />
          <Node kind="green" mono title="r2 = &s" sub="Читатель" />
          <Node kind="green" mono title="rN = &s" sub="Хоть сто" />
        </div>
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Один писатель"
      sub="Изменяемая ссылка — эксклюзивна"
      main="Пока жива изменяемая ссылка, никто не может ни писать, ни даже читать."
    >
      <RustCode>{`let mut score = 0;
let r = &mut score;   // единственный мутатор
*r += 10;
// let r2 = &mut score;    // ОШИБКА: писатель уже есть
// println!("{}", score);  // и читать при нём нельзя`}</RustCode>
      <div className="s-cols">
        <Node mono title="score" sub="Владелец" />
        <Arr />
        <Node
          kind="amber"
          mono
          title="&mut score"
          sub="Один писатель — полная тишина вокруг"
        />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Правило заимствования"
      sub="Либо читатели, либо писатель"
      main="В каждый момент: сколько угодно неизменяемых ссылок или ровно одна изменяемая."
    >
      <div className="s-table">
        <div>
          <span>n × &T</span>
          <span>можно — читают все</span>
        </div>
        <div>
          <span>1 × &mut T</span>
          <span>можно — пишет один</span>
        </div>
        <div>
          <span>&T рядом с &mut T</span>
          <span>нельзя — конфликт</span>
        </div>
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="data race"
          sub="Два участка меняют данные без синхронизации"
        />
        <Node
          kind="green"
          title="Rust"
          sub="Программа с гонкой данных не соберётся"
        />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Висячие ссылки"
      sub="Второй исключённый класс ошибок"
      main="Компилятор проверяет, что значение живёт дольше любой ссылки на него."
    >
      <RustCode>{`fn dangle() -> &String {
    let s = String::from("привет");
    &s   // ОШИБКА: s живёт слишком мало
}

fn owner() -> String {
    String::from("привет")   // ок: возвращаем владельца
}`}</RustCode>
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="dangle()"
          sub="Ссылка переживёт данные — запрещено"
        />
        <Node
          kind="green"
          mono
          title="owner()"
          sub="Возвращай полноценного владельца"
        />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Срезы"
      sub="Заимствование части данных"
      main="Срез — указатель на начало и длина: закладка запоминает страницу, а не переписывает главу."
    >
      <RustCode>{`let s = String::from("ownership");
let part = &s[0..4];   // "owne" — без копии
let all = &s[..];      // вся строка`}</RustCode>
      <div className="s-cols">
        <Node mono title="s" sub="Глава целиком" />
        <Arr />
        <Node
          kind="green"
          mono
          title="&s[0..4]"
          sub="Взгляд на диапазон символов"
        />
      </div>
      <p className="s-hint">
        Ничего не копируется — и у среза тоже нет владения.
      </p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Срезы в функциях"
      sub="Один тип аргумента на все случаи"
      main="Функция со срезом строки сработает и со String, и с её частью, и с литералом."
    >
      <RustCode>{`fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

let title = String::from("высота башни");
first_word(&title);          // String — подойдёт
first_word("первое слово");  // литерал — тоже`}</RustCode>
      <div className="s-grid2">
        <Node mono title="&str" sub="Универсальный параметр" />
        <Node
          kind="green"
          title="Бонус-гарантия"
          sub="Владелец не изменит данные, пока жив срез"
        />
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Как это ощущается"
      sub="Практика: от борьбы к интуиции"
      main="Споришь с компилятором всё реже — класс тревог просто исчез из жизни."
    >
      <div className="s-blocks">
        <div className="s-block">
          первые недели · «значение перемещено», «ссылка занята»
        </div>
        <div className="s-block changed">
          перелом · функции берут ссылки, возвращают владельцев
        </div>
        <div className="s-block changed">
          дальше · clone только там, где действительно нужно
        </div>
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Спор с компилятором"
          sub="Порча памяти, гонки, висячие указатели"
        />
        <Node
          kind="green"
          title="После перелома"
          sub="Эти ошибки невозможны по построению"
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
      sub="Владение — фундамент"
      main="Дальше начинаем строить на фундаменте: собственные типы данных."
    >
      <div className="s-grid2">
        <Node
          mono
          title="struct"
          sub="Структуры: связанные данные в одном целом"
        />
        <Node mono title="enum" sub="Перечисления: значение — одно из списка" />
      </div>
      <p className="s-hint">
        ГЛАВА 3 — описываем собственные типы предметной области.
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
      main="Следующая глава — собственные типы: структуры и перечисления."
    >
      <div className="s-cols">
        <Node kind="green" mono title="1 owner" sub="Один владелец" />
        <Node
          kind="green"
          mono
          title="move / clone"
          sub="Переместить или скопировать"
        />
        <Node kind="green" mono title="& / &mut" sub="Читатели или писатель" />
      </div>
      <div className="s-label">ЧЕК-ЛИСТ ГЛАВЫ</div>
      <Cmd>
        {
          "[x] один владелец — drop при выходе из области видимости\n[x] присваивание и аргументы перемещают владение\n[x] clone — явная независимая копия\n[x] ссылки: много читателей или один писатель\n[x] висячие ссылки и гонки данных — отвергнуты\n[x] срезы — заимствование части данных"
        }
      </Cmd>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R2 = {
  "10:2": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R2).
export const SLIDE_TITLES_R2 = {
  "10:2": [
    "Владение и заимствование",
    "Один владелец",
    "Перемещение",
    "Зачем move",
    "Владение и функции",
    "Стек и куча",
    "Клонирование",
    "Заимствование",
    "Читатели",
    "Один писатель",
    "Правило заимствования",
    "Висячие ссылки",
    "Срезы",
    "Срезы в функциях",
    "Как это ощущается",
    "Что дальше",
    "Итог",
  ],
};
