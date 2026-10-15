// Слайды для «Современный Frontend», глава 1 — «Сложность: считаем операции».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФУНДАМЕНТ / ГЛАВА 1</span>
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
    ["O", "Форма роста", "Как работа растёт вместе с данными"],
    ["±", "Три случая", "Лучший, средний и худший у одного решения"],
    ["↓", "Цены методов", "Shift, splice и копии прячут линейность"],
    ["~", "Амортизация", "Редкий дорогой переезд — константа в среднем"],
  ];
  return (
    <Slide
      n={1}
      title="Сложность: считаем операции"
      sub="Глава 1 · Фундамент"
      main="«Код работает» и «код работает на данных в тысячу раз больше» — разные вещи."
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
        Нужна мера, которая описывает само решение, а не конкретный ноутбук, —
        это анализ сложности.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Форма роста, а не секунды"
      sub="Поиск значения в массиве двумя способами"
      main="Нас интересует не время в миллисекундах, а то, как быстро растёт работа вместе с данными."
    >
      <div className="s-cols">
        <div className="s-card">
          <div className="s-label">INCLUDES — ЛИСТАТЬ ПОДРЯД</div>
          <span className="s-node-title">Рост линейный</span>
          <span className="s-node-sub">
            Элементов вдвое больше — проверок в среднем вдвое больше
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">ДЕЛИТЬ ПОПОЛАМ</div>
          <span className="s-node-title">Рост логарифмический</span>
          <span className="s-node-sub">
            Отсортированный массив стал вдвое толще — всего одно лишнее
            сравнение
          </span>
        </div>
      </div>
      <p className="s-hint">
        На десяти элементах разницы не заметите вовсе, а на миллионе она
        измеряется тысячами раз.
      </p>
    </Slide>
  );
}

function S03() {
  const rows = [
    ["O(1)", "Константа · arr[i], длина length, map.get(key)"],
    ["O(log n)", "Логарифм · бинарный поиск, спуск по дереву"],
    ["O(n)", "Линейность · один проход for: максимум, сумма"],
    ["O(n log n)", "Сортировка методом sort"],
    ["O(n²)", "Вложенные циклы · сравнить все пары"],
    ["O(2^n)", "Экспонента · умирает уже на паре десятков входов"],
  ];
  return (
    <Slide
      n={3}
      title="Классы роста"
      sub="Их стоит выучить как алфавит — в JavaScript они на каждом шагу"
      main="Классы роста — таблица умножения алгоритмиста."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Миллион элементов"
      sub="Разницу между классами стоит один раз почувствовать на числах"
      main="На больших данных класс роста сильнее любой аккуратности и любого железа."
    >
      <div className="s-bar-wrap">
        <span>
          <span className="s-path accent">O(log n)</span> · около 20 операций
        </span>
        <div className="s-bar">
          <div style={{ width: "2%" }} />
        </div>
        <span>
          <span className="s-path accent">O(n)</span> · 1 000 000
        </span>
        <div className="s-bar">
          <div style={{ width: "10%" }} />
        </div>
        <span>
          <span className="s-path accent">O(n log n)</span> · около 20 000 000
        </span>
        <div className="s-bar">
          <div style={{ width: "34%" }} />
        </div>
        <span className="amber-text">
          <span className="s-path accent">O(n²)</span> · триллион — часы работы
        </span>
        <div className="s-bar amber">
          <div style={{ width: "100%" }} />
        </div>
      </div>
      <p className="s-hint">
        Речь не о неуклюжем коде против аккуратного: на больших данных класс
        роста побеждает и аккуратность, и быстрый процессор.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Микрооптимизации не спасают"
      sub="Константы биг-о сознательно отбрасывает"
      main="Сначала выберите правильную форму роста, потом украшайте константы — не наоборот."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Константы не меняют класс"
          sub="forEach вместо for, вынести length — форма роста та же"
        />
        <Node
          kind="green"
          title="Меняет только решение"
          sub="Квадрат превращается в линейность новой идеей, а не правкой строк"
        />
      </div>
      <div className="s-note">
        Движок V8 творит чудеса компиляции, но не может превратить квадрат в
        линейность: форма роста принадлежит вашему решению, а не компилятору.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Три случая одного поиска"
      sub="У одного решения несколько лиц"
      main="Инженер проектирует по худшему случаю, а на средний смотрит как на бонус."
    >
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="Лучший"
          sub="find находит нужное первым же элементом — константа"
        />
        <Node mono title="Средний" sub="Что происходит на типичных данных" />
        <Node
          kind="amber"
          mono
          title="Худший"
          sub="Элемента нет вообще — перебор честно пройдёт весь массив"
        />
      </div>
      <div className="s-note">
        Исключение из правила: если средний случай радикально лучше худшего и
        злые данные маловероятны — ориентируйтесь на среднее. Так живёт
        большинство хеш-кода.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Сделка объектов и Map"
      sub="Главный инструмент ежедневного JavaScript"
      main="Усреднённая константа при редком линейном провале — сделка, которую надо осознавать."
    >
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="O(1) в среднем"
          sub="Чтение obj по ключу, map.get, set.has — ради этого их и берут"
        />
        <Node
          mono
          kind="amber"
          title="O(n) в худшем"
          sub="Все ключи сгрудились в одно ведро внутри таблицы"
        />
      </div>
      <div className="s-note">
        Сделка нормальная, если провал вам не встретится, и опасная, если по
        вашим ключам он гарантирован. Отличать первое от второго — признак
        инженера.
      </div>
    </Slide>
  );
}

function S08() {
  const rows = [
    ["O(1)", "Чтение по индексу"],
    ["O(1)", "push и pop — работа с концом массива"],
    ["O(n)", "shift и unshift — сдвиг всех остальных элементов"],
    ["O(n)", "splice в середине — сдвиг половины массива"],
    ["O(n)", "concat, slice, map, filter — копия, линейная работа и память"],
  ];
  return (
    <Slide
      n={8}
      title="Цены методов массива"
      sub="Именно они чаще всего портят сложность незаметно"
      main="Самые коварные методы — сдвигающие и копирующие."
    >
      <div className="s-table">
        {rows.map(([sym, d], i) => (
          <div key={i}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        Цикл, внутри которого на каждом шаге вызывается shift, — это квадрат,
        замаскированный под аккуратный код.
      </p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Амортизация push"
      sub="Слово из документации, которое стоит понимать"
      main="Редкие дорогие события размазываются по множеству дешёвых — это честная средняя цена."
    >
      <Cmd>
        {
          "запас ёмкости кончился → переезд в блок побольше ← редко\nдописать элемент в конец                ← обычно"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="amber"
          title="O(n)"
          sub="Переезд: разово копирует весь массив"
        />
        <Node
          mono
          kind="green"
          title="O(1)"
          sub="push в пересчёте на одну операцию — как копилка"
        />
      </div>
      <div className="s-note">
        Тот же расчёт применим к росту строк и к сборке мусора: биг-о описывает
        честную среднюю цену, а не худший мгновенный чек.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Вторая валюта — память"
      sub="Время и память обмениваются по курсу"
      main="Выбор курса обмена — часть проектирования, а не мелочь."
    >
      <div className="s-grid2">
        <Node
          title="Копии методов"
          sub="map, filter, slice — линейная память; цепочка из трёх держит три копии вживую"
        />
        <Node
          kind="amber"
          title="Рекурсия ест стек"
          sub="Каждый вложенный вызов занимает место — глубокая кончается «превышен размер стека»"
        />
        <Node
          kind="green"
          title="Память можно тратить с выгодой"
          sub="Set из виденных значений делает дедупликацию константной на элемент"
        />
      </div>
      <div className="s-note">
        Обмен памяти на скорость — классическая сделка, а не уловка: кэши и
        индексы в продакшне живут по этому же курсу.
      </div>
    </Slide>
  );
}

function S11() {
  const rows = [
    ["цикл × тело", "Сложность цикла умножается на сложность его тела"],
    ["шаг + шаг", "Последовательные шаги складываются: линейность + линейность = линейность"],
    ["O(n) внутри O(n)", "Вложенный цикл или includes по другому массиву — квадрат"],
  ];
  return (
    <Slide
      n={11}
      title="Арифметика сложности"
      sub="Два правила, которых хватает почти всегда"
      main="Умножение для вложенности, сложение для последовательности — и вы предсказываете зависания до запуска."
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
        Включая инструменты из библиотеки: includes, спрятанный в цикле, стоит
        столько же, сколько развёрнутый вложенный цикл.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Анализ и замер"
      sub="console.time и performance.now полезны — но в правильном порядке"
      main="Биг-о предсказывает, замер проверяет — инструменты работают в паре, а не вместо друг друга."
    >
      <div className="s-cols">
        <Node
          mono
          title="console.time · performance.now"
          sub="Правда конкретной машины, версии движка и конкретных данных"
        />
        <Node
          kind="amber"
          title="Замер без анализа опасен"
          sub="На маленьком массиве квадратный алгоритм запросто обгонит линейный"
        />
      </div>
      <div className="s-note">
        Правильный порядок обратный: сначала анализ выбирает форму решения,
        потом замеры подтверждают выбор на реальных объёмах.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["O", "Классы роста", "От константы до экспоненты — как алфавит"],
    ["±", "Три случая", "Гарантия по худшему, средний — бонус"],
    ["↓", "Цены методов", "Сдвигающие и копирующие — самые коварные"],
    ["~", "Амортизация", "Редкая дорогая работа — константа в среднем"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 1 · Сложность: считаем операции"
      main="Сложность — язык, на котором решения сравнивают независимо от железа."
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
        В следующей главе — спуск на землю: массивы, строки и связные списки,
        кирпичи, на которых стоит всё остальное.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J1 = {
  "11:1": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J1).
export const SLIDE_TITLES_J1 = {
  "11:1": [
    "Введение: считаем операции",
    "Форма роста",
    "Классы роста",
    "Миллион элементов",
    "Микрооптимизации не спасают",
    "Три случая",
    "Сделка хешей",
    "Цены методов массива",
    "Амортизация push",
    "Вторая валюта — память",
    "Арифметика сложности",
    "Анализ и замер",
    "Итог",
  ],
};
