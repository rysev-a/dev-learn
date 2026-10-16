import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 34 — «Числа и случайность».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 34", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Числа и случайность"}
      sub={"Глава 34 · Стандартная библиотека"}
      main={"Целые точны, дробные приблизительны; для денег — Decimal, для безопасности — secrets."}
    >
      <div className="s-grid2">
        {([["math", "Математика", "Корни, логарифмы, gcd, комбинаторика"], ["Decimal · Fraction", "Точность", "Деньги и точные дроби"], ["random", "Случайность", "Для игр и симуляций; seed делает повторяемой"], ["statistics · secrets", "Данные и защита", "Среднее и разброс; токены и пароли"]] as const).map(([big, t, d]) => (
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
      title={"Модуль math"}
      sub={"Функции и константы"}
      main={"Комбинаторика из дискретной математики — одной функцией: comb и perm."}
    >
      <PyCode>{`import math

print(math.sqrt(16), math.floor(2.7), math.ceil(2.1), math.trunc(-2.7))
print(round(math.pi, 4), round(math.e, 4), math.hypot(3, 4))
print(math.gcd(12, 18), math.lcm(4, 6), math.factorial(5))
print(math.comb(5, 2), math.perm(5, 2))
print(math.isinf(math.inf), math.isnan(math.nan))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4.0 2 3 -2\n3.1416 2.7183 5.0\n6 12 120\n10 20\nTrue True"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Погрешность float"}
      sub={"0.1 + 0.2 ≠ 0.3"}
      main={"Никогда не сравнивайте дробные на точное равенство: спрашивайте, достаточно ли они близки."}
    >
      <PyCode>{`import math

print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(2 ** 100, 2 ** 100 + 1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0.30000000000000004\nFalse\nTrue\n1267650600228229401496703205376 1267650600228229401496703205377"}</Cmd>
      <div className="s-note">{"Целые числа в Питоне точные и неограниченной длины."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Округление"}
      sub={"round, int, //, divmod"}
      main={"round округляет к ближайшему чётному; для вывода — формат :.2f, число не меняется."}
    >
      <PyCode>{`print(round(2.5), round(3.5), round(-2.5))
print(round(3.14159, 2), round(1234, -2))
x = 3.14159
print(f"{x:.2f}", int(-2.7), -7 // 2, divmod(17, 5))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 4 -2\n3.14 1200\n3.14 -2 -4 (3, 2)"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Decimal"}
      sub={"Точная десятичная арифметика"}
      main={"Создавайте из строки, а не из float — иначе погрешность уже внутри."}
    >
      <PyCode>{`from decimal import Decimal, ROUND_HALF_UP

print(Decimal("0.1") + Decimal("0.2"))
price = Decimal("19.99") * 3
print(price)
print(Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
print(Decimal(0.1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0.3\n59.97\n2.68\n0.1000000000000000055511151231257827021181583404541015625"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Fraction"}
      sub={"Точные обыкновенные дроби"}
      main={"Дроби сокращаются сами; limit_denominator находит ближайшую простую дробь."}
    >
      <PyCode>{`from fractions import Fraction

a = Fraction(1, 3) + Fraction(1, 6)
print(a, a == Fraction(1, 2))
print(Fraction("3/4") * 2)
print(Fraction(0.75), Fraction(3.14159).limit_denominator(100))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1/2 True\n3/2\n3/4 311/99"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"random"}
      sub={"Псевдослучайные числа"}
      main={"Одно и то же зерно — одна и та же «случайная» последовательность: удобно для тестов."}
    >
      <PyCode>{`import random

random.seed(1)
a = [random.randint(1, 6) for _ in range(5)]
random.seed(1)
b = [random.randint(1, 6) for _ in range(5)]
print(a == b)
print(1 <= random.randint(1, 6) <= 6, random.choice("абвг") in "абвг")
nums = [1, 2, 3, 4, 5]
random.shuffle(nums)
print(sorted(nums))
print(len(random.sample(range(10), 3)), 0 <= random.random() < 1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True\nTrue True\n[1, 2, 3, 4, 5]\n3 True"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Симуляции"}
      sub={"Кубики и метод Монте-Карло"}
      main={"Чем больше испытаний, тем ближе результат к теории."}
    >
      <PyCode>{`import random
from collections import Counter

random.seed(7)
rolls = Counter(random.randint(1, 6) + random.randint(1, 6) for _ in range(6000))
print(rolls.most_common(1)[0][0])
inside = 0
n = 100000
for _ in range(n):
    x, y = random.random(), random.random()
    if x * x + y * y <= 1:
        inside += 1
print(round(4 * inside / n, 1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"7\n3.1"}</Cmd>
      <div className="s-note">{"Доля случайных точек внутри четверти круга даёт оценку числа пи."}</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"statistics"}
      sub={"Среднее, медиана, мода, разброс"}
      main={"Одного среднего мало: медиана устойчива к выбросам, а разброс показывает разнообразие."}
    >
      <PyCode>{`import statistics as st

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(st.mean(data), st.median(data), st.mode(data))
print(st.pstdev(data), round(st.stdev(data), 3))
print(st.median([1, 2, 3, 100]), st.mean([1, 2, 3, 100]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5 4.5 4\n2.0 2.138\n2.5 26.5"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"secrets и хеши"}
      sub={"Случайность для безопасности"}
      main={"Игра и тесты — random; пароли, токены, доступ — secrets; в базе хранят хеш, а не пароль."}
    >
      <PyCode>{`import secrets
import hashlib
import string

token = secrets.token_hex(8)
print(len(token), all(c in "0123456789abcdef" for c in token))
alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(12))
print(len(password))
print(hashlib.sha256("пароль".encode("utf-8")).hexdigest()[:16])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"16 True\n12\n2dbc574daca52689"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Системы счисления и биты"}
      sub={"bin, hex, int(x, base), побитовые операции"}
      main={"Целые числа произвольной длины; биты — основа флагов, протоколов и шифрования."}
    >
      <PyCode>{`print(2 ** 100)
print(bin(10), hex(255), oct(8), int("ff", 16), f"{10:b}", f"{255:x}")
print(6 & 3, 6 | 3, 6 ^ 3, 1 << 4, 100 >> 2)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1267650600228229401496703205376\n0b1010 0xff 0o10 255 1010 ff\n2 7 5 16 25"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"round, Decimal из float, пустое среднее"}
      main={"Деньги — Decimal из строк; пароли — secrets; сравнение дробных — isclose."}
    >
      <PyCode>{`from decimal import Decimal
import statistics

print(round(2.675, 2))
print(Decimal(2.675) == Decimal("2.675"))
print(int(-2.7), -7 // 2, 7 % -3)
try:
    statistics.mean([])
except statistics.StatisticsError as e:
    print("пусто:", e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2.67\nFalse\n-2 -4 -2\nпусто: mean requires at least one data point"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 34 · Стандартная библиотека"}
      main={"Выбирайте тип числа под задачу: float, Decimal или Fraction."}
    >
      <div className="s-grid2">
        {([["math · isclose", "Математика", "Функции; сравнение дробных через isclose"], ["Decimal · Fraction", "Точность", "Деньги и рациональные числа"], ["random · seed", "Случайность", "Игры и симуляции; воспроизводимо"], ["secrets", "Безопасность", "Пароли и токены"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — дата и время."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P34 = {
  "13:34": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P34).
export const SLIDE_TITLES_P34 = {
  "13:34": [
    "Числа и случайность",
    "Модуль math",
    "Погрешность float",
    "Округление",
    "Decimal",
    "Fraction",
    "random",
    "Симуляции",
    "statistics",
    "secrets и хеши",
    "Системы счисления",
    "Типичные ошибки",
    "Итог",
  ],
};
