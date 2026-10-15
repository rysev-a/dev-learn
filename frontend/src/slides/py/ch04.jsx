// Слайды для «Python как первый язык», глава 4 — «Функции».
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
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / ОСНОВЫ / ГЛАВА 4</span>
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
      title={"Функции"}
      sub={"Глава 4 · Основы"}
      main={"Функция — именованный блок кода: описали один раз, вызываем сколько угодно."}
    >
      <div className="s-grid2">
        {[["def", "Описание", "Слово def, имя, параметры, тело с отступом"], ["f(x)", "Вызов", "Имя и круглые скобки — код выполняется"], ["return", "Результат", "Отдаёт значение и завершает функцию"], ["x=2", "Умолчания", "Значения параметров и именованные аргументы"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">{"Вы уже вызывали готовые функции: print, len, type, int. Теперь пишем свои."}</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Описание и вызов"}
      sub={"def задаёт функцию, скобки её запускают"}
      main={"Описание ничего не выполняет — код срабатывает только при вызове."}
    >
      <PyCode>{`def hello():
    print("Привет!")

hello()
hello()
hello()`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Привет!\nПривет!\nПривет!"}</Cmd>
      <div className="s-note">{"Описать функцию нужно раньше вызова: иначе Питон не знает такого имени."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Параметры"}
      sub={"Параметр — имя в описании, аргумент — значение при вызове"}
      main={"Одна функция обслуживает тысячу случаев — разные аргументы, один код."}
    >
      <PyCode>{`def hello(name):
    print("Привет,", name)

hello("Аня")
hello("Борис")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Привет, Аня\nПривет, Борис"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"name"} sub={"Параметр — внутри функции"} />
        <Node kind="green" mono={true} title={"\"Аня\""} sub={"Аргумент — при вызове"} />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"return"}
      sub={"Вернуть результат вызывающему коду"}
      main={"print — для человека, return — для программы."}
    >
      <PyCode>{`def square(x):
    return x * x

result = square(5)
print(result)
print(square(3) + square(4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"25\n25"}</Cmd>
      <div className="s-note">{"Нет return — функция вернёт None, то есть «ничего»."}</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Ветки и ранний выход"}
      sub={"return завершает функцию немедленно"}
      main={"На любом пути выполнения функция должна что-то вернуть."}
    >
      <PyCode>{`def sign(x):
    if x > 0:
        return "положительное"
    if x < 0:
        return "отрицательное"
    return "ноль"

print(sign(5), sign(-2), sign(0))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"положительное отрицательное ноль"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Значения по умолчанию"}
      sub={"И именованные аргументы"}
      main={"Параметры с умолчанием стоят после обычных; по имени аргументы можно в любом порядке."}
    >
      <PyCode>{`def power(x, n=2):
    return x ** n

print(power(5))
print(power(5, 3))
print(power(n=3, x=2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"25\n125\n8"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Область видимости"}
      sub={"Локальные переменные живут только внутри функции"}
      main={"Данные — в параметры, ответ — через return; чужие переменные не правим."}
    >
      <PyCode>{`def f():
    local = 10
    return local

f()
print(local)   # NameError`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"NameError: name 'local' is not defined"}</Cmd>
      <div className="s-note">{"Присваивание внутри функции создаёт новую локальную переменную, а внешнюю не трогает."}</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Докстринг и имена"}
      sub={"Описание в тройных кавычках"}
      main={"Одна функция — одна задача; если в описании нужно «и» — разделите её."}
    >
      <PyCode>{`def is_even(n):
    """Вернуть True, если n чётное."""
    return n % 2 == 0

print(is_even.__doc__)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Вернуть True, если n чётное."}</Cmd>
      <div className="s-note">{"Имя — глагол или вопрос: посчитать сумму, это чётное. Не f1 и не func."}</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Функции зовут функции"}
      sub={"Декомпозиция: большая задача из маленьких"}
      main={"Хорошая программа читается как оглавление: каждая функция кратко называет свою задачу."}
    >
      <PyCode>{`def divisible(n, d):
    return n % d == 0

def is_leap(year):
    return divisible(year, 4) and (not divisible(year, 100) or divisible(year, 400))

print(is_leap(2024), is_leap(1900), is_leap(2000))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True False True"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Рекурсия"}
      sub={"Функция вызывает саму себя"}
      main={"Нужен базовый случай — иначе рекурсия не остановится."}
    >
      <PyCode>{`def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(5))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"120"}</Cmd>
      <div className="s-cols">
        <Node kind="green" mono={true} title={"n == 0"} sub={"Базовый случай: готовый ответ"} />
        <Node kind="" mono={true} title={"n * f(n - 1)"} sub={"Шаг: задача поменьше"} />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"assert: проверяем функции"}
      sub={"Утверждение: истинно — тишина, ложно — ошибка"}
      main={"Проверяйте и типичные значения, и крайние случаи: ноль, минус, пустую строку."}
    >
      <PyCode>{`def square(x):
    return x * x

assert square(3) == 9
assert square(0) == 0
assert square(-2) == 4
print("всё в порядке")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"всё в порядке"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Скобки, return, порядок аргументов"}
      main={"Большинство ошибок ловится за минуту чтением кода вслух."}
    >
      <PyCode>{`def double(x):
    print(x * 2)      # напечатал, но не вернул

r = double(4)
print(r)               # None
print(double)          # без скобок — сам объект функции`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"8\nNone\n<function double at 0x...>"}</Cmd>
      <div className="s-note">{"Ещё: вызов до описания, правка внешней переменной, функция «делает слишком много»."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 4 · Основы"}
      main={"Данные — через параметры, ответ — через return."}
    >
      <div className="s-grid2">
        {[["def f(x):", "Описание", "Тело с отступом; вызов выполняет код"], ["return", "Результат", "Отдаёт значение; без него — None"], ["n=2", "Умолчания", "После обычных параметров; можно по имени"], ["assert", "Проверка", "Типичные и крайние случаи"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — циклы: научим программу повторять действия."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P4 = {
  "13:4": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P4).
export const SLIDE_TITLES_P4 = {
  "13:4": [
    "Функции",
    "Описание и вызов",
    "Параметры",
    "return",
    "Ветки и ранний выход",
    "Умолчания и имена",
    "Область видимости",
    "Докстринг и имена",
    "Функции зовут функции",
    "Рекурсия",
    "assert",
    "Типичные ошибки",
    "Итог",
  ],
};
