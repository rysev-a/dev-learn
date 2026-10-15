// Слайды для «Современный Frontend», глава 2 — «Массивы, строки и списки на JS».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФУНДАМЕНТ / ГЛАВА 2</span>
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
    ["[ ]", "Массив", "Непрерывный блок памяти с константным чтением"],
    ['"s"', "Строка", "Неизменяемая последовательность"],
    ["→", "Список", "Узлы «значение плюс ссылка на следующий»"],
    ["{}", "Словари", "Map и Set — быстрый поиск по ключу"],
  ];
  return (
    <Slide
      n={1}
      title="Массивы, строки и списки"
      sub="Глава 2 · Кирпичи данных"
      main="Кто знает кирпичи, тот читает алгоритмы как открытки."
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
        За простотой JavaScript спрятаны честные решения о памяти, копиях и
        ссылках.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Массив внутри"
      sub="Плотный массив — непрерывный блок памяти"
      main="Непрерывность даёт константный доступ: адрес элемента вычисляется арифметикой."
    >
      <Cmd>{"адрес(i) = начало + i · шаг   →   arr[i] за O(1)"}</Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="arr[i] · length"
          sub="Чтение по индексу — константа; длину движок помнит отдельно"
        />
        <Node
          title="Динамический рост"
          sub="Растёт сам, без просьб о перевыделении — платит амортизированными переездами"
        />
      </div>
    </Slide>
  );
}

function S03() {
  const rows = [
    ["O(1)", "Чтение по индексу"],
    ["O(1)", "push и pop — добавить или снять с конца"],
    ["O(n)", "shift и unshift — все элементы переезжают на клетку"],
    ["O(n)", "splice в середине — сдвиг правой половины"],
  ];
  return (
    <Slide
      n={3}
      title="Цены операций"
      sub="Распределение цен надо выучить наизусть"
      main="Непрерывность покупает быстрый доступ ценой дорогих перестроек."
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
        Shift на каждый элемент в цикле над растущей очередью — квадратная
        сложность при невинном коде.
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Дырки в массиве"
      sub="Тёмный подвал JavaScript-массивов"
      main="Не создавайте дырок: undefined как значение и дырка как отсутствие значения — разные вещи, и вторая дороже."
    >
      <Cmd>{"delete arr[2]   // [10, 20, <1 empty>, 40]\narr[2]          // undefined — длины не изменились"}</Cmd>
      <div className="s-cols">
        <Node
          kind="amber"
          title="Разреженный массив"
          sub="Движок держит его как словарь — все прелести непрерывной памяти исчезают"
        />
        <Node
          mono
          kind="green"
          title="splice · filter"
          sub="Честно сдвигают хвост и переписывают массив без дырок"
        />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Мутировать или копировать"
      sub="Два лагеря методов массива"
      main="Когда сомневаетесь — работайте с копией."
    >
      <div className="s-cols">
        <Node mono title="На месте" sub="sort · reverse · splice" />
        <Node
          mono
          kind="green"
          title="Новый массив"
          sub="map · filter · slice · concat · toSorted · toReversed · toSpliced"
        />
      </div>
      <div className="s-note">
        Копии читаемы и безопасны, но платят линейной памятью: цепочка
        map–фильтр–срез держит несколько копий вживую. Чекеры сравнивают ваш
        результат с ожидаемым, и мутация входа может испортить соседние тесты.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Строки неизменяемы"
      sub="Железное правило строк"
      main="Любая «правка» строки — новая строка: копите куски в массиве и клеите join один раз."
    >
      <Cmd>
        {
          's += piece;              // копия накопленного на каждом шаге → O(n²)\nparts.push(piece);       // копим в массиве\nparts.join("");          // один проход → O(n)'
        }
      </Cmd>
      <div className="s-note">
        Присвоить s[0] нельзя: в строгом режиме — ошибка, без него — молча
        ничего. Склейка в цикле — классическая ловушка производительности.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Итерация по строкам"
      sub="Кодовые юниты и полные символы"
      main="Символы за пределами базовой плоскости занимают два юнита — ходите по строкам итератором."
    >
      <div className="s-cols">
        <Node
          mono
          kind="amber"
          title='split("") · s[i]'
          sub="Ходят по кодовым юнитам — эмодзи развалится на две половинки"
        />
        <Node
          mono
          kind="green"
          title="for…of · spread"
          sub="Работают через итератор и понимают полные символы"
        />
      </div>
      <div className="s-note">
        Для серьёзной работы с текстом есть codePointAt и fromCodePoint.
        Однажды ловушка встретится в продакшне с эмодзи в никнейме.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Стек, очередь, дек"
      sub="Классические структуры поведения из массива"
      main="Это правила поведения, а не способы хранения: выбор структуры — выбор порядка выхода."
    >
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="Стек"
          sub="push · pop — последний пришёл, первый вышел"
        />
        <Node
          mono
          title="Очередь"
          sub="push · shift — первый пришёл, первый вышел; на ней строятся обходы в ширину"
        />
        <Node mono title="Дек" sub="Операции с обоих концов" />
      </div>
      <div className="s-note">
        Shift линеен — для больших очередей честнее хранить индекс головы и
        двигать его. Очередь с приоритетами потребует кучи из главы о деревьях.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Связный список"
      sub="Антипод массива: узлы со ссылками"
      main="Массив и список зеркальны: у одного дёшево читать, у другого — перестраивать."
    >
      <Cmd>{"узел = { value, next }   // в JavaScript нет встроенного списка"}</Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="amber"
          title="list[i] — O(n)"
          sub="До пятисотого элемента — пройти по ссылкам 499 промежуточных"
        />
        <Node
          mono
          kind="green"
          title="Вставка в голову — O(1)"
          sub="Переприсваивание одной ссылки: без сдвигов и копий"
        />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Разворот и поиск цикла"
      sub="Две задачи, которые решаются переменными"
      main="Обе задачи решаются голыми переменными: константная память на любой длине списка."
    >
      <Cmd>
        {
          "let prev = null, curr = head;   // разворот: сохранить хвост!\nlet slow = head, fast = head;   // Флойд: быстрый прыгает через два"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          title="Разворот"
          sub="Предыдущий, текущий, следующий — иначе остаток списка потеряется навсегда"
        />
        <Node
          kind="green"
          title="Флойд против Set"
          sub="Медленный шагает по узлу, быстрый — через два: догонит, если круг есть"
        />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Список против массива"
      sub="Признание, которое меняет практику"
      main="В современных движках списки проигрывают массивам даже там, где теория обещает им победу."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Теория"
          sub="Вставка в середину списка — константа против линейного сдвига массива"
        />
        <Node
          kind="green"
          title="Практика"
          sub="Чтобы встать в середину, надо линейно дойти; сдвиг в массиве — машинная операция над данными в кэше"
        />
      </div>
      <div className="s-note">
        Списки живут в специализированных ролях: планировщики, неизменяемые
        структуры функционального стиля, учебные задачи. Для повседневных
        коллекций — массив, Map или Set.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Словари: Map и Set"
      sub="Рядом с массивом и списком всегда идут они"
      main="Массив — про порядок и позиции, словарь — про быстрый поиск по ключу, список — про дешёвые перестройки."
    >
      <div className="s-grid2">
        <Node
          mono
          title="Map"
          sub="Пары ключ-значение, помнит порядок вставки, итерируется напрямую"
        />
        <Node mono title="Set" sub="Только ключи, мгновенно отвечает: видел ли он такой" />
        <Node
          mono
          kind="amber"
          title="WeakMap · WeakSet"
          sub="Позволяют сборщику мусора убирать объекты-ключи"
        />
      </div>
      <div className="s-note">
        Полный разбор словарей — в главе о хеш-таблицах; здесь запомните их
        место в системе кирпичей.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["[ ]", "Массив", "Константное чтение, дорогие сдвиги, дырки запрещены"],
    ['"s"', "Строки", "Неизменяемы: копить куски и клеить один раз"],
    ["⤮", "Стек и очередь", "Поведение, а не хранение: стек против очереди"],
    ["→", "Список", "Разворот тремя переменными, цикл — по Флойду"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 2 · Массивы, строки и списки"
      main="Выбор структуры становится осмысленным решением, а не привычкой."
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
        В следующей главе построим на этих кирпичах поиск и сортировку —
        базовые алгоритмы, на которых держится всё остальное.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J2 = {
  "11:2": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J2).
export const SLIDE_TITLES_J2 = {
  "11:2": [
    "Введение: кирпичи данных",
    "Массив внутри",
    "Цены операций",
    "Дырки в массиве",
    "Мутировать или копировать",
    "Строки неизменяемы",
    "Итерация по строкам",
    "Стек, очередь, дек",
    "Связный список",
    "Разворот и поиск цикла",
    "Список против массива",
    "Словари: Map и Set",
    "Итог",
  ],
};
