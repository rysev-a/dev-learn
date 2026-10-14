// Слайды для «Дискретной математики», глава 9 — «Обходы графов и деревья».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ДИСКРЕТНАЯ МАТЕМАТИКА / ГРАФЫ И ВЕРОЯТНОСТЬ / ГЛАВА 9</span>
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
    ["DFS", "Обход в глубину", "Стек и нитка в лабиринте: идти до упора"],
    ["BFS", "Обход в ширину", "Очередь и волна: кратчайшие пути без весов"],
    ["n−1", "Деревья и остовы", "Связный граф без циклов и его скелет"],
    ["deg", "Мосты Кёнигсберга", "Эйлеров путь и нечётные степени"],
  ];
  return (
    <Slide
      n={1}
      title="Обходы графов и деревья"
      sub="Глава 9 · Графы и вероятность"
      main="Обход — побывать во всех достижимых вершинах и не зациклиться."
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
        Пока вы спите, графы обходят сборщик мусора, краулер и менеджер
        пакетов — всё это вы встретите в продакшне, узнав в лицо.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Постановка задачи"
      sub="Дан граф и стартовая вершина"
      main="Каждую достижимую вершину — ровно один раз; от циклов спасает память."
    >
      <div className="s-opts">
        <span className="s-path accent">дано</span>
        <span>граф и стартовая вершина</span>
        <span className="s-path accent">найти</span>
        <span>всё, что из неё достижимо</span>
      </div>
      <div className="s-cols">
        <Node
          title="Способ выбирать следующую"
          sub="стек или очередь — сердце алгоритма"
        />
        <Node
          kind="green"
          title="Множество посещённых"
          sub="заглядываем перед каждым шагом"
        />
      </div>
      <div className="s-note amber">
        Без памяти обход вечно кружит по одному кольцу, как гость без карты в
        квартире-лабиринте.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Обход в глубину"
      sub="DFS: маршрут по лабиринту с ниткой"
      main="Иди вперёд, пока можно; упёрся — отступай на шаг назад и пробуй другую дверь."
    >
      <div className="s-cols">
        <Node mono title="A" />
        <Arr />
        <Node mono title="B" />
        <Arr />
        <Node mono title="C" />
        <Arr />
        <Node mono kind="amber" title="тупик" />
      </div>
      <div className="s-label">СТЕК</div>
      <div className="s-blocks">
        <div className="s-block changed">C — верх стека: где мы находимся</div>
        <div className="s-block">B — ждёт под верхним</div>
        <div className="s-block">A — старт</div>
      </div>
      <div className="s-note">
        Тупик — снимаем вершину со стека и пробуем другую дверь. Нитка в
        лабиринте — это и есть стек: она помнит, откуда вы пришли.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Рекурсия — это стек"
      sub="Готовый стек, встроенный в язык даром"
      main="Любая рекурсивная функция, гуляющая по вложенной структуре, — обход в глубину."
    >
      <Cmd>
        {
          "visit(v):\n  пометить v посещённой\n  для каждого соседа u:\n    если u не посещена — visit(u)"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Дом-дерево"
          sub="рекурсивно спускаемся к детям внутри каждого узла"
        />
        <Node
          title="Каталоги"
          sub="папка — рекурсивный вызов, файл — лист"
        />
      </div>
      <div className="s-note">
        Стек вызовов сам помнит обратный путь — даже если вы никогда не
        называли это обходом в глубину.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Обход в ширину"
      sub="BFS: сначала все ближние, потом дальние"
      main="Волна расходится кругами по воде; вместо стека — очередь."
    >
      <div className="s-cols">
        <Node mono kind="green" title="S · круг 0" />
        <Arr />
        <Node mono title="соседи · круг 1" />
        <Arr />
        <Node mono title="дальние · круг 2" />
      </div>
      <div className="s-label">ОЧЕРЕДЬ</div>
      <div className="s-blocks">
        <div className="s-block changed">
          голова: A — вынимаем и обрабатываем
        </div>
        <div className="s-block">
          хвост: B · C · D — добавляем непосещённых соседей в конец
        </div>
      </div>
      <div className="s-note">
        Первым пришёл — первым ушёл: порядок гарантирует обработку по кругам
        удалённости. Стек и очередь — единственная разница в коде, а поведение
        алгоритмов меняется радикально.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Кратчайшие пути волной"
      sub="Бесплатный бонус очереди"
      main="В графе без весов обход в ширину находит кратчайшие пути."
    >
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="расстояние 1"
          sub="все варианты на одном ребре проверены первыми"
        />
        <Node
          mono
          title="расстояние 2"
          sub="потом все варианты на двух рёбрах"
        />
      </div>
      <div className="s-grid2">
        <Node
          title="Соцсети"
          sub="«друзья друзей»: люди ровно на расстоянии два-три рукопожатия"
        />
        <Node
          title="Лабиринт"
          sub="выведет к выходу по самому короткому маршруту"
        />
      </div>
      <div className="s-note">
        Глубина же может утащить вас длинным, но первым попавшимся коридором.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Компоненты связности"
      sub="Утилитарная классика: посчитать острова"
      main="Каждый запуск обхода вычерпывает ровно одну компоненту; число запусков — число островов."
    >
      <Cmd>
        {
          "для каждой вершины v:\n  если v не посещена:\n    запуск(v) — вычерпана ещё одна компонента"
        }
      </Cmd>
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">ЗАПУСК 1</div>
          <div className="s-cols">
            <Node mono title="A" />
            <Edge />
            <Node mono title="B" />
            <Edge />
            <Node mono title="C" />
          </div>
        </div>
        <div className="s-card">
          <div className="s-label">ЗАПУСК 2</div>
          <div className="s-cols">
            <Node mono title="X" />
            <Edge />
            <Node mono title="Y" />
          </div>
        </div>
      </div>
      <div className="s-note">
        Глубина и ширина здесь взаимозаменяемы — важен лишь факт полного
        вычерпывания.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Дерево и формула n − 1"
      sub="Связный граф без циклов"
      main="Путь между любыми двумя вершинами ровно один — заблудиться невозможно."
    >
      <div className="s-tree">
        <div className="s-cols">
          <Node mono kind="green" title="корень" />
        </div>
        <Down />
        <div className="s-cols">
          <Node mono title="ребёнок" />
          <Node mono title="ребёнок" />
        </div>
        <Down />
        <div className="s-cols">
          <Node mono title="лист" />
          <Node mono title="лист" />
          <Node mono title="лист" />
        </div>
      </div>
      <Cmd>{"вершин n → рёбер ровно n − 1\nздесь: 6 вершин и 5 рёбер"}</Cmd>
      <div className="s-note">
        Проверьте: одна вершина — ноль рёбер, три цепочкой — два ребра.
        Формула работает в обе стороны: добавите ребро — родится цикл,
        уберёте — развалится на куски.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Деревья вокруг нас"
      sub="Самая частая форма графов в разработке"
      main="Идеальная среда для рекурсии: база на листьях, переход на детях."
    >
      <div className="s-grid2">
        <Node
          title="Файловая система"
          sub="папка-корень, у каждого ровно один родитель"
        />
        <Node
          title="Синтаксическое дерево"
          sub="компилятор разбирает программу в дерево выражений"
        />
        <Node title="DOM браузера" sub="разметка превращается в дерево узлов" />
        <Node
          title="Иерархии"
          sub="компания и категории товаров устроены так же"
        />
      </div>
      <div className="s-note">
        Не случайно почти вся рекурсия из прошлых глав тренировалась именно на
        деревьях.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Остовное дерево"
      sub="Выжать из графа скелет"
      main="Оставить ровно n − 1 ребро так, чтобы связность сохранилась."
    >
      <div className="s-cols">
        <Node
          title="Дан связный граф"
          sub="сеть районов и дороги-кандидаты с лишними рёбрами"
        />
        <Arr />
        <Node
          kind="green"
          title="Остов: n − 1 ребро"
          sub="скелет сети: связно и без циклов"
        />
      </div>
      <div className="s-grid2">
        <Node mono title="без цен" sub="подойдёт любой скелет" />
        <Node
          mono
          kind="amber"
          title="с ценами"
          sub="минимальное остовное — самый дешёвый способ связать всех"
        />
      </div>
      <div className="s-note">
        Прокладка кабелей между серверами, объединение офисов сетью,
        кластеризация точек на карте.
      </div>
    </Slide>
  );
}

function S11() {
  const rows = [
    ["берег A", "deg 3 · нечётная"],
    ["берег B", "deg 3 · нечётная"],
    ["остров C", "deg 5 · нечётная"],
    ["остров D", "deg 3 · нечётная"],
  ];
  return (
    <Slide
      n={11}
      title="Мосты Кёнигсберга"
      sub="Старейшая задача теории графов"
      main="Эйлеров путь существует, только если нечётных вершин ноль или две."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span className="amber-text">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-cols">
        <Node mono kind="green" title="0 нечётных" sub="эйлеров цикл: замыкается в круг" />
        <Node mono title="2 нечётных" sub="путь: старт и финиш в разных местах" />
        <Node mono kind="amber" title="4 нечётных" sub="Кёнигсберг: прогулка невозможна" />
      </div>
      <div className="s-note">
        Каждый заход в вершину тратит два ребра — войти и выйти, поэтому
        нечётные степени могут быть лишь у старта и финиша. Прогулка оказалась
        невозможна, а теория графов родилась.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Обходы в продакшне"
      sub="Одна пара алгоритмов, много декораций"
      main="Сборщик мусора, резолвер зависимостей и краулер — это DFS и BFS со сменой декораций."
    >
      <div className="s-grid2">
        <Node
          mono
          title="Сборщик мусора"
          sub="от корневых ссылок: достижимо — живо, остальное — мусор"
        />
        <Node
          mono
          title="Резолвер зависимостей"
          sub="обход в глубину, серое состояние узла ловит цикл"
        />
        <Node
          mono
          title="Краулер"
          sub="обход в ширину с множеством посещённых адресов"
        />
        <Node
          mono
          title="Права доступа"
          sub="проверка достижимости — тот же обход"
        />
      </div>
      <div className="s-note">
        Кратчайший путь в игре и обход дом-дерева в тестах — одна и та же пара
        алгоритмов.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["DFS", "В глубину", "Стек и рекурсия: до упора вперёд, от тупика назад"],
    ["BFS", "В ширину", "Очередь и волна: кратчайшие пути без весов"],
    ["n−1", "Дерево", "Связный граф без циклов — форма ФС, AST и DOM"],
    ["deg", "Мосты Эйлера", "Нечётных вершин ноль или две — путь существует"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 9 · Графы и вероятность"
      main="Множество посещённых защищает от циклов, повторные запуски вычерпывают компоненты."
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
        Следующая, финальная глава — неуверенность: вероятность и Байес,
        который правит спам-фильтрами.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_M9 = {
  "12:9": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_M9).
export const SLIDE_TITLES_M9 = {
  "12:9": [
    "Обходы вокруг нас",
    "Постановка задачи",
    "Обход в глубину",
    "Рекурсия — это стек",
    "Обход в ширину",
    "Кратчайшие пути волной",
    "Компоненты связности",
    "Дерево и формула n − 1",
    "Деревья вокруг нас",
    "Остовное дерево",
    "Мосты Кёнигсберга",
    "Обходы в продакшне",
    "Итог",
  ],
};
