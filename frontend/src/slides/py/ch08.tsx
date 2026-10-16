import { makeSlide } from "../SlideFrame.tsx";
import { Arr, Cmd, Node, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 8 — «Списки: сортировка и генераторы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ДАННЫЕ И ЦИКЛЫ / ГЛАВА 8", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics: [string, string, string][] = [
    ["sorted · key", "Сортировка", "По убыванию, по длине, по любому признаку"],
    ["[x for ...]", "Генератор", "Фильтрация и преобразование в одной строке"],
    ["any · all", "Вопросы о списке", "Есть ли хоть один — и все ли подходят"],
    ["append · pop", "Стопка", "Список как стек: скобки, отмена действий"],
  ];
  return (
    <Slide
      n={1}
      title="Списки: сортировка и генераторы"
      sub="Глава 8 · Данные и циклы"
      main="Инструменты, которые превращают десять строк в одну — и делают код яснее."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        После этой главы чужой код со списками читается без запинок, а свой —
        пишется короче.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Сорт и сортед"
      sub="На месте или новый список"
      main="Сортед ничего не портит: исходный порядок остаётся при нём."
    >
      <PyCode>{`nums = [3, 1, 2]
print(sorted(nums))        # [1, 2, 3]
print(nums)                # [3, 1, 2] — не тронут
nums.sort(reverse=True)    # на месте, по убыванию
print(nums)                # [3, 2, 1]`}</PyCode>
      <div className="s-cols">
        <Node mono title="nums.sort()" sub="Меняет список, возвращает пустоту" />
        <Node kind="amber" mono title="nums = nums.sort()" sub="Ошибка: в имени окажется None" />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Строки и регистр"
      sub="Заглавные идут раньше строчных; числа-строки — как текст"
      main="Перед сравнением приводите слова к одному регистру, а строки — к числам."
    >
      <PyCode>{`words = ["арбуз", "Яблоко", "банан"]
print(sorted(words))
print(sorted(["10", "2", "1"]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['Яблоко', 'арбуз', 'банан']\n['1', '10', '2']"}</Cmd>
      <div className="s-note">
        Числа и строки в одном списке Питон сортировать откажется — ошибка.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Параметр key"
      sub="Сортируем не элементы, а то, что из них вычислено"
      main="Функцию передают без скобок: её не вызывают, а отдают как инструмент."
    >
      <PyCode>{`words = ["ccc", "a", "bb"]
print(sorted(words, key=len))
names = ["вера", "Аня", "борис"]
print(sorted(names, key=str.lower))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['a', 'bb', 'ccc']\n['Аня', 'борис', 'вера']"}</Cmd>
      <div className="s-note">
        Сортировка устойчива: элементы с равным ключом сохраняют исходный порядок.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Приёмы с порядком"
      sub="Переворот, тройка лидеров, проверка порядка"
      main="Небольшие кирпичики — sorted, срез, равенство — складываются в решения."
    >
      <PyCode>{`nums = [5, 1, 9, 3]
print(sorted(nums, reverse=True)[:3])   # [9, 5, 3]
for x in reversed(nums):                # с конца: 3, 9, 1, 5
    print(x)
print(nums == sorted(nums))             # False`}</PyCode>
      <div className="s-note">
        Сортировка стоит времени: ради одного максимума её не заводят — есть max.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Генератор списка"
      sub="Цикл с аппендом — одной строкой"
      main="Читается как фраза: «квадрат икса для каждого икса из этих чисел»."
    >
      <PyCode>{`result = []
for x in range(1, 6):
    result.append(x * x)`}</PyCode>
      <div className="s-cols">
        <Arr />
        <Node kind="green" mono title="[x * x for x in range(1, 6)]" sub="[1, 4, 9, 16, 25] — тот же результат в одну строку" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Условие в генераторе"
      sub="if — в самом конце, после заголовка цикла"
      main="Условие в конце фильтрует, выражение в начале преобразует."
    >
      <PyCode>{`nums = [1, 2, 3, 4, 5, 6]
evens = [x for x in nums if x % 2 == 0]       # [2, 4, 6]
sq = [x * x for x in nums if x % 2 == 0]      # [4, 16, 36]`}</PyCode>
      <div className="s-cols">
        <Node mono title="x * x" sub="Что кладём" />
        <Node mono title="for x in nums" sub="Откуда берём" />
        <Node kind="green" mono title="if x % 2 == 0" sub="При каком условии" />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Строки: split и join"
      sub="Конвейер: разбили, обработали, склеили"
      main="join принимает только строки — числа сначала превращают через str."
    >
      <PyCode>{`words = "привет мир".split()
print([len(w) for w in words])         # [6, 3]
print([w.upper() for w in words])      # ['ПРИВЕТ', 'МИР']
print(", ".join(words))                # привет, мир
nums = [1, 2, 3]
print("+".join([str(n) for n in nums]))   # 1+2+3`}</PyCode>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Когда лучше цикл"
      sub="Читаемость важнее краткости"
      main="Хороший код — не самый короткий, а самый понятный."
    >
      <div className="s-cols">
        <Node kind="green" title="Генератор" sub="Новый список по простому правилу" />
        <Node kind="amber" title="Цикл" sub="Несколько действий, печать, запись в файл" />
        <Node kind="amber" title="Цикл" sub="Вложенность глубже двух уровней" />
      </div>
      <div className="s-note">
        Не читается с первого раза — возвращайтесь к обычному циклу.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="any и all"
      sub="Есть ли хоть один — и все ли подходят"
      main="Это кванторы из дискретной математики: «существует» и «для всех»."
    >
      <PyCode>{`nums = [5, 120, 8]
print(any(x > 100 for x in nums))    # True
print(all(x > 0 for x in nums))      # True
print(any([]), all([]))              # False True`}</PyCode>
      <div className="s-note">
        Пустой набор: подходящих нет — any даёт False, нарушителей нет — all даёт
        True.
      </div>
    </Slide>
  );
}

function S11() {
  const topics: [string, string, string][] = [
    ["total = 0", "Сумма", "Накопитель с нуля; произведение — с единицы"],
    ["nums[0]", "Максимум", "Начинайте с первого элемента, а не с нуля"],
    ["count += 1", "Подсчёт", "Счётчик растёт, когда условие истинно"],
    ["not in", "Без повторов", "Добавляем в результат только новое"],
  ];
  return (
    <Slide
      n={11}
      title="Шаблоны задач"
      sub="Большинство задач на списки — их комбинация"
      main="Это ваш набор слесаря: суммы, максимумы, подсчёты, поиск, повторы."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
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

function S12() {
  return (
    <Slide
      n={12}
      title="Список-стопка"
      sub="append кладёт наверх, pop снимает с вершины"
      main="Стек лежит в основе проверки скобок, кнопки «назад» и отмены действий."
    >
      <PyCode>{`stack = []
stack.append("(")
stack.append("(")
stack.pop()
print(stack)    # ['(']`}</PyCode>
      <div className="s-cols">
        <Node mono title="(" sub="Открывающая — в стопку" />
        <Node kind="green" mono title=")" sub="Закрывающая — снять; стопка пуста — скобки неверны" />
      </div>
    </Slide>
  );
}

function S13() {
  const topics: [string, string, string][] = [
    ["sorted · key", "Сортировка", "Сорт — на месте, сортед — новый; reverse и key"],
    ["[x for ...]", "Генератор", "Выражение, цикл и необязательное условие"],
    ["any · all", "Вопросы", "Есть ли подходящий — и подходят ли все"],
    ["append · pop", "Стек", "Скобки, отмена действий, разбор формул"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 8 · Данные и циклы"
      main="С этой главой тема списков закончена."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">
        Следующая глава — словари: пары «ключ-значение», где вместо номера —
        осмысленное имя.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P8 = {
  "13:8": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P8).
export const SLIDE_TITLES_P8 = {
  "13:8": [
    "Сортировка и генераторы",
    "Сорт и сортед",
    "Строки и регистр",
    "Параметр key",
    "Приёмы с порядком",
    "Генератор списка",
    "Условие в генераторе",
    "split и join",
    "Когда лучше цикл",
    "any и all",
    "Шаблоны задач",
    "Список-стопка",
    "Итог",
  ],
};
