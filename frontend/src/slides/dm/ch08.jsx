// Слайды для «Дискретной математики», глава 8 — «Графы: основы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ДИСКРЕТНАЯ МАТЕМАТИКА / ГРАФЫ И ВЕРОЯТНОСТЬ / ГЛАВА 8</span>
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
const Edge = () => <span className="s-arr">—</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["V·E", "Вершины и рёбра", "Самая экономная модель всего, где важны связи"],
    ["Σdeg", "Степени и рукопожатия", "Сумма степеней всегда равна двум числам рёбер"],
    ["→", "Пути и связность", "Компоненты — острова достижимости"],
    ["[·]", "Матрица или списки", "Два способа уложить граф в память"],
  ];
  return (
    <Slide
      n={1}
      title="Графы: основы"
      sub="Глава 8 · Графы и вероятность"
      main="Дерево элементов, зависимости и соцсеть — это графы, даже когда так не называются."
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
        Сегодня учимся говорить о связях строго, а в двух следующих главах —
        ходить по графам.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Что такое граф"
      sub="Множество вершин и множество рёбер"
      main="Ни координат, ни масштаба — только объекты и связи между ними."
    >
      <Cmd>{"G = (V, E)\nV = {A, B, C, D} · E = {A—B, B—C, A—C, C—D}"}</Cmd>
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">КАРТА ДРУЗЕЙ</div>
          <span className="s-node-title">Вершины — люди</span>
          <span className="s-node-sub">Рёбра — дружба: связь работает в обе стороны</span>
        </div>
        <div className="s-card">
          <div className="s-label">СХЕМА МЕТРО</div>
          <span className="s-node-title">Вершины — станции</span>
          <span className="s-node-sub">Рёбра — перегоны: дуга или ломаная не важны</span>
        </div>
      </div>
      <div className="s-note">
        Для графа важна лишь связка «эта станция соединена с той»: карта метро
        и список перегонов — один и тот же граф.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Направление рёбер"
      sub="Первое проектное решение: стрелки или нет"
      main="Перепутаете тип графа — алгоритм будет отвечать не на те вопросы."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">НЕОРИЕНТИРОВАННЫЙ</div>
          <div className="s-cols">
            <Node mono title="я" />
            <Edge />
            <Node mono title="друг" />
          </div>
          <span className="s-node-title">Дружба взаимна</span>
          <span className="s-node-sub">Если я вам друг, то и вы мне друг</span>
        </div>
        <div className="s-card">
          <div className="s-label">ОРИЕНТИРОВАННЫЙ</div>
          <div className="s-cols">
            <Node mono title="я" />
            <Arr />
            <Node mono title="блогер" />
          </div>
          <span className="s-node-title">Подписка — стрелка</span>
          <span className="s-node-sub">Блогер может меня не замечать: обратного ребра нет</span>
        </div>
      </div>
      <div className="s-note">
        Ссылки между страницами, потоки данных, переходы по сайту — всё это
        стрелки.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Лемма о рукопожатиях"
      sub="deg(v) — сколько рёбер касается вершины"
      main="Каждое рукопожатие прибавляет единицу обоим участникам — в сумме степеней каждое ребро считается дважды."
    >
      <div className="s-cols">
        <Node mono title="A · deg 2" />
        <Node mono title="B · deg 2" />
        <Node mono kind="amber" title="C · deg 3" sub="нечётная" />
        <Node mono kind="amber" title="D · deg 1" sub="нечётная" />
      </div>
      <div className="s-opts">
        <span className="s-path accent">A—B</span>
        <span className="s-path accent">B—C</span>
        <span className="s-path accent">A—C</span>
        <span className="s-path accent">C—D</span>
        <span>4 ребра — 8 рукопожатий</span>
      </div>
      <Cmd>{"deg(A) + deg(B) + deg(C) + deg(D) = 2 + 2 + 3 + 1 = 8 = 2 · |E|"}</Cmd>
      <div className="s-note">
        Следствие неочевидное: вершин с нечётной степенью в любом графе чётное
        число — здесь они две. Такие выводы из простого подсчёта — фирменный
        вкус теории графов.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Пути и циклы"
      sub="Движение по рёбрам"
      main="«Достижима ли база данных с этого сервиса?» — это вопрос о существовании пути."
    >
      <div className="s-cols">
        <Node mono title="дом" />
        <Arr />
        <Node mono title="магазин" />
        <Arr />
        <Node mono title="работа" />
      </div>
      <div className="s-opts">
        <span className="s-path accent">путь</span>
        <span>соседние вершины соединены ребром · длина = число рёбер</span>
      </div>
      <Cmd>{"цикл: A → B → C → A · вернулся в старт, рёбра не повторял"}</Cmd>
      <div className="s-note">
        Понятия выглядят очевидными, но на них держится половина практических
        задач — от навигации до достижимости сервисов.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Компоненты связности"
      sub="Когда граф распадается на острова"
      main="Связный граф — из любой вершины можно дойти до любой другой."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">КОМПОНЕНТА 1</div>
          <div className="s-cols">
            <Node mono title="A" />
            <Edge />
            <Node mono title="B" />
            <Edge />
            <Node mono title="C" />
          </div>
          <span className="s-node-sub">Все достижимы друг для друга</span>
        </div>
        <div className="s-card">
          <div className="s-label">КОМПОНЕНТА 2</div>
          <div className="s-cols">
            <Node mono title="X" />
            <Edge />
            <Node mono title="Y" />
          </div>
          <span className="s-node-sub">Мостов между островами нет</span>
        </div>
      </div>
      <div className="s-note">
        В соцсети компоненты — сообщества без общих знакомых; в зависимостях —
        пакеты, которые ставятся и удаляются только вместе. Поиск этих островов
        — задача следующей главы.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Три графа из жизни"
      sub="Дом-дерево, зависимости, маршруты"
      main="Веса не меняют устройство графа — к вопросу «как добраться» добавляется «почём»."
    >
      <div className="s-grid2">
        <Node
          mono
          title="DOM-дерево"
          sub="ориентированный, почти дерево: один родитель, сколько угодно детей"
        />
        <Node
          mono
          kind="amber"
          title="Зависимости пакетов"
          sub="ориентированный: цикл менеджер честно покажет ошибкой"
        />
        <Node
          mono
          kind="green"
          title="Карта маршрутов"
          sub="взвешенный: рёбра несут минуты или рубли"
        />
      </div>
      <div className="s-note">
        Навигатор ищет путь с минимальной суммой весов — так взвешенный граф
        превращает «как добраться» в «как добраться дешевле».
      </div>
    </Slide>
  );
}

function S08() {
  const rows = [
    ["ребро?", "A B C D"],
    ["A", "0 1 1 0"],
    ["B", "1 0 1 0"],
    ["C", "1 1 0 1"],
    ["D", "0 0 1 0"],
  ];
  return (
    <Slide
      n={8}
      title="Матрица смежности"
      sub="Таблица n × n: единица на пересечении — ребро есть"
      main="Проверка конкретного ребра — константа: заглянули в ячейку и узнали."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-cols">
        <Node mono kind="green" title="O(1)" sub="«есть ли ребро u—v?» — одна ячейка" />
        <Node mono title="n²" sub="память — квадрат от числа вершин, при любом числе рёбер" />
      </div>
      <div className="s-note">
        Плюс предельная простота: двумерный массив без всяких структур. Для
        плотных графов, где рёбер много, это честный выбор.
      </div>
    </Slide>
  );
}

function S09() {
  const rows = [
    ["A", "B, C"],
    ["B", "A, C"],
    ["C", "A, B, D"],
    ["D", "C"],
  ];
  return (
    <Slide
      n={9}
      title="Списки смежности"
      sub="Для каждой вершины — список её соседей"
      main="Для разреженных графов списки — радикальная экономия памяти."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="n + 2|E|"
          sub="память пропорциональна рёбрам: соцсеть с миллиардом помещается"
        />
        <Node
          mono
          kind="amber"
          title="n²"
          sub="матрица потребовала бы квадриллион ячеек"
        />
      </div>
      <div className="s-note">
        Цена: «дружат ли эти двое?» — придётся просматривать список. Зато
        главная операция обхода — «перечисли соседей» — делается без возни с
        пустыми ячейками.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Матрица или списки"
      sub="Выбор сводится к двум вопросам"
      main="Реальные графы разрежены, а ходить по ним приходится непрерывно — практика почти всегда на стороне списков."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">МАТРИЦА</div>
          <span className="s-node-title">Плотные графы</span>
          <span className="s-node-sub">
            Квадрат от n окупается частыми точечными проверками за O(1)
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">СПИСКИ</div>
          <span className="s-node-title">Разреженные графы</span>
          <span className="s-node-sub">
            Память по числу рёбер, соседи перечисляются без возни
          </span>
        </div>
      </div>
      <div className="s-opts">
        <span className="s-path accent">граф плотный?</span>
        <span>склон к матрице</span>
        <span className="s-path accent">горячая операция?</span>
        <span>проверки ребра — матрица, перебор соседей — списки</span>
      </div>
      <div className="s-note">
        Матрица выигрывает в нишах: маленькие плотные графы и точечные
        проверки.
      </div>
    </Slide>
  );
}

function S11() {
  const rows = [
    ["deg⁺ A = 2 · deg⁻ A = 0", "источник: только стрелки наружу"],
    ["deg⁺ B = 1 · deg⁻ B = 1", "транзит: входит и выходит"],
    ["deg⁺ C = 0 · deg⁻ C = 2", "сток: популярная страница, на неё ссылаются"],
  ];
  return (
    <Slide
      n={11}
      title="Степени в орграфе"
      sub="Исходящая и входящая"
      main="Каждая стрелка выходит один раз и входит один раз — поэтому обе суммы равны числу рёбер."
    >
      <div className="s-cols">
        <Node mono title="A" />
        <Arr />
        <Node mono title="B" />
        <Arr />
        <Node mono title="C" />
      </div>
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <Cmd>{"Σ deg⁺ = Σ deg⁻ = |E| = 3"}</Cmd>
      <div className="s-note">
        Когда-то именно подсчёт входящих стрелок — кто на какое число ссылок
        заслуживает — породил целые поисковые системы.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Циклы и топопорядок"
      sub="В зависимостях цикл — синоним беды"
      main="Граф без циклов выстраивается так, что каждая стрелка ведёт от более ранней вершины к более поздней."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">ЦИКЛ</div>
          <div className="s-cols">
            <Node mono kind="amber" title="a" />
            <Arr />
            <Node mono kind="amber" title="b" />
            <Arr />
            <Node mono kind="amber" title="c" />
            <Arr />
            <Node mono kind="amber" title="a" />
          </div>
          <span className="s-node-sub">Ни один из трёх нельзя установить первым</span>
        </div>
        <div className="s-card">
          <div className="s-label">БЕЗ ЦИКЛОВ</div>
          <div className="s-cols">
            <Node mono kind="green" title="a" />
            <Arr />
            <Node mono title="b" />
            <Arr />
            <Node mono title="c" />
          </div>
          <span className="s-node-sub">a → b → c — топологический порядок</span>
        </div>
      </div>
      <div className="s-note">
        Именно этот порядок строит менеджер пакетов перед установкой. Проверка
        на циклы и построение порядка — задачи главы про обходы.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["V·E", "Вершины и рёбра", "Экономная модель дом-деревьев, зависимостей и маршрутов"],
    ["Σdeg", "Рукопожатия", "Сумма степеней = 2 · число рёбер; нечётных вершин чётно"],
    ["→", "Путь, цикл, связность", "Цикл в зависимостях — порядка установки нет"],
    ["[·]", "Хранение", "Списки для разреженного мира, матрица для плотного"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 8 · Графы и вероятность"
      main="Граф — вершины и рёбра; всё остальное — производные вопросы о связях."
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
        Следующая глава — ходьба по графам: глубина, ширина, деревья и
        кёнигсбергские мосты.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_M8 = {
  "12:8": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_M8).
export const SLIDE_TITLES_M8 = {
  "12:8": [
    "Графы повсюду",
    "Что такое граф",
    "Направление рёбер",
    "Лемма о рукопожатиях",
    "Пути и циклы",
    "Компоненты связности",
    "Три графа из жизни",
    "Матрица смежности",
    "Списки смежности",
    "Матрица или списки",
    "Степени в орграфе",
    "Циклы и топопорядок",
    "Итог",
  ],
};
