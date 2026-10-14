// Слайды для «Изучаем Rust», глава 4 — «Коллекции: Vec, String, HashMap».
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
      <span>ДАННЫЕ И АБСТРАКЦИИ / ГЛАВА 4</span>
      <span>{String(n).padStart(2, "0")} / 16</span>
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

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title="Collections"
      sub="Глава 4 · Vec, String, HashMap"
      main="Три рабочие лошадки закрывают большинство повседневных задач."
    >
      <div className="s-cols">
        <Node mono title="Vec" sub="Растущий массив одного типа" />
        <Node mono title="String" sub="Владеющий текст в UTF-8" />
        <Node mono title="HashMap" sub="Пары ключ-значение" />
      </div>
      <div className="s-label">ПОЧЕМУ ЭТО ВАЖНО</div>
      <div className="s-grid2">
        <Node title="Много значений сразу" sub="Логи, корзина, настройки — коллекции растут и сжимаются на ходу" />
        <Node kind="green" title="Данные в куче" sub="В полную силу действуют правила владения из главы 2" />
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Vec: new + push"
      sub="Растущий массив"
      main="Под капотом — указатель, длина и ёмкость; место кончилось — переезд в блок побольше."
    >
      <RustCode>{`let mut v: Vec<i32> = Vec::new();  // пустой вектор
v.push(5);                         // добавить в конец
v.push(7);
let w = vec![1, 2, 3];             // литерал через макрос`}</RustCode>
      <div className="s-cols">
        <Node mono title="Vec" sub="ptr · len · cap" />
        <Arr />
        <Node kind="green" mono title="куча" sub="элементы лежат подряд" />
      </div>
      <p className="s-hint">Ёмкость растёт с запасом — поэтому push в среднем стоит одинаково дёшево.</p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Index vs get"
      sub="Два способа прочитать элемент"
      main="За границей чужая память не читается: паника или None — по твоему выбору."
    >
      <RustCode>{`let v = vec![10, 20, 30];
let a = v[1];       // 20; за границей — немедленная паника
let b = v.get(9);   // None: отсутствие как значение`}</RustCode>
      <div className="s-cols">
        <Node kind="amber" mono title="v[i]" sub="Краш с понятной ошибкой" />
        <Node kind="green" mono title="v.get(i)" sub="Option — сам решаешь, что делать" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Iteration"
      sub="Три способа перебрать вектор"
      main="Вектор владеет элементами: умирает он — умирают и они."
    >
      <RustCode>{`let mut v = vec![1, 2, 3];

for x in &v     { println!("{x}"); }   // читаем
for x in &mut v { *x *= 10; }          // меняем на месте
for x in v      { consume(x); }        // забрали во владение: v больше нет`}</RustCode>
      <div className="s-cols">
        <Node mono title="&v" sub="Только читать" />
        <Node mono title="&mut v" sub="Менять элементы" />
        <Node kind="green" mono title="v" sub="Разобрать вектор" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="One type per Vec"
      sub="Все элементы обязаны быть одного типа"
      main="Разные виды данных упакуй в enum — и храни его в векторе."
    >
      <RustCode>{`enum Cell {
    Num(i32),
    Text(String),
}

let row = vec![
    Cell::Num(3),
    Cell::Text(String::from("ok")),
];  // один тип, разное содержимое`}</RustCode>
      <p className="s-hint">Числа и строки в один список без обёртки компилятор не пустит.</p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="String vs &str"
      sub="Владелец и взгляд"
      main="Литерал в кавычках — это &str: заимствованный срез, а не владелец."
    >
      <RustCode>{`let owner = String::from("курс");  // владелец: можно расти
let view: &str = &owner;           // срез: только чтение
let lit: &str = "литерал";         // литерал — тоже срез`}</RustCode>
      <div className="s-table">
        <div>
          <span className="s-path accent">String</span>
          <span>владеет байтами в куче — расширяй, передавай, меняй</span>
        </div>
        <div>
          <span className="s-path accent">&str</span>
          <span>взгляд на текст — только чтение</span>
        </div>
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="UTF-8"
      sub="Символы разной длины"
      main="len() меряет байты, а не буквы; символ по номеру Раст честно запрещает."
    >
      <RustCode>{`let s = String::from("привет");
s.len();    // 12: байты, а не буквы
// s[0];    // ERROR: байт может попасть в середину символа`}</RustCode>
      <div className="s-label">СКОЛЬКО БАЙТОВ У СИМВОЛА</div>
      <div className="s-blocks">
        <div className="s-block">"a" — 1 байт</div>
        <div className="s-block changed">"п" — 2 байта</div>
        <div className="s-block changed">эмодзи — 4 байта</div>
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Concatenation"
      sub="Плюс и push_str"
      main="Плюс забирает левую строку во владение; дописывать лучше push_str."
    >
      <RustCode>{`let s1 = String::from("log: ");
let s2 = String::from("2026");

let s3 = s1 + &s2;   // s1 перемещён — им больше не пользоваться

let mut s = String::from("log: ");
s.push_str("2026");  // дописали на месте, без переселений`}</RustCode>
      <div className="s-cols">
        <Node kind="amber" mono title="a + b" sub="Забирает левую строку" />
        <Node kind="green" mono title="push_str" sub="Дописывает на месте" />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="format!"
      sub="Сборка строки из кусочков"
      main="Подставь значения в шаблон — ничего ни у кого не забирая."
    >
      <RustCode>{`let who = "мир";
let msg = format!("{who}, привет!");    // свежая строка
let line = format!("{} из {}", 4, 16);  // и здесь ничего не забрано`}</RustCode>
      <p className="s-hint">В реальном коде почти вся сборка текста — это format!.</p>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="HashMap"
      sub="Словарь: ключ → значение"
      main="Доступ по ключу честный: возвращает Option, потому что ключа может не быть."
    >
      <RustCode>{`use std::collections::HashMap;

let mut scores = HashMap::new();
scores.insert("анна", 90);
scores.insert("борис", 75);
scores.insert("анна", 95);      // тот же ключ — замена старого
let a = scores.get("анна");     // Some(&95)
let z = scores.get("зина");     // None`}</RustCode>
      <div className="s-cols">
        <Node mono title="insert(k, v)" sub="Вставить или заменить" />
        <Node kind="green" mono title="get(k)" sub="Option: нашлось или нет" />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Ownership in map"
      sub="Таблица забирает содержимое себе"
      main="Ключи и значения — собственность таблицы; нужен оригинал — отдай clone()."
    >
      <RustCode>{`let mut m = HashMap::new();

let k = String::from("цвет");
m.insert(k, 3);              // строка переехала в таблицу
// println!("{k}");          // ERROR: k перемещён

let key = String::from("тон");
m.insert(key.clone(), 9);    // оригинал нужен? отдай копию`}</RustCode>
      <p className="s-hint">Числовые ключи копируются бесплатно — для них вопрос отпадает.</p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="entry()"
      sub="Вставить-или-изменить одним движением"
      main="Подсчёт слов: одна операция вместо проверки, чтения и записи."
    >
      <RustCode>{`let mut counts: HashMap<String, i32> = HashMap::new();

for word in text.split_whitespace() {
    let c = counts.entry(word.to_string()).or_insert(0);
    *c += 1;   // пусто? положили 0. есть? увеличили
}`}</RustCode>
      <div className="s-cols">
        <Node mono title="entry(k)" sub="Взгляд на ячейку" />
        <Arr />
        <Node mono title="or_insert(0)" sub="Положи, если пусто" />
        <Arr />
        <Node kind="green" mono title="*c += 1" sub="Изменить на месте" />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Iterating a map"
      sub="Пары сразу, порядка нет"
      main="Перебор отдаёт ключ и значение сразу, но порядок обхода не гарантирован."
    >
      <RustCode>{`for (k, v) in &scores {
    println!("{k} → {v}");
}
// порядок обхода хеш-таблица выбирает сама`}</RustCode>
      <div className="s-grid2">
        <Node kind="amber" title="Порядка нет" sub="Ключи разложены так, как удобно для скорости" />
        <Node kind="green" mono title="BTreeMap" sub="Нужен порядок — сортированная родня на дереве" />
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Choosing"
      sub="Какая коллекция под задачу"
      main="На векторе, строке и хеш-таблице держится девять десятых реального кода."
    >
      <div className="s-table">
        <div>
          <span className="s-path accent">Vec</span>
          <span>порядок и доступ по номеру</span>
        </div>
        <div>
          <span className="s-path accent">HashMap</span>
          <span>быстрый поиск по ключу</span>
        </div>
        <div>
          <span className="s-path accent">String</span>
          <span>владеющий текст</span>
        </div>
      </div>
      <div className="s-label">ЕСЛИ ЗАДАЧА НЕСТАНДАРТНАЯ</div>
      <div className="s-grid2">
        <Node mono title="HashSet" sub="Множество уникальных значений" />
        <Node mono title="VecDeque" sub="Двусторонняя очередь" />
        <Node mono title="BTreeMap" sub="Словарь по возрастанию ключей" />
        <Node mono title="BTreeSet" sub="Множество с порядком" />
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="What's next"
      sub="Мост к ошибкам"
      main="Реальные программы постоянно что-то ломают — нужен достойный ответ."
    >
      <div className="s-cols">
        <Node kind="green" title="Коллекции освоены" sub="Данные умеем собирать, читать и искать" />
        <Node kind="amber" title="Но всё ломается" sub="Ключа нет · файл не открылся · текст не разобрался" />
      </div>
      <div className="s-label">СЛЕДУЮЩАЯ ГЛАВА</div>
      <div className="s-cols">
        <Node kind="green" mono title="Глава 5 · Обработка ошибок" sub="Как Раст обходится без единого исключения" />
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Summary"
      sub="Итог"
      main="Порядок — вектор, поиск — словарь, текст — стринг."
    >
      <div className="s-cols">
        <Node kind="green" mono title="Vec" sub="push · [] · get · for" />
        <Node kind="green" mono title="String" sub="владеет текстом · len — байты · format!" />
        <Node kind="green" mono title="HashMap" sub="insert · get · entry" />
      </div>
      <div className="s-label">ЧЕК-ЛИСТ ГЛАВЫ</div>
      <Cmd>{"[x] вектор: new и push, доступ по номеру и get\n[x] строка: String против &str, сборка через format!\n[x] словарь: insert, get, entry-or-insert\n[ ] следующий шаг — ошибки: паника и Result"}</Cmd>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R4 = {
  "10:4": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R4).
export const SLIDE_TITLES_R4 = {
  "10:4": [
    "Коллекции",
    "Вектор",
    "Индекс и get",
    "Перебор",
    "Один тип",
    "String и &str",
    "UTF-8",
    "Склейка строк",
    "format!",
    "Хеш-таблица",
    "Владение в словаре",
    "entry",
    "Перебор словаря",
    "Выбор коллекции",
    "Что дальше",
    "Итог",
  ],
};
