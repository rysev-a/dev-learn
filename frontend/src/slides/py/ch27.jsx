// Слайды для «Изучаем Python», глава 27 — «Регулярные выражения».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "print", "for", "in", "not", "and", "or", "if", "else", "while", "is",
  "True", "False", "None", "def", "return",
]);

// Крошечный токенизатор Python: комментарии, строки, числа, ключевые слова,
// вызовы функций. Достаточно для слайдов.
function pySpan(src) {
  const out = [];
  const re =
    /(#[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, word] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (word) {
      let cls = "";
      if (PY_KW.has(word)) cls = "rs-kw";
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

function PyCode({ children }) {
  return <pre className="rs-code">{pySpan(children)}</pre>;
}

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ ПИТОН / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 27</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
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

function Cmd({ children }) {
  return (
    <div className="s-cmd">
      <pre>{children}</pre>
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Регулярные выражения"}
      sub={"Глава 27 · Стандартная библиотека"}
      main={"Шаблон описывает не строку, а семейство строк: «три цифры, дефис, четыре цифры»."}
    >
      <div className="s-grid2">
        {[["\\d  \\w  [а-я]", "Символы", "Цифры, буквы, наборы"], ["*  +  ?  {n,m}", "Повторы", "По умолчанию жадные"], ["( )  (?P<name>)", "Группы", "Достать нужные куски"], ["sub · split · findall", "Функции", "Заменить, разрезать, найти все"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Основы шаблона"}
      sub={"Точка, наборы, якоря и функции поиска"}
      main={"search ищет где угодно, match — с начала, fullmatch — всю строку."}
    >
      <PyCode>{`import re

print(bool(re.search(r"\\d\\d", "в 2024 году")))
print(re.search(r"к.т", "кот и кит").group())
print(re.match(r"\\d+", "а123") is None, re.match(r"\\d+", "123а").group())
print(bool(re.fullmatch(r"[а-я]+", "привет")), bool(re.fullmatch(r"[а-я]+", "Привет")))
print(bool(re.search(r"^а", "арбуз")), bool(re.search(r"з$", "арбуз")))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True\nкот\nTrue 123\nTrue False\nTrue True"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Квантификаторы и жадность"}
      sub={"*, +, ?, {n,m}"}
      main={"Жадность — источник половины неожиданностей: добавьте ? и получите минимум."}
    >
      <PyCode>{`import re

print(re.findall(r"\\d{2,4}", "1 22 333 55555"))
print(re.search(r"<.*>", "<b>жирный</b>").group())
print(re.search(r"<.*?>", "<b>жирный</b>").group())
print(re.findall(r"colou?r", "color colour colr"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['22', '333', '5555']\n<b>жирный</b>\n<b>\n['color', 'colour']"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Группы"}
      sub={"Вытащить нужные куски текста"}
      main={"Группы — главный способ не просто проверить, а извлечь данные."}
    >
      <PyCode>{`import re

m = re.search(r"заказ (\\d+) от (\\d+)\\.(\\d+)", "заказ 123 от 05.03")
print(m.group(), m.group(1), m.groups(), m.span())
print(re.findall(r"(\\w+)@(\\w+)\\.ru", "ivan@mail.ru, olga@ya.ru"))
for m in re.finditer(r"\\d+", "a1 b22 c333"):
    print(m.group(), m.start())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"заказ 123 от 05.03 123 ('123', '05', '03') (0, 18)\n[('ivan', 'mail'), ('olga', 'ya')]\n1 1\n22 4\n333 8"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Именованные группы"}
      sub={"(?P<имя>...) и (?:...)"}
      main={"Имя читается лучше номера; незахватывающая группа нужна, когда запоминать не надо."}
    >
      <PyCode>{`import re

pat = re.compile(r"(?P<y>\\d{4})-(?P<m>\\d\\d)-(?P<d>\\d\\d)")
m = pat.search("дата: 2024-03-05")
print(m["y"], m.group("m"), m.groupdict())
print(re.findall(r"(?:кот|пёс)ы?", "коты и пёс, котёнок"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2024 03 {'y': '2024', 'm': '03', 'd': '05'}\n['коты', 'пёс', 'кот']"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"sub и split"}
      sub={"Заменить и разрезать по шаблону"}
      main={"В замене доступны группы (\\1) и даже функция, вычисляющая подстановку."}
    >
      <PyCode>{`import re

print(re.sub(r"\\s+", " ", "много   пробелов\\n тут"))
print(re.sub(r"(\\w+) (\\w+)", r"\\2 \\1", "Иван Петров"))
print(re.sub(r"\\d+", lambda m: str(int(m.group()) * 2), "5 яблок и 12 груш"))
print(re.split(r"[,;]\\s*", "а, б;в,  г"))
print(re.subn("а", "о", "ала"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"много пробелов тут\nПетров Иван\n10 яблок и 24 груш\n['а', 'б', 'в', 'г']\n('оло', 2)"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сырые строки, compile, флаги"}
      sub={"r\"...\", re.compile, re.I, re.M, re.X"}
      main={"Подробный режим re.X — лучший способ записать сложный шаблон: части и пояснения."}
    >
      <PyCode>{`import re

print(len(r"\\d"), len("\\\\d"))
pat = re.compile(r"""
    (\\d{3})   # код
    -
    (\\d{4})   # номер
""", re.X)
print(pat.fullmatch("555-1234").groups())
print(re.findall(r"кот", "Кот КОТ кот", re.I))
print(re.findall(r"^\\w+", "раз\\nдва\\nтри", re.M))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 2\n('555', '1234')\n['Кот', 'КОТ', 'кот']\n['раз', 'два', 'три']"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Границы и проверки контекста"}
      sub={"\\b, (?=...), (?<=...), (?!...)"}
      main={"Проверки контекста не входят в результат, но решают, подходит ли совпадение."}
    >
      <PyCode>{`import re

print(re.findall(r"\\bкот\\b", "кот коты котёл кот."))
print(re.findall(r"\\d+(?=%)", "скидка 20% и 5 штук, 30%"))
print(re.findall(r"(?<=\\$)\\d+", "цена $100 и 200"))
print(re.findall(r"\\b(?!не)\\w+", "не пойду, пойду"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['кот', 'кот']\n['20', '30']\n['100']\n['пойду', 'пойду']"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Практика"}
      sub={"Журнал, почта, телефон"}
      main={"Идеальных шаблонов для почты и телефонов не бывает: проверка лишь отсеивает явный мусор."}
    >
      <PyCode>{`import re

line = "2024-03-05 09:07:03 ERROR сбой диска"
m = re.match(r"(?P<date>\\S+) (?P<time>\\S+) (?P<level>[A-Z]+) (?P<msg>.*)", line)
print(m.groupdict())
text = "почта: ivan@mail.ru, olga@ya.ru; тел. +7-900-123-45-67"
print(re.findall(r"[\\w.]+@[\\w.]+\\w", text))
print(re.findall(r"\\+7(?:-\\d{2,3}){4}", text))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'date': '2024-03-05', 'time': '09:07:03', 'level': 'ERROR', 'msg': 'сбой диска'}\n['ivan@mail.ru', 'olga@ya.ru']\n['+7-900-123-45-67']"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Пределы регулярок"}
      sub={"Вложенное — не для них; простое — простыми методами"}
      main={"Не парсите ими HTML и JSON; избегайте вложенных квантификаторов — катастрофический откат."}
    >
      <PyCode>{`import re

print(re.search(r"<.+>", "<a><b>").group())
print(re.search(r"<[^>]+>", "<a><b>").group())
print("кот".startswith("к"), "кот" in "котёнок", "а-б".replace("-", "+"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"<a><b>\n<a>\nTrue True а+б"}</Cmd>
      <div className="s-note">{"Простое: startswith, in, replace. Регулярка — когда нужны варианты, повторы, группы."}</div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Русский текст"}
      sub={"\\w узнаёт кириллицу; ё — отдельно"}
      main={"[а-я] не включает «ё»; \\d узнаёт цифры других алфавитов — для обычных пишите [0-9]."}
    >
      <PyCode>{`import re

print(re.findall(r"\\w+", "Привет, мир! hello"))
print(re.findall(r"[а-я]+", "ёж и ель"))
print(re.findall(r"[а-яё]+", "ёж и ель"))
print(re.findall(r"\\w+", "Привет hello", re.ASCII))
print(re.findall(r"[0-9]+", "123 ٣٤٥"), re.findall(r"\\d+", "123 ٣٤٥"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['Привет', 'мир', 'hello']\n['ж', 'и', 'ель']\n['ёж', 'и', 'ель']\n['hello']\n['123'] ['123', '٣٤٥']"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"None вместо совпадения, неэкранированная точка"}
      main={"Проверяйте результат поиска перед обращением к группе; спецсимволы экранируйте через re.escape."}
    >
      <PyCode>{`import re

m = re.search(r"\\d+", "нет цифр")
print(m)
print(re.search(r"1.5", "1x5") is not None, re.search(r"1\\.5", "1x5") is not None)
print(re.escape("1.5+2"))
print(re.match(r"b", "abc"), re.search(r"b", "abc").group())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"None\nTrue False\n1\\.5\\+2\nNone b"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 27 · Стандартная библиотека"}
      main={"Простое — методами строк, гибкое — регулярками, вложенное — настоящими парсерами."}
    >
      <div className="s-grid2">
        {[["\\d \\w \\s [..] . ^ $", "Элементы", "Символы, наборы, якоря"], ["* + ? {n,m} *?", "Повторы", "Жадные и ленивые"], ["( ) (?P<n>) (?: )", "Группы", "Извлечение и альтернативы"], ["search · findall · sub · split", "Функции", "r-строки, compile, флаги, re.X"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — модули для программ: sys, argparse, logging, subprocess."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P27 = {
  "13:27": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P27).
export const SLIDE_TITLES_P27 = {
  "13:27": [
    "Регулярные выражения",
    "Основы шаблона",
    "Квантификаторы",
    "Группы",
    "Именованные группы",
    "sub и split",
    "Сырые строки и флаги",
    "Границы и контекст",
    "Практика",
    "Пределы регулярок",
    "Русский текст",
    "Типичные ошибки",
    "Итог",
  ],
};
