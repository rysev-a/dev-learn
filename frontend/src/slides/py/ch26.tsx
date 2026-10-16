import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 26 — «Замыкания и декораторы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ / ГЛАВА 26", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Замыкания и декораторы"}
      sub={"Глава 26 · Функциональное программирование"}
      main={"Функцию можно создать внутри функции — и вернуть вместе с её окружением."}
    >
      <div className="s-grid2">
        {[["def f(): def g()", "Вложенные", "Видят переменные внешней"], ["closure", "Замыкание", "Функция запоминает окружение"], ["@decorator", "Декоратор", "Функция, улучшающая функцию"], ["@wraps", "Аккуратно", "Сохраняет имя и докстринг"]].map(([big, t, d]) => (
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
      title={"Вложенные функции"}
      sub={"Читать внешние переменные можно, менять — через nonlocal"}
      main={"Имя ищется по цепочке: функция, охватывающая функция, модуль, встроенные."}
    >
      <PyCode>{`def outer():
    x = 10
    def inner():
        return x + 1          # читаем внешнюю
    return inner()

print(outer())

def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

c = counter()
print(c(), c(), c())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"11\n1 2 3"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Замыкание"}
      sub={"Функция уносит окружение с собой"}
      main={"Внешняя функция уже завершилась, а число n осталось жить внутри внутренней — как в капсуле."}
    >
      <PyCode>{`def make_multiplier(n):
    def mul(x):
        return x * n
    return mul

triple = make_multiplier(3)
five = make_multiplier(5)
print(triple(10), five(10))
print(triple.__closure__[0].cell_contents)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"30 50\n3"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Состояние в замыкании"}
      sub={"Каждый вызов фабрики — своя капсула"}
      main={"Один метод и немного состояния — замыкание короче; несколько методов — класс понятнее."}
    >
      <PyCode>{`def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

a, b = make_counter(), make_counter()
print(a(), a(), b())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2 1"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Поздняя привязка"}
      sub={"Функция помнит переменную, а не значение"}
      main={"Лечится значением по умолчанию, фабрикой или partial."}
    >
      <PyCode>{`funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
fixed = [lambda i=i: i for i in range(3)]
print([f() for f in fixed])

def make(i):
    return lambda: i

print([make(i)() for i in range(3)])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[2, 2, 2]\n[0, 1, 2]\n[0, 1, 2]"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Первый декоратор"}
      sub={"Принимает функцию, возвращает обёртку"}
      main={"@имя над def — сокращённая запись: square = timer(square)."}
    >
      <PyCode>{`import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: готово")
        return result
    return wrapper

@timer
def square(x):
    return x * x

print(square(7))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"square: готово\n49"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Аргументы и результат"}
      sub={"*args, **kwargs и return в обёртке"}
      main={"Шаблон наизусть: внутренняя функция, вызвать оригинал, вернуть результат, вернуть обёртку."}
    >
      <PyCode>{`def logged(func):
    def wrapper(*args, **kwargs):
        print("вызов", args, kwargs)
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a, b=0):
    return a + b

print(add(1, b=2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"вызов (1,) {'b': 2}\n3"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"functools.wraps"}
      sub={"Чтобы имя и документация не терялись"}
      main={"Любой декоратор, который вы пишете, украшайте @wraps."}
    >
      <PyCode>{`from functools import wraps

def deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@deco
def hello():
    """Поздороваться."""

print(hello.__name__, hello.__doc__)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"hello Поздороваться."}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Декоратор с параметрами"}
      sub={"Ещё один уровень: фабрика декораторов"}
      main={"Скобки после имени декоратора — это вызов фабрики, а не самого декоратора."}
    >
      <PyCode>{`def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("привет")

hello()`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"привет\nпривет\nпривет"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Кеш на декораторе"}
      sub={"Те же аргументы — тот же ответ"}
      main={"Замеры, логи, права, повторы при сбоях, регистрация обработчиков — одной строкой над функцией."}
    >
      <PyCode>{`def memo(func):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memo
def slow_square(n):
    print("считаю", n)
    return n * n

print(slow_square(4), slow_square(4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"считаю 4\n16 16"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Класс как декоратор"}
      sub={"__call__ делает экземпляр вызываемым"}
      main={"Несколько декораторов применяются снизу вверх: ближайший к функции срабатывает первым."}
    >
      <PyCode>{`class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def hi():
    return "привет"

hi()
hi()
print(hi.calls, hi())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 привет"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Забытый return в обёртке"}
      main={"Проверьте руками: имя = декоратор(функция) — и сразу видно, что вы возвращаете."}
    >
      <PyCode>{`def broken(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)          # забыли return
    return wrapper

@broken
def one():
    return 1

print(one())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"None"}</Cmd>
      <div className="s-note">{"Ещё: не вернули обёртку, нет @wraps, лямбды в цикле, порядок нескольких декораторов, слишком «умный» декоратор."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 26 · Функциональное программирование"}
      main={"Замыкание — функция с окружением; декоратор — замыкание, улучшающее другую функцию."}
    >
      <div className="s-grid2">
        {[["nonlocal", "Замыкание", "Фабрики функций и состояние"], ["@decorator", "Декоратор", "wrapper(*args, **kwargs) и return"], ["@wraps", "Аккуратность", "Имя и докстринг не теряются"], ["@repeat(3)", "С параметрами", "Фабрика декораторов"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — functools и operator: готовые инструменты."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P26 = {
  "13:26": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P26).
export const SLIDE_TITLES_P26 = {
  "13:26": [
    "Замыкания и декораторы",
    "Вложенные функции",
    "Замыкание",
    "Состояние в замыкании",
    "Поздняя привязка",
    "Первый декоратор",
    "Аргументы и результат",
    "wraps",
    "С параметрами",
    "Кеш",
    "Класс-декоратор",
    "Типичные ошибки",
    "Итог",
  ],
};
