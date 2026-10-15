// Слайды для «Python как первый язык», глава 30 — «Тестирование».
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
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 30</span>
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
      title={"Тестирование"}
      sub={"Глава 30 · Стандартная библиотека"}
      main={"Тесты дают уверенность менять код: сломалось — сразу видно, что и где."}
    >
      <div className="s-grid2">
        {[["assert", "Проверки", "Вызвать код и сверить результат"], ["unittest", "Каркас", "Классы, setUp, subTest, отчёт"], ["doctest", "Примеры", "Документация, которая не врёт"], ["mock · patch", "Изоляция", "Подменить сеть, время, случайность"]].map(([big, t, d]) => (
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
      title={"Тест через assert"}
      sub={"Известный вход — ожидаемый результат"}
      main={"Для маленьких скриптов хватает; но первая же ошибка останавливает остальные проверки."}
    >
      <PyCode>{`def add(a, b):
    return a + b

assert add(2, 3) == 5
assert add(-1, 1) == 0
print("проверки пройдены")
try:
    assert add(1, 1) == 3, "ожидали 3"
except AssertionError as e:
    print("упало:", e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"проверки пройдены\nупало: ожидали 3"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"unittest"}
      sub={"TestCase и методы test_*"}
      main={"Каждый тест независим: один сбой не прячет остальные; результат — понятный отчёт."}
    >
      <PyCode>{`import io
import unittest

def is_even(n):
    return n % 2 == 0

class TestEven(unittest.TestCase):
    def test_even(self):
        self.assertTrue(is_even(4))

    def test_odd(self):
        self.assertFalse(is_even(3))

    def test_zero(self):
        self.assertEqual(is_even(0), True)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEven)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 True"}</Cmd>
      <div className="s-note">{"В проекте запускают так: python -m unittest или unittest.main() в конце файла."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"setUp и subTest"}
      sub={"Чистое окружение и таблица случаев"}
      main={"Таблица «вход — ожидание»: новый случай — одна строка, а сбои сообщаются по каждому."}
    >
      <PyCode>{`import io
import unittest

class TestStack(unittest.TestCase):
    def setUp(self):
        self.items = []          # свежее окружение перед каждым тестом

    def test_push(self):
        self.items.append(1)
        self.assertEqual(self.items, [1])

    def test_empty(self):
        self.assertEqual(self.items, [])

    def test_table(self):
        for a, b, want in [(1, 2, 3), (2, 2, 4), (5, 5, 11)]:
            with self.subTest(a=a, b=b):
                self.assertEqual(a + b, want)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStack)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, len(result.failures))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 1"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Ошибки и крайние случаи"}
      sub={"assertRaises"}
      main={"Типичный случай, граничные значения, неправильный ввод — три слоя хорошего набора."}
    >
      <PyCode>{`import io
import unittest

def divide(a, b):
    if b == 0:
        raise ValueError("деление на ноль")
    return a / b

class T(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError) as ctx:
            divide(1, 0)
        self.assertIn("ноль", str(ctx.exception))

    def test_edges(self):
        self.assertEqual(divide(0, 5), 0)
        self.assertEqual(divide(-6, 3), -2)

r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(T))
print(r.testsRun, r.wasSuccessful())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 True"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"doctest"}
      sub={"Примеры в докстринге — это тесты"}
      main={"Если код изменился, а пример нет — тест упадёт: документация перестанет врать."}
    >
      <PyCode>{`import doctest

def square(x):
    """Возвести в квадрат.

    >>> square(3)
    9
    >>> square(-2)
    4
    """
    return x * x

runner = doctest.DocTestRunner(verbose=False)
for t in doctest.DocTestFinder().find(square, "square", globs={"square": square}):
    runner.run(t)
print(runner.summarize(verbose=False))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"TestResults(failed=0, attempted=2)"}</Cmd>
      <div className="s-note">{"Из терминала: python -m doctest файл.py."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Моки и patch"}
      sub={"Изолируем код от внешнего мира"}
      main={"Тест, целиком состоящий из подмен, проверяет сами подмены — не злоупотребляйте."}
    >
      <PyCode>{`from unittest.mock import Mock, patch
import random

def get_price(session, item):
    return session.get(item)["price"]

fake = Mock()
fake.get.return_value = {"price": 100}
print(get_price(fake, "кофе"))
fake.get.assert_called_once_with("кофе")

def roll():
    return random.randint(1, 6)

with patch("random.randint", return_value=4):
    print(roll())
print(1 <= roll() <= 6)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"100\n4\nTrue"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"pytest"}
      sub={"Сторонний каркас с теми же принципами"}
      main={"Тесты — обычные функции, проверки — обычные assert; фикстуры и параметризация экономят код."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"def test_add():"} sub={"assert add(2, 3) == 5"} />
        <Node kind="green" mono={true} title={"@pytest.mark.parametrize"} sub={"Один тест — таблица значений"} />
        <Node kind="" mono={true} title={"@pytest.fixture"} sub={"Подготовка данных по имени параметра"} />
      </div>
      <div className="s-note">{"pytest ставится отдельно (pip install pytest) и запускает в том числе тесты unittest."}</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"TDD: красный — зелёный — рефакторинг"}
      sub={"Тест раньше кода"}
      main={"Падающий тест — красный; минимальный код — зелёный; потом наводим порядок, не меняя поведение."}
    >
      <PyCode>{`# 1. красный: тест пишем первым
def test_fizz():
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(7) == "7"

# 2. зелёный: минимальный код
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

test_fizz()
print("зелёный")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"зелёный"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Код, который легко тестировать"}
      sub={"Зависимости — параметрами"}
      main={"Время, сеть и файлы передаём снаружи — и подмена тривиальна, даже мок не нужен."}
    >
      <PyCode>{`from datetime import datetime

def greeting(now):               # время — параметр, а не вызов внутри
    return "Доброе утро" if now.hour < 12 else "Добрый день"

assert greeting(datetime(2024, 1, 1, 9)) == "Доброе утро"
assert greeting(datetime(2024, 1, 1, 15)) == "Добрый день"
print("тестируемо без часов и без мока")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"тестируемо без часов и без мока"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Свойства и случайные тесты"}
      sub={"Много входов — одно утверждение"}
      main={"Фиксированное зерно делает «случайный» тест воспроизводимым: упавший случай можно повторить."}
    >
      <PyCode>{`import random

random.seed(1)
for _ in range(1000):
    xs = [random.randint(-50, 50) for _ in range(random.randint(0, 20))]
    s = sorted(xs)
    assert all(a <= b for a, b in zip(s, s[1:]))
    assert len(s) == len(xs) and sorted(s) == s
print("свойства сортировки выполнены на 1000 случайных входах")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"свойства сортировки выполнены на 1000 случайных входах"}</Cmd>
      <div className="s-note">{"Покрытие строк — ориентир, но не цель: 100 % не гарантирует правильность."}</div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Тест зависит от порядка"}
      main={"Тест должен быть маленьким, быстрым и описывать одну идею — и не зависеть от соседей."}
    >
      <PyCode>{`import io
import unittest

class Bad(unittest.TestCase):
    order = []
    def test_a(self):
        Bad.order.append("a")
    def test_b(self):
        self.assertEqual(Bad.order, ["a"])     # прошёл случайно: зависит от порядка

r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(Bad))
print(r.wasSuccessful(), Bad.order)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True ['a']"}</Cmd>
      <div className="s-note">{"Запустите test_b отдельно — он упадёт. Ещё: слишком много проверок в одном тесте, время и сеть без изоляции, ослабление теста вместо починки кода."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 30 · Стандартная библиотека"}
      main={"Вы прошли путь от первой строки до тестов собственных программ."}
    >
      <div className="s-grid2">
        {[["assert · unittest", "Проверки", "Независимые тесты, setUp, subTest, assertRaises"], ["doctest", "Примеры", "Живая документация"], ["Mock · patch", "Изоляция", "Подмена внешнего мира; без злоупотреблений"], ["TDD", "Подход", "Красный — зелёный — рефакторинг"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — алгоритмы на Python, а позже — асинхронность."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P30 = {
  "13:30": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P30).
export const SLIDE_TITLES_P30 = {
  "13:30": [
    "Тестирование",
    "assert",
    "unittest",
    "setUp и subTest",
    "Ошибки и крайние случаи",
    "doctest",
    "Моки и patch",
    "pytest",
    "TDD",
    "Тестируемый код",
    "Свойства",
    "Типичные ошибки",
    "Итог",
  ],
};
