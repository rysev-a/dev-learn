import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, Node, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 11 — «Кортежи».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / СЛОВАРИ И КОРТЕЖИ / ГЛАВА 11", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Кортежи"}
      sub={"Глава 11 · Словари и кортежи"}
      main={"Неизменяемость — полезное ограничение: содержимое кортежа не испортить случайно."}
    >
      <div className="s-grid2">
        {([["(1, 2)", "Кортеж", "Упорядоченный набор, который нельзя менять"], ["a, b = t", "Распаковка", "Раскладывает набор по переменным"], ["return a, b", "Несколько значений", "Функция отдаёт кортеж"], ["{(r, c): v}", "Ключ словаря", "Составной ключ — таблица по двум признакам"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">{"Вы уже встречали кортежи: каждая пара из enumerate, zip и items() — кортеж."}</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Создание кортежа"}
      sub={"Кортеж создаёт запятая, а не скобки"}
      main={"Один элемент — обязательно запятая в конце: (1,) — кортеж, (1) — просто число."}
    >
      <PyCode>{`t = (1, 2, 3)
point = 4, 5          # скобки не обязательны
one = (1,)            # запятая нужна
print(type((1)), type(one))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"<class 'int'> <class 'tuple'>"}</Cmd>
      <div className="s-note">{"tuple(список) и tuple(строка) превращают набор в кортеж."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Что умеет кортеж"}
      sub={"Всё, что не меняет — как у списка"}
      main={"Методов правки нет: ни append, ни remove, ни sort."}
    >
      <PyCode>{`t = (10, 20, 30)
print(t[0], t[-1], t[1:], len(t), 20 in t)
t[0] = 99                # TypeError`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 30 (20, 30) 3 True\nTypeError: 'tuple' object does not support item assignment"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Изменить — значит пересобрать"}
      sub={"Плюс, умножение, срезы — новый кортеж"}
      main={"Неизменяемость защищает от правки через вторую ссылку; в ключи годятся только такие данные."}
    >
      <PyCode>{`t = (1, 2, 3)
t = t[:1] + (99,) + t[2:]
print(t)
print(t * 2)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(1, 99, 3)\n(1, 99, 3, 1, 99, 3)"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Распаковка"}
      sub={"Имён слева — столько же, сколько элементов"}
      main={"Звёздочка собирает лишнее в список, подчёркивание — «значение не нужно»."}
    >
      <PyCode>{`a, b = (1, 2)
first, *rest = [10, 20, 30]
x, _ = ("нужное", "лишнее")
print(a, b, first, rest)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2 10 [20, 30]"}</Cmd>
      <div className="s-note">{"Не совпало число имён — ValueError."}</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Обмен значений"}
      sub={"Без временной переменной"}
      main={"Правая часть вычисляется целиком до присваивания — путаницы не возникает."}
    >
      <PyCode>{`a, b = 1, 2
a, b = b, a
print(a, b)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 1"}</Cmd>
      <div className="s-note">{"Работает с любым числом значений: a, b, c = b, c, a — сдвиг по кругу."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Возврат нескольких значений"}
      sub={"return a, b — это кортеж"}
      main={"Функция вернула один кортеж, а вызывающий тут же распаковал его в две переменные."}
    >
      <PyCode>{`def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([3, 1, 9])
print(low, high)
print(min_max([3, 1, 9]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 9\n(1, 9)"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Кортежи вокруг нас"}
      sub={"enumerate, zip и items() отдают кортежи"}
      main={"Магии нет: цикл достаёт очередной кортеж и раскладывает его по переменным."}
    >
      <PyCode>{`print(list(enumerate(["а", "б"])))
print(list(zip([1, 2], ["x", "y"])))
print(list({"k": 1}.items()))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(0, 'а'), (1, 'б')]\n[(1, 'x'), (2, 'y')]\n[('k', 1)]"}</Cmd>
      <div className="s-note">{"Не распаковали — в переменной весь кортеж, к частям идёт индекс: pair[1]."}</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Кортеж как ключ"}
      sub={"Составной ключ: строка и столбец"}
      main={"Список в ключи нельзя, кортеж можно — словарь становится таблицей по двум признакам."}
    >
      <PyCode>{`field = {}
field[(0, 0)] = "X"
field[(1, 2)] = "O"
print(field[(1, 2)])
print((0, 1) in field)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"O\nFalse"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Список или кортеж"}
      sub={"Однородный набор — или запись фиксированной структуры"}
      main={"Если в данные никто не должен писать — делайте кортеж; если всё время дописываете — список."}
    >
      <PyCode>{`grades = [5, 4, 5]               # список
person = ("Аня", 20, "Тверь")    # кортеж-запись
print(tuple(grades), list(person))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(5, 4, 5) ['Аня', 20, 'Тверь']"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"список"} sub={"Оценки, имена файлов — длина меняется"} />
        <Node kind="green" mono={true} title={"кортеж"} sub={"Имя, возраст, город — позиция имеет смысл"} />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Сравнение и сортировка"}
      sub={"Слева направо: сначала первые, потом вторые"}
      main={"Ключ-кортеж даёт сортировку по нескольким признакам: первый главный, второй решает ничьи."}
    >
      <PyCode>{`print((1, 5) < (2, 0), (1, 5) < (1, 7))
people = [("Аня", 20), ("Боря", 30), ("Вера", 20)]

def by_key(p):
    return -p[1], p[0]

print(sorted(people, key=by_key))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True\n[('Боря', 30), ('Аня', 20), ('Вера', 20)]"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Ловушки"}
      sub={"Запятая, поверхностность, число имён"}
      main={"Неизменяемость поверхностная: список внутри кортежа по-прежнему можно менять."}
    >
      <PyCode>{`not_tuple = (5)        # просто число
t = (1, [2, 3])
t[1].append(4)          # список внутри — меняется!
print(t)
# a, b = (1, 2, 3)      # ValueError: слишком много значений`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(1, [2, 3, 4])"}</Cmd>
      <div className="s-note">{"Такой кортеж нельзя взять в ключ словаря; += для кортежа создаёт новый."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 11 · Словари и кортежи"}
      main={"Мы закончили с основными контейнерами Питона: списки, словари и кортежи."}
    >
      <div className="s-grid2">
        {([["(1,) · a, b = t", "Кортеж и распаковка", "Запятая создаёт; * собирает лишнее"], ["return a, b", "Несколько значений", "enumerate, zip, items() отдают кортежи"], ["{(r, c): v}", "Ключ словаря", "Составной ключ — таблица по двум признакам"], ["(1, 5) < (2, 0)", "Сравнение", "Слева направо; ключ-кортеж для сортировки"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Список — для однородного набора, кортеж — для записи фиксированной структуры."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P11 = {
  "13:11": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P11).
export const SLIDE_TITLES_P11 = {
  "13:11": [
    "Кортежи",
    "Создание кортежа",
    "Что умеет кортеж",
    "Пересборка",
    "Распаковка",
    "Обмен значений",
    "Несколько значений",
    "Кортежи вокруг нас",
    "Кортеж как ключ",
    "Список или кортеж",
    "Сравнение кортежей",
    "Ловушки",
    "Итог",
  ],
};
