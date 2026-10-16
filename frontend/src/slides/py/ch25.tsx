import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, Node, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 25 — «Функции высшего порядка».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ / ГЛАВА 25", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Функции высшего порядка"}
      sub={"Глава 25 · Функциональное программирование"}
      main={"Функция — такое же значение, как число: её можно передать, сохранить и вернуть."}
    >
      <div className="s-grid2">
        {([["lambda x: x * 2", "Лямбда", "Анонимная функция из одного выражения"], ["map · filter", "Лениво", "Преобразовать и отобрать"], ["*args · **kwargs", "Звёздочки", "Любое число аргументов"], ["f(g(x))", "Композиция", "Новая функция из двух"]] as const).map(([big, t, d]) => (
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
      title={"Функция — значение"}
      sub={"Имя без скобок — сама функция"}
      main={"Скобки решают всё: с ними функция вызывается, без них — передаётся."}
    >
      <PyCode>{`f = print
f("привет")

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = {"+": add, "-": sub}
print(ops["+"](2, 3), ops["-"](5, 1))

def apply(func, x):
    return func(x)

print(apply(len, "привет"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"привет\n5 4\n6"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Лямбда"}
      sub={"lambda параметры: выражение"}
      main={"Длинная лямбда — повод превратить её в функцию с именем."}
    >
      <PyCode>{`double = lambda x: x * 2
print(double(21))
print((lambda a, b: a + b)(2, 3))
print(sorted([3, 1, 2], key=lambda x: -x))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"42\n5\n[3, 2, 1]"}</Cmd>
      <div className="s-note">{"return писать не нужно; в теле — одно выражение: без присваиваний и блоков."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Лямбда и key"}
      sub={"sorted, min и max принимают функцию-ключ"}
      main={"Несколько признаков — кортеж в ключе: первый главный, второй решает ничьи."}
    >
      <PyCode>{`words = ["ccc", "a", "bb"]
print(sorted(words, key=lambda w: len(w)))
users = [{"name": "Аня", "age": 31}, {"name": "Боря", "age": 25}]
print(max(users, key=lambda u: u["age"])["name"])
pairs = [("б", 2), ("а", 2), ("в", 1)]
print(sorted(pairs, key=lambda p: (p[1], p[0])))
print(max([], default="пусто"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['a', 'bb', 'ccc']\nАня\n[('в', 1), ('а', 2), ('б', 2)]\nпусто"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"map"}
      sub={"Применить функцию к каждому элементу — лениво"}
      main={"map возвращает итератор: чтобы увидеть значения, обернуть в list или перебрать."}
    >
      <PyCode>{`nums = [1, 2, 3]
print(list(map(str, nums)))
print(list(map(lambda x: x * 2, nums)))
print(list(map(lambda a, b: a + b, [1, 2], [10, 20])))
m = map(str, nums)
print(type(m).__name__, list(m), list(m))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['1', '2', '3']\n[2, 4, 6]\n[11, 22]\nmap ['1', '2', '3'] []"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"filter"}
      sub={"Оставить те, для которых функция истинна"}
      main={"filter(None, данные) убирает «пустое»: нули, пустые строки и списки, None."}
    >
      <PyCode>{`print(list(filter(lambda x: x > 0, [-1, 2, -3, 4])))
print(list(filter(None, [0, 1, "", "а", [], [0], None])))
print(list(filter(str.isalpha, ["abc", "a1", "xyz"])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[2, 4]\n[1, 'а', [0]]\n['abc', 'xyz']"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"map или генератор списка"}
      sub={"Обычно читается лучше второе"}
      main={"Готовая функция — map и filter; выражение с условиями — генератор списка."}
    >
      <PyCode>{`nums = [1, 2, 3, 4]
print(list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums))))
print([x * x for x in nums if x % 2 == 0])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[4, 16]\n[4, 16]"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"готовая функция"} sub={"map(int, строки)"} />
        <Node kind="green" mono={true} title={"выражение с условием"} sub={"[x * x for x in a if ...]"} />
        <Node kind="" mono={true} title={"один проход"} sub={"(x for x in a)"} />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Свёртка"}
      sub={"Отобрать, преобразовать — свернуть"}
      main={"Для суммы и максимума берите встроенные; reduce — для редких свёрток."}
    >
      <PyCode>{`from functools import reduce

nums = [1, 2, 3, 4]
print(sum(nums), max(nums))
print(reduce(lambda acc, x: acc * x, nums, 1))
print(reduce(lambda acc, x: acc + str(x), nums, ""))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 4\n24\n1234"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"*args и **kwargs"}
      sub={"Собрать любое число аргументов — и раздать обратно"}
      main={"Так пишутся универсальные обёртки, передающие всё дальше, не зная что именно."}
    >
      <PyCode>{`def show(*args, **kwargs):
    print(args, kwargs)

show(1, 2, a=3)
nums = [1, 2]
opts = {"sep": "-"}
print(*nums, **opts)

def only_named(a, *, b):
    return a + b

print(only_named(1, b=2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(1, 2) {'a': 3}\n1-2\n3"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Чистые функции"}
      sub={"Зависят только от аргументов и ничего не меняют"}
      main={"Эффекты — на краях программы, чистое ядро — внутри. Не меняйте чужие аргументы."}
    >
      <PyCode>{`def pure_add(items, x):
    return items + [x]          # новый список

def impure_add(items, x):
    items.append(x)             # меняет аргумент

a = [1]
print(pure_add(a, 2), a)
impure_add(a, 2)
print(a)

def bad(x, acc=[]):             # один список на все вызовы
    acc.append(x)
    return acc

print(bad(1), bad(2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2] [1]\n[1, 2]\n[1, 2] [1, 2]"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Композиция"}
      sub={"Новая функция из двух"}
      main={"Маленькие преобразования, собранные в конвейер, — и каждое можно заменить или переставить."}
    >
      <PyCode>{`def compose(f, g):
    return lambda x: f(g(x))

clean = compose(str.strip, str.lower)
shout = compose(str.upper, str.strip)
print(repr(clean("  ПрИвЕт ")))
print(shout("  тихо  "))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"'привет'\nТИХО"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Лямбды в цикле и ленивые map"}
      main={"Лямбда запоминает переменную, а не значение; map и filter возвращают итератор."}
    >
      <PyCode>{`funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])      # все видят последнее i
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])
print(len(map(str, [1, 2])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[2, 2, 2]\n[0, 1, 2]\nTypeError: object of type 'map' has no len()"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 25 · Функциональное программирование"}
      main={"Функции — значения; чистота лучше побочных эффектов; читаемость важнее краткости."}
    >
      <div className="s-grid2">
        {([["lambda", "Лямбда", "Одно выражение; главное место — key"], ["map · filter · reduce", "Три глагола", "Преобразовать, отобрать, свернуть"], ["*args · **kwargs", "Любые аргументы", "Собирают и раскладывают"], ["compose", "Композиция", "Конвейер из мелких функций"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — замыкания и декораторы."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P25 = {
  "13:25": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P25).
export const SLIDE_TITLES_P25 = {
  "13:25": [
    "Функции высшего порядка",
    "Функция — значение",
    "Лямбда",
    "Лямбда и key",
    "map",
    "filter",
    "map или генератор",
    "Свёртка",
    "*args и **kwargs",
    "Чистые функции",
    "Композиция",
    "Типичные ошибки",
    "Итог",
  ],
};
