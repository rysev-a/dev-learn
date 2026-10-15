// Слайды для «Современный Frontend», глава 3 — «Поиск и сортировка».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФУНДАМЕНТ / ГЛАВА 3</span>
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

const Arr = () => <span className="s-arr">→</span>;
const Down = () => <span className="s-arr">↓</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    [
      "find",
      "Линейный поиск",
      "Честный перебор: find, findIndex, indexOf, includes",
    ],
    ["÷2", "Бинарный поиск", "Логарифм — но только по отсортированному"],
    ["sort", "Встроенный sort", "Компаратор, устойчивость, мутация входа"],
    ["⚙", "Четыре сортировки", "Пузырёк, вставки, слияние, быстрая — руками"],
  ];
  return (
    <Slide
      n={1}
      title="Поиск и сортировка"
      sub="Глава 3 · Фундамент"
      main="После этого урока вы знаете, когда одной строчки достаточно, а когда алгоритм пишут руками."
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
        За коротким вызовом find или sort прячутся разные формы роста, разные
        гарантии и разные ловушки.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Линейный поиск"
      sub="Он уже у вас в руках"
      main="Если искать придётся многократно — данные надо готовить заранее: сортировать или складывать в словарь."
    >
      <Cmd>
        {"arr.find(x => x.id === 42)\narr.includes(x);  arr.indexOf(x)"}
      </Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="O(n)"
          sub="На неотсортированных данных лучше не существует"
        />
        <Node
          mono
          kind="amber"
          title="Поиск внутри поиска"
          sub="Вложенные переборы дают квадрат"
        />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Бинарный поиск"
      sub="Открываем словарь посередине и половину выбрасываем"
      main="Миллион элементов сжимается до двадцати сравнений — отсортированные данные это валюта."
    >
      <Cmd>
        {
          "let l = 0, r = a.length - 1;\nwhile (l <= r) {\n  const mid = (l + r) >> 1;      // середина, округление вниз\n  if (a[mid] === x) return mid;\n  if (a[mid] < x) l = mid + 1;   // правая половина\n  else            r = mid - 1;   // левая половина\n}"
        }
      </Cmd>
      <p className="s-hint">
        Каждый шаг режет кусок вдвое — это прямое следствие логарифма, а не
        метафора.
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Границы и вечный цикл"
      sub="Бинарный поиск славится ошибками на единицу"
      main="Симптом вечного цикла — зависшая вкладка без ошибки; проверяйте границы первыми."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Границы должны сходиться"
          sub="Неверное условие цикла или обновление без шага от середины — поиск зацикливается навсегда"
        />
        <Node
          title="Предпосылка строгая"
          sub="Массив обязан быть отсортирован, иначе логарифм превращается в гадание"
        />
      </div>
      <div className="s-note">
        Строки сравниваются иначе, чем числа, а для сложных критериев придётся
        написать функцию сравнения отдельно.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Компаратор для sort"
      sub="Первая страница сортировки — предупреждение"
      main="Числам нужен компаратор «а минус б», кириллице — localeCompare."
    >
      <Cmd>
        {
          "[10, 9, 1].sort()                     // [1, 10, 9] — как строки!\n[10, 9, 1].sort((a, b) => a - b)      // [1, 9, 10]\nitems.sort((a, b) => b.price - a.price)  // по полю, по убыванию\nnames.sort((a, b) => a.localeCompare(b)) // имена по-русски"
        }
      </Cmd>
      <div className="s-note">
        Обычное сравнение строк не знает про «ё» и регистры — оно рассортирует
        кириллицу по кодам юникода, а не по алфавиту.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Мутация и устойчивость"
      sub="Второе предупреждение и одно приятное обещание"
      main="Сортировка по нескольким полям — простая последовательность устойчивых проходов."
    >
      <div className="s-cols">
        <Node
          mono
          kind="amber"
          title="sort() на месте"
          sub="Нужен исходный порядок? Копия через спред или toSorted"
        />
        <Node
          kind="green"
          title="Устойчивость"
          sub="Равные по компаратору элементы сохраняют исходный порядок — формальная гарантия движка"
        />
      </div>
      <div className="s-note">
        Отсортировали заказы по дате, потом по городу — внутри каждого города
        хронология цела.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Пузырёк"
      sub="Первая сортировка, написанная руками"
      main="Квадратная сложность, зато идея видна с одного взгляда."
    >
      <Cmd>
        {
          "for (let i = 0; i < n; i++)\n  for (let j = 0; j < n - 1 - i; j++)\n    if (a[j] > a[j + 1])\n      [a[j], a[j + 1]] = [a[j + 1], a[j]];  // соседи меняются местами"
        }
      </Cmd>
      <div className="s-note">
        За каждый проход максимум всплывает в конец, как пузырёк воздуха. Если
        тесты просят не менять исходный массив — начните с копии: slice() или
        спред.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Вставки"
      sub="То, как раскладывают карты в руке"
      main="Реальные данные часто почти упорядочены — и вставки чувствуют это без всяких настроек."
    >
      <Cmd>
        {
          "const key = a[i];\nlet j = i - 1;\nwhile (j >= 0 && a[j] > key) {  // сдвигаем вправо\n  a[j + 1] = a[j];\n  j--;\n}\na[j + 1] = key;                 // вставили на место"
        }
      </Cmd>
      <div className="s-cols">
        <Node mono kind="amber" title="O(n²) в среднем" sub="Обычные данные" />
        <Node
          mono
          kind="green"
          title="Почти O(n) на почти отсортированных"
          sub="Каждый элемент сдвигается на одну-две позиции"
        />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Слияние"
      sub="Первый алгоритм «разделяй и властвуй»"
      main="Гарантированный n log n на любых данных; цена — линейная дополнительная память, и это честная сделка."
    >
      <Cmd>
        {
          "const left  = mergeSort(a.slice(0, m));  // половины — slice\nconst right = mergeSort(a.slice(m));\n// сливаем двумя указателями: сравниваем головы,\n// меньшую забираем в результат"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="O(n log n) всегда"
          sub="Независимо от коварства данных; решение чистое и устойчивое"
        />
        <Node
          mono
          kind="amber"
          title="O(n) памяти"
          sub="Копии половин и результат слияния"
        />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Быстрая сортировка"
      sub="Противоположность по характеру"
      main="Спасение от квадрата простое: случайная опора или медиана из трёх."
    >
      <Cmd>
        {
          "const less = a.filter(x => x < p);    // опорный элемент p\nconst more = a.filter(x => x >= p);\nreturn [...qsort(less), p, ...qsort(more)];"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="O(n log n) в среднем"
          sub="Читается как определение: разделил — повторил"
        />
        <Node
          mono
          kind="amber"
          title="O(n²) на отсортированных"
          sub="Неудачная опора скатывает сложность в квадрат"
        />
      </div>
      <div className="s-note">
        На случайных данных плохие расколы почти невероятны; библиотеки ещё и
        переключаются на слияние при подозрительно глубокой рекурсии.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Встроенный sort"
      sub="Не зря одна строчка: внутри гибриды вроде тимсорта"
      main="В продакшне сортируйте встроенным методом, свои сортировки пишите для понимания и особых случаев."
    >
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="Тимсорт"
          sub="Гарантированный n log n и отличное чувство почти упорядоченных данных"
        />
        <Node
          title="Особые случаи"
          sub="Частичная сортировка топ-n, слияние уже отсортированных потоков"
        />
      </div>
      <div className="s-note">
        Знание внутренностей превращает вас из пользователя функции в инженера,
        который понимает её гарантию и её цену.
      </div>
    </Slide>
  );
}

function S12() {
  const rows = [
    ["min · max", "Первый и последний элементы отсортированного массива"],
    ["O(log n)", "Бинарный поиск по отсортированным данным"],
    ["соседи", "Дубликаты после сортировки оказываются рядом"],
    ["топ-n", "Лучшие элементы без полной сортировки"],
  ];
  return (
    <Slide
      n={12}
      title="Сортировка как мышление"
      sub="Инструмент, а не только вызов"
      main="Вопрос «что изменится, если данные отсортировать?» — часто половина решения."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        Цена сортировки n log n окупается десятками линейных проходов после неё.
      </p>
    </Slide>
  );
}

function S13() {
  const topics = [
    [
      "find",
      "Линейный поиск",
      "O(n) — честная цена на неотсортированных данных",
    ],
    [
      "÷2",
      "Бинарный поиск",
      "Логарифм, отсортированность и аккуратные границы",
    ],
    ["sort", "Компаратор", "a - b для чисел, localeCompare для кириллицы"],
    ["⚙", "Четыре взгляда", "Пузырёк, вставки, слияние, быстрая"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 3 · Поиск и сортировка"
      main="От учебного пузырька до промышленного встроенного sort — четыре взгляда на одну задачу."
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
        В следующей главе — хеш-таблицы: структура, находящая данные без всякой
        сортировки, за константное время в среднем.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J3 = {
  "11:3": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J3).
export const SLIDE_TITLES_J3 = {
  "11:3": [
    "Введение: поиск и сортировка",
    "Линейный поиск",
    "Бинарный поиск",
    "Границы и вечный цикл",
    "Компаратор для sort",
    "Мутация и устойчивость",
    "Пузырёк",
    "Вставки",
    "Слияние",
    "Быстрая сортировка",
    "Встроенный sort",
    "Сортировка как мышление",
    "Итог",
  ],
};
